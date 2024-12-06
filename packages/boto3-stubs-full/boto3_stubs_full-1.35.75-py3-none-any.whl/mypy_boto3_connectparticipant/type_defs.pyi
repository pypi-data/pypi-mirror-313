"""
Type annotations for connectparticipant service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectparticipant/type_defs/)

Usage::

    ```python
    from mypy_boto3_connectparticipant.type_defs import AttachmentItemTypeDef

    data: AttachmentItemTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Sequence

from .literals import (
    ArtifactStatusType,
    ChatItemTypeType,
    ConnectionTypeType,
    ParticipantRoleType,
    ScanDirectionType,
    SortKeyType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AttachmentItemTypeDef",
    "CompleteAttachmentUploadRequestRequestTypeDef",
    "ConnectionCredentialsTypeDef",
    "CreateParticipantConnectionRequestRequestTypeDef",
    "CreateParticipantConnectionResponseTypeDef",
    "DescribeViewRequestRequestTypeDef",
    "DescribeViewResponseTypeDef",
    "DisconnectParticipantRequestRequestTypeDef",
    "GetAttachmentRequestRequestTypeDef",
    "GetAttachmentResponseTypeDef",
    "GetTranscriptRequestRequestTypeDef",
    "GetTranscriptResponseTypeDef",
    "ItemTypeDef",
    "MessageMetadataTypeDef",
    "ReceiptTypeDef",
    "ResponseMetadataTypeDef",
    "SendEventRequestRequestTypeDef",
    "SendEventResponseTypeDef",
    "SendMessageRequestRequestTypeDef",
    "SendMessageResponseTypeDef",
    "StartAttachmentUploadRequestRequestTypeDef",
    "StartAttachmentUploadResponseTypeDef",
    "StartPositionTypeDef",
    "UploadMetadataTypeDef",
    "ViewContentTypeDef",
    "ViewTypeDef",
    "WebsocketTypeDef",
)

class AttachmentItemTypeDef(TypedDict):
    ContentType: NotRequired[str]
    AttachmentId: NotRequired[str]
    AttachmentName: NotRequired[str]
    Status: NotRequired[ArtifactStatusType]

class CompleteAttachmentUploadRequestRequestTypeDef(TypedDict):
    AttachmentIds: Sequence[str]
    ClientToken: str
    ConnectionToken: str

class ConnectionCredentialsTypeDef(TypedDict):
    ConnectionToken: NotRequired[str]
    Expiry: NotRequired[str]

CreateParticipantConnectionRequestRequestTypeDef = TypedDict(
    "CreateParticipantConnectionRequestRequestTypeDef",
    {
        "ParticipantToken": str,
        "Type": NotRequired[Sequence[ConnectionTypeType]],
        "ConnectParticipant": NotRequired[bool],
    },
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class WebsocketTypeDef(TypedDict):
    Url: NotRequired[str]
    ConnectionExpiry: NotRequired[str]

class DescribeViewRequestRequestTypeDef(TypedDict):
    ViewToken: str
    ConnectionToken: str

class DisconnectParticipantRequestRequestTypeDef(TypedDict):
    ConnectionToken: str
    ClientToken: NotRequired[str]

class GetAttachmentRequestRequestTypeDef(TypedDict):
    AttachmentId: str
    ConnectionToken: str

class StartPositionTypeDef(TypedDict):
    Id: NotRequired[str]
    AbsoluteTime: NotRequired[str]
    MostRecent: NotRequired[int]

class ReceiptTypeDef(TypedDict):
    DeliveredTimestamp: NotRequired[str]
    ReadTimestamp: NotRequired[str]
    RecipientParticipantId: NotRequired[str]

class SendEventRequestRequestTypeDef(TypedDict):
    ContentType: str
    ConnectionToken: str
    Content: NotRequired[str]
    ClientToken: NotRequired[str]

class SendMessageRequestRequestTypeDef(TypedDict):
    ContentType: str
    Content: str
    ConnectionToken: str
    ClientToken: NotRequired[str]

class StartAttachmentUploadRequestRequestTypeDef(TypedDict):
    ContentType: str
    AttachmentSizeInBytes: int
    AttachmentName: str
    ClientToken: str
    ConnectionToken: str

class UploadMetadataTypeDef(TypedDict):
    Url: NotRequired[str]
    UrlExpiry: NotRequired[str]
    HeadersToInclude: NotRequired[Dict[str, str]]

class ViewContentTypeDef(TypedDict):
    InputSchema: NotRequired[str]
    Template: NotRequired[str]
    Actions: NotRequired[List[str]]

class GetAttachmentResponseTypeDef(TypedDict):
    Url: str
    UrlExpiry: str
    ResponseMetadata: ResponseMetadataTypeDef

class SendEventResponseTypeDef(TypedDict):
    Id: str
    AbsoluteTime: str
    ResponseMetadata: ResponseMetadataTypeDef

class SendMessageResponseTypeDef(TypedDict):
    Id: str
    AbsoluteTime: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateParticipantConnectionResponseTypeDef(TypedDict):
    Websocket: WebsocketTypeDef
    ConnectionCredentials: ConnectionCredentialsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetTranscriptRequestRequestTypeDef(TypedDict):
    ConnectionToken: str
    ContactId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ScanDirection: NotRequired[ScanDirectionType]
    SortOrder: NotRequired[SortKeyType]
    StartPosition: NotRequired[StartPositionTypeDef]

class MessageMetadataTypeDef(TypedDict):
    MessageId: NotRequired[str]
    Receipts: NotRequired[List[ReceiptTypeDef]]

class StartAttachmentUploadResponseTypeDef(TypedDict):
    AttachmentId: str
    UploadMetadata: UploadMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ViewTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    Version: NotRequired[int]
    Content: NotRequired[ViewContentTypeDef]

ItemTypeDef = TypedDict(
    "ItemTypeDef",
    {
        "AbsoluteTime": NotRequired[str],
        "Content": NotRequired[str],
        "ContentType": NotRequired[str],
        "Id": NotRequired[str],
        "Type": NotRequired[ChatItemTypeType],
        "ParticipantId": NotRequired[str],
        "DisplayName": NotRequired[str],
        "ParticipantRole": NotRequired[ParticipantRoleType],
        "Attachments": NotRequired[List[AttachmentItemTypeDef]],
        "MessageMetadata": NotRequired[MessageMetadataTypeDef],
        "RelatedContactId": NotRequired[str],
        "ContactId": NotRequired[str],
    },
)

class DescribeViewResponseTypeDef(TypedDict):
    View: ViewTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetTranscriptResponseTypeDef(TypedDict):
    InitialContactId: str
    Transcript: List[ItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
