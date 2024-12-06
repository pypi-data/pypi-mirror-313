#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ECR RegScale integration"""
from datetime import datetime

import click

from regscale.core.app.application import Application
from regscale.models.integration_models.ecr_models.ecr import ECR
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.validation.record import validate_regscale_object


@click.group()
def ecr():
    """Performs actions on ECR Scanner artifacts."""


FlatFileImporter.show_mapping(
    group=ecr,
    import_name="ecr",
)


@ecr.command(name="import_ecr")
@FlatFileImporter.common_scanner_options(
    message="File path to the folder containing ECR files to process to RegScale.",
    prompt="File path for ECR files",
    import_name="ecr",
)
def import_ecr(
    folder_path: click.Path,
    regscale_ssp_id: click.INT,
    scan_date: click.DateTime,
    mappings_path: click.Path,
    disable_mapping: click.BOOL,
):
    """
    Import ECR scans, vulnerabilities and assets to RegScale from ECR JSON files
    """
    import_ecr_scans(
        folder_path=folder_path,
        regscale_ssp_id=regscale_ssp_id,
        scan_date=scan_date,
        mappings_path=mappings_path,
        disable_mapping=disable_mapping,
    )


def import_ecr_scans(
    folder_path: click.Path,
    regscale_ssp_id: click.INT,
    scan_date: click.DateTime,
    mappings_path: click.Path,
    disable_mapping: click.BOOL,
) -> None:
    """
    Function to import ECR scans to RegScale as assets and vulnerabilities

    :param os.PathLike[str] folder_path: Path to the folder containing ECR files
    :param int regscale_ssp_id: RegScale System Security Plan ID
    :param datetime.date scan_date: Date of the scan
    :param click.Path mappings_path: Path to the header mapping file
    :param bool disable_mapping: Disable header mapping
    :rtype: None
    """
    from pathlib import Path

    app = Application()
    if not validate_regscale_object(regscale_ssp_id, "securityplans"):
        app.logger.warning("SSP #%i is not a valid RegScale Security Plan.", regscale_ssp_id)
        return
    json_files = list(Path(folder_path).glob("*.json"))
    csv_files = list(Path(folder_path).glob("*.csv"))
    ecr_files = json_files + csv_files
    if not scan_date or not FlatFileImporter.check_date_format(scan_date):
        scan_date = datetime.now()
    if not ecr_files:
        app.logger.warning("No ECR files found in %s", folder_path)
    from regscale.exceptions import ValidationException

    for file in ecr_files:
        try:
            ECR(
                name="ECR",
                file_path=str(file),
                parent_id=regscale_ssp_id,
                parent_module="securityplans",
                scan_date=scan_date,
                file_type=file.suffix,
                mappings_path=mappings_path,
                disable_mapping=disable_mapping,
            )
        except ValidationException as e:
            app.logger.error(e)
            continue
