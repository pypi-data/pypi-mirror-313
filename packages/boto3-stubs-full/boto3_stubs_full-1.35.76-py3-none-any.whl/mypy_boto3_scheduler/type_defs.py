"""
Type annotations for scheduler service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/type_defs/)

Usage::

    ```python
    from mypy_boto3_scheduler.type_defs import AwsVpcConfigurationOutputTypeDef

    data: AwsVpcConfigurationOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ActionAfterCompletionType,
    AssignPublicIpType,
    FlexibleTimeWindowModeType,
    LaunchTypeType,
    PlacementConstraintTypeType,
    PlacementStrategyTypeType,
    ScheduleGroupStateType,
    ScheduleStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AwsVpcConfigurationOutputTypeDef",
    "AwsVpcConfigurationTypeDef",
    "AwsVpcConfigurationUnionTypeDef",
    "CapacityProviderStrategyItemTypeDef",
    "CreateScheduleGroupInputRequestTypeDef",
    "CreateScheduleGroupOutputTypeDef",
    "CreateScheduleInputRequestTypeDef",
    "CreateScheduleOutputTypeDef",
    "DeadLetterConfigTypeDef",
    "DeleteScheduleGroupInputRequestTypeDef",
    "DeleteScheduleInputRequestTypeDef",
    "EcsParametersOutputTypeDef",
    "EcsParametersTypeDef",
    "EcsParametersUnionTypeDef",
    "EventBridgeParametersTypeDef",
    "FlexibleTimeWindowTypeDef",
    "GetScheduleGroupInputRequestTypeDef",
    "GetScheduleGroupOutputTypeDef",
    "GetScheduleInputRequestTypeDef",
    "GetScheduleOutputTypeDef",
    "KinesisParametersTypeDef",
    "ListScheduleGroupsInputListScheduleGroupsPaginateTypeDef",
    "ListScheduleGroupsInputRequestTypeDef",
    "ListScheduleGroupsOutputTypeDef",
    "ListSchedulesInputListSchedulesPaginateTypeDef",
    "ListSchedulesInputRequestTypeDef",
    "ListSchedulesOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "NetworkConfigurationOutputTypeDef",
    "NetworkConfigurationTypeDef",
    "NetworkConfigurationUnionTypeDef",
    "PaginatorConfigTypeDef",
    "PlacementConstraintTypeDef",
    "PlacementStrategyTypeDef",
    "ResponseMetadataTypeDef",
    "RetryPolicyTypeDef",
    "SageMakerPipelineParameterTypeDef",
    "SageMakerPipelineParametersOutputTypeDef",
    "SageMakerPipelineParametersTypeDef",
    "SageMakerPipelineParametersUnionTypeDef",
    "ScheduleGroupSummaryTypeDef",
    "ScheduleSummaryTypeDef",
    "SqsParametersTypeDef",
    "TagResourceInputRequestTypeDef",
    "TagTypeDef",
    "TargetOutputTypeDef",
    "TargetSummaryTypeDef",
    "TargetTypeDef",
    "TimestampTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateScheduleInputRequestTypeDef",
    "UpdateScheduleOutputTypeDef",
)


class AwsVpcConfigurationOutputTypeDef(TypedDict):
    Subnets: List[str]
    AssignPublicIp: NotRequired[AssignPublicIpType]
    SecurityGroups: NotRequired[List[str]]


class AwsVpcConfigurationTypeDef(TypedDict):
    Subnets: Sequence[str]
    AssignPublicIp: NotRequired[AssignPublicIpType]
    SecurityGroups: NotRequired[Sequence[str]]


class CapacityProviderStrategyItemTypeDef(TypedDict):
    capacityProvider: str
    base: NotRequired[int]
    weight: NotRequired[int]


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class FlexibleTimeWindowTypeDef(TypedDict):
    Mode: FlexibleTimeWindowModeType
    MaximumWindowInMinutes: NotRequired[int]


TimestampTypeDef = Union[datetime, str]


class DeadLetterConfigTypeDef(TypedDict):
    Arn: NotRequired[str]


class DeleteScheduleGroupInputRequestTypeDef(TypedDict):
    Name: str
    ClientToken: NotRequired[str]


class DeleteScheduleInputRequestTypeDef(TypedDict):
    Name: str
    ClientToken: NotRequired[str]
    GroupName: NotRequired[str]


PlacementConstraintTypeDef = TypedDict(
    "PlacementConstraintTypeDef",
    {
        "expression": NotRequired[str],
        "type": NotRequired[PlacementConstraintTypeType],
    },
)
PlacementStrategyTypeDef = TypedDict(
    "PlacementStrategyTypeDef",
    {
        "field": NotRequired[str],
        "type": NotRequired[PlacementStrategyTypeType],
    },
)


class EventBridgeParametersTypeDef(TypedDict):
    DetailType: str
    Source: str


class GetScheduleGroupInputRequestTypeDef(TypedDict):
    Name: str


class GetScheduleInputRequestTypeDef(TypedDict):
    Name: str
    GroupName: NotRequired[str]


class KinesisParametersTypeDef(TypedDict):
    PartitionKey: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListScheduleGroupsInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NamePrefix: NotRequired[str]
    NextToken: NotRequired[str]


class ScheduleGroupSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreationDate: NotRequired[datetime]
    LastModificationDate: NotRequired[datetime]
    Name: NotRequired[str]
    State: NotRequired[ScheduleGroupStateType]


class ListSchedulesInputRequestTypeDef(TypedDict):
    GroupName: NotRequired[str]
    MaxResults: NotRequired[int]
    NamePrefix: NotRequired[str]
    NextToken: NotRequired[str]
    State: NotRequired[ScheduleStateType]


class ListTagsForResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str


class RetryPolicyTypeDef(TypedDict):
    MaximumEventAgeInSeconds: NotRequired[int]
    MaximumRetryAttempts: NotRequired[int]


class SageMakerPipelineParameterTypeDef(TypedDict):
    Name: str
    Value: str


class TargetSummaryTypeDef(TypedDict):
    Arn: str


class SqsParametersTypeDef(TypedDict):
    MessageGroupId: NotRequired[str]


class UntagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class NetworkConfigurationOutputTypeDef(TypedDict):
    awsvpcConfiguration: NotRequired[AwsVpcConfigurationOutputTypeDef]


AwsVpcConfigurationUnionTypeDef = Union[
    AwsVpcConfigurationTypeDef, AwsVpcConfigurationOutputTypeDef
]


class CreateScheduleGroupInputRequestTypeDef(TypedDict):
    Name: str
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class TagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]


class CreateScheduleGroupOutputTypeDef(TypedDict):
    ScheduleGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateScheduleOutputTypeDef(TypedDict):
    ScheduleArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetScheduleGroupOutputTypeDef(TypedDict):
    Arn: str
    CreationDate: datetime
    LastModificationDate: datetime
    Name: str
    State: ScheduleGroupStateType
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceOutputTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateScheduleOutputTypeDef(TypedDict):
    ScheduleArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListScheduleGroupsInputListScheduleGroupsPaginateTypeDef(TypedDict):
    NamePrefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSchedulesInputListSchedulesPaginateTypeDef(TypedDict):
    GroupName: NotRequired[str]
    NamePrefix: NotRequired[str]
    State: NotRequired[ScheduleStateType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListScheduleGroupsOutputTypeDef(TypedDict):
    ScheduleGroups: List[ScheduleGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SageMakerPipelineParametersOutputTypeDef(TypedDict):
    PipelineParameterList: NotRequired[List[SageMakerPipelineParameterTypeDef]]


class SageMakerPipelineParametersTypeDef(TypedDict):
    PipelineParameterList: NotRequired[Sequence[SageMakerPipelineParameterTypeDef]]


class ScheduleSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreationDate: NotRequired[datetime]
    GroupName: NotRequired[str]
    LastModificationDate: NotRequired[datetime]
    Name: NotRequired[str]
    State: NotRequired[ScheduleStateType]
    Target: NotRequired[TargetSummaryTypeDef]


class EcsParametersOutputTypeDef(TypedDict):
    TaskDefinitionArn: str
    CapacityProviderStrategy: NotRequired[List[CapacityProviderStrategyItemTypeDef]]
    EnableECSManagedTags: NotRequired[bool]
    EnableExecuteCommand: NotRequired[bool]
    Group: NotRequired[str]
    LaunchType: NotRequired[LaunchTypeType]
    NetworkConfiguration: NotRequired[NetworkConfigurationOutputTypeDef]
    PlacementConstraints: NotRequired[List[PlacementConstraintTypeDef]]
    PlacementStrategy: NotRequired[List[PlacementStrategyTypeDef]]
    PlatformVersion: NotRequired[str]
    PropagateTags: NotRequired[Literal["TASK_DEFINITION"]]
    ReferenceId: NotRequired[str]
    Tags: NotRequired[List[Dict[str, str]]]
    TaskCount: NotRequired[int]


class NetworkConfigurationTypeDef(TypedDict):
    awsvpcConfiguration: NotRequired[AwsVpcConfigurationUnionTypeDef]


SageMakerPipelineParametersUnionTypeDef = Union[
    SageMakerPipelineParametersTypeDef, SageMakerPipelineParametersOutputTypeDef
]


class ListSchedulesOutputTypeDef(TypedDict):
    Schedules: List[ScheduleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TargetOutputTypeDef(TypedDict):
    Arn: str
    RoleArn: str
    DeadLetterConfig: NotRequired[DeadLetterConfigTypeDef]
    EcsParameters: NotRequired[EcsParametersOutputTypeDef]
    EventBridgeParameters: NotRequired[EventBridgeParametersTypeDef]
    Input: NotRequired[str]
    KinesisParameters: NotRequired[KinesisParametersTypeDef]
    RetryPolicy: NotRequired[RetryPolicyTypeDef]
    SageMakerPipelineParameters: NotRequired[SageMakerPipelineParametersOutputTypeDef]
    SqsParameters: NotRequired[SqsParametersTypeDef]


NetworkConfigurationUnionTypeDef = Union[
    NetworkConfigurationTypeDef, NetworkConfigurationOutputTypeDef
]


class GetScheduleOutputTypeDef(TypedDict):
    ActionAfterCompletion: ActionAfterCompletionType
    Arn: str
    CreationDate: datetime
    Description: str
    EndDate: datetime
    FlexibleTimeWindow: FlexibleTimeWindowTypeDef
    GroupName: str
    KmsKeyArn: str
    LastModificationDate: datetime
    Name: str
    ScheduleExpression: str
    ScheduleExpressionTimezone: str
    StartDate: datetime
    State: ScheduleStateType
    Target: TargetOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class EcsParametersTypeDef(TypedDict):
    TaskDefinitionArn: str
    CapacityProviderStrategy: NotRequired[Sequence[CapacityProviderStrategyItemTypeDef]]
    EnableECSManagedTags: NotRequired[bool]
    EnableExecuteCommand: NotRequired[bool]
    Group: NotRequired[str]
    LaunchType: NotRequired[LaunchTypeType]
    NetworkConfiguration: NotRequired[NetworkConfigurationUnionTypeDef]
    PlacementConstraints: NotRequired[Sequence[PlacementConstraintTypeDef]]
    PlacementStrategy: NotRequired[Sequence[PlacementStrategyTypeDef]]
    PlatformVersion: NotRequired[str]
    PropagateTags: NotRequired[Literal["TASK_DEFINITION"]]
    ReferenceId: NotRequired[str]
    Tags: NotRequired[Sequence[Mapping[str, str]]]
    TaskCount: NotRequired[int]


EcsParametersUnionTypeDef = Union[EcsParametersTypeDef, EcsParametersOutputTypeDef]


class TargetTypeDef(TypedDict):
    Arn: str
    RoleArn: str
    DeadLetterConfig: NotRequired[DeadLetterConfigTypeDef]
    EcsParameters: NotRequired[EcsParametersUnionTypeDef]
    EventBridgeParameters: NotRequired[EventBridgeParametersTypeDef]
    Input: NotRequired[str]
    KinesisParameters: NotRequired[KinesisParametersTypeDef]
    RetryPolicy: NotRequired[RetryPolicyTypeDef]
    SageMakerPipelineParameters: NotRequired[SageMakerPipelineParametersUnionTypeDef]
    SqsParameters: NotRequired[SqsParametersTypeDef]


class CreateScheduleInputRequestTypeDef(TypedDict):
    FlexibleTimeWindow: FlexibleTimeWindowTypeDef
    Name: str
    ScheduleExpression: str
    Target: TargetTypeDef
    ActionAfterCompletion: NotRequired[ActionAfterCompletionType]
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    EndDate: NotRequired[TimestampTypeDef]
    GroupName: NotRequired[str]
    KmsKeyArn: NotRequired[str]
    ScheduleExpressionTimezone: NotRequired[str]
    StartDate: NotRequired[TimestampTypeDef]
    State: NotRequired[ScheduleStateType]


class UpdateScheduleInputRequestTypeDef(TypedDict):
    FlexibleTimeWindow: FlexibleTimeWindowTypeDef
    Name: str
    ScheduleExpression: str
    Target: TargetTypeDef
    ActionAfterCompletion: NotRequired[ActionAfterCompletionType]
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    EndDate: NotRequired[TimestampTypeDef]
    GroupName: NotRequired[str]
    KmsKeyArn: NotRequired[str]
    ScheduleExpressionTimezone: NotRequired[str]
    StartDate: NotRequired[TimestampTypeDef]
    State: NotRequired[ScheduleStateType]
