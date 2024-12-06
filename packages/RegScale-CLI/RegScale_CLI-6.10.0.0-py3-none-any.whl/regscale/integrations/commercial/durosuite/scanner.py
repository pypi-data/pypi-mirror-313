#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RegScale DuroSuite Package

This module provides functionality for integrating DuroSuite with RegScale,
including syncing findings, assets, and performing scans.
"""
import logging
import tempfile
import time
from typing import Optional

import click

from regscale.integrations.commercial.durosuite import api
from regscale.integrations.commercial.durosuite.variables import DuroSuiteVariables
from regscale.integrations.commercial.stigv2 import StigIntegration

logger = logging.getLogger("rich")


@click.group()
def durosuite():
    """DuroSuite Integrations"""


@durosuite.command(name="scan")
@click.option(
    "-p",
    "--regscale_ssp_id",
    type=click.INT,
    help="The ID number from RegScale of the System Security Plan",
    prompt="Enter RegScale System Security Plan ID",
    required=True,
)
def scan(regscale_ssp_id):
    """
    Scan DuroSuite.

    This function initiates a scan in DuroSuite and syncs the results to RegScale.
    """
    durosuite_scan(regscale_ssp_id=regscale_ssp_id)


@durosuite.command(name="import_audit")
@click.option(
    "-p",
    "--regscale_ssp_id",
    type=click.INT,
    help="The ID number from RegScale of the System Security Plan",
    prompt="Enter RegScale System Security Plan ID",
    required=True,
)
@click.option(
    "-a",
    "--audit_id",
    type=click.INT,
    help="The ID of the DuroSuite audit to import",
    prompt="Enter DuroSuite Audit ID",
    required=True,
)
def cli_import_audit(audit_id: int, regscale_ssp_id: int) -> None:
    """
    Import a specific DuroSuite audit and sync it to RegScale.

    This function imports a specific audit from DuroSuite and syncs it to RegScale.

    :param int audit_id: The ID of the DuroSuite audit to import.
    :param int regscale_ssp_id: RegScale System Security Plan ID.
    """
    import_audit(audit_id, regscale_ssp_id)


def durosuite_scan(device_name="Ubuntu Server", os_id=95, regscale_ssp_id=7) -> None:
    """
    Perform a DuroSuite scan and import the results to RegScale.

    :param str device_name: Name of the device to scan. Defaults to "Ubuntu Server".
    :param int os_id: ID of the operating system. Defaults to 95.
    :param int regscale_ssp_id: RegScale System Security Plan ID. Defaults to 7.
    """
    base_url = DuroSuiteVariables.duroSuiteURL
    username = DuroSuiteVariables.duroSuiteUser
    password = DuroSuiteVariables.duroSuitePassword

    ds = api.DuroSuite(base_url, username, password)
    groups = [group for group in ds.get_groups() if group.os_id == os_id]
    if any(groups):
        group = groups[0]
        device = api.Device(group_id=group.id, name=device_name, os_id=os_id)  # type: ignore
        logger.info(f"DeviceData: {device.model_dump()}")

        # Create a new device and variable
        if not (created_device := ds.add_new_device(device)) or not created_device.id:
            from regscale.core.app.utils.app_utils import error_and_exit

            error_and_exit("Failed to create device")
        logger.info(f"Device created: {device}")
        var = api.Var(
            device_id=created_device.id, name="ansible_host", value=DuroSuiteVariables.duroSuiteDemoHost
        )  # type: ignore
        created_var = ds.add_new_device_variable(var)
        if created_var:
            logger.info(f"Var created: {created_var}")
        else:
            logger.error("Failed to create variable")

        # Get STIGs and perform audits
        stigs = ds.get_stigs_by_os_id(os_id=os_id)
        logger.info(f"STIGS: {stigs}")
        for stig in stigs:
            for template in ds.get_template_ids_by_group(group_id=group.id):
                audit_response = ds.audit_device(
                    device_id=created_device.id, group_id=group.id, playbook_id=stig.id, template_id=template.id
                )
                logger.info(f"Queued Audit: {audit_response}")

                # Import the audit results
                import_audit(audit_response.audit_id, regscale_ssp_id)


def import_audit(audit_id: int, regscale_ssp_id: int) -> None:
    """
    Import a DuroSuite audit and sync it to RegScale.

    :param int audit_id: The ID of the DuroSuite audit to import.
    :param int regscale_ssp_id: The RegScale System Security Plan ID.

    :raises TimeoutError: If the checklist file is not available after maximum attempts.
    :raises Exception: For any other errors during the import process.
    """
    base_url = DuroSuiteVariables.duroSuiteURL
    username = DuroSuiteVariables.duroSuiteUser
    password = DuroSuiteVariables.duroSuitePassword

    ds = api.DuroSuite(base_url, username, password)

    try:
        # Wait for the audit to complete
        finished = False
        while not finished:
            response = ds.get_audit_record(audit_id=audit_id)
            if response:
                logger.info(f"Audit Status for {audit_id}: {response['status']}")
                if response["status"].lower() == "complete":
                    finished = True
            time.sleep(5)

        # Retrieve the checklist file
        checklist_file: Optional[str] = None
        attempts = 0
        max_attempts = 12  # 1 minute total wait time
        while not checklist_file and attempts < max_attempts:
            logger.info(f"Waiting for checklist file for {audit_id}")
            checklist_file = ds.get_checklist_file_by_audit_id(audit_id)
            time.sleep(5)
            attempts += 1

        if not checklist_file:
            raise TimeoutError(f"Timed out waiting for checklist file for audit {audit_id}")

        # Process the checklist file
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".ckl", delete=True) as tmp_file:
            tmp_file.write(checklist_file)
            tmp_file_path = tmp_file.name

            # Sync the assets and findings
            StigIntegration.sync_assets(plan_id=regscale_ssp_id, path=tmp_file_path)  # type: ignore
            StigIntegration.sync_findings(plan_id=regscale_ssp_id, path=tmp_file_path)  # type: ignore

    except Exception as e:
        logger.error(f"Error importing audit {audit_id}: {str(e)}", exc_info=True)
        raise
