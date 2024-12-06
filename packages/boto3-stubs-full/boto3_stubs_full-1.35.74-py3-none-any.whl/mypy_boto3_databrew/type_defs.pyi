"""
Type annotations for databrew service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/type_defs/)

Usage::

    ```python
    from mypy_boto3_databrew.type_defs import AllowedStatisticsOutputTypeDef

    data: AllowedStatisticsOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AnalyticsModeType,
    CompressionFormatType,
    EncryptionModeType,
    InputFormatType,
    JobRunStateType,
    JobTypeType,
    LogSubscriptionType,
    OrderType,
    OutputFormatType,
    ParameterTypeType,
    SampleModeType,
    SampleTypeType,
    SessionStatusType,
    SourceType,
    ThresholdTypeType,
    ThresholdUnitType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AllowedStatisticsOutputTypeDef",
    "AllowedStatisticsTypeDef",
    "AllowedStatisticsUnionTypeDef",
    "BatchDeleteRecipeVersionRequestRequestTypeDef",
    "BatchDeleteRecipeVersionResponseTypeDef",
    "ColumnSelectorTypeDef",
    "ColumnStatisticsConfigurationOutputTypeDef",
    "ColumnStatisticsConfigurationTypeDef",
    "ColumnStatisticsConfigurationUnionTypeDef",
    "ConditionExpressionTypeDef",
    "CreateDatasetRequestRequestTypeDef",
    "CreateDatasetResponseTypeDef",
    "CreateProfileJobRequestRequestTypeDef",
    "CreateProfileJobResponseTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "CreateProjectResponseTypeDef",
    "CreateRecipeJobRequestRequestTypeDef",
    "CreateRecipeJobResponseTypeDef",
    "CreateRecipeRequestRequestTypeDef",
    "CreateRecipeResponseTypeDef",
    "CreateRulesetRequestRequestTypeDef",
    "CreateRulesetResponseTypeDef",
    "CreateScheduleRequestRequestTypeDef",
    "CreateScheduleResponseTypeDef",
    "CsvOptionsTypeDef",
    "CsvOutputOptionsTypeDef",
    "DataCatalogInputDefinitionTypeDef",
    "DataCatalogOutputTypeDef",
    "DatabaseInputDefinitionTypeDef",
    "DatabaseOutputTypeDef",
    "DatabaseTableOutputOptionsTypeDef",
    "DatasetParameterOutputTypeDef",
    "DatasetParameterTypeDef",
    "DatasetParameterUnionTypeDef",
    "DatasetTypeDef",
    "DatetimeOptionsTypeDef",
    "DeleteDatasetRequestRequestTypeDef",
    "DeleteDatasetResponseTypeDef",
    "DeleteJobRequestRequestTypeDef",
    "DeleteJobResponseTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DeleteProjectResponseTypeDef",
    "DeleteRecipeVersionRequestRequestTypeDef",
    "DeleteRecipeVersionResponseTypeDef",
    "DeleteRulesetRequestRequestTypeDef",
    "DeleteRulesetResponseTypeDef",
    "DeleteScheduleRequestRequestTypeDef",
    "DeleteScheduleResponseTypeDef",
    "DescribeDatasetRequestRequestTypeDef",
    "DescribeDatasetResponseTypeDef",
    "DescribeJobRequestRequestTypeDef",
    "DescribeJobResponseTypeDef",
    "DescribeJobRunRequestRequestTypeDef",
    "DescribeJobRunResponseTypeDef",
    "DescribeProjectRequestRequestTypeDef",
    "DescribeProjectResponseTypeDef",
    "DescribeRecipeRequestRequestTypeDef",
    "DescribeRecipeResponseTypeDef",
    "DescribeRulesetRequestRequestTypeDef",
    "DescribeRulesetResponseTypeDef",
    "DescribeScheduleRequestRequestTypeDef",
    "DescribeScheduleResponseTypeDef",
    "EntityDetectorConfigurationOutputTypeDef",
    "EntityDetectorConfigurationTypeDef",
    "EntityDetectorConfigurationUnionTypeDef",
    "ExcelOptionsOutputTypeDef",
    "ExcelOptionsTypeDef",
    "ExcelOptionsUnionTypeDef",
    "ExtraOutputTypeDef",
    "FilesLimitTypeDef",
    "FilterExpressionOutputTypeDef",
    "FilterExpressionTypeDef",
    "FilterExpressionUnionTypeDef",
    "FormatOptionsOutputTypeDef",
    "FormatOptionsTypeDef",
    "InputTypeDef",
    "JobRunTypeDef",
    "JobSampleTypeDef",
    "JobTypeDef",
    "JsonOptionsTypeDef",
    "ListDatasetsRequestListDatasetsPaginateTypeDef",
    "ListDatasetsRequestRequestTypeDef",
    "ListDatasetsResponseTypeDef",
    "ListJobRunsRequestListJobRunsPaginateTypeDef",
    "ListJobRunsRequestRequestTypeDef",
    "ListJobRunsResponseTypeDef",
    "ListJobsRequestListJobsPaginateTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListJobsResponseTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ListProjectsResponseTypeDef",
    "ListRecipeVersionsRequestListRecipeVersionsPaginateTypeDef",
    "ListRecipeVersionsRequestRequestTypeDef",
    "ListRecipeVersionsResponseTypeDef",
    "ListRecipesRequestListRecipesPaginateTypeDef",
    "ListRecipesRequestRequestTypeDef",
    "ListRecipesResponseTypeDef",
    "ListRulesetsRequestListRulesetsPaginateTypeDef",
    "ListRulesetsRequestRequestTypeDef",
    "ListRulesetsResponseTypeDef",
    "ListSchedulesRequestListSchedulesPaginateTypeDef",
    "ListSchedulesRequestRequestTypeDef",
    "ListSchedulesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MetadataTypeDef",
    "OutputFormatOptionsTypeDef",
    "OutputTypeDef",
    "PaginatorConfigTypeDef",
    "PathOptionsOutputTypeDef",
    "PathOptionsTypeDef",
    "ProfileConfigurationOutputTypeDef",
    "ProfileConfigurationTypeDef",
    "ProjectTypeDef",
    "PublishRecipeRequestRequestTypeDef",
    "PublishRecipeResponseTypeDef",
    "RecipeActionOutputTypeDef",
    "RecipeActionTypeDef",
    "RecipeActionUnionTypeDef",
    "RecipeReferenceTypeDef",
    "RecipeStepOutputTypeDef",
    "RecipeStepTypeDef",
    "RecipeStepUnionTypeDef",
    "RecipeTypeDef",
    "RecipeVersionErrorDetailTypeDef",
    "ResponseMetadataTypeDef",
    "RuleOutputTypeDef",
    "RuleTypeDef",
    "RuleUnionTypeDef",
    "RulesetItemTypeDef",
    "S3LocationTypeDef",
    "S3TableOutputOptionsTypeDef",
    "SampleTypeDef",
    "ScheduleTypeDef",
    "SendProjectSessionActionRequestRequestTypeDef",
    "SendProjectSessionActionResponseTypeDef",
    "StartJobRunRequestRequestTypeDef",
    "StartJobRunResponseTypeDef",
    "StartProjectSessionRequestRequestTypeDef",
    "StartProjectSessionResponseTypeDef",
    "StatisticOverrideOutputTypeDef",
    "StatisticOverrideTypeDef",
    "StatisticOverrideUnionTypeDef",
    "StatisticsConfigurationOutputTypeDef",
    "StatisticsConfigurationTypeDef",
    "StatisticsConfigurationUnionTypeDef",
    "StopJobRunRequestRequestTypeDef",
    "StopJobRunResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ThresholdTypeDef",
    "UnionTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDatasetRequestRequestTypeDef",
    "UpdateDatasetResponseTypeDef",
    "UpdateProfileJobRequestRequestTypeDef",
    "UpdateProfileJobResponseTypeDef",
    "UpdateProjectRequestRequestTypeDef",
    "UpdateProjectResponseTypeDef",
    "UpdateRecipeJobRequestRequestTypeDef",
    "UpdateRecipeJobResponseTypeDef",
    "UpdateRecipeRequestRequestTypeDef",
    "UpdateRecipeResponseTypeDef",
    "UpdateRulesetRequestRequestTypeDef",
    "UpdateRulesetResponseTypeDef",
    "UpdateScheduleRequestRequestTypeDef",
    "UpdateScheduleResponseTypeDef",
    "ValidationConfigurationTypeDef",
    "ViewFrameTypeDef",
)

class AllowedStatisticsOutputTypeDef(TypedDict):
    Statistics: List[str]

class AllowedStatisticsTypeDef(TypedDict):
    Statistics: Sequence[str]

class BatchDeleteRecipeVersionRequestRequestTypeDef(TypedDict):
    Name: str
    RecipeVersions: Sequence[str]

class RecipeVersionErrorDetailTypeDef(TypedDict):
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]
    RecipeVersion: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ColumnSelectorTypeDef(TypedDict):
    Regex: NotRequired[str]
    Name: NotRequired[str]

class ConditionExpressionTypeDef(TypedDict):
    Condition: str
    TargetColumn: str
    Value: NotRequired[str]

class JobSampleTypeDef(TypedDict):
    Mode: NotRequired[SampleModeType]
    Size: NotRequired[int]

class S3LocationTypeDef(TypedDict):
    Bucket: str
    Key: NotRequired[str]
    BucketOwner: NotRequired[str]

class ValidationConfigurationTypeDef(TypedDict):
    RulesetArn: str
    ValidationMode: NotRequired[Literal["CHECK_ALL"]]

SampleTypeDef = TypedDict(
    "SampleTypeDef",
    {
        "Type": SampleTypeType,
        "Size": NotRequired[int],
    },
)

class RecipeReferenceTypeDef(TypedDict):
    Name: str
    RecipeVersion: NotRequired[str]

class CreateScheduleRequestRequestTypeDef(TypedDict):
    CronExpression: str
    Name: str
    JobNames: NotRequired[Sequence[str]]
    Tags: NotRequired[Mapping[str, str]]

class CsvOptionsTypeDef(TypedDict):
    Delimiter: NotRequired[str]
    HeaderRow: NotRequired[bool]

class CsvOutputOptionsTypeDef(TypedDict):
    Delimiter: NotRequired[str]

class DatetimeOptionsTypeDef(TypedDict):
    Format: str
    TimezoneOffset: NotRequired[str]
    LocaleCode: NotRequired[str]

class FilterExpressionOutputTypeDef(TypedDict):
    Expression: str
    ValuesMap: Dict[str, str]

class DeleteDatasetRequestRequestTypeDef(TypedDict):
    Name: str

class DeleteJobRequestRequestTypeDef(TypedDict):
    Name: str

class DeleteProjectRequestRequestTypeDef(TypedDict):
    Name: str

class DeleteRecipeVersionRequestRequestTypeDef(TypedDict):
    Name: str
    RecipeVersion: str

class DeleteRulesetRequestRequestTypeDef(TypedDict):
    Name: str

class DeleteScheduleRequestRequestTypeDef(TypedDict):
    Name: str

class DescribeDatasetRequestRequestTypeDef(TypedDict):
    Name: str

class DescribeJobRequestRequestTypeDef(TypedDict):
    Name: str

class DescribeJobRunRequestRequestTypeDef(TypedDict):
    Name: str
    RunId: str

class DescribeProjectRequestRequestTypeDef(TypedDict):
    Name: str

class DescribeRecipeRequestRequestTypeDef(TypedDict):
    Name: str
    RecipeVersion: NotRequired[str]

class DescribeRulesetRequestRequestTypeDef(TypedDict):
    Name: str

class DescribeScheduleRequestRequestTypeDef(TypedDict):
    Name: str

class ExcelOptionsOutputTypeDef(TypedDict):
    SheetNames: NotRequired[List[str]]
    SheetIndexes: NotRequired[List[int]]
    HeaderRow: NotRequired[bool]

class ExcelOptionsTypeDef(TypedDict):
    SheetNames: NotRequired[Sequence[str]]
    SheetIndexes: NotRequired[Sequence[int]]
    HeaderRow: NotRequired[bool]

class FilesLimitTypeDef(TypedDict):
    MaxFiles: int
    OrderedBy: NotRequired[Literal["LAST_MODIFIED_DATE"]]
    Order: NotRequired[OrderType]

class FilterExpressionTypeDef(TypedDict):
    Expression: str
    ValuesMap: Mapping[str, str]

class JsonOptionsTypeDef(TypedDict):
    MultiLine: NotRequired[bool]

class MetadataTypeDef(TypedDict):
    SourceArn: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListDatasetsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListJobRunsRequestRequestTypeDef(TypedDict):
    Name: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListJobsRequestRequestTypeDef(TypedDict):
    DatasetName: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ProjectName: NotRequired[str]

class ListProjectsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListRecipeVersionsRequestRequestTypeDef(TypedDict):
    Name: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListRecipesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    RecipeVersion: NotRequired[str]

class ListRulesetsRequestRequestTypeDef(TypedDict):
    TargetArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class RulesetItemTypeDef(TypedDict):
    Name: str
    TargetArn: str
    AccountId: NotRequired[str]
    CreatedBy: NotRequired[str]
    CreateDate: NotRequired[datetime]
    Description: NotRequired[str]
    LastModifiedBy: NotRequired[str]
    LastModifiedDate: NotRequired[datetime]
    ResourceArn: NotRequired[str]
    RuleCount: NotRequired[int]
    Tags: NotRequired[Dict[str, str]]

class ListSchedulesRequestRequestTypeDef(TypedDict):
    JobName: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ScheduleTypeDef(TypedDict):
    Name: str
    AccountId: NotRequired[str]
    CreatedBy: NotRequired[str]
    CreateDate: NotRequired[datetime]
    JobNames: NotRequired[List[str]]
    LastModifiedBy: NotRequired[str]
    LastModifiedDate: NotRequired[datetime]
    ResourceArn: NotRequired[str]
    CronExpression: NotRequired[str]
    Tags: NotRequired[Dict[str, str]]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class PublishRecipeRequestRequestTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]

class RecipeActionOutputTypeDef(TypedDict):
    Operation: str
    Parameters: NotRequired[Dict[str, str]]

class RecipeActionTypeDef(TypedDict):
    Operation: str
    Parameters: NotRequired[Mapping[str, str]]

ThresholdTypeDef = TypedDict(
    "ThresholdTypeDef",
    {
        "Value": float,
        "Type": NotRequired[ThresholdTypeType],
        "Unit": NotRequired[ThresholdUnitType],
    },
)

class ViewFrameTypeDef(TypedDict):
    StartColumnIndex: int
    ColumnRange: NotRequired[int]
    HiddenColumns: NotRequired[Sequence[str]]
    StartRowIndex: NotRequired[int]
    RowRange: NotRequired[int]
    Analytics: NotRequired[AnalyticsModeType]

class StartJobRunRequestRequestTypeDef(TypedDict):
    Name: str

class StartProjectSessionRequestRequestTypeDef(TypedDict):
    Name: str
    AssumeControl: NotRequired[bool]

class StatisticOverrideOutputTypeDef(TypedDict):
    Statistic: str
    Parameters: Dict[str, str]

class StatisticOverrideTypeDef(TypedDict):
    Statistic: str
    Parameters: Mapping[str, str]

class StopJobRunRequestRequestTypeDef(TypedDict):
    Name: str
    RunId: str

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateScheduleRequestRequestTypeDef(TypedDict):
    CronExpression: str
    Name: str
    JobNames: NotRequired[Sequence[str]]

class EntityDetectorConfigurationOutputTypeDef(TypedDict):
    EntityTypes: List[str]
    AllowedStatistics: NotRequired[List[AllowedStatisticsOutputTypeDef]]

AllowedStatisticsUnionTypeDef = Union[AllowedStatisticsTypeDef, AllowedStatisticsOutputTypeDef]

class BatchDeleteRecipeVersionResponseTypeDef(TypedDict):
    Name: str
    Errors: List[RecipeVersionErrorDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDatasetResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateProfileJobResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateProjectResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRecipeJobResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRecipeResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRulesetResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateScheduleResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDatasetResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteJobResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteProjectResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteRecipeVersionResponseTypeDef(TypedDict):
    Name: str
    RecipeVersion: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteRulesetResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteScheduleResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeScheduleResponseTypeDef(TypedDict):
    CreateDate: datetime
    CreatedBy: str
    JobNames: List[str]
    LastModifiedBy: str
    LastModifiedDate: datetime
    ResourceArn: str
    CronExpression: str
    Tags: Dict[str, str]
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PublishRecipeResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class SendProjectSessionActionResponseTypeDef(TypedDict):
    Result: str
    Name: str
    ActionId: int
    ResponseMetadata: ResponseMetadataTypeDef

class StartJobRunResponseTypeDef(TypedDict):
    RunId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartProjectSessionResponseTypeDef(TypedDict):
    Name: str
    ClientSessionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StopJobRunResponseTypeDef(TypedDict):
    RunId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDatasetResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateProfileJobResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateProjectResponseTypeDef(TypedDict):
    LastModifiedDate: datetime
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRecipeJobResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRecipeResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRulesetResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateScheduleResponseTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class DataCatalogInputDefinitionTypeDef(TypedDict):
    DatabaseName: str
    TableName: str
    CatalogId: NotRequired[str]
    TempDirectory: NotRequired[S3LocationTypeDef]

class DatabaseInputDefinitionTypeDef(TypedDict):
    GlueConnectionName: str
    DatabaseTableName: NotRequired[str]
    TempDirectory: NotRequired[S3LocationTypeDef]
    QueryString: NotRequired[str]

class DatabaseTableOutputOptionsTypeDef(TypedDict):
    TableName: str
    TempDirectory: NotRequired[S3LocationTypeDef]

class S3TableOutputOptionsTypeDef(TypedDict):
    Location: S3LocationTypeDef

class CreateProjectRequestRequestTypeDef(TypedDict):
    DatasetName: str
    Name: str
    RecipeName: str
    RoleArn: str
    Sample: NotRequired[SampleTypeDef]
    Tags: NotRequired[Mapping[str, str]]

class DescribeProjectResponseTypeDef(TypedDict):
    CreateDate: datetime
    CreatedBy: str
    DatasetName: str
    LastModifiedDate: datetime
    LastModifiedBy: str
    Name: str
    RecipeName: str
    ResourceArn: str
    Sample: SampleTypeDef
    RoleArn: str
    Tags: Dict[str, str]
    SessionStatus: SessionStatusType
    OpenedBy: str
    OpenDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ProjectTypeDef(TypedDict):
    Name: str
    RecipeName: str
    AccountId: NotRequired[str]
    CreateDate: NotRequired[datetime]
    CreatedBy: NotRequired[str]
    DatasetName: NotRequired[str]
    LastModifiedDate: NotRequired[datetime]
    LastModifiedBy: NotRequired[str]
    ResourceArn: NotRequired[str]
    Sample: NotRequired[SampleTypeDef]
    Tags: NotRequired[Dict[str, str]]
    RoleArn: NotRequired[str]
    OpenedBy: NotRequired[str]
    OpenDate: NotRequired[datetime]

class UpdateProjectRequestRequestTypeDef(TypedDict):
    RoleArn: str
    Name: str
    Sample: NotRequired[SampleTypeDef]

class OutputFormatOptionsTypeDef(TypedDict):
    Csv: NotRequired[CsvOutputOptionsTypeDef]

DatasetParameterOutputTypeDef = TypedDict(
    "DatasetParameterOutputTypeDef",
    {
        "Name": str,
        "Type": ParameterTypeType,
        "DatetimeOptions": NotRequired[DatetimeOptionsTypeDef],
        "CreateColumn": NotRequired[bool],
        "Filter": NotRequired[FilterExpressionOutputTypeDef],
    },
)
ExcelOptionsUnionTypeDef = Union[ExcelOptionsTypeDef, ExcelOptionsOutputTypeDef]
FilterExpressionUnionTypeDef = Union[FilterExpressionTypeDef, FilterExpressionOutputTypeDef]

class FormatOptionsOutputTypeDef(TypedDict):
    Json: NotRequired[JsonOptionsTypeDef]
    Excel: NotRequired[ExcelOptionsOutputTypeDef]
    Csv: NotRequired[CsvOptionsTypeDef]

class ListDatasetsRequestListDatasetsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListJobRunsRequestListJobRunsPaginateTypeDef(TypedDict):
    Name: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListJobsRequestListJobsPaginateTypeDef(TypedDict):
    DatasetName: NotRequired[str]
    ProjectName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProjectsRequestListProjectsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRecipeVersionsRequestListRecipeVersionsPaginateTypeDef(TypedDict):
    Name: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRecipesRequestListRecipesPaginateTypeDef(TypedDict):
    RecipeVersion: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRulesetsRequestListRulesetsPaginateTypeDef(TypedDict):
    TargetArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSchedulesRequestListSchedulesPaginateTypeDef(TypedDict):
    JobName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRulesetsResponseTypeDef(TypedDict):
    Rulesets: List[RulesetItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListSchedulesResponseTypeDef(TypedDict):
    Schedules: List[ScheduleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class RecipeStepOutputTypeDef(TypedDict):
    Action: RecipeActionOutputTypeDef
    ConditionExpressions: NotRequired[List[ConditionExpressionTypeDef]]

RecipeActionUnionTypeDef = Union[RecipeActionTypeDef, RecipeActionOutputTypeDef]

class RuleOutputTypeDef(TypedDict):
    Name: str
    CheckExpression: str
    Disabled: NotRequired[bool]
    SubstitutionMap: NotRequired[Dict[str, str]]
    Threshold: NotRequired[ThresholdTypeDef]
    ColumnSelectors: NotRequired[List[ColumnSelectorTypeDef]]

class RuleTypeDef(TypedDict):
    Name: str
    CheckExpression: str
    Disabled: NotRequired[bool]
    SubstitutionMap: NotRequired[Mapping[str, str]]
    Threshold: NotRequired[ThresholdTypeDef]
    ColumnSelectors: NotRequired[Sequence[ColumnSelectorTypeDef]]

class StatisticsConfigurationOutputTypeDef(TypedDict):
    IncludedStatistics: NotRequired[List[str]]
    Overrides: NotRequired[List[StatisticOverrideOutputTypeDef]]

StatisticOverrideUnionTypeDef = Union[StatisticOverrideTypeDef, StatisticOverrideOutputTypeDef]

class EntityDetectorConfigurationTypeDef(TypedDict):
    EntityTypes: Sequence[str]
    AllowedStatistics: NotRequired[Sequence[AllowedStatisticsUnionTypeDef]]

class InputTypeDef(TypedDict):
    S3InputDefinition: NotRequired[S3LocationTypeDef]
    DataCatalogInputDefinition: NotRequired[DataCatalogInputDefinitionTypeDef]
    DatabaseInputDefinition: NotRequired[DatabaseInputDefinitionTypeDef]
    Metadata: NotRequired[MetadataTypeDef]

class DatabaseOutputTypeDef(TypedDict):
    GlueConnectionName: str
    DatabaseOptions: DatabaseTableOutputOptionsTypeDef
    DatabaseOutputMode: NotRequired[Literal["NEW_TABLE"]]

class DataCatalogOutputTypeDef(TypedDict):
    DatabaseName: str
    TableName: str
    CatalogId: NotRequired[str]
    S3Options: NotRequired[S3TableOutputOptionsTypeDef]
    DatabaseOptions: NotRequired[DatabaseTableOutputOptionsTypeDef]
    Overwrite: NotRequired[bool]

class ListProjectsResponseTypeDef(TypedDict):
    Projects: List[ProjectTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ExtraOutputTypeDef(TypedDict):
    Location: S3LocationTypeDef
    CompressionFormat: NotRequired[CompressionFormatType]
    Format: NotRequired[OutputFormatType]
    PartitionColumns: NotRequired[List[str]]
    Overwrite: NotRequired[bool]
    FormatOptions: NotRequired[OutputFormatOptionsTypeDef]
    MaxOutputFiles: NotRequired[int]

class OutputTypeDef(TypedDict):
    Location: S3LocationTypeDef
    CompressionFormat: NotRequired[CompressionFormatType]
    Format: NotRequired[OutputFormatType]
    PartitionColumns: NotRequired[Sequence[str]]
    Overwrite: NotRequired[bool]
    FormatOptions: NotRequired[OutputFormatOptionsTypeDef]
    MaxOutputFiles: NotRequired[int]

class PathOptionsOutputTypeDef(TypedDict):
    LastModifiedDateCondition: NotRequired[FilterExpressionOutputTypeDef]
    FilesLimit: NotRequired[FilesLimitTypeDef]
    Parameters: NotRequired[Dict[str, DatasetParameterOutputTypeDef]]

class FormatOptionsTypeDef(TypedDict):
    Json: NotRequired[JsonOptionsTypeDef]
    Excel: NotRequired[ExcelOptionsUnionTypeDef]
    Csv: NotRequired[CsvOptionsTypeDef]

DatasetParameterTypeDef = TypedDict(
    "DatasetParameterTypeDef",
    {
        "Name": str,
        "Type": ParameterTypeType,
        "DatetimeOptions": NotRequired[DatetimeOptionsTypeDef],
        "CreateColumn": NotRequired[bool],
        "Filter": NotRequired[FilterExpressionUnionTypeDef],
    },
)

class DescribeRecipeResponseTypeDef(TypedDict):
    CreatedBy: str
    CreateDate: datetime
    LastModifiedBy: str
    LastModifiedDate: datetime
    ProjectName: str
    PublishedBy: str
    PublishedDate: datetime
    Description: str
    Name: str
    Steps: List[RecipeStepOutputTypeDef]
    Tags: Dict[str, str]
    ResourceArn: str
    RecipeVersion: str
    ResponseMetadata: ResponseMetadataTypeDef

class RecipeTypeDef(TypedDict):
    Name: str
    CreatedBy: NotRequired[str]
    CreateDate: NotRequired[datetime]
    LastModifiedBy: NotRequired[str]
    LastModifiedDate: NotRequired[datetime]
    ProjectName: NotRequired[str]
    PublishedBy: NotRequired[str]
    PublishedDate: NotRequired[datetime]
    Description: NotRequired[str]
    ResourceArn: NotRequired[str]
    Steps: NotRequired[List[RecipeStepOutputTypeDef]]
    Tags: NotRequired[Dict[str, str]]
    RecipeVersion: NotRequired[str]

class RecipeStepTypeDef(TypedDict):
    Action: RecipeActionUnionTypeDef
    ConditionExpressions: NotRequired[Sequence[ConditionExpressionTypeDef]]

class DescribeRulesetResponseTypeDef(TypedDict):
    Name: str
    Description: str
    TargetArn: str
    Rules: List[RuleOutputTypeDef]
    CreateDate: datetime
    CreatedBy: str
    LastModifiedBy: str
    LastModifiedDate: datetime
    ResourceArn: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

RuleUnionTypeDef = Union[RuleTypeDef, RuleOutputTypeDef]

class UpdateRulesetRequestRequestTypeDef(TypedDict):
    Name: str
    Rules: Sequence[RuleTypeDef]
    Description: NotRequired[str]

class ColumnStatisticsConfigurationOutputTypeDef(TypedDict):
    Statistics: StatisticsConfigurationOutputTypeDef
    Selectors: NotRequired[List[ColumnSelectorTypeDef]]

class StatisticsConfigurationTypeDef(TypedDict):
    IncludedStatistics: NotRequired[Sequence[str]]
    Overrides: NotRequired[Sequence[StatisticOverrideUnionTypeDef]]

EntityDetectorConfigurationUnionTypeDef = Union[
    EntityDetectorConfigurationTypeDef, EntityDetectorConfigurationOutputTypeDef
]

class JobRunTypeDef(TypedDict):
    Attempt: NotRequired[int]
    CompletedOn: NotRequired[datetime]
    DatasetName: NotRequired[str]
    ErrorMessage: NotRequired[str]
    ExecutionTime: NotRequired[int]
    JobName: NotRequired[str]
    RunId: NotRequired[str]
    State: NotRequired[JobRunStateType]
    LogSubscription: NotRequired[LogSubscriptionType]
    LogGroupName: NotRequired[str]
    Outputs: NotRequired[List[ExtraOutputTypeDef]]
    DataCatalogOutputs: NotRequired[List[DataCatalogOutputTypeDef]]
    DatabaseOutputs: NotRequired[List[DatabaseOutputTypeDef]]
    RecipeReference: NotRequired[RecipeReferenceTypeDef]
    StartedBy: NotRequired[str]
    StartedOn: NotRequired[datetime]
    JobSample: NotRequired[JobSampleTypeDef]
    ValidationConfigurations: NotRequired[List[ValidationConfigurationTypeDef]]

JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "Name": str,
        "AccountId": NotRequired[str],
        "CreatedBy": NotRequired[str],
        "CreateDate": NotRequired[datetime],
        "DatasetName": NotRequired[str],
        "EncryptionKeyArn": NotRequired[str],
        "EncryptionMode": NotRequired[EncryptionModeType],
        "Type": NotRequired[JobTypeType],
        "LastModifiedBy": NotRequired[str],
        "LastModifiedDate": NotRequired[datetime],
        "LogSubscription": NotRequired[LogSubscriptionType],
        "MaxCapacity": NotRequired[int],
        "MaxRetries": NotRequired[int],
        "Outputs": NotRequired[List[ExtraOutputTypeDef]],
        "DataCatalogOutputs": NotRequired[List[DataCatalogOutputTypeDef]],
        "DatabaseOutputs": NotRequired[List[DatabaseOutputTypeDef]],
        "ProjectName": NotRequired[str],
        "RecipeReference": NotRequired[RecipeReferenceTypeDef],
        "ResourceArn": NotRequired[str],
        "RoleArn": NotRequired[str],
        "Timeout": NotRequired[int],
        "Tags": NotRequired[Dict[str, str]],
        "JobSample": NotRequired[JobSampleTypeDef],
        "ValidationConfigurations": NotRequired[List[ValidationConfigurationTypeDef]],
    },
)
UnionTypeDef = Union[OutputTypeDef, ExtraOutputTypeDef]

class UpdateRecipeJobRequestRequestTypeDef(TypedDict):
    Name: str
    RoleArn: str
    EncryptionKeyArn: NotRequired[str]
    EncryptionMode: NotRequired[EncryptionModeType]
    LogSubscription: NotRequired[LogSubscriptionType]
    MaxCapacity: NotRequired[int]
    MaxRetries: NotRequired[int]
    Outputs: NotRequired[Sequence[OutputTypeDef]]
    DataCatalogOutputs: NotRequired[Sequence[DataCatalogOutputTypeDef]]
    DatabaseOutputs: NotRequired[Sequence[DatabaseOutputTypeDef]]
    Timeout: NotRequired[int]

class DatasetTypeDef(TypedDict):
    Name: str
    Input: InputTypeDef
    AccountId: NotRequired[str]
    CreatedBy: NotRequired[str]
    CreateDate: NotRequired[datetime]
    Format: NotRequired[InputFormatType]
    FormatOptions: NotRequired[FormatOptionsOutputTypeDef]
    LastModifiedDate: NotRequired[datetime]
    LastModifiedBy: NotRequired[str]
    Source: NotRequired[SourceType]
    PathOptions: NotRequired[PathOptionsOutputTypeDef]
    Tags: NotRequired[Dict[str, str]]
    ResourceArn: NotRequired[str]

class DescribeDatasetResponseTypeDef(TypedDict):
    CreatedBy: str
    CreateDate: datetime
    Name: str
    Format: InputFormatType
    FormatOptions: FormatOptionsOutputTypeDef
    Input: InputTypeDef
    LastModifiedDate: datetime
    LastModifiedBy: str
    Source: SourceType
    PathOptions: PathOptionsOutputTypeDef
    Tags: Dict[str, str]
    ResourceArn: str
    ResponseMetadata: ResponseMetadataTypeDef

DatasetParameterUnionTypeDef = Union[DatasetParameterTypeDef, DatasetParameterOutputTypeDef]

class ListRecipeVersionsResponseTypeDef(TypedDict):
    Recipes: List[RecipeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListRecipesResponseTypeDef(TypedDict):
    Recipes: List[RecipeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

RecipeStepUnionTypeDef = Union[RecipeStepTypeDef, RecipeStepOutputTypeDef]

class SendProjectSessionActionRequestRequestTypeDef(TypedDict):
    Name: str
    Preview: NotRequired[bool]
    RecipeStep: NotRequired[RecipeStepTypeDef]
    StepIndex: NotRequired[int]
    ClientSessionId: NotRequired[str]
    ViewFrame: NotRequired[ViewFrameTypeDef]

class UpdateRecipeRequestRequestTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    Steps: NotRequired[Sequence[RecipeStepTypeDef]]

class CreateRulesetRequestRequestTypeDef(TypedDict):
    Name: str
    TargetArn: str
    Rules: Sequence[RuleUnionTypeDef]
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class ProfileConfigurationOutputTypeDef(TypedDict):
    DatasetStatisticsConfiguration: NotRequired[StatisticsConfigurationOutputTypeDef]
    ProfileColumns: NotRequired[List[ColumnSelectorTypeDef]]
    ColumnStatisticsConfigurations: NotRequired[List[ColumnStatisticsConfigurationOutputTypeDef]]
    EntityDetectorConfiguration: NotRequired[EntityDetectorConfigurationOutputTypeDef]

StatisticsConfigurationUnionTypeDef = Union[
    StatisticsConfigurationTypeDef, StatisticsConfigurationOutputTypeDef
]

class ListJobRunsResponseTypeDef(TypedDict):
    JobRuns: List[JobRunTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListJobsResponseTypeDef(TypedDict):
    Jobs: List[JobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateRecipeJobRequestRequestTypeDef(TypedDict):
    Name: str
    RoleArn: str
    DatasetName: NotRequired[str]
    EncryptionKeyArn: NotRequired[str]
    EncryptionMode: NotRequired[EncryptionModeType]
    LogSubscription: NotRequired[LogSubscriptionType]
    MaxCapacity: NotRequired[int]
    MaxRetries: NotRequired[int]
    Outputs: NotRequired[Sequence[UnionTypeDef]]
    DataCatalogOutputs: NotRequired[Sequence[DataCatalogOutputTypeDef]]
    DatabaseOutputs: NotRequired[Sequence[DatabaseOutputTypeDef]]
    ProjectName: NotRequired[str]
    RecipeReference: NotRequired[RecipeReferenceTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    Timeout: NotRequired[int]

class ListDatasetsResponseTypeDef(TypedDict):
    Datasets: List[DatasetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PathOptionsTypeDef(TypedDict):
    LastModifiedDateCondition: NotRequired[FilterExpressionUnionTypeDef]
    FilesLimit: NotRequired[FilesLimitTypeDef]
    Parameters: NotRequired[Mapping[str, DatasetParameterUnionTypeDef]]

class CreateRecipeRequestRequestTypeDef(TypedDict):
    Name: str
    Steps: Sequence[RecipeStepUnionTypeDef]
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

DescribeJobResponseTypeDef = TypedDict(
    "DescribeJobResponseTypeDef",
    {
        "CreateDate": datetime,
        "CreatedBy": str,
        "DatasetName": str,
        "EncryptionKeyArn": str,
        "EncryptionMode": EncryptionModeType,
        "Name": str,
        "Type": JobTypeType,
        "LastModifiedBy": str,
        "LastModifiedDate": datetime,
        "LogSubscription": LogSubscriptionType,
        "MaxCapacity": int,
        "MaxRetries": int,
        "Outputs": List[ExtraOutputTypeDef],
        "DataCatalogOutputs": List[DataCatalogOutputTypeDef],
        "DatabaseOutputs": List[DatabaseOutputTypeDef],
        "ProjectName": str,
        "ProfileConfiguration": ProfileConfigurationOutputTypeDef,
        "ValidationConfigurations": List[ValidationConfigurationTypeDef],
        "RecipeReference": RecipeReferenceTypeDef,
        "ResourceArn": str,
        "RoleArn": str,
        "Tags": Dict[str, str],
        "Timeout": int,
        "JobSample": JobSampleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class DescribeJobRunResponseTypeDef(TypedDict):
    Attempt: int
    CompletedOn: datetime
    DatasetName: str
    ErrorMessage: str
    ExecutionTime: int
    JobName: str
    ProfileConfiguration: ProfileConfigurationOutputTypeDef
    ValidationConfigurations: List[ValidationConfigurationTypeDef]
    RunId: str
    State: JobRunStateType
    LogSubscription: LogSubscriptionType
    LogGroupName: str
    Outputs: List[ExtraOutputTypeDef]
    DataCatalogOutputs: List[DataCatalogOutputTypeDef]
    DatabaseOutputs: List[DatabaseOutputTypeDef]
    RecipeReference: RecipeReferenceTypeDef
    StartedBy: str
    StartedOn: datetime
    JobSample: JobSampleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ColumnStatisticsConfigurationTypeDef(TypedDict):
    Statistics: StatisticsConfigurationUnionTypeDef
    Selectors: NotRequired[Sequence[ColumnSelectorTypeDef]]

class CreateDatasetRequestRequestTypeDef(TypedDict):
    Name: str
    Input: InputTypeDef
    Format: NotRequired[InputFormatType]
    FormatOptions: NotRequired[FormatOptionsTypeDef]
    PathOptions: NotRequired[PathOptionsTypeDef]
    Tags: NotRequired[Mapping[str, str]]

class UpdateDatasetRequestRequestTypeDef(TypedDict):
    Name: str
    Input: InputTypeDef
    Format: NotRequired[InputFormatType]
    FormatOptions: NotRequired[FormatOptionsTypeDef]
    PathOptions: NotRequired[PathOptionsTypeDef]

ColumnStatisticsConfigurationUnionTypeDef = Union[
    ColumnStatisticsConfigurationTypeDef, ColumnStatisticsConfigurationOutputTypeDef
]

class ProfileConfigurationTypeDef(TypedDict):
    DatasetStatisticsConfiguration: NotRequired[StatisticsConfigurationUnionTypeDef]
    ProfileColumns: NotRequired[Sequence[ColumnSelectorTypeDef]]
    ColumnStatisticsConfigurations: NotRequired[Sequence[ColumnStatisticsConfigurationUnionTypeDef]]
    EntityDetectorConfiguration: NotRequired[EntityDetectorConfigurationUnionTypeDef]

class CreateProfileJobRequestRequestTypeDef(TypedDict):
    DatasetName: str
    Name: str
    OutputLocation: S3LocationTypeDef
    RoleArn: str
    EncryptionKeyArn: NotRequired[str]
    EncryptionMode: NotRequired[EncryptionModeType]
    LogSubscription: NotRequired[LogSubscriptionType]
    MaxCapacity: NotRequired[int]
    MaxRetries: NotRequired[int]
    Configuration: NotRequired[ProfileConfigurationTypeDef]
    ValidationConfigurations: NotRequired[Sequence[ValidationConfigurationTypeDef]]
    Tags: NotRequired[Mapping[str, str]]
    Timeout: NotRequired[int]
    JobSample: NotRequired[JobSampleTypeDef]

class UpdateProfileJobRequestRequestTypeDef(TypedDict):
    Name: str
    OutputLocation: S3LocationTypeDef
    RoleArn: str
    Configuration: NotRequired[ProfileConfigurationTypeDef]
    EncryptionKeyArn: NotRequired[str]
    EncryptionMode: NotRequired[EncryptionModeType]
    LogSubscription: NotRequired[LogSubscriptionType]
    MaxCapacity: NotRequired[int]
    MaxRetries: NotRequired[int]
    ValidationConfigurations: NotRequired[Sequence[ValidationConfigurationTypeDef]]
    Timeout: NotRequired[int]
    JobSample: NotRequired[JobSampleTypeDef]
