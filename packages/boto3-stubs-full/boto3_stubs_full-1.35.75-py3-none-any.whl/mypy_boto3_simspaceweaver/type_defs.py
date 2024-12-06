"""
Type annotations for simspaceweaver service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/type_defs/)

Usage::

    ```python
    from mypy_boto3_simspaceweaver.type_defs import CloudWatchLogsLogGroupTypeDef

    data: CloudWatchLogsLogGroupTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ClockStatusType,
    ClockTargetStatusType,
    LifecycleManagementStrategyType,
    SimulationAppStatusType,
    SimulationAppTargetStatusType,
    SimulationStatusType,
    SimulationTargetStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "CloudWatchLogsLogGroupTypeDef",
    "CreateSnapshotInputRequestTypeDef",
    "DeleteAppInputRequestTypeDef",
    "DeleteSimulationInputRequestTypeDef",
    "DescribeAppInputRequestTypeDef",
    "DescribeAppOutputTypeDef",
    "DescribeSimulationInputRequestTypeDef",
    "DescribeSimulationOutputTypeDef",
    "DomainTypeDef",
    "LaunchOverridesOutputTypeDef",
    "LaunchOverridesTypeDef",
    "ListAppsInputRequestTypeDef",
    "ListAppsOutputTypeDef",
    "ListSimulationsInputRequestTypeDef",
    "ListSimulationsOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "LiveSimulationStateTypeDef",
    "LogDestinationTypeDef",
    "LoggingConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "S3DestinationTypeDef",
    "S3LocationTypeDef",
    "SimulationAppEndpointInfoTypeDef",
    "SimulationAppMetadataTypeDef",
    "SimulationAppPortMappingTypeDef",
    "SimulationClockTypeDef",
    "SimulationMetadataTypeDef",
    "StartAppInputRequestTypeDef",
    "StartAppOutputTypeDef",
    "StartClockInputRequestTypeDef",
    "StartSimulationInputRequestTypeDef",
    "StartSimulationOutputTypeDef",
    "StopAppInputRequestTypeDef",
    "StopClockInputRequestTypeDef",
    "StopSimulationInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
)


class CloudWatchLogsLogGroupTypeDef(TypedDict):
    LogGroupArn: NotRequired[str]


class S3DestinationTypeDef(TypedDict):
    BucketName: str
    ObjectKeyPrefix: NotRequired[str]


class DeleteAppInputRequestTypeDef(TypedDict):
    App: str
    Domain: str
    Simulation: str


class DeleteSimulationInputRequestTypeDef(TypedDict):
    Simulation: str


class DescribeAppInputRequestTypeDef(TypedDict):
    App: str
    Domain: str
    Simulation: str


class LaunchOverridesOutputTypeDef(TypedDict):
    LaunchCommands: NotRequired[List[str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DescribeSimulationInputRequestTypeDef(TypedDict):
    Simulation: str


class S3LocationTypeDef(TypedDict):
    BucketName: str
    ObjectKey: str


class DomainTypeDef(TypedDict):
    Lifecycle: NotRequired[LifecycleManagementStrategyType]
    Name: NotRequired[str]


class LaunchOverridesTypeDef(TypedDict):
    LaunchCommands: NotRequired[Sequence[str]]


class ListAppsInputRequestTypeDef(TypedDict):
    Simulation: str
    Domain: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class SimulationAppMetadataTypeDef(TypedDict):
    Domain: NotRequired[str]
    Name: NotRequired[str]
    Simulation: NotRequired[str]
    Status: NotRequired[SimulationAppStatusType]
    TargetStatus: NotRequired[SimulationAppTargetStatusType]


class ListSimulationsInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class SimulationMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreationTime: NotRequired[datetime]
    Name: NotRequired[str]
    Status: NotRequired[SimulationStatusType]
    TargetStatus: NotRequired[SimulationTargetStatusType]


class ListTagsForResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str


class SimulationClockTypeDef(TypedDict):
    Status: NotRequired[ClockStatusType]
    TargetStatus: NotRequired[ClockTargetStatusType]


class SimulationAppPortMappingTypeDef(TypedDict):
    Actual: NotRequired[int]
    Declared: NotRequired[int]


class StartClockInputRequestTypeDef(TypedDict):
    Simulation: str


class StopAppInputRequestTypeDef(TypedDict):
    App: str
    Domain: str
    Simulation: str


class StopClockInputRequestTypeDef(TypedDict):
    Simulation: str


class StopSimulationInputRequestTypeDef(TypedDict):
    Simulation: str


class TagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class LogDestinationTypeDef(TypedDict):
    CloudWatchLogsLogGroup: NotRequired[CloudWatchLogsLogGroupTypeDef]


class CreateSnapshotInputRequestTypeDef(TypedDict):
    Destination: S3DestinationTypeDef
    Simulation: str


class ListTagsForResourceOutputTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class StartAppOutputTypeDef(TypedDict):
    Domain: str
    Name: str
    Simulation: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartSimulationOutputTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    ExecutionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartSimulationInputRequestTypeDef(TypedDict):
    Name: str
    RoleArn: str
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    MaximumDuration: NotRequired[str]
    SchemaS3Location: NotRequired[S3LocationTypeDef]
    SnapshotS3Location: NotRequired[S3LocationTypeDef]
    Tags: NotRequired[Mapping[str, str]]


class StartAppInputRequestTypeDef(TypedDict):
    Domain: str
    Name: str
    Simulation: str
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    LaunchOverrides: NotRequired[LaunchOverridesTypeDef]


class ListAppsOutputTypeDef(TypedDict):
    Apps: List[SimulationAppMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListSimulationsOutputTypeDef(TypedDict):
    Simulations: List[SimulationMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LiveSimulationStateTypeDef(TypedDict):
    Clocks: NotRequired[List[SimulationClockTypeDef]]
    Domains: NotRequired[List[DomainTypeDef]]


class SimulationAppEndpointInfoTypeDef(TypedDict):
    Address: NotRequired[str]
    IngressPortMappings: NotRequired[List[SimulationAppPortMappingTypeDef]]


class LoggingConfigurationTypeDef(TypedDict):
    Destinations: NotRequired[List[LogDestinationTypeDef]]


class DescribeAppOutputTypeDef(TypedDict):
    Description: str
    Domain: str
    EndpointInfo: SimulationAppEndpointInfoTypeDef
    LaunchOverrides: LaunchOverridesOutputTypeDef
    Name: str
    Simulation: str
    Status: SimulationAppStatusType
    TargetStatus: SimulationAppTargetStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSimulationOutputTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    Description: str
    ExecutionId: str
    LiveSimulationState: LiveSimulationStateTypeDef
    LoggingConfiguration: LoggingConfigurationTypeDef
    MaximumDuration: str
    Name: str
    RoleArn: str
    SchemaError: str
    SchemaS3Location: S3LocationTypeDef
    SnapshotS3Location: S3LocationTypeDef
    StartError: str
    Status: SimulationStatusType
    TargetStatus: SimulationTargetStatusType
    ResponseMetadata: ResponseMetadataTypeDef
