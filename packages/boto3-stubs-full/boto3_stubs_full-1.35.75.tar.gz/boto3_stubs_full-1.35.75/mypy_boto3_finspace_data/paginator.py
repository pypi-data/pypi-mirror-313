"""
Type annotations for finspace-data service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_finspace_data.client import FinSpaceDataClient
    from mypy_boto3_finspace_data.paginator import (
        ListChangesetsPaginator,
        ListDataViewsPaginator,
        ListDatasetsPaginator,
        ListPermissionGroupsPaginator,
        ListUsersPaginator,
    )

    session = Session()
    client: FinSpaceDataClient = session.client("finspace-data")

    list_changesets_paginator: ListChangesetsPaginator = client.get_paginator("list_changesets")
    list_data_views_paginator: ListDataViewsPaginator = client.get_paginator("list_data_views")
    list_datasets_paginator: ListDatasetsPaginator = client.get_paginator("list_datasets")
    list_permission_groups_paginator: ListPermissionGroupsPaginator = client.get_paginator("list_permission_groups")
    list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListChangesetsRequestListChangesetsPaginateTypeDef,
    ListChangesetsResponseTypeDef,
    ListDatasetsRequestListDatasetsPaginateTypeDef,
    ListDatasetsResponseTypeDef,
    ListDataViewsRequestListDataViewsPaginateTypeDef,
    ListDataViewsResponseTypeDef,
    ListPermissionGroupsRequestListPermissionGroupsPaginateTypeDef,
    ListPermissionGroupsResponseTypeDef,
    ListUsersRequestListUsersPaginateTypeDef,
    ListUsersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListChangesetsPaginator",
    "ListDataViewsPaginator",
    "ListDatasetsPaginator",
    "ListPermissionGroupsPaginator",
    "ListUsersPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListChangesetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListChangesets.html#FinSpaceData.Paginator.ListChangesets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators/#listchangesetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListChangesetsRequestListChangesetsPaginateTypeDef]
    ) -> _PageIterator[ListChangesetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListChangesets.html#FinSpaceData.Paginator.ListChangesets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators/#listchangesetspaginator)
        """


class ListDataViewsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListDataViews.html#FinSpaceData.Paginator.ListDataViews)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators/#listdataviewspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDataViewsRequestListDataViewsPaginateTypeDef]
    ) -> _PageIterator[ListDataViewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListDataViews.html#FinSpaceData.Paginator.ListDataViews.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators/#listdataviewspaginator)
        """


class ListDatasetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListDatasets.html#FinSpaceData.Paginator.ListDatasets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators/#listdatasetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDatasetsRequestListDatasetsPaginateTypeDef]
    ) -> _PageIterator[ListDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListDatasets.html#FinSpaceData.Paginator.ListDatasets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators/#listdatasetspaginator)
        """


class ListPermissionGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListPermissionGroups.html#FinSpaceData.Paginator.ListPermissionGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators/#listpermissiongroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPermissionGroupsRequestListPermissionGroupsPaginateTypeDef]
    ) -> _PageIterator[ListPermissionGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListPermissionGroups.html#FinSpaceData.Paginator.ListPermissionGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators/#listpermissiongroupspaginator)
        """


class ListUsersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListUsers.html#FinSpaceData.Paginator.ListUsers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators/#listuserspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListUsersRequestListUsersPaginateTypeDef]
    ) -> _PageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListUsers.html#FinSpaceData.Paginator.ListUsers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators/#listuserspaginator)
        """
