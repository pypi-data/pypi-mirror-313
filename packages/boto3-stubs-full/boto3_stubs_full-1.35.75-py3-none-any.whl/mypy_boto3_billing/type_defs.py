"""
Type annotations for billing service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/type_defs/)

Usage::

    ```python
    from mypy_boto3_billing.type_defs import TimestampTypeDef

    data: TimestampTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Union

from .literals import BillingViewTypeType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "ActiveTimeRangeTypeDef",
    "BillingViewListElementTypeDef",
    "ListBillingViewsRequestListBillingViewsPaginateTypeDef",
    "ListBillingViewsRequestRequestTypeDef",
    "ListBillingViewsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TimestampTypeDef",
)

TimestampTypeDef = Union[datetime, str]


class BillingViewListElementTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    ownerAccountId: NotRequired[str]
    billingViewType: NotRequired[BillingViewTypeType]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class ActiveTimeRangeTypeDef(TypedDict):
    activeAfterInclusive: TimestampTypeDef
    activeBeforeInclusive: TimestampTypeDef


class ListBillingViewsResponseTypeDef(TypedDict):
    billingViews: List[BillingViewListElementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListBillingViewsRequestListBillingViewsPaginateTypeDef(TypedDict):
    activeTimeRange: ActiveTimeRangeTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBillingViewsRequestRequestTypeDef(TypedDict):
    activeTimeRange: ActiveTimeRangeTypeDef
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
