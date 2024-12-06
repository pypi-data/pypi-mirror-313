"""
Type annotations for iotsecuretunneling service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/type_defs/)

Usage::

    ```python
    from mypy_boto3_iotsecuretunneling.type_defs import CloseTunnelRequestRequestTypeDef

    data: CloseTunnelRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import ClientModeType, ConnectionStatusType, TunnelStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "CloseTunnelRequestRequestTypeDef",
    "ConnectionStateTypeDef",
    "DescribeTunnelRequestRequestTypeDef",
    "DescribeTunnelResponseTypeDef",
    "DestinationConfigOutputTypeDef",
    "DestinationConfigTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTunnelsRequestRequestTypeDef",
    "ListTunnelsResponseTypeDef",
    "OpenTunnelRequestRequestTypeDef",
    "OpenTunnelResponseTypeDef",
    "ResponseMetadataTypeDef",
    "RotateTunnelAccessTokenRequestRequestTypeDef",
    "RotateTunnelAccessTokenResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TimeoutConfigTypeDef",
    "TunnelSummaryTypeDef",
    "TunnelTypeDef",
    "UntagResourceRequestRequestTypeDef",
)

class CloseTunnelRequestRequestTypeDef(TypedDict):
    tunnelId: str
    delete: NotRequired[bool]

class ConnectionStateTypeDef(TypedDict):
    status: NotRequired[ConnectionStatusType]
    lastUpdatedAt: NotRequired[datetime]

class DescribeTunnelRequestRequestTypeDef(TypedDict):
    tunnelId: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DestinationConfigOutputTypeDef(TypedDict):
    services: List[str]
    thingName: NotRequired[str]

class DestinationConfigTypeDef(TypedDict):
    services: Sequence[str]
    thingName: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class TagTypeDef(TypedDict):
    key: str
    value: str

class ListTunnelsRequestRequestTypeDef(TypedDict):
    thingName: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class TunnelSummaryTypeDef(TypedDict):
    tunnelId: NotRequired[str]
    tunnelArn: NotRequired[str]
    status: NotRequired[TunnelStatusType]
    description: NotRequired[str]
    createdAt: NotRequired[datetime]
    lastUpdatedAt: NotRequired[datetime]

class TimeoutConfigTypeDef(TypedDict):
    maxLifetimeTimeoutMinutes: NotRequired[int]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class OpenTunnelResponseTypeDef(TypedDict):
    tunnelId: str
    tunnelArn: str
    sourceAccessToken: str
    destinationAccessToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class RotateTunnelAccessTokenResponseTypeDef(TypedDict):
    tunnelArn: str
    sourceAccessToken: str
    destinationAccessToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class RotateTunnelAccessTokenRequestRequestTypeDef(TypedDict):
    tunnelId: str
    clientMode: ClientModeType
    destinationConfig: NotRequired[DestinationConfigTypeDef]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]

class ListTunnelsResponseTypeDef(TypedDict):
    tunnelSummaries: List[TunnelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class OpenTunnelRequestRequestTypeDef(TypedDict):
    description: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    destinationConfig: NotRequired[DestinationConfigTypeDef]
    timeoutConfig: NotRequired[TimeoutConfigTypeDef]

class TunnelTypeDef(TypedDict):
    tunnelId: NotRequired[str]
    tunnelArn: NotRequired[str]
    status: NotRequired[TunnelStatusType]
    sourceConnectionState: NotRequired[ConnectionStateTypeDef]
    destinationConnectionState: NotRequired[ConnectionStateTypeDef]
    description: NotRequired[str]
    destinationConfig: NotRequired[DestinationConfigOutputTypeDef]
    timeoutConfig: NotRequired[TimeoutConfigTypeDef]
    tags: NotRequired[List[TagTypeDef]]
    createdAt: NotRequired[datetime]
    lastUpdatedAt: NotRequired[datetime]

class DescribeTunnelResponseTypeDef(TypedDict):
    tunnel: TunnelTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
