"""
Type annotations for workspaces service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_workspaces.client import WorkSpacesClient
    from mypy_boto3_workspaces.paginator import (
        DescribeAccountModificationsPaginator,
        DescribeIpGroupsPaginator,
        DescribeWorkspaceBundlesPaginator,
        DescribeWorkspaceDirectoriesPaginator,
        DescribeWorkspaceImagesPaginator,
        DescribeWorkspacesConnectionStatusPaginator,
        DescribeWorkspacesPaginator,
        ListAccountLinksPaginator,
        ListAvailableManagementCidrRangesPaginator,
    )

    session = Session()
    client: WorkSpacesClient = session.client("workspaces")

    describe_account_modifications_paginator: DescribeAccountModificationsPaginator = client.get_paginator("describe_account_modifications")
    describe_ip_groups_paginator: DescribeIpGroupsPaginator = client.get_paginator("describe_ip_groups")
    describe_workspace_bundles_paginator: DescribeWorkspaceBundlesPaginator = client.get_paginator("describe_workspace_bundles")
    describe_workspace_directories_paginator: DescribeWorkspaceDirectoriesPaginator = client.get_paginator("describe_workspace_directories")
    describe_workspace_images_paginator: DescribeWorkspaceImagesPaginator = client.get_paginator("describe_workspace_images")
    describe_workspaces_connection_status_paginator: DescribeWorkspacesConnectionStatusPaginator = client.get_paginator("describe_workspaces_connection_status")
    describe_workspaces_paginator: DescribeWorkspacesPaginator = client.get_paginator("describe_workspaces")
    list_account_links_paginator: ListAccountLinksPaginator = client.get_paginator("list_account_links")
    list_available_management_cidr_ranges_paginator: ListAvailableManagementCidrRangesPaginator = client.get_paginator("list_available_management_cidr_ranges")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeAccountModificationsRequestDescribeAccountModificationsPaginateTypeDef,
    DescribeAccountModificationsResultTypeDef,
    DescribeIpGroupsRequestDescribeIpGroupsPaginateTypeDef,
    DescribeIpGroupsResultTypeDef,
    DescribeWorkspaceBundlesRequestDescribeWorkspaceBundlesPaginateTypeDef,
    DescribeWorkspaceBundlesResultTypeDef,
    DescribeWorkspaceDirectoriesRequestDescribeWorkspaceDirectoriesPaginateTypeDef,
    DescribeWorkspaceDirectoriesResultTypeDef,
    DescribeWorkspaceImagesRequestDescribeWorkspaceImagesPaginateTypeDef,
    DescribeWorkspaceImagesResultTypeDef,
    DescribeWorkspacesConnectionStatusRequestDescribeWorkspacesConnectionStatusPaginateTypeDef,
    DescribeWorkspacesConnectionStatusResultTypeDef,
    DescribeWorkspacesRequestDescribeWorkspacesPaginateTypeDef,
    DescribeWorkspacesResultTypeDef,
    ListAccountLinksRequestListAccountLinksPaginateTypeDef,
    ListAccountLinksResultTypeDef,
    ListAvailableManagementCidrRangesRequestListAvailableManagementCidrRangesPaginateTypeDef,
    ListAvailableManagementCidrRangesResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeAccountModificationsPaginator",
    "DescribeIpGroupsPaginator",
    "DescribeWorkspaceBundlesPaginator",
    "DescribeWorkspaceDirectoriesPaginator",
    "DescribeWorkspaceImagesPaginator",
    "DescribeWorkspacesConnectionStatusPaginator",
    "DescribeWorkspacesPaginator",
    "ListAccountLinksPaginator",
    "ListAvailableManagementCidrRangesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeAccountModificationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeAccountModifications.html#WorkSpaces.Paginator.DescribeAccountModifications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#describeaccountmodificationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAccountModificationsRequestDescribeAccountModificationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeAccountModificationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeAccountModifications.html#WorkSpaces.Paginator.DescribeAccountModifications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#describeaccountmodificationspaginator)
        """


class DescribeIpGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeIpGroups.html#WorkSpaces.Paginator.DescribeIpGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#describeipgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeIpGroupsRequestDescribeIpGroupsPaginateTypeDef]
    ) -> _PageIterator[DescribeIpGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeIpGroups.html#WorkSpaces.Paginator.DescribeIpGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#describeipgroupspaginator)
        """


class DescribeWorkspaceBundlesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspaceBundles.html#WorkSpaces.Paginator.DescribeWorkspaceBundles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#describeworkspacebundlespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeWorkspaceBundlesRequestDescribeWorkspaceBundlesPaginateTypeDef],
    ) -> _PageIterator[DescribeWorkspaceBundlesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspaceBundles.html#WorkSpaces.Paginator.DescribeWorkspaceBundles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#describeworkspacebundlespaginator)
        """


class DescribeWorkspaceDirectoriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspaceDirectories.html#WorkSpaces.Paginator.DescribeWorkspaceDirectories)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#describeworkspacedirectoriespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeWorkspaceDirectoriesRequestDescribeWorkspaceDirectoriesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeWorkspaceDirectoriesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspaceDirectories.html#WorkSpaces.Paginator.DescribeWorkspaceDirectories.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#describeworkspacedirectoriespaginator)
        """


class DescribeWorkspaceImagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspaceImages.html#WorkSpaces.Paginator.DescribeWorkspaceImages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#describeworkspaceimagespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeWorkspaceImagesRequestDescribeWorkspaceImagesPaginateTypeDef]
    ) -> _PageIterator[DescribeWorkspaceImagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspaceImages.html#WorkSpaces.Paginator.DescribeWorkspaceImages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#describeworkspaceimagespaginator)
        """


class DescribeWorkspacesConnectionStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspacesConnectionStatus.html#WorkSpaces.Paginator.DescribeWorkspacesConnectionStatus)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#describeworkspacesconnectionstatuspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeWorkspacesConnectionStatusRequestDescribeWorkspacesConnectionStatusPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeWorkspacesConnectionStatusResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspacesConnectionStatus.html#WorkSpaces.Paginator.DescribeWorkspacesConnectionStatus.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#describeworkspacesconnectionstatuspaginator)
        """


class DescribeWorkspacesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspaces.html#WorkSpaces.Paginator.DescribeWorkspaces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#describeworkspacespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeWorkspacesRequestDescribeWorkspacesPaginateTypeDef]
    ) -> _PageIterator[DescribeWorkspacesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspaces.html#WorkSpaces.Paginator.DescribeWorkspaces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#describeworkspacespaginator)
        """


class ListAccountLinksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/ListAccountLinks.html#WorkSpaces.Paginator.ListAccountLinks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#listaccountlinkspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAccountLinksRequestListAccountLinksPaginateTypeDef]
    ) -> _PageIterator[ListAccountLinksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/ListAccountLinks.html#WorkSpaces.Paginator.ListAccountLinks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#listaccountlinkspaginator)
        """


class ListAvailableManagementCidrRangesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/ListAvailableManagementCidrRanges.html#WorkSpaces.Paginator.ListAvailableManagementCidrRanges)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#listavailablemanagementcidrrangespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListAvailableManagementCidrRangesRequestListAvailableManagementCidrRangesPaginateTypeDef
        ],
    ) -> _PageIterator[ListAvailableManagementCidrRangesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/ListAvailableManagementCidrRanges.html#WorkSpaces.Paginator.ListAvailableManagementCidrRanges.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/paginators/#listavailablemanagementcidrrangespaginator)
        """
