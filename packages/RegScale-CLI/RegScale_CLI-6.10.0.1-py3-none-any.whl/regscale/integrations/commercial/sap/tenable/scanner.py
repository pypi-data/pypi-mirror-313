import csv
import logging
from typing import Any, Dict, Iterator, Tuple

from regscale.core.app.utils.parser_utils import safe_datetime_str, safe_float, safe_int
from regscale.integrations.scanner_integration import (
    IntegrationAsset,
    IntegrationFinding,
    ScannerIntegration,
    issue_due_date,
)
from regscale.models import regscale_models

logger = logging.getLogger("rich")

# Constants for repeated literals
IP_ADDRESS_ANONYMIZED = "IP Address (Anonymized)"
DNS_NAME = "DNS Name"
LAST_OBSERVED = "Last Observed"
CVSS_V3_BASE_SCORE = "CVSS V3 Base Score"


class SAPConcurScanner(ScannerIntegration):
    title = "SAP Concur"
    asset_identifier_field = "tenableId"
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
        ip_address = asset.get(IP_ADDRESS_ANONYMIZED, "")
        external_id = asset.get("Host ID") or ip_address  # Use Host ID if available, otherwise use IP address

        return IntegrationAsset(
            name=asset.get(DNS_NAME) or ip_address,
            identifier=external_id,
            asset_type="Server",
            asset_category="Infrastructure",
            status="Active (On Network)",
            date_last_updated=safe_datetime_str(asset.get(LAST_OBSERVED)),
            ip_address=ip_address,
            mac_address=asset.get("MAC Address"),
            fqdn=asset.get(DNS_NAME),
            component_names=[],
            external_id=external_id,
            software_name=asset.get("Plugin Name"),
            software_version=asset.get("Version"),
            operating_system=None,
            os_version=None,
            source_data=asset,
            url=None,
            ports_and_protocols=(
                [
                    {
                        "start_port": safe_int(asset.get("Port")),
                        "end_port": safe_int(asset.get("Port")),
                        "protocol": asset.get("Protocol"),
                    }
                ]
                if safe_int(asset.get("Port"))
                else []
            ),
            software_inventory=[],
            notes=f"NetBIOS Name: {asset.get('NetBIOS Name', '')}, Repository: {asset.get('Repository', '')}",
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
                yield from self.parse_findings(row)

    def parse_findings(self, finding: Dict[str, Any]) -> Iterator[IntegrationFinding]:
        """
        Parse a single finding from the vulnerability data.

        :param Dict[str, Any] finding: A dictionary containing the finding data
        :return: An iterator of IntegrationFinding objects
        :rtype: Iterator[IntegrationFinding]
        """
        severity = self.finding_severity_map.get(finding["Severity"].lower(), regscale_models.IssueSeverity.Low)
        cves = finding.get("CVE", "").split(",") if finding.get("CVE") else []

        if not cves:
            # If there are no CVEs, yield a single finding without CVE information
            yield self._create_finding(finding, severity)
        else:
            # If there are CVEs, yield a finding for each CVE
            for cve in cves:
                yield self._create_finding(finding, severity, cve.strip())

    def _create_finding(
        self, finding: Dict[str, Any], severity: regscale_models.IssueSeverity, cve: str = ""
    ) -> IntegrationFinding:
        """
        Create an IntegrationFinding object from the given data.

        :param Dict[str, Any] finding: A dictionary containing the finding data
        :param regscale_models.IssueSeverity severity: The severity of the finding
        :param str cve: The CVE number (optional)
        :return: An IntegrationFinding object
        :rtype: IntegrationFinding
        """
        return IntegrationFinding(
            control_labels=[],
            title=finding.get("Plugin Name"),
            category=finding.get("Family", "Unknown"),
            plugin_name=finding.get("Plugin", ""),
            severity=severity,
            description=finding.get("Description", ""),
            status=regscale_models.IssueStatus.Open,
            priority=finding.get("Vulnerability Priority Rating", "Medium"),
            first_seen=safe_datetime_str(finding.get("First Discovered")),
            last_seen=safe_datetime_str(finding.get(LAST_OBSERVED)),
            cve=cve,
            cvss_v3_score=safe_float(finding.get(CVSS_V3_BASE_SCORE)),
            cvss_v2_score=safe_float(finding.get("CVSS V2 Base Score")),
            ip_address=finding.get(IP_ADDRESS_ANONYMIZED),
            plugin_id=finding.get("Plugin"),
            dns=finding.get(DNS_NAME),
            issue_title=f"Vulnerability {finding.get('Plugin Name')} found",
            issue_type="Risk",
            date_created=safe_datetime_str(finding.get("First Discovered")),
            date_last_updated=safe_datetime_str(finding.get(LAST_OBSERVED)),
            due_date=issue_due_date(severity=severity, created_date=safe_datetime_str(finding.get("First Discovered"))),
            external_id=finding.get("Plugin"),
            gaps="",
            observations="",
            evidence=finding.get("Plugin Output", ""),
            identified_risk=finding.get("Risk Factor", ""),
            impact="",
            recommendation_for_mitigation=finding.get("Steps to Remediate", ""),
            asset_identifier=finding.get(IP_ADDRESS_ANONYMIZED, ""),
            comments=None,
            poam_comments=None,
            cci_ref=None,
            rule_id=finding.get("Plugin", ""),
            rule_version=finding.get("Version", ""),
            results="",
            baseline="",
            vulnerability_number=cve,
            oval_def="",
            scan_date=safe_datetime_str(finding.get(LAST_OBSERVED)),
            rule_id_full="",
            group_id="",
            vulnerable_asset=finding.get(IP_ADDRESS_ANONYMIZED, ""),
            remediation=finding.get("Steps to Remediate", ""),
            cvss_score=safe_float(finding.get(CVSS_V3_BASE_SCORE) or finding.get("CVSS V2 Base Score")),
            cvs_sv3_base_score=safe_float(finding.get(CVSS_V3_BASE_SCORE)),
            source_rule_id=finding.get("Plugin", ""),
            vulnerability_type=finding.get("Family", ""),
            basis_for_adjustment=None,
        )
