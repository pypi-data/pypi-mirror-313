"""
This module contains the Group model class that represents a group in the RegScale application.
"""

import logging
from typing import Optional, List, Tuple

from pydantic import ConfigDict, Field

from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models import RegScaleModel, User
from regscale.models.regscale_models.user_group import UserGroup

logger = logging.getLogger(__name__)


class Group(RegScaleModel):
    _module_slug = "groups"

    id: Optional[int] = None
    name: Optional[str] = None
    userGroups: Optional[List[UserGroup]] = None
    activated: Optional[bool] = True
    createdById: Optional[str] = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    dateCreated: Optional[str] = Field(default_factory=get_current_datetime)
    lastUpdatedById: Optional[str] = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    isPublic: Optional[bool] = True
    dateLastUpdated: Optional[str] = Field(default_factory=get_current_datetime)
    tenantsId: Optional[int] = 1

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get additional endpoints for the Group model.

        :return: A dictionary of additional endpoints
        :rtype: ConfigDict
        """
        return ConfigDict(
            get_groups="/api/{model_slug}",
            change_group_status="/api/{model_slug}/changeGroupStatus/{id}/{strActivated}",
            find_groups_by_user="/api/{model_slug}/findGroupsByUser/{strUser}",
            filter_groups="/api/{model_slug}/filterGroups/{strName}/{strActivated}/{strSortBy}/{strDirection}/{intPage}/{intPageSize}",
            find_users_by_group="/api/{model_slug}/findUsersByGroup/{intGroupId}",
        )

    @classmethod
    def get_users_in_group(cls, name: str) -> Tuple[List[User], int]:
        """
        Get a list of users in a group.

        :param str name: The name of the group
        :return: A list of users
        :rtype: Tuple[List[User], int]
        """
        group_list_resp = cls._model_api_handler.get(
            endpoint=cls.get_endpoint("get_groups").format(model_slug=cls._module_slug)
        )
        group_id = 0
        if group_list_resp and group_list_resp.ok:
            group_list = group_list_resp.json()
            for group in group_list:
                if group.get("name") == name:
                    group_id = group.get("id")
                    break

        response = cls._model_api_handler.get(
            endpoint=cls.get_endpoint("find_users_by_group").format(model_slug=cls._module_slug, intGroupId=group_id)
        )
        if response and response.ok:
            users = [User(**user) for user in response.json()]
            for user in users:
                # add delegates to users list
                users.extend(user.get_delegates(user.id))
            return users, group_id
        else:
            logger.error(f"Failed to get users in group {name}")
            return [], group_id
