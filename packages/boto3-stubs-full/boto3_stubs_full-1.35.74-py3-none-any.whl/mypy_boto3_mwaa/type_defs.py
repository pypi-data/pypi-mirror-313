"""
Type annotations for mwaa service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mwaa/type_defs/)

Usage::

    ```python
    from mypy_boto3_mwaa.type_defs import CreateCliTokenRequestRequestTypeDef

    data: CreateCliTokenRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    EndpointManagementType,
    EnvironmentStatusType,
    LoggingLevelType,
    RestApiMethodType,
    UnitType,
    UpdateStatusType,
    WebserverAccessModeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "CreateCliTokenRequestRequestTypeDef",
    "CreateCliTokenResponseTypeDef",
    "CreateEnvironmentInputRequestTypeDef",
    "CreateEnvironmentOutputTypeDef",
    "CreateWebLoginTokenRequestRequestTypeDef",
    "CreateWebLoginTokenResponseTypeDef",
    "DeleteEnvironmentInputRequestTypeDef",
    "DimensionTypeDef",
    "EnvironmentTypeDef",
    "GetEnvironmentInputRequestTypeDef",
    "GetEnvironmentOutputTypeDef",
    "InvokeRestApiRequestRequestTypeDef",
    "InvokeRestApiResponseTypeDef",
    "LastUpdateTypeDef",
    "ListEnvironmentsInputListEnvironmentsPaginateTypeDef",
    "ListEnvironmentsInputRequestTypeDef",
    "ListEnvironmentsOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "LoggingConfigurationInputTypeDef",
    "LoggingConfigurationTypeDef",
    "MetricDatumTypeDef",
    "ModuleLoggingConfigurationInputTypeDef",
    "ModuleLoggingConfigurationTypeDef",
    "NetworkConfigurationOutputTypeDef",
    "NetworkConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PublishMetricsInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "StatisticSetTypeDef",
    "TagResourceInputRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateEnvironmentInputRequestTypeDef",
    "UpdateEnvironmentOutputTypeDef",
    "UpdateErrorTypeDef",
    "UpdateNetworkConfigurationInputTypeDef",
)


class CreateCliTokenRequestRequestTypeDef(TypedDict):
    Name: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class NetworkConfigurationTypeDef(TypedDict):
    SubnetIds: NotRequired[Sequence[str]]
    SecurityGroupIds: NotRequired[Sequence[str]]


class CreateWebLoginTokenRequestRequestTypeDef(TypedDict):
    Name: str


class DeleteEnvironmentInputRequestTypeDef(TypedDict):
    Name: str


class DimensionTypeDef(TypedDict):
    Name: str
    Value: str


class NetworkConfigurationOutputTypeDef(TypedDict):
    SubnetIds: NotRequired[List[str]]
    SecurityGroupIds: NotRequired[List[str]]


class GetEnvironmentInputRequestTypeDef(TypedDict):
    Name: str


class InvokeRestApiRequestRequestTypeDef(TypedDict):
    Name: str
    Path: str
    Method: RestApiMethodType
    QueryParameters: NotRequired[Mapping[str, Any]]
    Body: NotRequired[Mapping[str, Any]]


class UpdateErrorTypeDef(TypedDict):
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListEnvironmentsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTagsForResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str


class ModuleLoggingConfigurationInputTypeDef(TypedDict):
    Enabled: bool
    LogLevel: LoggingLevelType


class ModuleLoggingConfigurationTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    LogLevel: NotRequired[LoggingLevelType]
    CloudWatchLogGroupArn: NotRequired[str]


class StatisticSetTypeDef(TypedDict):
    SampleCount: NotRequired[int]
    Sum: NotRequired[float]
    Minimum: NotRequired[float]
    Maximum: NotRequired[float]


TimestampTypeDef = Union[datetime, str]


class TagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    tagKeys: Sequence[str]


class UpdateNetworkConfigurationInputTypeDef(TypedDict):
    SecurityGroupIds: Sequence[str]


class CreateCliTokenResponseTypeDef(TypedDict):
    CliToken: str
    WebServerHostname: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEnvironmentOutputTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateWebLoginTokenResponseTypeDef(TypedDict):
    WebToken: str
    WebServerHostname: str
    IamIdentity: str
    AirflowIdentity: str
    ResponseMetadata: ResponseMetadataTypeDef


class InvokeRestApiResponseTypeDef(TypedDict):
    RestApiStatusCode: int
    RestApiResponse: Dict[str, Any]
    ResponseMetadata: ResponseMetadataTypeDef


class ListEnvironmentsOutputTypeDef(TypedDict):
    Environments: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceOutputTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateEnvironmentOutputTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class LastUpdateTypeDef(TypedDict):
    Status: NotRequired[UpdateStatusType]
    CreatedAt: NotRequired[datetime]
    Error: NotRequired[UpdateErrorTypeDef]
    Source: NotRequired[str]


class ListEnvironmentsInputListEnvironmentsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class LoggingConfigurationInputTypeDef(TypedDict):
    DagProcessingLogs: NotRequired[ModuleLoggingConfigurationInputTypeDef]
    SchedulerLogs: NotRequired[ModuleLoggingConfigurationInputTypeDef]
    WebserverLogs: NotRequired[ModuleLoggingConfigurationInputTypeDef]
    WorkerLogs: NotRequired[ModuleLoggingConfigurationInputTypeDef]
    TaskLogs: NotRequired[ModuleLoggingConfigurationInputTypeDef]


class LoggingConfigurationTypeDef(TypedDict):
    DagProcessingLogs: NotRequired[ModuleLoggingConfigurationTypeDef]
    SchedulerLogs: NotRequired[ModuleLoggingConfigurationTypeDef]
    WebserverLogs: NotRequired[ModuleLoggingConfigurationTypeDef]
    WorkerLogs: NotRequired[ModuleLoggingConfigurationTypeDef]
    TaskLogs: NotRequired[ModuleLoggingConfigurationTypeDef]


class MetricDatumTypeDef(TypedDict):
    MetricName: str
    Timestamp: TimestampTypeDef
    Dimensions: NotRequired[Sequence[DimensionTypeDef]]
    Value: NotRequired[float]
    Unit: NotRequired[UnitType]
    StatisticValues: NotRequired[StatisticSetTypeDef]


class CreateEnvironmentInputRequestTypeDef(TypedDict):
    Name: str
    ExecutionRoleArn: str
    SourceBucketArn: str
    DagS3Path: str
    NetworkConfiguration: NetworkConfigurationTypeDef
    PluginsS3Path: NotRequired[str]
    PluginsS3ObjectVersion: NotRequired[str]
    RequirementsS3Path: NotRequired[str]
    RequirementsS3ObjectVersion: NotRequired[str]
    StartupScriptS3Path: NotRequired[str]
    StartupScriptS3ObjectVersion: NotRequired[str]
    AirflowConfigurationOptions: NotRequired[Mapping[str, str]]
    EnvironmentClass: NotRequired[str]
    MaxWorkers: NotRequired[int]
    KmsKey: NotRequired[str]
    AirflowVersion: NotRequired[str]
    LoggingConfiguration: NotRequired[LoggingConfigurationInputTypeDef]
    WeeklyMaintenanceWindowStart: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    WebserverAccessMode: NotRequired[WebserverAccessModeType]
    MinWorkers: NotRequired[int]
    Schedulers: NotRequired[int]
    EndpointManagement: NotRequired[EndpointManagementType]
    MinWebservers: NotRequired[int]
    MaxWebservers: NotRequired[int]


class UpdateEnvironmentInputRequestTypeDef(TypedDict):
    Name: str
    ExecutionRoleArn: NotRequired[str]
    AirflowVersion: NotRequired[str]
    SourceBucketArn: NotRequired[str]
    DagS3Path: NotRequired[str]
    PluginsS3Path: NotRequired[str]
    PluginsS3ObjectVersion: NotRequired[str]
    RequirementsS3Path: NotRequired[str]
    RequirementsS3ObjectVersion: NotRequired[str]
    StartupScriptS3Path: NotRequired[str]
    StartupScriptS3ObjectVersion: NotRequired[str]
    AirflowConfigurationOptions: NotRequired[Mapping[str, str]]
    EnvironmentClass: NotRequired[str]
    MaxWorkers: NotRequired[int]
    NetworkConfiguration: NotRequired[UpdateNetworkConfigurationInputTypeDef]
    LoggingConfiguration: NotRequired[LoggingConfigurationInputTypeDef]
    WeeklyMaintenanceWindowStart: NotRequired[str]
    WebserverAccessMode: NotRequired[WebserverAccessModeType]
    MinWorkers: NotRequired[int]
    Schedulers: NotRequired[int]
    MinWebservers: NotRequired[int]
    MaxWebservers: NotRequired[int]


class EnvironmentTypeDef(TypedDict):
    Name: NotRequired[str]
    Status: NotRequired[EnvironmentStatusType]
    Arn: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    WebserverUrl: NotRequired[str]
    ExecutionRoleArn: NotRequired[str]
    ServiceRoleArn: NotRequired[str]
    KmsKey: NotRequired[str]
    AirflowVersion: NotRequired[str]
    SourceBucketArn: NotRequired[str]
    DagS3Path: NotRequired[str]
    PluginsS3Path: NotRequired[str]
    PluginsS3ObjectVersion: NotRequired[str]
    RequirementsS3Path: NotRequired[str]
    RequirementsS3ObjectVersion: NotRequired[str]
    StartupScriptS3Path: NotRequired[str]
    StartupScriptS3ObjectVersion: NotRequired[str]
    AirflowConfigurationOptions: NotRequired[Dict[str, str]]
    EnvironmentClass: NotRequired[str]
    MaxWorkers: NotRequired[int]
    NetworkConfiguration: NotRequired[NetworkConfigurationOutputTypeDef]
    LoggingConfiguration: NotRequired[LoggingConfigurationTypeDef]
    LastUpdate: NotRequired[LastUpdateTypeDef]
    WeeklyMaintenanceWindowStart: NotRequired[str]
    Tags: NotRequired[Dict[str, str]]
    WebserverAccessMode: NotRequired[WebserverAccessModeType]
    MinWorkers: NotRequired[int]
    Schedulers: NotRequired[int]
    WebserverVpcEndpointService: NotRequired[str]
    DatabaseVpcEndpointService: NotRequired[str]
    CeleryExecutorQueue: NotRequired[str]
    EndpointManagement: NotRequired[EndpointManagementType]
    MinWebservers: NotRequired[int]
    MaxWebservers: NotRequired[int]


class PublishMetricsInputRequestTypeDef(TypedDict):
    EnvironmentName: str
    MetricData: Sequence[MetricDatumTypeDef]


class GetEnvironmentOutputTypeDef(TypedDict):
    Environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
