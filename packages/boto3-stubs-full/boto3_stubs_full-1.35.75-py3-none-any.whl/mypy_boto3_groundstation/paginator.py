"""
Type annotations for groundstation service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_groundstation.client import GroundStationClient
    from mypy_boto3_groundstation.paginator import (
        ListConfigsPaginator,
        ListContactsPaginator,
        ListDataflowEndpointGroupsPaginator,
        ListEphemeridesPaginator,
        ListGroundStationsPaginator,
        ListMissionProfilesPaginator,
        ListSatellitesPaginator,
    )

    session = Session()
    client: GroundStationClient = session.client("groundstation")

    list_configs_paginator: ListConfigsPaginator = client.get_paginator("list_configs")
    list_contacts_paginator: ListContactsPaginator = client.get_paginator("list_contacts")
    list_dataflow_endpoint_groups_paginator: ListDataflowEndpointGroupsPaginator = client.get_paginator("list_dataflow_endpoint_groups")
    list_ephemerides_paginator: ListEphemeridesPaginator = client.get_paginator("list_ephemerides")
    list_ground_stations_paginator: ListGroundStationsPaginator = client.get_paginator("list_ground_stations")
    list_mission_profiles_paginator: ListMissionProfilesPaginator = client.get_paginator("list_mission_profiles")
    list_satellites_paginator: ListSatellitesPaginator = client.get_paginator("list_satellites")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListConfigsRequestListConfigsPaginateTypeDef,
    ListConfigsResponseTypeDef,
    ListContactsRequestListContactsPaginateTypeDef,
    ListContactsResponseTypeDef,
    ListDataflowEndpointGroupsRequestListDataflowEndpointGroupsPaginateTypeDef,
    ListDataflowEndpointGroupsResponseTypeDef,
    ListEphemeridesRequestListEphemeridesPaginateTypeDef,
    ListEphemeridesResponseTypeDef,
    ListGroundStationsRequestListGroundStationsPaginateTypeDef,
    ListGroundStationsResponseTypeDef,
    ListMissionProfilesRequestListMissionProfilesPaginateTypeDef,
    ListMissionProfilesResponseTypeDef,
    ListSatellitesRequestListSatellitesPaginateTypeDef,
    ListSatellitesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListConfigsPaginator",
    "ListContactsPaginator",
    "ListDataflowEndpointGroupsPaginator",
    "ListEphemeridesPaginator",
    "ListGroundStationsPaginator",
    "ListMissionProfilesPaginator",
    "ListSatellitesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListConfigsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListConfigs.html#GroundStation.Paginator.ListConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listconfigspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListConfigsRequestListConfigsPaginateTypeDef]
    ) -> _PageIterator[ListConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListConfigs.html#GroundStation.Paginator.ListConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listconfigspaginator)
        """


class ListContactsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListContacts.html#GroundStation.Paginator.ListContacts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listcontactspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListContactsRequestListContactsPaginateTypeDef]
    ) -> _PageIterator[ListContactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListContacts.html#GroundStation.Paginator.ListContacts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listcontactspaginator)
        """


class ListDataflowEndpointGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListDataflowEndpointGroups.html#GroundStation.Paginator.ListDataflowEndpointGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listdataflowendpointgroupspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListDataflowEndpointGroupsRequestListDataflowEndpointGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[ListDataflowEndpointGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListDataflowEndpointGroups.html#GroundStation.Paginator.ListDataflowEndpointGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listdataflowendpointgroupspaginator)
        """


class ListEphemeridesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListEphemerides.html#GroundStation.Paginator.ListEphemerides)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listephemeridespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEphemeridesRequestListEphemeridesPaginateTypeDef]
    ) -> _PageIterator[ListEphemeridesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListEphemerides.html#GroundStation.Paginator.ListEphemerides.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listephemeridespaginator)
        """


class ListGroundStationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListGroundStations.html#GroundStation.Paginator.ListGroundStations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listgroundstationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGroundStationsRequestListGroundStationsPaginateTypeDef]
    ) -> _PageIterator[ListGroundStationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListGroundStations.html#GroundStation.Paginator.ListGroundStations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listgroundstationspaginator)
        """


class ListMissionProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListMissionProfiles.html#GroundStation.Paginator.ListMissionProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listmissionprofilespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMissionProfilesRequestListMissionProfilesPaginateTypeDef]
    ) -> _PageIterator[ListMissionProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListMissionProfiles.html#GroundStation.Paginator.ListMissionProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listmissionprofilespaginator)
        """


class ListSatellitesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListSatellites.html#GroundStation.Paginator.ListSatellites)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listsatellitespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSatellitesRequestListSatellitesPaginateTypeDef]
    ) -> _PageIterator[ListSatellitesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListSatellites.html#GroundStation.Paginator.ListSatellites.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listsatellitespaginator)
        """
