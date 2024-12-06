"""
Type annotations for rum service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rum/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_rum.client import CloudWatchRUMClient
    from mypy_boto3_rum.paginator import (
        BatchGetRumMetricDefinitionsPaginator,
        GetAppMonitorDataPaginator,
        ListAppMonitorsPaginator,
        ListRumMetricsDestinationsPaginator,
    )

    session = Session()
    client: CloudWatchRUMClient = session.client("rum")

    batch_get_rum_metric_definitions_paginator: BatchGetRumMetricDefinitionsPaginator = client.get_paginator("batch_get_rum_metric_definitions")
    get_app_monitor_data_paginator: GetAppMonitorDataPaginator = client.get_paginator("get_app_monitor_data")
    list_app_monitors_paginator: ListAppMonitorsPaginator = client.get_paginator("list_app_monitors")
    list_rum_metrics_destinations_paginator: ListRumMetricsDestinationsPaginator = client.get_paginator("list_rum_metrics_destinations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    BatchGetRumMetricDefinitionsRequestBatchGetRumMetricDefinitionsPaginateTypeDef,
    BatchGetRumMetricDefinitionsResponseTypeDef,
    GetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef,
    GetAppMonitorDataResponseTypeDef,
    ListAppMonitorsRequestListAppMonitorsPaginateTypeDef,
    ListAppMonitorsResponseTypeDef,
    ListRumMetricsDestinationsRequestListRumMetricsDestinationsPaginateTypeDef,
    ListRumMetricsDestinationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "BatchGetRumMetricDefinitionsPaginator",
    "GetAppMonitorDataPaginator",
    "ListAppMonitorsPaginator",
    "ListRumMetricsDestinationsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class BatchGetRumMetricDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/BatchGetRumMetricDefinitions.html#CloudWatchRUM.Paginator.BatchGetRumMetricDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rum/paginators/#batchgetrummetricdefinitionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            BatchGetRumMetricDefinitionsRequestBatchGetRumMetricDefinitionsPaginateTypeDef
        ],
    ) -> _PageIterator[BatchGetRumMetricDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/BatchGetRumMetricDefinitions.html#CloudWatchRUM.Paginator.BatchGetRumMetricDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rum/paginators/#batchgetrummetricdefinitionspaginator)
        """

class GetAppMonitorDataPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/GetAppMonitorData.html#CloudWatchRUM.Paginator.GetAppMonitorData)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rum/paginators/#getappmonitordatapaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef]
    ) -> _PageIterator[GetAppMonitorDataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/GetAppMonitorData.html#CloudWatchRUM.Paginator.GetAppMonitorData.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rum/paginators/#getappmonitordatapaginator)
        """

class ListAppMonitorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/ListAppMonitors.html#CloudWatchRUM.Paginator.ListAppMonitors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rum/paginators/#listappmonitorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAppMonitorsRequestListAppMonitorsPaginateTypeDef]
    ) -> _PageIterator[ListAppMonitorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/ListAppMonitors.html#CloudWatchRUM.Paginator.ListAppMonitors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rum/paginators/#listappmonitorspaginator)
        """

class ListRumMetricsDestinationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/ListRumMetricsDestinations.html#CloudWatchRUM.Paginator.ListRumMetricsDestinations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rum/paginators/#listrummetricsdestinationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListRumMetricsDestinationsRequestListRumMetricsDestinationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListRumMetricsDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/ListRumMetricsDestinations.html#CloudWatchRUM.Paginator.ListRumMetricsDestinations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rum/paginators/#listrummetricsdestinationspaginator)
        """
