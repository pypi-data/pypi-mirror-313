"""
Type annotations for m2 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/type_defs/)

Usage::

    ```python
    from mypy_boto3_m2.type_defs import AlternateKeyTypeDef

    data: AlternateKeyTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ApplicationDeploymentLifecycleType,
    ApplicationLifecycleType,
    ApplicationVersionLifecycleType,
    BatchJobExecutionStatusType,
    BatchJobTypeType,
    DataSetTaskLifecycleType,
    DeploymentLifecycleType,
    EngineTypeType,
    EnvironmentLifecycleType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AlternateKeyTypeDef",
    "ApplicationSummaryTypeDef",
    "ApplicationVersionSummaryTypeDef",
    "BatchJobDefinitionTypeDef",
    "BatchJobExecutionSummaryTypeDef",
    "BatchJobIdentifierTypeDef",
    "CancelBatchJobExecutionRequestRequestTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateDataSetImportTaskRequestRequestTypeDef",
    "CreateDataSetImportTaskResponseTypeDef",
    "CreateDeploymentRequestRequestTypeDef",
    "CreateDeploymentResponseTypeDef",
    "CreateEnvironmentRequestRequestTypeDef",
    "CreateEnvironmentResponseTypeDef",
    "DataSetImportConfigTypeDef",
    "DataSetImportItemTypeDef",
    "DataSetImportSummaryTypeDef",
    "DataSetImportTaskTypeDef",
    "DataSetSummaryTypeDef",
    "DataSetTypeDef",
    "DatasetDetailOrgAttributesTypeDef",
    "DatasetOrgAttributesTypeDef",
    "DefinitionTypeDef",
    "DeleteApplicationFromEnvironmentRequestRequestTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteEnvironmentRequestRequestTypeDef",
    "DeployedVersionSummaryTypeDef",
    "DeploymentSummaryTypeDef",
    "EfsStorageConfigurationTypeDef",
    "EngineVersionsSummaryTypeDef",
    "EnvironmentSummaryTypeDef",
    "ExternalLocationTypeDef",
    "FileBatchJobDefinitionTypeDef",
    "FileBatchJobIdentifierTypeDef",
    "FsxStorageConfigurationTypeDef",
    "GdgAttributesTypeDef",
    "GdgDetailAttributesTypeDef",
    "GetApplicationRequestRequestTypeDef",
    "GetApplicationResponseTypeDef",
    "GetApplicationVersionRequestRequestTypeDef",
    "GetApplicationVersionResponseTypeDef",
    "GetBatchJobExecutionRequestRequestTypeDef",
    "GetBatchJobExecutionResponseTypeDef",
    "GetDataSetDetailsRequestRequestTypeDef",
    "GetDataSetDetailsResponseTypeDef",
    "GetDataSetImportTaskRequestRequestTypeDef",
    "GetDataSetImportTaskResponseTypeDef",
    "GetDeploymentRequestRequestTypeDef",
    "GetDeploymentResponseTypeDef",
    "GetEnvironmentRequestRequestTypeDef",
    "GetEnvironmentResponseTypeDef",
    "GetSignedBluinsightsUrlResponseTypeDef",
    "HighAvailabilityConfigTypeDef",
    "JobIdentifierTypeDef",
    "JobStepRestartMarkerTypeDef",
    "JobStepTypeDef",
    "ListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef",
    "ListApplicationVersionsRequestRequestTypeDef",
    "ListApplicationVersionsResponseTypeDef",
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListBatchJobDefinitionsRequestListBatchJobDefinitionsPaginateTypeDef",
    "ListBatchJobDefinitionsRequestRequestTypeDef",
    "ListBatchJobDefinitionsResponseTypeDef",
    "ListBatchJobExecutionsRequestListBatchJobExecutionsPaginateTypeDef",
    "ListBatchJobExecutionsRequestRequestTypeDef",
    "ListBatchJobExecutionsResponseTypeDef",
    "ListBatchJobRestartPointsRequestRequestTypeDef",
    "ListBatchJobRestartPointsResponseTypeDef",
    "ListDataSetImportHistoryRequestListDataSetImportHistoryPaginateTypeDef",
    "ListDataSetImportHistoryRequestRequestTypeDef",
    "ListDataSetImportHistoryResponseTypeDef",
    "ListDataSetsRequestListDataSetsPaginateTypeDef",
    "ListDataSetsRequestRequestTypeDef",
    "ListDataSetsResponseTypeDef",
    "ListDeploymentsRequestListDeploymentsPaginateTypeDef",
    "ListDeploymentsRequestRequestTypeDef",
    "ListDeploymentsResponseTypeDef",
    "ListEngineVersionsRequestListEngineVersionsPaginateTypeDef",
    "ListEngineVersionsRequestRequestTypeDef",
    "ListEngineVersionsResponseTypeDef",
    "ListEnvironmentsRequestListEnvironmentsPaginateTypeDef",
    "ListEnvironmentsRequestRequestTypeDef",
    "ListEnvironmentsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LogGroupSummaryTypeDef",
    "MaintenanceScheduleTypeDef",
    "PaginatorConfigTypeDef",
    "PendingMaintenanceTypeDef",
    "PoAttributesTypeDef",
    "PoDetailAttributesTypeDef",
    "PrimaryKeyTypeDef",
    "PsAttributesTypeDef",
    "PsDetailAttributesTypeDef",
    "RecordLengthTypeDef",
    "ResponseMetadataTypeDef",
    "RestartBatchJobIdentifierTypeDef",
    "S3BatchJobIdentifierTypeDef",
    "ScriptBatchJobDefinitionTypeDef",
    "ScriptBatchJobIdentifierTypeDef",
    "StartApplicationRequestRequestTypeDef",
    "StartBatchJobRequestRequestTypeDef",
    "StartBatchJobResponseTypeDef",
    "StopApplicationRequestRequestTypeDef",
    "StorageConfigurationTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateApplicationResponseTypeDef",
    "UpdateEnvironmentRequestRequestTypeDef",
    "UpdateEnvironmentResponseTypeDef",
    "VsamAttributesTypeDef",
    "VsamDetailAttributesTypeDef",
)


class AlternateKeyTypeDef(TypedDict):
    length: int
    offset: int
    allowDuplicates: NotRequired[bool]
    name: NotRequired[str]


class ApplicationSummaryTypeDef(TypedDict):
    applicationArn: str
    applicationId: str
    applicationVersion: int
    creationTime: datetime
    engineType: EngineTypeType
    name: str
    status: ApplicationLifecycleType
    deploymentStatus: NotRequired[ApplicationDeploymentLifecycleType]
    description: NotRequired[str]
    environmentId: NotRequired[str]
    lastStartTime: NotRequired[datetime]
    roleArn: NotRequired[str]
    versionStatus: NotRequired[ApplicationVersionLifecycleType]


class ApplicationVersionSummaryTypeDef(TypedDict):
    applicationVersion: int
    creationTime: datetime
    status: ApplicationVersionLifecycleType
    statusReason: NotRequired[str]


class FileBatchJobDefinitionTypeDef(TypedDict):
    fileName: str
    folderPath: NotRequired[str]


class ScriptBatchJobDefinitionTypeDef(TypedDict):
    scriptName: str


class FileBatchJobIdentifierTypeDef(TypedDict):
    fileName: str
    folderPath: NotRequired[str]


class ScriptBatchJobIdentifierTypeDef(TypedDict):
    scriptName: str


class CancelBatchJobExecutionRequestRequestTypeDef(TypedDict):
    applicationId: str
    executionId: str
    authSecretsManagerArn: NotRequired[str]


class DefinitionTypeDef(TypedDict):
    content: NotRequired[str]
    s3Location: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateDeploymentRequestRequestTypeDef(TypedDict):
    applicationId: str
    applicationVersion: int
    environmentId: str
    clientToken: NotRequired[str]


class HighAvailabilityConfigTypeDef(TypedDict):
    desiredCapacity: int


class ExternalLocationTypeDef(TypedDict):
    s3Location: NotRequired[str]


class DataSetImportSummaryTypeDef(TypedDict):
    failed: int
    inProgress: int
    pending: int
    succeeded: int
    total: int


DataSetSummaryTypeDef = TypedDict(
    "DataSetSummaryTypeDef",
    {
        "dataSetName": str,
        "creationTime": NotRequired[datetime],
        "dataSetOrg": NotRequired[str],
        "format": NotRequired[str],
        "lastReferencedTime": NotRequired[datetime],
        "lastUpdatedTime": NotRequired[datetime],
    },
)
RecordLengthTypeDef = TypedDict(
    "RecordLengthTypeDef",
    {
        "max": int,
        "min": int,
    },
)


class GdgDetailAttributesTypeDef(TypedDict):
    limit: NotRequired[int]
    rollDisposition: NotRequired[str]


PoDetailAttributesTypeDef = TypedDict(
    "PoDetailAttributesTypeDef",
    {
        "encoding": str,
        "format": str,
    },
)
PsDetailAttributesTypeDef = TypedDict(
    "PsDetailAttributesTypeDef",
    {
        "encoding": str,
        "format": str,
    },
)


class GdgAttributesTypeDef(TypedDict):
    limit: NotRequired[int]
    rollDisposition: NotRequired[str]


PoAttributesTypeDef = TypedDict(
    "PoAttributesTypeDef",
    {
        "format": str,
        "memberFileExtensions": Sequence[str],
        "encoding": NotRequired[str],
    },
)
PsAttributesTypeDef = TypedDict(
    "PsAttributesTypeDef",
    {
        "format": str,
        "encoding": NotRequired[str],
    },
)


class DeleteApplicationFromEnvironmentRequestRequestTypeDef(TypedDict):
    applicationId: str
    environmentId: str


class DeleteApplicationRequestRequestTypeDef(TypedDict):
    applicationId: str


class DeleteEnvironmentRequestRequestTypeDef(TypedDict):
    environmentId: str


class DeployedVersionSummaryTypeDef(TypedDict):
    applicationVersion: int
    status: DeploymentLifecycleType
    statusReason: NotRequired[str]


class DeploymentSummaryTypeDef(TypedDict):
    applicationId: str
    applicationVersion: int
    creationTime: datetime
    deploymentId: str
    environmentId: str
    status: DeploymentLifecycleType
    statusReason: NotRequired[str]


class EfsStorageConfigurationTypeDef(TypedDict):
    fileSystemId: str
    mountPoint: str


class EngineVersionsSummaryTypeDef(TypedDict):
    engineType: str
    engineVersion: str


class EnvironmentSummaryTypeDef(TypedDict):
    creationTime: datetime
    engineType: EngineTypeType
    engineVersion: str
    environmentArn: str
    environmentId: str
    instanceType: str
    name: str
    status: EnvironmentLifecycleType


class FsxStorageConfigurationTypeDef(TypedDict):
    fileSystemId: str
    mountPoint: str


class GetApplicationRequestRequestTypeDef(TypedDict):
    applicationId: str


class LogGroupSummaryTypeDef(TypedDict):
    logGroupName: str
    logType: str


class GetApplicationVersionRequestRequestTypeDef(TypedDict):
    applicationId: str
    applicationVersion: int


class GetBatchJobExecutionRequestRequestTypeDef(TypedDict):
    applicationId: str
    executionId: str


class JobStepRestartMarkerTypeDef(TypedDict):
    fromStep: str
    fromProcStep: NotRequired[str]
    toProcStep: NotRequired[str]
    toStep: NotRequired[str]


class GetDataSetDetailsRequestRequestTypeDef(TypedDict):
    applicationId: str
    dataSetName: str


class GetDataSetImportTaskRequestRequestTypeDef(TypedDict):
    applicationId: str
    taskId: str


class GetDeploymentRequestRequestTypeDef(TypedDict):
    applicationId: str
    deploymentId: str


class GetEnvironmentRequestRequestTypeDef(TypedDict):
    environmentId: str


class JobIdentifierTypeDef(TypedDict):
    fileName: NotRequired[str]
    scriptName: NotRequired[str]


class JobStepTypeDef(TypedDict):
    procStepName: NotRequired[str]
    procStepNumber: NotRequired[int]
    stepCondCode: NotRequired[str]
    stepName: NotRequired[str]
    stepNumber: NotRequired[int]
    stepRestartable: NotRequired[bool]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListApplicationVersionsRequestRequestTypeDef(TypedDict):
    applicationId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListApplicationsRequestRequestTypeDef(TypedDict):
    environmentId: NotRequired[str]
    maxResults: NotRequired[int]
    names: NotRequired[Sequence[str]]
    nextToken: NotRequired[str]


class ListBatchJobDefinitionsRequestRequestTypeDef(TypedDict):
    applicationId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    prefix: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class ListBatchJobRestartPointsRequestRequestTypeDef(TypedDict):
    applicationId: str
    executionId: str
    authSecretsManagerArn: NotRequired[str]


class ListDataSetImportHistoryRequestRequestTypeDef(TypedDict):
    applicationId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListDataSetsRequestRequestTypeDef(TypedDict):
    applicationId: str
    maxResults: NotRequired[int]
    nameFilter: NotRequired[str]
    nextToken: NotRequired[str]
    prefix: NotRequired[str]


class ListDeploymentsRequestRequestTypeDef(TypedDict):
    applicationId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListEngineVersionsRequestRequestTypeDef(TypedDict):
    engineType: NotRequired[EngineTypeType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListEnvironmentsRequestRequestTypeDef(TypedDict):
    engineType: NotRequired[EngineTypeType]
    maxResults: NotRequired[int]
    names: NotRequired[Sequence[str]]
    nextToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class MaintenanceScheduleTypeDef(TypedDict):
    endTime: NotRequired[datetime]
    startTime: NotRequired[datetime]


class PrimaryKeyTypeDef(TypedDict):
    length: int
    offset: int
    name: NotRequired[str]


class StartApplicationRequestRequestTypeDef(TypedDict):
    applicationId: str


class StopApplicationRequestRequestTypeDef(TypedDict):
    applicationId: str
    forceStop: NotRequired[bool]


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateEnvironmentRequestRequestTypeDef(TypedDict):
    environmentId: str
    applyDuringMaintenanceWindow: NotRequired[bool]
    desiredCapacity: NotRequired[int]
    engineVersion: NotRequired[str]
    forceUpdate: NotRequired[bool]
    instanceType: NotRequired[str]
    preferredMaintenanceWindow: NotRequired[str]


class BatchJobDefinitionTypeDef(TypedDict):
    fileBatchJobDefinition: NotRequired[FileBatchJobDefinitionTypeDef]
    scriptBatchJobDefinition: NotRequired[ScriptBatchJobDefinitionTypeDef]


class CreateApplicationRequestRequestTypeDef(TypedDict):
    definition: DefinitionTypeDef
    engineType: EngineTypeType
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    kmsKeyId: NotRequired[str]
    roleArn: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class UpdateApplicationRequestRequestTypeDef(TypedDict):
    applicationId: str
    currentApplicationVersion: int
    definition: NotRequired[DefinitionTypeDef]
    description: NotRequired[str]


class CreateApplicationResponseTypeDef(TypedDict):
    applicationArn: str
    applicationId: str
    applicationVersion: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataSetImportTaskResponseTypeDef(TypedDict):
    taskId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDeploymentResponseTypeDef(TypedDict):
    deploymentId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEnvironmentResponseTypeDef(TypedDict):
    environmentId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetApplicationVersionResponseTypeDef(TypedDict):
    applicationVersion: int
    creationTime: datetime
    definitionContent: str
    description: str
    name: str
    status: ApplicationVersionLifecycleType
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetDeploymentResponseTypeDef(TypedDict):
    applicationId: str
    applicationVersion: int
    creationTime: datetime
    deploymentId: str
    environmentId: str
    status: DeploymentLifecycleType
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetSignedBluinsightsUrlResponseTypeDef(TypedDict):
    signedBiUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListApplicationVersionsResponseTypeDef(TypedDict):
    applicationVersions: List[ApplicationVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListApplicationsResponseTypeDef(TypedDict):
    applications: List[ApplicationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class StartBatchJobResponseTypeDef(TypedDict):
    executionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateApplicationResponseTypeDef(TypedDict):
    applicationVersion: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateEnvironmentResponseTypeDef(TypedDict):
    environmentId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DataSetImportTaskTypeDef(TypedDict):
    status: DataSetTaskLifecycleType
    summary: DataSetImportSummaryTypeDef
    taskId: str
    statusReason: NotRequired[str]


class GetDataSetImportTaskResponseTypeDef(TypedDict):
    status: DataSetTaskLifecycleType
    summary: DataSetImportSummaryTypeDef
    taskId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListDataSetsResponseTypeDef(TypedDict):
    dataSets: List[DataSetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListDeploymentsResponseTypeDef(TypedDict):
    deployments: List[DeploymentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListEngineVersionsResponseTypeDef(TypedDict):
    engineVersions: List[EngineVersionsSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListEnvironmentsResponseTypeDef(TypedDict):
    environments: List[EnvironmentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StorageConfigurationTypeDef(TypedDict):
    efs: NotRequired[EfsStorageConfigurationTypeDef]
    fsx: NotRequired[FsxStorageConfigurationTypeDef]


class GetApplicationResponseTypeDef(TypedDict):
    applicationArn: str
    applicationId: str
    creationTime: datetime
    deployedVersion: DeployedVersionSummaryTypeDef
    description: str
    engineType: EngineTypeType
    environmentId: str
    kmsKeyId: str
    lastStartTime: datetime
    latestVersion: ApplicationVersionSummaryTypeDef
    listenerArns: List[str]
    listenerPorts: List[int]
    loadBalancerDnsName: str
    logGroups: List[LogGroupSummaryTypeDef]
    name: str
    roleArn: str
    status: ApplicationLifecycleType
    statusReason: str
    tags: Dict[str, str]
    targetGroupArns: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class RestartBatchJobIdentifierTypeDef(TypedDict):
    executionId: str
    jobStepRestartMarker: JobStepRestartMarkerTypeDef


class S3BatchJobIdentifierTypeDef(TypedDict):
    bucket: str
    identifier: JobIdentifierTypeDef
    keyPrefix: NotRequired[str]


class ListBatchJobRestartPointsResponseTypeDef(TypedDict):
    batchJobSteps: List[JobStepTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef(TypedDict):
    applicationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListApplicationsRequestListApplicationsPaginateTypeDef(TypedDict):
    environmentId: NotRequired[str]
    names: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBatchJobDefinitionsRequestListBatchJobDefinitionsPaginateTypeDef(TypedDict):
    applicationId: str
    prefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataSetImportHistoryRequestListDataSetImportHistoryPaginateTypeDef(TypedDict):
    applicationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataSetsRequestListDataSetsPaginateTypeDef(TypedDict):
    applicationId: str
    nameFilter: NotRequired[str]
    prefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDeploymentsRequestListDeploymentsPaginateTypeDef(TypedDict):
    applicationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEngineVersionsRequestListEngineVersionsPaginateTypeDef(TypedDict):
    engineType: NotRequired[EngineTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEnvironmentsRequestListEnvironmentsPaginateTypeDef(TypedDict):
    engineType: NotRequired[EngineTypeType]
    names: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBatchJobExecutionsRequestListBatchJobExecutionsPaginateTypeDef(TypedDict):
    applicationId: str
    executionIds: NotRequired[Sequence[str]]
    jobName: NotRequired[str]
    startedAfter: NotRequired[TimestampTypeDef]
    startedBefore: NotRequired[TimestampTypeDef]
    status: NotRequired[BatchJobExecutionStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBatchJobExecutionsRequestRequestTypeDef(TypedDict):
    applicationId: str
    executionIds: NotRequired[Sequence[str]]
    jobName: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    startedAfter: NotRequired[TimestampTypeDef]
    startedBefore: NotRequired[TimestampTypeDef]
    status: NotRequired[BatchJobExecutionStatusType]


class PendingMaintenanceTypeDef(TypedDict):
    engineVersion: NotRequired[str]
    schedule: NotRequired[MaintenanceScheduleTypeDef]


VsamAttributesTypeDef = TypedDict(
    "VsamAttributesTypeDef",
    {
        "format": str,
        "alternateKeys": NotRequired[Sequence[AlternateKeyTypeDef]],
        "compressed": NotRequired[bool],
        "encoding": NotRequired[str],
        "primaryKey": NotRequired[PrimaryKeyTypeDef],
    },
)


class VsamDetailAttributesTypeDef(TypedDict):
    alternateKeys: NotRequired[List[AlternateKeyTypeDef]]
    cacheAtStartup: NotRequired[bool]
    compressed: NotRequired[bool]
    encoding: NotRequired[str]
    primaryKey: NotRequired[PrimaryKeyTypeDef]
    recordFormat: NotRequired[str]


class ListBatchJobDefinitionsResponseTypeDef(TypedDict):
    batchJobDefinitions: List[BatchJobDefinitionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListDataSetImportHistoryResponseTypeDef(TypedDict):
    dataSetImportTasks: List[DataSetImportTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateEnvironmentRequestRequestTypeDef(TypedDict):
    engineType: EngineTypeType
    instanceType: str
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    engineVersion: NotRequired[str]
    highAvailabilityConfig: NotRequired[HighAvailabilityConfigTypeDef]
    kmsKeyId: NotRequired[str]
    preferredMaintenanceWindow: NotRequired[str]
    publiclyAccessible: NotRequired[bool]
    securityGroupIds: NotRequired[Sequence[str]]
    storageConfigurations: NotRequired[Sequence[StorageConfigurationTypeDef]]
    subnetIds: NotRequired[Sequence[str]]
    tags: NotRequired[Mapping[str, str]]


class BatchJobIdentifierTypeDef(TypedDict):
    fileBatchJobIdentifier: NotRequired[FileBatchJobIdentifierTypeDef]
    restartBatchJobIdentifier: NotRequired[RestartBatchJobIdentifierTypeDef]
    s3BatchJobIdentifier: NotRequired[S3BatchJobIdentifierTypeDef]
    scriptBatchJobIdentifier: NotRequired[ScriptBatchJobIdentifierTypeDef]


class GetEnvironmentResponseTypeDef(TypedDict):
    actualCapacity: int
    creationTime: datetime
    description: str
    engineType: EngineTypeType
    engineVersion: str
    environmentArn: str
    environmentId: str
    highAvailabilityConfig: HighAvailabilityConfigTypeDef
    instanceType: str
    kmsKeyId: str
    loadBalancerArn: str
    name: str
    pendingMaintenance: PendingMaintenanceTypeDef
    preferredMaintenanceWindow: str
    publiclyAccessible: bool
    securityGroupIds: List[str]
    status: EnvironmentLifecycleType
    statusReason: str
    storageConfigurations: List[StorageConfigurationTypeDef]
    subnetIds: List[str]
    tags: Dict[str, str]
    vpcId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DatasetOrgAttributesTypeDef(TypedDict):
    gdg: NotRequired[GdgAttributesTypeDef]
    po: NotRequired[PoAttributesTypeDef]
    ps: NotRequired[PsAttributesTypeDef]
    vsam: NotRequired[VsamAttributesTypeDef]


class DatasetDetailOrgAttributesTypeDef(TypedDict):
    gdg: NotRequired[GdgDetailAttributesTypeDef]
    po: NotRequired[PoDetailAttributesTypeDef]
    ps: NotRequired[PsDetailAttributesTypeDef]
    vsam: NotRequired[VsamDetailAttributesTypeDef]


class BatchJobExecutionSummaryTypeDef(TypedDict):
    applicationId: str
    executionId: str
    startTime: datetime
    status: BatchJobExecutionStatusType
    batchJobIdentifier: NotRequired[BatchJobIdentifierTypeDef]
    endTime: NotRequired[datetime]
    jobId: NotRequired[str]
    jobName: NotRequired[str]
    jobType: NotRequired[BatchJobTypeType]
    returnCode: NotRequired[str]


class GetBatchJobExecutionResponseTypeDef(TypedDict):
    applicationId: str
    batchJobIdentifier: BatchJobIdentifierTypeDef
    endTime: datetime
    executionId: str
    jobId: str
    jobName: str
    jobStepRestartMarker: JobStepRestartMarkerTypeDef
    jobType: BatchJobTypeType
    jobUser: str
    returnCode: str
    startTime: datetime
    status: BatchJobExecutionStatusType
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartBatchJobRequestRequestTypeDef(TypedDict):
    applicationId: str
    batchJobIdentifier: BatchJobIdentifierTypeDef
    authSecretsManagerArn: NotRequired[str]
    jobParams: NotRequired[Mapping[str, str]]


class DataSetTypeDef(TypedDict):
    datasetName: str
    datasetOrg: DatasetOrgAttributesTypeDef
    recordLength: RecordLengthTypeDef
    relativePath: NotRequired[str]
    storageType: NotRequired[str]


class GetDataSetDetailsResponseTypeDef(TypedDict):
    blocksize: int
    creationTime: datetime
    dataSetName: str
    dataSetOrg: DatasetDetailOrgAttributesTypeDef
    fileSize: int
    lastReferencedTime: datetime
    lastUpdatedTime: datetime
    location: str
    recordLength: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListBatchJobExecutionsResponseTypeDef(TypedDict):
    batchJobExecutions: List[BatchJobExecutionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DataSetImportItemTypeDef(TypedDict):
    dataSet: DataSetTypeDef
    externalLocation: ExternalLocationTypeDef


class DataSetImportConfigTypeDef(TypedDict):
    dataSets: NotRequired[Sequence[DataSetImportItemTypeDef]]
    s3Location: NotRequired[str]


class CreateDataSetImportTaskRequestRequestTypeDef(TypedDict):
    applicationId: str
    importConfig: DataSetImportConfigTypeDef
    clientToken: NotRequired[str]
