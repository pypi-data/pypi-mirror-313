"""
Type annotations for timestream-influxdb service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/type_defs/)

Usage::

    ```python
    from mypy_boto3_timestream_influxdb.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Mapping, Sequence

from .literals import (
    DbInstanceTypeType,
    DbStorageTypeType,
    DeploymentTypeType,
    DurationTypeType,
    LogLevelType,
    StatusType,
    TracingTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "CreateDbInstanceInputRequestTypeDef",
    "CreateDbInstanceOutputTypeDef",
    "CreateDbParameterGroupInputRequestTypeDef",
    "CreateDbParameterGroupOutputTypeDef",
    "DbInstanceSummaryTypeDef",
    "DbParameterGroupSummaryTypeDef",
    "DeleteDbInstanceInputRequestTypeDef",
    "DeleteDbInstanceOutputTypeDef",
    "DurationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetDbInstanceInputRequestTypeDef",
    "GetDbInstanceOutputTypeDef",
    "GetDbParameterGroupInputRequestTypeDef",
    "GetDbParameterGroupOutputTypeDef",
    "InfluxDBv2ParametersTypeDef",
    "ListDbInstancesInputListDbInstancesPaginateTypeDef",
    "ListDbInstancesInputRequestTypeDef",
    "ListDbInstancesOutputTypeDef",
    "ListDbParameterGroupsInputListDbParameterGroupsPaginateTypeDef",
    "ListDbParameterGroupsInputRequestTypeDef",
    "ListDbParameterGroupsOutputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LogDeliveryConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ParametersTypeDef",
    "ResponseMetadataTypeDef",
    "S3ConfigurationTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDbInstanceInputRequestTypeDef",
    "UpdateDbInstanceOutputTypeDef",
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


DbInstanceSummaryTypeDef = TypedDict(
    "DbInstanceSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": NotRequired[StatusType],
        "endpoint": NotRequired[str],
        "port": NotRequired[int],
        "dbInstanceType": NotRequired[DbInstanceTypeType],
        "dbStorageType": NotRequired[DbStorageTypeType],
        "allocatedStorage": NotRequired[int],
        "deploymentType": NotRequired[DeploymentTypeType],
    },
)
DbParameterGroupSummaryTypeDef = TypedDict(
    "DbParameterGroupSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "description": NotRequired[str],
    },
)


class DeleteDbInstanceInputRequestTypeDef(TypedDict):
    identifier: str


class DurationTypeDef(TypedDict):
    durationType: DurationTypeType
    value: int


class GetDbInstanceInputRequestTypeDef(TypedDict):
    identifier: str


class GetDbParameterGroupInputRequestTypeDef(TypedDict):
    identifier: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListDbInstancesInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDbParameterGroupsInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class S3ConfigurationTypeDef(TypedDict):
    bucketName: str
    enabled: bool


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListDbInstancesOutputTypeDef(TypedDict):
    items: List[DbInstanceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListDbParameterGroupsOutputTypeDef(TypedDict):
    items: List[DbParameterGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class InfluxDBv2ParametersTypeDef(TypedDict):
    fluxLogEnabled: NotRequired[bool]
    logLevel: NotRequired[LogLevelType]
    noTasks: NotRequired[bool]
    queryConcurrency: NotRequired[int]
    queryQueueSize: NotRequired[int]
    tracingType: NotRequired[TracingTypeType]
    metricsDisabled: NotRequired[bool]
    httpIdleTimeout: NotRequired[DurationTypeDef]
    httpReadHeaderTimeout: NotRequired[DurationTypeDef]
    httpReadTimeout: NotRequired[DurationTypeDef]
    httpWriteTimeout: NotRequired[DurationTypeDef]
    influxqlMaxSelectBuckets: NotRequired[int]
    influxqlMaxSelectPoint: NotRequired[int]
    influxqlMaxSelectSeries: NotRequired[int]
    pprofDisabled: NotRequired[bool]
    queryInitialMemoryBytes: NotRequired[int]
    queryMaxMemoryBytes: NotRequired[int]
    queryMemoryBytes: NotRequired[int]
    sessionLength: NotRequired[int]
    sessionRenewDisabled: NotRequired[bool]
    storageCacheMaxMemorySize: NotRequired[int]
    storageCacheSnapshotMemorySize: NotRequired[int]
    storageCacheSnapshotWriteColdDuration: NotRequired[DurationTypeDef]
    storageCompactFullWriteColdDuration: NotRequired[DurationTypeDef]
    storageCompactThroughputBurst: NotRequired[int]
    storageMaxConcurrentCompactions: NotRequired[int]
    storageMaxIndexLogFileSize: NotRequired[int]
    storageNoValidateFieldSize: NotRequired[bool]
    storageRetentionCheckInterval: NotRequired[DurationTypeDef]
    storageSeriesFileMaxConcurrentSnapshotCompactions: NotRequired[int]
    storageSeriesIdSetCacheSize: NotRequired[int]
    storageWalMaxConcurrentWrites: NotRequired[int]
    storageWalMaxWriteDelay: NotRequired[DurationTypeDef]
    uiDisabled: NotRequired[bool]


class ListDbInstancesInputListDbInstancesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDbParameterGroupsInputListDbParameterGroupsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class LogDeliveryConfigurationTypeDef(TypedDict):
    s3Configuration: S3ConfigurationTypeDef


class ParametersTypeDef(TypedDict):
    InfluxDBv2: NotRequired[InfluxDBv2ParametersTypeDef]


class CreateDbInstanceInputRequestTypeDef(TypedDict):
    name: str
    password: str
    dbInstanceType: DbInstanceTypeType
    vpcSubnetIds: Sequence[str]
    vpcSecurityGroupIds: Sequence[str]
    allocatedStorage: int
    username: NotRequired[str]
    organization: NotRequired[str]
    bucket: NotRequired[str]
    publiclyAccessible: NotRequired[bool]
    dbStorageType: NotRequired[DbStorageTypeType]
    dbParameterGroupIdentifier: NotRequired[str]
    deploymentType: NotRequired[DeploymentTypeType]
    logDeliveryConfiguration: NotRequired[LogDeliveryConfigurationTypeDef]
    tags: NotRequired[Mapping[str, str]]
    port: NotRequired[int]


CreateDbInstanceOutputTypeDef = TypedDict(
    "CreateDbInstanceOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": StatusType,
        "endpoint": str,
        "port": int,
        "dbInstanceType": DbInstanceTypeType,
        "dbStorageType": DbStorageTypeType,
        "allocatedStorage": int,
        "deploymentType": DeploymentTypeType,
        "vpcSubnetIds": List[str],
        "publiclyAccessible": bool,
        "vpcSecurityGroupIds": List[str],
        "dbParameterGroupIdentifier": str,
        "availabilityZone": str,
        "secondaryAvailabilityZone": str,
        "logDeliveryConfiguration": LogDeliveryConfigurationTypeDef,
        "influxAuthParametersSecretArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteDbInstanceOutputTypeDef = TypedDict(
    "DeleteDbInstanceOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": StatusType,
        "endpoint": str,
        "port": int,
        "dbInstanceType": DbInstanceTypeType,
        "dbStorageType": DbStorageTypeType,
        "allocatedStorage": int,
        "deploymentType": DeploymentTypeType,
        "vpcSubnetIds": List[str],
        "publiclyAccessible": bool,
        "vpcSecurityGroupIds": List[str],
        "dbParameterGroupIdentifier": str,
        "availabilityZone": str,
        "secondaryAvailabilityZone": str,
        "logDeliveryConfiguration": LogDeliveryConfigurationTypeDef,
        "influxAuthParametersSecretArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDbInstanceOutputTypeDef = TypedDict(
    "GetDbInstanceOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": StatusType,
        "endpoint": str,
        "port": int,
        "dbInstanceType": DbInstanceTypeType,
        "dbStorageType": DbStorageTypeType,
        "allocatedStorage": int,
        "deploymentType": DeploymentTypeType,
        "vpcSubnetIds": List[str],
        "publiclyAccessible": bool,
        "vpcSecurityGroupIds": List[str],
        "dbParameterGroupIdentifier": str,
        "availabilityZone": str,
        "secondaryAvailabilityZone": str,
        "logDeliveryConfiguration": LogDeliveryConfigurationTypeDef,
        "influxAuthParametersSecretArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class UpdateDbInstanceInputRequestTypeDef(TypedDict):
    identifier: str
    logDeliveryConfiguration: NotRequired[LogDeliveryConfigurationTypeDef]
    dbParameterGroupIdentifier: NotRequired[str]
    port: NotRequired[int]
    dbInstanceType: NotRequired[DbInstanceTypeType]
    deploymentType: NotRequired[DeploymentTypeType]


UpdateDbInstanceOutputTypeDef = TypedDict(
    "UpdateDbInstanceOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": StatusType,
        "endpoint": str,
        "port": int,
        "dbInstanceType": DbInstanceTypeType,
        "dbStorageType": DbStorageTypeType,
        "allocatedStorage": int,
        "deploymentType": DeploymentTypeType,
        "vpcSubnetIds": List[str],
        "publiclyAccessible": bool,
        "vpcSecurityGroupIds": List[str],
        "dbParameterGroupIdentifier": str,
        "availabilityZone": str,
        "secondaryAvailabilityZone": str,
        "logDeliveryConfiguration": LogDeliveryConfigurationTypeDef,
        "influxAuthParametersSecretArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class CreateDbParameterGroupInputRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    parameters: NotRequired[ParametersTypeDef]
    tags: NotRequired[Mapping[str, str]]


CreateDbParameterGroupOutputTypeDef = TypedDict(
    "CreateDbParameterGroupOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "description": str,
        "parameters": ParametersTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDbParameterGroupOutputTypeDef = TypedDict(
    "GetDbParameterGroupOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "description": str,
        "parameters": ParametersTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
