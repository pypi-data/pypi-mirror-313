"""
Type annotations for mediapackage service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackage/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_mediapackage.client import MediaPackageClient
    from mypy_boto3_mediapackage.paginator import (
        ListChannelsPaginator,
        ListHarvestJobsPaginator,
        ListOriginEndpointsPaginator,
    )

    session = Session()
    client: MediaPackageClient = session.client("mediapackage")

    list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
    list_harvest_jobs_paginator: ListHarvestJobsPaginator = client.get_paginator("list_harvest_jobs")
    list_origin_endpoints_paginator: ListOriginEndpointsPaginator = client.get_paginator("list_origin_endpoints")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListChannelsRequestListChannelsPaginateTypeDef,
    ListChannelsResponseTypeDef,
    ListHarvestJobsRequestListHarvestJobsPaginateTypeDef,
    ListHarvestJobsResponseTypeDef,
    ListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef,
    ListOriginEndpointsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListChannelsPaginator", "ListHarvestJobsPaginator", "ListOriginEndpointsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListChannelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/paginator/ListChannels.html#MediaPackage.Paginator.ListChannels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackage/paginators/#listchannelspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListChannelsRequestListChannelsPaginateTypeDef]
    ) -> _PageIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/paginator/ListChannels.html#MediaPackage.Paginator.ListChannels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackage/paginators/#listchannelspaginator)
        """


class ListHarvestJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/paginator/ListHarvestJobs.html#MediaPackage.Paginator.ListHarvestJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackage/paginators/#listharvestjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListHarvestJobsRequestListHarvestJobsPaginateTypeDef]
    ) -> _PageIterator[ListHarvestJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/paginator/ListHarvestJobs.html#MediaPackage.Paginator.ListHarvestJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackage/paginators/#listharvestjobspaginator)
        """


class ListOriginEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/paginator/ListOriginEndpoints.html#MediaPackage.Paginator.ListOriginEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackage/paginators/#listoriginendpointspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef]
    ) -> _PageIterator[ListOriginEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/paginator/ListOriginEndpoints.html#MediaPackage.Paginator.ListOriginEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackage/paginators/#listoriginendpointspaginator)
        """
