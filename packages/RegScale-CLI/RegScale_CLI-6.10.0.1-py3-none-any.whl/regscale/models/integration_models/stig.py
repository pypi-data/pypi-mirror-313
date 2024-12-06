#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard python imports """
import datetime
import logging
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from json import dumps
from pathlib import Path
from threading import get_native_id, Lock
from typing import Any, Optional, Tuple, Union

import click
import requests
from rich.progress import Progress, TaskID

from regscale.core.app.api import Api, normalize_url
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import (
    convert_datetime_to_regscale_string,
    create_progress_object,
    format_data_to_html,
    get_current_datetime,
    xml_file_to_dict,
    walk_directory_for_files,
)
from regscale.core.app.utils.regscale_utils import error_and_exit
from regscale.models.regscale_models import Component, ControlImplementation
from regscale.models.regscale_models.asset import Asset
from regscale.models.regscale_models.checklist import Checklist
from regscale.models.regscale_models.implementation_objective import (
    ImplementationObjective,
    ImplementationStatus,
)
from regscale.models.regscale_models.implementation_option import ImplementationOptionDeprecated
from regscale.models.regscale_models.issue import Issue
from regscale.models.regscale_models.stig import STIG_FILE
from regscale.validation.address import validate_mac_address

asset_progress = create_progress_object()
update_objective_progress = create_progress_object()
insert_objective_progress = create_progress_object()
ssp_implementation_progress = create_progress_object()
component_progess = create_progress_object()


class STIG:
    """A class to process STIG files"""

    def __init__(
        self,
        folder_path: click.Path,
        regscale_ssp_id: click.INT,
        cci_mapping: Optional[dict] = None,
        regscale_dod_catalog_id: Optional[click.INT] = None,
    ):
        stig_logger = self.create_logger()
        app = Application()
        config = app.config
        api = Api()
        self.config = config
        self.cci_mapping = cci_mapping
        self.logger = stig_logger
        self.app = app
        self.api = api
        self.folder_path = folder_path
        self.regscale_ssp = regscale_ssp_id
        self.files = self.process_directory(folder_path)
        self.existing_components = set()
        self.ssp_issues: list[dict] = []
        self.mega_data: list[dict] = []
        self.catalog_details: list[dict] = []
        self.all_security_checklists: list[dict] = []
        self.regscale_dod_catalog_id = regscale_dod_catalog_id
        self.all_control_objectives: list[dict] = []
        self.all_rules: list[dict] = []
        self.all_implementation_objectives: list[ImplementationObjective] = []
        self.all_implementations: list[dict] = []
        self.all_implementation_options: set[ImplementationOptionDeprecated] = set()
        self.process(regscale_ssp_id=regscale_ssp_id)
        self.final_check()

    @classmethod
    def create(
        cls,
        folder_path: click.Path,
        regscale_ssp_id: click.INT,
        cci_mapping: Optional[dict] = None,
        regscale_dod_catalog_id: Optional[click.INT] = None,
    ) -> "STIG":
        """
        Create an instance of the STIG class

        :param click.Path folder_path: Path to directory to process for .ckl files
        :param click.INT regscale_ssp_id: RegScale SSP ID
        :param Optional[dict] cci_mapping: CCI Mapping
        :param Optional[click.INT] regscale_dod_catalog_id: RegScale DoD Catalog ID
        :return: Instance of STIG class
        :rtype: STIG
        """
        instance = cls(folder_path, regscale_ssp_id, cci_mapping, regscale_dod_catalog_id)
        instance.process(regscale_ssp_id=regscale_ssp_id)  # the instance method
        instance.final_check()
        return instance

    @staticmethod
    def process_directory(folder_path: Union[str, Path, click.Path]) -> list[str]:
        """
        Process a directory for .ckl files, if none found it will terminate the application

        :param Union[str, Path, click.Path] folder_path: Path to directory to process for .ckl files
        :return: List of .ckl file paths
        :rtype: list[str]
        """
        if isinstance(folder_path, click.Path) or isinstance(folder_path, Path):
            folder_path = str(folder_path)
        files = list(Path(folder_path).glob("*.ckl"))
        if not files:
            # no .ckl files were found in the provided directory so let's walk the directory for files
            files, _ = walk_directory_for_files(folder_path, ".ckl")
        return files or error_and_exit(f"No .ckl files found in provided directory: {folder_path}")

    @classmethod
    def create_logger(cls) -> logging.Logger:
        """Create logger object

        :return: Logger object
        :rtype: logging.Logger
        """
        logger = create_logger(propagate=True)
        return logger

    def final_check(self) -> None:
        """
        Assert that all objectives no longer have failed implementations Solves probable race conditions in "process"

        :rtype: None
        """
        # if any name from all rules is in the notes from all objectives, the objective fails

        objs_to_update = []
        for rule in self.all_rules:
            for obj in self.all_implementation_objectives:
                if rule["STIGRef"] in obj["notes"] and rule["STIGRef"] + str(obj["id"]) not in {
                    u_obj["rule"] + str(u_obj["obj"]["id"]) for u_obj in objs_to_update
                }:
                    objs_to_update.append({"rule": rule["STIGRef"], "obj": obj})
        if objs_to_update:
            for obj in objs_to_update:
                objective_id = obj["obj"]["id"]
                implementation_id = obj["obj"]["implementationId"]
                existing_implementation = self.api.get(
                    url=self.config["domain"] + f"/api/controlimplementation/{implementation_id}",
                ).json()

                # Get Full Objective
                existing_obj = [obj for obj in existing_implementation["objectives"] if obj["id"] == objective_id][0]
                if "status" not in existing_obj or existing_obj["status"] != ImplementationStatus.NOT_IMPLEMENTED.value:
                    existing_obj["status"] = ImplementationStatus.NOT_IMPLEMENTED.value
                    del existing_obj[
                        "implementation"
                    ]  # don't need this data for a put, this won't affect the database.
                    response = ImplementationObjective.update_objective(app=self.app, obj=existing_obj)
                    if not response.ok:
                        self.logger.error("Unable to update Objective: %s", existing_obj)
                    self.update_implementation(
                        existing_imp=existing_implementation,
                        status=existing_obj["status"],
                    )
        else:
            # Ensure SSP implementations are updated
            ssp_imps = self.get_implementations(parent_id=self.regscale_ssp, parent_module="securityplans")
            for imp in ssp_imps:
                component_imp = [
                    cntrl_imp
                    for cntrl_imp in self.all_implementations
                    if cntrl_imp["parentModule"] == "components"
                    and cntrl_imp["id"]
                    and cntrl_imp["controlName"] == imp["controlName"]
                    and cntrl_imp["status"] != imp["status"]
                ]
                if component_imp:
                    imp["status"] = component_imp[0]["status"]
                    # update imp
                    self.api.put(
                        self.app.config["domain"] + "/api/controlimplementation/" + str(imp["id"]),
                        json=imp,
                    )

    def get_checklists_by_implementation(self, implementation: dict) -> list:
        """
        Get all checklists for a given implementation

        :param dict implementation: Dictionary of implementation
        :return: List of checklists
        :rtype: list
        """
        checklists = []
        assets = self.api.get(
            url=self.config["domain"] + f"/api/assets/getAllByParent/{implementation['parentId']}/components"
        ).json()
        for asset in assets:
            checklists.extend(
                self.api.get(url=self.config["domain"] + f"/api/securityChecklist/getAllByParent/{asset['id']}").json()
            )
        return checklists

    def lookup_cci_status(self, cci: str, all_checklists: list[dict]) -> str:
        """
        A simple lookup to determine status from all the checklists with a given CCI

        :param str cci: CCI identifier
        :param list[dict] all_checklists: A list of all checklists
        :return: Checklist status
        :rtype: str
        """
        status = "Fail"
        results = {chk["status"] for chk in all_checklists if chk["cci"] == cci}
        c = Counter(results)
        self.logger.debug("Counter: %s", c)
        if "Pass" in c and c.total() == 1:
            status = "Pass"
        return status

    def refresh_mega_api(self) -> None:
        """
        Refresh the mega api data

        :raises ValueError: If unable to load controls from the SSP
        :rtype: None
        """
        self.logger.info("Refreshing Mega API dataset, this may take a while..")
        mega_res = self.api.get(url=self.config["domain"] + f"/api/securityplans/megaAPI/{self.regscale_ssp}")
        if mega_res.ok:
            self.mega_data = mega_res.json()
            if not self.mega_data["normalizedControls"]:
                raise ValueError("Unable to continue, please load some controls to the SSP!")
            self.logger.info("Mega data is Refreshed!")
            # Update Implementation Objectives
            self.all_implementation_objectives = []
            # update issues
            self.ssp_issues.extend(self.mega_data["issues"])
            # TODO: Refresh all implementation objectives from the mega api (currently only available at ssp level)
            self.refresh_implementation_objectives()

    def refresh_component_implementations(self, component_ids: set[int]) -> None:
        """
        Return all existing component implementations for a list of component ids

        :param set[int] component_ids: list of component ids
        :rtype: None
        """
        url = self.config["domain"] + "/api/controlimplementation"
        all_existing_component_implementations = []
        with ssp_implementation_progress:
            refreshing_components = ssp_implementation_progress.add_task(
                f"[#ffa500]Refreshing {len(component_ids)} component(s)...",
                total=len(component_ids),
            )
            for component_id in component_ids:
                existing_component_response = self.api.get(url=url + f"/getAllByParent/{component_id}/components")
                if existing_component_response.ok:
                    existing_component_implementations = existing_component_response.json()
                    all_existing_component_implementations.extend(existing_component_implementations)
                ssp_implementation_progress.advance(refreshing_components, 1)

            refreshing_comp_imps = ssp_implementation_progress.add_task(
                f"[#ffa500]Refreshing {len(all_existing_component_implementations)} component implementation(s)...",
                total=len(all_existing_component_implementations),
            )
            for imp in all_existing_component_implementations:
                if imp["id"] not in {imp["id"] for imp in self.all_implementations}:  # don't add duplicates
                    self.all_implementations.append(imp)
                ssp_implementation_progress.advance(refreshing_comp_imps, 1)

    def get_component_ids(self) -> set[int]:
        """
        Get a set of component ids

        :return: Set of component ids
        :rtype: set[int]
        """
        return {
            cmp["id"]
            for cmp in self.api.get(
                self.config["domain"] + f"/api/components/getAllByParent/{self.regscale_ssp}"
            ).json()
        }

    def get_security_control_ids(self, cat_id: Union[str, int]) -> dict:
        """
        Get a dictionary of security control ids for each CCI in the catalog

        :param Union[str, int] cat_id: Catalog ID
        :return: Dictionary of security control ids
        :rtype: dict
        """
        control_objectives = self.api.get(
            url=self.config["domain"] + f"/api/controlobjectives/getByCatalog/{cat_id}"
        ).json()
        return {obj["name"]: obj["securityControlId"] for obj in control_objectives}

    def get_new_implementations(self, cci_list: list[str], component_ids: set[int], security_control_ids: dict) -> set:
        """
        Get a set of new control implementations

        :param list[str] cci_list: List of CCIs
        :param set[int] component_ids: Set of component ids
        :param dict security_control_ids: Dictionary of security control ids
        :return: Set of new control implementations
        :rtype: set
        """
        cat_id = self.get_catalog_id()
        existing_imps = self.get_all_component_implementations()
        existing_imps_map = defaultdict(set)
        for imp in existing_imps:
            existing_imps_map[imp["parentId"]].add(imp["controlID"])
        total_new_imps = set()
        new_imps_lock = Lock()

        def _worker(
            ssp_control_id: int,
            comp_ids: set[int],
            progress_object: Progress,
            main_task_id: int,
            user_id: str,
            imp_status: str,
        ) -> None:
            """
            Worker function for creating new implementations in threads

            :param int ssp_control_id: Security control id
            :param set[int] comp_ids: Set of component ids
            :param Progress progress_object: Progress object to use for updating the correct task
            :param int main_task_id: Parent task id for updating progress
            :param str user_id: User id from config
            :param str imp_status: Implementation status
            :rtype: None
            """
            progress_task_id = progress_object.add_task(
                description=f"[#ffa500]Creating {len(comp_ids)} component implementation(s) for "
                f"control #{ssp_control_id}...",
                total=len(comp_ids),
            )
            new_comp_imps = set()
            new_imps_list = [
                ControlImplementation(
                    parentId=component_id,
                    parentModule="components",
                    controlOwnerId=user_id,
                    status=imp_status,
                    controlID=ssp_control_id,
                )
                for component_id in comp_ids
                if ssp_control_id not in existing_imps_map.get(component_id, set())
            ]
            new_comp_imps.update(new_imps_list)
            progress_object.advance(progress_task_id, 1)
            progress_object.advance(main_task_id, 1)
            progress_object.remove_task(progress_task_id)
            with new_imps_lock:
                total_new_imps.update(new_comp_imps)

        with ssp_implementation_progress as progress:
            fetching_new_imps = progress.add_task(
                f"[#ffa500]Analyzing {len(cci_list)} CCI(s) for new implementation(s)...",
                total=len(cci_list),
            )
            new_imps = []
            for cci in cci_list:
                try:
                    security_control_id = security_control_ids[cci]
                    new_imps.append(security_control_id)
                except KeyError:
                    self.logger.error("Unable to find %s in base catalog (#%i).", cci, cat_id)
                progress.advance(fetching_new_imps, 1)
            progress.update(fetching_new_imps, visible=False)
            # limited to 100 threads because this is a very expensive operation
            with ThreadPoolExecutor(max_workers=100) as executor:
                creating_imps = progress.add_task(
                    f"[#ffa500]Creating ~{len(new_imps) * len(component_ids)} new implementation(s)...",
                    total=len(new_imps),
                )
                futures = [
                    executor.submit(
                        _worker,
                        security_control_id,
                        component_ids,
                        progress,
                        creating_imps,
                        self.config["userId"],
                        ImplementationStatus.NOT_IMPLEMENTED.value,
                    )
                    for security_control_id in new_imps
                ]
                for future in as_completed(futures):
                    future.result()
        return total_new_imps

    def create_new_implementations(self, new_imps: list[Union[ControlImplementation, dict]]) -> None:
        """
        Create new control implementations in RegScale

        :param list[Union[ControlImplementation, dict]] new_imps: Set of new control implementations to create
        :rtype: None
        """
        if new_imps:
            if isinstance(list(new_imps)[0], ControlImplementation):
                new_imps = [imp.dict() for imp in new_imps]
            # create new control implementations in batches of 1000
            with ssp_implementation_progress:
                creating_imps = ssp_implementation_progress.add_task(
                    f"[#ffa500]Creating {len(new_imps)} new implementation(s) in RegScale...",
                    total=len(new_imps),
                )
                for i in range(0, len(new_imps), 1000):
                    response = self.api.post(
                        url=self.config["domain"] + "/api/controlimplementation/batchcreate",
                        json=new_imps[i : i + 1000],
                    )
                    if not response.raise_for_status():
                        self.create_implementations(ssp_implementation_progress, creating_imps, i, new_imps)

    def create_implementations(self, progress: Progress, task_id: TaskID, index: int, new_imps: list[dict]) -> None:
        """
        Create new control implementations in RegScale

        :param Progress progress: Progress object to use for updating the correct task
        :param TaskID task_id: Progress task id for updating progress bar
        :param int index: Index of new_imps
        :param list[dict] new_imps: Set of new control implementations to create
        :rtype: None
        """
        progress.advance(task_id, len(new_imps[index : index + 1000]))
        for new_imp in new_imps:
            if new_imp["id"] not in {imp["id"] for imp in self.all_implementations}:  # don't add duplicates
                self.all_implementations.append(new_imp)

    def refresh_implementations(self, cci_list: list[str], cat_id: int) -> Tuple[list[dict], list[dict]]:
        """Build a list of new implementations and a list of new objectives

        :param list[str] cci_list: A list of CCIs.
        :param int cat_id: A catalog id.
        :return: A tuple of new implementations and new objectives.
        :rtype: Tuple[list[dict], list[dict]]
        """
        component_ids = self.get_component_ids()
        security_control_ids = self.get_security_control_ids(cat_id)
        new_imps = self.get_new_implementations(cci_list, component_ids, security_control_ids)  # Slow
        self.logger.info("Creating %i new implementation(s) in RegScale...", len(new_imps))
        self.create_new_implementations(new_imps)
        self.all_control_objectives = []
        self.all_control_objectives.extend(
            self.api.get(url=self.config["domain"] + f"/api/controlobjectives/getByCatalog/{cat_id}").json()
        )
        self.refresh_component_implementations(component_ids=component_ids)
        return list(new_imps), self.all_control_objectives

    def send_objective_insert_or_update(
        self, url: str, imp_obj: dict, action_type: str = "update"
    ) -> requests.Response:
        """
        Function for updating or inserting objectives to RegScale via API

        :param str url: URL for API call
        :param dict imp_obj: Dictionary of implementation objective
        :param str action_type: method type for API method, default is update
        :return: API response object
        :rtype: requests.Response
        """
        imp_obj_id = imp_obj["id"]
        if action_type == "update":
            response = self.api.put(url=url + f"/{imp_obj_id}", json=imp_obj) if imp_obj_id else requests.Response()
        else:
            response = self.api.post(url=url, json=imp_obj)
        return response

    # TODO: look into making this a threaded function
    def create_objectives(
        self,
        implementation: dict,
        options: set[ImplementationOptionDeprecated],
        control_objectives: list[dict],
        all_checklists: list[dict],
    ) -> tuple[list[dict], list[dict]]:
        """
        Create objectives for a given implementation

        :param dict implementation: Dictionary of implementations
        :param set[ImplementationOptionDeprecated] options: Set of implementation options
        :param list[dict] control_objectives: List of control objectives
        :param list[dict] all_checklists: List of all checklists
        :raises ValueError: If unable to fetch options for implementation
        :return: Tuple of inserted and updated objectives
        :rtype: tuple[list[dict], list[dict]]
        """
        insert_objs = []
        update_objs = []
        if not options:
            raise ValueError(f"Unable to fetch options for implementation #{implementation['id']}")

        self.logger.debug(
            "Updating or creating %i implementation objectives for implementation # %i",
            len(control_objectives),
            implementation["id"],
        )
        for obj in control_objectives:
            # Status always comes from checklists
            status = self.lookup_cci_status(cci=obj["name"], all_checklists=all_checklists)
            opts = [opt for opt in options if opt.objectiveId == obj["id"]]
            key = (
                ImplementationStatus.FULLY_IMPLEMENTED.value
                if status == "Pass"
                else ImplementationStatus.NOT_IMPLEMENTED.value
            )
            option_id = [opt.id for opt in opts if opt.description == key][0]
            imp_obj = ImplementationObjective(
                id=0,
                uuid="",
                implementationId=implementation["id"],
                status=key,
                objectiveId=obj["id"],
                optionId=option_id,
                notes=obj["name"],
                securityControlId=obj["securityControlId"],
            )
            unique_objectives = {(obj.objectiveId, obj.implementationId) for obj in self.all_implementation_objectives}
            if (imp_obj.objectiveId, imp_obj.implementationId) not in unique_objectives:
                insert_objs.append(asdict(imp_obj))
                self.all_implementation_objectives.append(imp_obj)
            else:
                match_obj = [
                    obj
                    for obj in self.all_implementation_objectives
                    if obj.objectiveId == imp_obj.objectiveId and obj.implementationId == imp_obj.implementationId
                ]
                if match_obj:
                    option_id = imp_obj.optionId
                    imp_obj = match_obj[0]
                    imp_obj.status = key
                    imp_obj.optionId = option_id
                    update_objs.append(asdict(imp_obj))
        return insert_objs, update_objs

    def mass_update(self, update_objs: list[dict], insert_objs: list[dict]) -> None:
        """
        Function to update and insert objectives in batches to RegScale via API

        :param list[dict] update_objs: List of implementation objectives to update
        :param list[dict] insert_objs: List of implementation objectives to create
        :rtype: None
        """
        url = self.config["domain"] + "/api/implementationobjectives"
        self.logger.debug("Insert Objectives: %i", len(insert_objs))
        self.logger.debug("Update Objectives: %i", len(update_objs))

        def update(objs, progress, method="insert"):
            with progress:
                objectives = progress.add_task(
                    f"[#ffa500]{method.title()} {len(objs)} implementation objective(s) at the component level...",
                    total=len(objs),
                )
                with ThreadPoolExecutor(max_workers=self.config["maxThreads"]) as pool:
                    # Prone to race conditions on inserting new items with a lack of FK/Unique constraints, be careful
                    # Process each file
                    lst = [
                        pool.submit(
                            self.send_objective_insert_or_update,
                            url,
                            imp_obj,
                            action_type=method,
                        )
                        for imp_obj in objs
                    ]
                    for future in as_completed(lst):
                        if future.done():
                            progress.advance(objectives, 1)

        if insert_objs:
            update(objs=insert_objs, progress=insert_objective_progress, method="insert")
        if update_objs:
            update(objs=update_objs, progress=update_objective_progress, method="update")

    def get_all_component_implementations(self) -> list[dict]:
        """
        Get all Component Implementations

        :return: A list of all Component Implementations
        :rtype: list[dict]
        """
        existing_components = self.existing_components
        control_implementations = []
        for component in existing_components:
            control_implementations.extend(
                self.get_implementations(parent_id=component["id"], parent_module="components")
            )
            self.all_security_checklists.extend(
                Checklist.get_checklists(parent_id=component["id"], parent_module="components")
            )

        return control_implementations

    def update_component_implementations(self) -> None:
        """
        Update Component Implementations

        :rtype: None
        """

        def _workers(control: dict, progress: Progress, task_id: int) -> None:
            """
            Worker function for updating & analyzing component implementations in threads

            :param dict control: RegScale control object
            :param Progress progress: Progress object to use for updating the correct task
            :param int task_id: Parent task id for updating progress
            :rtype: None
            """
            objective_status = ImplementationStatus.NOT_IMPLEMENTED.value
            sec_control_objectives = ImplementationObjective.fetch_implementation_objectives(
                app=self.app,
                control_id=control["controlID"],
                query_type="control",
            )["implementationObjectives"]["items"]
            objectives = [obj for obj in sec_control_objectives if obj["implementationId"] == control["id"]]
            progress.advance(task_id, 1)
            if objectives:
                analyzing_objectives = progress.add_task(
                    f"[#ffa500]Analyzing {len(objectives)} objectives for control #{control['controlID']} "
                    "for possible updates...",
                    total=1,
                )
                cntr = Counter([obj["status"] for obj in objectives])
                if cntr[ImplementationStatus.FULLY_IMPLEMENTED.value] == cntr.total():
                    objective_status = ImplementationStatus.FULLY_IMPLEMENTED.value
                if control["status"] != objective_status:
                    control["status"] = objective_status
                    self.api.put(
                        url=f"{self.config['domain']}/api/controlImplementation/{control['id']}",
                        json=control,
                    )
                progress.update(analyzing_objectives, visible=False)

        control_implementations = self.get_all_component_implementations()
        self.logger.info(
            "Updating %i component implementation(s) in RegScale...",
            len(control_implementations),
        )
        # Update implementations
        with ssp_implementation_progress as progress, ThreadPoolExecutor() as executor:
            updating_imps = progress.add_task(
                f"[#ffa500]Updating {len(control_implementations)} component implementation(s)...",
                total=len(control_implementations),
            )
            futures = []
            for control in control_implementations:
                future = executor.submit(
                    _workers,
                    control,
                    progress,
                    updating_imps,
                )
                futures.append(future)

                for future in futures:
                    future.result()

    def _create_issue(self, issue: dict) -> list:
        """
        Create an issue in RegScale via API

        :param dict issue: Issue object to create in RegScale via API
        :return: JSON response from RegScale API
        :rtype: list
        """
        r = self.api.post(self.app.config["domain"] + "/api/issues", json=issue)
        if r.status_code == 200:
            self.logger.info("Created issue: %s - #%i", issue["title"], r.json()["id"])
            self.logger.debug(r.json())
        return r.json()

    def _update_issue(self, issue: dict) -> list:
        """
        Update an issue in RegScale via API

        :param dict issue: Issue object to update in RegScale via API
        :return: JSON response from RegScale API
        :rtype: list
        """
        r = self.api.put(self.app.config["domain"] + f"/api/issues/{issue['id']}", json=issue)
        if r.status_code == 200:
            self.logger.info("Updated issue: %s - #%i", issue["title"], issue["id"])
            self.logger.debug(r.json())
        return r.json()

    def update_ssp_issues(self) -> None:
        """
        Create or update issues for failed SSP control implementations

        :rtype: None
        """
        control_implementations = self.get_all_component_implementations()
        r = self.api.get(url=self.config["domain"] + f"/api/issues/getAllByParent/{self.regscale_ssp}/securityplans")
        if r.status_code == 200:
            self.ssp_issues = r.json()
        today_date = datetime.date.today().strftime("%m/%d/%y")
        due_date = datetime.datetime.strptime(today_date, "%m/%d/%y") + datetime.timedelta(days=30)
        assets_with_failed_security_checks = {
            (chk["asset"]["name"], chk["asset"]["id"])
            for chk in self.all_security_checklists
            if "asset" in chk and chk["status"] == "Fail"
        }
        assets_with_passed_security_checks = {
            (chk["asset"]["name"], chk["asset"]["id"])
            for chk in self.all_security_checklists
            if "asset" in chk and chk["status"] == "Pass"
        }
        for control in control_implementations:
            description = "No security checklist (STIG) coverage found."
            if assets_with_failed_security_checks:
                description = (
                    f"<p>Assets with failed Security Checks for control: {control['controlName'].upper()}</p>"
                    + "</p>".join(
                        [
                            f"""<p>{asset[0]}: <a href="{self.app.config['domain']}/form/assets/{asset[1]} title="">{self.app.config['domain']}/form/assets/{asset[1]}</a>"""
                            for asset in assets_with_failed_security_checks
                        ]
                    )
                )
            elif assets_with_passed_security_checks and not assets_with_failed_security_checks:
                description = "No failed security checks found."
            new_issue = Issue(
                title=f"{control['controlName']} is not implemented for component: {control['parentId']}",
                dateCreated=get_current_datetime(),
                status=("Open" if control["status"] == ImplementationStatus.NOT_IMPLEMENTED.value else "Closed"),
                severityLevel="I - High - Significant Deficiency",
                issueOwnerId=self.app.config["userId"],
                securityPlanId=self.regscale_ssp,
                componentId=control["parentId"],
                parentId=self.regscale_ssp,
                parentModule="securityplans",
                identification="STIG Assessment",
                dueDate=convert_datetime_to_regscale_string(due_date),
                description=description,
            )
            # if control["status"] == ImplementationStatus.NOT_IMPLEMENTED.value:
            match_issue = [iss for iss in self.ssp_issues if iss["title"] == new_issue.title]
            if match_issue:
                issue = match_issue[0]
            else:
                issue = new_issue.dict()
            # Check if issue exists
            if not match_issue and issue["status"] == "Open":
                # Create issue
                self._create_issue(issue)
            elif (new_issue.status != issue["status"]) or (new_issue.description != issue["description"]):
                # Update issue
                issue["status"] = new_issue.status
                del issue["dateCreated"]
                issue["description"] = new_issue.description
                issue["dateCompleted"] = get_current_datetime() if issue["status"] == "Closed" else ""
                self._update_issue(issue)

    def update_ssp_implementation_objectives(self) -> None:
        """
        Update SSP Implementation Objectives

        :rtype: None
        """

        def process_ssp_objectives(obj: ImplementationObjective) -> None:
            """
            Process a single objective

            :param ImplementationObjective obj: Objective data
            :rtype: None
            """
            fmt = "%Y-%m-%d %H:%M:%S"
            self.logger.debug("Entering Thread: %i", get_native_id())
            if obj.objectiveId not in {obj.objectiveId for obj in ssp_objectives}:
                # Create and Post SSP objective
                new_imp_obj = ImplementationObjective(
                    id=0,
                    uuid=None,
                    notes=obj.notes,
                    optionId=obj.optionId,  # need to put something here
                    status=obj.status,
                    dateLastAssessed=datetime.datetime.now().strftime(fmt),
                    objectiveId=obj.objectiveId,
                    securityControlId=imp["controlID"],
                    implementationId=imp["id"],
                    dateCreated=get_current_datetime(),
                    dateLastUpdated=get_current_datetime(),
                    lastUpdatedById=self.app.config["userId"],
                    createdById=self.app.config["userId"],
                )
                res = ImplementationObjective.insert_objective(app=self.app, obj=new_imp_obj)
                if res.status_code != 200:
                    self.logger.warning("Unable to post new objective: %s", new_imp_obj)
            else:
                # Update
                update_obj = None
                update_dat = [ssp_obj for ssp_obj in ssp_objectives if obj.objectiveId == ssp_obj.objectiveId]
                if update_dat:
                    update_obj = update_dat[0]
                if update_obj and update_obj.status != obj.status and update_obj.optionId != obj.optionId:
                    update_obj.status = obj.status
                    res = ImplementationObjective.update_objective(app=self.app, obj=update_obj)
                    if res.status_code != 200:
                        self.warning("Unable to update objective: %s", update_obj)

        component_implementations = []
        with component_progess as progress:
            fetching_components = progress.add_task(
                f"[#ffa500]Fetching {len(self.existing_components)} component(s) from RegScale...",
                total=len(self.existing_components),
            )
            for component in self.existing_components:
                # Create a list of all component implementations
                component_implementations.extend(
                    self.get_implementations(parent_id=component["id"], parent_module="components")
                )
                progress.advance(fetching_components, 1)
        # Create a list of all SSP implementations
        ssp_control_implementations = self.get_implementations(
            parent_id=self.regscale_ssp, parent_module="securityplans"
        )
        self.logger.info(
            "Updating %i control implementations for SSP #%i.",
            len(ssp_control_implementations),
            int(self.regscale_ssp),
        )
        updates = []
        self.logger.info("Analyzing %i SSP implementation(s)...", len(ssp_control_implementations))
        for _, imp in enumerate(ssp_control_implementations):
            component_objectives: list[ImplementationObjective] = []
            ssp_objectives: list[ImplementationObjective] = []
            ssp_implementation_status = ImplementationStatus.NOT_IMPLEMENTED.value
            implementation_dat: set[ImplementationObjective] = {
                dat for dat in self.all_implementation_objectives if dat.securityControlId == imp["controlID"]
            }
            if implementation_dat:
                ssp_objectives = {
                    item
                    for item in implementation_dat
                    if item.implementationId not in {imp["id"] for imp in component_implementations}
                }
                component_objectives = {
                    item
                    for item in implementation_dat
                    if item.implementationId in {imp["id"] for imp in component_implementations}
                }
            cntr = Counter([obj.status for obj in component_objectives])
            if len(cntr) > 0 and cntr[ImplementationStatus.FULLY_IMPLEMENTED.value] == cntr.total():
                ssp_implementation_status = ImplementationStatus.FULLY_IMPLEMENTED.value

            for obj in component_objectives:
                process_ssp_objectives(obj)

            # Update the SSP implementation
            imp["status"] = ssp_implementation_status
            entries_to_remove = [
                "createdBy",
                "lastUpdatedBy",
                "controlOwner",
                "systemRoles",
            ]
            for k in entries_to_remove:
                imp.pop(k, None)
            updates.append(imp)
        count = 0
        size = 50
        update_len = len(updates)
        while len(updates) > 0:
            if len(updates) > 0:
                self.logger.debug("Updated %i of %i SSP implementations", count, update_len)
                with ThreadPoolExecutor(max_workers=5) as imp_executor:
                    batch = updates[:size]
                    updates = updates[size:]
                    # batchUpdate broke, switched to put
                    for imp in batch:
                        imp_executor.submit(
                            self.api.put,
                            url=self.app.config["domain"] + f"/api/controlimplementation/{imp['id']}",
                            json=imp,
                        )
                    count += len(batch)
        self.logger.info("%i SSP implementation(s) updated.", count)

    def update_component_implementation_objectives(self) -> None:
        """
        Update the implementation objectives for each component

        :rtype: None
        """
        all_assets = []
        all_checklists = []
        insert_objs = []
        update_objs = []
        # Refresh catalog details
        self.query_catalog_details()
        # TODO: Use cache here
        self.refresh_implementation_objectives()
        with component_progess as progress:
            process_imps = progress.add_task(
                f"[#ffa500]Processing implementation objective(s) for {len(self.existing_components)} components...",
                total=len(self.existing_components),
            )
            for component in self.existing_components:
                component_assets_response = self.api.get(
                    url=self.config["domain"] + f"/api/assets/getAllByParent/{component['id']}/components"
                )
                if component_assets_response.status_code == 204:  # No Assets, move on.
                    progress.advance(process_imps, advance=1)
                    continue
                component_assets = component_assets_response.json()
                all_assets.extend(component_assets)
                for asset in component_assets:
                    # Fetch all checklists for an asset.
                    all_checklists.extend(
                        self.api.get(
                            url=self.config["domain"] + f"/api/securityChecklist/getAllByParent/{asset['id']}"
                        ).json()
                    )
                for imp in self.get_implementations(parent_id=component["id"], parent_module="components"):
                    if imp["id"] not in {imp["id"] for imp in self.all_implementations}:  # don't add duplicates
                        self.all_implementations.append(imp)
                progress.advance(process_imps, 1)

        # Refresh catalog details
        self.query_catalog_details()
        with component_progess as progress:
            process_imps = progress.add_task(
                f"[#ffa500]Processing {len(self.all_implementations)} implementation objective(s)...",
                total=len(self.all_implementations),
            )
            for imp in self.all_implementations:
                # Filter Control Objectives
                filtered_objectives = [
                    obj for obj in self.all_control_objectives if obj["securityControlId"] == imp["controlID"]
                ]
                new_objs, updated_objs = self.create_objectives(
                    implementation=imp,
                    control_objectives=filtered_objectives,
                    options=self.all_implementation_options,
                    all_checklists=all_checklists,
                )
                insert_objs.extend(new_objs)
                update_objs.extend(updated_objs)
                progress.advance(process_imps, 1)
        if update_objs or insert_objs:
            self.logger.info(
                "Attempting to Insert %i new implementation objectives and update %i existing implementation objectives",
                len(insert_objs),
                len(update_objs),
            )
            self.mass_update(update_objs=update_objs, insert_objs=insert_objs)
        else:
            self.logger.info("No objectives found to update or insert.")
        self.refresh_mega_api()

    def refresh_implementation_objectives(self) -> None:
        """
        Refresh all implementation objectives

        :rtype: None
        """
        # TODO: Refactor
        imp_start = time.perf_counter()
        self.all_implementation_objectives = []
        component_ids = [comp.id for comp in self.existing_components]
        query = """
        query GetImplementationObjective{
          controlImplementations (
            take: 50
            skip: 0
            where: {
              and: [{ parentId: { OPERATOR: COMPONENT_IDS } }, { parentModule: { eq: "PARENT_MODULE" } } {objectives: {any: true}}]
            }
          )
          {
            items {
              objectives {
                id
                uuid
                notes
                optionId
                status
                dateLastAssessed
                objectiveId
                securityControlId
                implementationId
                dateCreated
                dateLastUpdated
                lastUpdatedById
                createdById
              }
            }
            pageInfo {
             hasNextPage
            }
            totalCount
          }
        }
        """
        component_query = (
            query.replace("OPERATOR", "in")
            .replace("COMPONENT_IDS", str(component_ids))
            .replace("PARENT_MODULE", "components")
        )
        ssp_query = (
            query.replace("OPERATOR", "eq")
            .replace("COMPONENT_IDS", str(self.regscale_ssp))
            .replace("PARENT_MODULE", "securityplans")
        )
        ssp_results = self.api.graph(query=ssp_query)
        component_results = self.api.graph(query=component_query)
        results = [ssp_results, component_results]
        # Extend with Objectives
        for result in results:
            for obj_list in result["controlImplementations"]["items"]:
                self.all_implementation_objectives.extend(
                    ImplementationObjective(**obj) for obj in obj_list["objectives"]
                )
        imp_end = time.perf_counter()
        self.logger.info(
            "Refreshed %i implementation objectives in %f seconds",
            len(self.all_implementation_objectives),
            imp_end - imp_start,
        )

    def update_implementation(self, existing_imp: dict, status: str) -> None:
        """
        Update implementation in RegScale via API

        :param dict existing_imp: A dict of an existing implementation
        :param str status: The implementation status
        :rtpe: None
        """
        if existing_imp["status"] != status:
            existing_imp["status"] = status
            # Drop objectives section, not needed
            del existing_imp["objectives"]
            implementation_id = existing_imp["id"]
            response = self.api.put(
                url=self.config["domain"] + f"/api/controlImplementation/{implementation_id}",
                json=existing_imp,
            )
            if not response.ok:
                self.self.logger.error("Unable to update Implementation: %s", existing_imp)

    def process_file(
        self,
        file: Path,
        all_control_objectives: list[dict],
        catalog_controls: list[dict],
        existing_assets: set[Asset],
    ) -> None:
        """
        Process a STIG file

        :param Path file: The file path to the STIG file for parsing
        :param list[dict] all_control_objectives: A list of control objectives
        :param list[dict] catalog_controls: A list of catalog controls
        :param set[Asset] existing_assets: A set of existing assets
        :rtype: None
        """
        self.parse_stig(
            file,
            self.regscale_ssp,
            all_control_objectives,
            catalog_controls,
            existing_assets,
        )

    def parse_stig(
        self,
        file_path: Path,
        ssp_id: int,
        control_objectives: list[dict],
        security_controls: list[dict],
        existing_assets: set[Asset],
    ) -> STIG_FILE:
        """Parse Stig

        :param Path file_path: The file path to the STIG file
        :param int ssp_id: The RegScale SSP ID
        :param list[dict] control_objectives: A list of control objectives
        :param list[dict] security_controls: A list of security controls
        :param set[Asset] existing_assets: A list of existing assets, defaults to []
        :return: STIG_FILE object
        :rtype: STIG_FILE
        """

        # Pull down latest 800-53 rev4, drop all current objectives,
        # replace with the CCIs (make the CCIs an objective),
        # load into RegScale,
        # pull down new JSON file
        # and we will publish a DoD version

        stig_obj = None
        # check_powershell(app)
        self.logger.debug("Processing file: %s", str(file_path.absolute()))
        # retrieve security plan
        security_plan_url = normalize_url(self.config["domain"] + f"/api/securityplans/{ssp_id}")
        self.logger.debug(f"Retrieving SSP {security_plan_url}")
        securityplan_response = self.api.get(security_plan_url)
        self.logger.debug(f"securityplan_response.status_code: {securityplan_response.status_code}")

        if securityplan_response.status_code == 404:
            self.logger.error(f"Process failed. Security plan #{ssp_id} not found on RegScale server. Exiting...")
            exit()
        elif securityplan_response.status_code == 401:
            self.logger.error(
                "Unable to Authenticate to RegScale Server. Execute `regscale login` for a fresh token. Exiting..."
            )
            exit()
        elif securityplan_response.status_code != 200:
            self.logger.error(
                f"Unable to retrieve Security Plan #{ssp_id}. HTTP Status Code: {securityplan_response.status_code}. "
                f"Exiting..."
            )
            exit()
        else:
            # found security plan (status_code == 200), process STIG file
            stig_obj = STIG_FILE(
                file_path=file_path.absolute(),
                app=self.app,
                ssp_id=ssp_id,
                control_objectives=control_objectives,
                security_controls=security_controls,
                mapping=self.cci_mapping,
                assets=existing_assets,
                control_implementations=self.all_implementations,
            )
        return stig_obj

    def post_options(self, options: list[ImplementationOptionDeprecated]) -> None:
        """Post Implementation Option to RegScale

        :param list[ImplementationOptionDeprecated] options: A list of Implementation Options
        :rtype: None
        """
        if new_options := [opt.dict() for opt in options if opt not in self.all_implementation_options]:
            with component_progess as progress:
                posting_opts = progress.add_task(
                    f"[#ffa500]Posting {len(new_options)} new implementation option(s) to RegScale...",
                    total=len(new_options),
                )
                # process in batches of 1000
                for i in range(0, len(new_options), 1000):
                    response = self.api.post(
                        url=self.config["domain"] + "/api/implementationOptions/batchcreate",
                        json=new_options[i : i + 1000],
                    )
                    self.refresh_options()
                    progress.advance(posting_opts, len(new_options[i : i + 1000]))
                    if not response.raise_for_status():
                        self.logger.debug(
                            "Created a New Implementation Option: %s",
                            (dumps(response.json(), indent=2)),
                        )

    def refresh_options(self) -> None:
        """
        Refresh all implementation options

        :rtype: None
        """
        self.query_catalog_details()
        self.all_implementation_options.clear()
        for cat in self.catalog_details:
            # update option id
            # duplicate the set of options, update, and then replace
            for opt in cat["options"]:
                self.all_implementation_options.add(ImplementationOptionDeprecated(**opt))

    def refresh_existing_components(self) -> None:
        """
        Refresh existing components

        :rtype: None
        """
        self.existing_components.clear()
        comps = Component.get_components_from_ssp(app=self.app, ssp_id=self.regscale_ssp)
        for cmp in comps:
            self.existing_components.add(Component(**cmp))

    def check_components(self) -> None:
        """
        Create Hardware/Software pair of components, if necessary

        :rtype: None
        """
        self.refresh_existing_components()
        new_comps = set()

        def post_mapping(mapping: dict) -> None:
            """
            Post a component mapping from a successful component response

            :param dict mapping: A component mapping
            :rtype: None
            """
            self.api.post(
                url=self.config["domain"] + "/api/componentMapping",
                json=mapping,
            )

        def gen_component(file: Path) -> bool:
            """
            Create a new component object

            :param Path file: file Path
            :return: True
            :rtype: bool
            """
            _, _, title = self._get_metadata(file)
            titles = {cmp.title for cmp in self.existing_components}
            if title not in titles:
                component = Component(
                    title=title,  # TODO: STIG_NAME - Hardware
                    description=title,
                    componentType="hardware",
                    componentOwnerId=self.config["userId"],
                    securityPlansId=self.regscale_ssp,
                )
                if component:
                    new_comps.add(component)
            return True

        def post_component(component: Component) -> None:
            """
            Post a new component to RegScale

            :param Component component: A new component
            :rtype: None
            """
            # Need to check if component exists on the first run, subsequent runs will be handled by the above method.
            if component.title not in {comp.title for comp in self.existing_components}:
                response = self.api.post(self.config["domain"] + "/api/components", json=component.dict())
                if response.status_code == 200:
                    self.existing_components.add(Component(**response.json()))
            return None

        with component_progess:
            title_task = component_progess.add_task(
                f"[#FBFBA1]Processing {len(self.files)} file(s) and building components...",
                total=len(self.files),
            )

            with ThreadPoolExecutor() as title_pool:
                # Generate Components of a list of titles
                futures = [title_pool.submit(gen_component, file) for file in self.files]
                for future in as_completed(futures):
                    if future.done():
                        component_progess.update(title_task, advance=1)
            new_mappings = []
            if new_comps:
                comp_task = component_progess.add_task(
                    f"[#FBFBA1]Posting {len(new_comps)} new component(s) to RegScale...",
                    total=len(new_comps),
                )
                with ThreadPoolExecutor(max_workers=10) as component_pool:
                    # Prone to race conditions on inserting new items with a lack of FK/Unique contraints, be careful
                    # Process each file
                    futures = [component_pool.submit(post_component, comp) for comp in new_comps]
                    for _ in as_completed(futures):
                        component_progess.update(comp_task, advance=1)
                self.refresh_existing_components()
                with ThreadPoolExecutor(max_workers=5) as mapping_pool:
                    # Prone to race conditions on inserting new items with a lack of FK/Unique contraints, be careful
                    # Process each file
                    mapping_task = component_progess.add_task(
                        f"[#FBFBA1]Posting {len(new_comps)} new component mapping(s) to RegScale...",
                        total=len(new_comps),
                    )
                    for comp in self.existing_components:
                        mapping = {
                            "componentId": comp["id"],
                            "securityPlanId": self.regscale_ssp,
                        }
                        new_mappings.append(mapping)
                    futures = [mapping_pool.submit(post_mapping, map) for map in new_mappings]
                    for future in as_completed(futures):
                        if future.done():
                            component_progess.update(mapping_task, advance=1)

    def update_options(self) -> None:
        """
        Create or update all the Implementation Options this integration will need

        :rtype: None
        """
        self.logger.info("Updating Options")

        opts = []

        # Get All CCI Objectives
        for cat in self.catalog_details:
            for opt in cat["options"]:
                self.all_implementation_options.add(ImplementationOptionDeprecated(**opt))
        # Create two options per objective if they do not exist
        for obj in self.all_control_objectives:
            # Check to see if option exists, if not build it
            options = [
                opt for opt in self.all_implementation_options if opt.securityControlId == obj["securityControlId"]
            ]
            names = {name.name for name in options}
            if "Not Implemented Option" not in names:
                # Create Not Implemented Option
                opt = ImplementationOptionDeprecated(
                    id=0,
                    uuid=None,
                    createdById=self.config["userId"],
                    dateCreated=get_current_datetime(),
                    lastUpdatedById=self.config["userId"],
                    dateLastUpdated=get_current_datetime(),
                    name="Not Implemented Option",
                    description=ImplementationStatus.NOT_IMPLEMENTED.value,
                    archived=False,
                    securityControlId=obj["securityControlId"],
                    objectiveId=obj["id"],
                    otherId="",
                    acceptability=ImplementationStatus.NOT_IMPLEMENTED.value,
                )
                opts.append(opt)
            if "Fully Implemented Option" not in names:
                # Create Fully Implemented Option
                opt = ImplementationOptionDeprecated(
                    id=0,
                    uuid=None,
                    createdById=self.config["userId"],
                    dateCreated=get_current_datetime(),
                    lastUpdatedById=self.config["userId"],
                    dateLastUpdated=get_current_datetime(),
                    name="Fully Implemented Option",
                    description=ImplementationStatus.FULLY_IMPLEMENTED.value,
                    archived=False,
                    securityControlId=obj["securityControlId"],
                    objectiveId=obj["id"],
                    otherId="",
                    acceptability=ImplementationStatus.FULLY_IMPLEMENTED.value,
                )
                opts.append(opt)
        if opts:
            self.logger.info("Posting %i new implementation options", len(opts))
            self.post_options(options=opts)
            # Refresh mega data and catalog data if we actually posted something
            self.refresh_mega_api()
            self.query_catalog_details()

    def get_catalog_id(
        self,
    ) -> int:
        """Return the RegScale Catalogue ID

        :raises ValueError: If more than one catalog is used by this SSP
        :return: A catalog id
        :rtype: int
        """
        if self.regscale_dod_catalog_id:
            return self.regscale_dod_catalog_id
        cats = [cat["catalog"] for cat in self.catalog_details]

        if len(cats) > 1:
            raise ValueError("More than one catalog used by this SSP, unable to continue.")
        else:
            return cats.pop()

    def get_implementations(self, parent_id: int, parent_module: str = "components") -> list[dict]:
        """Return a list of control implementations by parent

        :param int parent_id: Parent ID
        :param str parent_module: Parent Module in RegScale, defaults to "components"
        :return: A list of control implementations
        :rtype: list[dict]
        """
        control_implementations = []
        response = self.api.get(
            self.config["domain"] + f"/api/controlimplementation/getAllByParent/{parent_id}/{parent_module}"
        )
        if response.ok:
            control_implementations = response.json()
        return control_implementations

    def get_security_controls(self) -> Tuple[int, list[dict]]:
        """Fetch a list of security controls by catalog, return controls and catalog id.

        :return: A tuple of catalog id and a list of security controls
        :rtype: Tuple[int, list[dict]]
        """
        cat_id = self.get_catalog_id()
        security_controls = []
        self.logger.info("Querying Additional Catalog details, this may also take a while..")
        self.query_catalog_details()
        self.logger.info("Done!")
        for cat in self.catalog_details:
            security_controls.extend(cat["controls"])
        return cat_id, security_controls

    def get_control_objective(self, security_control_id: int) -> list[dict]:
        """
        Fetch a list of control objectives by security control ID

        :param int security_control_id: Security control ID to get controls for
        :return: A list of control objectives with the associated security control ID
        :rtype: list[dict]
        """
        control_objectives = [obj for obj in self.mega_data if obj["securityControlId"] == security_control_id]
        return control_objectives

    def get_control_objectives(self) -> list[dict]:
        """
        Fetch a list of control objectives by existing_components

        :return: A list of control objectives
        :rtype: list[dict]
        """
        control_implementations = []
        control_objectives = []
        for component in self.existing_components:
            control_implementations.extend(
                self.get_implementations(parent_id=component["id"], parent_module="components")
            )
        for control in control_implementations:
            control_objectives.extend(self.get_control_objective(control["controlID"]))
        return control_objectives

    def pull_fresh_asset_list(self) -> set[Asset]:
        """
        Pull all assets from RegScale via API

        :return: A list of assets
        :rtype: set[Asset]
        """
        existing_assets: set[Asset] = set()
        for component in self.existing_components:
            existing_asset_response = self.api.get(
                self.config["domain"] + f"/api/assets/getAllByParent/{component['id']}/components"
            )
            if existing_asset_response.ok and existing_asset_response.status_code != 204:  # Empty content is 204
                for asset in existing_asset_response.json():
                    existing_assets.update({Asset(**asset)})

        return existing_assets

    def _get_metadata(self, file: Path) -> Tuple[dict, dict, str]:
        """
        Return metadata and title from a STIG file

        :param Path file: A file path.
        :return: Tuple of metadata (dict) and title
        :rtype: Tuple[dict, dict, str]
        """
        metadata = {}
        obj = {}
        title = ""
        with open(file, "r", encoding="utf-8"):
            obj = xml_file_to_dict(file)
            metadata = obj["CHECKLIST"]["STIGS"]["iSTIG"]["STIG_INFO"]["SI_DATA"]
            title = (
                [dat["SID_DATA"] for dat in metadata if dat["SID_NAME"] == "title"][0]
                .replace("Security Technical Implementation Guide", "")
                .strip()
            )
        return obj, metadata, title

    @classmethod
    def _get_asset_category(cls, obj_asset: dict) -> str:
        """
        Returns the asset category based on the asset type

        :param dict obj_asset: A dict of an asset
        :return: The asset category, either "Hardware" or "Software"
        :rtype: str
        """
        return "Hardware" if obj_asset["ASSET_TYPE"] == "Computing" else "Software"

    @classmethod
    def get_category_components(cls, existing_components: set, asset_category: str) -> list[dict]:
        """
        Returns a list of components that match the asset category

        :param set existing_components: A set of existing components
        :param str asset_category: The asset category
        :return: A list of components
        :rtype: list[dict]
        """
        return [
            component
            for component in existing_components
            if component["componentType"].lower() == asset_category.lower()
        ]

    @staticmethod
    def get_cci_from_rule(rule: dict) -> Optional[Any]:
        """
        Returns the CCI reference from a STIG rule

        :param dict rule: A STIG rule
        :return: A CCI reference
        :rtype: Optional[Any]
        """
        for key in ["VULN_ATTRIBUTE", "ATTRIBUTE_DATA"]:
            if isinstance(rule, dict) and key not in rule.keys():
                return None
            if rule[key] is None:
                return None
        if rule["VULN_ATTRIBUTE"].lower() == "cci_ref" and "CCI" in rule["ATTRIBUTE_DATA"]:
            return rule["ATTRIBUTE_DATA"]
        return None

    @classmethod
    def get_cci_from_vuln(cls, vuln: Any) -> Optional[Any]:
        """
        Returns the CCI reference from a STIG vulnerability

        :param Any vuln: A STIG vulnerability
        :return: A CCI reference
        :rtype: Optional[Any]
        """
        if isinstance(vuln, dict) and isinstance(vuln["STIG_DATA"], list):
            for rule in vuln["STIG_DATA"]:
                cci = cls.get_cci_from_rule(rule)
                if cci is not None:
                    return cci
        elif isinstance(vuln, str):
            try:
                ccis = [dat["ATTRIBUTE_DATA"] for dat in vuln["STIG_DATA"] if cls.get_cci_from_rule(dat) is not None]
                if ccis:
                    cci = ccis[0]
                return cci
            except (IndexError, TypeError):
                cls.create_logger().warning("Unable to process asset from this ckl property: %s", vuln)
        return None

    @classmethod
    def get_cci_refs(cls, stig_vulns: list[dict]) -> set[str]:
        """
        Returns a set of CCI references from a list of STIG vulnerabilities

        :param list[dict] stig_vulns: A list of STIG vulnerabilities
        :return: A set of CCI references
        :rtype: set[str]
        """
        cci_set = set()
        for vuln in stig_vulns:
            cci = cls.get_cci_from_vuln(vuln)
            if cci is not None:
                cci_set.add(cci)
        return cci_set

    def build_asset_from_file(self, file: str) -> Optional[Tuple[list[str], Optional[Asset]]]:
        """
        Builds an asset from a file

        :param str file: A file path as a string
        :return: A tuple of STIG vulnerabilities and an asset
        :rtype: Optional[Tuple[list[str], Optional[Asset]]]
        """
        obj, _, title = self._get_metadata(file)
        obj_asset = obj["CHECKLIST"]["ASSET"]
        asset_category = self._get_asset_category(obj_asset)
        category_components = self.get_category_components(self.existing_components, asset_category)
        stig_vulns = obj["CHECKLIST"]["STIGS"]["iSTIG"]["VULN"]
        mac = obj_asset["HOST_MAC"].upper() if validate_mac_address(obj_asset["HOST_MAC"]) else None
        if "HOST_IP" in obj_asset.keys() and obj_asset["HOST_IP"]:
            components = [cat["id"] for cat in category_components if cat["title"].lower() == f"{title.lower()}"]
            if components:
                component_id = components.pop()
            else:
                return None
            new_asset = Asset(
                name=title,
                status="Active (On Network)",
                assetOwnerId=self.app.config["userId"],
                assetCategory=asset_category,
                description=format_data_to_html(obj_asset),
                ipAddress=obj_asset["HOST_IP"],
                macAddress=mac,
                assetType="Other",
                parentId=component_id,
                parentModule="components",
                fqdn=obj_asset["HOST_FQDN"],
                otherTrackingNumber=obj_asset["TARGET_KEY"],
            )
            return stig_vulns, new_asset
        return stig_vulns, None

    def build_assets(self) -> Tuple[list[str], set[Asset]]:
        """
        Builds assets from a list of .ckl files

        :return: A list of CCI references and a list of existing assets
        :rtype: Tuple[list[str], set[Asset]]
        """
        cci_set = set()

        # Function to process a single file

        def insert_asset_and_mapping(new_asset):
            res = Asset.insert_asset(app=self.app, obj=new_asset.dict())
            mapping = {}
            mapping_res = None
            if res.ok:
                # Post mapping
                mapping = {
                    "assetId": res.json()["id"],
                    "componentId": new_asset.parentId,
                }
                mapping_res = self.api.post(url=self.config["domain"] + "/api/assetmapping", json=mapping)
            return res, mapping_res, mapping

        # Use ThreadPoolExecutor to run tasks in parallel
        with asset_progress:
            existing_assets = self.pull_fresh_asset_list()
            asset_task = asset_progress.add_task(
                f"[#FBFBA1]Processing {len(self.files)} file(s) and building assets...",
                total=len(self.files),
            )
            with ThreadPoolExecutor() as executor:
                futures = []
                res_futures = []
                new_assets = []
                # Build asset list
                for file in self.files:
                    futures.append(executor.submit(self.build_asset_from_file, file))
                for future in as_completed(futures):
                    # Append to new assets list so we can post unique assets
                    # check if asset exists, if not append to new_assets
                    if future.result():
                        new_asset = future.result()[1]
                        cci_set.update(self.get_cci_refs(future.result()[0]))
                    else:
                        self.logger.warning("Unable to build asset.")
                    if new_asset and new_asset not in existing_assets:
                        new_assets.append(new_asset)
                    asset_progress.advance(asset_task, 1)
                    # Populate the CCI set with CCI names
                if new_assets:
                    insert_task = asset_progress.add_task(
                        f"[#FBFBA1]Inserting {len(new_assets)} new asset(s)...",
                        total=len(new_assets),
                    )
                    for asset in new_assets:
                        res_futures.append(executor.submit(insert_asset_and_mapping, asset))
                    for future in as_completed(res_futures):
                        if future.done():
                            asset_progress.advance(insert_task, 1)
        existing_assets = self.pull_fresh_asset_list()  # This is probably slow
        return list(cci_set), existing_assets

    def query_catalog_details(self) -> None:
        """
        Query Catalog Details with information from Mega API

        :rtype: None
        """

        cats = set()
        details = []
        for normalized_control in self.mega_data["normalizedControls"]:
            cats.add(normalized_control["control"]["item3"]["catalogueID"])
        for cat in cats:
            details.append(
                self.api.get(url=self.config["domain"] + f"/api/catalogues/getCatalogWithAllDetails/{cat}").json()
            )
        self.catalog_details = details

    def process(self, regscale_ssp_id: click.INT) -> None:
        """
        Process Stig Files

        :param click.INT regscale_ssp_id: RegScale SSP ID
        :raises ValueError: A ValueError is raised if the SSP ID is invalid
        :rtype: None
        """
        if self.api.get(url=self.config["domain"] + f"/api/securityplans/{regscale_ssp_id}").status_code == 204:
            raise ValueError("Invalid SSP ID")
        # Build Components
        self.check_components()
        # Build Assets
        cci_list, existing_assets = self.build_assets()
        # Pull MegaAPI data
        self.refresh_mega_api()
        # Pull Catalog Details
        self.logger.info("Fetching catalog details...")
        self.query_catalog_details()
        try:
            cat_id = self.catalog_details[0]["controls"][0]["catalogueID"]
        except IndexError:
            error_and_exit("Unable to continue, no catalog details found")
        self.refresh_implementations(
            cci_list=cci_list,
            cat_id=cat_id,
        )
        # TODO: Loop through stigs and build component registry
        batch = 0
        for i in range(0, len(self.files), self.app.config["stigBatchSize"]):
            batch += 1
            self.logger.debug("Processing batch %i", batch)
            batch = self.files[i : i + self.app.config["stigBatchSize"]]
            # Code will need to be sync unless there are some database FK constraints
            for file in batch:
                self.process_file(
                    file,
                    self.all_control_objectives,
                    self.catalog_details[0]["controls"],
                    existing_assets,
                )

        # Update Implementation Options for all components
        opt_start = time.perf_counter()
        self.update_options()
        opt_end = time.perf_counter()
        self.logger.info(f"Processed options in {opt_end - opt_start:0.4f} seconds")
        comp_start = time.perf_counter()
        self.update_component_implementation_objectives()
        comp_end = time.perf_counter()
        self.logger.info(f"Processed component implementation objectives in {comp_end - comp_start:0.4f} seconds")
        self.logger.info("Processing Component Implementations...")
        comp_imp_start = time.perf_counter()
        self.update_component_implementations()
        comp_imp_end = time.perf_counter()
        self.logger.info(f"Processed component implementations in {comp_imp_end - comp_imp_start:0.4f} seconds")
        ssp_obj_start = time.perf_counter()
        self.logger.info("Processing SSP Implementation Objectives...")
        self.update_ssp_implementation_objectives()
        ssp_obj_end = time.perf_counter()
        self.logger.info(
            f"Processed ssp implementation objectives and implementations in {ssp_obj_end - ssp_obj_start:0.4f} seconds"
        )
        issue_start = time.perf_counter()
        self.logger.info("Processing SSP Issues...")
        self.update_ssp_issues()
        issue_end = time.perf_counter()
        self.logger.info(f"Processed ssp issues in {issue_end - issue_start:0.4f} seconds")
        self.logger.info("Done!")
