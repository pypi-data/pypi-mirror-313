#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Pydantic class for custom container scan mappings """
import json
from json import JSONDecodeError
from logging import Logger
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

from pydantic import BaseModel, ConfigDict, field_validator

from regscale.core.app import create_logger
from regscale.core.app.utils.app_utils import check_file_path, error_and_exit, save_data_to
from regscale.exceptions import ValidationException


class Mapping(BaseModel):
    """
    Pydantic class for custom container scan mappings
    """

    model_config = ConfigDict(populate_by_name=True, json_encoders={bytes: lambda v: v.decode()})

    mapping: Dict[str, str]
    # expected field names for validation
    expected_field_names: List[str] = []
    _logger: Logger = create_logger()

    @classmethod
    def _prompt_for_field(
        cls, field: str, mapping: Union[dict, "Mapping"], parsed_headers: Optional[List[str]] = None
    ) -> str:
        """
        Prompt for a field value

        :param str field: Field to prompt for
        :param Union[dict, "Mapping"] mapping: Mapping object or dictionary of the mapping object
        :param Optional[List[str]] parsed_headers: Parsed headers from file, defaults to None
        :return: Field value
        :rtype: str
        """
        cls._logger.default.info(
            f"Field '{field}' not found in mapping, please enter the mapping for this field or enter 'exit' to exit"
            f"\nAvailable headers are: {parsed_headers or list(mapping.items())}"
        )
        custom_mapping = input(f"Enter the mapping for field '{field}':")
        if custom_mapping.lower() == "exit":
            error_and_exit("Exiting...")
        confirm = input(f"Confirm the mapping for field '{field}' is '{custom_mapping}' (y/n)")
        if confirm.lower() == "y":
            if parsed_headers and custom_mapping not in parsed_headers:
                cls._logger.default.warning(
                    f"Mapping {custom_mapping} is not found in the headers. "
                    f"Please select one of the following headers: {parsed_headers}."
                )
                cls._prompt_for_field(field=field, mapping=mapping, parsed_headers=parsed_headers)
            elif custom_mapping not in mapping.values() and not parsed_headers:
                cls._logger.default.warning(
                    f"Mapping {custom_mapping} is not found in the headers. "
                    f"Please select one of the following headers: {list(mapping.values())}."
                )
                cls._prompt_for_field(field=field, mapping=mapping, parsed_headers=parsed_headers)
            else:
                if isinstance(mapping, dict):
                    mapping[field] = custom_mapping
                else:
                    mapping.mapping[field] = custom_mapping
        elif confirm.lower() == "exit":
            error_and_exit("Exiting...")
        else:
            cls._prompt_for_field(field=field, mapping=mapping, parsed_headers=parsed_headers)

    @field_validator("expected_field_names")
    def validate_mapping(cls: Type["Mapping"], expected_field_names: List[str], values: Dict[str, Any]) -> List[str]:
        """
        Validate the expected field names

        :param List[str] expected_field_names: Expected field names
        :param Dict[str, Any] values: Values
        :return: Expected field names
        """
        mapping = values.data.get("mapping")
        if mapping is not None and expected_field_names is not None:
            if missing_fields := [field for field in expected_field_names if field not in mapping]:
                for field in missing_fields:
                    cls._prompt_for_field(field, mapping)
        return expected_field_names

    @field_validator("expected_field_names")
    def validate_expected_field_names(cls: Type["Mapping"], expected_field_names: Any) -> List[str]:
        """
        Validate the expected field names and types

        :param Any expected_field_names: Expected field names
        :raises ValidationError: If expected_field_names is not a list or if any element in the list is not a string
        :rtype: List[str]
        :return: Expected field names
        """
        if not isinstance(expected_field_names, list):
            raise ValidationException("expected_field_names must be a list")
        if not all(isinstance(field_name, str) for field_name in expected_field_names):
            raise ValidationException("All elements in expected_field_names must be strings")
        return expected_field_names

    # Add a from file method to load the mapping from a JSON file
    @classmethod
    def from_file(cls, file_path: Path, expected_field_names: List[str], **kwargs) -> "Mapping":
        """
        Load the mapping from a JSON file

        :param Path file_path: Path to the JSON file
        :param List[str] expected_field_names: Expected field names
        :return: Validated Mapping ob
        :rtype: Mapping
        """
        if not file_path.exists() and kwargs.get("mapping"):
            check_file_path(file_path.parent)
            dat = kwargs.get("mapping")
            mapping = cls(mapping=dat["mapping"], expected_field_names=expected_field_names)
        else:
            with open(file_path, "r") as file:
                try:
                    dat = json.load(file)
                    # if mapping is not found in the JSON file, check the kwargs for the provided mapping and use that
                    if not dat.get("mapping"):
                        dat["mapping"] = kwargs.get("mapping")
                        if not dat.get("mapping"):
                            error_and_exit("Mapping not found in JSON file")
                    if parsed_headers := kwargs.get("parsed_headers"):
                        cls._verify_parsed_headers(parsed_headers, expected_field_names, dat)
                    mapping = cls(mapping=dat["mapping"], expected_field_names=expected_field_names)
                except JSONDecodeError as jex:
                    cls._logger.default.debug(jex)
                    error_and_exit("JSON file is badly formatted, please check the file")
                except (ValueError, SyntaxError) as exc:
                    error_and_exit(f"Error parsing JSON file: {exc}")
        if not mapping:
            error_and_exit("Error loading mapping from file. Exiting...")
        mapping.save_mapping(file_path)
        return mapping

    @classmethod
    def _verify_parsed_headers(cls, parsed_headers: List[str], expected_field_names: List[str], dat: dict) -> None:
        """
        Verify the parsed headers and prompt for missing headers

        :param List[str] parsed_headers: Parsed headers
        :param List[str] expected_field_names: Expected field names
        :param Dict[str, Any] dat: Data dictionary
        :rtype: None
        """
        if missing_headers := [
            header
            for header in expected_field_names
            if header not in parsed_headers and dat["mapping"].get(header) not in parsed_headers
        ]:
            for header in missing_headers:
                cls._logger.default.info(f"Header '{header}' not found in parsed headers. Please enter the mapping.")
                cls._prompt_for_field(field=header, mapping=dat["mapping"], parsed_headers=parsed_headers)

    def save_mapping(self, file_path: Path) -> None:
        """
        Save the mapping to a JSON file

        :param Path file_path: Path to save the mapping JSON file
        :rtype: None
        """
        check_file_path(file_path.parent)
        save_data_to(file_path, {"mapping": self.mapping})

    def get_header(self, key: str) -> str:
        """
        Get the header for a key

        :param str key: Key to get the header for
        :return: Header for the key
        :rtype: str
        """
        return self.mapping.get(key)

    def get_value(self, dat: Optional[dict], key: str, default_val: Optional[Any] = "", warnings: bool = True) -> Any:
        """
        Get the value from a dictionary by mapped key

        :param Optional[dict] dat: Data dictionary, defaults to None
        :param str key: Key to get the value for
        :param Optional[Any] default_val: Default value to return, defaults to empty string
        :param bool warnings: Whether to log warnings, defaults to False
        :return: Value for the key
        :rtype: Any
        """
        # check mapping
        mapped_key = self.mapping.get(key)
        if not mapped_key and warnings:
            self._logger.warning(f"Value for key '{key}' not found in mapping.")
        if dat and mapped_key:
            val = dat.get(mapped_key)
            if isinstance(val, str):
                return val.strip()
            return val or default_val
        return default_val

    def to_header(self) -> list[str]:
        """
        Convert the mapping to a header
        :return: Mapping as a header
        :rtype: list[str]
        """
        # convert mapping to a list of strings
        return [f"{value}" for key, value in self.mapping.items()]
