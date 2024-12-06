#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Jira integration for RegScale CLI """

# Standard python imports
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from typing import Any, Optional, Tuple, TYPE_CHECKING, Union
from urllib.parse import urljoin

if TYPE_CHECKING:
    from regscale.core.app.application import Application

import click
from jira import JIRA
from jira import Issue as jiraIssue
from jira import JIRAError
from rich.progress import Progress

from regscale.core.app.api import Api
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import (
    check_file_path,
    check_license,
    compute_hashes_in_directory,
    convert_datetime_to_regscale_string,
    create_progress_object,
    error_and_exit,
    get_current_datetime,
    save_data_to,
)
from regscale.core.app.utils.regscale_utils import verify_provided_module
from regscale.utils.threading.threadhandler import create_threads, thread_assignment
from regscale.models import regscale_id, regscale_module
from regscale.models.regscale_models.file import File
from regscale.models.regscale_models.issue import Issue
from regscale.models.regscale_models.task import Task

job_progress = create_progress_object()
logger = create_logger()
update_issues = []
new_regscale_issues = []
updated_regscale_issues = []
update_counter = []


####################################################################################################
#
# PROCESS ISSUES TO JIRA
# JIRA CLI Python Docs: https://jira.readthedocs.io/examples.html#issues
# JIRA API Docs: https://developer.atlassian.com/server/jira/platform/jira-rest-api-examples/
#
####################################################################################################


# Create group to handle Jira integration
@click.group()
def jira():
    """Sync issues between Jira and RegScale."""


@jira.command()
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
def issues(
    regscale_id: int,
    regscale_module: str,
    jira_project: str,
    jira_issue_type: str,
    sync_attachments: bool = True,
):
    """Sync issues from Jira into RegScale."""
    sync_regscale_and_jira(
        parent_id=regscale_id,
        parent_module=regscale_module,
        jira_project=jira_project,
        jira_issue_type=jira_issue_type,
        sync_attachments=sync_attachments,
    )


@jira.command()
@regscale_id()
@regscale_module()
@click.option(
    "--jira_project",
    type=click.STRING,
    help="RegScale will sync the issues for the record to the Jira project.",
    prompt="Enter the name of the project in Jira",
    required=True,
)
def tasks(
    regscale_id: int,
    regscale_module: str,
    jira_project: str,
):
    """Sync tasks from Jira into RegScale."""
    sync_regscale_and_jira(
        parent_id=regscale_id,
        parent_module=regscale_module,
        jira_project=jira_project,
        jira_issue_type="Task",
        sync_attachments=False,
        sync_tasks_only=True,
    )


def sync_regscale_and_jira(
    parent_id: int,
    parent_module: str,
    jira_project: str,
    jira_issue_type: str,
    sync_attachments: bool = True,
    sync_tasks_only: bool = False,
) -> None:
    """
    Sync issues, bidirectionally, from Jira into RegScale as issues

    :param int parent_id: ID # from RegScale to associate issues with
    :param str parent_module: RegScale module to associate issues with
    :param str jira_project: Name of the project in Jira
    :param str jira_issue_type: Type of issues to sync from Jira
    :param bool sync_attachments: Whether to sync attachments in RegScale & Jira, defaults to True
    :param bool sync_tasks_only: Whether to sync only tasks from Jira, defaults to False
    :rtype: None
    """
    app = check_license()
    api = Api()
    config = app.config

    # see if provided RegScale Module is an accepted option
    verify_provided_module(parent_module)

    # create Jira client
    jira_client = create_jira_client(config)

    if sync_tasks_only:
        jql_str = f"project = {jira_project} AND issueType = {jira_issue_type}"
        regscale_issues = Task.get_all_by_parent(parent_id, parent_module)
        regscale_attachments = []
    else:
        jql_str = f"project = {jira_project}"
        (
            regscale_issues,
            regscale_attachments,
        ) = Issue.fetch_issues_and_attachments_by_parent(
            parent_id=parent_id,
            parent_module=parent_module,
            fetch_attachments=sync_attachments,
        )

    jira_objects = fetch_jira_objects(
        jira_client=jira_client,
        jira_project=jira_project,
        jql_str=jql_str,
        jira_issue_type=jira_issue_type,
        sync_tasks_only=sync_tasks_only,
    )

    if regscale_issues and not sync_tasks_only:
        # sync RegScale issues to Jira
        if issues_to_update := sync_regscale_to_jira(
            regscale_issues=regscale_issues,
            jira_client=jira_client,
            jira_project=jira_project,
            jira_issue_type=jira_issue_type,
            api=api,
            sync_attachments=sync_attachments,
            attachments=regscale_attachments,
        ):
            with job_progress:
                # create task to update RegScale issues
                updating_issues = job_progress.add_task(
                    f"[#f8b737]Updating {len(issues_to_update)} RegScale {jira_issue_type.lower()}(s) from Jira...",
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
    elif not sync_tasks_only:
        logger.info("No issues need to be updated in RegScale.")

    if jira_objects:
        sync_regscale_objects_to_jira(
            jira_objects, regscale_issues, sync_attachments, app, parent_id, parent_module, sync_tasks_only
        )
    else:
        logger.info(f"No {'tasks' if sync_tasks_only else 'issues'} need to be analyzed from Jira.")


def sync_regscale_objects_to_jira(
    jira_issues: list[jiraIssue],
    regscale_objects: list[Union[Issue, Task]],
    sync_attachments: bool,
    app: "Application",
    parent_id: int,
    parent_module: str,
    sync_tasks_only: bool,
):
    """
    Sync issues from Jira to RegScale

    :param list[jiraIssue] jira_issues: List of Jira issues to sync to RegScale
    :param list[Union[Issue, Task]] regscale_objects: List of RegScale issues or tasks to compare to Jira issues
    :param bool sync_attachments: Sync attachments from Jira to RegScale, defaults to True
    :param Application app: RegScale CLI application object
    :param int parent_id: Parent record ID in RegScale
    :param str parent_module: Parent record module in RegScale
    :param bool sync_tasks_only: Whether to sync only tasks from Jira
    """
    issues_closed = []
    with job_progress:
        type_str = "task" if sync_tasks_only else "issue"
        creating_issues = job_progress.add_task(
            f"[#f8b737]Comparing {len(jira_issues)} Jira {type_str}(s)"
            f" and {len(regscale_objects)} RegScale {type_str}(s)...",
            total=len(jira_issues),
        )
        jira_client = create_jira_client(app.config)
        if sync_tasks_only:
            tasks_inserted, tasks_updated, tasks_closed = create_and_update_regscale_tasks(
                jira_issues=jira_issues,
                existing_tasks=regscale_objects,
                parent_id=parent_id,
                parent_module=parent_module,
                progress=job_progress,
                progress_task=creating_issues,
            )
        else:
            create_threads(
                process=create_and_update_regscale_issues,
                args=(
                    jira_issues,
                    regscale_objects,
                    sync_attachments,
                    jira_client,
                    app,
                    parent_id,
                    parent_module,
                    creating_issues,
                    job_progress,
                ),
                thread_count=len(jira_issues),
            )
        logger.info(
            "Analyzed %i Jira %s(s), created %i %s(s), updated %i %s(s), and closed %i %s(s) in RegScale.",
            len(jira_issues),
            type_str,
            len(new_regscale_issues) if not sync_tasks_only else tasks_inserted,
            type_str,
            len(updated_regscale_issues) if not sync_tasks_only else tasks_updated,
            type_str,
            len(issues_closed) if not sync_tasks_only else tasks_closed,
            type_str,
        )


def create_jira_client(
    config: dict,
) -> JIRA:
    """
    Create a Jira client to use for interacting with Jira

    :param dict config: RegScale CLI application config
    :return: JIRA Client
    :rtype: JIRA
    """
    url = config["jiraUrl"]
    token = config["jiraApiToken"]
    jira_user = config["jiraUserName"]

    # set the JIRA Url
    return JIRA(basic_auth=(jira_user, token), options={"server": url})


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
        app,
        task,
    ) = args
    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(regscale_issues))
    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        # set the issue for the thread for later use in the function
        issue = regscale_issues[threads[i]]
        # update the issue in RegScale
        issue.save()
        logger.debug(
            "RegScale Issue %i was updated with the Jira link.",
            issue.id,
        )
        update_counter.append(issue)
        # update progress bar
        job_progress.update(task, advance=1)


def convert_task_status(name: str) -> str:
    """
    Convert the task status from Jira to RegScale

    :param str name: Name of the task status in Jira
    :return: Name of the task status in RegScale
    :rtype: str
    """
    jira_regscale_map = {
        "to do": "Backlog",
        "in progress": "Open",
        "done": "Closed",
        "closed": "Closed",
        "cancelled": "Cancelled",
        "canceled": "Cancelled",
    }
    return jira_regscale_map.get(name.lower(), "Open")


def create_regscale_task_from_jira(config: dict, jira_issue: jiraIssue, parent_id: int, parent_module: str) -> Task:
    """
    Function to create a Task object from a Jira issue

    :param dict config: Application config
    :param jiraIssue jira_issue: Jira issue to create a Task object from
    :param int parent_id: Parent record ID in RegScale
    :param str parent_module: Parent record module in RegScale
    :return: RegScale Task object
    :rtype: Task
    """
    description = jira_issue.fields.description
    due_date = jira_issue.fields.duedate
    status = convert_task_status(jira_issue.fields.status.name)
    status_change_date = convert_datetime_to_regscale_string(
        datetime.strptime(jira_issue.fields.statuscategorychangedate, "%Y-%m-%dT%H:%M:%S.%f%z")
    )
    title = jira_issue.fields.summary
    date_closed = None
    percent_complete = None
    if not due_date:
        delta = config["issues"]["jira"]["medium"]
        due_date = convert_datetime_to_regscale_string(datetime.now() + timedelta(days=delta))
    if status == "Closed":
        date_closed = status_change_date
        percent_complete = 100

    return Task(
        title=title,
        status=status,
        description=description,
        dueDate=due_date,
        parentId=parent_id,
        parentModule=parent_module,
        dateClosed=date_closed,
        percentComplete=percent_complete,
        otherIdentifier=jira_issue.key,
    )


def check_and_close_tasks(existing_tasks: list[Task], all_jira_titles: set[str]) -> list[Task]:
    """
    Function to check and close tasks that are not in Jira

    :param list[Task] existing_tasks: List of existing tasks in RegScale
    :param set[str] all_jira_titles: Set of all Jira task titles
    :return: List of tasks to close
    :rtype: list[Task]
    """
    close_tasks = []
    for task in existing_tasks:
        if task.title not in all_jira_titles and task.status != "Closed":
            task.status = "Closed"
            task.percentComplete = 100
            task.dateClosed = get_current_datetime()
            close_tasks.append(task)
    return close_tasks


def create_and_update_regscale_tasks(
    jira_issues: list[jiraIssue],
    existing_tasks: list[Task],
    parent_id: int,
    parent_module: str,
    progress: Progress,
    progress_task: Any,
) -> tuple[int, int, int]:
    """
    Function to create or update Tasks in RegScale from Jira

    :param list[jiraIssue] jira_issues: List of Jira issues to create or update in RegScale
    :param list[Task] existing_tasks: List of existing tasks in RegScale
    :param int parent_id: Parent record ID in RegScale
    :param str parent_module: Parent record module in RegScale
    :param Progress progress: Job progress object to use for updating the progress bar
    :param Any progress_task: Task object to update the progress bar
    :return: A tuple of counts
    :rtype: tuple[int, int, int]
    """
    from regscale.core.app.application import Application

    app = Application()
    config = app.config
    insert_tasks = []
    update_tasks = []
    all_jira_titles = {jira_issue.fields.summary for jira_issue in jira_issues}
    for jira_issue in jira_issues:
        task = create_regscale_task_from_jira(config, jira_issue, parent_id, parent_module)
        if task not in existing_tasks:
            # set due date to today if not provided
            insert_tasks.append(task)
        else:
            existing_task = next((t for t in existing_tasks if t == task), None)
            task.id = existing_task.id
            update_tasks.append(task)
        progress.update(progress_task, advance=1)
    close_tasks = check_and_close_tasks(existing_tasks, all_jira_titles)

    with progress:
        with ThreadPoolExecutor(max_workers=10) as executor:
            if insert_tasks:
                creating_tasks = progress.add_task(
                    f"[#f8b737]Creating {len(insert_tasks)} task(s) in RegScale...",
                    total=len(insert_tasks),
                )
                create_futures = {executor.submit(task.create) for task in insert_tasks}
                for _ in as_completed(create_futures):
                    progress.update(creating_tasks, advance=1)
            if update_tasks:
                update_task = progress.add_task(
                    f"[#f8b737]Updating {len(update_tasks)} task(s) in RegScale...",
                    total=len(update_tasks),
                )
                update_futures = {executor.submit(task.save) for task in update_tasks}
                for _ in as_completed(update_futures):
                    progress.update(update_task, advance=1)
            if close_tasks:
                closing_tasks = progress.add_task(
                    f"[#f8b737]Closing {len(close_tasks)} task(s) in RegScale...",
                    total=len(close_tasks),
                )
                close_futures = {executor.submit(task.save) for task in close_tasks}
                for _ in as_completed(close_futures):
                    progress.update(closing_tasks, advance=1)
    return len(insert_tasks), len(update_tasks), len(close_tasks)


def create_and_update_regscale_issues(args: Tuple, thread: int) -> None:
    """
    Function to create or update issues in RegScale from Jira

    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :rtype: None
    """
    # set up local variables from the passed args
    (jira_issues, regscale_issues, add_attachments, jira_client, app, parent_id, parent_module, task, progress) = args
    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(jira_issues))

    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        jira_issue: jiraIssue = jira_issues[threads[i]]
        regscale_issue: Optional[Issue] = next(
            (issue for issue in regscale_issues if issue.jiraId == jira_issue.key), None
        )
        # see if the Jira issue needs to be created in RegScale
        if jira_issue.fields.status.name.lower() == "done" and regscale_issue:
            # update the status and date completed of the RegScale issue
            regscale_issue.status = "Closed"
            regscale_issue.dateCompleted = get_current_datetime()
            # update the issue in RegScale
            updated_regscale_issues.append(Issue.update_issue(app=app, issue=regscale_issue))
        elif regscale_issue:
            # update the issue in RegScale
            updated_regscale_issues.append(Issue.update_issue(app=app, issue=regscale_issue))
        else:
            # map the jira issue to a RegScale issue object
            issue = map_jira_to_regscale_issue(
                jira_issue=jira_issue,
                config=app.config,
                parent_id=parent_id,
                parent_module=parent_module,
            )
            # create the issue in RegScale
            if regscale_issue := Issue.insert_issue(
                app=app,
                issue=issue,
            ):
                logger.debug(
                    "Created issue #%i-%s in RegScale.",
                    regscale_issue.id,
                    regscale_issue.title,
                )
                new_regscale_issues.append(regscale_issue)
            else:
                logger.warning("Unable to create issue in RegScale.\nIssue: %s", issue.dict())
        if add_attachments and regscale_issue and jira_issue.fields.attachment:
            # determine which attachments need to be uploaded to prevent duplicates by
            # getting the hashes of all Jira & RegScale attachments
            compare_files_for_dupes_and_upload(
                jira_issue=jira_issue,
                regscale_issue=regscale_issue,
                jira_client=jira_client,
                api=Api(),
            )
        # update progress bar
        progress.update(task, advance=1)


def sync_regscale_to_jira(
    regscale_issues: list[Issue],
    jira_client: JIRA,
    jira_project: str,
    jira_issue_type: str,
    sync_attachments: bool = True,
    attachments: Optional[dict] = None,
    api: Optional[Api] = None,
) -> list[Issue]:
    """
    Sync issues from RegScale to Jira

    :param list[Issue] regscale_issues: list of RegScale issues to sync to Jira
    :param JIRA jira_client: Jira client to use for issue creation in Jira
    :param str jira_project: Jira Project to create the issues in
    :param str jira_issue_type: Type of issue to create in Jira
    :param bool sync_attachments: Sync attachments from RegScale to Jira, defaults to True
    :param Optional[dict] attachments: Dict of attachments to sync from RegScale to Jira, defaults to None
    :param Optional[Api] api: API object to download attachments, defaults to None
    :return: list of RegScale issues that need to be updated
    :rtype: list[Issue]
    """
    new_issue_counter = 0
    issuess_to_update = []
    with job_progress:
        # create task to create Jira issues
        creating_issues = job_progress.add_task(
            f"[#f8b737]Verifying {len(regscale_issues)} RegScale issue(s) exist in Jira...",
            total=len(regscale_issues),
        )
        for issue in regscale_issues:
            # see if Jira issue already exists
            if not issue.jiraId or issue.jiraId == "":
                new_issue = create_issue_in_jira(
                    issue=issue,
                    jira_client=jira_client,
                    jira_project=jira_project,
                    issue_type=jira_issue_type,
                    add_attachments=sync_attachments,
                    attachments=attachments,
                    api=api,
                )
                # log progress
                new_issue_counter += 1
                # get the Jira ID
                jira_id = new_issue.key
                # update the RegScale issue for the Jira link
                issue.jiraId = jira_id
                # add the issue to the update_issues global list
                issuess_to_update.append(issue)
            job_progress.update(creating_issues, advance=1)
    # output the final result
    logger.info("%i new issue(s) opened in Jira.", new_issue_counter)
    return issuess_to_update


def fetch_jira_objects(
    jira_client: JIRA, jira_project: str, jira_issue_type: str, jql_str: str = None, sync_tasks_only: bool = False
) -> list[jiraIssue]:
    """
    Fetch all issues from Jira for the provided project

    :param JIRA jira_client: Jira client to use for the request
    :param str jira_project: Name of the project in Jira
    :param str jira_issue_type: Type of issue to fetch from Jira
    :param str jql_str: JQL string to use for the request, default None
    :param bool sync_tasks_only: Whether to sync only tasks from Jira, defaults to False
    :return: List of Jira issues
    :rtype: list[jiraIssue]
    """
    start_pointer = 0
    page_size = 100
    jira_objects = []
    if sync_tasks_only:
        validate_issue_type(jira_client, jira_issue_type)
        output_str = "task"
    else:
        output_str = "issue"
    logger.info("Fetching %s(s) from Jira...", output_str.lower())
    # get all issues for the Jira project
    while True:
        start = start_pointer * page_size
        jira_issues_response = jira_client.search_issues(
            jql_str=jql_str,
            startAt=start,
            maxResults=page_size,
        )
        if len(jira_objects) == jira_issues_response.total:
            break
        start_pointer += 1
        # append new records to jira_issues
        jira_objects.extend(jira_issues_response)
        logger.info(
            "%i/%i Jira %s(s) retrieved.",
            len(jira_objects),
            jira_issues_response.total,
            output_str.lower(),
        )
    if jira_objects:
        check_file_path("artifacts")
        file_name = f"{jira_project.lower()}_existingJira{jira_issue_type}.json"
        file_path = Path(f"./artifacts/{file_name}")
        save_data_to(
            file=file_path,
            data=[issue.raw for issue in jira_objects],
            output_log=False,
        )
        logger.info(
            "Saved %i Jira %s(s), see %s",
            len(jira_objects),
            jira_issue_type.lower(),
            str(file_path.absolute()),
        )
    logger.info("%i %s(s) retrieved from Jira.", len(jira_objects), output_str.lower())
    return jira_objects


def map_jira_to_regscale_issue(jira_issue: jiraIssue, config: dict, parent_id: int, parent_module: str) -> Issue:
    """
    Map Jira issues to RegScale issues

    :param jiraIssue jira_issue: Jira issue to map to issue in RegScale
    :param dict config: Application config
    :param int parent_id: Parent record ID in RegScale
    :param str parent_module: Parent record module in RegScale
    :return: Issue object of the newly created issue in RegScale
    :rtype: Issue
    """
    due_date = map_jira_due_date(jira_issue, config)
    issue = Issue(
        title=jira_issue.fields.summary,
        severityLevel=Issue.assign_severity(jira_issue.fields.priority.name),
        issueOwnerId=config["userId"],
        dueDate=due_date,
        description=(
            f"Description {jira_issue.fields.description}"
            f"\nStatus: {jira_issue.fields.status.name}"
            f"\nDue Date: {due_date}"
        ),
        status=("Closed" if jira_issue.fields.status.name.lower() == "done" else config["issues"]["jira"]["status"]),
        jiraId=jira_issue.key,
        parentId=parent_id,
        parentModule=parent_module,
        dateCreated=get_current_datetime(),
        dateCompleted=(get_current_datetime() if jira_issue.fields.status.name.lower() == "done" else None),
    )
    return issue


def map_jira_due_date(jira_issue: Optional[jiraIssue], config: dict) -> str:
    """
    Parses the provided jira_issue for a due date and returns it as a string

    :param Optional[jiraIssue] jira_issue: Jira issue to parse for a due date
    :param dict config: Application config
    :return: Due date as a string
    :rtype: str
    """
    if jira_issue.fields.duedate:
        due_date = jira_issue.fields.duedate
    elif jira_issue.fields.priority:
        due_date = datetime.now() + timedelta(days=config["issues"]["jira"][jira_issue.fields.priority.name.lower()])
        due_date = convert_datetime_to_regscale_string(due_date)
    else:
        due_date = datetime.now() + timedelta(days=config["issues"]["jira"]["medium"])
        due_date = convert_datetime_to_regscale_string(due_date)
    return due_date


def _generate_jira_comment(issue: Issue) -> str:
    """
    Generate a Jira comment from a RegScale issue and it's populated fields

    :param Issue issue: RegScale issue to generate a Jira comment from
    :return: Jira comment
    :rtype: str
    """
    comment = ""
    exclude_fields = ["createdById", "lastUpdatedById", "issueOwnerId", "uuid"] + issue._exclude_graphql_fields
    for field_name, field_value in issue.__dict__.items():
        if field_value and field_name not in exclude_fields:
            comment += f"**{field_name}:** {field_value}\n"
    return comment


def create_issue_in_jira(
    issue: Issue,
    jira_client: JIRA,
    jira_project: str,
    issue_type: str,
    add_attachments: Optional[bool] = True,
    attachments: Optional[dict] = None,
    api: Optional[Api] = None,
) -> jiraIssue:
    """
    Create a new issue in Jira

    :param Issue issue: RegScale issue object
    :param JIRA jira_client: Jira client to use for issue creation in Jira
    :param str jira_project: Project name in Jira to create the issue in
    :param str issue_type: The type of issue to create in Jira
    :param Optional[bool] add_attachments: Whether to add attachments to new issue, defaults to true
    :param Optional[dict] attachments: Dictionary containing attachments, defaults to None
    :param Optional[Api] api: API object to download attachments, defaults to None
    :return: Newly created issue in Jira
    :rtype: jiraIssue
    """
    if not api:
        api = Api()
    try:
        reg_issue_url = f"RegScale Issue #{issue.id}: {urljoin(api.config['domain'], f'/form/issues/{issue.id}')}\n\n"
        logger.debug("Creating Jira issue: %s", issue.title)
        new_issue = jira_client.create_issue(
            project=jira_project,
            summary=issue.title,
            description=reg_issue_url + issue.description,
            issuetype=issue_type,
        )
        logger.debug("Jira issue created: %s", new_issue.key)
        # add a comment to the new Jira issue
        logger.debug("Adding comment to Jira issue: %s", new_issue.key)
        _ = jira_client.add_comment(
            issue=new_issue,
            body=reg_issue_url + _generate_jira_comment(issue),
        )
        logger.debug("Comment added to Jira issue: %s", new_issue.key)
    except JIRAError as ex:
        error_and_exit(f"Unable to create Jira issue.\nError: {ex}")
    # add the attachments to the new Jira issue
    if add_attachments and attachments:
        compare_files_for_dupes_and_upload(
            jira_issue=new_issue,
            regscale_issue=issue,
            jira_client=jira_client,
            api=api,
        )
    return new_issue


def compare_files_for_dupes_and_upload(
    jira_issue: jiraIssue, regscale_issue: Issue, jira_client: JIRA, api: Api
) -> None:
    """
    Compare files for duplicates and upload them to Jira and RegScale

    :param jiraIssue jira_issue: Jira issue to upload the attachments to
    :param Issue regscale_issue: RegScale issue to upload the attachments from
    :param JIRA jira_client: Jira client to use for uploading the attachments
    :param Api api: Api object to use for interacting with RegScale
    :rtype: None
    :return: None
    """
    jira_uploaded_attachments = []
    regscale_uploaded_attachments = []
    with tempfile.TemporaryDirectory() as temp_dir:
        jira_dir, regscale_dir = download_issue_attachments_to_directory(
            directory=temp_dir,
            jira_issue=jira_issue,
            regscale_issue=regscale_issue,
            api=api,
        )
        jira_attachment_hashes = compute_hashes_in_directory(jira_dir)
        regscale_attachment_hashes = compute_hashes_in_directory(regscale_dir)

        upload_files_to_jira(
            jira_attachment_hashes,
            regscale_attachment_hashes,
            jira_issue,
            regscale_issue,
            jira_client,
            jira_uploaded_attachments,
        )
        upload_files_to_regscale(
            jira_attachment_hashes, regscale_attachment_hashes, regscale_issue, api, regscale_uploaded_attachments
        )

    log_upload_results(regscale_uploaded_attachments, jira_uploaded_attachments, regscale_issue, jira_issue)


def upload_files_to_jira(
    jira_attachment_hashes: dict,
    regscale_attachment_hashes: dict,
    jira_issue: jiraIssue,
    regscale_issue: Issue,
    jira_client: JIRA,
    jira_uploaded_attachments: list,
) -> None:
    """
    Upload files to Jira

    :param dict jira_attachment_hashes: Dictionary of Jira attachment hashes
    :param dict regscale_attachment_hashes: Dictionary of RegScale attachment hashes
    :param jiraIssue jira_issue: Jira issue to upload the attachments to
    :param Issue regscale_issue: RegScale issue to upload the attachments from
    :param JIRA jira_client: Jira client to use for uploading the attachments
    :param list jira_uploaded_attachments: List of Jira attachments that were uploaded
    :rtype: None
    :return: None
    """
    for file_hash, file in regscale_attachment_hashes.items():
        if file_hash not in jira_attachment_hashes:
            try:
                with open(file, "rb") as in_file:
                    jira_client.add_attachment(
                        issue=jira_issue.id,
                        attachment=BytesIO(in_file.read()),  # type: ignore
                        filename=f"RegScale_Issue_{regscale_issue.id}_{Path(file).name}",
                    )
                    jira_uploaded_attachments.append(file)
            except JIRAError as ex:
                logger.error(
                    "Unable to upload %s to Jira issue %s.\nError: %s",
                    Path(file).name,
                    jira_issue.key,
                    ex,
                )
            except TypeError as ex:
                logger.error(
                    "Unable to upload %s to Jira issue %s.\nError: %s",
                    Path(file).name,
                    jira_issue.key,
                    ex,
                )


def upload_files_to_regscale(
    jira_attachment_hashes: dict,
    regscale_attachment_hashes: dict,
    regscale_issue: Issue,
    api: Api,
    regscale_uploaded_attachments: list,
) -> None:
    """
    Upload files to RegScale

    :param dict jira_attachment_hashes: Dictionary of Jira attachment hashes
    :param dict regscale_attachment_hashes: Dictionary of RegScale attachment hashes
    :param Issue regscale_issue: RegScale issue to upload the attachments to
    :param Api api: Api object to use for interacting with RegScale
    :param list regscale_uploaded_attachments: List of RegScale attachments that were uploaded
    :rtype: None
    :return: None
    """
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


def log_upload_results(
    regscale_uploaded_attachments: list, jira_uploaded_attachments: list, regscale_issue: Issue, jira_issue: jiraIssue
) -> None:
    """
    Log the results of the upload process

    :param list regscale_uploaded_attachments: List of RegScale attachments that were uploaded
    :param list jira_uploaded_attachments: List of Jira attachments that were uploaded
    :param Issue regscale_issue: RegScale issue that the attachments were uploaded to
    :param jiraIssue jira_issue: Jira issue that the attachments were uploaded to
    :rtype: None
    :return: None
    """
    if regscale_uploaded_attachments and jira_uploaded_attachments:
        logger.info(
            "%i file(s) uploaded to RegScale issue #%i and %i file(s) uploaded to Jira issue %s.",
            len(regscale_uploaded_attachments),
            regscale_issue.id,
            len(jira_uploaded_attachments),
            jira_issue.key,
        )
    elif jira_uploaded_attachments:
        logger.info(
            "%i file(s) uploaded to Jira issue %s.",
            len(jira_uploaded_attachments),
            jira_issue.key,
        )
    elif regscale_uploaded_attachments:
        logger.info(
            "%i file(s) uploaded to RegScale issue #%i.",
            len(regscale_uploaded_attachments),
            regscale_issue.id,
        )


def validate_issue_type(jira_client: JIRA, issue_type: str) -> Any:
    """
    Validate the provided issue type in Jira

    :param JIRA jira_client: Jira client to use for the request
    :param str issue_type: Issue type to validate
    :rtype: Any
    :return: True if the issue type is valid, otherwise exit with an error
    """
    issue_types = jira_client.issue_types()
    for issue in issue_types:
        if issue.name == issue_type:
            return True
    message = f"Invalid Jira issue type provided: {issue_type}, the available types are: " + ", ".join(
        {iss.name for iss in issue_types}
    )
    error_and_exit(error_desc=message)


def download_issue_attachments_to_directory(
    directory: str,
    jira_issue: jiraIssue,
    regscale_issue: Issue,
    api: Api,
) -> tuple[str, str]:
    """
    Function to download attachments from Jira and RegScale issues to a directory

    :param str directory: Directory to store the files in
    :param jiraIssue jira_issue: Jira issue to download the attachments for
    :param Issue regscale_issue: RegScale issue to download the attachments for
    :param Api api: Api object to use for interacting with RegScale
    :return: Tuple of strings containing the Jira and RegScale directories
    :rtype: tuple[str, str]
    """
    # determine which attachments need to be uploaded to prevent duplicates by checking hashes
    jira_dir = os.path.join(directory, "jira")
    check_file_path(jira_dir, False)
    # download all attachments from Jira to the jira directory in temp_dir
    for attachment in jira_issue.fields.attachment:
        with open(os.path.join(jira_dir, attachment.filename), "wb") as file:
            file.write(attachment.get())
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
