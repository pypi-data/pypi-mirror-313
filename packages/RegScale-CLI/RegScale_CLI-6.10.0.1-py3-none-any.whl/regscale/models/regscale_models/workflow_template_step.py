"""
This module contains the WorkflowTemplateStep model.
"""

from typing import Optional

from pydantic import ConfigDict, Field

from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models import RegScaleModel


class WorkflowTemplateStep(RegScaleModel):
    _module_slug = "workflowTemplateSteps"

    id: Optional[int] = None
    workflowTemplateId: Optional[int] = None
    name: Optional[str] = None
    order: Optional[int] = None
    actionType: Optional[str] = None
    executionType: Optional[str] = None
    createdById: Optional[str] = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    dateCreated: Optional[str] = Field(default_factory=get_current_datetime)
    lastUpdatedById: Optional[str] = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    isPublic: bool = True
    dateLastUpdated: Optional[str] = Field(default_factory=get_current_datetime)
    groupsId: Optional[int] = None
    tenantsId: int = 1
    assignedToId: Optional[str] = None
    functionalRoleId: Optional[int] = None
    stepType: Optional[str] = None

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get additional endpoints for the WorkflowTemplateStep model.

        :return: A dictionary of additional endpoints
        :rtype: ConfigDict
        """
        return ConfigDict(
            get_by_parent="/api/{model_slug}/getByParent/{intParentID}",
            filter_workflow_template_steps_by_parent="/api/{model_slug}/filterWorkflowTemplateStepsByParent/{intWorkflowTemplateID}/{strSortBy}/{strDirection}/{intPage}/{intPageSize}",
            create_workflow_template_step_post="/api/{model_slug}",
            update_workflow_template_step_put="/api/{model_slug}/{id}",
            remove_step_put="/api/{model_slug}/removeStep",
            reorder_post="/api/{model_slug}/reorder",
            get_workflow_template_step="/api/{model_slug}/{id}",
        )
