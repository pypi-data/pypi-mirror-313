import codecs
import csv
import datetime
import json
import logging
import time
import traceback
from contextlib import closing
from typing import Dict, List, Any, Optional
from zipfile import ZipFile

import cachetools
import requests
from pydantic import ValidationError

from regscale.core.app.api import Api
from regscale.core.app.utils.app_utils import (
    error_and_exit,
    check_file_path,
    get_current_datetime,
    format_dict_to_html,
    create_progress_object,
)
from regscale.core.utils.date import datetime_obj
from regscale.integrations.commercial.wizv2.constants import (
    DOWNLOAD_QUERY,
    BEARER,
    REPORTS_QUERY,
    CONTENT_TYPE,
    RATE_LIMIT_MSG,
    CREATE_REPORT_QUERY,
    MAX_RETRIES,
    CHECK_INTERVAL_FOR_DOWNLOAD_REPORT,
)
from regscale.integrations.commercial.wizv2.variables import WizVariables
from regscale.integrations.commercial.wizv2.wiz_auth import wiz_authenticate
from regscale.models import File, Sbom, SecurityPlan, Catalog, ControlImplementation, Assessment, regscale_models
from regscale.integrations.commercial.wizv2.models import ComplianceReport, ComplianceCheckStatus
from regscale.utils import PaginatedGraphQLClient
from regscale.utils.decorators import deprecated

logger = logging.getLogger("rich")
compliance_job_progress = create_progress_object()


def get_notes_from_wiz_props(wiz_entity_properties: Dict, external_id: str) -> str:
    """
    Get notes from wiz properties
    :param Dict wiz_entity_properties: Wiz entity properties
    :param str external_id: External ID
    :return: Notes
    :rtype: str
    """
    notes = []
    notes.append(f"External ID: {external_id}") if external_id else None
    (
        notes.append(f"Cloud Platform: {wiz_entity_properties.get('cloudPlatform')}")
        if wiz_entity_properties.get("cloudPlatform")
        else None
    )
    (
        notes.append(f"Provider Unique ID: {wiz_entity_properties.get('providerUniqueId')}")
        if wiz_entity_properties.get("providerUniqueId")
        else None
    )
    (
        notes.append(
            f"""cloudProviderURL:<a href="{wiz_entity_properties.get("cloudProviderURL")}"
                            target="_blank">{wiz_entity_properties.get("cloudProviderURL")}</a>"""
        )
        if wiz_entity_properties.get("cloudProviderURL")
        else None
    )
    (
        notes.append(f"Vertex ID: {wiz_entity_properties.get('_vertexID')}")
        if wiz_entity_properties.get("_vertexID")
        else None
    )
    (
        notes.append(f"Severity Name: {wiz_entity_properties.get('severity_name')}")
        if wiz_entity_properties.get("severity_name")
        else None
    )
    (
        notes.append(f"Severity Description: {wiz_entity_properties.get('severity_description')}")
        if wiz_entity_properties.get("severity_description")
        else None
    )
    return "<br>".join(notes)


def handle_management_type(wiz_entity_properties: Dict) -> str:
    """
    Handle management type
    :param Dict wiz_entity_properties: Wiz entity properties
    :return: Management type
    :rtype: str
    """
    return "External/Third Party Managed" if wiz_entity_properties.get("isManaged") else "Internally Managed"


@cachetools.cached(cachetools.TTLCache(maxsize=1024, ttl=3600))
def create_asset_type(asset_type: str) -> str:
    """
    Create asset type if it does not exist and reformat the string to Title Case ie
        ( "ASSET_TYPE" or "asset_type" -> "Asset Type")
    :param asset_type str Asset_type
    :return: Asset type
    :rtype: str
    """
    #
    asset_type = asset_type.title().replace("_", " ")
    meta_data_list = regscale_models.Metadata.get_metadata_by_module_field(module="assets", field="Asset Type")
    if not any(meta_data.value == asset_type for meta_data in meta_data_list):
        regscale_models.Metadata(
            field="Asset Type",
            module="assets",
            value=asset_type,
        ).create()
    return asset_type


def map_category(asset_string: str) -> regscale_models.AssetCategory:
    """
    category mapper

    :param str asset_string:
    :return: Category
    :rtype: regscale_models.AssetCategory
    """
    try:
        if asset_string in ["CONTAINER_IMAGE"]:
            return regscale_models.AssetCategory.Software
        return getattr(regscale_models.AssetCategory, asset_string)
    except (KeyError, AttributeError) as ex:
        # why map AssetCategory of everything is software?
        logger.debug("Unable to find %s in AssetType enum \n", ex)
        return regscale_models.AssetCategory.Hardware


def convert_first_seen_to_days(first_seen: str) -> int:
    """
    Converts the first seen date to days
    :param str first_seen: First seen date
    :returns: Days
    :rtype: int
    """
    first_seen_date = datetime_obj(first_seen)
    if not first_seen_date:
        return 0
    first_seen_date_naive = first_seen_date.replace(tzinfo=None)
    return (datetime.datetime.now() - first_seen_date_naive).days


def fetch_report_by_id(
    report_id: str, parent_id: int, report_file_name: str = "evidence_report", report_file_extension: str = "csv"
):
    """
    Fetch report by id and add it to evidence

    :param str report_id: Wiz report ID
    :param int parent_id: RegScale Parent ID
    :param str report_file_name: Report file name, defaults to "evidence_report"
    :param str report_file_extension: Report file extension, defaults to "csv"
    :rtype: None
    """

    current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file_path = f"artifacts/{report_file_name}_{current_datetime}.{report_file_extension}"
    variables = {"reportId": report_id}
    api_endpoint_url = WizVariables.wizUrl
    token = WizVariables.wizAccessToken
    if not token:
        error_and_exit("Wiz Access Token is missing. Authenticate with Wiz first.")
    client = PaginatedGraphQLClient(
        endpoint=api_endpoint_url,
        query=DOWNLOAD_QUERY,
        headers={
            "Content-Type": "application/json",
            "Authorization": BEARER + token,
        },
    )
    downloaded_report = client.fetch_results(variables=variables)
    logger.debug(f"Download Report result: {downloaded_report}")
    if "errors" in downloaded_report:
        logger.error(f"Error fetching report: {downloaded_report['errors']}")
        logger.error(f"Raw Response Data: {downloaded_report}")
        return

    if download_url := downloaded_report.get("report", {}).get("lastRun", {}).get("url"):
        logger.info(f"Download URL: {download_url}")
        download_file(url=download_url, local_filename=report_file_path)
        api = Api()
        _ = File.upload_file_to_regscale(
            file_name=str(report_file_path),
            parent_id=parent_id,
            parent_module="evidence",
            api=api,
        )
        logger.info("File uploaded successfully")
    else:
        logger.error("Could not retrieve the download URL.")


def download_file(url, local_filename="artifacts/test_report.csv"):
    """
    Download a file from a URL and save it to the local file system.

    :param url: The URL of the file to download.
    :param local_filename: The local path where the file should be saved.
    :return: None
    """

    check_file_path("artifacts")
    with requests.get(url, stream=True) as response:
        response.raise_for_status()  # Check if the request was successful
        with open(local_filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
                file.write(chunk)
    logger.info(f"File downloaded successfully and saved to {local_filename}")


def fetch_sbom_report(
    report_id: str,
    parent_id: str,
    report_file_name: str = "sbom_report",
    report_file_extension: str = "zip",
    standard="CycloneDX",
):
    """
    Fetch report by id and add it to evidence

    :param str report_id: Wiz report ID
    :param str parent_id: RegScale Parent ID
    :param str report_file_name: Report file name, defaults to "evidence_report"
    :param str report_file_extension: Report file extension, defaults to "zip"
    :param str standard: SBOM standard, defaults to "CycloneDX"
    :rtype: None
    """

    current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file_path = f"artifacts/{report_file_name}_{current_datetime}.{report_file_extension}"
    variables = {"reportId": report_id}
    api_endpoint_url = WizVariables.wizUrl
    token = WizVariables.wizAccessToken
    if not token:
        error_and_exit("Wiz Access Token is missing. Authenticate with Wiz first.")
    client = PaginatedGraphQLClient(
        endpoint=api_endpoint_url,
        query=DOWNLOAD_QUERY,
        headers={
            "Content-Type": "application/json",
            "Authorization": BEARER + token,
        },
    )
    download_report = client.fetch_results(variables=variables)
    logger.debug(f"Download Report result: {download_report}")
    if "errors" in download_report:
        logger.error(f"Error fetching report: {download_report['errors']}")
        logger.error(f"Raw Response Data: {download_report}")
        return
    report_data = None
    if download_url := download_report.get("report", {}).get("lastRun", {}).get("url"):
        logger.info(f"Download URL: {download_url}")
        download_file(url=download_url, local_filename=report_file_path)
        with ZipFile(report_file_path, "r") as zObject:
            for filename in zObject.namelist():
                with zObject.open(filename) as json_f:
                    file_name = ".".join(filename.split(".")[:-1])
                    report_data = json.load(json_f)
                    sbom_standard = report_data.get("bomFormat", standard)
                    standard_version = report_data.get("specVersion", 1.5)
                    Sbom(
                        name=file_name,
                        tool="Wiz",
                        parentId=int(parent_id),
                        parentModule=SecurityPlan.get_module_slug(),
                        results=json.dumps(report_data),
                        standardVersion=standard_version,
                        sbomStandard=sbom_standard,
                    ).create_or_update(
                        bulk_update=True
                    )  # need put in for this endpoint to update SBOMS

        logger.info("SBOM attached successfully!")
    else:
        logger.error("Could not retrieve the download URL.")


@deprecated("Use the 'fetch_report_by_id' command instead.")
def fetch_report_id(query: str, variables: Dict, url: str) -> str:
    """
    Fetch report ID from Wiz

    :param str query: Query string
    :param Dict variables: Variables
    :param str url: Wiz URL
    :return str: Wiz ID
    :rtype str: str
    """
    try:
        resp = send_request(
            query=query,
            variables=variables,
            api_endpoint_url=url,
        )
        if "error" in resp.json().keys():
            error_and_exit(f'Wiz Error: {resp.json()["error"]}')
        return resp.json()["data"]["createReport"]["report"]["id"]
    except (requests.RequestException, AttributeError, TypeError) as rex:
        logger.error("Unable to pull report id from requests object\n%s", rex)
    return ""


def get_framework_names(wiz_frameworks: List) -> List:
    """
    Get the names of frameworks and replace spaces with underscores.

    :param List wiz_frameworks: List of Wiz frameworks.
    :return List: List of framework names.
    :rtype List: list
    """
    return [framework["name"].replace(" ", "_") for framework in wiz_frameworks]


def check_reports_for_frameworks(reports: List, frames: List) -> bool:
    """
    Check if any reports contain the given frameworks.

    :param List reports: List of reports.
    :param List frames: List of framework names.
    :return bool: Boolean indicating if any report contains a framework.
    :rtype bool: bool
    """
    return any(frame in item["name"] for item in reports for frame in frames)


def create_report_if_needed(
    wiz_project_id: str, frames: List, wiz_frameworks: List, reports: List, snake_framework: str
) -> List:
    """
    Create a report if needed and return report IDs.

    :param str wiz_project_id: Wiz Project ID.
    :param List frames: List of framework names.
    :param List wiz_frameworks: List of Wiz frameworks.
    :param List reports: List of reports.
    :param str snake_framework: Framework name with spaces replaced by underscores.
    :return List: List of Wiz report IDs.
    :rtype List: list
    """
    if not check_reports_for_frameworks(reports, frames):
        selected_frame = snake_framework
        selected_index = frames.index(selected_frame)
        wiz_framework = wiz_frameworks[selected_index]
        wiz_report_id = create_compliance_report(
            wiz_project_id=wiz_project_id,
            report_name=f"{selected_frame}_project_{wiz_project_id}",
            framework_id=wiz_framework.get("id"),
        )
        logger.info(f"Wiz compliance report created with ID {wiz_report_id}")
        return [wiz_report_id]

    return [report["id"] for report in reports if any(frame in report["name"] for frame in frames)]


def fetch_and_process_report_data(wiz_report_ids: List) -> List:
    """
    Fetch and process report data from report IDs.

    :param List wiz_report_ids: List of Wiz report IDs.
    :return List: List of processed report data.
    :rtype List: List
    """
    report_data = []
    for wiz_report in wiz_report_ids:
        download_url = get_report_url_and_status(wiz_report)
        logger.debug(f"Download url: {download_url}")
        with closing(requests.get(url=download_url, stream=True, timeout=10)) as data:
            logger.info("Download URL fetched. Streaming and parsing report")
            reader = csv.DictReader(codecs.iterdecode(data.iter_lines(), encoding="utf-8"), delimiter=",")
            for row in reader:
                report_data.append(row)
    return report_data


def fetch_framework_report(wiz_project_id: str, snake_framework: str) -> List[Any]:
    """
    Fetch Framework Report from Wiz.

    :param str wiz_project_id: Wiz Project ID.
    :param str snake_framework: Framework name with spaces replaced by underscores.
    :return: List containing the framework report data.
    :rtype: List[Any]
    """
    wiz_frameworks = fetch_frameworks()
    frames = get_framework_names(wiz_frameworks)
    reports = list(query_reports())

    wiz_report_ids = create_report_if_needed(wiz_project_id, frames, wiz_frameworks, reports, snake_framework)
    return fetch_and_process_report_data(wiz_report_ids)


def fetch_frameworks() -> list:
    """
    Fetch frameworks from Wiz

    :raises General Error: If error in API response
    :return: List of frameworks
    :rtype: list
    """
    query = """
        query SecurityFrameworkAutosuggestOptions($policyTypes: [SecurityFrameworkPolicyType!],
        $onlyEnabledPolicies: Boolean) {
      securityFrameworks(
        first: 500
        filterBy: {policyTypes: $policyTypes, enabled: $onlyEnabledPolicies}
      ) {
        nodes {
          id
          name
        }
      }
    }
    """
    variables = {
        "policyTypes": "CLOUD",
        "first": 500,
    }
    resp = send_request(
        query=query,
        variables=variables,
        api_endpoint_url=WizVariables.wizUrl,
    )

    if resp.ok:
        # ["data"]["securityFrameworks"]["nodes"]
        data = resp.json()
        return data.get("data", {}).get("securityFrameworks", {}).get("nodes")
    else:
        error_and_exit(f"Wiz Error: {resp.status_code if resp else None} - {resp.text if resp else 'No response'}")


def query_reports() -> list:
    """
    Query Report table from Wiz

    :return: list object from an API response from Wiz
    :rtype: list
    """

    # The variables sent along with the above query
    variables = {"first": 100, "filterBy": {}}

    res = send_request(
        query=REPORTS_QUERY,
        variables=variables,
        api_endpoint_url=WizVariables.wizUrl,
    )
    result = []
    try:
        if "errors" in res.json().keys():
            error_and_exit(f'Wiz Error: {res.json()["errors"]}')
        json_result = res.json()
        result = json_result.get("data", {}).get("reports", {}).get("nodes")
    except requests.JSONDecodeError:
        error_and_exit(f"Unable to fetch reports from Wiz: {res.status_code}, {res.reason}")
    return result


def send_request(
    query: str,
    variables: Dict,
    api_endpoint_url: Optional[str] = None,
) -> requests.Response:
    """
    Send a graphQL request to Wiz.

    :param str query: Query to use for GraphQL
    :param Dict variables:
    :param Optional[str] api_endpoint_url: Wiz GraphQL URL Default is None
    :raises ValueError: Value Error if the access token is missing from wizAccessToken in init.yaml
    :return requests.Response: response from post call to provided api_endpoint_url
    :rtype requests.Response: requests.Response
    """
    logger.debug("Sending a request to Wiz API")
    api = Api()
    payload = dict({"query": query, "variables": variables})
    if api_endpoint_url is None:
        api_endpoint_url = WizVariables.wizUrl
    if WizVariables.wizAccessToken:
        return api.post(
            url=api_endpoint_url,
            headers={
                "Content-Type": CONTENT_TYPE,
                "Authorization": BEARER + WizVariables.wizAccessToken,
            },
            json=payload,
        )
    raise ValueError("An access token is missing.")


def create_compliance_report(
    report_name: str,
    wiz_project_id: str,
    framework_id: str,
) -> str:
    """Create Wiz compliance report

    :param str report_name: Report name
    :param str wiz_project_id: Wiz Project ID
    :param str framework_id: Wiz Framework ID
    :return str: Compliance Report id
    :rtype str: str
    """
    report_variables = {
        "input": {
            "name": report_name,
            "type": "COMPLIANCE_ASSESSMENTS",
            "csvDelimiter": "US",
            "projectId": wiz_project_id,
            "complianceAssessmentsParams": {"securityFrameworkIds": [framework_id]},
            "emailTargetParams": None,
            "exportDestinations": None,
        }
    }

    return fetch_report_id(CREATE_REPORT_QUERY, report_variables, url=WizVariables.wizUrl)


def get_report_url_and_status(report_id: str) -> str:
    """
    Generate Report URL from Wiz report

    :param str report_id: Wiz report ID
    :raises: requests.RequestException if download failed and exceeded max # of retries
    :return: URL of report
    :rtype: str
    """
    for attempt in range(MAX_RETRIES):
        if attempt:
            logger.info(
                "Report %s is still updating, waiting %.2f seconds", report_id, CHECK_INTERVAL_FOR_DOWNLOAD_REPORT
            )
            time.sleep(CHECK_INTERVAL_FOR_DOWNLOAD_REPORT)

        response = download_report({"reportId": report_id})
        if not response or not response.ok:
            raise requests.RequestException("Failed to download report")

        response_json = response.json()
        errors = response_json.get("errors")
        if errors:
            message = errors[0]["message"]
            if RATE_LIMIT_MSG in message:
                rate = errors[0]["extensions"]["retryAfter"]
                logger.warning("Sleeping %i seconds due to rate limit", rate)
                time.sleep(rate)
                continue

            logger.error(errors)
        else:
            status = response_json.get("data", {}).get("report", {}).get("lastRun", {}).get("status")
            if status == "COMPLETED":
                return response_json["data"]["report"]["lastRun"]["url"]

    raise requests.RequestException("Download failed, exceeding the maximum number of retries")


def download_report(variables: Dict) -> requests.Response:
    """
    Return a download URL for a provided Wiz report id

    :param Dict variables: Variables for Wiz request
    :return: response from Wiz API
    :rtype: requests.Response
    """
    response = send_request(DOWNLOAD_QUERY, variables=variables)
    return response


def _sync_compliance(
    wiz_project_id: str,
    regscale_id: int,
    regscale_module: str,
    include_not_implemented: bool,
    client_id: str,
    client_secret: str,
    catalog_id: int,
    framework: Optional[str] = "NIST800-53R5",
) -> List[ComplianceReport]:
    """
    Sync compliance posture from Wiz to RegScale

    :param str wiz_project_id: Wiz Project ID
    :param int regscale_id: RegScale ID
    :param str regscale_module: RegScale module
    :param bool include_not_implemented: Include not implemented controls
    :param str client_id: Wiz Client ID
    :param str client_secret: Wiz Client Secret
    :param int catalog_id: Catalog ID, defaults to None
    :param Optional[str] framework: Framework, defaults to NIST800-53R5
    :return: List of ComplianceReport objects
    :rtype: List[ComplianceReport]
    """

    logger.info("Syncing compliance from Wiz with project ID %s", wiz_project_id)
    wiz_authenticate(
        client_id=client_id,
        client_secret=client_secret,
    )
    report_job = compliance_job_progress.add_task("[#f68d1f]Fetching Wiz compliance report...", total=1)
    fetch_regscale_data_job = compliance_job_progress.add_task(
        "[#f68d1f]Fetching RegScale Catalog info for framework...", total=1
    )
    logger.info("Fetching Wiz compliance report for project ID %s...", wiz_project_id)
    compliance_job_progress.update(report_job, completed=True, advance=1)

    framework_mapping = {
        "CSF": "NIST CSF v1.1",
        "NIST800-53R5": "NIST SP 800-53 Revision 5",
        "NIST800-53R4": "NIST SP 800-53 Revision 4",
    }
    sync_framework = framework_mapping.get(framework)
    snake_framework = sync_framework.replace(" ", "_")
    logger.info(snake_framework)
    logger.info("Fetching Wiz compliance report for project ID %s", wiz_project_id)
    report_data = fetch_framework_report(wiz_project_id, snake_framework)
    report_models = []
    compliance_job_progress.update(report_job, completed=True, advance=1)

    catalog = Catalog.get_with_all_details(catalog_id=catalog_id)
    controls = catalog.get("controls") if catalog else []
    passing_controls = dict()
    failing_controls = dict()
    controls_to_reports = dict()
    existing_implementations = ControlImplementation.get_existing_control_implementations(parent_id=regscale_id)
    compliance_job_progress.update(fetch_regscale_data_job, completed=True, advance=1)
    logger.info(f"Analyzing ComplianceReport for framework {sync_framework} from Wiz")
    running_compliance_job = compliance_job_progress.add_task(
        "[#f68d1f]Building compliance posture from wiz report...",
        total=len(report_data),
    )
    for row in report_data:
        try:
            cr = ComplianceReport(**row)
            if cr.framework == sync_framework:
                check_compliance(
                    cr,
                    controls,
                    passing_controls,
                    failing_controls,
                    controls_to_reports,
                )
                report_models.append(cr)
                compliance_job_progress.update(running_compliance_job, advance=1)
        except ValidationError as e:
            logger.error(f"Error creating ComplianceReport: {e}")
    try:
        saving_regscale_data_job = compliance_job_progress.add_task("[#f68d1f]Saving RegScale data...", total=1)
        ControlImplementation.create_control_implementations(
            controls=controls,
            parent_id=regscale_id,
            parent_module=regscale_module,
            existing_implementation_dict=existing_implementations,
            full_controls=passing_controls,
            partial_controls={},
            failing_controls=failing_controls,
            include_not_implemented=include_not_implemented,
        )
        create_assessment_from_compliance_report(
            controls_to_reports=controls_to_reports,
            regscale_id=regscale_id,
            regscale_module=regscale_module,
            controls=controls,
        )
        compliance_job_progress.update(saving_regscale_data_job, completed=True, advance=1)

    except Exception as e:
        logger.error(f"Error creating ControlImplementations from compliance report: {e}")
        traceback.print_exc()
    return report_models


def check_compliance(
    cr: ComplianceReport,
    controls: List[Dict],
    passing: Dict,
    failing: Dict,
    controls_to_reports: Dict,
) -> None:
    """
    Check compliance report for against controls

    :param ComplianceReport cr: Compliance Report
    :param List[Dict] controls: Controls List
    :param Dict passing: Passing controls
    :param Dict failing: Failing controls
    :param Dict controls_to_reports: Controls to reports
    :return: None
    :rtype: None
    """
    for control in controls:
        if f"{control.get('controlId').lower()} " in cr.compliance_check.lower():
            _add_controls_to_controls_to_report_dict(control, controls_to_reports, cr)
            if cr.result == ComplianceCheckStatus.PASS.value:
                if control.get("controlId").lower() not in passing:
                    passing[control.get("controlId").lower()] = control
            else:
                if control.get("controlId").lower() not in failing:
                    failing[control.get("controlId").lower()] = control
    _clean_passing_list(passing, failing)


def _add_controls_to_controls_to_report_dict(control: Dict, controls_to_reports: Dict, cr: ComplianceReport) -> None:
    """
    Add controls to dict to process assessments from later

    :param Dict control: Control
    :param Dict controls_to_reports: Controls to reports
    :param ComplianceReport cr: Compliance Report
    :return: None
    :rtype: None
    """
    if control.get("controlId").lower() not in controls_to_reports.keys():
        controls_to_reports[control.get("controlId").lower()] = [cr]
    else:
        controls_to_reports[control.get("controlId").lower()].append(cr)


def _clean_passing_list(passing: Dict, failing: Dict) -> None:
    """
    Clean passing list. Ensures that controls that are passing are not also failing

    :param Dict passing: Passing controls
    :param Dict failing: Failing controls
    :return: None
    :rtype: None
    """
    for control_id in failing:
        if control_id in passing:
            passing.pop(control_id, None)


def create_assessment_from_compliance_report(
    controls_to_reports: Dict, regscale_id: int, regscale_module: str, controls: List
) -> None:
    """
    Create assessment from compliance report

    :param Dict controls_to_reports: Controls to reports
    :param int regscale_id: RegScale ID
    :param str regscale_module: RegScale module
    :param List controls: Controls
    :return: None
    :rtype: None
    """
    implementations = ControlImplementation.get_all_by_parent(parent_module=regscale_module, parent_id=regscale_id)
    for control_id, reports in controls_to_reports.items():
        control_record_id = None
        for control in controls:
            if control.get("controlId").lower() == control_id:
                control_record_id = control.get("id")
                break
        filtered_results = [x for x in implementations if x.controlID == control_record_id]
        create_report_assessment(filtered_results, reports, control_id)


def create_report_assessment(filtered_results: List, reports: List, control_id: str) -> None:
    """
    Create report assessment

    :param List filtered_results: Filtered results
    :param List reports: Reports
    :param str control_id: Control ID
    :return: None
    :rtype: None
    """
    implementation = filtered_results[0] if len(filtered_results) > 0 else None
    for report in reports:
        html_summary = format_dict_to_html(report.dict())
        if implementation:
            Assessment(
                leadAssessorId=implementation.createdById,
                title=f"Wiz compliance report assessment for {control_id}",
                assessmentType="Control Testing",
                plannedStart=get_current_datetime(),
                plannedFinish=get_current_datetime(),
                actualFinish=get_current_datetime(),
                assessmentResult=report.result,
                assessmentReport=html_summary,
                status="Complete",
                parentId=implementation.id,
                parentModule="controls",
                isPublic=True,
            ).create()
