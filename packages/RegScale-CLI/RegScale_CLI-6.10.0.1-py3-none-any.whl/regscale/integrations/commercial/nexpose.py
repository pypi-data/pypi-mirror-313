#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nexpose RegScale integration"""
import ast
from datetime import datetime
from os import PathLike
from pathlib import Path

import click
from rich.console import Console

from regscale.core.app.application import Application
from regscale.models.app_models.mapping import Mapping
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.models.integration_models.nexpose import Nexpose
from regscale.validation.record import validate_regscale_object


@click.group()
def nexpose():
    """Performs actions on Nexpose files."""


FlatFileImporter.show_mapping(
    group=nexpose,
    import_name="nexpose",
    file_type="csv",
)


@nexpose.command(name="import_nexpose")
@FlatFileImporter.common_scanner_options(
    message="File path to the folder containing Nexpose .csv files to process to RegScale.",
    prompt="File path for Nexpose files:",
    import_name="nexpose",
)
def import_nexpose(
    folder_path: PathLike[str], regscale_ssp_id: int, scan_date: datetime, mappings_path: Path, disable_mapping: bool
) -> None:
    """
    Import Nexpose scans, vulnerabilities and assets to RegScale from Nexpose files
    """
    app = Application()
    if not validate_regscale_object(regscale_ssp_id, "securityplans"):
        app.logger.warning("SSP #%i is not a valid RegScale Security Plan.", regscale_ssp_id)
        return
    if not scan_date or not FlatFileImporter.check_date_format(scan_date):
        scan_date = datetime.now()
    if len(list(Path(folder_path).glob("*.csv"))) == 0:
        app.logger.warning("No Nexpose(csv) files found in the specified folder.")
        return
    from regscale.exceptions import ValidationException

    for file in Path(folder_path).glob("*.csv"):
        try:
            Nexpose(
                name="Nexpose",
                file_path=str(file),
                plan_id=regscale_ssp_id,
                scan_date=scan_date,
                mappings_path=mappings_path,
                disable_mapping=disable_mapping,
            )
        except ValidationException as e:
            app.logger.error(f"Validation error: {e}")
            continue
