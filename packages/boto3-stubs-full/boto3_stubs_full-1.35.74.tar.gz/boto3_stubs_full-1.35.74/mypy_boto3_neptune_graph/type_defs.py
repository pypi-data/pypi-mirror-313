"""
Type annotations for neptune-graph service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/type_defs/)

Usage::

    ```python
    from mypy_boto3_neptune_graph.type_defs import CancelExportTaskInputRequestTypeDef

    data: CancelExportTaskInputRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ExplainModeType,
    ExportFormatType,
    ExportTaskStatusType,
    FormatType,
    GraphStatusType,
    GraphSummaryModeType,
    ImportTaskStatusType,
    MultiValueHandlingTypeType,
    PlanCacheTypeType,
    PrivateGraphEndpointStatusType,
    QueryStateInputType,
    QueryStateType,
    SnapshotStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "CancelExportTaskInputRequestTypeDef",
    "CancelExportTaskOutputTypeDef",
    "CancelImportTaskInputRequestTypeDef",
    "CancelImportTaskOutputTypeDef",
    "CancelQueryInputRequestTypeDef",
    "CreateGraphInputRequestTypeDef",
    "CreateGraphOutputTypeDef",
    "CreateGraphSnapshotInputRequestTypeDef",
    "CreateGraphSnapshotOutputTypeDef",
    "CreateGraphUsingImportTaskInputRequestTypeDef",
    "CreateGraphUsingImportTaskOutputTypeDef",
    "CreatePrivateGraphEndpointInputRequestTypeDef",
    "CreatePrivateGraphEndpointOutputTypeDef",
    "DeleteGraphInputRequestTypeDef",
    "DeleteGraphOutputTypeDef",
    "DeleteGraphSnapshotInputRequestTypeDef",
    "DeleteGraphSnapshotOutputTypeDef",
    "DeletePrivateGraphEndpointInputRequestTypeDef",
    "DeletePrivateGraphEndpointOutputTypeDef",
    "EdgeStructureTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExecuteQueryInputRequestTypeDef",
    "ExecuteQueryOutputTypeDef",
    "ExportFilterElementOutputTypeDef",
    "ExportFilterElementTypeDef",
    "ExportFilterElementUnionTypeDef",
    "ExportFilterOutputTypeDef",
    "ExportFilterPropertyAttributesTypeDef",
    "ExportFilterTypeDef",
    "ExportTaskDetailsTypeDef",
    "ExportTaskSummaryTypeDef",
    "GetExportTaskInputExportTaskCancelledWaitTypeDef",
    "GetExportTaskInputExportTaskSuccessfulWaitTypeDef",
    "GetExportTaskInputRequestTypeDef",
    "GetExportTaskOutputTypeDef",
    "GetGraphInputGraphAvailableWaitTypeDef",
    "GetGraphInputGraphDeletedWaitTypeDef",
    "GetGraphInputRequestTypeDef",
    "GetGraphOutputTypeDef",
    "GetGraphSnapshotInputGraphSnapshotAvailableWaitTypeDef",
    "GetGraphSnapshotInputGraphSnapshotDeletedWaitTypeDef",
    "GetGraphSnapshotInputRequestTypeDef",
    "GetGraphSnapshotOutputTypeDef",
    "GetGraphSummaryInputRequestTypeDef",
    "GetGraphSummaryOutputTypeDef",
    "GetImportTaskInputImportTaskCancelledWaitTypeDef",
    "GetImportTaskInputImportTaskSuccessfulWaitTypeDef",
    "GetImportTaskInputRequestTypeDef",
    "GetImportTaskOutputTypeDef",
    "GetPrivateGraphEndpointInputPrivateGraphEndpointAvailableWaitTypeDef",
    "GetPrivateGraphEndpointInputPrivateGraphEndpointDeletedWaitTypeDef",
    "GetPrivateGraphEndpointInputRequestTypeDef",
    "GetPrivateGraphEndpointOutputTypeDef",
    "GetQueryInputRequestTypeDef",
    "GetQueryOutputTypeDef",
    "GraphDataSummaryTypeDef",
    "GraphSnapshotSummaryTypeDef",
    "GraphSummaryTypeDef",
    "ImportOptionsTypeDef",
    "ImportTaskDetailsTypeDef",
    "ImportTaskSummaryTypeDef",
    "ListExportTasksInputListExportTasksPaginateTypeDef",
    "ListExportTasksInputRequestTypeDef",
    "ListExportTasksOutputTypeDef",
    "ListGraphSnapshotsInputListGraphSnapshotsPaginateTypeDef",
    "ListGraphSnapshotsInputRequestTypeDef",
    "ListGraphSnapshotsOutputTypeDef",
    "ListGraphsInputListGraphsPaginateTypeDef",
    "ListGraphsInputRequestTypeDef",
    "ListGraphsOutputTypeDef",
    "ListImportTasksInputListImportTasksPaginateTypeDef",
    "ListImportTasksInputRequestTypeDef",
    "ListImportTasksOutputTypeDef",
    "ListPrivateGraphEndpointsInputListPrivateGraphEndpointsPaginateTypeDef",
    "ListPrivateGraphEndpointsInputRequestTypeDef",
    "ListPrivateGraphEndpointsOutputTypeDef",
    "ListQueriesInputRequestTypeDef",
    "ListQueriesOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "NeptuneImportOptionsTypeDef",
    "NodeStructureTypeDef",
    "PaginatorConfigTypeDef",
    "PrivateGraphEndpointSummaryTypeDef",
    "QuerySummaryTypeDef",
    "ResetGraphInputRequestTypeDef",
    "ResetGraphOutputTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreGraphFromSnapshotInputRequestTypeDef",
    "RestoreGraphFromSnapshotOutputTypeDef",
    "StartExportTaskInputRequestTypeDef",
    "StartExportTaskOutputTypeDef",
    "StartImportTaskInputRequestTypeDef",
    "StartImportTaskOutputTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateGraphInputRequestTypeDef",
    "UpdateGraphOutputTypeDef",
    "VectorSearchConfigurationTypeDef",
    "WaiterConfigTypeDef",
)


class CancelExportTaskInputRequestTypeDef(TypedDict):
    taskIdentifier: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CancelImportTaskInputRequestTypeDef(TypedDict):
    taskIdentifier: str


class CancelQueryInputRequestTypeDef(TypedDict):
    graphIdentifier: str
    queryId: str


class VectorSearchConfigurationTypeDef(TypedDict):
    dimension: int


class CreateGraphSnapshotInputRequestTypeDef(TypedDict):
    graphIdentifier: str
    snapshotName: str
    tags: NotRequired[Mapping[str, str]]


class CreatePrivateGraphEndpointInputRequestTypeDef(TypedDict):
    graphIdentifier: str
    vpcId: NotRequired[str]
    subnetIds: NotRequired[Sequence[str]]
    vpcSecurityGroupIds: NotRequired[Sequence[str]]


class DeleteGraphInputRequestTypeDef(TypedDict):
    graphIdentifier: str
    skipSnapshot: bool


class DeleteGraphSnapshotInputRequestTypeDef(TypedDict):
    snapshotIdentifier: str


class DeletePrivateGraphEndpointInputRequestTypeDef(TypedDict):
    graphIdentifier: str
    vpcId: str


class EdgeStructureTypeDef(TypedDict):
    count: NotRequired[int]
    edgeProperties: NotRequired[List[str]]


class ExecuteQueryInputRequestTypeDef(TypedDict):
    graphIdentifier: str
    queryString: str
    language: Literal["OPEN_CYPHER"]
    parameters: NotRequired[Mapping[str, Mapping[str, Any]]]
    planCache: NotRequired[PlanCacheTypeType]
    explainMode: NotRequired[ExplainModeType]
    queryTimeoutMilliseconds: NotRequired[int]


class ExportFilterPropertyAttributesTypeDef(TypedDict):
    outputType: NotRequired[str]
    sourcePropertyName: NotRequired[str]
    multiValueHandling: NotRequired[MultiValueHandlingTypeType]


class ExportTaskDetailsTypeDef(TypedDict):
    startTime: datetime
    timeElapsedSeconds: int
    progressPercentage: int
    numVerticesWritten: NotRequired[int]
    numEdgesWritten: NotRequired[int]


ExportTaskSummaryTypeDef = TypedDict(
    "ExportTaskSummaryTypeDef",
    {
        "graphId": str,
        "roleArn": str,
        "taskId": str,
        "status": ExportTaskStatusType,
        "format": ExportFormatType,
        "destination": str,
        "kmsKeyIdentifier": str,
        "parquetType": NotRequired[Literal["COLUMNAR"]],
        "statusReason": NotRequired[str],
    },
)


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class GetExportTaskInputRequestTypeDef(TypedDict):
    taskIdentifier: str


class GetGraphInputRequestTypeDef(TypedDict):
    graphIdentifier: str


class GetGraphSnapshotInputRequestTypeDef(TypedDict):
    snapshotIdentifier: str


class GetGraphSummaryInputRequestTypeDef(TypedDict):
    graphIdentifier: str
    mode: NotRequired[GraphSummaryModeType]


class GetImportTaskInputRequestTypeDef(TypedDict):
    taskIdentifier: str


class ImportTaskDetailsTypeDef(TypedDict):
    status: str
    startTime: datetime
    timeElapsedSeconds: int
    progressPercentage: int
    errorCount: int
    statementCount: int
    dictionaryEntryCount: int
    errorDetails: NotRequired[str]


class GetPrivateGraphEndpointInputRequestTypeDef(TypedDict):
    graphIdentifier: str
    vpcId: str


class GetQueryInputRequestTypeDef(TypedDict):
    graphIdentifier: str
    queryId: str


class NodeStructureTypeDef(TypedDict):
    count: NotRequired[int]
    nodeProperties: NotRequired[List[str]]
    distinctOutgoingEdgeLabels: NotRequired[List[str]]


GraphSnapshotSummaryTypeDef = TypedDict(
    "GraphSnapshotSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "sourceGraphId": NotRequired[str],
        "snapshotCreateTime": NotRequired[datetime],
        "status": NotRequired[SnapshotStatusType],
        "kmsKeyIdentifier": NotRequired[str],
    },
)
GraphSummaryTypeDef = TypedDict(
    "GraphSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": NotRequired[GraphStatusType],
        "provisionedMemory": NotRequired[int],
        "publicConnectivity": NotRequired[bool],
        "endpoint": NotRequired[str],
        "replicaCount": NotRequired[int],
        "kmsKeyIdentifier": NotRequired[str],
        "deletionProtection": NotRequired[bool],
    },
)


class NeptuneImportOptionsTypeDef(TypedDict):
    s3ExportPath: str
    s3ExportKmsKeyId: str
    preserveDefaultVertexLabels: NotRequired[bool]
    preserveEdgeIds: NotRequired[bool]


ImportTaskSummaryTypeDef = TypedDict(
    "ImportTaskSummaryTypeDef",
    {
        "taskId": str,
        "source": str,
        "roleArn": str,
        "status": ImportTaskStatusType,
        "graphId": NotRequired[str],
        "format": NotRequired[FormatType],
        "parquetType": NotRequired[Literal["COLUMNAR"]],
    },
)


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListExportTasksInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListGraphSnapshotsInputRequestTypeDef(TypedDict):
    graphIdentifier: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListGraphsInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListImportTasksInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListPrivateGraphEndpointsInputRequestTypeDef(TypedDict):
    graphIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class PrivateGraphEndpointSummaryTypeDef(TypedDict):
    vpcId: str
    subnetIds: List[str]
    status: PrivateGraphEndpointStatusType
    vpcEndpointId: NotRequired[str]


class ListQueriesInputRequestTypeDef(TypedDict):
    graphIdentifier: str
    maxResults: int
    state: NotRequired[QueryStateInputType]


QuerySummaryTypeDef = TypedDict(
    "QuerySummaryTypeDef",
    {
        "id": NotRequired[str],
        "queryString": NotRequired[str],
        "waited": NotRequired[int],
        "elapsed": NotRequired[int],
        "state": NotRequired[QueryStateType],
    },
)


class ListTagsForResourceInputRequestTypeDef(TypedDict):
    resourceArn: str


class ResetGraphInputRequestTypeDef(TypedDict):
    graphIdentifier: str
    skipSnapshot: bool


class RestoreGraphFromSnapshotInputRequestTypeDef(TypedDict):
    snapshotIdentifier: str
    graphName: str
    provisionedMemory: NotRequired[int]
    deletionProtection: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]
    replicaCount: NotRequired[int]
    publicConnectivity: NotRequired[bool]


class TagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateGraphInputRequestTypeDef(TypedDict):
    graphIdentifier: str
    publicConnectivity: NotRequired[bool]
    provisionedMemory: NotRequired[int]
    deletionProtection: NotRequired[bool]


CancelExportTaskOutputTypeDef = TypedDict(
    "CancelExportTaskOutputTypeDef",
    {
        "graphId": str,
        "roleArn": str,
        "taskId": str,
        "status": ExportTaskStatusType,
        "format": ExportFormatType,
        "destination": str,
        "kmsKeyIdentifier": str,
        "parquetType": Literal["COLUMNAR"],
        "statusReason": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CancelImportTaskOutputTypeDef = TypedDict(
    "CancelImportTaskOutputTypeDef",
    {
        "graphId": str,
        "taskId": str,
        "source": str,
        "format": FormatType,
        "parquetType": Literal["COLUMNAR"],
        "roleArn": str,
        "status": ImportTaskStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateGraphSnapshotOutputTypeDef = TypedDict(
    "CreateGraphSnapshotOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "sourceGraphId": str,
        "snapshotCreateTime": datetime,
        "status": SnapshotStatusType,
        "kmsKeyIdentifier": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class CreatePrivateGraphEndpointOutputTypeDef(TypedDict):
    vpcId: str
    subnetIds: List[str]
    status: PrivateGraphEndpointStatusType
    vpcEndpointId: str
    ResponseMetadata: ResponseMetadataTypeDef


DeleteGraphSnapshotOutputTypeDef = TypedDict(
    "DeleteGraphSnapshotOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "sourceGraphId": str,
        "snapshotCreateTime": datetime,
        "status": SnapshotStatusType,
        "kmsKeyIdentifier": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class DeletePrivateGraphEndpointOutputTypeDef(TypedDict):
    vpcId: str
    subnetIds: List[str]
    status: PrivateGraphEndpointStatusType
    vpcEndpointId: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ExecuteQueryOutputTypeDef(TypedDict):
    payload: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef


GetGraphSnapshotOutputTypeDef = TypedDict(
    "GetGraphSnapshotOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "sourceGraphId": str,
        "snapshotCreateTime": datetime,
        "status": SnapshotStatusType,
        "kmsKeyIdentifier": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class GetPrivateGraphEndpointOutputTypeDef(TypedDict):
    vpcId: str
    subnetIds: List[str]
    status: PrivateGraphEndpointStatusType
    vpcEndpointId: str
    ResponseMetadata: ResponseMetadataTypeDef


GetQueryOutputTypeDef = TypedDict(
    "GetQueryOutputTypeDef",
    {
        "id": str,
        "queryString": str,
        "waited": int,
        "elapsed": int,
        "state": QueryStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateGraphInputRequestTypeDef(TypedDict):
    graphName: str
    provisionedMemory: int
    tags: NotRequired[Mapping[str, str]]
    publicConnectivity: NotRequired[bool]
    kmsKeyIdentifier: NotRequired[str]
    vectorSearchConfiguration: NotRequired[VectorSearchConfigurationTypeDef]
    replicaCount: NotRequired[int]
    deletionProtection: NotRequired[bool]


CreateGraphOutputTypeDef = TypedDict(
    "CreateGraphOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": GraphStatusType,
        "statusReason": str,
        "createTime": datetime,
        "provisionedMemory": int,
        "endpoint": str,
        "publicConnectivity": bool,
        "vectorSearchConfiguration": VectorSearchConfigurationTypeDef,
        "replicaCount": int,
        "kmsKeyIdentifier": str,
        "sourceSnapshotId": str,
        "deletionProtection": bool,
        "buildNumber": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteGraphOutputTypeDef = TypedDict(
    "DeleteGraphOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": GraphStatusType,
        "statusReason": str,
        "createTime": datetime,
        "provisionedMemory": int,
        "endpoint": str,
        "publicConnectivity": bool,
        "vectorSearchConfiguration": VectorSearchConfigurationTypeDef,
        "replicaCount": int,
        "kmsKeyIdentifier": str,
        "sourceSnapshotId": str,
        "deletionProtection": bool,
        "buildNumber": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetGraphOutputTypeDef = TypedDict(
    "GetGraphOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": GraphStatusType,
        "statusReason": str,
        "createTime": datetime,
        "provisionedMemory": int,
        "endpoint": str,
        "publicConnectivity": bool,
        "vectorSearchConfiguration": VectorSearchConfigurationTypeDef,
        "replicaCount": int,
        "kmsKeyIdentifier": str,
        "sourceSnapshotId": str,
        "deletionProtection": bool,
        "buildNumber": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ResetGraphOutputTypeDef = TypedDict(
    "ResetGraphOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": GraphStatusType,
        "statusReason": str,
        "createTime": datetime,
        "provisionedMemory": int,
        "endpoint": str,
        "publicConnectivity": bool,
        "vectorSearchConfiguration": VectorSearchConfigurationTypeDef,
        "replicaCount": int,
        "kmsKeyIdentifier": str,
        "sourceSnapshotId": str,
        "deletionProtection": bool,
        "buildNumber": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RestoreGraphFromSnapshotOutputTypeDef = TypedDict(
    "RestoreGraphFromSnapshotOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": GraphStatusType,
        "statusReason": str,
        "createTime": datetime,
        "provisionedMemory": int,
        "endpoint": str,
        "publicConnectivity": bool,
        "vectorSearchConfiguration": VectorSearchConfigurationTypeDef,
        "replicaCount": int,
        "kmsKeyIdentifier": str,
        "sourceSnapshotId": str,
        "deletionProtection": bool,
        "buildNumber": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateGraphOutputTypeDef = TypedDict(
    "UpdateGraphOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": GraphStatusType,
        "statusReason": str,
        "createTime": datetime,
        "provisionedMemory": int,
        "endpoint": str,
        "publicConnectivity": bool,
        "vectorSearchConfiguration": VectorSearchConfigurationTypeDef,
        "replicaCount": int,
        "kmsKeyIdentifier": str,
        "sourceSnapshotId": str,
        "deletionProtection": bool,
        "buildNumber": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ExportFilterElementOutputTypeDef(TypedDict):
    properties: NotRequired[Dict[str, ExportFilterPropertyAttributesTypeDef]]


class ExportFilterElementTypeDef(TypedDict):
    properties: NotRequired[Mapping[str, ExportFilterPropertyAttributesTypeDef]]


class ListExportTasksOutputTypeDef(TypedDict):
    tasks: List[ExportTaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetExportTaskInputExportTaskCancelledWaitTypeDef(TypedDict):
    taskIdentifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetExportTaskInputExportTaskSuccessfulWaitTypeDef(TypedDict):
    taskIdentifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetGraphInputGraphAvailableWaitTypeDef(TypedDict):
    graphIdentifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetGraphInputGraphDeletedWaitTypeDef(TypedDict):
    graphIdentifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetGraphSnapshotInputGraphSnapshotAvailableWaitTypeDef(TypedDict):
    snapshotIdentifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetGraphSnapshotInputGraphSnapshotDeletedWaitTypeDef(TypedDict):
    snapshotIdentifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetImportTaskInputImportTaskCancelledWaitTypeDef(TypedDict):
    taskIdentifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetImportTaskInputImportTaskSuccessfulWaitTypeDef(TypedDict):
    taskIdentifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetPrivateGraphEndpointInputPrivateGraphEndpointAvailableWaitTypeDef(TypedDict):
    graphIdentifier: str
    vpcId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetPrivateGraphEndpointInputPrivateGraphEndpointDeletedWaitTypeDef(TypedDict):
    graphIdentifier: str
    vpcId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GraphDataSummaryTypeDef(TypedDict):
    numNodes: NotRequired[int]
    numEdges: NotRequired[int]
    numNodeLabels: NotRequired[int]
    numEdgeLabels: NotRequired[int]
    nodeLabels: NotRequired[List[str]]
    edgeLabels: NotRequired[List[str]]
    numNodeProperties: NotRequired[int]
    numEdgeProperties: NotRequired[int]
    nodeProperties: NotRequired[List[Dict[str, int]]]
    edgeProperties: NotRequired[List[Dict[str, int]]]
    totalNodePropertyValues: NotRequired[int]
    totalEdgePropertyValues: NotRequired[int]
    nodeStructures: NotRequired[List[NodeStructureTypeDef]]
    edgeStructures: NotRequired[List[EdgeStructureTypeDef]]


class ListGraphSnapshotsOutputTypeDef(TypedDict):
    graphSnapshots: List[GraphSnapshotSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListGraphsOutputTypeDef(TypedDict):
    graphs: List[GraphSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ImportOptionsTypeDef(TypedDict):
    neptune: NotRequired[NeptuneImportOptionsTypeDef]


class ListImportTasksOutputTypeDef(TypedDict):
    tasks: List[ImportTaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListExportTasksInputListExportTasksPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGraphSnapshotsInputListGraphSnapshotsPaginateTypeDef(TypedDict):
    graphIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGraphsInputListGraphsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListImportTasksInputListImportTasksPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPrivateGraphEndpointsInputListPrivateGraphEndpointsPaginateTypeDef(TypedDict):
    graphIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPrivateGraphEndpointsOutputTypeDef(TypedDict):
    privateGraphEndpoints: List[PrivateGraphEndpointSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListQueriesOutputTypeDef(TypedDict):
    queries: List[QuerySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ExportFilterOutputTypeDef(TypedDict):
    vertexFilter: NotRequired[Dict[str, ExportFilterElementOutputTypeDef]]
    edgeFilter: NotRequired[Dict[str, ExportFilterElementOutputTypeDef]]


ExportFilterElementUnionTypeDef = Union[
    ExportFilterElementTypeDef, ExportFilterElementOutputTypeDef
]


class GetGraphSummaryOutputTypeDef(TypedDict):
    version: str
    lastStatisticsComputationTime: datetime
    graphSummary: GraphDataSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


CreateGraphUsingImportTaskInputRequestTypeDef = TypedDict(
    "CreateGraphUsingImportTaskInputRequestTypeDef",
    {
        "graphName": str,
        "source": str,
        "roleArn": str,
        "tags": NotRequired[Mapping[str, str]],
        "publicConnectivity": NotRequired[bool],
        "kmsKeyIdentifier": NotRequired[str],
        "vectorSearchConfiguration": NotRequired[VectorSearchConfigurationTypeDef],
        "replicaCount": NotRequired[int],
        "deletionProtection": NotRequired[bool],
        "importOptions": NotRequired[ImportOptionsTypeDef],
        "maxProvisionedMemory": NotRequired[int],
        "minProvisionedMemory": NotRequired[int],
        "failOnError": NotRequired[bool],
        "format": NotRequired[FormatType],
        "parquetType": NotRequired[Literal["COLUMNAR"]],
        "blankNodeHandling": NotRequired[Literal["convertToIri"]],
    },
)
CreateGraphUsingImportTaskOutputTypeDef = TypedDict(
    "CreateGraphUsingImportTaskOutputTypeDef",
    {
        "graphId": str,
        "taskId": str,
        "source": str,
        "format": FormatType,
        "parquetType": Literal["COLUMNAR"],
        "roleArn": str,
        "status": ImportTaskStatusType,
        "importOptions": ImportOptionsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetImportTaskOutputTypeDef = TypedDict(
    "GetImportTaskOutputTypeDef",
    {
        "graphId": str,
        "taskId": str,
        "source": str,
        "format": FormatType,
        "parquetType": Literal["COLUMNAR"],
        "roleArn": str,
        "status": ImportTaskStatusType,
        "importOptions": ImportOptionsTypeDef,
        "importTaskDetails": ImportTaskDetailsTypeDef,
        "attemptNumber": int,
        "statusReason": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartImportTaskInputRequestTypeDef = TypedDict(
    "StartImportTaskInputRequestTypeDef",
    {
        "source": str,
        "graphIdentifier": str,
        "roleArn": str,
        "importOptions": NotRequired[ImportOptionsTypeDef],
        "failOnError": NotRequired[bool],
        "format": NotRequired[FormatType],
        "parquetType": NotRequired[Literal["COLUMNAR"]],
        "blankNodeHandling": NotRequired[Literal["convertToIri"]],
    },
)
StartImportTaskOutputTypeDef = TypedDict(
    "StartImportTaskOutputTypeDef",
    {
        "graphId": str,
        "taskId": str,
        "source": str,
        "format": FormatType,
        "parquetType": Literal["COLUMNAR"],
        "roleArn": str,
        "status": ImportTaskStatusType,
        "importOptions": ImportOptionsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetExportTaskOutputTypeDef = TypedDict(
    "GetExportTaskOutputTypeDef",
    {
        "graphId": str,
        "roleArn": str,
        "taskId": str,
        "status": ExportTaskStatusType,
        "format": ExportFormatType,
        "destination": str,
        "kmsKeyIdentifier": str,
        "parquetType": Literal["COLUMNAR"],
        "statusReason": str,
        "exportTaskDetails": ExportTaskDetailsTypeDef,
        "exportFilter": ExportFilterOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartExportTaskOutputTypeDef = TypedDict(
    "StartExportTaskOutputTypeDef",
    {
        "graphId": str,
        "roleArn": str,
        "taskId": str,
        "status": ExportTaskStatusType,
        "format": ExportFormatType,
        "destination": str,
        "kmsKeyIdentifier": str,
        "parquetType": Literal["COLUMNAR"],
        "statusReason": str,
        "exportFilter": ExportFilterOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ExportFilterTypeDef(TypedDict):
    vertexFilter: NotRequired[Mapping[str, ExportFilterElementUnionTypeDef]]
    edgeFilter: NotRequired[Mapping[str, ExportFilterElementTypeDef]]


StartExportTaskInputRequestTypeDef = TypedDict(
    "StartExportTaskInputRequestTypeDef",
    {
        "graphIdentifier": str,
        "roleArn": str,
        "format": ExportFormatType,
        "destination": str,
        "kmsKeyIdentifier": str,
        "parquetType": NotRequired[Literal["COLUMNAR"]],
        "exportFilter": NotRequired[ExportFilterTypeDef],
        "tags": NotRequired[Mapping[str, str]],
    },
)
