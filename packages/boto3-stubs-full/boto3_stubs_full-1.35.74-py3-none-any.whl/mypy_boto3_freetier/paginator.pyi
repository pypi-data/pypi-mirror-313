"""
Type annotations for freetier service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_freetier/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_freetier.client import FreeTierClient
    from mypy_boto3_freetier.paginator import (
        GetFreeTierUsagePaginator,
    )

    session = Session()
    client: FreeTierClient = session.client("freetier")

    get_free_tier_usage_paginator: GetFreeTierUsagePaginator = client.get_paginator("get_free_tier_usage")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetFreeTierUsageRequestGetFreeTierUsagePaginateTypeDef,
    GetFreeTierUsageResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("GetFreeTierUsagePaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetFreeTierUsagePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/freetier/paginator/GetFreeTierUsage.html#FreeTier.Paginator.GetFreeTierUsage)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_freetier/paginators/#getfreetierusagepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetFreeTierUsageRequestGetFreeTierUsagePaginateTypeDef]
    ) -> _PageIterator[GetFreeTierUsageResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/freetier/paginator/GetFreeTierUsage.html#FreeTier.Paginator.GetFreeTierUsage.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_freetier/paginators/#getfreetierusagepaginator)
        """
