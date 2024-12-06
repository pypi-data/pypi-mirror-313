"""
Type annotations for logs service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_logs.client import CloudWatchLogsClient
    from mypy_boto3_logs.paginator import (
        DescribeConfigurationTemplatesPaginator,
        DescribeDeliveriesPaginator,
        DescribeDeliveryDestinationsPaginator,
        DescribeDeliverySourcesPaginator,
        DescribeDestinationsPaginator,
        DescribeExportTasksPaginator,
        DescribeLogGroupsPaginator,
        DescribeLogStreamsPaginator,
        DescribeMetricFiltersPaginator,
        DescribeQueriesPaginator,
        DescribeResourcePoliciesPaginator,
        DescribeSubscriptionFiltersPaginator,
        FilterLogEventsPaginator,
        ListAnomaliesPaginator,
        ListLogAnomalyDetectorsPaginator,
        ListLogGroupsForQueryPaginator,
    )

    session = Session()
    client: CloudWatchLogsClient = session.client("logs")

    describe_configuration_templates_paginator: DescribeConfigurationTemplatesPaginator = client.get_paginator("describe_configuration_templates")
    describe_deliveries_paginator: DescribeDeliveriesPaginator = client.get_paginator("describe_deliveries")
    describe_delivery_destinations_paginator: DescribeDeliveryDestinationsPaginator = client.get_paginator("describe_delivery_destinations")
    describe_delivery_sources_paginator: DescribeDeliverySourcesPaginator = client.get_paginator("describe_delivery_sources")
    describe_destinations_paginator: DescribeDestinationsPaginator = client.get_paginator("describe_destinations")
    describe_export_tasks_paginator: DescribeExportTasksPaginator = client.get_paginator("describe_export_tasks")
    describe_log_groups_paginator: DescribeLogGroupsPaginator = client.get_paginator("describe_log_groups")
    describe_log_streams_paginator: DescribeLogStreamsPaginator = client.get_paginator("describe_log_streams")
    describe_metric_filters_paginator: DescribeMetricFiltersPaginator = client.get_paginator("describe_metric_filters")
    describe_queries_paginator: DescribeQueriesPaginator = client.get_paginator("describe_queries")
    describe_resource_policies_paginator: DescribeResourcePoliciesPaginator = client.get_paginator("describe_resource_policies")
    describe_subscription_filters_paginator: DescribeSubscriptionFiltersPaginator = client.get_paginator("describe_subscription_filters")
    filter_log_events_paginator: FilterLogEventsPaginator = client.get_paginator("filter_log_events")
    list_anomalies_paginator: ListAnomaliesPaginator = client.get_paginator("list_anomalies")
    list_log_anomaly_detectors_paginator: ListLogAnomalyDetectorsPaginator = client.get_paginator("list_log_anomaly_detectors")
    list_log_groups_for_query_paginator: ListLogGroupsForQueryPaginator = client.get_paginator("list_log_groups_for_query")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeConfigurationTemplatesRequestDescribeConfigurationTemplatesPaginateTypeDef,
    DescribeConfigurationTemplatesResponseTypeDef,
    DescribeDeliveriesRequestDescribeDeliveriesPaginateTypeDef,
    DescribeDeliveriesResponseTypeDef,
    DescribeDeliveryDestinationsRequestDescribeDeliveryDestinationsPaginateTypeDef,
    DescribeDeliveryDestinationsResponseTypeDef,
    DescribeDeliverySourcesRequestDescribeDeliverySourcesPaginateTypeDef,
    DescribeDeliverySourcesResponseTypeDef,
    DescribeDestinationsRequestDescribeDestinationsPaginateTypeDef,
    DescribeDestinationsResponseTypeDef,
    DescribeExportTasksRequestDescribeExportTasksPaginateTypeDef,
    DescribeExportTasksResponseTypeDef,
    DescribeLogGroupsRequestDescribeLogGroupsPaginateTypeDef,
    DescribeLogGroupsResponseTypeDef,
    DescribeLogStreamsRequestDescribeLogStreamsPaginateTypeDef,
    DescribeLogStreamsResponseTypeDef,
    DescribeMetricFiltersRequestDescribeMetricFiltersPaginateTypeDef,
    DescribeMetricFiltersResponseTypeDef,
    DescribeQueriesRequestDescribeQueriesPaginateTypeDef,
    DescribeQueriesResponseTypeDef,
    DescribeResourcePoliciesRequestDescribeResourcePoliciesPaginateTypeDef,
    DescribeResourcePoliciesResponseTypeDef,
    DescribeSubscriptionFiltersRequestDescribeSubscriptionFiltersPaginateTypeDef,
    DescribeSubscriptionFiltersResponseTypeDef,
    FilterLogEventsRequestFilterLogEventsPaginateTypeDef,
    FilterLogEventsResponseTypeDef,
    ListAnomaliesRequestListAnomaliesPaginateTypeDef,
    ListAnomaliesResponseTypeDef,
    ListLogAnomalyDetectorsRequestListLogAnomalyDetectorsPaginateTypeDef,
    ListLogAnomalyDetectorsResponseTypeDef,
    ListLogGroupsForQueryRequestListLogGroupsForQueryPaginateTypeDef,
    ListLogGroupsForQueryResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeConfigurationTemplatesPaginator",
    "DescribeDeliveriesPaginator",
    "DescribeDeliveryDestinationsPaginator",
    "DescribeDeliverySourcesPaginator",
    "DescribeDestinationsPaginator",
    "DescribeExportTasksPaginator",
    "DescribeLogGroupsPaginator",
    "DescribeLogStreamsPaginator",
    "DescribeMetricFiltersPaginator",
    "DescribeQueriesPaginator",
    "DescribeResourcePoliciesPaginator",
    "DescribeSubscriptionFiltersPaginator",
    "FilterLogEventsPaginator",
    "ListAnomaliesPaginator",
    "ListLogAnomalyDetectorsPaginator",
    "ListLogGroupsForQueryPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeConfigurationTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeConfigurationTemplates.html#CloudWatchLogs.Paginator.DescribeConfigurationTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describeconfigurationtemplatespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeConfigurationTemplatesRequestDescribeConfigurationTemplatesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeConfigurationTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeConfigurationTemplates.html#CloudWatchLogs.Paginator.DescribeConfigurationTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describeconfigurationtemplatespaginator)
        """

class DescribeDeliveriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliveries.html#CloudWatchLogs.Paginator.DescribeDeliveries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describedeliveriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeDeliveriesRequestDescribeDeliveriesPaginateTypeDef]
    ) -> _PageIterator[DescribeDeliveriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliveries.html#CloudWatchLogs.Paginator.DescribeDeliveries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describedeliveriespaginator)
        """

class DescribeDeliveryDestinationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliveryDestinations.html#CloudWatchLogs.Paginator.DescribeDeliveryDestinations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describedeliverydestinationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeDeliveryDestinationsRequestDescribeDeliveryDestinationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeDeliveryDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliveryDestinations.html#CloudWatchLogs.Paginator.DescribeDeliveryDestinations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describedeliverydestinationspaginator)
        """

class DescribeDeliverySourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliverySources.html#CloudWatchLogs.Paginator.DescribeDeliverySources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describedeliverysourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeDeliverySourcesRequestDescribeDeliverySourcesPaginateTypeDef]
    ) -> _PageIterator[DescribeDeliverySourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliverySources.html#CloudWatchLogs.Paginator.DescribeDeliverySources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describedeliverysourcespaginator)
        """

class DescribeDestinationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDestinations.html#CloudWatchLogs.Paginator.DescribeDestinations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describedestinationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeDestinationsRequestDescribeDestinationsPaginateTypeDef]
    ) -> _PageIterator[DescribeDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDestinations.html#CloudWatchLogs.Paginator.DescribeDestinations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describedestinationspaginator)
        """

class DescribeExportTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeExportTasks.html#CloudWatchLogs.Paginator.DescribeExportTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describeexporttaskspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeExportTasksRequestDescribeExportTasksPaginateTypeDef]
    ) -> _PageIterator[DescribeExportTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeExportTasks.html#CloudWatchLogs.Paginator.DescribeExportTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describeexporttaskspaginator)
        """

class DescribeLogGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeLogGroups.html#CloudWatchLogs.Paginator.DescribeLogGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describeloggroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeLogGroupsRequestDescribeLogGroupsPaginateTypeDef]
    ) -> _PageIterator[DescribeLogGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeLogGroups.html#CloudWatchLogs.Paginator.DescribeLogGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describeloggroupspaginator)
        """

class DescribeLogStreamsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeLogStreams.html#CloudWatchLogs.Paginator.DescribeLogStreams)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describelogstreamspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeLogStreamsRequestDescribeLogStreamsPaginateTypeDef]
    ) -> _PageIterator[DescribeLogStreamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeLogStreams.html#CloudWatchLogs.Paginator.DescribeLogStreams.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describelogstreamspaginator)
        """

class DescribeMetricFiltersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeMetricFilters.html#CloudWatchLogs.Paginator.DescribeMetricFilters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describemetricfilterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeMetricFiltersRequestDescribeMetricFiltersPaginateTypeDef]
    ) -> _PageIterator[DescribeMetricFiltersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeMetricFilters.html#CloudWatchLogs.Paginator.DescribeMetricFilters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describemetricfilterspaginator)
        """

class DescribeQueriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeQueries.html#CloudWatchLogs.Paginator.DescribeQueries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describequeriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeQueriesRequestDescribeQueriesPaginateTypeDef]
    ) -> _PageIterator[DescribeQueriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeQueries.html#CloudWatchLogs.Paginator.DescribeQueries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describequeriespaginator)
        """

class DescribeResourcePoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeResourcePolicies.html#CloudWatchLogs.Paginator.DescribeResourcePolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describeresourcepoliciespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeResourcePoliciesRequestDescribeResourcePoliciesPaginateTypeDef],
    ) -> _PageIterator[DescribeResourcePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeResourcePolicies.html#CloudWatchLogs.Paginator.DescribeResourcePolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describeresourcepoliciespaginator)
        """

class DescribeSubscriptionFiltersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeSubscriptionFilters.html#CloudWatchLogs.Paginator.DescribeSubscriptionFilters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describesubscriptionfilterspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeSubscriptionFiltersRequestDescribeSubscriptionFiltersPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeSubscriptionFiltersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeSubscriptionFilters.html#CloudWatchLogs.Paginator.DescribeSubscriptionFilters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#describesubscriptionfilterspaginator)
        """

class FilterLogEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/FilterLogEvents.html#CloudWatchLogs.Paginator.FilterLogEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#filterlogeventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[FilterLogEventsRequestFilterLogEventsPaginateTypeDef]
    ) -> _PageIterator[FilterLogEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/FilterLogEvents.html#CloudWatchLogs.Paginator.FilterLogEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#filterlogeventspaginator)
        """

class ListAnomaliesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/ListAnomalies.html#CloudWatchLogs.Paginator.ListAnomalies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#listanomaliespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAnomaliesRequestListAnomaliesPaginateTypeDef]
    ) -> _PageIterator[ListAnomaliesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/ListAnomalies.html#CloudWatchLogs.Paginator.ListAnomalies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#listanomaliespaginator)
        """

class ListLogAnomalyDetectorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/ListLogAnomalyDetectors.html#CloudWatchLogs.Paginator.ListLogAnomalyDetectors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#listloganomalydetectorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLogAnomalyDetectorsRequestListLogAnomalyDetectorsPaginateTypeDef]
    ) -> _PageIterator[ListLogAnomalyDetectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/ListLogAnomalyDetectors.html#CloudWatchLogs.Paginator.ListLogAnomalyDetectors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#listloganomalydetectorspaginator)
        """

class ListLogGroupsForQueryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/ListLogGroupsForQuery.html#CloudWatchLogs.Paginator.ListLogGroupsForQuery)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#listloggroupsforquerypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLogGroupsForQueryRequestListLogGroupsForQueryPaginateTypeDef]
    ) -> _PageIterator[ListLogGroupsForQueryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/ListLogGroupsForQuery.html#CloudWatchLogs.Paginator.ListLogGroupsForQuery.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_logs/paginators/#listloggroupsforquerypaginator)
        """
