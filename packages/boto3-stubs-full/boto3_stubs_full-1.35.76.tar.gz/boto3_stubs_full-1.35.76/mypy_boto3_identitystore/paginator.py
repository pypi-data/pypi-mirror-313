"""
Type annotations for identitystore service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_identitystore.client import IdentityStoreClient
    from mypy_boto3_identitystore.paginator import (
        ListGroupMembershipsForMemberPaginator,
        ListGroupMembershipsPaginator,
        ListGroupsPaginator,
        ListUsersPaginator,
    )

    session = Session()
    client: IdentityStoreClient = session.client("identitystore")

    list_group_memberships_for_member_paginator: ListGroupMembershipsForMemberPaginator = client.get_paginator("list_group_memberships_for_member")
    list_group_memberships_paginator: ListGroupMembershipsPaginator = client.get_paginator("list_group_memberships")
    list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
    list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListGroupMembershipsForMemberRequestListGroupMembershipsForMemberPaginateTypeDef,
    ListGroupMembershipsForMemberResponseTypeDef,
    ListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef,
    ListGroupMembershipsResponseTypeDef,
    ListGroupsRequestListGroupsPaginateTypeDef,
    ListGroupsResponseTypeDef,
    ListUsersRequestListUsersPaginateTypeDef,
    ListUsersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListGroupMembershipsForMemberPaginator",
    "ListGroupMembershipsPaginator",
    "ListGroupsPaginator",
    "ListUsersPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListGroupMembershipsForMemberPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/paginator/ListGroupMembershipsForMember.html#IdentityStore.Paginator.ListGroupMembershipsForMember)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/paginators/#listgroupmembershipsformemberpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListGroupMembershipsForMemberRequestListGroupMembershipsForMemberPaginateTypeDef
        ],
    ) -> _PageIterator[ListGroupMembershipsForMemberResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/paginator/ListGroupMembershipsForMember.html#IdentityStore.Paginator.ListGroupMembershipsForMember.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/paginators/#listgroupmembershipsformemberpaginator)
        """


class ListGroupMembershipsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/paginator/ListGroupMemberships.html#IdentityStore.Paginator.ListGroupMemberships)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/paginators/#listgroupmembershipspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef]
    ) -> _PageIterator[ListGroupMembershipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/paginator/ListGroupMemberships.html#IdentityStore.Paginator.ListGroupMemberships.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/paginators/#listgroupmembershipspaginator)
        """


class ListGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/paginator/ListGroups.html#IdentityStore.Paginator.ListGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/paginators/#listgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGroupsRequestListGroupsPaginateTypeDef]
    ) -> _PageIterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/paginator/ListGroups.html#IdentityStore.Paginator.ListGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/paginators/#listgroupspaginator)
        """


class ListUsersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/paginator/ListUsers.html#IdentityStore.Paginator.ListUsers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/paginators/#listuserspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListUsersRequestListUsersPaginateTypeDef]
    ) -> _PageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/paginator/ListUsers.html#IdentityStore.Paginator.ListUsers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/paginators/#listuserspaginator)
        """
