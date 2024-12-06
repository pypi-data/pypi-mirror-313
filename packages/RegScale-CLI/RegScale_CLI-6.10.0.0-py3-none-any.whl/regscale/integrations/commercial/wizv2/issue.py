""" Wiz Issue Integration class """

import logging
from typing import List, Dict, Any, Iterator

from regscale.core.app.utils.parser_utils import safe_datetime_str
from regscale.integrations.scanner_integration import issue_due_date, IntegrationFinding
from regscale.utils.dict_utils import get_value
from .constants import (
    get_wiz_issue_queries,
    WizVulnerabilityType,
)
from .scanner import WizVulnerabilityIntegration

logger = logging.getLogger(__name__)


class WizIssue(WizVulnerabilityIntegration):
    """
    Wiz Issue class
    """

    title = "Wiz"
    asset_identifier_field = "wizId"

    def get_query_types(self) -> List[Dict[str, Any]]:
        return get_wiz_issue_queries(project_id=self.plan_id)

    def parse_findings(
        self, nodes: List[Dict[str, Any]], vulnerability_type: WizVulnerabilityType
    ) -> Iterator[IntegrationFinding]:
        """
        Parse the Wiz issues into IntegrationFinding objects
        :param nodes:
        :param vulnerability_type:
        :return:
        """
        for node in nodes:
            finding = self.parse_finding(node, vulnerability_type)
            if finding:
                yield finding

    # noinspection PyMethodOverriding
    def parse_finding(self, wiz_issue: Dict[str, Any], vulnerability_type: WizVulnerabilityType) -> IntegrationFinding:
        """
        Parses a Wiz issue into an IntegrationFinding object.

        :param Dict[str, Any] wiz_issue: The Wiz issue to parse
        :return: The parsed IntegrationFinding
        :rtype: IntegrationFinding
        """
        wiz_id = wiz_issue.get("id", "N/A")
        severity = self.get_issue_severity(wiz_issue.get("severity", "Low"))
        status = self.map_status_to_issue_status(wiz_issue.get("status", "OPEN"))
        date_created = safe_datetime_str(wiz_issue.get("firstDetectedAt"))
        name: str = wiz_issue.get("name", "")
        cve = (
            name
            if name and (name.startswith("CVE") or name.startswith("GHSA")) and not wiz_issue.get("cve")
            else wiz_issue.get("cve")
        )

        finding = IntegrationFinding(
            control_labels=[],
            category="Wiz Vulnerability",
            title=wiz_issue.get("name") or f"unknown - {wiz_id}",
            description=wiz_issue.get("description", ""),
            severity=severity,
            status=status,
            asset_identifier=get_value(wiz_issue, "vulnerableAsset.id"),
            external_id=wiz_id,
            first_seen=date_created,
            last_seen=safe_datetime_str(wiz_issue.get("lastDetectedAt")),
            remediation=f"Update to version {wiz_issue.get('fixedVersion')} or higher",
            cve=cve,
            plugin_name="Wiz",
            source_rule_id=wiz_id,
            vulnerability_type="Wiz",
            date_created=date_created,
            due_date=issue_due_date(severity, date_created),
            recommendation_for_mitigation=wiz_issue.get("description", ""),
            poam_comments=None,
            basis_for_adjustment=None,
        )

        return finding
