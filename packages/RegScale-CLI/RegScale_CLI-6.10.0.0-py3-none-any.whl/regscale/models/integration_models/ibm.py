"""
IBM Scan information
"""

from typing import Optional
from urllib.parse import urlparse

from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import epoch_to_datetime, get_current_datetime, is_valid_fqdn
from regscale.models import ImportValidater, Mapping
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.models.regscale_models import Asset, Vulnerability

ISSUE_TYPE = "Issue Type"
VULNERABILITY_TITLE = ISSUE_TYPE
VULNERABILITY_ID = ISSUE_TYPE


class AppScan(FlatFileImporter):
    """
    IBM Scan information
    """

    severity_map = {
        "Critical": "critical",
        "High": "high",
        "Medium": "medium",
        "Low": "low",
        "Informational": "low",
    }

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        regscale_ssp_id = kwargs.get("plan_id")
        self.vuln_title = VULNERABILITY_TITLE
        self.vuln_id = VULNERABILITY_ID
        logger = create_logger()
        self.required_headers = ["URL"]
        self.mapping_file = kwargs.get("mappings_path")
        self.disable_mapping = kwargs.get("disable_mapping")
        self.validater = ImportValidater(
            self.required_headers, kwargs.get("file_path"), self.mapping_file, self.disable_mapping
        )
        self.headers = self.validater.parsed_headers
        self.mapping = self.validater.mapping
        super().__init__(
            logger=logger,
            app=Application(),
            headers=self.headers,
            parent_id=regscale_ssp_id,
            parent_module="securityplans",
            asset_func=self.create_asset,
            vuln_func=self.create_vuln,
            extra_headers_allowed=True,
            **kwargs,
        )

    def create_asset(self, dat: Optional[dict] = None) -> Asset:
        """
        Create an asset from a row in the IBM csv file

        :param Optional[dict] dat: Data row from CSV file, defaults to None
        :return: RegScale Asset object
        :rtype: Asset
        """
        parsed_url = urlparse(self.mapping.get_value(dat, "URL"))
        hostname: str = f"{parsed_url.scheme}://{parsed_url.netloc}"
        return Asset(
            **{
                "id": 0,
                "name": hostname,
                "isPublic": True,
                "status": "Active (On Network)",
                "assetCategory": "Software",
                "bLatestScan": True,
                "bAuthenticatedScan": True,
                "scanningTool": self.name,
                "assetOwnerId": self.config["userId"],
                "assetType": "Other",
                "fqdn": hostname if is_valid_fqdn(hostname) else None,
                "systemAdministratorId": self.config["userId"],
                "parentId": self.attributes.parent_id,
                "parentModule": self.attributes.parent_module,
            }
        )

    def create_vuln(self, dat: Optional[dict] = None, **kwargs) -> Optional[Vulnerability]:
        """
        Create a vulnerability from a row in the IBM csv file

        :param Optional[dict] dat: Data row from CSV file, defaults to None
        :return: RegScale Vulnerability object or None
        :rtype: Optional[Vulnerability]
        """
        regscale_vuln = None
        parsed_url = urlparse(self.mapping.get_value(dat, "URL"))
        hostname: str = f"{parsed_url.scheme}://{parsed_url.netloc}"
        description: str = self.mapping.get_value(dat, ISSUE_TYPE)
        app_scan_severity = self.mapping.get_value(dat, "Severity")
        severity = self.severity_map.get(app_scan_severity, "Informational")
        config = self.attributes.app.config
        asset_match = [asset for asset in self.data["assets"] if asset.name == hostname]
        asset = asset_match[0] if asset_match else None
        if dat and asset_match:
            regscale_vuln = Vulnerability(
                id=0,
                scanId=0,  # set later
                parentId=asset.id,
                parentModule="assets",
                ipAddress="0.0.0.0",  # No ip address available
                lastSeen=get_current_datetime(),
                firstSeen=epoch_to_datetime(self.create_epoch),
                daysOpen=None,
                dns=hostname,
                mitigated=None,
                severity=severity,
                plugInName=description,
                cve="",
                vprScore=None,
                tenantsId=0,
                title=description[:255] if description else "No Title",
                description=description,
                plugInText=description,
                createdById=config["userId"],
                lastUpdatedById=config["userId"],
                dateCreated=get_current_datetime(),
            )
        return regscale_vuln
