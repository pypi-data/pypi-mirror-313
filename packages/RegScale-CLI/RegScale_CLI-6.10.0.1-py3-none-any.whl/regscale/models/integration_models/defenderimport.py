"""
Integration model to import data from Defender .csv export
"""

import json
from datetime import datetime
from typing import Optional

from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import get_current_datetime, is_valid_fqdn
from regscale.core.utils.date import datetime_obj, datetime_str
from regscale.models import Asset, ImportValidater, Vulnerability
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.regscale import Application


class DefenderImport(FlatFileImporter):
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.vuln_title = "SUBASSESSMENTNAME"
        self.vuln_id = "SUBASSESSMENTID"
        logger = create_logger()
        self.fmt = "%Y-%m-%d"
        self.dt_format = "%Y-%m-%d %H:%M:%S"
        self.required_headers = [
            "SEVERITY",
            self.vuln_title,
            self.vuln_id,
        ]
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
            asset_func=self.create_asset,
            vuln_func=self.create_vuln,
            file_type=".csv",
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
        # Remove the 'Z' at the end
        iso_string = self.mapping.get_value(dat, "TIMEGENERATED", "").rstrip("Z")

        # Convert to datetime object
        dt_object = datetime_obj(iso_string)

        return datetime_str(dt_object, self.dt_format)

    def create_asset(self, dat: Optional[dict] = None) -> Asset:
        """
        Create an asset from a row in the Snyk file

        :param Optional[dict] dat: Data row from CSV file, defaults to None
        :return: RegScale Asset object
        :rtype: Asset
        """
        additional_data = json.loads(self.mapping.get_value(dat, "ADDITIONALDATA", {}))
        os = Asset.find_os(additional_data.get("imageDetails", {}).get("osDetails", ""))
        name = additional_data.get("repositoryName", "")
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
                "operatingSystem": os,
            }
        )

    def create_vuln(self, dat: Optional[dict] = None, **kwargs: dict) -> Optional[Vulnerability]:
        """
        Create a vulnerability from a row in the Snyk csv file

        :param Optional[dict] dat: Data row from CSV file, defaults to None
        :param dict **kwargs: Additional keyword arguments
        :return: RegScale Vulnerability object or None
        :rtype: Optional[Vulnerability]
        """
        regscale_vuln = None
        severity = self.mapping.get_value(dat, "SEVERITY", "").lower()
        additional_data = json.loads(self.mapping.get_value(dat, "ADDITIONALDATA", {}))
        hostname = additional_data.get("repositoryName", "")
        description = self.mapping.get_value(dat, self.vuln_title)
        solution = self.mapping.get_value(dat, self.vuln_id)
        config = self.attributes.app.config
        asset_match = [asset for asset in self.data["assets"] if asset.name == hostname]
        asset = asset_match[0] if asset_match else None
        cves = [cve.get("title", "") for cve in additional_data.get("cve", [])]
        cvss_v3_score = float(additional_data.get("cvssV30Score", 0))
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
                cve=", ".join(cves) if cves else self.mapping.get_value(dat, self.vuln_title),
                vprScore=None,
                cvsSv3BaseScore=cvss_v3_score,
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
