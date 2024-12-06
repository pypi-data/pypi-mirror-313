#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Model for a RegScale Asset """
import logging
import warnings
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from typing import Any, List, Optional, Union, cast
from urllib.parse import urljoin

from pydantic import ConfigDict, Field
from requests import Response
from rich.progress import Progress

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models.regscale_models.regscale_model import RegScaleModel, T
from regscale.models.regscale_models.search import Search

logger = logging.getLogger(__name__)


class AssetStatus(str, Enum):
    """Asset Status Enum"""

    Active = "Active (On Network)"
    Inactive = "Off-Network"
    Decommissioned = "Decommissioned"

    def __str__(self):
        return self.value


class AssetCategory(str, Enum):
    """Asset Category Enum"""

    Hardware = "Hardware"
    Software = "Software"

    def __str__(self):
        return self.value


class AssetType(str, Enum):
    """Asset Type Enum"""

    PhysicalServer = "Physical Server"
    VM = "Virtual Machine (VM)"
    Appliance = "Appliance"
    NetworkRouter = "Network Router"
    NetworkSwitch = "Network Switch"
    Firewall = "Firewall"
    Desktop = "Desktop"
    Laptop = "Laptop"
    Tablet = "Tablet"
    Phone = "Phone"
    Other = "Other"


class Asset(RegScaleModel):
    """Asset Model"""

    _module_slug = "assets"
    _unique_fields = [
        ["name", "otherTrackingNumber"],
        ["fqdn"],  # Try FQDN first as it's most reliable
        ["name", "netBIOS"],  # Then try name + NetBIOS
        ["name", "ipAddress"],  # Then try name + IP
        ["ipAddress", "macAddress"],  # Then IP + MAC
    ]

    _exclude_graphql_fields = ["extra_data", "tenantsId"]

    id: int = 0  # Required
    name: str  # Required
    assetType: Union[AssetType, str]  # Required
    status: Union[AssetStatus, str]  # Required
    assetCategory: Union[AssetCategory, str]  # Required
    otherTrackingNumber: Optional[str] = None
    parentId: int = 0  # Required
    parentModule: str = ""  # Required
    isPublic: bool = True  # Required as Bool
    assetOwnerId: str = Field(default_factory=RegScaleModel._api_handler.get_user_id)  # Required as string
    dateCreated: str = Field(default_factory=get_current_datetime)  # Required as string
    dateLastUpdated: str = Field(default_factory=get_current_datetime)  # Required as string
    ram: Optional[int] = None
    location: Optional[str] = None
    diagramLevel: Optional[str] = None
    cpu: Optional[int] = 0
    description: Optional[str] = None
    diskStorage: Optional[int] = 0
    ipAddress: Optional[str] = None
    macAddress: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    osVersion: Optional[str] = None
    operatingSystem: Optional[str] = None
    uuid: Optional[str] = None
    serialNumber: Optional[str] = None
    createdById: Optional[str] = None
    lastUpdatedById: Optional[str] = None
    endOfLifeDate: Optional[str] = None
    purchaseDate: Optional[str] = None
    tenantsId: Optional[int] = None
    facilityId: Optional[int] = None
    orgId: Optional[int] = None
    cmmcAssetType: Optional[str] = None
    wizId: Optional[str] = None
    wizInfo: Optional[str] = None
    assetTagNumber: Optional[str] = None
    baselineConfiguration: Optional[str] = None
    fqdn: Optional[str] = None
    netBIOS: Optional[str] = None
    softwareName: Optional[str] = None
    softwareVendor: Optional[str] = None
    softwareVersion: Optional[str] = None
    softwareAcronym: Optional[str] = None
    vlanId: Optional[str] = None
    bAuthenticatedScan: Optional[bool] = None
    bPublicFacing: Optional[bool] = None
    bVirtual: Optional[bool] = True
    notes: Optional[str] = None
    patchLevel: Optional[str] = None
    softwareFunction: Optional[str] = None
    systemAdministratorId: Optional[str] = None
    bLatestScan: Optional[bool] = None
    managementType: Optional[str] = None
    qualysId: Optional[str] = None
    sicuraId: Optional[Union[str, int]] = None
    tenableId: Optional[str] = None
    firmwareVersion: Optional[str] = None
    purpose: Optional[str] = None
    awsIdentifier: Optional[str] = None
    azureIdentifier: Optional[str] = None
    googleIdentifier: Optional[str] = None
    otherCloudIdentifier: Optional[str] = None
    iPv6Address: Optional[str] = None
    scanningTool: Optional[str] = None
    uri: Optional[str] = None
    bScanDatabase: Optional[bool] = None
    bScanInfrastructure: Optional[bool] = None
    bScanWeb: Optional[bool] = None
    cpe: Optional[str] = None
    dadmsId: Optional[str] = None
    approvalStatus: Optional[str] = None
    processStatus: Optional[str] = None
    networkApproval: Optional[str] = None
    lastDateAllowed: Optional[str] = None
    bFamAccepted: Optional[bool] = None
    bExternallyAuthorized: Optional[bool] = None

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get additional endpoints for the Assets model.

        :return: A dictionary of additional endpoints
        :rtype: ConfigDict
        """
        return ConfigDict(  # type: ignore
            get_by_parent="/api/{model_slug}/getAllByParent/{intParentID}/{strModule}",
            get_all_by_search="/api/{model_slug}/getAllBySearch",
            drilldown="/api/{model_slug}/drilldown/{strMonth}/{strCategory}",
            get_count="/api/{model_slug}/getCount",
            graph="/api/{model_slug}/graph",
            graph_by_date="/api/{model_slug}/graphByDate/{strGroupBy}/{year}",
            filter_dashboard="/api/{model_slug}/filterDashboard/{dtStart}/{dtEnd}",
            dashboard="/api/{model_slug}/dashboard/{strGroupBy}",
            dashboard_by_parent="/api/{model_slug}/dashboardByParent/{strGroupBy}/{intId}/{strModule}",
            schedule="/api/{model_slug}/schedule/{year}/{dvar}",
            report="/api/{model_slug}/report/{strReport}",
            filter_assets="/api/{model_slug}/filterAssets",
            query_by_custom_field="/api/{model_slug}/queryByCustomField/{strFieldName}/{strValue}",
            batch_create="/api/{model_slug}/batchCreate",
            batch_update="/api/{model_slug}/batchUpdate",
        )

    @classmethod
    def get_map(cls, plan_id: int, key_field: str = "otherTrackingNumber") -> dict[str, "Asset"]:
        """
        Get the asset map for the asset and cache it in Redis.

        :param int plan_id: Security Plan ID
        :param str key_field: Key field to use, defaults to "identifier"
        :return: Asset Map
        :rtype: dict[str, "Asset"]
        """
        search_data = f"""query {{
            assetMappings(skip: 0, take: 50, where: {{component: {{securityPlansId: {{eq: {plan_id}}} }} }}) {{
                items {{
                id
                asset {{
                    {cls.build_graphql_fields()}
                }}
                }}
                totalCount
                pageInfo {{
                hasNextPage
                }}
            }}
        }}"""
        response = cls._api_handler.graph(query=search_data)
        assets = cast(List["Asset"], cls._handle_graph_response(response, child="asset"))
        return_assets = {}
        for asset in assets:
            identifier = getattr(asset, key_field, None)
            if identifier:
                return_assets[identifier] = asset

        return return_assets

    # Legacy code

    @classmethod
    def find_os(cls, os_string: Optional[str] = None) -> str:
        """
        Determine the RegScale OS from a string.

        :param Optional[str] os_string: String containing OS information or description, defaults to None
        :return: RegScale compatible OS string
        :rtype: str
        """
        if not os_string:
            return "Other"
        if "windows" in os_string.lower():
            return "Windows Server"
        elif any(sub_string in os_string.lower() for sub_string in ["linux", "ubuntu", "debian", "redhat", "suse"]):
            return "Linux"
        elif "mac" in os_string.lower():
            return "Mac OSX"
        else:
            return "Other"

    # 'uniqueness': 'ip, macaddress'
    # Enable object to be hashable
    def __hash__(self) -> hash:
        """
        Enable object to be hashable

        :return: Hashed TenableAsset
        :rtype: hash
        """
        return hash(
            (
                self.name,
                self.ipAddress,
                self.macAddress.lower() if self.macAddress else None,
                self.assetCategory,
                self.assetType,
                self.fqdn,
                self.parentId,
                self.parentModule,
                self.description,
                self.notes,
            )
        )

    def __getitem__(self, key: Any) -> Any:
        """
        Get attribute from Pipeline

        :param Any key: Key to get value of
        :return: value of provided key
        :rtype: Any
        """
        return getattr(self, key)

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set attribute in Pipeline with provided key

        :param Any key: Key to change to provided value
        :param Any value: New value for provided Key
        :rtype: None
        """
        return setattr(self, key, value)

    def __eq__(self, other: "Asset") -> bool:
        """
        Update items in Asset class

        :param Asset other: Asset object to compare to
        :return: Whether the two assets are equal
        :rtype: bool
        """
        return (
            self.name == other.name
            and self.ipAddress == other.ipAddress
            and self.macAddress == other.macAddress
            and self.wizId == other.wizId
            and self.description == other.description
            and self.notes == other.notes
            and self.status == other.status
            and self.parentId == other.parentId
            and self.otherTrackingNumber == other.otherTrackingNumber
            and self.parentModule == other.parentModule
        )

    @classmethod
    def get_all_by_search(cls, search: Search) -> List[T]:
        """
        Get all assets by search

        :param Search search: Search object
        :return: List of Assets
        :rtype: List[T]
        """
        return cls.get_all_by_parent(search=search, parent_module=search.module, parent_id=search.parentID)

    @staticmethod
    def insert_asset(
        app: Application,
        obj: Any,
        retry_count: int = 3,
    ) -> Response:
        """
        DEPRECATED: This method is deprecated and will be removed in a future version.
        Use create method to create assets.

        :param Application app: Application Instance
        :param Any obj: Asset Object
        :param int retry_count: Number of times to retry if it fails, defaults to 3
        :return: Response from RegScale after inserting the provided asset object
        :rtype: Response
        """
        import warnings

        warnings.warn(
            "insert_asset is deprecated and will be removed in a future version. Use create method instead.",
            DeprecationWarning,
        )
        url = urljoin(app.config["domain"], "/api/assets")
        if isinstance(obj, Asset):
            obj = obj.dict()
        api = Api()
        res = api.post(url=url, json=obj)
        if not res.ok:
            if res.status_code == 500:
                app.logger.error("%i: %s\nError creating asset: %s", res.status_code, res.text, obj)
            # as long as the status code is not 500, retry
            while res.status_code != 500 and retry_count >= 0:
                app.logger.warning("Retrying to create asset, attempts remaining: %i", retry_count)
                res = api.post(url=url, json=obj)
                retry_count -= 1
                if res.ok:
                    app.logger.info("[green]Successfully created asset: %s", res.json()["id"])
                    break
            if retry_count < 0:
                app.logger.error(
                    "%i: %s\n[red]Failed to create asset: %s",
                    res.status_code,
                    res.reason,
                    obj,
                )
        return res

    @staticmethod
    def update_asset(
        app: Application,
        obj: Any,
    ) -> Response:
        """
        DEPRECATED: This method is deprecated and will be removed in a future version.
        Use save method to update assets.

        :param Application app: Application Instance
        :param Any obj: Asset Object
        :return: Response from RegScale after inserting the provided asset object
        :rtype: Response
        """
        warnings.warn(
            "update_asset is deprecated and will be removed in a future version. Use save method instead.",
            DeprecationWarning,
        )
        url = urljoin(app.config["domain"], f"/api/assets/{obj['id']}")
        if isinstance(obj, Asset):
            obj = obj.dict()
        api = Api()
        res = api.put(url=url, json=obj)
        if res.status_code != 200:
            app.logger.error("Error updating asset: %s", obj)
        return res

    @staticmethod
    def bulk_insert(
        assets: List["Asset"],
        max_workers: int = 30,
        batch_size: int = 100,
        batch: bool = False,
    ) -> List[Response]:
        """
        Bulk insert assets using the RegScale API and ThreadPoolExecutor

        :param List[Asset] assets: Asset List
        :param int max_workers: Max Workers, defaults to 30
        :param int batch_size: Number of assets to insert per batch, defaults to 100
        :param bool batch: Insert assets in batches, defaults to False
        :return: List of Responses from RegScale
        :rtype: List[Response]
        """
        warnings.warn(
            "bulk_insert is deprecated and will be removed in a future version. Use batch_create instead.",
            DeprecationWarning,
        )
        api = Api()
        url = urljoin(api.config["domain"], "/api/assets/batchcreate")
        results = []
        if batch:
            # Chunk list into batches
            batches = [assets[i : i + batch_size] for i in range(0, len(assets), batch_size)]

            with Progress() as progress:
                total_task = progress.add_task("[red]Creating Total Assets", total=len(assets))
                for my_batch in batches:
                    res = api.post(url=url, json=[asset.dict() for asset in my_batch])
                    if not res.ok:
                        logger.error(
                            "%i: %s\nError creating batch of assets: %s",
                            res.status_code,
                            res.text,
                            my_batch,
                        )
                    results.append(res)
                    progress.update(total_task, advance=len(my_batch))

            return results
        # Deprecated in favor of batch
        else:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                workers = [executor.submit(asset.create) for asset in assets]
            return [worker.result() for worker in workers] or []

    @staticmethod
    def bulk_update(
        assets: List["Asset"],
        max_workers: int = 30,
        batch_size: int = 100,
        batch: bool = False,
    ) -> List[Response]:
        """Bulk insert assets using the RegScale API and ThreadPoolExecutor

        :param List[Asset] assets: Asset List
        :param int max_workers: Max Workers, defaults to 30
        :param int batch_size: Number of assets to insert per batch, defaults to 100
        :param bool batch: Insert assets in batches, defaults to False
        :return: List of Responses from RegScale
        :rtype: List[Response]
        """
        warnings.warn(
            "bulk_update is deprecated and will be removed in a future version. Use batch_update instead.",
            DeprecationWarning,
        )
        api = Api()
        url = urljoin(api.config["domain"], "/api/assets/batchupdate")
        results = []
        if batch:
            # Chunk list into batches
            batches = [assets[i : i + batch_size] for i in range(0, len(assets), batch_size)]
            with Progress() as progress:
                total_task = progress.add_task("[red]Updating Total Assets", total=len(assets))
                for my_batch in batches:
                    res = api.put(url=url, json=[asset.dict() for asset in my_batch])
                    if not res.ok:
                        logger.error(
                            "%i: %s\nError batch updating assets: %s",
                            res.status_code,
                            res.text,
                            my_batch,
                        )
                    results.append(res)
                    progress.update(total_task, advance=len(my_batch))
            return results
        else:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                workers = [executor.submit(asset.save) for asset in assets]
            return [worker.result() for worker in workers] or []

    @classmethod
    def find_assets_by_parent(
        cls,
        app: Application,  # noqa: F841
        parent_id: int,
        parent_module: str,
    ) -> List["Asset"]:
        """
        DEPRECATED: This method is deprecated and will be removed in a future version.
        Use alternative methods to fetch assets.
        Find all assets by parent id and parent module

        :param Application app: Application Instance
        :param int parent_id: Parent Id
        :param str parent_module: Parent Module
        :return: List of Assets
        :rtype: List[Asset]
        """
        warnings.warn(
            "find_asset_by_parent is deprecated and will be removed in a future version. "
            "Use get_all_by_parent instead.",
            DeprecationWarning,
        )
        return cls.get_all_by_parent(
            parent_id=parent_id,
            parent_module=parent_module,
        )

    @classmethod
    def fetch_asset_by_id(cls, asset_id: int) -> Optional["Asset"]:
        """
        DEPRECATED: This method is deprecated and will be removed in a future version.
        Use alternative methods to fetch assets.
        Find all assets by parent id and parent module

        :param int asset_id: RegScale Asset ID number
        :return: Asset, if found
        :rtype: Optional[Asset]
        """
        warnings.warn(
            "fetch_asset_by_id is deprecated and will be removed in a future version. Use get_object instead.",
            DeprecationWarning,
        )
        return cls.get_object(object_id=asset_id)

    @classmethod
    def fetch_assets_by_module(
        cls,
        app: Application,  # noqa: F841
        parent_id: int,
        parent_module: str,
    ) -> List["Asset"]:
        """
        DEPRECATED: This method is deprecated and will be removed in a future version.
        Use alternative methods to fetch assets.
        Find all assets by parent id and parent module
        :param Application app: Application Instance
        :param int parent_id: Parent Id
        :param str parent_module: Parent Module
        :return: List of Assets
        :rtype: List[Asset]
        """
        warnings.warn(
            "find_asset_by_parent is deprecated and will be removed in a future version. "
            "Use get_all_by_parent instead.",
            DeprecationWarning,
        )
        return cls.get_all_by_parent(
            parent_id=parent_id,
            parent_module=parent_module,
        )

    @classmethod
    def get_sort_position_dict(cls) -> dict:
        """
        Overrides the base method.

        :return: dict The sort position in the list of properties
        :rtype: dict
        """
        return {
            "id": 1,
            "name": 2,
            "assetType": 3,
            "status": 4,
            "assetCategory": 5,
            "parentId": 6,
            "parentModule": 7,
            "isPublic": -1,
            "ram": 8,
            "assetOwnerId": 9,
            "dateCreated": -1,
            "dateLastUpdated": -1,
            "location": 10,
            "diagramLevel": 11,
            "cpu": 12,
            "description": 13,
            "diskStorage": 14,
            "ipAddress": 15,
            "macAddress": 16,
            "manufacturer": 17,
            "model": 18,
            "osVersion": 19,
            "operatingSystem": 20,
            "otherTrackingNumber": 21,
            "uuid": -1,
            "serialNumber": 22,
            "createdById": -1,
            "lastUpdatedById": -1,
            "endOfLifeDate": 23,
            "purchaseDate": 24,
            "tenantsId": 25,
            "facilityId": 26,
            "orgId": 27,
            "cmmcAssetType": 28,
            "wizId": 29,
            "wizInfo": 30,
            "assetTagNumber": 31,
            "baselineConfiguration": 32,
            "fqdn": 33,
            "netBIOS": 34,
            "softwareName": 35,
            "softwareVendor": 36,
            "softwareVersion": 37,
            "softwareAcronym": 38,
            "vlanId": 39,
            "bAuthenticatedScan": 40,
            "bPublicFacing": 41,
            "bVirtual": 42,
            "notes": 43,
            "patchLevel": 44,
            "softwareFunction": 45,
            "systemAdministratorId": 46,
            "bLatestScan": 47,
            "managementType": 48,
            "qualysId": 49,
            "sicuraId": 50,
            "tenableId": 51,
            "firmwareVersion": 52,
            "purpose": 53,
            "awsIdentifier": 54,
            "azureIdentifier": 55,
            "googleIdentifier": 56,
            "otherCloudIdentifier": 57,
            "ipv6Address": 58,
            "scanningTool": 59,
            "uri": 60,
            "bScanDatabase": 61,
            "bScanInfrastructure": 62,
            "bScanWeb": 63,
            "cpe": 64,
            "dadmsId": 65,
            "approvalStatus": 66,
            "networkApproval": 67,
            "lastDateAllowed": 68,
            "bFamAccepted": 69,
            "bExternallyAuthorized": 70,
        }

    @classmethod
    def get_enum_values(cls, field_name: str) -> list:
        """
        Overrides the base method.

        :param str field_name: The property name to provide enum values for
        :return: list of strings
        :rtype: list
        """
        boolean_fields = ["bAuthenticatedScan", "bPublicFacing", "bVirtual"]
        optional_bools = [
            "bLatestScan",
            "bScanDatabase",
            "bScanInfrastructure",
            "bScanWeb",
            "bFamAccepted",
            "bExternallyAuthorized",
        ]
        if field_name == "assetType":
            return [
                "Physical Server",
                "Virtual Machine (VM)",
                "Appliance",
                "Network Router",
                "Network Switch",
                "Firewall",
                "Desktop",
                "Laptop",
                "Tablet",
                "Phone",
                "Other",
            ]
        if field_name == "status":
            return ["Active (On Network)", "Off-Network", "Decommissioned"]
        if field_name == "assetCategory":
            return ["Hardware", "Software"]
        if field_name in boolean_fields:
            return ["TRUE", "FALSE"]
        if field_name in optional_bools:
            return ["", "TRUE", "FALSE"]
        return []

    @classmethod
    def get_lookup_field(cls, field_name: str) -> str:
        """
        Overrides the base method.

        :param str field_name: The property name to provide enum values for
        :return: str the field name to look up
        :rtype: str
        """
        lookup_fields = {
            "assetOwnerId": "user",
            "tenantsId": "",
            "facilityId": "facilities",
            "orgId": "organizations",
            "wizId": "",
            "vlanId": "",
            "systemAdministratorId": "",
            "qualysId": "",
            "sicuraId": "",
            "tenableId": "",
            "dadmsId": "",
        }
        if field_name in lookup_fields.keys():
            return lookup_fields[field_name]
        return ""

    @classmethod
    def is_date_field(cls, field_name: str) -> bool:
        """
        Overrides the base method.

        :param str field_name: The property name to provide enum values for
        :return: bool if the field should be formatted as a date
        :rtype: bool
        """
        return field_name in ["endOfLifeDate", "purchaseDate", "lastDateAllowed"]
