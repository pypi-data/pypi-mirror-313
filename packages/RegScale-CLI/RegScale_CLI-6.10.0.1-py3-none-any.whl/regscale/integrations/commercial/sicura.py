#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Integration of Sicura into RegScale CLI tool """

# standard python imports
from json import JSONDecodeError
from typing import Optional

import click
import requests
from rich.progress import track

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.utils.app_utils import (
    check_license,
    error_and_exit,
    get_current_datetime,
    remove_timezone_from_date_str,
)
from regscale.core.app.utils.regscale_utils import verify_provided_module
from regscale.models import regscale_id as reg_id, regscale_module as reg_module, regscale_models
from regscale.models.regscale_models.asset import Asset
from regscale.models.regscale_models.checklist import Checklist


@click.group()
def sicura():
    """Sicura integration"""


@sicura.command(name="sync_nodes")
@reg_id()
@reg_module()
@click.option(
    "--node_id",
    type=click.INT,
    help="ID # for Sicura node to sync in RegScale. If none provided, all nodes will be synced.",
    prompt=False,
    default=None,
)
def sync_sicura_and_regscale(regscale_id: int, regscale_module, node_id: Optional[int] = None):
    """Sync nodes from Sicura to RegScale as assets"""
    sync_sicura_nodes_and_regscale_assets(regscale_id, regscale_module, node_id)


def sync_sicura_nodes_and_regscale_assets(regscale_id: int, regscale_module: str, node_id: Optional[int] = None):
    """
    Get all nodes from Sicura
    :param int regscale_id: ID # for RegScale instance to sync to
    :param str regscale_module: Module to Sicura nodes to in RegScale
    :param Optional[int] node_id: ID # for Sicura node to sync to RegScale, defaults to None
    """
    verify_provided_module(regscale_module)
    app = check_license()
    api = Api()
    # get all the nodes from Sicura
    nodes = fetch_nodes_from_sicura(api, node_id)
    # get all assets from RegScale
    existing_assets = Asset.get_all_by_parent(regscale_id, regscale_module)
    regscale_sicura_ids = {asset.sicuraId: asset for asset in existing_assets}
    sicura_node_ids = {str(node["id"]): node for node in nodes}
    created_assets, updated_assets = {}, {}
    if new_assets := [
        map_asset(node, regscale_id, regscale_module, app.config["userId"])
        for node in nodes
        if str(node["id"]) not in regscale_sicura_ids
    ]:
        created_assets = bulk_asset_operation("insert", app, new_assets)
    if update_assets := [asset for asset in existing_assets if asset.sicuraId in sicura_node_ids]:
        updated_assets = bulk_asset_operation("update", app, update_assets)
    for asset in track(
        {**created_assets, **updated_assets}.values(),
        description="Syncing Sicura Node(s) & Scan(s) to RegScale asset(s)...",
    ):
        existing_checks = {check.vulnerabilityId: check for check in Checklist.get_checklists_by_asset(api, asset.id)}
        results = sync_sicura_and_regscale_checks(app, asset, sicura_node_ids[asset.sicuraId]["scans"], existing_checks)
        inserted_count = len(results["inserted"])
        updated_count = len(results["updated"])
        if inserted_count or updated_count:
            app.logger.info(
                "Successfully created %i and updated %i checklist(s) for asset %s in RegScale.",
                inserted_count,
                updated_count,
                asset.name,
            )


def bulk_asset_operation(method: str, app: Application, assets: list[Asset]) -> dict:
    """
    Function to run bulk asset operations and returns the data after logging the results

    :param str method: Either 'insert' or 'update'
    :param Application app: Application object
    :param list[Asset] assets: List of assets to insert or update
    :return: dictionary containing the results of the bulk operation
    :rtype: dict
    """
    if method == "insert":
        results = Asset.bulk_insert(app, assets)
    elif method == "update":
        results = Asset.bulk_update(app, assets)
    else:
        error_and_exit(f"Invalid method provided: {method}. Must be 'insert' or 'update'.")
    method = f"{method}d" if method == "update" else "created"
    failures = [f"{res.status_code}: {res.reason}-{res.text}" for res in results if not res.ok]
    successes = {res.json()["id"]: Asset(**res.json()) for res in results if res.ok}
    app.logger.info(
        "%s %i/%i asset(s) in RegScale. With %i failure(s).",
        method.capitalize(),
        len(successes),
        len(results),
        len(failures),
    )
    if failures:
        app.logger.error("Failed to %s %i asset(s) in RegScale.", method[:-1], len(failures))
        app.logger.warning("Failure message(s):\n%s", "\n".join(failures))
    return successes


def get_most_recent_scan(scans: list[dict], date_field: Optional[str] = "scan_date") -> dict:
    """
    Function to get the most recent scan from a list of Sicura scans by the provided field in the scan metadata

    :param list[dict] scans: List of scans to get the most recent from using the provided field
    :param Optional[str] date_field: Field to use for determining the most recent scan, defaults to "scan_date"
    :return: Most recent scan from the provided list using the provided field
    :rtype: dict
    """
    return sorted(scans, key=lambda scan: scan["scan_metadata"][date_field])[-1]


def map_sicura_result(result: str) -> str:
    """
    Function to map Sicura result to RegScale security checklist result

    :param str result: Sicura result to map to RegScale security checklist result
    :return: RegScale security checklist result
    :rtype: str
    """
    if result.lower() in ["pass", "fail"]:
        return result.title()
    elif result.lower() == "notapplicable":
        return "Not Applicable"
    else:
        return "Not Reviewed"


def sync_sicura_and_regscale_checks(
    app: Application,
    regscale_asset: Asset,
    sicura_scans: list[dict],
    existing_checklists: Optional[dict] = None,
) -> dict:
    """
    Function to map Sicura scan results to securityChecklists in RegScale and posts them if they don't already exist

    :param Application app: Application object
    :param Asset regscale_asset: RegScale asset object to associate vulnerabilities with
    :param list[dict] sicura_scans: Sicura scans to create vulnerabilities from
    :param Optional[dict] existing_checklists: Existing checklists for the provided asset as a dictionary
    :return: Dictionary of results of batch processing
    :rtype: dict
    """
    new_checks = []
    recent_scan = get_most_recent_scan(sicura_scans)
    for sicura_scan in recent_scan["scans"]:
        scan_date = remove_timezone_from_date_str(recent_scan["scan_metadata"]["scan_date"])
        new_checks.append(
            Checklist(
                status=map_sicura_result(sicura_scan["result"]),
                assetId=regscale_asset.id,
                tool="CIS Benchmarks",
                baseline="N/A",
                vulnerabilityId=sicura_scan["name"],
                ruleId=parse_plugin_id(sicura_scan["name"]),
                check=sicura_scan["description"],
                results=sicura_scan["result"],
                comments=f"Imported from Sicura Node #{regscale_asset.sicuraId} on {get_current_datetime('%b %d, %Y')}",
                createdById=app.config["userId"],
                lastUpdatedById=app.config["userId"],
                datePerformed=scan_date,
            )
        )
    return Checklist.analyze_and_batch_process(app, new_checks, [check for check in existing_checklists.values()])


def convert_string_to_int(string: Optional[str] = "0") -> int:
    """
    Function to convert a string to an int

    :param Optional[str] string: String to convert to an int, defaults to "0"
    :return: Int value of the provided string
    :rtype: int
    """
    string_val = string.split(" ")[0]
    # check if decimal is in the string, round down to the nearest whole number
    if "." in string_val:
        return int(string_val.split(".")[0])
    return int(string_val)


def map_asset(sicura_node: dict, parent_id: int, parent_module: str, user_id: str) -> Asset:
    """
    Map a Sicura node to a RegScale asset

    :param dict sicura_node: Node from sicura to map to RegScale asset
    :param int parent_id: ID # for parent record
    :param str parent_module: to use for parent record
    :param str user_id: ID # for user to use for asset owner
    :return: RegScale asset object
    :rtype: Asset
    """
    new_asset = Asset(
        sicuraId=sicura_node["id"],
        name=sicura_node["name"],
        parentModule=parent_module,
        parentId=parent_id,
        assetOwnerId=user_id,
        fqdn=sicura_node["fqdn"],
        ipAddress=sicura_node["ip_address"],
        description=sicura_node["text"],
        assetCategory=regscale_models.AssetCategory.Hardware,
        assetType="Virtual Machine (VM)",
        status="Off-Network",
        scanningTool="Sicura",
        bScanWeb=True,
    )
    if properties := sicura_node.get("properties"):
        new_asset.uuid = properties.get("uuid")
        new_asset.bVirtual = properties.get("is_virtual")
        new_asset.iPv6Address = properties.get("ipaddress6")
        new_asset.macAddress = properties.get("macaddress")
        new_asset.manufacturer = properties.get("manufacturer")
        new_asset.operatingSystem = properties.get("os.name")
        new_asset.osVersion = properties.get("operatingsystemrelease")
        new_asset.cpu = properties.get("processorcount")
        new_asset.ram = convert_string_to_int(properties.get("memorysize")) if properties.get("memorysize") else 0
        new_asset.diskStorage = (
            convert_string_to_int(properties.get("mountpoints./.size")) if properties.get("mountpoints./.size") else 0
        )
        new_asset.serialNumber = properties.get("serialnumber")
    return new_asset


def fetch_nodes_from_sicura(api: Api, node_id: Optional[int] = None) -> list[dict]:
    """
    Function to fetch all nodes or a specific node from Sicura
    :param Api api: API Object for API calls
    :param Optional[int] node_id: ID # for Sicura node to fetch, defaults to None
    :return: List of nodes from Sicura
    :rtype: list[dict]
    """
    base_url = f'{api.config["sicuraUrl"]}/api/infrastructure/v1/'
    # set the params for the call
    params = {"verbose": "true", "attributes": "parent,scans,properties,children,text"}
    nodes = []
    node_url = f'{base_url}nodes{f"/{node_id}" if node_id else ""}'
    nodes_response = api.get(
        node_url,
        headers={"auth-token-signature": api.config["sicuraToken"]},
        params=params,
    )
    if not isinstance(nodes_response, requests.Response):
        error_and_exit(
            f"Please verify your sicuraUrl in init.yaml is correct. Currently set to: {api.config['sicuraUrl']}"
        )
    api.logger.debug(
        "Received response from Sicura: %i %s",
        nodes_response.status_code,
        nodes_response.text,
    )
    if not nodes_response.ok:
        error_and_exit(
            f"Received unexpected response from {node_url}.\n{nodes_response.status_code} {nodes_response.reason}"
        )
    try:
        nodes = nodes_response.json()
    except JSONDecodeError:
        error_and_exit(f"Unable to decode JSON from {node_url}")
    # if the provided node_id is a folder, we need to get its children items
    if node_id and nodes["type"] == "folder":
        params = {"verbose": "true", "filter[parent]": node_id}
        try:
            nodes_res = api.get(
                f"{base_url}nodes",
                params=params,
                headers={"auth-token-signature": api.config["sicuraToken"]},
            )
            api.logger.debug(
                "Received response from Sicura: %i %s",
                nodes_res.text,
                nodes_res.reason,
            )
            nodes = nodes_res.json()
        except JSONDecodeError:
            error_and_exit(f"Unable to decode JSON from {node_url}")
        # set node_id to None to filter out the folders
        node_id = None
    if not node_id:
        # No node ID was passed in, so filter out the folders
        nodes = [node for node in nodes if node["type"] == "endpoint"]
    # check to see if the response is a list or a single node
    if isinstance(nodes, dict):
        nodes = [nodes]
    for node in nodes:
        # get the scans for each node
        node["scans"] = get_scans_from_sicura(api, node["id"])
    return nodes or error_and_exit("No nodes found in Sicura.")


def get_scans_from_sicura(api: Api, node_id: int) -> dict:
    """
    Function to get all scans for a given node or set of nodes from Sicura

    :param Api api: API Object for API calls
    :param int node_id: ID # of Sicura node to get scans for
    :return: Dictionary containing scan info for the provided node ID
    :rtype: dict
    """
    # first get the profile for the Node to get the scans
    benchmark = ""
    sicura_scans = []
    response = api.get(
        f'{api.config["sicuraUrl"]}/api/infrastructure/v1/scans',
        headers={"auth-token-signature": api.config["sicuraToken"]},
        params={"verbose": "true", "filter[node_id]": node_id},
    )
    if not response.ok:
        error_and_exit(f"Unable to fetch scan info from {response.url}.\n{response.status_code} {response.reason}")
    try:
        benchmark = response.json()[0]["benchmark"]
    except JSONDecodeError:
        error_and_exit(f"Unable to fetch scan info from {response.url}.\n{response.status_code} {response.reason}")
    if not benchmark:
        error_and_exit(f"No benchmark found for node {node_id}.")
    params = {
        "verbose": "true",
        "profile": benchmark,
        "attributes": "id,benchmark,scan_metadata,scans,pass_status,text",
        "filter[id]": node_id,
    }
    scan_res = api.get(
        f'{api.config["sicuraUrl"]}/api/infrastructure/v1/nodes',
        headers={"auth-token-signature": api.config["sicuraToken"]},
        params=params,
    )
    try:
        sicura_scans = scan_res.json()
    except JSONDecodeError:
        api.logger.info(
            "Unable to fetch scan info from %s.\n%i %s",
            scan_res.url,
            scan_res.status_code,
            scan_res.reason,
        )
    return sicura_scans


def parse_plugin_id(plugin_name: str) -> Optional[str]:
    """
    Function to parse the plugin ID from the plugin name

    :param str plugin_name: Plugin ID to parse
    :return: Parsed plugin ID or None
    :rtype: Optional[str]
    """
    # limit string length to prevent regex from taking too long
    plugin_name = plugin_name[:100]
    # Define a regular expression pattern to find an integer
    pattern1 = r"(\d{1,8}:\d{1,8}:\d{1,8}(?::\d{1,8}){0,8})"
    pattern2 = r"(\d{1,8}r\d{1,8})"

    # imported locally because it's only used here
    import re

    # Use re.search to find the first integer in the string
    # Check if the first pattern was found and return it
    if match1 := re.search(pattern1, plugin_name):
        # Extract and return the matched integer as an integer type
        return match1.group(1)
    # Check if the second pattern was found and return it
    if match2 := re.search(pattern2, plugin_name):
        return match2.group(1)
    # Return None if no integer was found
    return None
