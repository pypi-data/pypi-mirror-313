"""
Nexpose Scan information
"""

from pathlib import Path
from typing import Optional

from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import epoch_to_datetime, get_current_datetime, is_valid_fqdn
from regscale.models import ImportValidater
from regscale.models.app_models.mapping import Mapping
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.models.regscale_models import Asset, Issue, Vulnerability

VULNERABILITY_TITLE = "Vulnerability Title"
VULNERABILITY_ID = "Vulnerability ID"
CVSS3_SCORE = "CVSSv3 Score"
IP_ADDRESS = "IP Address"


class Nexpose(FlatFileImporter):
    """
    Prisma/Nexpose Scan information
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        regscale_ssp_id = kwargs.get("plan_id")
        self.vuln_title = VULNERABILITY_TITLE
        self.vuln_id = VULNERABILITY_ID
        self.cvss3_score = CVSS3_SCORE
        self.required_headers = [
            "IP Address",
            "Hostname",
            "OS",
            "Vulnerability Title",
            "Vulnerability ID",
            "CVSSv2 Score",
            "CVSSv3 Score",
            "Description",
            "Proof",
            "Solution",
            "CVEs",
        ]
        self.mapping_file = kwargs.get("mappings_path")
        self.disable_mapping = kwargs.get("disable_mapping")
        self.validater = ImportValidater(
            self.required_headers, kwargs.get("file_path"), self.mapping_file, self.disable_mapping
        )
        self.headers = self.validater.parsed_headers
        self.mapping = self.validater.mapping
        logger = create_logger()
        super().__init__(
            logger=logger,
            app=Application(),
            headers=self.mapping.to_header(),
            parent_id=regscale_ssp_id,
            parent_module="securityplans",
            asset_func=self.create_asset,
            vuln_func=self.create_vuln,
            extra_headers_allowed=True,
            **kwargs,
        )

    def create_asset(self, dat: Optional[dict] = None) -> Asset:
        """
        Create an asset from a row in the Nexpose csv file

        :param Optional[dict] dat: Data row from CSV file, defaults to None
        :return: RegScale Asset object
        :rtype: Asset
        """
        hostname = self.mapping.get_value(dat, "Hostname")
        return Asset(
            **{
                "id": 0,
                "name": hostname,
                "ipAddress": self.mapping.get_value(dat, IP_ADDRESS),
                "isPublic": True,
                "status": "Active (On Network)",
                "assetCategory": "Hardware",
                "bLatestScan": True,
                "bAuthenticatedScan": True,
                "scanningTool": self.name,
                "assetOwnerId": self.config["userId"],
                "assetType": "Other",
                "fqdn": hostname if is_valid_fqdn(hostname) else None,
                "operatingSystem": Asset.find_os(self.mapping.get_value(dat, "OS")),
                "systemAdministratorId": self.config["userId"],
                "parentId": self.attributes.parent_id,
                "parentModule": self.attributes.parent_module,
            }
        )

    def create_vuln(self, dat: Optional[dict] = None, **kwargs) -> Optional[Vulnerability]:
        """
        Create a vulnerability from a row in the Prisma/Nexpose csv file

        :param Optional[dict] dat: Data row from CSV file, defaults to None
        :return: RegScale Vulnerability object or None
        :rtype: Optional[Vulnerability]
        """
        regscale_vuln = None
        cvss3_score = self.mapping.get_value(dat, self.cvss3_score)
        hostname: str = self.mapping.get_value(dat, "Hostname")
        os: str = self.mapping.get_value(dat, "OS")
        description: str = self.mapping.get_value(dat, "Description")
        severity = Vulnerability.determine_cvss3_severity_text(float(cvss3_score)) if cvss3_score else "low"
        config = self.attributes.app.config
        asset_match = [asset for asset in self.data["assets"] if asset.name == hostname]
        asset = asset_match[0] if asset_match else None
        if dat and asset_match:
            return Vulnerability(
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
                operatingSystem=(Asset.find_os(os) if Asset.find_os(os) else None),
                severity=severity,
                plugInName=self.mapping.get_value(dat, self.vuln_title),
                plugInId=self.mapping.get_value(dat, self.vuln_id),
                cve=self.mapping.get_value(dat, "CVEs"),
                vprScore=None,
                tenantsId=0,
                title=description[:255],
                description=description,
                plugInText=self.mapping.get_value(dat, self.vuln_title),
                createdById=config["userId"],
                lastUpdatedById=config["userId"],
                dateCreated=get_current_datetime(),
                extra_data={
                    "solution": self.mapping.get_value(dat, "Solution"),
                    "proof": self.mapping.get_value(dat, "Proof"),
                },
            )
        return regscale_vuln
