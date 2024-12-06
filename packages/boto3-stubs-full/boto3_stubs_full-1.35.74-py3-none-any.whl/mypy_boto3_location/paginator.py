"""
Type annotations for location service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_location.client import LocationServiceClient
    from mypy_boto3_location.paginator import (
        ForecastGeofenceEventsPaginator,
        GetDevicePositionHistoryPaginator,
        ListDevicePositionsPaginator,
        ListGeofenceCollectionsPaginator,
        ListGeofencesPaginator,
        ListKeysPaginator,
        ListMapsPaginator,
        ListPlaceIndexesPaginator,
        ListRouteCalculatorsPaginator,
        ListTrackerConsumersPaginator,
        ListTrackersPaginator,
    )

    session = Session()
    client: LocationServiceClient = session.client("location")

    forecast_geofence_events_paginator: ForecastGeofenceEventsPaginator = client.get_paginator("forecast_geofence_events")
    get_device_position_history_paginator: GetDevicePositionHistoryPaginator = client.get_paginator("get_device_position_history")
    list_device_positions_paginator: ListDevicePositionsPaginator = client.get_paginator("list_device_positions")
    list_geofence_collections_paginator: ListGeofenceCollectionsPaginator = client.get_paginator("list_geofence_collections")
    list_geofences_paginator: ListGeofencesPaginator = client.get_paginator("list_geofences")
    list_keys_paginator: ListKeysPaginator = client.get_paginator("list_keys")
    list_maps_paginator: ListMapsPaginator = client.get_paginator("list_maps")
    list_place_indexes_paginator: ListPlaceIndexesPaginator = client.get_paginator("list_place_indexes")
    list_route_calculators_paginator: ListRouteCalculatorsPaginator = client.get_paginator("list_route_calculators")
    list_tracker_consumers_paginator: ListTrackerConsumersPaginator = client.get_paginator("list_tracker_consumers")
    list_trackers_paginator: ListTrackersPaginator = client.get_paginator("list_trackers")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ForecastGeofenceEventsRequestForecastGeofenceEventsPaginateTypeDef,
    ForecastGeofenceEventsResponseTypeDef,
    GetDevicePositionHistoryRequestGetDevicePositionHistoryPaginateTypeDef,
    GetDevicePositionHistoryResponseTypeDef,
    ListDevicePositionsRequestListDevicePositionsPaginateTypeDef,
    ListDevicePositionsResponseTypeDef,
    ListGeofenceCollectionsRequestListGeofenceCollectionsPaginateTypeDef,
    ListGeofenceCollectionsResponseTypeDef,
    ListGeofencesRequestListGeofencesPaginateTypeDef,
    ListGeofencesResponseTypeDef,
    ListKeysRequestListKeysPaginateTypeDef,
    ListKeysResponseTypeDef,
    ListMapsRequestListMapsPaginateTypeDef,
    ListMapsResponseTypeDef,
    ListPlaceIndexesRequestListPlaceIndexesPaginateTypeDef,
    ListPlaceIndexesResponseTypeDef,
    ListRouteCalculatorsRequestListRouteCalculatorsPaginateTypeDef,
    ListRouteCalculatorsResponseTypeDef,
    ListTrackerConsumersRequestListTrackerConsumersPaginateTypeDef,
    ListTrackerConsumersResponseTypeDef,
    ListTrackersRequestListTrackersPaginateTypeDef,
    ListTrackersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ForecastGeofenceEventsPaginator",
    "GetDevicePositionHistoryPaginator",
    "ListDevicePositionsPaginator",
    "ListGeofenceCollectionsPaginator",
    "ListGeofencesPaginator",
    "ListKeysPaginator",
    "ListMapsPaginator",
    "ListPlaceIndexesPaginator",
    "ListRouteCalculatorsPaginator",
    "ListTrackerConsumersPaginator",
    "ListTrackersPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ForecastGeofenceEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ForecastGeofenceEvents.html#LocationService.Paginator.ForecastGeofenceEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#forecastgeofenceeventspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ForecastGeofenceEventsRequestForecastGeofenceEventsPaginateTypeDef]
    ) -> _PageIterator[ForecastGeofenceEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ForecastGeofenceEvents.html#LocationService.Paginator.ForecastGeofenceEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#forecastgeofenceeventspaginator)
        """


class GetDevicePositionHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/GetDevicePositionHistory.html#LocationService.Paginator.GetDevicePositionHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#getdevicepositionhistorypaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[GetDevicePositionHistoryRequestGetDevicePositionHistoryPaginateTypeDef],
    ) -> _PageIterator[GetDevicePositionHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/GetDevicePositionHistory.html#LocationService.Paginator.GetDevicePositionHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#getdevicepositionhistorypaginator)
        """


class ListDevicePositionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListDevicePositions.html#LocationService.Paginator.ListDevicePositions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listdevicepositionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDevicePositionsRequestListDevicePositionsPaginateTypeDef]
    ) -> _PageIterator[ListDevicePositionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListDevicePositions.html#LocationService.Paginator.ListDevicePositions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listdevicepositionspaginator)
        """


class ListGeofenceCollectionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListGeofenceCollections.html#LocationService.Paginator.ListGeofenceCollections)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listgeofencecollectionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGeofenceCollectionsRequestListGeofenceCollectionsPaginateTypeDef]
    ) -> _PageIterator[ListGeofenceCollectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListGeofenceCollections.html#LocationService.Paginator.ListGeofenceCollections.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listgeofencecollectionspaginator)
        """


class ListGeofencesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListGeofences.html#LocationService.Paginator.ListGeofences)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listgeofencespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGeofencesRequestListGeofencesPaginateTypeDef]
    ) -> _PageIterator[ListGeofencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListGeofences.html#LocationService.Paginator.ListGeofences.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listgeofencespaginator)
        """


class ListKeysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListKeys.html#LocationService.Paginator.ListKeys)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listkeyspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListKeysRequestListKeysPaginateTypeDef]
    ) -> _PageIterator[ListKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListKeys.html#LocationService.Paginator.ListKeys.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listkeyspaginator)
        """


class ListMapsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListMaps.html#LocationService.Paginator.ListMaps)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listmapspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMapsRequestListMapsPaginateTypeDef]
    ) -> _PageIterator[ListMapsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListMaps.html#LocationService.Paginator.ListMaps.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listmapspaginator)
        """


class ListPlaceIndexesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListPlaceIndexes.html#LocationService.Paginator.ListPlaceIndexes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listplaceindexespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPlaceIndexesRequestListPlaceIndexesPaginateTypeDef]
    ) -> _PageIterator[ListPlaceIndexesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListPlaceIndexes.html#LocationService.Paginator.ListPlaceIndexes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listplaceindexespaginator)
        """


class ListRouteCalculatorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListRouteCalculators.html#LocationService.Paginator.ListRouteCalculators)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listroutecalculatorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRouteCalculatorsRequestListRouteCalculatorsPaginateTypeDef]
    ) -> _PageIterator[ListRouteCalculatorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListRouteCalculators.html#LocationService.Paginator.ListRouteCalculators.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listroutecalculatorspaginator)
        """


class ListTrackerConsumersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListTrackerConsumers.html#LocationService.Paginator.ListTrackerConsumers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listtrackerconsumerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTrackerConsumersRequestListTrackerConsumersPaginateTypeDef]
    ) -> _PageIterator[ListTrackerConsumersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListTrackerConsumers.html#LocationService.Paginator.ListTrackerConsumers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listtrackerconsumerspaginator)
        """


class ListTrackersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListTrackers.html#LocationService.Paginator.ListTrackers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listtrackerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTrackersRequestListTrackersPaginateTypeDef]
    ) -> _PageIterator[ListTrackersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListTrackers.html#LocationService.Paginator.ListTrackers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/paginators/#listtrackerspaginator)
        """
