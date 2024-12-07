"""
Type annotations for marketplace-reporting service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_reporting/type_defs/)

Usage::

    ```python
    from mypy_boto3_marketplace_reporting.type_defs import GetBuyerDashboardInputRequestTypeDef

    data: GetBuyerDashboardInputRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Sequence

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "GetBuyerDashboardInputRequestTypeDef",
    "GetBuyerDashboardOutputTypeDef",
    "ResponseMetadataTypeDef",
)

class GetBuyerDashboardInputRequestTypeDef(TypedDict):
    dashboardIdentifier: str
    embeddingDomains: Sequence[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class GetBuyerDashboardOutputTypeDef(TypedDict):
    embedUrl: str
    dashboardIdentifier: str
    embeddingDomains: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
