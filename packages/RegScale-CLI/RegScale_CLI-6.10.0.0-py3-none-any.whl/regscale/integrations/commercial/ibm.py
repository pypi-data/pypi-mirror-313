#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IBM AppScan RegScale integration"""
from datetime import datetime
from os import PathLike

import click
from pathlib import Path

from regscale.core.app.application import Application
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.models.integration_models.ibm import AppScan
from regscale.validation.record import validate_regscale_object


@click.group()
def ibm():
    """Performs actions on IBM AppScan files."""


FlatFileImporter.show_mapping(
    group=ibm,
    import_name="ibm_appscan",
    file_type="csv",
)


@ibm.command(name="import_appscan")
@FlatFileImporter.common_scanner_options(
    message="File path to the folder containing IBM AppScan .csv files to process to RegScale.",
    prompt="File path for IBM AppScan files",
    import_name="ibm_appscan",
)
def import_appscan(
    folder_path: PathLike[str], regscale_ssp_id: int, scan_date: datetime, mappings_path: Path, disable_mapping: bool
) -> None:
    """
    Import IBM AppScan scans, vulnerabilities and assets to RegScale from IBM AppScan files
    """
    app = Application()
    if not validate_regscale_object(regscale_ssp_id, "securityplans"):
        app.logger.warning("SSP #%i is not a valid RegScale Security Plan.", regscale_ssp_id)
        return
    if not scan_date or not FlatFileImporter.check_date_format(scan_date):
        scan_date = datetime.now()
    if len(list(Path(folder_path).glob("*.csv"))) == 0:
        app.logger.warning("No IBM AppScan(csv) files found in the specified folder.")
        return
    from regscale.exceptions import ValidationException

    for file in Path(folder_path).glob("*.csv"):
        try:
            AppScan(
                name="IBM AppScan",
                file_path=str(file),
                plan_id=regscale_ssp_id,
                scan_date=scan_date,
                mappings_path=mappings_path,
                disable_mapping=disable_mapping,
            )
        except ValidationException as e:
            app.logger.error(f"Validation error: {e}")
            continue
