"""
Type annotations for ds-data service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds_data/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ds_data.client import DirectoryServiceDataClient
    from mypy_boto3_ds_data.paginator import (
        ListGroupMembersPaginator,
        ListGroupsForMemberPaginator,
        ListGroupsPaginator,
        ListUsersPaginator,
        SearchGroupsPaginator,
        SearchUsersPaginator,
    )

    session = Session()
    client: DirectoryServiceDataClient = session.client("ds-data")

    list_group_members_paginator: ListGroupMembersPaginator = client.get_paginator("list_group_members")
    list_groups_for_member_paginator: ListGroupsForMemberPaginator = client.get_paginator("list_groups_for_member")
    list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
    list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    search_groups_paginator: SearchGroupsPaginator = client.get_paginator("search_groups")
    search_users_paginator: SearchUsersPaginator = client.get_paginator("search_users")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListGroupMembersRequestListGroupMembersPaginateTypeDef,
    ListGroupMembersResultTypeDef,
    ListGroupsForMemberRequestListGroupsForMemberPaginateTypeDef,
    ListGroupsForMemberResultTypeDef,
    ListGroupsRequestListGroupsPaginateTypeDef,
    ListGroupsResultTypeDef,
    ListUsersRequestListUsersPaginateTypeDef,
    ListUsersResultTypeDef,
    SearchGroupsRequestSearchGroupsPaginateTypeDef,
    SearchGroupsResultTypeDef,
    SearchUsersRequestSearchUsersPaginateTypeDef,
    SearchUsersResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListGroupMembersPaginator",
    "ListGroupsForMemberPaginator",
    "ListGroupsPaginator",
    "ListUsersPaginator",
    "SearchGroupsPaginator",
    "SearchUsersPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListGroupMembersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/ListGroupMembers.html#DirectoryServiceData.Paginator.ListGroupMembers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds_data/paginators/#listgroupmemberspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGroupMembersRequestListGroupMembersPaginateTypeDef]
    ) -> _PageIterator[ListGroupMembersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/ListGroupMembers.html#DirectoryServiceData.Paginator.ListGroupMembers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds_data/paginators/#listgroupmemberspaginator)
        """


class ListGroupsForMemberPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/ListGroupsForMember.html#DirectoryServiceData.Paginator.ListGroupsForMember)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds_data/paginators/#listgroupsformemberpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGroupsForMemberRequestListGroupsForMemberPaginateTypeDef]
    ) -> _PageIterator[ListGroupsForMemberResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/ListGroupsForMember.html#DirectoryServiceData.Paginator.ListGroupsForMember.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds_data/paginators/#listgroupsformemberpaginator)
        """


class ListGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/ListGroups.html#DirectoryServiceData.Paginator.ListGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds_data/paginators/#listgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGroupsRequestListGroupsPaginateTypeDef]
    ) -> _PageIterator[ListGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/ListGroups.html#DirectoryServiceData.Paginator.ListGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds_data/paginators/#listgroupspaginator)
        """


class ListUsersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/ListUsers.html#DirectoryServiceData.Paginator.ListUsers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds_data/paginators/#listuserspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListUsersRequestListUsersPaginateTypeDef]
    ) -> _PageIterator[ListUsersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/ListUsers.html#DirectoryServiceData.Paginator.ListUsers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds_data/paginators/#listuserspaginator)
        """


class SearchGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/SearchGroups.html#DirectoryServiceData.Paginator.SearchGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds_data/paginators/#searchgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchGroupsRequestSearchGroupsPaginateTypeDef]
    ) -> _PageIterator[SearchGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/SearchGroups.html#DirectoryServiceData.Paginator.SearchGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds_data/paginators/#searchgroupspaginator)
        """


class SearchUsersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/SearchUsers.html#DirectoryServiceData.Paginator.SearchUsers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds_data/paginators/#searchuserspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchUsersRequestSearchUsersPaginateTypeDef]
    ) -> _PageIterator[SearchUsersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/SearchUsers.html#DirectoryServiceData.Paginator.SearchUsers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds_data/paginators/#searchuserspaginator)
        """
