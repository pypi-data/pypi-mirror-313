"""
This module contains the WorkflowInstanceStep model class that represents a workflow instance step in the RegScale application.
"""

from typing import Optional

from pydantic import ConfigDict, Field

from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models import RegScaleModel


class WorkflowInstanceStep(RegScaleModel):
    _module_slug = "workflowInstanceSteps"

    id: Optional[int] = None
    workflowInstanceId: Optional[int] = None
    name: Optional[str] = None
    comments: Optional[str] = None
    order: Optional[int] = 1
    status: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    actionType: Optional[str] = None
    executionType: Optional[str] = None
    createdById: Optional[str] = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    dateCreated: Optional[str] = Field(default_factory=get_current_datetime)
    lastUpdatedById: Optional[str] = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    isPublic: Optional[bool] = True
    dateLastUpdated: Optional[str] = Field(default_factory=get_current_datetime)
    groupsId: Optional[int] = None
    tenantsId: Optional[int] = 1
    stepType: Optional[str] = None
    assignedToId: Optional[str] = None
    functionalRoleId: Optional[int] = None
    parentId: Optional[int] = None
    parentModule: Optional[str] = None

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get additional endpoints for the WorkflowInstanceStep model.

        :return: A dictionary of additional endpoints
        :rtype: ConfigDict
        """
        return ConfigDict(
            get_by_parent="/api/{model_slug}/getByParent/{intParentID}",
            filter_workflow_instance_steps_by_parent="/api/{model_slug}/filterWorkflowInstanceStepsByParent/{intWorkflowInstanceID}/{strSortBy}/{strDirection}/{intPage}/{intPageSize}",
            update_workflow_instance_step_put="/api/{model_slug}/{id}",
            get_workflow_instance_step="/api/{model_slug}/{id}",
        )

    def find_by_unique(self):
        """
        Find a object by unique query.

        :return: The functional role
        :rtype: FunctionalRole
        """
        for instance in self.get_all_by_parent(parent_id=self.workflowInstanceId, parent_module=""):
            if instance.order == self.order:
                return instance
        return None
