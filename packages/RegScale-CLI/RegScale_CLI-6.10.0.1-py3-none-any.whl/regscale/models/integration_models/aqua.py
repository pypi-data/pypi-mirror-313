"""
Aqua Scan information
"""

from itertools import groupby
from operator import itemgetter
from typing import List, Optional

from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import get_current_datetime, is_valid_fqdn
from regscale.core.utils.date import datetime_str
from regscale.models.app_models import ImportValidater, Mapping
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.models.regscale_models.asset import Asset
from regscale.models.regscale_models.vulnerability import Vulnerability


class Aqua(FlatFileImporter):
    """Aqua Scan information"""

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        regscale_ssp_id = kwargs.get("regscale_ssp_id")
        self.vuln_title = "Vulnerability Name"
        self.fmt = "%m/%d/%Y"
        self.dt_format = "%Y-%m-%d %H:%M:%S"
        self.image_name = "Image Name"
        self.OS = "OS"
        self.description = "Description"
        self.ffi = "First Found on Image"
        self.last_image_scan = "Last Image Scan"
        self.installed_version = "Installed Version"
        self.vendor_cvss_v2_severity = "Vendor CVSS v2 Severity"
        self.vendor_cvss_v3_severity = "Vendor CVSS v3 Severity"
        self.vendor_cvss_v3_score = "Vendor CVSS v3 Score"
        self.nvd_cvss_v2_severity = "NVD CVSS v2 Severity"
        self.nvd_cvss_v3_severity = "NVD CVSS v3 Severity"
        self.required_headers = [
            self.image_name,
            self.OS,
            self.vuln_title,
            self.description,
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
            headers=self.headers,
            parent_id=regscale_ssp_id,
            parent_module="securityplans",
            asset_func=self.create_asset,
            vuln_func=self.create_vuln,
            app=Application(),
            ignore_validation=True,
            file_type=self.validater.file_type,
            **kwargs,
        )

    def create_asset(self, dat: Optional[dict] = None) -> Optional[Asset]:
        """
        Create an asset from a row in the Aqua file

        :param Optional[dict] dat: Data row from CSV file, defaults to None
        :return: RegScale Asset object or None
        :rtype: Optional[Asset]
        """
        name = self.mapping.get_value(dat, self.image_name)
        if not name:
            return None
        os = self.mapping.get_value(dat, self.OS)
        return Asset(
            **{
                "id": 0,
                "name": name,
                "description": "",
                "operatingSystem": Asset.find_os(os),
                "operatingSystemVersion": os,
                "ipAddress": "0.0.0.0",
                "isPublic": True,
                "status": "Active (On Network)",
                "assetCategory": "Hardware",
                "bLatestScan": True,
                "bAuthenticatedScan": True,
                "scanningTool": self.name,
                "assetOwnerId": self.config["userId"],
                "assetType": "Other",
                "fqdn": name if is_valid_fqdn(name) else None,
                "systemAdministratorId": self.config["userId"],
                "parentId": self.attributes.parent_id,
                "parentModule": self.attributes.parent_module,
                "extra_data": {"software_inventory": self.generate_software_inventory(name)},
            }
        )

    def generate_software_inventory(self, name: str) -> List[dict]:
        """
        Create and post a list of software inventory for a given asset

        :param str name: The name of the asset
        :return: List of software inventory
        :rtype: List[dict]
        """
        inventory: List[dict] = []

        image_group = {
            k: list(g) for k, g in groupby(self.file_data, key=itemgetter(self.mapping.get_header(self.image_name)))
        }

        softwares = image_group[name]
        for software in softwares:
            inv = {
                "name": software["Resource"],
                "version": str(software[self.installed_version]),
            }
            if (inv.get("name"), inv.get("version")) not in {
                (soft.get("name"), soft.get("version")) for soft in inventory
            }:
                inventory.append(inv)

        return inventory

    def current_datetime_w_log(self, field: str) -> str:
        """
        Get the current date and time with a log message

        :param str field: The field that is missing the date
        :return: The current date and time
        :rtype: str
        """
        self.logger.info(f"Unable to determine date for the '{field}' field, falling back to current date and time.")
        return get_current_datetime()

    def create_vuln(self, dat: Optional[dict] = None, **kwargs) -> Optional[Vulnerability]:
        """
        Create a vulnerability from a row in the Aqua csv file

        :param Optional[dict] dat: Data row from CSV file, defaults to None
        :return: RegScale Vulnerability object or None
        :rtype: Optional[Vulnerability]
        """
        regscale_vuln = None
        severity = self.determine_cvss_severity(dat)
        hostname = self.mapping.get_value(dat, self.image_name)
        description = self.mapping.get_value(dat, self.description)
        solution = self.mapping.get_value(dat, self.description) or "Upgrade affected package"
        config = self.attributes.app.config
        asset_match = [asset for asset in self.data["assets"] if asset.name == hostname]
        asset = asset_match[0] if asset_match else None
        if asset_match and self.validate(ix=kwargs.get("index"), dat=dat):
            regscale_vuln = Vulnerability(
                id=0,
                scanId=0,
                parentId=asset.id,
                parentModule="assets",
                ipAddress="0.0.0.0",
                lastSeen=datetime_str(self.mapping.get_value(dat, self.last_image_scan))
                or self.current_datetime_w_log(self.last_image_scan),
                firstSeen=datetime_str(self.mapping.get_value(dat, self.ffi)) or self.current_datetime_w_log(self.ffi),
                daysOpen=None,
                dns=hostname,
                mitigated=None,
                operatingSystem=asset.operatingSystem,
                severity=severity,
                plugInName=description,
                cve=self.mapping.get_value(dat, self.vuln_title),
                cvsSv3BaseScore=self.mapping.get_value(dat, self.vendor_cvss_v3_score),
                tenantsId=0,
                title=description[:255] if description else f"Vulnerability on {hostname}",
                description=description,
                plugInText=self.mapping.get_value(dat, self.vuln_title),
                createdById=config["userId"],
                lastUpdatedById=config["userId"],
                dateCreated=get_current_datetime(),
                extra_data={"solution": solution},
            )
        return regscale_vuln

    def determine_cvss_severity(self, dat: dict) -> str:
        """
        Determine the CVSS severity of the vulnerability

        :param dict dat: Data row from CSV file
        :return: A severity derived from the CVSS scores
        :rtype: str
        """
        precedence_order = [
            self.nvd_cvss_v3_severity,
            self.nvd_cvss_v2_severity,
            self.vendor_cvss_v3_severity,
            # This field may or may not be available in the file (Coalfire has it, BMC does not.)
            (
                self.vendor_cvss_v2_severity
                if self.mapping.get_value(dat, self.vendor_cvss_v2_severity, warnings=False)
                else None
            ),
        ]
        severity = "info"
        for key in precedence_order:
            if key and self.mapping.get_value(dat, key):
                severity = self.mapping.get_value(dat, key).lower()
                break
        # remap crits to highs
        if severity == "critical":
            severity = "high"
        return severity

    def validate(self, ix: Optional[int], dat: dict) -> bool:
        """
        Validate the row of data, and populate with something if missing

        :param Optional[int] ix: index
        :param dict dat: Data row from CSV file
        :return: True if the row is valid or has been updated with default value
        :rtype: bool
        """
        required_keys = [self.description]
        val = True
        for key in required_keys:
            if not dat.get(key):
                default_val = f"No {key} available."
                row_skip = (
                    f"Populating {key} for row #{ix + 1} with {default_val}"
                    if isinstance(ix, int)
                    else f"Populating {key} with {default_val}"
                )
                self.attributes.logger.warning(f"Missing value for required field: {key}, {row_skip}")
                dat[key] = default_val
        return val
