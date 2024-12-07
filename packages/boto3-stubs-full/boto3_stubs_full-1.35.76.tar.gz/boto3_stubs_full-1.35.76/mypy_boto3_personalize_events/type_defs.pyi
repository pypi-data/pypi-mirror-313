"""
Type annotations for personalize-events service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize_events/type_defs/)

Usage::

    ```python
    from mypy_boto3_personalize_events.type_defs import TimestampTypeDef

    data: TimestampTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, Sequence, Union

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ActionInteractionTypeDef",
    "ActionTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EventTypeDef",
    "ItemTypeDef",
    "MetricAttributionTypeDef",
    "PutActionInteractionsRequestRequestTypeDef",
    "PutActionsRequestRequestTypeDef",
    "PutEventsRequestRequestTypeDef",
    "PutItemsRequestRequestTypeDef",
    "PutUsersRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "TimestampTypeDef",
    "UserTypeDef",
)

TimestampTypeDef = Union[datetime, str]

class ActionTypeDef(TypedDict):
    actionId: str
    properties: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class MetricAttributionTypeDef(TypedDict):
    eventAttributionSource: str

class ItemTypeDef(TypedDict):
    itemId: str
    properties: NotRequired[str]

class UserTypeDef(TypedDict):
    userId: str
    properties: NotRequired[str]

class ActionInteractionTypeDef(TypedDict):
    actionId: str
    sessionId: str
    timestamp: TimestampTypeDef
    eventType: str
    userId: NotRequired[str]
    eventId: NotRequired[str]
    recommendationId: NotRequired[str]
    impression: NotRequired[Sequence[str]]
    properties: NotRequired[str]

class PutActionsRequestRequestTypeDef(TypedDict):
    datasetArn: str
    actions: Sequence[ActionTypeDef]

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class EventTypeDef(TypedDict):
    eventType: str
    sentAt: TimestampTypeDef
    eventId: NotRequired[str]
    eventValue: NotRequired[float]
    itemId: NotRequired[str]
    properties: NotRequired[str]
    recommendationId: NotRequired[str]
    impression: NotRequired[Sequence[str]]
    metricAttribution: NotRequired[MetricAttributionTypeDef]

class PutItemsRequestRequestTypeDef(TypedDict):
    datasetArn: str
    items: Sequence[ItemTypeDef]

class PutUsersRequestRequestTypeDef(TypedDict):
    datasetArn: str
    users: Sequence[UserTypeDef]

class PutActionInteractionsRequestRequestTypeDef(TypedDict):
    trackingId: str
    actionInteractions: Sequence[ActionInteractionTypeDef]

class PutEventsRequestRequestTypeDef(TypedDict):
    trackingId: str
    sessionId: str
    eventList: Sequence[EventTypeDef]
    userId: NotRequired[str]
