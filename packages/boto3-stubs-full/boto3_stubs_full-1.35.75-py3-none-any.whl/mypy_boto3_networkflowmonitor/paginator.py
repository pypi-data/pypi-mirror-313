"""
Type annotations for networkflowmonitor service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_networkflowmonitor.client import NetworkFlowMonitorClient
    from mypy_boto3_networkflowmonitor.paginator import (
        GetQueryResultsMonitorTopContributorsPaginator,
        GetQueryResultsWorkloadInsightsTopContributorsDataPaginator,
        GetQueryResultsWorkloadInsightsTopContributorsPaginator,
        ListMonitorsPaginator,
        ListScopesPaginator,
    )

    session = Session()
    client: NetworkFlowMonitorClient = session.client("networkflowmonitor")

    get_query_results_monitor_top_contributors_paginator: GetQueryResultsMonitorTopContributorsPaginator = client.get_paginator("get_query_results_monitor_top_contributors")
    get_query_results_workload_insights_top_contributors_data_paginator: GetQueryResultsWorkloadInsightsTopContributorsDataPaginator = client.get_paginator("get_query_results_workload_insights_top_contributors_data")
    get_query_results_workload_insights_top_contributors_paginator: GetQueryResultsWorkloadInsightsTopContributorsPaginator = client.get_paginator("get_query_results_workload_insights_top_contributors")
    list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
    list_scopes_paginator: ListScopesPaginator = client.get_paginator("list_scopes")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetQueryResultsMonitorTopContributorsInputGetQueryResultsMonitorTopContributorsPaginateTypeDef,
    GetQueryResultsMonitorTopContributorsOutputTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsDataInputGetQueryResultsWorkloadInsightsTopContributorsDataPaginateTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsDataOutputTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsInputGetQueryResultsWorkloadInsightsTopContributorsPaginateTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsOutputTypeDef,
    ListMonitorsInputListMonitorsPaginateTypeDef,
    ListMonitorsOutputTypeDef,
    ListScopesInputListScopesPaginateTypeDef,
    ListScopesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetQueryResultsMonitorTopContributorsPaginator",
    "GetQueryResultsWorkloadInsightsTopContributorsDataPaginator",
    "GetQueryResultsWorkloadInsightsTopContributorsPaginator",
    "ListMonitorsPaginator",
    "ListScopesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetQueryResultsMonitorTopContributorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsMonitorTopContributors.html#NetworkFlowMonitor.Paginator.GetQueryResultsMonitorTopContributors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/paginators/#getqueryresultsmonitortopcontributorspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetQueryResultsMonitorTopContributorsInputGetQueryResultsMonitorTopContributorsPaginateTypeDef
        ],
    ) -> _PageIterator[GetQueryResultsMonitorTopContributorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsMonitorTopContributors.html#NetworkFlowMonitor.Paginator.GetQueryResultsMonitorTopContributors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/paginators/#getqueryresultsmonitortopcontributorspaginator)
        """


class GetQueryResultsWorkloadInsightsTopContributorsDataPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsWorkloadInsightsTopContributorsData.html#NetworkFlowMonitor.Paginator.GetQueryResultsWorkloadInsightsTopContributorsData)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/paginators/#getqueryresultsworkloadinsightstopcontributorsdatapaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetQueryResultsWorkloadInsightsTopContributorsDataInputGetQueryResultsWorkloadInsightsTopContributorsDataPaginateTypeDef
        ],
    ) -> _PageIterator[GetQueryResultsWorkloadInsightsTopContributorsDataOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsWorkloadInsightsTopContributorsData.html#NetworkFlowMonitor.Paginator.GetQueryResultsWorkloadInsightsTopContributorsData.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/paginators/#getqueryresultsworkloadinsightstopcontributorsdatapaginator)
        """


class GetQueryResultsWorkloadInsightsTopContributorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsWorkloadInsightsTopContributors.html#NetworkFlowMonitor.Paginator.GetQueryResultsWorkloadInsightsTopContributors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/paginators/#getqueryresultsworkloadinsightstopcontributorspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetQueryResultsWorkloadInsightsTopContributorsInputGetQueryResultsWorkloadInsightsTopContributorsPaginateTypeDef
        ],
    ) -> _PageIterator[GetQueryResultsWorkloadInsightsTopContributorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsWorkloadInsightsTopContributors.html#NetworkFlowMonitor.Paginator.GetQueryResultsWorkloadInsightsTopContributors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/paginators/#getqueryresultsworkloadinsightstopcontributorspaginator)
        """


class ListMonitorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListMonitors.html#NetworkFlowMonitor.Paginator.ListMonitors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/paginators/#listmonitorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMonitorsInputListMonitorsPaginateTypeDef]
    ) -> _PageIterator[ListMonitorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListMonitors.html#NetworkFlowMonitor.Paginator.ListMonitors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/paginators/#listmonitorspaginator)
        """


class ListScopesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListScopes.html#NetworkFlowMonitor.Paginator.ListScopes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/paginators/#listscopespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListScopesInputListScopesPaginateTypeDef]
    ) -> _PageIterator[ListScopesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListScopes.html#NetworkFlowMonitor.Paginator.ListScopes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/paginators/#listscopespaginator)
        """
