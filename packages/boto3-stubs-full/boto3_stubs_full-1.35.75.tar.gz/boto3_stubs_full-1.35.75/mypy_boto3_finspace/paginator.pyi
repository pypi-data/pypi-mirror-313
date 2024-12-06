"""
Type annotations for finspace service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_finspace.client import FinspaceClient
    from mypy_boto3_finspace.paginator import (
        ListKxEnvironmentsPaginator,
    )

    session = Session()
    client: FinspaceClient = session.client("finspace")

    list_kx_environments_paginator: ListKxEnvironmentsPaginator = client.get_paginator("list_kx_environments")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListKxEnvironmentsRequestListKxEnvironmentsPaginateTypeDef,
    ListKxEnvironmentsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListKxEnvironmentsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListKxEnvironmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/paginator/ListKxEnvironments.html#Finspace.Paginator.ListKxEnvironments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/paginators/#listkxenvironmentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListKxEnvironmentsRequestListKxEnvironmentsPaginateTypeDef]
    ) -> _PageIterator[ListKxEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/paginator/ListKxEnvironments.html#Finspace.Paginator.ListKxEnvironments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/paginators/#listkxenvironmentspaginator)
        """
