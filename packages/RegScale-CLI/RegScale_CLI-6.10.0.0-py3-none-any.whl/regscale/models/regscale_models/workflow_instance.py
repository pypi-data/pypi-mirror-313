"""
This module contains the WorkflowInstance model.
"""

import logging
from typing import Optional, List

from pydantic import ConfigDict, Field

from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models import RegScaleModel
from regscale.models.regscale_models.workflow_instance_step import WorkflowInstanceStep

logger = logging.getLogger(__name__)


class WorkflowInstance(RegScaleModel):
    _module_slug = "workflowInstances"

    id: Optional[int] = None
    name: Optional[str] = None
    status: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    currentStep: Optional[int] = None
    comments: Optional[str] = None
    createdById: Optional[str] = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    dateCreated: Optional[str] = Field(default_factory=get_current_datetime)
    lastUpdatedById: Optional[str] = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    isPublic: Optional[bool] = True
    dateLastUpdated: Optional[str] = Field(default_factory=get_current_datetime)
    ownerId: Optional[str] = None
    parentId: Optional[int] = None
    atlasModule: Optional[str] = None
    workflowInstanceSteps: Optional[List[WorkflowInstanceStep]] = None
    tenantsId: Optional[int] = 1

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get additional endpoints for the WorkflowInstance model.

        :return: A dictionary of additional endpoints
        :rtype: ConfigDict
        """
        return ConfigDict(
            get_by_parent="/api/{model_slug}/filterWorkflowInstanceByParentId/{intParentID}/{strModule}/id/descending/1/100",
            get_count="/api/{model_slug}/getCount",
            get_open="/api/{model_slug}/getOpen",
            get_by_status="/api/{model_slug}/getByStatus",
            user_open_items_days="/api/{model_slug}/userOpenItemsDays/{strOwner}/{intDays}",
            filter_workflow_instances="/api/{model_slug}/filterWorkflowInstances/{strSearch}/{strStatus}/{strOwner}/{strSortBy}/{strDirection}/{intPage}/{intPageSize}",
            filter_workflow_instances_by_user="/api/{model_slug}/filterWorkflowInstancesByUser/{strUser}/{strSortBy}/{strDirection}/{intPage}/{intPageSize}",
            approve_step_put="/api/{model_slug}/approveStep/{strUserId}",
            submit_put="/api/{model_slug}/submit/{userId}",
            create_from_module_post="/api/{model_slug}/createFromModule/{intTemplateId}/{strUserId}",
            create_custom_workflow_post="/api/{model_slug}/createCustomWorkflow/{strModule}/{intParentId}",
            reject_step_put="/api/{model_slug}/rejectStep/{strUserId}",
            create_from_template_post="/api/{model_slug}/createFromTemplate/{intTemplateId}",
        )

    def find_by_unique(self):
        """
        Find a object by unique query.

        :param str name: The name of the functional role
        :return: The functional role
        :rtype: FunctionalRole
        """
        for instance in self.get_by_parent(parent_id=self.parentId, parent_module=self.atlasModule):
            if instance.name == self.name:
                return instance
        return None

    @classmethod
    def create_from_template(cls, template_id: int) -> Optional[int]:
        """
        Create a workflow instance from a template.

        :param int template_id: The ID of the template
        :return: The created workflow instance id
        :rtype: Optional[int]
        """
        response = cls._api_handler.post(
            endpoint=cls.get_endpoint("create_from_template_post").format(
                model_slug=cls._module_slug, intTemplateId=template_id
            ),
            data=cls.dict(),
        )
        if response and response.ok:
            return int(response.text)
        else:
            logger.error(f"Failed to create workflow instance from template {template_id}")
            return None

    def create_custom_workflow(self, module: str, parent_id: int) -> Optional[int]:
        """
        Create a custom workflow instance.

        :param str module: The module of the parent
        :param int parent_id: The ID of the parent
        :return: The created workflow instance id
        :rtype: Optional[int]
        """
        response = self._model_api_handler.post(
            endpoint=self.get_endpoint("create_custom_workflow_post").format(
                model_slug=self._module_slug, strModule=module, intParentId=parent_id
            ),
            data=self.dict(),
        )
        if response and response.ok:
            return int(response.text)
        else:
            logger.error(f"Failed to create custom workflow instance from module {module}. Error: {response.text}")
            return None

    def approve_step(self, user_id: str) -> bool:
        """
        Approve a step in a workflow instance.

        :param str user_id: The ID of the user
        :return: True if successful
        :rtype: bool
        """
        response = self._model_api_handler.put(
            endpoint=self.get_endpoint("approve_step_put").format(model_slug=self._module_slug, strUserId=user_id),
            data=self.dict(),
        )
        if getattr(response, "ok", False):
            return True
        else:
            logger.error(f"Failed to approve step for {self.name}")
            return False

    def approve_all_steps(self, user_id: str) -> None:
        """
        Approve all steps in a workflow instance.

        :param str user_id: The ID of the user
        :rtype: None
        """
        for step in WorkflowInstanceStep.get_all_by_parent(
            parent_id=self.id,
            parent_module=self.get_module_slug(),
        ):
            if step.order not in [0, 1000]:
                self.currentStep = step.order
                self.comments = "<p>I Approve</p>"
                self.approve_step(user_id=user_id)
