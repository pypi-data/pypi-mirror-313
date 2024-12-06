"""
Type annotations for mediapackagev2 service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackagev2/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_mediapackagev2.client import Mediapackagev2Client
    from mypy_boto3_mediapackagev2.paginator import (
        ListChannelGroupsPaginator,
        ListChannelsPaginator,
        ListHarvestJobsPaginator,
        ListOriginEndpointsPaginator,
    )

    session = Session()
    client: Mediapackagev2Client = session.client("mediapackagev2")

    list_channel_groups_paginator: ListChannelGroupsPaginator = client.get_paginator("list_channel_groups")
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
    ListChannelGroupsRequestListChannelGroupsPaginateTypeDef,
    ListChannelGroupsResponseTypeDef,
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

__all__ = (
    "ListChannelGroupsPaginator",
    "ListChannelsPaginator",
    "ListHarvestJobsPaginator",
    "ListOriginEndpointsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListChannelGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2/paginator/ListChannelGroups.html#Mediapackagev2.Paginator.ListChannelGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackagev2/paginators/#listchannelgroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListChannelGroupsRequestListChannelGroupsPaginateTypeDef]
    ) -> _PageIterator[ListChannelGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2/paginator/ListChannelGroups.html#Mediapackagev2.Paginator.ListChannelGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackagev2/paginators/#listchannelgroupspaginator)
        """

class ListChannelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2/paginator/ListChannels.html#Mediapackagev2.Paginator.ListChannels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackagev2/paginators/#listchannelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListChannelsRequestListChannelsPaginateTypeDef]
    ) -> _PageIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2/paginator/ListChannels.html#Mediapackagev2.Paginator.ListChannels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackagev2/paginators/#listchannelspaginator)
        """

class ListHarvestJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2/paginator/ListHarvestJobs.html#Mediapackagev2.Paginator.ListHarvestJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackagev2/paginators/#listharvestjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListHarvestJobsRequestListHarvestJobsPaginateTypeDef]
    ) -> _PageIterator[ListHarvestJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2/paginator/ListHarvestJobs.html#Mediapackagev2.Paginator.ListHarvestJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackagev2/paginators/#listharvestjobspaginator)
        """

class ListOriginEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2/paginator/ListOriginEndpoints.html#Mediapackagev2.Paginator.ListOriginEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackagev2/paginators/#listoriginendpointspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef]
    ) -> _PageIterator[ListOriginEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2/paginator/ListOriginEndpoints.html#Mediapackagev2.Paginator.ListOriginEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackagev2/paginators/#listoriginendpointspaginator)
        """
