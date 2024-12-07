"""
Type annotations for evidently service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/type_defs/)

Usage::

    ```python
    from mypy_boto3_evidently.type_defs import EvaluationRequestTypeDef

    data: EvaluationRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ChangeDirectionEnumType,
    EventTypeType,
    ExperimentResultRequestTypeType,
    ExperimentResultResponseTypeType,
    ExperimentStatusType,
    ExperimentStopDesiredStateType,
    FeatureEvaluationStrategyType,
    FeatureStatusType,
    LaunchStatusType,
    LaunchStopDesiredStateType,
    ProjectStatusType,
    SegmentReferenceResourceTypeType,
    VariationValueTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "BatchEvaluateFeatureRequestRequestTypeDef",
    "BatchEvaluateFeatureResponseTypeDef",
    "CloudWatchLogsDestinationConfigTypeDef",
    "CloudWatchLogsDestinationTypeDef",
    "CreateExperimentRequestRequestTypeDef",
    "CreateExperimentResponseTypeDef",
    "CreateFeatureRequestRequestTypeDef",
    "CreateFeatureResponseTypeDef",
    "CreateLaunchRequestRequestTypeDef",
    "CreateLaunchResponseTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "CreateProjectResponseTypeDef",
    "CreateSegmentRequestRequestTypeDef",
    "CreateSegmentResponseTypeDef",
    "DeleteExperimentRequestRequestTypeDef",
    "DeleteFeatureRequestRequestTypeDef",
    "DeleteLaunchRequestRequestTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DeleteSegmentRequestRequestTypeDef",
    "EvaluateFeatureRequestRequestTypeDef",
    "EvaluateFeatureResponseTypeDef",
    "EvaluationRequestTypeDef",
    "EvaluationResultTypeDef",
    "EvaluationRuleTypeDef",
    "EventTypeDef",
    "ExperimentExecutionTypeDef",
    "ExperimentReportTypeDef",
    "ExperimentResultsDataTypeDef",
    "ExperimentScheduleTypeDef",
    "ExperimentTypeDef",
    "FeatureSummaryTypeDef",
    "FeatureTypeDef",
    "GetExperimentRequestRequestTypeDef",
    "GetExperimentResponseTypeDef",
    "GetExperimentResultsRequestRequestTypeDef",
    "GetExperimentResultsResponseTypeDef",
    "GetFeatureRequestRequestTypeDef",
    "GetFeatureResponseTypeDef",
    "GetLaunchRequestRequestTypeDef",
    "GetLaunchResponseTypeDef",
    "GetProjectRequestRequestTypeDef",
    "GetProjectResponseTypeDef",
    "GetSegmentRequestRequestTypeDef",
    "GetSegmentResponseTypeDef",
    "LaunchExecutionTypeDef",
    "LaunchGroupConfigTypeDef",
    "LaunchGroupTypeDef",
    "LaunchTypeDef",
    "ListExperimentsRequestListExperimentsPaginateTypeDef",
    "ListExperimentsRequestRequestTypeDef",
    "ListExperimentsResponseTypeDef",
    "ListFeaturesRequestListFeaturesPaginateTypeDef",
    "ListFeaturesRequestRequestTypeDef",
    "ListFeaturesResponseTypeDef",
    "ListLaunchesRequestListLaunchesPaginateTypeDef",
    "ListLaunchesRequestRequestTypeDef",
    "ListLaunchesResponseTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ListProjectsResponseTypeDef",
    "ListSegmentReferencesRequestListSegmentReferencesPaginateTypeDef",
    "ListSegmentReferencesRequestRequestTypeDef",
    "ListSegmentReferencesResponseTypeDef",
    "ListSegmentsRequestListSegmentsPaginateTypeDef",
    "ListSegmentsRequestRequestTypeDef",
    "ListSegmentsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MetricDefinitionConfigTypeDef",
    "MetricDefinitionTypeDef",
    "MetricGoalConfigTypeDef",
    "MetricGoalTypeDef",
    "MetricMonitorConfigTypeDef",
    "MetricMonitorTypeDef",
    "OnlineAbConfigTypeDef",
    "OnlineAbDefinitionTypeDef",
    "PaginatorConfigTypeDef",
    "ProjectAppConfigResourceConfigTypeDef",
    "ProjectAppConfigResourceTypeDef",
    "ProjectDataDeliveryConfigTypeDef",
    "ProjectDataDeliveryTypeDef",
    "ProjectSummaryTypeDef",
    "ProjectTypeDef",
    "PutProjectEventsRequestRequestTypeDef",
    "PutProjectEventsResponseTypeDef",
    "PutProjectEventsResultEntryTypeDef",
    "RefResourceTypeDef",
    "ResponseMetadataTypeDef",
    "S3DestinationConfigTypeDef",
    "S3DestinationTypeDef",
    "ScheduledSplitConfigTypeDef",
    "ScheduledSplitTypeDef",
    "ScheduledSplitsLaunchConfigTypeDef",
    "ScheduledSplitsLaunchDefinitionTypeDef",
    "SegmentOverrideOutputTypeDef",
    "SegmentOverrideTypeDef",
    "SegmentOverrideUnionTypeDef",
    "SegmentTypeDef",
    "StartExperimentRequestRequestTypeDef",
    "StartExperimentResponseTypeDef",
    "StartLaunchRequestRequestTypeDef",
    "StartLaunchResponseTypeDef",
    "StopExperimentRequestRequestTypeDef",
    "StopExperimentResponseTypeDef",
    "StopLaunchRequestRequestTypeDef",
    "StopLaunchResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TestSegmentPatternRequestRequestTypeDef",
    "TestSegmentPatternResponseTypeDef",
    "TimestampTypeDef",
    "TreatmentConfigTypeDef",
    "TreatmentTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateExperimentRequestRequestTypeDef",
    "UpdateExperimentResponseTypeDef",
    "UpdateFeatureRequestRequestTypeDef",
    "UpdateFeatureResponseTypeDef",
    "UpdateLaunchRequestRequestTypeDef",
    "UpdateLaunchResponseTypeDef",
    "UpdateProjectDataDeliveryRequestRequestTypeDef",
    "UpdateProjectDataDeliveryResponseTypeDef",
    "UpdateProjectRequestRequestTypeDef",
    "UpdateProjectResponseTypeDef",
    "VariableValueTypeDef",
    "VariationConfigTypeDef",
    "VariationTypeDef",
)

class EvaluationRequestTypeDef(TypedDict):
    entityId: str
    feature: str
    evaluationContext: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CloudWatchLogsDestinationConfigTypeDef(TypedDict):
    logGroup: NotRequired[str]

class CloudWatchLogsDestinationTypeDef(TypedDict):
    logGroup: NotRequired[str]

class OnlineAbConfigTypeDef(TypedDict):
    controlTreatmentName: NotRequired[str]
    treatmentWeights: NotRequired[Mapping[str, int]]

class TreatmentConfigTypeDef(TypedDict):
    feature: str
    name: str
    variation: str
    description: NotRequired[str]

class LaunchGroupConfigTypeDef(TypedDict):
    feature: str
    name: str
    variation: str
    description: NotRequired[str]

class ProjectAppConfigResourceConfigTypeDef(TypedDict):
    applicationId: NotRequired[str]
    environmentId: NotRequired[str]

class CreateSegmentRequestRequestTypeDef(TypedDict):
    name: str
    pattern: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class SegmentTypeDef(TypedDict):
    arn: str
    createdTime: datetime
    lastUpdatedTime: datetime
    name: str
    pattern: str
    description: NotRequired[str]
    experimentCount: NotRequired[int]
    launchCount: NotRequired[int]
    tags: NotRequired[Dict[str, str]]

class DeleteExperimentRequestRequestTypeDef(TypedDict):
    experiment: str
    project: str

class DeleteFeatureRequestRequestTypeDef(TypedDict):
    feature: str
    project: str

class DeleteLaunchRequestRequestTypeDef(TypedDict):
    launch: str
    project: str

class DeleteProjectRequestRequestTypeDef(TypedDict):
    project: str

class DeleteSegmentRequestRequestTypeDef(TypedDict):
    segment: str

class EvaluateFeatureRequestRequestTypeDef(TypedDict):
    entityId: str
    feature: str
    project: str
    evaluationContext: NotRequired[str]

class VariableValueTypeDef(TypedDict):
    boolValue: NotRequired[bool]
    doubleValue: NotRequired[float]
    longValue: NotRequired[int]
    stringValue: NotRequired[str]

EvaluationRuleTypeDef = TypedDict(
    "EvaluationRuleTypeDef",
    {
        "type": str,
        "name": NotRequired[str],
    },
)
TimestampTypeDef = Union[datetime, str]

class ExperimentExecutionTypeDef(TypedDict):
    endedTime: NotRequired[datetime]
    startedTime: NotRequired[datetime]

class ExperimentReportTypeDef(TypedDict):
    content: NotRequired[str]
    metricName: NotRequired[str]
    reportName: NotRequired[Literal["BayesianInference"]]
    treatmentName: NotRequired[str]

class ExperimentResultsDataTypeDef(TypedDict):
    metricName: NotRequired[str]
    resultStat: NotRequired[ExperimentResultResponseTypeType]
    treatmentName: NotRequired[str]
    values: NotRequired[List[float]]

class ExperimentScheduleTypeDef(TypedDict):
    analysisCompleteTime: NotRequired[datetime]

class OnlineAbDefinitionTypeDef(TypedDict):
    controlTreatmentName: NotRequired[str]
    treatmentWeights: NotRequired[Dict[str, int]]

class TreatmentTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    featureVariations: NotRequired[Dict[str, str]]

class GetExperimentRequestRequestTypeDef(TypedDict):
    experiment: str
    project: str

class GetFeatureRequestRequestTypeDef(TypedDict):
    feature: str
    project: str

class GetLaunchRequestRequestTypeDef(TypedDict):
    launch: str
    project: str

class GetProjectRequestRequestTypeDef(TypedDict):
    project: str

class GetSegmentRequestRequestTypeDef(TypedDict):
    segment: str

class LaunchExecutionTypeDef(TypedDict):
    endedTime: NotRequired[datetime]
    startedTime: NotRequired[datetime]

class LaunchGroupTypeDef(TypedDict):
    featureVariations: Dict[str, str]
    name: str
    description: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListExperimentsRequestRequestTypeDef(TypedDict):
    project: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[ExperimentStatusType]

class ListFeaturesRequestRequestTypeDef(TypedDict):
    project: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListLaunchesRequestRequestTypeDef(TypedDict):
    project: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[LaunchStatusType]

class ListProjectsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ProjectSummaryTypeDef(TypedDict):
    arn: str
    createdTime: datetime
    lastUpdatedTime: datetime
    name: str
    status: ProjectStatusType
    activeExperimentCount: NotRequired[int]
    activeLaunchCount: NotRequired[int]
    description: NotRequired[str]
    experimentCount: NotRequired[int]
    featureCount: NotRequired[int]
    launchCount: NotRequired[int]
    tags: NotRequired[Dict[str, str]]

ListSegmentReferencesRequestRequestTypeDef = TypedDict(
    "ListSegmentReferencesRequestRequestTypeDef",
    {
        "segment": str,
        "type": SegmentReferenceResourceTypeType,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
RefResourceTypeDef = TypedDict(
    "RefResourceTypeDef",
    {
        "name": str,
        "type": str,
        "arn": NotRequired[str],
        "endTime": NotRequired[str],
        "lastUpdatedOn": NotRequired[str],
        "startTime": NotRequired[str],
        "status": NotRequired[str],
    },
)

class ListSegmentsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class MetricDefinitionConfigTypeDef(TypedDict):
    entityIdKey: str
    name: str
    valueKey: str
    eventPattern: NotRequired[str]
    unitLabel: NotRequired[str]

class MetricDefinitionTypeDef(TypedDict):
    entityIdKey: NotRequired[str]
    eventPattern: NotRequired[str]
    name: NotRequired[str]
    unitLabel: NotRequired[str]
    valueKey: NotRequired[str]

class ProjectAppConfigResourceTypeDef(TypedDict):
    applicationId: str
    configurationProfileId: str
    environmentId: str

class S3DestinationConfigTypeDef(TypedDict):
    bucket: NotRequired[str]
    prefix: NotRequired[str]

class S3DestinationTypeDef(TypedDict):
    bucket: NotRequired[str]
    prefix: NotRequired[str]

class PutProjectEventsResultEntryTypeDef(TypedDict):
    errorCode: NotRequired[str]
    errorMessage: NotRequired[str]
    eventId: NotRequired[str]

class SegmentOverrideOutputTypeDef(TypedDict):
    evaluationOrder: int
    segment: str
    weights: Dict[str, int]

class SegmentOverrideTypeDef(TypedDict):
    evaluationOrder: int
    segment: str
    weights: Mapping[str, int]

class StartLaunchRequestRequestTypeDef(TypedDict):
    launch: str
    project: str

class StopExperimentRequestRequestTypeDef(TypedDict):
    experiment: str
    project: str
    desiredState: NotRequired[ExperimentStopDesiredStateType]
    reason: NotRequired[str]

class StopLaunchRequestRequestTypeDef(TypedDict):
    launch: str
    project: str
    desiredState: NotRequired[LaunchStopDesiredStateType]
    reason: NotRequired[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class TestSegmentPatternRequestRequestTypeDef(TypedDict):
    pattern: str
    payload: str

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class BatchEvaluateFeatureRequestRequestTypeDef(TypedDict):
    project: str
    requests: Sequence[EvaluationRequestTypeDef]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class StartExperimentResponseTypeDef(TypedDict):
    startedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class StopExperimentResponseTypeDef(TypedDict):
    endedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class StopLaunchResponseTypeDef(TypedDict):
    endedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class TestSegmentPatternResponseTypeDef(TypedDict):
    match: bool
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateProjectRequestRequestTypeDef(TypedDict):
    project: str
    appConfigResource: NotRequired[ProjectAppConfigResourceConfigTypeDef]
    description: NotRequired[str]

class CreateSegmentResponseTypeDef(TypedDict):
    segment: SegmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSegmentResponseTypeDef(TypedDict):
    segment: SegmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListSegmentsResponseTypeDef(TypedDict):
    segments: List[SegmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class EvaluateFeatureResponseTypeDef(TypedDict):
    details: str
    reason: str
    value: VariableValueTypeDef
    variation: str
    ResponseMetadata: ResponseMetadataTypeDef

class EvaluationResultTypeDef(TypedDict):
    entityId: str
    feature: str
    details: NotRequired[str]
    project: NotRequired[str]
    reason: NotRequired[str]
    value: NotRequired[VariableValueTypeDef]
    variation: NotRequired[str]

class VariationConfigTypeDef(TypedDict):
    name: str
    value: VariableValueTypeDef

class VariationTypeDef(TypedDict):
    name: NotRequired[str]
    value: NotRequired[VariableValueTypeDef]

class FeatureSummaryTypeDef(TypedDict):
    arn: str
    createdTime: datetime
    evaluationStrategy: FeatureEvaluationStrategyType
    lastUpdatedTime: datetime
    name: str
    status: FeatureStatusType
    defaultVariation: NotRequired[str]
    evaluationRules: NotRequired[List[EvaluationRuleTypeDef]]
    project: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

EventTypeDef = TypedDict(
    "EventTypeDef",
    {
        "data": str,
        "timestamp": TimestampTypeDef,
        "type": EventTypeType,
    },
)

class GetExperimentResultsRequestRequestTypeDef(TypedDict):
    experiment: str
    metricNames: Sequence[str]
    project: str
    treatmentNames: Sequence[str]
    baseStat: NotRequired[Literal["Mean"]]
    endTime: NotRequired[TimestampTypeDef]
    period: NotRequired[int]
    reportNames: NotRequired[Sequence[Literal["BayesianInference"]]]
    resultStats: NotRequired[Sequence[ExperimentResultRequestTypeType]]
    startTime: NotRequired[TimestampTypeDef]

class StartExperimentRequestRequestTypeDef(TypedDict):
    analysisCompleteTime: TimestampTypeDef
    experiment: str
    project: str

class GetExperimentResultsResponseTypeDef(TypedDict):
    details: str
    reports: List[ExperimentReportTypeDef]
    resultsData: List[ExperimentResultsDataTypeDef]
    timestamps: List[datetime]
    ResponseMetadata: ResponseMetadataTypeDef

class ListExperimentsRequestListExperimentsPaginateTypeDef(TypedDict):
    project: str
    status: NotRequired[ExperimentStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFeaturesRequestListFeaturesPaginateTypeDef(TypedDict):
    project: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLaunchesRequestListLaunchesPaginateTypeDef(TypedDict):
    project: str
    status: NotRequired[LaunchStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProjectsRequestListProjectsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListSegmentReferencesRequestListSegmentReferencesPaginateTypeDef = TypedDict(
    "ListSegmentReferencesRequestListSegmentReferencesPaginateTypeDef",
    {
        "segment": str,
        "type": SegmentReferenceResourceTypeType,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListSegmentsRequestListSegmentsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProjectsResponseTypeDef(TypedDict):
    projects: List[ProjectSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSegmentReferencesResponseTypeDef(TypedDict):
    referencedBy: List[RefResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class MetricGoalConfigTypeDef(TypedDict):
    metricDefinition: MetricDefinitionConfigTypeDef
    desiredChange: NotRequired[ChangeDirectionEnumType]

class MetricMonitorConfigTypeDef(TypedDict):
    metricDefinition: MetricDefinitionConfigTypeDef

class MetricGoalTypeDef(TypedDict):
    metricDefinition: MetricDefinitionTypeDef
    desiredChange: NotRequired[ChangeDirectionEnumType]

class MetricMonitorTypeDef(TypedDict):
    metricDefinition: MetricDefinitionTypeDef

class ProjectDataDeliveryConfigTypeDef(TypedDict):
    cloudWatchLogs: NotRequired[CloudWatchLogsDestinationConfigTypeDef]
    s3Destination: NotRequired[S3DestinationConfigTypeDef]

class UpdateProjectDataDeliveryRequestRequestTypeDef(TypedDict):
    project: str
    cloudWatchLogs: NotRequired[CloudWatchLogsDestinationConfigTypeDef]
    s3Destination: NotRequired[S3DestinationConfigTypeDef]

class ProjectDataDeliveryTypeDef(TypedDict):
    cloudWatchLogs: NotRequired[CloudWatchLogsDestinationTypeDef]
    s3Destination: NotRequired[S3DestinationTypeDef]

class PutProjectEventsResponseTypeDef(TypedDict):
    eventResults: List[PutProjectEventsResultEntryTypeDef]
    failedEventCount: int
    ResponseMetadata: ResponseMetadataTypeDef

class ScheduledSplitTypeDef(TypedDict):
    startTime: datetime
    groupWeights: NotRequired[Dict[str, int]]
    segmentOverrides: NotRequired[List[SegmentOverrideOutputTypeDef]]

SegmentOverrideUnionTypeDef = Union[SegmentOverrideTypeDef, SegmentOverrideOutputTypeDef]

class BatchEvaluateFeatureResponseTypeDef(TypedDict):
    results: List[EvaluationResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFeatureRequestRequestTypeDef(TypedDict):
    name: str
    project: str
    variations: Sequence[VariationConfigTypeDef]
    defaultVariation: NotRequired[str]
    description: NotRequired[str]
    entityOverrides: NotRequired[Mapping[str, str]]
    evaluationStrategy: NotRequired[FeatureEvaluationStrategyType]
    tags: NotRequired[Mapping[str, str]]

class UpdateFeatureRequestRequestTypeDef(TypedDict):
    feature: str
    project: str
    addOrUpdateVariations: NotRequired[Sequence[VariationConfigTypeDef]]
    defaultVariation: NotRequired[str]
    description: NotRequired[str]
    entityOverrides: NotRequired[Mapping[str, str]]
    evaluationStrategy: NotRequired[FeatureEvaluationStrategyType]
    removeVariations: NotRequired[Sequence[str]]

class FeatureTypeDef(TypedDict):
    arn: str
    createdTime: datetime
    evaluationStrategy: FeatureEvaluationStrategyType
    lastUpdatedTime: datetime
    name: str
    status: FeatureStatusType
    valueType: VariationValueTypeType
    variations: List[VariationTypeDef]
    defaultVariation: NotRequired[str]
    description: NotRequired[str]
    entityOverrides: NotRequired[Dict[str, str]]
    evaluationRules: NotRequired[List[EvaluationRuleTypeDef]]
    project: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

class ListFeaturesResponseTypeDef(TypedDict):
    features: List[FeatureSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PutProjectEventsRequestRequestTypeDef(TypedDict):
    events: Sequence[EventTypeDef]
    project: str

class CreateExperimentRequestRequestTypeDef(TypedDict):
    metricGoals: Sequence[MetricGoalConfigTypeDef]
    name: str
    project: str
    treatments: Sequence[TreatmentConfigTypeDef]
    description: NotRequired[str]
    onlineAbConfig: NotRequired[OnlineAbConfigTypeDef]
    randomizationSalt: NotRequired[str]
    samplingRate: NotRequired[int]
    segment: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class UpdateExperimentRequestRequestTypeDef(TypedDict):
    experiment: str
    project: str
    description: NotRequired[str]
    metricGoals: NotRequired[Sequence[MetricGoalConfigTypeDef]]
    onlineAbConfig: NotRequired[OnlineAbConfigTypeDef]
    randomizationSalt: NotRequired[str]
    removeSegment: NotRequired[bool]
    samplingRate: NotRequired[int]
    segment: NotRequired[str]
    treatments: NotRequired[Sequence[TreatmentConfigTypeDef]]

ExperimentTypeDef = TypedDict(
    "ExperimentTypeDef",
    {
        "arn": str,
        "createdTime": datetime,
        "lastUpdatedTime": datetime,
        "name": str,
        "status": ExperimentStatusType,
        "type": Literal["aws.evidently.onlineab"],
        "description": NotRequired[str],
        "execution": NotRequired[ExperimentExecutionTypeDef],
        "metricGoals": NotRequired[List[MetricGoalTypeDef]],
        "onlineAbDefinition": NotRequired[OnlineAbDefinitionTypeDef],
        "project": NotRequired[str],
        "randomizationSalt": NotRequired[str],
        "samplingRate": NotRequired[int],
        "schedule": NotRequired[ExperimentScheduleTypeDef],
        "segment": NotRequired[str],
        "statusReason": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "treatments": NotRequired[List[TreatmentTypeDef]],
    },
)

class CreateProjectRequestRequestTypeDef(TypedDict):
    name: str
    appConfigResource: NotRequired[ProjectAppConfigResourceConfigTypeDef]
    dataDelivery: NotRequired[ProjectDataDeliveryConfigTypeDef]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class ProjectTypeDef(TypedDict):
    arn: str
    createdTime: datetime
    lastUpdatedTime: datetime
    name: str
    status: ProjectStatusType
    activeExperimentCount: NotRequired[int]
    activeLaunchCount: NotRequired[int]
    appConfigResource: NotRequired[ProjectAppConfigResourceTypeDef]
    dataDelivery: NotRequired[ProjectDataDeliveryTypeDef]
    description: NotRequired[str]
    experimentCount: NotRequired[int]
    featureCount: NotRequired[int]
    launchCount: NotRequired[int]
    tags: NotRequired[Dict[str, str]]

class ScheduledSplitsLaunchDefinitionTypeDef(TypedDict):
    steps: NotRequired[List[ScheduledSplitTypeDef]]

class ScheduledSplitConfigTypeDef(TypedDict):
    groupWeights: Mapping[str, int]
    startTime: TimestampTypeDef
    segmentOverrides: NotRequired[Sequence[SegmentOverrideUnionTypeDef]]

class CreateFeatureResponseTypeDef(TypedDict):
    feature: FeatureTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetFeatureResponseTypeDef(TypedDict):
    feature: FeatureTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateFeatureResponseTypeDef(TypedDict):
    feature: FeatureTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateExperimentResponseTypeDef(TypedDict):
    experiment: ExperimentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetExperimentResponseTypeDef(TypedDict):
    experiment: ExperimentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListExperimentsResponseTypeDef(TypedDict):
    experiments: List[ExperimentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateExperimentResponseTypeDef(TypedDict):
    experiment: ExperimentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateProjectResponseTypeDef(TypedDict):
    project: ProjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetProjectResponseTypeDef(TypedDict):
    project: ProjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateProjectDataDeliveryResponseTypeDef(TypedDict):
    project: ProjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateProjectResponseTypeDef(TypedDict):
    project: ProjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

LaunchTypeDef = TypedDict(
    "LaunchTypeDef",
    {
        "arn": str,
        "createdTime": datetime,
        "lastUpdatedTime": datetime,
        "name": str,
        "status": LaunchStatusType,
        "type": Literal["aws.evidently.splits"],
        "description": NotRequired[str],
        "execution": NotRequired[LaunchExecutionTypeDef],
        "groups": NotRequired[List[LaunchGroupTypeDef]],
        "metricMonitors": NotRequired[List[MetricMonitorTypeDef]],
        "project": NotRequired[str],
        "randomizationSalt": NotRequired[str],
        "scheduledSplitsDefinition": NotRequired[ScheduledSplitsLaunchDefinitionTypeDef],
        "statusReason": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)

class ScheduledSplitsLaunchConfigTypeDef(TypedDict):
    steps: Sequence[ScheduledSplitConfigTypeDef]

class CreateLaunchResponseTypeDef(TypedDict):
    launch: LaunchTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetLaunchResponseTypeDef(TypedDict):
    launch: LaunchTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListLaunchesResponseTypeDef(TypedDict):
    launches: List[LaunchTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class StartLaunchResponseTypeDef(TypedDict):
    launch: LaunchTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateLaunchResponseTypeDef(TypedDict):
    launch: LaunchTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLaunchRequestRequestTypeDef(TypedDict):
    groups: Sequence[LaunchGroupConfigTypeDef]
    name: str
    project: str
    description: NotRequired[str]
    metricMonitors: NotRequired[Sequence[MetricMonitorConfigTypeDef]]
    randomizationSalt: NotRequired[str]
    scheduledSplitsConfig: NotRequired[ScheduledSplitsLaunchConfigTypeDef]
    tags: NotRequired[Mapping[str, str]]

class UpdateLaunchRequestRequestTypeDef(TypedDict):
    launch: str
    project: str
    description: NotRequired[str]
    groups: NotRequired[Sequence[LaunchGroupConfigTypeDef]]
    metricMonitors: NotRequired[Sequence[MetricMonitorConfigTypeDef]]
    randomizationSalt: NotRequired[str]
    scheduledSplitsConfig: NotRequired[ScheduledSplitsLaunchConfigTypeDef]
