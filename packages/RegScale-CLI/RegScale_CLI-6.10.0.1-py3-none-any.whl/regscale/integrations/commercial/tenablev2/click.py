#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tenable integration for RegScale CLI"""

import queue
from typing import TYPE_CHECKING

# Delay import of Tenable libraries
if TYPE_CHECKING:
    from tenable.io import TenableIO  # type: ignore
    from tenable.sc import TenableSC  # type: ignore
    import pandas as pd  # Type Checking

import collections
import json
import os
import re
import tempfile
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from itertools import groupby
from pathlib import Path
from threading import Lock, current_thread, get_ident, get_native_id
from typing import Dict, List, Optional, Set, Tuple, Union
from urllib.parse import urljoin

import click
import requests
from requests.exceptions import RequestException
from rich.console import Console
from rich.pretty import pprint
from rich.progress import track
from tenable.sc.analysis import AnalysisResultsIterator

from regscale import __version__
from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import (
    check_file_path,
    check_license,
    create_progress_object,
    epoch_to_datetime,
    format_dict_to_html,
    get_current_datetime,
    regscale_string_to_epoch,
    save_data_to,
)
from regscale.core.app.utils.pickle_file_handler import PickleFileHandler
from regscale.integrations.commercial.nessus.nessus_utils import get_cpe_file
from regscale.models.app_models.click import file_types, hidden_file_path, regscale_ssp_id, save_output_to
from regscale.models.integration_models.tenable_models.integration import SCIntegration
from regscale.models.integration_models.tenable_models.models import AssetCheck, TenableAsset, TenableIOAsset
from regscale.models.regscale_models import ControlImplementation
from regscale.models.regscale_models.asset import Asset
from regscale.models.regscale_models.issue import Issue
from regscale.models.regscale_models.scan_history import ScanHistory
from regscale.utils.threading import ThreadSafeCounter
from regscale.validation.address import validate_mac_address

console = Console()

logger = create_logger("rich")
REGSCALE_INC = "RegScale, Inc."
REGSCALE_CLI = "RegScale CLI"

FULLY_IMPLEMENTED = "Fully Implemented"
NOT_IMPLEMENTED = "Not Implemented"
IN_REMEDIATION = "In Remediation"

DONE_MSG = "Done!"


#####################################################################################################
#
# Tenable.sc Documentation: https://docs.tenable.com/tenablesc/api/index.htm
# pyTenable GitHub repo: https://github.com/tenable/pyTenable
# Python tenable.sc documentation: https://pytenable.readthedocs.io/en/stable/api/sc/index.html
#
#####################################################################################################


# Create group to handle OSCAL processing
@click.group()
def tenable():
    """Performs actions on the Tenable APIs."""


@tenable.group(help="[BETA] Performs actions on the Tenable.io API.")
def io():
    """Performs actions on the Tenable.io API."""


@tenable.group(help="[BETA] Performs actions on the Tenable.sc API.")
def sc():
    """Performs actions on the Tenable.sc API."""


@tenable.group(help="[BETA] Import Nessus scans and assets to RegScale.")
def nessus():
    """Performs actions on the Tenable.sc API."""


@nessus.command(name="import_nessus")
@click.option(
    "--folder_path",
    prompt="Enter the folder path of the Nessus files to process",
    help="RegScale will load the Nessus Scans",
    type=click.Path(exists=True),
)
@click.option(
    "--scan_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="The the scan date of the file.",
    required=False,
)
@regscale_ssp_id()
def import_nessus(folder_path: click.Path, regscale_ssp_id: click.INT, scan_date: click.DateTime):
    """Import Nessus scans, vulnerabilities and assets to RegScale."""
    from regscale.integrations.commercial.nessus.scanner import NessusIntegration

    NessusIntegration.sync_assets(plan_id=regscale_ssp_id, path=folder_path)
    NessusIntegration.sync_findings(
        plan_id=regscale_ssp_id, path=folder_path, enable_finding_date_update=True, scan_date=scan_date
    )


@nessus.command(name="update_cpe_dictionary")
def update_cpe_dictionary():
    """
    Manually update the CPE 2.2 dictionary from NIST.
    """
    get_cpe_file(download=True)


@sc.command(name="export_scans")
@save_output_to()
@file_types([".json", ".csv", ".xlsx"])
def export_scans(save_output_to: Path, file_type: str):
    """Export scans from Tenable Host to a .json, .csv or .xlsx file."""
    # get the scan results
    results = get_usable_scan_list()

    # check if file path exists
    check_file_path(save_output_to)

    # set the file name
    file_name = f"tenable_scans_{get_current_datetime('%m%d%Y')}"

    # save the data as the selected file by the user
    save_data_to(
        file=Path(f"{save_output_to}/{file_name}{file_type}"),
        data=results,
    )


def get_usable_scan_list() -> list:
    """
    Usable Scans from Tenable Host

    :return: List of scans from Tenable
    :rtype: list
    """
    results = []
    try:
        client = gen_client()
        results = client.scans.list()["usable"]
    except Exception as ex:
        logger.error(ex)
    return results


def get_detailed_scans(scan_list: list = None) -> list:
    """
    Generate list of detailed scans (Warning: this action could take 20 minutes or more to complete)

    :param list scan_list: List of scans from Tenable, defaults to None
    :raise SystemExit: If there is an error with the request
    :return: Detailed list of Tenable scans
    :rtype: list
    """
    client = gen_client()
    detailed_scans = []
    for scan in track(scan_list, description="Fetching detailed scans..."):
        try:
            det = client.scans.details(id=scan["id"])
            detailed_scans.append(det)
        except RequestException as ex:  # This is the correct syntax
            raise SystemExit(ex) from ex

    return detailed_scans


@sc.command(name="save_queries")
@save_output_to()
@file_types([".json", ".csv", ".xlsx"])
def save_queries(save_output_to: Path, file_type: str):
    """Get a list of query definitions and save them as a .json, .csv or .xlsx file."""
    # get the queries from Tenable
    query_list = get_queries()

    # check if file path exists
    check_file_path(save_output_to)

    # set the file name
    file_name = f"tenable_queries_{get_current_datetime('%m%d%Y')}"

    # save the data as a .json file
    save_data_to(
        file=Path(f"{save_output_to}{os.sep}{file_name}{file_type}"),
        data=query_list,
    )


def get_queries() -> list:
    """
    List of query definitions

    :return: List of queries from Tenable
    :rtype: list
    """
    app = Application()
    tsc = gen_tsc(app.config)
    return tsc.queries.list()


@sc.command(name="query_vuln")
@click.option(
    "--query_id",
    type=click.INT,
    help="Tenable query ID to retrieve via API",
    prompt="Enter Tenable query ID",
    required=True,
)
@regscale_ssp_id()
@click.option(
    "--create_issue_from_recommendation",
    type=click.BOOL,
    help="Create Issue in RegScale from Vulnerability in RegScale.",
    default=False,
    required=False,
)
# Add Prompt for RegScale SSP name
def query_vuln(query_id: int, regscale_ssp_id: int, create_issue_from_recommendation: bool):
    """Query Tenable vulnerabilities and sync assets to RegScale."""
    if create_issue_from_recommendation:
        # Deprecation warning
        logger.warning(
            '"--create_issue_from_recommendation" is deprecated and will be removed in a future release.\n'
            + "Issues will be handled automatically with the new ScannerIntegration functionality."
        )
    q_vuln(
        query_id=query_id,
        ssp_id=regscale_ssp_id,
    )


@io.command(name="sync_assets")
@regscale_ssp_id()
# Add Prompt for RegScale SSP name
def query_assets(regscale_ssp_id: int):
    """Query Tenable Assets and sync to RegScale."""
    # Validate ssp
    from regscale.integrations.commercial.tenablev2.scanner import TenableIntegration

    TenableIntegration.sync_assets(plan_id=regscale_ssp_id)


def validate_regscale_security_plan(parent_id: int) -> bool:
    """
    Validate RegScale Security Plan exists

    :param int parent_id: The ID number from RegScale of the System Security Plan
    :return: If API call was successful
    :rtype: bool
    """
    app = check_license()
    config = app.config
    headers = {
        "Authorization": config["token"],
    }
    url = urljoin(config["domain"], f"/api/securityplans/{parent_id}")
    response = requests.get(url, headers=headers)
    return response.ok


@io.command(name="sync_vulns")
@regscale_ssp_id()
@click.option(
    "--create_issue_from_recommendation",
    type=click.BOOL,
    help="Create RegScale issue from Tenable recommendation.",
    required=False,
)
# Add Prompt for RegScale SSP name
def query_vulns(regscale_ssp_id: int, create_issue_from_recommendation: bool = False):
    from regscale.integrations.commercial.tenablev2.scanner import TenableIntegration

    TenableIntegration.sync_findings(plan_id=regscale_ssp_id)


@io.command(name="list_jobs")
@click.option(
    "--job_type",
    default="vulns",
    type=click.Choice(["vulns", "assets"]),
    show_default=True,
    help="Tenable job type.",
    required=False,
)
@click.option(
    "--last",
    type=click.INT,
    default=100,
    show_default=True,
    help="Filter the last n jobs.",
    required=False,
)
@click.option(
    "--job_status",
    type=click.Choice(["processing", "finished", "cancelled"]),
    help="Filter by status.",
    required=False,
)
def list_jobs(job_type: str, last: int, job_status: str):
    """Retrieve a list of jobs from Tenable.io."""
    app = Application()
    config = app.config
    client = gen_tio(config)
    if job_status:
        jobs = [job for job in client.exports.jobs(job_type) if job["status"] == str(job_status).upper()]
    else:
        jobs = client.exports.jobs(job_type)
    jobs = sorted(jobs, key=lambda k: (k["created"]), reverse=False)
    # filter the last N jobs
    for job in jobs[len(jobs) - last :]:
        console.print(
            f"UUID: {job['uuid']}, STATUS: {job['status']}, CREATED: {epoch_to_datetime(job['created'], epoch_type='milliseconds')}"
        )


@io.command(name="cancel_job")
@click.option(
    "--uuid",
    type=click.STRING,
    help="Tenable job UUID.",
    prompt="Enter the UUID of the job to cancel.",
    required=True,
)
@click.option(
    "--job_type",
    default="vulns",
    type=click.Choice(["vulns", "assets"]),
    show_default=True,
    help="Tenable job type.",
    required=False,
)
def cancel_job(uuid: str, job_type: str):
    """Cancel a Tenable IO job."""
    app = Application()
    config = app.config
    client = gen_tio(config)
    client.exports.cancel(job_type, export_uuid=uuid)


def process_vulnerabilities(counts: collections.Counter, reg_assets: list, ssp_id: int, tenable_vulns: list) -> list:
    """
    Process Tenable vulnerabilities

    :param collections.Counter counts: Dictionary of counts of each vulnerability
    :param list reg_assets: List of RegScale assets
    :param int ssp_id: RegScale System Security Plan ID
    :param list tenable_vulns: List of Tenable vulnerabilities
    :return: List of assets to update
    :rtype: list
    """
    update_assets = []
    for vuln in set(tenable_vulns):
        update_assets = process_vuln(counts, reg_assets, ssp_id, vuln)
    return update_assets


def q_vuln(query_id: int, ssp_id: int) -> list:
    """
    Query Tenable vulnerabilities

    :param int query_id: Tenable query ID
    :param int ssp_id: RegScale System Security Plan ID
    :return: List of queries from Tenable
    :rtype: list
    """
    check_license()
    # At SSP level, provide a list of vulnerabilities and the counts of each
    fetch_vulns(query_id=query_id, regscale_ssp_id=ssp_id)


def process_vuln(counts: collections.Counter, reg_assets: list, ssp_id: int, vuln: TenableAsset) -> list:
    """
    Process Tenable vulnerability data

    :param collections.Counter counts: Dictionary of counts of each vulnerability
    :param list reg_assets: List of RegScale assets
    :param int ssp_id: RegScale System Security Plan ID
    :param TenableAsset vuln: Tenable vulnerability object
    :return: List of assets to update
    :rtype: list
    """
    update_assets = []
    vuln.count = dict(counts)[vuln.pluginName]
    lookup_assets = lookup_asset(reg_assets, vuln.macAddress, vuln.dnsName)
    # Update parent id to SSP on insert
    if len(lookup_assets) > 0:
        for asset in set(lookup_assets):
            # Do update
            # asset = reg_asset[0]
            asset.parentId = ssp_id
            asset.parentModule = "securityplans"
            asset.macAddress = vuln.macAddress.upper()
            asset.osVersion = vuln.operatingSystem
            asset.purchaseDate = "01-01-1970"
            asset.endOfLifeDate = "01-01-1970"
            if asset.ipAddress is None:
                asset.ipAddress = vuln.ip
            asset.operatingSystem = determine_os(asset.operatingSystem)
            try:
                assert asset.id
                # avoid duplication
                if asset not in update_assets:
                    update_assets.append(asset)
            except AssertionError as aex:
                logger.error("Asset does not have an id, unable to update!\n%s", aex)
    return update_assets


def determine_os(os_string: str) -> str:
    """
    Determine RegScale friendly OS name

    :param str os_string: String of the asset's OS
    :return: RegScale acceptable OS
    :rtype: str
    """
    linux_words = ["linux", "ubuntu", "hat", "centos", "rocky", "alma", "alpine"]
    if re.compile("|".join(linux_words), re.IGNORECASE).search(os_string):
        return "Linux"
    elif (os_string.lower()).startswith("windows"):
        return "Windows Server" if "server" in os_string else "Windows Desktop"
    else:
        return "Other"


def lookup_asset(asset_list: list, mac_address: str, dns_name: str = None) -> list:
    """
    Lookup asset in Tenable and return the data from Tenable

    :param list asset_list: List of assets to lookup in Tenable
    :param str mac_address: Mac address of asset
    :param str dns_name: DNS Name of the asset, defaults to None
    :return: List of assets that fit the provided filters
    :rtype: list
    """
    results = []
    if validate_mac_address(mac_address):
        if dns_name:
            results = [
                Asset(**asset)
                for asset in asset_list
                if "macAddress" in asset
                and asset["macAddress"] == mac_address
                and asset["name"] == dns_name
                and "macAddress" in asset
                and "name" in asset
            ]
        else:
            results = [asset for asset in asset_list if asset["macAddress"] == mac_address]
    # Return unique list
    return list(set(results))


def create_issue_from_vuln(app: Application, row: "pd.Series", default_due_delta: int) -> "Issue":
    """
    Creates an Issue object from a Tenable vulnerability

    :param Application app: Application object
    :param pd.Series row: Row of data from Tenable
    :param int default_due_delta: Default due delta
    :return: Issue object
    :rtype: Issue
    """

    default_status = app.config["issues"]["tenable"]["status"]
    fmt = "%Y-%m-%d %H:%M:%S"
    plugin_id = row["pluginID"]
    port = row["port"]
    protocol = row["protocol"]
    due_date = datetime.strptime(row["last_scan"], fmt) + timedelta(days=default_due_delta)
    if due_date < datetime.now():
        due_date = datetime.now() + timedelta(days=default_due_delta)
    if "synopsis" in row:
        title = row["synopsis"]
    return Issue(
        title=title or row["pluginName"],
        description=row["description"] or row["pluginName"] + f"<br>Port: {port}<br>Protocol: {protocol}",
        issueOwnerId=app.config["userId"],
        status=default_status,
        severityLevel=Issue.assign_severity(row["severity"]),
        dueDate=due_date.strftime(fmt),
        identification="Vulnerability Assessment",
        parentId=row["regscale_ssp_id"],
        parentModule="securityplans",
        pluginId=plugin_id,
        vendorActions=row["solution"],
        assetIdentifier=f'DNS: {row["dnsName"]} - IP: {row["ip"]}',
    )


def create_issue_from_row(app: Application, row: "pd.Series", default_due_delta: int) -> "Issue":
    """
    Creates an Issue object from a Tenable vulnerability

    :param Application app: Application object
    :param pd.Series row: Row of data from Tenable
    :param int default_due_delta: Default due delta
    :return: Issue object
    :rtype: Issue
    """
    if row["severity"] != "Info":
        issue = create_issue_from_vuln(app, row, default_due_delta)
        if isinstance(issue, Issue):
            return issue
    return None


def prepare_issues_for_sync(
    app: Application, df: "pd.DataFrame", regscale_ssp_id: int
) -> Tuple[List["Issue"], List["Issue"]]:
    """
    Prepares Tenable vulnerabilities for synchronization as RegScale issues

    :param Application app: Application object
    :param pd.DataFrame df: Dataframe of Tenable data
    :param int regscale_ssp_id: RegScale System Security Plan ID
    :return: List of issues to insert, list of issues to update
    :rtype: Tuple[List[Issue], List[Issue]]
    """

    default_due_delta = app.config["issues"]["tenable"]["moderate"]
    existing_issues = Issue.get_all_by_parent(parent_id=regscale_ssp_id, parent_module="securityplans")
    sc_issues = []
    new_issues = set()
    update_issues = set()
    for index, row in df.iterrows():
        issue = create_issue_from_row(app, row, default_due_delta)
        if isinstance(issue, Issue):
            sc_issues.append(issue)
    # Generate list of completely new issues, and merge with existing issues if they have the same title
    # group issues by title
    grouped_issues = {k: list(g) for k, g in groupby(sc_issues, key=lambda x: x.title)}
    for title in grouped_issues:
        reg_key = 0
        regs = [iss for iss in existing_issues if iss.title == title and iss.id]
        if regs:
            reg_key = regs[0].id
        issues = set(grouped_issues[title])
        for issue in issues:
            asset_ident = combine_strings({iss.assetIdentifier for iss in issues})
            if reg_key and issue.title not in {iss.title for iss in update_issues}:
                issue.id = reg_key
                issue.assetIdentifier = asset_ident
                update_issues.add(issue)
            elif not reg_key:
                issue.assetIdentifier = asset_ident
                new_issues.add(issue)

    return list(new_issues), list(update_issues)


def combine_strings(set_of_strings: Set[str]) -> str:
    """
    Combines a set of strings into a single string

    :param Set[str] set_of_strings: Set of strings
    :rtype: str
    :return: Combined string
    """
    return "<br>".join(set_of_strings)


def sync_issues_to_regscale(new_issues: List["Issue"], update_issues: List["Issue"]) -> None:
    """
    Synchronizes issues to RegScale

    :param List[Issue] new_issues: New issues
    :param List[Issue] update_issues: Updated issues
    :rtype: None
    """
    logger = create_logger()

    if new_issues:
        logger.info(f"Creating {len(new_issues)} new issue(s) in RegScale...")
        Issue.batch_create(new_issues)
        logger.info("Finished creating issue(s) in RegScale.")
    else:
        logger.info("No new issues to create.")

    if update_issues:
        logger.info(f"Updating {len(update_issues)} existing issue(s) in RegScale...")
        Issue.batch_update(update_issues)
        logger.info("Finished updating issue(s) in RegScale.")
    else:
        logger.info("No issues to update.")


def create_regscale_issue_from_vuln(regscale_ssp_id: int, df: Optional["pd.DataFrame"] = None) -> None:
    """
    Sync Tenable Vulnerabilities to RegScale issues

    :param int regscale_ssp_id: RegScale System Security Plan ID
    :param Optional["pd.DataFrame"] df: Pandas dataframe of Tenable data
    :rtype: None
    """
    import pandas as pd  # Optimize import performance

    if df is None:
        df = pd.DataFrame()
    app = Application()
    new_issues, update_issues = prepare_issues_for_sync(app, df, regscale_ssp_id)
    sync_issues_to_regscale(new_issues, update_issues)


def fetch_assets(ssp_id: int) -> list[TenableIOAsset]:
    """
    Fetch assets from Tenable IO and sync to RegScale

    :param int ssp_id: RegScale System Security Plan ID
    :return: List of Tenable assets
    :rtype: list[TenableIOAsset]
    """
    tenable_last_updated: int = 0
    app = Application()
    config = app.config
    client = gen_tio(config=config)
    assets: List[TenableIOAsset] = []
    logger.info("Fetching existing assets from RegScale...")

    existing_assets: List[Asset] = Asset.get_all_by_parent(parent_id=ssp_id, parent_module="securityplans")

    logger.info("Found %i existing asset(s) in RegScale.", len(existing_assets))

    filtered_assets = [asset for asset in existing_assets if asset.tenableId and asset.dateLastUpdated]
    # Get last epoch updated from RegScale, limit to Tenable assets
    if filtered_assets:
        tenable_last_updated = max([regscale_string_to_epoch(asset.dateLastUpdated) for asset in filtered_assets])
    export = client.exports.assets(updated_at=tenable_last_updated)
    logger.info("Saving chunked asset files from Tenable IO for processing...")
    temp_loc = Path(tempfile.gettempdir()) / "tenable_io" / str(uuid.uuid4())  # random folder name
    # show process status
    box_len = 0
    status = client.exports.status(export_type=export.type, export_uuid=export.uuid)
    with create_progress_object(indeterminate=True) as job_progress:
        job_progress.add_task("Fetching Chunked Tenable IO data...", start=False, total=None)
        while status["status"] == "PROCESSING":
            box_len = len(status["chunks_available"])
            time.sleep(0.5)
            status = client.exports.status(export_type=export.type, export_uuid=export.uuid)
    # Process chunks of data
    with create_progress_object(indeterminate=True) as saving_progress:
        saving_task = saving_progress.add_task(
            "Saving Tenable IO data to disk...",
            total=box_len,
        )
        export.run_threaded(
            func=write_io_chunk,
            kwargs={"data_dir": temp_loc},
            num_threads=3,
        )
        saving_progress.update(saving_task, advance=1)
    process_to_regscale(data_dir=temp_loc, ssp_id=ssp_id, existing_assets=existing_assets)
    return assets


def fetch_vulns(query_id: int = 0, regscale_ssp_id: int = 0):
    """
    Fetch vulnerabilities from Tenable by query ID

    :param int query_id: Tenable query ID, defaults to 0
    :param int regscale_ssp_id: RegScale System Security Plan ID, defaults to 0
    """

    client = gen_client()
    if query_id and client._env_base == "TSC":
        vulns = client.analysis.vulns(query_id=query_id)
        sc = SCIntegration(plan_id=regscale_ssp_id)
        # Create pickle file to cache data
        # make sure folder exists
        with tempfile.TemporaryDirectory() as temp_dir:
            logger.info("Saving Tenable SC data to disk...%s", temp_dir)
            consume_iterator_to_file(iterator=vulns, dir_path=Path(temp_dir), scanner=sc)
            iterables = tenable_dir_to_tuple_generator(Path(temp_dir))
            try:
                sc.sync_assets(
                    plan_id=regscale_ssp_id,
                    integration_assets=(asset for sublist in iterables[0] for asset in sublist),
                )
                sc.sync_findings(
                    plan_id=regscale_ssp_id,
                    integration_findings=(finding for sublist in iterables[1] for finding in sublist),
                )
            except IndexError as ex:
                logger.error("Error processing Tenable SC data: %s", ex)


def tenable_dir_to_tuple_generator(dir_path: Path):
    """
    Generate a tuple of chained generators for Tenable directories.
    """
    from itertools import chain

    assets_gen = chain.from_iterable(
        (dat["assets"] for dat in PickleFileHandler(file).read()) for file in dir_path.iterdir()
    )
    findings_gen = chain.from_iterable(
        (dat["findings"] for dat in PickleFileHandler(file).read()) for file in dir_path.iterdir()
    )

    return assets_gen, findings_gen


def consume_iterator_to_file(iterator: AnalysisResultsIterator, dir_path: Path, scanner: SCIntegration) -> int:
    """
    Consume an iterator and write the results to a file

    :param AnalysisResultsIterator iterator: Tenable SC iterator
    :param Path dir_path: The directory to save the pickled files
    :param SCIntegration scanner: Tenable SC Integration object
    :rtype: int
    :return: The total count of items processed
    """
    app = Application()
    logger.info("Consuming Tenable SC iterator...")
    total_count = ThreadSafeCounter()
    page_number = ThreadSafeCounter()
    rec_count = ThreadSafeCounter()
    process_list = queue.Queue()
    with ThreadPoolExecutor(max_workers=5) as executor:
        for dat in iterator:
            total_count.increment()
            process_list.put(dat)
            rec_count.increment()
            if rec_count.value == len(iterator.page):
                page_number.increment()
                executor.submit(
                    process_sc_chunk,
                    app=app,
                    vulns=pop_queue(queue=process_list, queue_len=len(iterator.page)),
                    page=page_number.value,
                    dir_path=dir_path,
                    sc=scanner,
                )
                rec_count.set(0)
    if total_count.value == 0:
        logger.warning("No Tenable SC data found.")
    return total_count.value


def pop_queue(queue: queue.Queue, queue_len: int) -> list:
    """
    Pop items from a queue

    :param queue.Queue queue: Queue object
    :param int queue_len: Length of the queue
    :return: List of items from the queue
    :rtype: list
    """
    retrieved_items = []

    # Use a for loop to get 1000 items
    for _ in range(queue_len):
        # Check if the queue is not empty
        if not queue.empty():
            # Get an item from the queue and append it to the list
            retrieved_items.append(queue.get())
        else:
            # Break the loop if the queue is empty
            break
    return retrieved_items


def process_sc_chunk(**kwargs: dict) -> None:
    """
    Process Tenable SC chunk

    :param dict **kwargs: Keyword arguments
    :rtype: None
    :return: None
    """
    # iterator.page, iterator.page_count, file_path, query_id, ssp_id
    vulns = kwargs.get("vulns")
    dir_path = kwargs.get("dir_path")
    generated_file_name = f"tenable_scan_page_{kwargs.get('page')}.pkl"
    pickled_file_handler = PickleFileHandler(str(dir_path / generated_file_name))
    sc = kwargs.get("sc")
    thread = current_thread()
    if not len(vulns):
        return
    # I can't add a to-do thanks to sonarlint, but we need to add CVE lookup from plugin id
    # append file to path
    # Process to RegScale
    tenable_vulns = [TenableAsset(**vuln) for vuln in vulns]
    # Empty "DNS" should just be IP
    for vuln in tenable_vulns:
        if not vuln.dnsName:
            vuln.dnsName = vuln.ip
    findings = []
    assets = []
    for vuln in tenable_vulns:
        findings += sc.parse_findings(vuln)
        if vuln.dnsName not in {asset.name for asset in assets}:  # avoid duplicates
            assets.append(sc.to_integration_asset(vuln, **kwargs))
    pickled_file_handler.write({"assets": assets, "findings": findings})

    logger.info(
        "Submitting %i findings and %i assets to the CLI Job Queue from Tenable SC Page %i...",
        len(findings),
        len(assets),
        kwargs.get("page"),
    )
    logger.debug(f"Completed thread: name={thread.name}, idnet={get_ident()}, id={get_native_id()}")


def get_last_pull_epoch(regscale_ssp_id: int) -> int:
    """
    Gather last pull epoch from RegScale Security Plan

    :param int regscale_ssp_id: RegScale System Security Plan ID
    :return: Last pull epoch
    :rtype: int

    """
    fmt: str = "%Y-%m-%d"
    two_months_ago: datetime = datetime.now() - timedelta(weeks=8)
    two_weeks_ago: datetime = datetime.now() - timedelta(weeks=2)
    last_pull: int = round(two_weeks_ago.timestamp())  # default the last pull date to two weeks
    # Limit the query with a filter_date to avoid taxing the database in the case of a large number of scans
    if res := ScanHistory.get_by_parent_recursive(
        parent_id=regscale_ssp_id, parent_module="securityplans", filter_date=two_months_ago.strftime(fmt)
    ):
        # order by ScanDate desc
        fmt = "%Y-%m-%dT%H:%M:%S"
        res = sorted(res, key=lambda x: datetime.strptime(x.scanDate, fmt), reverse=True)
        # Convert to timestampe
        last_pull = round((datetime.strptime(res[0].scanDate, fmt)).timestamp())
    return last_pull


@sc.command(name="list_tags")
def sc_tags():
    """List tags from Tenable"""
    list_tags()


def list_tags() -> None:
    """
    Query a list of tags on the server and print to console

    :rtype: None
    """
    tag_list = get_tags()
    pprint(tag_list)


def get_tags() -> list:
    """
    List of Tenable query definitions

    :return: List of unique tags for Tenable queries
    :rtype: list
    """
    client = gen_client()
    logger.debug(client._env_base)
    if client._env_base == "TSC":
        return client.queries.tags()
    return list(client.tags.list())


def gen_client() -> Union["TenableIO", "TenableSC"]:
    """
    Return the appropriate Tenable client based on the URL

    :return: Client type
    :rtype: Union["TenableIO", "TenableSC"]
    """
    app = Application()
    config = app.config
    if "cloud.tenable.com" in config["tenableUrl"]:
        return gen_tio(config)
    return gen_tsc(config)


def gen_tsc(config: dict) -> "TenableSC":
    """
    Generate Tenable Object

    :param dict config: Configuration dictionary
    :return: Tenable client
    :rtype: "TenableSC"
    """
    from tenable.sc import TenableSC

    if not config:
        app = Application()
        config = app.config
    return TenableSC(
        url=config["tenableUrl"],
        access_key=config["tenableAccessKey"],
        secret_key=config["tenableSecretKey"],
        vendor=REGSCALE_INC,
        product=REGSCALE_CLI,
        build=__version__,
    )


def gen_tio(config: dict) -> "TenableIO":
    """
    Generate Tenable Object

    :param dict config: Configuration dictionary
    :return: Tenable client
    :rtype: "TenableIO"
    """

    from tenable.io import TenableIO

    return TenableIO(
        url=config["tenableUrl"],
        access_key=config["tenableAccessKey"],
        secret_key=config["tenableSecretKey"],
        vendor=REGSCALE_INC,
        product=REGSCALE_CLI,
        build=__version__,
    )


def get_controls(catalog_id: int) -> List[Dict]:
    """
    Gets all the controls

    :param int catalog_id: catalog id
    :return: list of controls
    :rtype: List[Dict]
    """
    app = Application()
    api = Api()
    url = urljoin(app.config.get("domain"), f"/api/SecurityControls/getList/{catalog_id}")
    response = api.get(url)
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()
    return []


def create_control_implementations(
    controls: list,
    parent_id: int,
    parent_module: str,
    existing_implementation_dict: Dict,
    passing_controls: Dict,
    failing_controls: Dict,
) -> List[Dict]:
    """
    Creates a list of control implementations

    :param list controls: list of controls
    :param int parent_id: parent control id
    :param str parent_module: parent module
    :param Dict existing_implementation_dict: Dictionary of existing control implementations
    :param Dict passing_controls: Dictionary of passing controls
    :param Dict failing_controls: Dictionary of failing controls
    :return: list of control implementations
    :rtype: List[Dict]
    """
    app = Application()
    api = Api()
    user_id = app.config.get("userId")
    domain = app.config.get("domain")
    control_implementations = []
    to_create = []
    to_update = []
    for control in controls:
        lower_case_control_id = control["controlId"].lower()
        status = check_implementation(
            passing_controls=passing_controls,
            failing_controls=failing_controls,
            control_id=lower_case_control_id,
        )
        if control["controlId"] not in existing_implementation_dict.keys():
            cim = ControlImplementation(
                controlOwnerId=user_id,
                dateLastAssessed=get_current_datetime(),
                status=status,
                controlID=control["id"],
                parentId=parent_id,
                parentModule=parent_module,
                createdById=user_id,
                dateCreated=get_current_datetime(),
                lastUpdatedById=user_id,
                dateLastUpdated=get_current_datetime(),
            ).dict()
            cim["controlSource"] = "Baseline"
            to_create.append(cim)

        else:
            # update existing control implementation data
            existing_imp = existing_implementation_dict.get(control["controlId"])
            existing_imp["status"] = status
            existing_imp["dateLastAssessed"] = get_current_datetime()
            existing_imp["lastUpdatedById"] = user_id
            existing_imp["dateLastUpdated"] = get_current_datetime()
            del existing_imp["createdBy"]
            del existing_imp["systemRole"]
            del existing_imp["controlOwner"]
            del existing_imp["lastUpdatedBy"]
            to_update.append(existing_imp)

    if len(to_create) > 0:
        ci_url = urljoin(domain, "/api/controlImplementation/batchCreate")
        resp = api.post(url=ci_url, json=to_create)
        if resp.ok:
            control_implementations.extend(resp.json())
            logger.info(f"Created {len(to_create)} Control Implementation(s), Successfully!")
        else:
            resp.raise_for_status()
    if len(to_update) > 0:
        ci_url = urljoin(domain, "/api/controlImplementation/batchUpdate")
        resp = api.post(url=ci_url, json=to_update)
        if resp.ok:
            control_implementations.extend(resp.json())
            logger.info(f"Updated {len(to_update)} Control Implementation(s), Successfully!")
        else:
            resp.raise_for_status()
    return control_implementations


def check_implementation(passing_controls: Dict, failing_controls: Dict, control_id: str) -> str:
    """
    Checks the status of a control implementation

    :param Dict passing_controls: Dictionary of passing controls
    :param Dict failing_controls: Dictionary of failing controls
    :param str control_id: control id
    :return: status of control implementation
    :rtype: str
    """
    if control_id in passing_controls.keys():
        return FULLY_IMPLEMENTED
    elif control_id in failing_controls.keys():
        return IN_REMEDIATION
    else:
        return NOT_IMPLEMENTED


def get_existing_control_implementations(parent_id: int) -> Dict:
    """
    fetch existing control implementations

    :param int parent_id: parent control id
    :return: Dictionary of existing control implementations
    :rtype: Dict
    """
    app = Application()
    api = Api()
    domain = app.config.get("domain")
    existing_implementation_dict = {}
    get_url = urljoin(domain, f"/api/controlImplementation/getAllByPlan/{parent_id}")
    response = api.get(get_url)
    if response.ok:
        existing_control_implementations_json = response.json()
        for cim in existing_control_implementations_json:
            existing_implementation_dict[cim["controlName"]] = cim
        logger.info(f"Found {len(existing_implementation_dict)} existing control implementations")
    elif response.status_code == 404:
        logger.info(f"No existing control implementations found for {parent_id}")
    else:
        logger.warn(f"Unable to get existing control implementations. {response.text}")

    return existing_implementation_dict


def get_matched_controls(tenable_controls: List[Dict], catalog_controls: List[Dict]) -> List[Dict]:
    """
    Get controls that match between Tenable and the catalog

    :param List[Dict] tenable_controls: List of controls from Tenable
    :param List[Dict] catalog_controls: List of controls from the catalog
    :return: List of matched controls
    :rtype: List[Dict]
    """
    matched_controls = []
    for control in tenable_controls:
        formatted_control = convert_control_id(control)
        logger.info(formatted_control)
        for catalog_control in catalog_controls:
            if catalog_control["controlId"].lower() == formatted_control.lower():
                logger.info(f"Catalog Control {formatted_control} matched")
                matched_controls.append(catalog_control)
                break
    return matched_controls


def get_assessment_status_from_implementation_status(status: str) -> str:
    """
    Get the assessment status from the implementation status

    :param str status: Implementation status
    :return: Assessment status
    :rtype: str
    """
    if status == FULLY_IMPLEMENTED:
        return "Pass"
    if status == IN_REMEDIATION:
        return "Fail"
    else:
        return "N/A"


def create_assessment_from_cim(cim: Dict, user_id: str, control: Dict, check: List[AssetCheck]) -> Dict:
    """
    Create an assessment from a control implementation

    :param Dict cim: Control Implementation
    :param str user_id: User ID
    :param Dict control: Control
    :param List[AssetCheck] check: Asset Check
    :return: Assessment
    :rtype: Dict
    """
    assessment_result = get_assessment_status_from_implementation_status(cim.get("status"))
    summary_dict = check[0].dict() if check else dict()
    summary_dict.pop("reference", None)
    title = summary_dict.get("check_name") if summary_dict else control.get("title")
    html_summary = format_dict_to_html(summary_dict)
    document_reviewed = check[0].audit_file if check else None
    check_name = check[0].check_name if check else None
    methodology = check[0].check_info if check else None
    summary_of_results = check[0].description if check else None
    uuid = check[0].asset_uuid if check and check[0].asset_uuid is not None else None
    title_part = f"{title} - {uuid}" if uuid else f"{title}"
    uuid_title = f"{title_part} Automated Assessment test"
    return {
        "leadAssessorId": user_id,
        "title": uuid_title,
        "assessmentType": "Control Testing",
        "plannedStart": get_current_datetime(),
        "plannedFinish": get_current_datetime(),
        "status": "Complete",
        "assessmentResult": assessment_result if assessment_result else "N/A",
        "controlID": cim["id"],
        "actualFinish": get_current_datetime(),
        "assessmentReport": html_summary if html_summary else "Passed",
        "parentId": cim["id"],
        "parentModule": "controls",
        "assessmentPlan": check_name if check_name else None,
        "documentsReviewed": document_reviewed if document_reviewed else None,
        "methodology": methodology if methodology else None,
        "summaryOfResults": summary_of_results if summary_of_results else None,
    }


def get_control_assessments(control: Dict, assessments_to_create: List[Dict]) -> List[Dict]:
    """
    Get control assessments

    :param Dict control: Control
    :param List[Dict] assessments_to_create: List of assessments to create
    :return: List of control assessments
    :rtype: List[Dict]
    """
    return [
        assess
        for assess in assessments_to_create
        if assess["controlID"] == control["id"] and assess["status"] == "Complete"
    ]


def sort_assessments(control_assessments: List[Dict]) -> List[Dict]:
    """
    Sort assessments by actual finish date

    :param List[Dict] control_assessments: List of control assessments
    :return: Sorted assessments
    :rtype: List[Dict]
    """
    dt_format = "%Y-%m-%d %H:%M:%S"
    return sorted(
        control_assessments,
        key=lambda x: datetime.strptime(x["actualFinish"], dt_format),
        reverse=True,
    )


def update_control_object(control: Dict, sorted_assessments: List[Dict]) -> None:
    """
    Update control object

    :param Dict control: Control
    :param List[Dict] sorted_assessments: Sorted assessments
    :rtype: None
    """
    dt_format = "%Y-%m-%d %H:%M:%S"
    app = Application()
    control["dateLastAssessed"] = sorted_assessments[0]["actualFinish"]
    control["lastAssessmentResult"] = sorted_assessments[0]["assessmentResult"]
    if control.get("lastAssessmentResult"):
        control_obj = ControlImplementation(**control)
        if control_obj.lastAssessmentResult == "Fail" and control_obj.status != IN_REMEDIATION:
            control_obj.status = IN_REMEDIATION
            control_obj.plannedImplementationDate = (datetime.now() + timedelta(30)).strftime(dt_format)
            control_obj.stepsToImplement = "n/a"
        elif control_obj.status == IN_REMEDIATION:
            control_obj.plannedImplementationDate = (
                (datetime.now() + timedelta(30)).strftime(dt_format)
                if not control_obj.plannedImplementationDate
                else control_obj.plannedImplementationDate
            )
            control_obj.stepsToImplement = "n/a" if not control_obj.stepsToImplement else control_obj.stepsToImplement
        elif control_obj.lastAssessmentResult == "Pass" and control_obj.status != FULLY_IMPLEMENTED:
            control_obj.status = FULLY_IMPLEMENTED
        ControlImplementation.update(app=app, implementation=control_obj)


def update_control_implementations(control_implementations: List[Dict], assessments_to_create: List[Dict]) -> None:
    """
    Update control implementations with assessments

    :param List[Dict] control_implementations: List of control implementations
    :param List[Dict] assessments_to_create: List of assessments to create
    :rtype: None
    """
    for control in control_implementations:
        control_assessments = get_control_assessments(control, assessments_to_create)
        if sorted_assessments := sort_assessments(control_assessments):
            update_control_object(control, sorted_assessments)


def post_assessments_to_api(assessments_to_create: List[Dict]) -> None:
    """
    Post assessments to the API

    :param List[Dict] assessments_to_create: List of assessments to create
    :rtype: None
    """
    app = Application()
    api = Api()
    assessment_url = urljoin(app.config.get("domain", ""), "/api/assessments/batchCreate")
    assessment_response = api.post(url=assessment_url, json=assessments_to_create)
    if assessment_response.ok:
        logger.info(f"Created {len(assessment_response.json())} Assessments!")
    else:
        logger.debug(assessment_response.status_code)
        logger.error(f"Failed to insert Assessment.\n{assessment_response.text}")


def create_assessments(
    control_implementations: List[Dict],
    catalog_controls_dict: Dict,
    asset_checks: Dict,
) -> None:
    """
    Create assessments from control implementations

    :param List[Dict] control_implementations: List of control implementations
    :param Dict catalog_controls_dict: Dictionary of catalog controls
    :param Dict asset_checks: Dictionary of asset checks
    :rtype: None
    :return: None
    """
    app = Application()
    user_id = app.config.get("userId", "")
    assessments_to_create = []
    for cim in control_implementations:
        control = catalog_controls_dict.get(cim["controlID"], {})
        check = asset_checks.get(control["controlId"].lower())
        assessment = create_assessment_from_cim(cim, user_id, control, check)
        assessments_to_create.append(assessment)
    update_control_implementations(control_implementations, assessments_to_create)
    post_assessments_to_api(assessments_to_create)


def process_compliance_data(
    framework_data: Dict,
    catalog_id: int,
    ssp_id: int,
    framework: str,
    passing_controls: Dict,
    failing_controls: Dict,
) -> None:
    """
    Processes the compliance data from Tenable.io to create control implementations for controls in frameworks

    :param Dict framework_data: List of tenable.io controls per framework
    :param int catalog_id: The catalog id
    :param int ssp_id: The ssp id
    :param str framework: The framework name
    :param Dict passing_controls: Dictionary of passing controls
    :param Dict failing_controls: Dictionary of failing controls
    :rtype: None
    """
    if not framework_data:
        return
    framework_controls = framework_data.get("controls", {})
    asset_checks = framework_data.get("asset_checks", {})
    existing_implementation_dict = get_existing_control_implementations(ssp_id)
    catalog_controls = get_controls(catalog_id)
    matched_controls = []
    for tenable_framework, tenable_controls in framework_controls.items():
        logger.info(f"Found {len(tenable_controls)} controls that passed for framework: {tenable_framework}")
        # logger.info(f"tenable_controls: {tenable_controls[0]}") if len(tenable_controls) >0 else None
        if tenable_framework == framework:
            matched_controls = get_matched_controls(tenable_controls, catalog_controls)

    logger.info(f"Found {len(matched_controls)} controls that matched")

    control_implementations = create_control_implementations(
        controls=matched_controls,
        parent_id=ssp_id,
        parent_module="securityplans",
        existing_implementation_dict=existing_implementation_dict,
        passing_controls=passing_controls,
        failing_controls=failing_controls,
    )

    logger.info(f"SSP now has {len(control_implementations)} control implementations")
    catalog_controls_dict = {c["id"]: c for c in catalog_controls}
    create_assessments(control_implementations, catalog_controls_dict, asset_checks)


def convert_control_id(control_id: str) -> str:
    """
    Convert the control id to a format that can be used in Tenable.io

    :param str control_id: The control id to convert
    :return: The converted control id
    :rtype: str
    """
    # Convert to lowercase
    control_id = control_id.lower()

    # Check if there's a parenthesis and replace its content
    if "(" in control_id and ")" in control_id:
        inner_value = control_id.split("(")[1].split(")")[0]
        control_id = control_id.replace(f"({inner_value})", f".{inner_value}")

    return control_id


@io.command(name="sync_compliance_controls")
@regscale_ssp_id()
@click.option(
    "--catalog_id",
    type=click.INT,
    help="The ID number from RegScale Catalog that the System Security Plan's controls belong to",
    prompt="Enter RegScale Catalog ID",
    required=True,
)
@click.option(
    "--framework",
    required=True,
    type=click.Choice(["800-53", "800-53r5", "CSF", "800-171"], case_sensitive=True),
    help="The framework to use. from Tenable.io frameworks MUST be the same RegScale Catalog of controls",
)
@hidden_file_path(help="The file path to load control data instead of fetching from Tenable.io")
def sync_compliance_data(regscale_ssp_id: int, catalog_id: int, framework: str, offline: Optional[Path] = None):
    """
    Sync the compliance data from Tenable.io to create control implementations for controls in frameworks.
    """
    _sync_compliance_data(ssp_id=regscale_ssp_id, catalog_id=catalog_id, framework=framework, offline=offline)


def _sync_compliance_data(ssp_id: int, catalog_id: int, framework: str, offline: Optional[Path] = None) -> None:
    """
    Sync the compliance data from Tenable.io to create control implementations for controls in frameworks
    :param int ssp_id: The ID number from RegScale of the System Security Plan
    :param int catalog_id: The ID number from RegScale Catalog that the System Security Plan's controls belong to
    :param str framework: The framework to use. from Tenable.io frameworks MUST be the same RegScale Catalog of controls
    :param Optional[Path] offline: The file path to load control data instead of fetching from Tenable.io, defaults to None
    :rtype: None
    """
    logger.info("Note: This command only available for Tenable.io")
    logger.info("Note: This command Requires admin access.")
    app = Application()
    config = app.config
    # we specifically don't gen client here, so we only get the client for Tenable.io as its only supported there

    compliance_data = _get_compliance_data(config=config, offline=offline)  # type: ignore

    dict_of_frameworks_and_asset_checks: Dict = dict()
    framework_controls: Dict[str, List[str]] = {}
    asset_checks: Dict[str, List[AssetCheck]] = {}
    passing_controls: Dict = dict()
    # partial_passing_controls: Dict = dict()
    failing_controls: Dict = dict()
    for findings in compliance_data:
        asset_check = AssetCheck(**findings)
        for ref in asset_check.reference:
            if ref.framework not in framework_controls:
                framework_controls[ref.framework] = []
            if ref.control not in framework_controls[ref.framework]:  # Avoid duplicate controls
                framework_controls[ref.framework].append(ref.control)
                formatted_control_id = convert_control_id(ref.control)
                # sort controls by status
                add_control_to_status_dict(
                    control_id=formatted_control_id,
                    status=asset_check.status,
                    dict_obj=failing_controls,
                    desired_status="FAILED",
                )
                add_control_to_status_dict(
                    control_id=formatted_control_id,
                    status=asset_check.status,
                    dict_obj=passing_controls,
                    desired_status="PASSED",
                )
                remove_passing_controls_if_in_failed_status(passing=passing_controls, failing=failing_controls)
                if formatted_control_id not in asset_checks:
                    asset_checks[formatted_control_id] = [asset_check]
                else:
                    asset_checks[formatted_control_id].append(asset_check)
        dict_of_frameworks_and_asset_checks = {
            key: {"controls": framework_controls, "asset_checks": asset_checks} for key in framework_controls.keys()
        }
    logger.info(f"Found {len(dict_of_frameworks_and_asset_checks)} findings to process")
    framework_data = dict_of_frameworks_and_asset_checks.get(framework, None)
    process_compliance_data(
        framework_data=framework_data,
        catalog_id=catalog_id,
        ssp_id=ssp_id,
        framework=framework,
        passing_controls=passing_controls,
        failing_controls=failing_controls,
    )


def _get_compliance_data(config: dict, offline: Optional[Path] = None) -> Dict:
    """
    Get compliance data from Tenable.io

    :param dict config: Configuration dictionary
    :param Optional[Path] offline: File path to load control data instead of fetching from Tenable.io
    :return: Compliance data
    :rtype: Dict
    """
    from tenable.io import TenableIO

    if offline:
        with open(offline.absolute(), "r") as f:
            compliance_data = json.load(f)
    else:
        client = TenableIO(
            url=config["tenableUrl"],
            access_key=config["tenableAccessKey"],
            secret_key=config["tenableSecretKey"],
            vendor=REGSCALE_INC,
            product=REGSCALE_CLI,
            build=__version__,
        )
        compliance_data = client.exports.compliance()
    return compliance_data


def add_control_to_status_dict(control_id: str, status: str, dict_obj: Dict, desired_status: str) -> None:
    """
    Add a control to a status dictionary

    :param str control_id: The control id to add to the dictionary
    :param str status: The status of the control
    :param Dict dict_obj: The dictionary to add the control to
    :param str desired_status: The desired status of the control
    :rtype: None
    """
    friendly_control_id = control_id.lower()
    if status == desired_status and friendly_control_id not in dict_obj:
        dict_obj[friendly_control_id] = desired_status


def remove_passing_controls_if_in_failed_status(passing: Dict, failing: Dict) -> None:
    """
    Remove passing controls if they are in failed status

    :param Dict passing: Dictionary of passing controls
    :param Dict failing: Dictionary of failing controls
    :rtype: None
    """
    to_remove = []
    for k in passing.keys():
        if k in failing.keys():
            to_remove.append(k)

    for k in to_remove:
        del passing[k]


def write_io_chunk(
    data: List[dict],
    data_dir: Path,
    export_uuid: str,
    export_type: str,
    export_chunk_id: int,
) -> None:
    """
    Write a chunk of data to a file, this function is formatted for use with PyTenable and Tenable IO

    :param List[dict] data: Data to write to a file
    :param Path data_dir: Directory to write the file to
    :param str export_uuid: UUID of the export (Tenable IO)
    :param str export_type: Type of export (Tenable IO)
    :param int export_chunk_id: ID of the chunk (Tenable IO)
    :rtype: None
    """
    # create tenable io directory
    data_dir.mkdir(parents=True, exist_ok=True)
    fn = data_dir / f"{export_type}-{export_uuid}-{export_chunk_id}.json"
    # append file to path
    with open(file=fn, mode="w", encoding="utf-8") as file_object:
        json.dump(data, file_object)


def process_to_regscale(data_dir: Path, ssp_id: int, existing_assets: List[Asset]) -> None:
    """
    Process the Tenable data to RegScale

    :param Path data_dir: Directory to process the data from
    :param int ssp_id: The ID of the System Security Plan
    :param List[Asset] existing_assets: List of existing assets
    :rtype: None
    :return: None
    """
    # get all files in the directory
    files = list(data_dir.glob("*.json"))
    if not files:
        logger.warning("No Tenable files found in %s.", data_dir)
        return
    logger.info("Processing %i chunked file(s) from Tenable...", len(list(files)))
    for file in files:
        logger.info("Processing chunked data: %s", file)
        file_assets = []
        with open(file=file, mode="r", encoding="utf-8") as file_object:
            tenable_io_data = json.load(file_object)
            for asset in tenable_io_data:
                file_assets.append(TenableIOAsset(**asset))
        TenableIOAsset.sync_to_regscale(assets=file_assets, ssp_id=ssp_id, existing_assets=existing_assets)
        # remove processed file
        file.unlink()
