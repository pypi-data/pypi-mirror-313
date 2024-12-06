"""
Type annotations for pipes service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_pipes.client import EventBridgePipesClient
    from mypy_boto3_pipes.paginator import (
        ListPipesPaginator,
    )

    session = Session()
    client: EventBridgePipesClient = session.client("pipes")

    list_pipes_paginator: ListPipesPaginator = client.get_paginator("list_pipes")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListPipesRequestListPipesPaginateTypeDef, ListPipesResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListPipesPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListPipesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/paginator/ListPipes.html#EventBridgePipes.Paginator.ListPipes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/paginators/#listpipespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPipesRequestListPipesPaginateTypeDef]
    ) -> _PageIterator[ListPipesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/paginator/ListPipes.html#EventBridgePipes.Paginator.ListPipes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/paginators/#listpipespaginator)
        """
