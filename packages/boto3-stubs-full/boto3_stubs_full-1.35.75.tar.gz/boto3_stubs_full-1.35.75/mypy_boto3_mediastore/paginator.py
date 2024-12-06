"""
Type annotations for mediastore service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_mediastore.client import MediaStoreClient
    from mypy_boto3_mediastore.paginator import (
        ListContainersPaginator,
    )

    session = Session()
    client: MediaStoreClient = session.client("mediastore")

    list_containers_paginator: ListContainersPaginator = client.get_paginator("list_containers")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListContainersInputListContainersPaginateTypeDef, ListContainersOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListContainersPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListContainersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/paginator/ListContainers.html#MediaStore.Paginator.ListContainers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/paginators/#listcontainerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListContainersInputListContainersPaginateTypeDef]
    ) -> _PageIterator[ListContainersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/paginator/ListContainers.html#MediaStore.Paginator.ListContainers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/paginators/#listcontainerspaginator)
        """
