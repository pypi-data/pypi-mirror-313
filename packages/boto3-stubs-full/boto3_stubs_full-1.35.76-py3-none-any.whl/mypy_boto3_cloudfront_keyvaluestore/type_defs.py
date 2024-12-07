"""
Type annotations for cloudfront-keyvaluestore service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront_keyvaluestore/type_defs/)

Usage::

    ```python
    from mypy_boto3_cloudfront_keyvaluestore.type_defs import DeleteKeyRequestListItemTypeDef

    data: DeleteKeyRequestListItemTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "DeleteKeyRequestListItemTypeDef",
    "DeleteKeyRequestRequestTypeDef",
    "DeleteKeyResponseTypeDef",
    "DescribeKeyValueStoreRequestRequestTypeDef",
    "DescribeKeyValueStoreResponseTypeDef",
    "GetKeyRequestRequestTypeDef",
    "GetKeyResponseTypeDef",
    "ListKeysRequestListKeysPaginateTypeDef",
    "ListKeysRequestRequestTypeDef",
    "ListKeysResponseListItemTypeDef",
    "ListKeysResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutKeyRequestListItemTypeDef",
    "PutKeyRequestRequestTypeDef",
    "PutKeyResponseTypeDef",
    "ResponseMetadataTypeDef",
    "UpdateKeysRequestRequestTypeDef",
    "UpdateKeysResponseTypeDef",
)


class DeleteKeyRequestListItemTypeDef(TypedDict):
    Key: str


class DeleteKeyRequestRequestTypeDef(TypedDict):
    KvsARN: str
    Key: str
    IfMatch: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DescribeKeyValueStoreRequestRequestTypeDef(TypedDict):
    KvsARN: str


class GetKeyRequestRequestTypeDef(TypedDict):
    KvsARN: str
    Key: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListKeysRequestRequestTypeDef(TypedDict):
    KvsARN: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListKeysResponseListItemTypeDef(TypedDict):
    Key: str
    Value: str


class PutKeyRequestListItemTypeDef(TypedDict):
    Key: str
    Value: str


class PutKeyRequestRequestTypeDef(TypedDict):
    Key: str
    Value: str
    KvsARN: str
    IfMatch: str


class DeleteKeyResponseTypeDef(TypedDict):
    ItemCount: int
    TotalSizeInBytes: int
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeKeyValueStoreResponseTypeDef(TypedDict):
    ItemCount: int
    TotalSizeInBytes: int
    KvsARN: str
    Created: datetime
    ETag: str
    LastModified: datetime
    Status: str
    FailureReason: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetKeyResponseTypeDef(TypedDict):
    Key: str
    Value: str
    ItemCount: int
    TotalSizeInBytes: int
    ResponseMetadata: ResponseMetadataTypeDef


class PutKeyResponseTypeDef(TypedDict):
    ItemCount: int
    TotalSizeInBytes: int
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateKeysResponseTypeDef(TypedDict):
    ItemCount: int
    TotalSizeInBytes: int
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListKeysRequestListKeysPaginateTypeDef(TypedDict):
    KvsARN: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListKeysResponseTypeDef(TypedDict):
    Items: List[ListKeysResponseListItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateKeysRequestRequestTypeDef(TypedDict):
    KvsARN: str
    IfMatch: str
    Puts: NotRequired[Sequence[PutKeyRequestListItemTypeDef]]
    Deletes: NotRequired[Sequence[DeleteKeyRequestListItemTypeDef]]
