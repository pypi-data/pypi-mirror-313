#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Model for Risk in the application """
import logging
from json import JSONDecodeError
from typing import Optional

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.models.regscale_models.regscale_model import RegScaleModel


logger = logging.getLogger("rich")


class Risk(RegScaleModel):
    """Represents a risk in the application"""

    _module_slug = "risks"

    uuid: Optional[str] = None
    dateIdentified: Optional[str] = None
    riskStatement: Optional[str] = None
    probability: Optional[str] = None
    probabilityReason: Optional[str] = None
    consequence: Optional[str] = None
    consequenceReason: Optional[str] = None
    trigger: Optional[str] = None
    mitigation: Optional[str] = None
    mitigationEffectiveness: Optional[str] = None
    residualProbability: Optional[str] = None
    residualConsequence: Optional[str] = None
    residualRisk: Optional[str] = None
    riskStrategy: Optional[str] = None
    businessRisk: Optional[str] = None
    operationalRisk: Optional[str] = None
    safetyRisk: Optional[str] = None
    securityRisk: Optional[str] = None
    qualityRisk: Optional[str] = None
    environmentalRisk: Optional[str] = None
    reputationRisk: Optional[str] = None
    complianceRisk: Optional[str] = None
    operationalRequirements: Optional[str] = None
    riskSource: Optional[str] = None
    parentId: Optional[int] = None
    parentModule: Optional[str] = None
    status: Optional[str] = None
    dateClosed: Optional[str] = None
    facilityId: Optional[int] = None
    orgId: Optional[int] = None
    comments: Optional[str] = None
    riskTier: Optional[str] = None
    title: Optional[str] = None
    recommendations: Optional[str] = None
    impactDescription: Optional[str] = None
    inherentRiskScore: Optional[int] = None
    residualRiskScore: Optional[int] = None
    targetRiskScore: Optional[int] = None
    difference: Optional[int] = None
    futureCosts: Optional[int] = None
    costToMitigate: Optional[int] = None
    controlId: Optional[int] = None
    assessmentId: Optional[int] = None
    requirementId: Optional[int] = None
    securityPlanId: Optional[int] = None
    projectId: Optional[int] = None
    supplyChainId: Optional[int] = None
    policyId: Optional[int] = None
    componentId: Optional[int] = None
    incidentId: Optional[int] = None
    riskAssessmentFrequency: Optional[str] = None
    dateLastAssessed: Optional[str] = None
    nextAssessmentDueDate: Optional[str] = None
    riskOwnerId: Optional[str] = None
    isPublic: bool = True

    @staticmethod
    def fetch_all_risks(app: Application) -> list["Risk"]:
        """
        Fetches all risks from RegScale

        :param Application app: Application object
        :return: List of Risks from RegScale
        :rtype: list[Risk]
        """
        api = Api()
        body = """
            query {
              risks(take: 50, skip: 0) {
                items {
                  assessmentId
                  id
                  mitigation
                  mitigationEffectiveness
                  residualProbability
                  residualConsequence
                  residualRisk
                  riskStrategy
                  facilityId
                  orgId
                  isPublic
                  businessRisk
                  operationalRisk
                  safetyRisk
                  securityRisk
                  qualityRisk
                  environmentalRisk
                  reputationRisk
                  complianceRisk
                  riskTier
                  title
                  uuid
                  operationalRequirements
                  riskSource
                  parentId
                  parentModule
                  status
                  dateClosed
                  comments
                  recommendations
                  impactDescription
                  inherentRiskScore
                  dateIdentified
                  residualRiskScore
                  targetRiskScore
                  difference
                  futureCosts
                  costToMitigate
                  controlId
                  assessmentId
                  requirementId
                  riskStatement
                  securityPlanId
                  projectId
                  supplyChainId
                  policyId
                  componentId
                  probability
                  incidentId
                  riskAssessmentFrequency
                  dateLastAssessed
                  nextAssessmentDueDate
                  createdById
                  dateCreated
                  lastUpdatedById
                  probabilityReason
                  dateLastUpdated
                  riskOwnerId
                  consequence
                  consequenceReason
                  trigger
                }
                pageInfo {
                  hasNextPage
                }
                totalCount
              }
            }
        """
        try:
            logger.info("Retrieving all risks in RegScale...")
            existing_risks = api.graph(query=body)["risks"]["items"]
            logger.info("%i risk(s) retrieved from RegScale.", len(existing_risks))
        except JSONDecodeError:
            existing_risks = []
        return [Risk(**risk) for risk in existing_risks]

    @classmethod
    def get_sort_position_dict(cls) -> dict:
        """
        Overrides the base method.

        :return: dict The sort position in the list of properties
        :rtype: dict
        """
        return {
            "id": 1,
            "uuid": -1,
            "dateIdentified": 2,
            "riskStatement": 3,
            "probability": 4,
            "probabilityReason": 5,
            "consequence": 6,
            "consequenceReason": 7,
            "trigger": 8,
            "mitigation": 9,
            "mitigationEffectiveness": 10,
            "residualProbability": 11,
            "residualConsequence": 12,
            "residualRisk": 13,
            "riskStrategy": 14,
            "businessRisk": 15,
            "operationalRisk": 16,
            "safetyRisk": 17,
            "securityRisk": 18,
            "qualityRisk": 19,
            "environmentalRisk": 20,
            "reputationRisk": 21,
            "complianceRisk": 22,
            "operationalRequirements": 23,
            "riskSource": 24,
            "parentId": -1,
            "parentModule": -1,
            "status": 25,
            "dateClosed": 26,
            "facilityId": 27,
            "orgId": 28,
            "comments": 29,
            "riskTier": 30,
            "title": 31,
            "recommendations": 32,
            "impactDescription": 33,
            "inherentRiskScore": 34,
            "residualRiskScore": 35,
            "targetRiskScore": 36,
            "difference": 37,
            "futureCosts": 38,
            "costToMitigate": 39,
            "controlId": 40,
            "assessmentId": 41,
            "requirementId": 42,
            "securityPlanId": 43,
            "projectId": 44,
            "supplyChainId": 45,
            "policyId": 46,
            "componentId": 47,
            "incidentId": 48,
            "riskAssessmentFrequency": 49,
            "dateLastAssessed": 50,
            "nextAssessmentDueDate": 51,
            "riskOwnerId": 52,
            "isPublic": -1,
        }

    # pylint: disable=W0613
    @classmethod
    def get_enum_values(cls, field_name: str) -> list:
        """
        Overrides the base method.

        :param str field_name: The property name to provide enum values for
        :return: list of strings
        :rtype: list
        """
        return []

    @classmethod
    def get_lookup_field(cls, field_name: str) -> str:
        """
        Overrides the base method.

        :param str field_name: The property name to provide enum values for
        :return: str the field name to look up
        :rtype: str
        """
        lookup_fields = {
            "facilityId": "facilities",
            "orgId": "organizations",
            "riskOwnerId": "user",
            "controlId": "",
            "assessmentId": "",
            "requirementId": "",
            "securityPlanId": "",
            "projectId": "",
            "supplyChainId": "",
            "policyId": "",
            "componentId": "",
            "incidentId": "",
        }
        if field_name in lookup_fields.keys():
            return lookup_fields[field_name]
        return ""

    @classmethod
    def is_date_field(cls, field_name: str) -> bool:
        """
        Overrides the base method.

        :param str field_name: The property name to provide enum values for
        :return: bool if the field should be formatted as a date
        :rtype: bool
        """
        return field_name in [
            "dateIdentified",
            "dateClosed",
            "dateLastAssessed",
            "nextAssessmentDueDate",
        ]

    @classmethod
    def get_export_query(cls, app: Application, parent_id: int, parent_module: str) -> list:
        """
        Overrides the base method.

        :param Application app: RegScale Application object
        :param int parent_id: RegScale ID of parent
        :param str parent_module: Module of parent
        :return: list response from RegScale
        :rtype: list
        """
        # This query returns all risks and doesn't use the parent ID or module provided.
        return cls.fetch_all_risks(app)

    @classmethod
    def use_query(cls) -> bool:
        """
        Overrides the base method.

        :return: bool
        :rtype: bool
        """
        return True

    @classmethod
    def get_extra_fields(cls) -> list:
        """
        Overrides the base method.

        :return: list of extra field names
        :rtype: list
        """
        # This method is here because this class isn't descended from RegScaleModel
        return []

    @classmethod
    def get_include_fields(cls) -> list:
        """
        Overrides the base method.

        :return: list of  field names
        :rtype: list
        """
        # This method is here because this class isn't descended from RegScaleModel
        return []
