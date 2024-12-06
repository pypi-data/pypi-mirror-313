#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""standard python imports"""
import glob
from datetime import date, datetime
from typing import Optional, Literal
import logging
import click
from dateutil.relativedelta import relativedelta

from regscale.core.app.utils.app_utils import create_progress_object
from regscale.core.app.utils.regscale_utils import check_module_id
from regscale.models import regscale_id, regscale_module

logger = logging.getLogger(__name__)


@click.group()
def fedramp():
    """[BETA] Performs bulk processing of FedRAMP files (Upload trusted data only)."""


# FedRAMP Docx Support
@fedramp.command(context_settings={"show_default": True})
@click.option(
    "--file_name",
    "-f",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    required=True,
    prompt="Enter the full file path of the FedRAMP (.docx) document to ingest to RegScale.",
    help="RegScale will process and load the FedRAMP document.",
)
@click.option(
    "--base_fedramp_profile",
    "-pn",
    type=click.STRING,
    required=False,
    help="Enter the name of the RegScale FedRAMP profile to use.",
    default="FedRAMP - High",
)
@click.option(
    "--base_fedramp_profile_id",
    "-p",
    type=click.INT,
    required=False,
    help="Enter the name of the RegScale FedRAMP profile to use.",
)
@click.option(
    "--save_data",
    type=click.BOOL,
    default=False,
    required=False,
    help="Whether to save the data as a JSON file.",
)
@click.option(
    "--add_missing",
    type=click.BOOL,
    default=False,
    required=False,
    help="Whether to create missing controls from profile in the SSP.",
)
def load_fedramp_docx(
    file_name: click.Path,
    base_fedramp_profile: click.STRING,
    base_fedramp_profile_id: Optional[click.STRING],
    save_data: click.BOOL,
    add_missing: click.BOOL,
):
    """
    Convert a FedRAMP docx file to a RegScale SSP.
    """
    from regscale.core.app.public.fedramp.fedramp_common import process_fedramp_docx

    logger.info(f"Processing FedRAMP document {file_name}.")
    process_fedramp_docx(file_name, base_fedramp_profile, base_fedramp_profile_id, save_data, add_missing)


@fedramp.command()
@click.option(
    "--file_name",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    required=True,
    prompt="Enter the file name of the FedRAMP JSON document to process.",
    help="RegScale will process and load the FedRAMP document.",
)
@click.option(
    "--submission_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
    required=True,
    prompt="Enter the submission date of this FedRAMP document.",
    help=f"Submission date, default is today: {date.today()}.",
)
@click.option(
    "--expiration_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str((datetime.now() + relativedelta(years=3)).date()),
    required=True,
    prompt="Enter the expiration date of this FedRAMP document.",
    help=f"Expiration date, default is {str((datetime.now() + relativedelta(years=3)).date())}.",
)
def load_fedramp_oscal(file_name, submission_date, expiration_date):
    """
    [BETA] Convert a FedRAMP OSCAL SSP json file to a RegScale SSP.
    """
    from regscale.core.app.public.fedramp.fedramp_common import process_fedramp_oscal_ssp

    if not expiration_date:
        today_dt = date.today()
        expiration_date = date(today_dt.year + 3, today_dt.month, today_dt.day)

    process_fedramp_oscal_ssp(file_name, submission_date, expiration_date)


@fedramp.command()
@click.option(
    "--file-path",
    "-f",
    type=click.Path(exists=True),
    help="File to upload to RegScale.",
    required=True,
)
@click.option(
    "--catalogue_id",
    "-c",
    type=click.INT,
    help="The RegScale ID # of the catalogue to use for controls in the profile.",
    required=True,
)
def import_fedramp_ssp_xml(file_path: click.Path, catalogue_id: click.INT):
    """
    Import FedRAMP Revision 4/5 SSP XML into RegScale
    """
    from collections import deque

    from regscale.core.app.public.fedramp.import_fedramp_r4_ssp import parse_and_load_xml_rev4
    from regscale.core.app.public.fedramp.ssp_logger import SSPLogger

    logger = SSPLogger()
    logger.info(event_msg="Importing FedRAMP SSP XML into RegScale")
    parse_generator = parse_and_load_xml_rev4(None, str(file_path), catalogue_id)
    deque(parse_generator, maxlen=1)


@fedramp.command(context_settings={"show_default": True})
@click.option(
    "--file_name",
    "-f",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    required=True,
    prompt="Enter the full file path of the FedRAMP (.docx) document to ingest to RegScale.",
    help="RegScale will process and load the FedRAMP document.",
)
@click.option(
    "--appendix_a_file_name",
    "-a",
    type=click.Path(exists=True),
    required=False,
    prompt="Enter the full file path of the FedRAMP Appendix A (.docx) document to ingest to RegScale.",
    help="RegScale will process and load the FedRAMP Appendix A document.",
)
@click.option(
    "--base_fedramp_profile_id",
    "-p",
    type=click.INT,
    required=True,
    help="The RegScale FedRAMP profile ID to use.",
)
@click.option(
    "--save_data",
    type=click.BOOL,
    default=False,
    required=False,
    help="Whether to save the data as a JSON file.",
)
@click.option(
    "--add_missing",
    type=click.BOOL,
    default=False,
    required=False,
    help="Whether to create missing controls from profile in the SSP.",
)
def load_fedramp_docx_v5(
    file_name: str,
    appendix_a_file_name: str,
    base_fedramp_profile_id: int,
    save_data: click.BOOL,
    add_missing: click.BOOL,
):
    """
    Convert a FedRAMP docx file to a RegScale SSP.
    """
    from regscale.core.app.public.fedramp.fedramp_five import process_fedramp_docx_v5

    process_fedramp_docx_v5(file_name, base_fedramp_profile_id, save_data, add_missing, appendix_a_file_name)


@fedramp.command(context_settings={"show_default": True})
@click.option(
    "--appendix_a_file_name",
    "-a",
    type=click.Path(exists=True),
    required=False,
    prompt="Enter the full file path of the FedRAMP Appendix A (.docx) document to ingest to RegScale.",
    help="RegScale will process and load the FedRAMP Appendix A document.",
)
@click.option(
    "--base_fedramp_profile_id",
    "-p",
    type=click.INT,
    required=True,
    help="The RegScale FedRAMP profile ID to use.",
)
@click.option(
    "--add_missing",
    type=click.BOOL,
    default=False,
    required=False,
    help="Whether to create missing controls from profile in the SSP.",
)
@click.option("--regscale_id", "-i", help="Regscale id to push inventory to in RegScale.", required=True)
def load_fedramp_appendix_a(
    appendix_a_file_name: str, base_fedramp_profile_id: int, add_missing: click.BOOL, regscale_id: int  # noqa
):
    """
    Convert a FedRAMP Appendix A docx file to a RegScale SSP.
    """
    from regscale.core.app.public.fedramp.fedramp_five import load_appendix_a as _load_appendix_a

    _load_appendix_a(
        appendix_a_file_name=appendix_a_file_name,
        parent_id=regscale_id,
        profile_id=base_fedramp_profile_id,
        add_missing=add_missing,
    )


@fedramp.command(name="import_fedramp_inventory")
@click.option(
    "--path",
    "-f",
    type=click.Path(exists=True, dir_okay=True),
    help="The File OR Folder Path to the inventory .xlsx files.",
    prompt="Inventory .xlsx folder location",
    required=True,
)
@click.option(
    "--sheet_name",
    "-s",
    type=click.STRING,
    help="Sheet name in the inventory .xlsx file to parse.",
    default="Inventory",
    required=False,
)
@click.option(
    "--regscale_id",
    "-i",
    type=click.INT,
    help="RegScale Record ID to update.",
    prompt="RegScale Record ID",
    required=True,
)
@click.option(
    "--regscale_module",
    "-m",
    type=click.STRING,
    help="RegScale Module for the provided ID.",
    prompt="RegScale Record Module",
    required=True,
)
def import_fedramp_inventory(path: click.Path, sheet_name: str, regscale_id: int, regscale_module: str):  # noqa
    """
    Import FedRAMP Workbook into RegScale
    """
    import os
    from pathlib import Path

    from regscale.core.app.logz import create_logger
    from regscale.core.app.public.fedramp.import_workbook import upload

    logger = create_logger()
    link_path = Path(path)
    if link_path.is_dir():
        files = glob.glob(str(link_path) + os.sep + "*.xlsx")
        if not files:
            logger.warning("No files found in the folder.")
            return
        for file in files:
            upload(inventory=file, sheet_name=sheet_name, record_id=regscale_id, module=regscale_module)
    elif link_path.is_file():
        upload(inventory=str(link_path), sheet_name=sheet_name, record_id=regscale_id, module=regscale_module)


@fedramp.command(name="import-poam")
@click.option(
    "--file_path",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    required=True,
    prompt="Enter the file path containing FedRAMP (.xlsx) POAM workbook to ingest to RegScale.",
    help="RegScale will process and load the FedRAMP POAMs as RegScale issues.",
)
@regscale_id()
@regscale_module()
@click.option(
    "--poam_id_column",
    "-pc",
    type=click.STRING,
    help="The column name containing the POAM ID.",
    required=False,
    default="POAM ID",
)
def import_fedramp_poam_template(
    file_path: click.Path, regscale_id: int, regscale_module: str, poam_id_column: str
) -> None:
    """
    Import a FedRamp POA&M document to RegScale issues.
    """
    # suppress UserWarnings from openpyxl
    import warnings

    from regscale.models.integration_models.poam import POAM

    warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

    if not check_module_id(parent_id=regscale_id, parent_module=regscale_module):
        raise ValueError(f"RegScale ID {regscale_id} is not a valid member of {regscale_module}.")
    POAM(file_path=file_path, module_id=regscale_id, module=regscale_module, poam_id_header=poam_id_column)


@fedramp.command(name="import-drf")
@click.option(
    "--file_path",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    required=True,
    prompt="Enter the file path containing FedRAMP (.xlsx) POAM workbook to ingest to RegScale.",
    help="RegScale will process and load the FedRAMP POAMs as RegScale issues.",
)
@regscale_id()
@regscale_module()
def import_drf(file_path: click.Path, regscale_id: int, regscale_module: str) -> None:
    """
    Import a FedRamp DRF document to RegScale issues.
    """
    # suppress UserWarnings from openpyxl
    import warnings

    from regscale.models.integration_models.drf import DRF

    warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

    if not check_module_id(parent_id=regscale_id, parent_module=regscale_module):
        raise ValueError(f"RegScale ID {regscale_id} is not a valid member of {regscale_module}.")
    DRF(file_path=file_path, module_id=regscale_id, module=regscale_module)


@fedramp.command(name="import-cis-crm")
@click.option(
    "--file_path",
    "-f",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    help="The file path to the FedRAMP CIS CRM .xlsx file.",
    prompt="FedRAMP CIS CRM .xlsx file location",
    required=True,
)
@click.option(
    "--version",
    "-rev",
    type=click.Choice(["rev4", "rev5", "4", "5"], case_sensitive=False),
    help="FedRAMP revision version.",
    prompt="Rev4 or Rev5",
    required=True,
)
@click.option(
    "--cis_sheet_name",
    "-cis",
    type=click.STRING,
    help="CIS sheet name in the FedRAMP CIS CRM .xlsx to parse.",
    prompt="CIS Sheet Name",
    required=True,
)
@click.option(
    "--crm_sheet_name",
    "-crm",
    type=click.STRING,
    help="CRM sheet name in the FedRAMP CIS CRM .xlsx to parse.",
    prompt="CRM Sheet Name",
    required=True,
)
@click.option(
    "--regscale_ssp_id",
    "-i",
    type=click.INT,
    help="The ID number from RegScale of the System Security Plan.",
    prompt="Enter RegScale System Security Plan ID",
    required=True,
)
@click.option(
    "--leveraged_auth_id",
    "-l",
    type=click.INT,
    help="RegScale Leveraged Authorization ID #, if none provided, one will be created.",
    required=False,
    default=0,
)
def import_ciscrm(
    file_path: click.Path,
    version: str,
    cis_sheet_name: str,
    crm_sheet_name: str,
    regscale_ssp_id: int,
    leveraged_auth_id: int = 0,
):
    """
    [BETA] Import FedRAMP Rev5 CIS/CRM Workbook into a RegScale System Security Plan.
    """
    parse_and_import_ciscrm(
        file_path=file_path,
        version=version,
        cis_sheet_name=cis_sheet_name,
        crm_sheet_name=crm_sheet_name,
        regscale_ssp_id=regscale_ssp_id,
        leveraged_auth_id=leveraged_auth_id,
    )


def parse_and_import_ciscrm(
    file_path: click.Path,
    version: Literal["rev4", "rev5", "4", "5"],
    cis_sheet_name: str,
    crm_sheet_name: str,
    regscale_ssp_id: int,
    leveraged_auth_id: int = 0,
) -> None:
    """
    Parse and import the FedRAMP Rev5 CIS/CRM Workbook into a RegScale System Security Plan

    :param click.Path file_path: The file path to the FedRAMP CIS CRM .xlsx file
    :param Literal["rev4", "rev5"] version: FedRAMP revision version
    :param str cis_sheet_name: CIS sheet name in the FedRAMP CIS CRM .xlsx to parse
    :param str crm_sheet_name: CRM sheet name in the FedRAMP CIS CRM .xlsx to parse
    :param int regscale_ssp_id: The ID number from RegScale of the System Security Plan
    :param int leveraged_auth_id: RegScale Leveraged Authorization ID #, if none provided, one will be created
    :raises ValueError: If the SSP with the given ID is not found in RegScale
    :rtype: None
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    from regscale.core.app.api import Api
    from regscale.core.app.public.fedramp.fedramp_common import (
        new_leveraged_auth,
        parse_and_map_data,
        parse_cis_worksheet,
        parse_crm_worksheet,
        parse_instructions_worksheet,
        update_objective,
    )
    from regscale.models import File, SecurityPlan

    sys_name_key = "System Name"
    api = Api()
    ssp: SecurityPlan = SecurityPlan.get_object(regscale_ssp_id)
    if not ssp:
        raise ValueError(f"SSP with ID {regscale_ssp_id} not found in RegScale.")

    if "5" in version:
        version = "rev5"
    else:
        version = "rev4"

    # parse the instructions worksheet to get the csp name, system name, and other data
    instructions_data = parse_instructions_worksheet(file_path=file_path, version=version)  # type: ignore

    # get the system names from the instructions data by dropping any non-string values
    system_names = [entry[sys_name_key] for entry in instructions_data if isinstance(entry[sys_name_key], str)]
    name_match: str = system_names[0]

    # update the instructions data to the matched system names
    instructions_data = [
        (
            entry
            if isinstance(entry[sys_name_key], str)
            and entry[sys_name_key] == name_match
            or entry[sys_name_key] == ssp.systemName
            else None
        )
        for entry in instructions_data
    ]
    # remove any None values from the instructions data
    instructions_data = [entry for entry in instructions_data if entry][0]
    if not any(instructions_data):
        raise ValueError("Unable to parse data from Instructions sheet.")

    # start parsing the workbook
    cis_data = parse_cis_worksheet(file_path=file_path, cis_sheet_name=cis_sheet_name)
    crm_data = parse_crm_worksheet(file_path=file_path, crm_sheet_name=crm_sheet_name, version=version)  # type: ignore

    if leveraged_auth_id == 0:
        leveraged_auth_id = new_leveraged_auth(
            ssp=ssp,
            user_id=api.config["userId"],
            instructions_data=instructions_data,
            version=version,  # type: ignore
        )

    # Update objectives using the mapped data using threads
    if mapped_data := parse_and_map_data(
        api=api,
        ssp_id=regscale_ssp_id,
        cis_data=cis_data,
        crm_data=crm_data,
    ):
        with create_progress_object() as progress:
            updating_objs = progress.add_task(
                f"Updating {len(mapped_data)} Implementation Objectives...", total=len(mapped_data)
            )
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = [
                    executor.submit(
                        update_objective,
                        api,
                        obj_data,
                        leveraged_auth_id,
                    )
                    for obj_data in mapped_data
                ]
                for future in as_completed(futures):
                    try:
                        future.result()
                    finally:
                        progress.update(updating_objs, advance=1)

    # upload workbook to the SSP
    File.upload_file_to_regscale(
        file_name=str(file_path),
        parent_id=regscale_ssp_id,
        parent_module="securityplans",
        api=api,
    )
