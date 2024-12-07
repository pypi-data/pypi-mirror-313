"""
Type annotations for iotevents service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/type_defs/)

Usage::

    ```python
    from mypy_boto3_iotevents.type_defs import AcknowledgeFlowTypeDef

    data: AcknowledgeFlowTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AlarmModelVersionStatusType,
    AnalysisResultLevelType,
    AnalysisStatusType,
    ComparisonOperatorType,
    DetectorModelVersionStatusType,
    EvaluationMethodType,
    InputStatusType,
    LoggingLevelType,
    PayloadTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AcknowledgeFlowTypeDef",
    "ActionTypeDef",
    "AlarmActionTypeDef",
    "AlarmCapabilitiesTypeDef",
    "AlarmEventActionsOutputTypeDef",
    "AlarmEventActionsTypeDef",
    "AlarmModelSummaryTypeDef",
    "AlarmModelVersionSummaryTypeDef",
    "AlarmNotificationOutputTypeDef",
    "AlarmNotificationTypeDef",
    "AlarmRuleTypeDef",
    "AnalysisResultLocationTypeDef",
    "AnalysisResultTypeDef",
    "AssetPropertyTimestampTypeDef",
    "AssetPropertyValueTypeDef",
    "AssetPropertyVariantTypeDef",
    "AttributeTypeDef",
    "ClearTimerActionTypeDef",
    "CreateAlarmModelRequestRequestTypeDef",
    "CreateAlarmModelResponseTypeDef",
    "CreateDetectorModelRequestRequestTypeDef",
    "CreateDetectorModelResponseTypeDef",
    "CreateInputRequestRequestTypeDef",
    "CreateInputResponseTypeDef",
    "DeleteAlarmModelRequestRequestTypeDef",
    "DeleteDetectorModelRequestRequestTypeDef",
    "DeleteInputRequestRequestTypeDef",
    "DescribeAlarmModelRequestRequestTypeDef",
    "DescribeAlarmModelResponseTypeDef",
    "DescribeDetectorModelAnalysisRequestRequestTypeDef",
    "DescribeDetectorModelAnalysisResponseTypeDef",
    "DescribeDetectorModelRequestRequestTypeDef",
    "DescribeDetectorModelResponseTypeDef",
    "DescribeInputRequestRequestTypeDef",
    "DescribeInputResponseTypeDef",
    "DescribeLoggingOptionsResponseTypeDef",
    "DetectorDebugOptionTypeDef",
    "DetectorModelConfigurationTypeDef",
    "DetectorModelDefinitionOutputTypeDef",
    "DetectorModelDefinitionTypeDef",
    "DetectorModelSummaryTypeDef",
    "DetectorModelTypeDef",
    "DetectorModelVersionSummaryTypeDef",
    "DynamoDBActionTypeDef",
    "DynamoDBv2ActionTypeDef",
    "EmailConfigurationOutputTypeDef",
    "EmailConfigurationTypeDef",
    "EmailConfigurationUnionTypeDef",
    "EmailContentTypeDef",
    "EmailRecipientsOutputTypeDef",
    "EmailRecipientsTypeDef",
    "EmailRecipientsUnionTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EventOutputTypeDef",
    "EventTypeDef",
    "EventUnionTypeDef",
    "FirehoseActionTypeDef",
    "GetDetectorModelAnalysisResultsRequestRequestTypeDef",
    "GetDetectorModelAnalysisResultsResponseTypeDef",
    "InitializationConfigurationTypeDef",
    "InputConfigurationTypeDef",
    "InputDefinitionOutputTypeDef",
    "InputDefinitionTypeDef",
    "InputIdentifierTypeDef",
    "InputSummaryTypeDef",
    "InputTypeDef",
    "IotEventsActionTypeDef",
    "IotEventsInputIdentifierTypeDef",
    "IotSiteWiseActionTypeDef",
    "IotSiteWiseAssetModelPropertyIdentifierTypeDef",
    "IotSiteWiseInputIdentifierTypeDef",
    "IotTopicPublishActionTypeDef",
    "LambdaActionTypeDef",
    "ListAlarmModelVersionsRequestRequestTypeDef",
    "ListAlarmModelVersionsResponseTypeDef",
    "ListAlarmModelsRequestRequestTypeDef",
    "ListAlarmModelsResponseTypeDef",
    "ListDetectorModelVersionsRequestRequestTypeDef",
    "ListDetectorModelVersionsResponseTypeDef",
    "ListDetectorModelsRequestRequestTypeDef",
    "ListDetectorModelsResponseTypeDef",
    "ListInputRoutingsRequestRequestTypeDef",
    "ListInputRoutingsResponseTypeDef",
    "ListInputsRequestRequestTypeDef",
    "ListInputsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LoggingOptionsOutputTypeDef",
    "LoggingOptionsTypeDef",
    "NotificationActionOutputTypeDef",
    "NotificationActionTypeDef",
    "NotificationActionUnionTypeDef",
    "NotificationTargetActionsTypeDef",
    "OnEnterLifecycleOutputTypeDef",
    "OnEnterLifecycleTypeDef",
    "OnEnterLifecycleUnionTypeDef",
    "OnExitLifecycleOutputTypeDef",
    "OnExitLifecycleTypeDef",
    "OnExitLifecycleUnionTypeDef",
    "OnInputLifecycleOutputTypeDef",
    "OnInputLifecycleTypeDef",
    "OnInputLifecycleUnionTypeDef",
    "PayloadTypeDef",
    "PutLoggingOptionsRequestRequestTypeDef",
    "RecipientDetailTypeDef",
    "ResetTimerActionTypeDef",
    "ResponseMetadataTypeDef",
    "RoutedResourceTypeDef",
    "SMSConfigurationOutputTypeDef",
    "SMSConfigurationTypeDef",
    "SMSConfigurationUnionTypeDef",
    "SNSTopicPublishActionTypeDef",
    "SSOIdentityTypeDef",
    "SetTimerActionTypeDef",
    "SetVariableActionTypeDef",
    "SimpleRuleTypeDef",
    "SqsActionTypeDef",
    "StartDetectorModelAnalysisRequestRequestTypeDef",
    "StartDetectorModelAnalysisResponseTypeDef",
    "StateOutputTypeDef",
    "StateTypeDef",
    "StateUnionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TransitionEventOutputTypeDef",
    "TransitionEventTypeDef",
    "TransitionEventUnionTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAlarmModelRequestRequestTypeDef",
    "UpdateAlarmModelResponseTypeDef",
    "UpdateDetectorModelRequestRequestTypeDef",
    "UpdateDetectorModelResponseTypeDef",
    "UpdateInputRequestRequestTypeDef",
    "UpdateInputResponseTypeDef",
)

class AcknowledgeFlowTypeDef(TypedDict):
    enabled: bool

class ClearTimerActionTypeDef(TypedDict):
    timerName: str

class ResetTimerActionTypeDef(TypedDict):
    timerName: str

class SetTimerActionTypeDef(TypedDict):
    timerName: str
    seconds: NotRequired[int]
    durationExpression: NotRequired[str]

class SetVariableActionTypeDef(TypedDict):
    variableName: str
    value: str

class InitializationConfigurationTypeDef(TypedDict):
    disabledOnInitialization: bool

class AlarmModelSummaryTypeDef(TypedDict):
    creationTime: NotRequired[datetime]
    alarmModelDescription: NotRequired[str]
    alarmModelName: NotRequired[str]

class AlarmModelVersionSummaryTypeDef(TypedDict):
    alarmModelName: NotRequired[str]
    alarmModelArn: NotRequired[str]
    alarmModelVersion: NotRequired[str]
    roleArn: NotRequired[str]
    creationTime: NotRequired[datetime]
    lastUpdateTime: NotRequired[datetime]
    status: NotRequired[AlarmModelVersionStatusType]
    statusMessage: NotRequired[str]

class SimpleRuleTypeDef(TypedDict):
    inputProperty: str
    comparisonOperator: ComparisonOperatorType
    threshold: str

class AnalysisResultLocationTypeDef(TypedDict):
    path: NotRequired[str]

class AssetPropertyTimestampTypeDef(TypedDict):
    timeInSeconds: str
    offsetInNanos: NotRequired[str]

class AssetPropertyVariantTypeDef(TypedDict):
    stringValue: NotRequired[str]
    integerValue: NotRequired[str]
    doubleValue: NotRequired[str]
    booleanValue: NotRequired[str]

class AttributeTypeDef(TypedDict):
    jsonPath: str

class TagTypeDef(TypedDict):
    key: str
    value: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DetectorModelConfigurationTypeDef(TypedDict):
    detectorModelName: NotRequired[str]
    detectorModelVersion: NotRequired[str]
    detectorModelDescription: NotRequired[str]
    detectorModelArn: NotRequired[str]
    roleArn: NotRequired[str]
    creationTime: NotRequired[datetime]
    lastUpdateTime: NotRequired[datetime]
    status: NotRequired[DetectorModelVersionStatusType]
    key: NotRequired[str]
    evaluationMethod: NotRequired[EvaluationMethodType]

class InputConfigurationTypeDef(TypedDict):
    inputName: str
    inputArn: str
    creationTime: datetime
    lastUpdateTime: datetime
    status: InputStatusType
    inputDescription: NotRequired[str]

class DeleteAlarmModelRequestRequestTypeDef(TypedDict):
    alarmModelName: str

class DeleteDetectorModelRequestRequestTypeDef(TypedDict):
    detectorModelName: str

class DeleteInputRequestRequestTypeDef(TypedDict):
    inputName: str

class DescribeAlarmModelRequestRequestTypeDef(TypedDict):
    alarmModelName: str
    alarmModelVersion: NotRequired[str]

class DescribeDetectorModelAnalysisRequestRequestTypeDef(TypedDict):
    analysisId: str

class DescribeDetectorModelRequestRequestTypeDef(TypedDict):
    detectorModelName: str
    detectorModelVersion: NotRequired[str]

class DescribeInputRequestRequestTypeDef(TypedDict):
    inputName: str

class DetectorDebugOptionTypeDef(TypedDict):
    detectorModelName: str
    keyValue: NotRequired[str]

class DetectorModelSummaryTypeDef(TypedDict):
    detectorModelName: NotRequired[str]
    detectorModelDescription: NotRequired[str]
    creationTime: NotRequired[datetime]

class DetectorModelVersionSummaryTypeDef(TypedDict):
    detectorModelName: NotRequired[str]
    detectorModelVersion: NotRequired[str]
    detectorModelArn: NotRequired[str]
    roleArn: NotRequired[str]
    creationTime: NotRequired[datetime]
    lastUpdateTime: NotRequired[datetime]
    status: NotRequired[DetectorModelVersionStatusType]
    evaluationMethod: NotRequired[EvaluationMethodType]

PayloadTypeDef = TypedDict(
    "PayloadTypeDef",
    {
        "contentExpression": str,
        "type": PayloadTypeType,
    },
)

class EmailContentTypeDef(TypedDict):
    subject: NotRequired[str]
    additionalMessage: NotRequired[str]

class GetDetectorModelAnalysisResultsRequestRequestTypeDef(TypedDict):
    analysisId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class IotEventsInputIdentifierTypeDef(TypedDict):
    inputName: str

class InputSummaryTypeDef(TypedDict):
    inputName: NotRequired[str]
    inputDescription: NotRequired[str]
    inputArn: NotRequired[str]
    creationTime: NotRequired[datetime]
    lastUpdateTime: NotRequired[datetime]
    status: NotRequired[InputStatusType]

class IotSiteWiseAssetModelPropertyIdentifierTypeDef(TypedDict):
    assetModelId: str
    propertyId: str

class ListAlarmModelVersionsRequestRequestTypeDef(TypedDict):
    alarmModelName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListAlarmModelsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListDetectorModelVersionsRequestRequestTypeDef(TypedDict):
    detectorModelName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListDetectorModelsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class RoutedResourceTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]

class ListInputsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class SSOIdentityTypeDef(TypedDict):
    identityStoreId: str
    userId: NotRequired[str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class AlarmCapabilitiesTypeDef(TypedDict):
    initializationConfiguration: NotRequired[InitializationConfigurationTypeDef]
    acknowledgeFlow: NotRequired[AcknowledgeFlowTypeDef]

class AlarmRuleTypeDef(TypedDict):
    simpleRule: NotRequired[SimpleRuleTypeDef]

AnalysisResultTypeDef = TypedDict(
    "AnalysisResultTypeDef",
    {
        "type": NotRequired[str],
        "level": NotRequired[AnalysisResultLevelType],
        "message": NotRequired[str],
        "locations": NotRequired[List[AnalysisResultLocationTypeDef]],
    },
)

class AssetPropertyValueTypeDef(TypedDict):
    value: NotRequired[AssetPropertyVariantTypeDef]
    timestamp: NotRequired[AssetPropertyTimestampTypeDef]
    quality: NotRequired[str]

class InputDefinitionOutputTypeDef(TypedDict):
    attributes: List[AttributeTypeDef]

class InputDefinitionTypeDef(TypedDict):
    attributes: Sequence[AttributeTypeDef]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]

class CreateAlarmModelResponseTypeDef(TypedDict):
    creationTime: datetime
    alarmModelArn: str
    alarmModelVersion: str
    lastUpdateTime: datetime
    status: AlarmModelVersionStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeDetectorModelAnalysisResponseTypeDef(TypedDict):
    status: AnalysisStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ListAlarmModelVersionsResponseTypeDef(TypedDict):
    alarmModelVersionSummaries: List[AlarmModelVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAlarmModelsResponseTypeDef(TypedDict):
    alarmModelSummaries: List[AlarmModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StartDetectorModelAnalysisResponseTypeDef(TypedDict):
    analysisId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAlarmModelResponseTypeDef(TypedDict):
    creationTime: datetime
    alarmModelArn: str
    alarmModelVersion: str
    lastUpdateTime: datetime
    status: AlarmModelVersionStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDetectorModelResponseTypeDef(TypedDict):
    detectorModelConfiguration: DetectorModelConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDetectorModelResponseTypeDef(TypedDict):
    detectorModelConfiguration: DetectorModelConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateInputResponseTypeDef(TypedDict):
    inputConfiguration: InputConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateInputResponseTypeDef(TypedDict):
    inputConfiguration: InputConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class LoggingOptionsOutputTypeDef(TypedDict):
    roleArn: str
    level: LoggingLevelType
    enabled: bool
    detectorDebugOptions: NotRequired[List[DetectorDebugOptionTypeDef]]

class LoggingOptionsTypeDef(TypedDict):
    roleArn: str
    level: LoggingLevelType
    enabled: bool
    detectorDebugOptions: NotRequired[Sequence[DetectorDebugOptionTypeDef]]

class ListDetectorModelsResponseTypeDef(TypedDict):
    detectorModelSummaries: List[DetectorModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDetectorModelVersionsResponseTypeDef(TypedDict):
    detectorModelVersionSummaries: List[DetectorModelVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DynamoDBActionTypeDef(TypedDict):
    hashKeyField: str
    hashKeyValue: str
    tableName: str
    hashKeyType: NotRequired[str]
    rangeKeyType: NotRequired[str]
    rangeKeyField: NotRequired[str]
    rangeKeyValue: NotRequired[str]
    operation: NotRequired[str]
    payloadField: NotRequired[str]
    payload: NotRequired[PayloadTypeDef]

class DynamoDBv2ActionTypeDef(TypedDict):
    tableName: str
    payload: NotRequired[PayloadTypeDef]

class FirehoseActionTypeDef(TypedDict):
    deliveryStreamName: str
    separator: NotRequired[str]
    payload: NotRequired[PayloadTypeDef]

class IotEventsActionTypeDef(TypedDict):
    inputName: str
    payload: NotRequired[PayloadTypeDef]

class IotTopicPublishActionTypeDef(TypedDict):
    mqttTopic: str
    payload: NotRequired[PayloadTypeDef]

class LambdaActionTypeDef(TypedDict):
    functionArn: str
    payload: NotRequired[PayloadTypeDef]

class SNSTopicPublishActionTypeDef(TypedDict):
    targetArn: str
    payload: NotRequired[PayloadTypeDef]

class SqsActionTypeDef(TypedDict):
    queueUrl: str
    useBase64: NotRequired[bool]
    payload: NotRequired[PayloadTypeDef]

class ListInputsResponseTypeDef(TypedDict):
    inputSummaries: List[InputSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class IotSiteWiseInputIdentifierTypeDef(TypedDict):
    iotSiteWiseAssetModelPropertyIdentifier: NotRequired[
        IotSiteWiseAssetModelPropertyIdentifierTypeDef
    ]

class ListInputRoutingsResponseTypeDef(TypedDict):
    routedResources: List[RoutedResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class RecipientDetailTypeDef(TypedDict):
    ssoIdentity: NotRequired[SSOIdentityTypeDef]

class GetDetectorModelAnalysisResultsResponseTypeDef(TypedDict):
    analysisResults: List[AnalysisResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class IotSiteWiseActionTypeDef(TypedDict):
    entryId: NotRequired[str]
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]
    propertyValue: NotRequired[AssetPropertyValueTypeDef]

class InputTypeDef(TypedDict):
    inputConfiguration: NotRequired[InputConfigurationTypeDef]
    inputDefinition: NotRequired[InputDefinitionOutputTypeDef]

class CreateInputRequestRequestTypeDef(TypedDict):
    inputName: str
    inputDefinition: InputDefinitionTypeDef
    inputDescription: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class UpdateInputRequestRequestTypeDef(TypedDict):
    inputName: str
    inputDefinition: InputDefinitionTypeDef
    inputDescription: NotRequired[str]

class DescribeLoggingOptionsResponseTypeDef(TypedDict):
    loggingOptions: LoggingOptionsOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutLoggingOptionsRequestRequestTypeDef(TypedDict):
    loggingOptions: LoggingOptionsTypeDef

class NotificationTargetActionsTypeDef(TypedDict):
    lambdaAction: NotRequired[LambdaActionTypeDef]

class InputIdentifierTypeDef(TypedDict):
    iotEventsInputIdentifier: NotRequired[IotEventsInputIdentifierTypeDef]
    iotSiteWiseInputIdentifier: NotRequired[IotSiteWiseInputIdentifierTypeDef]

class EmailRecipientsOutputTypeDef(TypedDict):
    to: NotRequired[List[RecipientDetailTypeDef]]

class EmailRecipientsTypeDef(TypedDict):
    to: NotRequired[Sequence[RecipientDetailTypeDef]]

class SMSConfigurationOutputTypeDef(TypedDict):
    recipients: List[RecipientDetailTypeDef]
    senderId: NotRequired[str]
    additionalMessage: NotRequired[str]

class SMSConfigurationTypeDef(TypedDict):
    recipients: Sequence[RecipientDetailTypeDef]
    senderId: NotRequired[str]
    additionalMessage: NotRequired[str]

ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "setVariable": NotRequired[SetVariableActionTypeDef],
        "sns": NotRequired[SNSTopicPublishActionTypeDef],
        "iotTopicPublish": NotRequired[IotTopicPublishActionTypeDef],
        "setTimer": NotRequired[SetTimerActionTypeDef],
        "clearTimer": NotRequired[ClearTimerActionTypeDef],
        "resetTimer": NotRequired[ResetTimerActionTypeDef],
        "lambda": NotRequired[LambdaActionTypeDef],
        "iotEvents": NotRequired[IotEventsActionTypeDef],
        "sqs": NotRequired[SqsActionTypeDef],
        "firehose": NotRequired[FirehoseActionTypeDef],
        "dynamoDB": NotRequired[DynamoDBActionTypeDef],
        "dynamoDBv2": NotRequired[DynamoDBv2ActionTypeDef],
        "iotSiteWise": NotRequired[IotSiteWiseActionTypeDef],
    },
)
AlarmActionTypeDef = TypedDict(
    "AlarmActionTypeDef",
    {
        "sns": NotRequired[SNSTopicPublishActionTypeDef],
        "iotTopicPublish": NotRequired[IotTopicPublishActionTypeDef],
        "lambda": NotRequired[LambdaActionTypeDef],
        "iotEvents": NotRequired[IotEventsActionTypeDef],
        "sqs": NotRequired[SqsActionTypeDef],
        "firehose": NotRequired[FirehoseActionTypeDef],
        "dynamoDB": NotRequired[DynamoDBActionTypeDef],
        "dynamoDBv2": NotRequired[DynamoDBv2ActionTypeDef],
        "iotSiteWise": NotRequired[IotSiteWiseActionTypeDef],
    },
)
DescribeInputResponseTypeDef = TypedDict(
    "DescribeInputResponseTypeDef",
    {
        "input": InputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ListInputRoutingsRequestRequestTypeDef(TypedDict):
    inputIdentifier: InputIdentifierTypeDef
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

EmailConfigurationOutputTypeDef = TypedDict(
    "EmailConfigurationOutputTypeDef",
    {
        "from": str,
        "recipients": EmailRecipientsOutputTypeDef,
        "content": NotRequired[EmailContentTypeDef],
    },
)
EmailRecipientsUnionTypeDef = Union[EmailRecipientsTypeDef, EmailRecipientsOutputTypeDef]
SMSConfigurationUnionTypeDef = Union[SMSConfigurationTypeDef, SMSConfigurationOutputTypeDef]

class EventOutputTypeDef(TypedDict):
    eventName: str
    condition: NotRequired[str]
    actions: NotRequired[List[ActionTypeDef]]

class EventTypeDef(TypedDict):
    eventName: str
    condition: NotRequired[str]
    actions: NotRequired[Sequence[ActionTypeDef]]

class TransitionEventOutputTypeDef(TypedDict):
    eventName: str
    condition: str
    nextState: str
    actions: NotRequired[List[ActionTypeDef]]

class TransitionEventTypeDef(TypedDict):
    eventName: str
    condition: str
    nextState: str
    actions: NotRequired[Sequence[ActionTypeDef]]

class AlarmEventActionsOutputTypeDef(TypedDict):
    alarmActions: NotRequired[List[AlarmActionTypeDef]]

class AlarmEventActionsTypeDef(TypedDict):
    alarmActions: NotRequired[Sequence[AlarmActionTypeDef]]

class NotificationActionOutputTypeDef(TypedDict):
    action: NotificationTargetActionsTypeDef
    smsConfigurations: NotRequired[List[SMSConfigurationOutputTypeDef]]
    emailConfigurations: NotRequired[List[EmailConfigurationOutputTypeDef]]

EmailConfigurationTypeDef = TypedDict(
    "EmailConfigurationTypeDef",
    {
        "from": str,
        "recipients": EmailRecipientsUnionTypeDef,
        "content": NotRequired[EmailContentTypeDef],
    },
)

class OnEnterLifecycleOutputTypeDef(TypedDict):
    events: NotRequired[List[EventOutputTypeDef]]

class OnExitLifecycleOutputTypeDef(TypedDict):
    events: NotRequired[List[EventOutputTypeDef]]

EventUnionTypeDef = Union[EventTypeDef, EventOutputTypeDef]

class OnEnterLifecycleTypeDef(TypedDict):
    events: NotRequired[Sequence[EventTypeDef]]

class OnExitLifecycleTypeDef(TypedDict):
    events: NotRequired[Sequence[EventTypeDef]]

class OnInputLifecycleOutputTypeDef(TypedDict):
    events: NotRequired[List[EventOutputTypeDef]]
    transitionEvents: NotRequired[List[TransitionEventOutputTypeDef]]

TransitionEventUnionTypeDef = Union[TransitionEventTypeDef, TransitionEventOutputTypeDef]

class AlarmNotificationOutputTypeDef(TypedDict):
    notificationActions: NotRequired[List[NotificationActionOutputTypeDef]]

EmailConfigurationUnionTypeDef = Union[EmailConfigurationTypeDef, EmailConfigurationOutputTypeDef]
OnEnterLifecycleUnionTypeDef = Union[OnEnterLifecycleTypeDef, OnEnterLifecycleOutputTypeDef]
OnExitLifecycleUnionTypeDef = Union[OnExitLifecycleTypeDef, OnExitLifecycleOutputTypeDef]

class StateOutputTypeDef(TypedDict):
    stateName: str
    onInput: NotRequired[OnInputLifecycleOutputTypeDef]
    onEnter: NotRequired[OnEnterLifecycleOutputTypeDef]
    onExit: NotRequired[OnExitLifecycleOutputTypeDef]

class OnInputLifecycleTypeDef(TypedDict):
    events: NotRequired[Sequence[EventUnionTypeDef]]
    transitionEvents: NotRequired[Sequence[TransitionEventUnionTypeDef]]

class DescribeAlarmModelResponseTypeDef(TypedDict):
    creationTime: datetime
    alarmModelArn: str
    alarmModelVersion: str
    lastUpdateTime: datetime
    status: AlarmModelVersionStatusType
    statusMessage: str
    alarmModelName: str
    alarmModelDescription: str
    roleArn: str
    key: str
    severity: int
    alarmRule: AlarmRuleTypeDef
    alarmNotification: AlarmNotificationOutputTypeDef
    alarmEventActions: AlarmEventActionsOutputTypeDef
    alarmCapabilities: AlarmCapabilitiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class NotificationActionTypeDef(TypedDict):
    action: NotificationTargetActionsTypeDef
    smsConfigurations: NotRequired[Sequence[SMSConfigurationUnionTypeDef]]
    emailConfigurations: NotRequired[Sequence[EmailConfigurationUnionTypeDef]]

class DetectorModelDefinitionOutputTypeDef(TypedDict):
    states: List[StateOutputTypeDef]
    initialStateName: str

OnInputLifecycleUnionTypeDef = Union[OnInputLifecycleTypeDef, OnInputLifecycleOutputTypeDef]
NotificationActionUnionTypeDef = Union[NotificationActionTypeDef, NotificationActionOutputTypeDef]

class DetectorModelTypeDef(TypedDict):
    detectorModelDefinition: NotRequired[DetectorModelDefinitionOutputTypeDef]
    detectorModelConfiguration: NotRequired[DetectorModelConfigurationTypeDef]

class StateTypeDef(TypedDict):
    stateName: str
    onInput: NotRequired[OnInputLifecycleUnionTypeDef]
    onEnter: NotRequired[OnEnterLifecycleUnionTypeDef]
    onExit: NotRequired[OnExitLifecycleUnionTypeDef]

class AlarmNotificationTypeDef(TypedDict):
    notificationActions: NotRequired[Sequence[NotificationActionUnionTypeDef]]

class DescribeDetectorModelResponseTypeDef(TypedDict):
    detectorModel: DetectorModelTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

StateUnionTypeDef = Union[StateTypeDef, StateOutputTypeDef]

class CreateAlarmModelRequestRequestTypeDef(TypedDict):
    alarmModelName: str
    roleArn: str
    alarmRule: AlarmRuleTypeDef
    alarmModelDescription: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    key: NotRequired[str]
    severity: NotRequired[int]
    alarmNotification: NotRequired[AlarmNotificationTypeDef]
    alarmEventActions: NotRequired[AlarmEventActionsTypeDef]
    alarmCapabilities: NotRequired[AlarmCapabilitiesTypeDef]

class UpdateAlarmModelRequestRequestTypeDef(TypedDict):
    alarmModelName: str
    roleArn: str
    alarmRule: AlarmRuleTypeDef
    alarmModelDescription: NotRequired[str]
    severity: NotRequired[int]
    alarmNotification: NotRequired[AlarmNotificationTypeDef]
    alarmEventActions: NotRequired[AlarmEventActionsTypeDef]
    alarmCapabilities: NotRequired[AlarmCapabilitiesTypeDef]

class DetectorModelDefinitionTypeDef(TypedDict):
    states: Sequence[StateUnionTypeDef]
    initialStateName: str

class CreateDetectorModelRequestRequestTypeDef(TypedDict):
    detectorModelName: str
    detectorModelDefinition: DetectorModelDefinitionTypeDef
    roleArn: str
    detectorModelDescription: NotRequired[str]
    key: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    evaluationMethod: NotRequired[EvaluationMethodType]

class StartDetectorModelAnalysisRequestRequestTypeDef(TypedDict):
    detectorModelDefinition: DetectorModelDefinitionTypeDef

class UpdateDetectorModelRequestRequestTypeDef(TypedDict):
    detectorModelName: str
    detectorModelDefinition: DetectorModelDefinitionTypeDef
    roleArn: str
    detectorModelDescription: NotRequired[str]
    evaluationMethod: NotRequired[EvaluationMethodType]
