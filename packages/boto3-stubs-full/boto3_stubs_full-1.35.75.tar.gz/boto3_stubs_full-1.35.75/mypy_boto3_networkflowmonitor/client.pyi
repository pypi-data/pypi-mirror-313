"""
Type annotations for networkflowmonitor service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_networkflowmonitor.client import NetworkFlowMonitorClient

    session = Session()
    client: NetworkFlowMonitorClient = session.client("networkflowmonitor")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    GetQueryResultsMonitorTopContributorsPaginator,
    GetQueryResultsWorkloadInsightsTopContributorsDataPaginator,
    GetQueryResultsWorkloadInsightsTopContributorsPaginator,
    ListMonitorsPaginator,
    ListScopesPaginator,
)
from .type_defs import (
    CreateMonitorInputRequestTypeDef,
    CreateMonitorOutputTypeDef,
    CreateScopeInputRequestTypeDef,
    CreateScopeOutputTypeDef,
    DeleteMonitorInputRequestTypeDef,
    DeleteScopeInputRequestTypeDef,
    GetMonitorInputRequestTypeDef,
    GetMonitorOutputTypeDef,
    GetQueryResultsMonitorTopContributorsInputRequestTypeDef,
    GetQueryResultsMonitorTopContributorsOutputTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsDataInputRequestTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsDataOutputTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsInputRequestTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsOutputTypeDef,
    GetQueryStatusMonitorTopContributorsInputRequestTypeDef,
    GetQueryStatusMonitorTopContributorsOutputTypeDef,
    GetQueryStatusWorkloadInsightsTopContributorsDataInputRequestTypeDef,
    GetQueryStatusWorkloadInsightsTopContributorsDataOutputTypeDef,
    GetQueryStatusWorkloadInsightsTopContributorsInputRequestTypeDef,
    GetQueryStatusWorkloadInsightsTopContributorsOutputTypeDef,
    GetScopeInputRequestTypeDef,
    GetScopeOutputTypeDef,
    ListMonitorsInputRequestTypeDef,
    ListMonitorsOutputTypeDef,
    ListScopesInputRequestTypeDef,
    ListScopesOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    StartQueryMonitorTopContributorsInputRequestTypeDef,
    StartQueryMonitorTopContributorsOutputTypeDef,
    StartQueryWorkloadInsightsTopContributorsDataInputRequestTypeDef,
    StartQueryWorkloadInsightsTopContributorsDataOutputTypeDef,
    StartQueryWorkloadInsightsTopContributorsInputRequestTypeDef,
    StartQueryWorkloadInsightsTopContributorsOutputTypeDef,
    StopQueryMonitorTopContributorsInputRequestTypeDef,
    StopQueryWorkloadInsightsTopContributorsDataInputRequestTypeDef,
    StopQueryWorkloadInsightsTopContributorsInputRequestTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateMonitorInputRequestTypeDef,
    UpdateMonitorOutputTypeDef,
    UpdateScopeInputRequestTypeDef,
    UpdateScopeOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("NetworkFlowMonitorClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class NetworkFlowMonitorClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor.html#NetworkFlowMonitor.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        NetworkFlowMonitorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor.html#NetworkFlowMonitor.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#close)
        """

    def create_monitor(
        self, **kwargs: Unpack[CreateMonitorInputRequestTypeDef]
    ) -> CreateMonitorOutputTypeDef:
        """
        Create a monitor for specific network flows between local and remote resources,
        so that you can monitor network performance for one or several of your
        workloads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/create_monitor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#create_monitor)
        """

    def create_scope(
        self, **kwargs: Unpack[CreateScopeInputRequestTypeDef]
    ) -> CreateScopeOutputTypeDef:
        """
        Create a scope of resources that you want to be available for Network Flow
        Monitor to generate metrics for, when you have active agents on those resources
        sending metrics reports to the Network Flow Monitor backend.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/create_scope.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#create_scope)
        """

    def delete_monitor(self, **kwargs: Unpack[DeleteMonitorInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a monitor in Network Flow Monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/delete_monitor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#delete_monitor)
        """

    def delete_scope(self, **kwargs: Unpack[DeleteScopeInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a scope that has been defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/delete_scope.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#delete_scope)
        """

    def get_monitor(
        self, **kwargs: Unpack[GetMonitorInputRequestTypeDef]
    ) -> GetMonitorOutputTypeDef:
        """
        Gets information about a monitor in Network Flow Monitor based on a monitor
        name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/get_monitor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#get_monitor)
        """

    def get_query_results_monitor_top_contributors(
        self, **kwargs: Unpack[GetQueryResultsMonitorTopContributorsInputRequestTypeDef]
    ) -> GetQueryResultsMonitorTopContributorsOutputTypeDef:
        """
        Return the data for a query with the Network Flow Monitor query interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/get_query_results_monitor_top_contributors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#get_query_results_monitor_top_contributors)
        """

    def get_query_results_workload_insights_top_contributors(
        self, **kwargs: Unpack[GetQueryResultsWorkloadInsightsTopContributorsInputRequestTypeDef]
    ) -> GetQueryResultsWorkloadInsightsTopContributorsOutputTypeDef:
        """
        Return the data for a query with the Network Flow Monitor query interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/get_query_results_workload_insights_top_contributors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#get_query_results_workload_insights_top_contributors)
        """

    def get_query_results_workload_insights_top_contributors_data(
        self,
        **kwargs: Unpack[GetQueryResultsWorkloadInsightsTopContributorsDataInputRequestTypeDef],
    ) -> GetQueryResultsWorkloadInsightsTopContributorsDataOutputTypeDef:
        """
        Return the data for a query with the Network Flow Monitor query interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/get_query_results_workload_insights_top_contributors_data.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#get_query_results_workload_insights_top_contributors_data)
        """

    def get_query_status_monitor_top_contributors(
        self, **kwargs: Unpack[GetQueryStatusMonitorTopContributorsInputRequestTypeDef]
    ) -> GetQueryStatusMonitorTopContributorsOutputTypeDef:
        """
        Returns the current status of a query for the Network Flow Monitor query
        interface, for a specified query ID and monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/get_query_status_monitor_top_contributors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#get_query_status_monitor_top_contributors)
        """

    def get_query_status_workload_insights_top_contributors(
        self, **kwargs: Unpack[GetQueryStatusWorkloadInsightsTopContributorsInputRequestTypeDef]
    ) -> GetQueryStatusWorkloadInsightsTopContributorsOutputTypeDef:
        """
        Return the data for a query with the Network Flow Monitor query interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/get_query_status_workload_insights_top_contributors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#get_query_status_workload_insights_top_contributors)
        """

    def get_query_status_workload_insights_top_contributors_data(
        self, **kwargs: Unpack[GetQueryStatusWorkloadInsightsTopContributorsDataInputRequestTypeDef]
    ) -> GetQueryStatusWorkloadInsightsTopContributorsDataOutputTypeDef:
        """
        Returns the current status of a query for the Network Flow Monitor query
        interface, for a specified query ID and monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/get_query_status_workload_insights_top_contributors_data.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#get_query_status_workload_insights_top_contributors_data)
        """

    def get_scope(self, **kwargs: Unpack[GetScopeInputRequestTypeDef]) -> GetScopeOutputTypeDef:
        """
        Gets information about a scope, including the name, status, tags, and target
        details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/get_scope.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#get_scope)
        """

    def list_monitors(
        self, **kwargs: Unpack[ListMonitorsInputRequestTypeDef]
    ) -> ListMonitorsOutputTypeDef:
        """
        List all monitors in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/list_monitors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#list_monitors)
        """

    def list_scopes(
        self, **kwargs: Unpack[ListScopesInputRequestTypeDef]
    ) -> ListScopesOutputTypeDef:
        """
        List all the scopes for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/list_scopes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#list_scopes)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Returns all the tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#list_tags_for_resource)
        """

    def start_query_monitor_top_contributors(
        self, **kwargs: Unpack[StartQueryMonitorTopContributorsInputRequestTypeDef]
    ) -> StartQueryMonitorTopContributorsOutputTypeDef:
        """
        Start a query to return the data with the Network Flow Monitor query interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/start_query_monitor_top_contributors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#start_query_monitor_top_contributors)
        """

    def start_query_workload_insights_top_contributors(
        self, **kwargs: Unpack[StartQueryWorkloadInsightsTopContributorsInputRequestTypeDef]
    ) -> StartQueryWorkloadInsightsTopContributorsOutputTypeDef:
        """
        Start a query to return the data with the Network Flow Monitor query interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/start_query_workload_insights_top_contributors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#start_query_workload_insights_top_contributors)
        """

    def start_query_workload_insights_top_contributors_data(
        self, **kwargs: Unpack[StartQueryWorkloadInsightsTopContributorsDataInputRequestTypeDef]
    ) -> StartQueryWorkloadInsightsTopContributorsDataOutputTypeDef:
        """
        Return the data for a query with the Network Flow Monitor query interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/start_query_workload_insights_top_contributors_data.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#start_query_workload_insights_top_contributors_data)
        """

    def stop_query_monitor_top_contributors(
        self, **kwargs: Unpack[StopQueryMonitorTopContributorsInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stop a query with the Network Flow Monitor query interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/stop_query_monitor_top_contributors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#stop_query_monitor_top_contributors)
        """

    def stop_query_workload_insights_top_contributors(
        self, **kwargs: Unpack[StopQueryWorkloadInsightsTopContributorsInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stop a query with the Network Flow Monitor query interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/stop_query_workload_insights_top_contributors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#stop_query_workload_insights_top_contributors)
        """

    def stop_query_workload_insights_top_contributors_data(
        self, **kwargs: Unpack[StopQueryWorkloadInsightsTopContributorsDataInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Return the data for a query with the Network Flow Monitor query interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/stop_query_workload_insights_top_contributors_data.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#stop_query_workload_insights_top_contributors_data)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds a tag to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#untag_resource)
        """

    def update_monitor(
        self, **kwargs: Unpack[UpdateMonitorInputRequestTypeDef]
    ) -> UpdateMonitorOutputTypeDef:
        """
        Update a monitor to add or remove local or remote resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/update_monitor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#update_monitor)
        """

    def update_scope(
        self, **kwargs: Unpack[UpdateScopeInputRequestTypeDef]
    ) -> UpdateScopeOutputTypeDef:
        """
        Update a scope to add or remove resources that you want to be available for
        Network Flow Monitor to generate metrics for, when you have active agents on
        those resources sending metrics reports to the Network Flow Monitor backend.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/update_scope.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#update_scope)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_query_results_monitor_top_contributors"]
    ) -> GetQueryResultsMonitorTopContributorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_query_results_workload_insights_top_contributors_data"]
    ) -> GetQueryResultsWorkloadInsightsTopContributorsDataPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_query_results_workload_insights_top_contributors"]
    ) -> GetQueryResultsWorkloadInsightsTopContributorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_monitors"]) -> ListMonitorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_scopes"]) -> ListScopesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/client/#get_paginator)
        """
