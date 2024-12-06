"""
Type annotations for qapps service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qapps/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_qapps.client import QAppsClient
    from mypy_boto3_qapps.paginator import (
        ListLibraryItemsPaginator,
        ListQAppsPaginator,
    )

    session = Session()
    client: QAppsClient = session.client("qapps")

    list_library_items_paginator: ListLibraryItemsPaginator = client.get_paginator("list_library_items")
    list_q_apps_paginator: ListQAppsPaginator = client.get_paginator("list_q_apps")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListLibraryItemsInputListLibraryItemsPaginateTypeDef,
    ListLibraryItemsOutputTypeDef,
    ListQAppsInputListQAppsPaginateTypeDef,
    ListQAppsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListLibraryItemsPaginator", "ListQAppsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListLibraryItemsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/paginator/ListLibraryItems.html#QApps.Paginator.ListLibraryItems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qapps/paginators/#listlibraryitemspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListLibraryItemsInputListLibraryItemsPaginateTypeDef]
    ) -> _PageIterator[ListLibraryItemsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/paginator/ListLibraryItems.html#QApps.Paginator.ListLibraryItems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qapps/paginators/#listlibraryitemspaginator)
        """


class ListQAppsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/paginator/ListQApps.html#QApps.Paginator.ListQApps)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qapps/paginators/#listqappspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListQAppsInputListQAppsPaginateTypeDef]
    ) -> _PageIterator[ListQAppsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/paginator/ListQApps.html#QApps.Paginator.ListQApps.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qapps/paginators/#listqappspaginator)
        """
