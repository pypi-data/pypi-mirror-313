"""
Type annotations for forecast service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_forecast.client import ForecastServiceClient

    session = Session()
    client: ForecastServiceClient = session.client("forecast")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
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
from .type_defs import (
    CreateAutoPredictorRequestRequestTypeDef,
    CreateAutoPredictorResponseTypeDef,
    CreateDatasetGroupRequestRequestTypeDef,
    CreateDatasetGroupResponseTypeDef,
    CreateDatasetImportJobRequestRequestTypeDef,
    CreateDatasetImportJobResponseTypeDef,
    CreateDatasetRequestRequestTypeDef,
    CreateDatasetResponseTypeDef,
    CreateExplainabilityExportRequestRequestTypeDef,
    CreateExplainabilityExportResponseTypeDef,
    CreateExplainabilityRequestRequestTypeDef,
    CreateExplainabilityResponseTypeDef,
    CreateForecastExportJobRequestRequestTypeDef,
    CreateForecastExportJobResponseTypeDef,
    CreateForecastRequestRequestTypeDef,
    CreateForecastResponseTypeDef,
    CreateMonitorRequestRequestTypeDef,
    CreateMonitorResponseTypeDef,
    CreatePredictorBacktestExportJobRequestRequestTypeDef,
    CreatePredictorBacktestExportJobResponseTypeDef,
    CreatePredictorRequestRequestTypeDef,
    CreatePredictorResponseTypeDef,
    CreateWhatIfAnalysisRequestRequestTypeDef,
    CreateWhatIfAnalysisResponseTypeDef,
    CreateWhatIfForecastExportRequestRequestTypeDef,
    CreateWhatIfForecastExportResponseTypeDef,
    CreateWhatIfForecastRequestRequestTypeDef,
    CreateWhatIfForecastResponseTypeDef,
    DeleteDatasetGroupRequestRequestTypeDef,
    DeleteDatasetImportJobRequestRequestTypeDef,
    DeleteDatasetRequestRequestTypeDef,
    DeleteExplainabilityExportRequestRequestTypeDef,
    DeleteExplainabilityRequestRequestTypeDef,
    DeleteForecastExportJobRequestRequestTypeDef,
    DeleteForecastRequestRequestTypeDef,
    DeleteMonitorRequestRequestTypeDef,
    DeletePredictorBacktestExportJobRequestRequestTypeDef,
    DeletePredictorRequestRequestTypeDef,
    DeleteResourceTreeRequestRequestTypeDef,
    DeleteWhatIfAnalysisRequestRequestTypeDef,
    DeleteWhatIfForecastExportRequestRequestTypeDef,
    DeleteWhatIfForecastRequestRequestTypeDef,
    DescribeAutoPredictorRequestRequestTypeDef,
    DescribeAutoPredictorResponseTypeDef,
    DescribeDatasetGroupRequestRequestTypeDef,
    DescribeDatasetGroupResponseTypeDef,
    DescribeDatasetImportJobRequestRequestTypeDef,
    DescribeDatasetImportJobResponseTypeDef,
    DescribeDatasetRequestRequestTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeExplainabilityExportRequestRequestTypeDef,
    DescribeExplainabilityExportResponseTypeDef,
    DescribeExplainabilityRequestRequestTypeDef,
    DescribeExplainabilityResponseTypeDef,
    DescribeForecastExportJobRequestRequestTypeDef,
    DescribeForecastExportJobResponseTypeDef,
    DescribeForecastRequestRequestTypeDef,
    DescribeForecastResponseTypeDef,
    DescribeMonitorRequestRequestTypeDef,
    DescribeMonitorResponseTypeDef,
    DescribePredictorBacktestExportJobRequestRequestTypeDef,
    DescribePredictorBacktestExportJobResponseTypeDef,
    DescribePredictorRequestRequestTypeDef,
    DescribePredictorResponseTypeDef,
    DescribeWhatIfAnalysisRequestRequestTypeDef,
    DescribeWhatIfAnalysisResponseTypeDef,
    DescribeWhatIfForecastExportRequestRequestTypeDef,
    DescribeWhatIfForecastExportResponseTypeDef,
    DescribeWhatIfForecastRequestRequestTypeDef,
    DescribeWhatIfForecastResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAccuracyMetricsRequestRequestTypeDef,
    GetAccuracyMetricsResponseTypeDef,
    ListDatasetGroupsRequestRequestTypeDef,
    ListDatasetGroupsResponseTypeDef,
    ListDatasetImportJobsRequestRequestTypeDef,
    ListDatasetImportJobsResponseTypeDef,
    ListDatasetsRequestRequestTypeDef,
    ListDatasetsResponseTypeDef,
    ListExplainabilitiesRequestRequestTypeDef,
    ListExplainabilitiesResponseTypeDef,
    ListExplainabilityExportsRequestRequestTypeDef,
    ListExplainabilityExportsResponseTypeDef,
    ListForecastExportJobsRequestRequestTypeDef,
    ListForecastExportJobsResponseTypeDef,
    ListForecastsRequestRequestTypeDef,
    ListForecastsResponseTypeDef,
    ListMonitorEvaluationsRequestRequestTypeDef,
    ListMonitorEvaluationsResponseTypeDef,
    ListMonitorsRequestRequestTypeDef,
    ListMonitorsResponseTypeDef,
    ListPredictorBacktestExportJobsRequestRequestTypeDef,
    ListPredictorBacktestExportJobsResponseTypeDef,
    ListPredictorsRequestRequestTypeDef,
    ListPredictorsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWhatIfAnalysesRequestRequestTypeDef,
    ListWhatIfAnalysesResponseTypeDef,
    ListWhatIfForecastExportsRequestRequestTypeDef,
    ListWhatIfForecastExportsResponseTypeDef,
    ListWhatIfForecastsRequestRequestTypeDef,
    ListWhatIfForecastsResponseTypeDef,
    ResumeResourceRequestRequestTypeDef,
    StopResourceRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDatasetGroupRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ForecastServiceClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]

class ForecastServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast.html#ForecastService.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ForecastServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast.html#ForecastService.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#close)
        """

    def create_auto_predictor(
        self, **kwargs: Unpack[CreateAutoPredictorRequestRequestTypeDef]
    ) -> CreateAutoPredictorResponseTypeDef:
        """
        Creates an Amazon Forecast predictor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/create_auto_predictor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#create_auto_predictor)
        """

    def create_dataset(
        self, **kwargs: Unpack[CreateDatasetRequestRequestTypeDef]
    ) -> CreateDatasetResponseTypeDef:
        """
        Creates an Amazon Forecast dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/create_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#create_dataset)
        """

    def create_dataset_group(
        self, **kwargs: Unpack[CreateDatasetGroupRequestRequestTypeDef]
    ) -> CreateDatasetGroupResponseTypeDef:
        """
        Creates a dataset group, which holds a collection of related datasets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/create_dataset_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#create_dataset_group)
        """

    def create_dataset_import_job(
        self, **kwargs: Unpack[CreateDatasetImportJobRequestRequestTypeDef]
    ) -> CreateDatasetImportJobResponseTypeDef:
        """
        Imports your training data to an Amazon Forecast dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/create_dataset_import_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#create_dataset_import_job)
        """

    def create_explainability(
        self, **kwargs: Unpack[CreateExplainabilityRequestRequestTypeDef]
    ) -> CreateExplainabilityResponseTypeDef:
        """
        Explainability is only available for Forecasts and Predictors generated from an
        AutoPredictor (<a>CreateAutoPredictor</a>).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/create_explainability.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#create_explainability)
        """

    def create_explainability_export(
        self, **kwargs: Unpack[CreateExplainabilityExportRequestRequestTypeDef]
    ) -> CreateExplainabilityExportResponseTypeDef:
        """
        Exports an Explainability resource created by the <a>CreateExplainability</a>
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/create_explainability_export.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#create_explainability_export)
        """

    def create_forecast(
        self, **kwargs: Unpack[CreateForecastRequestRequestTypeDef]
    ) -> CreateForecastResponseTypeDef:
        """
        Creates a forecast for each item in the <code>TARGET_TIME_SERIES</code> dataset
        that was used to train the predictor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/create_forecast.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#create_forecast)
        """

    def create_forecast_export_job(
        self, **kwargs: Unpack[CreateForecastExportJobRequestRequestTypeDef]
    ) -> CreateForecastExportJobResponseTypeDef:
        """
        Exports a forecast created by the <a>CreateForecast</a> operation to your
        Amazon Simple Storage Service (Amazon S3) bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/create_forecast_export_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#create_forecast_export_job)
        """

    def create_monitor(
        self, **kwargs: Unpack[CreateMonitorRequestRequestTypeDef]
    ) -> CreateMonitorResponseTypeDef:
        """
        Creates a predictor monitor resource for an existing auto predictor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/create_monitor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#create_monitor)
        """

    def create_predictor(
        self, **kwargs: Unpack[CreatePredictorRequestRequestTypeDef]
    ) -> CreatePredictorResponseTypeDef:
        """
        This operation creates a legacy predictor that does not include all the
        predictor functionalities provided by Amazon Forecast.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/create_predictor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#create_predictor)
        """

    def create_predictor_backtest_export_job(
        self, **kwargs: Unpack[CreatePredictorBacktestExportJobRequestRequestTypeDef]
    ) -> CreatePredictorBacktestExportJobResponseTypeDef:
        """
        Exports backtest forecasts and accuracy metrics generated by the
        <a>CreateAutoPredictor</a> or <a>CreatePredictor</a> operations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/create_predictor_backtest_export_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#create_predictor_backtest_export_job)
        """

    def create_what_if_analysis(
        self, **kwargs: Unpack[CreateWhatIfAnalysisRequestRequestTypeDef]
    ) -> CreateWhatIfAnalysisResponseTypeDef:
        """
        What-if analysis is a scenario modeling technique where you make a hypothetical
        change to a time series and compare the forecasts generated by these changes
        against the baseline, unchanged time series.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/create_what_if_analysis.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#create_what_if_analysis)
        """

    def create_what_if_forecast(
        self, **kwargs: Unpack[CreateWhatIfForecastRequestRequestTypeDef]
    ) -> CreateWhatIfForecastResponseTypeDef:
        """
        A what-if forecast is a forecast that is created from a modified version of the
        baseline forecast.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/create_what_if_forecast.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#create_what_if_forecast)
        """

    def create_what_if_forecast_export(
        self, **kwargs: Unpack[CreateWhatIfForecastExportRequestRequestTypeDef]
    ) -> CreateWhatIfForecastExportResponseTypeDef:
        """
        Exports a forecast created by the <a>CreateWhatIfForecast</a> operation to your
        Amazon Simple Storage Service (Amazon S3) bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/create_what_if_forecast_export.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#create_what_if_forecast_export)
        """

    def delete_dataset(
        self, **kwargs: Unpack[DeleteDatasetRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Forecast dataset that was created using the <a
        href="https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDataset.html">CreateDataset</a>
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/delete_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#delete_dataset)
        """

    def delete_dataset_group(
        self, **kwargs: Unpack[DeleteDatasetGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a dataset group created using the <a
        href="https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDatasetGroup.html">CreateDatasetGroup</a>
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/delete_dataset_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#delete_dataset_group)
        """

    def delete_dataset_import_job(
        self, **kwargs: Unpack[DeleteDatasetImportJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a dataset import job created using the <a
        href="https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDatasetImportJob.html">CreateDatasetImportJob</a>
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/delete_dataset_import_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#delete_dataset_import_job)
        """

    def delete_explainability(
        self, **kwargs: Unpack[DeleteExplainabilityRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Explainability resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/delete_explainability.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#delete_explainability)
        """

    def delete_explainability_export(
        self, **kwargs: Unpack[DeleteExplainabilityExportRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Explainability export.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/delete_explainability_export.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#delete_explainability_export)
        """

    def delete_forecast(
        self, **kwargs: Unpack[DeleteForecastRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a forecast created using the <a>CreateForecast</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/delete_forecast.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#delete_forecast)
        """

    def delete_forecast_export_job(
        self, **kwargs: Unpack[DeleteForecastExportJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a forecast export job created using the <a>CreateForecastExportJob</a>
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/delete_forecast_export_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#delete_forecast_export_job)
        """

    def delete_monitor(
        self, **kwargs: Unpack[DeleteMonitorRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a monitor resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/delete_monitor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#delete_monitor)
        """

    def delete_predictor(
        self, **kwargs: Unpack[DeletePredictorRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a predictor created using the <a>DescribePredictor</a> or
        <a>CreatePredictor</a> operations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/delete_predictor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#delete_predictor)
        """

    def delete_predictor_backtest_export_job(
        self, **kwargs: Unpack[DeletePredictorBacktestExportJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a predictor backtest export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/delete_predictor_backtest_export_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#delete_predictor_backtest_export_job)
        """

    def delete_resource_tree(
        self, **kwargs: Unpack[DeleteResourceTreeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an entire resource tree.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/delete_resource_tree.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#delete_resource_tree)
        """

    def delete_what_if_analysis(
        self, **kwargs: Unpack[DeleteWhatIfAnalysisRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a what-if analysis created using the <a>CreateWhatIfAnalysis</a>
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/delete_what_if_analysis.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#delete_what_if_analysis)
        """

    def delete_what_if_forecast(
        self, **kwargs: Unpack[DeleteWhatIfForecastRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a what-if forecast created using the <a>CreateWhatIfForecast</a>
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/delete_what_if_forecast.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#delete_what_if_forecast)
        """

    def delete_what_if_forecast_export(
        self, **kwargs: Unpack[DeleteWhatIfForecastExportRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a what-if forecast export created using the
        <a>CreateWhatIfForecastExport</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/delete_what_if_forecast_export.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#delete_what_if_forecast_export)
        """

    def describe_auto_predictor(
        self, **kwargs: Unpack[DescribeAutoPredictorRequestRequestTypeDef]
    ) -> DescribeAutoPredictorResponseTypeDef:
        """
        Describes a predictor created using the CreateAutoPredictor operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/describe_auto_predictor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#describe_auto_predictor)
        """

    def describe_dataset(
        self, **kwargs: Unpack[DescribeDatasetRequestRequestTypeDef]
    ) -> DescribeDatasetResponseTypeDef:
        """
        Describes an Amazon Forecast dataset created using the <a
        href="https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDataset.html">CreateDataset</a>
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/describe_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#describe_dataset)
        """

    def describe_dataset_group(
        self, **kwargs: Unpack[DescribeDatasetGroupRequestRequestTypeDef]
    ) -> DescribeDatasetGroupResponseTypeDef:
        """
        Describes a dataset group created using the <a
        href="https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDatasetGroup.html">CreateDatasetGroup</a>
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/describe_dataset_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#describe_dataset_group)
        """

    def describe_dataset_import_job(
        self, **kwargs: Unpack[DescribeDatasetImportJobRequestRequestTypeDef]
    ) -> DescribeDatasetImportJobResponseTypeDef:
        """
        Describes a dataset import job created using the <a
        href="https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDatasetImportJob.html">CreateDatasetImportJob</a>
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/describe_dataset_import_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#describe_dataset_import_job)
        """

    def describe_explainability(
        self, **kwargs: Unpack[DescribeExplainabilityRequestRequestTypeDef]
    ) -> DescribeExplainabilityResponseTypeDef:
        """
        Describes an Explainability resource created using the
        <a>CreateExplainability</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/describe_explainability.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#describe_explainability)
        """

    def describe_explainability_export(
        self, **kwargs: Unpack[DescribeExplainabilityExportRequestRequestTypeDef]
    ) -> DescribeExplainabilityExportResponseTypeDef:
        """
        Describes an Explainability export created using the
        <a>CreateExplainabilityExport</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/describe_explainability_export.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#describe_explainability_export)
        """

    def describe_forecast(
        self, **kwargs: Unpack[DescribeForecastRequestRequestTypeDef]
    ) -> DescribeForecastResponseTypeDef:
        """
        Describes a forecast created using the <a>CreateForecast</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/describe_forecast.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#describe_forecast)
        """

    def describe_forecast_export_job(
        self, **kwargs: Unpack[DescribeForecastExportJobRequestRequestTypeDef]
    ) -> DescribeForecastExportJobResponseTypeDef:
        """
        Describes a forecast export job created using the
        <a>CreateForecastExportJob</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/describe_forecast_export_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#describe_forecast_export_job)
        """

    def describe_monitor(
        self, **kwargs: Unpack[DescribeMonitorRequestRequestTypeDef]
    ) -> DescribeMonitorResponseTypeDef:
        """
        Describes a monitor resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/describe_monitor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#describe_monitor)
        """

    def describe_predictor(
        self, **kwargs: Unpack[DescribePredictorRequestRequestTypeDef]
    ) -> DescribePredictorResponseTypeDef:
        """
        This operation is only valid for legacy predictors created with CreatePredictor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/describe_predictor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#describe_predictor)
        """

    def describe_predictor_backtest_export_job(
        self, **kwargs: Unpack[DescribePredictorBacktestExportJobRequestRequestTypeDef]
    ) -> DescribePredictorBacktestExportJobResponseTypeDef:
        """
        Describes a predictor backtest export job created using the
        <a>CreatePredictorBacktestExportJob</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/describe_predictor_backtest_export_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#describe_predictor_backtest_export_job)
        """

    def describe_what_if_analysis(
        self, **kwargs: Unpack[DescribeWhatIfAnalysisRequestRequestTypeDef]
    ) -> DescribeWhatIfAnalysisResponseTypeDef:
        """
        Describes the what-if analysis created using the <a>CreateWhatIfAnalysis</a>
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/describe_what_if_analysis.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#describe_what_if_analysis)
        """

    def describe_what_if_forecast(
        self, **kwargs: Unpack[DescribeWhatIfForecastRequestRequestTypeDef]
    ) -> DescribeWhatIfForecastResponseTypeDef:
        """
        Describes the what-if forecast created using the <a>CreateWhatIfForecast</a>
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/describe_what_if_forecast.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#describe_what_if_forecast)
        """

    def describe_what_if_forecast_export(
        self, **kwargs: Unpack[DescribeWhatIfForecastExportRequestRequestTypeDef]
    ) -> DescribeWhatIfForecastExportResponseTypeDef:
        """
        Describes the what-if forecast export created using the
        <a>CreateWhatIfForecastExport</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/describe_what_if_forecast_export.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#describe_what_if_forecast_export)
        """

    def get_accuracy_metrics(
        self, **kwargs: Unpack[GetAccuracyMetricsRequestRequestTypeDef]
    ) -> GetAccuracyMetricsResponseTypeDef:
        """
        Provides metrics on the accuracy of the models that were trained by the
        <a>CreatePredictor</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/get_accuracy_metrics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#get_accuracy_metrics)
        """

    def list_dataset_groups(
        self, **kwargs: Unpack[ListDatasetGroupsRequestRequestTypeDef]
    ) -> ListDatasetGroupsResponseTypeDef:
        """
        Returns a list of dataset groups created using the <a
        href="https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDatasetGroup.html">CreateDatasetGroup</a>
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/list_dataset_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#list_dataset_groups)
        """

    def list_dataset_import_jobs(
        self, **kwargs: Unpack[ListDatasetImportJobsRequestRequestTypeDef]
    ) -> ListDatasetImportJobsResponseTypeDef:
        """
        Returns a list of dataset import jobs created using the <a
        href="https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDatasetImportJob.html">CreateDatasetImportJob</a>
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/list_dataset_import_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#list_dataset_import_jobs)
        """

    def list_datasets(
        self, **kwargs: Unpack[ListDatasetsRequestRequestTypeDef]
    ) -> ListDatasetsResponseTypeDef:
        """
        Returns a list of datasets created using the <a
        href="https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDataset.html">CreateDataset</a>
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/list_datasets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#list_datasets)
        """

    def list_explainabilities(
        self, **kwargs: Unpack[ListExplainabilitiesRequestRequestTypeDef]
    ) -> ListExplainabilitiesResponseTypeDef:
        """
        Returns a list of Explainability resources created using the
        <a>CreateExplainability</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/list_explainabilities.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#list_explainabilities)
        """

    def list_explainability_exports(
        self, **kwargs: Unpack[ListExplainabilityExportsRequestRequestTypeDef]
    ) -> ListExplainabilityExportsResponseTypeDef:
        """
        Returns a list of Explainability exports created using the
        <a>CreateExplainabilityExport</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/list_explainability_exports.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#list_explainability_exports)
        """

    def list_forecast_export_jobs(
        self, **kwargs: Unpack[ListForecastExportJobsRequestRequestTypeDef]
    ) -> ListForecastExportJobsResponseTypeDef:
        """
        Returns a list of forecast export jobs created using the
        <a>CreateForecastExportJob</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/list_forecast_export_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#list_forecast_export_jobs)
        """

    def list_forecasts(
        self, **kwargs: Unpack[ListForecastsRequestRequestTypeDef]
    ) -> ListForecastsResponseTypeDef:
        """
        Returns a list of forecasts created using the <a>CreateForecast</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/list_forecasts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#list_forecasts)
        """

    def list_monitor_evaluations(
        self, **kwargs: Unpack[ListMonitorEvaluationsRequestRequestTypeDef]
    ) -> ListMonitorEvaluationsResponseTypeDef:
        """
        Returns a list of the monitoring evaluation results and predictor events
        collected by the monitor resource during different windows of time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/list_monitor_evaluations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#list_monitor_evaluations)
        """

    def list_monitors(
        self, **kwargs: Unpack[ListMonitorsRequestRequestTypeDef]
    ) -> ListMonitorsResponseTypeDef:
        """
        Returns a list of monitors created with the <a>CreateMonitor</a> operation and
        <a>CreateAutoPredictor</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/list_monitors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#list_monitors)
        """

    def list_predictor_backtest_export_jobs(
        self, **kwargs: Unpack[ListPredictorBacktestExportJobsRequestRequestTypeDef]
    ) -> ListPredictorBacktestExportJobsResponseTypeDef:
        """
        Returns a list of predictor backtest export jobs created using the
        <a>CreatePredictorBacktestExportJob</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/list_predictor_backtest_export_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#list_predictor_backtest_export_jobs)
        """

    def list_predictors(
        self, **kwargs: Unpack[ListPredictorsRequestRequestTypeDef]
    ) -> ListPredictorsResponseTypeDef:
        """
        Returns a list of predictors created using the <a>CreateAutoPredictor</a> or
        <a>CreatePredictor</a> operations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/list_predictors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#list_predictors)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for an Amazon Forecast resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#list_tags_for_resource)
        """

    def list_what_if_analyses(
        self, **kwargs: Unpack[ListWhatIfAnalysesRequestRequestTypeDef]
    ) -> ListWhatIfAnalysesResponseTypeDef:
        """
        Returns a list of what-if analyses created using the
        <a>CreateWhatIfAnalysis</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/list_what_if_analyses.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#list_what_if_analyses)
        """

    def list_what_if_forecast_exports(
        self, **kwargs: Unpack[ListWhatIfForecastExportsRequestRequestTypeDef]
    ) -> ListWhatIfForecastExportsResponseTypeDef:
        """
        Returns a list of what-if forecast exports created using the
        <a>CreateWhatIfForecastExport</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/list_what_if_forecast_exports.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#list_what_if_forecast_exports)
        """

    def list_what_if_forecasts(
        self, **kwargs: Unpack[ListWhatIfForecastsRequestRequestTypeDef]
    ) -> ListWhatIfForecastsResponseTypeDef:
        """
        Returns a list of what-if forecasts created using the
        <a>CreateWhatIfForecast</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/list_what_if_forecasts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#list_what_if_forecasts)
        """

    def resume_resource(
        self, **kwargs: Unpack[ResumeResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Resumes a stopped monitor resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/resume_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#resume_resource)
        """

    def stop_resource(
        self, **kwargs: Unpack[StopResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/stop_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#stop_resource)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified
        <code>resourceArn</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#untag_resource)
        """

    def update_dataset_group(
        self, **kwargs: Unpack[UpdateDatasetGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Replaces the datasets in a dataset group with the specified datasets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/update_dataset_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#update_dataset_group)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dataset_groups"]
    ) -> ListDatasetGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dataset_import_jobs"]
    ) -> ListDatasetImportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_datasets"]) -> ListDatasetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_explainabilities"]
    ) -> ListExplainabilitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_explainability_exports"]
    ) -> ListExplainabilityExportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_forecast_export_jobs"]
    ) -> ListForecastExportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_forecasts"]) -> ListForecastsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_monitor_evaluations"]
    ) -> ListMonitorEvaluationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_monitors"]) -> ListMonitorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_predictor_backtest_export_jobs"]
    ) -> ListPredictorBacktestExportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_predictors"]) -> ListPredictorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_what_if_analyses"]
    ) -> ListWhatIfAnalysesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_what_if_forecast_exports"]
    ) -> ListWhatIfForecastExportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_what_if_forecasts"]
    ) -> ListWhatIfForecastsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/client/#get_paginator)
        """
