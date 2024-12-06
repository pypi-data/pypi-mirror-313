#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Scanner Integration Class """
from __future__ import annotations

import concurrent.futures
import dataclasses
import enum
import hashlib
import json
import logging
import re
import threading
import time
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Dict, Generic, Iterator, List, Optional, Set, TypeVar, Union

from rich.progress import Progress, TaskID

from regscale.core.app.application import Application
from regscale.core.app.utils.api_handler import APIHandler
from regscale.core.app.utils.app_utils import create_progress_object, get_current_datetime
from regscale.core.app.utils.catalog_utils.common import objective_to_control_dot
from regscale.core.utils.date import date_obj, date_str, datetime_str, days_from_today, get_day_increment
from regscale.integrations.commercial.stig_mapper.mapping_engine import StigMappingEngine as STIGMapper
from regscale.integrations.variables import ScannerVariables
from regscale.models import OpenIssueDict, ScanHistory, regscale_models
from regscale.utils.threading import ThreadSafeDict, ThreadSafeList

logger = logging.getLogger(__name__)

K = TypeVar("K")  # Key type
V = TypeVar("V")  # Value type


def get_thread_workers_max() -> int:
    """
    Get the maximum number of thread workers

    :return: The maximum number of thread workers
    :rtype: int
    """
    return ScannerVariables.threadMaxWorkers


def issue_due_date(
    severity: regscale_models.IssueSeverity,
    created_date: str,
    high: int = 60,
    moderate: int = 210,
    low: int = 364,
    title: str = "",
    config: Dict[str, Dict] = {},
) -> str:
    """
    Calculate the due date for an issue based on its severity and creation date.

    :param regscale_models.IssueSeverity severity: The severity of the issue.
    :param str created_date: The creation date of the issue.
    :param int high: Days until due for high severity issues. Default is 60.
    :param int moderate: Days until due for moderate severity issues. Default is 210.
    :param int low: Days until due for low severity issues. Default is 364.
    :param str title: The title of the Integration.
    :param Dict[str, Dict] config: Configuration options for the due date calculation.
    :return: The due date for the issue.
    :rtype: str
    """

    due_date_map = {
        regscale_models.IssueSeverity.High: high,
        regscale_models.IssueSeverity.Moderate: moderate,
        regscale_models.IssueSeverity.Low: low,
    }

    if title and config:
        # if title in a config key, use that key
        issues_dict = config.get("issues", {})
        matching_key = next((key.lower() for key in issues_dict if title.lower() in key.lower()), None)
        if matching_key:
            title_config = issues_dict.get(matching_key, {})
            due_date_map = {
                regscale_models.IssueSeverity.High: title_config.get("high", high),
                regscale_models.IssueSeverity.Moderate: title_config.get("moderate", moderate),
                regscale_models.IssueSeverity.Low: title_config.get("low", low),
            }

    days = due_date_map.get(severity, low)
    return date_str(get_day_increment(start=created_date, days=days))


class ManagedDefaultDict(Generic[K, V]):
    """
    A thread-safe default dictionary that uses a multiprocessing Manager.

    :param default_factory: A callable that produces default values for missing keys
    """

    def __init__(self, default_factory):
        self.store = ThreadSafeDict()
        self.default_factory = default_factory

    def __getitem__(self, key: Any) -> Any:
        """
        Get the item from the store

        :param Any key: Key to get the item from the store
        :return: Value from the store
        :rtype: Any
        """
        if key not in self.store:
            self.store[key] = self.default_factory()
        return self.store[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set the item in the store

        :param Any key: Key to set the item in the store
        :param Any value: Value to set in the store
        :rtype: None
        """
        self.store[key] = value

    def __contains__(self, key: Any) -> bool:
        """
        Check if the key is in the store

        :param Any key: Key to check in the store
        :return: Whether the key is in the store
        :rtype: bool
        """
        return key in self.store

    def __len__(self) -> int:
        """
        Get the length of the store

        :return: Number of items in the store
        :rtype: int
        """
        return len(self.store)

    def get(self, key: Any, default: Optional[Any] = None) -> Optional[Any]:
        """
        Get the value from the store

        :param Any key: Key to get the value from the store
        :param Optional[Any] default: Default value to return if the key is not in the store, defaults to None
        :return: The value from the store, or the default value
        :rtype: Optional[Any]
        """
        if key not in self.store:
            return default
        return self.store[key]

    def items(self) -> Any:
        """
        Get the items from the store

        :return: Items from the store
        :rtype: Any
        """
        return self.store.items()

    def keys(self) -> Any:
        """
        Get the keys from the store

        :return: Keys from the store
        :rtype: Any
        """
        return self.store.keys()

    def values(self) -> Any:
        """
        Get the values from the store

        :return: Values in the store
        :rtype: Any
        """
        return self.store.values()

    def update(self, *args, **kwargs) -> None:
        """
        Update the store

        :rtype: None
        """
        self.store.update(*args, **kwargs)


@dataclasses.dataclass
class IntegrationAsset:
    """
    Dataclass for integration assets.

    Represents an asset to be integrated, including its metadata and associated components.
    If a component does not exist, it will be created based on the names provided in ``component_names``.

    :param str name: The name of the asset.
    :param str identifier: A unique identifier for the asset.
    :param str asset_type: The type of the asset.
    :param str asset_category: The category of the asset.
    :param str component_type: The type of the component, defaults to ``ComponentType.Hardware``.
    :param Optional[int] parent_id: The ID of the parent asset, defaults to None.
    :param Optional[str] parent_module: The module of the parent asset, defaults to None.
    :param str status: The status of the asset, defaults to "Active (On Network)".
    :param str date_last_updated: The last update date of the asset, defaults to the current datetime.
    :param Optional[str] asset_owner_id: The ID of the asset owner, defaults to None.
    :param Optional[str] mac_address: The MAC address of the asset, defaults to None.
    :param Optional[str] fqdn: The Fully Qualified Domain Name of the asset, defaults to None.
    :param Optional[str] ip_address: The IP address of the asset, defaults to None.
    :param List[str] component_names: A list of strings that represent the names of the components associated with the
    asset, components will be created if they do not exist.
    """

    name: str
    identifier: str
    asset_type: str
    asset_category: str
    component_type: str = regscale_models.ComponentType.Hardware
    parent_id: Optional[int] = None
    parent_module: Optional[str] = None
    status: str = "Active (On Network)"
    date_last_updated: str = dataclasses.field(default_factory=get_current_datetime)
    asset_owner_id: Optional[str] = None
    mac_address: Optional[str] = None
    fqdn: Optional[str] = None
    ip_address: Optional[str] = None
    component_names: List[str] = dataclasses.field(default_factory=list)

    # Additional fields from Wiz integration
    external_id: Optional[str] = None
    management_type: Optional[str] = None
    software_vendor: Optional[str] = None
    software_version: Optional[str] = None
    software_name: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    other_tracking_number: Optional[str] = None
    serial_number: Optional[str] = None
    asset_tag_number: Optional[str] = None
    is_public_facing: Optional[bool] = None
    azure_identifier: Optional[str] = None
    disk_storage: Optional[int] = None
    cpu: Optional[int] = None
    ram: Optional[int] = None
    operating_system: Optional[str] = None
    os_version: Optional[str] = None
    end_of_life_date: Optional[str] = None
    vlan_id: Optional[str] = None
    uri: Optional[str] = None
    aws_identifier: Optional[str] = None
    google_identifier: Optional[str] = None
    other_cloud_identifier: Optional[str] = None
    patch_level: Optional[str] = None
    cpe: Optional[str] = None

    source_data: Optional[Dict[str, Any]] = None
    url: Optional[str] = None
    ports_and_protocols: List[Dict[str, Any]] = dataclasses.field(default_factory=list)
    software_inventory: List[Dict[str, Any]] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class IntegrationFinding:
    """
    Dataclass for integration findings.

    :param list[str] control_labels: A list of control labels associated with the finding.
    :param str title: The title of the finding.
    :param str category: The category of the finding.
    :param regscale_models.IssueSeverity severity: The severity of the finding, based on regscale_models.IssueSeverity.
    :param str description: A description of the finding.
    :param regscale_models.ControlTestResultStatus status: The status of the finding, based on
    regscale_models.ControlTestResultStatus.
    :param str pri[ority: The priority of the finding, defaults to "Medium".
    :param str issue_type: The type of issue, defaults to "Risk".
    :param str issue_title: The title of the issue, defaults to an empty string.
    :param str date_created: The creation date of the finding, defaults to the current datetime.
    :param str due_date: The due date of the finding, defaults to 60 days from the current datetime.
    :param str date_last_updated: The last update date of the finding, defaults to the current datetime.
    :param str external_id: An external identifier for the finding, defaults to an empty string.
    :param str gaps: A description of any gaps identified, defaults to an empty string.
    :param str observations: Observations related to the finding, defaults to an empty string.
    :param str evidence: Evidence supporting the finding, defaults to an empty string.
    :param str identified_risk: The risk identified by the finding, defaults to an empty string.
    :param str impact: The impact of the finding, defaults to an empty string.
    :param str recommendation_for_mitigation: Recommendations for mitigating the finding, defaults to an empty string.
    :param str asset_identifier: The identifier of the asset associated with the finding, defaults to an empty string.
    :param Optional[str] cci_ref: The Common Configuration Enumeration reference for the finding, defaults to None.
    :param str rule_id: The rule ID of the finding, defaults to an empty string.
    :param str rule_version: The version of the rule associated with the finding, defaults to an empty string.
    :param str results: The results of the finding, defaults to an empty string.
    :param Optional[str] comments: Additional comments related to the finding, defaults to None.
    :param str baseline: The baseline of the finding, defaults to an empty string.
    :param str poam_comments: Comments related to the Plan of Action and Milestones (POAM) for the finding, defaults to
    :param Optional[int] vulnerability_id: The ID of the vulnerability associated with the finding, defaults to None.
    an empty string.
    :param Optional[str] basis_for_adjustment: The basis for adjusting the finding, defaults to None.
    :param Optional[str] vulnerability_number: STIG vulnerability number
    """

    control_labels: List[str]
    title: str
    category: str
    plugin_name: str
    severity: regscale_models.IssueSeverity
    description: str
    status: Union[regscale_models.ControlTestResultStatus, regscale_models.ChecklistStatus, regscale_models.IssueStatus]
    priority: str = "Medium"

    # Vulns
    first_seen: str = dataclasses.field(default_factory=get_current_datetime)
    last_seen: str = dataclasses.field(default_factory=get_current_datetime)
    cve: Optional[str] = None
    cvss_v3_score: Optional[float] = None
    cvss_v2_score: Optional[float] = None
    ip_address: Optional[str] = None
    plugin_id: Optional[str] = None
    dns: Optional[str] = None
    severity_int: int = 0

    # Issues
    issue_title: str = ""
    issue_type: str = "Risk"
    date_created: str = dataclasses.field(default_factory=get_current_datetime)
    date_last_updated: str = dataclasses.field(default_factory=get_current_datetime)
    due_date: str = dataclasses.field(default_factory=lambda: date_str(days_from_today(60)))
    external_id: str = ""
    gaps: str = ""
    observations: str = ""
    evidence: str = ""
    identified_risk: str = ""
    impact: str = ""
    recommendation_for_mitigation: str = ""
    asset_identifier: str = ""
    comments: Optional[str] = None

    poam_comments: Optional[str] = None
    vulnerability_id: Optional[int] = None

    # Stig
    cci_ref: Optional[str] = None
    rule_id: str = ""
    rule_version: str = ""
    results: str = ""
    baseline: str = ""
    vulnerability_number: str = ""
    oval_def: str = ""
    scan_date: str = ""
    rule_id_full: str = ""
    group_id: str = ""

    # Wiz
    vulnerable_asset: Optional[str] = None
    remediation: Optional[str] = None
    cvss_score: Optional[float] = None
    cvs_sv3_base_score: Optional[float] = None
    source_rule_id: Optional[str] = None
    vulnerability_type: Optional[str] = None

    # CoalFre POAM
    basis_for_adjustment: Optional[str] = None

    def __eq__(self, other: Any) -> bool:
        """
        Check if the finding is equal to another finding

        :param Any other: The other finding to compare
        :return: Whether the findings are equal
        :rtype: bool
        """
        if not isinstance(other, IntegrationFinding):
            return NotImplemented
        return (self.title, self.category, self.external_id) == (other.title, other.category, other.external_id)

    def __hash__(self) -> int:
        """
        Get the hash of the finding

        :return: Hash of the finding
        :rtype: int
        """
        return hash((self.title, self.category, self.external_id))


class ScannerIntegrationType(str, enum.Enum):
    """
    Enumeration for scanner integration types.
    """

    CHECKLIST = "checklist"
    CONTROL_TEST = "control_test"
    VULNERABILITY = "vulnerability"


class ScannerIntegration(ABC):
    """
    Abstract class for scanner integrations.

    :param int plan_id: The ID of the security plan
    :param int tenant_id: The ID of the tenant, defaults to 1
    """

    stig_mapper = None
    # Basic configuration options
    options_map_assets_to_components: bool = False
    type: ScannerIntegrationType = ScannerIntegrationType.CONTROL_TEST
    title: str = "Scanner Integration"
    asset_identifier_field: str = ""
    _max_poam_id: Optional[int] = None  # Value holder for get_max_poam_id

    # Progress trackers
    asset_progress: Progress
    finding_progress: Progress

    # Processing counts
    num_assets_to_process: Optional[int] = None
    num_findings_to_process: Optional[int] = None

    # Lock registry
    _lock_registry: ThreadSafeDict = ThreadSafeDict()
    _global_lock = threading.Lock()  # Class-level lock

    # Error handling
    errors: List[str] = []

    # Mapping dictionaries
    finding_status_map: dict[Any, regscale_models.ChecklistStatus] = {}
    finding_severity_map: dict[Any, regscale_models.IssueSeverity] = {}
    issue_to_vulnerability_map: dict[regscale_models.IssueSeverity, regscale_models.VulnerabilitySeverity] = {
        regscale_models.IssueSeverity.Low: regscale_models.VulnerabilitySeverity.Low,
        regscale_models.IssueSeverity.Moderate: regscale_models.VulnerabilitySeverity.Medium,
        regscale_models.IssueSeverity.High: regscale_models.VulnerabilitySeverity.High,
    }
    asset_map: dict[str, regscale_models.Asset] = {}
    # cci_to_control_map: dict[str, set[int]] = {}
    control_implementation_id_map: dict[str, int] = {}
    control_map: dict[int, str] = {}
    control_id_to_implementation_map: dict[int, int] = {}

    # Existing issues map
    existing_issue_ids_by_implementation_map: dict[int, List[OpenIssueDict]] = defaultdict(list)

    # Scan Date
    scan_date: str = ""
    enable_finding_date_update = False

    def __init__(
        self,
        plan_id: int,
        tenant_id: int = 1,
    ):
        """
        Initialize the ScannerIntegration.

        :param int plan_id: The ID of the security plan
        :param int tenant_id: The ID of the tenant, defaults to 1
        """
        self.app = Application()
        self.alerted_assets: Set[str] = set()
        self.regscale_version: str = regscale_models.Issue._api_handler.regscale_version
        logger.info(f"RegScale Version: {self.regscale_version}")
        self.plan_id: int = plan_id
        self.tenant_id: int = tenant_id
        self.components: ThreadSafeList[Any] = ThreadSafeList()
        self.asset_map_by_identifier: ThreadSafeDict[str, regscale_models.Asset] = ThreadSafeDict()
        self.software_to_create: ThreadSafeList[regscale_models.SoftwareInventory] = ThreadSafeList()
        self.software_to_update: ThreadSafeList[regscale_models.SoftwareInventory] = ThreadSafeList()
        self.data_to_create: ThreadSafeList[regscale_models.Data] = ThreadSafeList()
        self.data_to_update: ThreadSafeList[regscale_models.Data] = ThreadSafeList()
        self.link_to_create: ThreadSafeList[regscale_models.Link] = ThreadSafeList()
        self.link_to_update: ThreadSafeList[regscale_models.Link] = ThreadSafeList()

        self.existing_issues_map: ThreadSafeDict[int, List[regscale_models.Issue]] = ThreadSafeDict()
        self.components_by_title: ThreadSafeDict[str, regscale_models.Component] = ThreadSafeDict()
        self.control_tests_map: ManagedDefaultDict[int, regscale_models.ControlTest] = ManagedDefaultDict(list)

        self.implementation_objective_map: ThreadSafeDict[str, int] = ThreadSafeDict
        self.implementation_option_map: ThreadSafeDict[str, int] = ThreadSafeDict
        self.control_implementation_map: ThreadSafeDict[int, regscale_models.ControlImplementation] = ThreadSafeDict

        self.control_implementation_id_map = regscale_models.ControlImplementation.get_control_label_map_by_plan(
            plan_id=plan_id
        )
        self.control_map = {v: k for k, v in self.control_implementation_id_map.items()}
        self.existing_issue_ids_by_implementation_map = regscale_models.Issue.get_open_issues_ids_by_implementation_id(
            plan_id=plan_id
        )  # GraphQL Call
        self.control_id_to_implementation_map = regscale_models.ControlImplementation.get_control_id_map_by_plan(
            plan_id=plan_id
        )
        self.cci_to_control_map: ThreadSafeDict[str, set[int]] = ThreadSafeDict()
        self._no_ccis: bool = False
        self.cci_to_control_map_lock: threading.Lock = threading.Lock()

        self.assessment_map: ThreadSafeDict[int, regscale_models.Assessment] = ThreadSafeDict()
        self.assessor_id: str = self.get_assessor_id()
        self.asset_progress: Progress = create_progress_object()
        self.finding_progress: Progress = create_progress_object()
        self.stig_mapper = self.load_stig_mapper()

    @classmethod
    def _get_lock(cls, key: str) -> threading.RLock:
        """
        Get or create a lock associated with a key.

        :param str key: The cache key
        :return: A reentrant lock
        :rtype: RLock
        """
        lock = cls._lock_registry.get(key)
        if lock is None:
            with cls._global_lock:  # Use a class-level lock to ensure thread safety
                lock = cls._lock_registry.get(key)
                if lock is None:
                    lock = threading.RLock()
                    cls._lock_registry[key] = lock
        return lock

    @staticmethod
    def load_stig_mapper() -> Optional[STIGMapper]:
        """
        Load the STIG Mapper file

        :return: None
        """
        from os import path

        stig_mapper_file = ScannerVariables.stigMapperFile
        if not path.exists(stig_mapper_file):
            return None
        try:
            stig_mapper = STIGMapper(json_file=stig_mapper_file)
            return stig_mapper
        except Exception as e:
            logger.debug(f"Warning Unable to loading STIG Mapper file: {e}")
        return None

    @staticmethod
    def get_assessor_id() -> str:
        """
        Gets the ID of the assessor

        :return: The ID of the assessor
        :rtype: str
        """

        api_handler = APIHandler()
        return api_handler.get_user_id()

    def get_cci_to_control_map(self) -> ThreadSafeDict[str, set[int]] | dict:
        """
        Gets the CCI to control map

        :return: The CCI to control map
        :rtype: ThreadSafeDict[str, set[int]] | dict
        """
        if self._no_ccis:
            return self.cci_to_control_map
        with self.cci_to_control_map_lock:
            if any(self.cci_to_control_map):
                return self.cci_to_control_map
            logger.info("Getting CCI to control map...")
            self.cci_to_control_map = regscale_models.map_ccis_to_control_ids(parent_id=self.plan_id)  # type: ignore
            if not any(self.cci_to_control_map):
                self._no_ccis = True
            return self.cci_to_control_map

    def get_control_to_cci_map(self) -> dict[int, set[str]]:
        """
        Gets the security control id to CCI map

        :return: The security control id to CCI map
        :rtype: dict[int, set[str]]
        """
        control_id_to_cci_map = defaultdict(set)
        for cci, control_ids in self.get_cci_to_control_map().items():
            for control_id in control_ids:
                control_id_to_cci_map[control_id].add(cci)
        return control_id_to_cci_map

    def get_control_implementation_id_for_cci(self, cci: Optional[str]) -> Optional[int]:
        """
        Gets the control implementation ID for a CCI

        :param Optional[str] cci: The CCI
        :return: The control ID
        :rtype: Optional[int]
        """
        cci_to_control_map = self.get_cci_to_control_map()
        if cci not in cci_to_control_map:
            cci = "CCI-000366"
        for control_id in cci_to_control_map.get(cci, set()):
            return self.control_id_to_implementation_map.get(control_id)
        return None

    def get_asset_map(self) -> dict[str, regscale_models.Asset]:
        """
        Retrieves a mapping of asset identifiers to their corresponding Asset objects. This method supports two modes
        of operation based on the `options_map_assets_to_components` flag. If the flag is set, it fetches the asset
        map using a specified key field from the assets associated with the given plan ID. Otherwise, it constructs
        the map by fetching all assets under the specified plan and using the asset identifier field as the key.

        :return: A dictionary mapping asset identifiers to Asset objects.
        :rtype: dict[str, regscale_models.Asset]
        """
        if self.options_map_assets_to_components:
            # Fetches the asset map directly using a specified key field.
            return regscale_models.Asset.get_map(plan_id=self.plan_id, key_field=self.asset_identifier_field)
        else:
            # Constructs the asset map by fetching all assets under the plan and using the asset identifier field as
            # the key.
            return {  # type: ignore
                getattr(x, self.asset_identifier_field): x
                for x in regscale_models.Asset.get_all_by_parent(
                    parent_id=self.plan_id,
                    parent_module=regscale_models.SecurityPlan.get_module_string(),
                )
            }

    @abstractmethod
    def fetch_findings(self, *args, **kwargs) -> Iterator[IntegrationFinding]:
        """
        Fetches findings from the integration

        :return: A list of findings
        :rtype: List[IntegrationFinding]
        """

    @abstractmethod
    def fetch_assets(self, *args, **kwargs) -> Iterator[IntegrationAsset]:
        """
        Fetches assets from the integration

        :return: An iterator of assets
        :rtype: Iterator[IntegrationAsset]
        """

    def get_finding_status(self, status: Optional[str]) -> regscale_models.ChecklistStatus:
        """
        Gets the RegScale checklist status based on the integration finding status

        :param Optional[str] status: The status of the finding
        :return: The RegScale checklist status
        :rtype: regscale_models.ChecklistStatus
        """
        return self.finding_status_map.get(status, regscale_models.ChecklistStatus.NOT_REVIEWED)

    def get_finding_severity(self, severity: Optional[str]) -> regscale_models.IssueSeverity:
        """
        Gets the RegScale issue severity based on the integration finding severity

        :param Optional[str] severity: The severity of the finding
        :return: The RegScale issue severity
        :rtype: regscale_models.IssueSeverity
        """
        return self.finding_severity_map.get(severity, regscale_models.IssueSeverity.NotAssigned)

    def get_finding_identifier(self, finding: IntegrationFinding) -> str:
        """
        Gets the finding identifier for the finding

        :param IntegrationFinding finding: The finding
        :return: The finding identifier
        :rtype: str
        """
        prefix = f"{self.plan_id}:"
        if ScannerVariables.tenableGroupByPlugin and finding.plugin_id:
            return f"{prefix}{finding.plugin_id}"
        prefix += finding.cve or self.hash_string(finding.external_id).__str__() or finding.rule_id
        if ScannerVariables.issueCreation.lower() == "perasset":
            return f"{prefix}:{finding.asset_identifier}"
        return prefix

    def get_or_create_assessment(self, control_implementation_id: int) -> regscale_models.Assessment:
        """
        Gets or creates a RegScale assessment

        :param int control_implementation_id: The ID of the control implementation
        :return: The assessment
        :rtype: regscale_models.Assessment
        """
        logger.info("Getting or create assessment for control implementation %d", control_implementation_id)
        assessment: Optional[regscale_models.Assessment] = self.assessment_map.get(control_implementation_id)
        if assessment:
            logger.debug(
                "Found cached assessment %s for control implementation %s", assessment.id, control_implementation_id
            )
        else:
            logger.debug("Assessment not found for control implementation %d", control_implementation_id)
            assessment = regscale_models.Assessment(
                plannedStart=get_current_datetime(),
                plannedFinish=get_current_datetime(),
                status=regscale_models.AssessmentStatus.COMPLETE.value,
                assessmentResult=regscale_models.AssessmentResultsStatus.FAIL.value,
                actualFinish=get_current_datetime(),
                leadAssessorId=self.assessor_id,
                parentId=control_implementation_id,
                parentModule=regscale_models.ControlImplementation.get_module_string(),
                title=f"{self.title} Assessment",
                assessmentType=regscale_models.AssessmentType.QA_SURVEILLANCE.value,
            ).create()
        self.assessment_map[control_implementation_id] = assessment
        return assessment

    def get_components(self) -> ThreadSafeList[regscale_models.Component]:
        """
        Get all components from the integration

        :return: A list of components
        :rtype: ThreadSafeList[regscale_models.Component]
        """
        if any(self.components):
            return self.components
        self.components = regscale_models.Component.get_all_by_parent(  # type: ignore
            parent_id=self.plan_id,
            parent_module=regscale_models.SecurityPlan.get_module_string(),
        )
        return self.components

    def get_component_by_title(self) -> dict:
        """
        Get all components from the integration

        :return: A dictionary of components
        :rtype: dict
        """
        return {component.title: component for component in self.get_components()}

    # Asset Methods
    def set_asset_defaults(self, asset: IntegrationAsset) -> IntegrationAsset:
        """
        Set default values for the asset (Thread Safe)

        :param IntegrationAsset asset: The integration asset
        :return: The asset with which defaults should be set
        :rtype: IntegrationAsset
        """
        if not asset.asset_owner_id:
            asset.asset_owner_id = self.get_assessor_id()
        if not asset.status:
            asset.status = "Active (On Network)"
        return asset

    def process_asset(
        self,
        asset: IntegrationAsset,
        loading_assets: TaskID,
    ) -> None:
        """
        Safely processes a single asset in a concurrent environment. This method ensures thread safety
        by utilizing a threading lock. It assigns default values to the asset if necessary, maps the asset
        to components if specified, and updates the progress of asset loading.
        (Thread Safe)

        :param IntegrationAsset asset: The integration asset to be processed.
        :param TaskID loading_assets: The identifier for the task tracking the progress of asset loading.
        :rtype: None
        """

        # Assign default values to the asset if they are not already set.
        asset = self.set_asset_defaults(asset)

        # If mapping assets to components is enabled and the asset has associated component names,
        # attempt to update or create each asset under its respective component.
        if any(asset.component_names):
            for component_name in asset.component_names:
                self.update_or_create_asset(asset, component_name)
        else:
            # If no component mapping is required, add the asset directly to the security plan without a component.
            self.update_or_create_asset(asset, None)

        if self.num_assets_to_process and self.asset_progress.tasks[loading_assets].total != float(
            self.num_assets_to_process
        ):
            self.asset_progress.update(
                loading_assets,
                total=self.num_assets_to_process,
                description=f"[#f8b737]Creating and updating {self.num_assets_to_process} assets from {self.title}.",
            )
        self.asset_progress.advance(loading_assets, 1)

    def update_or_create_asset(
        self,
        asset: IntegrationAsset,
        component_name: Optional[str] = None,
    ) -> None:
        """
        This method either updates an existing asset or creates a new one within a thread-safe manner. It handles
        the asset's association with a component, creating the component if it does not exist.
        (Thread Safe)

        :param IntegrationAsset asset: The asset to be updated or created.
        :param Optional[str] component_name: The name of the component to associate the asset with. If None, the asset
                                             is added directly to the security plan without a component association.
        :rtype: None
        """
        component = None
        if component_name:
            logger.debug("Searching for component: %s...", component_name)
            component = self.components_by_title.get(component_name)
            if not component:
                logger.debug("No existing component found with name %s, proceeding to create it...", component_name)
                component = regscale_models.Component(
                    title=component_name,
                    componentType=asset.component_type,
                    securityPlansId=self.plan_id,
                    description=component_name,
                    componentOwnerId=self.get_assessor_id(),
                ).get_or_create()
                self.components.append(component)
            if component.securityPlansId:
                component_mapping = regscale_models.ComponentMapping(
                    componentId=component.id,
                    securityPlanId=self.plan_id,
                )
                component_mapping.get_or_create()
            self.components_by_title[component_name] = component

        if self.options_map_assets_to_components:
            existing_or_new_asset = self.create_new_asset(asset, component=component)
        else:
            existing_or_new_asset = self.create_new_asset(asset, component=None)

        # If the asset is associated with a component, create a mapping between them.
        if existing_or_new_asset and component:
            regscale_models.AssetMapping(
                assetId=existing_or_new_asset.id,
                componentId=component.id,
            ).get_or_create()

    def create_new_asset(
        self, asset: IntegrationAsset, component: Optional[regscale_models.Component]
    ) -> Optional[regscale_models.Asset]:
        """
        Creates a new asset in the system based on the provided integration asset details.
        Associates the asset with a component or directly with the security plan.

        :param IntegrationAsset asset: The integration asset from which the new asset will be created.
        :param Optional[regscale_models.Component] component: The component to link the asset to, or None.
        :return: The newly created asset instance.
        :rtype: Optional[regscale_models.Asset]
        """
        # Ensure the asset has a name
        if not asset.name:
            logger.warning(
                "Asset name is required for asset creation. Skipping asset creation of asset_type: %s", asset.asset_type
            )
            return None

        new_asset = regscale_models.Asset(
            name=asset.name,
            otherTrackingNumber=asset.other_tracking_number or asset.identifier,
            assetOwnerId=asset.asset_owner_id or "Unknown",
            parentId=component.id if component else self.plan_id,
            parentModule=(
                regscale_models.Component.get_module_string()
                if component
                else regscale_models.SecurityPlan.get_module_string()
            ),
            assetType=asset.asset_type,
            dateLastUpdated=asset.date_last_updated or get_current_datetime(),
            status=asset.status,
            assetCategory=asset.asset_category,
            managementType=asset.management_type,
            notes=asset.notes,
            model=asset.model,
            manufacturer=asset.manufacturer,
            serialNumber=asset.serial_number,
            assetTagNumber=asset.asset_tag_number,
            bPublicFacing=asset.is_public_facing,
            azureIdentifier=asset.azure_identifier,
            location=asset.location,
            ipAddress=asset.ip_address,
            fqdn=asset.fqdn,
            macAddress=asset.mac_address,
            diskStorage=asset.disk_storage,
            cpu=asset.cpu,
            ram=asset.ram or 0,
            operatingSystem=asset.operating_system,
            osVersion=asset.os_version,
            endOfLifeDate=asset.end_of_life_date,
            vlanId=asset.vlan_id,
            uri=asset.uri,
            awsIdentifier=asset.aws_identifier,
            googleIdentifier=asset.google_identifier,
            otherCloudIdentifier=asset.other_cloud_identifier,
            patchLevel=asset.patch_level,
            cpe=asset.cpe,
            softwareVersion=asset.software_version,
            softwareName=asset.software_name,
            softwareVendor=asset.software_vendor,
        )
        if self.asset_identifier_field:
            setattr(new_asset, self.asset_identifier_field, asset.identifier)

        new_asset, created = new_asset.create_or_update(bulk_update=True, return_created=True)
        # add to asset_map_by_identifier
        self.asset_map_by_identifier[asset.identifier] = new_asset
        logger.debug("Created new asset with identifier %s", asset.identifier)

        self.handle_software_inventory(new_asset, asset.software_inventory, created)
        self.create_asset_data_and_link(new_asset, asset)
        self.create_or_update_ports_protocol(new_asset, asset)
        if self.stig_mapper:
            self.stig_mapper.map_associated_stigs_to_asset(asset=new_asset, ssp_id=self.plan_id)
        return new_asset

    def handle_software_inventory(
        self, new_asset: regscale_models.Asset, software_inventory: List[Dict], created: bool
    ) -> None:
        """
        Handles the software inventory for the asset.

        :param regscale_models.Asset new_asset: The newly created asset
        :param List[Dict] software_inventory: List of software inventory items
        :param bool created: Flag indicating if the asset was newly created
        :rtype: None
        """
        if not software_inventory:
            return

        existing_software = (
            []
            if created
            else regscale_models.SoftwareInventory.get_all_by_parent(parent_id=new_asset.id, parent_module=None)
        )
        existing_software_dict = {(s.name, s.version): s for s in existing_software}
        software_in_scan = set()

        for software in software_inventory:
            software_name = software.get("name")
            if not software_name:
                logger.error("Software name is required for software inventory")
                continue

            software_version = software.get("version")
            software_in_scan.add((software_name, software_version))

            if (software_name, software_version) not in existing_software_dict:
                self.software_to_create.append(
                    regscale_models.SoftwareInventory(
                        name=software_name,
                        parentHardwareAssetId=new_asset.id,
                        version=software_version,
                        # references=software.get("references", []),
                    )
                )
            else:
                self.software_to_update.append(existing_software_dict[(software_name, software_version)])

        # Remove software that is no longer in the scan
        for software_key, software_obj in existing_software_dict.items():
            if software_key not in software_in_scan:
                software_obj.delete()

    def create_asset_data_and_link(self, asset: regscale_models.Asset, integration_asset: IntegrationAsset) -> None:
        """
        Creates Data and Link objects for the given asset.

        :param regscale_models.Asset asset: The asset to create Data and Link for
        :param IntegrationAsset integration_asset: The integration asset containing source data and URL
        :rtype: None
        """
        if integration_asset.source_data:
            # Optimization, create an api that gets the data by plan and parent module
            regscale_models.Data(
                parentId=asset.id,
                parentModule=asset.get_module_string(),
                dataSource=self.title,
                dataType=regscale_models.DataDataType.JSON.value,
                rawData=json.dumps(integration_asset.source_data, indent=2),
                lastUpdatedById=integration_asset.asset_owner_id or "Unknown",
                createdById=integration_asset.asset_owner_id or "Unknown",
            ).create_or_update(bulk_create=True, bulk_update=True)
        if integration_asset.url:
            link = regscale_models.Link(
                parentID=asset.id,
                parentModule=asset.get_module_string(),
                url=integration_asset.url,
                title="Asset Provider URL",
            )
            if link.find_by_unique():
                self.link_to_update.append(link)
            else:
                self.link_to_create.append(link)

    @staticmethod
    def create_or_update_ports_protocol(asset: regscale_models.Asset, integration_asset: IntegrationAsset) -> None:
        """
        Creates or updates PortsProtocol objects for the given asset.

        :param regscale_models.Asset asset: The asset to create or update PortsProtocol for
        :param IntegrationAsset integration_asset: The integration asset containing ports and protocols information
        :rtype: None
        """
        if integration_asset.ports_and_protocols:
            for port_protocol in integration_asset.ports_and_protocols:
                if not port_protocol.get("start_port") or not port_protocol.get("end_port"):
                    logger.error("Invalid port protocol data: %s", port_protocol)
                    continue
                regscale_models.PortsProtocol(
                    parentId=asset.id,
                    parentModule=asset.get_module_string(),
                    startPort=port_protocol.get("start_port"),
                    endPort=port_protocol.get("end_port"),
                    service=port_protocol.get("service", asset.name),
                    protocol=port_protocol.get("protocol"),
                    purpose=port_protocol.get("purpose", f"Grant access to {asset.name}"),
                    usedBy=asset.name,
                ).create_or_update()

    def update_regscale_assets(self, assets: Iterator[IntegrationAsset]) -> int:
        """
        Updates RegScale assets based on the integration assets

        :param Iterator[IntegrationAsset] assets: The integration assets
        :return: The number of assets processed
        :rtype: int
        """
        logger.info("Updating RegScale assets...")
        loading_assets = self._setup_progress_bar()
        logger.info("Pre-populating cache")
        regscale_models.AssetMapping.populate_cache_by_plan(self.plan_id)
        regscale_models.ComponentMapping.populate_cache_by_plan(self.plan_id)

        if self.options_map_assets_to_components:
            self.components_by_title = self.get_component_by_title()

        assets_processed = self._process_assets(assets, loading_assets)

        self._perform_batch_operations()

        return assets_processed

    def _setup_progress_bar(self) -> TaskID:
        """
        Sets up the progress bar for asset processing.

        :return: The task ID for the progress bar
        :rtype: TaskID
        """
        return self.asset_progress.add_task(
            f"[#f8b737]Creating and updating assets from {self.title}.",
            total=self.num_assets_to_process if self.num_assets_to_process else None,
        )

    def _process_assets(self, assets: Iterator[IntegrationAsset], loading_assets: TaskID) -> int:
        """
        Processes the assets using single or multi-threaded approach based on THREAD_MAX_WORKERS.

        :param Iterator[IntegrationAsset] assets: The assets to process
        :param TaskID loading_assets: The task ID for the progress bar
        :return: The number of assets processed
        :rtype: int
        """
        assets_processed = 0
        # prime cache
        regscale_models.Asset.get_all_by_parent(
            parent_id=self.plan_id, parent_module=regscale_models.SecurityPlan.get_module_string()
        )

        process_func = lambda asset: self._process_single_asset(asset, loading_assets)  # noqa: E731

        if get_thread_workers_max() == 1:
            for asset in assets:
                if process_func(asset):
                    assets_processed = self._update_processed_count(assets_processed)
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=get_thread_workers_max()) as executor:
                future_to_asset = {executor.submit(process_func, asset): asset for asset in assets}
                for future in concurrent.futures.as_completed(future_to_asset):
                    if future.result():
                        assets_processed = self._update_processed_count(assets_processed)

        return assets_processed

    def _process_single_asset(self, asset: IntegrationAsset, loading_assets: TaskID) -> bool:
        """
        Processes a single asset and handles any exceptions.

        :param IntegrationAsset asset: The asset to process
        :param TaskID loading_assets: The task ID for the progress bar
        :return: True if the asset was processed successfully, False otherwise
        :rtype: bool
        """
        try:
            self.process_asset(asset, loading_assets)
            return True
        except Exception as exc:
            self.log_error("An error occurred when processing asset %s: %s", asset.name, exc)
            return False

    @staticmethod
    def _update_processed_count(assets_processed: int) -> int:
        """
        Updates and logs the count of processed assets.

        :param int assets_processed: The current count of processed assets
        :return: The updated count of processed assets
        :rtype: int
        """
        assets_processed += 1
        if assets_processed % 100 == 0:
            logger.info("Processed %d assets.", assets_processed)
        return assets_processed

    def _perform_batch_operations(self) -> None:
        """
        Performs batch operations for assets, software inventory, and data.

        :rtype: None
        """
        logger.info("Bulk saving assets...")
        regscale_models.Asset.bulk_save(progress_context=self.asset_progress)

        if self.software_to_create:
            regscale_models.SoftwareInventory.batch_create(
                items=self.software_to_create, progress_context=self.asset_progress
            )
        if self.software_to_update:
            regscale_models.SoftwareInventory.batch_update(
                items=self.software_to_update, progress_context=self.asset_progress
            )
        regscale_models.Data.bulk_save(progress_context=self.asset_progress)

    @staticmethod
    def get_issue_title(finding: IntegrationFinding) -> str:
        """
        Gets the issue title based on the POAM Title Type variable.

        :param IntegrationFinding finding: The finding data
        :return: The issue title
        :rtype: str
        """
        issue_title = finding.title or ""
        if ScannerVariables.poamTitleType.lower() == "pluginid" or not issue_title:
            issue_title = (
                f"{finding.plugin_id or finding.cve or finding.rule_id}: {finding.plugin_name or finding.description}"
            )
        return issue_title[:450]

    # Finding Methods
    def create_or_update_issue_from_finding(
        self,
        title: str,
        parent_id: int,
        parent_module: str,
        finding: IntegrationFinding,
    ) -> regscale_models.Issue:
        """
        Creates or updates a RegScale issue from a finding

        :param str title: The title of the issue
        :param int parent_id: The ID of the parent
        :param str parent_module: The module of the parent
        :param IntegrationFinding finding: The finding data
        :return: The created or updated RegScale issue
        :rtype: regscale_models.Issue
        """
        issue_status = (
            regscale_models.IssueStatus.Closed
            if (
                finding.status == regscale_models.ControlTestResultStatus.PASS
                or finding.status == regscale_models.IssueStatus.Closed
            )
            else regscale_models.IssueStatus.Open
        )

        finding_id = self.get_finding_identifier(finding)
        finding_id_lock = self._get_lock(finding_id)
        delimiter = "\n"

        with finding_id_lock:
            # Check if we should consolidate issues based on integrationFindingId
            if (
                ScannerVariables.issueCreation.lower() != "perasset"
                and issue_status == regscale_models.IssueStatus.Open
            ):
                existing_issues = regscale_models.Issue.find_by_integration_finding_id(finding_id)

                # Find an open issue to update
                issue = next(
                    (issue for issue in existing_issues if issue.status != regscale_models.IssueStatus.Closed), None
                )

                if issue:
                    # Update the existing issue
                    existing_asset_identifiers = set((issue.assetIdentifier or "").split(delimiter))
                    if finding.asset_identifier not in existing_asset_identifiers:
                        existing_asset_identifiers.add(finding.asset_identifier)
                        issue.assetIdentifier = delimiter.join(existing_asset_identifiers)

                    issue.status = issue_status
                    issue.dateLastUpdated = get_current_datetime()
                    if not issue.dateFirstDetected:
                        # This could be conceivably null if the issue was manually created, a bit of an edge case.
                        issue.dateFirstDetected = self.scan_date or finding.date_created
                    issue = self.group_by_plugin(issue, finding)
                    return issue.save()

            isPoam = self.is_poam(finding)

            def get_other_identifier():
                # Only called if isPoam is True and creating a new issue
                if isPoam and ScannerVariables.incrementPoamIdentifier:
                    return f"V-{self.get_next_poam_id():04d}"
                return None

            # Create a new issue if none exists
            return regscale_models.Issue(
                parentId=parent_id,
                parentModule=parent_module,
                vulnerabilityId=finding.vulnerability_id,
                title=self.get_issue_title(finding) or title,
                dateCreated=finding.date_created,
                status=issue_status,
                dateCompleted=(
                    self.get_date_completed(finding, issue_status)
                    if issue_status == regscale_models.IssueStatus.Closed
                    else None
                ),
                severityLevel=finding.severity,
                issueOwnerId=self.assessor_id,
                securityPlanId=self.plan_id,
                identification="Vulnerability Assessment",
                dateFirstDetected=finding.date_created,
                dueDate=finding.due_date,
                description=finding.description,
                sourceReport=self.title,
                recommendedActions=finding.recommendation_for_mitigation,
                assetIdentifier=finding.asset_identifier,
                securityChecks=finding.external_id,
                remediationDescription=finding.recommendation_for_mitigation,
                integrationFindingId=self.get_finding_identifier(finding),
                poamComments=finding.poam_comments,
                cve=finding.cve,
                controlId=(self.get_control_implementation_id_for_cci(finding.cci_ref) if finding.cci_ref else None),
                isPoam=isPoam,
                basisForAdjustment=(
                    finding.basis_for_adjustment if finding.basis_for_adjustment else f"{self.title} import"
                ),
                pluginId=finding.plugin_id,
                originalRiskRating=regscale_models.Issue.assign_risk_rating(finding.severity),
            ).create_or_update(defaults={"otherIdentifier": get_other_identifier})

    @staticmethod
    def group_by_plugin(existing_issue: regscale_models.Issue, finding: IntegrationFinding) -> regscale_models.Issue:
        """
        Merges the CVEs for the issue if the group by plugin is enabled

        :param regscale_models.Issue regscale_models.Issue existing_issue: The existing issue
        :param IntegrationFinding finding: The finding data
        :return: The existing issue
        :rtype: regscale_models.Issue
        """
        if ScannerVariables.tenableGroupByPlugin and finding.cve:
            # consolidate cve, but only for this switch
            existing_cves = (existing_issue.cve or "").split(",")
            existing_issue.cve = ",".join(set(existing_cves + [finding.cve]))
        return existing_issue

    @staticmethod
    def is_poam(finding: IntegrationFinding) -> bool:
        """
        Determines if an issue should be considered a Plan of Action and Milestones (POAM).

        :param IntegrationFinding finding: The finding to check
        :return: True if the issue should be a POAM, False otherwise
        :rtype: bool
        """
        if ScannerVariables.vulnerabilityCreation.lower() == "poamcreation":
            return True
        if finding.due_date < get_current_datetime():
            return True
        return False

    def handle_passing_finding(
        self,
        existing_issues: List[regscale_models.Issue],
        finding: IntegrationFinding,
        parent_id: int,
        parent_module: str,
    ) -> None:
        """
        Handles findings that have passed by closing any open issues associated with the finding.

        :param List[regscale_models.Issue] existing_issues: The list of existing issues to check against
        :param IntegrationFinding finding: The finding data that has passed
        :param int parent_id: The ID of the parent
        :param str parent_module: The module of the parent
        :rtype: None
        """
        logger.debug("Handling passing finding %s for %d", finding.external_id, parent_id)

        open_issue_ids = [x["id"] for x in self.existing_issue_ids_by_implementation_map[parent_id]]

        for issue in existing_issues:
            if issue.id in open_issue_ids:
                open_issue_ids.remove(issue.id)

            if (
                issue.integrationFindingId == self.get_finding_identifier(finding)
                and issue.status != regscale_models.IssueStatus.Closed
            ):
                self.update_issue_for_passing_finding(
                    issue, parent_module, parent_id, open_issue_ids, finding.asset_identifier, finding.date_last_updated
                )

    def update_issue_for_passing_finding(
        self,
        issue: regscale_models.Issue,
        parent_module: str,
        parent_id: int,
        open_issue_ids: List[int],
        asset_identifier: str,
        date_completed: Optional[str] = None,
    ) -> None:
        """
        Updates the given issue for a passing finding, potentially closing it if no assets remain.

        :param regscale_models.Issue issue: The issue to be updated
        :param str parent_module: The module of the parent
        :param int parent_id: The ID of the parent
        :param List[int] open_issue_ids: List of open issue IDs
        :param str asset_identifier: The identifier of the asset that passed
        :param Optional[str] date_completed: The date the finding passed
        :rtype: None
        """
        asset_identifiers = issue.assetIdentifier.split(",")
        if asset_identifier in asset_identifiers:
            asset_identifiers.remove(asset_identifier)

        if not asset_identifiers:
            # No more assets associated with this issue, so we can close it
            self.close_issue(issue, parent_module, parent_id, open_issue_ids, date_completed)
        else:
            # Update the issue with the remaining assets
            issue.assetIdentifier = ",".join(asset_identifiers)
            issue.dateLastUpdated = get_current_datetime()
            issue.save()
            logger.info("Updated issue %d for asset %s", issue.id, asset_identifier)

    def close_issue(
        self,
        issue: regscale_models.Issue,
        parent_module: str,
        parent_id: int,
        open_issue_ids: List[int],
        date_completed: Optional[str] = None,
    ) -> None:
        """
        Closes the given issue and updates control implementation status if needed.

        :param regscale_models.Issue issue: The issue to be closed
        :param str parent_module: The module of the parent
        :param int parent_id: The ID of the parent
        :param List[int] open_issue_ids: List of open issue IDs
        :param Optional[str] date_completed: The date the issue was completed
        :rtype: None
        """
        if parent_module == regscale_models.ControlImplementation.get_module_string():
            logger.info("Closing issue %d for control %s", issue.id, self.control_map[parent_id])
        else:
            logger.info("Closing issue %d for asset %d", issue.id, parent_id)

        issue.status = regscale_models.IssueStatus.Closed
        issue.dateCompleted = date_completed or get_current_datetime()
        issue.save()

        if not issue.controlId:
            logger.warning("Control ID not found for issue %d", issue.id)
        else:
            self.update_control_implementation_status(
                issue, parent_id, open_issue_ids, regscale_models.ImplementationStatus.FULLY_IMPLEMENTED
            )

    def update_control_implementation_status(
        self,
        issue: regscale_models.Issue,
        parent_id: int,
        open_issue_ids: List[int],
        status: regscale_models.ImplementationStatus,
    ) -> None:
        """
        Updates the control implementation status based on the open issues.

        :param regscale_models.Issue issue: The issue being closed
        :param int parent_id: The ID of the parent
        :param List[int] open_issue_ids: List of open issue IDs
        :param regscale_models.ImplementationStatus status: The status to set (default: FULLY_IMPLEMENTED)
        :rtype: None
        """
        # If there are still open issues, do not allow the status to be set to FULLY_IMPLEMENTED
        if any(open_issue_ids) and status == regscale_models.ImplementationStatus.FULLY_IMPLEMENTED:
            logger.debug("Asset %d still has open issues", parent_id)
            return
        logger.debug("Asset %d has no open issues", parent_id)
        if not issue.controlId:
            logger.warning("Control ID not found for issue %d", issue.id)
            return
        control_implementation = self.control_implementation_map.get(
            issue.controlId
        ) or regscale_models.ControlImplementation.get_object(object_id=issue.controlId)
        if not control_implementation:
            logger.warning("Control implementation %d not found", issue.controlId)
            return
        control_implementation.status = status
        self.control_implementation_map[issue.controlId] = control_implementation.save()

    def handle_failing_finding(
        self,
        issue_title: str,
        existing_issues: List[regscale_models.Issue],
        finding: IntegrationFinding,
        parent_id: int,
        parent_module: str,
    ) -> None:
        """
        Handles findings that have failed by updating an existing open issue or creating a new one and updating the
         control implementation status.

        :param str issue_title: The title of the issue
        :param List[regscale_models.Issue] existing_issues: The list of existing issues to check against
        :param IntegrationFinding finding: The finding data that has failed
        :param int parent_id: The ID of the parent
        :param str parent_module: The module of the parent
        :rtype: None
        """
        logger.info("Creating issue for %s %d", parent_module, parent_id)
        found_issue = self.create_or_update_issue_from_finding(
            title=issue_title,
            parent_id=parent_id,
            parent_module=parent_module,
            finding=finding,
        )
        # Update the control implementation status based on open issues
        self.update_control_implementation_status(
            found_issue,
            parent_id,
            [issue.id for issue in existing_issues],
            regscale_models.ImplementationStatus.NOT_IMPLEMENTED,
        )

    def handle_failing_checklist(
        self,
        finding: IntegrationFinding,
        plan_id: int,
        asset: regscale_models.Asset,
    ) -> None:
        """
        Handles failing checklists by creating or updating implementation options and objectives.

        :param IntegrationFinding finding: The finding data
        :param int plan_id: The ID of the security plan
        :param regscale_models.Asset asset: The asset associated with the finding
        :rtype: None
        """
        if finding.cci_ref:
            failing_objectives = regscale_models.ControlObjective.fetch_control_objectives_by_other_id(
                parent_id=plan_id, other_id_contains=finding.cci_ref
            )
            failing_objectives += regscale_models.ControlObjective.fetch_control_objectives_by_name(
                parent_id=plan_id, name_contains=finding.cci_ref
            )
            for failing_objective in failing_objectives:
                if failing_objective.name.lower().startswith("cci-"):
                    implementation_id = self.get_control_implementation_id_for_cci(failing_objective.name)
                else:
                    control_label = objective_to_control_dot(failing_objective.name)
                    if control_label not in self.control_implementation_id_map:
                        logger.warning("Control %s not found for %s", control_label, control_label)
                        continue
                    implementation_id = self.control_implementation_id_map[control_label]

                failing_option = regscale_models.ImplementationOption(
                    name="Failed STIG",
                    description="Failed STIG Security Checks",
                    acceptability=regscale_models.ImplementationStatus.NOT_IMPLEMENTED,
                    objectiveId=failing_objective.id,
                    securityControlId=failing_objective.securityControlId,
                    responsibility="Customer",
                ).create_or_update()
                regscale_models.ImplementationObjective(
                    securityControlId=failing_objective.securityControlId,
                    implementationId=implementation_id,
                    objectiveId=failing_objective.id,
                    optionId=failing_option.id,
                    status=regscale_models.ImplementationStatus.NOT_IMPLEMENTED,
                    statement=failing_objective.description,
                    responsibility="Customer",
                ).create_or_update()

    def get_asset_by_identifier(self, identifier: str) -> Optional[regscale_models.Asset]:
        """
        Gets an asset by its identifier

        :param str identifier: The identifier of the asset
        :return: The asset
        :rtype: Optional[regscale_models.Asset]
        """
        asset = self.asset_map_by_identifier.get(identifier)
        if not asset and identifier not in self.alerted_assets:
            self.alerted_assets.add(identifier)
            self.log_error("Asset not found for identifier %s", identifier)
        return asset

    def process_checklist(self, finding: IntegrationFinding) -> int:
        """
        Processes a single checklist item based on the provided finding.

        This method checks if the asset related to the finding exists, updates or creates a checklist item,
        and handles the finding based on its status (pass/fail).

        :param IntegrationFinding finding: The finding to process
        :return: 1 if the checklist was processed, 0 if not
        :rtype: int
        """
        logger.debug("Processing checklist %s", finding.external_id)
        if not (asset := self.get_asset_by_identifier(finding.asset_identifier)):
            logger.error("Asset not found for identifier %s", finding.asset_identifier)
            return 0
        tool = regscale_models.ChecklistTool.STIGs
        if finding.vulnerability_type == "Vulnerability Scan":
            tool = regscale_models.ChecklistTool.VulnerabilityScanner
        asset_module_string = regscale_models.Asset.get_module_string()

        if not finding.cci_ref:
            finding.cci_ref = "CCI-000366"

        logger.debug("Create or update checklist for %s", finding.external_id)
        regscale_models.Checklist(
            status=finding.status,
            assetId=asset.id,
            tool=tool,
            baseline=finding.baseline,
            vulnerabilityId=finding.vulnerability_number,
            results=finding.results,
            check=finding.title,
            cci=finding.cci_ref,
            ruleId=finding.rule_id,
            version=finding.rule_version,
            comments=finding.comments,
            datePerformed=finding.date_created,
        ).create_or_update()

        # with self.existing_issues_map_lock:
        if asset.id not in self.existing_issues_map:
            # If not, fetch and cache the issues
            logger.debug("Fetching issues for asset %d", asset.id)
            self.existing_issues_map[asset.id] = regscale_models.Issue.get_all_by_parent(
                parent_id=asset.id, parent_module=asset_module_string
            )

        # Now, existing_issues will always fetch from the cache, avoiding unnecessary database calls
        existing_issues = self.existing_issues_map[asset.id]

        if finding.status == regscale_models.ChecklistStatus.PASS:
            self.handle_passing_finding(existing_issues, finding, asset.id, asset_module_string)
        else:
            logger.debug("Handling failing checklist for %s", finding.external_id)
            if self.type == ScannerIntegrationType.CHECKLIST:
                self.handle_failing_checklist(finding=finding, plan_id=self.plan_id, asset=asset)
            else:
                self.handle_failing_finding(
                    issue_title=finding.issue_title or finding.title,
                    existing_issues=existing_issues,
                    finding=finding,
                    parent_id=asset.id,
                    parent_module=asset_module_string,
                )
        return 1

    def update_regscale_checklists(self, findings: List[IntegrationFinding]) -> int:
        """
        Process checklists from IntegrationFindings, optionally using multiple threads.

        :param List[IntegrationFinding] findings: The findings to process
        :return: The number of checklists processed
        :rtype: int
        """
        logger.info("Updating RegScale checklists...")
        loading_findings = self.finding_progress.add_task(
            f"[#f8b737]Creating and updating checklists from {self.title}."
        )
        checklists_processed = 0

        def process_finding(finding: IntegrationFinding) -> None:
            """
            Process a single finding and update the progress bar.
            :param IntegrationFinding finding:
            """
            nonlocal checklists_processed
            try:
                self.process_checklist(finding)
                if self.num_findings_to_process and self.finding_progress.tasks[loading_findings].total != float(
                    self.num_findings_to_process
                ):
                    self.finding_progress.update(
                        loading_findings,
                        total=self.num_findings_to_process,
                        description=f"[#f8b737]Creating and updating {self.num_findings_to_process} checklists from {self.title}.",
                    )
                self.finding_progress.advance(loading_findings, 1)
                checklists_processed += 1
            except Exception as exc:
                self.log_error(
                    "An error occurred when processing asset %s for finding %s: %s",
                    finding.asset_identifier,
                    finding.external_id,
                    exc,
                )

        if get_thread_workers_max() == 1:
            for finding in findings:
                process_finding(finding)
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=get_thread_workers_max()) as executor:
                list(executor.map(process_finding, findings))

        return checklists_processed

    def update_regscale_findings_and_vulnerabilities(self, findings: Iterator[IntegrationFinding]) -> int:
        """
        Updates RegScale findings and vulnerabilities based on the integration findings in a single pass.

        :param Iterator[IntegrationFinding] findings: The integration findings
        :return: The number of findings processed
        :rtype: int
        """
        logger.info("Updating RegScale findings and vulnerabilities...")
        existing_issues_dict = self.get_existing_issues_dict()
        scan_history = self.create_scan_history()
        current_vulnerabilities: Dict[int, Set[int]] = defaultdict(set)
        processed_findings_count = 0
        findings_to_process = self.num_findings_to_process
        loading_findings = self.finding_progress.add_task(
            f"[#f8b737]Processing findings from {self.title}",
            total=self.num_findings_to_process if self.num_findings_to_process else None,
        )

        # Locks for thread-safe operations
        count_lock = threading.RLock()
        vuln_lock = threading.RLock()

        def process_finding_threaded(finding: IntegrationFinding) -> None:
            """
            Process a single finding in a threaded environment.
            :param IntegrationFinding finding: The finding to process
            """
            nonlocal processed_findings_count, findings_to_process
            try:
                processed = self.process_finding(finding, existing_issues_dict, scan_history, current_vulnerabilities)

                with count_lock:
                    processed_findings_count += processed
                    if not findings_to_process:
                        findings_to_process = self.num_findings_to_process

                with vuln_lock:
                    self.finding_progress.update(
                        loading_findings,
                        advance=1,
                        description=f"[#f8b737]Processed {processed_findings_count} findings from {self.title}",
                        total=findings_to_process or processed_findings_count,
                    )
            except Exception as exc:
                self.log_error(
                    "An error occurred when processing finding %s: %s",
                    finding.external_id,
                    exc,
                )

        if get_thread_workers_max() == 1:
            for finding in findings:
                if not finding:
                    continue
                process_finding_threaded(finding)
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=get_thread_workers_max()) as executor:
                list(executor.map(process_finding_threaded, findings))

        scan_history.save()
        logger.info("Closing outdated issues...")
        self.close_outdated_items(current_vulnerabilities)

        logger.info("Processed %d findings for vulnerabilities and issues.", processed_findings_count)
        return processed_findings_count

    def get_existing_issues_dict(self) -> Dict[str, regscale_models.Issue]:
        """
        Retrieves all existing issues for the current security plan.

        :return: A dictionary of existing issues, keyed by a combination of integrationFindingId and assetIdentifier
        :rtype: Dict[str, regscale_models.Issue]
        """
        return {
            f"{i.integrationFindingId}_{i.assetIdentifier}": i
            for i in regscale_models.Issue.get_all_by_parent(
                parent_id=self.plan_id,
                parent_module=regscale_models.SecurityPlan.get_module_string(),
            )
        }

    def get_next_poam_id(self) -> int:
        """
        Retrieves the Next POAM ID for the current security plan in a thread-safe manner.

        :return: The Next POAM ID
        :rtype: int
        """
        # Use the class's _get_lock method to get a thread-safe lock
        with self._get_lock("poam_id"):
            # If we haven't cached the max ID yet
            if not isinstance(self._max_poam_id, int):
                logger.info("Fetching max POAM ID...")
                # Get all existing POAM IDs and find the maximum
                self._max_poam_id = max(
                    (
                        int(poam.otherIdentifier.split("-")[1])
                        for poam in self.get_existing_issues_dict().values()
                        if poam.otherIdentifier and poam.otherIdentifier.startswith("V-")
                    ),
                    default=0,
                )

            # Increment the cached max ID and store it
            self._max_poam_id += 1
            return self._max_poam_id

    def create_scan_history(self) -> regscale_models.ScanHistory:
        """
        Creates a new ScanHistory object for the current scan.

        :return: A newly created ScanHistory object
        :rtype: regscale_models.ScanHistory
        """
        scan_history = regscale_models.ScanHistory(
            parentId=self.plan_id,
            parentModule=regscale_models.SecurityPlan.get_module_string(),
            scanningTool=self.title,
            scanDate=get_current_datetime(),
            createdById=self.assessor_id,
            tenantsId=self.tenant_id,
            vLow=0,
            vMedium=0,
            vHigh=0,
            vCritical=0,
        ).create()

        count = 0
        ScanHistory.delete_object_cache(scan_history)
        while not regscale_models.ScanHistory.get_object(object_id=scan_history.id) or count > 10:
            logger.info("Waiting for ScanHistory to be created...")
            time.sleep(1)
            count += 1
            ScanHistory.delete_object_cache(scan_history)
        return scan_history

    def process_finding(
        self,
        finding: IntegrationFinding,
        existing_issues_dict: Dict[str, regscale_models.Issue],
        scan_history: regscale_models.ScanHistory,
        current_vulnerabilities: Dict[int, Set[int]],
    ) -> int:
        """
        Process a single finding, updating control findings, vulnerabilities, and scan history.

        :param IntegrationFinding finding: The finding to process
        :param Dict[str, regscale_models.Issue] existing_issues_dict: Dictionary of existing issues
        :param regscale_models.ScanHistory scan_history: The current scan history
        :param Dict[int, Set[int]] current_vulnerabilities: Dictionary of current vulnerabilities
        :rtype: None
        """
        if finding.cci_ref:  # Assume STIG if we have a CCI
            return self.process_checklist(finding=finding)
        else:
            finding = self.update_integration_finding_dates(
                scan_history=scan_history, finding=finding, existing_issues_dict=existing_issues_dict
            )
            self.process_control_findings(finding=finding)
            self.process_vulnerability(finding, existing_issues_dict, scan_history, current_vulnerabilities)
            self.set_severity_count_for_scan(finding.severity, scan_history)
            return 1

    def process_control_findings(self, finding: IntegrationFinding) -> None:
        """
        Process control findings for a given finding.

        :param IntegrationFinding finding: The finding to process
        :rtype: None
        """
        for control_label in finding.control_labels:
            if not (control_implementation_id := self.control_implementation_id_map.get(control_label)):
                logger.error("Control Implementation for %s not found in RegScale", control_label)
                continue
            self.process_control_test(finding, control_implementation_id)

    def process_control_test(self, finding: IntegrationFinding, control_implementation_id: int) -> None:
        """
        Process a control test for a given finding and control implementation.

        :param IntegrationFinding finding: The finding to process
        :param int control_implementation_id: The ID of the control implementation
        :rtype: None
        """
        assessment = self.get_or_create_assessment(control_implementation_id)
        control_test = self.create_or_get_control_test(finding, control_implementation_id)
        self.create_control_test_result(finding, control_test, assessment)
        self.handle_control_finding(finding, control_implementation_id)

    @staticmethod
    def create_or_get_control_test(
        finding: IntegrationFinding, control_implementation_id: int
    ) -> regscale_models.ControlTest:
        """
        Create or get an existing control test.

        :param IntegrationFinding finding: The finding associated with the control test
        :param int control_implementation_id: The ID of the control implementation
        :return: The created or existing control test
        :rtype: regscale_models.ControlTest
        """
        return regscale_models.ControlTest(
            uuid=finding.external_id,
            parentControlId=control_implementation_id,
            testCriteria=finding.cci_ref or finding.description,
        ).get_or_create()

    def create_control_test_result(
        self,
        finding: IntegrationFinding,
        control_test: regscale_models.ControlTest,
        assessment: regscale_models.Assessment,
    ) -> None:
        """
        Create a control test result.

        :param IntegrationFinding finding: The finding associated with the test result
        :param regscale_models.ControlTest control_test: The control test
        :param regscale_models.Assessment assessment: The assessment
        :rtype: None
        """
        regscale_models.ControlTestResult(
            parentTestId=control_test.id,
            parentAssessmentId=assessment.id,
            uuid=finding.external_id,
            result=finding.status,  # type: ignore
            dateAssessed=finding.date_created,
            assessedById=self.assessor_id,
            gaps=finding.gaps,
            observations=finding.observations,
            evidence=finding.evidence,
            identifiedRisk=finding.identified_risk,
            impact=finding.impact,
            recommendationForMitigation=finding.recommendation_for_mitigation,
        ).create()

    def handle_control_finding(self, finding: IntegrationFinding, control_implementation_id: int) -> None:
        """
        Handle a control finding, either passing or failing.

        :param IntegrationFinding finding: The finding to handle
        :param int control_implementation_id: The ID of the control implementation
        :rtype: None
        """
        existing_issues: list[regscale_models.Issue] = regscale_models.Issue.get_all_by_parent(
            parent_id=control_implementation_id,
            parent_module=regscale_models.ControlImplementation.get_module_string(),
        )
        if finding.status == regscale_models.ControlTestResultStatus.PASS:
            self.handle_passing_finding(
                existing_issues=existing_issues,
                finding=finding,
                parent_id=control_implementation_id,
                parent_module=regscale_models.ControlImplementation.get_module_string(),
            )
        else:
            self.handle_failing_finding(
                issue_title="Finding %s failed",
                existing_issues=existing_issues,
                finding=finding,
                parent_id=control_implementation_id,
                parent_module=regscale_models.ControlImplementation.get_module_string(),
            )

    def process_vulnerability(
        self,
        finding: IntegrationFinding,
        existing_issues_dict: Dict[str, regscale_models.Issue],
        scan_history: regscale_models.ScanHistory,
        current_vulnerabilities: Dict[int, Set[int]],
    ) -> None:
        """
        Process a vulnerability for a given finding.

        :param IntegrationFinding finding: The finding to process
        :param Dict[str, regscale_models.Issue] existing_issues_dict: Dictionary of existing issues
        :param regscale_models.ScanHistory scan_history: The current scan history
        :param Dict[int, Set[int]] current_vulnerabilities: Dictionary of current vulnerabilities
        :return: Number of findings processed
        :rtype: int
        """
        if not (asset := self.get_asset_by_identifier(finding.asset_identifier)):
            return

        if vulnerability_id := self.handle_vulnerability(
            finding,
            asset,
            scan_history,
            existing_issues_dict,
        ):
            current_vulnerabilities[asset.id].add(vulnerability_id)

    def close_outdated_items(self, current_vulnerabilities: Dict[int, Set[int]]) -> None:
        """
        Close outdated vulnerabilities and issues.

        :param Dict[int, Set[int]] current_vulnerabilities: Dictionary of current vulnerabilities
        :rtype: None
        """
        self.close_outdated_vulnerabilities(current_vulnerabilities)
        self.close_outdated_issues(current_vulnerabilities)

    def create_vulnerability_from_finding(
        self, finding: IntegrationFinding, asset: regscale_models.Asset, scan_history: regscale_models.ScanHistory
    ) -> regscale_models.Vulnerability:
        """
        Creates a vulnerability from an integration finding.

        :param IntegrationFinding finding: The integration finding
        :param regscale_models.Asset asset: The associated asset
        :param regscale_models.ScanHistory scan_history: The scan history
        :return: The created vulnerability
        :rtype: regscale_models.Vulnerability
        """
        vulnerability = regscale_models.Vulnerability(
            title=finding.title,
            cve=finding.cve,
            cvsSv3BaseScore=finding.cvs_sv3_base_score,
            scanId=scan_history.id,
            severity=self.issue_to_vulnerability_map.get(finding.severity, regscale_models.VulnerabilitySeverity.Low),
            description=finding.description,
            dateLastUpdated=finding.date_last_updated,
            parentId=self.plan_id,
            parentModule=regscale_models.SecurityPlan.get_module_string(),
            dns=asset.fqdn or "unknown",
            status=regscale_models.VulnerabilityStatus.Open,
            ipAddress=finding.ip_address or asset.ipAddress or "",
            firstSeen=finding.first_seen,
            lastSeen=finding.last_seen,
            plugInName=finding.cve or finding.plugin_name,  # Use CVE if available, otherwise use plugin name
            plugInId=finding.plugin_id,
            vprScore=finding.cvss_score,  # If this is the VPR score, otherwise use a different field
            exploitAvailable=None,  # Set this if you have information about exploit availability
            plugInText=finding.observations,  # or finding.evidence, whichever is more appropriate
            port=finding.port if hasattr(finding, "port") else None,
            protocol=finding.protocol if hasattr(finding, "protocol") else None,
            operatingSystem=asset.operating_system if hasattr(asset, "operating_system") else None,
        )
        vulnerability = vulnerability.create_or_update()
        if not re.match(r"^\d+\.\d+(\.\d+)?$", self.regscale_version) or self.regscale_version >= "5.64.0":
            regscale_models.VulnerabilityMapping(
                vulnerabilityId=vulnerability.id,
                assetId=asset.id,
                scanId=scan_history.id,
                securityPlansId=self.plan_id,
                createdById=self.assessor_id,
                tenantsId=self.tenant_id,
                isPublic=True,
                dateCreated=get_current_datetime(),
                firstSeen=finding.first_seen,
                lastSeen=finding.last_seen,
                status=finding.status,
            ).create_unique()
        return vulnerability

    def handle_vulnerability(
        self,
        finding: IntegrationFinding,
        asset: regscale_models.Asset,
        scan_history: regscale_models.ScanHistory,
        existing_issues_dict: Dict[str, regscale_models.Issue],
    ) -> Optional[int]:
        """
        Handles the vulnerabilities for a finding.

        :param IntegrationFinding finding: The integration finding
        :param regscale_models.Asset asset: The associated asset
        :param regscale_models.ScanHistory scan_history: The scan history
        :param Dict[str, regscale_models.Issue] existing_issues_dict: Existing issues
        :rtype: Optional[int]
        :return: The vulnerability ID
        """
        if not (finding.plugin_name or finding.cve):
            logger.warning("No Plugin Name or CVE found for finding %s", finding.title)
            return None

        vulnerability = self.create_vulnerability_from_finding(finding, asset, scan_history)
        finding.vulnerability_id = vulnerability.id

        # Handle associated issue
        self.create_or_update_issue_from_finding(
            title=finding.title,
            parent_id=asset.id,
            parent_module=asset.get_module_string(),
            finding=finding,
        )

        return vulnerability.id

    def _filter_vulns_open_by_other_tools(
        self, all_vulns: list[regscale_models.Vulnerability]
    ) -> list[regscale_models.Vulnerability]:
        """
        Fetch vulnerabilities that are open and not associated with other tools.
        :param list[regscale_models.Vulnerability] all_vulns: List of all vulnerabilities to check the scanningTool
        :return: List of matching vulnerabilities
        :rtype: list[regscale_models.Vulnerability]
        """
        vuln_list = []
        for vuln in all_vulns:
            other_tool = False
            open_vuln_mappings = regscale_models.VulnerabilityMapping.find_by_vulnerability(vuln.id, status="Open")
            for vuln_mapping in open_vuln_mappings:
                scan_history = regscale_models.ScanHistory.get_object(vuln_mapping.scanId)
                if scan_history.scanningTool != self.title:
                    other_tool = True
                    break
            if not other_tool:
                vuln_list.append(vuln)
        return vuln_list

    def close_outdated_vulnerabilities(self, current_vulnerabilities: Dict[int, Set[int]]) -> None:
        """
        Closes vulnerabilities that are not in the current set of vulnerability IDs for each asset.

        :param Dict[int, Set[int]] current_vulnerabilities: Dictionary of asset IDs to lists of current vulnerability IDs
        :rtype: None
        """
        # Get all current vulnerability IDs
        current_vuln_ids = {vuln_id for vuln_ids in current_vulnerabilities.values() for vuln_id in vuln_ids}

        # Get all vulnerabilities for this security plan
        all_vulnerabilities: list[regscale_models.Vulnerability] = regscale_models.Vulnerability.get_all_by_parent(
            parent_id=self.plan_id, parent_module=regscale_models.SecurityPlan.get_module_string()
        )

        # Pre-filter vulnerabilities that are not in current set
        outdated_vulns = [v for v in all_vulnerabilities if v.id not in current_vuln_ids]

        # Filter by tool
        tool_vulns = self._filter_vulns_open_by_other_tools(all_vulns=outdated_vulns)

        closed_count = 0
        for vuln in tool_vulns:
            if vuln.status != regscale_models.VulnerabilityStatus.Closed:
                self.close_mappings_list(vuln)  # Close matching mappings
                vuln.status = regscale_models.VulnerabilityStatus.Closed
                vuln.dateClosed = get_current_datetime()
                vuln.save()
                closed_count += 1
                logger.info("Closed vulnerability %d", vuln.id)

        logger.info("Closed %d outdated vulnerabilities.", closed_count)

    @staticmethod
    def close_mappings_list(vuln: regscale_models.Vulnerability) -> None:
        """
        Close all mappings for a vulnerability.

        :param regscale_models.Vulnerability vuln: The vulnerability to close mappings for
        :rtype: None
        """
        mappings = [
            mapping
            for mapping in regscale_models.VulnerabilityMapping.find_by_vulnerability(
                vuln.id, status=regscale_models.IssueStatus.Open
            )
        ]
        for mapping in mappings:
            # This one uses IssueStatus
            mapping.status = regscale_models.IssueStatus.Closed
            mapping.dateClosed = get_current_datetime()
            mapping.save()

    def close_outdated_issues(self, current_vulnerabilities: Dict[int, Set[int]]) -> int:
        """
        Closes issues that are not associated with current vulnerabilities for each asset.

        :param Dict[int, Set[int]] current_vulnerabilities: Dictionary mapping asset IDs to sets of current vulnerability IDs
        :return: Number of issues closed
        :rtype: int
        """
        closed_count = 0

        # Get all open issues for this security plan
        open_issues = regscale_models.Issue.fetch_issues_by_ssp(
            None, ssp_id=self.plan_id, status=regscale_models.IssueStatus.Open.value
        )

        # Create a progress bar
        task_id = self.finding_progress.add_task("[cyan]Closing outdated issues...", total=len(open_issues))

        for issue in open_issues:
            if self.should_close_issue(issue, current_vulnerabilities):
                issue.status = regscale_models.IssueStatus.Closed
                issue.dateCompleted = get_current_datetime()
                issue.save()
                closed_count += 1

            # Update the progress bar
            self.finding_progress.update(task_id, advance=1)

        logger.info("Closed %d outdated issues.", closed_count)
        return closed_count

    def should_close_issue(self, issue: regscale_models.Issue, current_vulnerabilities: Dict[int, Set[int]]) -> bool:
        """
        Determines if an issue should be closed based on current vulnerabilities.

        :param regscale_models.Issue issue: The issue to check
        :param Dict[int, Set[int]] current_vulnerabilities: Dictionary of current vulnerabilities
        :return: True if the issue should be closed, False otherwise
        :rtype: bool
        """
        # Do not close issues from other tools or issues without a vulnerabilityId
        if issue.sourceReport != self.title or not issue.vulnerabilityId:
            return False

        # Get vulnerability mappings for this issue
        vuln_mappings = regscale_models.VulnerabilityMapping.find_by_issue(issue.id)

        # Check if the issue's vulnerability is still current for any asset
        # If it is, we shouldn't close the issue
        return not any(
            mapping.assetId in current_vulnerabilities
            and issue.vulnerabilityId in current_vulnerabilities[mapping.assetId]
            for mapping in vuln_mappings
        )
        # If we've checked all mappings and found no current vulnerabilities, we should close the issue

    @staticmethod
    def set_severity_count_for_scan(severity: str, scan_history: regscale_models.ScanHistory) -> None:
        """
        Increments the count of the severity
        :param str severity: Severity of the vulnerability
        :param regscale_models.ScanHistory scan_history: Scan history object
        :rtype: None
        """
        if severity == regscale_models.IssueSeverity.Low:
            scan_history.vLow += 1
        elif severity == regscale_models.IssueSeverity.Moderate:
            scan_history.vMedium += 1
        elif severity == regscale_models.IssueSeverity.High:
            scan_history.vHigh += 1

    @classmethod
    def cci_assessment(cls, plan_id: int) -> None:
        """
        Creates or updates CCI assessments in RegScale

        :param int plan_id: The ID of the security plan
        :rtype: None
        """
        instance = cls(plan_id=plan_id)
        for control_id, ccis in instance.get_control_to_cci_map().items():
            if not (implementation_id := instance.control_id_to_implementation_map.get(control_id)):
                logger.error("Control Implementation for %d not found in RegScale", control_id)
                continue
            assessment = instance.get_or_create_assessment(implementation_id)
            assessment_result = regscale_models.AssessmentResultsStatus.PASS
            open_issues = instance.existing_issue_ids_by_implementation_map.get(implementation_id, [])
            ccis.add("CCI-000366")
            for cci in sorted(ccis):
                logger.debug("Creating assessment for CCI %s for implementation %d", cci, implementation_id)
                result = regscale_models.ControlTestResultStatus.PASS
                for issue in open_issues:
                    if cci.lower() in issue["integrationFindingId"].lower():
                        result = regscale_models.ControlTestResultStatus.FAIL
                        assessment_result = regscale_models.AssessmentResultsStatus.FAIL
                        break

                control_test_key = f"{implementation_id}-{cci}"
                control_test = instance.control_tests_map.get(
                    control_test_key,
                    regscale_models.ControlTest(
                        parentControlId=implementation_id,
                        testCriteria=cci,
                    ).get_or_create(),
                )
                regscale_models.ControlTestResult(
                    parentTestId=control_test.id,
                    parentAssessmentId=assessment.id,
                    result=result,
                    dateAssessed=get_current_datetime(),
                    assessedById=instance.assessor_id,
                ).create()
            assessment.assessmentResult = assessment_result
            assessment.save()

    @classmethod
    def sync_findings(cls, plan_id: int, **kwargs) -> int:
        """
        Syncs findings from the integration to RegScale

        :param int plan_id: The ID of the security plan
        :return: The number of findings processed
        :rtype: int
        """
        logger.info("Syncing %s findings...", cls.title)
        instance = cls(plan_id)
        instance.title = kwargs.get("title", cls.title)
        instance.finding_progress = create_progress_object()
        instance.scan_date = str(kwargs.get("scan_date")) if kwargs.get("scan_date") else None
        instance.enable_finding_date_update = kwargs.get("enable_finding_date_update", False)
        kwargs["plan_id"] = plan_id

        with instance.finding_progress:
            findings = instance.fetch_findings(**kwargs)
            # Update the asset map with the latest assets
            logger.info("Getting asset map...")
            instance.asset_map_by_identifier.update(instance.get_asset_map())
            if cls.type == ScannerIntegrationType.CHECKLIST:
                findings_processed = instance.update_regscale_checklists(findings=findings)
            else:
                findings_processed = instance.update_regscale_findings_and_vulnerabilities(findings=findings)

        if instance.errors:
            logger.error("Summary of errors encountered:")
            for error in instance.errors:
                logger.error(error)
        else:
            logger.info("All findings have been processed successfully.")

        logger.info("Processed %d findings.", findings_processed)
        return findings_processed

    @classmethod
    def sync_assets(cls, plan_id: int, **kwargs) -> int:
        """
        Syncs assets from the integration to RegScale

        :param int plan_id: The ID of the security plan
        :return: The number of assets processed
        :rtype: int
        """
        logger.info("Syncing %s assets...", cls.title)
        instance = cls(plan_id)
        instance.title = kwargs.get("title", cls.title)
        instance.asset_progress = create_progress_object()

        with instance.asset_progress:
            assets = instance.fetch_assets(**kwargs)
            assets_processed = instance.update_regscale_assets(assets=assets)

        if instance.errors:
            logger.error("Summary of errors encountered:")
            for error in instance.errors:
                logger.error(error)
        else:
            logger.info("All assets have been processed successfully.")

        APIHandler().log_api_summary()
        logger.info("%d assets processed.", assets_processed)
        return assets_processed

    def log_error(self, msg: str, *args: Any) -> None:
        """
        Logs an error message

        :param str msg: The error message
        :param Any *args: Additional arguments
        :rtype: None
        """
        logger.error(msg, *args, exc_info=True)
        self.errors.append(msg % args)

    def update_integration_finding_dates(
        self,
        finding: IntegrationFinding,
        existing_issues_dict: Dict[str, regscale_models.Issue],
        scan_history: regscale_models.ScanHistory,
    ) -> IntegrationFinding:
        """
        Update the dates of the integration finding based on the scan date and whether the finding is new or existing.

        :param IntegrationFinding finding: The integration finding
        :param Dict[str, regscale_models.Issue] existing_issues_dict: Dictionary of existing issues
        :param regscale_models.ScanHistory scan_history: List of existing scan history objects
        :return: The updated integration finding or the original finding if the scan date is not set
        :rtype: IntegrationFinding
        """
        if self.scan_date and self.enable_finding_date_update:
            issue = self.get_issue(existing_issues_dict, finding)
            vulnerabilities = self.get_vulnerabilities(issue=issue, status=regscale_models.IssueStatus.Open)
            existing_vuln = self.get_existing_vuln(vulnerabilities, finding)
            finding = self.update_finding_dates(finding, existing_vuln, issue)
            self.update_scan(scan_history=scan_history)

        return finding

    def get_issue(
        self, existing_issues_dict: Dict[str, regscale_models.Issue], finding: IntegrationFinding
    ) -> Optional[regscale_models.Issue]:
        """
        Get the existing issue for the integration finding

        :param Dict[str, regscale_models.Issue] existing_issues_dict: Dictionary of existing issues
        :param IntegrationFinding finding: The integration finding
        :return: The existing issue
        :rtype: Optional[regscale_models.Issue]
        """
        return existing_issues_dict.get(f"{self.get_finding_identifier(finding)}_{finding.asset_identifier}")

    def get_vulnerabilities(
        self, issue: regscale_models.Issue, status: str
    ) -> List[regscale_models.VulnerabilityMapping]:
        """
        Get the vulnerabilities for the issue

        :param regscale_models.Issue issue: The issue
        :param str status: The status of the vulnerability
        :return: The list of vulnerabilities
        :rtype: List[regscale_models.VulnerabilityMapping]
        """
        return regscale_models.VulnerabilityMapping.find_by_issue(issue.id, status=status) if issue else []

    def get_existing_vuln(
        self, vulnerabilities: List[regscale_models.VulnerabilityMapping], finding: IntegrationFinding
    ) -> Optional[regscale_models.VulnerabilityMapping]:
        """
        Get the existing vulnerability for the integration finding

        :param List[regscale_models.VulnerabilityMapping] vulnerabilities: The list of existing vulnerabilities
        :param IntegrationFinding finding: The integration finding
        :return: The existing vulnerability
        :rtype: Optional[regscale_models.VulnerabilityMapping]
        """
        existing_vuln = min(vulnerabilities, key=lambda vuln: vuln.firstSeen) if vulnerabilities else None
        if existing_vuln and date_obj(self.scan_date) < date_obj(finding.first_seen):
            finding.first_seen = self.scan_date
        return existing_vuln

    def update_finding_dates(
        self,
        finding: IntegrationFinding,
        existing_vuln: Optional[regscale_models.VulnerabilityMapping],
        issue: Optional[regscale_models.Issue],
    ) -> IntegrationFinding:
        """
        Update the dates of the integration finding based on the scan date and whether the finding is new or existing.

        :param IntegrationFinding finding: The integration finding
        :param Optional[regscale_models.VulnerabilityMapping] existing_vuln: The existing vulnerability mapping
        :param Optional[regscale_models.Issue] issue: The existing issue
        :return: The updated integration finding
        :rtype: IntegrationFinding
        """
        if not existing_vuln:
            finding.first_seen = self.scan_date
            finding.date_created = self.scan_date
            # From @mlongworth:
            # It also appears that the suspense date (due date for remediation) is set based upon the import date rather
            # than the scan date. This calculation needs to be based upon scan date e.g. scan date of 2/5/2024 severity
            # High, should set the due date for remediation in the POA&M to 4/5/2024.
            finding.due_date = issue_due_date(
                severity=finding.severity, created_date=self.scan_date, title=self.title, config=self.app.config
            )
        else:
            finding.first_seen = existing_vuln.firstSeen if existing_vuln else finding.first_seen
        if issue:
            finding.date_created = issue.dateFirstDetected or finding.date_created
        if date_obj(self.scan_date) >= date_obj(finding.first_seen):
            finding.last_seen = self.scan_date
        return finding

    def update_scan(self, scan_history: regscale_models.ScanHistory) -> None:
        """
        Update the scan history object for the current security plan

        :param regscale_models.ScanHistory scan_history: The list of existing scan history objects
        :return: None
        :rtype: None
        """
        scan_history.scanDate = datetime_str(self.scan_date)
        scan_history.save()

    @staticmethod
    def get_date_completed(finding: IntegrationFinding, issue_status: regscale_models.IssueStatus) -> Optional[str]:
        """
        Returns the date when the issue was completed based on the issue status.

        :param IntegrationFinding finding: The finding data
        :param regscale_models.IssueStatus issue_status: The status of the issue
        :return: The date when the issue was completed if the issue status is Closed, else None
        :rtype: Optional[str]
        """
        return finding.date_last_updated if issue_status == regscale_models.IssueStatus.Closed else None

    @staticmethod
    def hash_string(input_string: str) -> str:
        """
        Hashes a string using SHA-256

        :param str input_string: The string to hash
        :return: The hashed string
        :rtype: str
        """
        return hashlib.sha256(input_string.encode()).hexdigest()
