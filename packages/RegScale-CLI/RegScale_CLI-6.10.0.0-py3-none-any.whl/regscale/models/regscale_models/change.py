"""
This module contains the Change model for RegScale.
"""

import logging
from enum import Enum
from typing import Optional

from pydantic import ConfigDict, Field

from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models.regscale_models.regscale_model import RegScaleModel

logger = logging.getLogger(__name__)


class ChangeType(str, Enum):
    """
    Enum for the ChangeType field in the Change model.
    """

    emergency = "Emergency"
    normal = "Normal"
    standard = "Standard"


class ChangePriority(str, Enum):
    """
    Enum for the ChangePriority field in the Change model.
    """

    critical = "Critical"
    low = "Low"
    moderate = "Moderate"
    high = "High"
    security = "Security"


class ChangeStatus(str, Enum):
    """
    Enum for the ChangeStatus field in the Change model.
    """

    draft = "Draft"
    pending_approval = "Pending Approval"
    approved = "Approved"
    rejected = "Rejected"
    canceled = "Canceled"


class ChangeOutageRequired(str, Enum):
    """
    Enum for the ChangeOutageRequired field in the Change model.
    """

    yes = "Yes"
    no = "No"


class Change(RegScaleModel):
    """
    A class to represent the Change model in RegScale.
    """

    _module_slug = "changes"
    _parent_id_field = "parentId"

    id: Optional[int] = 0
    isPublic: bool = True
    uuid: Optional[str] = None
    title: str
    changeReason: str
    description: Optional[str] = None
    changeOwnerId: str = Field(default_factory=RegScaleModel._api_handler.get_config_user_id)
    dateRequested: str = Field(default_factory=get_current_datetime)
    startChangeWindow: Optional[str] = None
    endChangeWindow: Optional[str] = None
    outageRequired: str = ChangeOutageRequired.no.value
    outageSummary: Optional[str] = None
    status: str = ChangeStatus.draft.value
    dateChangeApproved: Optional[str] = None
    dateWorkCompleted: Optional[str] = None
    changeType: str = ChangeType.standard.value
    priority: str = ChangePriority.moderate.value
    securityImpactAssessment: Optional[str] = None
    changePlan: Optional[str] = None
    riskAssessment: Optional[str] = None
    rollbackPlan: Optional[str] = None
    communicationsPlan: Optional[str] = None
    notes: Optional[str] = None
    leadTesterId: Optional[str] = None
    testPlan: Optional[str] = None
    testResults: Optional[str] = None
    dateTested: Optional[str] = None
    facilityId: Optional[int] = None
    orgId: Optional[int] = None
    parentId: Optional[int] = None
    parentModule: Optional[str] = None

    # now create the _get_additional_endpoints method from this list of endpoints
    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get additional endpoints for the Changes model.

        :return: A dictionary of additional endpoints
        :rtype: ConfigDict
        """
        return ConfigDict(
            get_count="/api/changes/getCount",
            schedule="/api/changes/schedule/{year}/{strDateField}",
            report="/api/changes/report/{strReport}",
            filter_changes="/api/changes/filterChanges",
            query_by_custom_field="/api/changes/queryByCustomField/{strFieldName}/{strValue}",
        )
