"""
Type annotations for ebs service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ebs/type_defs/)

Usage::

    ```python
    from mypy_boto3_ebs.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import SSETypeType, StatusType

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "BlobTypeDef",
    "BlockTypeDef",
    "ChangedBlockTypeDef",
    "CompleteSnapshotRequestRequestTypeDef",
    "CompleteSnapshotResponseTypeDef",
    "GetSnapshotBlockRequestRequestTypeDef",
    "GetSnapshotBlockResponseTypeDef",
    "ListChangedBlocksRequestRequestTypeDef",
    "ListChangedBlocksResponseTypeDef",
    "ListSnapshotBlocksRequestRequestTypeDef",
    "ListSnapshotBlocksResponseTypeDef",
    "PutSnapshotBlockRequestRequestTypeDef",
    "PutSnapshotBlockResponseTypeDef",
    "ResponseMetadataTypeDef",
    "StartSnapshotRequestRequestTypeDef",
    "StartSnapshotResponseTypeDef",
    "TagTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class BlockTypeDef(TypedDict):
    BlockIndex: NotRequired[int]
    BlockToken: NotRequired[str]


class ChangedBlockTypeDef(TypedDict):
    BlockIndex: NotRequired[int]
    FirstBlockToken: NotRequired[str]
    SecondBlockToken: NotRequired[str]


class CompleteSnapshotRequestRequestTypeDef(TypedDict):
    SnapshotId: str
    ChangedBlocksCount: int
    Checksum: NotRequired[str]
    ChecksumAlgorithm: NotRequired[Literal["SHA256"]]
    ChecksumAggregationMethod: NotRequired[Literal["LINEAR"]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class GetSnapshotBlockRequestRequestTypeDef(TypedDict):
    SnapshotId: str
    BlockIndex: int
    BlockToken: str


class ListChangedBlocksRequestRequestTypeDef(TypedDict):
    SecondSnapshotId: str
    FirstSnapshotId: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    StartingBlockIndex: NotRequired[int]


class ListSnapshotBlocksRequestRequestTypeDef(TypedDict):
    SnapshotId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    StartingBlockIndex: NotRequired[int]


class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class PutSnapshotBlockRequestRequestTypeDef(TypedDict):
    SnapshotId: str
    BlockIndex: int
    BlockData: BlobTypeDef
    DataLength: int
    Checksum: str
    ChecksumAlgorithm: Literal["SHA256"]
    Progress: NotRequired[int]


class CompleteSnapshotResponseTypeDef(TypedDict):
    Status: StatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetSnapshotBlockResponseTypeDef(TypedDict):
    DataLength: int
    BlockData: StreamingBody
    Checksum: str
    ChecksumAlgorithm: Literal["SHA256"]
    ResponseMetadata: ResponseMetadataTypeDef


class ListChangedBlocksResponseTypeDef(TypedDict):
    ChangedBlocks: List[ChangedBlockTypeDef]
    ExpiryTime: datetime
    VolumeSize: int
    BlockSize: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListSnapshotBlocksResponseTypeDef(TypedDict):
    Blocks: List[BlockTypeDef]
    ExpiryTime: datetime
    VolumeSize: int
    BlockSize: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PutSnapshotBlockResponseTypeDef(TypedDict):
    Checksum: str
    ChecksumAlgorithm: Literal["SHA256"]
    ResponseMetadata: ResponseMetadataTypeDef


class StartSnapshotRequestRequestTypeDef(TypedDict):
    VolumeSize: int
    ParentSnapshotId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    Description: NotRequired[str]
    ClientToken: NotRequired[str]
    Encrypted: NotRequired[bool]
    KmsKeyArn: NotRequired[str]
    Timeout: NotRequired[int]


class StartSnapshotResponseTypeDef(TypedDict):
    Description: str
    SnapshotId: str
    OwnerId: str
    Status: StatusType
    StartTime: datetime
    VolumeSize: int
    BlockSize: int
    Tags: List[TagTypeDef]
    ParentSnapshotId: str
    KmsKeyArn: str
    SseType: SSETypeType
    ResponseMetadata: ResponseMetadataTypeDef
