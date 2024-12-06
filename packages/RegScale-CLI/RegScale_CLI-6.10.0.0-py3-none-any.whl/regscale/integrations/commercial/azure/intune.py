#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RegScale Azure InTune Integration"""
import logging
import multiprocessing
import re
from concurrent.futures import Future, ThreadPoolExecutor, wait
from datetime import datetime, timedelta
from queue import Queue
from typing import List, Optional, Tuple

import click
from requests import Response
from rich.progress import Progress, TaskID

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.utils.app_utils import (
    convert_datetime_to_regscale_string,
    create_progress_object,
    error_and_exit,
    get_current_datetime,
)
from regscale.core.app.utils.regscale_utils import verify_provided_module
from regscale.integrations.commercial.azure.common import get_token
from regscale.models import regscale_id, regscale_module, regscale_models
from regscale.models.regscale_models import Asset, Issue
from regscale.validation.record import validate_regscale_object

logger = logging.getLogger("rich")
issue_queue: Queue = Queue()


@click.group()
def intune():
    """Microsoft Azure InTune Integrations"""


@intune.command(name="sync_intune")
@regscale_id()
@regscale_module()
@click.option(
    "--create_issues",
    type=click.BOOL,
    required=False,
    help="Create Issues in RegScale from failed configurations in InTune.",
    default=False,
)
def sync_intune(regscale_id: int, regscale_module: str, create_issues: bool = False):
    """Sync Intune Alerts with RegScale Assets."""
    verify_provided_module(regscale_module)
    try:
        assert validate_regscale_object(parent_id=regscale_id, parent_module=regscale_module)
    except AssertionError:
        error_and_exit(
            "This RegScale object does not exist. Please check your RegScale Parent ID \
                     and Module."
        )
    sync_regscale_assets(
        regscale_parent_id=regscale_id,
        regscale_module=regscale_module,
        create_issues=create_issues,
    )


def page_graph_api(api: Api, headers: dict, response: Response) -> list[dict]:
    """Page through the Graph API.
    :param Api api: RegScale API instance
    :param dict headers: A simple dictionary of headers to send
    :param Response response: Response object
    :rtype: list[dict]
    :return: list of response data.
    """
    next_link_str = "@odata.nextLink"
    data = []
    if response.status_code == 200:
        data.extend(response.json()["value"])
        if next_link_str in response.json():
            while next_link_str in response.json():
                next_link = response.json()[next_link_str]
                response = api.get(url=next_link, headers=headers)
                data.extend(response.json()["value"])
    return data


def check_if_phone(device: dict) -> Optional[str]:
    """
    Check if the device is a phone or tablet

    :param dict device: The device dictionary
    :return: The device type
    :rtype: Optional[str]
    """

    if "iphone" in device["operatingSystem"].lower():
        return "Phone"
    if "android" in device["operatingSystem"].lower():
        return "Phone"
    if "ipad" in device["operatingSystem"].lower():
        return "Tablet"
    return None


def determine_asset_type(device: dict) -> str:
    """
    Determine the asset type

    :param dict device: The device dictionary
    :return: The asset type
    :rtype: str
    """
    asset_type = check_if_phone(device)
    if not asset_type:
        if device["operatingSystem"] and device["operatingSystem"].lower() in [
            "macmdm",
            "windows",
            "linux",
        ]:
            if device.get("model") and "vm" in device.get("model", "").lower():
                asset_type = "Virtual Machine"
            else:
                asset_type = "Laptop"
        else:
            asset_type = "Virtual Machine"
    return asset_type


def create_asset(device: dict, regscale_parent_id: int, regscale_module: str, config: dict) -> Asset:
    """
    Create an asset from the device dictionary

    :param dict device: The device dictionary
    :param int regscale_parent_id: The RegScale Parent ID
    :param str regscale_module: The RegScale Module
    :param dict config: The configuration dictionary
    :return: The asset
    :rtype: Asset
    """
    if device.get("approximateLastSignInDateTime"):
        last_sign_in = datetime.strptime(device["approximateLastSignInDateTime"], "%Y-%m-%dT%H:%M:%SZ")
        status = "Active (On-Network)" if determine_if_recent(last_sign_in) or device["isCompliant"] else "Off-Network"
    else:
        status = "Off-Network"
    asset_type = determine_asset_type(device)
    return Asset(
        name=device["displayName"],
        otherTrackingNumber=device["deviceId"],
        parentId=regscale_parent_id,
        parentModule=regscale_module,
        macAddress=None,
        ipAddress=None,
        manufacturer=device["manufacturer"],
        model=device["model"],
        operatingSystem=(
            device.get("operatingSystem") + " " + device.get("operatingSystemVersion")
            if device.get("operatingSystem") and device.get("operatingSystemVersion")
            else ""
        ),
        assetOwnerId=config["userId"],
        assetType=asset_type if asset_type else "Other",
        assetCategory=regscale_models.AssetCategory.Hardware,
        status=status,
        notes=f"<p>isCompliant: <strong>{device['isCompliant']}</strong><br>isManaged: "
        + f"<strong>{device['isManaged']}</strong><br>isRooted: <strong>"
        + f"{device['isRooted']}</strong><br>approximateLastSignInDateTime: <strong>"
        + f"{device['approximateLastSignInDateTime']}</strong>",
    )


def fetch_intune_assets(
    app: Application,
    headers: dict,
    response: Response,
    regscale_parent_id: int,
    regscale_module: str,
) -> List[Asset]:
    """
    Fetch InTune Assets

    :param Application app: Application instance
    :param dict headers: A simple dictionary of headers to send
    :param Response response: Response object
    :param int regscale_parent_id: RegScale Parent ID
    :param str regscale_module: RegScale Module
    :return: List of InTune Assets
    :rtype: List[Asset]
    """
    api = Api()
    intune_assets = []
    config = app.config
    if response.status_code == 200:
        devices = page_graph_api(api=api, headers=headers, response=response)
        logger.debug(response)
        logger.info("Building or updating RegScale Assets from %i InTune Devices...", len(devices))
        for device in devices:
            intune_assets.append(create_asset(device, regscale_parent_id, regscale_module, config))
            logger.debug(device)
    else:
        logger.error(
            "Error fetching Intune Assets: HTTP %s, %s",
            response.status_code,
            response.reason,
        )
    return intune_assets


def query_intune_devices(api: Api, token: str) -> Tuple[Response, dict]:
    """Query Azure Intune devices.

    :param Api api: requests.Session instance
    :param str token: Azure AD Token
    :return: Tuple containing Requests Response and headers dictionary
    :rtype: Tuple[Response, dict]
    """
    url = "https://graph.microsoft.com/v1.0/devices?$top=10"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = api.get(url=url, headers=headers)
    return response, headers


def find_compliance(notes: Optional[str]) -> bool:
    """
    Check if the notes field indicates compliance

    :param Optional[str] notes: A string containing the contents of the notes field
    :return: True if the notes field indicates compliance, False otherwise
    :rtype: bool
    """
    if notes:
        if match := re.search(r"isCompliant: <strong>(\w+)</strong>", notes):
            is_compliant = match.group(1)
            return is_compliant.lower() == "true"
    return False


def get_existing_issues(parent_id: int, regscale_module: str) -> list[Issue]:
    """
    Get existing issues from RegScale for the given issue

    :param int parent_id: RegScale parent ID
    :param str regscale_module: RegScale Module
    :return: List of existing issues from RegScale
    :rtype: list[Issue]
    """
    app = Application()
    if regscale_module == "securityplans":
        return Issue.fetch_issues_by_ssp(app=app, ssp_id=parent_id)
    return Issue.fetch_issues_by_parent(app=app, regscale_id=parent_id, regscale_module=regscale_module)


def create_or_update_issue(
    asset: Asset,
    existing_issues: List[Issue],
    regscale_parent_id: int,
    regscale_module: str,
) -> None:
    """
    Create or Update Issue in RegScale

    :param Asset asset: RegScale Asset instance
    :param List[Issue] existing_issues: List of existing issues
    :param int regscale_parent_id: RegScale Parent ID
    :param str regscale_module: RegScale Module
    :rtype: None
    :return: None
    """
    app = Application()
    issue_exists = False
    severity_level = Issue.assign_severity("High")
    due_date = datetime.now() + timedelta(days=30)
    # Extract the isCompliant boolean
    is_compliant = find_compliance(notes=asset.notes)
    issue = Issue(
        title=f"{asset.name} - Intune ID: {asset.otherTrackingNumber}",
        dateCreated=get_current_datetime(),
        status="Open",
        severityLevel=severity_level,
        issueOwnerId=app.config["userId"],
        securityPlanId=(regscale_parent_id if regscale_module == "securityplans" else None),
        componentId=regscale_parent_id if regscale_module == "components" else None,
        identification="Intune Compliance Check",
        dueDate=convert_datetime_to_regscale_string(due_date),
        description="Intune Compliance: Failed",
    )
    issue.parentId = asset.id
    issue.parentModule = "assets"
    asset_issues: List[Issue] = Issue.get_all_by_parent(parent_id=asset.id, parent_module="assets")
    if [iss for iss in asset_issues if iss.title == issue.title]:
        issue_exists = True
    if is_compliant and not issue_exists:
        return
    if issue_exists:
        determine_issue_status(issue, existing_issues, is_compliant)
    else:
        logger.debug('Creating issue "%s"', issue.title)
    issue_queue.put(issue)


def determine_issue_status(issue: Issue, existing_issues: List[Issue], is_compliant: bool) -> None:
    """
    Determine the issue status

    :param Issue issue: RegScale Issue instance
    :param List[Issue] existing_issues: List of existing issues
    :param bool is_compliant: Compliance status
    :rtype: None
    """
    try:
        issue.id = [iss for iss in existing_issues if iss.title == issue.title][0].id
        if issue.status == "Open" and is_compliant:
            # Update issue
            issue.status = "Closed"
            issue.dateCompleted = get_current_datetime() if issue.status == "Closed" else ""
        logger.debug('Updating issue "%s"', issue.title)
    except ValueError as vex:
        logger.error(vex)
    except IndexError as iex:
        logger.debug(iex)


def process_issue_queue() -> None:
    """
    Process the issue queue

    :rtype: None
    :return: None
    """
    saved: int = 0
    created: int = 0
    if not issue_queue.empty():
        logger.info("Processing %i issues", issue_queue.qsize())
    while not issue_queue.empty():
        item = issue_queue.get()
        if item.id:
            item.save()
            saved += 1
        else:
            item.create()
            created += 1
    logger.info("Created %i new issues and updated %i existing issues", created, saved)


def process_futures(
    future_list: List[Future],
    regscale_parent_id: int,
    regscale_module: str,
    create_issues: bool,
    job_objects=Tuple[TaskID, Progress, ThreadPoolExecutor],
) -> None:
    """Process a list of concurrent.futures

    :param List[Future] future_list: List of futures
    :param int regscale_parent_id: RegScale Parent ID
    :param str regscale_module: RegScale Module
    :param bool create_issues: Create Issues in RegScale from failed configurations in InTune
    :param Tuple[TaskID, Progress, ThreadPoolExecutor] job_objects: Tuple containing TaskID,
            Progress, ThreadPoolExecutor
    :rtype: None
    :return: None
    """
    task_name, job_progress, executor = job_objects
    # Refresh assets
    refreshed_assets: List[Asset] = Asset.get_all_by_parent(parent_id=regscale_parent_id, parent_module=regscale_module)
    for asset_future in future_list:
        # extract the asset from the future
        current_asset = asset_future.result()
        job_progress.update(task_name, advance=1)
        if create_issues and current_asset:
            matching_asset: List[Asset] = [
                asset for asset in refreshed_assets if asset.otherTrackingNumber == current_asset.otherTrackingNumber
            ]
            if matching_asset:
                asset_issues: List[Issue] = Issue.get_all_by_parent(
                    parent_id=matching_asset[0].id, parent_module="assets"
                )
                current_asset.id = matching_asset[0].id
                future_list.append(
                    executor.submit(
                        create_or_update_issue,
                        existing_issues=asset_issues,
                        asset=current_asset,
                        regscale_parent_id=regscale_parent_id,
                        regscale_module=regscale_module,
                    )
                )


def fetch_and_process_assets(
    assets: List[Asset], existing_assets: List[Asset], executor: ThreadPoolExecutor
) -> Tuple[List[Future], List[Future]]:
    """
    Fetch and process assets

    :param List[Asset] assets: List of assets
    :param List[Asset] existing_assets: List of existing assets
    :param ThreadPoolExecutor executor: ThreadPoolExecutor instance
    :rtype: Tuple[List[Future], List[Future]]
    :return: Tuple containing list of insert and update futures
    """
    insert_futures: List[Future] = []
    update_futures: List[Future] = []
    for asset in assets:
        if asset.otherTrackingNumber not in {ast.otherTrackingNumber for ast in existing_assets}:
            logger.debug("Inserting new asset: %s", asset.otherTrackingNumber)
            insert_futures.append(executor.submit(asset.create))
        else:
            # update id
            try:
                asset.id = [
                    asset for asset in existing_assets if asset.otherTrackingNumber == asset.otherTrackingNumber
                ][0].id
                logger.debug("Updating existing asset: %s", asset.otherTrackingNumber)
                update_futures.append(executor.submit(asset.save))
            except IndexError as vex:
                logger.error(vex)
    return insert_futures, update_futures


def sync_regscale_assets(regscale_parent_id: int, regscale_module: str, create_issues: bool) -> None:
    """Fetch assets from InTune and sync with RegScale

    :param int regscale_parent_id: RegScale Parent ID
    :param str regscale_module: RegScale Module
    :param bool create_issues: Create Issues in RegScale from failed configurations in InTune
    :rtype: None
    """
    import inflect  # Optimize import performance

    p = inflect.engine()
    app = Application()
    api = Api()
    job_progress = create_progress_object()

    token = get_token(app)
    response, headers = query_intune_devices(api=api, token=token)
    assets = fetch_intune_assets(
        app=app,
        headers=headers,
        response=response,
        regscale_parent_id=regscale_parent_id,
        regscale_module=regscale_module,
    )
    existing_assets: List[Asset] = Asset.get_all_by_parent(parent_id=regscale_parent_id, parent_module=regscale_module)
    if not assets:
        logger.warning("No InTune Devices Found")

    with job_progress, ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        insert_futures, update_futures = fetch_and_process_assets(assets, existing_assets, executor)
        wait(insert_futures + update_futures)
        if insert_futures:
            insert_asset_task = job_progress.add_task(
                f"Inserting {len(insert_futures)} assets at the " + f"{p.singular_noun(regscale_module)} level...",
                total=len(insert_futures),
            )
            process_futures(
                future_list=insert_futures,
                regscale_parent_id=regscale_parent_id,
                regscale_module=regscale_module,
                create_issues=create_issues,
                job_objects=(insert_asset_task, job_progress, executor),
            )
        if update_futures:
            update_asset_task = job_progress.add_task(
                f"Updating {len(update_futures)} assets at the " + f"{p.singular_noun(regscale_module)} level...",
                total=len(update_futures),
            )
            process_futures(
                future_list=update_futures,
                regscale_parent_id=regscale_parent_id,
                regscale_module=regscale_module,
                create_issues=create_issues,
                job_objects=(update_asset_task, job_progress, executor),
            )
    process_issue_queue()


def determine_if_recent(date: datetime, days: int = 7) -> bool:
    """
    Determine if a date is recent

    :param datetime date: The date to check
    :param int days: The number of days to consider recent
    :return: True if the date is recent, False otherwise
    :rtype: bool
    """
    # Using three days ago as the threshold
    days_ago = datetime.now() - timedelta(days=days)
    return date >= days_ago
