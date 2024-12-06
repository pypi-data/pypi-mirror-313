#!/usr/bin/python
""" Script to parse a .xlsx file and load the inventory into RegScale as assets"""

import json
import re
from datetime import datetime
from json import JSONDecodeError
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from regscale.core.utils.date import date_str

if TYPE_CHECKING:
    import pandas as pd  # Optimize import performance

from rich.console import Console
from rich.progress import track

from regscale.core.app.api import Api
from regscale.models import Asset

api = Api()
config = api.config
console = Console()

SOFTWARE_VENDOR = "Software/ Database Vendor"
SOFTWARE_NAME = "Software/ Database Name & Version"
PATCH_LEVEL = "Patch Level"
HARDWARE_MAKE = "Hardware Make/Model"
MAC_ADDRESS = "MAC Address"
OS_NAME = "OS Name and Version"
fmt = "%Y-%m-%d %H:%M:%S"


def import_inventory(
    file: Path,
    sheet_name: str,
    module_id: int,
    module: str,
):
    """
    Import inventory into RegScale from a .xlsx file
    """
    upload(
        inventory=str(file),
        sheet_name=sheet_name,
        record_id=module_id,
        module=module,
    )


def check_text(text: Optional[str] = None) -> str:
    """
    Check for NULL values and return empty string if NULL
    :param Optional[str] text: string to check if it is NULL, defaults to None
    :return: empty string if NULL, otherwise the string
    :rtype: str
    """
    return str(text or "")


def save_to_json(file_name: str, data: Any) -> None:
    """
    Save the data to a JSON file
    :param str file_name: name of the file to save
    :param Any data: data to save to the file
    :rtype: None
    """
    if not data:
        return
    if isinstance(data, list) and isinstance(data[0], Asset):
        lst = []
        for item in data:
            lst.append(item.dict())
        data = lst

    elif not isinstance(data, str):
        lst = []
        for key, value in data.items():
            lst.append(data[key]["asset"].dict())
        data = lst

    if file_name.endswith(".json"):
        file_name = file_name[:-5]
    with open(f"{file_name}.json", "w") as outfile:
        outfile.write(json.dumps(data, indent=4))


def map_str_to_bool(value: Optional[Union[bool, str]] = None) -> bool:
    """
    Map a string to a boolean value
    :param Optional[Union[bool, str]] value: string or bool value to map to a bool, defaults to False
    :return: boolean value
    :rtype: bool
    """
    if isinstance(value, bool):
        return value
    if value.lower() in ["yes", "true"]:
        return True
    elif value.lower() in ["no", "false"]:
        return False
    else:
        return False


def determine_ip_address_version(ip_address: Optional[str] = None) -> Optional[str]:
    """
    Determine if the IP address is IPv4 or IPv6
    :param Optional[str] ip_address: IP address to check, defaults to None
    :return: Key for the IP address version in the asset object
    :rtype: Optional[str]
    """
    if not isinstance(ip_address, str) or not ip_address:
        return None

    # Define a regular expression for IPv4
    ipv4_pattern = r"^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\."
    ipv4_pattern += r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\."
    ipv4_pattern += r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\."
    ipv4_pattern += r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"

    # Define a regular expression for IPv6
    ipv6_pattern = r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|"
    ipv6_pattern += r"([0-9a-fA-F]{1,4}:){1,7}:|"
    ipv6_pattern += r"([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|"
    ipv6_pattern += r"([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|"
    ipv6_pattern += r"([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|"
    ipv6_pattern += r"([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|"
    ipv6_pattern += r"([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|"
    ipv6_pattern += r"[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|"
    ipv6_pattern += r":((:[0-9a-fA-F]{1,4}){1,7}|:)|"
    ipv6_pattern += r"fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|"
    ipv6_pattern += r"::(ffff(:0{1,4}){0,1}:){0,1}"
    ipv6_pattern += r"((25[0-5]|(2[0-4]|1{0,1}[0-9])"
    ipv6_pattern += r"[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9])[0-9])))"
    # Check for IPv4
    try:
        if re.fullmatch(ipv4_pattern, ip_address):
            return "IPAddress"
        # Check for IPv6
        elif re.fullmatch(ipv6_pattern, ip_address):
            return "IPv6Address"
        else:
            return None
    except Exception:
        return None


def determine_asset_category(inventory: dict) -> str:
    """
    Determine the asset category based on the inventory item
    :param dict inventory: inventory item to parse & determine the asset category
    :return: asset category of Hardware, Software, or Unknown
    :rtype: str
    """
    software_fields = [
        check_text(inventory[SOFTWARE_VENDOR]),
        check_text(inventory[SOFTWARE_NAME]),
        check_text(inventory[PATCH_LEVEL]),
    ]
    hardware_fields = [
        check_text(inventory[HARDWARE_MAKE]),
        check_text(inventory[MAC_ADDRESS]),
        check_text(inventory[OS_NAME]),
    ]
    software_set = set(software_fields)
    hardware_set = set(hardware_fields)
    if len(hardware_set) > len(software_set):
        return "Hardware"
    if len(software_set) > len(hardware_set):
        return "Software"
    return "Unknown"


def map_inventory_to_asset(inventory: dict, parent_id: int, parent_module: str) -> Asset:
    """
    Map the inventory to a RegScale asset
    :param dict inventory: inventory item to map to a RegScale asset
    :param int parent_id: RegScale Record ID to use as parentId
    :param str parent_module: RegScale Module to use as parentModule
    :return: RegScale asset
    :rtype: Asset
    """
    # create a new asset
    asset_category = determine_asset_category(inventory)
    new_asset = {
        "id": 0,
        "isPublic": True,
        "uuid": "",
        "name": check_text(inventory["UNIQUE ASSET IDENTIFIER"]),
        "otherTrackingNumber": "",
        "serialNumber": check_text(inventory["Serial #/Asset Tag#"]),
        "macAddress": check_text(inventory[MAC_ADDRESS]),
        "manufacturer": "",
        "model": check_text(inventory[HARDWARE_MAKE]),
        "assetOwnerId": config["userId"],
        "systemAdministratorId": None,
        "operatingSystem": "",
        "osVersion": check_text(inventory[OS_NAME]),
        "assetType": check_text(inventory["Asset Type"]) or "Unknown",
        "location": check_text(inventory["Location"]),
        "cmmcAssetType": "",
        "cpu": 0,
        "ram": 0,
        "diskStorage": 0,
        "description": "",
        "endOfLifeDate": date_str(inventory.get("End-of-Life ")),
        "purchaseDate": None,
        "status": "Active (On Network)",
        "wizId": "",
        "wizInfo": "",
        "notes": check_text(inventory["Comments"]),
        "softwareVendor": "",
        "softwareName": check_text(inventory[SOFTWARE_VENDOR]),
        "softwareVersion": check_text(inventory[SOFTWARE_NAME]),
        "softwareFunction": check_text(inventory["Function"]),
        "patchLevel": check_text(inventory[PATCH_LEVEL]),
        "assetCategory": asset_category,
        "bVirtual": map_str_to_bool(inventory["Virtual"]),
        "bPublicFacing": map_str_to_bool(inventory["Public"]),
        "bAuthenticatedScan": map_str_to_bool(inventory["Authenticated Scan"]),
        "bLatestScan": map_str_to_bool(inventory["In Latest Scan"]),
        "netBIOS": check_text(inventory["NetBIOS Name"]),
        "baselineConfiguration": check_text(inventory["Baseline Configuration Name"]),
        "fqdn": check_text(inventory["DNS Name or URL"]),
        "assetTagNumber": "",
        "vlanId": check_text(inventory["VLAN/\nNetwork ID"]),
        "facilityId": None,
        "orgId": None,
        "parentId": parent_id,
        "parentModule": parent_module,
        "createdById": config["userId"],
        "dateCreated": datetime.now().strftime(fmt),
        "lastUpdatedById": config["userId"],
        "dateLastUpdated": datetime.now().strftime(fmt),
    }
    ip_address = check_text(inventory["IPv4 or IPv6\nAddress"])
    ipaddress_key = determine_ip_address_version(ip_address)
    if ipaddress_key and ip_address != "":
        new_asset[ipaddress_key] = ip_address
    if asset_category == "Hardware":
        new_asset["purpose"] = check_text(inventory["Function"])
    elif asset_category == "Software":
        new_asset["softwareFunction"] = check_text(inventory["Function"])
    return Asset(**new_asset)


def create_properties(data: dict, parent_id: int, parent_module: str) -> bool:
    """
    Create a list of properties and upload them to RegScale for the provided asset
    :param dict data: Dictionary of data to parse and create properties from
    :param int parent_id: ID to create properties for
    :param str parent_module: Parent module to create properties for
    :return: If batch update was successful
    :rtype: bool
    """
    import numpy as np  # Optimize import performance

    properties: list = []
    retry = 0
    for key, value in data.items():
        # skip the item if the key is id or contains unnamed
        if "unnamed" in key.lower():
            continue
        # see if the value is datetime
        elif isinstance(value, datetime):
            value = value.strftime("%b %d, %Y")
        # see if the value is a boolean
        elif isinstance(value, np.bool_):
            value = str(value).title()
        regscale_property = {
            "id": 0,
            "createdById": config["userId"],
            "dateCreated": None,
            "lastUpdatedById": config["userId"],
            "isPublic": True,
            "key": key,
            "value": value or "NULL",
            "parentId": parent_id,
            "parentModule": parent_module,
            "dateLastUpdated": None,
        }
        properties.append(regscale_property)
    try:
        batch_response = api.post(
            url=f"{config['domain']}/api/properties/batchCreate",
            json=properties,
        )
    except Exception:
        while retry < 3:
            batch_response = api.post(
                url=f"{config['domain']}/api/properties/batchCreate",
                json=properties,
            )
            if batch_response.ok:
                return True
            retry += 1
        console.print(
            f"[red]Error creating properties for asset #{parent_id} after {retry} attempt(s)."
            f"\n{json.dumps(properties, indent=4)}"
        )
    return batch_response.ok or False


def validate_columns(df: "pd.DataFrame") -> bool:
    """
    Validate the columns in the inventory

    :param pd.DataFrame df: DataFrame to validate
    :return: If the columns are valid
    :rtype: bool
    """
    cols = list(df.columns)
    expected_cols = [
        "UNIQUE ASSET IDENTIFIER",
        "IPv4 or IPv6\nAddress",
        "Virtual",
        "Public",
        "DNS Name or URL",
        "NetBIOS Name",
        MAC_ADDRESS,
        "Authenticated Scan",
        "Baseline Configuration Name",
        OS_NAME,
        "Location",
        "Asset Type",
        HARDWARE_MAKE,
        "In Latest Scan",
        SOFTWARE_VENDOR,
        SOFTWARE_NAME,
        PATCH_LEVEL,
        "Diagram Label",
        "Comments",
        "Serial #/Asset Tag#",
        "VLAN/\nNetwork ID",
        "System Administrator/ Owner",
        "Application Administrator/ Owner",
        "Function",
    ]
    count = 0
    # ensure all expected columns are present
    for col in expected_cols:
        if col not in cols:
            console.print(f"[yellow]Column not found: [red]{col}")
            count += 1
    if count > 0:
        console.print("\n[yellow]Unable to validate [red]%i [yellow]columns" % count)
        console.print("[yellow]exiting..")
        return False
    return True


def upload(
    inventory: str,
    record_id: int,
    module: str,
    sheet_name: str = "Inventory",
) -> None:
    """
    Main function to parse the inventory and load into RegScale
    :param str inventory: path to the inventory .xlsx file
    :param int record_id: RegScale Record ID to update
    :param str module: RegScale Module for the provided ID
    :param str sheet_name: sheet name in the inventory .xlsx file to parse, defaults to "Inventory"
    :rtype: None
    """
    import pandas as pd  # Optimize import performance

    try:
        df: pd.DataFrame = pd.read_excel(inventory, header=1, sheet_name=sheet_name)
    except FileNotFoundError:
        console.print(f"[red]File not found: {inventory}")
        return
    except ValueError:
        console.print("There is an issue with the file: %s, please check the file and try again" % inventory)
        console.print("skipping...")
        return
    valid = validate_columns(df)
    # make all NULL values empty strings
    if not valid:
        return
    df.fillna("", inplace=True)

    # convert into dictionary
    inventory_json = df.to_json(orient="records")
    inventory_list = df.to_dict(orient="records")

    # save locally
    save_to_json("inventory", inventory_json)
    console.print(f"[yellow]{len(inventory_list)} total inventory item(s) saved to inventory.json")

    # process the inventory
    inventory: Dict[int, Dict[str, Asset]] = {}
    existing_assets = Asset.get_all_by_parent(parent_id=record_id, parent_module=module)
    already_inserted: List[Asset] = []
    for inv in track(range(len(inventory_list)), description="Processing inventory..."):
        asset = map_inventory_to_asset(inventory_list[inv], record_id, module)
        if asset not in existing_assets:
            inventory[inv] = {}
            inventory[inv]["asset"] = asset
            inventory[inv]["raw_data"] = inventory_list[inv]
        else:
            already_inserted.append(asset)
    # reindex dict
    reindexed_dict = {new_index: inventory[old_index] for new_index, old_index in enumerate(inventory)}
    # print new objectives
    save_to_json("regscale-inventory", reindexed_dict)

    if not reindexed_dict:
        console.print("[yellow]No new inventory items to load, exiting...")
        return
    console.print(
        f"[yellow]{len(reindexed_dict)} total inventory item(s) ready to load ({len(already_inserted)} "
        f"already exists) Saved to regscale-inventory.json"
    )
    # loop through each asset in the inventory list
    processed = []
    failed = []
    for inv in track(range(len(reindexed_dict)), description="Loading inventory into RegScale..."):
        inv = reindexed_dict[inv]
        try:
            res_data = inv["asset"].create()
            processed.append(res_data)
            # create properties
            if not create_properties(inv["raw_data"], res_data["id"], "assets"):
                console.print(f"[red]Failed to create properties for asset #{res_data['id']}: {inv['asset']['name']}")
        except JSONDecodeError:
            failed.append(inv)
            continue

    if failed:
        save_to_json("failed-inventory", failed)
        console.print(f"[red]{len(failed)} total inventory item(s) failed to load. Saved to failed-inventory.json")
    # print new objectives
    save_to_json("processed-inventory", processed)
    console.print(
        f"[yellow]{len(processed)} total RegScale inventory successfully uploaded. Saved to processed-inventory.json"
    )
