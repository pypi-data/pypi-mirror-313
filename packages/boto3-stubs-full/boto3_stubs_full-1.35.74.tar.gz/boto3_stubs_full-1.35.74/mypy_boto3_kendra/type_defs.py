"""
Type annotations for kendra service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/type_defs/)

Usage::

    ```python
    from mypy_boto3_kendra.type_defs import AccessControlConfigurationSummaryTypeDef

    data: AccessControlConfigurationSummaryTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AlfrescoEntityType,
    AttributeSuggestionsModeType,
    ConditionOperatorType,
    ConfluenceAttachmentFieldNameType,
    ConfluenceAuthenticationTypeType,
    ConfluenceBlogFieldNameType,
    ConfluencePageFieldNameType,
    ConfluenceSpaceFieldNameType,
    ConfluenceVersionType,
    ContentTypeType,
    DatabaseEngineTypeType,
    DataSourceStatusType,
    DataSourceSyncJobStatusType,
    DataSourceTypeType,
    DocumentAttributeValueTypeType,
    DocumentStatusType,
    EntityTypeType,
    ErrorCodeType,
    ExperienceStatusType,
    FaqFileFormatType,
    FaqStatusType,
    FeaturedResultsSetStatusType,
    HighlightTypeType,
    IndexEditionType,
    IndexStatusType,
    IntervalType,
    IssueSubEntityType,
    KeyLocationType,
    MetricTypeType,
    MissingAttributeKeyStrategyType,
    ModeType,
    OrderType,
    PersonaType,
    PrincipalMappingStatusType,
    PrincipalTypeType,
    QueryIdentifiersEnclosingOptionType,
    QueryResultFormatType,
    QueryResultTypeType,
    QuerySuggestionsBlockListStatusType,
    QuerySuggestionsStatusType,
    ReadAccessTypeType,
    RelevanceTypeType,
    SalesforceChatterFeedIncludeFilterTypeType,
    SalesforceKnowledgeArticleStateType,
    SalesforceStandardObjectNameType,
    ScoreConfidenceType,
    ServiceNowAuthenticationTypeType,
    ServiceNowBuildVersionTypeType,
    SharePointOnlineAuthenticationTypeType,
    SharePointVersionType,
    SlackEntityType,
    SortOrderType,
    SuggestionTypeType,
    ThesaurusStatusType,
    TypeType,
    UserContextPolicyType,
    UserGroupResolutionModeType,
    WebCrawlerModeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccessControlConfigurationSummaryTypeDef",
    "AccessControlListConfigurationTypeDef",
    "AclConfigurationTypeDef",
    "AdditionalResultAttributeTypeDef",
    "AdditionalResultAttributeValueTypeDef",
    "AlfrescoConfigurationOutputTypeDef",
    "AlfrescoConfigurationTypeDef",
    "AlfrescoConfigurationUnionTypeDef",
    "AssociateEntitiesToExperienceRequestRequestTypeDef",
    "AssociateEntitiesToExperienceResponseTypeDef",
    "AssociatePersonasToEntitiesRequestRequestTypeDef",
    "AssociatePersonasToEntitiesResponseTypeDef",
    "AttributeFilterTypeDef",
    "AttributeSuggestionsDescribeConfigTypeDef",
    "AttributeSuggestionsGetConfigTypeDef",
    "AttributeSuggestionsUpdateConfigTypeDef",
    "AuthenticationConfigurationOutputTypeDef",
    "AuthenticationConfigurationTypeDef",
    "AuthenticationConfigurationUnionTypeDef",
    "BasicAuthenticationConfigurationTypeDef",
    "BatchDeleteDocumentRequestRequestTypeDef",
    "BatchDeleteDocumentResponseFailedDocumentTypeDef",
    "BatchDeleteDocumentResponseTypeDef",
    "BatchDeleteFeaturedResultsSetErrorTypeDef",
    "BatchDeleteFeaturedResultsSetRequestRequestTypeDef",
    "BatchDeleteFeaturedResultsSetResponseTypeDef",
    "BatchGetDocumentStatusRequestRequestTypeDef",
    "BatchGetDocumentStatusResponseErrorTypeDef",
    "BatchGetDocumentStatusResponseTypeDef",
    "BatchPutDocumentRequestRequestTypeDef",
    "BatchPutDocumentResponseFailedDocumentTypeDef",
    "BatchPutDocumentResponseTypeDef",
    "BlobTypeDef",
    "BoxConfigurationOutputTypeDef",
    "BoxConfigurationTypeDef",
    "BoxConfigurationUnionTypeDef",
    "CapacityUnitsConfigurationTypeDef",
    "ClearQuerySuggestionsRequestRequestTypeDef",
    "ClickFeedbackTypeDef",
    "CollapseConfigurationTypeDef",
    "CollapsedResultDetailTypeDef",
    "ColumnConfigurationOutputTypeDef",
    "ColumnConfigurationTypeDef",
    "ColumnConfigurationUnionTypeDef",
    "ConfluenceAttachmentConfigurationOutputTypeDef",
    "ConfluenceAttachmentConfigurationTypeDef",
    "ConfluenceAttachmentConfigurationUnionTypeDef",
    "ConfluenceAttachmentToIndexFieldMappingTypeDef",
    "ConfluenceBlogConfigurationOutputTypeDef",
    "ConfluenceBlogConfigurationTypeDef",
    "ConfluenceBlogConfigurationUnionTypeDef",
    "ConfluenceBlogToIndexFieldMappingTypeDef",
    "ConfluenceConfigurationOutputTypeDef",
    "ConfluenceConfigurationTypeDef",
    "ConfluenceConfigurationUnionTypeDef",
    "ConfluencePageConfigurationOutputTypeDef",
    "ConfluencePageConfigurationTypeDef",
    "ConfluencePageConfigurationUnionTypeDef",
    "ConfluencePageToIndexFieldMappingTypeDef",
    "ConfluenceSpaceConfigurationOutputTypeDef",
    "ConfluenceSpaceConfigurationTypeDef",
    "ConfluenceSpaceConfigurationUnionTypeDef",
    "ConfluenceSpaceToIndexFieldMappingTypeDef",
    "ConnectionConfigurationTypeDef",
    "ContentSourceConfigurationOutputTypeDef",
    "ContentSourceConfigurationTypeDef",
    "ContentSourceConfigurationUnionTypeDef",
    "CorrectionTypeDef",
    "CreateAccessControlConfigurationRequestRequestTypeDef",
    "CreateAccessControlConfigurationResponseTypeDef",
    "CreateDataSourceRequestRequestTypeDef",
    "CreateDataSourceResponseTypeDef",
    "CreateExperienceRequestRequestTypeDef",
    "CreateExperienceResponseTypeDef",
    "CreateFaqRequestRequestTypeDef",
    "CreateFaqResponseTypeDef",
    "CreateFeaturedResultsSetRequestRequestTypeDef",
    "CreateFeaturedResultsSetResponseTypeDef",
    "CreateIndexRequestRequestTypeDef",
    "CreateIndexResponseTypeDef",
    "CreateQuerySuggestionsBlockListRequestRequestTypeDef",
    "CreateQuerySuggestionsBlockListResponseTypeDef",
    "CreateThesaurusRequestRequestTypeDef",
    "CreateThesaurusResponseTypeDef",
    "CustomDocumentEnrichmentConfigurationOutputTypeDef",
    "CustomDocumentEnrichmentConfigurationTypeDef",
    "DataSourceConfigurationOutputTypeDef",
    "DataSourceConfigurationTypeDef",
    "DataSourceGroupTypeDef",
    "DataSourceSummaryTypeDef",
    "DataSourceSyncJobMetricTargetTypeDef",
    "DataSourceSyncJobMetricsTypeDef",
    "DataSourceSyncJobTypeDef",
    "DataSourceToIndexFieldMappingTypeDef",
    "DataSourceVpcConfigurationOutputTypeDef",
    "DataSourceVpcConfigurationTypeDef",
    "DataSourceVpcConfigurationUnionTypeDef",
    "DatabaseConfigurationOutputTypeDef",
    "DatabaseConfigurationTypeDef",
    "DatabaseConfigurationUnionTypeDef",
    "DeleteAccessControlConfigurationRequestRequestTypeDef",
    "DeleteDataSourceRequestRequestTypeDef",
    "DeleteExperienceRequestRequestTypeDef",
    "DeleteFaqRequestRequestTypeDef",
    "DeleteIndexRequestRequestTypeDef",
    "DeletePrincipalMappingRequestRequestTypeDef",
    "DeleteQuerySuggestionsBlockListRequestRequestTypeDef",
    "DeleteThesaurusRequestRequestTypeDef",
    "DescribeAccessControlConfigurationRequestRequestTypeDef",
    "DescribeAccessControlConfigurationResponseTypeDef",
    "DescribeDataSourceRequestRequestTypeDef",
    "DescribeDataSourceResponseTypeDef",
    "DescribeExperienceRequestRequestTypeDef",
    "DescribeExperienceResponseTypeDef",
    "DescribeFaqRequestRequestTypeDef",
    "DescribeFaqResponseTypeDef",
    "DescribeFeaturedResultsSetRequestRequestTypeDef",
    "DescribeFeaturedResultsSetResponseTypeDef",
    "DescribeIndexRequestRequestTypeDef",
    "DescribeIndexResponseTypeDef",
    "DescribePrincipalMappingRequestRequestTypeDef",
    "DescribePrincipalMappingResponseTypeDef",
    "DescribeQuerySuggestionsBlockListRequestRequestTypeDef",
    "DescribeQuerySuggestionsBlockListResponseTypeDef",
    "DescribeQuerySuggestionsConfigRequestRequestTypeDef",
    "DescribeQuerySuggestionsConfigResponseTypeDef",
    "DescribeThesaurusRequestRequestTypeDef",
    "DescribeThesaurusResponseTypeDef",
    "DisassociateEntitiesFromExperienceRequestRequestTypeDef",
    "DisassociateEntitiesFromExperienceResponseTypeDef",
    "DisassociatePersonasFromEntitiesRequestRequestTypeDef",
    "DisassociatePersonasFromEntitiesResponseTypeDef",
    "DocumentAttributeConditionOutputTypeDef",
    "DocumentAttributeConditionTypeDef",
    "DocumentAttributeConditionUnionTypeDef",
    "DocumentAttributeOutputTypeDef",
    "DocumentAttributeTargetOutputTypeDef",
    "DocumentAttributeTargetTypeDef",
    "DocumentAttributeTargetUnionTypeDef",
    "DocumentAttributeTypeDef",
    "DocumentAttributeUnionTypeDef",
    "DocumentAttributeValueCountPairTypeDef",
    "DocumentAttributeValueOutputTypeDef",
    "DocumentAttributeValueTypeDef",
    "DocumentAttributeValueUnionTypeDef",
    "DocumentInfoTypeDef",
    "DocumentMetadataConfigurationOutputTypeDef",
    "DocumentMetadataConfigurationTypeDef",
    "DocumentMetadataConfigurationUnionTypeDef",
    "DocumentRelevanceConfigurationTypeDef",
    "DocumentTypeDef",
    "DocumentsMetadataConfigurationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EntityConfigurationTypeDef",
    "EntityDisplayDataTypeDef",
    "EntityPersonaConfigurationTypeDef",
    "ExpandConfigurationTypeDef",
    "ExpandedResultItemTypeDef",
    "ExperienceConfigurationOutputTypeDef",
    "ExperienceConfigurationTypeDef",
    "ExperienceEndpointTypeDef",
    "ExperienceEntitiesSummaryTypeDef",
    "ExperiencesSummaryTypeDef",
    "FacetResultTypeDef",
    "FacetTypeDef",
    "FailedEntityTypeDef",
    "FaqStatisticsTypeDef",
    "FaqSummaryTypeDef",
    "FeaturedDocumentMissingTypeDef",
    "FeaturedDocumentTypeDef",
    "FeaturedDocumentWithMetadataTypeDef",
    "FeaturedResultsItemTypeDef",
    "FeaturedResultsSetSummaryTypeDef",
    "FeaturedResultsSetTypeDef",
    "FsxConfigurationOutputTypeDef",
    "FsxConfigurationTypeDef",
    "FsxConfigurationUnionTypeDef",
    "GetQuerySuggestionsRequestRequestTypeDef",
    "GetQuerySuggestionsResponseTypeDef",
    "GetSnapshotsRequestRequestTypeDef",
    "GetSnapshotsResponseTypeDef",
    "GitHubConfigurationOutputTypeDef",
    "GitHubConfigurationTypeDef",
    "GitHubConfigurationUnionTypeDef",
    "GitHubDocumentCrawlPropertiesTypeDef",
    "GoogleDriveConfigurationOutputTypeDef",
    "GoogleDriveConfigurationTypeDef",
    "GoogleDriveConfigurationUnionTypeDef",
    "GroupMembersTypeDef",
    "GroupOrderingIdSummaryTypeDef",
    "GroupSummaryTypeDef",
    "HierarchicalPrincipalOutputTypeDef",
    "HierarchicalPrincipalTypeDef",
    "HierarchicalPrincipalUnionTypeDef",
    "HighlightTypeDef",
    "HookConfigurationOutputTypeDef",
    "HookConfigurationTypeDef",
    "HookConfigurationUnionTypeDef",
    "IndexConfigurationSummaryTypeDef",
    "IndexStatisticsTypeDef",
    "InlineCustomDocumentEnrichmentConfigurationOutputTypeDef",
    "InlineCustomDocumentEnrichmentConfigurationTypeDef",
    "InlineCustomDocumentEnrichmentConfigurationUnionTypeDef",
    "JiraConfigurationOutputTypeDef",
    "JiraConfigurationTypeDef",
    "JiraConfigurationUnionTypeDef",
    "JsonTokenTypeConfigurationTypeDef",
    "JwtTokenTypeConfigurationTypeDef",
    "ListAccessControlConfigurationsRequestRequestTypeDef",
    "ListAccessControlConfigurationsResponseTypeDef",
    "ListDataSourceSyncJobsRequestRequestTypeDef",
    "ListDataSourceSyncJobsResponseTypeDef",
    "ListDataSourcesRequestRequestTypeDef",
    "ListDataSourcesResponseTypeDef",
    "ListEntityPersonasRequestRequestTypeDef",
    "ListEntityPersonasResponseTypeDef",
    "ListExperienceEntitiesRequestRequestTypeDef",
    "ListExperienceEntitiesResponseTypeDef",
    "ListExperiencesRequestRequestTypeDef",
    "ListExperiencesResponseTypeDef",
    "ListFaqsRequestRequestTypeDef",
    "ListFaqsResponseTypeDef",
    "ListFeaturedResultsSetsRequestRequestTypeDef",
    "ListFeaturedResultsSetsResponseTypeDef",
    "ListGroupsOlderThanOrderingIdRequestRequestTypeDef",
    "ListGroupsOlderThanOrderingIdResponseTypeDef",
    "ListIndicesRequestRequestTypeDef",
    "ListIndicesResponseTypeDef",
    "ListQuerySuggestionsBlockListsRequestRequestTypeDef",
    "ListQuerySuggestionsBlockListsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListThesauriRequestRequestTypeDef",
    "ListThesauriResponseTypeDef",
    "MemberGroupTypeDef",
    "MemberUserTypeDef",
    "OnPremiseConfigurationTypeDef",
    "OneDriveConfigurationOutputTypeDef",
    "OneDriveConfigurationTypeDef",
    "OneDriveConfigurationUnionTypeDef",
    "OneDriveUsersOutputTypeDef",
    "OneDriveUsersTypeDef",
    "OneDriveUsersUnionTypeDef",
    "PersonasSummaryTypeDef",
    "PrincipalTypeDef",
    "ProxyConfigurationTypeDef",
    "PutPrincipalMappingRequestRequestTypeDef",
    "QueryRequestRequestTypeDef",
    "QueryResultItemTypeDef",
    "QueryResultTypeDef",
    "QuerySuggestionsBlockListSummaryTypeDef",
    "QuipConfigurationOutputTypeDef",
    "QuipConfigurationTypeDef",
    "QuipConfigurationUnionTypeDef",
    "RelevanceFeedbackTypeDef",
    "RelevanceOutputTypeDef",
    "RelevanceTypeDef",
    "RelevanceUnionTypeDef",
    "ResponseMetadataTypeDef",
    "RetrieveRequestRequestTypeDef",
    "RetrieveResultItemTypeDef",
    "RetrieveResultTypeDef",
    "S3DataSourceConfigurationOutputTypeDef",
    "S3DataSourceConfigurationTypeDef",
    "S3DataSourceConfigurationUnionTypeDef",
    "S3PathTypeDef",
    "SaaSConfigurationTypeDef",
    "SalesforceChatterFeedConfigurationOutputTypeDef",
    "SalesforceChatterFeedConfigurationTypeDef",
    "SalesforceChatterFeedConfigurationUnionTypeDef",
    "SalesforceConfigurationOutputTypeDef",
    "SalesforceConfigurationTypeDef",
    "SalesforceConfigurationUnionTypeDef",
    "SalesforceCustomKnowledgeArticleTypeConfigurationOutputTypeDef",
    "SalesforceCustomKnowledgeArticleTypeConfigurationTypeDef",
    "SalesforceCustomKnowledgeArticleTypeConfigurationUnionTypeDef",
    "SalesforceKnowledgeArticleConfigurationOutputTypeDef",
    "SalesforceKnowledgeArticleConfigurationTypeDef",
    "SalesforceKnowledgeArticleConfigurationUnionTypeDef",
    "SalesforceStandardKnowledgeArticleTypeConfigurationOutputTypeDef",
    "SalesforceStandardKnowledgeArticleTypeConfigurationTypeDef",
    "SalesforceStandardKnowledgeArticleTypeConfigurationUnionTypeDef",
    "SalesforceStandardObjectAttachmentConfigurationOutputTypeDef",
    "SalesforceStandardObjectAttachmentConfigurationTypeDef",
    "SalesforceStandardObjectAttachmentConfigurationUnionTypeDef",
    "SalesforceStandardObjectConfigurationOutputTypeDef",
    "SalesforceStandardObjectConfigurationTypeDef",
    "SalesforceStandardObjectConfigurationUnionTypeDef",
    "ScoreAttributesTypeDef",
    "SearchTypeDef",
    "SeedUrlConfigurationOutputTypeDef",
    "SeedUrlConfigurationTypeDef",
    "SeedUrlConfigurationUnionTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "ServiceNowConfigurationOutputTypeDef",
    "ServiceNowConfigurationTypeDef",
    "ServiceNowConfigurationUnionTypeDef",
    "ServiceNowKnowledgeArticleConfigurationOutputTypeDef",
    "ServiceNowKnowledgeArticleConfigurationTypeDef",
    "ServiceNowKnowledgeArticleConfigurationUnionTypeDef",
    "ServiceNowServiceCatalogConfigurationOutputTypeDef",
    "ServiceNowServiceCatalogConfigurationTypeDef",
    "ServiceNowServiceCatalogConfigurationUnionTypeDef",
    "SharePointConfigurationOutputTypeDef",
    "SharePointConfigurationTypeDef",
    "SharePointConfigurationUnionTypeDef",
    "SiteMapsConfigurationOutputTypeDef",
    "SiteMapsConfigurationTypeDef",
    "SiteMapsConfigurationUnionTypeDef",
    "SlackConfigurationOutputTypeDef",
    "SlackConfigurationTypeDef",
    "SlackConfigurationUnionTypeDef",
    "SortingConfigurationTypeDef",
    "SourceDocumentTypeDef",
    "SpellCorrectedQueryTypeDef",
    "SpellCorrectionConfigurationTypeDef",
    "SqlConfigurationTypeDef",
    "StartDataSourceSyncJobRequestRequestTypeDef",
    "StartDataSourceSyncJobResponseTypeDef",
    "StatusTypeDef",
    "StopDataSourceSyncJobRequestRequestTypeDef",
    "SubmitFeedbackRequestRequestTypeDef",
    "SuggestableConfigTypeDef",
    "SuggestionHighlightTypeDef",
    "SuggestionTextWithHighlightsTypeDef",
    "SuggestionTypeDef",
    "SuggestionValueTypeDef",
    "TableCellTypeDef",
    "TableExcerptTypeDef",
    "TableRowTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TemplateConfigurationOutputTypeDef",
    "TemplateConfigurationTypeDef",
    "TemplateConfigurationUnionTypeDef",
    "TextDocumentStatisticsTypeDef",
    "TextWithHighlightsTypeDef",
    "ThesaurusSummaryTypeDef",
    "TimeRangeOutputTypeDef",
    "TimeRangeTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAccessControlConfigurationRequestRequestTypeDef",
    "UpdateDataSourceRequestRequestTypeDef",
    "UpdateExperienceRequestRequestTypeDef",
    "UpdateFeaturedResultsSetRequestRequestTypeDef",
    "UpdateFeaturedResultsSetResponseTypeDef",
    "UpdateIndexRequestRequestTypeDef",
    "UpdateQuerySuggestionsBlockListRequestRequestTypeDef",
    "UpdateQuerySuggestionsConfigRequestRequestTypeDef",
    "UpdateThesaurusRequestRequestTypeDef",
    "UrlsOutputTypeDef",
    "UrlsTypeDef",
    "UrlsUnionTypeDef",
    "UserContextTypeDef",
    "UserGroupResolutionConfigurationTypeDef",
    "UserIdentityConfigurationTypeDef",
    "UserTokenConfigurationTypeDef",
    "WarningTypeDef",
    "WebCrawlerConfigurationOutputTypeDef",
    "WebCrawlerConfigurationTypeDef",
    "WebCrawlerConfigurationUnionTypeDef",
    "WorkDocsConfigurationOutputTypeDef",
    "WorkDocsConfigurationTypeDef",
    "WorkDocsConfigurationUnionTypeDef",
)


class AccessControlConfigurationSummaryTypeDef(TypedDict):
    Id: str


class AccessControlListConfigurationTypeDef(TypedDict):
    KeyPath: NotRequired[str]


class AclConfigurationTypeDef(TypedDict):
    AllowedGroupsColumnName: str


class DataSourceToIndexFieldMappingTypeDef(TypedDict):
    DataSourceFieldName: str
    IndexFieldName: str
    DateFieldFormat: NotRequired[str]


class DataSourceVpcConfigurationOutputTypeDef(TypedDict):
    SubnetIds: List[str]
    SecurityGroupIds: List[str]


class S3PathTypeDef(TypedDict):
    Bucket: str
    Key: str


class EntityConfigurationTypeDef(TypedDict):
    EntityId: str
    EntityType: EntityTypeType


class FailedEntityTypeDef(TypedDict):
    EntityId: NotRequired[str]
    ErrorMessage: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class EntityPersonaConfigurationTypeDef(TypedDict):
    EntityId: str
    Persona: PersonaType


class SuggestableConfigTypeDef(TypedDict):
    AttributeName: NotRequired[str]
    Suggestable: NotRequired[bool]


class BasicAuthenticationConfigurationTypeDef(TypedDict):
    Host: str
    Port: int
    Credentials: str


class DataSourceSyncJobMetricTargetTypeDef(TypedDict):
    DataSourceId: str
    DataSourceSyncJobId: NotRequired[str]


class BatchDeleteDocumentResponseFailedDocumentTypeDef(TypedDict):
    Id: NotRequired[str]
    ErrorCode: NotRequired[ErrorCodeType]
    ErrorMessage: NotRequired[str]


class BatchDeleteFeaturedResultsSetErrorTypeDef(TypedDict):
    Id: str
    ErrorCode: ErrorCodeType
    ErrorMessage: str


class BatchDeleteFeaturedResultsSetRequestRequestTypeDef(TypedDict):
    IndexId: str
    FeaturedResultsSetIds: Sequence[str]


class BatchGetDocumentStatusResponseErrorTypeDef(TypedDict):
    DocumentId: NotRequired[str]
    ErrorCode: NotRequired[ErrorCodeType]
    ErrorMessage: NotRequired[str]


class StatusTypeDef(TypedDict):
    DocumentId: NotRequired[str]
    DocumentStatus: NotRequired[DocumentStatusType]
    FailureCode: NotRequired[str]
    FailureReason: NotRequired[str]


class BatchPutDocumentResponseFailedDocumentTypeDef(TypedDict):
    Id: NotRequired[str]
    ErrorCode: NotRequired[ErrorCodeType]
    ErrorMessage: NotRequired[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class CapacityUnitsConfigurationTypeDef(TypedDict):
    StorageCapacityUnits: int
    QueryCapacityUnits: int


class ClearQuerySuggestionsRequestRequestTypeDef(TypedDict):
    IndexId: str


TimestampTypeDef = Union[datetime, str]


class ExpandConfigurationTypeDef(TypedDict):
    MaxResultItemsToExpand: NotRequired[int]
    MaxExpandedResultsPerItem: NotRequired[int]


class SortingConfigurationTypeDef(TypedDict):
    DocumentAttributeKey: str
    SortOrder: SortOrderType


class ConfluenceAttachmentToIndexFieldMappingTypeDef(TypedDict):
    DataSourceFieldName: NotRequired[ConfluenceAttachmentFieldNameType]
    DateFieldFormat: NotRequired[str]
    IndexFieldName: NotRequired[str]


class ConfluenceBlogToIndexFieldMappingTypeDef(TypedDict):
    DataSourceFieldName: NotRequired[ConfluenceBlogFieldNameType]
    DateFieldFormat: NotRequired[str]
    IndexFieldName: NotRequired[str]


class ProxyConfigurationTypeDef(TypedDict):
    Host: str
    Port: int
    Credentials: NotRequired[str]


class ConfluencePageToIndexFieldMappingTypeDef(TypedDict):
    DataSourceFieldName: NotRequired[ConfluencePageFieldNameType]
    DateFieldFormat: NotRequired[str]
    IndexFieldName: NotRequired[str]


class ConfluenceSpaceToIndexFieldMappingTypeDef(TypedDict):
    DataSourceFieldName: NotRequired[ConfluenceSpaceFieldNameType]
    DateFieldFormat: NotRequired[str]
    IndexFieldName: NotRequired[str]


class ConnectionConfigurationTypeDef(TypedDict):
    DatabaseHost: str
    DatabasePort: int
    DatabaseName: str
    TableName: str
    SecretArn: str


class ContentSourceConfigurationOutputTypeDef(TypedDict):
    DataSourceIds: NotRequired[List[str]]
    FaqIds: NotRequired[List[str]]
    DirectPutContent: NotRequired[bool]


class ContentSourceConfigurationTypeDef(TypedDict):
    DataSourceIds: NotRequired[Sequence[str]]
    FaqIds: NotRequired[Sequence[str]]
    DirectPutContent: NotRequired[bool]


class CorrectionTypeDef(TypedDict):
    BeginOffset: NotRequired[int]
    EndOffset: NotRequired[int]
    Term: NotRequired[str]
    CorrectedTerm: NotRequired[str]


PrincipalTypeDef = TypedDict(
    "PrincipalTypeDef",
    {
        "Name": str,
        "Type": PrincipalTypeType,
        "Access": ReadAccessTypeType,
        "DataSourceId": NotRequired[str],
    },
)


class DataSourceVpcConfigurationTypeDef(TypedDict):
    SubnetIds: Sequence[str]
    SecurityGroupIds: Sequence[str]


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class FeaturedDocumentTypeDef(TypedDict):
    Id: NotRequired[str]


class ServerSideEncryptionConfigurationTypeDef(TypedDict):
    KmsKeyId: NotRequired[str]


class UserGroupResolutionConfigurationTypeDef(TypedDict):
    UserGroupResolutionMode: UserGroupResolutionModeType


class TemplateConfigurationOutputTypeDef(TypedDict):
    Template: NotRequired[Dict[str, Any]]


class DataSourceGroupTypeDef(TypedDict):
    GroupId: str
    DataSourceId: str


DataSourceSummaryTypeDef = TypedDict(
    "DataSourceSummaryTypeDef",
    {
        "Name": NotRequired[str],
        "Id": NotRequired[str],
        "Type": NotRequired[DataSourceTypeType],
        "CreatedAt": NotRequired[datetime],
        "UpdatedAt": NotRequired[datetime],
        "Status": NotRequired[DataSourceStatusType],
        "LanguageCode": NotRequired[str],
    },
)


class DataSourceSyncJobMetricsTypeDef(TypedDict):
    DocumentsAdded: NotRequired[str]
    DocumentsModified: NotRequired[str]
    DocumentsDeleted: NotRequired[str]
    DocumentsFailed: NotRequired[str]
    DocumentsScanned: NotRequired[str]


class SqlConfigurationTypeDef(TypedDict):
    QueryIdentifiersEnclosingOption: NotRequired[QueryIdentifiersEnclosingOptionType]


class DeleteAccessControlConfigurationRequestRequestTypeDef(TypedDict):
    IndexId: str
    Id: str


class DeleteDataSourceRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str


class DeleteExperienceRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str


class DeleteFaqRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str


class DeleteIndexRequestRequestTypeDef(TypedDict):
    Id: str


class DeletePrincipalMappingRequestRequestTypeDef(TypedDict):
    IndexId: str
    GroupId: str
    DataSourceId: NotRequired[str]
    OrderingId: NotRequired[int]


class DeleteQuerySuggestionsBlockListRequestRequestTypeDef(TypedDict):
    IndexId: str
    Id: str


class DeleteThesaurusRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str


class DescribeAccessControlConfigurationRequestRequestTypeDef(TypedDict):
    IndexId: str
    Id: str


class DescribeDataSourceRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str


class DescribeExperienceRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str


class ExperienceEndpointTypeDef(TypedDict):
    EndpointType: NotRequired[Literal["HOME"]]
    Endpoint: NotRequired[str]


class DescribeFaqRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str


class DescribeFeaturedResultsSetRequestRequestTypeDef(TypedDict):
    IndexId: str
    FeaturedResultsSetId: str


class FeaturedDocumentMissingTypeDef(TypedDict):
    Id: NotRequired[str]


class FeaturedDocumentWithMetadataTypeDef(TypedDict):
    Id: NotRequired[str]
    Title: NotRequired[str]
    URI: NotRequired[str]


class DescribeIndexRequestRequestTypeDef(TypedDict):
    Id: str


class DescribePrincipalMappingRequestRequestTypeDef(TypedDict):
    IndexId: str
    GroupId: str
    DataSourceId: NotRequired[str]


class GroupOrderingIdSummaryTypeDef(TypedDict):
    Status: NotRequired[PrincipalMappingStatusType]
    LastUpdatedAt: NotRequired[datetime]
    ReceivedAt: NotRequired[datetime]
    OrderingId: NotRequired[int]
    FailureReason: NotRequired[str]


class DescribeQuerySuggestionsBlockListRequestRequestTypeDef(TypedDict):
    IndexId: str
    Id: str


class DescribeQuerySuggestionsConfigRequestRequestTypeDef(TypedDict):
    IndexId: str


class DescribeThesaurusRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str


class DisassociatePersonasFromEntitiesRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str
    EntityIds: Sequence[str]


class DocumentAttributeValueOutputTypeDef(TypedDict):
    StringValue: NotRequired[str]
    StringListValue: NotRequired[List[str]]
    LongValue: NotRequired[int]
    DateValue: NotRequired[datetime]


class RelevanceOutputTypeDef(TypedDict):
    Freshness: NotRequired[bool]
    Importance: NotRequired[int]
    Duration: NotRequired[str]
    RankOrder: NotRequired[OrderType]
    ValueImportanceMap: NotRequired[Dict[str, int]]


class SearchTypeDef(TypedDict):
    Facetable: NotRequired[bool]
    Searchable: NotRequired[bool]
    Displayable: NotRequired[bool]
    Sortable: NotRequired[bool]


class DocumentsMetadataConfigurationTypeDef(TypedDict):
    S3Prefix: NotRequired[str]


class EntityDisplayDataTypeDef(TypedDict):
    UserName: NotRequired[str]
    GroupName: NotRequired[str]
    IdentifiedUserName: NotRequired[str]
    FirstName: NotRequired[str]
    LastName: NotRequired[str]


class UserIdentityConfigurationTypeDef(TypedDict):
    IdentityAttributeName: NotRequired[str]


class FacetTypeDef(TypedDict):
    DocumentAttributeKey: NotRequired[str]
    Facets: NotRequired[Sequence[Mapping[str, Any]]]
    MaxResults: NotRequired[int]


class FaqStatisticsTypeDef(TypedDict):
    IndexedQuestionAnswersCount: int


class FaqSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[FaqStatusType]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]
    FileFormat: NotRequired[FaqFileFormatType]
    LanguageCode: NotRequired[str]


class FeaturedResultsSetSummaryTypeDef(TypedDict):
    FeaturedResultsSetId: NotRequired[str]
    FeaturedResultsSetName: NotRequired[str]
    Status: NotRequired[FeaturedResultsSetStatusType]
    LastUpdatedTimestamp: NotRequired[int]
    CreationTimestamp: NotRequired[int]


class GetSnapshotsRequestRequestTypeDef(TypedDict):
    IndexId: str
    Interval: IntervalType
    MetricType: MetricTypeType
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class TimeRangeOutputTypeDef(TypedDict):
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]


class GitHubDocumentCrawlPropertiesTypeDef(TypedDict):
    CrawlRepositoryDocuments: NotRequired[bool]
    CrawlIssue: NotRequired[bool]
    CrawlIssueComment: NotRequired[bool]
    CrawlIssueCommentAttachment: NotRequired[bool]
    CrawlPullRequest: NotRequired[bool]
    CrawlPullRequestComment: NotRequired[bool]
    CrawlPullRequestCommentAttachment: NotRequired[bool]


class SaaSConfigurationTypeDef(TypedDict):
    OrganizationName: str
    HostUrl: str


class MemberGroupTypeDef(TypedDict):
    GroupId: str
    DataSourceId: NotRequired[str]


class MemberUserTypeDef(TypedDict):
    UserId: str


class GroupSummaryTypeDef(TypedDict):
    GroupId: NotRequired[str]
    OrderingId: NotRequired[int]


HighlightTypeDef = TypedDict(
    "HighlightTypeDef",
    {
        "BeginOffset": int,
        "EndOffset": int,
        "TopAnswer": NotRequired[bool],
        "Type": NotRequired[HighlightTypeType],
    },
)


class IndexConfigurationSummaryTypeDef(TypedDict):
    CreatedAt: datetime
    UpdatedAt: datetime
    Status: IndexStatusType
    Name: NotRequired[str]
    Id: NotRequired[str]
    Edition: NotRequired[IndexEditionType]


class TextDocumentStatisticsTypeDef(TypedDict):
    IndexedTextDocumentsCount: int
    IndexedTextBytes: int


class JsonTokenTypeConfigurationTypeDef(TypedDict):
    UserNameAttributeField: str
    GroupAttributeField: str


class JwtTokenTypeConfigurationTypeDef(TypedDict):
    KeyLocation: KeyLocationType
    URL: NotRequired[str]
    SecretManagerArn: NotRequired[str]
    UserNameAttributeField: NotRequired[str]
    GroupAttributeField: NotRequired[str]
    Issuer: NotRequired[str]
    ClaimRegex: NotRequired[str]


class ListAccessControlConfigurationsRequestRequestTypeDef(TypedDict):
    IndexId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDataSourcesRequestRequestTypeDef(TypedDict):
    IndexId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListEntityPersonasRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class PersonasSummaryTypeDef(TypedDict):
    EntityId: NotRequired[str]
    Persona: NotRequired[PersonaType]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]


class ListExperienceEntitiesRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str
    NextToken: NotRequired[str]


class ListExperiencesRequestRequestTypeDef(TypedDict):
    IndexId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListFaqsRequestRequestTypeDef(TypedDict):
    IndexId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListFeaturedResultsSetsRequestRequestTypeDef(TypedDict):
    IndexId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListGroupsOlderThanOrderingIdRequestRequestTypeDef(TypedDict):
    IndexId: str
    OrderingId: int
    DataSourceId: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListIndicesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListQuerySuggestionsBlockListsRequestRequestTypeDef(TypedDict):
    IndexId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class QuerySuggestionsBlockListSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[QuerySuggestionsBlockListStatusType]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]
    ItemCount: NotRequired[int]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str


class ListThesauriRequestRequestTypeDef(TypedDict):
    IndexId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ThesaurusSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[ThesaurusStatusType]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]


class SpellCorrectionConfigurationTypeDef(TypedDict):
    IncludeQuerySpellCheckSuggestions: bool


class ScoreAttributesTypeDef(TypedDict):
    ScoreConfidence: NotRequired[ScoreConfidenceType]


class WarningTypeDef(TypedDict):
    Message: NotRequired[str]
    Code: NotRequired[Literal["QUERY_LANGUAGE_INVALID_SYNTAX"]]


class RelevanceFeedbackTypeDef(TypedDict):
    ResultId: str
    RelevanceValue: RelevanceTypeType


class RelevanceTypeDef(TypedDict):
    Freshness: NotRequired[bool]
    Importance: NotRequired[int]
    Duration: NotRequired[str]
    RankOrder: NotRequired[OrderType]
    ValueImportanceMap: NotRequired[Mapping[str, int]]


class SeedUrlConfigurationOutputTypeDef(TypedDict):
    SeedUrls: List[str]
    WebCrawlerMode: NotRequired[WebCrawlerModeType]


class SeedUrlConfigurationTypeDef(TypedDict):
    SeedUrls: Sequence[str]
    WebCrawlerMode: NotRequired[WebCrawlerModeType]


class SiteMapsConfigurationOutputTypeDef(TypedDict):
    SiteMaps: List[str]


class SiteMapsConfigurationTypeDef(TypedDict):
    SiteMaps: Sequence[str]


class StartDataSourceSyncJobRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str


class StopDataSourceSyncJobRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str


class SuggestionHighlightTypeDef(TypedDict):
    BeginOffset: NotRequired[int]
    EndOffset: NotRequired[int]


class TableCellTypeDef(TypedDict):
    Value: NotRequired[str]
    TopAnswer: NotRequired[bool]
    Highlighted: NotRequired[bool]
    Header: NotRequired[bool]


class TemplateConfigurationTypeDef(TypedDict):
    Template: NotRequired[Mapping[str, Any]]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


class ColumnConfigurationOutputTypeDef(TypedDict):
    DocumentIdColumnName: str
    DocumentDataColumnName: str
    ChangeDetectingColumns: List[str]
    DocumentTitleColumnName: NotRequired[str]
    FieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]


class ColumnConfigurationTypeDef(TypedDict):
    DocumentIdColumnName: str
    DocumentDataColumnName: str
    ChangeDetectingColumns: Sequence[str]
    DocumentTitleColumnName: NotRequired[str]
    FieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]


class GoogleDriveConfigurationOutputTypeDef(TypedDict):
    SecretArn: str
    InclusionPatterns: NotRequired[List[str]]
    ExclusionPatterns: NotRequired[List[str]]
    FieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    ExcludeMimeTypes: NotRequired[List[str]]
    ExcludeUserAccounts: NotRequired[List[str]]
    ExcludeSharedDrives: NotRequired[List[str]]


class GoogleDriveConfigurationTypeDef(TypedDict):
    SecretArn: str
    InclusionPatterns: NotRequired[Sequence[str]]
    ExclusionPatterns: NotRequired[Sequence[str]]
    FieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    ExcludeMimeTypes: NotRequired[Sequence[str]]
    ExcludeUserAccounts: NotRequired[Sequence[str]]
    ExcludeSharedDrives: NotRequired[Sequence[str]]


class SalesforceChatterFeedConfigurationOutputTypeDef(TypedDict):
    DocumentDataFieldName: str
    DocumentTitleFieldName: NotRequired[str]
    FieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    IncludeFilterTypes: NotRequired[List[SalesforceChatterFeedIncludeFilterTypeType]]


class SalesforceChatterFeedConfigurationTypeDef(TypedDict):
    DocumentDataFieldName: str
    DocumentTitleFieldName: NotRequired[str]
    FieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    IncludeFilterTypes: NotRequired[Sequence[SalesforceChatterFeedIncludeFilterTypeType]]


class SalesforceCustomKnowledgeArticleTypeConfigurationOutputTypeDef(TypedDict):
    Name: str
    DocumentDataFieldName: str
    DocumentTitleFieldName: NotRequired[str]
    FieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]


class SalesforceCustomKnowledgeArticleTypeConfigurationTypeDef(TypedDict):
    Name: str
    DocumentDataFieldName: str
    DocumentTitleFieldName: NotRequired[str]
    FieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]


class SalesforceStandardKnowledgeArticleTypeConfigurationOutputTypeDef(TypedDict):
    DocumentDataFieldName: str
    DocumentTitleFieldName: NotRequired[str]
    FieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]


class SalesforceStandardKnowledgeArticleTypeConfigurationTypeDef(TypedDict):
    DocumentDataFieldName: str
    DocumentTitleFieldName: NotRequired[str]
    FieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]


class SalesforceStandardObjectAttachmentConfigurationOutputTypeDef(TypedDict):
    DocumentTitleFieldName: NotRequired[str]
    FieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]


class SalesforceStandardObjectAttachmentConfigurationTypeDef(TypedDict):
    DocumentTitleFieldName: NotRequired[str]
    FieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]


class SalesforceStandardObjectConfigurationOutputTypeDef(TypedDict):
    Name: SalesforceStandardObjectNameType
    DocumentDataFieldName: str
    DocumentTitleFieldName: NotRequired[str]
    FieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]


class SalesforceStandardObjectConfigurationTypeDef(TypedDict):
    Name: SalesforceStandardObjectNameType
    DocumentDataFieldName: str
    DocumentTitleFieldName: NotRequired[str]
    FieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]


class ServiceNowKnowledgeArticleConfigurationOutputTypeDef(TypedDict):
    DocumentDataFieldName: str
    CrawlAttachments: NotRequired[bool]
    IncludeAttachmentFilePatterns: NotRequired[List[str]]
    ExcludeAttachmentFilePatterns: NotRequired[List[str]]
    DocumentTitleFieldName: NotRequired[str]
    FieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    FilterQuery: NotRequired[str]


class ServiceNowKnowledgeArticleConfigurationTypeDef(TypedDict):
    DocumentDataFieldName: str
    CrawlAttachments: NotRequired[bool]
    IncludeAttachmentFilePatterns: NotRequired[Sequence[str]]
    ExcludeAttachmentFilePatterns: NotRequired[Sequence[str]]
    DocumentTitleFieldName: NotRequired[str]
    FieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    FilterQuery: NotRequired[str]


class ServiceNowServiceCatalogConfigurationOutputTypeDef(TypedDict):
    DocumentDataFieldName: str
    CrawlAttachments: NotRequired[bool]
    IncludeAttachmentFilePatterns: NotRequired[List[str]]
    ExcludeAttachmentFilePatterns: NotRequired[List[str]]
    DocumentTitleFieldName: NotRequired[str]
    FieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]


class ServiceNowServiceCatalogConfigurationTypeDef(TypedDict):
    DocumentDataFieldName: str
    CrawlAttachments: NotRequired[bool]
    IncludeAttachmentFilePatterns: NotRequired[Sequence[str]]
    ExcludeAttachmentFilePatterns: NotRequired[Sequence[str]]
    DocumentTitleFieldName: NotRequired[str]
    FieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]


class WorkDocsConfigurationOutputTypeDef(TypedDict):
    OrganizationId: str
    CrawlComments: NotRequired[bool]
    UseChangeLog: NotRequired[bool]
    InclusionPatterns: NotRequired[List[str]]
    ExclusionPatterns: NotRequired[List[str]]
    FieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]


class WorkDocsConfigurationTypeDef(TypedDict):
    OrganizationId: str
    CrawlComments: NotRequired[bool]
    UseChangeLog: NotRequired[bool]
    InclusionPatterns: NotRequired[Sequence[str]]
    ExclusionPatterns: NotRequired[Sequence[str]]
    FieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]


class BoxConfigurationOutputTypeDef(TypedDict):
    EnterpriseId: str
    SecretArn: str
    UseChangeLog: NotRequired[bool]
    CrawlComments: NotRequired[bool]
    CrawlTasks: NotRequired[bool]
    CrawlWebLinks: NotRequired[bool]
    FileFieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    TaskFieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    CommentFieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    WebLinkFieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    InclusionPatterns: NotRequired[List[str]]
    ExclusionPatterns: NotRequired[List[str]]
    VpcConfiguration: NotRequired[DataSourceVpcConfigurationOutputTypeDef]


class FsxConfigurationOutputTypeDef(TypedDict):
    FileSystemId: str
    FileSystemType: Literal["WINDOWS"]
    VpcConfiguration: DataSourceVpcConfigurationOutputTypeDef
    SecretArn: NotRequired[str]
    InclusionPatterns: NotRequired[List[str]]
    ExclusionPatterns: NotRequired[List[str]]
    FieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]


class JiraConfigurationOutputTypeDef(TypedDict):
    JiraAccountUrl: str
    SecretArn: str
    UseChangeLog: NotRequired[bool]
    Project: NotRequired[List[str]]
    IssueType: NotRequired[List[str]]
    Status: NotRequired[List[str]]
    IssueSubEntityFilter: NotRequired[List[IssueSubEntityType]]
    AttachmentFieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    CommentFieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    IssueFieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    ProjectFieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    WorkLogFieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    InclusionPatterns: NotRequired[List[str]]
    ExclusionPatterns: NotRequired[List[str]]
    VpcConfiguration: NotRequired[DataSourceVpcConfigurationOutputTypeDef]


class QuipConfigurationOutputTypeDef(TypedDict):
    Domain: str
    SecretArn: str
    CrawlFileComments: NotRequired[bool]
    CrawlChatRooms: NotRequired[bool]
    CrawlAttachments: NotRequired[bool]
    FolderIds: NotRequired[List[str]]
    ThreadFieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    MessageFieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    AttachmentFieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    InclusionPatterns: NotRequired[List[str]]
    ExclusionPatterns: NotRequired[List[str]]
    VpcConfiguration: NotRequired[DataSourceVpcConfigurationOutputTypeDef]


class SlackConfigurationOutputTypeDef(TypedDict):
    TeamId: str
    SecretArn: str
    SlackEntityList: List[SlackEntityType]
    SinceCrawlDate: str
    VpcConfiguration: NotRequired[DataSourceVpcConfigurationOutputTypeDef]
    UseChangeLog: NotRequired[bool]
    CrawlBotMessage: NotRequired[bool]
    ExcludeArchived: NotRequired[bool]
    LookBackPeriod: NotRequired[int]
    PrivateChannelFilter: NotRequired[List[str]]
    PublicChannelFilter: NotRequired[List[str]]
    InclusionPatterns: NotRequired[List[str]]
    ExclusionPatterns: NotRequired[List[str]]
    FieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]


class AlfrescoConfigurationOutputTypeDef(TypedDict):
    SiteUrl: str
    SiteId: str
    SecretArn: str
    SslCertificateS3Path: S3PathTypeDef
    CrawlSystemFolders: NotRequired[bool]
    CrawlComments: NotRequired[bool]
    EntityFilter: NotRequired[List[AlfrescoEntityType]]
    DocumentLibraryFieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    BlogFieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    WikiFieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    InclusionPatterns: NotRequired[List[str]]
    ExclusionPatterns: NotRequired[List[str]]
    VpcConfiguration: NotRequired[DataSourceVpcConfigurationOutputTypeDef]


class OnPremiseConfigurationTypeDef(TypedDict):
    HostUrl: str
    OrganizationName: str
    SslCertificateS3Path: S3PathTypeDef


class OneDriveUsersOutputTypeDef(TypedDict):
    OneDriveUserList: NotRequired[List[str]]
    OneDriveUserS3Path: NotRequired[S3PathTypeDef]


class OneDriveUsersTypeDef(TypedDict):
    OneDriveUserList: NotRequired[Sequence[str]]
    OneDriveUserS3Path: NotRequired[S3PathTypeDef]


class UpdateQuerySuggestionsBlockListRequestRequestTypeDef(TypedDict):
    IndexId: str
    Id: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    SourceS3Path: NotRequired[S3PathTypeDef]
    RoleArn: NotRequired[str]


class UpdateThesaurusRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    RoleArn: NotRequired[str]
    SourceS3Path: NotRequired[S3PathTypeDef]


class AssociateEntitiesToExperienceRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str
    EntityList: Sequence[EntityConfigurationTypeDef]


class DisassociateEntitiesFromExperienceRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str
    EntityList: Sequence[EntityConfigurationTypeDef]


class AssociateEntitiesToExperienceResponseTypeDef(TypedDict):
    FailedEntityList: List[FailedEntityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class AssociatePersonasToEntitiesResponseTypeDef(TypedDict):
    FailedEntityList: List[FailedEntityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAccessControlConfigurationResponseTypeDef(TypedDict):
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataSourceResponseTypeDef(TypedDict):
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateExperienceResponseTypeDef(TypedDict):
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFaqResponseTypeDef(TypedDict):
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateIndexResponseTypeDef(TypedDict):
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateQuerySuggestionsBlockListResponseTypeDef(TypedDict):
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateThesaurusResponseTypeDef(TypedDict):
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFaqResponseTypeDef(TypedDict):
    Id: str
    IndexId: str
    Name: str
    Description: str
    CreatedAt: datetime
    UpdatedAt: datetime
    S3Path: S3PathTypeDef
    Status: FaqStatusType
    RoleArn: str
    ErrorMessage: str
    FileFormat: FaqFileFormatType
    LanguageCode: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeQuerySuggestionsBlockListResponseTypeDef(TypedDict):
    IndexId: str
    Id: str
    Name: str
    Description: str
    Status: QuerySuggestionsBlockListStatusType
    ErrorMessage: str
    CreatedAt: datetime
    UpdatedAt: datetime
    SourceS3Path: S3PathTypeDef
    ItemCount: int
    FileSizeBytes: int
    RoleArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeThesaurusResponseTypeDef(TypedDict):
    Id: str
    IndexId: str
    Name: str
    Description: str
    Status: ThesaurusStatusType
    ErrorMessage: str
    CreatedAt: datetime
    UpdatedAt: datetime
    RoleArn: str
    SourceS3Path: S3PathTypeDef
    FileSizeBytes: int
    TermCount: int
    SynonymRuleCount: int
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateEntitiesFromExperienceResponseTypeDef(TypedDict):
    FailedEntityList: List[FailedEntityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociatePersonasFromEntitiesResponseTypeDef(TypedDict):
    FailedEntityList: List[FailedEntityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ListAccessControlConfigurationsResponseTypeDef(TypedDict):
    AccessControlConfigurations: List[AccessControlConfigurationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StartDataSourceSyncJobResponseTypeDef(TypedDict):
    ExecutionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociatePersonasToEntitiesRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str
    Personas: Sequence[EntityPersonaConfigurationTypeDef]


class AttributeSuggestionsDescribeConfigTypeDef(TypedDict):
    SuggestableConfigList: NotRequired[List[SuggestableConfigTypeDef]]
    AttributeSuggestionsMode: NotRequired[AttributeSuggestionsModeType]


class AttributeSuggestionsUpdateConfigTypeDef(TypedDict):
    SuggestableConfigList: NotRequired[Sequence[SuggestableConfigTypeDef]]
    AttributeSuggestionsMode: NotRequired[AttributeSuggestionsModeType]


class AuthenticationConfigurationOutputTypeDef(TypedDict):
    BasicAuthentication: NotRequired[List[BasicAuthenticationConfigurationTypeDef]]


class AuthenticationConfigurationTypeDef(TypedDict):
    BasicAuthentication: NotRequired[Sequence[BasicAuthenticationConfigurationTypeDef]]


class BatchDeleteDocumentRequestRequestTypeDef(TypedDict):
    IndexId: str
    DocumentIdList: Sequence[str]
    DataSourceSyncJobMetricTarget: NotRequired[DataSourceSyncJobMetricTargetTypeDef]


class BatchDeleteDocumentResponseTypeDef(TypedDict):
    FailedDocuments: List[BatchDeleteDocumentResponseFailedDocumentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchDeleteFeaturedResultsSetResponseTypeDef(TypedDict):
    Errors: List[BatchDeleteFeaturedResultsSetErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchGetDocumentStatusResponseTypeDef(TypedDict):
    Errors: List[BatchGetDocumentStatusResponseErrorTypeDef]
    DocumentStatusList: List[StatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchPutDocumentResponseTypeDef(TypedDict):
    FailedDocuments: List[BatchPutDocumentResponseFailedDocumentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ClickFeedbackTypeDef(TypedDict):
    ResultId: str
    ClickTime: TimestampTypeDef


class DocumentAttributeValueTypeDef(TypedDict):
    StringValue: NotRequired[str]
    StringListValue: NotRequired[Sequence[str]]
    LongValue: NotRequired[int]
    DateValue: NotRequired[TimestampTypeDef]


class TimeRangeTypeDef(TypedDict):
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]


class CollapseConfigurationTypeDef(TypedDict):
    DocumentAttributeKey: str
    SortingConfigurations: NotRequired[Sequence[SortingConfigurationTypeDef]]
    MissingAttributeKeyStrategy: NotRequired[MissingAttributeKeyStrategyType]
    Expand: NotRequired[bool]
    ExpandConfiguration: NotRequired[ExpandConfigurationTypeDef]


class ConfluenceAttachmentConfigurationOutputTypeDef(TypedDict):
    CrawlAttachments: NotRequired[bool]
    AttachmentFieldMappings: NotRequired[List[ConfluenceAttachmentToIndexFieldMappingTypeDef]]


class ConfluenceAttachmentConfigurationTypeDef(TypedDict):
    CrawlAttachments: NotRequired[bool]
    AttachmentFieldMappings: NotRequired[Sequence[ConfluenceAttachmentToIndexFieldMappingTypeDef]]


class ConfluenceBlogConfigurationOutputTypeDef(TypedDict):
    BlogFieldMappings: NotRequired[List[ConfluenceBlogToIndexFieldMappingTypeDef]]


class ConfluenceBlogConfigurationTypeDef(TypedDict):
    BlogFieldMappings: NotRequired[Sequence[ConfluenceBlogToIndexFieldMappingTypeDef]]


class SharePointConfigurationOutputTypeDef(TypedDict):
    SharePointVersion: SharePointVersionType
    Urls: List[str]
    SecretArn: str
    CrawlAttachments: NotRequired[bool]
    UseChangeLog: NotRequired[bool]
    InclusionPatterns: NotRequired[List[str]]
    ExclusionPatterns: NotRequired[List[str]]
    VpcConfiguration: NotRequired[DataSourceVpcConfigurationOutputTypeDef]
    FieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    DocumentTitleFieldName: NotRequired[str]
    DisableLocalGroups: NotRequired[bool]
    SslCertificateS3Path: NotRequired[S3PathTypeDef]
    AuthenticationType: NotRequired[SharePointOnlineAuthenticationTypeType]
    ProxyConfiguration: NotRequired[ProxyConfigurationTypeDef]


class ConfluencePageConfigurationOutputTypeDef(TypedDict):
    PageFieldMappings: NotRequired[List[ConfluencePageToIndexFieldMappingTypeDef]]


class ConfluencePageConfigurationTypeDef(TypedDict):
    PageFieldMappings: NotRequired[Sequence[ConfluencePageToIndexFieldMappingTypeDef]]


class ConfluenceSpaceConfigurationOutputTypeDef(TypedDict):
    CrawlPersonalSpaces: NotRequired[bool]
    CrawlArchivedSpaces: NotRequired[bool]
    IncludeSpaces: NotRequired[List[str]]
    ExcludeSpaces: NotRequired[List[str]]
    SpaceFieldMappings: NotRequired[List[ConfluenceSpaceToIndexFieldMappingTypeDef]]


class ConfluenceSpaceConfigurationTypeDef(TypedDict):
    CrawlPersonalSpaces: NotRequired[bool]
    CrawlArchivedSpaces: NotRequired[bool]
    IncludeSpaces: NotRequired[Sequence[str]]
    ExcludeSpaces: NotRequired[Sequence[str]]
    SpaceFieldMappings: NotRequired[Sequence[ConfluenceSpaceToIndexFieldMappingTypeDef]]


ContentSourceConfigurationUnionTypeDef = Union[
    ContentSourceConfigurationTypeDef, ContentSourceConfigurationOutputTypeDef
]


class SpellCorrectedQueryTypeDef(TypedDict):
    SuggestedQueryText: NotRequired[str]
    Corrections: NotRequired[List[CorrectionTypeDef]]


class HierarchicalPrincipalOutputTypeDef(TypedDict):
    PrincipalList: List[PrincipalTypeDef]


class HierarchicalPrincipalTypeDef(TypedDict):
    PrincipalList: Sequence[PrincipalTypeDef]


DataSourceVpcConfigurationUnionTypeDef = Union[
    DataSourceVpcConfigurationTypeDef, DataSourceVpcConfigurationOutputTypeDef
]


class CreateFaqRequestRequestTypeDef(TypedDict):
    IndexId: str
    Name: str
    S3Path: S3PathTypeDef
    RoleArn: str
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    FileFormat: NotRequired[FaqFileFormatType]
    ClientToken: NotRequired[str]
    LanguageCode: NotRequired[str]


class CreateQuerySuggestionsBlockListRequestRequestTypeDef(TypedDict):
    IndexId: str
    Name: str
    SourceS3Path: S3PathTypeDef
    RoleArn: str
    Description: NotRequired[str]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateThesaurusRequestRequestTypeDef(TypedDict):
    IndexId: str
    Name: str
    RoleArn: str
    SourceS3Path: S3PathTypeDef
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]


class CreateFeaturedResultsSetRequestRequestTypeDef(TypedDict):
    IndexId: str
    FeaturedResultsSetName: str
    Description: NotRequired[str]
    ClientToken: NotRequired[str]
    Status: NotRequired[FeaturedResultsSetStatusType]
    QueryTexts: NotRequired[Sequence[str]]
    FeaturedDocuments: NotRequired[Sequence[FeaturedDocumentTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class FeaturedResultsSetTypeDef(TypedDict):
    FeaturedResultsSetId: NotRequired[str]
    FeaturedResultsSetName: NotRequired[str]
    Description: NotRequired[str]
    Status: NotRequired[FeaturedResultsSetStatusType]
    QueryTexts: NotRequired[List[str]]
    FeaturedDocuments: NotRequired[List[FeaturedDocumentTypeDef]]
    LastUpdatedTimestamp: NotRequired[int]
    CreationTimestamp: NotRequired[int]


class UpdateFeaturedResultsSetRequestRequestTypeDef(TypedDict):
    IndexId: str
    FeaturedResultsSetId: str
    FeaturedResultsSetName: NotRequired[str]
    Description: NotRequired[str]
    Status: NotRequired[FeaturedResultsSetStatusType]
    QueryTexts: NotRequired[Sequence[str]]
    FeaturedDocuments: NotRequired[Sequence[FeaturedDocumentTypeDef]]


class UserContextTypeDef(TypedDict):
    Token: NotRequired[str]
    UserId: NotRequired[str]
    Groups: NotRequired[Sequence[str]]
    DataSourceGroups: NotRequired[Sequence[DataSourceGroupTypeDef]]


class ListDataSourcesResponseTypeDef(TypedDict):
    SummaryItems: List[DataSourceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DataSourceSyncJobTypeDef(TypedDict):
    ExecutionId: NotRequired[str]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    Status: NotRequired[DataSourceSyncJobStatusType]
    ErrorMessage: NotRequired[str]
    ErrorCode: NotRequired[ErrorCodeType]
    DataSourceErrorCode: NotRequired[str]
    Metrics: NotRequired[DataSourceSyncJobMetricsTypeDef]


class ExperiencesSummaryTypeDef(TypedDict):
    Name: NotRequired[str]
    Id: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    Status: NotRequired[ExperienceStatusType]
    Endpoints: NotRequired[List[ExperienceEndpointTypeDef]]


class DescribeFeaturedResultsSetResponseTypeDef(TypedDict):
    FeaturedResultsSetId: str
    FeaturedResultsSetName: str
    Description: str
    Status: FeaturedResultsSetStatusType
    QueryTexts: List[str]
    FeaturedDocumentsWithMetadata: List[FeaturedDocumentWithMetadataTypeDef]
    FeaturedDocumentsMissing: List[FeaturedDocumentMissingTypeDef]
    LastUpdatedTimestamp: int
    CreationTimestamp: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePrincipalMappingResponseTypeDef(TypedDict):
    IndexId: str
    DataSourceId: str
    GroupId: str
    GroupOrderingIdSummaries: List[GroupOrderingIdSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DocumentAttributeConditionOutputTypeDef(TypedDict):
    ConditionDocumentAttributeKey: str
    Operator: ConditionOperatorType
    ConditionOnValue: NotRequired[DocumentAttributeValueOutputTypeDef]


class DocumentAttributeOutputTypeDef(TypedDict):
    Key: str
    Value: DocumentAttributeValueOutputTypeDef


class DocumentAttributeTargetOutputTypeDef(TypedDict):
    TargetDocumentAttributeKey: NotRequired[str]
    TargetDocumentAttributeValueDeletion: NotRequired[bool]
    TargetDocumentAttributeValue: NotRequired[DocumentAttributeValueOutputTypeDef]


class DocumentAttributeValueCountPairTypeDef(TypedDict):
    DocumentAttributeValue: NotRequired[DocumentAttributeValueOutputTypeDef]
    Count: NotRequired[int]
    FacetResults: NotRequired[List[Dict[str, Any]]]


DocumentMetadataConfigurationOutputTypeDef = TypedDict(
    "DocumentMetadataConfigurationOutputTypeDef",
    {
        "Name": str,
        "Type": DocumentAttributeValueTypeType,
        "Relevance": NotRequired[RelevanceOutputTypeDef],
        "Search": NotRequired[SearchTypeDef],
    },
)


class S3DataSourceConfigurationOutputTypeDef(TypedDict):
    BucketName: str
    InclusionPrefixes: NotRequired[List[str]]
    InclusionPatterns: NotRequired[List[str]]
    ExclusionPatterns: NotRequired[List[str]]
    DocumentsMetadataConfiguration: NotRequired[DocumentsMetadataConfigurationTypeDef]
    AccessControlListConfiguration: NotRequired[AccessControlListConfigurationTypeDef]


class S3DataSourceConfigurationTypeDef(TypedDict):
    BucketName: str
    InclusionPrefixes: NotRequired[Sequence[str]]
    InclusionPatterns: NotRequired[Sequence[str]]
    ExclusionPatterns: NotRequired[Sequence[str]]
    DocumentsMetadataConfiguration: NotRequired[DocumentsMetadataConfigurationTypeDef]
    AccessControlListConfiguration: NotRequired[AccessControlListConfigurationTypeDef]


class ExperienceEntitiesSummaryTypeDef(TypedDict):
    EntityId: NotRequired[str]
    EntityType: NotRequired[EntityTypeType]
    DisplayData: NotRequired[EntityDisplayDataTypeDef]


class ExperienceConfigurationOutputTypeDef(TypedDict):
    ContentSourceConfiguration: NotRequired[ContentSourceConfigurationOutputTypeDef]
    UserIdentityConfiguration: NotRequired[UserIdentityConfigurationTypeDef]


class ListFaqsResponseTypeDef(TypedDict):
    FaqSummaryItems: List[FaqSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListFeaturedResultsSetsResponseTypeDef(TypedDict):
    FeaturedResultsSetSummaryItems: List[FeaturedResultsSetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetSnapshotsResponseTypeDef(TypedDict):
    SnapShotTimeFilter: TimeRangeOutputTypeDef
    SnapshotsDataHeader: List[str]
    SnapshotsData: List[List[str]]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GroupMembersTypeDef(TypedDict):
    MemberGroups: NotRequired[Sequence[MemberGroupTypeDef]]
    MemberUsers: NotRequired[Sequence[MemberUserTypeDef]]
    S3PathforGroupMembers: NotRequired[S3PathTypeDef]


class ListGroupsOlderThanOrderingIdResponseTypeDef(TypedDict):
    GroupsSummaries: List[GroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


TextWithHighlightsTypeDef = TypedDict(
    "TextWithHighlightsTypeDef",
    {
        "Text": NotRequired[str],
        "Highlights": NotRequired[List[HighlightTypeDef]],
    },
)


class ListIndicesResponseTypeDef(TypedDict):
    IndexConfigurationSummaryItems: List[IndexConfigurationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class IndexStatisticsTypeDef(TypedDict):
    FaqStatistics: FaqStatisticsTypeDef
    TextDocumentStatistics: TextDocumentStatisticsTypeDef


class UserTokenConfigurationTypeDef(TypedDict):
    JwtTokenTypeConfiguration: NotRequired[JwtTokenTypeConfigurationTypeDef]
    JsonTokenTypeConfiguration: NotRequired[JsonTokenTypeConfigurationTypeDef]


class ListEntityPersonasResponseTypeDef(TypedDict):
    SummaryItems: List[PersonasSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListQuerySuggestionsBlockListsResponseTypeDef(TypedDict):
    BlockListSummaryItems: List[QuerySuggestionsBlockListSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListThesauriResponseTypeDef(TypedDict):
    ThesaurusSummaryItems: List[ThesaurusSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


RelevanceUnionTypeDef = Union[RelevanceTypeDef, RelevanceOutputTypeDef]
SeedUrlConfigurationUnionTypeDef = Union[
    SeedUrlConfigurationTypeDef, SeedUrlConfigurationOutputTypeDef
]


class UrlsOutputTypeDef(TypedDict):
    SeedUrlConfiguration: NotRequired[SeedUrlConfigurationOutputTypeDef]
    SiteMapsConfiguration: NotRequired[SiteMapsConfigurationOutputTypeDef]


SiteMapsConfigurationUnionTypeDef = Union[
    SiteMapsConfigurationTypeDef, SiteMapsConfigurationOutputTypeDef
]
SuggestionTextWithHighlightsTypeDef = TypedDict(
    "SuggestionTextWithHighlightsTypeDef",
    {
        "Text": NotRequired[str],
        "Highlights": NotRequired[List[SuggestionHighlightTypeDef]],
    },
)


class TableRowTypeDef(TypedDict):
    Cells: NotRequired[List[TableCellTypeDef]]


TemplateConfigurationUnionTypeDef = Union[
    TemplateConfigurationTypeDef, TemplateConfigurationOutputTypeDef
]


class DatabaseConfigurationOutputTypeDef(TypedDict):
    DatabaseEngineType: DatabaseEngineTypeType
    ConnectionConfiguration: ConnectionConfigurationTypeDef
    ColumnConfiguration: ColumnConfigurationOutputTypeDef
    VpcConfiguration: NotRequired[DataSourceVpcConfigurationOutputTypeDef]
    AclConfiguration: NotRequired[AclConfigurationTypeDef]
    SqlConfiguration: NotRequired[SqlConfigurationTypeDef]


ColumnConfigurationUnionTypeDef = Union[
    ColumnConfigurationTypeDef, ColumnConfigurationOutputTypeDef
]
GoogleDriveConfigurationUnionTypeDef = Union[
    GoogleDriveConfigurationTypeDef, GoogleDriveConfigurationOutputTypeDef
]
SalesforceChatterFeedConfigurationUnionTypeDef = Union[
    SalesforceChatterFeedConfigurationTypeDef, SalesforceChatterFeedConfigurationOutputTypeDef
]
SalesforceCustomKnowledgeArticleTypeConfigurationUnionTypeDef = Union[
    SalesforceCustomKnowledgeArticleTypeConfigurationTypeDef,
    SalesforceCustomKnowledgeArticleTypeConfigurationOutputTypeDef,
]


class SalesforceKnowledgeArticleConfigurationOutputTypeDef(TypedDict):
    IncludedStates: List[SalesforceKnowledgeArticleStateType]
    StandardKnowledgeArticleTypeConfiguration: NotRequired[
        SalesforceStandardKnowledgeArticleTypeConfigurationOutputTypeDef
    ]
    CustomKnowledgeArticleTypeConfigurations: NotRequired[
        List[SalesforceCustomKnowledgeArticleTypeConfigurationOutputTypeDef]
    ]


SalesforceStandardKnowledgeArticleTypeConfigurationUnionTypeDef = Union[
    SalesforceStandardKnowledgeArticleTypeConfigurationTypeDef,
    SalesforceStandardKnowledgeArticleTypeConfigurationOutputTypeDef,
]
SalesforceStandardObjectAttachmentConfigurationUnionTypeDef = Union[
    SalesforceStandardObjectAttachmentConfigurationTypeDef,
    SalesforceStandardObjectAttachmentConfigurationOutputTypeDef,
]
SalesforceStandardObjectConfigurationUnionTypeDef = Union[
    SalesforceStandardObjectConfigurationTypeDef, SalesforceStandardObjectConfigurationOutputTypeDef
]
ServiceNowKnowledgeArticleConfigurationUnionTypeDef = Union[
    ServiceNowKnowledgeArticleConfigurationTypeDef,
    ServiceNowKnowledgeArticleConfigurationOutputTypeDef,
]


class ServiceNowConfigurationOutputTypeDef(TypedDict):
    HostUrl: str
    SecretArn: str
    ServiceNowBuildVersion: ServiceNowBuildVersionTypeType
    KnowledgeArticleConfiguration: NotRequired[ServiceNowKnowledgeArticleConfigurationOutputTypeDef]
    ServiceCatalogConfiguration: NotRequired[ServiceNowServiceCatalogConfigurationOutputTypeDef]
    AuthenticationType: NotRequired[ServiceNowAuthenticationTypeType]


ServiceNowServiceCatalogConfigurationUnionTypeDef = Union[
    ServiceNowServiceCatalogConfigurationTypeDef, ServiceNowServiceCatalogConfigurationOutputTypeDef
]
WorkDocsConfigurationUnionTypeDef = Union[
    WorkDocsConfigurationTypeDef, WorkDocsConfigurationOutputTypeDef
]
GitHubConfigurationOutputTypeDef = TypedDict(
    "GitHubConfigurationOutputTypeDef",
    {
        "SecretArn": str,
        "SaaSConfiguration": NotRequired[SaaSConfigurationTypeDef],
        "OnPremiseConfiguration": NotRequired[OnPremiseConfigurationTypeDef],
        "Type": NotRequired[TypeType],
        "UseChangeLog": NotRequired[bool],
        "GitHubDocumentCrawlProperties": NotRequired[GitHubDocumentCrawlPropertiesTypeDef],
        "RepositoryFilter": NotRequired[List[str]],
        "InclusionFolderNamePatterns": NotRequired[List[str]],
        "InclusionFileTypePatterns": NotRequired[List[str]],
        "InclusionFileNamePatterns": NotRequired[List[str]],
        "ExclusionFolderNamePatterns": NotRequired[List[str]],
        "ExclusionFileTypePatterns": NotRequired[List[str]],
        "ExclusionFileNamePatterns": NotRequired[List[str]],
        "VpcConfiguration": NotRequired[DataSourceVpcConfigurationOutputTypeDef],
        "GitHubRepositoryConfigurationFieldMappings": NotRequired[
            List[DataSourceToIndexFieldMappingTypeDef]
        ],
        "GitHubCommitConfigurationFieldMappings": NotRequired[
            List[DataSourceToIndexFieldMappingTypeDef]
        ],
        "GitHubIssueDocumentConfigurationFieldMappings": NotRequired[
            List[DataSourceToIndexFieldMappingTypeDef]
        ],
        "GitHubIssueCommentConfigurationFieldMappings": NotRequired[
            List[DataSourceToIndexFieldMappingTypeDef]
        ],
        "GitHubIssueAttachmentConfigurationFieldMappings": NotRequired[
            List[DataSourceToIndexFieldMappingTypeDef]
        ],
        "GitHubPullRequestCommentConfigurationFieldMappings": NotRequired[
            List[DataSourceToIndexFieldMappingTypeDef]
        ],
        "GitHubPullRequestDocumentConfigurationFieldMappings": NotRequired[
            List[DataSourceToIndexFieldMappingTypeDef]
        ],
        "GitHubPullRequestDocumentAttachmentConfigurationFieldMappings": NotRequired[
            List[DataSourceToIndexFieldMappingTypeDef]
        ],
    },
)


class OneDriveConfigurationOutputTypeDef(TypedDict):
    TenantDomain: str
    SecretArn: str
    OneDriveUsers: OneDriveUsersOutputTypeDef
    InclusionPatterns: NotRequired[List[str]]
    ExclusionPatterns: NotRequired[List[str]]
    FieldMappings: NotRequired[List[DataSourceToIndexFieldMappingTypeDef]]
    DisableLocalGroups: NotRequired[bool]


OneDriveUsersUnionTypeDef = Union[OneDriveUsersTypeDef, OneDriveUsersOutputTypeDef]


class DescribeQuerySuggestionsConfigResponseTypeDef(TypedDict):
    Mode: ModeType
    Status: QuerySuggestionsStatusType
    QueryLogLookBackWindowInDays: int
    IncludeQueriesWithoutUserInformation: bool
    MinimumNumberOfQueryingUsers: int
    MinimumQueryCount: int
    LastSuggestionsBuildTime: datetime
    LastClearTime: datetime
    TotalSuggestionsCount: int
    AttributeSuggestionsConfig: AttributeSuggestionsDescribeConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateQuerySuggestionsConfigRequestRequestTypeDef(TypedDict):
    IndexId: str
    Mode: NotRequired[ModeType]
    QueryLogLookBackWindowInDays: NotRequired[int]
    IncludeQueriesWithoutUserInformation: NotRequired[bool]
    MinimumNumberOfQueryingUsers: NotRequired[int]
    MinimumQueryCount: NotRequired[int]
    AttributeSuggestionsConfig: NotRequired[AttributeSuggestionsUpdateConfigTypeDef]


AuthenticationConfigurationUnionTypeDef = Union[
    AuthenticationConfigurationTypeDef, AuthenticationConfigurationOutputTypeDef
]


class SubmitFeedbackRequestRequestTypeDef(TypedDict):
    IndexId: str
    QueryId: str
    ClickFeedbackItems: NotRequired[Sequence[ClickFeedbackTypeDef]]
    RelevanceFeedbackItems: NotRequired[Sequence[RelevanceFeedbackTypeDef]]


DocumentAttributeValueUnionTypeDef = Union[
    DocumentAttributeValueTypeDef, DocumentAttributeValueOutputTypeDef
]


class ListDataSourceSyncJobsRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    StartTimeFilter: NotRequired[TimeRangeTypeDef]
    StatusFilter: NotRequired[DataSourceSyncJobStatusType]


ConfluenceAttachmentConfigurationUnionTypeDef = Union[
    ConfluenceAttachmentConfigurationTypeDef, ConfluenceAttachmentConfigurationOutputTypeDef
]
ConfluenceBlogConfigurationUnionTypeDef = Union[
    ConfluenceBlogConfigurationTypeDef, ConfluenceBlogConfigurationOutputTypeDef
]
ConfluencePageConfigurationUnionTypeDef = Union[
    ConfluencePageConfigurationTypeDef, ConfluencePageConfigurationOutputTypeDef
]


class ConfluenceConfigurationOutputTypeDef(TypedDict):
    ServerUrl: str
    SecretArn: str
    Version: ConfluenceVersionType
    SpaceConfiguration: NotRequired[ConfluenceSpaceConfigurationOutputTypeDef]
    PageConfiguration: NotRequired[ConfluencePageConfigurationOutputTypeDef]
    BlogConfiguration: NotRequired[ConfluenceBlogConfigurationOutputTypeDef]
    AttachmentConfiguration: NotRequired[ConfluenceAttachmentConfigurationOutputTypeDef]
    VpcConfiguration: NotRequired[DataSourceVpcConfigurationOutputTypeDef]
    InclusionPatterns: NotRequired[List[str]]
    ExclusionPatterns: NotRequired[List[str]]
    ProxyConfiguration: NotRequired[ProxyConfigurationTypeDef]
    AuthenticationType: NotRequired[ConfluenceAuthenticationTypeType]


ConfluenceSpaceConfigurationUnionTypeDef = Union[
    ConfluenceSpaceConfigurationTypeDef, ConfluenceSpaceConfigurationOutputTypeDef
]


class ExperienceConfigurationTypeDef(TypedDict):
    ContentSourceConfiguration: NotRequired[ContentSourceConfigurationUnionTypeDef]
    UserIdentityConfiguration: NotRequired[UserIdentityConfigurationTypeDef]


class DescribeAccessControlConfigurationResponseTypeDef(TypedDict):
    Name: str
    Description: str
    ErrorMessage: str
    AccessControlList: List[PrincipalTypeDef]
    HierarchicalAccessControlList: List[HierarchicalPrincipalOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


HierarchicalPrincipalUnionTypeDef = Union[
    HierarchicalPrincipalTypeDef, HierarchicalPrincipalOutputTypeDef
]


class UpdateAccessControlConfigurationRequestRequestTypeDef(TypedDict):
    IndexId: str
    Id: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    AccessControlList: NotRequired[Sequence[PrincipalTypeDef]]
    HierarchicalAccessControlList: NotRequired[Sequence[HierarchicalPrincipalTypeDef]]


class AlfrescoConfigurationTypeDef(TypedDict):
    SiteUrl: str
    SiteId: str
    SecretArn: str
    SslCertificateS3Path: S3PathTypeDef
    CrawlSystemFolders: NotRequired[bool]
    CrawlComments: NotRequired[bool]
    EntityFilter: NotRequired[Sequence[AlfrescoEntityType]]
    DocumentLibraryFieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    BlogFieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    WikiFieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    InclusionPatterns: NotRequired[Sequence[str]]
    ExclusionPatterns: NotRequired[Sequence[str]]
    VpcConfiguration: NotRequired[DataSourceVpcConfigurationUnionTypeDef]


class BoxConfigurationTypeDef(TypedDict):
    EnterpriseId: str
    SecretArn: str
    UseChangeLog: NotRequired[bool]
    CrawlComments: NotRequired[bool]
    CrawlTasks: NotRequired[bool]
    CrawlWebLinks: NotRequired[bool]
    FileFieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    TaskFieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    CommentFieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    WebLinkFieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    InclusionPatterns: NotRequired[Sequence[str]]
    ExclusionPatterns: NotRequired[Sequence[str]]
    VpcConfiguration: NotRequired[DataSourceVpcConfigurationUnionTypeDef]


class FsxConfigurationTypeDef(TypedDict):
    FileSystemId: str
    FileSystemType: Literal["WINDOWS"]
    VpcConfiguration: DataSourceVpcConfigurationUnionTypeDef
    SecretArn: NotRequired[str]
    InclusionPatterns: NotRequired[Sequence[str]]
    ExclusionPatterns: NotRequired[Sequence[str]]
    FieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]


GitHubConfigurationTypeDef = TypedDict(
    "GitHubConfigurationTypeDef",
    {
        "SecretArn": str,
        "SaaSConfiguration": NotRequired[SaaSConfigurationTypeDef],
        "OnPremiseConfiguration": NotRequired[OnPremiseConfigurationTypeDef],
        "Type": NotRequired[TypeType],
        "UseChangeLog": NotRequired[bool],
        "GitHubDocumentCrawlProperties": NotRequired[GitHubDocumentCrawlPropertiesTypeDef],
        "RepositoryFilter": NotRequired[Sequence[str]],
        "InclusionFolderNamePatterns": NotRequired[Sequence[str]],
        "InclusionFileTypePatterns": NotRequired[Sequence[str]],
        "InclusionFileNamePatterns": NotRequired[Sequence[str]],
        "ExclusionFolderNamePatterns": NotRequired[Sequence[str]],
        "ExclusionFileTypePatterns": NotRequired[Sequence[str]],
        "ExclusionFileNamePatterns": NotRequired[Sequence[str]],
        "VpcConfiguration": NotRequired[DataSourceVpcConfigurationUnionTypeDef],
        "GitHubRepositoryConfigurationFieldMappings": NotRequired[
            Sequence[DataSourceToIndexFieldMappingTypeDef]
        ],
        "GitHubCommitConfigurationFieldMappings": NotRequired[
            Sequence[DataSourceToIndexFieldMappingTypeDef]
        ],
        "GitHubIssueDocumentConfigurationFieldMappings": NotRequired[
            Sequence[DataSourceToIndexFieldMappingTypeDef]
        ],
        "GitHubIssueCommentConfigurationFieldMappings": NotRequired[
            Sequence[DataSourceToIndexFieldMappingTypeDef]
        ],
        "GitHubIssueAttachmentConfigurationFieldMappings": NotRequired[
            Sequence[DataSourceToIndexFieldMappingTypeDef]
        ],
        "GitHubPullRequestCommentConfigurationFieldMappings": NotRequired[
            Sequence[DataSourceToIndexFieldMappingTypeDef]
        ],
        "GitHubPullRequestDocumentConfigurationFieldMappings": NotRequired[
            Sequence[DataSourceToIndexFieldMappingTypeDef]
        ],
        "GitHubPullRequestDocumentAttachmentConfigurationFieldMappings": NotRequired[
            Sequence[DataSourceToIndexFieldMappingTypeDef]
        ],
    },
)


class JiraConfigurationTypeDef(TypedDict):
    JiraAccountUrl: str
    SecretArn: str
    UseChangeLog: NotRequired[bool]
    Project: NotRequired[Sequence[str]]
    IssueType: NotRequired[Sequence[str]]
    Status: NotRequired[Sequence[str]]
    IssueSubEntityFilter: NotRequired[Sequence[IssueSubEntityType]]
    AttachmentFieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    CommentFieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    IssueFieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    ProjectFieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    WorkLogFieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    InclusionPatterns: NotRequired[Sequence[str]]
    ExclusionPatterns: NotRequired[Sequence[str]]
    VpcConfiguration: NotRequired[DataSourceVpcConfigurationUnionTypeDef]


class QuipConfigurationTypeDef(TypedDict):
    Domain: str
    SecretArn: str
    CrawlFileComments: NotRequired[bool]
    CrawlChatRooms: NotRequired[bool]
    CrawlAttachments: NotRequired[bool]
    FolderIds: NotRequired[Sequence[str]]
    ThreadFieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    MessageFieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    AttachmentFieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    InclusionPatterns: NotRequired[Sequence[str]]
    ExclusionPatterns: NotRequired[Sequence[str]]
    VpcConfiguration: NotRequired[DataSourceVpcConfigurationUnionTypeDef]


class SharePointConfigurationTypeDef(TypedDict):
    SharePointVersion: SharePointVersionType
    Urls: Sequence[str]
    SecretArn: str
    CrawlAttachments: NotRequired[bool]
    UseChangeLog: NotRequired[bool]
    InclusionPatterns: NotRequired[Sequence[str]]
    ExclusionPatterns: NotRequired[Sequence[str]]
    VpcConfiguration: NotRequired[DataSourceVpcConfigurationUnionTypeDef]
    FieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    DocumentTitleFieldName: NotRequired[str]
    DisableLocalGroups: NotRequired[bool]
    SslCertificateS3Path: NotRequired[S3PathTypeDef]
    AuthenticationType: NotRequired[SharePointOnlineAuthenticationTypeType]
    ProxyConfiguration: NotRequired[ProxyConfigurationTypeDef]


class SlackConfigurationTypeDef(TypedDict):
    TeamId: str
    SecretArn: str
    SlackEntityList: Sequence[SlackEntityType]
    SinceCrawlDate: str
    VpcConfiguration: NotRequired[DataSourceVpcConfigurationUnionTypeDef]
    UseChangeLog: NotRequired[bool]
    CrawlBotMessage: NotRequired[bool]
    ExcludeArchived: NotRequired[bool]
    LookBackPeriod: NotRequired[int]
    PrivateChannelFilter: NotRequired[Sequence[str]]
    PublicChannelFilter: NotRequired[Sequence[str]]
    InclusionPatterns: NotRequired[Sequence[str]]
    ExclusionPatterns: NotRequired[Sequence[str]]
    FieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]


class CreateFeaturedResultsSetResponseTypeDef(TypedDict):
    FeaturedResultsSet: FeaturedResultsSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFeaturedResultsSetResponseTypeDef(TypedDict):
    FeaturedResultsSet: FeaturedResultsSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDataSourceSyncJobsResponseTypeDef(TypedDict):
    History: List[DataSourceSyncJobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListExperiencesResponseTypeDef(TypedDict):
    SummaryItems: List[ExperiencesSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class HookConfigurationOutputTypeDef(TypedDict):
    LambdaArn: str
    S3Bucket: str
    InvocationCondition: NotRequired[DocumentAttributeConditionOutputTypeDef]


class RetrieveResultItemTypeDef(TypedDict):
    Id: NotRequired[str]
    DocumentId: NotRequired[str]
    DocumentTitle: NotRequired[str]
    Content: NotRequired[str]
    DocumentURI: NotRequired[str]
    DocumentAttributes: NotRequired[List[DocumentAttributeOutputTypeDef]]
    ScoreAttributes: NotRequired[ScoreAttributesTypeDef]


class SourceDocumentTypeDef(TypedDict):
    DocumentId: NotRequired[str]
    SuggestionAttributes: NotRequired[List[str]]
    AdditionalAttributes: NotRequired[List[DocumentAttributeOutputTypeDef]]


class InlineCustomDocumentEnrichmentConfigurationOutputTypeDef(TypedDict):
    Condition: NotRequired[DocumentAttributeConditionOutputTypeDef]
    Target: NotRequired[DocumentAttributeTargetOutputTypeDef]
    DocumentContentDeletion: NotRequired[bool]


class FacetResultTypeDef(TypedDict):
    DocumentAttributeKey: NotRequired[str]
    DocumentAttributeValueType: NotRequired[DocumentAttributeValueTypeType]
    DocumentAttributeValueCountPairs: NotRequired[List[DocumentAttributeValueCountPairTypeDef]]


S3DataSourceConfigurationUnionTypeDef = Union[
    S3DataSourceConfigurationTypeDef, S3DataSourceConfigurationOutputTypeDef
]


class ListExperienceEntitiesResponseTypeDef(TypedDict):
    SummaryItems: List[ExperienceEntitiesSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeExperienceResponseTypeDef(TypedDict):
    Id: str
    IndexId: str
    Name: str
    Endpoints: List[ExperienceEndpointTypeDef]
    Configuration: ExperienceConfigurationOutputTypeDef
    CreatedAt: datetime
    UpdatedAt: datetime
    Description: str
    Status: ExperienceStatusType
    RoleArn: str
    ErrorMessage: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutPrincipalMappingRequestRequestTypeDef(TypedDict):
    IndexId: str
    GroupId: str
    GroupMembers: GroupMembersTypeDef
    DataSourceId: NotRequired[str]
    OrderingId: NotRequired[int]
    RoleArn: NotRequired[str]


class AdditionalResultAttributeValueTypeDef(TypedDict):
    TextWithHighlightsValue: NotRequired[TextWithHighlightsTypeDef]


class ExpandedResultItemTypeDef(TypedDict):
    Id: NotRequired[str]
    DocumentId: NotRequired[str]
    DocumentTitle: NotRequired[TextWithHighlightsTypeDef]
    DocumentExcerpt: NotRequired[TextWithHighlightsTypeDef]
    DocumentURI: NotRequired[str]
    DocumentAttributes: NotRequired[List[DocumentAttributeOutputTypeDef]]


class CreateIndexRequestRequestTypeDef(TypedDict):
    Name: str
    RoleArn: str
    Edition: NotRequired[IndexEditionType]
    ServerSideEncryptionConfiguration: NotRequired[ServerSideEncryptionConfigurationTypeDef]
    Description: NotRequired[str]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    UserTokenConfigurations: NotRequired[Sequence[UserTokenConfigurationTypeDef]]
    UserContextPolicy: NotRequired[UserContextPolicyType]
    UserGroupResolutionConfiguration: NotRequired[UserGroupResolutionConfigurationTypeDef]


class DescribeIndexResponseTypeDef(TypedDict):
    Name: str
    Id: str
    Edition: IndexEditionType
    RoleArn: str
    ServerSideEncryptionConfiguration: ServerSideEncryptionConfigurationTypeDef
    Status: IndexStatusType
    Description: str
    CreatedAt: datetime
    UpdatedAt: datetime
    DocumentMetadataConfigurations: List[DocumentMetadataConfigurationOutputTypeDef]
    IndexStatistics: IndexStatisticsTypeDef
    ErrorMessage: str
    CapacityUnits: CapacityUnitsConfigurationTypeDef
    UserTokenConfigurations: List[UserTokenConfigurationTypeDef]
    UserContextPolicy: UserContextPolicyType
    UserGroupResolutionConfiguration: UserGroupResolutionConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


DocumentMetadataConfigurationTypeDef = TypedDict(
    "DocumentMetadataConfigurationTypeDef",
    {
        "Name": str,
        "Type": DocumentAttributeValueTypeType,
        "Relevance": NotRequired[RelevanceUnionTypeDef],
        "Search": NotRequired[SearchTypeDef],
    },
)


class DocumentRelevanceConfigurationTypeDef(TypedDict):
    Name: str
    Relevance: RelevanceUnionTypeDef


class WebCrawlerConfigurationOutputTypeDef(TypedDict):
    Urls: UrlsOutputTypeDef
    CrawlDepth: NotRequired[int]
    MaxLinksPerPage: NotRequired[int]
    MaxContentSizePerPageInMegaBytes: NotRequired[float]
    MaxUrlsPerMinuteCrawlRate: NotRequired[int]
    UrlInclusionPatterns: NotRequired[List[str]]
    UrlExclusionPatterns: NotRequired[List[str]]
    ProxyConfiguration: NotRequired[ProxyConfigurationTypeDef]
    AuthenticationConfiguration: NotRequired[AuthenticationConfigurationOutputTypeDef]


class UrlsTypeDef(TypedDict):
    SeedUrlConfiguration: NotRequired[SeedUrlConfigurationUnionTypeDef]
    SiteMapsConfiguration: NotRequired[SiteMapsConfigurationUnionTypeDef]


SuggestionValueTypeDef = TypedDict(
    "SuggestionValueTypeDef",
    {
        "Text": NotRequired[SuggestionTextWithHighlightsTypeDef],
    },
)


class TableExcerptTypeDef(TypedDict):
    Rows: NotRequired[List[TableRowTypeDef]]
    TotalNumberOfRows: NotRequired[int]


class DatabaseConfigurationTypeDef(TypedDict):
    DatabaseEngineType: DatabaseEngineTypeType
    ConnectionConfiguration: ConnectionConfigurationTypeDef
    ColumnConfiguration: ColumnConfigurationUnionTypeDef
    VpcConfiguration: NotRequired[DataSourceVpcConfigurationUnionTypeDef]
    AclConfiguration: NotRequired[AclConfigurationTypeDef]
    SqlConfiguration: NotRequired[SqlConfigurationTypeDef]


class SalesforceConfigurationOutputTypeDef(TypedDict):
    ServerUrl: str
    SecretArn: str
    StandardObjectConfigurations: NotRequired[
        List[SalesforceStandardObjectConfigurationOutputTypeDef]
    ]
    KnowledgeArticleConfiguration: NotRequired[SalesforceKnowledgeArticleConfigurationOutputTypeDef]
    ChatterFeedConfiguration: NotRequired[SalesforceChatterFeedConfigurationOutputTypeDef]
    CrawlAttachments: NotRequired[bool]
    StandardObjectAttachmentConfiguration: NotRequired[
        SalesforceStandardObjectAttachmentConfigurationOutputTypeDef
    ]
    IncludeAttachmentFilePatterns: NotRequired[List[str]]
    ExcludeAttachmentFilePatterns: NotRequired[List[str]]


class SalesforceKnowledgeArticleConfigurationTypeDef(TypedDict):
    IncludedStates: Sequence[SalesforceKnowledgeArticleStateType]
    StandardKnowledgeArticleTypeConfiguration: NotRequired[
        SalesforceStandardKnowledgeArticleTypeConfigurationUnionTypeDef
    ]
    CustomKnowledgeArticleTypeConfigurations: NotRequired[
        Sequence[SalesforceCustomKnowledgeArticleTypeConfigurationUnionTypeDef]
    ]


class ServiceNowConfigurationTypeDef(TypedDict):
    HostUrl: str
    SecretArn: str
    ServiceNowBuildVersion: ServiceNowBuildVersionTypeType
    KnowledgeArticleConfiguration: NotRequired[ServiceNowKnowledgeArticleConfigurationUnionTypeDef]
    ServiceCatalogConfiguration: NotRequired[ServiceNowServiceCatalogConfigurationUnionTypeDef]
    AuthenticationType: NotRequired[ServiceNowAuthenticationTypeType]


class OneDriveConfigurationTypeDef(TypedDict):
    TenantDomain: str
    SecretArn: str
    OneDriveUsers: OneDriveUsersUnionTypeDef
    InclusionPatterns: NotRequired[Sequence[str]]
    ExclusionPatterns: NotRequired[Sequence[str]]
    FieldMappings: NotRequired[Sequence[DataSourceToIndexFieldMappingTypeDef]]
    DisableLocalGroups: NotRequired[bool]


class DocumentAttributeConditionTypeDef(TypedDict):
    ConditionDocumentAttributeKey: str
    Operator: ConditionOperatorType
    ConditionOnValue: NotRequired[DocumentAttributeValueUnionTypeDef]


class DocumentAttributeTargetTypeDef(TypedDict):
    TargetDocumentAttributeKey: NotRequired[str]
    TargetDocumentAttributeValueDeletion: NotRequired[bool]
    TargetDocumentAttributeValue: NotRequired[DocumentAttributeValueUnionTypeDef]


class DocumentAttributeTypeDef(TypedDict):
    Key: str
    Value: DocumentAttributeValueUnionTypeDef


class ConfluenceConfigurationTypeDef(TypedDict):
    ServerUrl: str
    SecretArn: str
    Version: ConfluenceVersionType
    SpaceConfiguration: NotRequired[ConfluenceSpaceConfigurationUnionTypeDef]
    PageConfiguration: NotRequired[ConfluencePageConfigurationUnionTypeDef]
    BlogConfiguration: NotRequired[ConfluenceBlogConfigurationUnionTypeDef]
    AttachmentConfiguration: NotRequired[ConfluenceAttachmentConfigurationUnionTypeDef]
    VpcConfiguration: NotRequired[DataSourceVpcConfigurationUnionTypeDef]
    InclusionPatterns: NotRequired[Sequence[str]]
    ExclusionPatterns: NotRequired[Sequence[str]]
    ProxyConfiguration: NotRequired[ProxyConfigurationTypeDef]
    AuthenticationType: NotRequired[ConfluenceAuthenticationTypeType]


class CreateExperienceRequestRequestTypeDef(TypedDict):
    Name: str
    IndexId: str
    RoleArn: NotRequired[str]
    Configuration: NotRequired[ExperienceConfigurationTypeDef]
    Description: NotRequired[str]
    ClientToken: NotRequired[str]


class UpdateExperienceRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str
    Name: NotRequired[str]
    RoleArn: NotRequired[str]
    Configuration: NotRequired[ExperienceConfigurationTypeDef]
    Description: NotRequired[str]


class CreateAccessControlConfigurationRequestRequestTypeDef(TypedDict):
    IndexId: str
    Name: str
    Description: NotRequired[str]
    AccessControlList: NotRequired[Sequence[PrincipalTypeDef]]
    HierarchicalAccessControlList: NotRequired[Sequence[HierarchicalPrincipalUnionTypeDef]]
    ClientToken: NotRequired[str]


AlfrescoConfigurationUnionTypeDef = Union[
    AlfrescoConfigurationTypeDef, AlfrescoConfigurationOutputTypeDef
]
BoxConfigurationUnionTypeDef = Union[BoxConfigurationTypeDef, BoxConfigurationOutputTypeDef]
FsxConfigurationUnionTypeDef = Union[FsxConfigurationTypeDef, FsxConfigurationOutputTypeDef]
GitHubConfigurationUnionTypeDef = Union[
    GitHubConfigurationTypeDef, GitHubConfigurationOutputTypeDef
]
JiraConfigurationUnionTypeDef = Union[JiraConfigurationTypeDef, JiraConfigurationOutputTypeDef]
QuipConfigurationUnionTypeDef = Union[QuipConfigurationTypeDef, QuipConfigurationOutputTypeDef]
SharePointConfigurationUnionTypeDef = Union[
    SharePointConfigurationTypeDef, SharePointConfigurationOutputTypeDef
]
SlackConfigurationUnionTypeDef = Union[SlackConfigurationTypeDef, SlackConfigurationOutputTypeDef]


class RetrieveResultTypeDef(TypedDict):
    QueryId: str
    ResultItems: List[RetrieveResultItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CustomDocumentEnrichmentConfigurationOutputTypeDef(TypedDict):
    InlineConfigurations: NotRequired[
        List[InlineCustomDocumentEnrichmentConfigurationOutputTypeDef]
    ]
    PreExtractionHookConfiguration: NotRequired[HookConfigurationOutputTypeDef]
    PostExtractionHookConfiguration: NotRequired[HookConfigurationOutputTypeDef]
    RoleArn: NotRequired[str]


class AdditionalResultAttributeTypeDef(TypedDict):
    Key: str
    ValueType: Literal["TEXT_WITH_HIGHLIGHTS_VALUE"]
    Value: AdditionalResultAttributeValueTypeDef


class CollapsedResultDetailTypeDef(TypedDict):
    DocumentAttribute: DocumentAttributeOutputTypeDef
    ExpandedResults: NotRequired[List[ExpandedResultItemTypeDef]]


DocumentMetadataConfigurationUnionTypeDef = Union[
    DocumentMetadataConfigurationTypeDef, DocumentMetadataConfigurationOutputTypeDef
]
UrlsUnionTypeDef = Union[UrlsTypeDef, UrlsOutputTypeDef]


class SuggestionTypeDef(TypedDict):
    Id: NotRequired[str]
    Value: NotRequired[SuggestionValueTypeDef]
    SourceDocuments: NotRequired[List[SourceDocumentTypeDef]]


DatabaseConfigurationUnionTypeDef = Union[
    DatabaseConfigurationTypeDef, DatabaseConfigurationOutputTypeDef
]


class DataSourceConfigurationOutputTypeDef(TypedDict):
    S3Configuration: NotRequired[S3DataSourceConfigurationOutputTypeDef]
    SharePointConfiguration: NotRequired[SharePointConfigurationOutputTypeDef]
    DatabaseConfiguration: NotRequired[DatabaseConfigurationOutputTypeDef]
    SalesforceConfiguration: NotRequired[SalesforceConfigurationOutputTypeDef]
    OneDriveConfiguration: NotRequired[OneDriveConfigurationOutputTypeDef]
    ServiceNowConfiguration: NotRequired[ServiceNowConfigurationOutputTypeDef]
    ConfluenceConfiguration: NotRequired[ConfluenceConfigurationOutputTypeDef]
    GoogleDriveConfiguration: NotRequired[GoogleDriveConfigurationOutputTypeDef]
    WebCrawlerConfiguration: NotRequired[WebCrawlerConfigurationOutputTypeDef]
    WorkDocsConfiguration: NotRequired[WorkDocsConfigurationOutputTypeDef]
    FsxConfiguration: NotRequired[FsxConfigurationOutputTypeDef]
    SlackConfiguration: NotRequired[SlackConfigurationOutputTypeDef]
    BoxConfiguration: NotRequired[BoxConfigurationOutputTypeDef]
    QuipConfiguration: NotRequired[QuipConfigurationOutputTypeDef]
    JiraConfiguration: NotRequired[JiraConfigurationOutputTypeDef]
    GitHubConfiguration: NotRequired[GitHubConfigurationOutputTypeDef]
    AlfrescoConfiguration: NotRequired[AlfrescoConfigurationOutputTypeDef]
    TemplateConfiguration: NotRequired[TemplateConfigurationOutputTypeDef]


SalesforceKnowledgeArticleConfigurationUnionTypeDef = Union[
    SalesforceKnowledgeArticleConfigurationTypeDef,
    SalesforceKnowledgeArticleConfigurationOutputTypeDef,
]
ServiceNowConfigurationUnionTypeDef = Union[
    ServiceNowConfigurationTypeDef, ServiceNowConfigurationOutputTypeDef
]
OneDriveConfigurationUnionTypeDef = Union[
    OneDriveConfigurationTypeDef, OneDriveConfigurationOutputTypeDef
]
DocumentAttributeConditionUnionTypeDef = Union[
    DocumentAttributeConditionTypeDef, DocumentAttributeConditionOutputTypeDef
]
DocumentAttributeTargetUnionTypeDef = Union[
    DocumentAttributeTargetTypeDef, DocumentAttributeTargetOutputTypeDef
]
DocumentAttributeUnionTypeDef = Union[DocumentAttributeTypeDef, DocumentAttributeOutputTypeDef]
ConfluenceConfigurationUnionTypeDef = Union[
    ConfluenceConfigurationTypeDef, ConfluenceConfigurationOutputTypeDef
]
FeaturedResultsItemTypeDef = TypedDict(
    "FeaturedResultsItemTypeDef",
    {
        "Id": NotRequired[str],
        "Type": NotRequired[QueryResultTypeType],
        "AdditionalAttributes": NotRequired[List[AdditionalResultAttributeTypeDef]],
        "DocumentId": NotRequired[str],
        "DocumentTitle": NotRequired[TextWithHighlightsTypeDef],
        "DocumentExcerpt": NotRequired[TextWithHighlightsTypeDef],
        "DocumentURI": NotRequired[str],
        "DocumentAttributes": NotRequired[List[DocumentAttributeOutputTypeDef]],
        "FeedbackToken": NotRequired[str],
    },
)
QueryResultItemTypeDef = TypedDict(
    "QueryResultItemTypeDef",
    {
        "Id": NotRequired[str],
        "Type": NotRequired[QueryResultTypeType],
        "Format": NotRequired[QueryResultFormatType],
        "AdditionalAttributes": NotRequired[List[AdditionalResultAttributeTypeDef]],
        "DocumentId": NotRequired[str],
        "DocumentTitle": NotRequired[TextWithHighlightsTypeDef],
        "DocumentExcerpt": NotRequired[TextWithHighlightsTypeDef],
        "DocumentURI": NotRequired[str],
        "DocumentAttributes": NotRequired[List[DocumentAttributeOutputTypeDef]],
        "ScoreAttributes": NotRequired[ScoreAttributesTypeDef],
        "FeedbackToken": NotRequired[str],
        "TableExcerpt": NotRequired[TableExcerptTypeDef],
        "CollapsedResultDetail": NotRequired[CollapsedResultDetailTypeDef],
    },
)


class UpdateIndexRequestRequestTypeDef(TypedDict):
    Id: str
    Name: NotRequired[str]
    RoleArn: NotRequired[str]
    Description: NotRequired[str]
    DocumentMetadataConfigurationUpdates: NotRequired[
        Sequence[DocumentMetadataConfigurationUnionTypeDef]
    ]
    CapacityUnits: NotRequired[CapacityUnitsConfigurationTypeDef]
    UserTokenConfigurations: NotRequired[Sequence[UserTokenConfigurationTypeDef]]
    UserContextPolicy: NotRequired[UserContextPolicyType]
    UserGroupResolutionConfiguration: NotRequired[UserGroupResolutionConfigurationTypeDef]


class WebCrawlerConfigurationTypeDef(TypedDict):
    Urls: UrlsUnionTypeDef
    CrawlDepth: NotRequired[int]
    MaxLinksPerPage: NotRequired[int]
    MaxContentSizePerPageInMegaBytes: NotRequired[float]
    MaxUrlsPerMinuteCrawlRate: NotRequired[int]
    UrlInclusionPatterns: NotRequired[Sequence[str]]
    UrlExclusionPatterns: NotRequired[Sequence[str]]
    ProxyConfiguration: NotRequired[ProxyConfigurationTypeDef]
    AuthenticationConfiguration: NotRequired[AuthenticationConfigurationUnionTypeDef]


class GetQuerySuggestionsResponseTypeDef(TypedDict):
    QuerySuggestionsId: str
    Suggestions: List[SuggestionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


DescribeDataSourceResponseTypeDef = TypedDict(
    "DescribeDataSourceResponseTypeDef",
    {
        "Id": str,
        "IndexId": str,
        "Name": str,
        "Type": DataSourceTypeType,
        "Configuration": DataSourceConfigurationOutputTypeDef,
        "VpcConfiguration": DataSourceVpcConfigurationOutputTypeDef,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "Description": str,
        "Status": DataSourceStatusType,
        "Schedule": str,
        "RoleArn": str,
        "ErrorMessage": str,
        "LanguageCode": str,
        "CustomDocumentEnrichmentConfiguration": CustomDocumentEnrichmentConfigurationOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class SalesforceConfigurationTypeDef(TypedDict):
    ServerUrl: str
    SecretArn: str
    StandardObjectConfigurations: NotRequired[
        Sequence[SalesforceStandardObjectConfigurationUnionTypeDef]
    ]
    KnowledgeArticleConfiguration: NotRequired[SalesforceKnowledgeArticleConfigurationUnionTypeDef]
    ChatterFeedConfiguration: NotRequired[SalesforceChatterFeedConfigurationUnionTypeDef]
    CrawlAttachments: NotRequired[bool]
    StandardObjectAttachmentConfiguration: NotRequired[
        SalesforceStandardObjectAttachmentConfigurationUnionTypeDef
    ]
    IncludeAttachmentFilePatterns: NotRequired[Sequence[str]]
    ExcludeAttachmentFilePatterns: NotRequired[Sequence[str]]


class HookConfigurationTypeDef(TypedDict):
    LambdaArn: str
    S3Bucket: str
    InvocationCondition: NotRequired[DocumentAttributeConditionUnionTypeDef]


class InlineCustomDocumentEnrichmentConfigurationTypeDef(TypedDict):
    Condition: NotRequired[DocumentAttributeConditionUnionTypeDef]
    Target: NotRequired[DocumentAttributeTargetUnionTypeDef]
    DocumentContentDeletion: NotRequired[bool]


class AttributeFilterTypeDef(TypedDict):
    AndAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    OrAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    NotFilter: NotRequired[Mapping[str, Any]]
    EqualsTo: NotRequired[DocumentAttributeUnionTypeDef]
    ContainsAll: NotRequired[DocumentAttributeUnionTypeDef]
    ContainsAny: NotRequired[DocumentAttributeUnionTypeDef]
    GreaterThan: NotRequired[DocumentAttributeUnionTypeDef]
    GreaterThanOrEquals: NotRequired[DocumentAttributeUnionTypeDef]
    LessThan: NotRequired[DocumentAttributeUnionTypeDef]
    LessThanOrEquals: NotRequired[DocumentAttributeUnionTypeDef]


class DocumentInfoTypeDef(TypedDict):
    DocumentId: str
    Attributes: NotRequired[Sequence[DocumentAttributeUnionTypeDef]]


class DocumentTypeDef(TypedDict):
    Id: str
    Title: NotRequired[str]
    Blob: NotRequired[BlobTypeDef]
    S3Path: NotRequired[S3PathTypeDef]
    Attributes: NotRequired[Sequence[DocumentAttributeUnionTypeDef]]
    AccessControlList: NotRequired[Sequence[PrincipalTypeDef]]
    HierarchicalAccessControlList: NotRequired[Sequence[HierarchicalPrincipalUnionTypeDef]]
    ContentType: NotRequired[ContentTypeType]
    AccessControlConfigurationId: NotRequired[str]


class QueryResultTypeDef(TypedDict):
    QueryId: str
    ResultItems: List[QueryResultItemTypeDef]
    FacetResults: List[FacetResultTypeDef]
    TotalNumberOfResults: int
    Warnings: List[WarningTypeDef]
    SpellCorrectedQueries: List[SpellCorrectedQueryTypeDef]
    FeaturedResultsItems: List[FeaturedResultsItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


WebCrawlerConfigurationUnionTypeDef = Union[
    WebCrawlerConfigurationTypeDef, WebCrawlerConfigurationOutputTypeDef
]
SalesforceConfigurationUnionTypeDef = Union[
    SalesforceConfigurationTypeDef, SalesforceConfigurationOutputTypeDef
]
HookConfigurationUnionTypeDef = Union[HookConfigurationTypeDef, HookConfigurationOutputTypeDef]
InlineCustomDocumentEnrichmentConfigurationUnionTypeDef = Union[
    InlineCustomDocumentEnrichmentConfigurationTypeDef,
    InlineCustomDocumentEnrichmentConfigurationOutputTypeDef,
]


class AttributeSuggestionsGetConfigTypeDef(TypedDict):
    SuggestionAttributes: NotRequired[Sequence[str]]
    AdditionalResponseAttributes: NotRequired[Sequence[str]]
    AttributeFilter: NotRequired[AttributeFilterTypeDef]
    UserContext: NotRequired[UserContextTypeDef]


class QueryRequestRequestTypeDef(TypedDict):
    IndexId: str
    QueryText: NotRequired[str]
    AttributeFilter: NotRequired[AttributeFilterTypeDef]
    Facets: NotRequired[Sequence[FacetTypeDef]]
    RequestedDocumentAttributes: NotRequired[Sequence[str]]
    QueryResultTypeFilter: NotRequired[QueryResultTypeType]
    DocumentRelevanceOverrideConfigurations: NotRequired[
        Sequence[DocumentRelevanceConfigurationTypeDef]
    ]
    PageNumber: NotRequired[int]
    PageSize: NotRequired[int]
    SortingConfiguration: NotRequired[SortingConfigurationTypeDef]
    SortingConfigurations: NotRequired[Sequence[SortingConfigurationTypeDef]]
    UserContext: NotRequired[UserContextTypeDef]
    VisitorId: NotRequired[str]
    SpellCorrectionConfiguration: NotRequired[SpellCorrectionConfigurationTypeDef]
    CollapseConfiguration: NotRequired[CollapseConfigurationTypeDef]


class RetrieveRequestRequestTypeDef(TypedDict):
    IndexId: str
    QueryText: str
    AttributeFilter: NotRequired[AttributeFilterTypeDef]
    RequestedDocumentAttributes: NotRequired[Sequence[str]]
    DocumentRelevanceOverrideConfigurations: NotRequired[
        Sequence[DocumentRelevanceConfigurationTypeDef]
    ]
    PageNumber: NotRequired[int]
    PageSize: NotRequired[int]
    UserContext: NotRequired[UserContextTypeDef]


class BatchGetDocumentStatusRequestRequestTypeDef(TypedDict):
    IndexId: str
    DocumentInfoList: Sequence[DocumentInfoTypeDef]


class DataSourceConfigurationTypeDef(TypedDict):
    S3Configuration: NotRequired[S3DataSourceConfigurationUnionTypeDef]
    SharePointConfiguration: NotRequired[SharePointConfigurationUnionTypeDef]
    DatabaseConfiguration: NotRequired[DatabaseConfigurationUnionTypeDef]
    SalesforceConfiguration: NotRequired[SalesforceConfigurationUnionTypeDef]
    OneDriveConfiguration: NotRequired[OneDriveConfigurationUnionTypeDef]
    ServiceNowConfiguration: NotRequired[ServiceNowConfigurationUnionTypeDef]
    ConfluenceConfiguration: NotRequired[ConfluenceConfigurationUnionTypeDef]
    GoogleDriveConfiguration: NotRequired[GoogleDriveConfigurationUnionTypeDef]
    WebCrawlerConfiguration: NotRequired[WebCrawlerConfigurationUnionTypeDef]
    WorkDocsConfiguration: NotRequired[WorkDocsConfigurationUnionTypeDef]
    FsxConfiguration: NotRequired[FsxConfigurationUnionTypeDef]
    SlackConfiguration: NotRequired[SlackConfigurationUnionTypeDef]
    BoxConfiguration: NotRequired[BoxConfigurationUnionTypeDef]
    QuipConfiguration: NotRequired[QuipConfigurationUnionTypeDef]
    JiraConfiguration: NotRequired[JiraConfigurationUnionTypeDef]
    GitHubConfiguration: NotRequired[GitHubConfigurationUnionTypeDef]
    AlfrescoConfiguration: NotRequired[AlfrescoConfigurationUnionTypeDef]
    TemplateConfiguration: NotRequired[TemplateConfigurationUnionTypeDef]


class CustomDocumentEnrichmentConfigurationTypeDef(TypedDict):
    InlineConfigurations: NotRequired[
        Sequence[InlineCustomDocumentEnrichmentConfigurationUnionTypeDef]
    ]
    PreExtractionHookConfiguration: NotRequired[HookConfigurationUnionTypeDef]
    PostExtractionHookConfiguration: NotRequired[HookConfigurationUnionTypeDef]
    RoleArn: NotRequired[str]


class GetQuerySuggestionsRequestRequestTypeDef(TypedDict):
    IndexId: str
    QueryText: str
    MaxSuggestionsCount: NotRequired[int]
    SuggestionTypes: NotRequired[Sequence[SuggestionTypeType]]
    AttributeSuggestionsConfig: NotRequired[AttributeSuggestionsGetConfigTypeDef]


class BatchPutDocumentRequestRequestTypeDef(TypedDict):
    IndexId: str
    Documents: Sequence[DocumentTypeDef]
    RoleArn: NotRequired[str]
    CustomDocumentEnrichmentConfiguration: NotRequired[CustomDocumentEnrichmentConfigurationTypeDef]


CreateDataSourceRequestRequestTypeDef = TypedDict(
    "CreateDataSourceRequestRequestTypeDef",
    {
        "Name": str,
        "IndexId": str,
        "Type": DataSourceTypeType,
        "Configuration": NotRequired[DataSourceConfigurationTypeDef],
        "VpcConfiguration": NotRequired[DataSourceVpcConfigurationTypeDef],
        "Description": NotRequired[str],
        "Schedule": NotRequired[str],
        "RoleArn": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "ClientToken": NotRequired[str],
        "LanguageCode": NotRequired[str],
        "CustomDocumentEnrichmentConfiguration": NotRequired[
            CustomDocumentEnrichmentConfigurationTypeDef
        ],
    },
)


class UpdateDataSourceRequestRequestTypeDef(TypedDict):
    Id: str
    IndexId: str
    Name: NotRequired[str]
    Configuration: NotRequired[DataSourceConfigurationTypeDef]
    VpcConfiguration: NotRequired[DataSourceVpcConfigurationTypeDef]
    Description: NotRequired[str]
    Schedule: NotRequired[str]
    RoleArn: NotRequired[str]
    LanguageCode: NotRequired[str]
    CustomDocumentEnrichmentConfiguration: NotRequired[CustomDocumentEnrichmentConfigurationTypeDef]
