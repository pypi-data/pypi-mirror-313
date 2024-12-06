"""
UserGroup model for the RegScale API.
"""

from typing import Optional

from pydantic import ConfigDict, Field

from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models import RegScaleModel


class UserGroup(RegScaleModel):
    _module_slug = "userGroups"

    id: Optional[int] = None
    groupsId: int
    userId: str
    isPublic: Optional[bool] = True
    tenantsId: Optional[int] = 1
    createdById: Optional[str] = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    dateCreated: Optional[str] = Field(default_factory=get_current_datetime)
    lastUpdatedById: Optional[str] = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    dateLastUpdated: Optional[str] = Field(default_factory=get_current_datetime)

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get additional endpoints for the UserGroup model.

        :return: A dictionary of additional endpoints
        :rtype: ConfigDict
        """
        return ConfigDict(
            filter_user_groups="/api/{model_slug}/filterUserGroups/{intGroupId}/{intPage}/{intPageSize}",
        )
