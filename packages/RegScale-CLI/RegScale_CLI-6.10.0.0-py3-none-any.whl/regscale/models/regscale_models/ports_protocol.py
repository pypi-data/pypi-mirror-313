#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Class for a RegScale Ports and Protocols """
from typing import Optional

from pydantic import ConfigDict

from regscale.models.regscale_models.regscale_model import RegScaleModel


class PortsProtocol(RegScaleModel):
    """Ports And Protocols"""

    _module_slug = "portsprotocols"
    _unique_fields = [
        [
            "parentId",
            "parentModule",
            "startPort",
            "endPort",
            "protocol",
            "service",
        ],
    ]

    startPort: int
    endPort: int
    parentId: int = 0
    parentModule: str = ""
    protocol: Optional[str] = None
    service: Optional[str] = None
    purpose: Optional[str] = None
    usedBy: Optional[str] = None
    createdById: Optional[str] = None
    lastUpdatedById: Optional[str] = None
    isPublic: Optional[bool] = True

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get additional endpoints for the PortsProtocols model.

        :return: A dictionary of additional endpoints
        :rtype: ConfigDict
        """
        return ConfigDict(
            get_all_by_parent="/api/{model_slug}/getAllByParent/{intParentID}/{strModule}",
            find="/api/{model_slug}/find/{id}",
        )

    def __eq__(self, other: object) -> bool:
        """
        Compare two PortsProtocols objects

        :param object other: PortsProtocols object
        :return: True if PortsProtocols are equal
        :rtype: bool
        """
        if isinstance(other, PortsProtocol):
            return self.dict() == other.dict()
        return False

    def __hash__(self) -> hash:
        """
        Return hash of PortsProtocols

        :return: hash of PortsProtocols
        :rtype: hash
        """
        return hash(
            (
                self.parentId,
                self.parentModule,
                self.startPort,
                self.endPort,
                self.protocol,
                self.service,
                self.purpose,
                self.usedBy,
            )
        )
