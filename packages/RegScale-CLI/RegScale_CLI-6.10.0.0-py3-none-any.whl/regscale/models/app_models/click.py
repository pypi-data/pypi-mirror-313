#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Module to allow dynamic click arguments and store commonly used click commands """

from pathlib import Path
from typing import Tuple, Any

# stand python imports
import click

from regscale.models.regscale_models.modules import Modules


class NotRequiredIf(click.Option):
    """
    NotRequiredIf class for dynamic click options Updates the help command to let the user know if a
    command is exclusive or not

    :param Tuple *args: List of arguments
    :param **kwargs: Dictionary of keyword arguments
    """

    def __init__(self, *args: Tuple, **kwargs):
        self.not_required_if: list = kwargs.pop("not_required_if")

        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs["help"] = (
            kwargs.get("help", "") + "Option is mutually exclusive with " + ", ".join(self.not_required_if) + "."
        ).strip()
        super(NotRequiredIf, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx: Any, opts: Any, args: Any) -> Any:
        """
        Function to handle the click arguments and whether a parameter is required

        :param Any ctx: Any context
        :param Any opts: Any options
        :param Any args: Any arguments
        :raises click.UsageError: Raises a UsageError if the option is mutually exclusive
        :return: Returns the click option
        :rtype: Any
        """
        current_opt: bool = self.name in opts
        for mutex_opt in self.not_required_if:
            if mutex_opt in opts:
                if current_opt:
                    raise click.UsageError(
                        "Illegal usage: '" + str(self.name) + "' is mutually exclusive with " + str(mutex_opt) + "."
                    )
                else:
                    self.prompt = None
        return super(NotRequiredIf, self).handle_parse_result(ctx, opts, args)


def save_output_to(exists: bool = False, dir_okay: bool = True, file_okay: bool = False) -> click.option:
    """
    Function to return a click.option for saving data to a directory

    :param bool exists: Whether the directory has to exist, default False
    :param bool dir_okay:  Whether to accept a directory, default True
    :param bool file_okay:  Whether a file path will be accepted, default False
    :return: click.option with the provided parameters
    :rtype: click.option
    """
    return click.option(
        "--save_output_to",
        type=click.Path(
            exists=exists,
            dir_okay=dir_okay,
            file_okay=file_okay,
            path_type=Path,
        ),
        help="Provide the path where you would like to save the output to.",
        prompt="Enter directory for file output",
        required=True,
    )


def file_types(accepted_files: list) -> click.option:
    """
    Function to return click.option for accepted file types

    :param list accepted_files: list of file extensions
    :return: click.option with provided file list
    :rtype: click.option
    """
    return click.option(
        "--file_type",
        type=click.Choice(accepted_files, case_sensitive=False),
        help="Select a file type to save the output as.",
        prompt="Enter desired file type",
        required=True,
    )


def regscale_ssp_id(
    help: str = "The ID number from RegScale of the System Security Plan",
    required: bool = True,
    **kwargs: dict,
) -> click.option:
    """
    Function to return click.option for RegScale SSP ID

    :param str help: String to display when user enters --help
    :param bool required: Whether input is required, defaults to True
    :param dict **kwargs: kwargs to pass to click.option
    :return: click.option for RegScale SSP ID
    :rtype: click.option
    """
    if "prompt" not in kwargs:
        return click.option(
            "--regscale_ssp_id",
            "-id",
            "--id",
            type=click.INT,
            help=help,
            required=required,
            prompt="Enter the RegScale System Security Plan ID",
            **kwargs,
        )
    return click.option(
        "--regscale_id",
        "-id",
        type=click.INT,
        help=help,
        required=required,
        **kwargs,
    )


def regscale_id(
    help: str = "Enter the desired ID # from RegScale.",
    required: bool = True,
    **kwargs,
) -> click.option:
    """
    Function to return click.option for RegScale parent ID

    :param str help: String to display when user enters --help
    :param bool required: Whether input is required, defaults to True
    :param **kwargs: kwargs to pass to click.option
    :return: click.option for RegScale parent ID
    :rtype: click.option
    """
    if kwargs.get("prompt") is None:
        return click.option(
            "--regscale_id",
            "-id",
            type=click.INT,
            help=help,
            prompt="Enter the RegScale Record ID",
            required=required,
            **kwargs,
        )
    return click.option(
        "--regscale_id",
        "-id",
        type=click.INT,
        help=help,
        required=required,
        **kwargs,
    )


def regscale_module(required: bool = True, **kwargs) -> click.option:
    """
    Function to return click.option for RegScale modules

    :param bool required: Whether input is required, defaults to True
    :param **kwargs: kwargs to pass to click.option
    :return: click.option for RegScale modules
    :rtype: click.option
    """
    if kwargs.get("prompt") is None:
        return click.option(
            "--regscale_module",
            "-m",
            type=click.STRING,
            help=f"Enter the RegScale module name.\n\n{Modules().to_str_table()}",
            prompt="Enter the RegScale Module name",
            required=required,
            **kwargs,
        )
    return click.option(
        "--regscale_module",
        "-m",
        type=click.STRING,
        help=f"Enter the RegScale module name.\n\n{Modules().to_str_table()}",
        required=required,
        **kwargs,
    )


def hidden_file_path(**kwargs) -> click.option:
    """
    Function to return a hidden click.option for file path
    """
    return click.option(
        "--offline",
        type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path, resolve_path=True),
        help=kwargs.pop("help") if kwargs.get("help") else "Enter the file path",
        hidden=True,
        default=kwargs.get("default"),
        **kwargs,
    )
