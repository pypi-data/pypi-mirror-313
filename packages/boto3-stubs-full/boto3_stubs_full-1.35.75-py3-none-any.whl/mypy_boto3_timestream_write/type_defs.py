"""
Type annotations for timestream-write service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_write/type_defs/)

Usage::

    ```python
    from mypy_boto3_timestream_write.type_defs import BatchLoadProgressReportTypeDef

    data: BatchLoadProgressReportTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    BatchLoadStatusType,
    MeasureValueTypeType,
    PartitionKeyEnforcementLevelType,
    PartitionKeyTypeType,
    S3EncryptionOptionType,
    ScalarMeasureValueTypeType,
    TableStatusType,
    TimeUnitType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "BatchLoadProgressReportTypeDef",
    "BatchLoadTaskDescriptionTypeDef",
    "BatchLoadTaskTypeDef",
    "CreateBatchLoadTaskRequestRequestTypeDef",
    "CreateBatchLoadTaskResponseTypeDef",
    "CreateDatabaseRequestRequestTypeDef",
    "CreateDatabaseResponseTypeDef",
    "CreateTableRequestRequestTypeDef",
    "CreateTableResponseTypeDef",
    "CsvConfigurationTypeDef",
    "DataModelConfigurationOutputTypeDef",
    "DataModelConfigurationTypeDef",
    "DataModelOutputTypeDef",
    "DataModelS3ConfigurationTypeDef",
    "DataModelTypeDef",
    "DataModelUnionTypeDef",
    "DataSourceConfigurationTypeDef",
    "DataSourceS3ConfigurationTypeDef",
    "DatabaseTypeDef",
    "DeleteDatabaseRequestRequestTypeDef",
    "DeleteTableRequestRequestTypeDef",
    "DescribeBatchLoadTaskRequestRequestTypeDef",
    "DescribeBatchLoadTaskResponseTypeDef",
    "DescribeDatabaseRequestRequestTypeDef",
    "DescribeDatabaseResponseTypeDef",
    "DescribeEndpointsResponseTypeDef",
    "DescribeTableRequestRequestTypeDef",
    "DescribeTableResponseTypeDef",
    "DimensionMappingTypeDef",
    "DimensionTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EndpointTypeDef",
    "ListBatchLoadTasksRequestRequestTypeDef",
    "ListBatchLoadTasksResponseTypeDef",
    "ListDatabasesRequestRequestTypeDef",
    "ListDatabasesResponseTypeDef",
    "ListTablesRequestRequestTypeDef",
    "ListTablesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MagneticStoreRejectedDataLocationTypeDef",
    "MagneticStoreWritePropertiesTypeDef",
    "MeasureValueTypeDef",
    "MixedMeasureMappingOutputTypeDef",
    "MixedMeasureMappingTypeDef",
    "MixedMeasureMappingUnionTypeDef",
    "MultiMeasureAttributeMappingTypeDef",
    "MultiMeasureMappingsOutputTypeDef",
    "MultiMeasureMappingsTypeDef",
    "MultiMeasureMappingsUnionTypeDef",
    "PartitionKeyTypeDef",
    "RecordTypeDef",
    "RecordsIngestedTypeDef",
    "ReportConfigurationTypeDef",
    "ReportS3ConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "ResumeBatchLoadTaskRequestRequestTypeDef",
    "RetentionPropertiesTypeDef",
    "S3ConfigurationTypeDef",
    "SchemaOutputTypeDef",
    "SchemaTypeDef",
    "TableTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDatabaseRequestRequestTypeDef",
    "UpdateDatabaseResponseTypeDef",
    "UpdateTableRequestRequestTypeDef",
    "UpdateTableResponseTypeDef",
    "WriteRecordsRequestRequestTypeDef",
    "WriteRecordsResponseTypeDef",
)


class BatchLoadProgressReportTypeDef(TypedDict):
    RecordsProcessed: NotRequired[int]
    RecordsIngested: NotRequired[int]
    ParseFailures: NotRequired[int]
    RecordIngestionFailures: NotRequired[int]
    FileFailures: NotRequired[int]
    BytesMetered: NotRequired[int]


class BatchLoadTaskTypeDef(TypedDict):
    TaskId: NotRequired[str]
    TaskStatus: NotRequired[BatchLoadStatusType]
    DatabaseName: NotRequired[str]
    TableName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    ResumableUntil: NotRequired[datetime]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class DatabaseTypeDef(TypedDict):
    Arn: NotRequired[str]
    DatabaseName: NotRequired[str]
    TableCount: NotRequired[int]
    KmsKeyId: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]


class RetentionPropertiesTypeDef(TypedDict):
    MemoryStoreRetentionPeriodInHours: int
    MagneticStoreRetentionPeriodInDays: int


class CsvConfigurationTypeDef(TypedDict):
    ColumnSeparator: NotRequired[str]
    EscapeChar: NotRequired[str]
    QuoteChar: NotRequired[str]
    NullValue: NotRequired[str]
    TrimWhiteSpace: NotRequired[bool]


class DataModelS3ConfigurationTypeDef(TypedDict):
    BucketName: NotRequired[str]
    ObjectKey: NotRequired[str]


class DimensionMappingTypeDef(TypedDict):
    SourceColumn: NotRequired[str]
    DestinationColumn: NotRequired[str]


class DataSourceS3ConfigurationTypeDef(TypedDict):
    BucketName: str
    ObjectKeyPrefix: NotRequired[str]


class DeleteDatabaseRequestRequestTypeDef(TypedDict):
    DatabaseName: str


class DeleteTableRequestRequestTypeDef(TypedDict):
    DatabaseName: str
    TableName: str


class DescribeBatchLoadTaskRequestRequestTypeDef(TypedDict):
    TaskId: str


class DescribeDatabaseRequestRequestTypeDef(TypedDict):
    DatabaseName: str


class EndpointTypeDef(TypedDict):
    Address: str
    CachePeriodInMinutes: int


class DescribeTableRequestRequestTypeDef(TypedDict):
    DatabaseName: str
    TableName: str


class DimensionTypeDef(TypedDict):
    Name: str
    Value: str
    DimensionValueType: NotRequired[Literal["VARCHAR"]]


class ListBatchLoadTasksRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    TaskStatus: NotRequired[BatchLoadStatusType]


class ListDatabasesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTablesRequestRequestTypeDef(TypedDict):
    DatabaseName: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str


class S3ConfigurationTypeDef(TypedDict):
    BucketName: NotRequired[str]
    ObjectKeyPrefix: NotRequired[str]
    EncryptionOption: NotRequired[S3EncryptionOptionType]
    KmsKeyId: NotRequired[str]


MeasureValueTypeDef = TypedDict(
    "MeasureValueTypeDef",
    {
        "Name": str,
        "Value": str,
        "Type": MeasureValueTypeType,
    },
)


class MultiMeasureAttributeMappingTypeDef(TypedDict):
    SourceColumn: str
    TargetMultiMeasureAttributeName: NotRequired[str]
    MeasureValueType: NotRequired[ScalarMeasureValueTypeType]


PartitionKeyTypeDef = TypedDict(
    "PartitionKeyTypeDef",
    {
        "Type": PartitionKeyTypeType,
        "Name": NotRequired[str],
        "EnforcementInRecord": NotRequired[PartitionKeyEnforcementLevelType],
    },
)


class RecordsIngestedTypeDef(TypedDict):
    Total: NotRequired[int]
    MemoryStore: NotRequired[int]
    MagneticStore: NotRequired[int]


class ReportS3ConfigurationTypeDef(TypedDict):
    BucketName: str
    ObjectKeyPrefix: NotRequired[str]
    EncryptionOption: NotRequired[S3EncryptionOptionType]
    KmsKeyId: NotRequired[str]


class ResumeBatchLoadTaskRequestRequestTypeDef(TypedDict):
    TaskId: str


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


class UpdateDatabaseRequestRequestTypeDef(TypedDict):
    DatabaseName: str
    KmsKeyId: str


class CreateBatchLoadTaskResponseTypeDef(TypedDict):
    TaskId: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ListBatchLoadTasksResponseTypeDef(TypedDict):
    BatchLoadTasks: List[BatchLoadTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateDatabaseRequestRequestTypeDef(TypedDict):
    DatabaseName: str
    KmsKeyId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]


class CreateDatabaseResponseTypeDef(TypedDict):
    Database: DatabaseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDatabaseResponseTypeDef(TypedDict):
    Database: DatabaseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDatabasesResponseTypeDef(TypedDict):
    Databases: List[DatabaseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateDatabaseResponseTypeDef(TypedDict):
    Database: DatabaseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DataSourceConfigurationTypeDef(TypedDict):
    DataSourceS3Configuration: DataSourceS3ConfigurationTypeDef
    DataFormat: Literal["CSV"]
    CsvConfiguration: NotRequired[CsvConfigurationTypeDef]


class DescribeEndpointsResponseTypeDef(TypedDict):
    Endpoints: List[EndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class MagneticStoreRejectedDataLocationTypeDef(TypedDict):
    S3Configuration: NotRequired[S3ConfigurationTypeDef]


class RecordTypeDef(TypedDict):
    Dimensions: NotRequired[Sequence[DimensionTypeDef]]
    MeasureName: NotRequired[str]
    MeasureValue: NotRequired[str]
    MeasureValueType: NotRequired[MeasureValueTypeType]
    Time: NotRequired[str]
    TimeUnit: NotRequired[TimeUnitType]
    Version: NotRequired[int]
    MeasureValues: NotRequired[Sequence[MeasureValueTypeDef]]


class MixedMeasureMappingOutputTypeDef(TypedDict):
    MeasureValueType: MeasureValueTypeType
    MeasureName: NotRequired[str]
    SourceColumn: NotRequired[str]
    TargetMeasureName: NotRequired[str]
    MultiMeasureAttributeMappings: NotRequired[List[MultiMeasureAttributeMappingTypeDef]]


class MixedMeasureMappingTypeDef(TypedDict):
    MeasureValueType: MeasureValueTypeType
    MeasureName: NotRequired[str]
    SourceColumn: NotRequired[str]
    TargetMeasureName: NotRequired[str]
    MultiMeasureAttributeMappings: NotRequired[Sequence[MultiMeasureAttributeMappingTypeDef]]


class MultiMeasureMappingsOutputTypeDef(TypedDict):
    MultiMeasureAttributeMappings: List[MultiMeasureAttributeMappingTypeDef]
    TargetMultiMeasureName: NotRequired[str]


class MultiMeasureMappingsTypeDef(TypedDict):
    MultiMeasureAttributeMappings: Sequence[MultiMeasureAttributeMappingTypeDef]
    TargetMultiMeasureName: NotRequired[str]


class SchemaOutputTypeDef(TypedDict):
    CompositePartitionKey: NotRequired[List[PartitionKeyTypeDef]]


class SchemaTypeDef(TypedDict):
    CompositePartitionKey: NotRequired[Sequence[PartitionKeyTypeDef]]


class WriteRecordsResponseTypeDef(TypedDict):
    RecordsIngested: RecordsIngestedTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ReportConfigurationTypeDef(TypedDict):
    ReportS3Configuration: NotRequired[ReportS3ConfigurationTypeDef]


class MagneticStoreWritePropertiesTypeDef(TypedDict):
    EnableMagneticStoreWrites: bool
    MagneticStoreRejectedDataLocation: NotRequired[MagneticStoreRejectedDataLocationTypeDef]


class WriteRecordsRequestRequestTypeDef(TypedDict):
    DatabaseName: str
    TableName: str
    Records: Sequence[RecordTypeDef]
    CommonAttributes: NotRequired[RecordTypeDef]


MixedMeasureMappingUnionTypeDef = Union[
    MixedMeasureMappingTypeDef, MixedMeasureMappingOutputTypeDef
]


class DataModelOutputTypeDef(TypedDict):
    DimensionMappings: List[DimensionMappingTypeDef]
    TimeColumn: NotRequired[str]
    TimeUnit: NotRequired[TimeUnitType]
    MultiMeasureMappings: NotRequired[MultiMeasureMappingsOutputTypeDef]
    MixedMeasureMappings: NotRequired[List[MixedMeasureMappingOutputTypeDef]]
    MeasureNameColumn: NotRequired[str]


MultiMeasureMappingsUnionTypeDef = Union[
    MultiMeasureMappingsTypeDef, MultiMeasureMappingsOutputTypeDef
]


class CreateTableRequestRequestTypeDef(TypedDict):
    DatabaseName: str
    TableName: str
    RetentionProperties: NotRequired[RetentionPropertiesTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    MagneticStoreWriteProperties: NotRequired[MagneticStoreWritePropertiesTypeDef]
    Schema: NotRequired[SchemaTypeDef]


class TableTypeDef(TypedDict):
    Arn: NotRequired[str]
    TableName: NotRequired[str]
    DatabaseName: NotRequired[str]
    TableStatus: NotRequired[TableStatusType]
    RetentionProperties: NotRequired[RetentionPropertiesTypeDef]
    CreationTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    MagneticStoreWriteProperties: NotRequired[MagneticStoreWritePropertiesTypeDef]
    Schema: NotRequired[SchemaOutputTypeDef]


class UpdateTableRequestRequestTypeDef(TypedDict):
    DatabaseName: str
    TableName: str
    RetentionProperties: NotRequired[RetentionPropertiesTypeDef]
    MagneticStoreWriteProperties: NotRequired[MagneticStoreWritePropertiesTypeDef]
    Schema: NotRequired[SchemaTypeDef]


class DataModelConfigurationOutputTypeDef(TypedDict):
    DataModel: NotRequired[DataModelOutputTypeDef]
    DataModelS3Configuration: NotRequired[DataModelS3ConfigurationTypeDef]


class DataModelTypeDef(TypedDict):
    DimensionMappings: Sequence[DimensionMappingTypeDef]
    TimeColumn: NotRequired[str]
    TimeUnit: NotRequired[TimeUnitType]
    MultiMeasureMappings: NotRequired[MultiMeasureMappingsUnionTypeDef]
    MixedMeasureMappings: NotRequired[Sequence[MixedMeasureMappingUnionTypeDef]]
    MeasureNameColumn: NotRequired[str]


class CreateTableResponseTypeDef(TypedDict):
    Table: TableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTableResponseTypeDef(TypedDict):
    Table: TableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListTablesResponseTypeDef(TypedDict):
    Tables: List[TableTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateTableResponseTypeDef(TypedDict):
    Table: TableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class BatchLoadTaskDescriptionTypeDef(TypedDict):
    TaskId: NotRequired[str]
    ErrorMessage: NotRequired[str]
    DataSourceConfiguration: NotRequired[DataSourceConfigurationTypeDef]
    ProgressReport: NotRequired[BatchLoadProgressReportTypeDef]
    ReportConfiguration: NotRequired[ReportConfigurationTypeDef]
    DataModelConfiguration: NotRequired[DataModelConfigurationOutputTypeDef]
    TargetDatabaseName: NotRequired[str]
    TargetTableName: NotRequired[str]
    TaskStatus: NotRequired[BatchLoadStatusType]
    RecordVersion: NotRequired[int]
    CreationTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    ResumableUntil: NotRequired[datetime]


DataModelUnionTypeDef = Union[DataModelTypeDef, DataModelOutputTypeDef]


class DescribeBatchLoadTaskResponseTypeDef(TypedDict):
    BatchLoadTaskDescription: BatchLoadTaskDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DataModelConfigurationTypeDef(TypedDict):
    DataModel: NotRequired[DataModelUnionTypeDef]
    DataModelS3Configuration: NotRequired[DataModelS3ConfigurationTypeDef]


class CreateBatchLoadTaskRequestRequestTypeDef(TypedDict):
    DataSourceConfiguration: DataSourceConfigurationTypeDef
    ReportConfiguration: ReportConfigurationTypeDef
    TargetDatabaseName: str
    TargetTableName: str
    ClientToken: NotRequired[str]
    DataModelConfiguration: NotRequired[DataModelConfigurationTypeDef]
    RecordVersion: NotRequired[int]
