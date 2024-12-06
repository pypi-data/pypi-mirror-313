#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Wiz Variables """

from regscale.core.app.utils.variables import RsVariableType, RsVariablesMeta


class WizVariables(metaclass=RsVariablesMeta):
    """
    Wiz Variables class to define class-level attributes with type annotations and examples
    """

    # Define class-level attributes with type annotations and examples
    wizFullPullLimitHours: RsVariableType(int, 8)  # type: ignore
    wizUrl: RsVariableType(str, "https://api.us27.app.wiz.io/graphql", required=False)  # type: ignore
    wizIssueFilterBy: RsVariableType(
        str,
        '{"projectId": ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"], "type": ["API_GATEWAY"]}',
        default={},
        required=False,
    )  # type: ignore
    wizInventoryFilterBy: RsVariableType(
        str,
        '{"projectId": ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"], "type": ["API_GATEWAY"]}',
        default="""{"type":
  [ "API_GATEWAY", "BACKUP_SERVICE", "CDN", "CICD_SERVICE", "CLOUD_LOG_CONFIGURATION",
  "CLOUD_ORGANIZATION", "CONTAINER", "CONTAINER_IMAGE", "CONTAINER_REGISTRY", "CONTAINER_SERVICE",
  "CONTROLLER_REVISION", "DATABASE", "DB_SERVER", "DOMAIN", "EMAIL_SERVICE", "ENCRYPTION_KEY",
  "FILE_SYSTEM_SERVICE", "FIREWALL", "GATEWAY", "KUBERNETES_CLUSTER", "LOAD_BALANCER",
  "MANAGED_CERTIFICATE", "MESSAGING_SERVICE", "NAMESPACE", "NETWORK_INTERFACE", "PRIVATE_ENDPOINT",
  "PRIVATE_LINK", "RAW_ACCESS_POLICY", "REGISTERED_DOMAIN", "RESOURCE_GROUP", "SECRET",
  "SECRET_CONTAINER", "SERVERLESS", "SERVERLESS_PACKAGE", "SERVICE_CONFIGURATION",
  "STORAGE_ACCOUNT", "SUBNET", "SUBSCRIPTION", "VIRTUAL_DESKTOP", "VIRTUAL_MACHINE",
  "VIRTUAL_MACHINE_IMAGE", "VIRTUAL_NETWORK", "VOLUME", "WEB_SERVICE" ] }""",
    )  # type: ignore
    wizAccessToken: RsVariableType(str, "", sensitive=True, required=False)  # type: ignore
    wizClientId: RsVariableType(str, "", sensitive=True)  # type: ignore
    wizClientSecret: RsVariableType(str, "", sensitive=True)  # type: ignore
    wizLastInventoryPull: RsVariableType(str, "2022-01-01T00:00:00Z", required=False)  # type: ignore
