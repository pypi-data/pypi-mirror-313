"""
Type annotations for devops-guru service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_devops_guru.client import DevOpsGuruClient
    from mypy_boto3_devops_guru.paginator import (
        DescribeOrganizationResourceCollectionHealthPaginator,
        DescribeResourceCollectionHealthPaginator,
        GetCostEstimationPaginator,
        GetResourceCollectionPaginator,
        ListAnomaliesForInsightPaginator,
        ListAnomalousLogGroupsPaginator,
        ListEventsPaginator,
        ListInsightsPaginator,
        ListMonitoredResourcesPaginator,
        ListNotificationChannelsPaginator,
        ListOrganizationInsightsPaginator,
        ListRecommendationsPaginator,
        SearchInsightsPaginator,
        SearchOrganizationInsightsPaginator,
    )

    session = Session()
    client: DevOpsGuruClient = session.client("devops-guru")

    describe_organization_resource_collection_health_paginator: DescribeOrganizationResourceCollectionHealthPaginator = client.get_paginator("describe_organization_resource_collection_health")
    describe_resource_collection_health_paginator: DescribeResourceCollectionHealthPaginator = client.get_paginator("describe_resource_collection_health")
    get_cost_estimation_paginator: GetCostEstimationPaginator = client.get_paginator("get_cost_estimation")
    get_resource_collection_paginator: GetResourceCollectionPaginator = client.get_paginator("get_resource_collection")
    list_anomalies_for_insight_paginator: ListAnomaliesForInsightPaginator = client.get_paginator("list_anomalies_for_insight")
    list_anomalous_log_groups_paginator: ListAnomalousLogGroupsPaginator = client.get_paginator("list_anomalous_log_groups")
    list_events_paginator: ListEventsPaginator = client.get_paginator("list_events")
    list_insights_paginator: ListInsightsPaginator = client.get_paginator("list_insights")
    list_monitored_resources_paginator: ListMonitoredResourcesPaginator = client.get_paginator("list_monitored_resources")
    list_notification_channels_paginator: ListNotificationChannelsPaginator = client.get_paginator("list_notification_channels")
    list_organization_insights_paginator: ListOrganizationInsightsPaginator = client.get_paginator("list_organization_insights")
    list_recommendations_paginator: ListRecommendationsPaginator = client.get_paginator("list_recommendations")
    search_insights_paginator: SearchInsightsPaginator = client.get_paginator("search_insights")
    search_organization_insights_paginator: SearchOrganizationInsightsPaginator = client.get_paginator("search_organization_insights")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeOrganizationResourceCollectionHealthRequestDescribeOrganizationResourceCollectionHealthPaginateTypeDef,
    DescribeOrganizationResourceCollectionHealthResponseTypeDef,
    DescribeResourceCollectionHealthRequestDescribeResourceCollectionHealthPaginateTypeDef,
    DescribeResourceCollectionHealthResponseTypeDef,
    GetCostEstimationRequestGetCostEstimationPaginateTypeDef,
    GetCostEstimationResponseTypeDef,
    GetResourceCollectionRequestGetResourceCollectionPaginateTypeDef,
    GetResourceCollectionResponseTypeDef,
    ListAnomaliesForInsightRequestListAnomaliesForInsightPaginateTypeDef,
    ListAnomaliesForInsightResponseTypeDef,
    ListAnomalousLogGroupsRequestListAnomalousLogGroupsPaginateTypeDef,
    ListAnomalousLogGroupsResponseTypeDef,
    ListEventsRequestListEventsPaginateTypeDef,
    ListEventsResponseTypeDef,
    ListInsightsRequestListInsightsPaginateTypeDef,
    ListInsightsResponseTypeDef,
    ListMonitoredResourcesRequestListMonitoredResourcesPaginateTypeDef,
    ListMonitoredResourcesResponseTypeDef,
    ListNotificationChannelsRequestListNotificationChannelsPaginateTypeDef,
    ListNotificationChannelsResponseTypeDef,
    ListOrganizationInsightsRequestListOrganizationInsightsPaginateTypeDef,
    ListOrganizationInsightsResponseTypeDef,
    ListRecommendationsRequestListRecommendationsPaginateTypeDef,
    ListRecommendationsResponseTypeDef,
    SearchInsightsRequestSearchInsightsPaginateTypeDef,
    SearchInsightsResponseTypeDef,
    SearchOrganizationInsightsRequestSearchOrganizationInsightsPaginateTypeDef,
    SearchOrganizationInsightsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeOrganizationResourceCollectionHealthPaginator",
    "DescribeResourceCollectionHealthPaginator",
    "GetCostEstimationPaginator",
    "GetResourceCollectionPaginator",
    "ListAnomaliesForInsightPaginator",
    "ListAnomalousLogGroupsPaginator",
    "ListEventsPaginator",
    "ListInsightsPaginator",
    "ListMonitoredResourcesPaginator",
    "ListNotificationChannelsPaginator",
    "ListOrganizationInsightsPaginator",
    "ListRecommendationsPaginator",
    "SearchInsightsPaginator",
    "SearchOrganizationInsightsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeOrganizationResourceCollectionHealthPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/DescribeOrganizationResourceCollectionHealth.html#DevOpsGuru.Paginator.DescribeOrganizationResourceCollectionHealth)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#describeorganizationresourcecollectionhealthpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeOrganizationResourceCollectionHealthRequestDescribeOrganizationResourceCollectionHealthPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeOrganizationResourceCollectionHealthResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/DescribeOrganizationResourceCollectionHealth.html#DevOpsGuru.Paginator.DescribeOrganizationResourceCollectionHealth.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#describeorganizationresourcecollectionhealthpaginator)
        """


class DescribeResourceCollectionHealthPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/DescribeResourceCollectionHealth.html#DevOpsGuru.Paginator.DescribeResourceCollectionHealth)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#describeresourcecollectionhealthpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeResourceCollectionHealthRequestDescribeResourceCollectionHealthPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeResourceCollectionHealthResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/DescribeResourceCollectionHealth.html#DevOpsGuru.Paginator.DescribeResourceCollectionHealth.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#describeresourcecollectionhealthpaginator)
        """


class GetCostEstimationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/GetCostEstimation.html#DevOpsGuru.Paginator.GetCostEstimation)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#getcostestimationpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetCostEstimationRequestGetCostEstimationPaginateTypeDef]
    ) -> _PageIterator[GetCostEstimationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/GetCostEstimation.html#DevOpsGuru.Paginator.GetCostEstimation.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#getcostestimationpaginator)
        """


class GetResourceCollectionPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/GetResourceCollection.html#DevOpsGuru.Paginator.GetResourceCollection)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#getresourcecollectionpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetResourceCollectionRequestGetResourceCollectionPaginateTypeDef]
    ) -> _PageIterator[GetResourceCollectionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/GetResourceCollection.html#DevOpsGuru.Paginator.GetResourceCollection.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#getresourcecollectionpaginator)
        """


class ListAnomaliesForInsightPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListAnomaliesForInsight.html#DevOpsGuru.Paginator.ListAnomaliesForInsight)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#listanomaliesforinsightpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAnomaliesForInsightRequestListAnomaliesForInsightPaginateTypeDef]
    ) -> _PageIterator[ListAnomaliesForInsightResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListAnomaliesForInsight.html#DevOpsGuru.Paginator.ListAnomaliesForInsight.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#listanomaliesforinsightpaginator)
        """


class ListAnomalousLogGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListAnomalousLogGroups.html#DevOpsGuru.Paginator.ListAnomalousLogGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#listanomalousloggroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAnomalousLogGroupsRequestListAnomalousLogGroupsPaginateTypeDef]
    ) -> _PageIterator[ListAnomalousLogGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListAnomalousLogGroups.html#DevOpsGuru.Paginator.ListAnomalousLogGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#listanomalousloggroupspaginator)
        """


class ListEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListEvents.html#DevOpsGuru.Paginator.ListEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#listeventspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEventsRequestListEventsPaginateTypeDef]
    ) -> _PageIterator[ListEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListEvents.html#DevOpsGuru.Paginator.ListEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#listeventspaginator)
        """


class ListInsightsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListInsights.html#DevOpsGuru.Paginator.ListInsights)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#listinsightspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListInsightsRequestListInsightsPaginateTypeDef]
    ) -> _PageIterator[ListInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListInsights.html#DevOpsGuru.Paginator.ListInsights.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#listinsightspaginator)
        """


class ListMonitoredResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListMonitoredResources.html#DevOpsGuru.Paginator.ListMonitoredResources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#listmonitoredresourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMonitoredResourcesRequestListMonitoredResourcesPaginateTypeDef]
    ) -> _PageIterator[ListMonitoredResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListMonitoredResources.html#DevOpsGuru.Paginator.ListMonitoredResources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#listmonitoredresourcespaginator)
        """


class ListNotificationChannelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListNotificationChannels.html#DevOpsGuru.Paginator.ListNotificationChannels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#listnotificationchannelspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListNotificationChannelsRequestListNotificationChannelsPaginateTypeDef],
    ) -> _PageIterator[ListNotificationChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListNotificationChannels.html#DevOpsGuru.Paginator.ListNotificationChannels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#listnotificationchannelspaginator)
        """


class ListOrganizationInsightsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListOrganizationInsights.html#DevOpsGuru.Paginator.ListOrganizationInsights)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#listorganizationinsightspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListOrganizationInsightsRequestListOrganizationInsightsPaginateTypeDef],
    ) -> _PageIterator[ListOrganizationInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListOrganizationInsights.html#DevOpsGuru.Paginator.ListOrganizationInsights.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#listorganizationinsightspaginator)
        """


class ListRecommendationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListRecommendations.html#DevOpsGuru.Paginator.ListRecommendations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#listrecommendationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRecommendationsRequestListRecommendationsPaginateTypeDef]
    ) -> _PageIterator[ListRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListRecommendations.html#DevOpsGuru.Paginator.ListRecommendations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#listrecommendationspaginator)
        """


class SearchInsightsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/SearchInsights.html#DevOpsGuru.Paginator.SearchInsights)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#searchinsightspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchInsightsRequestSearchInsightsPaginateTypeDef]
    ) -> _PageIterator[SearchInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/SearchInsights.html#DevOpsGuru.Paginator.SearchInsights.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#searchinsightspaginator)
        """


class SearchOrganizationInsightsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/SearchOrganizationInsights.html#DevOpsGuru.Paginator.SearchOrganizationInsights)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#searchorganizationinsightspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            SearchOrganizationInsightsRequestSearchOrganizationInsightsPaginateTypeDef
        ],
    ) -> _PageIterator[SearchOrganizationInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/SearchOrganizationInsights.html#DevOpsGuru.Paginator.SearchOrganizationInsights.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/paginators/#searchorganizationinsightspaginator)
        """
