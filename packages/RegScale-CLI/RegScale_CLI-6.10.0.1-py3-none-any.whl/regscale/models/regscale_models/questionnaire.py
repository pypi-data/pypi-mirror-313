"""
This module contains the Questionnaires model in RegScale.
"""

import logging
from typing import Optional, List, Dict

from pydantic import ConfigDict

from regscale.models.regscale_models.regscale_model import RegScaleModel

logger = logging.getLogger(__name__)


class Questionnaires(RegScaleModel):
    """
    A class to represent the Questionnaires model in RegScale.
    """

    _module_slug = "questionnaires"

    id: Optional[int] = 0
    uuid: Optional[str] = None
    title: str
    ownerId: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    createdById: Optional[str] = None
    dateCreated: Optional[str] = None
    lastUpdatedById: Optional[str] = None
    dateLastUpdated: Optional[str] = None
    tenantsId: Optional[int] = 1
    active: bool = True
    isPublic: bool = True
    sections: Optional[List[int]] = [0]  # Adjust the type if it's not a string
    rules: Optional[str] = None  # Adjust the type if it's not a string
    loginRequired: Optional[bool] = True
    allowPublicUrl: Optional[bool] = True
    enableScoring: Optional[bool] = False
    questionnaireIds: Optional[List[int]] = None
    parentQuestionnaireId: Optional[int] = None

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get endpoints for the Questionnaire model.

        :return: A dictionary of endpoints
        :rtype: ConfigDict
        """
        return ConfigDict(
            get_count="/api/{model_slug}/getCount",
            graph_post="/api/{model_slug}/graph",
            filter_post="/api/{model_slug}/filterQuestionnaires",
            create_with_data_post="/api/{model_slug}/createWithData",
            insert="/api/{model_slug}/create",
            create_instances_from_questionnaires_post="/api/{model_slug}/createInstancesFromQuestionnaires",
            upload_post="/api/{model_slug}/upload",
            upload_bulk_email_assignment_post="/api/{model_slug}/uploadBulkEmailAssignment/{questionnaireId}",
            get_updatable_instances_get="/api/{model_slug}/getUpdatableInstances/{questionnaireId}",
            update_assigned_instances_put="/api/{model_slug}/updateAssignedInstances",
            export_get="/api/{model_slug}/exportQuestionnaire/{questionnaireId}",
            export_example_get="/api/{model_slug}/exportQuestionnaireExample",
            export_responses_post="/api/{model_slug}/exportQuestionnaireResponses",
        )

    @classmethod
    def create_instances_from_questionnaires(cls, payload: Dict) -> Optional[Dict]:
        """
        Creates instances from questionnaires.

        :param Dict payload: The data to be sent in the request body
        :return: The response from the API or None
        :rtype: Optional[Dict]
        """
        endpoint = cls.get_endpoint("create_instances_from_questionnaires_post").format(model_slug=cls._module_slug)
        headers = {
            "Authorization": cls._api_handler.config.get("token"),
            "accept": "application/json",
            "Content-Type": "application/json",
            "Origin": cls._api_handler.domain,
        }  # origin is required for this to work properly
        response = cls._api_handler.post(endpoint, data=payload, headers=headers)
        if not response or response.status_code in [204, 404]:
            return None
        if response and response.ok:
            return response.json()
        else:
            logger.info(f"Failed to create instances from questionnaires {response.status_code} - {response.text}")
        return None
