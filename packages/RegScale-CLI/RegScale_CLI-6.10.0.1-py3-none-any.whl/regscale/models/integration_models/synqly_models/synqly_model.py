#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Base Synqly Model """
import json
import logging
import signal
from abc import ABC
from typing import Any, Optional, TypeVar

import httpx
from pydantic import BaseModel, ConfigDict, Field
from rich.progress import Progress
from synqly import management as mgmt
from synqly.engine.client import SynqlyEngine
from synqly.management.client import SynqlyManagement

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.utils.app_utils import create_progress_object, error_and_exit
from regscale.models.integration_models.synqly_models.connector_types import ConnectorType
from regscale.models.integration_models.synqly_models.ocsf_mapper import Mapper
from regscale.models.integration_models.synqly_models.param import Param
from regscale.models.integration_models.synqly_models.tenants import Tenant

S = TypeVar("S", bound="SynqlyModel")


class SynqlyModel(BaseModel, ABC):
    """Class for Synqly integration to add functionality to interact with Synqly via SDK"""

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True, arbitrary_types_allowed=True)

    _connector_type: Optional[str] = ""
    tenant: Optional[Tenant] = None
    client: Optional[SynqlyEngine] = None
    connectors: dict = {}
    # defined using the openApi spec on 7/16/2024, this is updated via _get_integrations_and_secrets()
    connector_types: set = set([type.__str__() for type in ConnectorType])
    terminated: Optional[bool] = False
    app: Application = Field(default_factory=Application, alias="app")
    api: Api = Field(default_factory=Api, alias="api")
    logger: logging.Logger = Field(default=logging.getLogger("rich"), alias="logger")
    job_progress: Optional[Progress] = None
    integration: str = ""
    integrations: list = []
    integrations_and_secrets: dict = {}
    integration_config: Any = None
    capabilities: list[str] = []
    authentication_type: str = ""
    authentication_object: str = ""
    synqly_url: str = "https://api.synqly.com/v1/capabilities/providers"
    config_types: list = []
    mapper: Mapper = Field(default_factory=Mapper, alias="mapper")
    required_secrets: dict[str, list[Param]] = {}
    optional_params: dict[str, list[Param]] = {}
    required_params: dict[str, list[Param]] = {}
    created_integration_objects: list = []
    created_regscale_objects: list = []
    updated_regscale_objects: list = []
    regscale_objects_to_update: list = []

    def __init__(self: S, connector_type: Optional[str] = None, integration: Optional[str] = None, **kwargs):
        try:
            if connector_type and integration:
                super().__init__(connector_type=connector_type, integration=integration, **kwargs)
                job_progress = create_progress_object()
                self.job_progress = job_progress
                self.logger.info(f"Initializing {connector_type} connector for the {integration} integration...")
                self._connector_type = connector_type.lower()
                self.connectors = self._get_integrations_and_secrets()
                if self._connector_type not in self.connector_types:
                    raise ValueError(
                        f"Invalid connector type: {self._connector_type}. "
                        f"Please use one of {', '.join(self.connector_types)}."
                    )
                self.integrations = self.connectors[self._connector_type]
                self.integration = self._correct_integration_name(integration)
                if self.integration not in self.integrations:
                    raise ValueError(
                        f"Invalid integration: {self.integration}. Please use one of {', '.join(self.integrations)}."
                    )
                # Populate the required secrets and optional params
                self._flatten_secrets()
                # Initialize signal handlers to intercept Ctrl-C and perform cleanup
                signal.signal(signal.SIGINT, lambda signal, frame: self._cleanup_handler())
                signal.signal(signal.SIGTERM, lambda signal, frame: self._cleanup_handler())
                self.logger.info(f"{self._connector_type.title()} initialized for {integration}.")
            else:
                # if the connector type and integration are not provided, we need to generate jobs
                super().__init__(**kwargs)
        except Exception as e:
            if connector_type and integration:
                error_and_exit(f"Error creating {connector_type} connector for the {integration} integration: {e}")
            else:
                error_and_exit(f"Error creating {self.__class__.__name__}: {e}")

    def _correct_integration_name(self, provided_integration: str) -> str:
        """
        Correct the integration name to match the integration case

        :param str provided_integration: Integration name to correct
        :return: Corrected integration name
        :rtype: str
        """
        for integration in self.integrations:
            if provided_integration.lower() == integration.lower():
                return integration
        return provided_integration

    def _update_secret_and_param(self, key: str, data: dict, attribute: str) -> None:
        """
        Update the secret and parameter objects

        :param str key: The key to update
        :param dict data: The data to update
        :param str attribute: The attribute to update
        :rtype: None
        """
        if key == "credential" and any(isinstance(v, dict) for v in data[key].values()):
            for k, v in data[key].items():
                if k == "optional":
                    continue
                getattr(self, attribute)[k] = Param(**v)
        elif key != "optional":
            try:
                getattr(self, attribute)[key] = Param(**data[key])
            except Exception as e:
                self.logger.error(f"Error updating {key} in {attribute}: {e}\n{data=}")

    def _flatten_secrets(self, integration: Optional[str] = None, return_secrets: bool = False) -> Optional[dict]:
        """
        Flatten the secrets for the integration into required and optional parameters

        :param Optional[str] integration: Integration to flatten secrets for, used during code gen, defaults to None
        :param bool return_secrets: Whether the secrets should be returned, used during code gen, defaults to False
        :return: Params and secrets as a dictionary, if return_secrets is True
        :rtype: Optional[dict]
        """
        if return_secrets:
            self.required_secrets = {}
            self.optional_params = {}
            self.required_params = {}
        for attribute in ["required_secrets", "optional_params", "required_params"]:
            key = f"{self._connector_type}_{self.integration}" if not integration else f"{integration}"
            data = self.integrations_and_secrets[key][attribute]
            for secret in data:
                self._update_secret_and_param(secret, data, attribute)
        if return_secrets:
            return {
                "required_secrets": self.required_secrets,
                "optional_params": self.optional_params,
                "expected_params": self.required_params,
            }

    def create_config_and_validate_secrets(self, **kwargs) -> Any:
        """
        Create a new config for the integration and validates the secrets using kwargs and init.yaml

        :raises ModuleNotFoundError: If unable to parse the config object
        :return: The ticketing configuration
        :rtype: Any
        """
        # store config if we need to update it, if needed
        config = self.app.config
        # build a dictionary to contain missing secrets
        missing_secrets: dict[str, Param] = {}
        skip_prompts = kwargs.pop("skip_prompts", False)
        config_object = getattr(mgmt, f"ProviderConfig_{self._connector_type.title()}{self.integration.title()}", None)
        if not config_object:
            raise ModuleNotFoundError(f"Unable to find the config object for {self._connector_type}_{self.integration}")
        check_attributes = [self.required_secrets, self.required_params]
        for attribute in check_attributes:
            for secret in attribute:
                if secret != "optional":
                    kwargs.update(
                        self._update_config_and_kwargs(
                            attribute=attribute,  # type: ignore
                            key=secret,
                            config=config,
                            skip_prompts=skip_prompts,
                            missing_secrets=missing_secrets,
                            **kwargs,
                        )
                    )
        self.app.save_config(config)
        if missing_secrets:
            self.logger.error("Missing required secrets:")
            for secret, data in missing_secrets.items():
                self.logger.error(f"{secret} ({data.expected_type}) - {data.description}")
            error_and_exit("Please provide the required secrets mentioned above.")
        self.integration_config = config_object(
            type=f"{self._connector_type.lower()}_{self.integration.lower()}",
            url=kwargs.get("url"),
            credential=self._get_auth_method(**kwargs),
        )

    def _get_auth_method(self, **kwargs) -> Any:
        """
        Get the authentication method for the integration

        :raises ValueError: If unable to find the authentication method
        :return: The authentication method
        :rtype: Any
        """
        if auth_object := getattr(mgmt, f"{self.authentication_object}_{self.authentication_type.title()}"):
            return auth_object(type=self.authentication_type, **kwargs)
        else:
            raise ValueError(f"Unable to find the authentication method for {self.integration}")

    def _update_config_and_kwargs(
        self,
        attribute: dict[str, Param],
        key: str,
        config: Any,
        skip_prompts: bool,
        missing_secrets: dict[str, Param],
        **kwargs,
    ) -> dict:
        """
        Update the config object and keyword arguments

        :param dict[str, list[Param]] attribute: The attribute to update
        :param str key: The secret to check and update
        :param Any config: The config object to update
        :param bool skip_prompts: Flag to indicate if prompts should be skipped
        :param dict[str, Param] missing_secrets: Dictionary to store missing secrets
        :return: Updated kwargs if the secret is found in the config, rather than kwargs
        :rtype: dict
        """
        if key not in kwargs and not config.get(f"{self._connector_type}_{self.integration}_{key}"):
            if not skip_prompts:
                self.logger.info(f"Enter the {key} for {self.integration}. Description: {attribute[key].description}")
                provided_secret = input(f"{key}: ")
                kwargs[key] = provided_secret
                config[f"{self._connector_type}_{self.integration}_{key}"] = provided_secret
            else:
                missing_secrets[key] = attribute[key]
        # make sure the secret is in the config
        if key in kwargs and not config.get(f"{self._connector_type}_{self.integration}_{key}"):
            config[f"{self._connector_type}_{self.integration}_{key}"] = kwargs[key]
        # make sure the secret is in the kwargs, load it from the config
        if key not in kwargs and config.get(f"{self._connector_type}_{self.integration}_{key}"):
            kwargs[key] = config[f"{self._connector_type}_{self.integration}_{key}"]
        return kwargs

    @staticmethod
    def _load_from_package() -> dict:
        """
        Load the capabilities.json from the RegScale CLI package

        :return: The capabilities.json
        :rtype: dict
        """
        import importlib.resources as pkg_resources

        # check if the filepath exists before trying to open it
        with pkg_resources.open_text("regscale.models.integration_models.synqly_models", "capabilities.json") as file:
            data = json.load(file)
            return data["result"]

    def _get_integrations_and_secrets(self, return_params: bool = False) -> dict:
        """
        Function to get the integrations and secrets from the API

        :param bool return_params: Flag to indicate if the params should be returned
        :return: Integrations and secrets
        :rtype: dict
        """
        res = self.api.get(self.synqly_url, headers={})
        if res.status_code != 200:
            # load the metadata.yaml from the CLI package
            raw_data = self._load_from_package()
        else:
            try:
                raw_data = res.json()["result"]
            except (json.JSONDecodeError, KeyError):
                raw_data = self._load_from_package()
        return self._parse_api_spec_data(raw_data, return_params)

    def _parse_api_spec_data(self, data: dict, return_params: bool = False) -> dict:
        """
        Function to parse the Synqly OpenAPI spec metadata

        :param dict data: Data to parse
        :param bool return_params: Flag to indicate if the params should be returned
        :return: Parsed integrations, or parsed data and params if return_params is True
        :rtype: dict
        """
        integrations: dict = {}
        # per Synqly, this is the best way to get all integrations in one place
        parsed_integrations = [integration["id"] for integration in data if "mock" not in integration.get("id", "")]
        self.connector_types = {key.split("_")[0] for key in parsed_integrations}
        total_count = len(parsed_integrations)
        scrubbed_data = {
            integration["id"]: integration for integration in data if integration["id"] in parsed_integrations
        }
        parsed_count = 0
        for key, val in scrubbed_data.items():
            code_gen = False
            # Split the string at the underscore
            if self._connector_type and self._connector_type.lower() not in key.lower():
                continue
            elif not self._connector_type:
                code_gen = True
            self.config_types.append(key)
            self.logger.debug(f"Processing secrets for {key}")
            self.integrations_and_secrets[key] = self._parse_capabilities_params_and_secrets(scrubbed_data, key)
            self.logger.debug(f"Successfully processed secrets for {key}")
            parsed_count += 1
            # Add the item to the dictionary
            if self._connector_type not in integrations:
                integrations[self._connector_type] = []
            integrations[self._connector_type].append(key.split("_")[-1])
            self.logger.debug(f"Successfully processed {parsed_count}/{total_count} integrations")
            if code_gen:
                self._connector_type = None
        if return_params:
            return self.integrations_and_secrets
        return integrations

    def _set_optional_flag(self, data: dict, optional: bool) -> dict:
        """
        Function to recursively set the optional flag in the provided dictionary

        :param dict data: Object to set the optional flag for
        :param bool optional: Flag to indicate if the object is optional
        :return: Updated dictionary object with the optional flag set
        :rtype: dict
        """
        # Check if there is a nested dict and set the optional flag for the nested dict
        for key, value in data.items():
            if isinstance(value, dict):
                data[key]["optional"] = data[key].get("optional", optional)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        index = value.index(item)
                        value[index] = self._set_optional_flag(item, optional)
        data["optional"] = optional
        return data

    @staticmethod
    def _select_auth_method(credential_schema: dict) -> dict:
        """
        Function to iterate different auth methods and their required secrets: basic -> token -> oath

        :param dict credential_schema: Credential schema to select auth method from
        :return: Auth method schema
        :rtype: dict
        """
        for item in credential_schema["oneOf"]:
            if "basic" in item.get("title", "").lower():
                return item
        for item in credential_schema["oneOf"]:
            if "token" in item.get("title", "").lower():
                return item
        for item in credential_schema["oneOf"]:
            if "oath" in item.get("title", "").lower():
                return item

    def _process_credential_schema(
        self, credential_schema: dict, credentials: dict, integration: Optional[str] = None
    ) -> None:
        """
        Function to process credential schema and update credentials dictionary

        :param dict credential_schema: Credential schema to update credentials from
        :param dict credentials: Credentials to update
        :param Optional[str] integration: Integration to set authentication type for, defaults to None
        :rtype: None
        """
        if "oneOf" in credential_schema:
            credential_schema = self._select_auth_method(credential_schema)
        required_secrets = credential_schema.get("required", [])
        for key, value in credential_schema.get("properties", {}).items():
            if key == "type" and integration and self.integration.lower() == integration.lower():
                self.authentication_type = value["const"]
                self.authentication_object = credential_schema["x-synqly-credential"]["type"]
            elif key != "type" and value.get("nullable", False):
                continue
            elif key != "type":
                value["optional"] = value in required_secrets
                credentials[key] = value

    def _parse_capabilities_params_and_secrets(self, data: dict, key: Optional[str] = None) -> dict:
        """
        Function to parse the required secrets, params and capabilities from the Synqly metadata, with the provided key

        :param dict data: Data from the OpenAPI spec
        :param Optional[str] key: The schema key to parse the required secrets from, defaults to None
        :raises KeyError: If the schema key is not found in the OpenAPI schema
        :raises ValueError: If no 'credential' property is found for the schema key
        :return: Dictionary of the required secrets
        :rtype: dict
        """
        if key is None:
            raise KeyError(f"Key '{key}' not found in the JSON schema.")

        schema = data[key]
        if schema.get("provider_config") is None:
            raise ValueError(f"No 'provider_config' found for key '{key}'.")

        if schema["provider_config"].get("properties") is None:
            raise ValueError(f"No 'properties' found in the 'provider_config' for key '{key}'.")

        operations = schema.get("operations", [])
        capabilities = [item["name"] for item in operations if item.get("supported")]
        capabilities_params = list(
            field
            for item in operations
            if item.get("supported") and "required_fields" in item.keys()
            for field in item.get("required_fields", [])
        )
        if self.integration.lower() in key.lower():
            self.capabilities = capabilities
        schema = schema["provider_config"]

        credentials = {}
        final_creds = {"description": "", "required_params": {}, "optional_params": {}, "required_secrets": {}}
        required = schema.get("required", [])

        for prop_key, prop in schema["properties"].items():
            if prop_key == "type":
                continue
            elif prop_key == "credential":
                self._process_credential_schema(
                    credential_schema=prop, credentials=credentials, integration=key.split("_")[-1]
                )
            elif prop_key in required:
                prop["optional"] = False
                credentials[prop_key] = prop
            else:
                if prop.get("nullable", True):
                    prop["optional"] = True
                    final_creds["optional_params"][prop_key] = prop
                else:
                    prop["optional"] = False
                    final_creds["required_params"][prop_key] = prop
        self._parse_capability_params(capabilities_params=capabilities_params, integration=key, final_creds=final_creds)

        final_creds["required_secrets"] = credentials
        final_creds["description"] = schema.get("description", "")
        final_creds["capabilities"] = capabilities
        return final_creds

    @staticmethod
    def _parse_capability_params(capabilities_params: list[str], integration: str, final_creds: dict) -> None:
        """
        Function to parse the capability parameters and determine if they are required or optional

        :param list[str] capabilities_params: List of capability parameters
        :param str integration: The name of the integration
        :param dict final_creds: The final credentials dictionary to update
        :rtype: None
        """
        for param in capabilities_params:
            if param in ["summary", "creator", "priority", "status"]:
                continue
            prop = {
                "description": f'{integration.split("_")[-1]} {" ".join(param.split("_"))}',
                "type": "string",
                "optional": False,
            }
            final_creds["required_params"][param] = prop

    @staticmethod
    def create_name_safe_string(tenant_name: str, replace_char: Optional[str] = "-") -> str:
        """
        Function to create a friendly Synqly tenant name

        :param str tenant_name: The original string to convert
        :param Optional[str] replace_char: The character to replace unsafe characters with, defaults to "-"
        :return: Safe tenant name
        :rtype: str
        """
        for unsafe_char in [".", " ", "/", ":"]:
            tenant_name = tenant_name.replace(unsafe_char, replace_char)
        return tenant_name.lower()

    def _cleanup_handler(self):
        """
        Deletes resources created by the connector and integration
        """
        if self.tenant:
            self.logger.info(f"\nCleaning up {self._connector_type} connector resources:")
            self.tenant.management_client.accounts.delete(self.tenant.account_id)
            self.logger.debug("Cleaned up Account " + self.tenant.account_id)
            self.terminated = True
            self.logger.info("Cleanup complete.")
            quit()

    def get_or_create_tenant(self, synqly_org_token: str, new_tenant_name: str):
        """
        Adds a new "tenant" to the App. A tenant represents a user or
        organization within your application.

        :param str synqly_org_token: The Synqly Organization token
        :param str new_tenant_name: The name of the new tenant
        :raises ValueError: If the tenant already exists
        """
        # configure a custom httpx_client so that all errors are retried
        transport = httpx.HTTPTransport(retries=3)

        # this creates a httpx logger
        management_client = SynqlyManagement(
            token=synqly_org_token,
            httpx_client=httpx.Client(transport=transport),
        )
        # Get the httpx logger and set the logging level to CRITICAL in order to suppress all lower level log messages
        httpx_logger = logging.getLogger("httpx")
        httpx_logger.setLevel(logging.CRITICAL)

        # Each tenant needs an associated Account in Synqly, so we create that now.

        account_request = mgmt.CreateAccountRequest(name=new_tenant_name)
        try:
            account_response = management_client.accounts.create(request=account_request)
            account_id = account_response.result.account.id
        except Exception as ex:
            existing_accounts = management_client.accounts.list(filter=f"name[eq]{new_tenant_name}")
            account_id = [account.id for account in existing_accounts.result if account.fullname == new_tenant_name]
            if not account_id:
                raise ValueError("Failed to create account: " + str(ex))
            account_id = account_id[0]

        self.tenant = Tenant(
            tenant_name=new_tenant_name,
            account_id=account_id,
            management_client=management_client,
            engine_client=None,
        )

    def configure_integration(self, tenant_name: str, provider_config: mgmt.ProviderConfig, retries: int = 3):
        """
        Configures a Synqly Integration for a tenant

        :param str tenant_name: The name of the tenant
        :param mgmt.ProviderConfig provider_config: The provider configuration
        :param int retries: The number of retries to attempt to create or recreate the integration
        :raises RuntimeError: If unable to create the Integration after 3 attempts
        :raises ValueError: If unable to find an existing Integration for the provided tenant_name
        """
        # check retries
        if retries == 0:
            raise RuntimeError("Failed to create Integration after 3 attempts")
        # Use the Management API to create a Synqly Integration
        integration_name = f"{tenant_name}-integration"
        integration_req = mgmt.CreateIntegrationRequest(
            name=integration_name,
            provider_config=provider_config,
        )
        # try to create it, if there is an error see if it already exists
        try:
            integration_resp = self.tenant.management_client.integrations.create(
                account_id=self.tenant.account_id, request=integration_req
            )
            # Add Synqly Engine client to the Tenant for use in the background job
            self.tenant.engine_client = SynqlyEngine(
                token=integration_resp.result.token.access.secret,
            )
            self.client = self.tenant.engine_client
            self.logger.debug(
                "Created {} Integration '{}' for {}".format(
                    integration_resp.result.integration.category,
                    integration_resp.result.integration.id,
                    tenant_name,
                )
            )
        except Exception as ex:
            existing_integrations = self.tenant.management_client.integrations.list(
                filter=f"name[eq]{integration_name}"
            )
            integration = [
                integration for integration in existing_integrations.result if integration.name == integration_name
            ]
            if not integration:
                raise ValueError(f"Failed to create Integration. {ex}")
            integration = integration[0]
            # delete the integration and create a new one
            self.tenant.management_client.integrations.delete(
                account_id=self.tenant.account_id, integration_id=integration.id
            )
            self.logger.debug(
                "Deleting existing {} Integration '{}' for {} and attempting to create a new one".format(
                    integration.category,
                    integration.id,
                    tenant_name,
                )
            )
            self.configure_integration(tenant_name, provider_config, retries - 1)
