"""
Type annotations for oam service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_oam.client import CloudWatchObservabilityAccessManagerClient
    from mypy_boto3_oam.paginator import (
        ListAttachedLinksPaginator,
        ListLinksPaginator,
        ListSinksPaginator,
    )

    session = Session()
    client: CloudWatchObservabilityAccessManagerClient = session.client("oam")

    list_attached_links_paginator: ListAttachedLinksPaginator = client.get_paginator("list_attached_links")
    list_links_paginator: ListLinksPaginator = client.get_paginator("list_links")
    list_sinks_paginator: ListSinksPaginator = client.get_paginator("list_sinks")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAttachedLinksInputListAttachedLinksPaginateTypeDef,
    ListAttachedLinksOutputTypeDef,
    ListLinksInputListLinksPaginateTypeDef,
    ListLinksOutputTypeDef,
    ListSinksInputListSinksPaginateTypeDef,
    ListSinksOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListAttachedLinksPaginator", "ListLinksPaginator", "ListSinksPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAttachedLinksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListAttachedLinks.html#CloudWatchObservabilityAccessManager.Paginator.ListAttachedLinks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/paginators/#listattachedlinkspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAttachedLinksInputListAttachedLinksPaginateTypeDef]
    ) -> _PageIterator[ListAttachedLinksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListAttachedLinks.html#CloudWatchObservabilityAccessManager.Paginator.ListAttachedLinks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/paginators/#listattachedlinkspaginator)
        """

class ListLinksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListLinks.html#CloudWatchObservabilityAccessManager.Paginator.ListLinks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/paginators/#listlinkspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLinksInputListLinksPaginateTypeDef]
    ) -> _PageIterator[ListLinksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListLinks.html#CloudWatchObservabilityAccessManager.Paginator.ListLinks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/paginators/#listlinkspaginator)
        """

class ListSinksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListSinks.html#CloudWatchObservabilityAccessManager.Paginator.ListSinks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/paginators/#listsinkspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSinksInputListSinksPaginateTypeDef]
    ) -> _PageIterator[ListSinksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListSinks.html#CloudWatchObservabilityAccessManager.Paginator.ListSinks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/paginators/#listsinkspaginator)
        """
