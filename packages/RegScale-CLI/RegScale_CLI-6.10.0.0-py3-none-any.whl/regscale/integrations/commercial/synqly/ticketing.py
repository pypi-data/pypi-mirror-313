# flake8: noqa E501
# pylint: disable=line-too-long

"""Ticketing connector commands for the RegScale CLI"""

import click
from regscale.models import regscale_id, regscale_module
from regscale.models.integration_models.synqly_models.connectors import Ticketing


@click.group()
def ticketing() -> None:
    """Ticketing connector commands for the RegScale CLI"""
    pass


@ticketing.command(name="sync_jira")
@regscale_id()
@regscale_module()
@click.option(
    "--issue_type",
    type=click.STRING,
    help="jira issue type",
    required=True,
    prompt="jira issue type",
)
@click.option(
    "--project",
    type=click.STRING,
    help="jira project",
    required=True,
    prompt="jira project",
)
@click.option(
    "--default_project",
    type=click.STRING,
    help="Default Project for the integration.",
    required=False,
)
@click.option(
    "--sync_attachments",
    type=click.BOOL,
    help="Whether to sync attachments between jira and RegScale",
    required=False,
    default=True,
)
def sync_jira(
    regscale_id: int, regscale_module: str, issue_type: str, project: str, default_project: str, sync_attachments: bool
) -> None:
    """Sync data Ticketing between jira and RegScale."""
    ticketing_jira = Ticketing("jira")
    ticketing_jira.run_sync(
        regscale_id=regscale_id,
        regscale_module=regscale_module,
        issue_type=issue_type,
        project=project,
        default_project=default_project,
        sync_attachments=sync_attachments,
    )


@ticketing.command(name="sync_pagerduty")
@regscale_id()
@regscale_module()
@click.option(
    "--project",
    type=click.STRING,
    help="pagerduty project",
    required=True,
    prompt="pagerduty project",
)
@click.option(
    "--name",
    type=click.STRING,
    help="pagerduty name",
    required=True,
    prompt="pagerduty name",
)
def sync_pagerduty(regscale_id: int, regscale_module: str, project: str, name: str) -> None:
    """Sync data Ticketing between pagerduty and RegScale."""
    ticketing_pagerduty = Ticketing("pagerduty")
    ticketing_pagerduty.run_sync(regscale_id=regscale_id, regscale_module=regscale_module, project=project, name=name)


@ticketing.command(name="sync_servicenow")
@regscale_id()
@regscale_module()
@click.option(
    "--issue_type",
    type=click.STRING,
    help="servicenow issue type",
    required=True,
    prompt="servicenow issue type",
)
@click.option(
    "--default_project",
    type=click.STRING,
    help="Default Project for the integration. This maps to the custom table for tickets. This table should be derived from Incident table. If not provided, defaults to the incident table.",
    required=False,
)
def sync_servicenow(regscale_id: int, regscale_module: str, issue_type: str, default_project: str) -> None:
    """Sync data Ticketing between servicenow and RegScale."""
    ticketing_servicenow = Ticketing("servicenow")
    ticketing_servicenow.run_sync(
        regscale_id=regscale_id, regscale_module=regscale_module, issue_type=issue_type, default_project=default_project
    )


@ticketing.command(name="sync_torq")
@regscale_id()
@regscale_module()
@click.option(
    "--name",
    type=click.STRING,
    help="torq name",
    required=True,
    prompt="torq name",
)
def sync_torq(regscale_id: int, regscale_module: str, name: str) -> None:
    """Sync data Ticketing between torq and RegScale."""
    ticketing_torq = Ticketing("torq")
    ticketing_torq.run_sync(regscale_id=regscale_id, regscale_module=regscale_module, name=name)


# pylint: enable=line-too-long
