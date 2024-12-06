"""
Type annotations for chime service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_chime.client import ChimeClient
    from mypy_boto3_chime.paginator import (
        ListAccountsPaginator,
        ListUsersPaginator,
    )

    session = Session()
    client: ChimeClient = session.client("chime")

    list_accounts_paginator: ListAccountsPaginator = client.get_paginator("list_accounts")
    list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAccountsRequestListAccountsPaginateTypeDef,
    ListAccountsResponseTypeDef,
    ListUsersRequestListUsersPaginateTypeDef,
    ListUsersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListAccountsPaginator", "ListUsersPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAccountsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/paginator/ListAccounts.html#Chime.Paginator.ListAccounts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/paginators/#listaccountspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAccountsRequestListAccountsPaginateTypeDef]
    ) -> _PageIterator[ListAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/paginator/ListAccounts.html#Chime.Paginator.ListAccounts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/paginators/#listaccountspaginator)
        """

class ListUsersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/paginator/ListUsers.html#Chime.Paginator.ListUsers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/paginators/#listuserspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUsersRequestListUsersPaginateTypeDef]
    ) -> _PageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/paginator/ListUsers.html#Chime.Paginator.ListUsers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/paginators/#listuserspaginator)
        """
