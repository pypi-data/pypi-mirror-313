"""
Type annotations for datasync service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/type_defs/)

Usage::

    ```python
    from mypy_boto3_datasync.type_defs import CredentialsTypeDef

    data: CredentialsTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AgentStatusType,
    AtimeType,
    AzureAccessTierType,
    DiscoveryJobStatusType,
    DiscoveryResourceTypeType,
    EfsInTransitEncryptionType,
    EndpointTypeType,
    GidType,
    HdfsAuthenticationTypeType,
    HdfsDataTransferProtectionType,
    HdfsRpcProtectionType,
    LocationFilterNameType,
    LogLevelType,
    MtimeType,
    NfsVersionType,
    ObjectStorageServerProtocolType,
    ObjectTagsType,
    ObjectVersionIdsType,
    OperatorType,
    OverwriteModeType,
    PhaseStatusType,
    PosixPermissionsType,
    PreserveDeletedFilesType,
    PreserveDevicesType,
    RecommendationStatusType,
    ReportLevelType,
    ReportOutputTypeType,
    S3StorageClassType,
    ScheduleDisabledByType,
    ScheduleStatusType,
    SmbSecurityDescriptorCopyFlagsType,
    SmbVersionType,
    StorageSystemConnectivityStatusType,
    TaskExecutionStatusType,
    TaskFilterNameType,
    TaskModeType,
    TaskQueueingType,
    TaskStatusType,
    TransferModeType,
    UidType,
    VerifyModeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AddStorageSystemRequestRequestTypeDef",
    "AddStorageSystemResponseTypeDef",
    "AgentListEntryTypeDef",
    "AzureBlobSasConfigurationTypeDef",
    "BlobTypeDef",
    "CancelTaskExecutionRequestRequestTypeDef",
    "CapacityTypeDef",
    "CreateAgentRequestRequestTypeDef",
    "CreateAgentResponseTypeDef",
    "CreateLocationAzureBlobRequestRequestTypeDef",
    "CreateLocationAzureBlobResponseTypeDef",
    "CreateLocationEfsRequestRequestTypeDef",
    "CreateLocationEfsResponseTypeDef",
    "CreateLocationFsxLustreRequestRequestTypeDef",
    "CreateLocationFsxLustreResponseTypeDef",
    "CreateLocationFsxOntapRequestRequestTypeDef",
    "CreateLocationFsxOntapResponseTypeDef",
    "CreateLocationFsxOpenZfsRequestRequestTypeDef",
    "CreateLocationFsxOpenZfsResponseTypeDef",
    "CreateLocationFsxWindowsRequestRequestTypeDef",
    "CreateLocationFsxWindowsResponseTypeDef",
    "CreateLocationHdfsRequestRequestTypeDef",
    "CreateLocationHdfsResponseTypeDef",
    "CreateLocationNfsRequestRequestTypeDef",
    "CreateLocationNfsResponseTypeDef",
    "CreateLocationObjectStorageRequestRequestTypeDef",
    "CreateLocationObjectStorageResponseTypeDef",
    "CreateLocationS3RequestRequestTypeDef",
    "CreateLocationS3ResponseTypeDef",
    "CreateLocationSmbRequestRequestTypeDef",
    "CreateLocationSmbResponseTypeDef",
    "CreateTaskRequestRequestTypeDef",
    "CreateTaskResponseTypeDef",
    "CredentialsTypeDef",
    "DeleteAgentRequestRequestTypeDef",
    "DeleteLocationRequestRequestTypeDef",
    "DeleteTaskRequestRequestTypeDef",
    "DescribeAgentRequestRequestTypeDef",
    "DescribeAgentResponseTypeDef",
    "DescribeDiscoveryJobRequestRequestTypeDef",
    "DescribeDiscoveryJobResponseTypeDef",
    "DescribeLocationAzureBlobRequestRequestTypeDef",
    "DescribeLocationAzureBlobResponseTypeDef",
    "DescribeLocationEfsRequestRequestTypeDef",
    "DescribeLocationEfsResponseTypeDef",
    "DescribeLocationFsxLustreRequestRequestTypeDef",
    "DescribeLocationFsxLustreResponseTypeDef",
    "DescribeLocationFsxOntapRequestRequestTypeDef",
    "DescribeLocationFsxOntapResponseTypeDef",
    "DescribeLocationFsxOpenZfsRequestRequestTypeDef",
    "DescribeLocationFsxOpenZfsResponseTypeDef",
    "DescribeLocationFsxWindowsRequestRequestTypeDef",
    "DescribeLocationFsxWindowsResponseTypeDef",
    "DescribeLocationHdfsRequestRequestTypeDef",
    "DescribeLocationHdfsResponseTypeDef",
    "DescribeLocationNfsRequestRequestTypeDef",
    "DescribeLocationNfsResponseTypeDef",
    "DescribeLocationObjectStorageRequestRequestTypeDef",
    "DescribeLocationObjectStorageResponseTypeDef",
    "DescribeLocationS3RequestRequestTypeDef",
    "DescribeLocationS3ResponseTypeDef",
    "DescribeLocationSmbRequestRequestTypeDef",
    "DescribeLocationSmbResponseTypeDef",
    "DescribeStorageSystemRequestRequestTypeDef",
    "DescribeStorageSystemResourceMetricsRequestDescribeStorageSystemResourceMetricsPaginateTypeDef",
    "DescribeStorageSystemResourceMetricsRequestRequestTypeDef",
    "DescribeStorageSystemResourceMetricsResponseTypeDef",
    "DescribeStorageSystemResourcesRequestRequestTypeDef",
    "DescribeStorageSystemResourcesResponseTypeDef",
    "DescribeStorageSystemResponseTypeDef",
    "DescribeTaskExecutionRequestRequestTypeDef",
    "DescribeTaskExecutionResponseTypeDef",
    "DescribeTaskRequestRequestTypeDef",
    "DescribeTaskResponseTypeDef",
    "DiscoveryJobListEntryTypeDef",
    "DiscoveryServerConfigurationTypeDef",
    "Ec2ConfigOutputTypeDef",
    "Ec2ConfigTypeDef",
    "FilterRuleTypeDef",
    "FsxProtocolNfsTypeDef",
    "FsxProtocolSmbTypeDef",
    "FsxProtocolTypeDef",
    "GenerateRecommendationsRequestRequestTypeDef",
    "HdfsNameNodeTypeDef",
    "IOPSTypeDef",
    "LatencyTypeDef",
    "ListAgentsRequestListAgentsPaginateTypeDef",
    "ListAgentsRequestRequestTypeDef",
    "ListAgentsResponseTypeDef",
    "ListDiscoveryJobsRequestListDiscoveryJobsPaginateTypeDef",
    "ListDiscoveryJobsRequestRequestTypeDef",
    "ListDiscoveryJobsResponseTypeDef",
    "ListLocationsRequestListLocationsPaginateTypeDef",
    "ListLocationsRequestRequestTypeDef",
    "ListLocationsResponseTypeDef",
    "ListStorageSystemsRequestListStorageSystemsPaginateTypeDef",
    "ListStorageSystemsRequestRequestTypeDef",
    "ListStorageSystemsResponseTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTaskExecutionsRequestListTaskExecutionsPaginateTypeDef",
    "ListTaskExecutionsRequestRequestTypeDef",
    "ListTaskExecutionsResponseTypeDef",
    "ListTasksRequestListTasksPaginateTypeDef",
    "ListTasksRequestRequestTypeDef",
    "ListTasksResponseTypeDef",
    "LocationFilterTypeDef",
    "LocationListEntryTypeDef",
    "ManifestConfigTypeDef",
    "MaxP95PerformanceTypeDef",
    "NetAppONTAPClusterTypeDef",
    "NetAppONTAPSVMTypeDef",
    "NetAppONTAPVolumeTypeDef",
    "NfsMountOptionsTypeDef",
    "OnPremConfigOutputTypeDef",
    "OnPremConfigTypeDef",
    "OptionsTypeDef",
    "P95MetricsTypeDef",
    "PaginatorConfigTypeDef",
    "PlatformTypeDef",
    "PrivateLinkConfigTypeDef",
    "QopConfigurationTypeDef",
    "RecommendationTypeDef",
    "RemoveStorageSystemRequestRequestTypeDef",
    "ReportDestinationS3TypeDef",
    "ReportDestinationTypeDef",
    "ReportOverrideTypeDef",
    "ReportOverridesTypeDef",
    "ReportResultTypeDef",
    "ResourceDetailsTypeDef",
    "ResourceMetricsTypeDef",
    "ResponseMetadataTypeDef",
    "S3ConfigTypeDef",
    "S3ManifestConfigTypeDef",
    "SmbMountOptionsTypeDef",
    "SourceManifestConfigTypeDef",
    "StartDiscoveryJobRequestRequestTypeDef",
    "StartDiscoveryJobResponseTypeDef",
    "StartTaskExecutionRequestRequestTypeDef",
    "StartTaskExecutionResponseTypeDef",
    "StopDiscoveryJobRequestRequestTypeDef",
    "StorageSystemListEntryTypeDef",
    "TagListEntryTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TaskExecutionFilesFailedDetailTypeDef",
    "TaskExecutionFilesListedDetailTypeDef",
    "TaskExecutionListEntryTypeDef",
    "TaskExecutionResultDetailTypeDef",
    "TaskFilterTypeDef",
    "TaskListEntryTypeDef",
    "TaskReportConfigTypeDef",
    "TaskScheduleDetailsTypeDef",
    "TaskScheduleTypeDef",
    "ThroughputTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAgentRequestRequestTypeDef",
    "UpdateDiscoveryJobRequestRequestTypeDef",
    "UpdateLocationAzureBlobRequestRequestTypeDef",
    "UpdateLocationHdfsRequestRequestTypeDef",
    "UpdateLocationNfsRequestRequestTypeDef",
    "UpdateLocationObjectStorageRequestRequestTypeDef",
    "UpdateLocationSmbRequestRequestTypeDef",
    "UpdateStorageSystemRequestRequestTypeDef",
    "UpdateTaskExecutionRequestRequestTypeDef",
    "UpdateTaskRequestRequestTypeDef",
)


class CredentialsTypeDef(TypedDict):
    Username: str
    Password: str


class DiscoveryServerConfigurationTypeDef(TypedDict):
    ServerHostname: str
    ServerPort: NotRequired[int]


class TagListEntryTypeDef(TypedDict):
    Key: str
    Value: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class PlatformTypeDef(TypedDict):
    Version: NotRequired[str]


class AzureBlobSasConfigurationTypeDef(TypedDict):
    Token: str


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class CancelTaskExecutionRequestRequestTypeDef(TypedDict):
    TaskExecutionArn: str


class CapacityTypeDef(TypedDict):
    Used: NotRequired[int]
    Provisioned: NotRequired[int]
    LogicalUsed: NotRequired[int]
    ClusterCloudStorageUsed: NotRequired[int]


class Ec2ConfigTypeDef(TypedDict):
    SubnetArn: str
    SecurityGroupArns: Sequence[str]


class HdfsNameNodeTypeDef(TypedDict):
    Hostname: str
    Port: int


class QopConfigurationTypeDef(TypedDict):
    RpcProtection: NotRequired[HdfsRpcProtectionType]
    DataTransferProtection: NotRequired[HdfsDataTransferProtectionType]


class NfsMountOptionsTypeDef(TypedDict):
    Version: NotRequired[NfsVersionType]


class OnPremConfigTypeDef(TypedDict):
    AgentArns: Sequence[str]


class S3ConfigTypeDef(TypedDict):
    BucketAccessRoleArn: str


class SmbMountOptionsTypeDef(TypedDict):
    Version: NotRequired[SmbVersionType]


class FilterRuleTypeDef(TypedDict):
    FilterType: NotRequired[Literal["SIMPLE_PATTERN"]]
    Value: NotRequired[str]


class OptionsTypeDef(TypedDict):
    VerifyMode: NotRequired[VerifyModeType]
    OverwriteMode: NotRequired[OverwriteModeType]
    Atime: NotRequired[AtimeType]
    Mtime: NotRequired[MtimeType]
    Uid: NotRequired[UidType]
    Gid: NotRequired[GidType]
    PreserveDeletedFiles: NotRequired[PreserveDeletedFilesType]
    PreserveDevices: NotRequired[PreserveDevicesType]
    PosixPermissions: NotRequired[PosixPermissionsType]
    BytesPerSecond: NotRequired[int]
    TaskQueueing: NotRequired[TaskQueueingType]
    LogLevel: NotRequired[LogLevelType]
    TransferMode: NotRequired[TransferModeType]
    SecurityDescriptorCopyFlags: NotRequired[SmbSecurityDescriptorCopyFlagsType]
    ObjectTags: NotRequired[ObjectTagsType]


class TaskScheduleTypeDef(TypedDict):
    ScheduleExpression: str
    Status: NotRequired[ScheduleStatusType]


class DeleteAgentRequestRequestTypeDef(TypedDict):
    AgentArn: str


class DeleteLocationRequestRequestTypeDef(TypedDict):
    LocationArn: str


class DeleteTaskRequestRequestTypeDef(TypedDict):
    TaskArn: str


class DescribeAgentRequestRequestTypeDef(TypedDict):
    AgentArn: str


class PrivateLinkConfigTypeDef(TypedDict):
    VpcEndpointId: NotRequired[str]
    PrivateLinkEndpoint: NotRequired[str]
    SubnetArns: NotRequired[List[str]]
    SecurityGroupArns: NotRequired[List[str]]


class DescribeDiscoveryJobRequestRequestTypeDef(TypedDict):
    DiscoveryJobArn: str


class DescribeLocationAzureBlobRequestRequestTypeDef(TypedDict):
    LocationArn: str


class DescribeLocationEfsRequestRequestTypeDef(TypedDict):
    LocationArn: str


class Ec2ConfigOutputTypeDef(TypedDict):
    SubnetArn: str
    SecurityGroupArns: List[str]


class DescribeLocationFsxLustreRequestRequestTypeDef(TypedDict):
    LocationArn: str


class DescribeLocationFsxOntapRequestRequestTypeDef(TypedDict):
    LocationArn: str


class DescribeLocationFsxOpenZfsRequestRequestTypeDef(TypedDict):
    LocationArn: str


class DescribeLocationFsxWindowsRequestRequestTypeDef(TypedDict):
    LocationArn: str


class DescribeLocationHdfsRequestRequestTypeDef(TypedDict):
    LocationArn: str


class DescribeLocationNfsRequestRequestTypeDef(TypedDict):
    LocationArn: str


class OnPremConfigOutputTypeDef(TypedDict):
    AgentArns: List[str]


class DescribeLocationObjectStorageRequestRequestTypeDef(TypedDict):
    LocationArn: str


class DescribeLocationS3RequestRequestTypeDef(TypedDict):
    LocationArn: str


class DescribeLocationSmbRequestRequestTypeDef(TypedDict):
    LocationArn: str


class DescribeStorageSystemRequestRequestTypeDef(TypedDict):
    StorageSystemArn: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class DescribeStorageSystemResourcesRequestRequestTypeDef(TypedDict):
    DiscoveryJobArn: str
    ResourceType: DiscoveryResourceTypeType
    ResourceIds: NotRequired[Sequence[str]]
    Filter: NotRequired[Mapping[Literal["SVM"], Sequence[str]]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeTaskExecutionRequestRequestTypeDef(TypedDict):
    TaskExecutionArn: str


class ReportResultTypeDef(TypedDict):
    Status: NotRequired[PhaseStatusType]
    ErrorCode: NotRequired[str]
    ErrorDetail: NotRequired[str]


class TaskExecutionFilesFailedDetailTypeDef(TypedDict):
    Prepare: NotRequired[int]
    Transfer: NotRequired[int]
    Verify: NotRequired[int]
    Delete: NotRequired[int]


class TaskExecutionFilesListedDetailTypeDef(TypedDict):
    AtSource: NotRequired[int]
    AtDestinationForDelete: NotRequired[int]


class TaskExecutionResultDetailTypeDef(TypedDict):
    PrepareDuration: NotRequired[int]
    PrepareStatus: NotRequired[PhaseStatusType]
    TotalDuration: NotRequired[int]
    TransferDuration: NotRequired[int]
    TransferStatus: NotRequired[PhaseStatusType]
    VerifyDuration: NotRequired[int]
    VerifyStatus: NotRequired[PhaseStatusType]
    ErrorCode: NotRequired[str]
    ErrorDetail: NotRequired[str]


class DescribeTaskRequestRequestTypeDef(TypedDict):
    TaskArn: str


class TaskScheduleDetailsTypeDef(TypedDict):
    StatusUpdateTime: NotRequired[datetime]
    DisabledReason: NotRequired[str]
    DisabledBy: NotRequired[ScheduleDisabledByType]


class DiscoveryJobListEntryTypeDef(TypedDict):
    DiscoveryJobArn: NotRequired[str]
    Status: NotRequired[DiscoveryJobStatusType]


class GenerateRecommendationsRequestRequestTypeDef(TypedDict):
    DiscoveryJobArn: str
    ResourceIds: Sequence[str]
    ResourceType: DiscoveryResourceTypeType


class IOPSTypeDef(TypedDict):
    Read: NotRequired[float]
    Write: NotRequired[float]
    Other: NotRequired[float]
    Total: NotRequired[float]


class LatencyTypeDef(TypedDict):
    Read: NotRequired[float]
    Write: NotRequired[float]
    Other: NotRequired[float]


class ListAgentsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListDiscoveryJobsRequestRequestTypeDef(TypedDict):
    StorageSystemArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class LocationFilterTypeDef(TypedDict):
    Name: LocationFilterNameType
    Values: Sequence[str]
    Operator: OperatorType


class LocationListEntryTypeDef(TypedDict):
    LocationArn: NotRequired[str]
    LocationUri: NotRequired[str]


class ListStorageSystemsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class StorageSystemListEntryTypeDef(TypedDict):
    StorageSystemArn: NotRequired[str]
    Name: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTaskExecutionsRequestRequestTypeDef(TypedDict):
    TaskArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class TaskExecutionListEntryTypeDef(TypedDict):
    TaskExecutionArn: NotRequired[str]
    Status: NotRequired[TaskExecutionStatusType]
    TaskMode: NotRequired[TaskModeType]


class TaskFilterTypeDef(TypedDict):
    Name: TaskFilterNameType
    Values: Sequence[str]
    Operator: OperatorType


class TaskListEntryTypeDef(TypedDict):
    TaskArn: NotRequired[str]
    Status: NotRequired[TaskStatusType]
    Name: NotRequired[str]
    TaskMode: NotRequired[TaskModeType]


class MaxP95PerformanceTypeDef(TypedDict):
    IopsRead: NotRequired[float]
    IopsWrite: NotRequired[float]
    IopsOther: NotRequired[float]
    IopsTotal: NotRequired[float]
    ThroughputRead: NotRequired[float]
    ThroughputWrite: NotRequired[float]
    ThroughputOther: NotRequired[float]
    ThroughputTotal: NotRequired[float]
    LatencyRead: NotRequired[float]
    LatencyWrite: NotRequired[float]
    LatencyOther: NotRequired[float]


class RecommendationTypeDef(TypedDict):
    StorageType: NotRequired[str]
    StorageConfiguration: NotRequired[Dict[str, str]]
    EstimatedMonthlyStorageCost: NotRequired[str]


class ThroughputTypeDef(TypedDict):
    Read: NotRequired[float]
    Write: NotRequired[float]
    Other: NotRequired[float]
    Total: NotRequired[float]


class RemoveStorageSystemRequestRequestTypeDef(TypedDict):
    StorageSystemArn: str


class ReportDestinationS3TypeDef(TypedDict):
    S3BucketArn: str
    BucketAccessRoleArn: str
    Subdirectory: NotRequired[str]


class ReportOverrideTypeDef(TypedDict):
    ReportLevel: NotRequired[ReportLevelType]


class S3ManifestConfigTypeDef(TypedDict):
    ManifestObjectPath: str
    BucketAccessRoleArn: str
    S3BucketArn: str
    ManifestObjectVersionId: NotRequired[str]


class StopDiscoveryJobRequestRequestTypeDef(TypedDict):
    DiscoveryJobArn: str


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Keys: Sequence[str]


class UpdateAgentRequestRequestTypeDef(TypedDict):
    AgentArn: str
    Name: NotRequired[str]


class UpdateDiscoveryJobRequestRequestTypeDef(TypedDict):
    DiscoveryJobArn: str
    CollectionDurationMinutes: int


class UpdateStorageSystemRequestRequestTypeDef(TypedDict):
    StorageSystemArn: str
    ServerConfiguration: NotRequired[DiscoveryServerConfigurationTypeDef]
    AgentArns: NotRequired[Sequence[str]]
    Name: NotRequired[str]
    CloudWatchLogGroupArn: NotRequired[str]
    Credentials: NotRequired[CredentialsTypeDef]


class AddStorageSystemRequestRequestTypeDef(TypedDict):
    ServerConfiguration: DiscoveryServerConfigurationTypeDef
    SystemType: Literal["NetAppONTAP"]
    AgentArns: Sequence[str]
    ClientToken: str
    Credentials: CredentialsTypeDef
    CloudWatchLogGroupArn: NotRequired[str]
    Tags: NotRequired[Sequence[TagListEntryTypeDef]]
    Name: NotRequired[str]


class CreateAgentRequestRequestTypeDef(TypedDict):
    ActivationKey: str
    AgentName: NotRequired[str]
    Tags: NotRequired[Sequence[TagListEntryTypeDef]]
    VpcEndpointId: NotRequired[str]
    SubnetArns: NotRequired[Sequence[str]]
    SecurityGroupArns: NotRequired[Sequence[str]]


class CreateLocationFsxLustreRequestRequestTypeDef(TypedDict):
    FsxFilesystemArn: str
    SecurityGroupArns: Sequence[str]
    Subdirectory: NotRequired[str]
    Tags: NotRequired[Sequence[TagListEntryTypeDef]]


class CreateLocationFsxWindowsRequestRequestTypeDef(TypedDict):
    FsxFilesystemArn: str
    SecurityGroupArns: Sequence[str]
    User: str
    Password: str
    Subdirectory: NotRequired[str]
    Tags: NotRequired[Sequence[TagListEntryTypeDef]]
    Domain: NotRequired[str]


class StartDiscoveryJobRequestRequestTypeDef(TypedDict):
    StorageSystemArn: str
    CollectionDurationMinutes: int
    ClientToken: str
    Tags: NotRequired[Sequence[TagListEntryTypeDef]]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagListEntryTypeDef]


class AddStorageSystemResponseTypeDef(TypedDict):
    StorageSystemArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAgentResponseTypeDef(TypedDict):
    AgentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLocationAzureBlobResponseTypeDef(TypedDict):
    LocationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLocationEfsResponseTypeDef(TypedDict):
    LocationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLocationFsxLustreResponseTypeDef(TypedDict):
    LocationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLocationFsxOntapResponseTypeDef(TypedDict):
    LocationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLocationFsxOpenZfsResponseTypeDef(TypedDict):
    LocationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLocationFsxWindowsResponseTypeDef(TypedDict):
    LocationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLocationHdfsResponseTypeDef(TypedDict):
    LocationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLocationNfsResponseTypeDef(TypedDict):
    LocationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLocationObjectStorageResponseTypeDef(TypedDict):
    LocationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLocationS3ResponseTypeDef(TypedDict):
    LocationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLocationSmbResponseTypeDef(TypedDict):
    LocationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTaskResponseTypeDef(TypedDict):
    TaskArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDiscoveryJobResponseTypeDef(TypedDict):
    StorageSystemArn: str
    DiscoveryJobArn: str
    CollectionDurationMinutes: int
    Status: DiscoveryJobStatusType
    JobStartTime: datetime
    JobEndTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLocationAzureBlobResponseTypeDef(TypedDict):
    LocationArn: str
    LocationUri: str
    AuthenticationType: Literal["SAS"]
    BlobType: Literal["BLOCK"]
    AccessTier: AzureAccessTierType
    AgentArns: List[str]
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLocationFsxLustreResponseTypeDef(TypedDict):
    LocationArn: str
    LocationUri: str
    SecurityGroupArns: List[str]
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLocationFsxWindowsResponseTypeDef(TypedDict):
    LocationArn: str
    LocationUri: str
    SecurityGroupArns: List[str]
    CreationTime: datetime
    User: str
    Domain: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLocationObjectStorageResponseTypeDef(TypedDict):
    LocationArn: str
    LocationUri: str
    AccessKey: str
    ServerPort: int
    ServerProtocol: ObjectStorageServerProtocolType
    AgentArns: List[str]
    CreationTime: datetime
    ServerCertificate: bytes
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeStorageSystemResponseTypeDef(TypedDict):
    StorageSystemArn: str
    ServerConfiguration: DiscoveryServerConfigurationTypeDef
    SystemType: Literal["NetAppONTAP"]
    AgentArns: List[str]
    Name: str
    ErrorMessage: str
    ConnectivityStatus: StorageSystemConnectivityStatusType
    CloudWatchLogGroupArn: str
    CreationTime: datetime
    SecretsManagerArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagListEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StartDiscoveryJobResponseTypeDef(TypedDict):
    DiscoveryJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartTaskExecutionResponseTypeDef(TypedDict):
    TaskExecutionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class AgentListEntryTypeDef(TypedDict):
    AgentArn: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[AgentStatusType]
    Platform: NotRequired[PlatformTypeDef]


class CreateLocationAzureBlobRequestRequestTypeDef(TypedDict):
    ContainerUrl: str
    AuthenticationType: Literal["SAS"]
    AgentArns: Sequence[str]
    SasConfiguration: NotRequired[AzureBlobSasConfigurationTypeDef]
    BlobType: NotRequired[Literal["BLOCK"]]
    AccessTier: NotRequired[AzureAccessTierType]
    Subdirectory: NotRequired[str]
    Tags: NotRequired[Sequence[TagListEntryTypeDef]]


class UpdateLocationAzureBlobRequestRequestTypeDef(TypedDict):
    LocationArn: str
    Subdirectory: NotRequired[str]
    AuthenticationType: NotRequired[Literal["SAS"]]
    SasConfiguration: NotRequired[AzureBlobSasConfigurationTypeDef]
    BlobType: NotRequired[Literal["BLOCK"]]
    AccessTier: NotRequired[AzureAccessTierType]
    AgentArns: NotRequired[Sequence[str]]


class CreateLocationObjectStorageRequestRequestTypeDef(TypedDict):
    ServerHostname: str
    BucketName: str
    AgentArns: Sequence[str]
    ServerPort: NotRequired[int]
    ServerProtocol: NotRequired[ObjectStorageServerProtocolType]
    Subdirectory: NotRequired[str]
    AccessKey: NotRequired[str]
    SecretKey: NotRequired[str]
    Tags: NotRequired[Sequence[TagListEntryTypeDef]]
    ServerCertificate: NotRequired[BlobTypeDef]


class UpdateLocationObjectStorageRequestRequestTypeDef(TypedDict):
    LocationArn: str
    ServerPort: NotRequired[int]
    ServerProtocol: NotRequired[ObjectStorageServerProtocolType]
    Subdirectory: NotRequired[str]
    AccessKey: NotRequired[str]
    SecretKey: NotRequired[str]
    AgentArns: NotRequired[Sequence[str]]
    ServerCertificate: NotRequired[BlobTypeDef]


class CreateLocationEfsRequestRequestTypeDef(TypedDict):
    EfsFilesystemArn: str
    Ec2Config: Ec2ConfigTypeDef
    Subdirectory: NotRequired[str]
    Tags: NotRequired[Sequence[TagListEntryTypeDef]]
    AccessPointArn: NotRequired[str]
    FileSystemAccessRoleArn: NotRequired[str]
    InTransitEncryption: NotRequired[EfsInTransitEncryptionType]


class CreateLocationHdfsRequestRequestTypeDef(TypedDict):
    NameNodes: Sequence[HdfsNameNodeTypeDef]
    AuthenticationType: HdfsAuthenticationTypeType
    AgentArns: Sequence[str]
    Subdirectory: NotRequired[str]
    BlockSize: NotRequired[int]
    ReplicationFactor: NotRequired[int]
    KmsKeyProviderUri: NotRequired[str]
    QopConfiguration: NotRequired[QopConfigurationTypeDef]
    SimpleUser: NotRequired[str]
    KerberosPrincipal: NotRequired[str]
    KerberosKeytab: NotRequired[BlobTypeDef]
    KerberosKrb5Conf: NotRequired[BlobTypeDef]
    Tags: NotRequired[Sequence[TagListEntryTypeDef]]


class DescribeLocationHdfsResponseTypeDef(TypedDict):
    LocationArn: str
    LocationUri: str
    NameNodes: List[HdfsNameNodeTypeDef]
    BlockSize: int
    ReplicationFactor: int
    KmsKeyProviderUri: str
    QopConfiguration: QopConfigurationTypeDef
    AuthenticationType: HdfsAuthenticationTypeType
    SimpleUser: str
    KerberosPrincipal: str
    AgentArns: List[str]
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateLocationHdfsRequestRequestTypeDef(TypedDict):
    LocationArn: str
    Subdirectory: NotRequired[str]
    NameNodes: NotRequired[Sequence[HdfsNameNodeTypeDef]]
    BlockSize: NotRequired[int]
    ReplicationFactor: NotRequired[int]
    KmsKeyProviderUri: NotRequired[str]
    QopConfiguration: NotRequired[QopConfigurationTypeDef]
    AuthenticationType: NotRequired[HdfsAuthenticationTypeType]
    SimpleUser: NotRequired[str]
    KerberosPrincipal: NotRequired[str]
    KerberosKeytab: NotRequired[BlobTypeDef]
    KerberosKrb5Conf: NotRequired[BlobTypeDef]
    AgentArns: NotRequired[Sequence[str]]


class FsxProtocolNfsTypeDef(TypedDict):
    MountOptions: NotRequired[NfsMountOptionsTypeDef]


class CreateLocationNfsRequestRequestTypeDef(TypedDict):
    Subdirectory: str
    ServerHostname: str
    OnPremConfig: OnPremConfigTypeDef
    MountOptions: NotRequired[NfsMountOptionsTypeDef]
    Tags: NotRequired[Sequence[TagListEntryTypeDef]]


class UpdateLocationNfsRequestRequestTypeDef(TypedDict):
    LocationArn: str
    Subdirectory: NotRequired[str]
    OnPremConfig: NotRequired[OnPremConfigTypeDef]
    MountOptions: NotRequired[NfsMountOptionsTypeDef]


class CreateLocationS3RequestRequestTypeDef(TypedDict):
    S3BucketArn: str
    S3Config: S3ConfigTypeDef
    Subdirectory: NotRequired[str]
    S3StorageClass: NotRequired[S3StorageClassType]
    AgentArns: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagListEntryTypeDef]]


class DescribeLocationS3ResponseTypeDef(TypedDict):
    LocationArn: str
    LocationUri: str
    S3StorageClass: S3StorageClassType
    S3Config: S3ConfigTypeDef
    AgentArns: List[str]
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLocationSmbRequestRequestTypeDef(TypedDict):
    Subdirectory: str
    ServerHostname: str
    User: str
    Password: str
    AgentArns: Sequence[str]
    Domain: NotRequired[str]
    MountOptions: NotRequired[SmbMountOptionsTypeDef]
    Tags: NotRequired[Sequence[TagListEntryTypeDef]]


class DescribeLocationSmbResponseTypeDef(TypedDict):
    LocationArn: str
    LocationUri: str
    AgentArns: List[str]
    User: str
    Domain: str
    MountOptions: SmbMountOptionsTypeDef
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class FsxProtocolSmbTypeDef(TypedDict):
    Password: str
    User: str
    Domain: NotRequired[str]
    MountOptions: NotRequired[SmbMountOptionsTypeDef]


class UpdateLocationSmbRequestRequestTypeDef(TypedDict):
    LocationArn: str
    Subdirectory: NotRequired[str]
    User: NotRequired[str]
    Domain: NotRequired[str]
    Password: NotRequired[str]
    AgentArns: NotRequired[Sequence[str]]
    MountOptions: NotRequired[SmbMountOptionsTypeDef]


class UpdateTaskExecutionRequestRequestTypeDef(TypedDict):
    TaskExecutionArn: str
    Options: OptionsTypeDef


class DescribeAgentResponseTypeDef(TypedDict):
    AgentArn: str
    Name: str
    Status: AgentStatusType
    LastConnectionTime: datetime
    CreationTime: datetime
    EndpointType: EndpointTypeType
    PrivateLinkConfig: PrivateLinkConfigTypeDef
    Platform: PlatformTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLocationEfsResponseTypeDef(TypedDict):
    LocationArn: str
    LocationUri: str
    Ec2Config: Ec2ConfigOutputTypeDef
    CreationTime: datetime
    AccessPointArn: str
    FileSystemAccessRoleArn: str
    InTransitEncryption: EfsInTransitEncryptionType
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLocationNfsResponseTypeDef(TypedDict):
    LocationArn: str
    LocationUri: str
    OnPremConfig: OnPremConfigOutputTypeDef
    MountOptions: NfsMountOptionsTypeDef
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ListAgentsRequestListAgentsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDiscoveryJobsRequestListDiscoveryJobsPaginateTypeDef(TypedDict):
    StorageSystemArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStorageSystemsRequestListStorageSystemsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(TypedDict):
    ResourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTaskExecutionsRequestListTaskExecutionsPaginateTypeDef(TypedDict):
    TaskArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeStorageSystemResourceMetricsRequestDescribeStorageSystemResourceMetricsPaginateTypeDef(
    TypedDict
):
    DiscoveryJobArn: str
    ResourceType: DiscoveryResourceTypeType
    ResourceId: str
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeStorageSystemResourceMetricsRequestRequestTypeDef(TypedDict):
    DiscoveryJobArn: str
    ResourceType: DiscoveryResourceTypeType
    ResourceId: str
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListDiscoveryJobsResponseTypeDef(TypedDict):
    DiscoveryJobs: List[DiscoveryJobListEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListLocationsRequestListLocationsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[LocationFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLocationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[LocationFilterTypeDef]]


class ListLocationsResponseTypeDef(TypedDict):
    Locations: List[LocationListEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListStorageSystemsResponseTypeDef(TypedDict):
    StorageSystems: List[StorageSystemListEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTaskExecutionsResponseTypeDef(TypedDict):
    TaskExecutions: List[TaskExecutionListEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTasksRequestListTasksPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[TaskFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTasksRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[TaskFilterTypeDef]]


class ListTasksResponseTypeDef(TypedDict):
    Tasks: List[TaskListEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class NetAppONTAPClusterTypeDef(TypedDict):
    CifsShareCount: NotRequired[int]
    NfsExportedVolumes: NotRequired[int]
    ResourceId: NotRequired[str]
    ClusterName: NotRequired[str]
    MaxP95Performance: NotRequired[MaxP95PerformanceTypeDef]
    ClusterBlockStorageSize: NotRequired[int]
    ClusterBlockStorageUsed: NotRequired[int]
    ClusterBlockStorageLogicalUsed: NotRequired[int]
    Recommendations: NotRequired[List[RecommendationTypeDef]]
    RecommendationStatus: NotRequired[RecommendationStatusType]
    LunCount: NotRequired[int]
    ClusterCloudStorageUsed: NotRequired[int]


class NetAppONTAPSVMTypeDef(TypedDict):
    ClusterUuid: NotRequired[str]
    ResourceId: NotRequired[str]
    SvmName: NotRequired[str]
    CifsShareCount: NotRequired[int]
    EnabledProtocols: NotRequired[List[str]]
    TotalCapacityUsed: NotRequired[int]
    TotalCapacityProvisioned: NotRequired[int]
    TotalLogicalCapacityUsed: NotRequired[int]
    MaxP95Performance: NotRequired[MaxP95PerformanceTypeDef]
    Recommendations: NotRequired[List[RecommendationTypeDef]]
    NfsExportedVolumes: NotRequired[int]
    RecommendationStatus: NotRequired[RecommendationStatusType]
    TotalSnapshotCapacityUsed: NotRequired[int]
    LunCount: NotRequired[int]


class NetAppONTAPVolumeTypeDef(TypedDict):
    VolumeName: NotRequired[str]
    ResourceId: NotRequired[str]
    CifsShareCount: NotRequired[int]
    SecurityStyle: NotRequired[str]
    SvmUuid: NotRequired[str]
    SvmName: NotRequired[str]
    CapacityUsed: NotRequired[int]
    CapacityProvisioned: NotRequired[int]
    LogicalCapacityUsed: NotRequired[int]
    NfsExported: NotRequired[bool]
    SnapshotCapacityUsed: NotRequired[int]
    MaxP95Performance: NotRequired[MaxP95PerformanceTypeDef]
    Recommendations: NotRequired[List[RecommendationTypeDef]]
    RecommendationStatus: NotRequired[RecommendationStatusType]
    LunCount: NotRequired[int]


class P95MetricsTypeDef(TypedDict):
    IOPS: NotRequired[IOPSTypeDef]
    Throughput: NotRequired[ThroughputTypeDef]
    Latency: NotRequired[LatencyTypeDef]


class ReportDestinationTypeDef(TypedDict):
    S3: NotRequired[ReportDestinationS3TypeDef]


class ReportOverridesTypeDef(TypedDict):
    Transferred: NotRequired[ReportOverrideTypeDef]
    Verified: NotRequired[ReportOverrideTypeDef]
    Deleted: NotRequired[ReportOverrideTypeDef]
    Skipped: NotRequired[ReportOverrideTypeDef]


class SourceManifestConfigTypeDef(TypedDict):
    S3: S3ManifestConfigTypeDef


class ListAgentsResponseTypeDef(TypedDict):
    Agents: List[AgentListEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class FsxProtocolTypeDef(TypedDict):
    NFS: NotRequired[FsxProtocolNfsTypeDef]
    SMB: NotRequired[FsxProtocolSmbTypeDef]


class ResourceDetailsTypeDef(TypedDict):
    NetAppONTAPSVMs: NotRequired[List[NetAppONTAPSVMTypeDef]]
    NetAppONTAPVolumes: NotRequired[List[NetAppONTAPVolumeTypeDef]]
    NetAppONTAPClusters: NotRequired[List[NetAppONTAPClusterTypeDef]]


class ResourceMetricsTypeDef(TypedDict):
    Timestamp: NotRequired[datetime]
    P95Metrics: NotRequired[P95MetricsTypeDef]
    Capacity: NotRequired[CapacityTypeDef]
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[DiscoveryResourceTypeType]


class TaskReportConfigTypeDef(TypedDict):
    Destination: NotRequired[ReportDestinationTypeDef]
    OutputType: NotRequired[ReportOutputTypeType]
    ReportLevel: NotRequired[ReportLevelType]
    ObjectVersionIds: NotRequired[ObjectVersionIdsType]
    Overrides: NotRequired[ReportOverridesTypeDef]


class ManifestConfigTypeDef(TypedDict):
    Action: NotRequired[Literal["TRANSFER"]]
    Format: NotRequired[Literal["CSV"]]
    Source: NotRequired[SourceManifestConfigTypeDef]


CreateLocationFsxOntapRequestRequestTypeDef = TypedDict(
    "CreateLocationFsxOntapRequestRequestTypeDef",
    {
        "Protocol": FsxProtocolTypeDef,
        "SecurityGroupArns": Sequence[str],
        "StorageVirtualMachineArn": str,
        "Subdirectory": NotRequired[str],
        "Tags": NotRequired[Sequence[TagListEntryTypeDef]],
    },
)
CreateLocationFsxOpenZfsRequestRequestTypeDef = TypedDict(
    "CreateLocationFsxOpenZfsRequestRequestTypeDef",
    {
        "FsxFilesystemArn": str,
        "Protocol": FsxProtocolTypeDef,
        "SecurityGroupArns": Sequence[str],
        "Subdirectory": NotRequired[str],
        "Tags": NotRequired[Sequence[TagListEntryTypeDef]],
    },
)
DescribeLocationFsxOntapResponseTypeDef = TypedDict(
    "DescribeLocationFsxOntapResponseTypeDef",
    {
        "CreationTime": datetime,
        "LocationArn": str,
        "LocationUri": str,
        "Protocol": FsxProtocolTypeDef,
        "SecurityGroupArns": List[str],
        "StorageVirtualMachineArn": str,
        "FsxFilesystemArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeLocationFsxOpenZfsResponseTypeDef = TypedDict(
    "DescribeLocationFsxOpenZfsResponseTypeDef",
    {
        "LocationArn": str,
        "LocationUri": str,
        "SecurityGroupArns": List[str],
        "Protocol": FsxProtocolTypeDef,
        "CreationTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class DescribeStorageSystemResourcesResponseTypeDef(TypedDict):
    ResourceDetails: ResourceDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeStorageSystemResourceMetricsResponseTypeDef(TypedDict):
    Metrics: List[ResourceMetricsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateTaskRequestRequestTypeDef(TypedDict):
    SourceLocationArn: str
    DestinationLocationArn: str
    CloudWatchLogGroupArn: NotRequired[str]
    Name: NotRequired[str]
    Options: NotRequired[OptionsTypeDef]
    Excludes: NotRequired[Sequence[FilterRuleTypeDef]]
    Schedule: NotRequired[TaskScheduleTypeDef]
    Tags: NotRequired[Sequence[TagListEntryTypeDef]]
    Includes: NotRequired[Sequence[FilterRuleTypeDef]]
    ManifestConfig: NotRequired[ManifestConfigTypeDef]
    TaskReportConfig: NotRequired[TaskReportConfigTypeDef]
    TaskMode: NotRequired[TaskModeType]


class DescribeTaskExecutionResponseTypeDef(TypedDict):
    TaskExecutionArn: str
    Status: TaskExecutionStatusType
    Options: OptionsTypeDef
    Excludes: List[FilterRuleTypeDef]
    Includes: List[FilterRuleTypeDef]
    ManifestConfig: ManifestConfigTypeDef
    StartTime: datetime
    EstimatedFilesToTransfer: int
    EstimatedBytesToTransfer: int
    FilesTransferred: int
    BytesWritten: int
    BytesTransferred: int
    BytesCompressed: int
    Result: TaskExecutionResultDetailTypeDef
    TaskReportConfig: TaskReportConfigTypeDef
    FilesDeleted: int
    FilesSkipped: int
    FilesVerified: int
    ReportResult: ReportResultTypeDef
    EstimatedFilesToDelete: int
    TaskMode: TaskModeType
    FilesPrepared: int
    FilesListed: TaskExecutionFilesListedDetailTypeDef
    FilesFailed: TaskExecutionFilesFailedDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTaskResponseTypeDef(TypedDict):
    TaskArn: str
    Status: TaskStatusType
    Name: str
    CurrentTaskExecutionArn: str
    SourceLocationArn: str
    DestinationLocationArn: str
    CloudWatchLogGroupArn: str
    SourceNetworkInterfaceArns: List[str]
    DestinationNetworkInterfaceArns: List[str]
    Options: OptionsTypeDef
    Excludes: List[FilterRuleTypeDef]
    Schedule: TaskScheduleTypeDef
    ErrorCode: str
    ErrorDetail: str
    CreationTime: datetime
    Includes: List[FilterRuleTypeDef]
    ManifestConfig: ManifestConfigTypeDef
    TaskReportConfig: TaskReportConfigTypeDef
    ScheduleDetails: TaskScheduleDetailsTypeDef
    TaskMode: TaskModeType
    ResponseMetadata: ResponseMetadataTypeDef


class StartTaskExecutionRequestRequestTypeDef(TypedDict):
    TaskArn: str
    OverrideOptions: NotRequired[OptionsTypeDef]
    Includes: NotRequired[Sequence[FilterRuleTypeDef]]
    Excludes: NotRequired[Sequence[FilterRuleTypeDef]]
    ManifestConfig: NotRequired[ManifestConfigTypeDef]
    TaskReportConfig: NotRequired[TaskReportConfigTypeDef]
    Tags: NotRequired[Sequence[TagListEntryTypeDef]]


class UpdateTaskRequestRequestTypeDef(TypedDict):
    TaskArn: str
    Options: NotRequired[OptionsTypeDef]
    Excludes: NotRequired[Sequence[FilterRuleTypeDef]]
    Schedule: NotRequired[TaskScheduleTypeDef]
    Name: NotRequired[str]
    CloudWatchLogGroupArn: NotRequired[str]
    Includes: NotRequired[Sequence[FilterRuleTypeDef]]
    ManifestConfig: NotRequired[ManifestConfigTypeDef]
    TaskReportConfig: NotRequired[TaskReportConfigTypeDef]
