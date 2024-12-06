"""
Type annotations for appstream service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_appstream.client import AppStreamClient
    from mypy_boto3_appstream.paginator import (
        DescribeDirectoryConfigsPaginator,
        DescribeFleetsPaginator,
        DescribeImageBuildersPaginator,
        DescribeImagesPaginator,
        DescribeSessionsPaginator,
        DescribeStacksPaginator,
        DescribeUserStackAssociationsPaginator,
        DescribeUsersPaginator,
        ListAssociatedFleetsPaginator,
        ListAssociatedStacksPaginator,
    )

    session = Session()
    client: AppStreamClient = session.client("appstream")

    describe_directory_configs_paginator: DescribeDirectoryConfigsPaginator = client.get_paginator("describe_directory_configs")
    describe_fleets_paginator: DescribeFleetsPaginator = client.get_paginator("describe_fleets")
    describe_image_builders_paginator: DescribeImageBuildersPaginator = client.get_paginator("describe_image_builders")
    describe_images_paginator: DescribeImagesPaginator = client.get_paginator("describe_images")
    describe_sessions_paginator: DescribeSessionsPaginator = client.get_paginator("describe_sessions")
    describe_stacks_paginator: DescribeStacksPaginator = client.get_paginator("describe_stacks")
    describe_user_stack_associations_paginator: DescribeUserStackAssociationsPaginator = client.get_paginator("describe_user_stack_associations")
    describe_users_paginator: DescribeUsersPaginator = client.get_paginator("describe_users")
    list_associated_fleets_paginator: ListAssociatedFleetsPaginator = client.get_paginator("list_associated_fleets")
    list_associated_stacks_paginator: ListAssociatedStacksPaginator = client.get_paginator("list_associated_stacks")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeDirectoryConfigsRequestDescribeDirectoryConfigsPaginateTypeDef,
    DescribeDirectoryConfigsResultTypeDef,
    DescribeFleetsRequestDescribeFleetsPaginateTypeDef,
    DescribeFleetsResultTypeDef,
    DescribeImageBuildersRequestDescribeImageBuildersPaginateTypeDef,
    DescribeImageBuildersResultTypeDef,
    DescribeImagesRequestDescribeImagesPaginateTypeDef,
    DescribeImagesResultTypeDef,
    DescribeSessionsRequestDescribeSessionsPaginateTypeDef,
    DescribeSessionsResultTypeDef,
    DescribeStacksRequestDescribeStacksPaginateTypeDef,
    DescribeStacksResultTypeDef,
    DescribeUsersRequestDescribeUsersPaginateTypeDef,
    DescribeUsersResultTypeDef,
    DescribeUserStackAssociationsRequestDescribeUserStackAssociationsPaginateTypeDef,
    DescribeUserStackAssociationsResultTypeDef,
    ListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef,
    ListAssociatedFleetsResultTypeDef,
    ListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef,
    ListAssociatedStacksResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeDirectoryConfigsPaginator",
    "DescribeFleetsPaginator",
    "DescribeImageBuildersPaginator",
    "DescribeImagesPaginator",
    "DescribeSessionsPaginator",
    "DescribeStacksPaginator",
    "DescribeUserStackAssociationsPaginator",
    "DescribeUsersPaginator",
    "ListAssociatedFleetsPaginator",
    "ListAssociatedStacksPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeDirectoryConfigsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeDirectoryConfigs.html#AppStream.Paginator.DescribeDirectoryConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#describedirectoryconfigspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeDirectoryConfigsRequestDescribeDirectoryConfigsPaginateTypeDef],
    ) -> _PageIterator[DescribeDirectoryConfigsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeDirectoryConfigs.html#AppStream.Paginator.DescribeDirectoryConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#describedirectoryconfigspaginator)
        """


class DescribeFleetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeFleets.html#AppStream.Paginator.DescribeFleets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#describefleetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeFleetsRequestDescribeFleetsPaginateTypeDef]
    ) -> _PageIterator[DescribeFleetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeFleets.html#AppStream.Paginator.DescribeFleets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#describefleetspaginator)
        """


class DescribeImageBuildersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeImageBuilders.html#AppStream.Paginator.DescribeImageBuilders)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#describeimagebuilderspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeImageBuildersRequestDescribeImageBuildersPaginateTypeDef]
    ) -> _PageIterator[DescribeImageBuildersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeImageBuilders.html#AppStream.Paginator.DescribeImageBuilders.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#describeimagebuilderspaginator)
        """


class DescribeImagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeImages.html#AppStream.Paginator.DescribeImages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#describeimagespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeImagesRequestDescribeImagesPaginateTypeDef]
    ) -> _PageIterator[DescribeImagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeImages.html#AppStream.Paginator.DescribeImages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#describeimagespaginator)
        """


class DescribeSessionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeSessions.html#AppStream.Paginator.DescribeSessions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#describesessionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeSessionsRequestDescribeSessionsPaginateTypeDef]
    ) -> _PageIterator[DescribeSessionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeSessions.html#AppStream.Paginator.DescribeSessions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#describesessionspaginator)
        """


class DescribeStacksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeStacks.html#AppStream.Paginator.DescribeStacks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#describestackspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeStacksRequestDescribeStacksPaginateTypeDef]
    ) -> _PageIterator[DescribeStacksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeStacks.html#AppStream.Paginator.DescribeStacks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#describestackspaginator)
        """


class DescribeUserStackAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeUserStackAssociations.html#AppStream.Paginator.DescribeUserStackAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#describeuserstackassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeUserStackAssociationsRequestDescribeUserStackAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeUserStackAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeUserStackAssociations.html#AppStream.Paginator.DescribeUserStackAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#describeuserstackassociationspaginator)
        """


class DescribeUsersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeUsers.html#AppStream.Paginator.DescribeUsers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#describeuserspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeUsersRequestDescribeUsersPaginateTypeDef]
    ) -> _PageIterator[DescribeUsersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeUsers.html#AppStream.Paginator.DescribeUsers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#describeuserspaginator)
        """


class ListAssociatedFleetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/ListAssociatedFleets.html#AppStream.Paginator.ListAssociatedFleets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#listassociatedfleetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef]
    ) -> _PageIterator[ListAssociatedFleetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/ListAssociatedFleets.html#AppStream.Paginator.ListAssociatedFleets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#listassociatedfleetspaginator)
        """


class ListAssociatedStacksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/ListAssociatedStacks.html#AppStream.Paginator.ListAssociatedStacks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#listassociatedstackspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef]
    ) -> _PageIterator[ListAssociatedStacksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/ListAssociatedStacks.html#AppStream.Paginator.ListAssociatedStacks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/paginators/#listassociatedstackspaginator)
        """
