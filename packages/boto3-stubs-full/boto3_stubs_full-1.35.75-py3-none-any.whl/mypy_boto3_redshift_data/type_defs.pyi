"""
Type annotations for redshift-data service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_data/type_defs/)

Usage::

    ```python
    from mypy_boto3_redshift_data.type_defs import BatchExecuteStatementInputRequestTypeDef

    data: BatchExecuteStatementInputRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import ResultFormatStringType, StatementStatusStringType, StatusStringType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "BatchExecuteStatementInputRequestTypeDef",
    "BatchExecuteStatementOutputTypeDef",
    "CancelStatementRequestRequestTypeDef",
    "CancelStatementResponseTypeDef",
    "ColumnMetadataTypeDef",
    "DescribeStatementRequestRequestTypeDef",
    "DescribeStatementResponseTypeDef",
    "DescribeTableRequestDescribeTablePaginateTypeDef",
    "DescribeTableRequestRequestTypeDef",
    "DescribeTableResponseTypeDef",
    "ExecuteStatementInputRequestTypeDef",
    "ExecuteStatementOutputTypeDef",
    "FieldTypeDef",
    "GetStatementResultRequestGetStatementResultPaginateTypeDef",
    "GetStatementResultRequestRequestTypeDef",
    "GetStatementResultResponseTypeDef",
    "GetStatementResultV2RequestGetStatementResultV2PaginateTypeDef",
    "GetStatementResultV2RequestRequestTypeDef",
    "GetStatementResultV2ResponseTypeDef",
    "ListDatabasesRequestListDatabasesPaginateTypeDef",
    "ListDatabasesRequestRequestTypeDef",
    "ListDatabasesResponseTypeDef",
    "ListSchemasRequestListSchemasPaginateTypeDef",
    "ListSchemasRequestRequestTypeDef",
    "ListSchemasResponseTypeDef",
    "ListStatementsRequestListStatementsPaginateTypeDef",
    "ListStatementsRequestRequestTypeDef",
    "ListStatementsResponseTypeDef",
    "ListTablesRequestListTablesPaginateTypeDef",
    "ListTablesRequestRequestTypeDef",
    "ListTablesResponseTypeDef",
    "PaginatorConfigTypeDef",
    "QueryRecordsTypeDef",
    "ResponseMetadataTypeDef",
    "SqlParameterTypeDef",
    "StatementDataTypeDef",
    "SubStatementDataTypeDef",
    "TableMemberTypeDef",
)

class BatchExecuteStatementInputRequestTypeDef(TypedDict):
    Sqls: Sequence[str]
    ClientToken: NotRequired[str]
    ClusterIdentifier: NotRequired[str]
    Database: NotRequired[str]
    DbUser: NotRequired[str]
    ResultFormat: NotRequired[ResultFormatStringType]
    SecretArn: NotRequired[str]
    SessionId: NotRequired[str]
    SessionKeepAliveSeconds: NotRequired[int]
    StatementName: NotRequired[str]
    WithEvent: NotRequired[bool]
    WorkgroupName: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CancelStatementRequestRequestTypeDef(TypedDict):
    Id: str

class ColumnMetadataTypeDef(TypedDict):
    columnDefault: NotRequired[str]
    isCaseSensitive: NotRequired[bool]
    isCurrency: NotRequired[bool]
    isSigned: NotRequired[bool]
    label: NotRequired[str]
    length: NotRequired[int]
    name: NotRequired[str]
    nullable: NotRequired[int]
    precision: NotRequired[int]
    scale: NotRequired[int]
    schemaName: NotRequired[str]
    tableName: NotRequired[str]
    typeName: NotRequired[str]

class DescribeStatementRequestRequestTypeDef(TypedDict):
    Id: str

class SqlParameterTypeDef(TypedDict):
    name: str
    value: str

class SubStatementDataTypeDef(TypedDict):
    Id: str
    CreatedAt: NotRequired[datetime]
    Duration: NotRequired[int]
    Error: NotRequired[str]
    HasResultSet: NotRequired[bool]
    QueryString: NotRequired[str]
    RedshiftQueryId: NotRequired[int]
    ResultRows: NotRequired[int]
    ResultSize: NotRequired[int]
    Status: NotRequired[StatementStatusStringType]
    UpdatedAt: NotRequired[datetime]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeTableRequestRequestTypeDef(TypedDict):
    Database: str
    ClusterIdentifier: NotRequired[str]
    ConnectedDatabase: NotRequired[str]
    DbUser: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Schema: NotRequired[str]
    SecretArn: NotRequired[str]
    Table: NotRequired[str]
    WorkgroupName: NotRequired[str]

class FieldTypeDef(TypedDict):
    blobValue: NotRequired[bytes]
    booleanValue: NotRequired[bool]
    doubleValue: NotRequired[float]
    isNull: NotRequired[bool]
    longValue: NotRequired[int]
    stringValue: NotRequired[str]

class GetStatementResultRequestRequestTypeDef(TypedDict):
    Id: str
    NextToken: NotRequired[str]

class GetStatementResultV2RequestRequestTypeDef(TypedDict):
    Id: str
    NextToken: NotRequired[str]

class QueryRecordsTypeDef(TypedDict):
    CSVRecords: NotRequired[str]

class ListDatabasesRequestRequestTypeDef(TypedDict):
    Database: str
    ClusterIdentifier: NotRequired[str]
    DbUser: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    SecretArn: NotRequired[str]
    WorkgroupName: NotRequired[str]

class ListSchemasRequestRequestTypeDef(TypedDict):
    Database: str
    ClusterIdentifier: NotRequired[str]
    ConnectedDatabase: NotRequired[str]
    DbUser: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    SchemaPattern: NotRequired[str]
    SecretArn: NotRequired[str]
    WorkgroupName: NotRequired[str]

class ListStatementsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    RoleLevel: NotRequired[bool]
    StatementName: NotRequired[str]
    Status: NotRequired[StatusStringType]

class ListTablesRequestRequestTypeDef(TypedDict):
    Database: str
    ClusterIdentifier: NotRequired[str]
    ConnectedDatabase: NotRequired[str]
    DbUser: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    SchemaPattern: NotRequired[str]
    SecretArn: NotRequired[str]
    TablePattern: NotRequired[str]
    WorkgroupName: NotRequired[str]

TableMemberTypeDef = TypedDict(
    "TableMemberTypeDef",
    {
        "name": NotRequired[str],
        "schema": NotRequired[str],
        "type": NotRequired[str],
    },
)

class BatchExecuteStatementOutputTypeDef(TypedDict):
    ClusterIdentifier: str
    CreatedAt: datetime
    Database: str
    DbGroups: List[str]
    DbUser: str
    Id: str
    SecretArn: str
    SessionId: str
    WorkgroupName: str
    ResponseMetadata: ResponseMetadataTypeDef

class CancelStatementResponseTypeDef(TypedDict):
    Status: bool
    ResponseMetadata: ResponseMetadataTypeDef

class ExecuteStatementOutputTypeDef(TypedDict):
    ClusterIdentifier: str
    CreatedAt: datetime
    Database: str
    DbGroups: List[str]
    DbUser: str
    Id: str
    SecretArn: str
    SessionId: str
    WorkgroupName: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListDatabasesResponseTypeDef(TypedDict):
    Databases: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListSchemasResponseTypeDef(TypedDict):
    Schemas: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeTableResponseTypeDef(TypedDict):
    ColumnList: List[ColumnMetadataTypeDef]
    TableName: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ExecuteStatementInputRequestTypeDef(TypedDict):
    Sql: str
    ClientToken: NotRequired[str]
    ClusterIdentifier: NotRequired[str]
    Database: NotRequired[str]
    DbUser: NotRequired[str]
    Parameters: NotRequired[Sequence[SqlParameterTypeDef]]
    ResultFormat: NotRequired[ResultFormatStringType]
    SecretArn: NotRequired[str]
    SessionId: NotRequired[str]
    SessionKeepAliveSeconds: NotRequired[int]
    StatementName: NotRequired[str]
    WithEvent: NotRequired[bool]
    WorkgroupName: NotRequired[str]

class StatementDataTypeDef(TypedDict):
    Id: str
    CreatedAt: NotRequired[datetime]
    IsBatchStatement: NotRequired[bool]
    QueryParameters: NotRequired[List[SqlParameterTypeDef]]
    QueryString: NotRequired[str]
    QueryStrings: NotRequired[List[str]]
    ResultFormat: NotRequired[ResultFormatStringType]
    SecretArn: NotRequired[str]
    SessionId: NotRequired[str]
    StatementName: NotRequired[str]
    Status: NotRequired[StatusStringType]
    UpdatedAt: NotRequired[datetime]

class DescribeStatementResponseTypeDef(TypedDict):
    ClusterIdentifier: str
    CreatedAt: datetime
    Database: str
    DbUser: str
    Duration: int
    Error: str
    HasResultSet: bool
    Id: str
    QueryParameters: List[SqlParameterTypeDef]
    QueryString: str
    RedshiftPid: int
    RedshiftQueryId: int
    ResultFormat: ResultFormatStringType
    ResultRows: int
    ResultSize: int
    SecretArn: str
    SessionId: str
    Status: StatusStringType
    SubStatements: List[SubStatementDataTypeDef]
    UpdatedAt: datetime
    WorkgroupName: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeTableRequestDescribeTablePaginateTypeDef(TypedDict):
    Database: str
    ClusterIdentifier: NotRequired[str]
    ConnectedDatabase: NotRequired[str]
    DbUser: NotRequired[str]
    Schema: NotRequired[str]
    SecretArn: NotRequired[str]
    Table: NotRequired[str]
    WorkgroupName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetStatementResultRequestGetStatementResultPaginateTypeDef(TypedDict):
    Id: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetStatementResultV2RequestGetStatementResultV2PaginateTypeDef(TypedDict):
    Id: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDatabasesRequestListDatabasesPaginateTypeDef(TypedDict):
    Database: str
    ClusterIdentifier: NotRequired[str]
    DbUser: NotRequired[str]
    SecretArn: NotRequired[str]
    WorkgroupName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSchemasRequestListSchemasPaginateTypeDef(TypedDict):
    Database: str
    ClusterIdentifier: NotRequired[str]
    ConnectedDatabase: NotRequired[str]
    DbUser: NotRequired[str]
    SchemaPattern: NotRequired[str]
    SecretArn: NotRequired[str]
    WorkgroupName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListStatementsRequestListStatementsPaginateTypeDef(TypedDict):
    RoleLevel: NotRequired[bool]
    StatementName: NotRequired[str]
    Status: NotRequired[StatusStringType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTablesRequestListTablesPaginateTypeDef(TypedDict):
    Database: str
    ClusterIdentifier: NotRequired[str]
    ConnectedDatabase: NotRequired[str]
    DbUser: NotRequired[str]
    SchemaPattern: NotRequired[str]
    SecretArn: NotRequired[str]
    TablePattern: NotRequired[str]
    WorkgroupName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetStatementResultResponseTypeDef(TypedDict):
    ColumnMetadata: List[ColumnMetadataTypeDef]
    Records: List[List[FieldTypeDef]]
    TotalNumRows: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetStatementResultV2ResponseTypeDef(TypedDict):
    ColumnMetadata: List[ColumnMetadataTypeDef]
    Records: List[QueryRecordsTypeDef]
    ResultFormat: ResultFormatStringType
    TotalNumRows: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTablesResponseTypeDef(TypedDict):
    Tables: List[TableMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListStatementsResponseTypeDef(TypedDict):
    Statements: List[StatementDataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
