"""
Type annotations for connectcases service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcases/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_connectcases.client import ConnectCasesClient
    from mypy_boto3_connectcases.paginator import (
        SearchCasesPaginator,
        SearchRelatedItemsPaginator,
    )

    session = Session()
    client: ConnectCasesClient = session.client("connectcases")

    search_cases_paginator: SearchCasesPaginator = client.get_paginator("search_cases")
    search_related_items_paginator: SearchRelatedItemsPaginator = client.get_paginator("search_related_items")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    SearchCasesRequestSearchCasesPaginateTypeDef,
    SearchCasesResponseTypeDef,
    SearchRelatedItemsRequestSearchRelatedItemsPaginateTypeDef,
    SearchRelatedItemsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("SearchCasesPaginator", "SearchRelatedItemsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class SearchCasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/paginator/SearchCases.html#ConnectCases.Paginator.SearchCases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcases/paginators/#searchcasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchCasesRequestSearchCasesPaginateTypeDef]
    ) -> _PageIterator[SearchCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/paginator/SearchCases.html#ConnectCases.Paginator.SearchCases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcases/paginators/#searchcasespaginator)
        """

class SearchRelatedItemsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/paginator/SearchRelatedItems.html#ConnectCases.Paginator.SearchRelatedItems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcases/paginators/#searchrelateditemspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchRelatedItemsRequestSearchRelatedItemsPaginateTypeDef]
    ) -> _PageIterator[SearchRelatedItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/paginator/SearchRelatedItems.html#ConnectCases.Paginator.SearchRelatedItems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcases/paginators/#searchrelateditemspaginator)
        """
