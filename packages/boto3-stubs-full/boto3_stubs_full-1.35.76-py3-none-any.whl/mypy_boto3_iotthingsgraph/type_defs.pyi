"""
Type annotations for iotthingsgraph service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/type_defs/)

Usage::

    ```python
    from mypy_boto3_iotthingsgraph.type_defs import AssociateEntityToThingRequestRequestTypeDef

    data: AssociateEntityToThingRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    DeploymentTargetType,
    EntityFilterNameType,
    EntityTypeType,
    FlowExecutionEventTypeType,
    FlowExecutionStatusType,
    NamespaceDeletionStatusType,
    SystemInstanceDeploymentStatusType,
    SystemInstanceFilterNameType,
    UploadStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AssociateEntityToThingRequestRequestTypeDef",
    "CreateFlowTemplateRequestRequestTypeDef",
    "CreateFlowTemplateResponseTypeDef",
    "CreateSystemInstanceRequestRequestTypeDef",
    "CreateSystemInstanceResponseTypeDef",
    "CreateSystemTemplateRequestRequestTypeDef",
    "CreateSystemTemplateResponseTypeDef",
    "DefinitionDocumentTypeDef",
    "DeleteFlowTemplateRequestRequestTypeDef",
    "DeleteNamespaceResponseTypeDef",
    "DeleteSystemInstanceRequestRequestTypeDef",
    "DeleteSystemTemplateRequestRequestTypeDef",
    "DependencyRevisionTypeDef",
    "DeploySystemInstanceRequestRequestTypeDef",
    "DeploySystemInstanceResponseTypeDef",
    "DeprecateFlowTemplateRequestRequestTypeDef",
    "DeprecateSystemTemplateRequestRequestTypeDef",
    "DescribeNamespaceRequestRequestTypeDef",
    "DescribeNamespaceResponseTypeDef",
    "DissociateEntityFromThingRequestRequestTypeDef",
    "EntityDescriptionTypeDef",
    "EntityFilterTypeDef",
    "FlowExecutionMessageTypeDef",
    "FlowExecutionSummaryTypeDef",
    "FlowTemplateDescriptionTypeDef",
    "FlowTemplateFilterTypeDef",
    "FlowTemplateSummaryTypeDef",
    "GetEntitiesRequestRequestTypeDef",
    "GetEntitiesResponseTypeDef",
    "GetFlowTemplateRequestRequestTypeDef",
    "GetFlowTemplateResponseTypeDef",
    "GetFlowTemplateRevisionsRequestGetFlowTemplateRevisionsPaginateTypeDef",
    "GetFlowTemplateRevisionsRequestRequestTypeDef",
    "GetFlowTemplateRevisionsResponseTypeDef",
    "GetNamespaceDeletionStatusResponseTypeDef",
    "GetSystemInstanceRequestRequestTypeDef",
    "GetSystemInstanceResponseTypeDef",
    "GetSystemTemplateRequestRequestTypeDef",
    "GetSystemTemplateResponseTypeDef",
    "GetSystemTemplateRevisionsRequestGetSystemTemplateRevisionsPaginateTypeDef",
    "GetSystemTemplateRevisionsRequestRequestTypeDef",
    "GetSystemTemplateRevisionsResponseTypeDef",
    "GetUploadStatusRequestRequestTypeDef",
    "GetUploadStatusResponseTypeDef",
    "ListFlowExecutionMessagesRequestListFlowExecutionMessagesPaginateTypeDef",
    "ListFlowExecutionMessagesRequestRequestTypeDef",
    "ListFlowExecutionMessagesResponseTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MetricsConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "SearchEntitiesRequestRequestTypeDef",
    "SearchEntitiesRequestSearchEntitiesPaginateTypeDef",
    "SearchEntitiesResponseTypeDef",
    "SearchFlowExecutionsRequestRequestTypeDef",
    "SearchFlowExecutionsRequestSearchFlowExecutionsPaginateTypeDef",
    "SearchFlowExecutionsResponseTypeDef",
    "SearchFlowTemplatesRequestRequestTypeDef",
    "SearchFlowTemplatesRequestSearchFlowTemplatesPaginateTypeDef",
    "SearchFlowTemplatesResponseTypeDef",
    "SearchSystemInstancesRequestRequestTypeDef",
    "SearchSystemInstancesRequestSearchSystemInstancesPaginateTypeDef",
    "SearchSystemInstancesResponseTypeDef",
    "SearchSystemTemplatesRequestRequestTypeDef",
    "SearchSystemTemplatesRequestSearchSystemTemplatesPaginateTypeDef",
    "SearchSystemTemplatesResponseTypeDef",
    "SearchThingsRequestRequestTypeDef",
    "SearchThingsRequestSearchThingsPaginateTypeDef",
    "SearchThingsResponseTypeDef",
    "SystemInstanceDescriptionTypeDef",
    "SystemInstanceFilterTypeDef",
    "SystemInstanceSummaryTypeDef",
    "SystemTemplateDescriptionTypeDef",
    "SystemTemplateFilterTypeDef",
    "SystemTemplateSummaryTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "ThingTypeDef",
    "TimestampTypeDef",
    "UndeploySystemInstanceRequestRequestTypeDef",
    "UndeploySystemInstanceResponseTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFlowTemplateRequestRequestTypeDef",
    "UpdateFlowTemplateResponseTypeDef",
    "UpdateSystemTemplateRequestRequestTypeDef",
    "UpdateSystemTemplateResponseTypeDef",
    "UploadEntityDefinitionsRequestRequestTypeDef",
    "UploadEntityDefinitionsResponseTypeDef",
)

class AssociateEntityToThingRequestRequestTypeDef(TypedDict):
    thingName: str
    entityId: str
    namespaceVersion: NotRequired[int]

class DefinitionDocumentTypeDef(TypedDict):
    language: Literal["GRAPHQL"]
    text: str

FlowTemplateSummaryTypeDef = TypedDict(
    "FlowTemplateSummaryTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "revisionNumber": NotRequired[int],
        "createdAt": NotRequired[datetime],
    },
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class MetricsConfigurationTypeDef(TypedDict):
    cloudMetricEnabled: NotRequired[bool]
    metricRuleRoleArn: NotRequired[str]

class TagTypeDef(TypedDict):
    key: str
    value: str

SystemInstanceSummaryTypeDef = TypedDict(
    "SystemInstanceSummaryTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "status": NotRequired[SystemInstanceDeploymentStatusType],
        "target": NotRequired[DeploymentTargetType],
        "greengrassGroupName": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "greengrassGroupId": NotRequired[str],
        "greengrassGroupVersionId": NotRequired[str],
    },
)
SystemTemplateSummaryTypeDef = TypedDict(
    "SystemTemplateSummaryTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "revisionNumber": NotRequired[int],
        "createdAt": NotRequired[datetime],
    },
)
DeleteFlowTemplateRequestRequestTypeDef = TypedDict(
    "DeleteFlowTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)
DeleteSystemInstanceRequestRequestTypeDef = TypedDict(
    "DeleteSystemInstanceRequestRequestTypeDef",
    {
        "id": NotRequired[str],
    },
)
DeleteSystemTemplateRequestRequestTypeDef = TypedDict(
    "DeleteSystemTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)
DependencyRevisionTypeDef = TypedDict(
    "DependencyRevisionTypeDef",
    {
        "id": NotRequired[str],
        "revisionNumber": NotRequired[int],
    },
)
DeploySystemInstanceRequestRequestTypeDef = TypedDict(
    "DeploySystemInstanceRequestRequestTypeDef",
    {
        "id": NotRequired[str],
    },
)
DeprecateFlowTemplateRequestRequestTypeDef = TypedDict(
    "DeprecateFlowTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)
DeprecateSystemTemplateRequestRequestTypeDef = TypedDict(
    "DeprecateSystemTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)

class DescribeNamespaceRequestRequestTypeDef(TypedDict):
    namespaceName: NotRequired[str]

class DissociateEntityFromThingRequestRequestTypeDef(TypedDict):
    thingName: str
    entityType: EntityTypeType

class EntityFilterTypeDef(TypedDict):
    name: NotRequired[EntityFilterNameType]
    value: NotRequired[Sequence[str]]

class FlowExecutionMessageTypeDef(TypedDict):
    messageId: NotRequired[str]
    eventType: NotRequired[FlowExecutionEventTypeType]
    timestamp: NotRequired[datetime]
    payload: NotRequired[str]

class FlowExecutionSummaryTypeDef(TypedDict):
    flowExecutionId: NotRequired[str]
    status: NotRequired[FlowExecutionStatusType]
    systemInstanceId: NotRequired[str]
    flowTemplateId: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class FlowTemplateFilterTypeDef(TypedDict):
    name: Literal["DEVICE_MODEL_ID"]
    value: Sequence[str]

class GetEntitiesRequestRequestTypeDef(TypedDict):
    ids: Sequence[str]
    namespaceVersion: NotRequired[int]

GetFlowTemplateRequestRequestTypeDef = TypedDict(
    "GetFlowTemplateRequestRequestTypeDef",
    {
        "id": str,
        "revisionNumber": NotRequired[int],
    },
)

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

GetFlowTemplateRevisionsRequestRequestTypeDef = TypedDict(
    "GetFlowTemplateRevisionsRequestRequestTypeDef",
    {
        "id": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
GetSystemInstanceRequestRequestTypeDef = TypedDict(
    "GetSystemInstanceRequestRequestTypeDef",
    {
        "id": str,
    },
)
GetSystemTemplateRequestRequestTypeDef = TypedDict(
    "GetSystemTemplateRequestRequestTypeDef",
    {
        "id": str,
        "revisionNumber": NotRequired[int],
    },
)
GetSystemTemplateRevisionsRequestRequestTypeDef = TypedDict(
    "GetSystemTemplateRevisionsRequestRequestTypeDef",
    {
        "id": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

class GetUploadStatusRequestRequestTypeDef(TypedDict):
    uploadId: str

class ListFlowExecutionMessagesRequestRequestTypeDef(TypedDict):
    flowExecutionId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class SystemInstanceFilterTypeDef(TypedDict):
    name: NotRequired[SystemInstanceFilterNameType]
    value: NotRequired[Sequence[str]]

class SystemTemplateFilterTypeDef(TypedDict):
    name: Literal["FLOW_TEMPLATE_ID"]
    value: Sequence[str]

class SearchThingsRequestRequestTypeDef(TypedDict):
    entityId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    namespaceVersion: NotRequired[int]

class ThingTypeDef(TypedDict):
    thingArn: NotRequired[str]
    thingName: NotRequired[str]

UndeploySystemInstanceRequestRequestTypeDef = TypedDict(
    "UndeploySystemInstanceRequestRequestTypeDef",
    {
        "id": NotRequired[str],
    },
)

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class CreateFlowTemplateRequestRequestTypeDef(TypedDict):
    definition: DefinitionDocumentTypeDef
    compatibleNamespaceVersion: NotRequired[int]

class CreateSystemTemplateRequestRequestTypeDef(TypedDict):
    definition: DefinitionDocumentTypeDef
    compatibleNamespaceVersion: NotRequired[int]

EntityDescriptionTypeDef = TypedDict(
    "EntityDescriptionTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "type": NotRequired[EntityTypeType],
        "createdAt": NotRequired[datetime],
        "definition": NotRequired[DefinitionDocumentTypeDef],
    },
)
UpdateFlowTemplateRequestRequestTypeDef = TypedDict(
    "UpdateFlowTemplateRequestRequestTypeDef",
    {
        "id": str,
        "definition": DefinitionDocumentTypeDef,
        "compatibleNamespaceVersion": NotRequired[int],
    },
)
UpdateSystemTemplateRequestRequestTypeDef = TypedDict(
    "UpdateSystemTemplateRequestRequestTypeDef",
    {
        "id": str,
        "definition": DefinitionDocumentTypeDef,
        "compatibleNamespaceVersion": NotRequired[int],
    },
)

class UploadEntityDefinitionsRequestRequestTypeDef(TypedDict):
    document: NotRequired[DefinitionDocumentTypeDef]
    syncWithPublicNamespace: NotRequired[bool]
    deprecateExistingEntities: NotRequired[bool]

class FlowTemplateDescriptionTypeDef(TypedDict):
    summary: NotRequired[FlowTemplateSummaryTypeDef]
    definition: NotRequired[DefinitionDocumentTypeDef]
    validatedNamespaceVersion: NotRequired[int]

class CreateFlowTemplateResponseTypeDef(TypedDict):
    summary: FlowTemplateSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteNamespaceResponseTypeDef(TypedDict):
    namespaceArn: str
    namespaceName: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeNamespaceResponseTypeDef(TypedDict):
    namespaceArn: str
    namespaceName: str
    trackingNamespaceName: str
    trackingNamespaceVersion: int
    namespaceVersion: int
    ResponseMetadata: ResponseMetadataTypeDef

class GetFlowTemplateRevisionsResponseTypeDef(TypedDict):
    summaries: List[FlowTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetNamespaceDeletionStatusResponseTypeDef(TypedDict):
    namespaceArn: str
    namespaceName: str
    status: NamespaceDeletionStatusType
    errorCode: Literal["VALIDATION_FAILED"]
    errorMessage: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetUploadStatusResponseTypeDef(TypedDict):
    uploadId: str
    uploadStatus: UploadStatusType
    namespaceArn: str
    namespaceName: str
    namespaceVersion: int
    failureReason: List[str]
    createdDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class SearchFlowTemplatesResponseTypeDef(TypedDict):
    summaries: List[FlowTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateFlowTemplateResponseTypeDef(TypedDict):
    summary: FlowTemplateSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UploadEntityDefinitionsResponseTypeDef(TypedDict):
    uploadId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSystemInstanceRequestRequestTypeDef(TypedDict):
    definition: DefinitionDocumentTypeDef
    target: DeploymentTargetType
    tags: NotRequired[Sequence[TagTypeDef]]
    greengrassGroupName: NotRequired[str]
    s3BucketName: NotRequired[str]
    metricsConfiguration: NotRequired[MetricsConfigurationTypeDef]
    flowActionsRoleArn: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]

class CreateSystemInstanceResponseTypeDef(TypedDict):
    summary: SystemInstanceSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeploySystemInstanceResponseTypeDef(TypedDict):
    summary: SystemInstanceSummaryTypeDef
    greengrassDeploymentId: str
    ResponseMetadata: ResponseMetadataTypeDef

class SearchSystemInstancesResponseTypeDef(TypedDict):
    summaries: List[SystemInstanceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UndeploySystemInstanceResponseTypeDef(TypedDict):
    summary: SystemInstanceSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSystemTemplateResponseTypeDef(TypedDict):
    summary: SystemTemplateSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSystemTemplateRevisionsResponseTypeDef(TypedDict):
    summaries: List[SystemTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SearchSystemTemplatesResponseTypeDef(TypedDict):
    summaries: List[SystemTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SystemTemplateDescriptionTypeDef(TypedDict):
    summary: NotRequired[SystemTemplateSummaryTypeDef]
    definition: NotRequired[DefinitionDocumentTypeDef]
    validatedNamespaceVersion: NotRequired[int]

class UpdateSystemTemplateResponseTypeDef(TypedDict):
    summary: SystemTemplateSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SystemInstanceDescriptionTypeDef(TypedDict):
    summary: NotRequired[SystemInstanceSummaryTypeDef]
    definition: NotRequired[DefinitionDocumentTypeDef]
    s3BucketName: NotRequired[str]
    metricsConfiguration: NotRequired[MetricsConfigurationTypeDef]
    validatedNamespaceVersion: NotRequired[int]
    validatedDependencyRevisions: NotRequired[List[DependencyRevisionTypeDef]]
    flowActionsRoleArn: NotRequired[str]

class SearchEntitiesRequestRequestTypeDef(TypedDict):
    entityTypes: Sequence[EntityTypeType]
    filters: NotRequired[Sequence[EntityFilterTypeDef]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    namespaceVersion: NotRequired[int]

class ListFlowExecutionMessagesResponseTypeDef(TypedDict):
    messages: List[FlowExecutionMessageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SearchFlowExecutionsResponseTypeDef(TypedDict):
    summaries: List[FlowExecutionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SearchFlowTemplatesRequestRequestTypeDef(TypedDict):
    filters: NotRequired[Sequence[FlowTemplateFilterTypeDef]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

GetFlowTemplateRevisionsRequestGetFlowTemplateRevisionsPaginateTypeDef = TypedDict(
    "GetFlowTemplateRevisionsRequestGetFlowTemplateRevisionsPaginateTypeDef",
    {
        "id": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetSystemTemplateRevisionsRequestGetSystemTemplateRevisionsPaginateTypeDef = TypedDict(
    "GetSystemTemplateRevisionsRequestGetSystemTemplateRevisionsPaginateTypeDef",
    {
        "id": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListFlowExecutionMessagesRequestListFlowExecutionMessagesPaginateTypeDef(TypedDict):
    flowExecutionId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(TypedDict):
    resourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchEntitiesRequestSearchEntitiesPaginateTypeDef(TypedDict):
    entityTypes: Sequence[EntityTypeType]
    filters: NotRequired[Sequence[EntityFilterTypeDef]]
    namespaceVersion: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchFlowTemplatesRequestSearchFlowTemplatesPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[FlowTemplateFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchThingsRequestSearchThingsPaginateTypeDef(TypedDict):
    entityId: str
    namespaceVersion: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchFlowExecutionsRequestRequestTypeDef(TypedDict):
    systemInstanceId: str
    flowExecutionId: NotRequired[str]
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class SearchFlowExecutionsRequestSearchFlowExecutionsPaginateTypeDef(TypedDict):
    systemInstanceId: str
    flowExecutionId: NotRequired[str]
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchSystemInstancesRequestRequestTypeDef(TypedDict):
    filters: NotRequired[Sequence[SystemInstanceFilterTypeDef]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class SearchSystemInstancesRequestSearchSystemInstancesPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[SystemInstanceFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchSystemTemplatesRequestRequestTypeDef(TypedDict):
    filters: NotRequired[Sequence[SystemTemplateFilterTypeDef]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class SearchSystemTemplatesRequestSearchSystemTemplatesPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[SystemTemplateFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchThingsResponseTypeDef(TypedDict):
    things: List[ThingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetEntitiesResponseTypeDef(TypedDict):
    descriptions: List[EntityDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class SearchEntitiesResponseTypeDef(TypedDict):
    descriptions: List[EntityDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetFlowTemplateResponseTypeDef(TypedDict):
    description: FlowTemplateDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSystemTemplateResponseTypeDef(TypedDict):
    description: SystemTemplateDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSystemInstanceResponseTypeDef(TypedDict):
    description: SystemInstanceDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
