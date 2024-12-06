"""
This module contains the Tenable SC Integration class that is responsible for fetching assets and findings from Tenable
"""

import logging
from typing import Any, Iterator, List, Tuple

from regscale.core.app.utils.app_utils import epoch_to_datetime
from regscale.integrations.commercial.tenablev2.utils import get_filtered_severities
from regscale.integrations.scanner_integration import IntegrationAsset, IntegrationFinding, ScannerIntegration
from regscale.models import regscale_models
from regscale.models.integration_models.tenable_models.models import TenableAsset

logger = logging.getLogger(__name__)


class SCIntegration(ScannerIntegration):
    """
    Tenable SC Integration class that is responsible for fetching assets and findings from Tenable
    """

    finding_severity_map = {
        "Info": regscale_models.IssueSeverity.NotAssigned,
        "Low": regscale_models.IssueSeverity.Low,
        "Medium": regscale_models.IssueSeverity.Moderate,
        "High": regscale_models.IssueSeverity.High,
        "Critical": regscale_models.IssueSeverity.High,
    }
    # Required fields from ScannerIntegration
    title = "Tenable SC"
    asset_identifier_field = "tenableId"

    def fetch_assets(self, *args: Any, **kwargs: Any) -> Iterator[IntegrationAsset]:
        """
        Fetches assets from SCIntegration

        :param Tuple args: Additional arguments
        :param dict kwargs: Additional keyword arguments
        :yields: Iterator[IntegrationAsset]
        """
        integration_assets = kwargs.get("integration_assets")
        yield from integration_assets

    def fetch_findings(self, *args: Tuple, **kwargs: dict) -> Iterator[IntegrationFinding]:
        """
        Fetches findings from the SCIntegration

        :param Tuple args: Additional arguments
        :param dict kwargs: Additional keyword arguments
        :yields: Iterator[IntegrationFinding]

        """
        integration_findings = kwargs.get("integration_findings")
        yield from integration_findings

    from typing import List

    def parse_findings(self, vuln: TenableAsset) -> List[IntegrationFinding]:
        """
        Parses a TenableAsset into an IntegrationFinding object

        :param TenableAsset vuln: The Tenable SC finding
        :return: A list of IntegrationFinding objects
        :rtype: List[IntegrationFinding]
        """
        findings = []
        try:
            severity = self.finding_severity_map.get(vuln.severity.name, regscale_models.IssueSeverity.Low)
            cve_list = set(vuln.cve.split(",")) if vuln.cve else set()
            if severity in get_filtered_severities():
                if cve_list:
                    for cve in cve_list:
                        findings.append(self._create_finding(vuln, severity, cve))
                else:
                    findings.append(self._create_finding(vuln, severity, ""))
        except (KeyError, TypeError, ValueError) as e:
            logger.error("Error parsing Tenable SC finding: %s", str(e), exc_info=True)

        return findings

    def _create_finding(self, vuln: TenableAsset, severity: str, cve: str) -> IntegrationFinding:
        """
        Helper method to create an IntegrationFinding object

        :param TenableAsset vuln: The Tenable SC finding
        :param str severity: The severity of the finding
        :param str cve: The CVE identifier
        :return: An IntegrationFinding object
        :rtype: IntegrationFinding
        """
        return IntegrationFinding(
            control_labels=[],  # Add an empty list for control_labels
            category="Tenable SC Vulnerability",  # Add a default category
            dns=vuln.dnsName,
            title=vuln.synopsis or vuln.pluginName,  # Add CVE to title
            description=vuln.description or vuln.pluginInfo,
            severity=severity,
            status=regscale_models.IssueStatus.Open,  # Findings of > Low are considered as FAIL
            asset_identifier=vuln.dnsName or vuln.ip,
            external_id=vuln.pluginID,  # Weakness Source Identifier
            first_seen=epoch_to_datetime(vuln.firstSeen),
            last_seen=epoch_to_datetime(vuln.lastSeen),
            date_created=epoch_to_datetime(vuln.firstSeen),
            date_last_updated=epoch_to_datetime(vuln.lastSeen),
            recommendation_for_mitigation=vuln.solution,
            cve=cve,
            cvss_v3_score=float(vuln.cvssV3BaseScore) if vuln.cvssV3BaseScore else 0.0,
            plugin_id=vuln.pluginID,
            plugin_name=vuln.pluginName,
            rule_id=vuln.pluginID,
            rule_version=vuln.pluginName,
            basis_for_adjustment="Tenable SC import",
            vulnerability_type="Tenable SC Vulnerability",
            vulnerable_asset=vuln.dnsName,
        )

    def to_integration_asset(self, asset: TenableAsset, **kwargs: dict) -> IntegrationAsset:
        """Converts a TenableAsset object to an IntegrationAsset object

        :param TenableAsset asset: The Tenable SC asset
        :param dict **kwargs: Additional keyword arguments
        :return: An IntegrationAsset object
        :rtype: IntegrationAsset
        """
        app = kwargs.get("app")
        config = app.config
        name = asset.dnsName if asset.dnsName else asset.ip
        return IntegrationAsset(
            name=name,
            identifier=asset.dnsName or asset.ip or asset.macAddress,
            ip_address=asset.ip,
            mac_address=asset.macAddress,
            asset_owner_id=config["userId"],
            status="Active (On Network)" if asset.family.type else "Off-Network",
            asset_type="Other",
            asset_category="Hardware",
        )
