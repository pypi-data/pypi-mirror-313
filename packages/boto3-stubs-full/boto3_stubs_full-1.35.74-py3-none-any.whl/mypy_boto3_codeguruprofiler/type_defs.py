"""
Type annotations for codeguruprofiler service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguruprofiler/type_defs/)

Usage::

    ```python
    from mypy_boto3_codeguruprofiler.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AgentParameterFieldType,
    AggregationPeriodType,
    ComputePlatformType,
    FeedbackTypeType,
    MetadataFieldType,
    OrderByType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AddNotificationChannelsRequestRequestTypeDef",
    "AddNotificationChannelsResponseTypeDef",
    "AgentConfigurationTypeDef",
    "AgentOrchestrationConfigTypeDef",
    "AggregatedProfileTimeTypeDef",
    "AnomalyInstanceTypeDef",
    "AnomalyTypeDef",
    "BatchGetFrameMetricDataRequestRequestTypeDef",
    "BatchGetFrameMetricDataResponseTypeDef",
    "BlobTypeDef",
    "ChannelOutputTypeDef",
    "ChannelTypeDef",
    "ChannelUnionTypeDef",
    "ConfigureAgentRequestRequestTypeDef",
    "ConfigureAgentResponseTypeDef",
    "CreateProfilingGroupRequestRequestTypeDef",
    "CreateProfilingGroupResponseTypeDef",
    "DeleteProfilingGroupRequestRequestTypeDef",
    "DescribeProfilingGroupRequestRequestTypeDef",
    "DescribeProfilingGroupResponseTypeDef",
    "FindingsReportSummaryTypeDef",
    "FrameMetricDatumTypeDef",
    "FrameMetricOutputTypeDef",
    "FrameMetricTypeDef",
    "FrameMetricUnionTypeDef",
    "GetFindingsReportAccountSummaryRequestRequestTypeDef",
    "GetFindingsReportAccountSummaryResponseTypeDef",
    "GetNotificationConfigurationRequestRequestTypeDef",
    "GetNotificationConfigurationResponseTypeDef",
    "GetPolicyRequestRequestTypeDef",
    "GetPolicyResponseTypeDef",
    "GetProfileRequestRequestTypeDef",
    "GetProfileResponseTypeDef",
    "GetRecommendationsRequestRequestTypeDef",
    "GetRecommendationsResponseTypeDef",
    "ListFindingsReportsRequestRequestTypeDef",
    "ListFindingsReportsResponseTypeDef",
    "ListProfileTimesRequestListProfileTimesPaginateTypeDef",
    "ListProfileTimesRequestRequestTypeDef",
    "ListProfileTimesResponseTypeDef",
    "ListProfilingGroupsRequestRequestTypeDef",
    "ListProfilingGroupsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MatchTypeDef",
    "MetricTypeDef",
    "NotificationConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PatternTypeDef",
    "PostAgentProfileRequestRequestTypeDef",
    "ProfileTimeTypeDef",
    "ProfilingGroupDescriptionTypeDef",
    "ProfilingStatusTypeDef",
    "PutPermissionRequestRequestTypeDef",
    "PutPermissionResponseTypeDef",
    "RecommendationTypeDef",
    "RemoveNotificationChannelRequestRequestTypeDef",
    "RemoveNotificationChannelResponseTypeDef",
    "RemovePermissionRequestRequestTypeDef",
    "RemovePermissionResponseTypeDef",
    "ResponseMetadataTypeDef",
    "SubmitFeedbackRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimestampStructureTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateProfilingGroupRequestRequestTypeDef",
    "UpdateProfilingGroupResponseTypeDef",
    "UserFeedbackTypeDef",
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AgentConfigurationTypeDef(TypedDict):
    periodInSeconds: int
    shouldProfile: bool
    agentParameters: NotRequired[Dict[AgentParameterFieldType, str]]


class AgentOrchestrationConfigTypeDef(TypedDict):
    profilingEnabled: bool


class AggregatedProfileTimeTypeDef(TypedDict):
    period: NotRequired[AggregationPeriodType]
    start: NotRequired[datetime]


UserFeedbackTypeDef = TypedDict(
    "UserFeedbackTypeDef",
    {
        "type": FeedbackTypeType,
    },
)
MetricTypeDef = TypedDict(
    "MetricTypeDef",
    {
        "frameName": str,
        "threadStates": List[str],
        "type": Literal["AggregatedRelativeTotalTime"],
    },
)
TimestampTypeDef = Union[datetime, str]


class TimestampStructureTypeDef(TypedDict):
    value: datetime


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
ChannelOutputTypeDef = TypedDict(
    "ChannelOutputTypeDef",
    {
        "eventPublishers": List[Literal["AnomalyDetection"]],
        "uri": str,
        "id": NotRequired[str],
    },
)
ChannelTypeDef = TypedDict(
    "ChannelTypeDef",
    {
        "eventPublishers": Sequence[Literal["AnomalyDetection"]],
        "uri": str,
        "id": NotRequired[str],
    },
)


class ConfigureAgentRequestRequestTypeDef(TypedDict):
    profilingGroupName: str
    fleetInstanceId: NotRequired[str]
    metadata: NotRequired[Mapping[MetadataFieldType, str]]


class DeleteProfilingGroupRequestRequestTypeDef(TypedDict):
    profilingGroupName: str


class DescribeProfilingGroupRequestRequestTypeDef(TypedDict):
    profilingGroupName: str


FindingsReportSummaryTypeDef = TypedDict(
    "FindingsReportSummaryTypeDef",
    {
        "id": NotRequired[str],
        "profileEndTime": NotRequired[datetime],
        "profileStartTime": NotRequired[datetime],
        "profilingGroupName": NotRequired[str],
        "totalNumberOfFindings": NotRequired[int],
    },
)
FrameMetricOutputTypeDef = TypedDict(
    "FrameMetricOutputTypeDef",
    {
        "frameName": str,
        "threadStates": List[str],
        "type": Literal["AggregatedRelativeTotalTime"],
    },
)
FrameMetricTypeDef = TypedDict(
    "FrameMetricTypeDef",
    {
        "frameName": str,
        "threadStates": Sequence[str],
        "type": Literal["AggregatedRelativeTotalTime"],
    },
)


class GetFindingsReportAccountSummaryRequestRequestTypeDef(TypedDict):
    dailyReportsOnly: NotRequired[bool]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class GetNotificationConfigurationRequestRequestTypeDef(TypedDict):
    profilingGroupName: str


class GetPolicyRequestRequestTypeDef(TypedDict):
    profilingGroupName: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ProfileTimeTypeDef(TypedDict):
    start: NotRequired[datetime]


class ListProfilingGroupsRequestRequestTypeDef(TypedDict):
    includeDescription: NotRequired[bool]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class MatchTypeDef(TypedDict):
    frameAddress: NotRequired[str]
    targetFramesIndex: NotRequired[int]
    thresholdBreachValue: NotRequired[float]


PatternTypeDef = TypedDict(
    "PatternTypeDef",
    {
        "countersToAggregate": NotRequired[List[str]],
        "description": NotRequired[str],
        "id": NotRequired[str],
        "name": NotRequired[str],
        "resolutionSteps": NotRequired[str],
        "targetFrames": NotRequired[List[List[str]]],
        "thresholdPercent": NotRequired[float],
    },
)


class PutPermissionRequestRequestTypeDef(TypedDict):
    actionGroup: Literal["agentPermissions"]
    principals: Sequence[str]
    profilingGroupName: str
    revisionId: NotRequired[str]


class RemoveNotificationChannelRequestRequestTypeDef(TypedDict):
    channelId: str
    profilingGroupName: str


class RemovePermissionRequestRequestTypeDef(TypedDict):
    actionGroup: Literal["agentPermissions"]
    profilingGroupName: str
    revisionId: str


SubmitFeedbackRequestRequestTypeDef = TypedDict(
    "SubmitFeedbackRequestRequestTypeDef",
    {
        "anomalyInstanceId": str,
        "profilingGroupName": str,
        "type": FeedbackTypeType,
        "comment": NotRequired[str],
    },
)


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class GetPolicyResponseTypeDef(TypedDict):
    policy: str
    revisionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetProfileResponseTypeDef(TypedDict):
    contentEncoding: str
    contentType: str
    profile: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PutPermissionResponseTypeDef(TypedDict):
    policy: str
    revisionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class RemovePermissionResponseTypeDef(TypedDict):
    policy: str
    revisionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ConfigureAgentResponseTypeDef(TypedDict):
    configuration: AgentConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProfilingGroupRequestRequestTypeDef(TypedDict):
    clientToken: str
    profilingGroupName: str
    agentOrchestrationConfig: NotRequired[AgentOrchestrationConfigTypeDef]
    computePlatform: NotRequired[ComputePlatformType]
    tags: NotRequired[Mapping[str, str]]


class UpdateProfilingGroupRequestRequestTypeDef(TypedDict):
    agentOrchestrationConfig: AgentOrchestrationConfigTypeDef
    profilingGroupName: str


class ProfilingStatusTypeDef(TypedDict):
    latestAgentOrchestratedAt: NotRequired[datetime]
    latestAgentProfileReportedAt: NotRequired[datetime]
    latestAggregatedProfile: NotRequired[AggregatedProfileTimeTypeDef]


AnomalyInstanceTypeDef = TypedDict(
    "AnomalyInstanceTypeDef",
    {
        "id": str,
        "startTime": datetime,
        "endTime": NotRequired[datetime],
        "userFeedback": NotRequired[UserFeedbackTypeDef],
    },
)


class GetProfileRequestRequestTypeDef(TypedDict):
    profilingGroupName: str
    accept: NotRequired[str]
    endTime: NotRequired[TimestampTypeDef]
    maxDepth: NotRequired[int]
    period: NotRequired[str]
    startTime: NotRequired[TimestampTypeDef]


class GetRecommendationsRequestRequestTypeDef(TypedDict):
    endTime: TimestampTypeDef
    profilingGroupName: str
    startTime: TimestampTypeDef
    locale: NotRequired[str]


class ListFindingsReportsRequestRequestTypeDef(TypedDict):
    endTime: TimestampTypeDef
    profilingGroupName: str
    startTime: TimestampTypeDef
    dailyReportsOnly: NotRequired[bool]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListProfileTimesRequestRequestTypeDef(TypedDict):
    endTime: TimestampTypeDef
    period: AggregationPeriodType
    profilingGroupName: str
    startTime: TimestampTypeDef
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    orderBy: NotRequired[OrderByType]


class PostAgentProfileRequestRequestTypeDef(TypedDict):
    agentProfile: BlobTypeDef
    contentType: str
    profilingGroupName: str
    profileToken: NotRequired[str]


class NotificationConfigurationTypeDef(TypedDict):
    channels: NotRequired[List[ChannelOutputTypeDef]]


ChannelUnionTypeDef = Union[ChannelTypeDef, ChannelOutputTypeDef]


class GetFindingsReportAccountSummaryResponseTypeDef(TypedDict):
    reportSummaries: List[FindingsReportSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListFindingsReportsResponseTypeDef(TypedDict):
    findingsReportSummaries: List[FindingsReportSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class FrameMetricDatumTypeDef(TypedDict):
    frameMetric: FrameMetricOutputTypeDef
    values: List[float]


FrameMetricUnionTypeDef = Union[FrameMetricTypeDef, FrameMetricOutputTypeDef]


class ListProfileTimesRequestListProfileTimesPaginateTypeDef(TypedDict):
    endTime: TimestampTypeDef
    period: AggregationPeriodType
    profilingGroupName: str
    startTime: TimestampTypeDef
    orderBy: NotRequired[OrderByType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProfileTimesResponseTypeDef(TypedDict):
    profileTimes: List[ProfileTimeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class RecommendationTypeDef(TypedDict):
    allMatchesCount: int
    allMatchesSum: float
    endTime: datetime
    pattern: PatternTypeDef
    startTime: datetime
    topMatches: List[MatchTypeDef]


class ProfilingGroupDescriptionTypeDef(TypedDict):
    agentOrchestrationConfig: NotRequired[AgentOrchestrationConfigTypeDef]
    arn: NotRequired[str]
    computePlatform: NotRequired[ComputePlatformType]
    createdAt: NotRequired[datetime]
    name: NotRequired[str]
    profilingStatus: NotRequired[ProfilingStatusTypeDef]
    tags: NotRequired[Dict[str, str]]
    updatedAt: NotRequired[datetime]


class AnomalyTypeDef(TypedDict):
    instances: List[AnomalyInstanceTypeDef]
    metric: MetricTypeDef
    reason: str


class AddNotificationChannelsResponseTypeDef(TypedDict):
    notificationConfiguration: NotificationConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetNotificationConfigurationResponseTypeDef(TypedDict):
    notificationConfiguration: NotificationConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RemoveNotificationChannelResponseTypeDef(TypedDict):
    notificationConfiguration: NotificationConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AddNotificationChannelsRequestRequestTypeDef(TypedDict):
    channels: Sequence[ChannelUnionTypeDef]
    profilingGroupName: str


class BatchGetFrameMetricDataResponseTypeDef(TypedDict):
    endTime: datetime
    endTimes: List[TimestampStructureTypeDef]
    frameMetricData: List[FrameMetricDatumTypeDef]
    resolution: AggregationPeriodType
    startTime: datetime
    unprocessedEndTimes: Dict[str, List[TimestampStructureTypeDef]]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchGetFrameMetricDataRequestRequestTypeDef(TypedDict):
    profilingGroupName: str
    endTime: NotRequired[TimestampTypeDef]
    frameMetrics: NotRequired[Sequence[FrameMetricUnionTypeDef]]
    period: NotRequired[str]
    startTime: NotRequired[TimestampTypeDef]
    targetResolution: NotRequired[AggregationPeriodType]


class CreateProfilingGroupResponseTypeDef(TypedDict):
    profilingGroup: ProfilingGroupDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeProfilingGroupResponseTypeDef(TypedDict):
    profilingGroup: ProfilingGroupDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListProfilingGroupsResponseTypeDef(TypedDict):
    profilingGroupNames: List[str]
    profilingGroups: List[ProfilingGroupDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateProfilingGroupResponseTypeDef(TypedDict):
    profilingGroup: ProfilingGroupDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetRecommendationsResponseTypeDef(TypedDict):
    anomalies: List[AnomalyTypeDef]
    profileEndTime: datetime
    profileStartTime: datetime
    profilingGroupName: str
    recommendations: List[RecommendationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
