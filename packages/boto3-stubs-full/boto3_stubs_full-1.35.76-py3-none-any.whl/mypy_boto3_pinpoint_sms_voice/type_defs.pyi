"""
Type annotations for pinpoint-sms-voice service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice/type_defs/)

Usage::

    ```python
    from mypy_boto3_pinpoint_sms_voice.type_defs import CallInstructionsMessageTypeTypeDef

    data: CallInstructionsMessageTypeTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Sequence

from .literals import EventTypeType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "CallInstructionsMessageTypeTypeDef",
    "CloudWatchLogsDestinationTypeDef",
    "CreateConfigurationSetEventDestinationRequestRequestTypeDef",
    "CreateConfigurationSetRequestRequestTypeDef",
    "DeleteConfigurationSetEventDestinationRequestRequestTypeDef",
    "DeleteConfigurationSetRequestRequestTypeDef",
    "EventDestinationDefinitionTypeDef",
    "EventDestinationTypeDef",
    "GetConfigurationSetEventDestinationsRequestRequestTypeDef",
    "GetConfigurationSetEventDestinationsResponseTypeDef",
    "KinesisFirehoseDestinationTypeDef",
    "PlainTextMessageTypeTypeDef",
    "ResponseMetadataTypeDef",
    "SSMLMessageTypeTypeDef",
    "SendVoiceMessageRequestRequestTypeDef",
    "SendVoiceMessageResponseTypeDef",
    "SnsDestinationTypeDef",
    "UpdateConfigurationSetEventDestinationRequestRequestTypeDef",
    "VoiceMessageContentTypeDef",
)

CallInstructionsMessageTypeTypeDef = TypedDict(
    "CallInstructionsMessageTypeTypeDef",
    {
        "Text": NotRequired[str],
    },
)

class CloudWatchLogsDestinationTypeDef(TypedDict):
    IamRoleArn: NotRequired[str]
    LogGroupArn: NotRequired[str]

class CreateConfigurationSetRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: NotRequired[str]

class DeleteConfigurationSetEventDestinationRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    EventDestinationName: str

class DeleteConfigurationSetRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str

class KinesisFirehoseDestinationTypeDef(TypedDict):
    DeliveryStreamArn: NotRequired[str]
    IamRoleArn: NotRequired[str]

class SnsDestinationTypeDef(TypedDict):
    TopicArn: NotRequired[str]

class GetConfigurationSetEventDestinationsRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

PlainTextMessageTypeTypeDef = TypedDict(
    "PlainTextMessageTypeTypeDef",
    {
        "LanguageCode": NotRequired[str],
        "Text": NotRequired[str],
        "VoiceId": NotRequired[str],
    },
)
SSMLMessageTypeTypeDef = TypedDict(
    "SSMLMessageTypeTypeDef",
    {
        "LanguageCode": NotRequired[str],
        "Text": NotRequired[str],
        "VoiceId": NotRequired[str],
    },
)

class EventDestinationDefinitionTypeDef(TypedDict):
    CloudWatchLogsDestination: NotRequired[CloudWatchLogsDestinationTypeDef]
    Enabled: NotRequired[bool]
    KinesisFirehoseDestination: NotRequired[KinesisFirehoseDestinationTypeDef]
    MatchingEventTypes: NotRequired[Sequence[EventTypeType]]
    SnsDestination: NotRequired[SnsDestinationTypeDef]

class EventDestinationTypeDef(TypedDict):
    CloudWatchLogsDestination: NotRequired[CloudWatchLogsDestinationTypeDef]
    Enabled: NotRequired[bool]
    KinesisFirehoseDestination: NotRequired[KinesisFirehoseDestinationTypeDef]
    MatchingEventTypes: NotRequired[List[EventTypeType]]
    Name: NotRequired[str]
    SnsDestination: NotRequired[SnsDestinationTypeDef]

class SendVoiceMessageResponseTypeDef(TypedDict):
    MessageId: str
    ResponseMetadata: ResponseMetadataTypeDef

class VoiceMessageContentTypeDef(TypedDict):
    CallInstructionsMessage: NotRequired[CallInstructionsMessageTypeTypeDef]
    PlainTextMessage: NotRequired[PlainTextMessageTypeTypeDef]
    SSMLMessage: NotRequired[SSMLMessageTypeTypeDef]

class CreateConfigurationSetEventDestinationRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    EventDestination: NotRequired[EventDestinationDefinitionTypeDef]
    EventDestinationName: NotRequired[str]

class UpdateConfigurationSetEventDestinationRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    EventDestinationName: str
    EventDestination: NotRequired[EventDestinationDefinitionTypeDef]

class GetConfigurationSetEventDestinationsResponseTypeDef(TypedDict):
    EventDestinations: List[EventDestinationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class SendVoiceMessageRequestRequestTypeDef(TypedDict):
    CallerId: NotRequired[str]
    ConfigurationSetName: NotRequired[str]
    Content: NotRequired[VoiceMessageContentTypeDef]
    DestinationPhoneNumber: NotRequired[str]
    OriginationPhoneNumber: NotRequired[str]
