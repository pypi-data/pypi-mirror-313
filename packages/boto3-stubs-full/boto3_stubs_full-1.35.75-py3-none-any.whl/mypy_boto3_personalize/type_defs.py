"""
Type annotations for personalize service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/type_defs/)

Usage::

    ```python
    from mypy_boto3_personalize.type_defs import AlgorithmImageTypeDef

    data: AlgorithmImageTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    BatchInferenceJobModeType,
    DomainType,
    ImportModeType,
    IngestionModeType,
    ObjectiveSensitivityType,
    TrainingModeType,
    TrainingTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AlgorithmImageTypeDef",
    "AlgorithmTypeDef",
    "AutoMLConfigOutputTypeDef",
    "AutoMLConfigTypeDef",
    "AutoMLConfigUnionTypeDef",
    "AutoMLResultTypeDef",
    "AutoTrainingConfigTypeDef",
    "BatchInferenceJobConfigOutputTypeDef",
    "BatchInferenceJobConfigTypeDef",
    "BatchInferenceJobInputTypeDef",
    "BatchInferenceJobOutputTypeDef",
    "BatchInferenceJobSummaryTypeDef",
    "BatchInferenceJobTypeDef",
    "BatchSegmentJobInputTypeDef",
    "BatchSegmentJobOutputTypeDef",
    "BatchSegmentJobSummaryTypeDef",
    "BatchSegmentJobTypeDef",
    "CampaignConfigOutputTypeDef",
    "CampaignConfigTypeDef",
    "CampaignSummaryTypeDef",
    "CampaignTypeDef",
    "CampaignUpdateSummaryTypeDef",
    "CategoricalHyperParameterRangeOutputTypeDef",
    "CategoricalHyperParameterRangeTypeDef",
    "CategoricalHyperParameterRangeUnionTypeDef",
    "ContinuousHyperParameterRangeTypeDef",
    "CreateBatchInferenceJobRequestRequestTypeDef",
    "CreateBatchInferenceJobResponseTypeDef",
    "CreateBatchSegmentJobRequestRequestTypeDef",
    "CreateBatchSegmentJobResponseTypeDef",
    "CreateCampaignRequestRequestTypeDef",
    "CreateCampaignResponseTypeDef",
    "CreateDataDeletionJobRequestRequestTypeDef",
    "CreateDataDeletionJobResponseTypeDef",
    "CreateDatasetExportJobRequestRequestTypeDef",
    "CreateDatasetExportJobResponseTypeDef",
    "CreateDatasetGroupRequestRequestTypeDef",
    "CreateDatasetGroupResponseTypeDef",
    "CreateDatasetImportJobRequestRequestTypeDef",
    "CreateDatasetImportJobResponseTypeDef",
    "CreateDatasetRequestRequestTypeDef",
    "CreateDatasetResponseTypeDef",
    "CreateEventTrackerRequestRequestTypeDef",
    "CreateEventTrackerResponseTypeDef",
    "CreateFilterRequestRequestTypeDef",
    "CreateFilterResponseTypeDef",
    "CreateMetricAttributionRequestRequestTypeDef",
    "CreateMetricAttributionResponseTypeDef",
    "CreateRecommenderRequestRequestTypeDef",
    "CreateRecommenderResponseTypeDef",
    "CreateSchemaRequestRequestTypeDef",
    "CreateSchemaResponseTypeDef",
    "CreateSolutionRequestRequestTypeDef",
    "CreateSolutionResponseTypeDef",
    "CreateSolutionVersionRequestRequestTypeDef",
    "CreateSolutionVersionResponseTypeDef",
    "DataDeletionJobSummaryTypeDef",
    "DataDeletionJobTypeDef",
    "DataSourceTypeDef",
    "DatasetExportJobOutputTypeDef",
    "DatasetExportJobSummaryTypeDef",
    "DatasetExportJobTypeDef",
    "DatasetGroupSummaryTypeDef",
    "DatasetGroupTypeDef",
    "DatasetImportJobSummaryTypeDef",
    "DatasetImportJobTypeDef",
    "DatasetSchemaSummaryTypeDef",
    "DatasetSchemaTypeDef",
    "DatasetSummaryTypeDef",
    "DatasetTypeDef",
    "DatasetUpdateSummaryTypeDef",
    "DefaultCategoricalHyperParameterRangeTypeDef",
    "DefaultContinuousHyperParameterRangeTypeDef",
    "DefaultHyperParameterRangesTypeDef",
    "DefaultIntegerHyperParameterRangeTypeDef",
    "DeleteCampaignRequestRequestTypeDef",
    "DeleteDatasetGroupRequestRequestTypeDef",
    "DeleteDatasetRequestRequestTypeDef",
    "DeleteEventTrackerRequestRequestTypeDef",
    "DeleteFilterRequestRequestTypeDef",
    "DeleteMetricAttributionRequestRequestTypeDef",
    "DeleteRecommenderRequestRequestTypeDef",
    "DeleteSchemaRequestRequestTypeDef",
    "DeleteSolutionRequestRequestTypeDef",
    "DescribeAlgorithmRequestRequestTypeDef",
    "DescribeAlgorithmResponseTypeDef",
    "DescribeBatchInferenceJobRequestRequestTypeDef",
    "DescribeBatchInferenceJobResponseTypeDef",
    "DescribeBatchSegmentJobRequestRequestTypeDef",
    "DescribeBatchSegmentJobResponseTypeDef",
    "DescribeCampaignRequestRequestTypeDef",
    "DescribeCampaignResponseTypeDef",
    "DescribeDataDeletionJobRequestRequestTypeDef",
    "DescribeDataDeletionJobResponseTypeDef",
    "DescribeDatasetExportJobRequestRequestTypeDef",
    "DescribeDatasetExportJobResponseTypeDef",
    "DescribeDatasetGroupRequestRequestTypeDef",
    "DescribeDatasetGroupResponseTypeDef",
    "DescribeDatasetImportJobRequestRequestTypeDef",
    "DescribeDatasetImportJobResponseTypeDef",
    "DescribeDatasetRequestRequestTypeDef",
    "DescribeDatasetResponseTypeDef",
    "DescribeEventTrackerRequestRequestTypeDef",
    "DescribeEventTrackerResponseTypeDef",
    "DescribeFeatureTransformationRequestRequestTypeDef",
    "DescribeFeatureTransformationResponseTypeDef",
    "DescribeFilterRequestRequestTypeDef",
    "DescribeFilterResponseTypeDef",
    "DescribeMetricAttributionRequestRequestTypeDef",
    "DescribeMetricAttributionResponseTypeDef",
    "DescribeRecipeRequestRequestTypeDef",
    "DescribeRecipeResponseTypeDef",
    "DescribeRecommenderRequestRequestTypeDef",
    "DescribeRecommenderResponseTypeDef",
    "DescribeSchemaRequestRequestTypeDef",
    "DescribeSchemaResponseTypeDef",
    "DescribeSolutionRequestRequestTypeDef",
    "DescribeSolutionResponseTypeDef",
    "DescribeSolutionVersionRequestRequestTypeDef",
    "DescribeSolutionVersionResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EventTrackerSummaryTypeDef",
    "EventTrackerTypeDef",
    "FeatureTransformationTypeDef",
    "FieldsForThemeGenerationTypeDef",
    "FilterSummaryTypeDef",
    "FilterTypeDef",
    "GetSolutionMetricsRequestRequestTypeDef",
    "GetSolutionMetricsResponseTypeDef",
    "HPOConfigOutputTypeDef",
    "HPOConfigTypeDef",
    "HPOConfigUnionTypeDef",
    "HPOObjectiveTypeDef",
    "HPOResourceConfigTypeDef",
    "HyperParameterRangesOutputTypeDef",
    "HyperParameterRangesTypeDef",
    "HyperParameterRangesUnionTypeDef",
    "IntegerHyperParameterRangeTypeDef",
    "ListBatchInferenceJobsRequestListBatchInferenceJobsPaginateTypeDef",
    "ListBatchInferenceJobsRequestRequestTypeDef",
    "ListBatchInferenceJobsResponseTypeDef",
    "ListBatchSegmentJobsRequestListBatchSegmentJobsPaginateTypeDef",
    "ListBatchSegmentJobsRequestRequestTypeDef",
    "ListBatchSegmentJobsResponseTypeDef",
    "ListCampaignsRequestListCampaignsPaginateTypeDef",
    "ListCampaignsRequestRequestTypeDef",
    "ListCampaignsResponseTypeDef",
    "ListDataDeletionJobsRequestRequestTypeDef",
    "ListDataDeletionJobsResponseTypeDef",
    "ListDatasetExportJobsRequestListDatasetExportJobsPaginateTypeDef",
    "ListDatasetExportJobsRequestRequestTypeDef",
    "ListDatasetExportJobsResponseTypeDef",
    "ListDatasetGroupsRequestListDatasetGroupsPaginateTypeDef",
    "ListDatasetGroupsRequestRequestTypeDef",
    "ListDatasetGroupsResponseTypeDef",
    "ListDatasetImportJobsRequestListDatasetImportJobsPaginateTypeDef",
    "ListDatasetImportJobsRequestRequestTypeDef",
    "ListDatasetImportJobsResponseTypeDef",
    "ListDatasetsRequestListDatasetsPaginateTypeDef",
    "ListDatasetsRequestRequestTypeDef",
    "ListDatasetsResponseTypeDef",
    "ListEventTrackersRequestListEventTrackersPaginateTypeDef",
    "ListEventTrackersRequestRequestTypeDef",
    "ListEventTrackersResponseTypeDef",
    "ListFiltersRequestListFiltersPaginateTypeDef",
    "ListFiltersRequestRequestTypeDef",
    "ListFiltersResponseTypeDef",
    "ListMetricAttributionMetricsRequestListMetricAttributionMetricsPaginateTypeDef",
    "ListMetricAttributionMetricsRequestRequestTypeDef",
    "ListMetricAttributionMetricsResponseTypeDef",
    "ListMetricAttributionsRequestListMetricAttributionsPaginateTypeDef",
    "ListMetricAttributionsRequestRequestTypeDef",
    "ListMetricAttributionsResponseTypeDef",
    "ListRecipesRequestListRecipesPaginateTypeDef",
    "ListRecipesRequestRequestTypeDef",
    "ListRecipesResponseTypeDef",
    "ListRecommendersRequestListRecommendersPaginateTypeDef",
    "ListRecommendersRequestRequestTypeDef",
    "ListRecommendersResponseTypeDef",
    "ListSchemasRequestListSchemasPaginateTypeDef",
    "ListSchemasRequestRequestTypeDef",
    "ListSchemasResponseTypeDef",
    "ListSolutionVersionsRequestListSolutionVersionsPaginateTypeDef",
    "ListSolutionVersionsRequestRequestTypeDef",
    "ListSolutionVersionsResponseTypeDef",
    "ListSolutionsRequestListSolutionsPaginateTypeDef",
    "ListSolutionsRequestRequestTypeDef",
    "ListSolutionsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MetricAttributeTypeDef",
    "MetricAttributionOutputTypeDef",
    "MetricAttributionSummaryTypeDef",
    "MetricAttributionTypeDef",
    "OptimizationObjectiveTypeDef",
    "PaginatorConfigTypeDef",
    "RecipeSummaryTypeDef",
    "RecipeTypeDef",
    "RecommenderConfigOutputTypeDef",
    "RecommenderConfigTypeDef",
    "RecommenderSummaryTypeDef",
    "RecommenderTypeDef",
    "RecommenderUpdateSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "S3DataConfigTypeDef",
    "SolutionConfigOutputTypeDef",
    "SolutionConfigTypeDef",
    "SolutionSummaryTypeDef",
    "SolutionTypeDef",
    "SolutionUpdateConfigTypeDef",
    "SolutionUpdateSummaryTypeDef",
    "SolutionVersionSummaryTypeDef",
    "SolutionVersionTypeDef",
    "StartRecommenderRequestRequestTypeDef",
    "StartRecommenderResponseTypeDef",
    "StopRecommenderRequestRequestTypeDef",
    "StopRecommenderResponseTypeDef",
    "StopSolutionVersionCreationRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "ThemeGenerationConfigTypeDef",
    "TrainingDataConfigOutputTypeDef",
    "TrainingDataConfigTypeDef",
    "TrainingDataConfigUnionTypeDef",
    "TunedHPOParamsTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCampaignRequestRequestTypeDef",
    "UpdateCampaignResponseTypeDef",
    "UpdateDatasetRequestRequestTypeDef",
    "UpdateDatasetResponseTypeDef",
    "UpdateMetricAttributionRequestRequestTypeDef",
    "UpdateMetricAttributionResponseTypeDef",
    "UpdateRecommenderRequestRequestTypeDef",
    "UpdateRecommenderResponseTypeDef",
    "UpdateSolutionRequestRequestTypeDef",
    "UpdateSolutionResponseTypeDef",
)


class AlgorithmImageTypeDef(TypedDict):
    dockerURI: str
    name: NotRequired[str]


class AutoMLConfigOutputTypeDef(TypedDict):
    metricName: NotRequired[str]
    recipeList: NotRequired[List[str]]


class AutoMLConfigTypeDef(TypedDict):
    metricName: NotRequired[str]
    recipeList: NotRequired[Sequence[str]]


class AutoMLResultTypeDef(TypedDict):
    bestRecipeArn: NotRequired[str]


class AutoTrainingConfigTypeDef(TypedDict):
    schedulingExpression: NotRequired[str]


class BatchInferenceJobConfigOutputTypeDef(TypedDict):
    itemExplorationConfig: NotRequired[Dict[str, str]]


class BatchInferenceJobConfigTypeDef(TypedDict):
    itemExplorationConfig: NotRequired[Mapping[str, str]]


class S3DataConfigTypeDef(TypedDict):
    path: str
    kmsKeyArn: NotRequired[str]


class BatchInferenceJobSummaryTypeDef(TypedDict):
    batchInferenceJobArn: NotRequired[str]
    jobName: NotRequired[str]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    failureReason: NotRequired[str]
    solutionVersionArn: NotRequired[str]
    batchInferenceJobMode: NotRequired[BatchInferenceJobModeType]


class BatchSegmentJobSummaryTypeDef(TypedDict):
    batchSegmentJobArn: NotRequired[str]
    jobName: NotRequired[str]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    failureReason: NotRequired[str]
    solutionVersionArn: NotRequired[str]


class CampaignConfigOutputTypeDef(TypedDict):
    itemExplorationConfig: NotRequired[Dict[str, str]]
    enableMetadataWithRecommendations: NotRequired[bool]
    syncWithLatestSolutionVersion: NotRequired[bool]


class CampaignConfigTypeDef(TypedDict):
    itemExplorationConfig: NotRequired[Mapping[str, str]]
    enableMetadataWithRecommendations: NotRequired[bool]
    syncWithLatestSolutionVersion: NotRequired[bool]


class CampaignSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    campaignArn: NotRequired[str]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    failureReason: NotRequired[str]


class CategoricalHyperParameterRangeOutputTypeDef(TypedDict):
    name: NotRequired[str]
    values: NotRequired[List[str]]


class CategoricalHyperParameterRangeTypeDef(TypedDict):
    name: NotRequired[str]
    values: NotRequired[Sequence[str]]


class ContinuousHyperParameterRangeTypeDef(TypedDict):
    name: NotRequired[str]
    minValue: NotRequired[float]
    maxValue: NotRequired[float]


class TagTypeDef(TypedDict):
    tagKey: str
    tagValue: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DataSourceTypeDef(TypedDict):
    dataLocation: NotRequired[str]


class MetricAttributeTypeDef(TypedDict):
    eventType: str
    metricName: str
    expression: str


class CreateSchemaRequestRequestTypeDef(TypedDict):
    name: str
    schema: str
    domain: NotRequired[DomainType]


class DataDeletionJobSummaryTypeDef(TypedDict):
    dataDeletionJobArn: NotRequired[str]
    datasetGroupArn: NotRequired[str]
    jobName: NotRequired[str]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    failureReason: NotRequired[str]


class DatasetExportJobSummaryTypeDef(TypedDict):
    datasetExportJobArn: NotRequired[str]
    jobName: NotRequired[str]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    failureReason: NotRequired[str]


class DatasetGroupSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    datasetGroupArn: NotRequired[str]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    failureReason: NotRequired[str]
    domain: NotRequired[DomainType]


class DatasetGroupTypeDef(TypedDict):
    name: NotRequired[str]
    datasetGroupArn: NotRequired[str]
    status: NotRequired[str]
    roleArn: NotRequired[str]
    kmsKeyArn: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    failureReason: NotRequired[str]
    domain: NotRequired[DomainType]


class DatasetImportJobSummaryTypeDef(TypedDict):
    datasetImportJobArn: NotRequired[str]
    jobName: NotRequired[str]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    failureReason: NotRequired[str]
    importMode: NotRequired[ImportModeType]


class DatasetSchemaSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    schemaArn: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    domain: NotRequired[DomainType]


class DatasetSchemaTypeDef(TypedDict):
    name: NotRequired[str]
    schemaArn: NotRequired[str]
    schema: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    domain: NotRequired[DomainType]


class DatasetSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    datasetArn: NotRequired[str]
    datasetType: NotRequired[str]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]


class DatasetUpdateSummaryTypeDef(TypedDict):
    schemaArn: NotRequired[str]
    status: NotRequired[str]
    failureReason: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]


class DefaultCategoricalHyperParameterRangeTypeDef(TypedDict):
    name: NotRequired[str]
    values: NotRequired[List[str]]
    isTunable: NotRequired[bool]


class DefaultContinuousHyperParameterRangeTypeDef(TypedDict):
    name: NotRequired[str]
    minValue: NotRequired[float]
    maxValue: NotRequired[float]
    isTunable: NotRequired[bool]


class DefaultIntegerHyperParameterRangeTypeDef(TypedDict):
    name: NotRequired[str]
    minValue: NotRequired[int]
    maxValue: NotRequired[int]
    isTunable: NotRequired[bool]


class DeleteCampaignRequestRequestTypeDef(TypedDict):
    campaignArn: str


class DeleteDatasetGroupRequestRequestTypeDef(TypedDict):
    datasetGroupArn: str


class DeleteDatasetRequestRequestTypeDef(TypedDict):
    datasetArn: str


class DeleteEventTrackerRequestRequestTypeDef(TypedDict):
    eventTrackerArn: str


class DeleteFilterRequestRequestTypeDef(TypedDict):
    filterArn: str


class DeleteMetricAttributionRequestRequestTypeDef(TypedDict):
    metricAttributionArn: str


class DeleteRecommenderRequestRequestTypeDef(TypedDict):
    recommenderArn: str


class DeleteSchemaRequestRequestTypeDef(TypedDict):
    schemaArn: str


class DeleteSolutionRequestRequestTypeDef(TypedDict):
    solutionArn: str


class DescribeAlgorithmRequestRequestTypeDef(TypedDict):
    algorithmArn: str


class DescribeBatchInferenceJobRequestRequestTypeDef(TypedDict):
    batchInferenceJobArn: str


class DescribeBatchSegmentJobRequestRequestTypeDef(TypedDict):
    batchSegmentJobArn: str


class DescribeCampaignRequestRequestTypeDef(TypedDict):
    campaignArn: str


class DescribeDataDeletionJobRequestRequestTypeDef(TypedDict):
    dataDeletionJobArn: str


class DescribeDatasetExportJobRequestRequestTypeDef(TypedDict):
    datasetExportJobArn: str


class DescribeDatasetGroupRequestRequestTypeDef(TypedDict):
    datasetGroupArn: str


class DescribeDatasetImportJobRequestRequestTypeDef(TypedDict):
    datasetImportJobArn: str


class DescribeDatasetRequestRequestTypeDef(TypedDict):
    datasetArn: str


class DescribeEventTrackerRequestRequestTypeDef(TypedDict):
    eventTrackerArn: str


class EventTrackerTypeDef(TypedDict):
    name: NotRequired[str]
    eventTrackerArn: NotRequired[str]
    accountId: NotRequired[str]
    trackingId: NotRequired[str]
    datasetGroupArn: NotRequired[str]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]


class DescribeFeatureTransformationRequestRequestTypeDef(TypedDict):
    featureTransformationArn: str


class FeatureTransformationTypeDef(TypedDict):
    name: NotRequired[str]
    featureTransformationArn: NotRequired[str]
    defaultParameters: NotRequired[Dict[str, str]]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    status: NotRequired[str]


class DescribeFilterRequestRequestTypeDef(TypedDict):
    filterArn: str


class FilterTypeDef(TypedDict):
    name: NotRequired[str]
    filterArn: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    datasetGroupArn: NotRequired[str]
    failureReason: NotRequired[str]
    filterExpression: NotRequired[str]
    status: NotRequired[str]


class DescribeMetricAttributionRequestRequestTypeDef(TypedDict):
    metricAttributionArn: str


class DescribeRecipeRequestRequestTypeDef(TypedDict):
    recipeArn: str


class RecipeTypeDef(TypedDict):
    name: NotRequired[str]
    recipeArn: NotRequired[str]
    algorithmArn: NotRequired[str]
    featureTransformationArn: NotRequired[str]
    status: NotRequired[str]
    description: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    recipeType: NotRequired[str]
    lastUpdatedDateTime: NotRequired[datetime]


class DescribeRecommenderRequestRequestTypeDef(TypedDict):
    recommenderArn: str


class DescribeSchemaRequestRequestTypeDef(TypedDict):
    schemaArn: str


class DescribeSolutionRequestRequestTypeDef(TypedDict):
    solutionArn: str


class DescribeSolutionVersionRequestRequestTypeDef(TypedDict):
    solutionVersionArn: str


class EventTrackerSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    eventTrackerArn: NotRequired[str]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]


class FieldsForThemeGenerationTypeDef(TypedDict):
    itemName: str


class FilterSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    filterArn: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    datasetGroupArn: NotRequired[str]
    failureReason: NotRequired[str]
    status: NotRequired[str]


class GetSolutionMetricsRequestRequestTypeDef(TypedDict):
    solutionVersionArn: str


HPOObjectiveTypeDef = TypedDict(
    "HPOObjectiveTypeDef",
    {
        "type": NotRequired[str],
        "metricName": NotRequired[str],
        "metricRegex": NotRequired[str],
    },
)


class HPOResourceConfigTypeDef(TypedDict):
    maxNumberOfTrainingJobs: NotRequired[str]
    maxParallelTrainingJobs: NotRequired[str]


class IntegerHyperParameterRangeTypeDef(TypedDict):
    name: NotRequired[str]
    minValue: NotRequired[int]
    maxValue: NotRequired[int]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListBatchInferenceJobsRequestRequestTypeDef(TypedDict):
    solutionVersionArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListBatchSegmentJobsRequestRequestTypeDef(TypedDict):
    solutionVersionArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListCampaignsRequestRequestTypeDef(TypedDict):
    solutionArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDataDeletionJobsRequestRequestTypeDef(TypedDict):
    datasetGroupArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDatasetExportJobsRequestRequestTypeDef(TypedDict):
    datasetArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDatasetGroupsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDatasetImportJobsRequestRequestTypeDef(TypedDict):
    datasetArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDatasetsRequestRequestTypeDef(TypedDict):
    datasetGroupArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListEventTrackersRequestRequestTypeDef(TypedDict):
    datasetGroupArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListFiltersRequestRequestTypeDef(TypedDict):
    datasetGroupArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListMetricAttributionMetricsRequestRequestTypeDef(TypedDict):
    metricAttributionArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListMetricAttributionsRequestRequestTypeDef(TypedDict):
    datasetGroupArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class MetricAttributionSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    metricAttributionArn: NotRequired[str]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    failureReason: NotRequired[str]


class ListRecipesRequestRequestTypeDef(TypedDict):
    recipeProvider: NotRequired[Literal["SERVICE"]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    domain: NotRequired[DomainType]


class RecipeSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    recipeArn: NotRequired[str]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    domain: NotRequired[DomainType]


class ListRecommendersRequestRequestTypeDef(TypedDict):
    datasetGroupArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListSchemasRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListSolutionVersionsRequestRequestTypeDef(TypedDict):
    solutionArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class SolutionVersionSummaryTypeDef(TypedDict):
    solutionVersionArn: NotRequired[str]
    status: NotRequired[str]
    trainingMode: NotRequired[TrainingModeType]
    trainingType: NotRequired[TrainingTypeType]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    failureReason: NotRequired[str]


class ListSolutionsRequestRequestTypeDef(TypedDict):
    datasetGroupArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class SolutionSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    solutionArn: NotRequired[str]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    recipeArn: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class OptimizationObjectiveTypeDef(TypedDict):
    itemAttribute: NotRequired[str]
    objectiveSensitivity: NotRequired[ObjectiveSensitivityType]


class TrainingDataConfigOutputTypeDef(TypedDict):
    excludedDatasetColumns: NotRequired[Dict[str, List[str]]]


class TunedHPOParamsTypeDef(TypedDict):
    algorithmHyperParameters: NotRequired[Dict[str, str]]


class StartRecommenderRequestRequestTypeDef(TypedDict):
    recommenderArn: str


class StopRecommenderRequestRequestTypeDef(TypedDict):
    recommenderArn: str


class StopSolutionVersionCreationRequestRequestTypeDef(TypedDict):
    solutionVersionArn: str


class TrainingDataConfigTypeDef(TypedDict):
    excludedDatasetColumns: NotRequired[Mapping[str, Sequence[str]]]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateDatasetRequestRequestTypeDef(TypedDict):
    datasetArn: str
    schemaArn: str


AutoMLConfigUnionTypeDef = Union[AutoMLConfigTypeDef, AutoMLConfigOutputTypeDef]


class SolutionUpdateConfigTypeDef(TypedDict):
    autoTrainingConfig: NotRequired[AutoTrainingConfigTypeDef]


class BatchInferenceJobInputTypeDef(TypedDict):
    s3DataSource: S3DataConfigTypeDef


class BatchInferenceJobOutputTypeDef(TypedDict):
    s3DataDestination: S3DataConfigTypeDef


class BatchSegmentJobInputTypeDef(TypedDict):
    s3DataSource: S3DataConfigTypeDef


class BatchSegmentJobOutputTypeDef(TypedDict):
    s3DataDestination: S3DataConfigTypeDef


class DatasetExportJobOutputTypeDef(TypedDict):
    s3DataDestination: S3DataConfigTypeDef


class MetricAttributionOutputTypeDef(TypedDict):
    roleArn: str
    s3DataDestination: NotRequired[S3DataConfigTypeDef]


class CampaignUpdateSummaryTypeDef(TypedDict):
    solutionVersionArn: NotRequired[str]
    minProvisionedTPS: NotRequired[int]
    campaignConfig: NotRequired[CampaignConfigOutputTypeDef]
    status: NotRequired[str]
    failureReason: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]


class UpdateCampaignRequestRequestTypeDef(TypedDict):
    campaignArn: str
    solutionVersionArn: NotRequired[str]
    minProvisionedTPS: NotRequired[int]
    campaignConfig: NotRequired[CampaignConfigTypeDef]


CategoricalHyperParameterRangeUnionTypeDef = Union[
    CategoricalHyperParameterRangeTypeDef, CategoricalHyperParameterRangeOutputTypeDef
]


class CreateCampaignRequestRequestTypeDef(TypedDict):
    name: str
    solutionVersionArn: str
    minProvisionedTPS: NotRequired[int]
    campaignConfig: NotRequired[CampaignConfigTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateDatasetGroupRequestRequestTypeDef(TypedDict):
    name: str
    roleArn: NotRequired[str]
    kmsKeyArn: NotRequired[str]
    domain: NotRequired[DomainType]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateDatasetRequestRequestTypeDef(TypedDict):
    name: str
    schemaArn: str
    datasetGroupArn: str
    datasetType: str
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateEventTrackerRequestRequestTypeDef(TypedDict):
    name: str
    datasetGroupArn: str
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateFilterRequestRequestTypeDef(TypedDict):
    name: str
    datasetGroupArn: str
    filterExpression: str
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateSolutionVersionRequestRequestTypeDef(TypedDict):
    solutionArn: str
    name: NotRequired[str]
    trainingMode: NotRequired[TrainingModeType]
    tags: NotRequired[Sequence[TagTypeDef]]


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]


class CreateBatchInferenceJobResponseTypeDef(TypedDict):
    batchInferenceJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBatchSegmentJobResponseTypeDef(TypedDict):
    batchSegmentJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCampaignResponseTypeDef(TypedDict):
    campaignArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataDeletionJobResponseTypeDef(TypedDict):
    dataDeletionJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDatasetExportJobResponseTypeDef(TypedDict):
    datasetExportJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDatasetGroupResponseTypeDef(TypedDict):
    datasetGroupArn: str
    domain: DomainType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDatasetImportJobResponseTypeDef(TypedDict):
    datasetImportJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDatasetResponseTypeDef(TypedDict):
    datasetArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEventTrackerResponseTypeDef(TypedDict):
    eventTrackerArn: str
    trackingId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFilterResponseTypeDef(TypedDict):
    filterArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMetricAttributionResponseTypeDef(TypedDict):
    metricAttributionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRecommenderResponseTypeDef(TypedDict):
    recommenderArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSchemaResponseTypeDef(TypedDict):
    schemaArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSolutionResponseTypeDef(TypedDict):
    solutionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSolutionVersionResponseTypeDef(TypedDict):
    solutionVersionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetSolutionMetricsResponseTypeDef(TypedDict):
    solutionVersionArn: str
    metrics: Dict[str, float]
    ResponseMetadata: ResponseMetadataTypeDef


class ListBatchInferenceJobsResponseTypeDef(TypedDict):
    batchInferenceJobs: List[BatchInferenceJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListBatchSegmentJobsResponseTypeDef(TypedDict):
    batchSegmentJobs: List[BatchSegmentJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListCampaignsResponseTypeDef(TypedDict):
    campaigns: List[CampaignSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class StartRecommenderResponseTypeDef(TypedDict):
    recommenderArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StopRecommenderResponseTypeDef(TypedDict):
    recommenderArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCampaignResponseTypeDef(TypedDict):
    campaignArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDatasetResponseTypeDef(TypedDict):
    datasetArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMetricAttributionResponseTypeDef(TypedDict):
    metricAttributionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRecommenderResponseTypeDef(TypedDict):
    recommenderArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSolutionResponseTypeDef(TypedDict):
    solutionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataDeletionJobRequestRequestTypeDef(TypedDict):
    jobName: str
    datasetGroupArn: str
    dataSource: DataSourceTypeDef
    roleArn: str
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateDatasetImportJobRequestRequestTypeDef(TypedDict):
    jobName: str
    datasetArn: str
    dataSource: DataSourceTypeDef
    roleArn: str
    tags: NotRequired[Sequence[TagTypeDef]]
    importMode: NotRequired[ImportModeType]
    publishAttributionMetricsToS3: NotRequired[bool]


class DataDeletionJobTypeDef(TypedDict):
    jobName: NotRequired[str]
    dataDeletionJobArn: NotRequired[str]
    datasetGroupArn: NotRequired[str]
    dataSource: NotRequired[DataSourceTypeDef]
    roleArn: NotRequired[str]
    status: NotRequired[str]
    numDeleted: NotRequired[int]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    failureReason: NotRequired[str]


class DatasetImportJobTypeDef(TypedDict):
    jobName: NotRequired[str]
    datasetImportJobArn: NotRequired[str]
    datasetArn: NotRequired[str]
    dataSource: NotRequired[DataSourceTypeDef]
    roleArn: NotRequired[str]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    failureReason: NotRequired[str]
    importMode: NotRequired[ImportModeType]
    publishAttributionMetricsToS3: NotRequired[bool]


class ListMetricAttributionMetricsResponseTypeDef(TypedDict):
    metrics: List[MetricAttributeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListDataDeletionJobsResponseTypeDef(TypedDict):
    dataDeletionJobs: List[DataDeletionJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListDatasetExportJobsResponseTypeDef(TypedDict):
    datasetExportJobs: List[DatasetExportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListDatasetGroupsResponseTypeDef(TypedDict):
    datasetGroups: List[DatasetGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DescribeDatasetGroupResponseTypeDef(TypedDict):
    datasetGroup: DatasetGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDatasetImportJobsResponseTypeDef(TypedDict):
    datasetImportJobs: List[DatasetImportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSchemasResponseTypeDef(TypedDict):
    schemas: List[DatasetSchemaSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DescribeSchemaResponseTypeDef(TypedDict):
    schema: DatasetSchemaTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDatasetsResponseTypeDef(TypedDict):
    datasets: List[DatasetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DatasetTypeDef(TypedDict):
    name: NotRequired[str]
    datasetArn: NotRequired[str]
    datasetGroupArn: NotRequired[str]
    datasetType: NotRequired[str]
    schemaArn: NotRequired[str]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    latestDatasetUpdate: NotRequired[DatasetUpdateSummaryTypeDef]
    trackingId: NotRequired[str]


class DefaultHyperParameterRangesTypeDef(TypedDict):
    integerHyperParameterRanges: NotRequired[List[DefaultIntegerHyperParameterRangeTypeDef]]
    continuousHyperParameterRanges: NotRequired[List[DefaultContinuousHyperParameterRangeTypeDef]]
    categoricalHyperParameterRanges: NotRequired[List[DefaultCategoricalHyperParameterRangeTypeDef]]


class DescribeEventTrackerResponseTypeDef(TypedDict):
    eventTracker: EventTrackerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFeatureTransformationResponseTypeDef(TypedDict):
    featureTransformation: FeatureTransformationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


DescribeFilterResponseTypeDef = TypedDict(
    "DescribeFilterResponseTypeDef",
    {
        "filter": FilterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class DescribeRecipeResponseTypeDef(TypedDict):
    recipe: RecipeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListEventTrackersResponseTypeDef(TypedDict):
    eventTrackers: List[EventTrackerSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ThemeGenerationConfigTypeDef(TypedDict):
    fieldsForThemeGeneration: FieldsForThemeGenerationTypeDef


class ListFiltersResponseTypeDef(TypedDict):
    Filters: List[FilterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class HyperParameterRangesOutputTypeDef(TypedDict):
    integerHyperParameterRanges: NotRequired[List[IntegerHyperParameterRangeTypeDef]]
    continuousHyperParameterRanges: NotRequired[List[ContinuousHyperParameterRangeTypeDef]]
    categoricalHyperParameterRanges: NotRequired[List[CategoricalHyperParameterRangeOutputTypeDef]]


class ListBatchInferenceJobsRequestListBatchInferenceJobsPaginateTypeDef(TypedDict):
    solutionVersionArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBatchSegmentJobsRequestListBatchSegmentJobsPaginateTypeDef(TypedDict):
    solutionVersionArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCampaignsRequestListCampaignsPaginateTypeDef(TypedDict):
    solutionArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDatasetExportJobsRequestListDatasetExportJobsPaginateTypeDef(TypedDict):
    datasetArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDatasetGroupsRequestListDatasetGroupsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDatasetImportJobsRequestListDatasetImportJobsPaginateTypeDef(TypedDict):
    datasetArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDatasetsRequestListDatasetsPaginateTypeDef(TypedDict):
    datasetGroupArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEventTrackersRequestListEventTrackersPaginateTypeDef(TypedDict):
    datasetGroupArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFiltersRequestListFiltersPaginateTypeDef(TypedDict):
    datasetGroupArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMetricAttributionMetricsRequestListMetricAttributionMetricsPaginateTypeDef(TypedDict):
    metricAttributionArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMetricAttributionsRequestListMetricAttributionsPaginateTypeDef(TypedDict):
    datasetGroupArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRecipesRequestListRecipesPaginateTypeDef(TypedDict):
    recipeProvider: NotRequired[Literal["SERVICE"]]
    domain: NotRequired[DomainType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRecommendersRequestListRecommendersPaginateTypeDef(TypedDict):
    datasetGroupArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSchemasRequestListSchemasPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSolutionVersionsRequestListSolutionVersionsPaginateTypeDef(TypedDict):
    solutionArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSolutionsRequestListSolutionsPaginateTypeDef(TypedDict):
    datasetGroupArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMetricAttributionsResponseTypeDef(TypedDict):
    metricAttributions: List[MetricAttributionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListRecipesResponseTypeDef(TypedDict):
    recipes: List[RecipeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSolutionVersionsResponseTypeDef(TypedDict):
    solutionVersions: List[SolutionVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSolutionsResponseTypeDef(TypedDict):
    solutions: List[SolutionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class RecommenderConfigOutputTypeDef(TypedDict):
    itemExplorationConfig: NotRequired[Dict[str, str]]
    minRecommendationRequestsPerSecond: NotRequired[int]
    trainingDataConfig: NotRequired[TrainingDataConfigOutputTypeDef]
    enableMetadataWithRecommendations: NotRequired[bool]


TrainingDataConfigUnionTypeDef = Union[TrainingDataConfigTypeDef, TrainingDataConfigOutputTypeDef]


class SolutionUpdateSummaryTypeDef(TypedDict):
    solutionUpdateConfig: NotRequired[SolutionUpdateConfigTypeDef]
    status: NotRequired[str]
    performAutoTraining: NotRequired[bool]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    failureReason: NotRequired[str]


class UpdateSolutionRequestRequestTypeDef(TypedDict):
    solutionArn: str
    performAutoTraining: NotRequired[bool]
    solutionUpdateConfig: NotRequired[SolutionUpdateConfigTypeDef]


class BatchSegmentJobTypeDef(TypedDict):
    jobName: NotRequired[str]
    batchSegmentJobArn: NotRequired[str]
    filterArn: NotRequired[str]
    failureReason: NotRequired[str]
    solutionVersionArn: NotRequired[str]
    numResults: NotRequired[int]
    jobInput: NotRequired[BatchSegmentJobInputTypeDef]
    jobOutput: NotRequired[BatchSegmentJobOutputTypeDef]
    roleArn: NotRequired[str]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]


class CreateBatchSegmentJobRequestRequestTypeDef(TypedDict):
    jobName: str
    solutionVersionArn: str
    jobInput: BatchSegmentJobInputTypeDef
    jobOutput: BatchSegmentJobOutputTypeDef
    roleArn: str
    filterArn: NotRequired[str]
    numResults: NotRequired[int]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateDatasetExportJobRequestRequestTypeDef(TypedDict):
    jobName: str
    datasetArn: str
    roleArn: str
    jobOutput: DatasetExportJobOutputTypeDef
    ingestionMode: NotRequired[IngestionModeType]
    tags: NotRequired[Sequence[TagTypeDef]]


class DatasetExportJobTypeDef(TypedDict):
    jobName: NotRequired[str]
    datasetExportJobArn: NotRequired[str]
    datasetArn: NotRequired[str]
    ingestionMode: NotRequired[IngestionModeType]
    roleArn: NotRequired[str]
    status: NotRequired[str]
    jobOutput: NotRequired[DatasetExportJobOutputTypeDef]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    failureReason: NotRequired[str]


class CreateMetricAttributionRequestRequestTypeDef(TypedDict):
    name: str
    datasetGroupArn: str
    metrics: Sequence[MetricAttributeTypeDef]
    metricsOutputConfig: MetricAttributionOutputTypeDef


class MetricAttributionTypeDef(TypedDict):
    name: NotRequired[str]
    metricAttributionArn: NotRequired[str]
    datasetGroupArn: NotRequired[str]
    metricsOutputConfig: NotRequired[MetricAttributionOutputTypeDef]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    failureReason: NotRequired[str]


class UpdateMetricAttributionRequestRequestTypeDef(TypedDict):
    addMetrics: NotRequired[Sequence[MetricAttributeTypeDef]]
    removeMetrics: NotRequired[Sequence[str]]
    metricsOutputConfig: NotRequired[MetricAttributionOutputTypeDef]
    metricAttributionArn: NotRequired[str]


class CampaignTypeDef(TypedDict):
    name: NotRequired[str]
    campaignArn: NotRequired[str]
    solutionVersionArn: NotRequired[str]
    minProvisionedTPS: NotRequired[int]
    campaignConfig: NotRequired[CampaignConfigOutputTypeDef]
    status: NotRequired[str]
    failureReason: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    latestCampaignUpdate: NotRequired[CampaignUpdateSummaryTypeDef]


class HyperParameterRangesTypeDef(TypedDict):
    integerHyperParameterRanges: NotRequired[Sequence[IntegerHyperParameterRangeTypeDef]]
    continuousHyperParameterRanges: NotRequired[Sequence[ContinuousHyperParameterRangeTypeDef]]
    categoricalHyperParameterRanges: NotRequired[
        Sequence[CategoricalHyperParameterRangeUnionTypeDef]
    ]


class DescribeDataDeletionJobResponseTypeDef(TypedDict):
    dataDeletionJob: DataDeletionJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDatasetImportJobResponseTypeDef(TypedDict):
    datasetImportJob: DatasetImportJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDatasetResponseTypeDef(TypedDict):
    dataset: DatasetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AlgorithmTypeDef(TypedDict):
    name: NotRequired[str]
    algorithmArn: NotRequired[str]
    algorithmImage: NotRequired[AlgorithmImageTypeDef]
    defaultHyperParameters: NotRequired[Dict[str, str]]
    defaultHyperParameterRanges: NotRequired[DefaultHyperParameterRangesTypeDef]
    defaultResourceConfig: NotRequired[Dict[str, str]]
    trainingInputMode: NotRequired[str]
    roleArn: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]


class BatchInferenceJobTypeDef(TypedDict):
    jobName: NotRequired[str]
    batchInferenceJobArn: NotRequired[str]
    filterArn: NotRequired[str]
    failureReason: NotRequired[str]
    solutionVersionArn: NotRequired[str]
    numResults: NotRequired[int]
    jobInput: NotRequired[BatchInferenceJobInputTypeDef]
    jobOutput: NotRequired[BatchInferenceJobOutputTypeDef]
    batchInferenceJobConfig: NotRequired[BatchInferenceJobConfigOutputTypeDef]
    roleArn: NotRequired[str]
    batchInferenceJobMode: NotRequired[BatchInferenceJobModeType]
    themeGenerationConfig: NotRequired[ThemeGenerationConfigTypeDef]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]


class CreateBatchInferenceJobRequestRequestTypeDef(TypedDict):
    jobName: str
    solutionVersionArn: str
    jobInput: BatchInferenceJobInputTypeDef
    jobOutput: BatchInferenceJobOutputTypeDef
    roleArn: str
    filterArn: NotRequired[str]
    numResults: NotRequired[int]
    batchInferenceJobConfig: NotRequired[BatchInferenceJobConfigTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]
    batchInferenceJobMode: NotRequired[BatchInferenceJobModeType]
    themeGenerationConfig: NotRequired[ThemeGenerationConfigTypeDef]


class HPOConfigOutputTypeDef(TypedDict):
    hpoObjective: NotRequired[HPOObjectiveTypeDef]
    hpoResourceConfig: NotRequired[HPOResourceConfigTypeDef]
    algorithmHyperParameterRanges: NotRequired[HyperParameterRangesOutputTypeDef]


class RecommenderSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    recommenderArn: NotRequired[str]
    datasetGroupArn: NotRequired[str]
    recipeArn: NotRequired[str]
    recommenderConfig: NotRequired[RecommenderConfigOutputTypeDef]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]


class RecommenderUpdateSummaryTypeDef(TypedDict):
    recommenderConfig: NotRequired[RecommenderConfigOutputTypeDef]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    status: NotRequired[str]
    failureReason: NotRequired[str]


class RecommenderConfigTypeDef(TypedDict):
    itemExplorationConfig: NotRequired[Mapping[str, str]]
    minRecommendationRequestsPerSecond: NotRequired[int]
    trainingDataConfig: NotRequired[TrainingDataConfigUnionTypeDef]
    enableMetadataWithRecommendations: NotRequired[bool]


class DescribeBatchSegmentJobResponseTypeDef(TypedDict):
    batchSegmentJob: BatchSegmentJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDatasetExportJobResponseTypeDef(TypedDict):
    datasetExportJob: DatasetExportJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeMetricAttributionResponseTypeDef(TypedDict):
    metricAttribution: MetricAttributionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCampaignResponseTypeDef(TypedDict):
    campaign: CampaignTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


HyperParameterRangesUnionTypeDef = Union[
    HyperParameterRangesTypeDef, HyperParameterRangesOutputTypeDef
]


class DescribeAlgorithmResponseTypeDef(TypedDict):
    algorithm: AlgorithmTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeBatchInferenceJobResponseTypeDef(TypedDict):
    batchInferenceJob: BatchInferenceJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SolutionConfigOutputTypeDef(TypedDict):
    eventValueThreshold: NotRequired[str]
    hpoConfig: NotRequired[HPOConfigOutputTypeDef]
    algorithmHyperParameters: NotRequired[Dict[str, str]]
    featureTransformationParameters: NotRequired[Dict[str, str]]
    autoMLConfig: NotRequired[AutoMLConfigOutputTypeDef]
    optimizationObjective: NotRequired[OptimizationObjectiveTypeDef]
    trainingDataConfig: NotRequired[TrainingDataConfigOutputTypeDef]
    autoTrainingConfig: NotRequired[AutoTrainingConfigTypeDef]


class ListRecommendersResponseTypeDef(TypedDict):
    recommenders: List[RecommenderSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class RecommenderTypeDef(TypedDict):
    recommenderArn: NotRequired[str]
    datasetGroupArn: NotRequired[str]
    name: NotRequired[str]
    recipeArn: NotRequired[str]
    recommenderConfig: NotRequired[RecommenderConfigOutputTypeDef]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    status: NotRequired[str]
    failureReason: NotRequired[str]
    latestRecommenderUpdate: NotRequired[RecommenderUpdateSummaryTypeDef]
    modelMetrics: NotRequired[Dict[str, float]]


class CreateRecommenderRequestRequestTypeDef(TypedDict):
    name: str
    datasetGroupArn: str
    recipeArn: str
    recommenderConfig: NotRequired[RecommenderConfigTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]


class UpdateRecommenderRequestRequestTypeDef(TypedDict):
    recommenderArn: str
    recommenderConfig: RecommenderConfigTypeDef


class HPOConfigTypeDef(TypedDict):
    hpoObjective: NotRequired[HPOObjectiveTypeDef]
    hpoResourceConfig: NotRequired[HPOResourceConfigTypeDef]
    algorithmHyperParameterRanges: NotRequired[HyperParameterRangesUnionTypeDef]


class SolutionTypeDef(TypedDict):
    name: NotRequired[str]
    solutionArn: NotRequired[str]
    performHPO: NotRequired[bool]
    performAutoML: NotRequired[bool]
    performAutoTraining: NotRequired[bool]
    recipeArn: NotRequired[str]
    datasetGroupArn: NotRequired[str]
    eventType: NotRequired[str]
    solutionConfig: NotRequired[SolutionConfigOutputTypeDef]
    autoMLResult: NotRequired[AutoMLResultTypeDef]
    status: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    latestSolutionVersion: NotRequired[SolutionVersionSummaryTypeDef]
    latestSolutionUpdate: NotRequired[SolutionUpdateSummaryTypeDef]


class SolutionVersionTypeDef(TypedDict):
    name: NotRequired[str]
    solutionVersionArn: NotRequired[str]
    solutionArn: NotRequired[str]
    performHPO: NotRequired[bool]
    performAutoML: NotRequired[bool]
    recipeArn: NotRequired[str]
    eventType: NotRequired[str]
    datasetGroupArn: NotRequired[str]
    solutionConfig: NotRequired[SolutionConfigOutputTypeDef]
    trainingHours: NotRequired[float]
    trainingMode: NotRequired[TrainingModeType]
    tunedHPOParams: NotRequired[TunedHPOParamsTypeDef]
    status: NotRequired[str]
    failureReason: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    trainingType: NotRequired[TrainingTypeType]


class DescribeRecommenderResponseTypeDef(TypedDict):
    recommender: RecommenderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


HPOConfigUnionTypeDef = Union[HPOConfigTypeDef, HPOConfigOutputTypeDef]


class DescribeSolutionResponseTypeDef(TypedDict):
    solution: SolutionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSolutionVersionResponseTypeDef(TypedDict):
    solutionVersion: SolutionVersionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SolutionConfigTypeDef(TypedDict):
    eventValueThreshold: NotRequired[str]
    hpoConfig: NotRequired[HPOConfigUnionTypeDef]
    algorithmHyperParameters: NotRequired[Mapping[str, str]]
    featureTransformationParameters: NotRequired[Mapping[str, str]]
    autoMLConfig: NotRequired[AutoMLConfigUnionTypeDef]
    optimizationObjective: NotRequired[OptimizationObjectiveTypeDef]
    trainingDataConfig: NotRequired[TrainingDataConfigUnionTypeDef]
    autoTrainingConfig: NotRequired[AutoTrainingConfigTypeDef]


class CreateSolutionRequestRequestTypeDef(TypedDict):
    name: str
    datasetGroupArn: str
    performHPO: NotRequired[bool]
    performAutoML: NotRequired[bool]
    performAutoTraining: NotRequired[bool]
    recipeArn: NotRequired[str]
    eventType: NotRequired[str]
    solutionConfig: NotRequired[SolutionConfigTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]
