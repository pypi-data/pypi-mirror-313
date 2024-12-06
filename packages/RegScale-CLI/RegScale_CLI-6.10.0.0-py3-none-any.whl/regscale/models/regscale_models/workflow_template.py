"""
This module contains the WorkflowTemplate model.
"""

from typing import Optional, List

from pydantic import ConfigDict, Field

from regscale.models import RegScaleModel
from regscale.models.regscale_models.workflow_template_step import WorkflowTemplateStep


class WorkflowTemplate(RegScaleModel):
    _module_slug = "workflowTemplates"

    id: Optional[int] = None
    name: Optional[str] = None
    status: Optional[str] = None
    createdById: Optional[str] = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    dateCreated: Optional[str] = None
    lastUpdatedById: Optional[str] = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    isPublic: Optional[bool] = None
    dateLastUpdated: Optional[str] = None
    atlasModule: Optional[str] = None
    workflowTemplateSteps: Optional[List[WorkflowTemplateStep]] = None
    tenantsId: int = 1

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get additional endpoints for the WorkflowTemplate model.

        :return: A dictionary of additional endpoints
        :rtype: ConfigDict
        """
        return ConfigDict(
            get_count="/api/{model_slug}/getCount",
            get_by_atlas_module="/api/{model_slug}/getByAtlasModule/{strModule}",
            filter_workflow_templates="/api/{model_slug}/filterWorkflowTemplates/{strSearch}/{strSortBy}/{strDirection}/{intPage}/{intPageSize}",
            create_workflow_template_post="/api/{model_slug}",
            update_workflow_template_put="/api/{model_slug}/{id}",
            get_workflow_template="/api/{model_slug}/{id}",
        )

    @classmethod
    def get_by_atlas_module(cls, module: str) -> List["WorkflowTemplate"]:
        """
        Get all workflow templates by atlas module.

        :param str module: The module of the parent
        :return: A list of workflow templates
        :rtype: List["WorkflowTemplate"]
        """
        response = cls._model_api_handler.get(
            endpoint=cls.get_endpoint("get_by_atlas_module").format(model_slug=cls._module_slug, strModule=module)
        )
        if response and response.ok:
            return [cls(**o) for o in response.json()]
        else:
            cls.log_response_error(response=response)
            return []
