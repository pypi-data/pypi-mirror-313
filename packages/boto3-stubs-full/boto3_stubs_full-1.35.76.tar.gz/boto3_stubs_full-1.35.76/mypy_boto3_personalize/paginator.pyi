"""
Type annotations for personalize service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_personalize.client import PersonalizeClient
    from mypy_boto3_personalize.paginator import (
        ListBatchInferenceJobsPaginator,
        ListBatchSegmentJobsPaginator,
        ListCampaignsPaginator,
        ListDatasetExportJobsPaginator,
        ListDatasetGroupsPaginator,
        ListDatasetImportJobsPaginator,
        ListDatasetsPaginator,
        ListEventTrackersPaginator,
        ListFiltersPaginator,
        ListMetricAttributionMetricsPaginator,
        ListMetricAttributionsPaginator,
        ListRecipesPaginator,
        ListRecommendersPaginator,
        ListSchemasPaginator,
        ListSolutionVersionsPaginator,
        ListSolutionsPaginator,
    )

    session = Session()
    client: PersonalizeClient = session.client("personalize")

    list_batch_inference_jobs_paginator: ListBatchInferenceJobsPaginator = client.get_paginator("list_batch_inference_jobs")
    list_batch_segment_jobs_paginator: ListBatchSegmentJobsPaginator = client.get_paginator("list_batch_segment_jobs")
    list_campaigns_paginator: ListCampaignsPaginator = client.get_paginator("list_campaigns")
    list_dataset_export_jobs_paginator: ListDatasetExportJobsPaginator = client.get_paginator("list_dataset_export_jobs")
    list_dataset_groups_paginator: ListDatasetGroupsPaginator = client.get_paginator("list_dataset_groups")
    list_dataset_import_jobs_paginator: ListDatasetImportJobsPaginator = client.get_paginator("list_dataset_import_jobs")
    list_datasets_paginator: ListDatasetsPaginator = client.get_paginator("list_datasets")
    list_event_trackers_paginator: ListEventTrackersPaginator = client.get_paginator("list_event_trackers")
    list_filters_paginator: ListFiltersPaginator = client.get_paginator("list_filters")
    list_metric_attribution_metrics_paginator: ListMetricAttributionMetricsPaginator = client.get_paginator("list_metric_attribution_metrics")
    list_metric_attributions_paginator: ListMetricAttributionsPaginator = client.get_paginator("list_metric_attributions")
    list_recipes_paginator: ListRecipesPaginator = client.get_paginator("list_recipes")
    list_recommenders_paginator: ListRecommendersPaginator = client.get_paginator("list_recommenders")
    list_schemas_paginator: ListSchemasPaginator = client.get_paginator("list_schemas")
    list_solution_versions_paginator: ListSolutionVersionsPaginator = client.get_paginator("list_solution_versions")
    list_solutions_paginator: ListSolutionsPaginator = client.get_paginator("list_solutions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListBatchInferenceJobsRequestListBatchInferenceJobsPaginateTypeDef,
    ListBatchInferenceJobsResponseTypeDef,
    ListBatchSegmentJobsRequestListBatchSegmentJobsPaginateTypeDef,
    ListBatchSegmentJobsResponseTypeDef,
    ListCampaignsRequestListCampaignsPaginateTypeDef,
    ListCampaignsResponseTypeDef,
    ListDatasetExportJobsRequestListDatasetExportJobsPaginateTypeDef,
    ListDatasetExportJobsResponseTypeDef,
    ListDatasetGroupsRequestListDatasetGroupsPaginateTypeDef,
    ListDatasetGroupsResponseTypeDef,
    ListDatasetImportJobsRequestListDatasetImportJobsPaginateTypeDef,
    ListDatasetImportJobsResponseTypeDef,
    ListDatasetsRequestListDatasetsPaginateTypeDef,
    ListDatasetsResponseTypeDef,
    ListEventTrackersRequestListEventTrackersPaginateTypeDef,
    ListEventTrackersResponseTypeDef,
    ListFiltersRequestListFiltersPaginateTypeDef,
    ListFiltersResponseTypeDef,
    ListMetricAttributionMetricsRequestListMetricAttributionMetricsPaginateTypeDef,
    ListMetricAttributionMetricsResponseTypeDef,
    ListMetricAttributionsRequestListMetricAttributionsPaginateTypeDef,
    ListMetricAttributionsResponseTypeDef,
    ListRecipesRequestListRecipesPaginateTypeDef,
    ListRecipesResponseTypeDef,
    ListRecommendersRequestListRecommendersPaginateTypeDef,
    ListRecommendersResponseTypeDef,
    ListSchemasRequestListSchemasPaginateTypeDef,
    ListSchemasResponseTypeDef,
    ListSolutionsRequestListSolutionsPaginateTypeDef,
    ListSolutionsResponseTypeDef,
    ListSolutionVersionsRequestListSolutionVersionsPaginateTypeDef,
    ListSolutionVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListBatchInferenceJobsPaginator",
    "ListBatchSegmentJobsPaginator",
    "ListCampaignsPaginator",
    "ListDatasetExportJobsPaginator",
    "ListDatasetGroupsPaginator",
    "ListDatasetImportJobsPaginator",
    "ListDatasetsPaginator",
    "ListEventTrackersPaginator",
    "ListFiltersPaginator",
    "ListMetricAttributionMetricsPaginator",
    "ListMetricAttributionsPaginator",
    "ListRecipesPaginator",
    "ListRecommendersPaginator",
    "ListSchemasPaginator",
    "ListSolutionVersionsPaginator",
    "ListSolutionsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListBatchInferenceJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListBatchInferenceJobs.html#Personalize.Paginator.ListBatchInferenceJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listbatchinferencejobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBatchInferenceJobsRequestListBatchInferenceJobsPaginateTypeDef]
    ) -> _PageIterator[ListBatchInferenceJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListBatchInferenceJobs.html#Personalize.Paginator.ListBatchInferenceJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listbatchinferencejobspaginator)
        """

class ListBatchSegmentJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListBatchSegmentJobs.html#Personalize.Paginator.ListBatchSegmentJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listbatchsegmentjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBatchSegmentJobsRequestListBatchSegmentJobsPaginateTypeDef]
    ) -> _PageIterator[ListBatchSegmentJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListBatchSegmentJobs.html#Personalize.Paginator.ListBatchSegmentJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listbatchsegmentjobspaginator)
        """

class ListCampaignsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListCampaigns.html#Personalize.Paginator.ListCampaigns)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listcampaignspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCampaignsRequestListCampaignsPaginateTypeDef]
    ) -> _PageIterator[ListCampaignsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListCampaigns.html#Personalize.Paginator.ListCampaigns.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listcampaignspaginator)
        """

class ListDatasetExportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListDatasetExportJobs.html#Personalize.Paginator.ListDatasetExportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listdatasetexportjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDatasetExportJobsRequestListDatasetExportJobsPaginateTypeDef]
    ) -> _PageIterator[ListDatasetExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListDatasetExportJobs.html#Personalize.Paginator.ListDatasetExportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listdatasetexportjobspaginator)
        """

class ListDatasetGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListDatasetGroups.html#Personalize.Paginator.ListDatasetGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listdatasetgroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDatasetGroupsRequestListDatasetGroupsPaginateTypeDef]
    ) -> _PageIterator[ListDatasetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListDatasetGroups.html#Personalize.Paginator.ListDatasetGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listdatasetgroupspaginator)
        """

class ListDatasetImportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListDatasetImportJobs.html#Personalize.Paginator.ListDatasetImportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listdatasetimportjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDatasetImportJobsRequestListDatasetImportJobsPaginateTypeDef]
    ) -> _PageIterator[ListDatasetImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListDatasetImportJobs.html#Personalize.Paginator.ListDatasetImportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listdatasetimportjobspaginator)
        """

class ListDatasetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListDatasets.html#Personalize.Paginator.ListDatasets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listdatasetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDatasetsRequestListDatasetsPaginateTypeDef]
    ) -> _PageIterator[ListDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListDatasets.html#Personalize.Paginator.ListDatasets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listdatasetspaginator)
        """

class ListEventTrackersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListEventTrackers.html#Personalize.Paginator.ListEventTrackers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listeventtrackerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEventTrackersRequestListEventTrackersPaginateTypeDef]
    ) -> _PageIterator[ListEventTrackersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListEventTrackers.html#Personalize.Paginator.ListEventTrackers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listeventtrackerspaginator)
        """

class ListFiltersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListFilters.html#Personalize.Paginator.ListFilters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listfilterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFiltersRequestListFiltersPaginateTypeDef]
    ) -> _PageIterator[ListFiltersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListFilters.html#Personalize.Paginator.ListFilters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listfilterspaginator)
        """

class ListMetricAttributionMetricsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListMetricAttributionMetrics.html#Personalize.Paginator.ListMetricAttributionMetrics)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listmetricattributionmetricspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListMetricAttributionMetricsRequestListMetricAttributionMetricsPaginateTypeDef
        ],
    ) -> _PageIterator[ListMetricAttributionMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListMetricAttributionMetrics.html#Personalize.Paginator.ListMetricAttributionMetrics.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listmetricattributionmetricspaginator)
        """

class ListMetricAttributionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListMetricAttributions.html#Personalize.Paginator.ListMetricAttributions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listmetricattributionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMetricAttributionsRequestListMetricAttributionsPaginateTypeDef]
    ) -> _PageIterator[ListMetricAttributionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListMetricAttributions.html#Personalize.Paginator.ListMetricAttributions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listmetricattributionspaginator)
        """

class ListRecipesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListRecipes.html#Personalize.Paginator.ListRecipes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listrecipespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRecipesRequestListRecipesPaginateTypeDef]
    ) -> _PageIterator[ListRecipesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListRecipes.html#Personalize.Paginator.ListRecipes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listrecipespaginator)
        """

class ListRecommendersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListRecommenders.html#Personalize.Paginator.ListRecommenders)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listrecommenderspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRecommendersRequestListRecommendersPaginateTypeDef]
    ) -> _PageIterator[ListRecommendersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListRecommenders.html#Personalize.Paginator.ListRecommenders.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listrecommenderspaginator)
        """

class ListSchemasPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListSchemas.html#Personalize.Paginator.ListSchemas)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listschemaspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSchemasRequestListSchemasPaginateTypeDef]
    ) -> _PageIterator[ListSchemasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListSchemas.html#Personalize.Paginator.ListSchemas.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listschemaspaginator)
        """

class ListSolutionVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListSolutionVersions.html#Personalize.Paginator.ListSolutionVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listsolutionversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSolutionVersionsRequestListSolutionVersionsPaginateTypeDef]
    ) -> _PageIterator[ListSolutionVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListSolutionVersions.html#Personalize.Paginator.ListSolutionVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listsolutionversionspaginator)
        """

class ListSolutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListSolutions.html#Personalize.Paginator.ListSolutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listsolutionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSolutionsRequestListSolutionsPaginateTypeDef]
    ) -> _PageIterator[ListSolutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListSolutions.html#Personalize.Paginator.ListSolutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/paginators/#listsolutionspaginator)
        """
