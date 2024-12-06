from typing import List, Optional

from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models import Asset, Vulnerability, Mapping, ImportValidater
from regscale.models.integration_models.flat_file_importer import FlatFileImporter

APP_NAME = "@app_name"
VERSION = "@version"
ACCOUNT_ID = "@account_id"


class Veracode(FlatFileImporter):
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "Veracode")
        logger = create_logger()
        self.vuln_title = "PROBLEM_TITLE"
        self.fmt = "%Y-%m-%d"
        self.dt_format = "%Y-%m-%d %H:%M:%S"
        csv_headers = [
            "Source",
        ]
        xml_headers = [
            "app_name",
        ]
        self.mapping_file = kwargs.get("mappings_path")
        self.disable_mapping = kwargs.get("disable_mapping")
        file_type = kwargs.get("file_type")
        if file_type == ".xml":
            self.required_headers = xml_headers
        else:
            self.required_headers = csv_headers
        xml_tag = "detailedreport" if file_type == ".xml" else None
        self.validater = ImportValidater(
            self.required_headers, kwargs.get("file_path"), self.mapping_file, self.disable_mapping, xml_tag=xml_tag
        )
        self.headers = self.validater.parsed_headers
        self.mapping = self.validater.mapping
        super().__init__(
            logger=logger,
            headers=self.headers,
            asset_func=self.create_asset,
            vuln_func=self.create_vuln,
            extra_headers_allowed=False,
            **kwargs,
        )

    def create_asset(self, dat: Optional[dict] = None) -> List[Asset]:
        """
        Create a RegScale asset from an asset  in the Veracode export file

        :param Optional[dict] dat: The data from the Veracode export file
        :return: List of RegScale Asset objects
        :rtype: List[Asset]
        """
        version = None
        # Veracode is a Web Application Security Scanner, so these will be software assets, scanning a
        # single web application
        if "detailedreport" in self.mapping.mapping.keys():
            name = self.mapping.get_value(dat, "detailedreport", {}).get(APP_NAME, "")
            account_id = self.mapping.get_value(dat, "detailedreport", {}).get(ACCOUNT_ID, "")
            version = self.mapping.get_value(dat, "detailedreport", {}).get(VERSION, "")
        else:
            name = self.mapping.get_value(dat, "Source", "")
            account_id = str(self.mapping.get_value(dat, "ID", ""))
        asset = Asset(
            **{
                "id": 0,
                "name": name,
                "otherTrackingNumber": account_id,
                "ipAddress": "0.0.0.0",
                "isPublic": True,
                "status": "Active (On Network)",
                "assetCategory": "Software",
                "bLatestScan": True,
                "bAuthenticatedScan": True,
                "scanningTool": self.name,
                "assetOwnerId": self.config["userId"],
                "assetType": "Other",
                "softwareVendor": "Veracode",
                "softwareName": name,
                "softwareVersion": version,
                "systemAdministratorId": self.config["userId"],
                "parentId": self.attributes.parent_id,
                "parentModule": self.attributes.parent_module,
            }
        )
        return [asset]

    def create_vuln(self, dat: Optional[dict] = None, **kwargs) -> List[Vulnerability]:
        """
        Create a RegScale vulnerability from a vulnerability in the Veracode export file

        :param Optional[dict]  dat: The data from the Veracode export file
        :return: List of RegScale Vulnerability objects
        :rtype: List[Vulnerability]
        """
        import_type = "xml" if isinstance(dat, str) else "csv"
        # Veracode is a Web Application Security Scanner, so these will be software assets,
        # scanning a single web application
        if import_type == "xml":
            name = self.mapping.get_value(dat, "detailedreport", {}).get(APP_NAME, "")
            all_sev_data = self.mapping.get_value(dat, "detailedreport", {}).get("severity", [])
            severity = self.severity_info(all_sev_data)[0] if all_sev_data else "low"
            if severity_data := self.severity_info(all_sev_data):
                if isinstance(severity_data, list) and len(severity_data) >= 2:
                    cwes = [
                        f"{c.get('cweid')} {c.get('cwename')}" for c in severity_data[1].get("cwe", [])
                    ]  # Multiple cwes per asset in official XML
            else:
                cwes = []
        else:
            name = self.mapping.get_value(dat, "Source", "")
            severity = self.mapping.get_value(dat, "Sev", "").lower()
            cwes = [self.mapping.get_value(dat, "CWE ID & Name", [])]  # Coalfire should flatten data for asset -> cwes

        return self.process_csv_vulns(name, cwes, severity)

    def process_csv_vulns(self, hostname: str, cwes: List[str], severity: str) -> List[Vulnerability]:
        """
        Process the CSV findings from the ECR scan

        :param str hostname: The hostname
        :param List[str] cwes: The CWEs
        :param str severity: The severity
        :return: A list of vulnerabilities
        :rtype: List[Vulnerability]
        """
        vulns = []
        for cwe in cwes:
            severity = self.determine_severity(severity)
            if asset := self.get_asset(hostname):
                vuln = self.create_vulnerability_object(asset, hostname, cwe, severity, "")
                vulns.append(vuln)
        return vulns

    def create_vulnerability_object(
        self, asset: Asset, hostname: str, cwe: str, severity: str, description: str
    ) -> Vulnerability:
        """
        Create a vulnerability from a row in the Veracode file

        :param Asset asset: The asset
        :param str hostname: The hostname
        :param str cwe: The CWE
        :param str severity: The severity
        :param str description: The description
        :return: The vulnerability
        :rtype: Vulnerability
        """
        config = self.attributes.app.config

        return Vulnerability(  # type: ignore
            id=0,
            scanId=0,
            parentId=asset.id,
            parentModule="assets",
            ipAddress="0.0.0.0",
            lastSeen=get_current_datetime(),  # No timestamp on Veracode
            firstSeen=get_current_datetime(),  # No timestamp on Veracode
            daysOpen=None,
            dns=hostname,
            mitigated=None,
            operatingSystem=asset.operatingSystem,
            severity=severity,
            plugInName=cwe,
            cve="",
            tenantsId=0,
            title=f"{cwe} on asset {asset.name}",
            description=cwe,
            plugInText=description,
            createdById=config["userId"],
            lastUpdatedById=config["userId"],
            dateCreated=get_current_datetime(),
        )

    def get_asset(self, hostname: str) -> Optional[Asset]:
        """
        Get the asset from the hostname

        :param str hostname: The hostname
        :return: The asset, if found
        :rtype: Optional[Asset]
        """
        asset_match = [asset for asset in self.data["assets"] if asset.name == hostname]
        return asset_match[0] if asset_match else None

    def severity_info(self, severity_list: list) -> Optional[tuple]:
        """
        Get the severity level and category of the vulnerability

        :param list severity_list: List of severity levels
        :return: Severity level and category
        :rtype: Optional[tuple]
        """
        hit = [sev for sev in severity_list if sev.get("category")]
        if hit:
            return (self.hit_mapping().get(hit[0].get("level"), "low"), hit[0].get("category"))
        return None

    @staticmethod
    def hit_mapping() -> dict:
        """
        Mapping of severity levels

        :return: Mapping of severity levels
        :rtype: dict
        """
        return {
            "5": "critical",
            "4": "high",
            "3": "moderate",
            "2": "low",
            "1": "low",
            "0": "info",
        }
