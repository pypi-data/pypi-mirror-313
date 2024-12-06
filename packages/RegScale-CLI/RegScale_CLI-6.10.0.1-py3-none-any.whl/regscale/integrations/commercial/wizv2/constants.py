"""This module contains all the constants used in the Wiz SDK."""

from enum import Enum
from typing import List, Optional

from regscale.models import IssueSeverity

SBOM_FILE_PATH = "artifacts/wiz_sbom.json"
INVENTORY_FILE_PATH = "artifacts/wiz_inventory.json"
ISSUES_FILE_PATH = "artifacts/wiz_issues.json"
VULNERABILITY_FILE_PATH = "artifacts/wiz_vulnerabilities.json"
CLOUD_CONFIG_FINDINGS_FILE_PATH = "artifacts/wiz_cloud_config_findings.json"
HOST_VULNERABILITY_FILE_PATH = "artifacts/wiz_host_vulnerabilities.json"
DATA_FINDINGS_FILE_PATH = "artifacts/wiz_data_findings.json"
CONTENT_TYPE = "application/json"
RATE_LIMIT_MSG = "Rate limit exceeded"
PROVIDER = "Provider ID"
RESOURCE = "Resource Type"
CHECK_INTERVAL_FOR_DOWNLOAD_REPORT = 7
MAX_RETRIES = 100
ASSET_TYPE_MAPPING = {
    "ACCESS_ROLE": "Other",
    "ACCESS_ROLE_BINDING": "Other",
    "ACCESS_ROLE_PERMISSION": "Other",
    "API_GATEWAY": "Other",
    "APPLICATION": "Other",
    "AUTHENTICATION_CONFIGURATION": "Other",
    "BACKUP_SERVICE": "Other",
    "BUCKET": "Other",
    "CDN": "Other",
    "CERTIFICATE": "Other",
    "CICD_SERVICE": "Other",
    "CLOUD_LOG_CONFIGURATION": "Other",
    "CLOUD_ORGANIZATION": "Other",
    "COMPUTE_INSTANCE_GROUP": "Other",
    "CONFIG_MAP": "Other",
    "CONTAINER": "Other",
    "CONTAINER_GROUP": "Other",
    "CONTAINER_IMAGE": "Other",
    "CONTAINER_REGISTRY": "Other",
    "CONTAINER_SERVICE": "Other",
    "DAEMON_SET": "Other",
    "DATABASE": "Other",
    "DATA_WORKLOAD": "Other",
    "DB_SERVER": "Physical Server",
    "DEPLOYMENT": "Other",
    "DNS_RECORD": "Other",
    "DNS_ZONE": "Other",
    "DOMAIN": "Other",
    "EMAIL_SERVICE": "Other",
    "ENCRYPTION_KEY": "Other",
    "ENDPOINT": "Other",
    "FILE_SYSTEM_SERVICE": "Other",
    "FIREWALL": "Firewall",
    "GATEWAY": "Other",
    "GOVERNANCE_POLICY": "Other",
    "GOVERNANCE_POLICY_GROUP": "Other",
    "HOSTED_APPLICATION": "Other",
    "IAM_BINDING": "Other",
    "IP_RANGE": "Other",
    "KUBERNETES_CLUSTER": "Other",
    "KUBERNETES_CRON_JOB": "Other",
    "KUBERNETES_INGRESS": "Other",
    "KUBERNETES_INGRESS_CONTROLLER": "Other",
    "KUBERNETES_JOB": "Other",
    "KUBERNETES_NETWORK_POLICY": "Other",
    "KUBERNETES_NODE": "Other",
    "KUBERNETES_PERSISTENT_VOLUME": "Other",
    "KUBERNETES_PERSISTENT_VOLUME_CLAIM": "Other",
    "KUBERNETES_POD_SECURITY_POLICY": "Other",
    "KUBERNETES_SERVICE": "Other",
    "KUBERNETES_STORAGE_CLASS": "Other",
    "KUBERNETES_VOLUME": "Other",
    "LOAD_BALANCER": "Other",
    "MANAGED_CERTIFICATE": "Other",
    "MANAGEMENT_SERVICE": "Other",
    "NETWORK_ADDRESS": "Other",
    "NETWORK_INTERFACE": "Other",
    "NETWORK_ROUTING_RULE": "Other",
    "NETWORK_SECURITY_RULE": "Other",
    "PEERING": "Other",
    "POD": "Other",
    "PORT_RANGE": "Other",
    "PRIVATE_ENDPOINT": "Other",
    "PROXY": "Other",
    "PROXY_RULE": "Other",
    "RAW_ACCESS_POLICY": "Other",
    "REGISTERED_DOMAIN": "Other",
    "REPLICA_SET": "Other",
    "RESOURCE_GROUP": "Other",
    "SEARCH_INDEX": "Other",
    "SUBNET": "Other",
    "SUBSCRIPTION": "Other",
    "SWITCH": "Network Switch",
    "VIRTUAL_DESKTOP": "Virtual Machine (VM)",
    "VIRTUAL_MACHINE": "Virtual Machine (VM)",
    "VIRTUAL_MACHINE_IMAGE": "Other",
    "VIRTUAL_NETWORK": "Other",
    "VOLUME": "Other",
    "WEB_SERVICE": "Other",
    "DATA_WORKFLOW": "Other",
}

INVENTORY_QUERY = """
    query CloudResourceSearch(
    $filterBy: CloudResourceFilters
    $first: Int
    $after: String
  ) {
    cloudResources(
      filterBy: $filterBy
      first: $first
      after: $after
    ) {
      nodes {
        ...CloudResourceFragment
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
  fragment CloudResourceFragment on CloudResource {
    id
    name
    type
    subscriptionId
    subscriptionExternalId
    graphEntity{
      id
      providerUniqueId
      name
      type
      projects {
        id
      }
      properties
      firstSeen
      lastSeen
    }
  }
"""
DATASOURCE = "Wiz"
SBOM_QUERY = """
    query ArtifactsGroupedByNameTable($filterBy: SBOMArtifactsGroupedByNameFilter, $first: Int, $after: String, $orderBy: SBOMArtifactsGroupedByNameOrder) {
  sbomArtifactsGroupedByName(
    filterBy: $filterBy
    first: $first
    after: $after
    orderBy: $orderBy
  ) {
    nodes {
      id
      type {
        ...SBOMArtifactTypeFragment
      }
      name
      validatedInRuntime
      artifacts(first: 0) {
        totalCount
      }
      versions(first: 500) {
        nodes {
          version
        }
      }
    }
    updatedAt
    pageInfo {
      endCursor
      hasNextPage
    }
    totalCount
  }
}
    fragment SBOMArtifactTypeFragment on SBOMArtifactType {
  group
  codeLibraryLanguage
  osPackageManager
  hostedTechnology {
    id
    name
    icon
  }
  plugin
}
"""

TECHNOLOGIES_FILE_PATH = "./artifacts/technologies.json"
AUTH0_URLS = [
    "https://auth.wiz.io/oauth/token",
    "https://auth0.gov.wiz.io/oauth/token",
    "https://auth0.test.wiz.io/oauth/token",
    "https://auth0.demo.wiz.io/oauth/token",
]
COGNITO_URLS = [
    "https://auth.app.wiz.io/oauth/token",
    "https://auth.gov.wiz.io/oauth/token",
    "https://auth.test.wiz.io/oauth/token",
    "https://auth.demo.wiz.io/oauth/token",
    "https://auth.app.wiz.us/oauth/token",
]
CREATE_REPORT_QUERY = """
    mutation CreateReport($input: CreateReportInput!) {
    createReport(input: $input) {
        report {
        id
        }
    }
    }
"""
REPORTS_QUERY = """
        query ReportsTable($filterBy: ReportFilters, $first: Int, $after: String) {
          reports(first: $first, after: $after, filterBy: $filterBy) {
            nodes {
              id
              name
              type {
                id
                name
              }
              project {
                id
                name
              }
              emailTarget {
                to
              }
              parameters {
                query
                framework {
                  name
                }
                subscriptions {
                  id
                  name
                  type
                }
                entities {
                  id
                  name
                  type
                }
              }
              lastRun {
                ...LastRunDetails
              }
              nextRunAt
              runIntervalHours
            }
            pageInfo {
              hasNextPage
              endCursor
            }
            totalCount
          }
        }
            fragment LastRunDetails on ReportRun {
          id
          status
          failedReason
          runAt
          progress
          results {
            ... on ReportRunResultsBenchmark {
              errorCount
              passedCount
              failedCount
              scannedCount
            }
            ... on ReportRunResultsGraphQuery {
              resultCount
              entityCount
            }
            ... on ReportRunResultsNetworkExposure {
              scannedCount
              publiclyAccessibleCount
            }
            ... on ReportRunResultsConfigurationFindings {
              findingsCount
            }
            ... on ReportRunResultsVulnerabilities {
              count
            }
            ... on ReportRunResultsIssues {
              count
            }
          }
        }
    """
DOWNLOAD_QUERY = """
    query ReportDownloadUrl($reportId: ID!) {
        report(id: $reportId) {
            lastRun {
                url
                status
            }
        }
    }
    """
ISSUE_QUERY = """query IssuesTable(
  $filterBy: IssueFilters
  $first: Int
  $after: String
  $orderBy: IssueOrder
) {
  issues:issuesV2(filterBy: $filterBy
    first: $first
    after: $after
    orderBy: $orderBy) {
    nodes {
      id
      sourceRule{
        __typename
        ... on Control {
          id
          name
          controlDescription: description
          resolutionRecommendation
          securitySubCategories {
            title
            externalId
            category {
              name
              framework {
                name
              }
            }
          }
        }
        ... on CloudEventRule{
          id
          name
          cloudEventRuleDescription: description
          sourceType
          type
        }
        ... on CloudConfigurationRule{
          id
          name
          cloudConfigurationRuleDescription: description
          remediationInstructions
          serviceType
        }
      }
      createdAt
      updatedAt
      dueAt
      type
      resolvedAt
      statusChangedAt
      projects {
        id
        name
        slug
        businessUnit
        riskProfile {
          businessImpact
        }
      }
      status
      severity
      entitySnapshot {
        id
        type
        nativeType
        name
        status
        cloudPlatform
        cloudProviderURL
        providerId
        region
        resourceGroupExternalId
        subscriptionExternalId
        subscriptionName
        subscriptionTags
        tags
        createdAt
        externalId
      }
      serviceTickets {
        externalId
        name
        url
      }
      notes {
        createdAt
        updatedAt
        text
        user {
          name
          email
        }
        serviceAccount {
          name
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}"""

VULNERABILITY_QUERY = """
    query VulnerabilityFindingsTable($filterBy: VulnerabilityFindingFilters, $first: Int, $after: String) {
  vulnerabilityFindings(
    filterBy: $filterBy
    first: $first
    after: $after
    orderBy: {direction: DESC}
  ) {
    nodes {
      id
      name
      detailedName
      description
      severity: vendorSeverity
      weightedSeverity
      status
      fixedVersion
      detectionMethod
      hasExploit
      hasCisaKevExploit
      cisaKevReleaseDate
      cisaKevDueDate
      firstDetectedAt
      lastDetectedAt
      resolvedAt
      score
      validatedInRuntime
      epssSeverity
      epssPercentile
      epssProbability
      dataSourceName
      fixDate
      fixDateBefore
      publishedDate
      projects{
        id
      }
      cvssv2 {
        attackVector
        attackComplexity
        confidentialityImpact
        integrityImpact
        privilegesRequired
        userInteractionRequired
      }
      cvssv3 {
        attackVector
        attackComplexity
        confidentialityImpact
        integrityImpact
        privilegesRequired
        userInteractionRequired
      }
      ignoreRules {
        id
      }
      layerMetadata {
        id
        details
        isBaseLayer
      }
      vulnerableAsset {
        ... on VulnerableAssetBase {
          id
          type
          name
          cloudPlatform
          subscriptionName
          subscriptionExternalId
          subscriptionId
          tags
          hasLimitedInternetExposure
          hasWideInternetExposure
          isAccessibleFromVPN
          isAccessibleFromOtherVnets
          isAccessibleFromOtherSubscriptions
        }
        ... on VulnerableAssetVirtualMachine {
          id
          type
          name
          cloudPlatform
          subscriptionName
          subscriptionExternalId
          subscriptionId
          tags
          operatingSystem
          imageName
          imageId
          imageNativeType
          hasLimitedInternetExposure
          hasWideInternetExposure
          isAccessibleFromVPN
          isAccessibleFromOtherVnets
          isAccessibleFromOtherSubscriptions
        }
        ... on VulnerableAssetServerless {
          id
          type
          name
          cloudPlatform
          subscriptionName
          subscriptionExternalId
          subscriptionId
          tags
          hasLimitedInternetExposure
          hasWideInternetExposure
          isAccessibleFromVPN
          isAccessibleFromOtherVnets
          isAccessibleFromOtherSubscriptions
        }
        ... on VulnerableAssetContainerImage {
          id
          type
          name
          cloudPlatform
          subscriptionName
          subscriptionExternalId
          subscriptionId
          tags
          hasLimitedInternetExposure
          hasWideInternetExposure
          isAccessibleFromVPN
          isAccessibleFromOtherVnets
          isAccessibleFromOtherSubscriptions
          repository {
            vertexId
            name
          }
          registry {
            vertexId
            name
          }
          scanSource
          executionControllers {
            ...VulnerableAssetExecutionControllerDetails
          }
        }
        ... on VulnerableAssetContainer {
          id
          type
          name
          cloudPlatform
          subscriptionName
          subscriptionExternalId
          subscriptionId
          tags
          hasLimitedInternetExposure
          hasWideInternetExposure
          isAccessibleFromVPN
          isAccessibleFromOtherVnets
          isAccessibleFromOtherSubscriptions
          executionControllers {
            ...VulnerableAssetExecutionControllerDetails
          }
        }
        ... on VulnerableAssetRepositoryBranch {
          id
          type
          name
          cloudPlatform
          repositoryId
          repositoryName
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
    fragment VulnerableAssetExecutionControllerDetails on VulnerableAssetExecutionController {
  id
  entityType
  externalId
  providerUniqueId
  name
  subscriptionExternalId
  subscriptionId
  subscriptionName
  ancestors {
    id
    name
    entityType
    externalId
    providerUniqueId
  }
}
"""
# CIS_BENCHMARK_QUERY
CLOUD_CONFIG_FINDING_QUERY = """
query CloudConfigurationFindingsTable($filterBy: ConfigurationFindingFilters, $first: Int, $after: String, $quick: Boolean) {
  configurationFindings(
    filterBy: $filterBy
    first: $first
    after: $after
    quick: $quick
  ) {
    nodes {
      id
      name
      analyzedAt
      firstSeenAt
      severity
      result
      status
      remediation
      source
      targetExternalId
      statusChangedAt
      ignoreRules {
        id
        tags {
          key
          value
        }
      }
      subscription {
        id
        name
        externalId
        cloudProvider
      }
      resource {
        id
        name
        type
        projects {
          id
          name
          riskProfile {
            businessImpact
          }
        }
      }
      rule {
        id
        shortId
        graphId
        name
        description
        remediationInstructions
        securitySubCategories {
          id
          title
          externalId
          category {
            id
            framework {
              id
              name
            }
            name
          }
        }
        tags {
          key
          value
        }
      }
    }
    maxCountReached
    pageInfo {
      hasNextPage
      endCursor
    }
    totalCount
  }
}
"""
HOST_VULNERABILITY_QUERY = """
query HostConfigurationFindingsTable($filterBy: HostConfigurationRuleAssessmentFilters, $orderBy: HostConfigurationRuleAssessmentOrder, $first: Int, $after: String) {
  hostConfigurationRuleAssessments(
    filterBy: $filterBy
    orderBy: $orderBy
    first: $first
    after: $after
  ) {
    nodes {
      id
      firstSeen
      analyzedAt
      updatedAt
      resource {
        id
        type
        name
        subscription {
          id
          name
          externalId
          cloudProvider
        }
      }
      result
      status
      ignoreRules {
        id
      }
      rule {
        id
        shortName
        description
        name
        severity
        securitySubCategories {
          ...SecuritySubCategoryDetails
        }
      }
      hasGraphObject
    }
    pageInfo {
      endCursor
      hasNextPage
    }
    maxCountReached
    totalCount
  }
}
fragment SecuritySubCategoryDetails on SecuritySubCategory {
  id
  title
  externalId
  description
  category {
    id
    name
    framework {
      id
      name
      enabled
    }
  }
}
"""
DATA_FINDING_QUERY = """
query DataFindingsGroupedByValueTable($groupBy: DataFindingsGroupedByValueField!, $after: String, $first: Int, $filterBy: DataFindingFilters, $orderBy: DataFindingsGroupedByValueOrder) {
  dataFindingsGroupedByValue(
    groupBy: $groupBy
    filterBy: $filterBy
    first: $first
    after: $after
    orderBy: $orderBy
  ) {
    nodes {
      categories
      location {
        countryCode
        state
      }
      regionCount
      graphEntityCount
      graphEntity {
        id
        name
        type
        properties
        projects {
          id
          name
          slug
          isFolder
        }
        issues(filterBy: {status: [OPEN, IN_PROGRESS]}) {
          criticalSeverityCount
          highSeverityCount
          mediumSeverityCount
          lowSeverityCount
          informationalSeverityCount
        }
      }
      cloudAccount {
        id
        name
        externalId
        cloudProvider
      }
      dataClassifiers {
        id
        name
        category
        matcherType
        severity
      }
      securitySubCategories {
        id
        title
        externalId
        description
        category {
          id
          name
          description
          framework {
            id
            name
            description
            enabled
          }
        }
      }
      findingsCount
      dataFindings(first: 5) {
        nodes {
          ...DataFindingDetails
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
    totalCount
  }
}
fragment DataFindingDetails on DataFinding {
  id
  name
  dataClassifier {
    id
    name
    category
    securitySubCategories {
      id
      title
      externalId
      description
      category {
        id
        name
        description
        framework {
          id
          name
          description
          enabled
        }
      }
    }
  }
  cloudAccount {
    id
    name
    externalId
    cloudProvider
  }
  location {
    countryCode
    state
  }
  severity
  totalMatchCount
  uniqueMatchCount
  graphEntity {
    id
    name
    type
    properties
    projects {
      id
      name
      slug
      isFolder
    }
  }
  externalSource
}
"""


SEVERITY_MAP = {
    "CRITICAL": IssueSeverity.High.value,
    "HIGH": IssueSeverity.High.value,
    "MEDIUM": IssueSeverity.Moderate.value,
    "LOW": IssueSeverity.Low.value,
    None: IssueSeverity.NotAssigned.value,
}

BEARER = "Bearer "


class WizVulnerabilityType(Enum):
    """
    Enum for Wiz vulnerability types
    """

    HOST_FINDING = "host_finding"
    DATA_FINDING = "data_finding"
    VULNERABILITY = "vulnerability"
    CONFIGURATION = "configuration_finding"


def get_wiz_vulnerability_queries(project_id: int, filter_by: Optional[dict] = None) -> List[dict]:
    if not filter_by:
        filter_by = {"projectId": project_id.split(",")}

    return [
        {
            "type": WizVulnerabilityType.VULNERABILITY,
            "query": VULNERABILITY_QUERY,
            "topic_key": "vulnerabilityFindings",
            "file_path": VULNERABILITY_FILE_PATH,
            "asset_lookup": "vulnerableAsset",
            "variables": {
                "first": 200,
                "filterBy": filter_by,
                "fetchTotalCount": False,
            },
        },
        {
            "type": WizVulnerabilityType.CONFIGURATION,
            "query": CLOUD_CONFIG_FINDING_QUERY,
            "topic_key": "configurationFindings",
            "file_path": CLOUD_CONFIG_FINDINGS_FILE_PATH,
            "asset_lookup": "resource",
            "variables": {
                "first": 200,
                "quick": True,
                "filterBy": {
                    "rule": {},
                    "resource": {"projectId": [project_id]},
                },
            },
        },
        {
            "type": WizVulnerabilityType.HOST_FINDING,
            "query": HOST_VULNERABILITY_QUERY,
            "topic_key": "hostConfigurationRuleAssessments",
            "file_path": HOST_VULNERABILITY_FILE_PATH,
            "asset_lookup": "resource",
            "variables": {
                "first": 200,
                "filterBy": {
                    "resource": {"projectId": [project_id]},
                    "frameworkCategory": [],
                },
            },
        },
        {
            "type": WizVulnerabilityType.DATA_FINDING,
            "query": DATA_FINDING_QUERY,
            "topic_key": "dataFindingsGroupedByValue",
            "file_path": DATA_FINDINGS_FILE_PATH,
            "asset_lookup": "resource",
            "variables": {
                "first": 200,
                "filterBy": {"projectId": [project_id]},
                "orderBy": {"field": "FINDING_COUNT", "direction": "DESC"},
                "groupBy": "GRAPH_ENTITY",
            },
        },
    ]


def get_wiz_issue_queries(project_id: int, filter_by: Optional[dict] = None) -> List[dict]:
    if not filter_by:
        filter_by = {"projectId": project_id.split(",")}

    return [
        {
            "type": WizVulnerabilityType.ISSUE,
            "query": ISSUE_QUERY,
            "topic_key": "issues",
            "file_path": ISSUES_FILE_PATH,
            "variables": {
                "first": 200,
                "filterBy": filter_by,
            },
        },
    ]
