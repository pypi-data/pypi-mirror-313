"""
Synqly Python SDK Ticketing Example

This example demonstrates how to use the Synqly Python SDK to create a
Ticketing Integration for a tenant.
"""

# Standard imports
import base64
import os
import tempfile
from datetime import datetime
from typing import Tuple, Optional

import click
from pathlib import Path
from synqly import engine, management as mgmt
from synqly.engine import CreateTicketRequest
from synqly.engine.resources.ticketing.types.priority import Priority
from synqly.engine.resources.ticketing.types.ticket import Ticket

import regscale.utils.synqly_utils as utils
from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.utils.app_utils import (
    create_progress_object,
    create_logger,
    get_current_datetime,
    convert_datetime_to_regscale_string,
    error_and_exit,
    check_file_path,
    compute_hashes_in_directory,
)
from regscale.utils.threading.threadhandler import create_threads, thread_assignment
from regscale.models import regscale_id, regscale_module, File
from regscale.models.regscale_models.issue import Issue

job_progress = create_progress_object()
logger = create_logger()
update_issues = []
new_regscale_issues = []
updated_regscale_issues = []
update_counter = []


@click.group()
def synqly():
    """
    Sync RegScale issues with Jira issues using Synqly
    """


def jira_provider_config(jira_url: str, jira_username: str, jira_token: str) -> mgmt.ProviderConfig_TicketingJira:
    """
    Helper method to construct a JIRA ProviderConfig object.

    :param str jira_url: JIRA URL
    :param str jira_username: JIRA username
    :param str jira_token: JIRA token
    :return: JIRA ProviderConfig object
    :rtype: mgmt.ProviderConfig_TicketingJira
    """
    return mgmt.ProviderConfig_TicketingJira(
        type="ticketing_jira",
        url=jira_url,
        credential=mgmt.JiraCredential_Basic(
            type="basic",
            username=jira_username,
            secret=jira_token,
        ),
    )


def download_issue_attachments_to_directory(
    directory: str,
    synqly_issue: Ticket,
    regscale_issue: Issue,
    api: Api,
    synqly_client: utils.Tenant,
) -> tuple[str, str]:
    """
    Function to download attachments from Jira and RegScale issues to a directory

    :param str directory: Directory to store the files in
    :param Ticket synqly_issue: Synqly issue to download the attachments for
    :param Issue regscale_issue: RegScale issue to download the attachments for
    :param Api api: Api object to use for interacting with RegScale
    :param utils.Tenant synqly_client: Synqly client to use for uploading attachments
    :return: Tuple of strings containing the Jira and RegScale directories
    :rtype: tuple[str, str]
    """
    # determine which attachments need to be uploaded to prevent duplicates by checking hashes
    jira_dir = os.path.join(directory, "jira")
    check_file_path(jira_dir, False)
    # download all attachments from Jira to the jira directory in temp_dir
    download_synqly_attachments(tenant=synqly_client, ticket_id=synqly_issue.id, download_dir=jira_dir)
    # get the regscale issue attachments
    regscale_issue_attachments = File.get_files_for_parent_from_regscale(
        api=api,
        parent_id=regscale_issue.id,
        parent_module="issues",
    )
    # create a directory for the regscale attachments
    regscale_dir = os.path.join(directory, "regscale")
    check_file_path(regscale_dir, False)
    # download regscale attachments to the directory
    for attachment in regscale_issue_attachments:
        with open(os.path.join(regscale_dir, attachment.trustedDisplayName), "wb") as file:
            file.write(
                File.download_file_from_regscale_to_memory(
                    api=api,
                    record_id=regscale_issue.id,
                    module="issues",
                    stored_name=attachment.trustedStorageName,
                    file_hash=(attachment.fileHash if attachment.fileHash else attachment.shaHash),
                )
            )
    return jira_dir, regscale_dir


def compare_files_for_dupes_and_upload(
    synqly_issue: Ticket, regscale_issue: Issue, synqly_client: utils.Tenant, api: Api
) -> None:
    """
    Compare attachments for provided Jira and RegScale issues via hash to prevent duplicates

    :param Ticket synqly_issue: Synqly issue object to compare attachments from
    :param Issue regscale_issue: RegScale issue object to compare attachments from
    :param utils.Tenant synqly_client: Jira client to use for uploading attachments
    :param Api api: RegScale API object to use for interacting with RegScale
    :rtype: None
    """
    jira_uploaded_attachments = []
    regscale_uploaded_attachments = []
    # create a temporary directory to store the downloaded attachments from Jira and RegScale
    with tempfile.TemporaryDirectory() as temp_dir:
        # write attachments to the temporary directory
        jira_dir, regscale_dir = download_issue_attachments_to_directory(
            directory=temp_dir,
            synqly_issue=synqly_issue,
            regscale_issue=regscale_issue,
            api=api,
            synqly_client=synqly_client,
        )
        # get the hashes for the attachments in the regscale and jira directories
        # iterate all files in the jira directory and compute their hashes
        jira_attachment_hashes = compute_hashes_in_directory(jira_dir)
        regscale_attachment_hashes = compute_hashes_in_directory(regscale_dir)

        # check where the files need to be uploaded to before uploading
        for file_hash, file in regscale_attachment_hashes.items():
            if file_hash not in jira_attachment_hashes:
                try:
                    upload_synqly_attachments(
                        tenant=synqly_client,
                        ticket_id=synqly_issue.id,
                        file_path=Path(file),
                    )
                    jira_uploaded_attachments.append(file)
                except TypeError as ex:
                    logger.error(
                        "Unable to upload %s to Jira issue %s.\nError: %s",
                        Path(file).name,
                        synqly_issue.id,
                        ex,
                    )
        for file_hash, file in jira_attachment_hashes.items():
            if file_hash not in regscale_attachment_hashes:
                with open(file, "rb") as in_file:
                    if File.upload_file_to_regscale(
                        file_name=f"Jira_attachment_{Path(file).name}",
                        parent_id=regscale_issue.id,
                        parent_module="issues",
                        api=api,
                        file_data=in_file.read(),
                    ):
                        regscale_uploaded_attachments.append(file)
                        logger.debug(
                            "Uploaded %s to RegScale issue #%i.",
                            Path(file).name,
                            regscale_issue.id,
                        )
                    else:
                        logger.warning(
                            "Unable to upload %s to RegScale issue #%i.",
                            Path(file).name,
                            regscale_issue.id,
                        )
    log_upload_results(regscale_uploaded_attachments, jira_uploaded_attachments, regscale_issue, synqly_issue)


def log_upload_results(
    regscale_uploaded_attachments: list, jira_uploaded_attachments: list, regscale_issue: Issue, synqly_issue: Ticket
) -> None:
    """
    Log the results of the upload process

    :param list regscale_uploaded_attachments: List of RegScale attachments that were uploaded
    :param list jira_uploaded_attachments: List of Jira attachments that were uploaded
    :param Issue regscale_issue: RegScale issue that the attachments were uploaded to
    :param Ticket synqly_issue: Jira issue that the attachments were uploaded to
    :rtype: None
    :return: None
    """
    if regscale_uploaded_attachments and jira_uploaded_attachments:
        logger.info(
            "%i file(s) uploaded to RegScale issue #%i and %i file(s) uploaded to Jira issue %s.",
            len(regscale_uploaded_attachments),
            regscale_issue.id,
            len(jira_uploaded_attachments),
            synqly_issue.id,
        )
    elif jira_uploaded_attachments:
        logger.info(
            "%i file(s) uploaded to Jira issue %s.",
            len(jira_uploaded_attachments),
            synqly_issue.id,
        )
    elif regscale_uploaded_attachments:
        logger.info(
            "%i file(s) uploaded to RegScale issue #%i.",
            len(regscale_uploaded_attachments),
            regscale_issue.id,
        )


def download_synqly_attachments(tenant: utils.Tenant, ticket_id: str, download_dir: str) -> int:
    """
    Downloads attachments from a ticket via Synqly

    :param utils.Tenant tenant: Synqly Tenant object
    :param str ticket_id: Ticket ID to download attachments from
    :param str download_dir: Directory to download attachments to
    :return: # of Synqly attachments downloaded
    :rtype: int
    """
    attachments = tenant.synqly_engine_client.ticketing.list_attachments_metadata(ticket_id)
    logger.debug("Found %i attachments for ticket %s", len(attachments.result), ticket_id)
    for attachment in attachments.result:
        download_response = tenant.synqly_engine_client.ticketing.download_attachment(
            ticket_id=ticket_id, attachment_id=attachment.id
        )
        output_path = os.path.join(download_dir, attachment.file_name)
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(download_response.result.content))
        logger.debug(
            "Downloaded attachment: %s and wrote its contents to %s",
            download_response.result.file_name,
            attachment.file_name,
        )
    return len(attachments.result)


def upload_synqly_attachments(tenant: utils.Tenant, ticket_id: str, file_path: Path) -> None:
    """
    Uploads an attachment to a ticket via Synqly

    :param utils.Tenant tenant: Synqly Tenant object
    :param str ticket_id: Ticket ID to attach the file to
    :param Path file_path: Path to the file to attach
    :rtype: None
    """
    with open(file_path, "rb") as file:
        content = base64.b64encode(file.read())
        logger.debug("Creating attachment for ticket %s", ticket_id)
        tenant.synqly_engine_client.ticketing.create_attachment(
            ticket_id=ticket_id,
            request=engine.CreateAttachmentRequest(
                file_name=file_path.name,
                content=content,
            ),
        )
    logger.info("Added an attachment to ticket %s", ticket_id)


def map_jira_issue_to_regscale_issue(synqly_issue: Ticket, parent_id: int, parent_module: str, config: dict) -> Issue:
    """
    Maps a JIRA issue to a RegScale issue

    :param Ticket synqly_issue: Synqly Ticket object
    :param int parent_id: Parent ID of the issue
    :param str parent_module: Parent module of the issue
    :param dict config: Configuration object
    :return: RegScale issue object
    :rtype: Issue
    """
    due_date = convert_datetime_to_regscale_string(synqly_issue.due_date)
    return Issue(
        title=synqly_issue.summary,
        severityLevel=Issue.assign_severity(synqly_issue.priority),
        issueOwnerId=config["userId"],
        dueDate=due_date,
        description=(f"Description {synqly_issue.description}\nStatus: {synqly_issue.status}\nDue Date: {due_date}"),
        status=("Closed" if synqly_issue.status.lower() == "done" else config["issues"]["jira"]["status"]),
        jiraId=synqly_issue.id,
        parentId=parent_id,
        parentModule=parent_module,
        dateCreated=get_current_datetime(),
        dateCompleted=(
            convert_datetime_to_regscale_string(synqly_issue.completion_date)
            if synqly_issue.status.lower() == "done"
            else None
        ),
    )


def map_regscale_issue_to_jira_issue(
    regscale_issue: Issue, jira_project_key: str, jira_username: str, issue_type: str
) -> CreateTicketRequest:
    """
    Maps a RegScale issue to a JIRA issue

    :param Issue regscale_issue: RegScale issue object
    :param str jira_project_key: Jira project key
    :param str jira_username: Username to use for creating issues in Jira
    :param str issue_type: Type of issue to create in Jira
    :return: Synqly CreateTicketRequest object
    :rtype: CreateTicketRequest
    """
    return engine.CreateTicketRequest(
        id=regscale_issue.title,
        name=regscale_issue.title,
        summary=f"{regscale_issue.description}\n\n{regscale_issue_fields_to_markdown(regscale_issue)}",
        project=jira_project_key,
        creator=jira_username,
        issue_type=issue_type,
        priority=map_regscale_severity_to_jira_priority(regscale_issue.severityLevel.lower()),
        status="To Do",
        due_date=datetime.strptime(regscale_issue.dueDate, "%Y-%m-%dT%H:%M:%S"),  # convert string to datetime
    )


def regscale_issue_fields_to_markdown(regscale_issue: Issue) -> str:
    """
    Converts a RegScale issue's fields to a Markdown string

    :param Issue regscale_issue: RegScale issue object
    :return: Markdown string of RegScale issue fields
    :rtype: str
    """
    regscale_issue_dict = regscale_issue.dict()
    markdown_table = "| RegScale Field | Value |\n| --- | --- |\n"
    for key in regscale_issue_dict:
        markdown_table += f"| {key} | {regscale_issue_dict[key]} |\n"
    return markdown_table


def map_regscale_severity_to_jira_priority(regscale_severity: str) -> Priority:
    """
    Map RegScale severity to OCSF priority

    :param str regscale_severity: RegScale severity
    :return: Jira priority
    :rtype: Priority
    """
    if "high" in regscale_severity.lower():
        return Priority.HIGH
    elif "moderate" in regscale_severity.lower():
        return Priority.MEDIUM
    else:
        return Priority.LOW


def background_job(
    synqly_app: utils.App,
    jira_project_key: str,
    jira_username: str,
    jira_issue_type: str,
    regscale_id: int,
    regscale_module: str,
    sync_attachments: bool = True,
) -> None:
    """
    Simulates a background process performing work on behalf of tenants.
    Iterates through all tenants and, for any tenant with a Synqly Engine
    Client defined, creates a new ticket. After a short delay,
    background_job will update the ticket's status to "Done".

    :param utils.App synqly_app: Synqly Application object
    :param str jira_project_key: Jira project key
    :param str jira_username: Username to use for creating issues in Jira
    :param str jira_issue_type: Type of issue to create in Jira
    :param int regscale_id: RegScale record ID Number to sync issues to
    :param str regscale_module: RegScale module to sync issues to
    :param bool sync_attachments: Flag to determine if attachments should be synced, defaults to True
    :rtype: None
    """
    # Iterate through each tenant and send an event to their Event Logger
    for tenant in synqly_app.tenants.values():
        # Skip tenants that don't have a Synqly Engine Client initialized
        if tenant.synqly_engine_client is None:
            continue

        regscale_issues = Issue.get_all_by_parent(regscale_id, regscale_module)
        logger.info("Found {} issues in RegScale".format(len(regscale_issues)))
        jira_issues: list[Issue] = []
        fetch_res = tenant.synqly_engine_client.ticketing.query_tickets(
            filter=f"project[eq]{jira_project_key}",
            limit=100,
        )
        jira_issues.extend(fetch_res.result)
        # check and handle pagination
        while int(fetch_res.cursor) == len(jira_issues):
            fetch_res = tenant.synqly_engine_client.ticketing.query_tickets(
                filter=f"project[eq]{jira_project_key}",
                limit=100,
                cursor=fetch_res.cursor,
            )
            jira_issues.extend(fetch_res.result)
        logger.info("Found {} issues in JIRA".format(len(jira_issues)))
        regscale_cli = Application()
        api = Api()
        (
            regscale_issues,
            regscale_attachments,
        ) = Issue.fetch_issues_and_attachments_by_parent(
            app=regscale_cli,
            parent_id=regscale_id,
            parent_module=regscale_module,
            fetch_attachments=sync_attachments,
        )

        if regscale_issues:
            # sync RegScale issues to Jira
            if issues_to_update := sync_regscale_to_jira(
                regscale_issues=regscale_issues,
                jira_client=tenant,
                jira_project=jira_project_key,
                jira_issue_type=jira_issue_type,
                jira_username=jira_username,
                sync_attachments=sync_attachments,
                attachments=regscale_attachments,
            ):
                with job_progress:
                    # create task to update RegScale issues
                    updating_issues = job_progress.add_task(
                        f"[#f8b737]Updating {len(issues_to_update)} RegScale issue(s) from Jira...",
                        total=len(issues_to_update),
                    )
                    # create threads to analyze Jira issues and RegScale issues
                    create_threads(
                        process=update_regscale_issues,
                        args=(
                            issues_to_update,
                            api,
                            updating_issues,
                        ),
                        thread_count=len(issues_to_update),
                    )
                    # output the final result
                    logger.info(
                        "%i/%i issue(s) updated in RegScale.",
                        len(issues_to_update),
                        len(update_counter),
                    )
        else:
            logger.info("No issues need to be updated in RegScale.")

        if jira_issues:
            # sync Jira issues to RegScale
            with job_progress:
                # create task to create RegScale issues
                creating_issues = job_progress.add_task(
                    f"[#f8b737]Analyzing {len(jira_issues)} Jira issue(s)"
                    f" and {len(regscale_issues)} RegScale issue(s)...",
                    total=len(jira_issues),
                )
                # create threads to analyze Jira issues and RegScale issues
                create_threads(
                    process=create_and_update_regscale_issues,
                    args=(
                        jira_issues,
                        regscale_issues,
                        sync_attachments,
                        regscale_cli,
                        regscale_id,
                        regscale_module,
                        tenant,
                        creating_issues,
                    ),
                    thread_count=len(jira_issues),
                )
                # output the final result
                logger.info(
                    "Analyzed %i Jira issue(s), created %i issue(s) and updated %i issue(s) in RegScale.",
                    len(jira_issues),
                    len(new_regscale_issues),
                    len(updated_regscale_issues),
                )
        else:
            logger.info("No issues need to be analyzed from Jira.")


def update_regscale_issues(args: Tuple, thread: int) -> None:
    """
    Function to compare Jira issues and RegScale issues

    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :rtype: None
    """
    # set up local variables from the passed args
    (
        regscale_issues,
        regscale_cli,
        task,
    ) = args
    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(regscale_issues))
    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        # set the issue for the thread for later use in the function
        issue = regscale_issues[threads[i]]
        # update the issue in RegScale
        Issue.update_issue(app=regscale_cli, issue=issue)
        logger.info(
            "RegScale Issue %i was updated with the Jira link.",
            issue.id,
        )
        update_counter.append(issue)
        # update progress bar
        job_progress.update(task, advance=1)


def get_synqly_attachment_count(tenant: utils.Tenant, ticket_id: str) -> int:
    """
    Get the number of attachments for a ticket in Synqly

    :param utils.Tenant tenant: Synqly Tenant object
    :param str ticket_id: Ticket ID to get the attachments for
    :return: Number of attachments for the ticket
    :rtype: int
    """
    try:
        attachments = tenant.synqly_engine_client.ticketing.list_attachments_metadata(ticket_id)
        return len(attachments.result)
    except Exception as ex:
        logger.error(f"Unable to get attachments for ticket {ticket_id}.\nError: {ex}")
        return 0


def create_and_update_regscale_issues(args: Tuple, thread: int) -> None:
    """
    Function to create or update issues in RegScale from Jira

    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :rtype: None
    """
    # set up local variables from the passed args
    (
        jira_issues,
        regscale_issues,
        add_attachments,
        regscale_cli,
        parent_id,
        parent_module,
        jira_client,
        task,
    ) = args
    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(jira_issues))

    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        jira_issue: Ticket = jira_issues[threads[i]]
        regscale_issue: Optional[Issue] = next(
            (issue for issue in regscale_issues if issue.jiraId == jira_issue.id), None
        )
        # see if the Jira issue needs to be created in RegScale
        if jira_issue.status.lower() == "done" and regscale_issue:
            # update the status and date completed of the RegScale issue
            regscale_issue.status = "Closed"
            regscale_issue.dateCompleted = get_current_datetime()
            # update the issue in RegScale
            updated_regscale_issues.append(Issue.update_issue(app=regscale_cli, issue=regscale_issue))
        elif regscale_issue:
            # update the issue in RegScale
            updated_regscale_issues.append(Issue.update_issue(app=regscale_cli, issue=regscale_issue))
        else:
            # map the jira issue to a RegScale issue object
            issue = map_jira_issue_to_regscale_issue(
                synqly_issue=jira_issue,
                config=regscale_cli.config,
                parent_id=parent_id,
                parent_module=parent_module,
            )
            # create the issue in RegScale
            if regscale_issue := Issue.insert_issue(
                app=regscale_cli,
                issue=issue,
            ):
                if regscale_issue.id:
                    logger.debug(
                        "Created issue #%i-%s in RegScale.",
                        regscale_issue.id,
                        regscale_issue.title,
                    )
                else:
                    logger.warning("Unable to create issue in RegScale.\nIssue: %s", issue.dict())
                new_regscale_issues.append(regscale_issue)
        handle_attachments(
            add_attachments=add_attachments,
            regscale_issue=regscale_issue,
            jira_client=jira_client,
            jira_issue=jira_issue,
        )
        # update progress bar
        job_progress.update(task, advance=1)


def handle_attachments(
    add_attachments: bool, regscale_issue: Issue, jira_client: utils.Tenant, jira_issue: Ticket
) -> None:
    """
    Handle attachments for Jira and RegScale issues

    :param bool add_attachments: Flag to determine if attachments should be added to the issue
    :param Issue regscale_issue: RegScale issue object
    :param utils.Tenant jira_client: Jira client to use for issue creation in Jira
    :param Ticket jira_issue: Jira issue object
    :rtype: None
    """
    if add_attachments and regscale_issue:
        # check if the jira issue has attachments
        attachment_count = get_synqly_attachment_count(jira_client, jira_issue.id)
        if attachment_count > 0:
            # determine which attachments need to be uploaded to prevent duplicates by
            # getting the hashes of all Jira & RegScale attachments
            compare_files_for_dupes_and_upload(
                synqly_issue=jira_issue,
                regscale_issue=regscale_issue,
                synqly_client=jira_client,
                api=Api(),
            )


def sync_regscale_to_jira(
    regscale_issues: list[Issue],
    jira_client: utils.Tenant,
    jira_project: str,
    jira_issue_type: str,
    jira_username: str,
    sync_attachments: bool = True,
    attachments: Optional[dict] = None,
) -> list[Issue]:
    """
    Sync issues from RegScale to Jira

    :param list[Issue] regscale_issues: list of RegScale issues to sync to Jira
    :param utils.Tenant jira_client: Jira client to use for issue creation in Jira
    :param str jira_project: Jira Project to create the issues in
    :param str jira_issue_type: Type of issue to create in Jira
    :param str jira_username: Username to use for creating issues in Jira
    :param bool sync_attachments: Flag to determine if attachments should be synced, defaults to True
    :param Optional[dict] attachments: Dictionary of attachments to sync, defaults to None
    :return: list of RegScale issues that need to be updated
    :rtype: list[Issue]
    """
    new_issue_counter = 0
    issuess_to_update = []
    for issue in regscale_issues:
        # see if Jira issue already exists
        if not issue.jiraId or issue.jiraId == "":
            new_issue = create_issue_in_jira(
                issue=issue,
                jira_client=jira_client,
                jira_project=jira_project,
                issue_type=jira_issue_type,
                jira_username=jira_username,
                add_attachments=sync_attachments,
                attachments=attachments,
            )
            if not new_issue:
                continue
            # log progress
            new_issue_counter += 1
            # get the Jira ID
            jira_id = new_issue.id
            # update the RegScale issue for the Jira link
            issue.jiraId = jira_id
            # add the issue to the update_issues global list
            issuess_to_update.append(issue)
    # output the final result
    logger.info("%i new issue(s) opened in Jira.", new_issue_counter)
    return issuess_to_update


def create_issue_in_jira(
    issue: Issue,
    jira_client: utils.Tenant,
    jira_project: str,
    issue_type: str,
    jira_username: str,
    add_attachments: Optional[bool] = False,
    attachments: list[File] = None,
    api: Optional[Api] = None,
) -> Optional[Ticket]:
    """
    Create a new issue in Jira

    :param Issue issue: RegScale issue object
    :param utils.Tenant jira_client: Jira client to use for issue creation in Jira
    :param str jira_project: Project name in Jira to create the issue in
    :param str issue_type: The type of issue to create in Jira
    :param str jira_username: Username to use for creating issues in Jira
    :param Optional[bool] add_attachments: Flag to determine if attachments should be added to the issue
    :param list[File] attachments: List of attachments to add to the issue
    :param Optional[Api] api: RegScale API object to use for interacting with RegScale
    :return: Newly created issue in Jira
    :rtype: Optional[Ticket]
    """
    try:
        new_issue = map_regscale_issue_to_jira_issue(issue, jira_project, jira_username, issue_type)
        create_response = jira_client.synqly_engine_client.ticketing.create_ticket(request=new_issue)
    except Exception as ex:
        logger.error(f"Unable to create Jira issue.\nError: {ex}")
        return None
        # error_and_exit(f"Unable to create Jira issue.\nError: {ex}")
    if add_attachments and attachments:
        if not api:
            api = Api()
        compare_files_for_dupes_and_upload(
            synqly_issue=create_response.result.Ticket,
            regscale_issue=issue,
            synqly_client=jira_client,
            api=Api(),
        )
    logger.info("Created ticket: {}".format(create_response.result.name))
    return create_response.result


@synqly.command(name="sync_jira")
@regscale_id()
@regscale_module()
@click.option(
    "--jira_project",
    type=click.STRING,
    help="RegScale will sync the issues for the record to the Jira project.",
    prompt="Enter the name of the project in Jira",
    required=True,
)
@click.option(
    "--jira_issue_type",
    type=click.STRING,
    help="Enter the Jira issue type to use when creating new issues from RegScale. (CASE SENSITIVE)",
    prompt="Enter the Jira issue type",
    required=True,
)
@click.option(
    "--sync_attachments",
    type=click.BOOL,
    help=(
        "Whether RegScale will sync the attachments for the issue "
        "in the provided Jira project and vice versa. Defaults to True."
    ),
    required=False,
    default=True,
)
def sync_jira(
    regscale_id: int, regscale_module: str, jira_project: str, jira_issue_type: str, sync_attachments: bool = True
):
    """
    Parses command line arguments for this example.
    """
    sync_with_jira(
        regscale_id,
        regscale_module,
        jira_project,
        jira_issue_type,
        sync_attachments,
    )


def sync_with_jira(
    regscale_id: int, regscale_module: str, jira_project_key: str, jira_issue_type: str, sync_attachments: bool = True
) -> None:
    """
    Syncs RegScale issues with Jira issues using Synqly

    :param int regscale_id: RegScale record ID Number to sync issues to
    :param str regscale_module: RegScale module to sync issues to
    :param str jira_project_key: Jira project key
    :param str jira_issue_type: Type of issue to create in Jira
    :param bool sync_attachments: Flag to determine if attachments should be synced, defaults to True
    :raises Exception: If an error occurs during the sync process
    :rtype: None
    """
    # Initialize an empty application to store our simulated tenants
    synqly = utils.App("ticketing")
    app = Application()
    synqly_access_token = os.getenv("SYNQLY_ACCESS_TOKEN") or app.config["synqlyAccessToken"]
    jira_url = os.getenv("JIRA_URL") or app.config["jiraUrl"]
    jira_username = os.getenv("JIRA_USERNAME") or app.config["jiraUserName"]
    jira_token = os.getenv("JIRA_API_TOKEN") or app.config["jiraApiToken"]
    if (
        not jira_url
        or not jira_username
        or not jira_token
        or not synqly_access_token
        or synqly_access_token == app.template["synqlyAccessToken"]
        or jira_url == app.template["jiraUrl"]
        or jira_username == app.template["jiraUserName"]
        or jira_token == app.template["jiraApiToken"]
    ):
        error_and_exit(
            "jiraUrl, jiraUserName, and jiraApiToken are required. Please provide them in the environment or init.yaml."
        )
    # Initialize tenants within our Application
    try:
        synqly.new_tenant(synqly_access_token, "RegScale-CLI")
        app.logger.debug("RegScale-CLI created")
    except Exception as e:
        app.logger.error("Error creating Tenant RegScale-CLI:" + str(e))
        synqly._cleanup_handler()
        raise e

    # Configure a ticketing integration based on the configuration. If no jira credentials
    # are provided, then mock ticket provider is used
    provider_config: mgmt.ProviderConfig = jira_provider_config(jira_url, jira_username, jira_token)

    # Configure a mock integration for tenant ABC and a JIRA Integration for Tenant XYZ
    try:
        synqly.configure_integration("RegScale-CLI", provider_config)
    except Exception as e:
        print("Error configuring provider integration for Tenant RegScale-CLI: " + str(e))
        synqly._cleanup_handler()
        raise e

    # Start a background job to generate data
    try:
        background_job(
            synqly, jira_project_key, jira_username, jira_issue_type, regscale_id, regscale_module, sync_attachments
        )
    except Exception as e:
        print("Error running background job: " + str(e))
        synqly._cleanup_handler()
        raise e

    synqly._cleanup_handler()
