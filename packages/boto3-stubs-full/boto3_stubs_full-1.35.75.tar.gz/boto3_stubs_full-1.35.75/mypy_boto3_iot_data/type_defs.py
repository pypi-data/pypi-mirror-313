"""
Type annotations for iot-data service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/type_defs/)

Usage::

    ```python
    from mypy_boto3_iot_data.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import IO, Any, Dict, List, Union

from botocore.response import StreamingBody

from .literals import PayloadFormatIndicatorType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "BlobTypeDef",
    "DeleteThingShadowRequestRequestTypeDef",
    "DeleteThingShadowResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetRetainedMessageRequestRequestTypeDef",
    "GetRetainedMessageResponseTypeDef",
    "GetThingShadowRequestRequestTypeDef",
    "GetThingShadowResponseTypeDef",
    "ListNamedShadowsForThingRequestRequestTypeDef",
    "ListNamedShadowsForThingResponseTypeDef",
    "ListRetainedMessagesRequestListRetainedMessagesPaginateTypeDef",
    "ListRetainedMessagesRequestRequestTypeDef",
    "ListRetainedMessagesResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PublishRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "RetainedMessageSummaryTypeDef",
    "UpdateThingShadowRequestRequestTypeDef",
    "UpdateThingShadowResponseTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class DeleteThingShadowRequestRequestTypeDef(TypedDict):
    thingName: str
    shadowName: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class GetRetainedMessageRequestRequestTypeDef(TypedDict):
    topic: str


class GetThingShadowRequestRequestTypeDef(TypedDict):
    thingName: str
    shadowName: NotRequired[str]


class ListNamedShadowsForThingRequestRequestTypeDef(TypedDict):
    thingName: str
    nextToken: NotRequired[str]
    pageSize: NotRequired[int]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListRetainedMessagesRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class RetainedMessageSummaryTypeDef(TypedDict):
    topic: NotRequired[str]
    payloadSize: NotRequired[int]
    qos: NotRequired[int]
    lastModifiedTime: NotRequired[int]


class PublishRequestRequestTypeDef(TypedDict):
    topic: str
    qos: NotRequired[int]
    retain: NotRequired[bool]
    payload: NotRequired[BlobTypeDef]
    userProperties: NotRequired[str]
    payloadFormatIndicator: NotRequired[PayloadFormatIndicatorType]
    contentType: NotRequired[str]
    responseTopic: NotRequired[str]
    correlationData: NotRequired[str]
    messageExpiry: NotRequired[int]


class UpdateThingShadowRequestRequestTypeDef(TypedDict):
    thingName: str
    payload: BlobTypeDef
    shadowName: NotRequired[str]


class DeleteThingShadowResponseTypeDef(TypedDict):
    payload: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetRetainedMessageResponseTypeDef(TypedDict):
    topic: str
    payload: bytes
    qos: int
    lastModifiedTime: int
    userProperties: bytes
    ResponseMetadata: ResponseMetadataTypeDef


class GetThingShadowResponseTypeDef(TypedDict):
    payload: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef


class ListNamedShadowsForThingResponseTypeDef(TypedDict):
    results: List[str]
    timestamp: int
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateThingShadowResponseTypeDef(TypedDict):
    payload: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef


class ListRetainedMessagesRequestListRetainedMessagesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRetainedMessagesResponseTypeDef(TypedDict):
    retainedTopics: List[RetainedMessageSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
