"""
Type annotations for apigatewaymanagementapi service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewaymanagementapi/type_defs/)

Usage::

    ```python
    from mypy_boto3_apigatewaymanagementapi.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, Union

from botocore.response import StreamingBody

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "BlobTypeDef",
    "DeleteConnectionRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetConnectionRequestRequestTypeDef",
    "GetConnectionResponseTypeDef",
    "IdentityTypeDef",
    "PostToConnectionRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class DeleteConnectionRequestRequestTypeDef(TypedDict):
    ConnectionId: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class GetConnectionRequestRequestTypeDef(TypedDict):
    ConnectionId: str

class IdentityTypeDef(TypedDict):
    SourceIp: str
    UserAgent: str

class PostToConnectionRequestRequestTypeDef(TypedDict):
    Data: BlobTypeDef
    ConnectionId: str

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetConnectionResponseTypeDef(TypedDict):
    ConnectedAt: datetime
    Identity: IdentityTypeDef
    LastActiveAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef
