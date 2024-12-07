"""
Type annotations for frauddetector service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_frauddetector/type_defs/)

Usage::

    ```python
    from mypy_boto3_frauddetector.type_defs import ATIMetricDataPointTypeDef

    data: ATIMetricDataPointTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AsyncJobStatusType,
    DataSourceType,
    DataTypeType,
    DetectorVersionStatusType,
    EventIngestionType,
    ListUpdateModeType,
    ModelEndpointStatusType,
    ModelInputDataFormatType,
    ModelOutputDataFormatType,
    ModelTypeEnumType,
    ModelVersionStatusType,
    RuleExecutionModeType,
    TrainingDataSourceEnumType,
    UnlabeledEventsTreatmentType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "ATIMetricDataPointTypeDef",
    "ATIModelPerformanceTypeDef",
    "ATITrainingMetricsValueTypeDef",
    "AggregatedLogOddsMetricTypeDef",
    "AggregatedVariablesImpactExplanationTypeDef",
    "AggregatedVariablesImportanceMetricsTypeDef",
    "AllowDenyListTypeDef",
    "BatchCreateVariableErrorTypeDef",
    "BatchCreateVariableRequestRequestTypeDef",
    "BatchCreateVariableResultTypeDef",
    "BatchGetVariableErrorTypeDef",
    "BatchGetVariableRequestRequestTypeDef",
    "BatchGetVariableResultTypeDef",
    "BatchImportTypeDef",
    "BatchPredictionTypeDef",
    "BlobTypeDef",
    "CancelBatchImportJobRequestRequestTypeDef",
    "CancelBatchPredictionJobRequestRequestTypeDef",
    "CreateBatchImportJobRequestRequestTypeDef",
    "CreateBatchPredictionJobRequestRequestTypeDef",
    "CreateDetectorVersionRequestRequestTypeDef",
    "CreateDetectorVersionResultTypeDef",
    "CreateListRequestRequestTypeDef",
    "CreateModelRequestRequestTypeDef",
    "CreateModelVersionRequestRequestTypeDef",
    "CreateModelVersionResultTypeDef",
    "CreateRuleRequestRequestTypeDef",
    "CreateRuleResultTypeDef",
    "CreateVariableRequestRequestTypeDef",
    "DataValidationMetricsTypeDef",
    "DeleteBatchImportJobRequestRequestTypeDef",
    "DeleteBatchPredictionJobRequestRequestTypeDef",
    "DeleteDetectorRequestRequestTypeDef",
    "DeleteDetectorVersionRequestRequestTypeDef",
    "DeleteEntityTypeRequestRequestTypeDef",
    "DeleteEventRequestRequestTypeDef",
    "DeleteEventTypeRequestRequestTypeDef",
    "DeleteEventsByEventTypeRequestRequestTypeDef",
    "DeleteEventsByEventTypeResultTypeDef",
    "DeleteExternalModelRequestRequestTypeDef",
    "DeleteLabelRequestRequestTypeDef",
    "DeleteListRequestRequestTypeDef",
    "DeleteModelRequestRequestTypeDef",
    "DeleteModelVersionRequestRequestTypeDef",
    "DeleteOutcomeRequestRequestTypeDef",
    "DeleteRuleRequestRequestTypeDef",
    "DeleteVariableRequestRequestTypeDef",
    "DescribeDetectorRequestRequestTypeDef",
    "DescribeDetectorResultTypeDef",
    "DescribeModelVersionsRequestRequestTypeDef",
    "DescribeModelVersionsResultTypeDef",
    "DetectorTypeDef",
    "DetectorVersionSummaryTypeDef",
    "EntityTypeDef",
    "EntityTypeTypeDef",
    "EvaluatedExternalModelTypeDef",
    "EvaluatedModelVersionTypeDef",
    "EvaluatedRuleTypeDef",
    "EventOrchestrationTypeDef",
    "EventPredictionSummaryTypeDef",
    "EventTypeDef",
    "EventTypeTypeDef",
    "EventVariableSummaryTypeDef",
    "ExternalEventsDetailTypeDef",
    "ExternalModelOutputsTypeDef",
    "ExternalModelSummaryTypeDef",
    "ExternalModelTypeDef",
    "FieldValidationMessageTypeDef",
    "FileValidationMessageTypeDef",
    "FilterConditionTypeDef",
    "GetBatchImportJobsRequestRequestTypeDef",
    "GetBatchImportJobsResultTypeDef",
    "GetBatchPredictionJobsRequestRequestTypeDef",
    "GetBatchPredictionJobsResultTypeDef",
    "GetDeleteEventsByEventTypeStatusRequestRequestTypeDef",
    "GetDeleteEventsByEventTypeStatusResultTypeDef",
    "GetDetectorVersionRequestRequestTypeDef",
    "GetDetectorVersionResultTypeDef",
    "GetDetectorsRequestRequestTypeDef",
    "GetDetectorsResultTypeDef",
    "GetEntityTypesRequestRequestTypeDef",
    "GetEntityTypesResultTypeDef",
    "GetEventPredictionMetadataRequestRequestTypeDef",
    "GetEventPredictionMetadataResultTypeDef",
    "GetEventPredictionRequestRequestTypeDef",
    "GetEventPredictionResultTypeDef",
    "GetEventRequestRequestTypeDef",
    "GetEventResultTypeDef",
    "GetEventTypesRequestRequestTypeDef",
    "GetEventTypesResultTypeDef",
    "GetExternalModelsRequestRequestTypeDef",
    "GetExternalModelsResultTypeDef",
    "GetKMSEncryptionKeyResultTypeDef",
    "GetLabelsRequestRequestTypeDef",
    "GetLabelsResultTypeDef",
    "GetListElementsRequestRequestTypeDef",
    "GetListElementsResultTypeDef",
    "GetListsMetadataRequestRequestTypeDef",
    "GetListsMetadataResultTypeDef",
    "GetModelVersionRequestRequestTypeDef",
    "GetModelVersionResultTypeDef",
    "GetModelsRequestRequestTypeDef",
    "GetModelsResultTypeDef",
    "GetOutcomesRequestRequestTypeDef",
    "GetOutcomesResultTypeDef",
    "GetRulesRequestRequestTypeDef",
    "GetRulesResultTypeDef",
    "GetVariablesRequestRequestTypeDef",
    "GetVariablesResultTypeDef",
    "IngestedEventStatisticsTypeDef",
    "IngestedEventsDetailTypeDef",
    "IngestedEventsTimeWindowTypeDef",
    "KMSKeyTypeDef",
    "LabelSchemaOutputTypeDef",
    "LabelSchemaTypeDef",
    "LabelSchemaUnionTypeDef",
    "LabelTypeDef",
    "ListEventPredictionsRequestRequestTypeDef",
    "ListEventPredictionsResultTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResultTypeDef",
    "LogOddsMetricTypeDef",
    "MetricDataPointTypeDef",
    "ModelEndpointDataBlobTypeDef",
    "ModelInputConfigurationTypeDef",
    "ModelOutputConfigurationOutputTypeDef",
    "ModelOutputConfigurationTypeDef",
    "ModelScoresTypeDef",
    "ModelTypeDef",
    "ModelVersionDetailTypeDef",
    "ModelVersionEvaluationTypeDef",
    "ModelVersionTypeDef",
    "OFIMetricDataPointTypeDef",
    "OFIModelPerformanceTypeDef",
    "OFITrainingMetricsValueTypeDef",
    "OutcomeTypeDef",
    "PredictionExplanationsTypeDef",
    "PredictionTimeRangeTypeDef",
    "PutDetectorRequestRequestTypeDef",
    "PutEntityTypeRequestRequestTypeDef",
    "PutEventTypeRequestRequestTypeDef",
    "PutExternalModelRequestRequestTypeDef",
    "PutKMSEncryptionKeyRequestRequestTypeDef",
    "PutLabelRequestRequestTypeDef",
    "PutOutcomeRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "RuleDetailTypeDef",
    "RuleResultTypeDef",
    "RuleTypeDef",
    "SendEventRequestRequestTypeDef",
    "TFIMetricDataPointTypeDef",
    "TFIModelPerformanceTypeDef",
    "TFITrainingMetricsValueTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TrainingDataSchemaOutputTypeDef",
    "TrainingDataSchemaTypeDef",
    "TrainingMetricsTypeDef",
    "TrainingMetricsV2TypeDef",
    "TrainingResultTypeDef",
    "TrainingResultV2TypeDef",
    "UncertaintyRangeTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDetectorVersionMetadataRequestRequestTypeDef",
    "UpdateDetectorVersionRequestRequestTypeDef",
    "UpdateDetectorVersionStatusRequestRequestTypeDef",
    "UpdateEventLabelRequestRequestTypeDef",
    "UpdateListRequestRequestTypeDef",
    "UpdateModelRequestRequestTypeDef",
    "UpdateModelVersionRequestRequestTypeDef",
    "UpdateModelVersionResultTypeDef",
    "UpdateModelVersionStatusRequestRequestTypeDef",
    "UpdateRuleMetadataRequestRequestTypeDef",
    "UpdateRuleVersionRequestRequestTypeDef",
    "UpdateRuleVersionResultTypeDef",
    "UpdateVariableRequestRequestTypeDef",
    "VariableEntryTypeDef",
    "VariableImpactExplanationTypeDef",
    "VariableImportanceMetricsTypeDef",
    "VariableTypeDef",
)

class ATIMetricDataPointTypeDef(TypedDict):
    cr: NotRequired[float]
    adr: NotRequired[float]
    threshold: NotRequired[float]
    atodr: NotRequired[float]

class ATIModelPerformanceTypeDef(TypedDict):
    asi: NotRequired[float]

class AggregatedLogOddsMetricTypeDef(TypedDict):
    variableNames: List[str]
    aggregatedVariablesImportance: float

class AggregatedVariablesImpactExplanationTypeDef(TypedDict):
    eventVariableNames: NotRequired[List[str]]
    relativeImpact: NotRequired[str]
    logOddsImpact: NotRequired[float]

class AllowDenyListTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    variableType: NotRequired[str]
    createdTime: NotRequired[str]
    updatedTime: NotRequired[str]
    arn: NotRequired[str]

class BatchCreateVariableErrorTypeDef(TypedDict):
    name: NotRequired[str]
    code: NotRequired[int]
    message: NotRequired[str]

class TagTypeDef(TypedDict):
    key: str
    value: str

class VariableEntryTypeDef(TypedDict):
    name: NotRequired[str]
    dataType: NotRequired[str]
    dataSource: NotRequired[str]
    defaultValue: NotRequired[str]
    description: NotRequired[str]
    variableType: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BatchGetVariableErrorTypeDef(TypedDict):
    name: NotRequired[str]
    code: NotRequired[int]
    message: NotRequired[str]

class BatchGetVariableRequestRequestTypeDef(TypedDict):
    names: Sequence[str]

class VariableTypeDef(TypedDict):
    name: NotRequired[str]
    dataType: NotRequired[DataTypeType]
    dataSource: NotRequired[DataSourceType]
    defaultValue: NotRequired[str]
    description: NotRequired[str]
    variableType: NotRequired[str]
    lastUpdatedTime: NotRequired[str]
    createdTime: NotRequired[str]
    arn: NotRequired[str]

class BatchImportTypeDef(TypedDict):
    jobId: NotRequired[str]
    status: NotRequired[AsyncJobStatusType]
    failureReason: NotRequired[str]
    startTime: NotRequired[str]
    completionTime: NotRequired[str]
    inputPath: NotRequired[str]
    outputPath: NotRequired[str]
    eventTypeName: NotRequired[str]
    iamRoleArn: NotRequired[str]
    arn: NotRequired[str]
    processedRecordsCount: NotRequired[int]
    failedRecordsCount: NotRequired[int]
    totalRecordsCount: NotRequired[int]

class BatchPredictionTypeDef(TypedDict):
    jobId: NotRequired[str]
    status: NotRequired[AsyncJobStatusType]
    failureReason: NotRequired[str]
    startTime: NotRequired[str]
    completionTime: NotRequired[str]
    lastHeartbeatTime: NotRequired[str]
    inputPath: NotRequired[str]
    outputPath: NotRequired[str]
    eventTypeName: NotRequired[str]
    detectorName: NotRequired[str]
    detectorVersion: NotRequired[str]
    iamRoleArn: NotRequired[str]
    arn: NotRequired[str]
    processedRecordsCount: NotRequired[int]
    totalRecordsCount: NotRequired[int]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class CancelBatchImportJobRequestRequestTypeDef(TypedDict):
    jobId: str

class CancelBatchPredictionJobRequestRequestTypeDef(TypedDict):
    jobId: str

class ModelVersionTypeDef(TypedDict):
    modelId: str
    modelType: ModelTypeEnumType
    modelVersionNumber: str
    arn: NotRequired[str]

class RuleTypeDef(TypedDict):
    detectorId: str
    ruleId: str
    ruleVersion: str

class ExternalEventsDetailTypeDef(TypedDict):
    dataLocation: str
    dataAccessRoleArn: str

FieldValidationMessageTypeDef = TypedDict(
    "FieldValidationMessageTypeDef",
    {
        "fieldName": NotRequired[str],
        "identifier": NotRequired[str],
        "title": NotRequired[str],
        "content": NotRequired[str],
        "type": NotRequired[str],
    },
)
FileValidationMessageTypeDef = TypedDict(
    "FileValidationMessageTypeDef",
    {
        "title": NotRequired[str],
        "content": NotRequired[str],
        "type": NotRequired[str],
    },
)

class DeleteBatchImportJobRequestRequestTypeDef(TypedDict):
    jobId: str

class DeleteBatchPredictionJobRequestRequestTypeDef(TypedDict):
    jobId: str

class DeleteDetectorRequestRequestTypeDef(TypedDict):
    detectorId: str

class DeleteDetectorVersionRequestRequestTypeDef(TypedDict):
    detectorId: str
    detectorVersionId: str

class DeleteEntityTypeRequestRequestTypeDef(TypedDict):
    name: str

class DeleteEventRequestRequestTypeDef(TypedDict):
    eventId: str
    eventTypeName: str
    deleteAuditHistory: NotRequired[bool]

class DeleteEventTypeRequestRequestTypeDef(TypedDict):
    name: str

class DeleteEventsByEventTypeRequestRequestTypeDef(TypedDict):
    eventTypeName: str

class DeleteExternalModelRequestRequestTypeDef(TypedDict):
    modelEndpoint: str

class DeleteLabelRequestRequestTypeDef(TypedDict):
    name: str

class DeleteListRequestRequestTypeDef(TypedDict):
    name: str

class DeleteModelRequestRequestTypeDef(TypedDict):
    modelId: str
    modelType: ModelTypeEnumType

class DeleteModelVersionRequestRequestTypeDef(TypedDict):
    modelId: str
    modelType: ModelTypeEnumType
    modelVersionNumber: str

class DeleteOutcomeRequestRequestTypeDef(TypedDict):
    name: str

class DeleteVariableRequestRequestTypeDef(TypedDict):
    name: str

class DescribeDetectorRequestRequestTypeDef(TypedDict):
    detectorId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class DetectorVersionSummaryTypeDef(TypedDict):
    detectorVersionId: NotRequired[str]
    status: NotRequired[DetectorVersionStatusType]
    description: NotRequired[str]
    lastUpdatedTime: NotRequired[str]

class DescribeModelVersionsRequestRequestTypeDef(TypedDict):
    modelId: NotRequired[str]
    modelVersionNumber: NotRequired[str]
    modelType: NotRequired[ModelTypeEnumType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class DetectorTypeDef(TypedDict):
    detectorId: NotRequired[str]
    description: NotRequired[str]
    eventTypeName: NotRequired[str]
    lastUpdatedTime: NotRequired[str]
    createdTime: NotRequired[str]
    arn: NotRequired[str]

class EntityTypeDef(TypedDict):
    entityType: str
    entityId: str

class EntityTypeTypeDef(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    lastUpdatedTime: NotRequired[str]
    createdTime: NotRequired[str]
    arn: NotRequired[str]

class EvaluatedExternalModelTypeDef(TypedDict):
    modelEndpoint: NotRequired[str]
    useEventVariables: NotRequired[bool]
    inputVariables: NotRequired[Dict[str, str]]
    outputVariables: NotRequired[Dict[str, str]]

class EvaluatedRuleTypeDef(TypedDict):
    ruleId: NotRequired[str]
    ruleVersion: NotRequired[str]
    expression: NotRequired[str]
    expressionWithValues: NotRequired[str]
    outcomes: NotRequired[List[str]]
    evaluated: NotRequired[bool]
    matched: NotRequired[bool]

class EventOrchestrationTypeDef(TypedDict):
    eventBridgeEnabled: bool

class EventPredictionSummaryTypeDef(TypedDict):
    eventId: NotRequired[str]
    eventTypeName: NotRequired[str]
    eventTimestamp: NotRequired[str]
    predictionTimestamp: NotRequired[str]
    detectorId: NotRequired[str]
    detectorVersionId: NotRequired[str]

class IngestedEventStatisticsTypeDef(TypedDict):
    numberOfEvents: NotRequired[int]
    eventDataSizeInBytes: NotRequired[int]
    leastRecentEvent: NotRequired[str]
    mostRecentEvent: NotRequired[str]
    lastUpdatedTime: NotRequired[str]

class EventVariableSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    value: NotRequired[str]
    source: NotRequired[str]

class ExternalModelSummaryTypeDef(TypedDict):
    modelEndpoint: NotRequired[str]
    modelSource: NotRequired[Literal["SAGEMAKER"]]

ModelInputConfigurationTypeDef = TypedDict(
    "ModelInputConfigurationTypeDef",
    {
        "useEventVariables": bool,
        "eventTypeName": NotRequired[str],
        "format": NotRequired[ModelInputDataFormatType],
        "jsonInputTemplate": NotRequired[str],
        "csvInputTemplate": NotRequired[str],
    },
)
ModelOutputConfigurationOutputTypeDef = TypedDict(
    "ModelOutputConfigurationOutputTypeDef",
    {
        "format": ModelOutputDataFormatType,
        "jsonKeyToVariableMap": NotRequired[Dict[str, str]],
        "csvIndexToVariableMap": NotRequired[Dict[str, str]],
    },
)

class FilterConditionTypeDef(TypedDict):
    value: NotRequired[str]

class GetBatchImportJobsRequestRequestTypeDef(TypedDict):
    jobId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class GetBatchPredictionJobsRequestRequestTypeDef(TypedDict):
    jobId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class GetDeleteEventsByEventTypeStatusRequestRequestTypeDef(TypedDict):
    eventTypeName: str

class GetDetectorVersionRequestRequestTypeDef(TypedDict):
    detectorId: str
    detectorVersionId: str

class GetDetectorsRequestRequestTypeDef(TypedDict):
    detectorId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class GetEntityTypesRequestRequestTypeDef(TypedDict):
    name: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class GetEventPredictionMetadataRequestRequestTypeDef(TypedDict):
    eventId: str
    eventTypeName: str
    detectorId: str
    detectorVersionId: str
    predictionTimestamp: str

class RuleResultTypeDef(TypedDict):
    ruleId: NotRequired[str]
    outcomes: NotRequired[List[str]]

class GetEventRequestRequestTypeDef(TypedDict):
    eventId: str
    eventTypeName: str

class GetEventTypesRequestRequestTypeDef(TypedDict):
    name: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class GetExternalModelsRequestRequestTypeDef(TypedDict):
    modelEndpoint: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class KMSKeyTypeDef(TypedDict):
    kmsEncryptionKeyArn: NotRequired[str]

class GetLabelsRequestRequestTypeDef(TypedDict):
    name: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class LabelTypeDef(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    lastUpdatedTime: NotRequired[str]
    createdTime: NotRequired[str]
    arn: NotRequired[str]

class GetListElementsRequestRequestTypeDef(TypedDict):
    name: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class GetListsMetadataRequestRequestTypeDef(TypedDict):
    name: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class GetModelVersionRequestRequestTypeDef(TypedDict):
    modelId: str
    modelType: ModelTypeEnumType
    modelVersionNumber: str

class GetModelsRequestRequestTypeDef(TypedDict):
    modelId: NotRequired[str]
    modelType: NotRequired[ModelTypeEnumType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ModelTypeDef(TypedDict):
    modelId: NotRequired[str]
    modelType: NotRequired[ModelTypeEnumType]
    description: NotRequired[str]
    eventTypeName: NotRequired[str]
    createdTime: NotRequired[str]
    lastUpdatedTime: NotRequired[str]
    arn: NotRequired[str]

class GetOutcomesRequestRequestTypeDef(TypedDict):
    name: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class OutcomeTypeDef(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    lastUpdatedTime: NotRequired[str]
    createdTime: NotRequired[str]
    arn: NotRequired[str]

class GetRulesRequestRequestTypeDef(TypedDict):
    detectorId: str
    ruleId: NotRequired[str]
    ruleVersion: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class RuleDetailTypeDef(TypedDict):
    ruleId: NotRequired[str]
    description: NotRequired[str]
    detectorId: NotRequired[str]
    ruleVersion: NotRequired[str]
    expression: NotRequired[str]
    language: NotRequired[Literal["DETECTORPL"]]
    outcomes: NotRequired[List[str]]
    lastUpdatedTime: NotRequired[str]
    createdTime: NotRequired[str]
    arn: NotRequired[str]

class GetVariablesRequestRequestTypeDef(TypedDict):
    name: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class IngestedEventsTimeWindowTypeDef(TypedDict):
    startTime: str
    endTime: str

class LabelSchemaOutputTypeDef(TypedDict):
    labelMapper: NotRequired[Dict[str, List[str]]]
    unlabeledEventsTreatment: NotRequired[UnlabeledEventsTreatmentType]

class LabelSchemaTypeDef(TypedDict):
    labelMapper: NotRequired[Mapping[str, Sequence[str]]]
    unlabeledEventsTreatment: NotRequired[UnlabeledEventsTreatmentType]

class PredictionTimeRangeTypeDef(TypedDict):
    startTime: str
    endTime: str

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class LogOddsMetricTypeDef(TypedDict):
    variableName: str
    variableType: str
    variableImportance: float

class MetricDataPointTypeDef(TypedDict):
    fpr: NotRequired[float]
    precision: NotRequired[float]
    tpr: NotRequired[float]
    threshold: NotRequired[float]

ModelOutputConfigurationTypeDef = TypedDict(
    "ModelOutputConfigurationTypeDef",
    {
        "format": ModelOutputDataFormatType,
        "jsonKeyToVariableMap": NotRequired[Mapping[str, str]],
        "csvIndexToVariableMap": NotRequired[Mapping[str, str]],
    },
)

class OFIMetricDataPointTypeDef(TypedDict):
    fpr: NotRequired[float]
    precision: NotRequired[float]
    tpr: NotRequired[float]
    threshold: NotRequired[float]

class UncertaintyRangeTypeDef(TypedDict):
    lowerBoundValue: float
    upperBoundValue: float

class VariableImpactExplanationTypeDef(TypedDict):
    eventVariableName: NotRequired[str]
    relativeImpact: NotRequired[str]
    logOddsImpact: NotRequired[float]

class PutKMSEncryptionKeyRequestRequestTypeDef(TypedDict):
    kmsEncryptionKeyArn: str

class TFIMetricDataPointTypeDef(TypedDict):
    fpr: NotRequired[float]
    precision: NotRequired[float]
    tpr: NotRequired[float]
    threshold: NotRequired[float]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str
    tagKeys: Sequence[str]

class UpdateDetectorVersionMetadataRequestRequestTypeDef(TypedDict):
    detectorId: str
    detectorVersionId: str
    description: str

class UpdateDetectorVersionStatusRequestRequestTypeDef(TypedDict):
    detectorId: str
    detectorVersionId: str
    status: DetectorVersionStatusType

class UpdateEventLabelRequestRequestTypeDef(TypedDict):
    eventId: str
    eventTypeName: str
    assignedLabel: str
    labelTimestamp: str

class UpdateListRequestRequestTypeDef(TypedDict):
    name: str
    elements: NotRequired[Sequence[str]]
    description: NotRequired[str]
    updateMode: NotRequired[ListUpdateModeType]
    variableType: NotRequired[str]

class UpdateModelRequestRequestTypeDef(TypedDict):
    modelId: str
    modelType: ModelTypeEnumType
    description: NotRequired[str]

class UpdateModelVersionStatusRequestRequestTypeDef(TypedDict):
    modelId: str
    modelType: ModelTypeEnumType
    modelVersionNumber: str
    status: ModelVersionStatusType

class UpdateVariableRequestRequestTypeDef(TypedDict):
    name: str
    defaultValue: NotRequired[str]
    description: NotRequired[str]
    variableType: NotRequired[str]

class ATITrainingMetricsValueTypeDef(TypedDict):
    metricDataPoints: NotRequired[List[ATIMetricDataPointTypeDef]]
    modelPerformance: NotRequired[ATIModelPerformanceTypeDef]

class AggregatedVariablesImportanceMetricsTypeDef(TypedDict):
    logOddsMetrics: NotRequired[List[AggregatedLogOddsMetricTypeDef]]

class CreateBatchImportJobRequestRequestTypeDef(TypedDict):
    jobId: str
    inputPath: str
    outputPath: str
    eventTypeName: str
    iamRoleArn: str
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateBatchPredictionJobRequestRequestTypeDef(TypedDict):
    jobId: str
    inputPath: str
    outputPath: str
    eventTypeName: str
    detectorName: str
    iamRoleArn: str
    detectorVersion: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateListRequestRequestTypeDef(TypedDict):
    name: str
    elements: NotRequired[Sequence[str]]
    variableType: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateModelRequestRequestTypeDef(TypedDict):
    modelId: str
    modelType: ModelTypeEnumType
    eventTypeName: str
    description: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateRuleRequestRequestTypeDef(TypedDict):
    ruleId: str
    detectorId: str
    expression: str
    language: Literal["DETECTORPL"]
    outcomes: Sequence[str]
    description: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateVariableRequestRequestTypeDef(TypedDict):
    name: str
    dataType: DataTypeType
    dataSource: DataSourceType
    defaultValue: str
    description: NotRequired[str]
    variableType: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class PutDetectorRequestRequestTypeDef(TypedDict):
    detectorId: str
    eventTypeName: str
    description: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class PutEntityTypeRequestRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class PutLabelRequestRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class PutOutcomeRequestRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str
    tags: Sequence[TagTypeDef]

class BatchCreateVariableRequestRequestTypeDef(TypedDict):
    variableEntries: Sequence[VariableEntryTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]

class BatchCreateVariableResultTypeDef(TypedDict):
    errors: List[BatchCreateVariableErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDetectorVersionResultTypeDef(TypedDict):
    detectorId: str
    detectorVersionId: str
    status: DetectorVersionStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateModelVersionResultTypeDef(TypedDict):
    modelId: str
    modelType: ModelTypeEnumType
    modelVersionNumber: str
    status: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteEventsByEventTypeResultTypeDef(TypedDict):
    eventTypeName: str
    eventsDeletionStatus: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetDeleteEventsByEventTypeStatusResultTypeDef(TypedDict):
    eventTypeName: str
    eventsDeletionStatus: AsyncJobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class GetListElementsResultTypeDef(TypedDict):
    elements: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetListsMetadataResultTypeDef(TypedDict):
    lists: List[AllowDenyListTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResultTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateModelVersionResultTypeDef(TypedDict):
    modelId: str
    modelType: ModelTypeEnumType
    modelVersionNumber: str
    status: str
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetVariableResultTypeDef(TypedDict):
    variables: List[VariableTypeDef]
    errors: List[BatchGetVariableErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetVariablesResultTypeDef(TypedDict):
    variables: List[VariableTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetBatchImportJobsResultTypeDef(TypedDict):
    batchImports: List[BatchImportTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetBatchPredictionJobsResultTypeDef(TypedDict):
    batchPredictions: List[BatchPredictionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ModelEndpointDataBlobTypeDef(TypedDict):
    byteBuffer: NotRequired[BlobTypeDef]
    contentType: NotRequired[str]

class ModelScoresTypeDef(TypedDict):
    modelVersion: NotRequired[ModelVersionTypeDef]
    scores: NotRequired[Dict[str, float]]

class CreateDetectorVersionRequestRequestTypeDef(TypedDict):
    detectorId: str
    rules: Sequence[RuleTypeDef]
    description: NotRequired[str]
    externalModelEndpoints: NotRequired[Sequence[str]]
    modelVersions: NotRequired[Sequence[ModelVersionTypeDef]]
    ruleExecutionMode: NotRequired[RuleExecutionModeType]
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateRuleResultTypeDef(TypedDict):
    rule: RuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteRuleRequestRequestTypeDef(TypedDict):
    rule: RuleTypeDef

class GetDetectorVersionResultTypeDef(TypedDict):
    detectorId: str
    detectorVersionId: str
    description: str
    externalModelEndpoints: List[str]
    modelVersions: List[ModelVersionTypeDef]
    rules: List[RuleTypeDef]
    status: DetectorVersionStatusType
    lastUpdatedTime: str
    createdTime: str
    ruleExecutionMode: RuleExecutionModeType
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDetectorVersionRequestRequestTypeDef(TypedDict):
    detectorId: str
    detectorVersionId: str
    externalModelEndpoints: Sequence[str]
    rules: Sequence[RuleTypeDef]
    description: NotRequired[str]
    modelVersions: NotRequired[Sequence[ModelVersionTypeDef]]
    ruleExecutionMode: NotRequired[RuleExecutionModeType]

class UpdateRuleMetadataRequestRequestTypeDef(TypedDict):
    rule: RuleTypeDef
    description: str

class UpdateRuleVersionRequestRequestTypeDef(TypedDict):
    rule: RuleTypeDef
    expression: str
    language: Literal["DETECTORPL"]
    outcomes: Sequence[str]
    description: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class UpdateRuleVersionResultTypeDef(TypedDict):
    rule: RuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DataValidationMetricsTypeDef(TypedDict):
    fileLevelMessages: NotRequired[List[FileValidationMessageTypeDef]]
    fieldLevelMessages: NotRequired[List[FieldValidationMessageTypeDef]]

class DescribeDetectorResultTypeDef(TypedDict):
    detectorId: str
    detectorVersionSummaries: List[DetectorVersionSummaryTypeDef]
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetDetectorsResultTypeDef(TypedDict):
    detectors: List[DetectorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class EventTypeDef(TypedDict):
    eventId: NotRequired[str]
    eventTypeName: NotRequired[str]
    eventTimestamp: NotRequired[str]
    eventVariables: NotRequired[Dict[str, str]]
    currentLabel: NotRequired[str]
    labelTimestamp: NotRequired[str]
    entities: NotRequired[List[EntityTypeDef]]

class SendEventRequestRequestTypeDef(TypedDict):
    eventId: str
    eventTypeName: str
    eventTimestamp: str
    eventVariables: Mapping[str, str]
    entities: Sequence[EntityTypeDef]
    assignedLabel: NotRequired[str]
    labelTimestamp: NotRequired[str]

class GetEntityTypesResultTypeDef(TypedDict):
    entityTypes: List[EntityTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PutEventTypeRequestRequestTypeDef(TypedDict):
    name: str
    eventVariables: Sequence[str]
    entityTypes: Sequence[str]
    description: NotRequired[str]
    labels: NotRequired[Sequence[str]]
    eventIngestion: NotRequired[EventIngestionType]
    tags: NotRequired[Sequence[TagTypeDef]]
    eventOrchestration: NotRequired[EventOrchestrationTypeDef]

class ListEventPredictionsResultTypeDef(TypedDict):
    eventPredictionSummaries: List[EventPredictionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class EventTypeTypeDef(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    eventVariables: NotRequired[List[str]]
    labels: NotRequired[List[str]]
    entityTypes: NotRequired[List[str]]
    eventIngestion: NotRequired[EventIngestionType]
    ingestedEventStatistics: NotRequired[IngestedEventStatisticsTypeDef]
    lastUpdatedTime: NotRequired[str]
    createdTime: NotRequired[str]
    arn: NotRequired[str]
    eventOrchestration: NotRequired[EventOrchestrationTypeDef]

class ExternalModelOutputsTypeDef(TypedDict):
    externalModel: NotRequired[ExternalModelSummaryTypeDef]
    outputs: NotRequired[Dict[str, str]]

class ExternalModelTypeDef(TypedDict):
    modelEndpoint: NotRequired[str]
    modelSource: NotRequired[Literal["SAGEMAKER"]]
    invokeModelEndpointRoleArn: NotRequired[str]
    inputConfiguration: NotRequired[ModelInputConfigurationTypeDef]
    outputConfiguration: NotRequired[ModelOutputConfigurationOutputTypeDef]
    modelEndpointStatus: NotRequired[ModelEndpointStatusType]
    lastUpdatedTime: NotRequired[str]
    createdTime: NotRequired[str]
    arn: NotRequired[str]

class GetKMSEncryptionKeyResultTypeDef(TypedDict):
    kmsKey: KMSKeyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetLabelsResultTypeDef(TypedDict):
    labels: List[LabelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetModelsResultTypeDef(TypedDict):
    models: List[ModelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetOutcomesResultTypeDef(TypedDict):
    outcomes: List[OutcomeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetRulesResultTypeDef(TypedDict):
    ruleDetails: List[RuleDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class IngestedEventsDetailTypeDef(TypedDict):
    ingestedEventsTimeWindow: IngestedEventsTimeWindowTypeDef

class TrainingDataSchemaOutputTypeDef(TypedDict):
    modelVariables: List[str]
    labelSchema: NotRequired[LabelSchemaOutputTypeDef]

LabelSchemaUnionTypeDef = Union[LabelSchemaTypeDef, LabelSchemaOutputTypeDef]

class ListEventPredictionsRequestRequestTypeDef(TypedDict):
    eventId: NotRequired[FilterConditionTypeDef]
    eventType: NotRequired[FilterConditionTypeDef]
    detectorId: NotRequired[FilterConditionTypeDef]
    detectorVersionId: NotRequired[FilterConditionTypeDef]
    predictionTimeRange: NotRequired[PredictionTimeRangeTypeDef]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class VariableImportanceMetricsTypeDef(TypedDict):
    logOddsMetrics: NotRequired[List[LogOddsMetricTypeDef]]

class TrainingMetricsTypeDef(TypedDict):
    auc: NotRequired[float]
    metricDataPoints: NotRequired[List[MetricDataPointTypeDef]]

class PutExternalModelRequestRequestTypeDef(TypedDict):
    modelEndpoint: str
    modelSource: Literal["SAGEMAKER"]
    invokeModelEndpointRoleArn: str
    inputConfiguration: ModelInputConfigurationTypeDef
    outputConfiguration: ModelOutputConfigurationTypeDef
    modelEndpointStatus: ModelEndpointStatusType
    tags: NotRequired[Sequence[TagTypeDef]]

class OFIModelPerformanceTypeDef(TypedDict):
    auc: NotRequired[float]
    uncertaintyRange: NotRequired[UncertaintyRangeTypeDef]

class TFIModelPerformanceTypeDef(TypedDict):
    auc: NotRequired[float]
    uncertaintyRange: NotRequired[UncertaintyRangeTypeDef]

class PredictionExplanationsTypeDef(TypedDict):
    variableImpactExplanations: NotRequired[List[VariableImpactExplanationTypeDef]]
    aggregatedVariablesImpactExplanations: NotRequired[
        List[AggregatedVariablesImpactExplanationTypeDef]
    ]

class GetEventPredictionRequestRequestTypeDef(TypedDict):
    detectorId: str
    eventId: str
    eventTypeName: str
    entities: Sequence[EntityTypeDef]
    eventTimestamp: str
    eventVariables: Mapping[str, str]
    detectorVersionId: NotRequired[str]
    externalModelEndpointDataBlobs: NotRequired[Mapping[str, ModelEndpointDataBlobTypeDef]]

class GetEventResultTypeDef(TypedDict):
    event: EventTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetEventTypesResultTypeDef(TypedDict):
    eventTypes: List[EventTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetEventPredictionResultTypeDef(TypedDict):
    modelScores: List[ModelScoresTypeDef]
    ruleResults: List[RuleResultTypeDef]
    externalModelOutputs: List[ExternalModelOutputsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetExternalModelsResultTypeDef(TypedDict):
    externalModels: List[ExternalModelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateModelVersionRequestRequestTypeDef(TypedDict):
    modelId: str
    modelType: ModelTypeEnumType
    majorVersionNumber: str
    externalEventsDetail: NotRequired[ExternalEventsDetailTypeDef]
    ingestedEventsDetail: NotRequired[IngestedEventsDetailTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]

class GetModelVersionResultTypeDef(TypedDict):
    modelId: str
    modelType: ModelTypeEnumType
    modelVersionNumber: str
    trainingDataSource: TrainingDataSourceEnumType
    trainingDataSchema: TrainingDataSchemaOutputTypeDef
    externalEventsDetail: ExternalEventsDetailTypeDef
    ingestedEventsDetail: IngestedEventsDetailTypeDef
    status: str
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class TrainingDataSchemaTypeDef(TypedDict):
    modelVariables: Sequence[str]
    labelSchema: NotRequired[LabelSchemaUnionTypeDef]

class TrainingResultTypeDef(TypedDict):
    dataValidationMetrics: NotRequired[DataValidationMetricsTypeDef]
    trainingMetrics: NotRequired[TrainingMetricsTypeDef]
    variableImportanceMetrics: NotRequired[VariableImportanceMetricsTypeDef]

class OFITrainingMetricsValueTypeDef(TypedDict):
    metricDataPoints: NotRequired[List[OFIMetricDataPointTypeDef]]
    modelPerformance: NotRequired[OFIModelPerformanceTypeDef]

class TFITrainingMetricsValueTypeDef(TypedDict):
    metricDataPoints: NotRequired[List[TFIMetricDataPointTypeDef]]
    modelPerformance: NotRequired[TFIModelPerformanceTypeDef]

class ModelVersionEvaluationTypeDef(TypedDict):
    outputVariableName: NotRequired[str]
    evaluationScore: NotRequired[str]
    predictionExplanations: NotRequired[PredictionExplanationsTypeDef]

class CreateModelVersionRequestRequestTypeDef(TypedDict):
    modelId: str
    modelType: ModelTypeEnumType
    trainingDataSource: TrainingDataSourceEnumType
    trainingDataSchema: TrainingDataSchemaTypeDef
    externalEventsDetail: NotRequired[ExternalEventsDetailTypeDef]
    ingestedEventsDetail: NotRequired[IngestedEventsDetailTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]

class TrainingMetricsV2TypeDef(TypedDict):
    ofi: NotRequired[OFITrainingMetricsValueTypeDef]
    tfi: NotRequired[TFITrainingMetricsValueTypeDef]
    ati: NotRequired[ATITrainingMetricsValueTypeDef]

class EvaluatedModelVersionTypeDef(TypedDict):
    modelId: NotRequired[str]
    modelVersion: NotRequired[str]
    modelType: NotRequired[str]
    evaluations: NotRequired[List[ModelVersionEvaluationTypeDef]]

class TrainingResultV2TypeDef(TypedDict):
    dataValidationMetrics: NotRequired[DataValidationMetricsTypeDef]
    trainingMetricsV2: NotRequired[TrainingMetricsV2TypeDef]
    variableImportanceMetrics: NotRequired[VariableImportanceMetricsTypeDef]
    aggregatedVariablesImportanceMetrics: NotRequired[AggregatedVariablesImportanceMetricsTypeDef]

class GetEventPredictionMetadataResultTypeDef(TypedDict):
    eventId: str
    eventTypeName: str
    entityId: str
    entityType: str
    eventTimestamp: str
    detectorId: str
    detectorVersionId: str
    detectorVersionStatus: str
    eventVariables: List[EventVariableSummaryTypeDef]
    rules: List[EvaluatedRuleTypeDef]
    ruleExecutionMode: RuleExecutionModeType
    outcomes: List[str]
    evaluatedModelVersions: List[EvaluatedModelVersionTypeDef]
    evaluatedExternalModels: List[EvaluatedExternalModelTypeDef]
    predictionTimestamp: str
    ResponseMetadata: ResponseMetadataTypeDef

class ModelVersionDetailTypeDef(TypedDict):
    modelId: NotRequired[str]
    modelType: NotRequired[ModelTypeEnumType]
    modelVersionNumber: NotRequired[str]
    status: NotRequired[str]
    trainingDataSource: NotRequired[TrainingDataSourceEnumType]
    trainingDataSchema: NotRequired[TrainingDataSchemaOutputTypeDef]
    externalEventsDetail: NotRequired[ExternalEventsDetailTypeDef]
    ingestedEventsDetail: NotRequired[IngestedEventsDetailTypeDef]
    trainingResult: NotRequired[TrainingResultTypeDef]
    lastUpdatedTime: NotRequired[str]
    createdTime: NotRequired[str]
    arn: NotRequired[str]
    trainingResultV2: NotRequired[TrainingResultV2TypeDef]

class DescribeModelVersionsResultTypeDef(TypedDict):
    modelVersionDetails: List[ModelVersionDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
