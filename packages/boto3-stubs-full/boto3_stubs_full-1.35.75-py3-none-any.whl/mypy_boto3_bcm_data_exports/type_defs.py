"""
Type annotations for bcm-data-exports service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_data_exports/type_defs/)

Usage::

    ```python
    from mypy_boto3_bcm_data_exports.type_defs import ColumnTypeDef

    data: ColumnTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    CompressionOptionType,
    ExecutionStatusCodeType,
    ExecutionStatusReasonType,
    ExportStatusCodeType,
    FormatOptionType,
    OverwriteOptionType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ColumnTypeDef",
    "CreateExportRequestRequestTypeDef",
    "CreateExportResponseTypeDef",
    "DataQueryOutputTypeDef",
    "DataQueryTypeDef",
    "DataQueryUnionTypeDef",
    "DeleteExportRequestRequestTypeDef",
    "DeleteExportResponseTypeDef",
    "DestinationConfigurationsTypeDef",
    "ExecutionReferenceTypeDef",
    "ExecutionStatusTypeDef",
    "ExportOutputTypeDef",
    "ExportReferenceTypeDef",
    "ExportStatusTypeDef",
    "ExportTypeDef",
    "GetExecutionRequestRequestTypeDef",
    "GetExecutionResponseTypeDef",
    "GetExportRequestRequestTypeDef",
    "GetExportResponseTypeDef",
    "GetTableRequestRequestTypeDef",
    "GetTableResponseTypeDef",
    "ListExecutionsRequestListExecutionsPaginateTypeDef",
    "ListExecutionsRequestRequestTypeDef",
    "ListExecutionsResponseTypeDef",
    "ListExportsRequestListExportsPaginateTypeDef",
    "ListExportsRequestRequestTypeDef",
    "ListExportsResponseTypeDef",
    "ListTablesRequestListTablesPaginateTypeDef",
    "ListTablesRequestRequestTypeDef",
    "ListTablesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "RefreshCadenceTypeDef",
    "ResourceTagTypeDef",
    "ResponseMetadataTypeDef",
    "S3DestinationTypeDef",
    "S3OutputConfigurationsTypeDef",
    "TablePropertyDescriptionTypeDef",
    "TableTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateExportRequestRequestTypeDef",
    "UpdateExportResponseTypeDef",
)

ColumnTypeDef = TypedDict(
    "ColumnTypeDef",
    {
        "Description": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[str],
    },
)


class ResourceTagTypeDef(TypedDict):
    Key: str
    Value: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DataQueryOutputTypeDef(TypedDict):
    QueryStatement: str
    TableConfigurations: NotRequired[Dict[str, Dict[str, str]]]


class DataQueryTypeDef(TypedDict):
    QueryStatement: str
    TableConfigurations: NotRequired[Mapping[str, Mapping[str, str]]]


class DeleteExportRequestRequestTypeDef(TypedDict):
    ExportArn: str


class ExecutionStatusTypeDef(TypedDict):
    CompletedAt: NotRequired[datetime]
    CreatedAt: NotRequired[datetime]
    LastUpdatedAt: NotRequired[datetime]
    StatusCode: NotRequired[ExecutionStatusCodeType]
    StatusReason: NotRequired[ExecutionStatusReasonType]


class RefreshCadenceTypeDef(TypedDict):
    Frequency: Literal["SYNCHRONOUS"]


class ExportStatusTypeDef(TypedDict):
    CreatedAt: NotRequired[datetime]
    LastRefreshedAt: NotRequired[datetime]
    LastUpdatedAt: NotRequired[datetime]
    StatusCode: NotRequired[ExportStatusCodeType]
    StatusReason: NotRequired[ExecutionStatusReasonType]


class GetExecutionRequestRequestTypeDef(TypedDict):
    ExecutionId: str
    ExportArn: str


class GetExportRequestRequestTypeDef(TypedDict):
    ExportArn: str


class GetTableRequestRequestTypeDef(TypedDict):
    TableName: str
    TableProperties: NotRequired[Mapping[str, str]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListExecutionsRequestRequestTypeDef(TypedDict):
    ExportArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListExportsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTablesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class S3OutputConfigurationsTypeDef(TypedDict):
    Compression: CompressionOptionType
    Format: FormatOptionType
    OutputType: Literal["CUSTOM"]
    Overwrite: OverwriteOptionType


class TablePropertyDescriptionTypeDef(TypedDict):
    DefaultValue: NotRequired[str]
    Description: NotRequired[str]
    Name: NotRequired[str]
    ValidValues: NotRequired[List[str]]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    ResourceTagKeys: Sequence[str]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    ResourceTags: Sequence[ResourceTagTypeDef]


class CreateExportResponseTypeDef(TypedDict):
    ExportArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteExportResponseTypeDef(TypedDict):
    ExportArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetTableResponseTypeDef(TypedDict):
    Description: str
    Schema: List[ColumnTypeDef]
    TableName: str
    TableProperties: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    ResourceTags: List[ResourceTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateExportResponseTypeDef(TypedDict):
    ExportArn: str
    ResponseMetadata: ResponseMetadataTypeDef


DataQueryUnionTypeDef = Union[DataQueryTypeDef, DataQueryOutputTypeDef]


class ExecutionReferenceTypeDef(TypedDict):
    ExecutionId: str
    ExecutionStatus: ExecutionStatusTypeDef


class ExportReferenceTypeDef(TypedDict):
    ExportArn: str
    ExportName: str
    ExportStatus: ExportStatusTypeDef


class ListExecutionsRequestListExecutionsPaginateTypeDef(TypedDict):
    ExportArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListExportsRequestListExportsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTablesRequestListTablesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class S3DestinationTypeDef(TypedDict):
    S3Bucket: str
    S3OutputConfigurations: S3OutputConfigurationsTypeDef
    S3Prefix: str
    S3Region: str


class TableTypeDef(TypedDict):
    Description: NotRequired[str]
    TableName: NotRequired[str]
    TableProperties: NotRequired[List[TablePropertyDescriptionTypeDef]]


class ListExecutionsResponseTypeDef(TypedDict):
    Executions: List[ExecutionReferenceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListExportsResponseTypeDef(TypedDict):
    Exports: List[ExportReferenceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DestinationConfigurationsTypeDef(TypedDict):
    S3Destination: S3DestinationTypeDef


class ListTablesResponseTypeDef(TypedDict):
    Tables: List[TableTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ExportOutputTypeDef(TypedDict):
    DataQuery: DataQueryOutputTypeDef
    DestinationConfigurations: DestinationConfigurationsTypeDef
    Name: str
    RefreshCadence: RefreshCadenceTypeDef
    Description: NotRequired[str]
    ExportArn: NotRequired[str]


class ExportTypeDef(TypedDict):
    DataQuery: DataQueryUnionTypeDef
    DestinationConfigurations: DestinationConfigurationsTypeDef
    Name: str
    RefreshCadence: RefreshCadenceTypeDef
    Description: NotRequired[str]
    ExportArn: NotRequired[str]


class GetExecutionResponseTypeDef(TypedDict):
    ExecutionId: str
    ExecutionStatus: ExecutionStatusTypeDef
    Export: ExportOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetExportResponseTypeDef(TypedDict):
    Export: ExportOutputTypeDef
    ExportStatus: ExportStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateExportRequestRequestTypeDef(TypedDict):
    Export: ExportTypeDef
    ResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]


class UpdateExportRequestRequestTypeDef(TypedDict):
    Export: ExportTypeDef
    ExportArn: str
