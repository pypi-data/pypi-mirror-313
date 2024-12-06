""" This module contains the Profile model. """

from typing import Optional

from pydantic import ConfigDict, Field

from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models.regscale_models.regscale_model import RegScaleModel


class Profile(RegScaleModel):
    """
    Represents a security profile with various attributes.
    """

    _module_slug = "profiles"

    id: Optional[int] = None
    category: Optional[str] = None
    name: Optional[str]
    createdById: str = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    dateCreated: str = Field(default_factory=get_current_datetime)
    lastUpdatedById: str = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    dateLastUpdated: str = Field(default_factory=get_current_datetime)
    profileOwnerId: Optional[str] = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    tenantsId: Optional[int] = 1
    uuid: Optional[str] = None
    isPublic: Optional[bool] = True
    availability: Optional[str] = None
    confidentiality: Optional[str] = None
    integrity: Optional[str] = None

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get additional endpoints for the Profile model.

        :return: A dictionary of additional endpoints
        :rtype: ConfigDict
        """
        return ConfigDict(
            get_list="/api/{model_slug}/getList",
            get_list_with_controls="/api/{model_slug}/getListWithControls",
            get_count="/api/{model_slug}/getCount",
            graph="/api/{model_slug}/graph",
            apply_profile="/api/{model_slug}/applyProfile/{moduleId}/{moduleName}/{profileId}/{isPublic}",
            filter_profiles="/api/{model_slug}/filterProfiles",
            query_by_custom_field="/api/{model_slug}/queryByCustomField/{strFieldName}/{strValue}",
            find_by_name="/api/{model_slug}/findByName/{strName}/{intID}",
        )
