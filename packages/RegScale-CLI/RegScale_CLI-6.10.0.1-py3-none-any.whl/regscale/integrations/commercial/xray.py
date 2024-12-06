#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""xray RegScale integration"""
from datetime import datetime

from pathlib import Path
from os import PathLike

import click

from regscale.core.app.application import Application
from regscale.models.integration_models.xray import XRay
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.exceptions import ValidationException


@click.group()
def xray():
    """Performs actions on xray files."""


FlatFileImporter.show_mapping(
    group=xray,
    import_name="xray",
    file_type="json",
)


@xray.command(name="import_xray")
@FlatFileImporter.common_scanner_options(
    message="File path to the folder containing JFrog XRay .json files to process to RegScale.",
    prompt="File path for JFrog XRay files",
    import_name="xray",
)
def import_xray(
    folder_path: PathLike[str],
    regscale_ssp_id: int,
    scan_date: datetime,
    mappings_path: Path,
    disable_mapping: bool,
) -> None:
    """
    Import JFrog XRay scans, vulnerabilities and assets to RegScale from XRay .json files
    """
    from regscale.validation.record import validate_regscale_object

    # click.types.Path to pathlib.Path
    folder_path = Path(folder_path)
    app = Application()
    if not validate_regscale_object(regscale_ssp_id, "securityplans"):
        app.logger.warning("SSP #%i is not a valid RegScale Security Plan.", regscale_ssp_id)
        return
    if len(list(folder_path.glob("*.json"))) == 0:
        app.logger.warning("No xray(JSON) files found in the specified folder.")
        return
    if not scan_date or not FlatFileImporter.check_date_format(scan_date):
        scan_date = datetime.now()
    for file in list(folder_path.glob("*.json")):
        try:
            XRay(
                name="Xray",
                file_path=str(file),
                file_type=file.suffix,
                regscale_ssp_id=regscale_ssp_id,
                scan_date=scan_date,
                mappings_path=mappings_path,
                disable_mapping=disable_mapping,
            )
        except ValidationException as e:
            app.logger.error(f"Validation error: {e}")
            continue
