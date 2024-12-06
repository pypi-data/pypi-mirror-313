"""
Type annotations for application-insights service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_insights/type_defs/)

Usage::

    ```python
    from mypy_boto3_application_insights.type_defs import WorkloadConfigurationTypeDef

    data: WorkloadConfigurationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    CloudWatchEventSourceType,
    ConfigurationEventResourceTypeType,
    ConfigurationEventStatusType,
    DiscoveryTypeType,
    FeedbackValueType,
    LogFilterType,
    OsTypeType,
    RecommendationTypeType,
    ResolutionMethodType,
    SeverityLevelType,
    StatusType,
    TierType,
    VisibilityType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AddWorkloadRequestRequestTypeDef",
    "AddWorkloadResponseTypeDef",
    "ApplicationComponentTypeDef",
    "ApplicationInfoTypeDef",
    "ConfigurationEventTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateComponentRequestRequestTypeDef",
    "CreateLogPatternRequestRequestTypeDef",
    "CreateLogPatternResponseTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteComponentRequestRequestTypeDef",
    "DeleteLogPatternRequestRequestTypeDef",
    "DescribeApplicationRequestRequestTypeDef",
    "DescribeApplicationResponseTypeDef",
    "DescribeComponentConfigurationRecommendationRequestRequestTypeDef",
    "DescribeComponentConfigurationRecommendationResponseTypeDef",
    "DescribeComponentConfigurationRequestRequestTypeDef",
    "DescribeComponentConfigurationResponseTypeDef",
    "DescribeComponentRequestRequestTypeDef",
    "DescribeComponentResponseTypeDef",
    "DescribeLogPatternRequestRequestTypeDef",
    "DescribeLogPatternResponseTypeDef",
    "DescribeObservationRequestRequestTypeDef",
    "DescribeObservationResponseTypeDef",
    "DescribeProblemObservationsRequestRequestTypeDef",
    "DescribeProblemObservationsResponseTypeDef",
    "DescribeProblemRequestRequestTypeDef",
    "DescribeProblemResponseTypeDef",
    "DescribeWorkloadRequestRequestTypeDef",
    "DescribeWorkloadResponseTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListComponentsRequestRequestTypeDef",
    "ListComponentsResponseTypeDef",
    "ListConfigurationHistoryRequestRequestTypeDef",
    "ListConfigurationHistoryResponseTypeDef",
    "ListLogPatternSetsRequestRequestTypeDef",
    "ListLogPatternSetsResponseTypeDef",
    "ListLogPatternsRequestRequestTypeDef",
    "ListLogPatternsResponseTypeDef",
    "ListProblemsRequestRequestTypeDef",
    "ListProblemsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListWorkloadsRequestRequestTypeDef",
    "ListWorkloadsResponseTypeDef",
    "LogPatternTypeDef",
    "ObservationTypeDef",
    "ProblemTypeDef",
    "RelatedObservationsTypeDef",
    "RemoveWorkloadRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateApplicationResponseTypeDef",
    "UpdateComponentConfigurationRequestRequestTypeDef",
    "UpdateComponentRequestRequestTypeDef",
    "UpdateLogPatternRequestRequestTypeDef",
    "UpdateLogPatternResponseTypeDef",
    "UpdateProblemRequestRequestTypeDef",
    "UpdateWorkloadRequestRequestTypeDef",
    "UpdateWorkloadResponseTypeDef",
    "WorkloadConfigurationTypeDef",
    "WorkloadTypeDef",
)

class WorkloadConfigurationTypeDef(TypedDict):
    WorkloadName: NotRequired[str]
    Tier: NotRequired[TierType]
    Configuration: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ApplicationComponentTypeDef(TypedDict):
    ComponentName: NotRequired[str]
    ComponentRemarks: NotRequired[str]
    ResourceType: NotRequired[str]
    OsType: NotRequired[OsTypeType]
    Tier: NotRequired[TierType]
    Monitor: NotRequired[bool]
    DetectedWorkload: NotRequired[Dict[TierType, Dict[str, str]]]

class ApplicationInfoTypeDef(TypedDict):
    AccountId: NotRequired[str]
    ResourceGroupName: NotRequired[str]
    LifeCycle: NotRequired[str]
    OpsItemSNSTopicArn: NotRequired[str]
    SNSNotificationArn: NotRequired[str]
    OpsCenterEnabled: NotRequired[bool]
    CWEMonitorEnabled: NotRequired[bool]
    Remarks: NotRequired[str]
    AutoConfigEnabled: NotRequired[bool]
    DiscoveryType: NotRequired[DiscoveryTypeType]
    AttachMissingPermission: NotRequired[bool]

class ConfigurationEventTypeDef(TypedDict):
    ResourceGroupName: NotRequired[str]
    AccountId: NotRequired[str]
    MonitoredResourceARN: NotRequired[str]
    EventStatus: NotRequired[ConfigurationEventStatusType]
    EventResourceType: NotRequired[ConfigurationEventResourceTypeType]
    EventTime: NotRequired[datetime]
    EventDetail: NotRequired[str]
    EventResourceName: NotRequired[str]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class CreateComponentRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    ComponentName: str
    ResourceList: Sequence[str]

class CreateLogPatternRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    PatternSetName: str
    PatternName: str
    Pattern: str
    Rank: int

class LogPatternTypeDef(TypedDict):
    PatternSetName: NotRequired[str]
    PatternName: NotRequired[str]
    Pattern: NotRequired[str]
    Rank: NotRequired[int]

class DeleteApplicationRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str

class DeleteComponentRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    ComponentName: str

class DeleteLogPatternRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    PatternSetName: str
    PatternName: str

class DescribeApplicationRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    AccountId: NotRequired[str]

class DescribeComponentConfigurationRecommendationRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    ComponentName: str
    Tier: TierType
    WorkloadName: NotRequired[str]
    RecommendationType: NotRequired[RecommendationTypeType]

class DescribeComponentConfigurationRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    ComponentName: str
    AccountId: NotRequired[str]

class DescribeComponentRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    ComponentName: str
    AccountId: NotRequired[str]

class DescribeLogPatternRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    PatternSetName: str
    PatternName: str
    AccountId: NotRequired[str]

class DescribeObservationRequestRequestTypeDef(TypedDict):
    ObservationId: str
    AccountId: NotRequired[str]

class ObservationTypeDef(TypedDict):
    Id: NotRequired[str]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    SourceType: NotRequired[str]
    SourceARN: NotRequired[str]
    LogGroup: NotRequired[str]
    LineTime: NotRequired[datetime]
    LogText: NotRequired[str]
    LogFilter: NotRequired[LogFilterType]
    MetricNamespace: NotRequired[str]
    MetricName: NotRequired[str]
    Unit: NotRequired[str]
    Value: NotRequired[float]
    CloudWatchEventId: NotRequired[str]
    CloudWatchEventSource: NotRequired[CloudWatchEventSourceType]
    CloudWatchEventDetailType: NotRequired[str]
    HealthEventArn: NotRequired[str]
    HealthService: NotRequired[str]
    HealthEventTypeCode: NotRequired[str]
    HealthEventTypeCategory: NotRequired[str]
    HealthEventDescription: NotRequired[str]
    CodeDeployDeploymentId: NotRequired[str]
    CodeDeployDeploymentGroup: NotRequired[str]
    CodeDeployState: NotRequired[str]
    CodeDeployApplication: NotRequired[str]
    CodeDeployInstanceGroupId: NotRequired[str]
    Ec2State: NotRequired[str]
    RdsEventCategories: NotRequired[str]
    RdsEventMessage: NotRequired[str]
    S3EventName: NotRequired[str]
    StatesExecutionArn: NotRequired[str]
    StatesArn: NotRequired[str]
    StatesStatus: NotRequired[str]
    StatesInput: NotRequired[str]
    EbsEvent: NotRequired[str]
    EbsResult: NotRequired[str]
    EbsCause: NotRequired[str]
    EbsRequestId: NotRequired[str]
    XRayFaultPercent: NotRequired[int]
    XRayThrottlePercent: NotRequired[int]
    XRayErrorPercent: NotRequired[int]
    XRayRequestCount: NotRequired[int]
    XRayRequestAverageLatency: NotRequired[int]
    XRayNodeName: NotRequired[str]
    XRayNodeType: NotRequired[str]

class DescribeProblemObservationsRequestRequestTypeDef(TypedDict):
    ProblemId: str
    AccountId: NotRequired[str]

class DescribeProblemRequestRequestTypeDef(TypedDict):
    ProblemId: str
    AccountId: NotRequired[str]

class ProblemTypeDef(TypedDict):
    Id: NotRequired[str]
    Title: NotRequired[str]
    ShortName: NotRequired[str]
    Insights: NotRequired[str]
    Status: NotRequired[StatusType]
    AffectedResource: NotRequired[str]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    SeverityLevel: NotRequired[SeverityLevelType]
    AccountId: NotRequired[str]
    ResourceGroupName: NotRequired[str]
    Feedback: NotRequired[Dict[Literal["INSIGHTS_FEEDBACK"], FeedbackValueType]]
    RecurringCount: NotRequired[int]
    LastRecurrenceTime: NotRequired[datetime]
    Visibility: NotRequired[VisibilityType]
    ResolutionMethod: NotRequired[ResolutionMethodType]

class DescribeWorkloadRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    ComponentName: str
    WorkloadId: str
    AccountId: NotRequired[str]

class ListApplicationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    AccountId: NotRequired[str]

class ListComponentsRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    AccountId: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class ListLogPatternSetsRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    AccountId: NotRequired[str]

class ListLogPatternsRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    PatternSetName: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    AccountId: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str

class ListWorkloadsRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    ComponentName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    AccountId: NotRequired[str]

class WorkloadTypeDef(TypedDict):
    WorkloadId: NotRequired[str]
    ComponentName: NotRequired[str]
    WorkloadName: NotRequired[str]
    Tier: NotRequired[TierType]
    WorkloadRemarks: NotRequired[str]
    MissingWorkloadConfig: NotRequired[bool]

class RemoveWorkloadRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    ComponentName: str
    WorkloadId: str

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]

class UpdateApplicationRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    OpsCenterEnabled: NotRequired[bool]
    CWEMonitorEnabled: NotRequired[bool]
    OpsItemSNSTopicArn: NotRequired[str]
    SNSNotificationArn: NotRequired[str]
    RemoveSNSTopic: NotRequired[bool]
    AutoConfigEnabled: NotRequired[bool]
    AttachMissingPermission: NotRequired[bool]

class UpdateComponentConfigurationRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    ComponentName: str
    Monitor: NotRequired[bool]
    Tier: NotRequired[TierType]
    ComponentConfiguration: NotRequired[str]
    AutoConfigEnabled: NotRequired[bool]

class UpdateComponentRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    ComponentName: str
    NewComponentName: NotRequired[str]
    ResourceList: NotRequired[Sequence[str]]

class UpdateLogPatternRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    PatternSetName: str
    PatternName: str
    Pattern: NotRequired[str]
    Rank: NotRequired[int]

class UpdateProblemRequestRequestTypeDef(TypedDict):
    ProblemId: str
    UpdateStatus: NotRequired[Literal["RESOLVED"]]
    Visibility: NotRequired[VisibilityType]

class AddWorkloadRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    ComponentName: str
    WorkloadConfiguration: WorkloadConfigurationTypeDef

class UpdateWorkloadRequestRequestTypeDef(TypedDict):
    ResourceGroupName: str
    ComponentName: str
    WorkloadConfiguration: WorkloadConfigurationTypeDef
    WorkloadId: NotRequired[str]

class AddWorkloadResponseTypeDef(TypedDict):
    WorkloadId: str
    WorkloadConfiguration: WorkloadConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeComponentConfigurationRecommendationResponseTypeDef(TypedDict):
    ComponentConfiguration: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeComponentConfigurationResponseTypeDef(TypedDict):
    Monitor: bool
    Tier: TierType
    ComponentConfiguration: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeWorkloadResponseTypeDef(TypedDict):
    WorkloadId: str
    WorkloadRemarks: str
    WorkloadConfiguration: WorkloadConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListLogPatternSetsResponseTypeDef(TypedDict):
    ResourceGroupName: str
    AccountId: str
    LogPatternSets: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateWorkloadResponseTypeDef(TypedDict):
    WorkloadId: str
    WorkloadConfiguration: WorkloadConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeComponentResponseTypeDef(TypedDict):
    ApplicationComponent: ApplicationComponentTypeDef
    ResourceList: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListComponentsResponseTypeDef(TypedDict):
    ApplicationComponentList: List[ApplicationComponentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateApplicationResponseTypeDef(TypedDict):
    ApplicationInfo: ApplicationInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeApplicationResponseTypeDef(TypedDict):
    ApplicationInfo: ApplicationInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListApplicationsResponseTypeDef(TypedDict):
    ApplicationInfoList: List[ApplicationInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateApplicationResponseTypeDef(TypedDict):
    ApplicationInfo: ApplicationInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListConfigurationHistoryResponseTypeDef(TypedDict):
    EventList: List[ConfigurationEventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateApplicationRequestRequestTypeDef(TypedDict):
    ResourceGroupName: NotRequired[str]
    OpsCenterEnabled: NotRequired[bool]
    CWEMonitorEnabled: NotRequired[bool]
    OpsItemSNSTopicArn: NotRequired[str]
    SNSNotificationArn: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    AutoConfigEnabled: NotRequired[bool]
    AutoCreate: NotRequired[bool]
    GroupingType: NotRequired[Literal["ACCOUNT_BASED"]]
    AttachMissingPermission: NotRequired[bool]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]

class CreateLogPatternResponseTypeDef(TypedDict):
    LogPattern: LogPatternTypeDef
    ResourceGroupName: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeLogPatternResponseTypeDef(TypedDict):
    ResourceGroupName: str
    AccountId: str
    LogPattern: LogPatternTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListLogPatternsResponseTypeDef(TypedDict):
    ResourceGroupName: str
    AccountId: str
    LogPatterns: List[LogPatternTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateLogPatternResponseTypeDef(TypedDict):
    ResourceGroupName: str
    LogPattern: LogPatternTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeObservationResponseTypeDef(TypedDict):
    Observation: ObservationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class RelatedObservationsTypeDef(TypedDict):
    ObservationList: NotRequired[List[ObservationTypeDef]]

class DescribeProblemResponseTypeDef(TypedDict):
    Problem: ProblemTypeDef
    SNSNotificationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListProblemsResponseTypeDef(TypedDict):
    ProblemList: List[ProblemTypeDef]
    ResourceGroupName: str
    AccountId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListConfigurationHistoryRequestRequestTypeDef(TypedDict):
    ResourceGroupName: NotRequired[str]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    EventStatus: NotRequired[ConfigurationEventStatusType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    AccountId: NotRequired[str]

class ListProblemsRequestRequestTypeDef(TypedDict):
    AccountId: NotRequired[str]
    ResourceGroupName: NotRequired[str]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ComponentName: NotRequired[str]
    Visibility: NotRequired[VisibilityType]

class ListWorkloadsResponseTypeDef(TypedDict):
    WorkloadList: List[WorkloadTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeProblemObservationsResponseTypeDef(TypedDict):
    RelatedObservations: RelatedObservationsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
