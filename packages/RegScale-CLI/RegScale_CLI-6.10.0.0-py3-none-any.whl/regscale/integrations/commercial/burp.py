#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Burp Scanner RegScale integration"""
from pathlib import Path

import click

from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.models.integration_models.burp import Burp
from regscale.models.integration_models.flat_file_importer import FlatFileIntegration

logger = create_logger(__name__)


# Create group to handle Burp .xml file processing
@click.group()
def burp():
    """Performs actions on Burp Scanner artifacts."""


@burp.command(name="import_burp")
@click.option(
    "--folder_path",
    help="File path to the folder containing Burp files to process to RegScale.",
    prompt="File path for Burp files",
    type=click.Path(exists=True, dir_okay=True, resolve_path=True),
)
@click.option(
    "--regscale_ssp_id",
    type=click.INT,
    help="The ID number from RegScale of the System Security Plan.",
    prompt="Enter RegScale System Security Plan ID",
    required=True,
)
@click.option(
    "--scan_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="The the scan date of the file.",
    required=False,
)
def import_burp(folder_path: click.Path, regscale_ssp_id: click.INT, scan_date: click.DateTime):
    """
    Import Burp scans, vulnerabilities and assets to RegScale from burp files

    """
    app = Application()
    if len(list(Path(folder_path).glob("*.xml"))) == 0:
        logger.warning("No Burp files found in the specified folder.")
        return
    for file in Path(folder_path).glob("*.xml"):
        burp = Burp(app, file, parentId=regscale_ssp_id, parentModule="securityplans")
        flat_int = FlatFileIntegration(plan_id=regscale_ssp_id)
        flat_int.num_findings_to_process = burp.num_findings
        flat_int.num_assets_to_process = burp.num_assets
        flat_int.sync_assets(
            plan_id=regscale_ssp_id,
            integration_assets=burp.integration_assets,
            title="Burp Suite",
        )
        flat_int.sync_findings(
            plan_id=regscale_ssp_id,
            integration_findings=burp.integration_findings,
            title="Burp Suite",
            enable_finding_date_update=True,
            scan_date=scan_date,
        )
        burp.move_files()
