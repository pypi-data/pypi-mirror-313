"""
Type annotations for rds-data service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds_data/type_defs/)

Usage::

    ```python
    from mypy_boto3_rds_data.type_defs import ArrayValueOutputTypeDef

    data: ArrayValueOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import DecimalReturnTypeType, LongReturnTypeType, RecordsFormatTypeType, TypeHintType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ArrayValueOutputTypeDef",
    "ArrayValueTypeDef",
    "ArrayValueUnionTypeDef",
    "BatchExecuteStatementRequestRequestTypeDef",
    "BatchExecuteStatementResponseTypeDef",
    "BeginTransactionRequestRequestTypeDef",
    "BeginTransactionResponseTypeDef",
    "BlobTypeDef",
    "ColumnMetadataTypeDef",
    "CommitTransactionRequestRequestTypeDef",
    "CommitTransactionResponseTypeDef",
    "ExecuteSqlRequestRequestTypeDef",
    "ExecuteSqlResponseTypeDef",
    "ExecuteStatementRequestRequestTypeDef",
    "ExecuteStatementResponseTypeDef",
    "FieldOutputTypeDef",
    "FieldTypeDef",
    "FieldUnionTypeDef",
    "RecordTypeDef",
    "ResponseMetadataTypeDef",
    "ResultFrameTypeDef",
    "ResultSetMetadataTypeDef",
    "ResultSetOptionsTypeDef",
    "RollbackTransactionRequestRequestTypeDef",
    "RollbackTransactionResponseTypeDef",
    "SqlParameterTypeDef",
    "SqlStatementResultTypeDef",
    "StructValueTypeDef",
    "UpdateResultTypeDef",
    "ValueTypeDef",
)

class ArrayValueOutputTypeDef(TypedDict):
    booleanValues: NotRequired[List[bool]]
    longValues: NotRequired[List[int]]
    doubleValues: NotRequired[List[float]]
    stringValues: NotRequired[List[str]]
    arrayValues: NotRequired[List[Dict[str, Any]]]

class ArrayValueTypeDef(TypedDict):
    booleanValues: NotRequired[Sequence[bool]]
    longValues: NotRequired[Sequence[int]]
    doubleValues: NotRequired[Sequence[float]]
    stringValues: NotRequired[Sequence[str]]
    arrayValues: NotRequired[Sequence[Mapping[str, Any]]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BeginTransactionRequestRequestTypeDef(TypedDict):
    resourceArn: str
    secretArn: str
    database: NotRequired[str]
    schema: NotRequired[str]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
ColumnMetadataTypeDef = TypedDict(
    "ColumnMetadataTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[int],
        "typeName": NotRequired[str],
        "label": NotRequired[str],
        "schemaName": NotRequired[str],
        "tableName": NotRequired[str],
        "isAutoIncrement": NotRequired[bool],
        "isSigned": NotRequired[bool],
        "isCurrency": NotRequired[bool],
        "isCaseSensitive": NotRequired[bool],
        "nullable": NotRequired[int],
        "precision": NotRequired[int],
        "scale": NotRequired[int],
        "arrayBaseColumnType": NotRequired[int],
    },
)

class CommitTransactionRequestRequestTypeDef(TypedDict):
    resourceArn: str
    secretArn: str
    transactionId: str

class ExecuteSqlRequestRequestTypeDef(TypedDict):
    dbClusterOrInstanceArn: str
    awsSecretStoreArn: str
    sqlStatements: str
    database: NotRequired[str]
    schema: NotRequired[str]

class ResultSetOptionsTypeDef(TypedDict):
    decimalReturnType: NotRequired[DecimalReturnTypeType]
    longReturnType: NotRequired[LongReturnTypeType]

class RollbackTransactionRequestRequestTypeDef(TypedDict):
    resourceArn: str
    secretArn: str
    transactionId: str

class StructValueTypeDef(TypedDict):
    attributes: NotRequired[List[Dict[str, Any]]]

class FieldOutputTypeDef(TypedDict):
    isNull: NotRequired[bool]
    booleanValue: NotRequired[bool]
    longValue: NotRequired[int]
    doubleValue: NotRequired[float]
    stringValue: NotRequired[str]
    blobValue: NotRequired[bytes]
    arrayValue: NotRequired[ArrayValueOutputTypeDef]

ArrayValueUnionTypeDef = Union[ArrayValueTypeDef, ArrayValueOutputTypeDef]

class BeginTransactionResponseTypeDef(TypedDict):
    transactionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CommitTransactionResponseTypeDef(TypedDict):
    transactionStatus: str
    ResponseMetadata: ResponseMetadataTypeDef

class RollbackTransactionResponseTypeDef(TypedDict):
    transactionStatus: str
    ResponseMetadata: ResponseMetadataTypeDef

class ResultSetMetadataTypeDef(TypedDict):
    columnCount: NotRequired[int]
    columnMetadata: NotRequired[List[ColumnMetadataTypeDef]]

class ValueTypeDef(TypedDict):
    isNull: NotRequired[bool]
    bitValue: NotRequired[bool]
    bigIntValue: NotRequired[int]
    intValue: NotRequired[int]
    doubleValue: NotRequired[float]
    realValue: NotRequired[float]
    stringValue: NotRequired[str]
    blobValue: NotRequired[bytes]
    arrayValues: NotRequired[List[Dict[str, Any]]]
    structValue: NotRequired[StructValueTypeDef]

class ExecuteStatementResponseTypeDef(TypedDict):
    records: List[List[FieldOutputTypeDef]]
    columnMetadata: List[ColumnMetadataTypeDef]
    numberOfRecordsUpdated: int
    generatedFields: List[FieldOutputTypeDef]
    formattedRecords: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateResultTypeDef(TypedDict):
    generatedFields: NotRequired[List[FieldOutputTypeDef]]

class FieldTypeDef(TypedDict):
    isNull: NotRequired[bool]
    booleanValue: NotRequired[bool]
    longValue: NotRequired[int]
    doubleValue: NotRequired[float]
    stringValue: NotRequired[str]
    blobValue: NotRequired[BlobTypeDef]
    arrayValue: NotRequired[ArrayValueUnionTypeDef]

class RecordTypeDef(TypedDict):
    values: NotRequired[List[ValueTypeDef]]

class BatchExecuteStatementResponseTypeDef(TypedDict):
    updateResults: List[UpdateResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

FieldUnionTypeDef = Union[FieldTypeDef, FieldOutputTypeDef]

class ResultFrameTypeDef(TypedDict):
    resultSetMetadata: NotRequired[ResultSetMetadataTypeDef]
    records: NotRequired[List[RecordTypeDef]]

class SqlParameterTypeDef(TypedDict):
    name: NotRequired[str]
    value: NotRequired[FieldUnionTypeDef]
    typeHint: NotRequired[TypeHintType]

class SqlStatementResultTypeDef(TypedDict):
    resultFrame: NotRequired[ResultFrameTypeDef]
    numberOfRecordsUpdated: NotRequired[int]

class BatchExecuteStatementRequestRequestTypeDef(TypedDict):
    resourceArn: str
    secretArn: str
    sql: str
    database: NotRequired[str]
    schema: NotRequired[str]
    parameterSets: NotRequired[Sequence[Sequence[SqlParameterTypeDef]]]
    transactionId: NotRequired[str]

class ExecuteStatementRequestRequestTypeDef(TypedDict):
    resourceArn: str
    secretArn: str
    sql: str
    database: NotRequired[str]
    schema: NotRequired[str]
    parameters: NotRequired[Sequence[SqlParameterTypeDef]]
    transactionId: NotRequired[str]
    includeResultMetadata: NotRequired[bool]
    continueAfterTimeout: NotRequired[bool]
    resultSetOptions: NotRequired[ResultSetOptionsTypeDef]
    formatRecordsAs: NotRequired[RecordsFormatTypeType]

class ExecuteSqlResponseTypeDef(TypedDict):
    sqlStatementResults: List[SqlStatementResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
