"""
Type annotations for mediapackage-vod service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackage_vod/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_mediapackage_vod.client import MediaPackageVodClient
    from mypy_boto3_mediapackage_vod.paginator import (
        ListAssetsPaginator,
        ListPackagingConfigurationsPaginator,
        ListPackagingGroupsPaginator,
    )

    session = Session()
    client: MediaPackageVodClient = session.client("mediapackage-vod")

    list_assets_paginator: ListAssetsPaginator = client.get_paginator("list_assets")
    list_packaging_configurations_paginator: ListPackagingConfigurationsPaginator = client.get_paginator("list_packaging_configurations")
    list_packaging_groups_paginator: ListPackagingGroupsPaginator = client.get_paginator("list_packaging_groups")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAssetsRequestListAssetsPaginateTypeDef,
    ListAssetsResponseTypeDef,
    ListPackagingConfigurationsRequestListPackagingConfigurationsPaginateTypeDef,
    ListPackagingConfigurationsResponseTypeDef,
    ListPackagingGroupsRequestListPackagingGroupsPaginateTypeDef,
    ListPackagingGroupsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAssetsPaginator",
    "ListPackagingConfigurationsPaginator",
    "ListPackagingGroupsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAssetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/paginator/ListAssets.html#MediaPackageVod.Paginator.ListAssets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackage_vod/paginators/#listassetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAssetsRequestListAssetsPaginateTypeDef]
    ) -> _PageIterator[ListAssetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/paginator/ListAssets.html#MediaPackageVod.Paginator.ListAssets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackage_vod/paginators/#listassetspaginator)
        """


class ListPackagingConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/paginator/ListPackagingConfigurations.html#MediaPackageVod.Paginator.ListPackagingConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackage_vod/paginators/#listpackagingconfigurationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListPackagingConfigurationsRequestListPackagingConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListPackagingConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/paginator/ListPackagingConfigurations.html#MediaPackageVod.Paginator.ListPackagingConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackage_vod/paginators/#listpackagingconfigurationspaginator)
        """


class ListPackagingGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/paginator/ListPackagingGroups.html#MediaPackageVod.Paginator.ListPackagingGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackage_vod/paginators/#listpackaginggroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPackagingGroupsRequestListPackagingGroupsPaginateTypeDef]
    ) -> _PageIterator[ListPackagingGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/paginator/ListPackagingGroups.html#MediaPackageVod.Paginator.ListPackagingGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackage_vod/paginators/#listpackaginggroupspaginator)
        """
