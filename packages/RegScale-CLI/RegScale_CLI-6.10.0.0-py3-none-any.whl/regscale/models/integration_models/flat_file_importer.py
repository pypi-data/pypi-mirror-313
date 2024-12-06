""" Container Scan Abstract """

import ast
import csv
import json
import re
import shutil
from abc import ABC, abstractmethod
from collections import namedtuple
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Generator, Iterator, List, Optional, Sequence, TextIO, Tuple, Union

import click
import requests
import xmltodict
from openpyxl.reader.excel import load_workbook

from regscale.core.app.api import Api
from regscale.core.app.utils.app_utils import (
    check_file_path,
    convert_datetime_to_regscale_string,
    create_progress_object,
    creation_date,
    error_and_exit,
    get_current_datetime,
)
from regscale.core.app.utils.report_utils import ReportGenerator
from regscale.integrations.public.cisa import pull_cisa_kev
from regscale.integrations.scanner_integration import IntegrationAsset, IntegrationFinding, ScannerIntegration
from regscale.models import IssueStatus, Metadata, regscale_models
from regscale.models.app_models.mapping import Mapping
from regscale.models.regscale_models import Asset, File, Issue, Vulnerability

DT_FORMAT = "%Y-%m-%d"


class FlatFileIntegration(ScannerIntegration):
    title = "Flat File Integration"
    # Required fields from ScannerIntegration
    asset_identifier_field = "name"
    finding_severity_map = {
        "Critical": regscale_models.IssueSeverity.High,
        "High": regscale_models.IssueSeverity.High,
        "Medium": regscale_models.IssueSeverity.Moderate,
        "Low": regscale_models.IssueSeverity.Low,
    }
    type = ScannerIntegration.type.CONTROL_TEST

    def fetch_assets(self, *args: Any, **kwargs: Any) -> Iterator[IntegrationAsset]:
        """
        Fetches assets from FlatFileImporter

        :param Tuple args: Additional arguments
        :param dict kwargs: Additional keyword arguments
        :yields: Iterator[IntegrationAsset]
        """
        integration_assets = kwargs.get("integration_assets")
        for asset in integration_assets:
            yield asset

    def fetch_findings(self, *args: Tuple, **kwargs: dict) -> Iterator[IntegrationFinding]:
        """
        Fetches findings from the integration

        :param Tuple args: Additional arguments
        :param dict kwargs: Additional keyword arguments
        :yields: Iterator[IntegrationFinding]

        """
        integration_findings = kwargs.get("integration_findings")
        for vuln in integration_findings:
            yield vuln


class FlatFileImporter(ABC):
    """
    Abstract class for container scan integration

    :param dict **kwargs: Keyword arguments
    """

    name: str
    mapping: "Mapping"

    def __init__(self, **kwargs: dict):
        self.finding_severity_map = {
            "Critical": regscale_models.IssueSeverity.High,
            "High": regscale_models.IssueSeverity.High,
            "Medium": regscale_models.IssueSeverity.Moderate,
            "Low": regscale_models.IssueSeverity.Low,
        }
        # empty generator
        self.integration_assets: Generator[IntegrationAsset, None, None] = (x for x in [])
        self.integration_findings: Generator[IntegrationAsset, None, None] = (x for x in [])
        self.field_names = [
            "logger",
            "headers",
            "file_type",
            "app",
            "file_path",
            "name",
            "parent_id",
            "parent_module",
            "scan_date",
            "asset_func",
            "vuln_func",
            "issue_func",
            "extra_headers_allowed",
            "mapping",
            "ignore_validation",
            "header_line_number",
            "regscale_ssp_id",
            "plan_id",
            "disable_mapping",
            "mappings_path",
        ]
        _attributes = namedtuple(
            "Attributes",
            self.field_names,
            defaults=[None] * len(self.field_names),
        )
        self.attributes = _attributes(**kwargs)

        self.file_type = kwargs.get("file_type", ".csv")
        self.extra_headers_allowed = kwargs.get("extra_headers_allowed", False)
        self.scan_date = kwargs.get("scan_date", datetime.now()).date()
        self.attributes.logger.info("Processing %s...", self.attributes.file_path)
        self.formatted_headers = None
        self.config = self.attributes.app.config
        self.cisa_kev = pull_cisa_kev()
        self.header, self.file_data = self.file_to_list_of_dicts()
        self.data = {
            "assets": [],
            "issues": [],
            "scans": [],
            "vulns": [],
        }
        self.create_epoch = str(int(creation_date(self.attributes.file_path)))
        self.create_assets(kwargs["asset_func"])  # type: ignore # Pass in the function to create an asset
        flat_int = FlatFileIntegration(plan_id=self.attributes.parent_id)
        flat_int.title = self.attributes.name
        flat_int.num_findings_to_process = len(self.data["vulns"])
        flat_int.num_assets_to_process = len(self.data["assets"])
        flat_int.sync_assets(
            plan_id=self.attributes.parent_id,
            integration_assets=self.integration_assets,
            title=self.attributes.name,
        )
        self.create_vulns(kwargs["vuln_func"])  # type: ignore # Pass in the function to create a vuln
        flat_int.sync_findings(
            plan_id=self.attributes.parent_id,
            integration_findings=self.integration_findings,
            title=self.attributes.name,
            enable_finding_date_update=True,
            scan_date=self.scan_date,
        )
        self.clean_up()

    def parse_finding(self, vuln: Vulnerability) -> Optional[IntegrationFinding]:
        """
        Parses a vulnerability object into an IntegrationFinding object

        :param Vulnerability vuln: A vulnerability object
        :return: The parsed IntegrationFinding or None if parsing fails
        :rtype: Optional[IntegrationFinding]
        """
        try:
            asset_id = vuln.dns or vuln.ipAddress
            if not asset_id:
                return None

            severity = self.finding_severity_map.get(vuln.severity.capitalize(), regscale_models.IssueSeverity.Low)
            status = self.map_status_to_issue_status(vuln.status)
            cve: Optional[str] = vuln.cve if vuln.cve else ""
            extract_vuln: Any = self.extract_ghsa_strings(vuln.plugInName or "")
            plugin_name = vuln.plugInName if vuln.plugInName else vuln.title
            if not self.assert_valid_cve(cve):
                if isinstance(extract_vuln, list):
                    cve = ", ".join(extract_vuln)
                if isinstance(extract_vuln, str):
                    # Coalfire requires vulnerabilities to be stuffed into this field, regardless if they start
                    # with CVE or not.
                    cve = extract_vuln
            if not self.assert_valid_cve(cve):
                plugin_name = cve
                cve = ""
            #  get_value(vuln, "vulnerableAsset.name")
            return IntegrationFinding(
                control_labels=[],  # Add an empty list for control_labels
                category=f"{self.name} Vulnerability",  # Add a default category
                title=vuln.title,
                description=vuln.description,
                severity=severity,
                status=status,
                asset_identifier=asset_id,
                external_id=str(vuln.plugInId),
                rule_id=str(vuln.plugInId),
                first_seen=vuln.firstSeen,
                last_seen=vuln.lastSeen,
                remediation=vuln.extra_data.get("solution"),
                cvss_score=vuln.vprScore,
                cve=cve,
                cvs_sv3_base_score=vuln.cvsSv3BaseScore,
                source_rule_id=str(vuln.plugInId),
                vulnerability_type="Vulnerability Scan",
                baseline=f"{self.name} Host",
                results=vuln.title,
                plugin_name=plugin_name,
                date_created=vuln.firstSeen,
                date_last_updated=vuln.lastSeen,
            )
        except (KeyError, TypeError, ValueError) as e:
            self.attributes.logger.error("Error parsing Wiz finding: %s", str(e), exc_info=True)
            return None

    def parse_asset(self, asset: Asset) -> IntegrationAsset:
        """
        Converts Asset -> IntegrationAsset

        :param Asset asset: The asset to parse
        :return: The parsed IntegrationAsset
        :rtype: IntegrationAsset
        """
        return IntegrationAsset(
            name=asset.name,
            external_id=asset.otherTrackingNumber,
            other_tracking_number=asset.otherTrackingNumber,
            identifier=asset.name,
            asset_type=asset.assetType,
            asset_owner_id=asset.assetOwnerId,
            parent_id=self.attributes.parent_id,
            parent_module=regscale_models.SecurityPlan.get_module_slug(),
            asset_category=asset.assetCategory,
            date_last_updated=asset.dateLastUpdated,
            status=asset.status,
            ip_address=asset.ipAddress if asset.ipAddress else "Unknown",
            software_vendor=asset.softwareVendor,
            software_version=asset.softwareVersion,
            software_name=asset.softwareName,
            location=asset.location,
            notes=asset.notes,
            model=asset.model,
            serial_number=asset.serialNumber,
            is_public_facing=False,
            azure_identifier=asset.azureIdentifier,
            mac_address=asset.macAddress,
            fqdn=asset.fqdn,
            disk_storage=0,
            cpu=0,
            ram=0,
            operating_system=asset.operatingSystem,
            os_version=asset.osVersion,
            end_of_life_date=asset.endOfLifeDate,
            vlan_id=asset.vlanId,
            uri=asset.uri,
            aws_identifier=asset.awsIdentifier,
            google_identifier=asset.googleIdentifier,
            other_cloud_identifier=asset.otherCloudIdentifier,
            patch_level=asset.patchLevel,
            cpe=asset.cpe,
            component_names=[],
            source_data=None,
            url=None,
            ports_and_protocols=[],
            software_inventory=asset.extra_data.get("software_inventory", []),
        )

    @staticmethod
    def create_asset_type(asset_type: str) -> str:
        """
        Create asset type if it does not exist and reformat the string to Title Case

        :param str asset_type: The asset to parse
        :return: Asset type in title case
        :rtype: str
        """
        #
        asset_type = asset_type.title().replace("_", " ")
        meta_data_list = Metadata.get_metadata_by_module_field(module="assets", field="Asset Type")
        if not any(meta_data.value == asset_type for meta_data in meta_data_list):
            Metadata(
                field="Asset Type",
                module="assets",
                value=asset_type,
            ).create()
        return asset_type

    def file_to_list_of_dicts(self) -> tuple[Optional[Sequence[str]], list[Any]]:
        """
        Converts a csv file to a list of dictionaries

        :raises AssertionError: If the headers in the csv/xlsx file do not match the expected headers
        :return: Tuple of header and data from csv file
        :rtype: tuple[Optional[Sequence[str]], list[Any]]
        """
        header = []
        data = []
        start_line_number = 0 if not self.attributes.header_line_number else self.attributes.header_line_number
        with open(self.attributes.file_path, encoding="utf-8-sig") as file:
            # Skip lines until the start line is reached
            for _ in range(start_line_number):
                next(file)
            if file.name.endswith(".csv"):
                data, header = self.convert_csv_to_dict(file)
            elif file.name.endswith(".xlsx"):
                data, header = self.convert_xlsx_to_dict(file)
            elif file.name.endswith(".json"):
                try:
                    # Filter possible null values
                    file_data = json.load(file)
                    if isinstance(file_data, dict):
                        data = file_data
                    if isinstance(file_data, list):
                        data = [dat for dat in file_data if dat]
                except json.JSONDecodeError:
                    raise AssertionError("Invalid JSON file")
            elif file.name.endswith(".xml"):
                data = self.convert_xml_to_dict(file)
            else:
                raise AssertionError("Unsupported file type")
        return header, data

    def handle_extra_headers(self, header: list) -> None:
        """
        Handle extra headers in the csv file

        :param list header: The headers from the csv file
        :raises AssertionError: If the headers in the csv file do not contain the required headers
        """
        extra_headers = [column for column in header if column not in self.attributes.headers]
        required_headers = [column for column in header if column in self.attributes.headers]

        if not all(item in self.attributes.headers for item in required_headers):
            raise AssertionError(
                "The headers in the csv file do not contain the required headers "
                + f"headers, is this a valid {self.attributes.name} {self.file_type} file?"
            )

        if extra_headers:
            self.attributes.logger.warning(
                "The following extra columns were found and will be ignored: %s",
                ", ".join(extra_headers),
            )

    def convert_csv_to_dict(self, file: TextIO) -> tuple:
        """
        Converts a csv file to a list of dictionaries

        :param TextIO file: The csv file to convert
        :return: Tuple of header and data from csv file
        :rtype: tuple
        """
        # if file is empty, error and exit
        if not file.read(1):
            error_and_exit("File is empty")
        # Rewind file and skip lines until the start line is reached
        file.seek(0)
        for _ in range(getattr(self.attributes, "header_line_number", 0) or 0):
            next(file)
        reader = csv.DictReader(file)

        header = [head for head in list(reader.fieldnames) if head]

        if self.extra_headers_allowed:
            self.handle_extra_headers(header=header)

        data = list(reader)
        return data, header

    def convert_xlsx_to_dict(self, file: TextIO) -> tuple:
        """
        Converts a xlsx file to a list of dictionaries

        :param TextIO file: The xlsx file to convert
        :return: Tuple of data and header from xlsx file
        :rtype: tuple
        """
        # Load the workbook
        workbook = load_workbook(filename=file.name)

        # Select the first sheet
        sheet = workbook.active

        # Get the data from the sheet
        data = list(sheet.values)

        # Get the header from the first row
        header = list(data[0])

        # Get the rest of the data
        data = data[1:]

        # Convert the data to a dictionary
        data_dict = [dict(zip(header, row)) for row in data]

        # Loop through the data and convert any string lists to lists
        for dat in data_dict:
            for key, val in dat.items():
                if isinstance(val, str) and val.startswith("["):
                    try:
                        dat[key] = ast.literal_eval(dat[key])
                    except SyntaxError as rex:
                        # Object is probably not a list, so just leave it as a string
                        self.attributes.app.logger.debug("SyntaxError: %s", rex)
        return data_dict, header

    def count_vuln_by_severity(self, severity: str, asset_id: int) -> int:
        """
        Count the number of vulnerabilities by the provided severity

        :param str severity: The severity to count
        :param int asset_id: The asset id to match the vulnerability's parentId
        :return: The number of vulnerabilities
        :rtype: int
        """
        return len([vuln for vuln in self.data["vulns"] if vuln.parentId == asset_id and vuln.severity == severity])

    def create_assets(self, func: Callable) -> None:
        """
        Create assets in RegScale from csv file

        :param Callable func: Function to create asset
        :return: None
        :rtype: None
        """
        self.process_assets(func=func)

    def process_assets(self, func: Callable) -> None:
        """
        Process the assets in the data
        """
        # The passed function creates asset objects. Convert to IntegrationAsset here
        if isinstance(self.file_data, list):
            for dat in self.file_data:
                self.process_asset_data(dat, func)
        elif isinstance(self.file_data, dict):
            self.data["assets"] = func(self.file_data)
        self.integration_assets = (self.parse_asset(asset) for asset in self.data["assets"])

    def process_asset_data(self, dat: Any, func: Callable) -> None:
        """
        Process the asset data

        :param Any dat: The data to process
        :param Callable func: The function to process the data
        :rtype: None
        """

        res = func(dat)
        if not res:
            return
        if isinstance(res, Asset) and res not in self.data["assets"]:
            self.data["assets"].append(res)
        elif isinstance(res, list):
            for asset in res:
                if asset not in self.data["assets"]:
                    self.data["assets"].append(asset)

    @staticmethod
    def check_status_codes(response_list: list) -> None:
        """
        Check if any of the responses are not 200

        :param list response_list: List of responses
        :raises AssertionError: If any of the responses are not 200
        :rtype: None
        """
        for response in response_list:
            if isinstance(response, requests.Response) and response.status_code != 200:
                raise AssertionError(
                    f"Unable to {response.request.method} asset to RegScale.\n"
                    f"Code: {response.status_code}\nReason: {response.reason}"
                    f"\nPayload: {response.text}"
                )

    def lookup_kev(self, cve: str) -> str:
        """
        Determine if the cve is part of the published CISA KEV list

        :param str cve: The CVE to lookup.
        :return: A string containing the KEV CVE due date.
        :rtype: str
        """
        kev_data = None
        kev_date = None
        if self.cisa_kev:
            try:
                # Update kev and date
                kev_data = next(
                    dat
                    for dat in self.cisa_kev["vulnerabilities"]  # type: ignore
                    if "vulnerabilities" in self.cisa_kev and cve and dat["cveID"].lower() == cve.lower()
                )
            except (StopIteration, ConnectionRefusedError):
                kev_data = None
        if kev_data:
            # Convert YYYY-MM-DD to datetime
            kev_date = convert_datetime_to_regscale_string(datetime.strptime(kev_data["dueDate"], DT_FORMAT))
        return kev_date

    def update_due_dt(self, iss: Issue, kev_due_date: Optional[str], scanner: str, severity: str) -> Issue:
        """
        Find the due date for the issue

        :param Issue iss: RegScale Issue object
        :param Optional[str] kev_due_date: The KEV due date
        :param str scanner: The scanner
        :param str severity: The severity of the issue
        :return: RegScale Issue object
        :rtype: Issue
        """
        fmt = "%Y-%m-%d %H:%M:%S"
        days = 30
        if severity == "medium":
            severity = "moderate"
        if severity == "important":
            severity = "high"
        if severity not in ["low", "moderate", "high", "critical"]:
            # An odd severity should be treated as low.
            severity = "low"
        try:
            days = self.attributes.app.config["issues"][scanner][severity]
        except KeyError:
            self.attributes.logger.error(
                "Unable to find severity '%s'\n defaulting to %i days\nPlease add %s to the init.yaml configuration",
                severity,
                days,
                severity,
            )
        if kev_due_date and (datetime.strptime(kev_due_date, fmt) > datetime.now()):
            iss.dueDate = kev_due_date
        else:
            iss.dueDate = datetime.strftime(
                datetime.now() + timedelta(days=days),
                fmt,
            )
        return iss

    def _check_issue(self, issue: Issue) -> None:
        """
        Check if the issue is in the data

        :param Issue issue: The issue to check to prevent duplicates
        :rtype: None
        """
        if issue and issue not in self.data["issues"]:
            self.data["issues"].append(issue)

    def _check_issues(self, issues: List[Issue]) -> None:
        """
        Check if the issues are in the data

        :param List[Issue] issues: The issues to check to prevent duplicates
        """
        for issue in issues:
            self._check_issue(issue)

    def check_and_close_issues(self, existing_issues: list[Issue]) -> None:
        """
        Function to close issues that are no longer being reported in the export file

        :param list[Issue] existing_issues: List of existing issues in RegScale
        :rtype: None
        """
        existing_cves = self.group_issues_by_cve_id(existing_issues)
        parsed_cves = {issue.cve for issue in self.data["issues"] if issue.cve}
        closed_issues = []
        with create_progress_object() as close_issue_progress:
            closing_issues = close_issue_progress.add_task(
                "Comparing parsed issue(s) and existing issue(s)...",
                total=len(existing_cves),
            )
            for cve, issues in existing_cves.items():
                if cve not in parsed_cves:
                    for issue in issues:
                        if issue.status == "Closed":
                            continue
                        self.attributes.logger.debug("Closing issue #%s", issue.id)
                        issue.status = "Closed"
                        issue.dateCompleted = self.scan_date.strftime("%Y-%m-%d %H:%M:%S")
                        if issue.save():
                            self.attributes.logger.debug("Issue #%s closed", issue.id)
                            closed_issues.append(issue)
                close_issue_progress.advance(closing_issues, advance=1)
        self.log_and_save_closed_issues(closed_issues)

    @staticmethod
    def group_issues_by_cve_id(existing_issues: list[Issue]) -> dict[str, list[Issue]]:
        """
        Function to group existing issues from RegScale by cve and returns a dictionary of cveId and issues

        :param list[Issue] existing_issues: List of existing issues in RegScale
        :returns: A dictionary of cveId and list of issues with the same cveId
        :rtype: dict[str, list[Issue]]
        """
        from collections import defaultdict

        # create a dict with an empty list for each cve, so we can close issues that have duplicate CVEs
        existing_cves = defaultdict(list)
        # group issues by cve
        for issue in existing_issues:
            if issue.cve:
                existing_cves[issue.cve].append(issue)
        return existing_cves

    def log_and_save_closed_issues(self, closed_issues: list[Issue]) -> None:
        """
        Log and save the closed issues if any

        :param list[Issue] closed_issues: List of closed issues to log and save
        :rtype: None
        """
        if len(closed_issues) > 0:
            self.attributes.logger.info("Closed %i issue(s) in RegScale.", len(closed_issues))
            ReportGenerator(
                objects=closed_issues,
                to_file=True,
                report_name=f"{self.attributes.name}_closed_issues",
                regscale_id=self.attributes.parent_id,
                regscale_module=self.attributes.parent_module,
            )

    def create_vulns(self, func: Callable) -> None:
        """
        Create vulns in RegScale from csv file

        :param Callable func: Function to create vuln
        :rtype: None
        """

        def check_vuln(vuln_to_check: Vulnerability) -> None:
            """
            Check if the vuln is in the data

            :param Vulnerability vuln_to_check: The vulnerability to check to prevent duplicates
            :rtype: None
            """
            if (vuln_to_check and vuln_to_check not in self.data["vulns"]) and hasattr(vuln_to_check, "id"):
                self.data["vulns"].append(vuln_to_check)

        with create_progress_object() as vuln_progress:
            vuln_task = vuln_progress.add_task("Processing vulnerabilities...", total=len(self.file_data))
            for ix, dat in enumerate(self.file_data):
                vuln = func(dat, index=ix)
                if not vuln:
                    vuln_progress.advance(vuln_task, advance=1)
                    continue
                if isinstance(vuln, Vulnerability):
                    check_vuln(vuln)
                if isinstance(vuln, list):
                    for v in vuln:
                        check_vuln(v)
                vuln_progress.advance(vuln_task, advance=1)
        self.integration_findings = (self.parse_finding(vuln) for vuln in self.data["vulns"])

    def clean_up(self) -> None:
        """
        Move the Nexpose file to the processed folder

        :rtype: None
        """
        if self.attributes.parent_id:
            file_path = Path(self.attributes.file_path)
            processed_dir = file_path.parent / "processed"
            check_file_path(str(processed_dir.absolute()))
            api = Api()
            file_name = (f"{file_path.stem}_" + f"{get_current_datetime('%Y%m%d-%I%M%S%p')}").replace(" ", "_")
            # Rename to friendly file name and post to Regscale
            new_name = (file_path.parent / file_name).with_suffix(file_path.suffix)
            new_file_path = file_path.rename(new_name)
            try:
                self.attributes.logger.info(
                    "Renaming %s to %s, and uploading it to RegScale...",
                    file_path.name,
                    new_file_path.name,
                )
                File.upload_file_to_regscale(
                    file_name=str(new_file_path.absolute()),
                    parent_id=self.attributes.parent_id,
                    parent_module=self.attributes.parent_module,
                    api=api,
                )
                shutil.move(new_file_path, processed_dir)
                self.attributes.logger.info("File uploaded to RegScale and moved to %s", processed_dir)
            except shutil.Error:
                self.attributes.logger.debug(
                    "File %s already exists in %s",
                    new_file_path.name,
                    processed_dir,
                )

    @abstractmethod
    def create_asset(self):
        """Create an asset"""

    @abstractmethod
    def create_vuln(self):
        """Create a Vulnerability"""

    @classmethod
    def common_scanner_options(cls, message: str, prompt: str, import_name: str) -> Callable[[Callable], click.option]:
        """
        Common options for container scanner integrations

        :param str message: The message to display to the user
        :param str prompt: The prompt to display to the user
        :param str import_name: The name of the import function
        :return: The decorated function
        :rtype: Callable[[Callable], click.option]
        """
        import os

        mapping_dir = os.path.join("./", "mappings", import_name)

        def decorator(this_func) -> Callable[[Callable], click.option]:
            """
            Decorator for common options
            """
            this_func = click.option(
                "--folder_path",
                "-f",
                help=message,
                prompt=prompt,
                required=True,
                type=click.Path(exists=True, dir_okay=True, resolve_path=True),
            )(this_func)
            this_func = click.option(
                "--regscale_ssp_id",
                "-id",
                type=click.INT,
                help="The ID number from RegScale of the System Security Plan.",
                prompt="Enter RegScale System Security Plan ID",
                required=True,
            )(this_func)
            this_func = click.option(
                "--scan_date",
                "-sd",
                type=click.DateTime(formats=[DT_FORMAT]),
                help="The scan date of the file.",
                required=False,
            )(this_func)
            this_func = click.option(
                "--mappings_path",
                "-m",
                type=click.Path(dir_okay=True, resolve_path=True),
                help=f"The CLI will use the custom header from the provided mappings directory or file, example is {mapping_dir}",
                default=mapping_dir,
                required=False,
            )(this_func)
            this_func = click.option(
                "--disable_mapping",
                "-dm",
                help="Whether to disable the default mapping",
                is_flag=True,
            )(this_func)
            return this_func

        return decorator

    @classmethod
    def show_mapping(cls, group: click.Group, import_name: str, file_type: Optional[str] = None) -> click.Command:
        """
        Show the mapping for the given import_name

        :param click.Group group: The click group to register the command with
        :param str import_name: The name of the import function
        :param Optional[str] file_type: The file type of the import, defaults to None
        :return: The decorated function.
        :rtype: Callable[[Callable], click.option]
        """
        import os

        # Define default path based on import_name and file_type
        default = os.path.join("./", "mappings", import_name, f"{file_type}_mapping.json") if file_type else None

        @click.command(help=f"Show the mapping file used during {import_name} imports.")
        @click.option(
            "--file_path",
            "-f",
            help="File path to the mapping file to display",
            type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
            required=True,
            default=default if default else None,
        )
        # Define the desired function behavior
        def wrapped_func(file_path: str) -> None:
            """
            Show the mapping file used during imports
            """
            from rich.console import Console

            console = Console()
            with open(file_path, "r", encoding="utf-8") as file:
                mapping = json.load(file)
            dat = json.dumps(mapping, indent=4)
            console.print(f"{file_path} mapping:")
            console.print(dat)

        # Register the decorated function with the given click group
        group.add_command(wrapped_func, name="show_mapping")

    @staticmethod
    def check_date_format(the_date: Any) -> bool:
        """
        Check if the date is in the correct format

        :param Any the_date: The date to check
        :return: True if the date is in the correct format
        :rtype: bool

        """
        try:
            if isinstance(the_date, str):
                the_date = datetime.strptime(the_date, DT_FORMAT)
            # make sure the date is not in the future
            if the_date >= datetime.now():
                error_and_exit("The scan date cannot be in the future.")
            res = True
        except ValueError:
            error_and_exit("Incorrect data format, should be YYYY-MM-DD")
        return res

    @staticmethod
    def convert_xml_to_dict(file: TextIO) -> dict:
        """
        Convert an XML file to a Python dictionary.

        :param TextIO file: The file object representing the XML file.
        :return: A dictionary representation of the XML content.
        :rtype: dict
        """

        xml_content = file.read()
        dict_content = xmltodict.parse(xml_content)
        return dict_content

    @staticmethod
    def determine_severity(s: str) -> str:
        """
        Determine the CVSS severity of the vulnerability

        :param str s: The severity
        :return: The severity
        :rtype: str
        """
        severity = "info"
        if s:
            severity = s.lower()
        # remap crits to highs
        if severity == "critical":
            severity = "high"
        return severity

    @staticmethod
    def map_status_to_issue_status(status: str) -> IssueStatus:
        """
        Maps the vuln status to issue status
        :param str status: Status of the vulnerability
        :returns: Issue status
        :rtype: IssueStatus
        """
        issue_status = IssueStatus.Open
        if status.lower() in ["resolved", "rejected", "closed", "completed"]:
            issue_status = IssueStatus.Closed
        return issue_status

    @staticmethod
    def extract_ghsa_strings(text: str) -> Union[List[str], str]:
        """
        Extract GHSA strings from a given text.

        :param str text: The input text containing GHSA strings
        :return: A list of GHSA strings or the input text if no GHSA strings are found
        :rtype: Union[List[str], str]
        """
        ghsa_pattern = r"GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}"
        res = re.findall(ghsa_pattern, text)
        if res:
            return res
        return text

    @staticmethod
    def assert_valid_cve(cve: str) -> bool:
        """
        Assert that the CVE identifier is valid

        :param str cve: The CVE identifier
        :return: True if the CVE identifier is valid
        :rtype: bool
        """
        pattern = r"^CVE-\d{4}-\d{4,}$"
        return bool(re.match(pattern, cve))
