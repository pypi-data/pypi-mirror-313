"""
Type annotations for datapipeline service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/type_defs/)

Usage::

    ```python
    from mypy_boto3_datapipeline.type_defs import ParameterValueTypeDef

    data: ParameterValueTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import OperatorTypeType, TaskStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "ActivatePipelineInputRequestTypeDef",
    "AddTagsInputRequestTypeDef",
    "CreatePipelineInputRequestTypeDef",
    "CreatePipelineOutputTypeDef",
    "DeactivatePipelineInputRequestTypeDef",
    "DeletePipelineInputRequestTypeDef",
    "DescribeObjectsInputDescribeObjectsPaginateTypeDef",
    "DescribeObjectsInputRequestTypeDef",
    "DescribeObjectsOutputTypeDef",
    "DescribePipelinesInputRequestTypeDef",
    "DescribePipelinesOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EvaluateExpressionInputRequestTypeDef",
    "EvaluateExpressionOutputTypeDef",
    "FieldTypeDef",
    "GetPipelineDefinitionInputRequestTypeDef",
    "GetPipelineDefinitionOutputTypeDef",
    "InstanceIdentityTypeDef",
    "ListPipelinesInputListPipelinesPaginateTypeDef",
    "ListPipelinesInputRequestTypeDef",
    "ListPipelinesOutputTypeDef",
    "OperatorTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterAttributeTypeDef",
    "ParameterObjectOutputTypeDef",
    "ParameterObjectTypeDef",
    "ParameterObjectUnionTypeDef",
    "ParameterValueTypeDef",
    "PipelineDescriptionTypeDef",
    "PipelineIdNameTypeDef",
    "PipelineObjectOutputTypeDef",
    "PipelineObjectTypeDef",
    "PipelineObjectUnionTypeDef",
    "PollForTaskInputRequestTypeDef",
    "PollForTaskOutputTypeDef",
    "PutPipelineDefinitionInputRequestTypeDef",
    "PutPipelineDefinitionOutputTypeDef",
    "QueryObjectsInputQueryObjectsPaginateTypeDef",
    "QueryObjectsInputRequestTypeDef",
    "QueryObjectsOutputTypeDef",
    "QueryTypeDef",
    "RemoveTagsInputRequestTypeDef",
    "ReportTaskProgressInputRequestTypeDef",
    "ReportTaskProgressOutputTypeDef",
    "ReportTaskRunnerHeartbeatInputRequestTypeDef",
    "ReportTaskRunnerHeartbeatOutputTypeDef",
    "ResponseMetadataTypeDef",
    "SelectorTypeDef",
    "SetStatusInputRequestTypeDef",
    "SetTaskStatusInputRequestTypeDef",
    "TagTypeDef",
    "TaskObjectTypeDef",
    "TimestampTypeDef",
    "ValidatePipelineDefinitionInputRequestTypeDef",
    "ValidatePipelineDefinitionOutputTypeDef",
    "ValidationErrorTypeDef",
    "ValidationWarningTypeDef",
)

ParameterValueTypeDef = TypedDict(
    "ParameterValueTypeDef",
    {
        "id": str,
        "stringValue": str,
    },
)
TimestampTypeDef = Union[datetime, str]


class TagTypeDef(TypedDict):
    key: str
    value: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeactivatePipelineInputRequestTypeDef(TypedDict):
    pipelineId: str
    cancelActive: NotRequired[bool]


class DeletePipelineInputRequestTypeDef(TypedDict):
    pipelineId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeObjectsInputRequestTypeDef(TypedDict):
    pipelineId: str
    objectIds: Sequence[str]
    evaluateExpressions: NotRequired[bool]
    marker: NotRequired[str]


class DescribePipelinesInputRequestTypeDef(TypedDict):
    pipelineIds: Sequence[str]


class EvaluateExpressionInputRequestTypeDef(TypedDict):
    pipelineId: str
    objectId: str
    expression: str


class FieldTypeDef(TypedDict):
    key: str
    stringValue: NotRequired[str]
    refValue: NotRequired[str]


class GetPipelineDefinitionInputRequestTypeDef(TypedDict):
    pipelineId: str
    version: NotRequired[str]


class InstanceIdentityTypeDef(TypedDict):
    document: NotRequired[str]
    signature: NotRequired[str]


class ListPipelinesInputRequestTypeDef(TypedDict):
    marker: NotRequired[str]


PipelineIdNameTypeDef = TypedDict(
    "PipelineIdNameTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)
OperatorTypeDef = TypedDict(
    "OperatorTypeDef",
    {
        "type": NotRequired[OperatorTypeType],
        "values": NotRequired[Sequence[str]],
    },
)


class ParameterAttributeTypeDef(TypedDict):
    key: str
    stringValue: str


ValidationErrorTypeDef = TypedDict(
    "ValidationErrorTypeDef",
    {
        "id": NotRequired[str],
        "errors": NotRequired[List[str]],
    },
)
ValidationWarningTypeDef = TypedDict(
    "ValidationWarningTypeDef",
    {
        "id": NotRequired[str],
        "warnings": NotRequired[List[str]],
    },
)


class RemoveTagsInputRequestTypeDef(TypedDict):
    pipelineId: str
    tagKeys: Sequence[str]


class ReportTaskRunnerHeartbeatInputRequestTypeDef(TypedDict):
    taskrunnerId: str
    workerGroup: NotRequired[str]
    hostname: NotRequired[str]


class SetStatusInputRequestTypeDef(TypedDict):
    pipelineId: str
    objectIds: Sequence[str]
    status: str


class SetTaskStatusInputRequestTypeDef(TypedDict):
    taskId: str
    taskStatus: TaskStatusType
    errorId: NotRequired[str]
    errorMessage: NotRequired[str]
    errorStackTrace: NotRequired[str]


class ActivatePipelineInputRequestTypeDef(TypedDict):
    pipelineId: str
    parameterValues: NotRequired[Sequence[ParameterValueTypeDef]]
    startTimestamp: NotRequired[TimestampTypeDef]


class AddTagsInputRequestTypeDef(TypedDict):
    pipelineId: str
    tags: Sequence[TagTypeDef]


class CreatePipelineInputRequestTypeDef(TypedDict):
    name: str
    uniqueId: str
    description: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreatePipelineOutputTypeDef(TypedDict):
    pipelineId: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class EvaluateExpressionOutputTypeDef(TypedDict):
    evaluatedExpression: str
    ResponseMetadata: ResponseMetadataTypeDef


class QueryObjectsOutputTypeDef(TypedDict):
    ids: List[str]
    marker: str
    hasMoreResults: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ReportTaskProgressOutputTypeDef(TypedDict):
    canceled: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ReportTaskRunnerHeartbeatOutputTypeDef(TypedDict):
    terminate: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeObjectsInputDescribeObjectsPaginateTypeDef(TypedDict):
    pipelineId: str
    objectIds: Sequence[str]
    evaluateExpressions: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPipelinesInputListPipelinesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class PipelineDescriptionTypeDef(TypedDict):
    pipelineId: str
    name: str
    fields: List[FieldTypeDef]
    description: NotRequired[str]
    tags: NotRequired[List[TagTypeDef]]


PipelineObjectOutputTypeDef = TypedDict(
    "PipelineObjectOutputTypeDef",
    {
        "id": str,
        "name": str,
        "fields": List[FieldTypeDef],
    },
)
PipelineObjectTypeDef = TypedDict(
    "PipelineObjectTypeDef",
    {
        "id": str,
        "name": str,
        "fields": Sequence[FieldTypeDef],
    },
)


class ReportTaskProgressInputRequestTypeDef(TypedDict):
    taskId: str
    fields: NotRequired[Sequence[FieldTypeDef]]


class PollForTaskInputRequestTypeDef(TypedDict):
    workerGroup: str
    hostname: NotRequired[str]
    instanceIdentity: NotRequired[InstanceIdentityTypeDef]


class ListPipelinesOutputTypeDef(TypedDict):
    pipelineIdList: List[PipelineIdNameTypeDef]
    marker: str
    hasMoreResults: bool
    ResponseMetadata: ResponseMetadataTypeDef


SelectorTypeDef = TypedDict(
    "SelectorTypeDef",
    {
        "fieldName": NotRequired[str],
        "operator": NotRequired[OperatorTypeDef],
    },
)
ParameterObjectOutputTypeDef = TypedDict(
    "ParameterObjectOutputTypeDef",
    {
        "id": str,
        "attributes": List[ParameterAttributeTypeDef],
    },
)
ParameterObjectTypeDef = TypedDict(
    "ParameterObjectTypeDef",
    {
        "id": str,
        "attributes": Sequence[ParameterAttributeTypeDef],
    },
)


class PutPipelineDefinitionOutputTypeDef(TypedDict):
    validationErrors: List[ValidationErrorTypeDef]
    validationWarnings: List[ValidationWarningTypeDef]
    errored: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ValidatePipelineDefinitionOutputTypeDef(TypedDict):
    validationErrors: List[ValidationErrorTypeDef]
    validationWarnings: List[ValidationWarningTypeDef]
    errored: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePipelinesOutputTypeDef(TypedDict):
    pipelineDescriptionList: List[PipelineDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeObjectsOutputTypeDef(TypedDict):
    pipelineObjects: List[PipelineObjectOutputTypeDef]
    marker: str
    hasMoreResults: bool
    ResponseMetadata: ResponseMetadataTypeDef


class TaskObjectTypeDef(TypedDict):
    taskId: NotRequired[str]
    pipelineId: NotRequired[str]
    attemptId: NotRequired[str]
    objects: NotRequired[Dict[str, PipelineObjectOutputTypeDef]]


PipelineObjectUnionTypeDef = Union[PipelineObjectTypeDef, PipelineObjectOutputTypeDef]


class QueryTypeDef(TypedDict):
    selectors: NotRequired[Sequence[SelectorTypeDef]]


class GetPipelineDefinitionOutputTypeDef(TypedDict):
    pipelineObjects: List[PipelineObjectOutputTypeDef]
    parameterObjects: List[ParameterObjectOutputTypeDef]
    parameterValues: List[ParameterValueTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


ParameterObjectUnionTypeDef = Union[ParameterObjectTypeDef, ParameterObjectOutputTypeDef]


class ValidatePipelineDefinitionInputRequestTypeDef(TypedDict):
    pipelineId: str
    pipelineObjects: Sequence[PipelineObjectTypeDef]
    parameterObjects: NotRequired[Sequence[ParameterObjectTypeDef]]
    parameterValues: NotRequired[Sequence[ParameterValueTypeDef]]


class PollForTaskOutputTypeDef(TypedDict):
    taskObject: TaskObjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class QueryObjectsInputQueryObjectsPaginateTypeDef(TypedDict):
    pipelineId: str
    sphere: str
    query: NotRequired[QueryTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class QueryObjectsInputRequestTypeDef(TypedDict):
    pipelineId: str
    sphere: str
    query: NotRequired[QueryTypeDef]
    marker: NotRequired[str]
    limit: NotRequired[int]


class PutPipelineDefinitionInputRequestTypeDef(TypedDict):
    pipelineId: str
    pipelineObjects: Sequence[PipelineObjectUnionTypeDef]
    parameterObjects: NotRequired[Sequence[ParameterObjectUnionTypeDef]]
    parameterValues: NotRequired[Sequence[ParameterValueTypeDef]]
