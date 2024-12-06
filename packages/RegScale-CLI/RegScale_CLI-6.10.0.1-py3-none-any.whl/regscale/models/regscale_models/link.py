""" Model for a RegScale Link """

import logging
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional

from pydantic import ConfigDict, Field

from regscale.core.app.utils.app_utils import get_current_datetime
from .regscale_model import RegScaleModel
from requests import JSONDecodeError, Response

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger

logger = logging.getLogger("rich")


class Link(RegScaleModel):
    _module_slug = "links"
    _unique_fields = [
        ["title", "parentID", "parentModule"],
    ]
    _parent_id_field = "parentID"

    id: Optional[int] = 0
    url: str
    title: str
    createdById: Optional[str] = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    dateCreated: Optional[str] = Field(default_factory=get_current_datetime)
    lastUpdatedById: Optional[str] = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    isPublic: bool = True
    parentID: Optional[int] = None
    parentModule: Optional[str] = None
    tenantsId: Optional[int] = None
    dateLastUpdated: Optional[str] = Field(default_factory=get_current_datetime)
    otherAttributes: Optional[str] = None
    externalId: Optional[str] = None

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get additional endpoints for the Links model.

        :return: A dictionary of additional endpoints
        :rtype: ConfigDict
        """
        return ConfigDict(
            get_all_by_part="/api/{model_slug}/getAllByPart/{intParentID}/{strModule}/{strType}/{strPart}",
            get_all_from_list="/api/{model_slug}/getAllFromList",
            batch_create="/api/{model_slug}/batchCreate",
            batch_update="/api/{model_slug}/batchUpdate",
        )

    def __hash__(self) -> hash:
        """
        Enable object to be hashable

        :return: Hashed Link
        :rtype: hash
        """
        return hash(
            (
                self.title,
                self.parentID,
                self.parentModule,
                self.url,
            )
        )

    def __eq__(self, other: "Link") -> bool:
        """
        Determine if two Links are equal

        :param Link other: Link Object to compare to
        :return: True if equal
        :rtype: bool
        """
        return (
            self.title == other.title
            and self.parentID == other.parentID
            and self.parentModule == other.parentModule
            and self.url == other.url
        )

    @staticmethod
    def update_link(app: Application, link: "Link") -> Optional["Link"]:
        """
        Update a Link in RegScale via API

        :param Application app: Application
        :param Link link: Link to update
        :return: Updated Link
        :rtype: Optional[Link]
        """
        api = Api()
        link_id = link.id

        response = api.put(app.config["domain"] + f"/api/links/{link_id}", json=link.dict())
        if response.status_code == 200:
            try:
                link = Link(**response.json())
            except JSONDecodeError:
                link = None
        return link

    @staticmethod
    def bulk_insert(api: Api, links: List["Link"], thread_count: Optional[int] = 10) -> List[Response]:
        """
        Bulk insert Links to the RegScale API

        :param Api api: RegScale API
        :param List[Link] links: List of links to insert
        :param Optional[int] thread_count: Number of threads to use, defaults to 10
        :return: List of Responses from RegScale API
        :rtype: List[Response]
        """
        app = api.app
        results = []

        # use threadpoolexecutor to speed up inserts
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = [
                executor.submit(
                    Link.insert_link,
                    app,
                    link,
                )
                for link in links
            ]
            for future in as_completed(futures):
                results.append(future.result())
        return results

    @staticmethod
    def insert_link(app: Application, link: "Link") -> "Link":
        """
        Insert a Link into RegScale

        :param Application app: Application
        :param Link link: Link to insert
        :return: Inserted Link
        :rtype: Link
        """
        api = Api()
        logger = create_logger()
        response = api.post(app.config["domain"] + "/api/links", json=link.dict())
        if response.status_code == 200:
            try:
                link = Link(**response.json())
            except JSONDecodeError as jex:
                logger.error("Unable to read link:\n%s", jex)
                link = None
        else:
            logger.warning("Unable to insert link: %s", link.title)
        return link

    @staticmethod
    def fetch_links_by_parent(
        app: Application,
        regscale_id: int,
        regscale_module: str,
    ) -> List["Link"]:
        """
        Fetch Links by Parent ID and Module

        :param Application app: Application
        :param int regscale_id: RegScale ID
        :param str regscale_module: RegScale Module
        :return: List of Links
        :rtype: List[Link]
        """
        api = Api()
        body = """
                query {
                    links(take: 50, skip: 0, where: { parentModule: {eq: "parent_module"} parentID: {
                      eq: parent_id
                    }}) {
                    items {
                        id
                        title
                        url
                        parentID
                        parentModule
                        dateCreated
                        createdById
                        lastUpdatedById
                        dateLastUpdated
                        isPublic
                    },
                    pageInfo {
                        hasNextPage
                    }
                    ,totalCount}
                }
                    """.replace(
            "parent_module", regscale_module
        ).replace(
            "parent_id", str(regscale_id)
        )
        existing_regscale_links = api.graph(query=body)["links"]["items"]
        return [Link(**link) for link in existing_regscale_links]


class Links(Link):
    """
    Deprecated Links class
    """

    def __init__(self, *args, **kwargs):
        warnings.warn("The 'Links' class is deprecated, use 'Link' instead", DeprecationWarning)
        super().__init__(*args, **kwargs)
