"""
Type annotations for mediatailor service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_mediatailor.client import MediaTailorClient
    from mypy_boto3_mediatailor.paginator import (
        GetChannelSchedulePaginator,
        ListAlertsPaginator,
        ListChannelsPaginator,
        ListLiveSourcesPaginator,
        ListPlaybackConfigurationsPaginator,
        ListPrefetchSchedulesPaginator,
        ListSourceLocationsPaginator,
        ListVodSourcesPaginator,
    )

    session = Session()
    client: MediaTailorClient = session.client("mediatailor")

    get_channel_schedule_paginator: GetChannelSchedulePaginator = client.get_paginator("get_channel_schedule")
    list_alerts_paginator: ListAlertsPaginator = client.get_paginator("list_alerts")
    list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
    list_live_sources_paginator: ListLiveSourcesPaginator = client.get_paginator("list_live_sources")
    list_playback_configurations_paginator: ListPlaybackConfigurationsPaginator = client.get_paginator("list_playback_configurations")
    list_prefetch_schedules_paginator: ListPrefetchSchedulesPaginator = client.get_paginator("list_prefetch_schedules")
    list_source_locations_paginator: ListSourceLocationsPaginator = client.get_paginator("list_source_locations")
    list_vod_sources_paginator: ListVodSourcesPaginator = client.get_paginator("list_vod_sources")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetChannelScheduleRequestGetChannelSchedulePaginateTypeDef,
    GetChannelScheduleResponseTypeDef,
    ListAlertsRequestListAlertsPaginateTypeDef,
    ListAlertsResponseTypeDef,
    ListChannelsRequestListChannelsPaginateTypeDef,
    ListChannelsResponseTypeDef,
    ListLiveSourcesRequestListLiveSourcesPaginateTypeDef,
    ListLiveSourcesResponseTypeDef,
    ListPlaybackConfigurationsRequestListPlaybackConfigurationsPaginateTypeDef,
    ListPlaybackConfigurationsResponseTypeDef,
    ListPrefetchSchedulesRequestListPrefetchSchedulesPaginateTypeDef,
    ListPrefetchSchedulesResponseTypeDef,
    ListSourceLocationsRequestListSourceLocationsPaginateTypeDef,
    ListSourceLocationsResponseTypeDef,
    ListVodSourcesRequestListVodSourcesPaginateTypeDef,
    ListVodSourcesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetChannelSchedulePaginator",
    "ListAlertsPaginator",
    "ListChannelsPaginator",
    "ListLiveSourcesPaginator",
    "ListPlaybackConfigurationsPaginator",
    "ListPrefetchSchedulesPaginator",
    "ListSourceLocationsPaginator",
    "ListVodSourcesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetChannelSchedulePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/GetChannelSchedule.html#MediaTailor.Paginator.GetChannelSchedule)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/paginators/#getchannelschedulepaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetChannelScheduleRequestGetChannelSchedulePaginateTypeDef]
    ) -> _PageIterator[GetChannelScheduleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/GetChannelSchedule.html#MediaTailor.Paginator.GetChannelSchedule.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/paginators/#getchannelschedulepaginator)
        """


class ListAlertsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListAlerts.html#MediaTailor.Paginator.ListAlerts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/paginators/#listalertspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAlertsRequestListAlertsPaginateTypeDef]
    ) -> _PageIterator[ListAlertsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListAlerts.html#MediaTailor.Paginator.ListAlerts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/paginators/#listalertspaginator)
        """


class ListChannelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListChannels.html#MediaTailor.Paginator.ListChannels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/paginators/#listchannelspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListChannelsRequestListChannelsPaginateTypeDef]
    ) -> _PageIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListChannels.html#MediaTailor.Paginator.ListChannels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/paginators/#listchannelspaginator)
        """


class ListLiveSourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListLiveSources.html#MediaTailor.Paginator.ListLiveSources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/paginators/#listlivesourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListLiveSourcesRequestListLiveSourcesPaginateTypeDef]
    ) -> _PageIterator[ListLiveSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListLiveSources.html#MediaTailor.Paginator.ListLiveSources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/paginators/#listlivesourcespaginator)
        """


class ListPlaybackConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListPlaybackConfigurations.html#MediaTailor.Paginator.ListPlaybackConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/paginators/#listplaybackconfigurationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListPlaybackConfigurationsRequestListPlaybackConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListPlaybackConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListPlaybackConfigurations.html#MediaTailor.Paginator.ListPlaybackConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/paginators/#listplaybackconfigurationspaginator)
        """


class ListPrefetchSchedulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListPrefetchSchedules.html#MediaTailor.Paginator.ListPrefetchSchedules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/paginators/#listprefetchschedulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPrefetchSchedulesRequestListPrefetchSchedulesPaginateTypeDef]
    ) -> _PageIterator[ListPrefetchSchedulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListPrefetchSchedules.html#MediaTailor.Paginator.ListPrefetchSchedules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/paginators/#listprefetchschedulespaginator)
        """


class ListSourceLocationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListSourceLocations.html#MediaTailor.Paginator.ListSourceLocations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/paginators/#listsourcelocationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSourceLocationsRequestListSourceLocationsPaginateTypeDef]
    ) -> _PageIterator[ListSourceLocationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListSourceLocations.html#MediaTailor.Paginator.ListSourceLocations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/paginators/#listsourcelocationspaginator)
        """


class ListVodSourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListVodSources.html#MediaTailor.Paginator.ListVodSources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/paginators/#listvodsourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListVodSourcesRequestListVodSourcesPaginateTypeDef]
    ) -> _PageIterator[ListVodSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListVodSources.html#MediaTailor.Paginator.ListVodSources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/paginators/#listvodsourcespaginator)
        """
