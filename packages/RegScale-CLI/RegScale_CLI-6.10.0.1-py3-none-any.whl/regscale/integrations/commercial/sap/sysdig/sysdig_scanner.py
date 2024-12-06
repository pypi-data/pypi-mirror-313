import csv
import logging
from typing import Any, Dict, Iterator, Tuple

from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.core.app.utils.parser_utils import safe_datetime_str, safe_float
from regscale.integrations.scanner_integration import (
    IntegrationAsset,
    IntegrationFinding,
    ScannerIntegration,
    issue_due_date,
)
from regscale.integrations.variables import ScannerVariables
from regscale.models import regscale_models

logger = logging.getLogger("rich")


class SAPConcurSysDigScanner(ScannerIntegration):
    title = "SAP Concur - SysDig"
    asset_identifier_field = "name"
    finding_severity_map = {
        "critical": regscale_models.IssueSeverity.High,
        "high": regscale_models.IssueSeverity.High,
        "medium": regscale_models.IssueSeverity.Moderate,
        "low": regscale_models.IssueSeverity.Low,
    }

    def parse_assets(self, asset: Dict[str, Any]) -> IntegrationAsset:
        """
        Parse a single asset from the vulnerability data.

        :param Dict[str, Any] asset: A dictionary containing the asset data
        :return: An IntegrationAsset object with parsed data
        :rtype: IntegrationAsset
        """
        name = (
            asset.get("Image name", None) + ":" + asset.get("Image tag", None)
            if (asset.get("Image name") and asset.get("Image tag"))
            else None
        )
        return IntegrationAsset(
            name=name,
            identifier=name
            or asset.get("Container name")
            or asset.get("Cluster name")
            or asset.get("Pod")
            or asset.get("Namespace"),
            asset_type="Other",  # Sysdig primarily concerns itself with containers
            asset_category=regscale_models.AssetCategory.Hardware,
            asset_owner_id=ScannerVariables.userId,
            status="Active (On Network)",
            mac_address="",
            fqdn="",
            ip_address="",
            operating_system="",
            aws_identifier="",
            vlan_id="",
            location="",
            software_inventory=[],
        )

    def fetch_assets(self, *args: Tuple, **kwargs: dict) -> Iterator[IntegrationAsset]:
        """
        Fetch assets from a CSV file and yield IntegrationAsset objects.

        :param Tuple args: Variable length argument list
        :param dict kwargs: Arbitrary keyword arguments
        :return: An iterator of IntegrationAsset objects
        :rtype: Iterator[IntegrationAsset]
        """
        path: str = kwargs.get("path", "")
        if not path:
            raise ValueError("Path is required")

        logger.info(f"Fetching assets from {path}")
        with open(path, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield self.parse_assets(row)

    def fetch_findings(self, *args: Tuple, **kwargs: dict) -> Iterator[IntegrationFinding]:
        """
        Fetch findings from a CSV file and yield IntegrationFinding objects.

        :param Tuple args: Variable length argument list
        :param dict kwargs: Arbitrary keyword arguments
        :return: An iterator of IntegrationFinding objects
        :rtype: Iterator[IntegrationFinding]
        """
        path: str = kwargs.get("path", "")
        if not path:
            raise ValueError("Path is required")

        logger.info(f"Fetching findings from {path}")

        with open(path, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield from self.parse_findings(finding=row, kwargs=kwargs)

    def parse_findings(self, finding: Dict[str, Any], **kwargs: dict) -> Iterator[IntegrationFinding]:
        """
        Parse a single finding from the vulnerability data.

        :param Dict[str, Any] finding: A dictionary containing the finding data
        :param dict kwargs: Arbitrary keyword arguments
        :return: An iterator of IntegrationFinding objects
        :rtype: Iterator[IntegrationFinding]
        """
        severity = self.finding_severity_map.get(finding["Severity"].lower(), regscale_models.IssueSeverity.Low)
        cves = finding.get("Vulnerability ID", "").split(",") if finding.get("Vulnerability ID") else []

        if not cves:
            # If there are no CVEs, yield a single finding without CVE information
            yield self._create_finding(finding=finding, severity=severity, kwargs=kwargs)
        else:
            # If there are CVEs, yield a finding for each CVE
            for cve in cves:
                yield self._create_finding(finding=finding, severity=severity, cve=cve.strip(), kwargs=kwargs)

    def _create_finding(
        self, finding: Dict[str, Any], severity: regscale_models.IssueSeverity, cve: str = "", **kwargs: dict
    ) -> IntegrationFinding:
        """
        Create an IntegrationFinding object from the given data.

        :param Dict[str, Any] finding: A dictionary containing the finding data
        :param regscale_models.IssueSeverity severity: The severity of the finding
        :param str cve: The CVE number (optional)
        :return: An IntegrationFinding object
        :rtype: IntegrationFinding
        """
        asset_name = (
            finding.get("Image name", None) + ":" + finding.get("Image tag", None)
            if (finding.get("Image name") and finding.get("Image tag"))
            else None
        )
        asset_id = (
            asset_name
            or finding.get("Container name")
            or finding.get("Cluster name")
            or finding.get("Pod")
            or finding.get("Namespace")
        )
        cve_description = finding.get("Cve description")
        category = "Sysdig Vulnerability: General"
        issue_type = "Vulnerability"
        scan_date = kwargs.get("scan_date", get_current_datetime())
        return IntegrationFinding(
            cvs_sv3_base_score=safe_float(finding.get("CVSS v3 base score")),
            cvss_score=safe_float(finding.get("CVSS v2 base score")),
            control_labels=[],
            category=category,
            title=cve or cve_description,
            issue_title=cve or cve_description,
            description=cve_description or cve,
            severity=severity,
            status=regscale_models.IssueStatus.Open,
            asset_identifier=asset_id,
            external_id=finding.get("pluginID", "Unknown"),
            scan_date=scan_date,
            first_seen=scan_date,
            last_seen=scan_date,
            remediation=finding.get("Vuln link", ""),
            cve=cve,
            vulnerability_type=self.title,
            plugin_id="0",
            plugin_name=cve or "",
            ip_address="",
            dns=cve,
            issue_type=issue_type,
            date_created=get_current_datetime(),
            date_last_updated=get_current_datetime(),
            gaps="",
            observations=finding.get("plugin_output", ""),
            evidence=finding.get("plugin_output", ""),
            identified_risk=finding.get("risk_factor", ""),
            impact="",
            recommendation_for_mitigation=finding.get("Vuln link", ""),
            rule_id=finding.get("pluginID"),
            rule_version=finding.get("script_version"),
            results=finding.get("plugin_output", ""),
            comments=None,
            baseline="",
            poam_comments=None,
            vulnerable_asset=asset_id,
            source_rule_id=finding.get("fname"),
            basis_for_adjustment=None,
        )
