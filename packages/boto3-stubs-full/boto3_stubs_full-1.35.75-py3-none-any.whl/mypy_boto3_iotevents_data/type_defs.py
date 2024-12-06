"""
Type annotations for iotevents-data service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/type_defs/)

Usage::

    ```python
    from mypy_boto3_iotevents_data.type_defs import AcknowledgeActionConfigurationTypeDef

    data: AcknowledgeActionConfigurationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AlarmStateNameType,
    ComparisonOperatorType,
    CustomerActionNameType,
    ErrorCodeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AcknowledgeActionConfigurationTypeDef",
    "AcknowledgeAlarmActionRequestTypeDef",
    "AlarmStateTypeDef",
    "AlarmSummaryTypeDef",
    "AlarmTypeDef",
    "BatchAcknowledgeAlarmRequestRequestTypeDef",
    "BatchAcknowledgeAlarmResponseTypeDef",
    "BatchAlarmActionErrorEntryTypeDef",
    "BatchDeleteDetectorErrorEntryTypeDef",
    "BatchDeleteDetectorRequestRequestTypeDef",
    "BatchDeleteDetectorResponseTypeDef",
    "BatchDisableAlarmRequestRequestTypeDef",
    "BatchDisableAlarmResponseTypeDef",
    "BatchEnableAlarmRequestRequestTypeDef",
    "BatchEnableAlarmResponseTypeDef",
    "BatchPutMessageErrorEntryTypeDef",
    "BatchPutMessageRequestRequestTypeDef",
    "BatchPutMessageResponseTypeDef",
    "BatchResetAlarmRequestRequestTypeDef",
    "BatchResetAlarmResponseTypeDef",
    "BatchSnoozeAlarmRequestRequestTypeDef",
    "BatchSnoozeAlarmResponseTypeDef",
    "BatchUpdateDetectorErrorEntryTypeDef",
    "BatchUpdateDetectorRequestRequestTypeDef",
    "BatchUpdateDetectorResponseTypeDef",
    "BlobTypeDef",
    "CustomerActionTypeDef",
    "DeleteDetectorRequestTypeDef",
    "DescribeAlarmRequestRequestTypeDef",
    "DescribeAlarmResponseTypeDef",
    "DescribeDetectorRequestRequestTypeDef",
    "DescribeDetectorResponseTypeDef",
    "DetectorStateDefinitionTypeDef",
    "DetectorStateSummaryTypeDef",
    "DetectorStateTypeDef",
    "DetectorSummaryTypeDef",
    "DetectorTypeDef",
    "DisableActionConfigurationTypeDef",
    "DisableAlarmActionRequestTypeDef",
    "EnableActionConfigurationTypeDef",
    "EnableAlarmActionRequestTypeDef",
    "ListAlarmsRequestRequestTypeDef",
    "ListAlarmsResponseTypeDef",
    "ListDetectorsRequestRequestTypeDef",
    "ListDetectorsResponseTypeDef",
    "MessageTypeDef",
    "ResetActionConfigurationTypeDef",
    "ResetAlarmActionRequestTypeDef",
    "ResponseMetadataTypeDef",
    "RuleEvaluationTypeDef",
    "SimpleRuleEvaluationTypeDef",
    "SnoozeActionConfigurationTypeDef",
    "SnoozeAlarmActionRequestTypeDef",
    "StateChangeConfigurationTypeDef",
    "SystemEventTypeDef",
    "TimerDefinitionTypeDef",
    "TimerTypeDef",
    "TimestampValueTypeDef",
    "UpdateDetectorRequestTypeDef",
    "VariableDefinitionTypeDef",
    "VariableTypeDef",
)


class AcknowledgeActionConfigurationTypeDef(TypedDict):
    note: NotRequired[str]


class AcknowledgeAlarmActionRequestTypeDef(TypedDict):
    requestId: str
    alarmModelName: str
    keyValue: NotRequired[str]
    note: NotRequired[str]


class AlarmSummaryTypeDef(TypedDict):
    alarmModelName: NotRequired[str]
    alarmModelVersion: NotRequired[str]
    keyValue: NotRequired[str]
    stateName: NotRequired[AlarmStateNameType]
    creationTime: NotRequired[datetime]
    lastUpdateTime: NotRequired[datetime]


class BatchAlarmActionErrorEntryTypeDef(TypedDict):
    requestId: NotRequired[str]
    errorCode: NotRequired[ErrorCodeType]
    errorMessage: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class BatchDeleteDetectorErrorEntryTypeDef(TypedDict):
    messageId: NotRequired[str]
    errorCode: NotRequired[ErrorCodeType]
    errorMessage: NotRequired[str]


class DeleteDetectorRequestTypeDef(TypedDict):
    messageId: str
    detectorModelName: str
    keyValue: NotRequired[str]


class DisableAlarmActionRequestTypeDef(TypedDict):
    requestId: str
    alarmModelName: str
    keyValue: NotRequired[str]
    note: NotRequired[str]


class EnableAlarmActionRequestTypeDef(TypedDict):
    requestId: str
    alarmModelName: str
    keyValue: NotRequired[str]
    note: NotRequired[str]


class BatchPutMessageErrorEntryTypeDef(TypedDict):
    messageId: NotRequired[str]
    errorCode: NotRequired[ErrorCodeType]
    errorMessage: NotRequired[str]


class ResetAlarmActionRequestTypeDef(TypedDict):
    requestId: str
    alarmModelName: str
    keyValue: NotRequired[str]
    note: NotRequired[str]


class SnoozeAlarmActionRequestTypeDef(TypedDict):
    requestId: str
    alarmModelName: str
    snoozeDuration: int
    keyValue: NotRequired[str]
    note: NotRequired[str]


class BatchUpdateDetectorErrorEntryTypeDef(TypedDict):
    messageId: NotRequired[str]
    errorCode: NotRequired[ErrorCodeType]
    errorMessage: NotRequired[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class DisableActionConfigurationTypeDef(TypedDict):
    note: NotRequired[str]


class EnableActionConfigurationTypeDef(TypedDict):
    note: NotRequired[str]


class ResetActionConfigurationTypeDef(TypedDict):
    note: NotRequired[str]


class SnoozeActionConfigurationTypeDef(TypedDict):
    snoozeDuration: NotRequired[int]
    note: NotRequired[str]


class DescribeAlarmRequestRequestTypeDef(TypedDict):
    alarmModelName: str
    keyValue: NotRequired[str]


class DescribeDetectorRequestRequestTypeDef(TypedDict):
    detectorModelName: str
    keyValue: NotRequired[str]


class TimerDefinitionTypeDef(TypedDict):
    name: str
    seconds: int


class VariableDefinitionTypeDef(TypedDict):
    name: str
    value: str


class DetectorStateSummaryTypeDef(TypedDict):
    stateName: NotRequired[str]


class TimerTypeDef(TypedDict):
    name: str
    timestamp: datetime


class VariableTypeDef(TypedDict):
    name: str
    value: str


class ListAlarmsRequestRequestTypeDef(TypedDict):
    alarmModelName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDetectorsRequestRequestTypeDef(TypedDict):
    detectorModelName: str
    stateName: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class TimestampValueTypeDef(TypedDict):
    timeInMillis: NotRequired[int]


SimpleRuleEvaluationTypeDef = TypedDict(
    "SimpleRuleEvaluationTypeDef",
    {
        "inputPropertyValue": NotRequired[str],
        "operator": NotRequired[ComparisonOperatorType],
        "thresholdValue": NotRequired[str],
    },
)


class StateChangeConfigurationTypeDef(TypedDict):
    triggerType: NotRequired[Literal["SNOOZE_TIMEOUT"]]


class BatchAcknowledgeAlarmRequestRequestTypeDef(TypedDict):
    acknowledgeActionRequests: Sequence[AcknowledgeAlarmActionRequestTypeDef]


class BatchAcknowledgeAlarmResponseTypeDef(TypedDict):
    errorEntries: List[BatchAlarmActionErrorEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchDisableAlarmResponseTypeDef(TypedDict):
    errorEntries: List[BatchAlarmActionErrorEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchEnableAlarmResponseTypeDef(TypedDict):
    errorEntries: List[BatchAlarmActionErrorEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchResetAlarmResponseTypeDef(TypedDict):
    errorEntries: List[BatchAlarmActionErrorEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchSnoozeAlarmResponseTypeDef(TypedDict):
    errorEntries: List[BatchAlarmActionErrorEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListAlarmsResponseTypeDef(TypedDict):
    alarmSummaries: List[AlarmSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class BatchDeleteDetectorResponseTypeDef(TypedDict):
    batchDeleteDetectorErrorEntries: List[BatchDeleteDetectorErrorEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchDeleteDetectorRequestRequestTypeDef(TypedDict):
    detectors: Sequence[DeleteDetectorRequestTypeDef]


class BatchDisableAlarmRequestRequestTypeDef(TypedDict):
    disableActionRequests: Sequence[DisableAlarmActionRequestTypeDef]


class BatchEnableAlarmRequestRequestTypeDef(TypedDict):
    enableActionRequests: Sequence[EnableAlarmActionRequestTypeDef]


class BatchPutMessageResponseTypeDef(TypedDict):
    BatchPutMessageErrorEntries: List[BatchPutMessageErrorEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchResetAlarmRequestRequestTypeDef(TypedDict):
    resetActionRequests: Sequence[ResetAlarmActionRequestTypeDef]


class BatchSnoozeAlarmRequestRequestTypeDef(TypedDict):
    snoozeActionRequests: Sequence[SnoozeAlarmActionRequestTypeDef]


class BatchUpdateDetectorResponseTypeDef(TypedDict):
    batchUpdateDetectorErrorEntries: List[BatchUpdateDetectorErrorEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CustomerActionTypeDef(TypedDict):
    actionName: NotRequired[CustomerActionNameType]
    snoozeActionConfiguration: NotRequired[SnoozeActionConfigurationTypeDef]
    enableActionConfiguration: NotRequired[EnableActionConfigurationTypeDef]
    disableActionConfiguration: NotRequired[DisableActionConfigurationTypeDef]
    acknowledgeActionConfiguration: NotRequired[AcknowledgeActionConfigurationTypeDef]
    resetActionConfiguration: NotRequired[ResetActionConfigurationTypeDef]


class DetectorStateDefinitionTypeDef(TypedDict):
    stateName: str
    variables: Sequence[VariableDefinitionTypeDef]
    timers: Sequence[TimerDefinitionTypeDef]


class DetectorSummaryTypeDef(TypedDict):
    detectorModelName: NotRequired[str]
    keyValue: NotRequired[str]
    detectorModelVersion: NotRequired[str]
    state: NotRequired[DetectorStateSummaryTypeDef]
    creationTime: NotRequired[datetime]
    lastUpdateTime: NotRequired[datetime]


class DetectorStateTypeDef(TypedDict):
    stateName: str
    variables: List[VariableTypeDef]
    timers: List[TimerTypeDef]


class MessageTypeDef(TypedDict):
    messageId: str
    inputName: str
    payload: BlobTypeDef
    timestamp: NotRequired[TimestampValueTypeDef]


class RuleEvaluationTypeDef(TypedDict):
    simpleRuleEvaluation: NotRequired[SimpleRuleEvaluationTypeDef]


class SystemEventTypeDef(TypedDict):
    eventType: NotRequired[Literal["STATE_CHANGE"]]
    stateChangeConfiguration: NotRequired[StateChangeConfigurationTypeDef]


class UpdateDetectorRequestTypeDef(TypedDict):
    messageId: str
    detectorModelName: str
    state: DetectorStateDefinitionTypeDef
    keyValue: NotRequired[str]


class ListDetectorsResponseTypeDef(TypedDict):
    detectorSummaries: List[DetectorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DetectorTypeDef(TypedDict):
    detectorModelName: NotRequired[str]
    keyValue: NotRequired[str]
    detectorModelVersion: NotRequired[str]
    state: NotRequired[DetectorStateTypeDef]
    creationTime: NotRequired[datetime]
    lastUpdateTime: NotRequired[datetime]


class BatchPutMessageRequestRequestTypeDef(TypedDict):
    messages: Sequence[MessageTypeDef]


class AlarmStateTypeDef(TypedDict):
    stateName: NotRequired[AlarmStateNameType]
    ruleEvaluation: NotRequired[RuleEvaluationTypeDef]
    customerAction: NotRequired[CustomerActionTypeDef]
    systemEvent: NotRequired[SystemEventTypeDef]


class BatchUpdateDetectorRequestRequestTypeDef(TypedDict):
    detectors: Sequence[UpdateDetectorRequestTypeDef]


class DescribeDetectorResponseTypeDef(TypedDict):
    detector: DetectorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AlarmTypeDef(TypedDict):
    alarmModelName: NotRequired[str]
    alarmModelVersion: NotRequired[str]
    keyValue: NotRequired[str]
    alarmState: NotRequired[AlarmStateTypeDef]
    severity: NotRequired[int]
    creationTime: NotRequired[datetime]
    lastUpdateTime: NotRequired[datetime]


class DescribeAlarmResponseTypeDef(TypedDict):
    alarm: AlarmTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
