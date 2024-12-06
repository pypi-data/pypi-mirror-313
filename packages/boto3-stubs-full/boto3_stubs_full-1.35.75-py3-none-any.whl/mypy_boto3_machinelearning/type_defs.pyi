"""
Type annotations for machinelearning service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/type_defs/)

Usage::

    ```python
    from mypy_boto3_machinelearning.type_defs import TagTypeDef

    data: TagTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    BatchPredictionFilterVariableType,
    DataSourceFilterVariableType,
    DetailsAttributesType,
    EntityStatusType,
    EvaluationFilterVariableType,
    MLModelFilterVariableType,
    MLModelTypeType,
    RealtimeEndpointStatusType,
    SortOrderType,
    TaggableResourceTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AddTagsInputRequestTypeDef",
    "AddTagsOutputTypeDef",
    "BatchPredictionTypeDef",
    "CreateBatchPredictionInputRequestTypeDef",
    "CreateBatchPredictionOutputTypeDef",
    "CreateDataSourceFromRDSInputRequestTypeDef",
    "CreateDataSourceFromRDSOutputTypeDef",
    "CreateDataSourceFromRedshiftInputRequestTypeDef",
    "CreateDataSourceFromRedshiftOutputTypeDef",
    "CreateDataSourceFromS3InputRequestTypeDef",
    "CreateDataSourceFromS3OutputTypeDef",
    "CreateEvaluationInputRequestTypeDef",
    "CreateEvaluationOutputTypeDef",
    "CreateMLModelInputRequestTypeDef",
    "CreateMLModelOutputTypeDef",
    "CreateRealtimeEndpointInputRequestTypeDef",
    "CreateRealtimeEndpointOutputTypeDef",
    "DataSourceTypeDef",
    "DeleteBatchPredictionInputRequestTypeDef",
    "DeleteBatchPredictionOutputTypeDef",
    "DeleteDataSourceInputRequestTypeDef",
    "DeleteDataSourceOutputTypeDef",
    "DeleteEvaluationInputRequestTypeDef",
    "DeleteEvaluationOutputTypeDef",
    "DeleteMLModelInputRequestTypeDef",
    "DeleteMLModelOutputTypeDef",
    "DeleteRealtimeEndpointInputRequestTypeDef",
    "DeleteRealtimeEndpointOutputTypeDef",
    "DeleteTagsInputRequestTypeDef",
    "DeleteTagsOutputTypeDef",
    "DescribeBatchPredictionsInputBatchPredictionAvailableWaitTypeDef",
    "DescribeBatchPredictionsInputDescribeBatchPredictionsPaginateTypeDef",
    "DescribeBatchPredictionsInputRequestTypeDef",
    "DescribeBatchPredictionsOutputTypeDef",
    "DescribeDataSourcesInputDataSourceAvailableWaitTypeDef",
    "DescribeDataSourcesInputDescribeDataSourcesPaginateTypeDef",
    "DescribeDataSourcesInputRequestTypeDef",
    "DescribeDataSourcesOutputTypeDef",
    "DescribeEvaluationsInputDescribeEvaluationsPaginateTypeDef",
    "DescribeEvaluationsInputEvaluationAvailableWaitTypeDef",
    "DescribeEvaluationsInputRequestTypeDef",
    "DescribeEvaluationsOutputTypeDef",
    "DescribeMLModelsInputDescribeMLModelsPaginateTypeDef",
    "DescribeMLModelsInputMLModelAvailableWaitTypeDef",
    "DescribeMLModelsInputRequestTypeDef",
    "DescribeMLModelsOutputTypeDef",
    "DescribeTagsInputRequestTypeDef",
    "DescribeTagsOutputTypeDef",
    "EvaluationTypeDef",
    "GetBatchPredictionInputRequestTypeDef",
    "GetBatchPredictionOutputTypeDef",
    "GetDataSourceInputRequestTypeDef",
    "GetDataSourceOutputTypeDef",
    "GetEvaluationInputRequestTypeDef",
    "GetEvaluationOutputTypeDef",
    "GetMLModelInputRequestTypeDef",
    "GetMLModelOutputTypeDef",
    "MLModelTypeDef",
    "PaginatorConfigTypeDef",
    "PerformanceMetricsTypeDef",
    "PredictInputRequestTypeDef",
    "PredictOutputTypeDef",
    "PredictionTypeDef",
    "RDSDataSpecTypeDef",
    "RDSDatabaseCredentialsTypeDef",
    "RDSDatabaseTypeDef",
    "RDSMetadataTypeDef",
    "RealtimeEndpointInfoTypeDef",
    "RedshiftDataSpecTypeDef",
    "RedshiftDatabaseCredentialsTypeDef",
    "RedshiftDatabaseTypeDef",
    "RedshiftMetadataTypeDef",
    "ResponseMetadataTypeDef",
    "S3DataSpecTypeDef",
    "TagTypeDef",
    "UpdateBatchPredictionInputRequestTypeDef",
    "UpdateBatchPredictionOutputTypeDef",
    "UpdateDataSourceInputRequestTypeDef",
    "UpdateDataSourceOutputTypeDef",
    "UpdateEvaluationInputRequestTypeDef",
    "UpdateEvaluationOutputTypeDef",
    "UpdateMLModelInputRequestTypeDef",
    "UpdateMLModelOutputTypeDef",
    "WaiterConfigTypeDef",
)

class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BatchPredictionTypeDef(TypedDict):
    BatchPredictionId: NotRequired[str]
    MLModelId: NotRequired[str]
    BatchPredictionDataSourceId: NotRequired[str]
    InputDataLocationS3: NotRequired[str]
    CreatedByIamUser: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    LastUpdatedAt: NotRequired[datetime]
    Name: NotRequired[str]
    Status: NotRequired[EntityStatusType]
    OutputUri: NotRequired[str]
    Message: NotRequired[str]
    ComputeTime: NotRequired[int]
    FinishedAt: NotRequired[datetime]
    StartedAt: NotRequired[datetime]
    TotalRecordCount: NotRequired[int]
    InvalidRecordCount: NotRequired[int]

class CreateBatchPredictionInputRequestTypeDef(TypedDict):
    BatchPredictionId: str
    MLModelId: str
    BatchPredictionDataSourceId: str
    OutputUri: str
    BatchPredictionName: NotRequired[str]

class S3DataSpecTypeDef(TypedDict):
    DataLocationS3: str
    DataRearrangement: NotRequired[str]
    DataSchema: NotRequired[str]
    DataSchemaLocationS3: NotRequired[str]

class CreateEvaluationInputRequestTypeDef(TypedDict):
    EvaluationId: str
    MLModelId: str
    EvaluationDataSourceId: str
    EvaluationName: NotRequired[str]

class CreateMLModelInputRequestTypeDef(TypedDict):
    MLModelId: str
    MLModelType: MLModelTypeType
    TrainingDataSourceId: str
    MLModelName: NotRequired[str]
    Parameters: NotRequired[Mapping[str, str]]
    Recipe: NotRequired[str]
    RecipeUri: NotRequired[str]

class CreateRealtimeEndpointInputRequestTypeDef(TypedDict):
    MLModelId: str

class RealtimeEndpointInfoTypeDef(TypedDict):
    PeakRequestsPerSecond: NotRequired[int]
    CreatedAt: NotRequired[datetime]
    EndpointUrl: NotRequired[str]
    EndpointStatus: NotRequired[RealtimeEndpointStatusType]

class DeleteBatchPredictionInputRequestTypeDef(TypedDict):
    BatchPredictionId: str

class DeleteDataSourceInputRequestTypeDef(TypedDict):
    DataSourceId: str

class DeleteEvaluationInputRequestTypeDef(TypedDict):
    EvaluationId: str

class DeleteMLModelInputRequestTypeDef(TypedDict):
    MLModelId: str

class DeleteRealtimeEndpointInputRequestTypeDef(TypedDict):
    MLModelId: str

class DeleteTagsInputRequestTypeDef(TypedDict):
    TagKeys: Sequence[str]
    ResourceId: str
    ResourceType: TaggableResourceTypeType

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeBatchPredictionsInputRequestTypeDef(TypedDict):
    FilterVariable: NotRequired[BatchPredictionFilterVariableType]
    EQ: NotRequired[str]
    GT: NotRequired[str]
    LT: NotRequired[str]
    GE: NotRequired[str]
    LE: NotRequired[str]
    NE: NotRequired[str]
    Prefix: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]

class DescribeDataSourcesInputRequestTypeDef(TypedDict):
    FilterVariable: NotRequired[DataSourceFilterVariableType]
    EQ: NotRequired[str]
    GT: NotRequired[str]
    LT: NotRequired[str]
    GE: NotRequired[str]
    LE: NotRequired[str]
    NE: NotRequired[str]
    Prefix: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]

class DescribeEvaluationsInputRequestTypeDef(TypedDict):
    FilterVariable: NotRequired[EvaluationFilterVariableType]
    EQ: NotRequired[str]
    GT: NotRequired[str]
    LT: NotRequired[str]
    GE: NotRequired[str]
    LE: NotRequired[str]
    NE: NotRequired[str]
    Prefix: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]

class DescribeMLModelsInputRequestTypeDef(TypedDict):
    FilterVariable: NotRequired[MLModelFilterVariableType]
    EQ: NotRequired[str]
    GT: NotRequired[str]
    LT: NotRequired[str]
    GE: NotRequired[str]
    LE: NotRequired[str]
    NE: NotRequired[str]
    Prefix: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]

class DescribeTagsInputRequestTypeDef(TypedDict):
    ResourceId: str
    ResourceType: TaggableResourceTypeType

class PerformanceMetricsTypeDef(TypedDict):
    Properties: NotRequired[Dict[str, str]]

class GetBatchPredictionInputRequestTypeDef(TypedDict):
    BatchPredictionId: str

class GetDataSourceInputRequestTypeDef(TypedDict):
    DataSourceId: str
    Verbose: NotRequired[bool]

class GetEvaluationInputRequestTypeDef(TypedDict):
    EvaluationId: str

class GetMLModelInputRequestTypeDef(TypedDict):
    MLModelId: str
    Verbose: NotRequired[bool]

class PredictInputRequestTypeDef(TypedDict):
    MLModelId: str
    Record: Mapping[str, str]
    PredictEndpoint: str

class PredictionTypeDef(TypedDict):
    predictedLabel: NotRequired[str]
    predictedValue: NotRequired[float]
    predictedScores: NotRequired[Dict[str, float]]
    details: NotRequired[Dict[DetailsAttributesType, str]]

class RDSDatabaseCredentialsTypeDef(TypedDict):
    Username: str
    Password: str

class RDSDatabaseTypeDef(TypedDict):
    InstanceIdentifier: str
    DatabaseName: str

class RedshiftDatabaseCredentialsTypeDef(TypedDict):
    Username: str
    Password: str

class RedshiftDatabaseTypeDef(TypedDict):
    DatabaseName: str
    ClusterIdentifier: str

class UpdateBatchPredictionInputRequestTypeDef(TypedDict):
    BatchPredictionId: str
    BatchPredictionName: str

class UpdateDataSourceInputRequestTypeDef(TypedDict):
    DataSourceId: str
    DataSourceName: str

class UpdateEvaluationInputRequestTypeDef(TypedDict):
    EvaluationId: str
    EvaluationName: str

class UpdateMLModelInputRequestTypeDef(TypedDict):
    MLModelId: str
    MLModelName: NotRequired[str]
    ScoreThreshold: NotRequired[float]

class AddTagsInputRequestTypeDef(TypedDict):
    Tags: Sequence[TagTypeDef]
    ResourceId: str
    ResourceType: TaggableResourceTypeType

class AddTagsOutputTypeDef(TypedDict):
    ResourceId: str
    ResourceType: TaggableResourceTypeType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBatchPredictionOutputTypeDef(TypedDict):
    BatchPredictionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDataSourceFromRDSOutputTypeDef(TypedDict):
    DataSourceId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDataSourceFromRedshiftOutputTypeDef(TypedDict):
    DataSourceId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDataSourceFromS3OutputTypeDef(TypedDict):
    DataSourceId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEvaluationOutputTypeDef(TypedDict):
    EvaluationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMLModelOutputTypeDef(TypedDict):
    MLModelId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBatchPredictionOutputTypeDef(TypedDict):
    BatchPredictionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDataSourceOutputTypeDef(TypedDict):
    DataSourceId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteEvaluationOutputTypeDef(TypedDict):
    EvaluationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteMLModelOutputTypeDef(TypedDict):
    MLModelId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteTagsOutputTypeDef(TypedDict):
    ResourceId: str
    ResourceType: TaggableResourceTypeType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeTagsOutputTypeDef(TypedDict):
    ResourceId: str
    ResourceType: TaggableResourceTypeType
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetBatchPredictionOutputTypeDef(TypedDict):
    BatchPredictionId: str
    MLModelId: str
    BatchPredictionDataSourceId: str
    InputDataLocationS3: str
    CreatedByIamUser: str
    CreatedAt: datetime
    LastUpdatedAt: datetime
    Name: str
    Status: EntityStatusType
    OutputUri: str
    LogUri: str
    Message: str
    ComputeTime: int
    FinishedAt: datetime
    StartedAt: datetime
    TotalRecordCount: int
    InvalidRecordCount: int
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBatchPredictionOutputTypeDef(TypedDict):
    BatchPredictionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDataSourceOutputTypeDef(TypedDict):
    DataSourceId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEvaluationOutputTypeDef(TypedDict):
    EvaluationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateMLModelOutputTypeDef(TypedDict):
    MLModelId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeBatchPredictionsOutputTypeDef(TypedDict):
    Results: List[BatchPredictionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateDataSourceFromS3InputRequestTypeDef(TypedDict):
    DataSourceId: str
    DataSpec: S3DataSpecTypeDef
    DataSourceName: NotRequired[str]
    ComputeStatistics: NotRequired[bool]

class CreateRealtimeEndpointOutputTypeDef(TypedDict):
    MLModelId: str
    RealtimeEndpointInfo: RealtimeEndpointInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteRealtimeEndpointOutputTypeDef(TypedDict):
    MLModelId: str
    RealtimeEndpointInfo: RealtimeEndpointInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetMLModelOutputTypeDef(TypedDict):
    MLModelId: str
    TrainingDataSourceId: str
    CreatedByIamUser: str
    CreatedAt: datetime
    LastUpdatedAt: datetime
    Name: str
    Status: EntityStatusType
    SizeInBytes: int
    EndpointInfo: RealtimeEndpointInfoTypeDef
    TrainingParameters: Dict[str, str]
    InputDataLocationS3: str
    MLModelType: MLModelTypeType
    ScoreThreshold: float
    ScoreThresholdLastUpdatedAt: datetime
    LogUri: str
    Message: str
    ComputeTime: int
    FinishedAt: datetime
    StartedAt: datetime
    Recipe: str
    Schema: str
    ResponseMetadata: ResponseMetadataTypeDef

class MLModelTypeDef(TypedDict):
    MLModelId: NotRequired[str]
    TrainingDataSourceId: NotRequired[str]
    CreatedByIamUser: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    LastUpdatedAt: NotRequired[datetime]
    Name: NotRequired[str]
    Status: NotRequired[EntityStatusType]
    SizeInBytes: NotRequired[int]
    EndpointInfo: NotRequired[RealtimeEndpointInfoTypeDef]
    TrainingParameters: NotRequired[Dict[str, str]]
    InputDataLocationS3: NotRequired[str]
    Algorithm: NotRequired[Literal["sgd"]]
    MLModelType: NotRequired[MLModelTypeType]
    ScoreThreshold: NotRequired[float]
    ScoreThresholdLastUpdatedAt: NotRequired[datetime]
    Message: NotRequired[str]
    ComputeTime: NotRequired[int]
    FinishedAt: NotRequired[datetime]
    StartedAt: NotRequired[datetime]

class DescribeBatchPredictionsInputBatchPredictionAvailableWaitTypeDef(TypedDict):
    FilterVariable: NotRequired[BatchPredictionFilterVariableType]
    EQ: NotRequired[str]
    GT: NotRequired[str]
    LT: NotRequired[str]
    GE: NotRequired[str]
    LE: NotRequired[str]
    NE: NotRequired[str]
    Prefix: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeDataSourcesInputDataSourceAvailableWaitTypeDef(TypedDict):
    FilterVariable: NotRequired[DataSourceFilterVariableType]
    EQ: NotRequired[str]
    GT: NotRequired[str]
    LT: NotRequired[str]
    GE: NotRequired[str]
    LE: NotRequired[str]
    NE: NotRequired[str]
    Prefix: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeEvaluationsInputEvaluationAvailableWaitTypeDef(TypedDict):
    FilterVariable: NotRequired[EvaluationFilterVariableType]
    EQ: NotRequired[str]
    GT: NotRequired[str]
    LT: NotRequired[str]
    GE: NotRequired[str]
    LE: NotRequired[str]
    NE: NotRequired[str]
    Prefix: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeMLModelsInputMLModelAvailableWaitTypeDef(TypedDict):
    FilterVariable: NotRequired[MLModelFilterVariableType]
    EQ: NotRequired[str]
    GT: NotRequired[str]
    LT: NotRequired[str]
    GE: NotRequired[str]
    LE: NotRequired[str]
    NE: NotRequired[str]
    Prefix: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeBatchPredictionsInputDescribeBatchPredictionsPaginateTypeDef(TypedDict):
    FilterVariable: NotRequired[BatchPredictionFilterVariableType]
    EQ: NotRequired[str]
    GT: NotRequired[str]
    LT: NotRequired[str]
    GE: NotRequired[str]
    LE: NotRequired[str]
    NE: NotRequired[str]
    Prefix: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeDataSourcesInputDescribeDataSourcesPaginateTypeDef(TypedDict):
    FilterVariable: NotRequired[DataSourceFilterVariableType]
    EQ: NotRequired[str]
    GT: NotRequired[str]
    LT: NotRequired[str]
    GE: NotRequired[str]
    LE: NotRequired[str]
    NE: NotRequired[str]
    Prefix: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeEvaluationsInputDescribeEvaluationsPaginateTypeDef(TypedDict):
    FilterVariable: NotRequired[EvaluationFilterVariableType]
    EQ: NotRequired[str]
    GT: NotRequired[str]
    LT: NotRequired[str]
    GE: NotRequired[str]
    LE: NotRequired[str]
    NE: NotRequired[str]
    Prefix: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeMLModelsInputDescribeMLModelsPaginateTypeDef(TypedDict):
    FilterVariable: NotRequired[MLModelFilterVariableType]
    EQ: NotRequired[str]
    GT: NotRequired[str]
    LT: NotRequired[str]
    GE: NotRequired[str]
    LE: NotRequired[str]
    NE: NotRequired[str]
    Prefix: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class EvaluationTypeDef(TypedDict):
    EvaluationId: NotRequired[str]
    MLModelId: NotRequired[str]
    EvaluationDataSourceId: NotRequired[str]
    InputDataLocationS3: NotRequired[str]
    CreatedByIamUser: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    LastUpdatedAt: NotRequired[datetime]
    Name: NotRequired[str]
    Status: NotRequired[EntityStatusType]
    PerformanceMetrics: NotRequired[PerformanceMetricsTypeDef]
    Message: NotRequired[str]
    ComputeTime: NotRequired[int]
    FinishedAt: NotRequired[datetime]
    StartedAt: NotRequired[datetime]

class GetEvaluationOutputTypeDef(TypedDict):
    EvaluationId: str
    MLModelId: str
    EvaluationDataSourceId: str
    InputDataLocationS3: str
    CreatedByIamUser: str
    CreatedAt: datetime
    LastUpdatedAt: datetime
    Name: str
    Status: EntityStatusType
    PerformanceMetrics: PerformanceMetricsTypeDef
    LogUri: str
    Message: str
    ComputeTime: int
    FinishedAt: datetime
    StartedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class PredictOutputTypeDef(TypedDict):
    Prediction: PredictionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class RDSDataSpecTypeDef(TypedDict):
    DatabaseInformation: RDSDatabaseTypeDef
    SelectSqlQuery: str
    DatabaseCredentials: RDSDatabaseCredentialsTypeDef
    S3StagingLocation: str
    ResourceRole: str
    ServiceRole: str
    SubnetId: str
    SecurityGroupIds: Sequence[str]
    DataRearrangement: NotRequired[str]
    DataSchema: NotRequired[str]
    DataSchemaUri: NotRequired[str]

class RDSMetadataTypeDef(TypedDict):
    Database: NotRequired[RDSDatabaseTypeDef]
    DatabaseUserName: NotRequired[str]
    SelectSqlQuery: NotRequired[str]
    ResourceRole: NotRequired[str]
    ServiceRole: NotRequired[str]
    DataPipelineId: NotRequired[str]

class RedshiftDataSpecTypeDef(TypedDict):
    DatabaseInformation: RedshiftDatabaseTypeDef
    SelectSqlQuery: str
    DatabaseCredentials: RedshiftDatabaseCredentialsTypeDef
    S3StagingLocation: str
    DataRearrangement: NotRequired[str]
    DataSchema: NotRequired[str]
    DataSchemaUri: NotRequired[str]

class RedshiftMetadataTypeDef(TypedDict):
    RedshiftDatabase: NotRequired[RedshiftDatabaseTypeDef]
    DatabaseUserName: NotRequired[str]
    SelectSqlQuery: NotRequired[str]

class DescribeMLModelsOutputTypeDef(TypedDict):
    Results: List[MLModelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeEvaluationsOutputTypeDef(TypedDict):
    Results: List[EvaluationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateDataSourceFromRDSInputRequestTypeDef(TypedDict):
    DataSourceId: str
    RDSData: RDSDataSpecTypeDef
    RoleARN: str
    DataSourceName: NotRequired[str]
    ComputeStatistics: NotRequired[bool]

class CreateDataSourceFromRedshiftInputRequestTypeDef(TypedDict):
    DataSourceId: str
    DataSpec: RedshiftDataSpecTypeDef
    RoleARN: str
    DataSourceName: NotRequired[str]
    ComputeStatistics: NotRequired[bool]

class DataSourceTypeDef(TypedDict):
    DataSourceId: NotRequired[str]
    DataLocationS3: NotRequired[str]
    DataRearrangement: NotRequired[str]
    CreatedByIamUser: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    LastUpdatedAt: NotRequired[datetime]
    DataSizeInBytes: NotRequired[int]
    NumberOfFiles: NotRequired[int]
    Name: NotRequired[str]
    Status: NotRequired[EntityStatusType]
    Message: NotRequired[str]
    RedshiftMetadata: NotRequired[RedshiftMetadataTypeDef]
    RDSMetadata: NotRequired[RDSMetadataTypeDef]
    RoleARN: NotRequired[str]
    ComputeStatistics: NotRequired[bool]
    ComputeTime: NotRequired[int]
    FinishedAt: NotRequired[datetime]
    StartedAt: NotRequired[datetime]

class GetDataSourceOutputTypeDef(TypedDict):
    DataSourceId: str
    DataLocationS3: str
    DataRearrangement: str
    CreatedByIamUser: str
    CreatedAt: datetime
    LastUpdatedAt: datetime
    DataSizeInBytes: int
    NumberOfFiles: int
    Name: str
    Status: EntityStatusType
    LogUri: str
    Message: str
    RedshiftMetadata: RedshiftMetadataTypeDef
    RDSMetadata: RDSMetadataTypeDef
    RoleARN: str
    ComputeStatistics: bool
    ComputeTime: int
    FinishedAt: datetime
    StartedAt: datetime
    DataSourceSchema: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeDataSourcesOutputTypeDef(TypedDict):
    Results: List[DataSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
