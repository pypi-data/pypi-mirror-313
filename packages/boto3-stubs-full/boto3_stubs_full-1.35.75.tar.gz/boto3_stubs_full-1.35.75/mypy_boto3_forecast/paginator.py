"""
Type annotations for forecast service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_forecast.client import ForecastServiceClient
    from mypy_boto3_forecast.paginator import (
        ListDatasetGroupsPaginator,
        ListDatasetImportJobsPaginator,
        ListDatasetsPaginator,
        ListExplainabilitiesPaginator,
        ListExplainabilityExportsPaginator,
        ListForecastExportJobsPaginator,
        ListForecastsPaginator,
        ListMonitorEvaluationsPaginator,
        ListMonitorsPaginator,
        ListPredictorBacktestExportJobsPaginator,
        ListPredictorsPaginator,
        ListWhatIfAnalysesPaginator,
        ListWhatIfForecastExportsPaginator,
        ListWhatIfForecastsPaginator,
    )

    session = Session()
    client: ForecastServiceClient = session.client("forecast")

    list_dataset_groups_paginator: ListDatasetGroupsPaginator = client.get_paginator("list_dataset_groups")
    list_dataset_import_jobs_paginator: ListDatasetImportJobsPaginator = client.get_paginator("list_dataset_import_jobs")
    list_datasets_paginator: ListDatasetsPaginator = client.get_paginator("list_datasets")
    list_explainabilities_paginator: ListExplainabilitiesPaginator = client.get_paginator("list_explainabilities")
    list_explainability_exports_paginator: ListExplainabilityExportsPaginator = client.get_paginator("list_explainability_exports")
    list_forecast_export_jobs_paginator: ListForecastExportJobsPaginator = client.get_paginator("list_forecast_export_jobs")
    list_forecasts_paginator: ListForecastsPaginator = client.get_paginator("list_forecasts")
    list_monitor_evaluations_paginator: ListMonitorEvaluationsPaginator = client.get_paginator("list_monitor_evaluations")
    list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
    list_predictor_backtest_export_jobs_paginator: ListPredictorBacktestExportJobsPaginator = client.get_paginator("list_predictor_backtest_export_jobs")
    list_predictors_paginator: ListPredictorsPaginator = client.get_paginator("list_predictors")
    list_what_if_analyses_paginator: ListWhatIfAnalysesPaginator = client.get_paginator("list_what_if_analyses")
    list_what_if_forecast_exports_paginator: ListWhatIfForecastExportsPaginator = client.get_paginator("list_what_if_forecast_exports")
    list_what_if_forecasts_paginator: ListWhatIfForecastsPaginator = client.get_paginator("list_what_if_forecasts")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDatasetGroupsRequestListDatasetGroupsPaginateTypeDef,
    ListDatasetGroupsResponseTypeDef,
    ListDatasetImportJobsRequestListDatasetImportJobsPaginateTypeDef,
    ListDatasetImportJobsResponseTypeDef,
    ListDatasetsRequestListDatasetsPaginateTypeDef,
    ListDatasetsResponseTypeDef,
    ListExplainabilitiesRequestListExplainabilitiesPaginateTypeDef,
    ListExplainabilitiesResponseTypeDef,
    ListExplainabilityExportsRequestListExplainabilityExportsPaginateTypeDef,
    ListExplainabilityExportsResponseTypeDef,
    ListForecastExportJobsRequestListForecastExportJobsPaginateTypeDef,
    ListForecastExportJobsResponseTypeDef,
    ListForecastsRequestListForecastsPaginateTypeDef,
    ListForecastsResponseTypeDef,
    ListMonitorEvaluationsRequestListMonitorEvaluationsPaginateTypeDef,
    ListMonitorEvaluationsResponseTypeDef,
    ListMonitorsRequestListMonitorsPaginateTypeDef,
    ListMonitorsResponseTypeDef,
    ListPredictorBacktestExportJobsRequestListPredictorBacktestExportJobsPaginateTypeDef,
    ListPredictorBacktestExportJobsResponseTypeDef,
    ListPredictorsRequestListPredictorsPaginateTypeDef,
    ListPredictorsResponseTypeDef,
    ListWhatIfAnalysesRequestListWhatIfAnalysesPaginateTypeDef,
    ListWhatIfAnalysesResponseTypeDef,
    ListWhatIfForecastExportsRequestListWhatIfForecastExportsPaginateTypeDef,
    ListWhatIfForecastExportsResponseTypeDef,
    ListWhatIfForecastsRequestListWhatIfForecastsPaginateTypeDef,
    ListWhatIfForecastsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListDatasetGroupsPaginator",
    "ListDatasetImportJobsPaginator",
    "ListDatasetsPaginator",
    "ListExplainabilitiesPaginator",
    "ListExplainabilityExportsPaginator",
    "ListForecastExportJobsPaginator",
    "ListForecastsPaginator",
    "ListMonitorEvaluationsPaginator",
    "ListMonitorsPaginator",
    "ListPredictorBacktestExportJobsPaginator",
    "ListPredictorsPaginator",
    "ListWhatIfAnalysesPaginator",
    "ListWhatIfForecastExportsPaginator",
    "ListWhatIfForecastsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDatasetGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListDatasetGroups.html#ForecastService.Paginator.ListDatasetGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listdatasetgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDatasetGroupsRequestListDatasetGroupsPaginateTypeDef]
    ) -> _PageIterator[ListDatasetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListDatasetGroups.html#ForecastService.Paginator.ListDatasetGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listdatasetgroupspaginator)
        """


class ListDatasetImportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListDatasetImportJobs.html#ForecastService.Paginator.ListDatasetImportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listdatasetimportjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDatasetImportJobsRequestListDatasetImportJobsPaginateTypeDef]
    ) -> _PageIterator[ListDatasetImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListDatasetImportJobs.html#ForecastService.Paginator.ListDatasetImportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listdatasetimportjobspaginator)
        """


class ListDatasetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListDatasets.html#ForecastService.Paginator.ListDatasets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listdatasetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDatasetsRequestListDatasetsPaginateTypeDef]
    ) -> _PageIterator[ListDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListDatasets.html#ForecastService.Paginator.ListDatasets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listdatasetspaginator)
        """


class ListExplainabilitiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListExplainabilities.html#ForecastService.Paginator.ListExplainabilities)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listexplainabilitiespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListExplainabilitiesRequestListExplainabilitiesPaginateTypeDef]
    ) -> _PageIterator[ListExplainabilitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListExplainabilities.html#ForecastService.Paginator.ListExplainabilities.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listexplainabilitiespaginator)
        """


class ListExplainabilityExportsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListExplainabilityExports.html#ForecastService.Paginator.ListExplainabilityExports)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listexplainabilityexportspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListExplainabilityExportsRequestListExplainabilityExportsPaginateTypeDef],
    ) -> _PageIterator[ListExplainabilityExportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListExplainabilityExports.html#ForecastService.Paginator.ListExplainabilityExports.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listexplainabilityexportspaginator)
        """


class ListForecastExportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListForecastExportJobs.html#ForecastService.Paginator.ListForecastExportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listforecastexportjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListForecastExportJobsRequestListForecastExportJobsPaginateTypeDef]
    ) -> _PageIterator[ListForecastExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListForecastExportJobs.html#ForecastService.Paginator.ListForecastExportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listforecastexportjobspaginator)
        """


class ListForecastsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListForecasts.html#ForecastService.Paginator.ListForecasts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listforecastspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListForecastsRequestListForecastsPaginateTypeDef]
    ) -> _PageIterator[ListForecastsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListForecasts.html#ForecastService.Paginator.ListForecasts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listforecastspaginator)
        """


class ListMonitorEvaluationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListMonitorEvaluations.html#ForecastService.Paginator.ListMonitorEvaluations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listmonitorevaluationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMonitorEvaluationsRequestListMonitorEvaluationsPaginateTypeDef]
    ) -> _PageIterator[ListMonitorEvaluationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListMonitorEvaluations.html#ForecastService.Paginator.ListMonitorEvaluations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listmonitorevaluationspaginator)
        """


class ListMonitorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListMonitors.html#ForecastService.Paginator.ListMonitors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listmonitorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMonitorsRequestListMonitorsPaginateTypeDef]
    ) -> _PageIterator[ListMonitorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListMonitors.html#ForecastService.Paginator.ListMonitors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listmonitorspaginator)
        """


class ListPredictorBacktestExportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListPredictorBacktestExportJobs.html#ForecastService.Paginator.ListPredictorBacktestExportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listpredictorbacktestexportjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListPredictorBacktestExportJobsRequestListPredictorBacktestExportJobsPaginateTypeDef
        ],
    ) -> _PageIterator[ListPredictorBacktestExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListPredictorBacktestExportJobs.html#ForecastService.Paginator.ListPredictorBacktestExportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listpredictorbacktestexportjobspaginator)
        """


class ListPredictorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListPredictors.html#ForecastService.Paginator.ListPredictors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listpredictorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPredictorsRequestListPredictorsPaginateTypeDef]
    ) -> _PageIterator[ListPredictorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListPredictors.html#ForecastService.Paginator.ListPredictors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listpredictorspaginator)
        """


class ListWhatIfAnalysesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListWhatIfAnalyses.html#ForecastService.Paginator.ListWhatIfAnalyses)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listwhatifanalysespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWhatIfAnalysesRequestListWhatIfAnalysesPaginateTypeDef]
    ) -> _PageIterator[ListWhatIfAnalysesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListWhatIfAnalyses.html#ForecastService.Paginator.ListWhatIfAnalyses.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listwhatifanalysespaginator)
        """


class ListWhatIfForecastExportsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListWhatIfForecastExports.html#ForecastService.Paginator.ListWhatIfForecastExports)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listwhatifforecastexportspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListWhatIfForecastExportsRequestListWhatIfForecastExportsPaginateTypeDef],
    ) -> _PageIterator[ListWhatIfForecastExportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListWhatIfForecastExports.html#ForecastService.Paginator.ListWhatIfForecastExports.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listwhatifforecastexportspaginator)
        """


class ListWhatIfForecastsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListWhatIfForecasts.html#ForecastService.Paginator.ListWhatIfForecasts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listwhatifforecastspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWhatIfForecastsRequestListWhatIfForecastsPaginateTypeDef]
    ) -> _PageIterator[ListWhatIfForecastsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/paginator/ListWhatIfForecasts.html#ForecastService.Paginator.ListWhatIfForecasts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/paginators/#listwhatifforecastspaginator)
        """
