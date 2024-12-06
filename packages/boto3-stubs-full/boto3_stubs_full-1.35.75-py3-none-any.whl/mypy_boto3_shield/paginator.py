"""
Type annotations for shield service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_shield/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_shield.client import ShieldClient
    from mypy_boto3_shield.paginator import (
        ListAttacksPaginator,
        ListProtectionsPaginator,
    )

    session = Session()
    client: ShieldClient = session.client("shield")

    list_attacks_paginator: ListAttacksPaginator = client.get_paginator("list_attacks")
    list_protections_paginator: ListProtectionsPaginator = client.get_paginator("list_protections")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAttacksRequestListAttacksPaginateTypeDef,
    ListAttacksResponseTypeDef,
    ListProtectionsRequestListProtectionsPaginateTypeDef,
    ListProtectionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListAttacksPaginator", "ListProtectionsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAttacksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield/paginator/ListAttacks.html#Shield.Paginator.ListAttacks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_shield/paginators/#listattackspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAttacksRequestListAttacksPaginateTypeDef]
    ) -> _PageIterator[ListAttacksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield/paginator/ListAttacks.html#Shield.Paginator.ListAttacks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_shield/paginators/#listattackspaginator)
        """


class ListProtectionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield/paginator/ListProtections.html#Shield.Paginator.ListProtections)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_shield/paginators/#listprotectionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListProtectionsRequestListProtectionsPaginateTypeDef]
    ) -> _PageIterator[ListProtectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield/paginator/ListProtections.html#Shield.Paginator.ListProtections.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_shield/paginators/#listprotectionspaginator)
        """
