"""
Type annotations for internetmonitor service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_internetmonitor/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_internetmonitor.client import CloudWatchInternetMonitorClient
    from mypy_boto3_internetmonitor.paginator import (
        ListHealthEventsPaginator,
        ListInternetEventsPaginator,
        ListMonitorsPaginator,
    )

    session = Session()
    client: CloudWatchInternetMonitorClient = session.client("internetmonitor")

    list_health_events_paginator: ListHealthEventsPaginator = client.get_paginator("list_health_events")
    list_internet_events_paginator: ListInternetEventsPaginator = client.get_paginator("list_internet_events")
    list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListHealthEventsInputListHealthEventsPaginateTypeDef,
    ListHealthEventsOutputTypeDef,
    ListInternetEventsInputListInternetEventsPaginateTypeDef,
    ListInternetEventsOutputTypeDef,
    ListMonitorsInputListMonitorsPaginateTypeDef,
    ListMonitorsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListHealthEventsPaginator", "ListInternetEventsPaginator", "ListMonitorsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListHealthEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/paginator/ListHealthEvents.html#CloudWatchInternetMonitor.Paginator.ListHealthEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_internetmonitor/paginators/#listhealtheventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListHealthEventsInputListHealthEventsPaginateTypeDef]
    ) -> _PageIterator[ListHealthEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/paginator/ListHealthEvents.html#CloudWatchInternetMonitor.Paginator.ListHealthEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_internetmonitor/paginators/#listhealtheventspaginator)
        """

class ListInternetEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/paginator/ListInternetEvents.html#CloudWatchInternetMonitor.Paginator.ListInternetEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_internetmonitor/paginators/#listinterneteventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInternetEventsInputListInternetEventsPaginateTypeDef]
    ) -> _PageIterator[ListInternetEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/paginator/ListInternetEvents.html#CloudWatchInternetMonitor.Paginator.ListInternetEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_internetmonitor/paginators/#listinterneteventspaginator)
        """

class ListMonitorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/paginator/ListMonitors.html#CloudWatchInternetMonitor.Paginator.ListMonitors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_internetmonitor/paginators/#listmonitorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMonitorsInputListMonitorsPaginateTypeDef]
    ) -> _PageIterator[ListMonitorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/paginator/ListMonitors.html#CloudWatchInternetMonitor.Paginator.ListMonitors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_internetmonitor/paginators/#listmonitorspaginator)
        """
