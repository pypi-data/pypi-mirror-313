""" SBOM model class """

from typing import Optional

from pydantic import ConfigDict, Field

from regscale.core.app.utils.app_utils import get_current_datetime
from .regscale_model import RegScaleModel


class Sbom(RegScaleModel):
    """SBOM model class"""

    _parent_id_field = "parentId"
    _unique_fields = [
        ["parentId", "parentModule", "name", "tool"],
    ]
    _module_slug = "sbom"
    id: Optional[int] = None
    uuid: Optional[str] = None
    name: Optional[str] = None
    sbomStandard: Optional[str] = None
    tool: Optional[str] = None
    standardVersion: Optional[str] = None
    results: Optional[str] = None
    parentId: int = 0
    parentModule: Optional[str] = None
    tenantsId: int = 1
    createdById: str = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    dateCreated: str = Field(default_factory=get_current_datetime)
    lastUpdatedById: str = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    isPublic: bool = True
    dateLastUpdated: str = Field(default_factory=get_current_datetime)

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get additional endpoints for the SBOM model.

        :return: A dictionary of additional endpoints
        :rtype: ConfigDict
        """
        return ConfigDict(
            get_count="/api/sbom/getCount",
            filter_sboms="/api/sbom/filterSBOMs/{intID}/{strModule}/{intPage}/{intPageSize}",
            find_by_guid="/api/sbom/findByGUID/{strGUID}",
            batch_create="/api/{model_slug}/batchCreate",
            batch_update="/api/{model_slug}/batchUpdate",
        )
