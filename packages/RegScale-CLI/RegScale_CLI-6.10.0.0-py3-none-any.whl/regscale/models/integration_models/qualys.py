"""
Qualys Scan information
"""

# pylint: disable=C0415
import re
from typing import Any, Optional, TypeVar

from regscale.core.app import create_logger
from regscale.core.app.application import Application
from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models import ImportValidater, Mapping
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.models.regscale_models import Asset, Vulnerability

T = TypeVar("T")
QG_HOST_ID = "QG Host ID"
CVE_ID = "CVE ID"
SEVERITY = "Severity"
EXPLOITABILITY = "Exploitability"
SOLUTION = "Solution"
DNS = "DNS"
IP = "IP"
OS = "OS"
NETBIOS = "NetBIOS"
FQDN = "FQDN"


class Qualys(FlatFileImporter):
    """Qualys Scan information"""

    title = "Qualys Scanner Export Integration"
    asset_identifier_field = "name"

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.vuln_title = "Title"
        self.fmt = "%Y-%m-%d"
        self.dt_format = "%Y-%m-%d %H:%M:%S"
        self.required_headers = [
            SEVERITY,
            self.vuln_title,
            EXPLOITABILITY,
            CVE_ID,
            SOLUTION,
            DNS,
            IP,
            QG_HOST_ID,
            OS,
            NETBIOS,
            FQDN,
        ]
        logger = create_logger()
        skip_rows = kwargs.pop("skip_rows")
        self.mapping_file = kwargs.get("mappings_path")
        self.disable_mapping = kwargs.get("disable_mapping")
        self.validater = ImportValidater(
            self.required_headers, kwargs.get("file_path"), self.mapping_file, self.disable_mapping, skip_rows=skip_rows
        )
        self.headers = self.validater.parsed_headers
        self.mapping = self.validater.mapping
        super().__init__(
            logger=logger,
            app=Application(),
            headers=self.headers,
            header_line_number=skip_rows,
            asset_func=self.create_asset,
            vuln_func=self.create_vuln,
            **kwargs,
        )
        # header is line# 11
        # start self.file_data from line #12

    def create_asset(self, dat: Optional[dict] = None) -> Optional[Asset]:
        """
        Create an asset from a row in the Qualys file

        :param Optional[dict] dat: Data row from CSV file
        :return: RegScale Issue object or None
        :rtype: Optional[Asset]
        """
        return Asset(
            **{
                "id": 0,
                "name": self.mapping.get_value(dat, DNS),
                "ipAddress": self.mapping.get_value(dat, IP),
                "isPublic": True,
                "status": "Active (On Network)",
                "assetCategory": "Hardware",
                "qualysId": self.mapping.get_value(dat, QG_HOST_ID),  # UUID from Nessus HostProperties tag
                "bLatestScan": True,
                "bAuthenticatedScan": True,
                "scanningTool": "Qualys",
                "assetOwnerId": self.attributes.app.config["userId"],
                "netBIOS": self.mapping.get_value(dat, NETBIOS),
                "assetType": "Other",
                "fqdn": self.mapping.get_value(dat, FQDN),
                "operatingSystem": Asset.find_os(self.mapping.get_value(dat, OS)),
                "operatingSystemVersion": self.mapping.get_value(dat, OS),
                "systemAdministratorId": self.attributes.app.config["userId"],
                "parentId": self.attributes.parent_id,
                "parentModule": self.attributes.parent_module,
            }
        )

    def create_vuln(self, dat: Optional[dict] = None, **kwargs) -> None:
        """
        Create a vuln from a row in the Qualys file

        :param Optional[dict] dat: Data row from CSV file, defaults to None
        :rtype: None
        """
        from regscale.integrations.commercial.qualys import map_qualys_severity_to_regscale

        dns: str = self.mapping.get_value(dat, DNS)
        other_id: str = self.mapping.get_value(dat, QG_HOST_ID)
        distro: str = self.mapping.get_value(dat, OS)
        cve: str = self.mapping.get_value(dat, CVE_ID)
        description: str = self.mapping.get_value(dat, "Threat")
        title = self.mapping.get_value(dat, self.vuln_title)
        regscale_vuln = None
        severity = self.mapping.get_value(dat, SEVERITY)
        regscale_severity = map_qualys_severity_to_regscale(int(severity))[1]
        config = self.attributes.app.config
        asset_match = [asset for asset in self.data["assets"] if asset.name == dns]
        asset = asset_match[0] if asset_match else None
        if dat and asset_match:
            regscale_vuln = Vulnerability(
                id=0,
                scanId=0,  # set later
                parentId=asset.id,
                parentModule="assets",
                ipAddress=self.mapping.get_value(dat, IP),
                lastSeen=self.mapping.get_value(dat, "Last Detected"),
                firstSeen=self.mapping.get_value(dat, "First Detected"),
                daysOpen=None,
                dns=self.mapping.get_value(dat, DNS, other_id),
                mitigated=None,
                operatingSystem=(Asset.find_os(distro) if Asset.find_os(distro) else None),
                severity=regscale_severity,
                plugInName=self.mapping.get_value(dat, self.vuln_title),
                plugInId=self.mapping.get_value(dat, "QID"),
                cve=cve,
                vprScore=None,
                cvsSv3BaseScore=self.extract_float(self.mapping.get_value(dat, "CVSS3.1 Base", 0.0)),
                tenantsId=0,
                title=title,
                description=description,
                plugInText=title,
                createdById=config["userId"],
                lastUpdatedById=config["userId"],
                dateCreated=get_current_datetime(),
            )
        return regscale_vuln

    @staticmethod
    def extract_float(s: str) -> Any:
        """
        Extract a float from a string

        :param str s: String to extract float from
        :return: Float extracted from string or None
        :rtype: Any
        """
        matches = re.findall(r"[-+]?[0-9]*\.?[0-9]+", s)
        if matches:
            return float(matches[0])
        else:
            return None
