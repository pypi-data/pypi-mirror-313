"""
Type annotations for billing service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_billing.client import BillingClient
    from mypy_boto3_billing.paginator import (
        ListBillingViewsPaginator,
    )

    session = Session()
    client: BillingClient = session.client("billing")

    list_billing_views_paginator: ListBillingViewsPaginator = client.get_paginator("list_billing_views")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListBillingViewsRequestListBillingViewsPaginateTypeDef,
    ListBillingViewsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListBillingViewsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListBillingViewsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBillingViews.html#Billing.Paginator.ListBillingViews)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listbillingviewspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBillingViewsRequestListBillingViewsPaginateTypeDef]
    ) -> _PageIterator[ListBillingViewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBillingViews.html#Billing.Paginator.ListBillingViews.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listbillingviewspaginator)
        """
