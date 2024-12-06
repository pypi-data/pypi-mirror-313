"""
ECR Scan information
"""

import json
from pathlib import Path
from typing import Any, List, Optional, Sequence, Union

from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import get_current_datetime, is_valid_fqdn
from regscale.exceptions import ValidationException
from regscale.models import ImportValidater
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.models.regscale_models.asset import Asset
from regscale.models.regscale_models.vulnerability import Vulnerability


class ECR(FlatFileImporter):
    """ECR Scan information"""

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.vuln_title = "name"
        self.fmt = "%m/%d/%y"
        self.dt_format = "%Y-%m-%d %H:%M:%S"
        self.image_name = "Name"
        self.raw_dict = {}
        file_path = Path(kwargs.get("file_path")) if kwargs.get("file_path") else Path()
        parent_id = kwargs.get("parent_id")
        parent_module = kwargs.get("parent_module")
        self.required_headers = [
            self.image_name,
        ]
        self.mapping_file = kwargs.get("mappings_path")
        self.disable_mapping = kwargs.get("disable_mapping")
        self.file_type = kwargs.get("file_type")
        keys = ["imageScanFindings", "findings"] if self.file_type == ".json" else None
        self.validater = ImportValidater(
            self.required_headers, kwargs.get("file_path"), self.mapping_file, self.disable_mapping, keys=keys
        )
        self.headers = self.validater.parsed_headers
        self.mapping = self.validater.mapping
        logger = create_logger()
        super().__init__(
            name=self.name,
            logger=logger,
            app=Application(),
            file_path=file_path,
            headers=self.headers,
            parent_id=parent_id,
            parent_module=parent_module,
            file_type=self.file_type.replace(".", ""),
            asset_func=self.create_asset,
            vuln_func=self.create_vuln,
        )

    def file_to_list_of_dicts(
        self,
    ) -> tuple[Optional[Sequence[str]], Union[dict, list[Any]]]:
        """
        Override the base method: Converts a json or csv file to a list of dictionaries

        :raises ValidationException: If the headers in the csv/xlsx file do not match the expected headers
        :return: Tuple of header and data from csv file
        :rtype: tuple[Optional[Sequence[str]], Union[dict, list[Any]]]
        """
        header: Optional[Sequence[str]] = []
        data: dict = {}
        with open(self.attributes.file_path, encoding="utf-8") as file:
            if file.name.endswith(".csv"):
                data, header = self.convert_csv_to_dict(file)
            elif file.name.endswith(".json"):
                try:
                    # Filter possible null values
                    self.raw_dict = json.load(file)
                    if not isinstance(self.raw_dict, dict):
                        raise ValidationException(
                            f"Invalid JSON file. Must be a dictionary, it is {type(self.raw_dict)}"
                        )
                    data = self.raw_dict.get("imageScanFindings", {}).get("findings", [])
                except json.JSONDecodeError:
                    raise ValidationException("Invalid JSON file. Encountered a JSONDecodeError.")
            else:
                raise ValidationException(
                    f"Unsupported file type. Must be a .csv or .json file.\nProvided: {self.file_type}"
                )
        return header, data

    def create_asset(self, dat: Optional[dict] = None) -> Asset:
        """
        Create an asset from a row in the ECR file

        :param Optional[dict] dat: Data row from file, defaults to None
        :return: RegScale Asset object
        :rtype: Asset
        """
        name = self.mapping.get_value(dat, "Name") or self.mapping.get_value(dat, "name")
        if repository_name := self.mapping.get_value(
            dat, "repositoryName", self.raw_dict.get("repositoryName", ""), warnings=False
        ):
            if (image_id_data := self.raw_dict.get("imageId", {}).get("imageDigest", "").split(":")) and len(
                image_id_data
            ) > 1:
                image_id = image_id_data[1]
            else:
                image_id = image_id_data[0]
            name = f"{repository_name}:{image_id}"

        # Check if string has a forward slash
        return Asset(
            **{
                "id": 0,
                "name": name,
                "description": "Container Image" if name and "/" in name else "",
                "operatingSystem": "Linux",
                "operatingSystemVersion": "",
                "ipAddress": "0.0.0.0",
                "isPublic": True,
                "status": "Active (On Network)",
                "assetCategory": "Software",
                "bLatestScan": True,
                "bAuthenticatedScan": True,
                "scanningTool": self.name,
                "assetOwnerId": self.config["userId"],
                "assetType": "Other",
                "fqdn": name if is_valid_fqdn(name) else None,
                "systemAdministratorId": self.config["userId"],
                "parentId": self.attributes.parent_id,
                "parentModule": self.attributes.parent_module,
            }
        )

    def create_vuln(self, dat: Optional[dict] = None, **kwargs) -> Union[Vulnerability, List[Vulnerability], None]:
        """
        Create a vulnerability from a row in the ECR csv file

        :param Optional[dict] dat: Data row from file, defaults to None
        :return: RegScale Vulnerability object, a list of RegScale Vulnerability objects or None
        :rtype: Union[Vulnerability, List[Vulnerability], None]
        """
        vulns: List[Vulnerability] = []
        hostname = dat.get("Name") or dat.get("name")
        if repository_name := self.mapping.get_value(
            dat, "repositoryName", self.raw_dict.get("repositoryName", ""), warnings=False
        ):
            image_id_data = self.raw_dict.get("imageId", {}).get("imageDigest", "").split(":")
            if len(image_id_data) > 1:
                image_id = image_id_data[1]
            else:
                image_id = image_id_data[0]
            hostname = f"{repository_name}:{image_id}"
        if dat.get("imageScanFindings"):
            vulns = self.process_json_vulns(dat, hostname)
        else:
            single_vuln = self.process_csv_vulns(dat, hostname)
            if single_vuln:
                return single_vuln
        return vulns

    def get_asset(self, hostname: str) -> Optional[Asset]:
        """
        Get the asset by hostname

        :param str hostname: The hostname
        :return: The asset if found, otherwise None
        :rtype: Optional[Asset]
        """
        asset_match = [asset for asset in self.data["assets"] if asset.name == hostname]
        return asset_match[0] if asset_match else None

    def create_vulnerability_object(
        self, asset: Asset, hostname: str, cve: str, severity: str, description: str
    ) -> Vulnerability:
        """
        Create a vulnerability from a row in the ECR file

        :param Asset asset: The asset
        :param str hostname: The hostname
        :param str cve: The CVE
        :param str severity: The severity
        :param str description: The description
        :return: The vulnerability
        :rtype: Vulnerability
        """
        config = self.attributes.app.config

        return Vulnerability(
            id=0,
            scanId=0,
            parentId=asset.id,
            parentModule="assets",
            ipAddress="0.0.0.0",
            firstSeen=get_current_datetime(),  # No timestamp on ECR
            lastSeen=get_current_datetime(),  # No timestamp on ECR
            daysOpen=None,
            dns=hostname,
            mitigated=None,
            operatingSystem=asset.operatingSystem,
            severity=severity,
            plugInName=cve,
            cve=cve,
            tenantsId=0,
            title=f"{cve} on asset {asset.name}",
            description=cve,
            plugInText=description,
            createdById=config["userId"],
            lastUpdatedById=config["userId"],
            dateCreated=get_current_datetime(),
        )

    def process_csv_vulns(self, dat: dict, hostname: str) -> Optional[Vulnerability]:
        """
        Process the CSV findings from the ECR scan

        :param dict dat: The data from the ECR scan
        :param str hostname: The hostname
        :return: The vulnerability or None
        :rtype: Optional[Vulnerability]

        """
        cve = dat.get("CVE", "")
        severity = self.determine_severity(dat.get("Severity", "Info"))
        if asset := self.get_asset(hostname):
            return self.create_vulnerability_object(asset, hostname, cve, severity, dat.get("uri", ""))
        return None

    def process_json_vulns(self, dat: dict, hostname: str) -> List[Vulnerability]:
        """
        Process the JSON findings from the ECR scan

        :param dict dat: The data from the ECR scan
        :param str hostname: The hostname
        :return: The list of vulnerabilities
        :rtype: List[Vulnerability]
        """
        vulns: List[Vulnerability] = []
        if findings := dat.get("imageScanFindings", {}).get("findings"):
            for finding in findings:
                cve = finding.get("name")
                severity = self.determine_severity(finding["severity"])
                asset = self.get_asset(hostname)
                if asset:
                    vuln = self.create_vulnerability_object(asset, hostname, cve, severity, finding.get("uri", ""))
                    vulns.append(vuln)
        return vulns
