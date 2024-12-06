"""
Type annotations for managedblockchain service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_managedblockchain.client import ManagedBlockchainClient
    from mypy_boto3_managedblockchain.paginator import (
        ListAccessorsPaginator,
    )

    session = Session()
    client: ManagedBlockchainClient = session.client("managedblockchain")

    list_accessors_paginator: ListAccessorsPaginator = client.get_paginator("list_accessors")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListAccessorsInputListAccessorsPaginateTypeDef, ListAccessorsOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListAccessorsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAccessorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/paginator/ListAccessors.html#ManagedBlockchain.Paginator.ListAccessors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain/paginators/#listaccessorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAccessorsInputListAccessorsPaginateTypeDef]
    ) -> _PageIterator[ListAccessorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/paginator/ListAccessors.html#ManagedBlockchain.Paginator.ListAccessors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain/paginators/#listaccessorspaginator)
        """
