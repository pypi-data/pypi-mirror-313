"""
Type annotations for account service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_account.client import AccountClient
    from mypy_boto3_account.paginator import (
        ListRegionsPaginator,
    )

    session = Session()
    client: AccountClient = session.client("account")

    list_regions_paginator: ListRegionsPaginator = client.get_paginator("list_regions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListRegionsRequestListRegionsPaginateTypeDef, ListRegionsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListRegionsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListRegionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/paginator/ListRegions.html#Account.Paginator.ListRegions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account/paginators/#listregionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRegionsRequestListRegionsPaginateTypeDef]
    ) -> _PageIterator[ListRegionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/paginator/ListRegions.html#Account.Paginator.ListRegions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account/paginators/#listregionspaginator)
        """
