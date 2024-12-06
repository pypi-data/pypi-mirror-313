#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" RegScale SonarCloud Integration """

import sys
from typing import Optional

import click

# standard python imports
import math
import requests  # type: ignore

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import (
    get_current_datetime,
    days_between,
)
from regscale.core.app.utils.regscale_utils import create_regscale_assessment
from regscale.models import regscale_id, regscale_module
from regscale.models.regscale_models.assessment import Assessment
from regscale.models.regscale_models.issue import Issue

# create logger function to log to the console
logger = create_logger()


def get_sonarcloud_results(config: dict) -> list[list[dict]]:
    """
    Retrieve Sonarcloud Results from the Sonarcloud.io API
    :param dict config: RegScale CLI configuration
    :return: json response data from API GET request
    :rtype: list[list[dict]]
    """
    # api endpoint
    url = "https://sonarcloud.io/api/issues/search"
    # SONAR_TOKEN from Sonarcloud
    token = config["sonarToken"]
    # arguments to pass to the API call
    query = {
        "organization": "regscale",
        "projects": "RegScale_regscale",
        "branch": "main",
        "projectKey": "RegScale_regscale",
        "statuses": "OPEN, CONFIRMED, REOPENED",
        "createdInLast": "1m",
        "ps": 500,
    }
    # GET request pulls in data to check results size
    r = requests.get(url, auth=(str(token), ""), params=query)
    # if the status code does not equal 200
    if r and not r.ok:
        # exit the script gracefully
        sys.exit("Sonarcloud API call failed please check the configuration")
    # pull in response data to a dictionary
    data = r.json()
    # find the total results number
    total = data["paging"]["total"]
    # find the number of results in each result page
    size = data["paging"]["pageSize"]
    # calculate the number of pages to iterate through sequentially
    pages = math.ceil(total / size)
    # create an empty list to hold multiple pages of data
    complete = []
    # loop through each page number
    for i in range(1, pages + 1, 1):
        # parameters to pass to the API call
        filters = {
            "organization": "regscale",
            "projects": "RegScale_regscale",
            "branch": "main",
            "projectKey": "RegScale_regscale",
            "statuses": "OPEN, CONFIRMED, REOPENED",
            "createdInLast": "1m",
            "ps": 500,
            "p": f"{i}",
        }
        # for each page make a GET request to pull in the data
        r = requests.get(url, auth=(str(token), ""), params=filters)
        # pull in response data to a dictionary
        data = r.json()
        # extract only the issues from the data
        issues = data["issues"]
        # add each page to the total results page
        complete.append(issues)
    # return the list of json response objects for use
    return complete


def build_data(api: Api) -> list[dict]:
    """
    Build vulnerability alert data list
    :param Api api: API object
    :return: vulnerability data list
    :rtype: list[dict]
    """
    # execute GET request
    data = get_sonarcloud_results(config=api.config)
    # create empty list to hold json response dicts
    vulnerability_data_list = []
    # loop through the lists in API response data
    for result in data:
        # loop through the list of dicts in the API response data
        for i, issue in enumerate(result):
            # format datetime stamp to use with days_between function
            create_date = issue["creationDate"][0:19] + "Z"
            # build vulnerability list
            vulnerability_data_list.append(
                {
                    "key": issue["key"],
                    "severity": issue["severity"],
                    "component": issue["component"],
                    "status": issue["status"],
                    "message": issue["message"],
                    "creationDate": issue["creationDate"][0:19],
                    "updateDate": issue["updateDate"][0:19],
                    "type": issue["type"],
                    "days_elapsed": days_between(vuln_time=create_date),
                }
            )
    return vulnerability_data_list


def build_dataframes(api: Api) -> str:
    """
    Build pandas dataframes from vulnerability alert data list

    :param Api api: API object
    :return: dataframe as an HTML table
    :rtype: str
    """
    import pandas as pd  # Optimize import performance

    # create vulnerability data list
    vuln_data_list = build_data(api=api)

    # for vulnerability in vuln_data_list:
    df = pd.DataFrame(vuln_data_list)
    # sort dataframe by severity
    df.sort_values(by=["severity"], inplace=True)
    # reset and drop the index
    df.reset_index(drop=True, inplace=True)
    # convert the dataframe to an html table
    output = df.to_html(header=True, index=False, justify="center", border=1)
    return output


def create_alert_assessment(api: Api, parent_id: Optional[int] = None, parent_module: Optional[str] = None) -> int:
    """
    Create Assessment containing SonarCloud alerts
    :param Api api: API object
    :param Optional[int] parent_id: Parent ID of the assessment, defaults to None
    :param Optional[str] parent_module: Parent module of the assessment, defaults to None
    :return: New Assessment ID
    :rtype: int
    """
    # create the assessment report HTML table
    df_output = build_dataframes(api)
    # build assessment model data
    assessment_data = Assessment(
        leadAssessorId=api.config["userId"],
        title="SonarCloud Code Scan Assessment",
        assessmentType="Control Testing",
        plannedStart=get_current_datetime(),
        plannedFinish=get_current_datetime(),
        assessmentReport=df_output,
        assessmentPlan="Complete the child issues created by the SonarCloud code scan results that were retrieved by the API. The assessment will fail if any high severity vulnerabilities has a days_elapsed value greater than or equal to 10 days.",
        createdById=api.config["userId"],
        dateCreated=get_current_datetime(),
        lastUpdatedById=api.config["userId"],
        dateLastUpdated=get_current_datetime(),
        status="In Progress",
    )
    if parent_id and parent_module:
        assessment_data.parentId = parent_id
        assessment_data.parentModule = parent_module
    # create vulnerability data list
    vuln_data_list = build_data(api)
    # if assessmentResult is changed to Pass / Fail then status has to be
    # changed to complete and a completion date has to be passed
    for vulnerability in vuln_data_list:
        if vulnerability["severity"] == "CRITICAL" and vulnerability["days_elapsed"] >= 10:
            assessment_data.status = "Complete"
            assessment_data.actualFinish = get_current_datetime()
            assessment_data.assessmentResult = "Fail"

    # create a new assessment in RegScale
    new_assessment_id = create_regscale_assessment(
        url=f"{api.config['domain']}/api/assessments",
        new_assessment=assessment_data.dict(),
        api=api,
    )
    # log assessment creation result
    if new_assessment_id is not None:
        logger.info("Assessment was created successfully")
    else:
        logger.info("Assessment was not created")
    return new_assessment_id


def create_alert_issues(parent_id: Optional[int] = None, parent_module: Optional[str] = None) -> None:
    """
    Create child issues from the alert assessment
    :param Optional[int] parent_id: Parent ID record to associate the assessment to, defaults to None
    :param Optional[str] parent_module: Parent module to associate the assessment to, defaults to None
    :rtype: None
    """
    # set environment and application configuration
    app = Application()
    api = Api()
    # execute POST request and return new assessment ID
    assessment_id = create_alert_assessment(api=api, parent_id=parent_id, parent_module=parent_module)

    # create vulnerability data list
    vuln_data_list = build_data(api)
    # loop through each vulnerability alert in the list
    for vulnerability in vuln_data_list:
        # create issue model
        issue_data = Issue(
            title="Sonarcloud Code Scan",  # Required
            dateCreated=get_current_datetime("%Y-%m-%dT%H:%M:%S"),
            description=vulnerability["message"],
            severityLevel=Issue.assign_severity(vulnerability["severity"]),  # Required
            issueOwnerId=app.config["userId"],  # Required
            dueDate=get_current_datetime(),
            identification="Code scan assessment",
            status="Open",
            assessmentId=assessment_id,
            createdBy=app.config["userId"],
            lastUpdatedById=app.config["userId"],
            dateLastUpdated=get_current_datetime(),
            parentId=assessment_id,
            parentModule="assessments",
        )
        # create assessment child issue via POST
        iss = api.post(
            f'{app.config["domain"]}/api/issues',
            json=issue_data.dict(),
        )
        # log issue creation result
        if iss.ok:
            logger.info("Issue created successfully.")
        else:
            logger.info("Issue was not created.")


@click.group()
def sonarcloud() -> None:
    """
    Create an assessment and child issues in RegScale from SonarCloud alerts.
    """
    pass


@sonarcloud.command(name="sync_alerts")
@regscale_id(required=False, default=None)
@regscale_module(required=False, default=None)
def create_alerts(regscale_id: Optional[int] = None, regscale_module: Optional[str] = None) -> None:
    """
    Create a child assessment and child issues in RegScale from SonarCloud alerts.
    """
    create_alert_issues(regscale_id, regscale_module)
