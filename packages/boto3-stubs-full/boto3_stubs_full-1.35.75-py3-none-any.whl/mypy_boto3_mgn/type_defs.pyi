"""
Type annotations for mgn service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/type_defs/)

Usage::

    ```python
    from mypy_boto3_mgn.type_defs import ApplicationAggregatedStatusTypeDef

    data: ApplicationAggregatedStatusTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ActionCategoryType,
    ApplicationHealthStatusType,
    ApplicationProgressStatusType,
    BootModeType,
    ChangeServerLifeCycleStateSourceServerLifecycleStateType,
    DataReplicationErrorStringType,
    DataReplicationInitiationStepNameType,
    DataReplicationInitiationStepStatusType,
    DataReplicationStateType,
    ExportStatusType,
    FirstBootType,
    ImportErrorTypeType,
    ImportStatusType,
    InitiatedByType,
    JobLogEventType,
    JobStatusType,
    JobTypeType,
    LaunchDispositionType,
    LaunchStatusType,
    LifeCycleStateType,
    PostLaunchActionExecutionStatusType,
    PostLaunchActionsDeploymentTypeType,
    ReplicationConfigurationDataPlaneRoutingType,
    ReplicationConfigurationDefaultLargeStagingDiskTypeType,
    ReplicationConfigurationEbsEncryptionType,
    ReplicationConfigurationReplicatedDiskStagingDiskTypeType,
    ReplicationTypeType,
    SsmDocumentTypeType,
    TargetInstanceTypeRightSizingMethodType,
    VolumeTypeType,
    WaveHealthStatusType,
    WaveProgressStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "ApplicationAggregatedStatusTypeDef",
    "ApplicationResponseTypeDef",
    "ApplicationTypeDef",
    "ArchiveApplicationRequestRequestTypeDef",
    "ArchiveWaveRequestRequestTypeDef",
    "AssociateApplicationsRequestRequestTypeDef",
    "AssociateSourceServersRequestRequestTypeDef",
    "CPUTypeDef",
    "ChangeServerLifeCycleStateRequestRequestTypeDef",
    "ChangeServerLifeCycleStateSourceServerLifecycleTypeDef",
    "ConnectorResponseTypeDef",
    "ConnectorSsmCommandConfigTypeDef",
    "ConnectorTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateConnectorRequestRequestTypeDef",
    "CreateLaunchConfigurationTemplateRequestRequestTypeDef",
    "CreateReplicationConfigurationTemplateRequestRequestTypeDef",
    "CreateWaveRequestRequestTypeDef",
    "DataReplicationErrorTypeDef",
    "DataReplicationInfoReplicatedDiskTypeDef",
    "DataReplicationInfoTypeDef",
    "DataReplicationInitiationStepTypeDef",
    "DataReplicationInitiationTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteConnectorRequestRequestTypeDef",
    "DeleteJobRequestRequestTypeDef",
    "DeleteLaunchConfigurationTemplateRequestRequestTypeDef",
    "DeleteReplicationConfigurationTemplateRequestRequestTypeDef",
    "DeleteSourceServerRequestRequestTypeDef",
    "DeleteVcenterClientRequestRequestTypeDef",
    "DeleteWaveRequestRequestTypeDef",
    "DescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef",
    "DescribeJobLogItemsRequestRequestTypeDef",
    "DescribeJobLogItemsResponseTypeDef",
    "DescribeJobsRequestDescribeJobsPaginateTypeDef",
    "DescribeJobsRequestFiltersTypeDef",
    "DescribeJobsRequestRequestTypeDef",
    "DescribeJobsResponseTypeDef",
    "DescribeLaunchConfigurationTemplatesRequestDescribeLaunchConfigurationTemplatesPaginateTypeDef",
    "DescribeLaunchConfigurationTemplatesRequestRequestTypeDef",
    "DescribeLaunchConfigurationTemplatesResponseTypeDef",
    "DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef",
    "DescribeReplicationConfigurationTemplatesRequestRequestTypeDef",
    "DescribeReplicationConfigurationTemplatesResponseTypeDef",
    "DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef",
    "DescribeSourceServersRequestFiltersTypeDef",
    "DescribeSourceServersRequestRequestTypeDef",
    "DescribeSourceServersResponseTypeDef",
    "DescribeVcenterClientsRequestDescribeVcenterClientsPaginateTypeDef",
    "DescribeVcenterClientsRequestRequestTypeDef",
    "DescribeVcenterClientsResponseTypeDef",
    "DisassociateApplicationsRequestRequestTypeDef",
    "DisassociateSourceServersRequestRequestTypeDef",
    "DisconnectFromServiceRequestRequestTypeDef",
    "DiskTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExportErrorDataTypeDef",
    "ExportTaskErrorTypeDef",
    "ExportTaskSummaryTypeDef",
    "ExportTaskTypeDef",
    "FinalizeCutoverRequestRequestTypeDef",
    "GetLaunchConfigurationRequestRequestTypeDef",
    "GetReplicationConfigurationRequestRequestTypeDef",
    "IdentificationHintsTypeDef",
    "ImportErrorDataTypeDef",
    "ImportTaskErrorTypeDef",
    "ImportTaskSummaryApplicationsTypeDef",
    "ImportTaskSummaryServersTypeDef",
    "ImportTaskSummaryTypeDef",
    "ImportTaskSummaryWavesTypeDef",
    "ImportTaskTypeDef",
    "JobLogEventDataTypeDef",
    "JobLogTypeDef",
    "JobPostLaunchActionsLaunchStatusTypeDef",
    "JobTypeDef",
    "LaunchConfigurationTemplateResponseTypeDef",
    "LaunchConfigurationTemplateTypeDef",
    "LaunchConfigurationTypeDef",
    "LaunchTemplateDiskConfTypeDef",
    "LaunchedInstanceTypeDef",
    "LicensingTypeDef",
    "LifeCycleLastCutoverFinalizedTypeDef",
    "LifeCycleLastCutoverInitiatedTypeDef",
    "LifeCycleLastCutoverRevertedTypeDef",
    "LifeCycleLastCutoverTypeDef",
    "LifeCycleLastTestFinalizedTypeDef",
    "LifeCycleLastTestInitiatedTypeDef",
    "LifeCycleLastTestRevertedTypeDef",
    "LifeCycleLastTestTypeDef",
    "LifeCycleTypeDef",
    "ListApplicationsRequestFiltersTypeDef",
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListConnectorsRequestFiltersTypeDef",
    "ListConnectorsRequestListConnectorsPaginateTypeDef",
    "ListConnectorsRequestRequestTypeDef",
    "ListConnectorsResponseTypeDef",
    "ListExportErrorsRequestListExportErrorsPaginateTypeDef",
    "ListExportErrorsRequestRequestTypeDef",
    "ListExportErrorsResponseTypeDef",
    "ListExportsRequestFiltersTypeDef",
    "ListExportsRequestListExportsPaginateTypeDef",
    "ListExportsRequestRequestTypeDef",
    "ListExportsResponseTypeDef",
    "ListImportErrorsRequestListImportErrorsPaginateTypeDef",
    "ListImportErrorsRequestRequestTypeDef",
    "ListImportErrorsResponseTypeDef",
    "ListImportsRequestFiltersTypeDef",
    "ListImportsRequestListImportsPaginateTypeDef",
    "ListImportsRequestRequestTypeDef",
    "ListImportsResponseTypeDef",
    "ListManagedAccountsRequestListManagedAccountsPaginateTypeDef",
    "ListManagedAccountsRequestRequestTypeDef",
    "ListManagedAccountsResponseTypeDef",
    "ListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef",
    "ListSourceServerActionsRequestRequestTypeDef",
    "ListSourceServerActionsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTemplateActionsRequestListTemplateActionsPaginateTypeDef",
    "ListTemplateActionsRequestRequestTypeDef",
    "ListTemplateActionsResponseTypeDef",
    "ListWavesRequestFiltersTypeDef",
    "ListWavesRequestListWavesPaginateTypeDef",
    "ListWavesRequestRequestTypeDef",
    "ListWavesResponseTypeDef",
    "ManagedAccountTypeDef",
    "MarkAsArchivedRequestRequestTypeDef",
    "NetworkInterfaceTypeDef",
    "OSTypeDef",
    "PaginatorConfigTypeDef",
    "ParticipatingServerTypeDef",
    "PauseReplicationRequestRequestTypeDef",
    "PostLaunchActionsOutputTypeDef",
    "PostLaunchActionsStatusTypeDef",
    "PostLaunchActionsTypeDef",
    "PutSourceServerActionRequestRequestTypeDef",
    "PutTemplateActionRequestRequestTypeDef",
    "RemoveSourceServerActionRequestRequestTypeDef",
    "RemoveTemplateActionRequestRequestTypeDef",
    "ReplicationConfigurationReplicatedDiskTypeDef",
    "ReplicationConfigurationTemplateResponseTypeDef",
    "ReplicationConfigurationTemplateTypeDef",
    "ReplicationConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "ResumeReplicationRequestRequestTypeDef",
    "RetryDataReplicationRequestRequestTypeDef",
    "S3BucketSourceTypeDef",
    "SourcePropertiesTypeDef",
    "SourceServerActionDocumentResponseTypeDef",
    "SourceServerActionDocumentTypeDef",
    "SourceServerActionsRequestFiltersTypeDef",
    "SourceServerConnectorActionTypeDef",
    "SourceServerResponseTypeDef",
    "SourceServerTypeDef",
    "SsmDocumentOutputTypeDef",
    "SsmDocumentTypeDef",
    "SsmDocumentUnionTypeDef",
    "SsmExternalParameterTypeDef",
    "SsmParameterStoreParameterTypeDef",
    "StartCutoverRequestRequestTypeDef",
    "StartCutoverResponseTypeDef",
    "StartExportRequestRequestTypeDef",
    "StartExportResponseTypeDef",
    "StartImportRequestRequestTypeDef",
    "StartImportResponseTypeDef",
    "StartReplicationRequestRequestTypeDef",
    "StartTestRequestRequestTypeDef",
    "StartTestResponseTypeDef",
    "StopReplicationRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TemplateActionDocumentResponseTypeDef",
    "TemplateActionDocumentTypeDef",
    "TemplateActionsRequestFiltersTypeDef",
    "TerminateTargetInstancesRequestRequestTypeDef",
    "TerminateTargetInstancesResponseTypeDef",
    "UnarchiveApplicationRequestRequestTypeDef",
    "UnarchiveWaveRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateConnectorRequestRequestTypeDef",
    "UpdateLaunchConfigurationRequestRequestTypeDef",
    "UpdateLaunchConfigurationTemplateRequestRequestTypeDef",
    "UpdateReplicationConfigurationRequestRequestTypeDef",
    "UpdateReplicationConfigurationTemplateRequestRequestTypeDef",
    "UpdateSourceServerReplicationTypeRequestRequestTypeDef",
    "UpdateSourceServerRequestRequestTypeDef",
    "UpdateWaveRequestRequestTypeDef",
    "VcenterClientTypeDef",
    "WaveAggregatedStatusTypeDef",
    "WaveResponseTypeDef",
    "WaveTypeDef",
)

class ApplicationAggregatedStatusTypeDef(TypedDict):
    healthStatus: NotRequired[ApplicationHealthStatusType]
    lastUpdateDateTime: NotRequired[str]
    progressStatus: NotRequired[ApplicationProgressStatusType]
    totalSourceServers: NotRequired[int]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ArchiveApplicationRequestRequestTypeDef(TypedDict):
    applicationID: str
    accountID: NotRequired[str]

class ArchiveWaveRequestRequestTypeDef(TypedDict):
    waveID: str
    accountID: NotRequired[str]

class AssociateApplicationsRequestRequestTypeDef(TypedDict):
    applicationIDs: Sequence[str]
    waveID: str
    accountID: NotRequired[str]

class AssociateSourceServersRequestRequestTypeDef(TypedDict):
    applicationID: str
    sourceServerIDs: Sequence[str]
    accountID: NotRequired[str]

class CPUTypeDef(TypedDict):
    cores: NotRequired[int]
    modelName: NotRequired[str]

class ChangeServerLifeCycleStateSourceServerLifecycleTypeDef(TypedDict):
    state: ChangeServerLifeCycleStateSourceServerLifecycleStateType

class ConnectorSsmCommandConfigTypeDef(TypedDict):
    cloudWatchOutputEnabled: bool
    s3OutputEnabled: bool
    cloudWatchLogGroupName: NotRequired[str]
    outputS3BucketName: NotRequired[str]

class CreateApplicationRequestRequestTypeDef(TypedDict):
    name: str
    accountID: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class LaunchTemplateDiskConfTypeDef(TypedDict):
    iops: NotRequired[int]
    throughput: NotRequired[int]
    volumeType: NotRequired[VolumeTypeType]

class LicensingTypeDef(TypedDict):
    osByol: NotRequired[bool]

class CreateReplicationConfigurationTemplateRequestRequestTypeDef(TypedDict):
    associateDefaultSecurityGroup: bool
    bandwidthThrottling: int
    createPublicIP: bool
    dataPlaneRouting: ReplicationConfigurationDataPlaneRoutingType
    defaultLargeStagingDiskType: ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ebsEncryption: ReplicationConfigurationEbsEncryptionType
    replicationServerInstanceType: str
    replicationServersSecurityGroupsIDs: Sequence[str]
    stagingAreaSubnetId: str
    stagingAreaTags: Mapping[str, str]
    useDedicatedReplicationServer: bool
    ebsEncryptionKeyArn: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    useFipsEndpoint: NotRequired[bool]

class CreateWaveRequestRequestTypeDef(TypedDict):
    name: str
    accountID: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class DataReplicationErrorTypeDef(TypedDict):
    error: NotRequired[DataReplicationErrorStringType]
    rawError: NotRequired[str]

class DataReplicationInfoReplicatedDiskTypeDef(TypedDict):
    backloggedStorageBytes: NotRequired[int]
    deviceName: NotRequired[str]
    replicatedStorageBytes: NotRequired[int]
    rescannedStorageBytes: NotRequired[int]
    totalStorageBytes: NotRequired[int]

class DataReplicationInitiationStepTypeDef(TypedDict):
    name: NotRequired[DataReplicationInitiationStepNameType]
    status: NotRequired[DataReplicationInitiationStepStatusType]

class DeleteApplicationRequestRequestTypeDef(TypedDict):
    applicationID: str
    accountID: NotRequired[str]

class DeleteConnectorRequestRequestTypeDef(TypedDict):
    connectorID: str

class DeleteJobRequestRequestTypeDef(TypedDict):
    jobID: str
    accountID: NotRequired[str]

class DeleteLaunchConfigurationTemplateRequestRequestTypeDef(TypedDict):
    launchConfigurationTemplateID: str

class DeleteReplicationConfigurationTemplateRequestRequestTypeDef(TypedDict):
    replicationConfigurationTemplateID: str

class DeleteSourceServerRequestRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]

class DeleteVcenterClientRequestRequestTypeDef(TypedDict):
    vcenterClientID: str

class DeleteWaveRequestRequestTypeDef(TypedDict):
    waveID: str
    accountID: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeJobLogItemsRequestRequestTypeDef(TypedDict):
    jobID: str
    accountID: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class DescribeJobsRequestFiltersTypeDef(TypedDict):
    fromDate: NotRequired[str]
    jobIDs: NotRequired[Sequence[str]]
    toDate: NotRequired[str]

class DescribeLaunchConfigurationTemplatesRequestRequestTypeDef(TypedDict):
    launchConfigurationTemplateIDs: NotRequired[Sequence[str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class DescribeReplicationConfigurationTemplatesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    replicationConfigurationTemplateIDs: NotRequired[Sequence[str]]

class ReplicationConfigurationTemplateTypeDef(TypedDict):
    replicationConfigurationTemplateID: str
    arn: NotRequired[str]
    associateDefaultSecurityGroup: NotRequired[bool]
    bandwidthThrottling: NotRequired[int]
    createPublicIP: NotRequired[bool]
    dataPlaneRouting: NotRequired[ReplicationConfigurationDataPlaneRoutingType]
    defaultLargeStagingDiskType: NotRequired[
        ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ]
    ebsEncryption: NotRequired[ReplicationConfigurationEbsEncryptionType]
    ebsEncryptionKeyArn: NotRequired[str]
    replicationServerInstanceType: NotRequired[str]
    replicationServersSecurityGroupsIDs: NotRequired[List[str]]
    stagingAreaSubnetId: NotRequired[str]
    stagingAreaTags: NotRequired[Dict[str, str]]
    tags: NotRequired[Dict[str, str]]
    useDedicatedReplicationServer: NotRequired[bool]
    useFipsEndpoint: NotRequired[bool]

class DescribeSourceServersRequestFiltersTypeDef(TypedDict):
    applicationIDs: NotRequired[Sequence[str]]
    isArchived: NotRequired[bool]
    lifeCycleStates: NotRequired[Sequence[LifeCycleStateType]]
    replicationTypes: NotRequired[Sequence[ReplicationTypeType]]
    sourceServerIDs: NotRequired[Sequence[str]]

class DescribeVcenterClientsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class VcenterClientTypeDef(TypedDict):
    arn: NotRequired[str]
    datacenterName: NotRequired[str]
    hostname: NotRequired[str]
    lastSeenDatetime: NotRequired[str]
    sourceServerTags: NotRequired[Dict[str, str]]
    tags: NotRequired[Dict[str, str]]
    vcenterClientID: NotRequired[str]
    vcenterUUID: NotRequired[str]

class DisassociateApplicationsRequestRequestTypeDef(TypedDict):
    applicationIDs: Sequence[str]
    waveID: str
    accountID: NotRequired[str]

class DisassociateSourceServersRequestRequestTypeDef(TypedDict):
    applicationID: str
    sourceServerIDs: Sequence[str]
    accountID: NotRequired[str]

class DisconnectFromServiceRequestRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]

DiskTypeDef = TypedDict(
    "DiskTypeDef",
    {
        "bytes": NotRequired[int],
        "deviceName": NotRequired[str],
    },
)

class ExportErrorDataTypeDef(TypedDict):
    rawError: NotRequired[str]

class ExportTaskSummaryTypeDef(TypedDict):
    applicationsCount: NotRequired[int]
    serversCount: NotRequired[int]
    wavesCount: NotRequired[int]

class FinalizeCutoverRequestRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]

class GetLaunchConfigurationRequestRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]

class GetReplicationConfigurationRequestRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]

class IdentificationHintsTypeDef(TypedDict):
    awsInstanceID: NotRequired[str]
    fqdn: NotRequired[str]
    hostname: NotRequired[str]
    vmPath: NotRequired[str]
    vmWareUuid: NotRequired[str]

class ImportErrorDataTypeDef(TypedDict):
    accountID: NotRequired[str]
    applicationID: NotRequired[str]
    ec2LaunchTemplateID: NotRequired[str]
    rawError: NotRequired[str]
    rowNumber: NotRequired[int]
    sourceServerID: NotRequired[str]
    waveID: NotRequired[str]

class ImportTaskSummaryApplicationsTypeDef(TypedDict):
    createdCount: NotRequired[int]
    modifiedCount: NotRequired[int]

class ImportTaskSummaryServersTypeDef(TypedDict):
    createdCount: NotRequired[int]
    modifiedCount: NotRequired[int]

class ImportTaskSummaryWavesTypeDef(TypedDict):
    createdCount: NotRequired[int]
    modifiedCount: NotRequired[int]

class S3BucketSourceTypeDef(TypedDict):
    s3Bucket: str
    s3Key: str
    s3BucketOwner: NotRequired[str]

class JobLogEventDataTypeDef(TypedDict):
    conversionServerID: NotRequired[str]
    rawError: NotRequired[str]
    sourceServerID: NotRequired[str]
    targetInstanceID: NotRequired[str]

class LaunchedInstanceTypeDef(TypedDict):
    ec2InstanceID: NotRequired[str]
    firstBoot: NotRequired[FirstBootType]
    jobID: NotRequired[str]

class LifeCycleLastCutoverFinalizedTypeDef(TypedDict):
    apiCallDateTime: NotRequired[str]

class LifeCycleLastCutoverInitiatedTypeDef(TypedDict):
    apiCallDateTime: NotRequired[str]
    jobID: NotRequired[str]

class LifeCycleLastCutoverRevertedTypeDef(TypedDict):
    apiCallDateTime: NotRequired[str]

class LifeCycleLastTestFinalizedTypeDef(TypedDict):
    apiCallDateTime: NotRequired[str]

class LifeCycleLastTestInitiatedTypeDef(TypedDict):
    apiCallDateTime: NotRequired[str]
    jobID: NotRequired[str]

class LifeCycleLastTestRevertedTypeDef(TypedDict):
    apiCallDateTime: NotRequired[str]

class ListApplicationsRequestFiltersTypeDef(TypedDict):
    applicationIDs: NotRequired[Sequence[str]]
    isArchived: NotRequired[bool]
    waveIDs: NotRequired[Sequence[str]]

class ListConnectorsRequestFiltersTypeDef(TypedDict):
    connectorIDs: NotRequired[Sequence[str]]

class ListExportErrorsRequestRequestTypeDef(TypedDict):
    exportID: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListExportsRequestFiltersTypeDef(TypedDict):
    exportIDs: NotRequired[Sequence[str]]

class ListImportErrorsRequestRequestTypeDef(TypedDict):
    importID: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListImportsRequestFiltersTypeDef(TypedDict):
    importIDs: NotRequired[Sequence[str]]

class ListManagedAccountsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ManagedAccountTypeDef(TypedDict):
    accountId: NotRequired[str]

class SourceServerActionsRequestFiltersTypeDef(TypedDict):
    actionIDs: NotRequired[Sequence[str]]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class TemplateActionsRequestFiltersTypeDef(TypedDict):
    actionIDs: NotRequired[Sequence[str]]

class ListWavesRequestFiltersTypeDef(TypedDict):
    isArchived: NotRequired[bool]
    waveIDs: NotRequired[Sequence[str]]

class MarkAsArchivedRequestRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]

class NetworkInterfaceTypeDef(TypedDict):
    ips: NotRequired[List[str]]
    isPrimary: NotRequired[bool]
    macAddress: NotRequired[str]

class OSTypeDef(TypedDict):
    fullString: NotRequired[str]

class PauseReplicationRequestRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]

class SsmExternalParameterTypeDef(TypedDict):
    dynamicPath: NotRequired[str]

class SsmParameterStoreParameterTypeDef(TypedDict):
    parameterName: str
    parameterType: Literal["STRING"]

class RemoveSourceServerActionRequestRequestTypeDef(TypedDict):
    actionID: str
    sourceServerID: str
    accountID: NotRequired[str]

class RemoveTemplateActionRequestRequestTypeDef(TypedDict):
    actionID: str
    launchConfigurationTemplateID: str

class ReplicationConfigurationReplicatedDiskTypeDef(TypedDict):
    deviceName: NotRequired[str]
    iops: NotRequired[int]
    isBootDisk: NotRequired[bool]
    stagingDiskType: NotRequired[ReplicationConfigurationReplicatedDiskStagingDiskTypeType]
    throughput: NotRequired[int]

class ResumeReplicationRequestRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]

class RetryDataReplicationRequestRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]

class SourceServerConnectorActionTypeDef(TypedDict):
    connectorArn: NotRequired[str]
    credentialsSecretArn: NotRequired[str]

class StartCutoverRequestRequestTypeDef(TypedDict):
    sourceServerIDs: Sequence[str]
    accountID: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class StartExportRequestRequestTypeDef(TypedDict):
    s3Bucket: str
    s3Key: str
    s3BucketOwner: NotRequired[str]

class StartReplicationRequestRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]

class StartTestRequestRequestTypeDef(TypedDict):
    sourceServerIDs: Sequence[str]
    accountID: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class StopReplicationRequestRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class TerminateTargetInstancesRequestRequestTypeDef(TypedDict):
    sourceServerIDs: Sequence[str]
    accountID: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class UnarchiveApplicationRequestRequestTypeDef(TypedDict):
    applicationID: str
    accountID: NotRequired[str]

class UnarchiveWaveRequestRequestTypeDef(TypedDict):
    waveID: str
    accountID: NotRequired[str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateApplicationRequestRequestTypeDef(TypedDict):
    applicationID: str
    accountID: NotRequired[str]
    description: NotRequired[str]
    name: NotRequired[str]

class UpdateReplicationConfigurationTemplateRequestRequestTypeDef(TypedDict):
    replicationConfigurationTemplateID: str
    arn: NotRequired[str]
    associateDefaultSecurityGroup: NotRequired[bool]
    bandwidthThrottling: NotRequired[int]
    createPublicIP: NotRequired[bool]
    dataPlaneRouting: NotRequired[ReplicationConfigurationDataPlaneRoutingType]
    defaultLargeStagingDiskType: NotRequired[
        ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ]
    ebsEncryption: NotRequired[ReplicationConfigurationEbsEncryptionType]
    ebsEncryptionKeyArn: NotRequired[str]
    replicationServerInstanceType: NotRequired[str]
    replicationServersSecurityGroupsIDs: NotRequired[Sequence[str]]
    stagingAreaSubnetId: NotRequired[str]
    stagingAreaTags: NotRequired[Mapping[str, str]]
    useDedicatedReplicationServer: NotRequired[bool]
    useFipsEndpoint: NotRequired[bool]

class UpdateSourceServerReplicationTypeRequestRequestTypeDef(TypedDict):
    replicationType: ReplicationTypeType
    sourceServerID: str
    accountID: NotRequired[str]

class UpdateWaveRequestRequestTypeDef(TypedDict):
    waveID: str
    accountID: NotRequired[str]
    description: NotRequired[str]
    name: NotRequired[str]

class WaveAggregatedStatusTypeDef(TypedDict):
    healthStatus: NotRequired[WaveHealthStatusType]
    lastUpdateDateTime: NotRequired[str]
    progressStatus: NotRequired[WaveProgressStatusType]
    replicationStartedDateTime: NotRequired[str]
    totalApplications: NotRequired[int]

class ApplicationTypeDef(TypedDict):
    applicationAggregatedStatus: NotRequired[ApplicationAggregatedStatusTypeDef]
    applicationID: NotRequired[str]
    arn: NotRequired[str]
    creationDateTime: NotRequired[str]
    description: NotRequired[str]
    isArchived: NotRequired[bool]
    lastModifiedDateTime: NotRequired[str]
    name: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    waveID: NotRequired[str]

class ApplicationResponseTypeDef(TypedDict):
    applicationAggregatedStatus: ApplicationAggregatedStatusTypeDef
    applicationID: str
    arn: str
    creationDateTime: str
    description: str
    isArchived: bool
    lastModifiedDateTime: str
    name: str
    tags: Dict[str, str]
    waveID: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ReplicationConfigurationTemplateResponseTypeDef(TypedDict):
    arn: str
    associateDefaultSecurityGroup: bool
    bandwidthThrottling: int
    createPublicIP: bool
    dataPlaneRouting: ReplicationConfigurationDataPlaneRoutingType
    defaultLargeStagingDiskType: ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ebsEncryption: ReplicationConfigurationEbsEncryptionType
    ebsEncryptionKeyArn: str
    replicationConfigurationTemplateID: str
    replicationServerInstanceType: str
    replicationServersSecurityGroupsIDs: List[str]
    stagingAreaSubnetId: str
    stagingAreaTags: Dict[str, str]
    tags: Dict[str, str]
    useDedicatedReplicationServer: bool
    useFipsEndpoint: bool
    ResponseMetadata: ResponseMetadataTypeDef

class ChangeServerLifeCycleStateRequestRequestTypeDef(TypedDict):
    lifeCycle: ChangeServerLifeCycleStateSourceServerLifecycleTypeDef
    sourceServerID: str
    accountID: NotRequired[str]

class ConnectorResponseTypeDef(TypedDict):
    arn: str
    connectorID: str
    name: str
    ssmCommandConfig: ConnectorSsmCommandConfigTypeDef
    ssmInstanceID: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ConnectorTypeDef(TypedDict):
    arn: NotRequired[str]
    connectorID: NotRequired[str]
    name: NotRequired[str]
    ssmCommandConfig: NotRequired[ConnectorSsmCommandConfigTypeDef]
    ssmInstanceID: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

class CreateConnectorRequestRequestTypeDef(TypedDict):
    name: str
    ssmInstanceID: str
    ssmCommandConfig: NotRequired[ConnectorSsmCommandConfigTypeDef]
    tags: NotRequired[Mapping[str, str]]

class UpdateConnectorRequestRequestTypeDef(TypedDict):
    connectorID: str
    name: NotRequired[str]
    ssmCommandConfig: NotRequired[ConnectorSsmCommandConfigTypeDef]

class DataReplicationInitiationTypeDef(TypedDict):
    nextAttemptDateTime: NotRequired[str]
    startDateTime: NotRequired[str]
    steps: NotRequired[List[DataReplicationInitiationStepTypeDef]]

class DescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef(TypedDict):
    jobID: str
    accountID: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeLaunchConfigurationTemplatesRequestDescribeLaunchConfigurationTemplatesPaginateTypeDef(
    TypedDict
):
    launchConfigurationTemplateIDs: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef(
    TypedDict
):
    replicationConfigurationTemplateIDs: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeVcenterClientsRequestDescribeVcenterClientsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListExportErrorsRequestListExportErrorsPaginateTypeDef(TypedDict):
    exportID: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListImportErrorsRequestListImportErrorsPaginateTypeDef(TypedDict):
    importID: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListManagedAccountsRequestListManagedAccountsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeJobsRequestDescribeJobsPaginateTypeDef(TypedDict):
    accountID: NotRequired[str]
    filters: NotRequired[DescribeJobsRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeJobsRequestRequestTypeDef(TypedDict):
    accountID: NotRequired[str]
    filters: NotRequired[DescribeJobsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class DescribeReplicationConfigurationTemplatesResponseTypeDef(TypedDict):
    items: List[ReplicationConfigurationTemplateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef(TypedDict):
    accountID: NotRequired[str]
    filters: NotRequired[DescribeSourceServersRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeSourceServersRequestRequestTypeDef(TypedDict):
    accountID: NotRequired[str]
    filters: NotRequired[DescribeSourceServersRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class DescribeVcenterClientsResponseTypeDef(TypedDict):
    items: List[VcenterClientTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ExportTaskErrorTypeDef(TypedDict):
    errorData: NotRequired[ExportErrorDataTypeDef]
    errorDateTime: NotRequired[str]

class ExportTaskTypeDef(TypedDict):
    creationDateTime: NotRequired[str]
    endDateTime: NotRequired[str]
    exportID: NotRequired[str]
    progressPercentage: NotRequired[float]
    s3Bucket: NotRequired[str]
    s3BucketOwner: NotRequired[str]
    s3Key: NotRequired[str]
    status: NotRequired[ExportStatusType]
    summary: NotRequired[ExportTaskSummaryTypeDef]

class ImportTaskErrorTypeDef(TypedDict):
    errorData: NotRequired[ImportErrorDataTypeDef]
    errorDateTime: NotRequired[str]
    errorType: NotRequired[ImportErrorTypeType]

class ImportTaskSummaryTypeDef(TypedDict):
    applications: NotRequired[ImportTaskSummaryApplicationsTypeDef]
    servers: NotRequired[ImportTaskSummaryServersTypeDef]
    waves: NotRequired[ImportTaskSummaryWavesTypeDef]

class StartImportRequestRequestTypeDef(TypedDict):
    s3BucketSource: S3BucketSourceTypeDef
    clientToken: NotRequired[str]

class JobLogTypeDef(TypedDict):
    event: NotRequired[JobLogEventType]
    eventData: NotRequired[JobLogEventDataTypeDef]
    logDateTime: NotRequired[str]

class LifeCycleLastCutoverTypeDef(TypedDict):
    finalized: NotRequired[LifeCycleLastCutoverFinalizedTypeDef]
    initiated: NotRequired[LifeCycleLastCutoverInitiatedTypeDef]
    reverted: NotRequired[LifeCycleLastCutoverRevertedTypeDef]

class LifeCycleLastTestTypeDef(TypedDict):
    finalized: NotRequired[LifeCycleLastTestFinalizedTypeDef]
    initiated: NotRequired[LifeCycleLastTestInitiatedTypeDef]
    reverted: NotRequired[LifeCycleLastTestRevertedTypeDef]

class ListApplicationsRequestListApplicationsPaginateTypeDef(TypedDict):
    accountID: NotRequired[str]
    filters: NotRequired[ListApplicationsRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationsRequestRequestTypeDef(TypedDict):
    accountID: NotRequired[str]
    filters: NotRequired[ListApplicationsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListConnectorsRequestListConnectorsPaginateTypeDef(TypedDict):
    filters: NotRequired[ListConnectorsRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConnectorsRequestRequestTypeDef(TypedDict):
    filters: NotRequired[ListConnectorsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListExportsRequestListExportsPaginateTypeDef(TypedDict):
    filters: NotRequired[ListExportsRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListExportsRequestRequestTypeDef(TypedDict):
    filters: NotRequired[ListExportsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListImportsRequestListImportsPaginateTypeDef(TypedDict):
    filters: NotRequired[ListImportsRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListImportsRequestRequestTypeDef(TypedDict):
    filters: NotRequired[ListImportsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListManagedAccountsResponseTypeDef(TypedDict):
    items: List[ManagedAccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]
    filters: NotRequired[SourceServerActionsRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSourceServerActionsRequestRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]
    filters: NotRequired[SourceServerActionsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTemplateActionsRequestListTemplateActionsPaginateTypeDef(TypedDict):
    launchConfigurationTemplateID: str
    filters: NotRequired[TemplateActionsRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTemplateActionsRequestRequestTypeDef(TypedDict):
    launchConfigurationTemplateID: str
    filters: NotRequired[TemplateActionsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListWavesRequestListWavesPaginateTypeDef(TypedDict):
    accountID: NotRequired[str]
    filters: NotRequired[ListWavesRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWavesRequestRequestTypeDef(TypedDict):
    accountID: NotRequired[str]
    filters: NotRequired[ListWavesRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class SourcePropertiesTypeDef(TypedDict):
    cpus: NotRequired[List[CPUTypeDef]]
    disks: NotRequired[List[DiskTypeDef]]
    identificationHints: NotRequired[IdentificationHintsTypeDef]
    lastUpdatedDateTime: NotRequired[str]
    networkInterfaces: NotRequired[List[NetworkInterfaceTypeDef]]
    os: NotRequired[OSTypeDef]
    ramBytes: NotRequired[int]
    recommendedInstanceType: NotRequired[str]

class PutSourceServerActionRequestRequestTypeDef(TypedDict):
    actionID: str
    actionName: str
    documentIdentifier: str
    order: int
    sourceServerID: str
    accountID: NotRequired[str]
    active: NotRequired[bool]
    category: NotRequired[ActionCategoryType]
    description: NotRequired[str]
    documentVersion: NotRequired[str]
    externalParameters: NotRequired[Mapping[str, SsmExternalParameterTypeDef]]
    mustSucceedForCutover: NotRequired[bool]
    parameters: NotRequired[Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]]]
    timeoutSeconds: NotRequired[int]

class PutTemplateActionRequestRequestTypeDef(TypedDict):
    actionID: str
    actionName: str
    documentIdentifier: str
    launchConfigurationTemplateID: str
    order: int
    active: NotRequired[bool]
    category: NotRequired[ActionCategoryType]
    description: NotRequired[str]
    documentVersion: NotRequired[str]
    externalParameters: NotRequired[Mapping[str, SsmExternalParameterTypeDef]]
    mustSucceedForCutover: NotRequired[bool]
    operatingSystem: NotRequired[str]
    parameters: NotRequired[Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]]]
    timeoutSeconds: NotRequired[int]

class SourceServerActionDocumentResponseTypeDef(TypedDict):
    actionID: str
    actionName: str
    active: bool
    category: ActionCategoryType
    description: str
    documentIdentifier: str
    documentVersion: str
    externalParameters: Dict[str, SsmExternalParameterTypeDef]
    mustSucceedForCutover: bool
    order: int
    parameters: Dict[str, List[SsmParameterStoreParameterTypeDef]]
    timeoutSeconds: int
    ResponseMetadata: ResponseMetadataTypeDef

class SourceServerActionDocumentTypeDef(TypedDict):
    actionID: NotRequired[str]
    actionName: NotRequired[str]
    active: NotRequired[bool]
    category: NotRequired[ActionCategoryType]
    description: NotRequired[str]
    documentIdentifier: NotRequired[str]
    documentVersion: NotRequired[str]
    externalParameters: NotRequired[Dict[str, SsmExternalParameterTypeDef]]
    mustSucceedForCutover: NotRequired[bool]
    order: NotRequired[int]
    parameters: NotRequired[Dict[str, List[SsmParameterStoreParameterTypeDef]]]
    timeoutSeconds: NotRequired[int]

class SsmDocumentOutputTypeDef(TypedDict):
    actionName: str
    ssmDocumentName: str
    externalParameters: NotRequired[Dict[str, SsmExternalParameterTypeDef]]
    mustSucceedForCutover: NotRequired[bool]
    parameters: NotRequired[Dict[str, List[SsmParameterStoreParameterTypeDef]]]
    timeoutSeconds: NotRequired[int]

class SsmDocumentTypeDef(TypedDict):
    actionName: str
    ssmDocumentName: str
    externalParameters: NotRequired[Mapping[str, SsmExternalParameterTypeDef]]
    mustSucceedForCutover: NotRequired[bool]
    parameters: NotRequired[Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]]]
    timeoutSeconds: NotRequired[int]

class TemplateActionDocumentResponseTypeDef(TypedDict):
    actionID: str
    actionName: str
    active: bool
    category: ActionCategoryType
    description: str
    documentIdentifier: str
    documentVersion: str
    externalParameters: Dict[str, SsmExternalParameterTypeDef]
    mustSucceedForCutover: bool
    operatingSystem: str
    order: int
    parameters: Dict[str, List[SsmParameterStoreParameterTypeDef]]
    timeoutSeconds: int
    ResponseMetadata: ResponseMetadataTypeDef

class TemplateActionDocumentTypeDef(TypedDict):
    actionID: NotRequired[str]
    actionName: NotRequired[str]
    active: NotRequired[bool]
    category: NotRequired[ActionCategoryType]
    description: NotRequired[str]
    documentIdentifier: NotRequired[str]
    documentVersion: NotRequired[str]
    externalParameters: NotRequired[Dict[str, SsmExternalParameterTypeDef]]
    mustSucceedForCutover: NotRequired[bool]
    operatingSystem: NotRequired[str]
    order: NotRequired[int]
    parameters: NotRequired[Dict[str, List[SsmParameterStoreParameterTypeDef]]]
    timeoutSeconds: NotRequired[int]

class ReplicationConfigurationTypeDef(TypedDict):
    associateDefaultSecurityGroup: bool
    bandwidthThrottling: int
    createPublicIP: bool
    dataPlaneRouting: ReplicationConfigurationDataPlaneRoutingType
    defaultLargeStagingDiskType: ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ebsEncryption: ReplicationConfigurationEbsEncryptionType
    ebsEncryptionKeyArn: str
    name: str
    replicatedDisks: List[ReplicationConfigurationReplicatedDiskTypeDef]
    replicationServerInstanceType: str
    replicationServersSecurityGroupsIDs: List[str]
    sourceServerID: str
    stagingAreaSubnetId: str
    stagingAreaTags: Dict[str, str]
    useDedicatedReplicationServer: bool
    useFipsEndpoint: bool
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateReplicationConfigurationRequestRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]
    associateDefaultSecurityGroup: NotRequired[bool]
    bandwidthThrottling: NotRequired[int]
    createPublicIP: NotRequired[bool]
    dataPlaneRouting: NotRequired[ReplicationConfigurationDataPlaneRoutingType]
    defaultLargeStagingDiskType: NotRequired[
        ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ]
    ebsEncryption: NotRequired[ReplicationConfigurationEbsEncryptionType]
    ebsEncryptionKeyArn: NotRequired[str]
    name: NotRequired[str]
    replicatedDisks: NotRequired[Sequence[ReplicationConfigurationReplicatedDiskTypeDef]]
    replicationServerInstanceType: NotRequired[str]
    replicationServersSecurityGroupsIDs: NotRequired[Sequence[str]]
    stagingAreaSubnetId: NotRequired[str]
    stagingAreaTags: NotRequired[Mapping[str, str]]
    useDedicatedReplicationServer: NotRequired[bool]
    useFipsEndpoint: NotRequired[bool]

class UpdateSourceServerRequestRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]
    connectorAction: NotRequired[SourceServerConnectorActionTypeDef]

class WaveResponseTypeDef(TypedDict):
    arn: str
    creationDateTime: str
    description: str
    isArchived: bool
    lastModifiedDateTime: str
    name: str
    tags: Dict[str, str]
    waveAggregatedStatus: WaveAggregatedStatusTypeDef
    waveID: str
    ResponseMetadata: ResponseMetadataTypeDef

class WaveTypeDef(TypedDict):
    arn: NotRequired[str]
    creationDateTime: NotRequired[str]
    description: NotRequired[str]
    isArchived: NotRequired[bool]
    lastModifiedDateTime: NotRequired[str]
    name: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    waveAggregatedStatus: NotRequired[WaveAggregatedStatusTypeDef]
    waveID: NotRequired[str]

class ListApplicationsResponseTypeDef(TypedDict):
    items: List[ApplicationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListConnectorsResponseTypeDef(TypedDict):
    items: List[ConnectorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DataReplicationInfoTypeDef(TypedDict):
    dataReplicationError: NotRequired[DataReplicationErrorTypeDef]
    dataReplicationInitiation: NotRequired[DataReplicationInitiationTypeDef]
    dataReplicationState: NotRequired[DataReplicationStateType]
    etaDateTime: NotRequired[str]
    lagDuration: NotRequired[str]
    lastSnapshotDateTime: NotRequired[str]
    replicatedDisks: NotRequired[List[DataReplicationInfoReplicatedDiskTypeDef]]

class ListExportErrorsResponseTypeDef(TypedDict):
    items: List[ExportTaskErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListExportsResponseTypeDef(TypedDict):
    items: List[ExportTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class StartExportResponseTypeDef(TypedDict):
    exportTask: ExportTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListImportErrorsResponseTypeDef(TypedDict):
    items: List[ImportTaskErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ImportTaskTypeDef(TypedDict):
    creationDateTime: NotRequired[str]
    endDateTime: NotRequired[str]
    importID: NotRequired[str]
    progressPercentage: NotRequired[float]
    s3BucketSource: NotRequired[S3BucketSourceTypeDef]
    status: NotRequired[ImportStatusType]
    summary: NotRequired[ImportTaskSummaryTypeDef]

class DescribeJobLogItemsResponseTypeDef(TypedDict):
    items: List[JobLogTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class LifeCycleTypeDef(TypedDict):
    addedToServiceDateTime: NotRequired[str]
    elapsedReplicationDuration: NotRequired[str]
    firstByteDateTime: NotRequired[str]
    lastCutover: NotRequired[LifeCycleLastCutoverTypeDef]
    lastSeenByServiceDateTime: NotRequired[str]
    lastTest: NotRequired[LifeCycleLastTestTypeDef]
    state: NotRequired[LifeCycleStateType]

class ListSourceServerActionsResponseTypeDef(TypedDict):
    items: List[SourceServerActionDocumentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class JobPostLaunchActionsLaunchStatusTypeDef(TypedDict):
    executionID: NotRequired[str]
    executionStatus: NotRequired[PostLaunchActionExecutionStatusType]
    failureReason: NotRequired[str]
    ssmDocument: NotRequired[SsmDocumentOutputTypeDef]
    ssmDocumentType: NotRequired[SsmDocumentTypeType]

class PostLaunchActionsOutputTypeDef(TypedDict):
    cloudWatchLogGroupName: NotRequired[str]
    deployment: NotRequired[PostLaunchActionsDeploymentTypeType]
    s3LogBucket: NotRequired[str]
    s3OutputKeyPrefix: NotRequired[str]
    ssmDocuments: NotRequired[List[SsmDocumentOutputTypeDef]]

SsmDocumentUnionTypeDef = Union[SsmDocumentTypeDef, SsmDocumentOutputTypeDef]

class ListTemplateActionsResponseTypeDef(TypedDict):
    items: List[TemplateActionDocumentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListWavesResponseTypeDef(TypedDict):
    items: List[WaveTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListImportsResponseTypeDef(TypedDict):
    items: List[ImportTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class StartImportResponseTypeDef(TypedDict):
    importTask: ImportTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SourceServerResponseTypeDef(TypedDict):
    applicationID: str
    arn: str
    connectorAction: SourceServerConnectorActionTypeDef
    dataReplicationInfo: DataReplicationInfoTypeDef
    fqdnForActionFramework: str
    isArchived: bool
    launchedInstance: LaunchedInstanceTypeDef
    lifeCycle: LifeCycleTypeDef
    replicationType: ReplicationTypeType
    sourceProperties: SourcePropertiesTypeDef
    sourceServerID: str
    tags: Dict[str, str]
    userProvidedID: str
    vcenterClientID: str
    ResponseMetadata: ResponseMetadataTypeDef

class SourceServerTypeDef(TypedDict):
    applicationID: NotRequired[str]
    arn: NotRequired[str]
    connectorAction: NotRequired[SourceServerConnectorActionTypeDef]
    dataReplicationInfo: NotRequired[DataReplicationInfoTypeDef]
    fqdnForActionFramework: NotRequired[str]
    isArchived: NotRequired[bool]
    launchedInstance: NotRequired[LaunchedInstanceTypeDef]
    lifeCycle: NotRequired[LifeCycleTypeDef]
    replicationType: NotRequired[ReplicationTypeType]
    sourceProperties: NotRequired[SourcePropertiesTypeDef]
    sourceServerID: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    userProvidedID: NotRequired[str]
    vcenterClientID: NotRequired[str]

class PostLaunchActionsStatusTypeDef(TypedDict):
    postLaunchActionsLaunchStatusList: NotRequired[List[JobPostLaunchActionsLaunchStatusTypeDef]]
    ssmAgentDiscoveryDatetime: NotRequired[str]

class LaunchConfigurationTemplateResponseTypeDef(TypedDict):
    arn: str
    associatePublicIpAddress: bool
    bootMode: BootModeType
    copyPrivateIp: bool
    copyTags: bool
    ec2LaunchTemplateID: str
    enableMapAutoTagging: bool
    largeVolumeConf: LaunchTemplateDiskConfTypeDef
    launchConfigurationTemplateID: str
    launchDisposition: LaunchDispositionType
    licensing: LicensingTypeDef
    mapAutoTaggingMpeID: str
    postLaunchActions: PostLaunchActionsOutputTypeDef
    smallVolumeConf: LaunchTemplateDiskConfTypeDef
    smallVolumeMaxSize: int
    tags: Dict[str, str]
    targetInstanceTypeRightSizingMethod: TargetInstanceTypeRightSizingMethodType
    ResponseMetadata: ResponseMetadataTypeDef

class LaunchConfigurationTemplateTypeDef(TypedDict):
    launchConfigurationTemplateID: str
    arn: NotRequired[str]
    associatePublicIpAddress: NotRequired[bool]
    bootMode: NotRequired[BootModeType]
    copyPrivateIp: NotRequired[bool]
    copyTags: NotRequired[bool]
    ec2LaunchTemplateID: NotRequired[str]
    enableMapAutoTagging: NotRequired[bool]
    largeVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    launchDisposition: NotRequired[LaunchDispositionType]
    licensing: NotRequired[LicensingTypeDef]
    mapAutoTaggingMpeID: NotRequired[str]
    postLaunchActions: NotRequired[PostLaunchActionsOutputTypeDef]
    smallVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    smallVolumeMaxSize: NotRequired[int]
    tags: NotRequired[Dict[str, str]]
    targetInstanceTypeRightSizingMethod: NotRequired[TargetInstanceTypeRightSizingMethodType]

class LaunchConfigurationTypeDef(TypedDict):
    bootMode: BootModeType
    copyPrivateIp: bool
    copyTags: bool
    ec2LaunchTemplateID: str
    enableMapAutoTagging: bool
    launchDisposition: LaunchDispositionType
    licensing: LicensingTypeDef
    mapAutoTaggingMpeID: str
    name: str
    postLaunchActions: PostLaunchActionsOutputTypeDef
    sourceServerID: str
    targetInstanceTypeRightSizingMethod: TargetInstanceTypeRightSizingMethodType
    ResponseMetadata: ResponseMetadataTypeDef

class PostLaunchActionsTypeDef(TypedDict):
    cloudWatchLogGroupName: NotRequired[str]
    deployment: NotRequired[PostLaunchActionsDeploymentTypeType]
    s3LogBucket: NotRequired[str]
    s3OutputKeyPrefix: NotRequired[str]
    ssmDocuments: NotRequired[Sequence[SsmDocumentUnionTypeDef]]

class DescribeSourceServersResponseTypeDef(TypedDict):
    items: List[SourceServerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ParticipatingServerTypeDef(TypedDict):
    sourceServerID: str
    launchStatus: NotRequired[LaunchStatusType]
    launchedEc2InstanceID: NotRequired[str]
    postLaunchActionsStatus: NotRequired[PostLaunchActionsStatusTypeDef]

class DescribeLaunchConfigurationTemplatesResponseTypeDef(TypedDict):
    items: List[LaunchConfigurationTemplateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateLaunchConfigurationTemplateRequestRequestTypeDef(TypedDict):
    associatePublicIpAddress: NotRequired[bool]
    bootMode: NotRequired[BootModeType]
    copyPrivateIp: NotRequired[bool]
    copyTags: NotRequired[bool]
    enableMapAutoTagging: NotRequired[bool]
    largeVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    launchDisposition: NotRequired[LaunchDispositionType]
    licensing: NotRequired[LicensingTypeDef]
    mapAutoTaggingMpeID: NotRequired[str]
    postLaunchActions: NotRequired[PostLaunchActionsTypeDef]
    smallVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    smallVolumeMaxSize: NotRequired[int]
    tags: NotRequired[Mapping[str, str]]
    targetInstanceTypeRightSizingMethod: NotRequired[TargetInstanceTypeRightSizingMethodType]

class UpdateLaunchConfigurationRequestRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]
    bootMode: NotRequired[BootModeType]
    copyPrivateIp: NotRequired[bool]
    copyTags: NotRequired[bool]
    enableMapAutoTagging: NotRequired[bool]
    launchDisposition: NotRequired[LaunchDispositionType]
    licensing: NotRequired[LicensingTypeDef]
    mapAutoTaggingMpeID: NotRequired[str]
    name: NotRequired[str]
    postLaunchActions: NotRequired[PostLaunchActionsTypeDef]
    targetInstanceTypeRightSizingMethod: NotRequired[TargetInstanceTypeRightSizingMethodType]

class UpdateLaunchConfigurationTemplateRequestRequestTypeDef(TypedDict):
    launchConfigurationTemplateID: str
    associatePublicIpAddress: NotRequired[bool]
    bootMode: NotRequired[BootModeType]
    copyPrivateIp: NotRequired[bool]
    copyTags: NotRequired[bool]
    enableMapAutoTagging: NotRequired[bool]
    largeVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    launchDisposition: NotRequired[LaunchDispositionType]
    licensing: NotRequired[LicensingTypeDef]
    mapAutoTaggingMpeID: NotRequired[str]
    postLaunchActions: NotRequired[PostLaunchActionsTypeDef]
    smallVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    smallVolumeMaxSize: NotRequired[int]
    targetInstanceTypeRightSizingMethod: NotRequired[TargetInstanceTypeRightSizingMethodType]

JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "jobID": str,
        "arn": NotRequired[str],
        "creationDateTime": NotRequired[str],
        "endDateTime": NotRequired[str],
        "initiatedBy": NotRequired[InitiatedByType],
        "participatingServers": NotRequired[List[ParticipatingServerTypeDef]],
        "status": NotRequired[JobStatusType],
        "tags": NotRequired[Dict[str, str]],
        "type": NotRequired[JobTypeType],
    },
)

class DescribeJobsResponseTypeDef(TypedDict):
    items: List[JobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class StartCutoverResponseTypeDef(TypedDict):
    job: JobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartTestResponseTypeDef(TypedDict):
    job: JobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class TerminateTargetInstancesResponseTypeDef(TypedDict):
    job: JobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
