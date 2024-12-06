#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Snyk RegScale integration"""
from datetime import datetime
from os import PathLike
from pathlib import Path

import click

from regscale.core.app.application import Application
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.models.integration_models.snyk import Snyk
from regscale.validation.record import validate_regscale_object


@click.group()
def snyk():
    """Performs actions on Snyk export files."""


FlatFileImporter.show_mapping(
    group=snyk,
    import_name="snyk",
    file_type="xlsx",
)


@snyk.command(name="import_snyk")
@FlatFileImporter.common_scanner_options(
    message="File path to the folder containing Snyk .xlsx files to process to RegScale.",
    prompt="File path for Snyk files",
    import_name="snyk",
)
def import_snyk(
    folder_path: PathLike[str], regscale_ssp_id: int, scan_date: datetime, mappings_path: Path, disable_mapping: bool
):
    """
    Import scans, vulnerabilities and assets to RegScale from Snyk export files

    """
    app = Application()
    if not validate_regscale_object(regscale_ssp_id, "securityplans"):
        app.logger.warning("SSP #%i is not a valid RegScale Security Plan.", regscale_ssp_id)
        return
    if not scan_date or not FlatFileImporter.check_date_format(scan_date):
        scan_date = datetime.now()
    if len(list(Path(folder_path).glob("*.xlsx"))) == 0:
        app.logger.warning("No Snyk files found in the specified folder.")
        return
    from regscale.exceptions import ValidationException

    for file in Path(folder_path).glob("*.xlsx"):
        try:
            Snyk(
                name="Snyk",
                file_path=str(file),
                parent_id=regscale_ssp_id,
                parent_module="securityplans",
                scan_date=scan_date,
                mappings_path=mappings_path,
                disable_mapping=disable_mapping,
            )
        except ValidationException as e:
            app.logger.error(f"Validation error: {e}")
            continue
