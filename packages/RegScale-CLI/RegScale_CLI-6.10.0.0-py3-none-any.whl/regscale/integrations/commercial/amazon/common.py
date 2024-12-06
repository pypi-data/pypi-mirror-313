#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" RegScale AWS Integrations """
import itertools
import operator
import re
from datetime import datetime, timedelta, date
from typing import Any, Optional, Tuple

from botocore.client import BaseClient
from botocore.exceptions import ClientError
from dateutil import parser

from regscale.core.app.api import Api
from regscale.core.app.application import Application

from regscale.core.app.utils.app_utils import (
    convert_datetime_to_regscale_string,
    create_logger,
    format_data_to_html,
    reformat_str_date,
)
from regscale.core.app.utils.regscale_utils import format_control
from regscale.core.utils.date import date_obj, date_str
from regscale.models import regscale_models
from regscale.models.regscale_models import Asset, Checklist, ControlImplementation, Issue


def sync_aws_findings(
    regscale_ssp_id: int,
    create_issue: bool = False,
    aws_secret_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> None:
    """
    Sync AWS Security Hub Findings to RegScale SSP

    :param int regscale_ssp_id: RegScale System Security Plan ID
    :param bool create_issue: Create Issue in RegScale from vulnerabilities in AWS Security Hub
    :param Optional[str] aws_secret_key_id: AWS Access Key ID
    :param Optional[str] aws_secret_access_key: AWS Secret Access Key
    :rtype: None
    """
    import boto3  # pylint: disable=C0415

    client = boto3.client(
        "securityhub",
        region_name="us-east-1",
        aws_access_key_id=aws_secret_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    findings = fetch_aws_findings(aws_client=client)
    fetch_aws_findings_and_sync_regscale(regscale_ssp_id, create_issue, findings)


def get_failed_checklist_controls(existing_checklists: list[dict]) -> list[dict]:
    """Extracts failed checklist controls from a list of checklists

    :param list[dict] existing_checklists: List of existing checklists
    :return: List of failed checklist controls
    :rtype: list[dict]
    """
    failed_checklist_controls = []
    for checklist in existing_checklists:
        pattern = r"NIST\.800-53\.r5 ([A-Z]{2}-\d+\(\w\)|[A-Z]{2}-\d+|\w+-\d+\(\w\))"
        matches = re.findall(pattern, checklist["results"])
        if matches and checklist["status"] == "Fail":
            failed_checklist_controls.extend(matches)
    return failed_checklist_controls


def update_control_implementation(api: Api, app: Application, control_implementation: dict) -> None:
    """Updates a control implementation using the RegScale API

    :param Api api: Api instance
    :param Application app: Application instance
    :param dict control_implementation: RegScale control implementation
    :rtype: None
    """
    res = api.put(
        url=f"{app.config['domain']}/api/controlimplementation/{control_implementation['id']}",
        json=control_implementation,
    )
    if not res.ok:
        control_implementation["status"] = "Planned"
        control_implementation["stepsToImplement"] = (
            "Planned by RegScale CLI on " + f"{convert_datetime_to_regscale_string(datetime.now(), '%B %d, %Y')}"
        )
        app.logger.warning(
            "Encountered %i error during updating control #%i: %s. \nRetrying...",
            res.status_code,
            control_implementation["id"],
            res.text,
        )
        res = api.put(
            url=f"{app.config['domain']}/api/controlimplementation/{control_implementation['id']}",
            json=control_implementation,
            headers={"Authorization": app.config["token"]},
        )
    if not res.raise_for_status():
        app.logger.info(
            "Successfully updated control %s",
            control_implementation["controlName"],
        )


def update_implementations(app: Application, regscale_ssp_id: int) -> None:
    """Update Control Implementations

    :param Application app: Application instance
    :param int regscale_ssp_id: RegScale System Security Plan ID
    :rtype: None
    """

    api = Api()
    existing_checklists = Checklist.get_checklists(parent_id=regscale_ssp_id, parent_module="securityplans")
    failed_checklist_controls = get_failed_checklist_controls(existing_checklists)
    existing_ssp_implementations = ControlImplementation.fetch_existing_implementations(
        app=app, regscale_parent_id=regscale_ssp_id, regscale_module="securityplans"
    )
    for control in failed_checklist_controls:
        control_id = format_control(control)
        control_implementation_data = [
            control for control in existing_ssp_implementations if control["controlName"] == control_id
        ]
        if control_implementation_data:
            control_implementation = control_implementation_data[0]
            control_implementation["status"] = "Not Implemented"
            planned_datetime = datetime.now() + timedelta(days=7)
            control_implementation["plannedImplementationDate"] = convert_datetime_to_regscale_string(
                planned_datetime,
                "%Y-%m-%d",
            )
            update_control_implementation(api, app, control_implementation)
        else:
            app.logger.info("No control implementation found for %s", control_id)


def check_finding_severity(comment: Optional[str]) -> str:
    """Check the severity of the finding

    :param Optional[str] comment: Comment from AWS Security Hub finding
    :return: Severity of the finding
    :rtype: str
    """
    result = ""
    match = re.search(r"(?<=Finding Severity: ).*", comment)
    if match:
        severity = match.group()
        result = severity  # Output: "High"
    return result


def extract_severities(checklists: list[Any]) -> str:
    """Extract severities from a list of checklists, return the highest severity found

    :param list[Any] checklists: list of Checklist
    :return: Highest severity found
    :rtype: str
    """
    severities: set[str] = set()
    if isinstance(checklists[0], dict):
        severities = {check_finding_severity(chk["comments"]) for chk in checklists}
    if isinstance(checklists[0], Checklist):
        severities = {check_finding_severity(chk.comments) for chk in checklists}
    if any(item in ["HIGH", "CRITICAL"] for item in severities):
        return "High"
    if "MEDIUM" in severities:
        return "Moderate"
    return "Low"


def get_earliest_date_performed(checklists: list[Checklist]) -> str:
    """Returns the earliest datePerformed from a list of checklists

    :param list[Checklist] checklists: list of checklists
    :return: Earliest date performed
    :rtype: str
    """
    if isinstance(checklists[0], Checklist):
        checklists = [chk.dict() for chk in checklists]
    return min(chk["datePerformed"] for chk in checklists)


def get_asset_link(checklist: Checklist, app: Application) -> str:
    """Returns an HTML link to the asset in RegScale

    :param Checklist checklist: Checklist
    :param Application app: Application
    :return: HTML link to the asset in RegScale
    :rtype: str
    """
    return f"""<a href="{app.config['domain']}/form/assets/{checklist.assetId}" \
        " title="Link">Asset</a>:<br></br><br>"""


def get_failed_checks(checklists: list[Checklist]) -> list[dict]:
    """Returns a list of failed checks from a list of checklists

    :param list[Checklist] checklists: list of checklists
    :return: list of checklists
    :rtype: list[dict]
    """
    return [chk for chk in checklists if chk.status == "Fail"]


def get_due_date(earliest_date_performed: datetime, days: int) -> datetime:
    """Returns the due date for an issue

    :param datetime earliest_date_performed: Earliest date performed
    :param int days: Days to add to the earliest date performed
    :return: Due date
    :rtype: datetime
    """
    fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
    try:
        due_date = datetime.strptime(earliest_date_performed, fmt) + timedelta(days=days)
    except ValueError:
        # Try to determine the date format from a string
        due_date = parser.parse(earliest_date_performed) + timedelta(days)
    return due_date


def get_status(checklists: list[Checklist]) -> str:
    """Returns the status for an issue

    :param list[Checklist] checklists: List of checklists
    :return: Status
    :rtype: str
    """
    return "Open" if "Fail" in {chk.status for chk in checklists} else "Closed"


def get_due_date_string(due_date: datetime, status: str, days: int) -> str:
    """Returns the due date string for an issue

    :param datetime due_date: Due date
    :param str status: Status
    :param int days: Days to add to the earliest date performed
    :return: Due date as a string
    :rtype: str
    """
    fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
    if status == "Open" and due_date < datetime.now():
        due_date = (due_date + timedelta(days=days)).strftime(fmt)
    else:
        due_date = due_date.strftime(fmt)
    return due_date


def build_issue(
    checklists: list[Checklist],
    app: Application,
    regscale_ssp_id: int,
    existing_issues: list[Issue],
) -> tuple[Optional[Issue], Optional[int]]:
    """Creates issue in RegScale and returns Issue and ID

    :param list[Checklist] checklists: Checklists
    :param Application app: Application
    :param int regscale_ssp_id: RegScale System Security Plan ID
    :param list[Issue] existing_issues: Existing issues in RegScale
    :return: Tuple containing issue object and issue ID
    :rtype: tuple[Optional[Issue], Optional[int]]
    """
    earliest_date_performed = get_earliest_date_performed(checklists)
    asset_link = get_asset_link(checklists[0], app)
    failed_checks = get_failed_checks(checklists)
    days = app.config["issues"]["amazon"][extract_severities(checklists).lower()]
    due_date = get_due_date(earliest_date_performed, days)
    status = get_status(checklists)
    due_date_string = get_due_date_string(due_date, status, days)
    # Ensure due date is in the future if status is Open
    if status == regscale_models.IssueStatus.Open:
        due_date_obj = date_obj(due_date_string)
        if due_date_obj and due_date_obj < date.today():
            due_date_string = date_str(date.today())
    issue = Issue(
        title=f"Failed Security Check(s) on AWS asset: {checklists[0].assetId}",
        description=f"AWS Security Checks performed on {asset_link}"
        f" {'</br><br>'.join({chk.ruleId for chk in checklists})} </br>",
        issueOwnerId=app.config["userId"],
        status=status,
        severityLevel="IV - Not Assigned",
        dueDate=due_date_string,
        dateCompleted=(
            None
            if "Fail" in {chk.status for chk in checklists}
            else convert_datetime_to_regscale_string(datetime.now())
        ),
        parentId=regscale_ssp_id,
        parentModule="securityplans",
        recommendedActions=(
            "See Recommendations in these failed checklists"
            if len(failed_checks) > 0
            else "No critical or high recommendations available"
        ),
        identification="Vulnerability Assessment",
    )
    if issue.title not in {iss.title for iss in existing_issues} and issue.status == "Open":
        return issue, None
    if matches := {iss.id for iss in existing_issues if iss.title == issue.title}:
        issue.id = matches.pop()
        return issue, issue.id
    return None, None


def create_or_update_regscale_issue(
    app: Application,
    checklists: list[Checklist],
    regscale_ssp_id: int,
    existing_issues: list[Issue],
) -> Optional[int]:
    """Create Issues in RegScale for failed AWS Security Checks

    :param Application app: Application
    :param list[Checklist] checklists: List of AWS Security Checks
    :param int regscale_ssp_id: RegScale System Security Plan ID
    :param list[Issue] existing_issues: List of existing issues in RegScale
    :return: Issue ID number if it was updated or created
    :rtype: Optional[int]
    """
    issue, issue_id = build_issue(checklists, app, regscale_ssp_id, existing_issues)
    if issue is not None:
        if issue_id is None:
            # post
            if issue_id := issue.create().id:
                app.logger.info("Successfully created issue #%s %s", issue_id, issue.title)
        else:
            # update
            issue.save()
            app.logger.info("Successfully updated issue #%s %s", issue_id, issue.title)
        return issue_id


def create_or_update_regscale_checklists(*args: Tuple) -> Checklist:
    """
    Create or Update RegScale Checklists

    :param Tuple *args: Tuple containing Application, AWS Finding, AWS Resource, RegScale SSP ID
    :return: New Checklist
    :rtype: Checklist
    """
    app, finding, resource, regscale_ssp_id = args
    existing_asset_id = handle_asset_creation(app, resource, regscale_ssp_id)
    status, results = determine_status_and_results(finding)
    comments = get_comments(finding)
    new_checklist = create_checklist(existing_asset_id, status, results, comments, finding)
    new_checklist.id = new_checklist.create_or_update().id
    return new_checklist


def handle_asset_creation(app: Application, resource: Any, regscale_ssp_id: int) -> int:
    """
    Handle Asset Creation

    :param Application app: Application
    :param Any resource: AWS Resource
    :param int regscale_ssp_id: RegScale SSP ID
    :return: Existing Asset ID
    :rtype: int
    """
    existing_assets = Asset.get_all_by_parent(regscale_ssp_id, "securityplans")
    new_asset = create_asset(resource, regscale_ssp_id, app.config["userId"])
    if new_asset not in existing_assets:
        return new_asset.create().id
    return next(asset.id for asset in existing_assets if asset.name == new_asset.name)


def create_asset(resource: Any, regscale_ssp_id: int, user_id: str) -> Asset:
    """
    Create Asset

    :param Any resource: AWS Resource
    :param int regscale_ssp_id: RegScale SSP ID
    :param str user_id: User ID
    :return: New Asset
    :rtype: Asset
    """
    account = None
    if resource["Type"] == "AwsAccount":
        account = re.findall(r"\d+", resource["Id"])
        if account:
            account = account.pop()
    return Asset(
        name=resource["Type"],
        status="Active (On Network)",
        assetOwnerId=user_id,
        assetCategory=regscale_models.AssetCategory.Hardware,
        description=format_data_to_html(resource),
        assetType="Other",
        parentId=regscale_ssp_id,
        parentModule="securityplans",
        otherTrackingNumber=account or resource["Id"],
    )


def determine_status_and_results(finding: Any) -> Tuple[str, Optional[str]]:
    """
    Determine Status and Results

    :param Any finding: AWS Finding
    :return: Status and Results
    :rtype: Tuple[str, Optional[str]]
    """
    status = "Pass"
    results = None
    if "Compliance" in finding.keys():
        status = "Fail" if finding["Compliance"]["Status"] == "FAILED" else "Pass"
        results = ", ".join(finding["Compliance"]["RelatedRequirements"])
    if "FindingProviderFields" in finding.keys():
        status = (
            "Fail"
            if finding["FindingProviderFields"]["Severity"]["Label"] in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
            else "Pass"
        )
    if "PatchSummary" in finding.keys() and not results:
        results = (
            f"{finding['PatchSummary']['MissingCount']} Missing Patch(s) of "
            "{finding['PatchSummary']['InstalledCount']}"
        )
    return status, results


def get_comments(finding: dict) -> str:
    """
    Get Comments

    :param dict finding: AWS Finding
    :return: Comments
    :rtype: str
    """
    try:
        return (
            finding["Remediation"]["Recommendation"]["Text"]
            + "<br></br>"
            + finding["Remediation"]["Recommendation"]["Url"]
            + "<br></br>"
            + f"""Finding Severity: {finding["FindingProviderFields"]["Severity"]["Label"]}"""
        )
    except KeyError:
        return "No remediation recommendation available"


def create_checklist(
    existing_asset_id: int,
    status: str,
    results: Optional[str],
    comments: str,
    finding: dict,
) -> Checklist:
    """
    Create Checklist

    :param int existing_asset_id: Existing Asset ID
    :param str status: Status
    :param Optional[str] results: Results
    :param str comments: Comments
    :param dict finding: AWS Finding
    :return: New Checklist
    :rtype: Checklist
    """
    return Checklist(
        assetId=existing_asset_id,
        status=status,
        tool="Other",
        datePerformed=(
            finding["UpdatedAt"] if reformat_str_date(finding["UpdatedAt"]) else reformat_str_date(datetime.now())
        ),
        vulnerabilityId=finding["Id"],
        ruleId=finding["Title"],
        baseline=finding["GeneratorId"],
        check=finding["Description"],
        results=results if results else "No results available",
        comments=comments,
    )


def fetch_aws_findings(aws_client: BaseClient) -> list:
    """Fetch AWS Findings

    :param BaseClient aws_client: AWS Security Hub Client
    :return: AWS Findings
    :rtype: list
    """
    findings = []
    try:
        findings = aws_client.get_findings()["Findings"]
    except ClientError as cex:
        create_logger().error("Unexpected error: %s", cex)
    return findings


def fetch_aws_findings_and_sync_regscale(
    regscale_ssp_id: int, create_issue: bool = False, findings: Optional[list] = None
) -> None:
    """Sync AWS Security Hub Findings with RegScale

    :param int regscale_ssp_id: RegScale System Security Plan ID
    :param bool create_issue: Create Issue in RegScale from vulnerabilities in AWS Security Hub
                              , defaults to False
    :param Optional[list] findings: List of AWS Security Hub Findings, defaults to None
    :rtype: None
    """
    app = Application()
    for finding in findings:
        # Create or update Assets
        for resource in finding["Resources"]:
            create_or_update_regscale_checklists(
                app,
                finding,
                resource,
                regscale_ssp_id,
            )
    update_implementations(app, regscale_ssp_id)
    existing_issues = Issue.fetch_issues_by_parent(
        app=app, regscale_id=regscale_ssp_id, regscale_module="securityplans"
    )
    get_attr = operator.attrgetter("assetId")

    if create_issue:
        # Refresh existing checklists
        existing_checklists = Checklist.get_checklists(parent_id=regscale_ssp_id, parent_module="securityplans")
        checklists_grouped = [
            list(g)
            for _, g in itertools.groupby(
                sorted(
                    [Checklist(**chk) for chk in existing_checklists],
                    key=get_attr,
                ),
                get_attr,
            )
        ]
        for checklist in checklists_grouped:
            create_or_update_regscale_issue(
                app=app,
                checklists=checklist,
                regscale_ssp_id=regscale_ssp_id,
                existing_issues=existing_issues,
            )
