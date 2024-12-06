"""
Type annotations for wisdom service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/type_defs/)

Usage::

    ```python
    from mypy_boto3_wisdom.type_defs import AppIntegrationsConfigurationOutputTypeDef

    data: AppIntegrationsConfigurationOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AssistantStatusType,
    ContentStatusType,
    ImportJobStatusType,
    KnowledgeBaseStatusType,
    KnowledgeBaseTypeType,
    OrderType,
    PriorityType,
    QuickResponseFilterOperatorType,
    QuickResponseQueryOperatorType,
    QuickResponseStatusType,
    RecommendationSourceTypeType,
    RelevanceLevelType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AppIntegrationsConfigurationOutputTypeDef",
    "AppIntegrationsConfigurationTypeDef",
    "AppIntegrationsConfigurationUnionTypeDef",
    "AssistantAssociationDataTypeDef",
    "AssistantAssociationInputDataTypeDef",
    "AssistantAssociationOutputDataTypeDef",
    "AssistantAssociationSummaryTypeDef",
    "AssistantDataTypeDef",
    "AssistantIntegrationConfigurationTypeDef",
    "AssistantSummaryTypeDef",
    "ConfigurationTypeDef",
    "ConnectConfigurationTypeDef",
    "ContentDataTypeDef",
    "ContentReferenceTypeDef",
    "ContentSummaryTypeDef",
    "CreateAssistantAssociationRequestRequestTypeDef",
    "CreateAssistantAssociationResponseTypeDef",
    "CreateAssistantRequestRequestTypeDef",
    "CreateAssistantResponseTypeDef",
    "CreateContentRequestRequestTypeDef",
    "CreateContentResponseTypeDef",
    "CreateKnowledgeBaseRequestRequestTypeDef",
    "CreateKnowledgeBaseResponseTypeDef",
    "CreateQuickResponseRequestRequestTypeDef",
    "CreateQuickResponseResponseTypeDef",
    "CreateSessionRequestRequestTypeDef",
    "CreateSessionResponseTypeDef",
    "DeleteAssistantAssociationRequestRequestTypeDef",
    "DeleteAssistantRequestRequestTypeDef",
    "DeleteContentRequestRequestTypeDef",
    "DeleteImportJobRequestRequestTypeDef",
    "DeleteKnowledgeBaseRequestRequestTypeDef",
    "DeleteQuickResponseRequestRequestTypeDef",
    "DocumentTextTypeDef",
    "DocumentTypeDef",
    "ExternalSourceConfigurationTypeDef",
    "FilterTypeDef",
    "GetAssistantAssociationRequestRequestTypeDef",
    "GetAssistantAssociationResponseTypeDef",
    "GetAssistantRequestRequestTypeDef",
    "GetAssistantResponseTypeDef",
    "GetContentRequestRequestTypeDef",
    "GetContentResponseTypeDef",
    "GetContentSummaryRequestRequestTypeDef",
    "GetContentSummaryResponseTypeDef",
    "GetImportJobRequestRequestTypeDef",
    "GetImportJobResponseTypeDef",
    "GetKnowledgeBaseRequestRequestTypeDef",
    "GetKnowledgeBaseResponseTypeDef",
    "GetQuickResponseRequestRequestTypeDef",
    "GetQuickResponseResponseTypeDef",
    "GetRecommendationsRequestRequestTypeDef",
    "GetRecommendationsResponseTypeDef",
    "GetSessionRequestRequestTypeDef",
    "GetSessionResponseTypeDef",
    "GroupingConfigurationOutputTypeDef",
    "GroupingConfigurationTypeDef",
    "HighlightTypeDef",
    "ImportJobDataTypeDef",
    "ImportJobSummaryTypeDef",
    "KnowledgeBaseAssociationDataTypeDef",
    "KnowledgeBaseDataTypeDef",
    "KnowledgeBaseSummaryTypeDef",
    "ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef",
    "ListAssistantAssociationsRequestRequestTypeDef",
    "ListAssistantAssociationsResponseTypeDef",
    "ListAssistantsRequestListAssistantsPaginateTypeDef",
    "ListAssistantsRequestRequestTypeDef",
    "ListAssistantsResponseTypeDef",
    "ListContentsRequestListContentsPaginateTypeDef",
    "ListContentsRequestRequestTypeDef",
    "ListContentsResponseTypeDef",
    "ListImportJobsRequestListImportJobsPaginateTypeDef",
    "ListImportJobsRequestRequestTypeDef",
    "ListImportJobsResponseTypeDef",
    "ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef",
    "ListKnowledgeBasesRequestRequestTypeDef",
    "ListKnowledgeBasesResponseTypeDef",
    "ListQuickResponsesRequestListQuickResponsesPaginateTypeDef",
    "ListQuickResponsesRequestRequestTypeDef",
    "ListQuickResponsesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NotifyRecommendationsReceivedErrorTypeDef",
    "NotifyRecommendationsReceivedRequestRequestTypeDef",
    "NotifyRecommendationsReceivedResponseTypeDef",
    "PaginatorConfigTypeDef",
    "QueryAssistantRequestQueryAssistantPaginateTypeDef",
    "QueryAssistantRequestRequestTypeDef",
    "QueryAssistantResponseTypeDef",
    "QueryRecommendationTriggerDataTypeDef",
    "QuickResponseContentProviderTypeDef",
    "QuickResponseContentsTypeDef",
    "QuickResponseDataProviderTypeDef",
    "QuickResponseDataTypeDef",
    "QuickResponseFilterFieldTypeDef",
    "QuickResponseOrderFieldTypeDef",
    "QuickResponseQueryFieldTypeDef",
    "QuickResponseSearchExpressionTypeDef",
    "QuickResponseSearchResultDataTypeDef",
    "QuickResponseSummaryTypeDef",
    "RecommendationDataTypeDef",
    "RecommendationTriggerDataTypeDef",
    "RecommendationTriggerTypeDef",
    "RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef",
    "RenderingConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "ResultDataTypeDef",
    "SearchContentRequestRequestTypeDef",
    "SearchContentRequestSearchContentPaginateTypeDef",
    "SearchContentResponseTypeDef",
    "SearchExpressionTypeDef",
    "SearchQuickResponsesRequestRequestTypeDef",
    "SearchQuickResponsesRequestSearchQuickResponsesPaginateTypeDef",
    "SearchQuickResponsesResponseTypeDef",
    "SearchSessionsRequestRequestTypeDef",
    "SearchSessionsRequestSearchSessionsPaginateTypeDef",
    "SearchSessionsResponseTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "SessionDataTypeDef",
    "SessionIntegrationConfigurationTypeDef",
    "SessionSummaryTypeDef",
    "SourceConfigurationOutputTypeDef",
    "SourceConfigurationTypeDef",
    "StartContentUploadRequestRequestTypeDef",
    "StartContentUploadResponseTypeDef",
    "StartImportJobRequestRequestTypeDef",
    "StartImportJobResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateContentRequestRequestTypeDef",
    "UpdateContentResponseTypeDef",
    "UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef",
    "UpdateKnowledgeBaseTemplateUriResponseTypeDef",
    "UpdateQuickResponseRequestRequestTypeDef",
    "UpdateQuickResponseResponseTypeDef",
)

class AppIntegrationsConfigurationOutputTypeDef(TypedDict):
    appIntegrationArn: str
    objectFields: NotRequired[List[str]]

class AppIntegrationsConfigurationTypeDef(TypedDict):
    appIntegrationArn: str
    objectFields: NotRequired[Sequence[str]]

class AssistantAssociationInputDataTypeDef(TypedDict):
    knowledgeBaseId: NotRequired[str]

class KnowledgeBaseAssociationDataTypeDef(TypedDict):
    knowledgeBaseArn: NotRequired[str]
    knowledgeBaseId: NotRequired[str]

class AssistantIntegrationConfigurationTypeDef(TypedDict):
    topicIntegrationArn: NotRequired[str]

class ServerSideEncryptionConfigurationTypeDef(TypedDict):
    kmsKeyId: NotRequired[str]

class ConnectConfigurationTypeDef(TypedDict):
    instanceId: NotRequired[str]

class ContentDataTypeDef(TypedDict):
    contentArn: str
    contentId: str
    contentType: str
    knowledgeBaseArn: str
    knowledgeBaseId: str
    metadata: Dict[str, str]
    name: str
    revisionId: str
    status: ContentStatusType
    title: str
    url: str
    urlExpiry: datetime
    linkOutUri: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

class ContentReferenceTypeDef(TypedDict):
    contentArn: NotRequired[str]
    contentId: NotRequired[str]
    knowledgeBaseArn: NotRequired[str]
    knowledgeBaseId: NotRequired[str]

class ContentSummaryTypeDef(TypedDict):
    contentArn: str
    contentId: str
    contentType: str
    knowledgeBaseArn: str
    knowledgeBaseId: str
    metadata: Dict[str, str]
    name: str
    revisionId: str
    status: ContentStatusType
    title: str
    tags: NotRequired[Dict[str, str]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateContentRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    name: str
    uploadId: str
    clientToken: NotRequired[str]
    metadata: NotRequired[Mapping[str, str]]
    overrideLinkOutUri: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    title: NotRequired[str]

class RenderingConfigurationTypeDef(TypedDict):
    templateUri: NotRequired[str]

class GroupingConfigurationTypeDef(TypedDict):
    criteria: NotRequired[str]
    values: NotRequired[Sequence[str]]

class QuickResponseDataProviderTypeDef(TypedDict):
    content: NotRequired[str]

class CreateSessionRequestRequestTypeDef(TypedDict):
    assistantId: str
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class DeleteAssistantAssociationRequestRequestTypeDef(TypedDict):
    assistantAssociationId: str
    assistantId: str

class DeleteAssistantRequestRequestTypeDef(TypedDict):
    assistantId: str

class DeleteContentRequestRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str

class DeleteImportJobRequestRequestTypeDef(TypedDict):
    importJobId: str
    knowledgeBaseId: str

class DeleteKnowledgeBaseRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str

class DeleteQuickResponseRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    quickResponseId: str

class HighlightTypeDef(TypedDict):
    beginOffsetInclusive: NotRequired[int]
    endOffsetExclusive: NotRequired[int]

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "field": Literal["NAME"],
        "operator": Literal["EQUALS"],
        "value": str,
    },
)

class GetAssistantAssociationRequestRequestTypeDef(TypedDict):
    assistantAssociationId: str
    assistantId: str

class GetAssistantRequestRequestTypeDef(TypedDict):
    assistantId: str

class GetContentRequestRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str

class GetContentSummaryRequestRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str

class GetImportJobRequestRequestTypeDef(TypedDict):
    importJobId: str
    knowledgeBaseId: str

class GetKnowledgeBaseRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str

class GetQuickResponseRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    quickResponseId: str

class GetRecommendationsRequestRequestTypeDef(TypedDict):
    assistantId: str
    sessionId: str
    maxResults: NotRequired[int]
    waitTimeSeconds: NotRequired[int]

class GetSessionRequestRequestTypeDef(TypedDict):
    assistantId: str
    sessionId: str

class GroupingConfigurationOutputTypeDef(TypedDict):
    criteria: NotRequired[str]
    values: NotRequired[List[str]]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAssistantAssociationsRequestRequestTypeDef(TypedDict):
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAssistantsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListContentsRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListImportJobsRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListKnowledgeBasesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListQuickResponsesRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class QuickResponseSummaryTypeDef(TypedDict):
    contentType: str
    createdTime: datetime
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    name: str
    quickResponseArn: str
    quickResponseId: str
    status: QuickResponseStatusType
    channels: NotRequired[List[str]]
    description: NotRequired[str]
    isActive: NotRequired[bool]
    lastModifiedBy: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class NotifyRecommendationsReceivedErrorTypeDef(TypedDict):
    message: NotRequired[str]
    recommendationId: NotRequired[str]

class NotifyRecommendationsReceivedRequestRequestTypeDef(TypedDict):
    assistantId: str
    recommendationIds: Sequence[str]
    sessionId: str

class QueryAssistantRequestRequestTypeDef(TypedDict):
    assistantId: str
    queryText: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class QueryRecommendationTriggerDataTypeDef(TypedDict):
    text: NotRequired[str]

class QuickResponseContentProviderTypeDef(TypedDict):
    content: NotRequired[str]

QuickResponseFilterFieldTypeDef = TypedDict(
    "QuickResponseFilterFieldTypeDef",
    {
        "name": str,
        "operator": QuickResponseFilterOperatorType,
        "includeNoExistence": NotRequired[bool],
        "values": NotRequired[Sequence[str]],
    },
)

class QuickResponseOrderFieldTypeDef(TypedDict):
    name: str
    order: NotRequired[OrderType]

QuickResponseQueryFieldTypeDef = TypedDict(
    "QuickResponseQueryFieldTypeDef",
    {
        "name": str,
        "operator": QuickResponseQueryOperatorType,
        "values": Sequence[str],
        "allowFuzziness": NotRequired[bool],
        "priority": NotRequired[PriorityType],
    },
)

class RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str

class SessionSummaryTypeDef(TypedDict):
    assistantArn: str
    assistantId: str
    sessionArn: str
    sessionId: str

class SessionIntegrationConfigurationTypeDef(TypedDict):
    topicIntegrationArn: NotRequired[str]

class StartContentUploadRequestRequestTypeDef(TypedDict):
    contentType: str
    knowledgeBaseId: str
    presignedUrlTimeToLive: NotRequired[int]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateContentRequestRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str
    metadata: NotRequired[Mapping[str, str]]
    overrideLinkOutUri: NotRequired[str]
    removeOverrideLinkOutUri: NotRequired[bool]
    revisionId: NotRequired[str]
    title: NotRequired[str]
    uploadId: NotRequired[str]

class UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    templateUri: str

class SourceConfigurationOutputTypeDef(TypedDict):
    appIntegrations: NotRequired[AppIntegrationsConfigurationOutputTypeDef]

AppIntegrationsConfigurationUnionTypeDef = Union[
    AppIntegrationsConfigurationTypeDef, AppIntegrationsConfigurationOutputTypeDef
]

class CreateAssistantAssociationRequestRequestTypeDef(TypedDict):
    assistantId: str
    association: AssistantAssociationInputDataTypeDef
    associationType: Literal["KNOWLEDGE_BASE"]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class AssistantAssociationOutputDataTypeDef(TypedDict):
    knowledgeBaseAssociation: NotRequired[KnowledgeBaseAssociationDataTypeDef]

AssistantDataTypeDef = TypedDict(
    "AssistantDataTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "name": str,
        "status": AssistantStatusType,
        "type": Literal["AGENT"],
        "description": NotRequired[str],
        "integrationConfiguration": NotRequired[AssistantIntegrationConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)
AssistantSummaryTypeDef = TypedDict(
    "AssistantSummaryTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "name": str,
        "status": AssistantStatusType,
        "type": Literal["AGENT"],
        "description": NotRequired[str],
        "integrationConfiguration": NotRequired[AssistantIntegrationConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)
CreateAssistantRequestRequestTypeDef = TypedDict(
    "CreateAssistantRequestRequestTypeDef",
    {
        "name": str,
        "type": Literal["AGENT"],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Mapping[str, str]],
    },
)

class ConfigurationTypeDef(TypedDict):
    connectConfiguration: NotRequired[ConnectConfigurationTypeDef]

class CreateContentResponseTypeDef(TypedDict):
    content: ContentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetContentResponseTypeDef(TypedDict):
    content: ContentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetContentSummaryResponseTypeDef(TypedDict):
    contentSummary: ContentSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListContentsResponseTypeDef(TypedDict):
    contentSummaries: List[ContentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class SearchContentResponseTypeDef(TypedDict):
    contentSummaries: List[ContentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class StartContentUploadResponseTypeDef(TypedDict):
    headersToInclude: Dict[str, str]
    uploadId: str
    url: str
    urlExpiry: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateContentResponseTypeDef(TypedDict):
    content: ContentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateQuickResponseRequestRequestTypeDef(TypedDict):
    content: QuickResponseDataProviderTypeDef
    knowledgeBaseId: str
    name: str
    channels: NotRequired[Sequence[str]]
    clientToken: NotRequired[str]
    contentType: NotRequired[str]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationTypeDef]
    isActive: NotRequired[bool]
    language: NotRequired[str]
    shortcutKey: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class UpdateQuickResponseRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    quickResponseId: str
    channels: NotRequired[Sequence[str]]
    content: NotRequired[QuickResponseDataProviderTypeDef]
    contentType: NotRequired[str]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationTypeDef]
    isActive: NotRequired[bool]
    language: NotRequired[str]
    name: NotRequired[str]
    removeDescription: NotRequired[bool]
    removeGroupingConfiguration: NotRequired[bool]
    removeShortcutKey: NotRequired[bool]
    shortcutKey: NotRequired[str]

class DocumentTextTypeDef(TypedDict):
    highlights: NotRequired[List[HighlightTypeDef]]
    text: NotRequired[str]

class SearchExpressionTypeDef(TypedDict):
    filters: Sequence[FilterTypeDef]

class ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef(TypedDict):
    assistantId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAssistantsRequestListAssistantsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListContentsRequestListContentsPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListImportJobsRequestListImportJobsPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListQuickResponsesRequestListQuickResponsesPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class QueryAssistantRequestQueryAssistantPaginateTypeDef(TypedDict):
    assistantId: str
    queryText: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListQuickResponsesResponseTypeDef(TypedDict):
    quickResponseSummaries: List[QuickResponseSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class NotifyRecommendationsReceivedResponseTypeDef(TypedDict):
    errors: List[NotifyRecommendationsReceivedErrorTypeDef]
    recommendationIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class RecommendationTriggerDataTypeDef(TypedDict):
    query: NotRequired[QueryRecommendationTriggerDataTypeDef]

class QuickResponseContentsTypeDef(TypedDict):
    markdown: NotRequired[QuickResponseContentProviderTypeDef]
    plainText: NotRequired[QuickResponseContentProviderTypeDef]

class QuickResponseSearchExpressionTypeDef(TypedDict):
    filters: NotRequired[Sequence[QuickResponseFilterFieldTypeDef]]
    orderOnField: NotRequired[QuickResponseOrderFieldTypeDef]
    queries: NotRequired[Sequence[QuickResponseQueryFieldTypeDef]]

class SearchSessionsResponseTypeDef(TypedDict):
    sessionSummaries: List[SessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SessionDataTypeDef(TypedDict):
    name: str
    sessionArn: str
    sessionId: str
    description: NotRequired[str]
    integrationConfiguration: NotRequired[SessionIntegrationConfigurationTypeDef]
    tags: NotRequired[Dict[str, str]]

class KnowledgeBaseDataTypeDef(TypedDict):
    knowledgeBaseArn: str
    knowledgeBaseId: str
    knowledgeBaseType: KnowledgeBaseTypeType
    name: str
    status: KnowledgeBaseStatusType
    description: NotRequired[str]
    lastContentModificationTime: NotRequired[datetime]
    renderingConfiguration: NotRequired[RenderingConfigurationTypeDef]
    serverSideEncryptionConfiguration: NotRequired[ServerSideEncryptionConfigurationTypeDef]
    sourceConfiguration: NotRequired[SourceConfigurationOutputTypeDef]
    tags: NotRequired[Dict[str, str]]

class KnowledgeBaseSummaryTypeDef(TypedDict):
    knowledgeBaseArn: str
    knowledgeBaseId: str
    knowledgeBaseType: KnowledgeBaseTypeType
    name: str
    status: KnowledgeBaseStatusType
    description: NotRequired[str]
    renderingConfiguration: NotRequired[RenderingConfigurationTypeDef]
    serverSideEncryptionConfiguration: NotRequired[ServerSideEncryptionConfigurationTypeDef]
    sourceConfiguration: NotRequired[SourceConfigurationOutputTypeDef]
    tags: NotRequired[Dict[str, str]]

class SourceConfigurationTypeDef(TypedDict):
    appIntegrations: NotRequired[AppIntegrationsConfigurationUnionTypeDef]

class AssistantAssociationDataTypeDef(TypedDict):
    assistantArn: str
    assistantAssociationArn: str
    assistantAssociationId: str
    assistantId: str
    associationData: AssistantAssociationOutputDataTypeDef
    associationType: Literal["KNOWLEDGE_BASE"]
    tags: NotRequired[Dict[str, str]]

class AssistantAssociationSummaryTypeDef(TypedDict):
    assistantArn: str
    assistantAssociationArn: str
    assistantAssociationId: str
    assistantId: str
    associationData: AssistantAssociationOutputDataTypeDef
    associationType: Literal["KNOWLEDGE_BASE"]
    tags: NotRequired[Dict[str, str]]

class CreateAssistantResponseTypeDef(TypedDict):
    assistant: AssistantDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAssistantResponseTypeDef(TypedDict):
    assistant: AssistantDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAssistantsResponseTypeDef(TypedDict):
    assistantSummaries: List[AssistantSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ExternalSourceConfigurationTypeDef(TypedDict):
    configuration: ConfigurationTypeDef
    source: Literal["AMAZON_CONNECT"]

class DocumentTypeDef(TypedDict):
    contentReference: ContentReferenceTypeDef
    excerpt: NotRequired[DocumentTextTypeDef]
    title: NotRequired[DocumentTextTypeDef]

class SearchContentRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: SearchExpressionTypeDef
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class SearchContentRequestSearchContentPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: SearchExpressionTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchSessionsRequestRequestTypeDef(TypedDict):
    assistantId: str
    searchExpression: SearchExpressionTypeDef
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class SearchSessionsRequestSearchSessionsPaginateTypeDef(TypedDict):
    assistantId: str
    searchExpression: SearchExpressionTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

RecommendationTriggerTypeDef = TypedDict(
    "RecommendationTriggerTypeDef",
    {
        "data": RecommendationTriggerDataTypeDef,
        "id": str,
        "recommendationIds": List[str],
        "source": RecommendationSourceTypeType,
        "type": Literal["QUERY"],
    },
)

class QuickResponseDataTypeDef(TypedDict):
    contentType: str
    createdTime: datetime
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    name: str
    quickResponseArn: str
    quickResponseId: str
    status: QuickResponseStatusType
    channels: NotRequired[List[str]]
    contents: NotRequired[QuickResponseContentsTypeDef]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationOutputTypeDef]
    isActive: NotRequired[bool]
    language: NotRequired[str]
    lastModifiedBy: NotRequired[str]
    shortcutKey: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

class QuickResponseSearchResultDataTypeDef(TypedDict):
    contentType: str
    contents: QuickResponseContentsTypeDef
    createdTime: datetime
    isActive: bool
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    name: str
    quickResponseArn: str
    quickResponseId: str
    status: QuickResponseStatusType
    attributesInterpolated: NotRequired[List[str]]
    attributesNotInterpolated: NotRequired[List[str]]
    channels: NotRequired[List[str]]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationOutputTypeDef]
    language: NotRequired[str]
    lastModifiedBy: NotRequired[str]
    shortcutKey: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

class SearchQuickResponsesRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: QuickResponseSearchExpressionTypeDef
    attributes: NotRequired[Mapping[str, str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class SearchQuickResponsesRequestSearchQuickResponsesPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: QuickResponseSearchExpressionTypeDef
    attributes: NotRequired[Mapping[str, str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class CreateSessionResponseTypeDef(TypedDict):
    session: SessionDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSessionResponseTypeDef(TypedDict):
    session: SessionDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateKnowledgeBaseResponseTypeDef(TypedDict):
    knowledgeBase: KnowledgeBaseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetKnowledgeBaseResponseTypeDef(TypedDict):
    knowledgeBase: KnowledgeBaseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateKnowledgeBaseTemplateUriResponseTypeDef(TypedDict):
    knowledgeBase: KnowledgeBaseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListKnowledgeBasesResponseTypeDef(TypedDict):
    knowledgeBaseSummaries: List[KnowledgeBaseSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateKnowledgeBaseRequestRequestTypeDef(TypedDict):
    knowledgeBaseType: KnowledgeBaseTypeType
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    renderingConfiguration: NotRequired[RenderingConfigurationTypeDef]
    serverSideEncryptionConfiguration: NotRequired[ServerSideEncryptionConfigurationTypeDef]
    sourceConfiguration: NotRequired[SourceConfigurationTypeDef]
    tags: NotRequired[Mapping[str, str]]

class CreateAssistantAssociationResponseTypeDef(TypedDict):
    assistantAssociation: AssistantAssociationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAssistantAssociationResponseTypeDef(TypedDict):
    assistantAssociation: AssistantAssociationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAssistantAssociationsResponseTypeDef(TypedDict):
    assistantAssociationSummaries: List[AssistantAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ImportJobDataTypeDef(TypedDict):
    createdTime: datetime
    importJobId: str
    importJobType: Literal["QUICK_RESPONSES"]
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    status: ImportJobStatusType
    uploadId: str
    url: str
    urlExpiry: datetime
    externalSourceConfiguration: NotRequired[ExternalSourceConfigurationTypeDef]
    failedRecordReport: NotRequired[str]
    metadata: NotRequired[Dict[str, str]]

class ImportJobSummaryTypeDef(TypedDict):
    createdTime: datetime
    importJobId: str
    importJobType: Literal["QUICK_RESPONSES"]
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    status: ImportJobStatusType
    uploadId: str
    externalSourceConfiguration: NotRequired[ExternalSourceConfigurationTypeDef]
    metadata: NotRequired[Dict[str, str]]

class StartImportJobRequestRequestTypeDef(TypedDict):
    importJobType: Literal["QUICK_RESPONSES"]
    knowledgeBaseId: str
    uploadId: str
    clientToken: NotRequired[str]
    externalSourceConfiguration: NotRequired[ExternalSourceConfigurationTypeDef]
    metadata: NotRequired[Mapping[str, str]]

RecommendationDataTypeDef = TypedDict(
    "RecommendationDataTypeDef",
    {
        "document": DocumentTypeDef,
        "recommendationId": str,
        "relevanceLevel": NotRequired[RelevanceLevelType],
        "relevanceScore": NotRequired[float],
        "type": NotRequired[Literal["KNOWLEDGE_CONTENT"]],
    },
)

class ResultDataTypeDef(TypedDict):
    document: DocumentTypeDef
    resultId: str
    relevanceScore: NotRequired[float]

class CreateQuickResponseResponseTypeDef(TypedDict):
    quickResponse: QuickResponseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetQuickResponseResponseTypeDef(TypedDict):
    quickResponse: QuickResponseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateQuickResponseResponseTypeDef(TypedDict):
    quickResponse: QuickResponseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SearchQuickResponsesResponseTypeDef(TypedDict):
    results: List[QuickResponseSearchResultDataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetImportJobResponseTypeDef(TypedDict):
    importJob: ImportJobDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartImportJobResponseTypeDef(TypedDict):
    importJob: ImportJobDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListImportJobsResponseTypeDef(TypedDict):
    importJobSummaries: List[ImportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetRecommendationsResponseTypeDef(TypedDict):
    recommendations: List[RecommendationDataTypeDef]
    triggers: List[RecommendationTriggerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class QueryAssistantResponseTypeDef(TypedDict):
    results: List[ResultDataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
