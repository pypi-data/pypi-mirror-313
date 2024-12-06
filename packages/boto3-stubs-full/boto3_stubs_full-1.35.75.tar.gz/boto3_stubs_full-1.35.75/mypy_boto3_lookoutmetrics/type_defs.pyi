"""
Type annotations for lookoutmetrics service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/type_defs/)

Usage::

    ```python
    from mypy_boto3_lookoutmetrics.type_defs import LambdaConfigurationTypeDef

    data: LambdaConfigurationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AggregationFunctionType,
    AlertStatusType,
    AlertTypeType,
    AnomalyDetectionTaskStatusType,
    AnomalyDetectorFailureTypeType,
    AnomalyDetectorStatusType,
    ConfidenceType,
    CSVFileCompressionType,
    DataQualityMetricTypeType,
    FrequencyType,
    JsonFileCompressionType,
    RelationshipTypeType,
    SnsFormatType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "ActionTypeDef",
    "ActivateAnomalyDetectorRequestRequestTypeDef",
    "AlertFiltersOutputTypeDef",
    "AlertFiltersTypeDef",
    "AlertSummaryTypeDef",
    "AlertTypeDef",
    "AnomalyDetectorConfigSummaryTypeDef",
    "AnomalyDetectorConfigTypeDef",
    "AnomalyDetectorDataQualityMetricTypeDef",
    "AnomalyDetectorSummaryTypeDef",
    "AnomalyGroupStatisticsTypeDef",
    "AnomalyGroupSummaryTypeDef",
    "AnomalyGroupTimeSeriesFeedbackTypeDef",
    "AnomalyGroupTimeSeriesTypeDef",
    "AnomalyGroupTypeDef",
    "AppFlowConfigTypeDef",
    "AthenaSourceConfigTypeDef",
    "AttributeValueTypeDef",
    "AutoDetectionMetricSourceTypeDef",
    "AutoDetectionS3SourceConfigTypeDef",
    "BackTestAnomalyDetectorRequestRequestTypeDef",
    "BackTestConfigurationTypeDef",
    "CloudWatchConfigTypeDef",
    "ContributionMatrixTypeDef",
    "CreateAlertRequestRequestTypeDef",
    "CreateAlertResponseTypeDef",
    "CreateAnomalyDetectorRequestRequestTypeDef",
    "CreateAnomalyDetectorResponseTypeDef",
    "CreateMetricSetRequestRequestTypeDef",
    "CreateMetricSetResponseTypeDef",
    "CsvFormatDescriptorOutputTypeDef",
    "CsvFormatDescriptorTypeDef",
    "CsvFormatDescriptorUnionTypeDef",
    "DataQualityMetricTypeDef",
    "DeactivateAnomalyDetectorRequestRequestTypeDef",
    "DeleteAlertRequestRequestTypeDef",
    "DeleteAnomalyDetectorRequestRequestTypeDef",
    "DescribeAlertRequestRequestTypeDef",
    "DescribeAlertResponseTypeDef",
    "DescribeAnomalyDetectionExecutionsRequestRequestTypeDef",
    "DescribeAnomalyDetectionExecutionsResponseTypeDef",
    "DescribeAnomalyDetectorRequestRequestTypeDef",
    "DescribeAnomalyDetectorResponseTypeDef",
    "DescribeMetricSetRequestRequestTypeDef",
    "DescribeMetricSetResponseTypeDef",
    "DetectMetricSetConfigRequestRequestTypeDef",
    "DetectMetricSetConfigResponseTypeDef",
    "DetectedCsvFormatDescriptorTypeDef",
    "DetectedFieldTypeDef",
    "DetectedFileFormatDescriptorTypeDef",
    "DetectedJsonFormatDescriptorTypeDef",
    "DetectedMetricSetConfigTypeDef",
    "DetectedMetricSourceTypeDef",
    "DetectedS3SourceConfigTypeDef",
    "DimensionContributionTypeDef",
    "DimensionFilterOutputTypeDef",
    "DimensionFilterTypeDef",
    "DimensionFilterUnionTypeDef",
    "DimensionNameValueTypeDef",
    "DimensionValueContributionTypeDef",
    "ExecutionStatusTypeDef",
    "FileFormatDescriptorOutputTypeDef",
    "FileFormatDescriptorTypeDef",
    "FileFormatDescriptorUnionTypeDef",
    "FilterTypeDef",
    "GetAnomalyGroupRequestRequestTypeDef",
    "GetAnomalyGroupResponseTypeDef",
    "GetDataQualityMetricsRequestRequestTypeDef",
    "GetDataQualityMetricsResponseTypeDef",
    "GetFeedbackRequestRequestTypeDef",
    "GetFeedbackResponseTypeDef",
    "GetSampleDataRequestRequestTypeDef",
    "GetSampleDataResponseTypeDef",
    "InterMetricImpactDetailsTypeDef",
    "ItemizedMetricStatsTypeDef",
    "JsonFormatDescriptorTypeDef",
    "LambdaConfigurationTypeDef",
    "ListAlertsRequestRequestTypeDef",
    "ListAlertsResponseTypeDef",
    "ListAnomalyDetectorsRequestRequestTypeDef",
    "ListAnomalyDetectorsResponseTypeDef",
    "ListAnomalyGroupRelatedMetricsRequestRequestTypeDef",
    "ListAnomalyGroupRelatedMetricsResponseTypeDef",
    "ListAnomalyGroupSummariesRequestRequestTypeDef",
    "ListAnomalyGroupSummariesResponseTypeDef",
    "ListAnomalyGroupTimeSeriesRequestRequestTypeDef",
    "ListAnomalyGroupTimeSeriesResponseTypeDef",
    "ListMetricSetsRequestRequestTypeDef",
    "ListMetricSetsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MetricLevelImpactTypeDef",
    "MetricSetDataQualityMetricTypeDef",
    "MetricSetDimensionFilterOutputTypeDef",
    "MetricSetDimensionFilterTypeDef",
    "MetricSetDimensionFilterUnionTypeDef",
    "MetricSetSummaryTypeDef",
    "MetricSourceOutputTypeDef",
    "MetricSourceTypeDef",
    "MetricTypeDef",
    "PutFeedbackRequestRequestTypeDef",
    "RDSSourceConfigOutputTypeDef",
    "RDSSourceConfigTypeDef",
    "RDSSourceConfigUnionTypeDef",
    "RedshiftSourceConfigOutputTypeDef",
    "RedshiftSourceConfigTypeDef",
    "RedshiftSourceConfigUnionTypeDef",
    "ResponseMetadataTypeDef",
    "S3SourceConfigOutputTypeDef",
    "S3SourceConfigTypeDef",
    "S3SourceConfigUnionTypeDef",
    "SNSConfigurationTypeDef",
    "SampleDataS3SourceConfigTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimeSeriesFeedbackTypeDef",
    "TimeSeriesTypeDef",
    "TimestampColumnTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAlertRequestRequestTypeDef",
    "UpdateAlertResponseTypeDef",
    "UpdateAnomalyDetectorRequestRequestTypeDef",
    "UpdateAnomalyDetectorResponseTypeDef",
    "UpdateMetricSetRequestRequestTypeDef",
    "UpdateMetricSetResponseTypeDef",
    "VpcConfigurationOutputTypeDef",
    "VpcConfigurationTypeDef",
    "VpcConfigurationUnionTypeDef",
)

class LambdaConfigurationTypeDef(TypedDict):
    RoleArn: str
    LambdaArn: str

class SNSConfigurationTypeDef(TypedDict):
    RoleArn: str
    SnsTopicArn: str
    SnsFormat: NotRequired[SnsFormatType]

class ActivateAnomalyDetectorRequestRequestTypeDef(TypedDict):
    AnomalyDetectorArn: str

class DimensionFilterOutputTypeDef(TypedDict):
    DimensionName: NotRequired[str]
    DimensionValueList: NotRequired[List[str]]

class AlertSummaryTypeDef(TypedDict):
    AlertArn: NotRequired[str]
    AnomalyDetectorArn: NotRequired[str]
    AlertName: NotRequired[str]
    AlertSensitivityThreshold: NotRequired[int]
    AlertType: NotRequired[AlertTypeType]
    AlertStatus: NotRequired[AlertStatusType]
    LastModificationTime: NotRequired[datetime]
    CreationTime: NotRequired[datetime]
    Tags: NotRequired[Dict[str, str]]

class AnomalyDetectorConfigSummaryTypeDef(TypedDict):
    AnomalyDetectorFrequency: NotRequired[FrequencyType]

class AnomalyDetectorConfigTypeDef(TypedDict):
    AnomalyDetectorFrequency: NotRequired[FrequencyType]

class AnomalyDetectorSummaryTypeDef(TypedDict):
    AnomalyDetectorArn: NotRequired[str]
    AnomalyDetectorName: NotRequired[str]
    AnomalyDetectorDescription: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModificationTime: NotRequired[datetime]
    Status: NotRequired[AnomalyDetectorStatusType]
    Tags: NotRequired[Dict[str, str]]

class ItemizedMetricStatsTypeDef(TypedDict):
    MetricName: NotRequired[str]
    OccurrenceCount: NotRequired[int]

class AnomalyGroupSummaryTypeDef(TypedDict):
    StartTime: NotRequired[str]
    EndTime: NotRequired[str]
    AnomalyGroupId: NotRequired[str]
    AnomalyGroupScore: NotRequired[float]
    PrimaryMetricName: NotRequired[str]

class AnomalyGroupTimeSeriesFeedbackTypeDef(TypedDict):
    AnomalyGroupId: str
    TimeSeriesId: str
    IsAnomaly: bool

class AnomalyGroupTimeSeriesTypeDef(TypedDict):
    AnomalyGroupId: str
    TimeSeriesId: NotRequired[str]

class AppFlowConfigTypeDef(TypedDict):
    RoleArn: NotRequired[str]
    FlowName: NotRequired[str]

class BackTestConfigurationTypeDef(TypedDict):
    RunBackTestMode: bool

class AttributeValueTypeDef(TypedDict):
    S: NotRequired[str]
    N: NotRequired[str]
    B: NotRequired[str]
    SS: NotRequired[List[str]]
    NS: NotRequired[List[str]]
    BS: NotRequired[List[str]]

class AutoDetectionS3SourceConfigTypeDef(TypedDict):
    TemplatedPathList: NotRequired[Sequence[str]]
    HistoricalDataPathList: NotRequired[Sequence[str]]

class BackTestAnomalyDetectorRequestRequestTypeDef(TypedDict):
    AnomalyDetectorArn: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class MetricTypeDef(TypedDict):
    MetricName: str
    AggregationFunction: AggregationFunctionType
    Namespace: NotRequired[str]

class TimestampColumnTypeDef(TypedDict):
    ColumnName: NotRequired[str]
    ColumnFormat: NotRequired[str]

class CsvFormatDescriptorOutputTypeDef(TypedDict):
    FileCompression: NotRequired[CSVFileCompressionType]
    Charset: NotRequired[str]
    ContainsHeader: NotRequired[bool]
    Delimiter: NotRequired[str]
    HeaderList: NotRequired[List[str]]
    QuoteSymbol: NotRequired[str]

class CsvFormatDescriptorTypeDef(TypedDict):
    FileCompression: NotRequired[CSVFileCompressionType]
    Charset: NotRequired[str]
    ContainsHeader: NotRequired[bool]
    Delimiter: NotRequired[str]
    HeaderList: NotRequired[Sequence[str]]
    QuoteSymbol: NotRequired[str]

class DataQualityMetricTypeDef(TypedDict):
    MetricType: NotRequired[DataQualityMetricTypeType]
    MetricDescription: NotRequired[str]
    RelatedColumnName: NotRequired[str]
    MetricValue: NotRequired[float]

class DeactivateAnomalyDetectorRequestRequestTypeDef(TypedDict):
    AnomalyDetectorArn: str

class DeleteAlertRequestRequestTypeDef(TypedDict):
    AlertArn: str

class DeleteAnomalyDetectorRequestRequestTypeDef(TypedDict):
    AnomalyDetectorArn: str

class DescribeAlertRequestRequestTypeDef(TypedDict):
    AlertArn: str

class DescribeAnomalyDetectionExecutionsRequestRequestTypeDef(TypedDict):
    AnomalyDetectorArn: str
    Timestamp: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ExecutionStatusTypeDef(TypedDict):
    Timestamp: NotRequired[str]
    Status: NotRequired[AnomalyDetectionTaskStatusType]
    FailureReason: NotRequired[str]

class DescribeAnomalyDetectorRequestRequestTypeDef(TypedDict):
    AnomalyDetectorArn: str

class DescribeMetricSetRequestRequestTypeDef(TypedDict):
    MetricSetArn: str

class DimensionValueContributionTypeDef(TypedDict):
    DimensionValue: NotRequired[str]
    ContributionScore: NotRequired[float]

class DimensionFilterTypeDef(TypedDict):
    DimensionName: NotRequired[str]
    DimensionValueList: NotRequired[Sequence[str]]

class DimensionNameValueTypeDef(TypedDict):
    DimensionName: str
    DimensionValue: str

class JsonFormatDescriptorTypeDef(TypedDict):
    FileCompression: NotRequired[JsonFileCompressionType]
    Charset: NotRequired[str]

class FilterTypeDef(TypedDict):
    DimensionValue: NotRequired[str]
    FilterOperation: NotRequired[Literal["EQUALS"]]

class GetAnomalyGroupRequestRequestTypeDef(TypedDict):
    AnomalyGroupId: str
    AnomalyDetectorArn: str

class GetDataQualityMetricsRequestRequestTypeDef(TypedDict):
    AnomalyDetectorArn: str
    MetricSetArn: NotRequired[str]

class TimeSeriesFeedbackTypeDef(TypedDict):
    TimeSeriesId: NotRequired[str]
    IsAnomaly: NotRequired[bool]

class InterMetricImpactDetailsTypeDef(TypedDict):
    MetricName: NotRequired[str]
    AnomalyGroupId: NotRequired[str]
    RelationshipType: NotRequired[RelationshipTypeType]
    ContributionPercentage: NotRequired[float]

class ListAlertsRequestRequestTypeDef(TypedDict):
    AnomalyDetectorArn: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListAnomalyDetectorsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListAnomalyGroupRelatedMetricsRequestRequestTypeDef(TypedDict):
    AnomalyDetectorArn: str
    AnomalyGroupId: str
    RelationshipTypeFilter: NotRequired[RelationshipTypeType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListAnomalyGroupSummariesRequestRequestTypeDef(TypedDict):
    AnomalyDetectorArn: str
    SensitivityThreshold: int
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListAnomalyGroupTimeSeriesRequestRequestTypeDef(TypedDict):
    AnomalyDetectorArn: str
    AnomalyGroupId: str
    MetricName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListMetricSetsRequestRequestTypeDef(TypedDict):
    AnomalyDetectorArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class MetricSetSummaryTypeDef(TypedDict):
    MetricSetArn: NotRequired[str]
    AnomalyDetectorArn: NotRequired[str]
    MetricSetDescription: NotRequired[str]
    MetricSetName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModificationTime: NotRequired[datetime]
    Tags: NotRequired[Dict[str, str]]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class VpcConfigurationOutputTypeDef(TypedDict):
    SubnetIdList: List[str]
    SecurityGroupIdList: List[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class VpcConfigurationTypeDef(TypedDict):
    SubnetIdList: Sequence[str]
    SecurityGroupIdList: Sequence[str]

class ActionTypeDef(TypedDict):
    SNSConfiguration: NotRequired[SNSConfigurationTypeDef]
    LambdaConfiguration: NotRequired[LambdaConfigurationTypeDef]

class AlertFiltersOutputTypeDef(TypedDict):
    MetricList: NotRequired[List[str]]
    DimensionFilterList: NotRequired[List[DimensionFilterOutputTypeDef]]

class CreateAnomalyDetectorRequestRequestTypeDef(TypedDict):
    AnomalyDetectorName: str
    AnomalyDetectorConfig: AnomalyDetectorConfigTypeDef
    AnomalyDetectorDescription: NotRequired[str]
    KmsKeyArn: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class UpdateAnomalyDetectorRequestRequestTypeDef(TypedDict):
    AnomalyDetectorArn: str
    KmsKeyArn: NotRequired[str]
    AnomalyDetectorDescription: NotRequired[str]
    AnomalyDetectorConfig: NotRequired[AnomalyDetectorConfigTypeDef]

class AnomalyGroupStatisticsTypeDef(TypedDict):
    EvaluationStartDate: NotRequired[str]
    TotalCount: NotRequired[int]
    ItemizedMetricStatsList: NotRequired[List[ItemizedMetricStatsTypeDef]]

class PutFeedbackRequestRequestTypeDef(TypedDict):
    AnomalyDetectorArn: str
    AnomalyGroupTimeSeriesFeedback: AnomalyGroupTimeSeriesFeedbackTypeDef

class GetFeedbackRequestRequestTypeDef(TypedDict):
    AnomalyDetectorArn: str
    AnomalyGroupTimeSeriesFeedback: AnomalyGroupTimeSeriesTypeDef
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class AthenaSourceConfigTypeDef(TypedDict):
    RoleArn: NotRequired[str]
    DatabaseName: NotRequired[str]
    DataCatalog: NotRequired[str]
    TableName: NotRequired[str]
    WorkGroupName: NotRequired[str]
    S3ResultsPath: NotRequired[str]
    BackTestConfiguration: NotRequired[BackTestConfigurationTypeDef]

class CloudWatchConfigTypeDef(TypedDict):
    RoleArn: NotRequired[str]
    BackTestConfiguration: NotRequired[BackTestConfigurationTypeDef]

class DetectedFieldTypeDef(TypedDict):
    Value: NotRequired[AttributeValueTypeDef]
    Confidence: NotRequired[ConfidenceType]
    Message: NotRequired[str]

class AutoDetectionMetricSourceTypeDef(TypedDict):
    S3SourceConfig: NotRequired[AutoDetectionS3SourceConfigTypeDef]

class CreateAlertResponseTypeDef(TypedDict):
    AlertArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAnomalyDetectorResponseTypeDef(TypedDict):
    AnomalyDetectorArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMetricSetResponseTypeDef(TypedDict):
    MetricSetArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAnomalyDetectorResponseTypeDef(TypedDict):
    AnomalyDetectorArn: str
    AnomalyDetectorName: str
    AnomalyDetectorDescription: str
    AnomalyDetectorConfig: AnomalyDetectorConfigSummaryTypeDef
    CreationTime: datetime
    LastModificationTime: datetime
    Status: AnomalyDetectorStatusType
    FailureReason: str
    KmsKeyArn: str
    FailureType: AnomalyDetectorFailureTypeType
    ResponseMetadata: ResponseMetadataTypeDef

class GetSampleDataResponseTypeDef(TypedDict):
    HeaderValues: List[str]
    SampleRows: List[List[str]]
    ResponseMetadata: ResponseMetadataTypeDef

class ListAlertsResponseTypeDef(TypedDict):
    AlertSummaryList: List[AlertSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAnomalyDetectorsResponseTypeDef(TypedDict):
    AnomalyDetectorSummaryList: List[AnomalyDetectorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAlertResponseTypeDef(TypedDict):
    AlertArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAnomalyDetectorResponseTypeDef(TypedDict):
    AnomalyDetectorArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateMetricSetResponseTypeDef(TypedDict):
    MetricSetArn: str
    ResponseMetadata: ResponseMetadataTypeDef

CsvFormatDescriptorUnionTypeDef = Union[
    CsvFormatDescriptorTypeDef, CsvFormatDescriptorOutputTypeDef
]

class MetricSetDataQualityMetricTypeDef(TypedDict):
    MetricSetArn: NotRequired[str]
    DataQualityMetricList: NotRequired[List[DataQualityMetricTypeDef]]

class DescribeAnomalyDetectionExecutionsResponseTypeDef(TypedDict):
    ExecutionList: List[ExecutionStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DimensionContributionTypeDef(TypedDict):
    DimensionName: NotRequired[str]
    DimensionValueContributionList: NotRequired[List[DimensionValueContributionTypeDef]]

DimensionFilterUnionTypeDef = Union[DimensionFilterTypeDef, DimensionFilterOutputTypeDef]

class TimeSeriesTypeDef(TypedDict):
    TimeSeriesId: str
    DimensionList: List[DimensionNameValueTypeDef]
    MetricValueList: List[float]

class FileFormatDescriptorOutputTypeDef(TypedDict):
    CsvFormatDescriptor: NotRequired[CsvFormatDescriptorOutputTypeDef]
    JsonFormatDescriptor: NotRequired[JsonFormatDescriptorTypeDef]

class MetricSetDimensionFilterOutputTypeDef(TypedDict):
    Name: NotRequired[str]
    FilterList: NotRequired[List[FilterTypeDef]]

class MetricSetDimensionFilterTypeDef(TypedDict):
    Name: NotRequired[str]
    FilterList: NotRequired[Sequence[FilterTypeDef]]

class GetFeedbackResponseTypeDef(TypedDict):
    AnomalyGroupTimeSeriesFeedback: List[TimeSeriesFeedbackTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAnomalyGroupRelatedMetricsResponseTypeDef(TypedDict):
    InterMetricImpactList: List[InterMetricImpactDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListMetricSetsResponseTypeDef(TypedDict):
    MetricSetSummaryList: List[MetricSetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class RDSSourceConfigOutputTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    DatabaseHost: NotRequired[str]
    DatabasePort: NotRequired[int]
    SecretManagerArn: NotRequired[str]
    DatabaseName: NotRequired[str]
    TableName: NotRequired[str]
    RoleArn: NotRequired[str]
    VpcConfiguration: NotRequired[VpcConfigurationOutputTypeDef]

class RedshiftSourceConfigOutputTypeDef(TypedDict):
    ClusterIdentifier: NotRequired[str]
    DatabaseHost: NotRequired[str]
    DatabasePort: NotRequired[int]
    SecretManagerArn: NotRequired[str]
    DatabaseName: NotRequired[str]
    TableName: NotRequired[str]
    RoleArn: NotRequired[str]
    VpcConfiguration: NotRequired[VpcConfigurationOutputTypeDef]

VpcConfigurationUnionTypeDef = Union[VpcConfigurationTypeDef, VpcConfigurationOutputTypeDef]

class AlertTypeDef(TypedDict):
    Action: NotRequired[ActionTypeDef]
    AlertDescription: NotRequired[str]
    AlertArn: NotRequired[str]
    AnomalyDetectorArn: NotRequired[str]
    AlertName: NotRequired[str]
    AlertSensitivityThreshold: NotRequired[int]
    AlertType: NotRequired[AlertTypeType]
    AlertStatus: NotRequired[AlertStatusType]
    LastModificationTime: NotRequired[datetime]
    CreationTime: NotRequired[datetime]
    AlertFilters: NotRequired[AlertFiltersOutputTypeDef]

class ListAnomalyGroupSummariesResponseTypeDef(TypedDict):
    AnomalyGroupSummaryList: List[AnomalyGroupSummaryTypeDef]
    AnomalyGroupStatistics: AnomalyGroupStatisticsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DetectedCsvFormatDescriptorTypeDef(TypedDict):
    FileCompression: NotRequired[DetectedFieldTypeDef]
    Charset: NotRequired[DetectedFieldTypeDef]
    ContainsHeader: NotRequired[DetectedFieldTypeDef]
    Delimiter: NotRequired[DetectedFieldTypeDef]
    HeaderList: NotRequired[DetectedFieldTypeDef]
    QuoteSymbol: NotRequired[DetectedFieldTypeDef]

class DetectedJsonFormatDescriptorTypeDef(TypedDict):
    FileCompression: NotRequired[DetectedFieldTypeDef]
    Charset: NotRequired[DetectedFieldTypeDef]

class DetectMetricSetConfigRequestRequestTypeDef(TypedDict):
    AnomalyDetectorArn: str
    AutoDetectionMetricSource: AutoDetectionMetricSourceTypeDef

class FileFormatDescriptorTypeDef(TypedDict):
    CsvFormatDescriptor: NotRequired[CsvFormatDescriptorUnionTypeDef]
    JsonFormatDescriptor: NotRequired[JsonFormatDescriptorTypeDef]

class AnomalyDetectorDataQualityMetricTypeDef(TypedDict):
    StartTimestamp: NotRequired[datetime]
    MetricSetDataQualityMetricList: NotRequired[List[MetricSetDataQualityMetricTypeDef]]

class ContributionMatrixTypeDef(TypedDict):
    DimensionContributionList: NotRequired[List[DimensionContributionTypeDef]]

class AlertFiltersTypeDef(TypedDict):
    MetricList: NotRequired[Sequence[str]]
    DimensionFilterList: NotRequired[Sequence[DimensionFilterUnionTypeDef]]

class ListAnomalyGroupTimeSeriesResponseTypeDef(TypedDict):
    AnomalyGroupId: str
    MetricName: str
    TimestampList: List[str]
    TimeSeriesList: List[TimeSeriesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class S3SourceConfigOutputTypeDef(TypedDict):
    RoleArn: NotRequired[str]
    TemplatedPathList: NotRequired[List[str]]
    HistoricalDataPathList: NotRequired[List[str]]
    FileFormatDescriptor: NotRequired[FileFormatDescriptorOutputTypeDef]

MetricSetDimensionFilterUnionTypeDef = Union[
    MetricSetDimensionFilterTypeDef, MetricSetDimensionFilterOutputTypeDef
]

class RDSSourceConfigTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    DatabaseHost: NotRequired[str]
    DatabasePort: NotRequired[int]
    SecretManagerArn: NotRequired[str]
    DatabaseName: NotRequired[str]
    TableName: NotRequired[str]
    RoleArn: NotRequired[str]
    VpcConfiguration: NotRequired[VpcConfigurationUnionTypeDef]

class RedshiftSourceConfigTypeDef(TypedDict):
    ClusterIdentifier: NotRequired[str]
    DatabaseHost: NotRequired[str]
    DatabasePort: NotRequired[int]
    SecretManagerArn: NotRequired[str]
    DatabaseName: NotRequired[str]
    TableName: NotRequired[str]
    RoleArn: NotRequired[str]
    VpcConfiguration: NotRequired[VpcConfigurationUnionTypeDef]

class DescribeAlertResponseTypeDef(TypedDict):
    Alert: AlertTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DetectedFileFormatDescriptorTypeDef(TypedDict):
    CsvFormatDescriptor: NotRequired[DetectedCsvFormatDescriptorTypeDef]
    JsonFormatDescriptor: NotRequired[DetectedJsonFormatDescriptorTypeDef]

FileFormatDescriptorUnionTypeDef = Union[
    FileFormatDescriptorTypeDef, FileFormatDescriptorOutputTypeDef
]

class GetDataQualityMetricsResponseTypeDef(TypedDict):
    AnomalyDetectorDataQualityMetricList: List[AnomalyDetectorDataQualityMetricTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class MetricLevelImpactTypeDef(TypedDict):
    MetricName: NotRequired[str]
    NumTimeSeries: NotRequired[int]
    ContributionMatrix: NotRequired[ContributionMatrixTypeDef]

class CreateAlertRequestRequestTypeDef(TypedDict):
    AlertName: str
    AnomalyDetectorArn: str
    Action: ActionTypeDef
    AlertSensitivityThreshold: NotRequired[int]
    AlertDescription: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    AlertFilters: NotRequired[AlertFiltersTypeDef]

class UpdateAlertRequestRequestTypeDef(TypedDict):
    AlertArn: str
    AlertDescription: NotRequired[str]
    AlertSensitivityThreshold: NotRequired[int]
    Action: NotRequired[ActionTypeDef]
    AlertFilters: NotRequired[AlertFiltersTypeDef]

class MetricSourceOutputTypeDef(TypedDict):
    S3SourceConfig: NotRequired[S3SourceConfigOutputTypeDef]
    AppFlowConfig: NotRequired[AppFlowConfigTypeDef]
    CloudWatchConfig: NotRequired[CloudWatchConfigTypeDef]
    RDSSourceConfig: NotRequired[RDSSourceConfigOutputTypeDef]
    RedshiftSourceConfig: NotRequired[RedshiftSourceConfigOutputTypeDef]
    AthenaSourceConfig: NotRequired[AthenaSourceConfigTypeDef]

RDSSourceConfigUnionTypeDef = Union[RDSSourceConfigTypeDef, RDSSourceConfigOutputTypeDef]
RedshiftSourceConfigUnionTypeDef = Union[
    RedshiftSourceConfigTypeDef, RedshiftSourceConfigOutputTypeDef
]

class DetectedS3SourceConfigTypeDef(TypedDict):
    FileFormatDescriptor: NotRequired[DetectedFileFormatDescriptorTypeDef]

class S3SourceConfigTypeDef(TypedDict):
    RoleArn: NotRequired[str]
    TemplatedPathList: NotRequired[Sequence[str]]
    HistoricalDataPathList: NotRequired[Sequence[str]]
    FileFormatDescriptor: NotRequired[FileFormatDescriptorUnionTypeDef]

class SampleDataS3SourceConfigTypeDef(TypedDict):
    RoleArn: str
    FileFormatDescriptor: FileFormatDescriptorUnionTypeDef
    TemplatedPathList: NotRequired[Sequence[str]]
    HistoricalDataPathList: NotRequired[Sequence[str]]

class AnomalyGroupTypeDef(TypedDict):
    StartTime: NotRequired[str]
    EndTime: NotRequired[str]
    AnomalyGroupId: NotRequired[str]
    AnomalyGroupScore: NotRequired[float]
    PrimaryMetricName: NotRequired[str]
    MetricLevelImpactList: NotRequired[List[MetricLevelImpactTypeDef]]

class DescribeMetricSetResponseTypeDef(TypedDict):
    MetricSetArn: str
    AnomalyDetectorArn: str
    MetricSetName: str
    MetricSetDescription: str
    CreationTime: datetime
    LastModificationTime: datetime
    Offset: int
    MetricList: List[MetricTypeDef]
    TimestampColumn: TimestampColumnTypeDef
    DimensionList: List[str]
    MetricSetFrequency: FrequencyType
    Timezone: str
    MetricSource: MetricSourceOutputTypeDef
    DimensionFilterList: List[MetricSetDimensionFilterOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DetectedMetricSourceTypeDef(TypedDict):
    S3SourceConfig: NotRequired[DetectedS3SourceConfigTypeDef]

S3SourceConfigUnionTypeDef = Union[S3SourceConfigTypeDef, S3SourceConfigOutputTypeDef]

class GetSampleDataRequestRequestTypeDef(TypedDict):
    S3SourceConfig: NotRequired[SampleDataS3SourceConfigTypeDef]

class GetAnomalyGroupResponseTypeDef(TypedDict):
    AnomalyGroup: AnomalyGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DetectedMetricSetConfigTypeDef(TypedDict):
    Offset: NotRequired[DetectedFieldTypeDef]
    MetricSetFrequency: NotRequired[DetectedFieldTypeDef]
    MetricSource: NotRequired[DetectedMetricSourceTypeDef]

class MetricSourceTypeDef(TypedDict):
    S3SourceConfig: NotRequired[S3SourceConfigUnionTypeDef]
    AppFlowConfig: NotRequired[AppFlowConfigTypeDef]
    CloudWatchConfig: NotRequired[CloudWatchConfigTypeDef]
    RDSSourceConfig: NotRequired[RDSSourceConfigUnionTypeDef]
    RedshiftSourceConfig: NotRequired[RedshiftSourceConfigUnionTypeDef]
    AthenaSourceConfig: NotRequired[AthenaSourceConfigTypeDef]

class DetectMetricSetConfigResponseTypeDef(TypedDict):
    DetectedMetricSetConfig: DetectedMetricSetConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMetricSetRequestRequestTypeDef(TypedDict):
    AnomalyDetectorArn: str
    MetricSetName: str
    MetricList: Sequence[MetricTypeDef]
    MetricSource: MetricSourceTypeDef
    MetricSetDescription: NotRequired[str]
    Offset: NotRequired[int]
    TimestampColumn: NotRequired[TimestampColumnTypeDef]
    DimensionList: NotRequired[Sequence[str]]
    MetricSetFrequency: NotRequired[FrequencyType]
    Timezone: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    DimensionFilterList: NotRequired[Sequence[MetricSetDimensionFilterUnionTypeDef]]

class UpdateMetricSetRequestRequestTypeDef(TypedDict):
    MetricSetArn: str
    MetricSetDescription: NotRequired[str]
    MetricList: NotRequired[Sequence[MetricTypeDef]]
    Offset: NotRequired[int]
    TimestampColumn: NotRequired[TimestampColumnTypeDef]
    DimensionList: NotRequired[Sequence[str]]
    MetricSetFrequency: NotRequired[FrequencyType]
    MetricSource: NotRequired[MetricSourceTypeDef]
    DimensionFilterList: NotRequired[Sequence[MetricSetDimensionFilterTypeDef]]
