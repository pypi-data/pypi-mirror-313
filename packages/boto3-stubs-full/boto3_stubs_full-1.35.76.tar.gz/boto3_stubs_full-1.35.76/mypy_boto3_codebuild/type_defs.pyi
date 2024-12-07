"""
Type annotations for codebuild service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/type_defs/)

Usage::

    ```python
    from mypy_boto3_codebuild.type_defs import AutoRetryConfigTypeDef

    data: AutoRetryConfigTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    ArtifactNamespaceType,
    ArtifactPackagingType,
    ArtifactsTypeType,
    AuthTypeType,
    BatchReportModeTypeType,
    BucketOwnerAccessType,
    BuildBatchPhaseTypeType,
    BuildPhaseTypeType,
    CacheModeType,
    CacheTypeType,
    ComputeTypeType,
    EnvironmentTypeType,
    EnvironmentVariableTypeType,
    FleetContextCodeType,
    FleetOverflowBehaviorType,
    FleetProxyRuleBehaviorType,
    FleetProxyRuleEffectTypeType,
    FleetProxyRuleTypeType,
    FleetSortByTypeType,
    FleetStatusCodeType,
    ImagePullCredentialsTypeType,
    LanguageTypeType,
    LogsConfigStatusTypeType,
    MachineTypeType,
    PlatformTypeType,
    ProjectSortByTypeType,
    ProjectVisibilityTypeType,
    ReportCodeCoverageSortByTypeType,
    ReportExportConfigTypeType,
    ReportGroupSortByTypeType,
    ReportGroupStatusTypeType,
    ReportGroupTrendFieldTypeType,
    ReportPackagingTypeType,
    ReportStatusTypeType,
    ReportTypeType,
    RetryBuildBatchTypeType,
    ServerTypeType,
    SharedResourceSortByTypeType,
    SortOrderTypeType,
    SourceAuthTypeType,
    SourceTypeType,
    StatusTypeType,
    WebhookBuildTypeType,
    WebhookFilterTypeType,
    WebhookScopeTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AutoRetryConfigTypeDef",
    "BatchDeleteBuildsInputRequestTypeDef",
    "BatchDeleteBuildsOutputTypeDef",
    "BatchGetBuildBatchesInputRequestTypeDef",
    "BatchGetBuildBatchesOutputTypeDef",
    "BatchGetBuildsInputRequestTypeDef",
    "BatchGetBuildsOutputTypeDef",
    "BatchGetFleetsInputRequestTypeDef",
    "BatchGetFleetsOutputTypeDef",
    "BatchGetProjectsInputRequestTypeDef",
    "BatchGetProjectsOutputTypeDef",
    "BatchGetReportGroupsInputRequestTypeDef",
    "BatchGetReportGroupsOutputTypeDef",
    "BatchGetReportsInputRequestTypeDef",
    "BatchGetReportsOutputTypeDef",
    "BatchRestrictionsOutputTypeDef",
    "BatchRestrictionsTypeDef",
    "BatchRestrictionsUnionTypeDef",
    "BuildArtifactsTypeDef",
    "BuildBatchFilterTypeDef",
    "BuildBatchPhaseTypeDef",
    "BuildBatchTypeDef",
    "BuildGroupTypeDef",
    "BuildNotDeletedTypeDef",
    "BuildPhaseTypeDef",
    "BuildStatusConfigTypeDef",
    "BuildSummaryTypeDef",
    "BuildTypeDef",
    "CloudWatchLogsConfigTypeDef",
    "CodeCoverageReportSummaryTypeDef",
    "CodeCoverageTypeDef",
    "ComputeConfigurationTypeDef",
    "CreateFleetInputRequestTypeDef",
    "CreateFleetOutputTypeDef",
    "CreateProjectInputRequestTypeDef",
    "CreateProjectOutputTypeDef",
    "CreateReportGroupInputRequestTypeDef",
    "CreateReportGroupOutputTypeDef",
    "CreateWebhookInputRequestTypeDef",
    "CreateWebhookOutputTypeDef",
    "DebugSessionTypeDef",
    "DeleteBuildBatchInputRequestTypeDef",
    "DeleteBuildBatchOutputTypeDef",
    "DeleteFleetInputRequestTypeDef",
    "DeleteProjectInputRequestTypeDef",
    "DeleteReportGroupInputRequestTypeDef",
    "DeleteReportInputRequestTypeDef",
    "DeleteResourcePolicyInputRequestTypeDef",
    "DeleteSourceCredentialsInputRequestTypeDef",
    "DeleteSourceCredentialsOutputTypeDef",
    "DeleteWebhookInputRequestTypeDef",
    "DescribeCodeCoveragesInputDescribeCodeCoveragesPaginateTypeDef",
    "DescribeCodeCoveragesInputRequestTypeDef",
    "DescribeCodeCoveragesOutputTypeDef",
    "DescribeTestCasesInputDescribeTestCasesPaginateTypeDef",
    "DescribeTestCasesInputRequestTypeDef",
    "DescribeTestCasesOutputTypeDef",
    "EnvironmentImageTypeDef",
    "EnvironmentLanguageTypeDef",
    "EnvironmentPlatformTypeDef",
    "EnvironmentVariableTypeDef",
    "ExportedEnvironmentVariableTypeDef",
    "FleetProxyRuleOutputTypeDef",
    "FleetProxyRuleTypeDef",
    "FleetProxyRuleUnionTypeDef",
    "FleetStatusTypeDef",
    "FleetTypeDef",
    "GetReportGroupTrendInputRequestTypeDef",
    "GetReportGroupTrendOutputTypeDef",
    "GetResourcePolicyInputRequestTypeDef",
    "GetResourcePolicyOutputTypeDef",
    "GitSubmodulesConfigTypeDef",
    "ImportSourceCredentialsInputRequestTypeDef",
    "ImportSourceCredentialsOutputTypeDef",
    "InvalidateProjectCacheInputRequestTypeDef",
    "ListBuildBatchesForProjectInputListBuildBatchesForProjectPaginateTypeDef",
    "ListBuildBatchesForProjectInputRequestTypeDef",
    "ListBuildBatchesForProjectOutputTypeDef",
    "ListBuildBatchesInputListBuildBatchesPaginateTypeDef",
    "ListBuildBatchesInputRequestTypeDef",
    "ListBuildBatchesOutputTypeDef",
    "ListBuildsForProjectInputListBuildsForProjectPaginateTypeDef",
    "ListBuildsForProjectInputRequestTypeDef",
    "ListBuildsForProjectOutputTypeDef",
    "ListBuildsInputListBuildsPaginateTypeDef",
    "ListBuildsInputRequestTypeDef",
    "ListBuildsOutputTypeDef",
    "ListCuratedEnvironmentImagesOutputTypeDef",
    "ListFleetsInputRequestTypeDef",
    "ListFleetsOutputTypeDef",
    "ListProjectsInputListProjectsPaginateTypeDef",
    "ListProjectsInputRequestTypeDef",
    "ListProjectsOutputTypeDef",
    "ListReportGroupsInputListReportGroupsPaginateTypeDef",
    "ListReportGroupsInputRequestTypeDef",
    "ListReportGroupsOutputTypeDef",
    "ListReportsForReportGroupInputListReportsForReportGroupPaginateTypeDef",
    "ListReportsForReportGroupInputRequestTypeDef",
    "ListReportsForReportGroupOutputTypeDef",
    "ListReportsInputListReportsPaginateTypeDef",
    "ListReportsInputRequestTypeDef",
    "ListReportsOutputTypeDef",
    "ListSharedProjectsInputListSharedProjectsPaginateTypeDef",
    "ListSharedProjectsInputRequestTypeDef",
    "ListSharedProjectsOutputTypeDef",
    "ListSharedReportGroupsInputListSharedReportGroupsPaginateTypeDef",
    "ListSharedReportGroupsInputRequestTypeDef",
    "ListSharedReportGroupsOutputTypeDef",
    "ListSourceCredentialsOutputTypeDef",
    "LogsConfigTypeDef",
    "LogsLocationTypeDef",
    "NetworkInterfaceTypeDef",
    "PaginatorConfigTypeDef",
    "PhaseContextTypeDef",
    "ProjectArtifactsTypeDef",
    "ProjectBadgeTypeDef",
    "ProjectBuildBatchConfigOutputTypeDef",
    "ProjectBuildBatchConfigTypeDef",
    "ProjectCacheOutputTypeDef",
    "ProjectCacheTypeDef",
    "ProjectEnvironmentOutputTypeDef",
    "ProjectEnvironmentTypeDef",
    "ProjectFileSystemLocationTypeDef",
    "ProjectFleetTypeDef",
    "ProjectSourceTypeDef",
    "ProjectSourceVersionTypeDef",
    "ProjectTypeDef",
    "ProxyConfigurationOutputTypeDef",
    "ProxyConfigurationTypeDef",
    "PutResourcePolicyInputRequestTypeDef",
    "PutResourcePolicyOutputTypeDef",
    "RegistryCredentialTypeDef",
    "ReportExportConfigTypeDef",
    "ReportFilterTypeDef",
    "ReportGroupTrendStatsTypeDef",
    "ReportGroupTypeDef",
    "ReportTypeDef",
    "ReportWithRawDataTypeDef",
    "ResolvedArtifactTypeDef",
    "ResponseMetadataTypeDef",
    "RetryBuildBatchInputRequestTypeDef",
    "RetryBuildBatchOutputTypeDef",
    "RetryBuildInputRequestTypeDef",
    "RetryBuildOutputTypeDef",
    "S3LogsConfigTypeDef",
    "S3ReportExportConfigTypeDef",
    "ScalingConfigurationInputTypeDef",
    "ScalingConfigurationOutputTypeDef",
    "ScopeConfigurationTypeDef",
    "SourceAuthTypeDef",
    "SourceCredentialsInfoTypeDef",
    "StartBuildBatchInputRequestTypeDef",
    "StartBuildBatchOutputTypeDef",
    "StartBuildInputRequestTypeDef",
    "StartBuildOutputTypeDef",
    "StopBuildBatchInputRequestTypeDef",
    "StopBuildBatchOutputTypeDef",
    "StopBuildInputRequestTypeDef",
    "StopBuildOutputTypeDef",
    "TagTypeDef",
    "TargetTrackingScalingConfigurationTypeDef",
    "TestCaseFilterTypeDef",
    "TestCaseTypeDef",
    "TestReportSummaryTypeDef",
    "UpdateFleetInputRequestTypeDef",
    "UpdateFleetOutputTypeDef",
    "UpdateProjectInputRequestTypeDef",
    "UpdateProjectOutputTypeDef",
    "UpdateProjectVisibilityInputRequestTypeDef",
    "UpdateProjectVisibilityOutputTypeDef",
    "UpdateReportGroupInputRequestTypeDef",
    "UpdateReportGroupOutputTypeDef",
    "UpdateWebhookInputRequestTypeDef",
    "UpdateWebhookOutputTypeDef",
    "VpcConfigOutputTypeDef",
    "VpcConfigTypeDef",
    "WebhookFilterTypeDef",
    "WebhookTypeDef",
)

class AutoRetryConfigTypeDef(TypedDict):
    autoRetryLimit: NotRequired[int]
    autoRetryNumber: NotRequired[int]
    nextAutoRetry: NotRequired[str]
    previousAutoRetry: NotRequired[str]

class BatchDeleteBuildsInputRequestTypeDef(TypedDict):
    ids: Sequence[str]

BuildNotDeletedTypeDef = TypedDict(
    "BuildNotDeletedTypeDef",
    {
        "id": NotRequired[str],
        "statusCode": NotRequired[str],
    },
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BatchGetBuildBatchesInputRequestTypeDef(TypedDict):
    ids: Sequence[str]

class BatchGetBuildsInputRequestTypeDef(TypedDict):
    ids: Sequence[str]

class BatchGetFleetsInputRequestTypeDef(TypedDict):
    names: Sequence[str]

class BatchGetProjectsInputRequestTypeDef(TypedDict):
    names: Sequence[str]

class BatchGetReportGroupsInputRequestTypeDef(TypedDict):
    reportGroupArns: Sequence[str]

class BatchGetReportsInputRequestTypeDef(TypedDict):
    reportArns: Sequence[str]

class BatchRestrictionsOutputTypeDef(TypedDict):
    maximumBuildsAllowed: NotRequired[int]
    computeTypesAllowed: NotRequired[List[str]]

class BatchRestrictionsTypeDef(TypedDict):
    maximumBuildsAllowed: NotRequired[int]
    computeTypesAllowed: NotRequired[Sequence[str]]

class BuildArtifactsTypeDef(TypedDict):
    location: NotRequired[str]
    sha256sum: NotRequired[str]
    md5sum: NotRequired[str]
    overrideArtifactName: NotRequired[bool]
    encryptionDisabled: NotRequired[bool]
    artifactIdentifier: NotRequired[str]
    bucketOwnerAccess: NotRequired[BucketOwnerAccessType]

class BuildBatchFilterTypeDef(TypedDict):
    status: NotRequired[StatusTypeType]

class PhaseContextTypeDef(TypedDict):
    statusCode: NotRequired[str]
    message: NotRequired[str]

ProjectCacheOutputTypeDef = TypedDict(
    "ProjectCacheOutputTypeDef",
    {
        "type": CacheTypeType,
        "location": NotRequired[str],
        "modes": NotRequired[List[CacheModeType]],
    },
)
ProjectFileSystemLocationTypeDef = TypedDict(
    "ProjectFileSystemLocationTypeDef",
    {
        "type": NotRequired[Literal["EFS"]],
        "location": NotRequired[str],
        "mountPoint": NotRequired[str],
        "identifier": NotRequired[str],
        "mountOptions": NotRequired[str],
    },
)

class ProjectSourceVersionTypeDef(TypedDict):
    sourceIdentifier: str
    sourceVersion: str

class VpcConfigOutputTypeDef(TypedDict):
    vpcId: NotRequired[str]
    subnets: NotRequired[List[str]]
    securityGroupIds: NotRequired[List[str]]

class BuildStatusConfigTypeDef(TypedDict):
    context: NotRequired[str]
    targetUrl: NotRequired[str]

ResolvedArtifactTypeDef = TypedDict(
    "ResolvedArtifactTypeDef",
    {
        "type": NotRequired[ArtifactsTypeType],
        "location": NotRequired[str],
        "identifier": NotRequired[str],
    },
)

class DebugSessionTypeDef(TypedDict):
    sessionEnabled: NotRequired[bool]
    sessionTarget: NotRequired[str]

class ExportedEnvironmentVariableTypeDef(TypedDict):
    name: NotRequired[str]
    value: NotRequired[str]

class NetworkInterfaceTypeDef(TypedDict):
    subnetId: NotRequired[str]
    networkInterfaceId: NotRequired[str]

class CloudWatchLogsConfigTypeDef(TypedDict):
    status: LogsConfigStatusTypeType
    groupName: NotRequired[str]
    streamName: NotRequired[str]

class CodeCoverageReportSummaryTypeDef(TypedDict):
    lineCoveragePercentage: NotRequired[float]
    linesCovered: NotRequired[int]
    linesMissed: NotRequired[int]
    branchCoveragePercentage: NotRequired[float]
    branchesCovered: NotRequired[int]
    branchesMissed: NotRequired[int]

CodeCoverageTypeDef = TypedDict(
    "CodeCoverageTypeDef",
    {
        "id": NotRequired[str],
        "reportARN": NotRequired[str],
        "filePath": NotRequired[str],
        "lineCoveragePercentage": NotRequired[float],
        "linesCovered": NotRequired[int],
        "linesMissed": NotRequired[int],
        "branchCoveragePercentage": NotRequired[float],
        "branchesCovered": NotRequired[int],
        "branchesMissed": NotRequired[int],
        "expired": NotRequired[datetime],
    },
)

class ComputeConfigurationTypeDef(TypedDict):
    vCpu: NotRequired[int]
    memory: NotRequired[int]
    disk: NotRequired[int]
    machineType: NotRequired[MachineTypeType]

class TagTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[str]

class VpcConfigTypeDef(TypedDict):
    vpcId: NotRequired[str]
    subnets: NotRequired[Sequence[str]]
    securityGroupIds: NotRequired[Sequence[str]]

ProjectArtifactsTypeDef = TypedDict(
    "ProjectArtifactsTypeDef",
    {
        "type": ArtifactsTypeType,
        "location": NotRequired[str],
        "path": NotRequired[str],
        "namespaceType": NotRequired[ArtifactNamespaceType],
        "name": NotRequired[str],
        "packaging": NotRequired[ArtifactPackagingType],
        "overrideArtifactName": NotRequired[bool],
        "encryptionDisabled": NotRequired[bool],
        "artifactIdentifier": NotRequired[str],
        "bucketOwnerAccess": NotRequired[BucketOwnerAccessType],
    },
)
ProjectCacheTypeDef = TypedDict(
    "ProjectCacheTypeDef",
    {
        "type": CacheTypeType,
        "location": NotRequired[str],
        "modes": NotRequired[Sequence[CacheModeType]],
    },
)

class ScopeConfigurationTypeDef(TypedDict):
    name: str
    scope: WebhookScopeTypeType
    domain: NotRequired[str]

WebhookFilterTypeDef = TypedDict(
    "WebhookFilterTypeDef",
    {
        "type": WebhookFilterTypeType,
        "pattern": str,
        "excludeMatchedPattern": NotRequired[bool],
    },
)
DeleteBuildBatchInputRequestTypeDef = TypedDict(
    "DeleteBuildBatchInputRequestTypeDef",
    {
        "id": str,
    },
)

class DeleteFleetInputRequestTypeDef(TypedDict):
    arn: str

class DeleteProjectInputRequestTypeDef(TypedDict):
    name: str

class DeleteReportGroupInputRequestTypeDef(TypedDict):
    arn: str
    deleteReports: NotRequired[bool]

class DeleteReportInputRequestTypeDef(TypedDict):
    arn: str

class DeleteResourcePolicyInputRequestTypeDef(TypedDict):
    resourceArn: str

class DeleteSourceCredentialsInputRequestTypeDef(TypedDict):
    arn: str

class DeleteWebhookInputRequestTypeDef(TypedDict):
    projectName: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeCodeCoveragesInputRequestTypeDef(TypedDict):
    reportArn: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    sortOrder: NotRequired[SortOrderTypeType]
    sortBy: NotRequired[ReportCodeCoverageSortByTypeType]
    minLineCoveragePercentage: NotRequired[float]
    maxLineCoveragePercentage: NotRequired[float]

class TestCaseFilterTypeDef(TypedDict):
    status: NotRequired[str]
    keyword: NotRequired[str]

class TestCaseTypeDef(TypedDict):
    reportArn: NotRequired[str]
    testRawDataPath: NotRequired[str]
    prefix: NotRequired[str]
    name: NotRequired[str]
    status: NotRequired[str]
    durationInNanoSeconds: NotRequired[int]
    message: NotRequired[str]
    expired: NotRequired[datetime]

class EnvironmentImageTypeDef(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    versions: NotRequired[List[str]]

EnvironmentVariableTypeDef = TypedDict(
    "EnvironmentVariableTypeDef",
    {
        "name": str,
        "value": str,
        "type": NotRequired[EnvironmentVariableTypeType],
    },
)
FleetProxyRuleOutputTypeDef = TypedDict(
    "FleetProxyRuleOutputTypeDef",
    {
        "type": FleetProxyRuleTypeType,
        "effect": FleetProxyRuleEffectTypeType,
        "entities": List[str],
    },
)
FleetProxyRuleTypeDef = TypedDict(
    "FleetProxyRuleTypeDef",
    {
        "type": FleetProxyRuleTypeType,
        "effect": FleetProxyRuleEffectTypeType,
        "entities": Sequence[str],
    },
)

class FleetStatusTypeDef(TypedDict):
    statusCode: NotRequired[FleetStatusCodeType]
    context: NotRequired[FleetContextCodeType]
    message: NotRequired[str]

class GetReportGroupTrendInputRequestTypeDef(TypedDict):
    reportGroupArn: str
    trendField: ReportGroupTrendFieldTypeType
    numOfReports: NotRequired[int]

ReportGroupTrendStatsTypeDef = TypedDict(
    "ReportGroupTrendStatsTypeDef",
    {
        "average": NotRequired[str],
        "max": NotRequired[str],
        "min": NotRequired[str],
    },
)

class ReportWithRawDataTypeDef(TypedDict):
    reportArn: NotRequired[str]
    data: NotRequired[str]

class GetResourcePolicyInputRequestTypeDef(TypedDict):
    resourceArn: str

class GitSubmodulesConfigTypeDef(TypedDict):
    fetchSubmodules: bool

class ImportSourceCredentialsInputRequestTypeDef(TypedDict):
    token: str
    serverType: ServerTypeType
    authType: AuthTypeType
    username: NotRequired[str]
    shouldOverwrite: NotRequired[bool]

class InvalidateProjectCacheInputRequestTypeDef(TypedDict):
    projectName: str

class ListBuildsForProjectInputRequestTypeDef(TypedDict):
    projectName: str
    sortOrder: NotRequired[SortOrderTypeType]
    nextToken: NotRequired[str]

class ListBuildsInputRequestTypeDef(TypedDict):
    sortOrder: NotRequired[SortOrderTypeType]
    nextToken: NotRequired[str]

class ListFleetsInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    sortOrder: NotRequired[SortOrderTypeType]
    sortBy: NotRequired[FleetSortByTypeType]

class ListProjectsInputRequestTypeDef(TypedDict):
    sortBy: NotRequired[ProjectSortByTypeType]
    sortOrder: NotRequired[SortOrderTypeType]
    nextToken: NotRequired[str]

class ListReportGroupsInputRequestTypeDef(TypedDict):
    sortOrder: NotRequired[SortOrderTypeType]
    sortBy: NotRequired[ReportGroupSortByTypeType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ReportFilterTypeDef(TypedDict):
    status: NotRequired[ReportStatusTypeType]

class ListSharedProjectsInputRequestTypeDef(TypedDict):
    sortBy: NotRequired[SharedResourceSortByTypeType]
    sortOrder: NotRequired[SortOrderTypeType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListSharedReportGroupsInputRequestTypeDef(TypedDict):
    sortOrder: NotRequired[SortOrderTypeType]
    sortBy: NotRequired[SharedResourceSortByTypeType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class SourceCredentialsInfoTypeDef(TypedDict):
    arn: NotRequired[str]
    serverType: NotRequired[ServerTypeType]
    authType: NotRequired[AuthTypeType]
    resource: NotRequired[str]

class S3LogsConfigTypeDef(TypedDict):
    status: LogsConfigStatusTypeType
    location: NotRequired[str]
    encryptionDisabled: NotRequired[bool]
    bucketOwnerAccess: NotRequired[BucketOwnerAccessType]

class ProjectBadgeTypeDef(TypedDict):
    badgeEnabled: NotRequired[bool]
    badgeRequestUrl: NotRequired[str]

class ProjectFleetTypeDef(TypedDict):
    fleetArn: NotRequired[str]

class RegistryCredentialTypeDef(TypedDict):
    credential: str
    credentialProvider: Literal["SECRETS_MANAGER"]

SourceAuthTypeDef = TypedDict(
    "SourceAuthTypeDef",
    {
        "type": SourceAuthTypeType,
        "resource": NotRequired[str],
    },
)

class PutResourcePolicyInputRequestTypeDef(TypedDict):
    policy: str
    resourceArn: str

class S3ReportExportConfigTypeDef(TypedDict):
    bucket: NotRequired[str]
    bucketOwner: NotRequired[str]
    path: NotRequired[str]
    packaging: NotRequired[ReportPackagingTypeType]
    encryptionKey: NotRequired[str]
    encryptionDisabled: NotRequired[bool]

class TestReportSummaryTypeDef(TypedDict):
    total: int
    statusCounts: Dict[str, int]
    durationInNanoSeconds: int

RetryBuildBatchInputRequestTypeDef = TypedDict(
    "RetryBuildBatchInputRequestTypeDef",
    {
        "id": NotRequired[str],
        "idempotencyToken": NotRequired[str],
        "retryType": NotRequired[RetryBuildBatchTypeType],
    },
)
RetryBuildInputRequestTypeDef = TypedDict(
    "RetryBuildInputRequestTypeDef",
    {
        "id": NotRequired[str],
        "idempotencyToken": NotRequired[str],
    },
)

class TargetTrackingScalingConfigurationTypeDef(TypedDict):
    metricType: NotRequired[Literal["FLEET_UTILIZATION_RATE"]]
    targetValue: NotRequired[float]

StopBuildBatchInputRequestTypeDef = TypedDict(
    "StopBuildBatchInputRequestTypeDef",
    {
        "id": str,
    },
)
StopBuildInputRequestTypeDef = TypedDict(
    "StopBuildInputRequestTypeDef",
    {
        "id": str,
    },
)

class UpdateProjectVisibilityInputRequestTypeDef(TypedDict):
    projectArn: str
    projectVisibility: ProjectVisibilityTypeType
    resourceAccessRole: NotRequired[str]

class BatchDeleteBuildsOutputTypeDef(TypedDict):
    buildsDeleted: List[str]
    buildsNotDeleted: List[BuildNotDeletedTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBuildBatchOutputTypeDef(TypedDict):
    statusCode: str
    buildsDeleted: List[str]
    buildsNotDeleted: List[BuildNotDeletedTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteSourceCredentialsOutputTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourcePolicyOutputTypeDef(TypedDict):
    policy: str
    ResponseMetadata: ResponseMetadataTypeDef

class ImportSourceCredentialsOutputTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListBuildBatchesForProjectOutputTypeDef(TypedDict):
    ids: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListBuildBatchesOutputTypeDef(TypedDict):
    ids: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListBuildsForProjectOutputTypeDef(TypedDict):
    ids: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListBuildsOutputTypeDef(TypedDict):
    ids: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListFleetsOutputTypeDef(TypedDict):
    fleets: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListProjectsOutputTypeDef(TypedDict):
    projects: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListReportGroupsOutputTypeDef(TypedDict):
    reportGroups: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListReportsForReportGroupOutputTypeDef(TypedDict):
    reports: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListReportsOutputTypeDef(TypedDict):
    reports: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSharedProjectsOutputTypeDef(TypedDict):
    projects: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSharedReportGroupsOutputTypeDef(TypedDict):
    reportGroups: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PutResourcePolicyOutputTypeDef(TypedDict):
    resourceArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateProjectVisibilityOutputTypeDef(TypedDict):
    projectArn: str
    publicProjectAlias: str
    projectVisibility: ProjectVisibilityTypeType
    ResponseMetadata: ResponseMetadataTypeDef

class ProjectBuildBatchConfigOutputTypeDef(TypedDict):
    serviceRole: NotRequired[str]
    combineArtifacts: NotRequired[bool]
    restrictions: NotRequired[BatchRestrictionsOutputTypeDef]
    timeoutInMins: NotRequired[int]
    batchReportMode: NotRequired[BatchReportModeTypeType]

BatchRestrictionsUnionTypeDef = Union[BatchRestrictionsTypeDef, BatchRestrictionsOutputTypeDef]
ListBuildBatchesForProjectInputRequestTypeDef = TypedDict(
    "ListBuildBatchesForProjectInputRequestTypeDef",
    {
        "projectName": NotRequired[str],
        "filter": NotRequired[BuildBatchFilterTypeDef],
        "maxResults": NotRequired[int],
        "sortOrder": NotRequired[SortOrderTypeType],
        "nextToken": NotRequired[str],
    },
)
ListBuildBatchesInputRequestTypeDef = TypedDict(
    "ListBuildBatchesInputRequestTypeDef",
    {
        "filter": NotRequired[BuildBatchFilterTypeDef],
        "maxResults": NotRequired[int],
        "sortOrder": NotRequired[SortOrderTypeType],
        "nextToken": NotRequired[str],
    },
)

class BuildBatchPhaseTypeDef(TypedDict):
    phaseType: NotRequired[BuildBatchPhaseTypeType]
    phaseStatus: NotRequired[StatusTypeType]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    durationInSeconds: NotRequired[int]
    contexts: NotRequired[List[PhaseContextTypeDef]]

class BuildPhaseTypeDef(TypedDict):
    phaseType: NotRequired[BuildPhaseTypeType]
    phaseStatus: NotRequired[StatusTypeType]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    durationInSeconds: NotRequired[int]
    contexts: NotRequired[List[PhaseContextTypeDef]]

class BuildSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    requestedOn: NotRequired[datetime]
    buildStatus: NotRequired[StatusTypeType]
    primaryArtifact: NotRequired[ResolvedArtifactTypeDef]
    secondaryArtifacts: NotRequired[List[ResolvedArtifactTypeDef]]

class DescribeCodeCoveragesOutputTypeDef(TypedDict):
    codeCoverages: List[CodeCoverageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateWebhookInputRequestTypeDef(TypedDict):
    projectName: str
    branchFilter: NotRequired[str]
    filterGroups: NotRequired[Sequence[Sequence[WebhookFilterTypeDef]]]
    buildType: NotRequired[WebhookBuildTypeType]
    manualCreation: NotRequired[bool]
    scopeConfiguration: NotRequired[ScopeConfigurationTypeDef]

class UpdateWebhookInputRequestTypeDef(TypedDict):
    projectName: str
    branchFilter: NotRequired[str]
    rotateSecret: NotRequired[bool]
    filterGroups: NotRequired[Sequence[Sequence[WebhookFilterTypeDef]]]
    buildType: NotRequired[WebhookBuildTypeType]

class WebhookTypeDef(TypedDict):
    url: NotRequired[str]
    payloadUrl: NotRequired[str]
    secret: NotRequired[str]
    branchFilter: NotRequired[str]
    filterGroups: NotRequired[List[List[WebhookFilterTypeDef]]]
    buildType: NotRequired[WebhookBuildTypeType]
    manualCreation: NotRequired[bool]
    lastModifiedSecret: NotRequired[datetime]
    scopeConfiguration: NotRequired[ScopeConfigurationTypeDef]

class DescribeCodeCoveragesInputDescribeCodeCoveragesPaginateTypeDef(TypedDict):
    reportArn: str
    sortOrder: NotRequired[SortOrderTypeType]
    sortBy: NotRequired[ReportCodeCoverageSortByTypeType]
    minLineCoveragePercentage: NotRequired[float]
    maxLineCoveragePercentage: NotRequired[float]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListBuildBatchesForProjectInputListBuildBatchesForProjectPaginateTypeDef = TypedDict(
    "ListBuildBatchesForProjectInputListBuildBatchesForProjectPaginateTypeDef",
    {
        "projectName": NotRequired[str],
        "filter": NotRequired[BuildBatchFilterTypeDef],
        "sortOrder": NotRequired[SortOrderTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListBuildBatchesInputListBuildBatchesPaginateTypeDef = TypedDict(
    "ListBuildBatchesInputListBuildBatchesPaginateTypeDef",
    {
        "filter": NotRequired[BuildBatchFilterTypeDef],
        "sortOrder": NotRequired[SortOrderTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListBuildsForProjectInputListBuildsForProjectPaginateTypeDef(TypedDict):
    projectName: str
    sortOrder: NotRequired[SortOrderTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListBuildsInputListBuildsPaginateTypeDef(TypedDict):
    sortOrder: NotRequired[SortOrderTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProjectsInputListProjectsPaginateTypeDef(TypedDict):
    sortBy: NotRequired[ProjectSortByTypeType]
    sortOrder: NotRequired[SortOrderTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListReportGroupsInputListReportGroupsPaginateTypeDef(TypedDict):
    sortOrder: NotRequired[SortOrderTypeType]
    sortBy: NotRequired[ReportGroupSortByTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSharedProjectsInputListSharedProjectsPaginateTypeDef(TypedDict):
    sortBy: NotRequired[SharedResourceSortByTypeType]
    sortOrder: NotRequired[SortOrderTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSharedReportGroupsInputListSharedReportGroupsPaginateTypeDef(TypedDict):
    sortOrder: NotRequired[SortOrderTypeType]
    sortBy: NotRequired[SharedResourceSortByTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

DescribeTestCasesInputDescribeTestCasesPaginateTypeDef = TypedDict(
    "DescribeTestCasesInputDescribeTestCasesPaginateTypeDef",
    {
        "reportArn": str,
        "filter": NotRequired[TestCaseFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
DescribeTestCasesInputRequestTypeDef = TypedDict(
    "DescribeTestCasesInputRequestTypeDef",
    {
        "reportArn": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "filter": NotRequired[TestCaseFilterTypeDef],
    },
)

class DescribeTestCasesOutputTypeDef(TypedDict):
    testCases: List[TestCaseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class EnvironmentLanguageTypeDef(TypedDict):
    language: NotRequired[LanguageTypeType]
    images: NotRequired[List[EnvironmentImageTypeDef]]

class ProxyConfigurationOutputTypeDef(TypedDict):
    defaultBehavior: NotRequired[FleetProxyRuleBehaviorType]
    orderedProxyRules: NotRequired[List[FleetProxyRuleOutputTypeDef]]

FleetProxyRuleUnionTypeDef = Union[FleetProxyRuleTypeDef, FleetProxyRuleOutputTypeDef]

class GetReportGroupTrendOutputTypeDef(TypedDict):
    stats: ReportGroupTrendStatsTypeDef
    rawData: List[ReportWithRawDataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

ListReportsForReportGroupInputListReportsForReportGroupPaginateTypeDef = TypedDict(
    "ListReportsForReportGroupInputListReportsForReportGroupPaginateTypeDef",
    {
        "reportGroupArn": str,
        "sortOrder": NotRequired[SortOrderTypeType],
        "filter": NotRequired[ReportFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListReportsForReportGroupInputRequestTypeDef = TypedDict(
    "ListReportsForReportGroupInputRequestTypeDef",
    {
        "reportGroupArn": str,
        "nextToken": NotRequired[str],
        "sortOrder": NotRequired[SortOrderTypeType],
        "maxResults": NotRequired[int],
        "filter": NotRequired[ReportFilterTypeDef],
    },
)
ListReportsInputListReportsPaginateTypeDef = TypedDict(
    "ListReportsInputListReportsPaginateTypeDef",
    {
        "sortOrder": NotRequired[SortOrderTypeType],
        "filter": NotRequired[ReportFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListReportsInputRequestTypeDef = TypedDict(
    "ListReportsInputRequestTypeDef",
    {
        "sortOrder": NotRequired[SortOrderTypeType],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "filter": NotRequired[ReportFilterTypeDef],
    },
)

class ListSourceCredentialsOutputTypeDef(TypedDict):
    sourceCredentialsInfos: List[SourceCredentialsInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class LogsConfigTypeDef(TypedDict):
    cloudWatchLogs: NotRequired[CloudWatchLogsConfigTypeDef]
    s3Logs: NotRequired[S3LogsConfigTypeDef]

class LogsLocationTypeDef(TypedDict):
    groupName: NotRequired[str]
    streamName: NotRequired[str]
    deepLink: NotRequired[str]
    s3DeepLink: NotRequired[str]
    cloudWatchLogsArn: NotRequired[str]
    s3LogsArn: NotRequired[str]
    cloudWatchLogs: NotRequired[CloudWatchLogsConfigTypeDef]
    s3Logs: NotRequired[S3LogsConfigTypeDef]

ProjectEnvironmentOutputTypeDef = TypedDict(
    "ProjectEnvironmentOutputTypeDef",
    {
        "type": EnvironmentTypeType,
        "image": str,
        "computeType": ComputeTypeType,
        "computeConfiguration": NotRequired[ComputeConfigurationTypeDef],
        "fleet": NotRequired[ProjectFleetTypeDef],
        "environmentVariables": NotRequired[List[EnvironmentVariableTypeDef]],
        "privilegedMode": NotRequired[bool],
        "certificate": NotRequired[str],
        "registryCredential": NotRequired[RegistryCredentialTypeDef],
        "imagePullCredentialsType": NotRequired[ImagePullCredentialsTypeType],
    },
)
ProjectEnvironmentTypeDef = TypedDict(
    "ProjectEnvironmentTypeDef",
    {
        "type": EnvironmentTypeType,
        "image": str,
        "computeType": ComputeTypeType,
        "computeConfiguration": NotRequired[ComputeConfigurationTypeDef],
        "fleet": NotRequired[ProjectFleetTypeDef],
        "environmentVariables": NotRequired[Sequence[EnvironmentVariableTypeDef]],
        "privilegedMode": NotRequired[bool],
        "certificate": NotRequired[str],
        "registryCredential": NotRequired[RegistryCredentialTypeDef],
        "imagePullCredentialsType": NotRequired[ImagePullCredentialsTypeType],
    },
)
ProjectSourceTypeDef = TypedDict(
    "ProjectSourceTypeDef",
    {
        "type": SourceTypeType,
        "location": NotRequired[str],
        "gitCloneDepth": NotRequired[int],
        "gitSubmodulesConfig": NotRequired[GitSubmodulesConfigTypeDef],
        "buildspec": NotRequired[str],
        "auth": NotRequired[SourceAuthTypeDef],
        "reportBuildStatus": NotRequired[bool],
        "buildStatusConfig": NotRequired[BuildStatusConfigTypeDef],
        "insecureSsl": NotRequired[bool],
        "sourceIdentifier": NotRequired[str],
    },
)

class ReportExportConfigTypeDef(TypedDict):
    exportConfigType: NotRequired[ReportExportConfigTypeType]
    s3Destination: NotRequired[S3ReportExportConfigTypeDef]

class ScalingConfigurationInputTypeDef(TypedDict):
    scalingType: NotRequired[Literal["TARGET_TRACKING_SCALING"]]
    targetTrackingScalingConfigs: NotRequired[Sequence[TargetTrackingScalingConfigurationTypeDef]]
    maxCapacity: NotRequired[int]

class ScalingConfigurationOutputTypeDef(TypedDict):
    scalingType: NotRequired[Literal["TARGET_TRACKING_SCALING"]]
    targetTrackingScalingConfigs: NotRequired[List[TargetTrackingScalingConfigurationTypeDef]]
    maxCapacity: NotRequired[int]
    desiredCapacity: NotRequired[int]

class ProjectBuildBatchConfigTypeDef(TypedDict):
    serviceRole: NotRequired[str]
    combineArtifacts: NotRequired[bool]
    restrictions: NotRequired[BatchRestrictionsUnionTypeDef]
    timeoutInMins: NotRequired[int]
    batchReportMode: NotRequired[BatchReportModeTypeType]

class BuildGroupTypeDef(TypedDict):
    identifier: NotRequired[str]
    dependsOn: NotRequired[List[str]]
    ignoreFailure: NotRequired[bool]
    currentBuildSummary: NotRequired[BuildSummaryTypeDef]
    priorBuildSummaryList: NotRequired[List[BuildSummaryTypeDef]]

class CreateWebhookOutputTypeDef(TypedDict):
    webhook: WebhookTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateWebhookOutputTypeDef(TypedDict):
    webhook: WebhookTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class EnvironmentPlatformTypeDef(TypedDict):
    platform: NotRequired[PlatformTypeType]
    languages: NotRequired[List[EnvironmentLanguageTypeDef]]

class ProxyConfigurationTypeDef(TypedDict):
    defaultBehavior: NotRequired[FleetProxyRuleBehaviorType]
    orderedProxyRules: NotRequired[Sequence[FleetProxyRuleUnionTypeDef]]

BuildTypeDef = TypedDict(
    "BuildTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "buildNumber": NotRequired[int],
        "startTime": NotRequired[datetime],
        "endTime": NotRequired[datetime],
        "currentPhase": NotRequired[str],
        "buildStatus": NotRequired[StatusTypeType],
        "sourceVersion": NotRequired[str],
        "resolvedSourceVersion": NotRequired[str],
        "projectName": NotRequired[str],
        "phases": NotRequired[List[BuildPhaseTypeDef]],
        "source": NotRequired[ProjectSourceTypeDef],
        "secondarySources": NotRequired[List[ProjectSourceTypeDef]],
        "secondarySourceVersions": NotRequired[List[ProjectSourceVersionTypeDef]],
        "artifacts": NotRequired[BuildArtifactsTypeDef],
        "secondaryArtifacts": NotRequired[List[BuildArtifactsTypeDef]],
        "cache": NotRequired[ProjectCacheOutputTypeDef],
        "environment": NotRequired[ProjectEnvironmentOutputTypeDef],
        "serviceRole": NotRequired[str],
        "logs": NotRequired[LogsLocationTypeDef],
        "timeoutInMinutes": NotRequired[int],
        "queuedTimeoutInMinutes": NotRequired[int],
        "buildComplete": NotRequired[bool],
        "initiator": NotRequired[str],
        "vpcConfig": NotRequired[VpcConfigOutputTypeDef],
        "networkInterface": NotRequired[NetworkInterfaceTypeDef],
        "encryptionKey": NotRequired[str],
        "exportedEnvironmentVariables": NotRequired[List[ExportedEnvironmentVariableTypeDef]],
        "reportArns": NotRequired[List[str]],
        "fileSystemLocations": NotRequired[List[ProjectFileSystemLocationTypeDef]],
        "debugSession": NotRequired[DebugSessionTypeDef],
        "buildBatchArn": NotRequired[str],
        "autoRetryConfig": NotRequired[AutoRetryConfigTypeDef],
    },
)

class ProjectTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    description: NotRequired[str]
    source: NotRequired[ProjectSourceTypeDef]
    secondarySources: NotRequired[List[ProjectSourceTypeDef]]
    sourceVersion: NotRequired[str]
    secondarySourceVersions: NotRequired[List[ProjectSourceVersionTypeDef]]
    artifacts: NotRequired[ProjectArtifactsTypeDef]
    secondaryArtifacts: NotRequired[List[ProjectArtifactsTypeDef]]
    cache: NotRequired[ProjectCacheOutputTypeDef]
    environment: NotRequired[ProjectEnvironmentOutputTypeDef]
    serviceRole: NotRequired[str]
    timeoutInMinutes: NotRequired[int]
    queuedTimeoutInMinutes: NotRequired[int]
    encryptionKey: NotRequired[str]
    tags: NotRequired[List[TagTypeDef]]
    created: NotRequired[datetime]
    lastModified: NotRequired[datetime]
    webhook: NotRequired[WebhookTypeDef]
    vpcConfig: NotRequired[VpcConfigOutputTypeDef]
    badge: NotRequired[ProjectBadgeTypeDef]
    logsConfig: NotRequired[LogsConfigTypeDef]
    fileSystemLocations: NotRequired[List[ProjectFileSystemLocationTypeDef]]
    buildBatchConfig: NotRequired[ProjectBuildBatchConfigOutputTypeDef]
    concurrentBuildLimit: NotRequired[int]
    projectVisibility: NotRequired[ProjectVisibilityTypeType]
    publicProjectAlias: NotRequired[str]
    resourceAccessRole: NotRequired[str]
    autoRetryLimit: NotRequired[int]

class StartBuildInputRequestTypeDef(TypedDict):
    projectName: str
    secondarySourcesOverride: NotRequired[Sequence[ProjectSourceTypeDef]]
    secondarySourcesVersionOverride: NotRequired[Sequence[ProjectSourceVersionTypeDef]]
    sourceVersion: NotRequired[str]
    artifactsOverride: NotRequired[ProjectArtifactsTypeDef]
    secondaryArtifactsOverride: NotRequired[Sequence[ProjectArtifactsTypeDef]]
    environmentVariablesOverride: NotRequired[Sequence[EnvironmentVariableTypeDef]]
    sourceTypeOverride: NotRequired[SourceTypeType]
    sourceLocationOverride: NotRequired[str]
    sourceAuthOverride: NotRequired[SourceAuthTypeDef]
    gitCloneDepthOverride: NotRequired[int]
    gitSubmodulesConfigOverride: NotRequired[GitSubmodulesConfigTypeDef]
    buildspecOverride: NotRequired[str]
    insecureSslOverride: NotRequired[bool]
    reportBuildStatusOverride: NotRequired[bool]
    buildStatusConfigOverride: NotRequired[BuildStatusConfigTypeDef]
    environmentTypeOverride: NotRequired[EnvironmentTypeType]
    imageOverride: NotRequired[str]
    computeTypeOverride: NotRequired[ComputeTypeType]
    certificateOverride: NotRequired[str]
    cacheOverride: NotRequired[ProjectCacheTypeDef]
    serviceRoleOverride: NotRequired[str]
    privilegedModeOverride: NotRequired[bool]
    timeoutInMinutesOverride: NotRequired[int]
    queuedTimeoutInMinutesOverride: NotRequired[int]
    encryptionKeyOverride: NotRequired[str]
    idempotencyToken: NotRequired[str]
    logsConfigOverride: NotRequired[LogsConfigTypeDef]
    registryCredentialOverride: NotRequired[RegistryCredentialTypeDef]
    imagePullCredentialsTypeOverride: NotRequired[ImagePullCredentialsTypeType]
    debugSessionEnabled: NotRequired[bool]
    fleetOverride: NotRequired[ProjectFleetTypeDef]
    autoRetryLimitOverride: NotRequired[int]

CreateReportGroupInputRequestTypeDef = TypedDict(
    "CreateReportGroupInputRequestTypeDef",
    {
        "name": str,
        "type": ReportTypeType,
        "exportConfig": ReportExportConfigTypeDef,
        "tags": NotRequired[Sequence[TagTypeDef]],
    },
)
ReportGroupTypeDef = TypedDict(
    "ReportGroupTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "type": NotRequired[ReportTypeType],
        "exportConfig": NotRequired[ReportExportConfigTypeDef],
        "created": NotRequired[datetime],
        "lastModified": NotRequired[datetime],
        "tags": NotRequired[List[TagTypeDef]],
        "status": NotRequired[ReportGroupStatusTypeType],
    },
)
ReportTypeDef = TypedDict(
    "ReportTypeDef",
    {
        "arn": NotRequired[str],
        "type": NotRequired[ReportTypeType],
        "name": NotRequired[str],
        "reportGroupArn": NotRequired[str],
        "executionId": NotRequired[str],
        "status": NotRequired[ReportStatusTypeType],
        "created": NotRequired[datetime],
        "expired": NotRequired[datetime],
        "exportConfig": NotRequired[ReportExportConfigTypeDef],
        "truncated": NotRequired[bool],
        "testSummary": NotRequired[TestReportSummaryTypeDef],
        "codeCoverageSummary": NotRequired[CodeCoverageReportSummaryTypeDef],
    },
)

class UpdateReportGroupInputRequestTypeDef(TypedDict):
    arn: str
    exportConfig: NotRequired[ReportExportConfigTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]

FleetTypeDef = TypedDict(
    "FleetTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "id": NotRequired[str],
        "created": NotRequired[datetime],
        "lastModified": NotRequired[datetime],
        "status": NotRequired[FleetStatusTypeDef],
        "baseCapacity": NotRequired[int],
        "environmentType": NotRequired[EnvironmentTypeType],
        "computeType": NotRequired[ComputeTypeType],
        "computeConfiguration": NotRequired[ComputeConfigurationTypeDef],
        "scalingConfiguration": NotRequired[ScalingConfigurationOutputTypeDef],
        "overflowBehavior": NotRequired[FleetOverflowBehaviorType],
        "vpcConfig": NotRequired[VpcConfigOutputTypeDef],
        "proxyConfiguration": NotRequired[ProxyConfigurationOutputTypeDef],
        "imageId": NotRequired[str],
        "fleetServiceRole": NotRequired[str],
        "tags": NotRequired[List[TagTypeDef]],
    },
)

class CreateProjectInputRequestTypeDef(TypedDict):
    name: str
    source: ProjectSourceTypeDef
    artifacts: ProjectArtifactsTypeDef
    environment: ProjectEnvironmentTypeDef
    serviceRole: str
    description: NotRequired[str]
    secondarySources: NotRequired[Sequence[ProjectSourceTypeDef]]
    sourceVersion: NotRequired[str]
    secondarySourceVersions: NotRequired[Sequence[ProjectSourceVersionTypeDef]]
    secondaryArtifacts: NotRequired[Sequence[ProjectArtifactsTypeDef]]
    cache: NotRequired[ProjectCacheTypeDef]
    timeoutInMinutes: NotRequired[int]
    queuedTimeoutInMinutes: NotRequired[int]
    encryptionKey: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    vpcConfig: NotRequired[VpcConfigTypeDef]
    badgeEnabled: NotRequired[bool]
    logsConfig: NotRequired[LogsConfigTypeDef]
    fileSystemLocations: NotRequired[Sequence[ProjectFileSystemLocationTypeDef]]
    buildBatchConfig: NotRequired[ProjectBuildBatchConfigTypeDef]
    concurrentBuildLimit: NotRequired[int]
    autoRetryLimit: NotRequired[int]

class StartBuildBatchInputRequestTypeDef(TypedDict):
    projectName: str
    secondarySourcesOverride: NotRequired[Sequence[ProjectSourceTypeDef]]
    secondarySourcesVersionOverride: NotRequired[Sequence[ProjectSourceVersionTypeDef]]
    sourceVersion: NotRequired[str]
    artifactsOverride: NotRequired[ProjectArtifactsTypeDef]
    secondaryArtifactsOverride: NotRequired[Sequence[ProjectArtifactsTypeDef]]
    environmentVariablesOverride: NotRequired[Sequence[EnvironmentVariableTypeDef]]
    sourceTypeOverride: NotRequired[SourceTypeType]
    sourceLocationOverride: NotRequired[str]
    sourceAuthOverride: NotRequired[SourceAuthTypeDef]
    gitCloneDepthOverride: NotRequired[int]
    gitSubmodulesConfigOverride: NotRequired[GitSubmodulesConfigTypeDef]
    buildspecOverride: NotRequired[str]
    insecureSslOverride: NotRequired[bool]
    reportBuildBatchStatusOverride: NotRequired[bool]
    environmentTypeOverride: NotRequired[EnvironmentTypeType]
    imageOverride: NotRequired[str]
    computeTypeOverride: NotRequired[ComputeTypeType]
    certificateOverride: NotRequired[str]
    cacheOverride: NotRequired[ProjectCacheTypeDef]
    serviceRoleOverride: NotRequired[str]
    privilegedModeOverride: NotRequired[bool]
    buildTimeoutInMinutesOverride: NotRequired[int]
    queuedTimeoutInMinutesOverride: NotRequired[int]
    encryptionKeyOverride: NotRequired[str]
    idempotencyToken: NotRequired[str]
    logsConfigOverride: NotRequired[LogsConfigTypeDef]
    registryCredentialOverride: NotRequired[RegistryCredentialTypeDef]
    imagePullCredentialsTypeOverride: NotRequired[ImagePullCredentialsTypeType]
    buildBatchConfigOverride: NotRequired[ProjectBuildBatchConfigTypeDef]
    debugSessionEnabled: NotRequired[bool]

class UpdateProjectInputRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    source: NotRequired[ProjectSourceTypeDef]
    secondarySources: NotRequired[Sequence[ProjectSourceTypeDef]]
    sourceVersion: NotRequired[str]
    secondarySourceVersions: NotRequired[Sequence[ProjectSourceVersionTypeDef]]
    artifacts: NotRequired[ProjectArtifactsTypeDef]
    secondaryArtifacts: NotRequired[Sequence[ProjectArtifactsTypeDef]]
    cache: NotRequired[ProjectCacheTypeDef]
    environment: NotRequired[ProjectEnvironmentTypeDef]
    serviceRole: NotRequired[str]
    timeoutInMinutes: NotRequired[int]
    queuedTimeoutInMinutes: NotRequired[int]
    encryptionKey: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    vpcConfig: NotRequired[VpcConfigTypeDef]
    badgeEnabled: NotRequired[bool]
    logsConfig: NotRequired[LogsConfigTypeDef]
    fileSystemLocations: NotRequired[Sequence[ProjectFileSystemLocationTypeDef]]
    buildBatchConfig: NotRequired[ProjectBuildBatchConfigTypeDef]
    concurrentBuildLimit: NotRequired[int]
    autoRetryLimit: NotRequired[int]

BuildBatchTypeDef = TypedDict(
    "BuildBatchTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "startTime": NotRequired[datetime],
        "endTime": NotRequired[datetime],
        "currentPhase": NotRequired[str],
        "buildBatchStatus": NotRequired[StatusTypeType],
        "sourceVersion": NotRequired[str],
        "resolvedSourceVersion": NotRequired[str],
        "projectName": NotRequired[str],
        "phases": NotRequired[List[BuildBatchPhaseTypeDef]],
        "source": NotRequired[ProjectSourceTypeDef],
        "secondarySources": NotRequired[List[ProjectSourceTypeDef]],
        "secondarySourceVersions": NotRequired[List[ProjectSourceVersionTypeDef]],
        "artifacts": NotRequired[BuildArtifactsTypeDef],
        "secondaryArtifacts": NotRequired[List[BuildArtifactsTypeDef]],
        "cache": NotRequired[ProjectCacheOutputTypeDef],
        "environment": NotRequired[ProjectEnvironmentOutputTypeDef],
        "serviceRole": NotRequired[str],
        "logConfig": NotRequired[LogsConfigTypeDef],
        "buildTimeoutInMinutes": NotRequired[int],
        "queuedTimeoutInMinutes": NotRequired[int],
        "complete": NotRequired[bool],
        "initiator": NotRequired[str],
        "vpcConfig": NotRequired[VpcConfigOutputTypeDef],
        "encryptionKey": NotRequired[str],
        "buildBatchNumber": NotRequired[int],
        "fileSystemLocations": NotRequired[List[ProjectFileSystemLocationTypeDef]],
        "buildBatchConfig": NotRequired[ProjectBuildBatchConfigOutputTypeDef],
        "buildGroups": NotRequired[List[BuildGroupTypeDef]],
        "debugSessionEnabled": NotRequired[bool],
    },
)

class ListCuratedEnvironmentImagesOutputTypeDef(TypedDict):
    platforms: List[EnvironmentPlatformTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFleetInputRequestTypeDef(TypedDict):
    name: str
    baseCapacity: int
    environmentType: EnvironmentTypeType
    computeType: ComputeTypeType
    computeConfiguration: NotRequired[ComputeConfigurationTypeDef]
    scalingConfiguration: NotRequired[ScalingConfigurationInputTypeDef]
    overflowBehavior: NotRequired[FleetOverflowBehaviorType]
    vpcConfig: NotRequired[VpcConfigTypeDef]
    proxyConfiguration: NotRequired[ProxyConfigurationTypeDef]
    imageId: NotRequired[str]
    fleetServiceRole: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class UpdateFleetInputRequestTypeDef(TypedDict):
    arn: str
    baseCapacity: NotRequired[int]
    environmentType: NotRequired[EnvironmentTypeType]
    computeType: NotRequired[ComputeTypeType]
    computeConfiguration: NotRequired[ComputeConfigurationTypeDef]
    scalingConfiguration: NotRequired[ScalingConfigurationInputTypeDef]
    overflowBehavior: NotRequired[FleetOverflowBehaviorType]
    vpcConfig: NotRequired[VpcConfigTypeDef]
    proxyConfiguration: NotRequired[ProxyConfigurationTypeDef]
    imageId: NotRequired[str]
    fleetServiceRole: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class BatchGetBuildsOutputTypeDef(TypedDict):
    builds: List[BuildTypeDef]
    buildsNotFound: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class RetryBuildOutputTypeDef(TypedDict):
    build: BuildTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartBuildOutputTypeDef(TypedDict):
    build: BuildTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StopBuildOutputTypeDef(TypedDict):
    build: BuildTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetProjectsOutputTypeDef(TypedDict):
    projects: List[ProjectTypeDef]
    projectsNotFound: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateProjectOutputTypeDef(TypedDict):
    project: ProjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateProjectOutputTypeDef(TypedDict):
    project: ProjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetReportGroupsOutputTypeDef(TypedDict):
    reportGroups: List[ReportGroupTypeDef]
    reportGroupsNotFound: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateReportGroupOutputTypeDef(TypedDict):
    reportGroup: ReportGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateReportGroupOutputTypeDef(TypedDict):
    reportGroup: ReportGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetReportsOutputTypeDef(TypedDict):
    reports: List[ReportTypeDef]
    reportsNotFound: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetFleetsOutputTypeDef(TypedDict):
    fleets: List[FleetTypeDef]
    fleetsNotFound: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFleetOutputTypeDef(TypedDict):
    fleet: FleetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateFleetOutputTypeDef(TypedDict):
    fleet: FleetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetBuildBatchesOutputTypeDef(TypedDict):
    buildBatches: List[BuildBatchTypeDef]
    buildBatchesNotFound: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class RetryBuildBatchOutputTypeDef(TypedDict):
    buildBatch: BuildBatchTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartBuildBatchOutputTypeDef(TypedDict):
    buildBatch: BuildBatchTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StopBuildBatchOutputTypeDef(TypedDict):
    buildBatch: BuildBatchTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
