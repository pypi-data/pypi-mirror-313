"""
Module for Tenable vulnerability scanning integration.
"""

import datetime
import json
import linecache
import logging
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.integrations.commercial.nessus.nessus_utils import get_min_cvss_score, validate_nessus_severity
from regscale.core.utils.date import datetime_obj
from regscale.integrations.commercial.tenablev2.utils import get_last_pull_epoch
from regscale.integrations.commercial.tenablev2.authenticate import gen_tio
from regscale.integrations.commercial.tenablev2.stig_parsers import parse_stig_output
from regscale.integrations.commercial.tenablev2.variables import TenableVariables
from regscale.integrations.scanner_integration import IntegrationAsset, IntegrationFinding, ScannerIntegration
from regscale.integrations.variables import ScannerVariables
from regscale.models import regscale_models

logger = logging.getLogger("rich")


class TenableIntegration(ScannerIntegration):
    """Integration class for Tenable vulnerability scanning."""

    title: str = "Tenable"
    asset_identifier_field: str = "tenableId"
    finding_severity_map: Dict[str, regscale_models.IssueSeverity] = {
        "critical": regscale_models.IssueSeverity.High,
        "high": regscale_models.IssueSeverity.High,
        "medium": regscale_models.IssueSeverity.Moderate,
        "low": regscale_models.IssueSeverity.Low,
    }

    def __init__(self, plan_id: int, tenant_id: int = 1):
        """
        Initialize the TenableIntegration.

        :param int plan_id: The ID of the security plan
        :param int tenant_id: The ID of the tenant, defaults to 1
        """
        super().__init__(plan_id, tenant_id)
        self.client = None

    def authenticate(self) -> None:
        """Authenticate to Tenable."""
        self.client = gen_tio()

    def fetch_assets(self, *args: Any, **kwargs: Any) -> Iterator[IntegrationAsset]:
        """
        Fetches Tenable assets using the Tenable.io API

        :yields: Iterator[IntegrationAsset]
        """
        plan_id = int(kwargs.get("plan_id", self.plan_id))
        # Create artifacts directory if not exist
        Path("artifacts").mkdir(parents=True, exist_ok=True)

        cache_file = Path("artifacts") / f"tenable_assets_cache{plan_id}.json"

        if (
            cache_file.exists()
            and (datetime.datetime.now() - datetime.datetime.fromtimestamp(cache_file.stat().st_mtime)).days < 1
        ):
            logger.info("Loading assets from cache...")
        else:
            self.authenticate()
            logger.info("Fetching Tenable assets...")

            if not self.client:
                raise ValueError("Client not authenticated")

            tenable_last_updated = self.get_last_update_time()
            assets_iterator = self.client.exports.assets(updated_at=int(tenable_last_updated.timestamp()))

            i = 0
            with open(cache_file, "w") as f:
                for i, asset in enumerate(assets_iterator, 1):
                    f.write(json.dumps(asset) + "\n")
                    if i % 100 == 0:
                        logger.info(f"Fetched {i} assets")

            logger.info(f"Total assets fetched: {i}")

        # Count the number of lines in the file using linecache
        self.num_assets_to_process = len(linecache.getlines(str(cache_file)))
        logger.info(f"Total assets to process: {self.num_assets_to_process}")

        # Process the assets
        with open(cache_file, "r") as f:
            for line in f:
                asset = json.loads(line)
                parsed_asset = self.parse_asset(asset)
                yield parsed_asset

    def get_last_update_time(self) -> datetime.datetime:
        """
        Get the last update time for Tenable assets.

        :return: The last update time
        :rtype: datetime.datetime
        """
        existing_assets: List[regscale_models.Asset] = regscale_models.Asset.get_all_by_parent(
            parent_id=self.plan_id, parent_module="securityplans"
        )
        filtered_assets = [asset for asset in existing_assets if asset.tenableId and asset.dateLastUpdated]

        if not filtered_assets:
            return datetime.datetime.fromtimestamp(0)

        return max(
            datetime_obj(asset.dateLastUpdated) or datetime.datetime.fromtimestamp(0)
            for asset in filtered_assets
            if datetime_obj(asset.dateLastUpdated)
        )

    def parse_asset(self, node: Dict[str, Any]) -> IntegrationAsset:
        """
        Parses Tenable assets

        :param Dict[str, Any] node: The Tenable asset to parse
        :return: The parsed IntegrationAsset
        :rtype: IntegrationAsset
        """
        system_types = node.get("system_types", [])
        tenable_asset_type = system_types[0] if system_types else None
        asset_type = self.map_tenable_to_regscale_asset_type(tenable_asset_type)

        software_inventory = node.get("installed_software", [])
        if software_inventory and isinstance(software_inventory[0], str):
            software_inventory = [{"name": sw} for sw in software_inventory]

        return IntegrationAsset(
            name=self.get_asset_name(node),
            external_id=node.get("id", ""),
            identifier=node.get("id", ""),
            asset_type=asset_type,
            asset_owner_id=ScannerVariables.userId,
            parent_id=self.plan_id,
            parent_module=regscale_models.SecurityPlan.get_module_slug(),
            asset_category=self.map_asset_category(tenable_asset_type),
            date_last_updated=node.get("last_seen", ""),
            status=self.map_tenable_status(node.get("terminated_at")),
            ip_address=", ".join(node.get("ipv4s", []) + node.get("ipv6s", [])),
            mac_address=", ".join(self.get_all_mac_addresses(node)),
            fqdn=", ".join(node.get("fqdns", [])),
            component_names=node.get("agent_names", []),
            operating_system=", ".join(node.get("operating_systems", [])),
            serial_number=node.get("bios_uuid", ""),
            notes=self.generate_notes(node),
            source_data=node,
            software_inventory=software_inventory,
            azure_identifier=node.get("azure_vm_id") or node.get("azure_resource_id", ""),
            aws_identifier=node.get("aws_ec2_instance_id", ""),
            google_identifier=node.get("gcp_instance_id", ""),
            other_cloud_identifier=self.get_other_cloud_identifier(node),
        )

    @staticmethod
    def get_asset_name(node: Dict[str, Any]) -> str:
        """
        Get the asset name from various possible sources

        :param Dict[str, Any] node: The Tenable asset data
        :return: The asset name
        :rtype: str
        """
        for key in ["hostnames", "fqdns", "netbios_names", "ipv4s"]:
            values = node.get(key, [])
            if values and values[0]:
                return values[0]
        return "Unknown Asset"

    @staticmethod
    def get_all_mac_addresses(node: Dict[str, Any]) -> List[str]:
        """
        Get all MAC addresses from all network interfaces

        :param Dict[str, Any] node: The Tenable asset data
        :return: List of MAC addresses
        :rtype: List[str]
        """
        mac_addresses = set()
        for interface in node.get("network_interfaces", []):
            mac_addresses.update(interface.get("mac_addresses", []))
        return list(mac_addresses)

    @staticmethod
    def generate_notes(node: Dict[str, Any]) -> str:
        """
        Generate notes from Tenable asset data

        :param Dict[str, Any] node: The Tenable asset data
        :return: Generated notes
        :rtype: str
        """
        notes = []
        if node.get("network_name"):
            notes.append(f"Network: {node.get('network_name')}")
        if node.get("acr_score") is not None:
            notes.append(f"ACR Score: {node.get('acr_score')}")
        if node.get("exposure_score") is not None:
            notes.append(f"Exposure Score: {node.get('exposure_score')}")
        if node.get("tags"):
            tag_str = "; ".join([f"{tag.get('key', '')}: {tag.get('value', '')}" for tag in node.get("tags", [])])
            notes.append(f"Tags: {tag_str}")
        if node.get("sources"):
            sources_str = "; ".join(
                [
                    f"{source.get('name', '')} (First seen: {source.get('first_seen', '')}, Last seen: {source.get('last_seen', '')})"
                    for source in node.get("sources", [])
                ]
            )
            notes.append(f"Sources: {sources_str}")
        return "\n".join(notes)

    @staticmethod
    def get_other_cloud_identifier(node: Dict[str, Any]) -> Optional[str]:
        """
        Get other cloud identifier if present

        :param Dict[str, Any] node: The Tenable asset data
        :return: Other cloud identifier if present, None otherwise
        :rtype: Optional[str]
        """
        if node.get("gcp_project_id"):
            return f"GCP Project: {node.get('gcp_project_id')}"
        if node.get("aws_vpc_id"):
            return f"AWS VPC: {node.get('aws_vpc_id')}"
        return None

    @staticmethod
    def map_asset_category(tenable_type: Optional[str]) -> str:
        """
        Map Tenable asset type to RegScale asset category.

        :param Optional[str] tenable_type: The Tenable asset type
        :return: Mapped asset category (either "Software" or "Hardware")
        :rtype: regscale_models.AssetCategory
        """
        if not tenable_type:
            return regscale_models.AssetCategory.Hardware  # Default to Hardware if type is unknown

        # List of types that are typically considered software
        software_types = ["application"]

        return (
            regscale_models.AssetCategory.Software
            if tenable_type.lower() in software_types
            else regscale_models.AssetCategory.Hardware
        )

    @staticmethod
    def map_tenable_status(terminated_at: Optional[str]) -> str:
        """
        Map Tenable status to IntegrationAsset status

        :param Optional[str] terminated_at: The terminated_at value from Tenable
        :return: Mapped status
        :rtype: str
        """
        return "Off-Network" if terminated_at else "Active (On Network)"

    @staticmethod
    def map_tenable_to_regscale_asset_type(tenable_type: Optional[str]) -> regscale_models.AssetType:
        """
        Map Tenable asset type to RegScale AssetType enum.

        :param Optional[str] tenable_type: The Tenable asset type
        :return: Mapped RegScale AssetType
        :rtype: regscale_models.AssetType
        """
        if not tenable_type:
            return regscale_models.AssetType.Other

        tenable_to_regscale_map = {
            "general-purpose": regscale_models.AssetType.Desktop,
            "laptop": regscale_models.AssetType.Laptop,
            "server": regscale_models.AssetType.PhysicalServer,
            "hypervisor": regscale_models.AssetType.VM,
            "mobile": regscale_models.AssetType.Phone,
            "network": regscale_models.AssetType.NetworkRouter,
            "firewall": regscale_models.AssetType.Firewall,
            "tablet": regscale_models.AssetType.Tablet,
            "switch": regscale_models.AssetType.NetworkSwitch,
            "appliance": regscale_models.AssetType.Appliance,
        }

        return tenable_to_regscale_map.get(tenable_type.lower(), regscale_models.AssetType.Other)

    def fetch_findings(self, *args: Any, **kwargs: Any) -> Iterator[IntegrationFinding]:
        """
        Fetches Tenable findings using the Tenable.io API

        :yields: Iterator[IntegrationFinding]
        """
        plan_id = int(kwargs.get("plan_id", self.plan_id))
        Path("artifacts").mkdir(parents=True, exist_ok=True)
        cache_file = Path("artifacts") / f"tenable_findings_cache_{plan_id}.json"

        if (
            cache_file.exists()
            and (datetime.datetime.now() - datetime.datetime.fromtimestamp(cache_file.stat().st_mtime)).days < 1
        ):
            logger.info("Loading findings from cache...")
        else:
            logger.info("Fetching findings from Tenable...")
            minimum_severity = validate_nessus_severity(TenableVariables.tenableMinimumSeverityFilter)
            cvss2_min = get_min_cvss_score(minimum_severity)
            latest_scan: int = get_last_pull_epoch(regscale_ssp_id=plan_id)
            logger.info("Latest scan: %s", datetime.datetime.fromtimestamp(latest_scan))
            self.authenticate()
            if not self.client:
                raise ValueError("Client not authenticated")
            with open(cache_file, "w", encoding="utf-8") as f:
                for i, line in enumerate(
                    self.client.exports.vulns(
                        vpr_score={"gte": cvss2_min}, since=latest_scan, state=["OPEN", "REOPENED"]
                    )
                ):
                    f.write(json.dumps(line) + "\n")
                    if i % 100 == 0:
                        logger.info(f"Fetched {i} vulnerabilities")

        # Count the number of lines in the file using linecache
        self.num_findings_to_process = len(linecache.getlines(str(cache_file)))
        logger.info(f"Total findings to process: {self.num_findings_to_process}")
        with open(cache_file, "r") as f:
            for line in f:
                parsed_asset = self.parse_finding(json.loads(line))
                if parsed_asset:
                    yield parsed_asset

    def parse_finding(self, vuln: Dict[str, Any]) -> Optional[IntegrationFinding]:
        """
        Parses a Tenable vulnerability into an IntegrationFinding object.

        :param Dict[str, Any] vuln: The Tenable vulnerability to parse
        :return: The parsed IntegrationFinding or None if parsing fails
        :rtype: Optional[IntegrationFinding]
        """
        try:
            # Extract relevant data from the vulnerability dict
            asset = vuln.get("asset", {})
            plugin = vuln.get("plugin", {})
            plugin_output = vuln.get("output", "")
            is_stig = "xccdf_mil.disa.stig_rule" in plugin_output
            plugin_name = plugin.get("name", [])[0] if isinstance(plugin.get("name"), list) else plugin.get("name")

            severity = vuln.get("severity", "info").lower()
            severity_id = vuln.get("severity_id", 0)

            # Determine if this is an informational item or a vulnerability
            is_informational = severity == "info" or severity_id == 0

            if is_informational and not is_stig:
                logger.info(f"Ignoring Informational Vulnerability {plugin_name}")
                return None

            category = f"Tenable Vulnerability: {plugin.get('family', 'General')}"
            issue_type = "Vulnerability"
            severity = self.finding_severity_map.get(severity, regscale_models.IssueSeverity.Low)
            status = (
                regscale_models.IssueStatus.Open if vuln.get("state") == "OPEN" else regscale_models.IssueStatus.Closed
            )

            # Mapping for severity strings to integers
            severity_map = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}
            severity_int = severity_map.get(severity, 0)

            identifier = plugin.get("cve", []) or [plugin.get("name", "")]
            identifier = identifier[0] if isinstance(identifier, list) else identifier
            asset_id = asset.get("uuid", "")

            cve = plugin.get("cve", [])[0] if isinstance(plugin.get("cve"), list) else None

            integration_finding = IntegrationFinding(
                control_labels=[],
                category=category,
                title=f"{identifier}: {plugin.get('name', '')}",
                issue_title=f"{identifier}: {plugin.get('name', '')}",
                description=plugin.get("description", ""),
                severity=severity,
                status=status,
                asset_identifier=asset_id,
                external_id=str(plugin.get("id", "")),
                first_seen=vuln.get("first_found", get_current_datetime()),
                last_seen=vuln.get("last_found", get_current_datetime()),
                remediation=plugin.get("solution", ""),
                cvss_score=float(plugin.get("cvss3_base_score") or plugin.get("cvss_base_score") or 0),
                cve=cve,
                vulnerability_type=self.title,
                plugin_id=str(plugin.get("id", "")),
                plugin_name=plugin_name,
                ip_address=asset.get("ipv4", ""),
                dns=asset.get("fqdn", ""),
                severity_int=severity_int,
                issue_type=issue_type,
                date_created=get_current_datetime(),
                date_last_updated=get_current_datetime(),
                gaps="",
                observations=vuln.get("output", ""),
                evidence=vuln.get("output", ""),
                identified_risk=plugin.get("risk_factor", ""),
                impact="",
                recommendation_for_mitigation=plugin.get("solution", ""),
                rule_id=str(plugin.get("id", "")),
                rule_version=plugin.get("version", ""),
                results=vuln.get("output", ""),
                comments=None,
                baseline="",
                poam_comments=None,
                vulnerable_asset=asset_id,
                source_rule_id=str(plugin.get("id", "")),
            )
            if is_stig:
                integration_finding = parse_stig_output(output=plugin_output, finding=integration_finding)
            return integration_finding
        except Exception as e:
            logger.error("Error parsing Tenable finding: %s", str(e), exc_info=True)
            return None
