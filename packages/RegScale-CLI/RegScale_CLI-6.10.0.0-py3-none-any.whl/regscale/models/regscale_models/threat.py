#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale Threat """

from concurrent.futures import ThreadPoolExecutor, as_completed

# standard python imports
from dataclasses import dataclass
from typing import Any, List, Optional
from urllib.parse import urljoin

from requests import Response

from regscale.core.app.api import Api


@dataclass
class Threat:
    """Threat Model"""

    title: str
    threatType: str
    threatOwnerId: str
    dateIdentified: str
    targetType: str
    description: str
    vulnerabilityAnalysis: str
    mitigations: str
    dateCreated: str
    uuid: Optional[str] = None
    id: int = 0
    investigationResults: str = ""
    notes: str = ""
    organization: str = ""
    status: str = "Under Investigation"
    source: str = "Open Source"

    def __getitem__(self, key: Any) -> Any:
        """
        Get attribute from Pipeline

        :param Any key: Key to get value from
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

    @staticmethod
    def xstr(str_eval: Any) -> str:
        """
        Replaces string with None value to ""

        :param Any str_eval: key to replace None value to ""
        :return: Updates provided str field to ""
        :rtype: str
        """
        return "" if str_eval is None else str_eval

    @staticmethod
    def bulk_insert(api: Api, threats: list[dict]) -> List[Response]:
        """
        Bulk insert Threats to the RegScale API

        :param Api api: RegScale API
        :param list[dict] threats: List of Threats to insert
        :return: List of Responses from RegScale API
        :rtype: List[Response]
        """
        app = api.app
        results = []

        # use threadpoolexecutor to speed up inserts
        with ThreadPoolExecutor(max_workers=30) as executor:
            url = app.config["domain"] + "/api/threats"
            futures = [
                executor.submit(
                    api.post,
                    url,
                    json=threat,
                )
                for threat in threats
            ]
            for future in as_completed(futures):
                results.append(future.result())
        return results

    @staticmethod
    def bulk_update(api: Api, threats: list[dict]) -> List[Response]:
        """
        Bulk insert Threats to the RegScale API

        :param Api api: RegScale API
        :param list[dict] threats: List of Threats to update
        :return: List of Responses from RegScale API
        :rtype: List[Response]
        """
        app = api.app
        results = []

        # use threadpoolexecutor to speed up inserts
        with ThreadPoolExecutor(max_workers=30) as executor:
            url = app.config["domain"] + "/api/threats"
            futures = [
                executor.submit(
                    api.post,
                    urljoin(url, str(threat["id"])),
                    json=threat,
                )
                for threat in threats
            ]
            for future in as_completed(futures):
                results.append(future.result())
        return results
