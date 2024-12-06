"""
Snyk Scan information
"""

from datetime import datetime
from typing import Optional

from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import epoch_to_datetime, get_current_datetime, is_valid_fqdn
from regscale.models import ImportValidater, Mapping
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.models.regscale_models.asset import Asset
from regscale.models.regscale_models.vulnerability import Vulnerability


class Snyk(FlatFileImporter):
    """
    Snyk Scan information
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.vuln_title = "PROBLEM_TITLE"
        self.project_name = "PROJECT_NAME"
        self.issue_severity = "ISSUE_SEVERITY"
        self.auto_fixable = "AUTOFIXABLE"
        self.fmt = "%Y-%m-%d"
        self.dt_format = "%Y-%m-%d %H:%M:%S"
        self.required_headers = [
            self.project_name,
            self.issue_severity,
            self.vuln_title,
            self.auto_fixable,
        ]
        self.mapping_file = kwargs.get("mappings_path")
        self.disable_mapping = kwargs.get("disable_mapping")
        self.validater = ImportValidater(
            self.required_headers, kwargs.get("file_path"), self.mapping_file, self.disable_mapping
        )
        self.headers = self.validater.parsed_headers
        self.mapping = self.validater.mapping
        logger = create_logger()
        self.logger = logger
        super().__init__(
            logger=logger,
            app=Application(),
            headers=self.headers,
            asset_func=self.create_asset,
            vuln_func=self.create_vuln,
            file_type=".xlsx",
            extra_headers_allowed=True,
            **kwargs,
        )

    def determine_first_seen(self, dat: dict) -> str:
        """
        Determine the first seen date of the vulnerability

        :param dict dat: Data row from CSV file
        :return: The first seen date as a string
        :rtype: str
        """
        return datetime.combine(
            datetime.strptime(epoch_to_datetime(self.create_epoch, self.fmt), self.dt_format),
            self.mapping.get_value(dat, "FIRST_INTRODUCED", datetime.now().time()),
        ).strftime(self.dt_format)

    def create_asset(self, dat: Optional[dict] = None) -> Asset:
        """
        Create an asset from a row in the Snyk file

        :param Optional[dict] dat: Data row from CSV file, defaults to None
        :return: RegScale Asset object
        :rtype: Asset
        """
        name = self.extract_host(self.mapping.get_value(dat, self.project_name))
        valid_name = is_valid_fqdn(name)
        return Asset(
            **{
                "id": 0,
                "name": name,
                "ipAddress": "0.0.0.0",
                "isPublic": True,
                "status": "Active (On Network)",
                "assetCategory": "Software",
                "bLatestScan": True,
                "bAuthenticatedScan": True,
                "scanningTool": self.name,
                "assetOwnerId": self.config["userId"],
                "assetType": "Other",
                "fqdn": name if valid_name else None,
                "systemAdministratorId": self.config["userId"],
                "parentId": self.attributes.parent_id,
                "parentModule": self.attributes.parent_module,
            }
        )

    def create_vuln(self, dat: Optional[dict] = None, **kwargs) -> Optional[Vulnerability]:
        """
        Create a vulnerability from a row in the Snyk csv file

        :param Optional[dict] dat: Data row from CSV file, defaults to None
        :return: RegScale Vulnerability object or None
        :rtype: Optional[Vulnerability]
        """
        regscale_vuln = None
        severity = self.mapping.get_value(dat, self.issue_severity).lower()
        hostname = self.extract_host(self.mapping.get_value(dat, self.project_name))
        description = self.mapping.get_value(dat, self.vuln_title)
        solution = self.mapping.get_value(dat, self.auto_fixable)
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
                firstSeen=self.determine_first_seen(dat),
                daysOpen=None,
                dns=hostname,
                mitigated=None,
                operatingSystem=None,
                severity=severity,
                plugInName=description,
                cve=", ".join(self.mapping.get_value(dat, "CVE", "")),
                vprScore=None,
                tenantsId=0,
                title=f"{description} on asset {asset.name}",
                description=description,
                plugInText=self.mapping.get_value(dat, self.vuln_title),
                createdById=config["userId"],
                lastUpdatedById=config["userId"],
                dateCreated=get_current_datetime(),
                extra_data={"solution": solution},
            )
        return regscale_vuln

    @staticmethod
    def extract_host(s: str) -> str:
        """
        Extract the host from the project name

        :param str s: The project name
        :return: The host
        :rtype: str
        """
        try:
            res = (s.split("|"))[1].split("/")[0]
        except IndexError:
            res = s
        return res
