"""
Type annotations for xray service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_xray.client import XRayClient
    from mypy_boto3_xray.paginator import (
        BatchGetTracesPaginator,
        GetGroupsPaginator,
        GetSamplingRulesPaginator,
        GetSamplingStatisticSummariesPaginator,
        GetServiceGraphPaginator,
        GetTimeSeriesServiceStatisticsPaginator,
        GetTraceGraphPaginator,
        GetTraceSummariesPaginator,
        ListResourcePoliciesPaginator,
        ListTagsForResourcePaginator,
    )

    session = Session()
    client: XRayClient = session.client("xray")

    batch_get_traces_paginator: BatchGetTracesPaginator = client.get_paginator("batch_get_traces")
    get_groups_paginator: GetGroupsPaginator = client.get_paginator("get_groups")
    get_sampling_rules_paginator: GetSamplingRulesPaginator = client.get_paginator("get_sampling_rules")
    get_sampling_statistic_summaries_paginator: GetSamplingStatisticSummariesPaginator = client.get_paginator("get_sampling_statistic_summaries")
    get_service_graph_paginator: GetServiceGraphPaginator = client.get_paginator("get_service_graph")
    get_time_series_service_statistics_paginator: GetTimeSeriesServiceStatisticsPaginator = client.get_paginator("get_time_series_service_statistics")
    get_trace_graph_paginator: GetTraceGraphPaginator = client.get_paginator("get_trace_graph")
    get_trace_summaries_paginator: GetTraceSummariesPaginator = client.get_paginator("get_trace_summaries")
    list_resource_policies_paginator: ListResourcePoliciesPaginator = client.get_paginator("list_resource_policies")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    BatchGetTracesRequestBatchGetTracesPaginateTypeDef,
    BatchGetTracesResultTypeDef,
    GetGroupsRequestGetGroupsPaginateTypeDef,
    GetGroupsResultTypeDef,
    GetSamplingRulesRequestGetSamplingRulesPaginateTypeDef,
    GetSamplingRulesResultTypeDef,
    GetSamplingStatisticSummariesRequestGetSamplingStatisticSummariesPaginateTypeDef,
    GetSamplingStatisticSummariesResultTypeDef,
    GetServiceGraphRequestGetServiceGraphPaginateTypeDef,
    GetServiceGraphResultTypeDef,
    GetTimeSeriesServiceStatisticsRequestGetTimeSeriesServiceStatisticsPaginateTypeDef,
    GetTimeSeriesServiceStatisticsResultTypeDef,
    GetTraceGraphRequestGetTraceGraphPaginateTypeDef,
    GetTraceGraphResultTypeDef,
    GetTraceSummariesRequestGetTraceSummariesPaginateTypeDef,
    GetTraceSummariesResultTypeDef,
    ListResourcePoliciesRequestListResourcePoliciesPaginateTypeDef,
    ListResourcePoliciesResultTypeDef,
    ListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "BatchGetTracesPaginator",
    "GetGroupsPaginator",
    "GetSamplingRulesPaginator",
    "GetSamplingStatisticSummariesPaginator",
    "GetServiceGraphPaginator",
    "GetTimeSeriesServiceStatisticsPaginator",
    "GetTraceGraphPaginator",
    "GetTraceSummariesPaginator",
    "ListResourcePoliciesPaginator",
    "ListTagsForResourcePaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class BatchGetTracesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/BatchGetTraces.html#XRay.Paginator.BatchGetTraces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#batchgettracespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[BatchGetTracesRequestBatchGetTracesPaginateTypeDef]
    ) -> _PageIterator[BatchGetTracesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/BatchGetTraces.html#XRay.Paginator.BatchGetTraces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#batchgettracespaginator)
        """

class GetGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetGroups.html#XRay.Paginator.GetGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#getgroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetGroupsRequestGetGroupsPaginateTypeDef]
    ) -> _PageIterator[GetGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetGroups.html#XRay.Paginator.GetGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#getgroupspaginator)
        """

class GetSamplingRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetSamplingRules.html#XRay.Paginator.GetSamplingRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#getsamplingrulespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetSamplingRulesRequestGetSamplingRulesPaginateTypeDef]
    ) -> _PageIterator[GetSamplingRulesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetSamplingRules.html#XRay.Paginator.GetSamplingRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#getsamplingrulespaginator)
        """

class GetSamplingStatisticSummariesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetSamplingStatisticSummaries.html#XRay.Paginator.GetSamplingStatisticSummaries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#getsamplingstatisticsummariespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetSamplingStatisticSummariesRequestGetSamplingStatisticSummariesPaginateTypeDef
        ],
    ) -> _PageIterator[GetSamplingStatisticSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetSamplingStatisticSummaries.html#XRay.Paginator.GetSamplingStatisticSummaries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#getsamplingstatisticsummariespaginator)
        """

class GetServiceGraphPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetServiceGraph.html#XRay.Paginator.GetServiceGraph)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#getservicegraphpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetServiceGraphRequestGetServiceGraphPaginateTypeDef]
    ) -> _PageIterator[GetServiceGraphResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetServiceGraph.html#XRay.Paginator.GetServiceGraph.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#getservicegraphpaginator)
        """

class GetTimeSeriesServiceStatisticsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetTimeSeriesServiceStatistics.html#XRay.Paginator.GetTimeSeriesServiceStatistics)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#gettimeseriesservicestatisticspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetTimeSeriesServiceStatisticsRequestGetTimeSeriesServiceStatisticsPaginateTypeDef
        ],
    ) -> _PageIterator[GetTimeSeriesServiceStatisticsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetTimeSeriesServiceStatistics.html#XRay.Paginator.GetTimeSeriesServiceStatistics.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#gettimeseriesservicestatisticspaginator)
        """

class GetTraceGraphPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetTraceGraph.html#XRay.Paginator.GetTraceGraph)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#gettracegraphpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetTraceGraphRequestGetTraceGraphPaginateTypeDef]
    ) -> _PageIterator[GetTraceGraphResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetTraceGraph.html#XRay.Paginator.GetTraceGraph.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#gettracegraphpaginator)
        """

class GetTraceSummariesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetTraceSummaries.html#XRay.Paginator.GetTraceSummaries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#gettracesummariespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetTraceSummariesRequestGetTraceSummariesPaginateTypeDef]
    ) -> _PageIterator[GetTraceSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetTraceSummaries.html#XRay.Paginator.GetTraceSummaries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#gettracesummariespaginator)
        """

class ListResourcePoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/ListResourcePolicies.html#XRay.Paginator.ListResourcePolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#listresourcepoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListResourcePoliciesRequestListResourcePoliciesPaginateTypeDef]
    ) -> _PageIterator[ListResourcePoliciesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/ListResourcePolicies.html#XRay.Paginator.ListResourcePolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#listresourcepoliciespaginator)
        """

class ListTagsForResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/ListTagsForResource.html#XRay.Paginator.ListTagsForResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#listtagsforresourcepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceRequestListTagsForResourcePaginateTypeDef]
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/ListTagsForResource.html#XRay.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#listtagsforresourcepaginator)
        """
