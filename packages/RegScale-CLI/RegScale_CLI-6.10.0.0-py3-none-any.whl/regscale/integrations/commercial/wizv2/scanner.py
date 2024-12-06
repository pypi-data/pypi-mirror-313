"""Module for Wiz vulnerability scanning integration."""

import datetime
import json
import logging
import os
import re
from typing import Any, Dict, Iterator, List, Optional

from regscale.core.app.utils.app_utils import check_file_path, get_current_datetime
from regscale.core.utils import get_base_protocol_from_port
from regscale.integrations.commercial.wizv2.constants import (
    VULNERABILITY_QUERY,
    INVENTORY_QUERY,
    INVENTORY_FILE_PATH,
    get_wiz_vulnerability_queries,
    WizVulnerabilityType,
)
from regscale.integrations.commercial.wizv2.parsers import (
    collect_components_to_create,
    fetch_wiz_data,
    get_disk_storage,
    get_ip_address_from_props,
    get_latest_version,
    get_network_info,
    get_product_ids,
    get_software_name_from_cpe,
    handle_provider,
    handle_software_version,
    pull_resource_info_from_props,
    handle_container_image_version,
)
from regscale.integrations.commercial.wizv2.utils import (
    create_asset_type,
    map_category,
    handle_management_type,
    get_notes_from_wiz_props,
)
from regscale.integrations.commercial.wizv2.variables import WizVariables
from regscale.integrations.commercial.wizv2.wiz_auth import wiz_authenticate
from regscale.integrations.scanner_integration import IntegrationAsset, IntegrationFinding, ScannerIntegration
from regscale.integrations.variables import ScannerVariables
from regscale.models import regscale_models, IssueStatus

logger = logging.getLogger("rich")


class WizVulnerabilityIntegration(ScannerIntegration):
    """Integration class for Wiz vulnerability scanning."""

    title = "Wiz"
    asset_identifier_field = "wizId"
    finding_severity_map = {
        "Critical": regscale_models.IssueSeverity.High,
        "High": regscale_models.IssueSeverity.High,
        "Medium": regscale_models.IssueSeverity.Moderate,
        "Low": regscale_models.IssueSeverity.Low,
    }
    asset_lookup = "vulnerableAsset"
    wiz_token = None

    @staticmethod
    def get_variables():
        return {
            "first": 100,
            "filterBy": {},
        }

    def authenticate(self, client_id: Optional[str] = None, client_secret: Optional[str] = None) -> None:
        """
        Authenticates to Wiz using the client ID and client secret

        :param Optional[str] client_id: Wiz client ID
        :param Optional[str] client_secret: WiZ client secret
        :rtype: None
        """
        client_id = client_id or WizVariables.wizClientId
        client_secret = client_secret or WizVariables.wizClientSecret
        logger.info("Authenticating to Wiz...")
        self.wiz_token = wiz_authenticate(client_id, client_secret)

    def get_query_types(self):
        return get_wiz_vulnerability_queries(project_id=self.plan_id)

    def fetch_findings(self, *args, **kwargs) -> Iterator[IntegrationFinding]:
        """
        Fetches Wiz findings using the GraphQL API

        :yield: IntegrationFinding objects
        :rtype: Iterator[IntegrationFinding]
        """
        self.authenticate(kwargs.get("client_id"), kwargs.get("client_secret"))
        project_id = kwargs.get("wiz_project_id")
        if not project_id:
            raise ValueError("Wiz project ID is required")

        logger.info("Fetching Wiz findings...")

        for wiz_vulnerability_type in get_wiz_vulnerability_queries(project_id=project_id):
            logger.info("Fetching Wiz findings for %s...", wiz_vulnerability_type["type"])
            variables = self.get_variables()
            variables["filterBy"]["projectId"] = [project_id]

            nodes = self.fetch_wiz_data_if_needed(
                query=VULNERABILITY_QUERY,
                variables=variables,
                topic_key=wiz_vulnerability_type["topic_key"],
                file_path=wiz_vulnerability_type["file_path"],
            )
            yield from self.parse_findings(nodes, wiz_vulnerability_type["type"])

        logger.info("Finished fetching Wiz findings.")

    def parse_findings(
        self, nodes: List[Dict[str, Any]], vulnerability_type: WizVulnerabilityType
    ) -> Iterator[IntegrationFinding]:
        """
        Parses a list of Wiz finding nodes into IntegrationFinding objects.

        :param List[Dict[str, Any]] nodes: List of Wiz finding nodes
        :param WizVulnerabilityType vulnerability_type: The type of vulnerability
        :yield: IntegrationFinding objects
        :rtype: Iterator[IntegrationFinding]
        """
        for node in nodes:
            finding = self.parse_finding(node, vulnerability_type)
            if finding:
                yield finding

    @classmethod
    def get_issue_severity(cls, severity: str) -> regscale_models.IssueSeverity:
        """
        Get the issue severity from the Wiz severity

        :param str severity: The severity of the vulnerability
        :return: The issue severity
        :rtype: regscale_models.IssueSeverity
        """
        return cls.finding_severity_map.get(severity.capitalize(), regscale_models.IssueSeverity.Low)

    def parse_finding(
        self, node: Dict[str, Any], vulnerability_type: WizVulnerabilityType
    ) -> Optional[IntegrationFinding]:
        """
        Parses a Wiz finding node into an IntegrationFinding object

        :param Dict[str, Any] node: The Wiz finding node to parse
        :param WizVulnerabilityType vulnerability_type: The type of vulnerability
        :return: The parsed IntegrationFinding or None if parsing fails
        :rtype: Optional[IntegrationFinding]
        """
        try:
            asset_id = node.get(self.asset_lookup, {}).get("id")
            if not asset_id:
                return None

            severity = self.get_issue_severity(node.get("severity", "Low"))

            status = self.map_status_to_issue_status(node.get("status", "Open"))
            name: str = node.get("name", "")
            cve = (
                name
                if name and (name.startswith("CVE") or name.startswith("GHSA")) and not node.get("cve")
                else node.get("cve")
            )

            return IntegrationFinding(
                control_labels=[],
                category="Wiz Vulnerability",
                title=node.get("name", "Unknown vulnerability"),
                description=node.get("description", ""),
                severity=severity,
                status=status,
                asset_identifier=asset_id,
                external_id=f"{node.get('sourceRule', {'id': cve}).get('id')}",
                first_seen=node.get("firstDetectedAt") or node.get("firstSeenAt") or get_current_datetime(),
                last_seen=node.get("lastDetectedAt") or node.get("analyzedAt") or get_current_datetime(),
                remediation=node.get("description", ""),
                cvss_score=node.get("score"),
                cve=cve,
                plugin_name=cve,
                cvs_sv3_base_score=node.get("score"),
                source_rule_id=node.get("sourceRule", {}).get("id"),
                vulnerability_type=vulnerability_type.value,
            )
        except (KeyError, TypeError, ValueError) as e:
            logger.error("Error parsing Wiz finding: %s", str(e), exc_info=True)
            return None

    @staticmethod
    def map_status_to_issue_status(status: str) -> IssueStatus:
        """
        Maps the Wiz status to issue status
        :param str status: Status of the vulnerability
        :returns: Issue status
        :rtype: str
        """
        status_lower = status.lower()
        if status_lower == "open":
            return IssueStatus.Open
        elif status_lower in ["resolved", "rejected"]:
            return IssueStatus.Closed
        return IssueStatus.Open

    def fetch_assets(self, *args, **kwargs) -> Iterator[IntegrationAsset]:
        """
        Fetches Wiz assets using the GraphQL API

        :yields: Iterator[IntegrationAsset]
        """
        self.authenticate(kwargs.get("client_id"), kwargs.get("client_secret"))
        wiz_project_id = kwargs.get("wiz_project_id")
        logger.info("Fetching Wiz assets...")
        filter_by_override = kwargs.get("filter_by_override") or WizVariables.wizInventoryFilterBy
        filter_by = self.get_filter_by(filter_by_override, wiz_project_id)

        variables = self.get_variables()
        variables["filterBy"].update(filter_by)

        nodes = self.fetch_wiz_data_if_needed(
            query=INVENTORY_QUERY, variables=variables, topic_key="cloudResources", file_path=INVENTORY_FILE_PATH
        )
        logger.info("Fetched %d Wiz assets.", len(nodes))
        self.num_assets_to_process = len(nodes)

        for node in nodes:
            asset = self.parse_asset(node)
            if asset:
                yield asset

    @staticmethod
    def get_filter_by(filter_by_override, wiz_project_id):
        if filter_by_override:
            return json.loads(filter_by_override) if isinstance(filter_by_override, str) else filter_by_override
        filter_by = {"project": wiz_project_id}
        if WizVariables.wizLastInventoryPull and not WizVariables.wizFullPullLimitHours:
            filter_by["updatedAt"] = {"after": WizVariables.wizLastInventoryPull}
        return filter_by

    def parse_asset(self, node: Dict[str, Any]) -> Optional[IntegrationAsset]:
        """
        Parses Wiz assets

        :param Dict[str, Any] node: The Wiz asset to parse
        :return: The parsed IntegrationAsset
        :rtype: Optional[IntegrationAsset]
        """
        name = node.get("name", "")
        wiz_entity = node.get("graphEntity", {})
        if not wiz_entity:
            logger.warning("No graph entity found for asset %s", name)
            return None

        wiz_entity_properties = wiz_entity.get("properties", {})
        network_dict = get_network_info(wiz_entity_properties)
        handle_provider_dict = handle_provider(wiz_entity_properties)
        software_name_dict = get_software_name_from_cpe(wiz_entity_properties, name)
        software_list = self.create_name_version_dict(wiz_entity_properties.get("installedPackages", []))

        ports_and_protocols = self.get_ports_and_protocols(wiz_entity_properties)

        if node.get("type", "") == "CONTAINER_IMAGE":
            software_version = handle_container_image_version(
                image_tags=wiz_entity_properties.get("imageTags", []), name=name
            )
            software_name = name.split(":")[0].split("/")[-1] if name else ""
            software_vendor = name.split(":")[0].split("/")[1] if len(name.split(":")[0].split("/")) > 1 else None
        else:
            software_version = self.get_software_version(wiz_entity_properties, node)
            software_name = self.get_software_name(software_name_dict, wiz_entity_properties, node)
            software_vendor = self.get_software_vendor(software_name_dict, wiz_entity_properties, node)

        return IntegrationAsset(
            name=name,
            external_id=node.get("name"),
            asset_tag_number=node.get("subscriptionExternalId"),
            other_tracking_number=node.get("subscriptionExternalId"),
            identifier=node.get("id", ""),
            asset_type=create_asset_type(node.get("type", "")),
            asset_owner_id=ScannerVariables.userId,
            parent_id=self.plan_id,
            parent_module=regscale_models.SecurityPlan.get_module_slug(),
            asset_category=map_category(node.get("type", "")),
            date_last_updated=wiz_entity.get("lastSeen", ""),
            management_type=handle_management_type(wiz_entity_properties),
            status=self.map_wiz_status(wiz_entity_properties.get("status")),
            ip_address=get_ip_address_from_props(wiz_entity_properties),
            software_vendor=software_vendor,
            software_version=software_version,
            software_name=software_name,
            location=wiz_entity_properties.get("region"),
            notes=get_notes_from_wiz_props(wiz_entity_properties, node.get("id", "")),
            model=wiz_entity_properties.get("nativeType"),
            manufacturer=wiz_entity_properties.get("cloudPlatform"),
            serial_number=get_product_ids(wiz_entity_properties),
            is_public_facing=wiz_entity_properties.get("directlyInternetFacing", False),
            azure_identifier=handle_provider_dict.get("azureIdentifier"),
            mac_address=wiz_entity_properties.get("macAddress"),
            fqdn=wiz_entity_properties.get("dnsName") or network_dict.get("dns"),
            disk_storage=get_disk_storage(wiz_entity_properties) or 0,
            cpu=pull_resource_info_from_props(wiz_entity_properties)[1] or 0,
            ram=pull_resource_info_from_props(wiz_entity_properties)[0] or 0,
            operating_system=wiz_entity_properties.get("operatingSystem"),
            os_version=wiz_entity_properties.get("version"),
            end_of_life_date=wiz_entity_properties.get("versionEndOfLifeDate"),
            vlan_id=wiz_entity_properties.get("zone"),
            uri=network_dict.get("url"),
            aws_identifier=handle_provider_dict.get("awsIdentifier"),
            google_identifier=handle_provider_dict.get("googleIdentifier"),
            other_cloud_identifier=handle_provider_dict.get("otherCloudIdentifier"),
            patch_level=get_latest_version(wiz_entity_properties),
            cpe=wiz_entity_properties.get("cpe"),
            component_names=collect_components_to_create([node], []),
            source_data=node,
            url=wiz_entity_properties.get("cloudProviderURL"),
            ports_and_protocols=ports_and_protocols,
            software_inventory=software_list,
        )

    @staticmethod
    def get_ports_and_protocols(wiz_entity_properties):
        start_port = wiz_entity_properties.get("portStart")
        if start_port:
            end_port = wiz_entity_properties.get("portEnd") or start_port
            protocol = wiz_entity_properties.get("protocols", wiz_entity_properties.get("protocol"))
            if protocol in ["other", None]:
                protocol = get_base_protocol_from_port(start_port)
            return [{"start_port": start_port, "end_port": end_port, "protocol": protocol}]
        return []

    @staticmethod
    def get_software_vendor(software_name_dict, wiz_entity_properties, node):
        if map_category(node.get("type")) == regscale_models.AssetCategory.Software:
            return software_name_dict.get("software_vendor") or wiz_entity_properties.get("cloudPlatform")
        return None

    @staticmethod
    def get_software_version(wiz_entity_properties, node):
        if map_category(node.get("type")) == regscale_models.AssetCategory.Software:
            return handle_software_version(wiz_entity_properties, map_category(node.get("type"))) or "1.0"
        return None

    @staticmethod
    def get_software_name(software_name_dict, wiz_entity_properties, node):
        if map_category(node.get("type")) == regscale_models.AssetCategory.Software:
            return software_name_dict.get("software_name") or wiz_entity_properties.get("nativeType")
        return None

    @staticmethod
    def create_name_version_dict(package_list: List[str]) -> List[Dict[str, str]]:
        """
        Creates a dictionary of package names and their versions from a list of strings in the format "name (version)".

        :param List[str] package_list: A list of strings containing package names and versions.
        :return Dict[str, str]: A dictionary with package names as keys and versions as values.
        """
        software_inventory = []
        for package in package_list:
            match = re.match(r"(.+?) \((.+?)\)", package)
            if match:
                name, version = match.groups()
                software_inventory.append({"name": name, "version": version})
        return software_inventory

    @staticmethod
    def map_wiz_status(wiz_status: Optional[str]) -> str:
        """Map Wiz status to RegScale status."""
        return "Active (On Network)" if wiz_status != "Inactive" else "Off-Network"

    @staticmethod
    def fetch_wiz_data_if_needed(query: str, variables: Dict, topic_key: str, file_path: str) -> List[Dict]:
        """
        Fetch Wiz data if needed and save to file if not already fetched within the last 8 hours and return the data

        :param str query: GraphQL query string
        :param Dict variables: Query variables
        :param str topic_key: The key for the data in the response
        :param str file_path: Path to save the fetched data
        :return: List of nodes as dictionaries
        :rtype: List[Dict]
        """
        fetch_interval = datetime.timedelta(hours=WizVariables.wizFullPullLimitHours or 8)  # Interval to fetch new data
        current_time = datetime.datetime.now()
        check_file_path(os.path.dirname(file_path))

        if os.path.exists(file_path):
            file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if current_time - file_mod_time < fetch_interval:
                logger.info("File %s is newer than %s hours. Using cached data...", file_path, fetch_interval)
                with open(file_path, "r", encoding="utf-8") as file:
                    return json.load(file)
            else:
                logger.info("File %s is older than %s hours. Fetching new data...", file_path, fetch_interval)
        else:
            logger.info("File %s does not exist. Fetching new data...", file_path)

        nodes = fetch_wiz_data(
            query=query,
            variables=variables,
            api_endpoint_url=WizVariables.wizUrl,
            token=WizVariables.wizAccessToken,
            topic_key=topic_key,
        )
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(nodes, file)

        return nodes
