"""
Type annotations for appsync service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/type_defs/)

Usage::

    ```python
    from mypy_boto3_appsync.type_defs import CognitoUserPoolConfigTypeDef

    data: CognitoUserPoolConfigTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ApiCacheStatusType,
    ApiCacheTypeType,
    ApiCachingBehaviorType,
    AssociationStatusType,
    AuthenticationTypeType,
    CacheHealthMetricsConfigType,
    ConflictDetectionTypeType,
    ConflictHandlerTypeType,
    DataSourceIntrospectionStatusType,
    DataSourceLevelMetricsBehaviorType,
    DataSourceLevelMetricsConfigType,
    DataSourceTypeType,
    DefaultActionType,
    EventLogLevelType,
    FieldLogLevelType,
    GraphQLApiIntrospectionConfigType,
    GraphQLApiTypeType,
    GraphQLApiVisibilityType,
    MergeTypeType,
    OperationLevelMetricsConfigType,
    OutputTypeType,
    OwnershipType,
    ResolverKindType,
    ResolverLevelMetricsBehaviorType,
    ResolverLevelMetricsConfigType,
    SchemaStatusType,
    SourceApiAssociationStatusType,
    TypeDefinitionFormatType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AdditionalAuthenticationProviderTypeDef",
    "ApiAssociationTypeDef",
    "ApiCacheTypeDef",
    "ApiKeyTypeDef",
    "ApiTypeDef",
    "AppSyncRuntimeTypeDef",
    "AssociateApiRequestRequestTypeDef",
    "AssociateApiResponseTypeDef",
    "AssociateMergedGraphqlApiRequestRequestTypeDef",
    "AssociateMergedGraphqlApiResponseTypeDef",
    "AssociateSourceGraphqlApiRequestRequestTypeDef",
    "AssociateSourceGraphqlApiResponseTypeDef",
    "AuthModeTypeDef",
    "AuthProviderTypeDef",
    "AuthorizationConfigTypeDef",
    "AwsIamConfigTypeDef",
    "BlobTypeDef",
    "CachingConfigOutputTypeDef",
    "CachingConfigTypeDef",
    "ChannelNamespaceTypeDef",
    "CodeErrorLocationTypeDef",
    "CodeErrorTypeDef",
    "CognitoConfigTypeDef",
    "CognitoUserPoolConfigTypeDef",
    "CreateApiCacheRequestRequestTypeDef",
    "CreateApiCacheResponseTypeDef",
    "CreateApiKeyRequestRequestTypeDef",
    "CreateApiKeyResponseTypeDef",
    "CreateApiRequestRequestTypeDef",
    "CreateApiResponseTypeDef",
    "CreateChannelNamespaceRequestRequestTypeDef",
    "CreateChannelNamespaceResponseTypeDef",
    "CreateDataSourceRequestRequestTypeDef",
    "CreateDataSourceResponseTypeDef",
    "CreateDomainNameRequestRequestTypeDef",
    "CreateDomainNameResponseTypeDef",
    "CreateFunctionRequestRequestTypeDef",
    "CreateFunctionResponseTypeDef",
    "CreateGraphqlApiRequestRequestTypeDef",
    "CreateGraphqlApiResponseTypeDef",
    "CreateResolverRequestRequestTypeDef",
    "CreateResolverResponseTypeDef",
    "CreateTypeRequestRequestTypeDef",
    "CreateTypeResponseTypeDef",
    "DataSourceIntrospectionModelFieldTypeDef",
    "DataSourceIntrospectionModelFieldTypeTypeDef",
    "DataSourceIntrospectionModelIndexTypeDef",
    "DataSourceIntrospectionModelTypeDef",
    "DataSourceIntrospectionResultTypeDef",
    "DataSourceTypeDef",
    "DeleteApiCacheRequestRequestTypeDef",
    "DeleteApiKeyRequestRequestTypeDef",
    "DeleteApiRequestRequestTypeDef",
    "DeleteChannelNamespaceRequestRequestTypeDef",
    "DeleteDataSourceRequestRequestTypeDef",
    "DeleteDomainNameRequestRequestTypeDef",
    "DeleteFunctionRequestRequestTypeDef",
    "DeleteGraphqlApiRequestRequestTypeDef",
    "DeleteResolverRequestRequestTypeDef",
    "DeleteTypeRequestRequestTypeDef",
    "DeltaSyncConfigTypeDef",
    "DisassociateApiRequestRequestTypeDef",
    "DisassociateMergedGraphqlApiRequestRequestTypeDef",
    "DisassociateMergedGraphqlApiResponseTypeDef",
    "DisassociateSourceGraphqlApiRequestRequestTypeDef",
    "DisassociateSourceGraphqlApiResponseTypeDef",
    "DomainNameConfigTypeDef",
    "DynamodbDataSourceConfigTypeDef",
    "ElasticsearchDataSourceConfigTypeDef",
    "EnhancedMetricsConfigTypeDef",
    "ErrorDetailTypeDef",
    "EvaluateCodeErrorDetailTypeDef",
    "EvaluateCodeRequestRequestTypeDef",
    "EvaluateCodeResponseTypeDef",
    "EvaluateMappingTemplateRequestRequestTypeDef",
    "EvaluateMappingTemplateResponseTypeDef",
    "EventBridgeDataSourceConfigTypeDef",
    "EventConfigOutputTypeDef",
    "EventConfigTypeDef",
    "EventLogConfigTypeDef",
    "FlushApiCacheRequestRequestTypeDef",
    "FunctionConfigurationTypeDef",
    "GetApiAssociationRequestRequestTypeDef",
    "GetApiAssociationResponseTypeDef",
    "GetApiCacheRequestRequestTypeDef",
    "GetApiCacheResponseTypeDef",
    "GetApiRequestRequestTypeDef",
    "GetApiResponseTypeDef",
    "GetChannelNamespaceRequestRequestTypeDef",
    "GetChannelNamespaceResponseTypeDef",
    "GetDataSourceIntrospectionRequestRequestTypeDef",
    "GetDataSourceIntrospectionResponseTypeDef",
    "GetDataSourceRequestRequestTypeDef",
    "GetDataSourceResponseTypeDef",
    "GetDomainNameRequestRequestTypeDef",
    "GetDomainNameResponseTypeDef",
    "GetFunctionRequestRequestTypeDef",
    "GetFunctionResponseTypeDef",
    "GetGraphqlApiEnvironmentVariablesRequestRequestTypeDef",
    "GetGraphqlApiEnvironmentVariablesResponseTypeDef",
    "GetGraphqlApiRequestRequestTypeDef",
    "GetGraphqlApiResponseTypeDef",
    "GetIntrospectionSchemaRequestRequestTypeDef",
    "GetIntrospectionSchemaResponseTypeDef",
    "GetResolverRequestRequestTypeDef",
    "GetResolverResponseTypeDef",
    "GetSchemaCreationStatusRequestRequestTypeDef",
    "GetSchemaCreationStatusResponseTypeDef",
    "GetSourceApiAssociationRequestRequestTypeDef",
    "GetSourceApiAssociationResponseTypeDef",
    "GetTypeRequestRequestTypeDef",
    "GetTypeResponseTypeDef",
    "GraphqlApiTypeDef",
    "HttpDataSourceConfigTypeDef",
    "LambdaAuthorizerConfigTypeDef",
    "LambdaConflictHandlerConfigTypeDef",
    "LambdaDataSourceConfigTypeDef",
    "ListApiKeysRequestListApiKeysPaginateTypeDef",
    "ListApiKeysRequestRequestTypeDef",
    "ListApiKeysResponseTypeDef",
    "ListApisRequestListApisPaginateTypeDef",
    "ListApisRequestRequestTypeDef",
    "ListApisResponseTypeDef",
    "ListChannelNamespacesRequestListChannelNamespacesPaginateTypeDef",
    "ListChannelNamespacesRequestRequestTypeDef",
    "ListChannelNamespacesResponseTypeDef",
    "ListDataSourcesRequestListDataSourcesPaginateTypeDef",
    "ListDataSourcesRequestRequestTypeDef",
    "ListDataSourcesResponseTypeDef",
    "ListDomainNamesRequestListDomainNamesPaginateTypeDef",
    "ListDomainNamesRequestRequestTypeDef",
    "ListDomainNamesResponseTypeDef",
    "ListFunctionsRequestListFunctionsPaginateTypeDef",
    "ListFunctionsRequestRequestTypeDef",
    "ListFunctionsResponseTypeDef",
    "ListGraphqlApisRequestListGraphqlApisPaginateTypeDef",
    "ListGraphqlApisRequestRequestTypeDef",
    "ListGraphqlApisResponseTypeDef",
    "ListResolversByFunctionRequestListResolversByFunctionPaginateTypeDef",
    "ListResolversByFunctionRequestRequestTypeDef",
    "ListResolversByFunctionResponseTypeDef",
    "ListResolversRequestListResolversPaginateTypeDef",
    "ListResolversRequestRequestTypeDef",
    "ListResolversResponseTypeDef",
    "ListSourceApiAssociationsRequestListSourceApiAssociationsPaginateTypeDef",
    "ListSourceApiAssociationsRequestRequestTypeDef",
    "ListSourceApiAssociationsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTypesByAssociationRequestListTypesByAssociationPaginateTypeDef",
    "ListTypesByAssociationRequestRequestTypeDef",
    "ListTypesByAssociationResponseTypeDef",
    "ListTypesRequestListTypesPaginateTypeDef",
    "ListTypesRequestRequestTypeDef",
    "ListTypesResponseTypeDef",
    "LogConfigTypeDef",
    "OpenIDConnectConfigTypeDef",
    "OpenSearchServiceDataSourceConfigTypeDef",
    "PaginatorConfigTypeDef",
    "PipelineConfigOutputTypeDef",
    "PipelineConfigTypeDef",
    "PutGraphqlApiEnvironmentVariablesRequestRequestTypeDef",
    "PutGraphqlApiEnvironmentVariablesResponseTypeDef",
    "RdsDataApiConfigTypeDef",
    "RdsHttpEndpointConfigTypeDef",
    "RelationalDatabaseDataSourceConfigTypeDef",
    "ResolverTypeDef",
    "ResponseMetadataTypeDef",
    "SourceApiAssociationConfigTypeDef",
    "SourceApiAssociationSummaryTypeDef",
    "SourceApiAssociationTypeDef",
    "StartDataSourceIntrospectionRequestRequestTypeDef",
    "StartDataSourceIntrospectionResponseTypeDef",
    "StartSchemaCreationRequestRequestTypeDef",
    "StartSchemaCreationResponseTypeDef",
    "StartSchemaMergeRequestRequestTypeDef",
    "StartSchemaMergeResponseTypeDef",
    "SyncConfigTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TypeTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApiCacheRequestRequestTypeDef",
    "UpdateApiCacheResponseTypeDef",
    "UpdateApiKeyRequestRequestTypeDef",
    "UpdateApiKeyResponseTypeDef",
    "UpdateApiRequestRequestTypeDef",
    "UpdateApiResponseTypeDef",
    "UpdateChannelNamespaceRequestRequestTypeDef",
    "UpdateChannelNamespaceResponseTypeDef",
    "UpdateDataSourceRequestRequestTypeDef",
    "UpdateDataSourceResponseTypeDef",
    "UpdateDomainNameRequestRequestTypeDef",
    "UpdateDomainNameResponseTypeDef",
    "UpdateFunctionRequestRequestTypeDef",
    "UpdateFunctionResponseTypeDef",
    "UpdateGraphqlApiRequestRequestTypeDef",
    "UpdateGraphqlApiResponseTypeDef",
    "UpdateResolverRequestRequestTypeDef",
    "UpdateResolverResponseTypeDef",
    "UpdateSourceApiAssociationRequestRequestTypeDef",
    "UpdateSourceApiAssociationResponseTypeDef",
    "UpdateTypeRequestRequestTypeDef",
    "UpdateTypeResponseTypeDef",
    "UserPoolConfigTypeDef",
)


class CognitoUserPoolConfigTypeDef(TypedDict):
    userPoolId: str
    awsRegion: str
    appIdClientRegex: NotRequired[str]


class LambdaAuthorizerConfigTypeDef(TypedDict):
    authorizerUri: str
    authorizerResultTtlInSeconds: NotRequired[int]
    identityValidationExpression: NotRequired[str]


class OpenIDConnectConfigTypeDef(TypedDict):
    issuer: str
    clientId: NotRequired[str]
    iatTTL: NotRequired[int]
    authTTL: NotRequired[int]


class ApiAssociationTypeDef(TypedDict):
    domainName: NotRequired[str]
    apiId: NotRequired[str]
    associationStatus: NotRequired[AssociationStatusType]
    deploymentDetail: NotRequired[str]


ApiCacheTypeDef = TypedDict(
    "ApiCacheTypeDef",
    {
        "ttl": NotRequired[int],
        "apiCachingBehavior": NotRequired[ApiCachingBehaviorType],
        "transitEncryptionEnabled": NotRequired[bool],
        "atRestEncryptionEnabled": NotRequired[bool],
        "type": NotRequired[ApiCacheTypeType],
        "status": NotRequired[ApiCacheStatusType],
        "healthMetricsConfig": NotRequired[CacheHealthMetricsConfigType],
    },
)
ApiKeyTypeDef = TypedDict(
    "ApiKeyTypeDef",
    {
        "id": NotRequired[str],
        "description": NotRequired[str],
        "expires": NotRequired[int],
        "deletes": NotRequired[int],
    },
)


class AppSyncRuntimeTypeDef(TypedDict):
    name: Literal["APPSYNC_JS"]
    runtimeVersion: str


class AssociateApiRequestRequestTypeDef(TypedDict):
    domainName: str
    apiId: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class SourceApiAssociationConfigTypeDef(TypedDict):
    mergeType: NotRequired[MergeTypeType]


class AuthModeTypeDef(TypedDict):
    authType: AuthenticationTypeType


class CognitoConfigTypeDef(TypedDict):
    userPoolId: str
    awsRegion: str
    appIdClientRegex: NotRequired[str]


class AwsIamConfigTypeDef(TypedDict):
    signingRegion: NotRequired[str]
    signingServiceName: NotRequired[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class CachingConfigOutputTypeDef(TypedDict):
    ttl: int
    cachingKeys: NotRequired[List[str]]


class CachingConfigTypeDef(TypedDict):
    ttl: int
    cachingKeys: NotRequired[Sequence[str]]


class CodeErrorLocationTypeDef(TypedDict):
    line: NotRequired[int]
    column: NotRequired[int]
    span: NotRequired[int]


CreateApiCacheRequestRequestTypeDef = TypedDict(
    "CreateApiCacheRequestRequestTypeDef",
    {
        "apiId": str,
        "ttl": int,
        "apiCachingBehavior": ApiCachingBehaviorType,
        "type": ApiCacheTypeType,
        "transitEncryptionEnabled": NotRequired[bool],
        "atRestEncryptionEnabled": NotRequired[bool],
        "healthMetricsConfig": NotRequired[CacheHealthMetricsConfigType],
    },
)


class CreateApiKeyRequestRequestTypeDef(TypedDict):
    apiId: str
    description: NotRequired[str]
    expires: NotRequired[int]


class ElasticsearchDataSourceConfigTypeDef(TypedDict):
    endpoint: str
    awsRegion: str


class EventBridgeDataSourceConfigTypeDef(TypedDict):
    eventBusArn: str


class LambdaDataSourceConfigTypeDef(TypedDict):
    lambdaFunctionArn: str


class OpenSearchServiceDataSourceConfigTypeDef(TypedDict):
    endpoint: str
    awsRegion: str


class CreateDomainNameRequestRequestTypeDef(TypedDict):
    domainName: str
    certificateArn: str
    description: NotRequired[str]


class DomainNameConfigTypeDef(TypedDict):
    domainName: NotRequired[str]
    description: NotRequired[str]
    certificateArn: NotRequired[str]
    appsyncDomainName: NotRequired[str]
    hostedZoneId: NotRequired[str]


class EnhancedMetricsConfigTypeDef(TypedDict):
    resolverLevelMetricsBehavior: ResolverLevelMetricsBehaviorType
    dataSourceLevelMetricsBehavior: DataSourceLevelMetricsBehaviorType
    operationLevelMetricsConfig: OperationLevelMetricsConfigType


class LogConfigTypeDef(TypedDict):
    fieldLogLevel: FieldLogLevelType
    cloudWatchLogsRoleArn: str
    excludeVerboseContent: NotRequired[bool]


class UserPoolConfigTypeDef(TypedDict):
    userPoolId: str
    awsRegion: str
    defaultAction: DefaultActionType
    appIdClientRegex: NotRequired[str]


class PipelineConfigTypeDef(TypedDict):
    functions: NotRequired[Sequence[str]]


CreateTypeRequestRequestTypeDef = TypedDict(
    "CreateTypeRequestRequestTypeDef",
    {
        "apiId": str,
        "definition": str,
        "format": TypeDefinitionFormatType,
    },
)
TypeTypeDef = TypedDict(
    "TypeTypeDef",
    {
        "name": NotRequired[str],
        "description": NotRequired[str],
        "arn": NotRequired[str],
        "definition": NotRequired[str],
        "format": NotRequired[TypeDefinitionFormatType],
    },
)
DataSourceIntrospectionModelFieldTypeTypeDef = TypedDict(
    "DataSourceIntrospectionModelFieldTypeTypeDef",
    {
        "kind": NotRequired[str],
        "name": NotRequired[str],
        "type": NotRequired[Dict[str, Any]],
        "values": NotRequired[List[str]],
    },
)


class DataSourceIntrospectionModelIndexTypeDef(TypedDict):
    name: NotRequired[str]
    fields: NotRequired[List[str]]


class DeleteApiCacheRequestRequestTypeDef(TypedDict):
    apiId: str


DeleteApiKeyRequestRequestTypeDef = TypedDict(
    "DeleteApiKeyRequestRequestTypeDef",
    {
        "apiId": str,
        "id": str,
    },
)


class DeleteApiRequestRequestTypeDef(TypedDict):
    apiId: str


class DeleteChannelNamespaceRequestRequestTypeDef(TypedDict):
    apiId: str
    name: str


class DeleteDataSourceRequestRequestTypeDef(TypedDict):
    apiId: str
    name: str


class DeleteDomainNameRequestRequestTypeDef(TypedDict):
    domainName: str


class DeleteFunctionRequestRequestTypeDef(TypedDict):
    apiId: str
    functionId: str


class DeleteGraphqlApiRequestRequestTypeDef(TypedDict):
    apiId: str


class DeleteResolverRequestRequestTypeDef(TypedDict):
    apiId: str
    typeName: str
    fieldName: str


class DeleteTypeRequestRequestTypeDef(TypedDict):
    apiId: str
    typeName: str


class DeltaSyncConfigTypeDef(TypedDict):
    baseTableTTL: NotRequired[int]
    deltaSyncTableName: NotRequired[str]
    deltaSyncTableTTL: NotRequired[int]


class DisassociateApiRequestRequestTypeDef(TypedDict):
    domainName: str


class DisassociateMergedGraphqlApiRequestRequestTypeDef(TypedDict):
    sourceApiIdentifier: str
    associationId: str


class DisassociateSourceGraphqlApiRequestRequestTypeDef(TypedDict):
    mergedApiIdentifier: str
    associationId: str


class ErrorDetailTypeDef(TypedDict):
    message: NotRequired[str]


class EvaluateMappingTemplateRequestRequestTypeDef(TypedDict):
    template: str
    context: str


class EventLogConfigTypeDef(TypedDict):
    logLevel: EventLogLevelType
    cloudWatchLogsRoleArn: str


class FlushApiCacheRequestRequestTypeDef(TypedDict):
    apiId: str


class GetApiAssociationRequestRequestTypeDef(TypedDict):
    domainName: str


class GetApiCacheRequestRequestTypeDef(TypedDict):
    apiId: str


class GetApiRequestRequestTypeDef(TypedDict):
    apiId: str


class GetChannelNamespaceRequestRequestTypeDef(TypedDict):
    apiId: str
    name: str


class GetDataSourceIntrospectionRequestRequestTypeDef(TypedDict):
    introspectionId: str
    includeModelsSDL: NotRequired[bool]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class GetDataSourceRequestRequestTypeDef(TypedDict):
    apiId: str
    name: str


class GetDomainNameRequestRequestTypeDef(TypedDict):
    domainName: str


class GetFunctionRequestRequestTypeDef(TypedDict):
    apiId: str
    functionId: str


class GetGraphqlApiEnvironmentVariablesRequestRequestTypeDef(TypedDict):
    apiId: str


class GetGraphqlApiRequestRequestTypeDef(TypedDict):
    apiId: str


GetIntrospectionSchemaRequestRequestTypeDef = TypedDict(
    "GetIntrospectionSchemaRequestRequestTypeDef",
    {
        "apiId": str,
        "format": OutputTypeType,
        "includeDirectives": NotRequired[bool],
    },
)


class GetResolverRequestRequestTypeDef(TypedDict):
    apiId: str
    typeName: str
    fieldName: str


class GetSchemaCreationStatusRequestRequestTypeDef(TypedDict):
    apiId: str


class GetSourceApiAssociationRequestRequestTypeDef(TypedDict):
    mergedApiIdentifier: str
    associationId: str


GetTypeRequestRequestTypeDef = TypedDict(
    "GetTypeRequestRequestTypeDef",
    {
        "apiId": str,
        "typeName": str,
        "format": TypeDefinitionFormatType,
    },
)


class LambdaConflictHandlerConfigTypeDef(TypedDict):
    lambdaConflictHandlerArn: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListApiKeysRequestRequestTypeDef(TypedDict):
    apiId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListApisRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListChannelNamespacesRequestRequestTypeDef(TypedDict):
    apiId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDataSourcesRequestRequestTypeDef(TypedDict):
    apiId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDomainNamesRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListFunctionsRequestRequestTypeDef(TypedDict):
    apiId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListGraphqlApisRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    apiType: NotRequired[GraphQLApiTypeType]
    owner: NotRequired[OwnershipType]


class ListResolversByFunctionRequestRequestTypeDef(TypedDict):
    apiId: str
    functionId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListResolversRequestRequestTypeDef(TypedDict):
    apiId: str
    typeName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListSourceApiAssociationsRequestRequestTypeDef(TypedDict):
    apiId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class SourceApiAssociationSummaryTypeDef(TypedDict):
    associationId: NotRequired[str]
    associationArn: NotRequired[str]
    sourceApiId: NotRequired[str]
    sourceApiArn: NotRequired[str]
    mergedApiId: NotRequired[str]
    mergedApiArn: NotRequired[str]
    description: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


ListTypesByAssociationRequestRequestTypeDef = TypedDict(
    "ListTypesByAssociationRequestRequestTypeDef",
    {
        "mergedApiIdentifier": str,
        "associationId": str,
        "format": TypeDefinitionFormatType,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListTypesRequestRequestTypeDef = TypedDict(
    "ListTypesRequestRequestTypeDef",
    {
        "apiId": str,
        "format": TypeDefinitionFormatType,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)


class PipelineConfigOutputTypeDef(TypedDict):
    functions: NotRequired[List[str]]


class PutGraphqlApiEnvironmentVariablesRequestRequestTypeDef(TypedDict):
    apiId: str
    environmentVariables: Mapping[str, str]


class RdsDataApiConfigTypeDef(TypedDict):
    resourceArn: str
    secretArn: str
    databaseName: str


class RdsHttpEndpointConfigTypeDef(TypedDict):
    awsRegion: NotRequired[str]
    dbClusterIdentifier: NotRequired[str]
    databaseName: NotRequired[str]
    schema: NotRequired[str]
    awsSecretStoreArn: NotRequired[str]


class StartSchemaMergeRequestRequestTypeDef(TypedDict):
    associationId: str
    mergedApiIdentifier: str


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


UpdateApiCacheRequestRequestTypeDef = TypedDict(
    "UpdateApiCacheRequestRequestTypeDef",
    {
        "apiId": str,
        "ttl": int,
        "apiCachingBehavior": ApiCachingBehaviorType,
        "type": ApiCacheTypeType,
        "healthMetricsConfig": NotRequired[CacheHealthMetricsConfigType],
    },
)
UpdateApiKeyRequestRequestTypeDef = TypedDict(
    "UpdateApiKeyRequestRequestTypeDef",
    {
        "apiId": str,
        "id": str,
        "description": NotRequired[str],
        "expires": NotRequired[int],
    },
)


class UpdateDomainNameRequestRequestTypeDef(TypedDict):
    domainName: str
    description: NotRequired[str]


UpdateTypeRequestRequestTypeDef = TypedDict(
    "UpdateTypeRequestRequestTypeDef",
    {
        "apiId": str,
        "typeName": str,
        "format": TypeDefinitionFormatType,
        "definition": NotRequired[str],
    },
)


class AdditionalAuthenticationProviderTypeDef(TypedDict):
    authenticationType: NotRequired[AuthenticationTypeType]
    openIDConnectConfig: NotRequired[OpenIDConnectConfigTypeDef]
    userPoolConfig: NotRequired[CognitoUserPoolConfigTypeDef]
    lambdaAuthorizerConfig: NotRequired[LambdaAuthorizerConfigTypeDef]


class EvaluateCodeRequestRequestTypeDef(TypedDict):
    runtime: AppSyncRuntimeTypeDef
    code: str
    context: str
    function: NotRequired[str]


class AssociateApiResponseTypeDef(TypedDict):
    apiAssociation: ApiAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateApiCacheResponseTypeDef(TypedDict):
    apiCache: ApiCacheTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateApiKeyResponseTypeDef(TypedDict):
    apiKey: ApiKeyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateMergedGraphqlApiResponseTypeDef(TypedDict):
    sourceApiAssociationStatus: SourceApiAssociationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateSourceGraphqlApiResponseTypeDef(TypedDict):
    sourceApiAssociationStatus: SourceApiAssociationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetApiAssociationResponseTypeDef(TypedDict):
    apiAssociation: ApiAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetApiCacheResponseTypeDef(TypedDict):
    apiCache: ApiCacheTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetGraphqlApiEnvironmentVariablesResponseTypeDef(TypedDict):
    environmentVariables: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetIntrospectionSchemaResponseTypeDef(TypedDict):
    schema: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef


class GetSchemaCreationStatusResponseTypeDef(TypedDict):
    status: SchemaStatusType
    details: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListApiKeysResponseTypeDef(TypedDict):
    apiKeys: List[ApiKeyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PutGraphqlApiEnvironmentVariablesResponseTypeDef(TypedDict):
    environmentVariables: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class StartDataSourceIntrospectionResponseTypeDef(TypedDict):
    introspectionId: str
    introspectionStatus: DataSourceIntrospectionStatusType
    introspectionStatusDetail: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartSchemaCreationResponseTypeDef(TypedDict):
    status: SchemaStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class StartSchemaMergeResponseTypeDef(TypedDict):
    sourceApiAssociationStatus: SourceApiAssociationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateApiCacheResponseTypeDef(TypedDict):
    apiCache: ApiCacheTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateApiKeyResponseTypeDef(TypedDict):
    apiKey: ApiKeyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateMergedGraphqlApiRequestRequestTypeDef(TypedDict):
    sourceApiIdentifier: str
    mergedApiIdentifier: str
    description: NotRequired[str]
    sourceApiAssociationConfig: NotRequired[SourceApiAssociationConfigTypeDef]


class AssociateSourceGraphqlApiRequestRequestTypeDef(TypedDict):
    mergedApiIdentifier: str
    sourceApiIdentifier: str
    description: NotRequired[str]
    sourceApiAssociationConfig: NotRequired[SourceApiAssociationConfigTypeDef]


class SourceApiAssociationTypeDef(TypedDict):
    associationId: NotRequired[str]
    associationArn: NotRequired[str]
    sourceApiId: NotRequired[str]
    sourceApiArn: NotRequired[str]
    mergedApiArn: NotRequired[str]
    mergedApiId: NotRequired[str]
    description: NotRequired[str]
    sourceApiAssociationConfig: NotRequired[SourceApiAssociationConfigTypeDef]
    sourceApiAssociationStatus: NotRequired[SourceApiAssociationStatusType]
    sourceApiAssociationStatusDetail: NotRequired[str]
    lastSuccessfulMergeDate: NotRequired[datetime]


class UpdateSourceApiAssociationRequestRequestTypeDef(TypedDict):
    associationId: str
    mergedApiIdentifier: str
    description: NotRequired[str]
    sourceApiAssociationConfig: NotRequired[SourceApiAssociationConfigTypeDef]


class ChannelNamespaceTypeDef(TypedDict):
    apiId: NotRequired[str]
    name: NotRequired[str]
    subscribeAuthModes: NotRequired[List[AuthModeTypeDef]]
    publishAuthModes: NotRequired[List[AuthModeTypeDef]]
    codeHandlers: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    channelNamespaceArn: NotRequired[str]
    created: NotRequired[datetime]
    lastModified: NotRequired[datetime]


class CreateChannelNamespaceRequestRequestTypeDef(TypedDict):
    apiId: str
    name: str
    subscribeAuthModes: NotRequired[Sequence[AuthModeTypeDef]]
    publishAuthModes: NotRequired[Sequence[AuthModeTypeDef]]
    codeHandlers: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class UpdateChannelNamespaceRequestRequestTypeDef(TypedDict):
    apiId: str
    name: str
    subscribeAuthModes: NotRequired[Sequence[AuthModeTypeDef]]
    publishAuthModes: NotRequired[Sequence[AuthModeTypeDef]]
    codeHandlers: NotRequired[str]


class AuthProviderTypeDef(TypedDict):
    authType: AuthenticationTypeType
    cognitoConfig: NotRequired[CognitoConfigTypeDef]
    openIDConnectConfig: NotRequired[OpenIDConnectConfigTypeDef]
    lambdaAuthorizerConfig: NotRequired[LambdaAuthorizerConfigTypeDef]


class AuthorizationConfigTypeDef(TypedDict):
    authorizationType: Literal["AWS_IAM"]
    awsIamConfig: NotRequired[AwsIamConfigTypeDef]


class StartSchemaCreationRequestRequestTypeDef(TypedDict):
    apiId: str
    definition: BlobTypeDef


class CodeErrorTypeDef(TypedDict):
    errorType: NotRequired[str]
    value: NotRequired[str]
    location: NotRequired[CodeErrorLocationTypeDef]


class CreateDomainNameResponseTypeDef(TypedDict):
    domainNameConfig: DomainNameConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDomainNameResponseTypeDef(TypedDict):
    domainNameConfig: DomainNameConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDomainNamesResponseTypeDef(TypedDict):
    domainNameConfigs: List[DomainNameConfigTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateDomainNameResponseTypeDef(TypedDict):
    domainNameConfig: DomainNameConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


CreateTypeResponseTypeDef = TypedDict(
    "CreateTypeResponseTypeDef",
    {
        "type": TypeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetTypeResponseTypeDef = TypedDict(
    "GetTypeResponseTypeDef",
    {
        "type": TypeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTypesByAssociationResponseTypeDef = TypedDict(
    "ListTypesByAssociationResponseTypeDef",
    {
        "types": List[TypeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
ListTypesResponseTypeDef = TypedDict(
    "ListTypesResponseTypeDef",
    {
        "types": List[TypeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
UpdateTypeResponseTypeDef = TypedDict(
    "UpdateTypeResponseTypeDef",
    {
        "type": TypeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DataSourceIntrospectionModelFieldTypeDef = TypedDict(
    "DataSourceIntrospectionModelFieldTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[DataSourceIntrospectionModelFieldTypeTypeDef],
        "length": NotRequired[int],
    },
)


class DynamodbDataSourceConfigTypeDef(TypedDict):
    tableName: str
    awsRegion: str
    useCallerCredentials: NotRequired[bool]
    deltaSyncConfig: NotRequired[DeltaSyncConfigTypeDef]
    versioned: NotRequired[bool]


class EvaluateMappingTemplateResponseTypeDef(TypedDict):
    evaluationResult: str
    error: ErrorDetailTypeDef
    logs: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class SyncConfigTypeDef(TypedDict):
    conflictHandler: NotRequired[ConflictHandlerTypeType]
    conflictDetection: NotRequired[ConflictDetectionTypeType]
    lambdaConflictHandlerConfig: NotRequired[LambdaConflictHandlerConfigTypeDef]


class ListApiKeysRequestListApiKeysPaginateTypeDef(TypedDict):
    apiId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListApisRequestListApisPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListChannelNamespacesRequestListChannelNamespacesPaginateTypeDef(TypedDict):
    apiId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataSourcesRequestListDataSourcesPaginateTypeDef(TypedDict):
    apiId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDomainNamesRequestListDomainNamesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFunctionsRequestListFunctionsPaginateTypeDef(TypedDict):
    apiId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGraphqlApisRequestListGraphqlApisPaginateTypeDef(TypedDict):
    apiType: NotRequired[GraphQLApiTypeType]
    owner: NotRequired[OwnershipType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResolversByFunctionRequestListResolversByFunctionPaginateTypeDef(TypedDict):
    apiId: str
    functionId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResolversRequestListResolversPaginateTypeDef(TypedDict):
    apiId: str
    typeName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSourceApiAssociationsRequestListSourceApiAssociationsPaginateTypeDef(TypedDict):
    apiId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListTypesByAssociationRequestListTypesByAssociationPaginateTypeDef = TypedDict(
    "ListTypesByAssociationRequestListTypesByAssociationPaginateTypeDef",
    {
        "mergedApiIdentifier": str,
        "associationId": str,
        "format": TypeDefinitionFormatType,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListTypesRequestListTypesPaginateTypeDef = TypedDict(
    "ListTypesRequestListTypesPaginateTypeDef",
    {
        "apiId": str,
        "format": TypeDefinitionFormatType,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListSourceApiAssociationsResponseTypeDef(TypedDict):
    sourceApiAssociationSummaries: List[SourceApiAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StartDataSourceIntrospectionRequestRequestTypeDef(TypedDict):
    rdsDataApiConfig: NotRequired[RdsDataApiConfigTypeDef]


class RelationalDatabaseDataSourceConfigTypeDef(TypedDict):
    relationalDatabaseSourceType: NotRequired[Literal["RDS_HTTP_ENDPOINT"]]
    rdsHttpEndpointConfig: NotRequired[RdsHttpEndpointConfigTypeDef]


class CreateGraphqlApiRequestRequestTypeDef(TypedDict):
    name: str
    authenticationType: AuthenticationTypeType
    logConfig: NotRequired[LogConfigTypeDef]
    userPoolConfig: NotRequired[UserPoolConfigTypeDef]
    openIDConnectConfig: NotRequired[OpenIDConnectConfigTypeDef]
    tags: NotRequired[Mapping[str, str]]
    additionalAuthenticationProviders: NotRequired[
        Sequence[AdditionalAuthenticationProviderTypeDef]
    ]
    xrayEnabled: NotRequired[bool]
    lambdaAuthorizerConfig: NotRequired[LambdaAuthorizerConfigTypeDef]
    apiType: NotRequired[GraphQLApiTypeType]
    mergedApiExecutionRoleArn: NotRequired[str]
    visibility: NotRequired[GraphQLApiVisibilityType]
    ownerContact: NotRequired[str]
    introspectionConfig: NotRequired[GraphQLApiIntrospectionConfigType]
    queryDepthLimit: NotRequired[int]
    resolverCountLimit: NotRequired[int]
    enhancedMetricsConfig: NotRequired[EnhancedMetricsConfigTypeDef]


class GraphqlApiTypeDef(TypedDict):
    name: NotRequired[str]
    apiId: NotRequired[str]
    authenticationType: NotRequired[AuthenticationTypeType]
    logConfig: NotRequired[LogConfigTypeDef]
    userPoolConfig: NotRequired[UserPoolConfigTypeDef]
    openIDConnectConfig: NotRequired[OpenIDConnectConfigTypeDef]
    arn: NotRequired[str]
    uris: NotRequired[Dict[str, str]]
    tags: NotRequired[Dict[str, str]]
    additionalAuthenticationProviders: NotRequired[List[AdditionalAuthenticationProviderTypeDef]]
    xrayEnabled: NotRequired[bool]
    wafWebAclArn: NotRequired[str]
    lambdaAuthorizerConfig: NotRequired[LambdaAuthorizerConfigTypeDef]
    dns: NotRequired[Dict[str, str]]
    visibility: NotRequired[GraphQLApiVisibilityType]
    apiType: NotRequired[GraphQLApiTypeType]
    mergedApiExecutionRoleArn: NotRequired[str]
    owner: NotRequired[str]
    ownerContact: NotRequired[str]
    introspectionConfig: NotRequired[GraphQLApiIntrospectionConfigType]
    queryDepthLimit: NotRequired[int]
    resolverCountLimit: NotRequired[int]
    enhancedMetricsConfig: NotRequired[EnhancedMetricsConfigTypeDef]


class UpdateGraphqlApiRequestRequestTypeDef(TypedDict):
    apiId: str
    name: str
    logConfig: NotRequired[LogConfigTypeDef]
    authenticationType: NotRequired[AuthenticationTypeType]
    userPoolConfig: NotRequired[UserPoolConfigTypeDef]
    openIDConnectConfig: NotRequired[OpenIDConnectConfigTypeDef]
    additionalAuthenticationProviders: NotRequired[
        Sequence[AdditionalAuthenticationProviderTypeDef]
    ]
    xrayEnabled: NotRequired[bool]
    lambdaAuthorizerConfig: NotRequired[LambdaAuthorizerConfigTypeDef]
    mergedApiExecutionRoleArn: NotRequired[str]
    ownerContact: NotRequired[str]
    introspectionConfig: NotRequired[GraphQLApiIntrospectionConfigType]
    queryDepthLimit: NotRequired[int]
    resolverCountLimit: NotRequired[int]
    enhancedMetricsConfig: NotRequired[EnhancedMetricsConfigTypeDef]


class AssociateMergedGraphqlApiResponseTypeDef(TypedDict):
    sourceApiAssociation: SourceApiAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateSourceGraphqlApiResponseTypeDef(TypedDict):
    sourceApiAssociation: SourceApiAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetSourceApiAssociationResponseTypeDef(TypedDict):
    sourceApiAssociation: SourceApiAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSourceApiAssociationResponseTypeDef(TypedDict):
    sourceApiAssociation: SourceApiAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateChannelNamespaceResponseTypeDef(TypedDict):
    channelNamespace: ChannelNamespaceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetChannelNamespaceResponseTypeDef(TypedDict):
    channelNamespace: ChannelNamespaceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListChannelNamespacesResponseTypeDef(TypedDict):
    channelNamespaces: List[ChannelNamespaceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateChannelNamespaceResponseTypeDef(TypedDict):
    channelNamespace: ChannelNamespaceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class EventConfigOutputTypeDef(TypedDict):
    authProviders: List[AuthProviderTypeDef]
    connectionAuthModes: List[AuthModeTypeDef]
    defaultPublishAuthModes: List[AuthModeTypeDef]
    defaultSubscribeAuthModes: List[AuthModeTypeDef]
    logConfig: NotRequired[EventLogConfigTypeDef]


class EventConfigTypeDef(TypedDict):
    authProviders: Sequence[AuthProviderTypeDef]
    connectionAuthModes: Sequence[AuthModeTypeDef]
    defaultPublishAuthModes: Sequence[AuthModeTypeDef]
    defaultSubscribeAuthModes: Sequence[AuthModeTypeDef]
    logConfig: NotRequired[EventLogConfigTypeDef]


class HttpDataSourceConfigTypeDef(TypedDict):
    endpoint: NotRequired[str]
    authorizationConfig: NotRequired[AuthorizationConfigTypeDef]


class EvaluateCodeErrorDetailTypeDef(TypedDict):
    message: NotRequired[str]
    codeErrors: NotRequired[List[CodeErrorTypeDef]]


class DataSourceIntrospectionModelTypeDef(TypedDict):
    name: NotRequired[str]
    fields: NotRequired[List[DataSourceIntrospectionModelFieldTypeDef]]
    primaryKey: NotRequired[DataSourceIntrospectionModelIndexTypeDef]
    indexes: NotRequired[List[DataSourceIntrospectionModelIndexTypeDef]]
    sdl: NotRequired[str]


class CreateFunctionRequestRequestTypeDef(TypedDict):
    apiId: str
    name: str
    dataSourceName: str
    description: NotRequired[str]
    requestMappingTemplate: NotRequired[str]
    responseMappingTemplate: NotRequired[str]
    functionVersion: NotRequired[str]
    syncConfig: NotRequired[SyncConfigTypeDef]
    maxBatchSize: NotRequired[int]
    runtime: NotRequired[AppSyncRuntimeTypeDef]
    code: NotRequired[str]


class CreateResolverRequestRequestTypeDef(TypedDict):
    apiId: str
    typeName: str
    fieldName: str
    dataSourceName: NotRequired[str]
    requestMappingTemplate: NotRequired[str]
    responseMappingTemplate: NotRequired[str]
    kind: NotRequired[ResolverKindType]
    pipelineConfig: NotRequired[PipelineConfigTypeDef]
    syncConfig: NotRequired[SyncConfigTypeDef]
    cachingConfig: NotRequired[CachingConfigTypeDef]
    maxBatchSize: NotRequired[int]
    runtime: NotRequired[AppSyncRuntimeTypeDef]
    code: NotRequired[str]
    metricsConfig: NotRequired[ResolverLevelMetricsConfigType]


class FunctionConfigurationTypeDef(TypedDict):
    functionId: NotRequired[str]
    functionArn: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    dataSourceName: NotRequired[str]
    requestMappingTemplate: NotRequired[str]
    responseMappingTemplate: NotRequired[str]
    functionVersion: NotRequired[str]
    syncConfig: NotRequired[SyncConfigTypeDef]
    maxBatchSize: NotRequired[int]
    runtime: NotRequired[AppSyncRuntimeTypeDef]
    code: NotRequired[str]


class ResolverTypeDef(TypedDict):
    typeName: NotRequired[str]
    fieldName: NotRequired[str]
    dataSourceName: NotRequired[str]
    resolverArn: NotRequired[str]
    requestMappingTemplate: NotRequired[str]
    responseMappingTemplate: NotRequired[str]
    kind: NotRequired[ResolverKindType]
    pipelineConfig: NotRequired[PipelineConfigOutputTypeDef]
    syncConfig: NotRequired[SyncConfigTypeDef]
    cachingConfig: NotRequired[CachingConfigOutputTypeDef]
    maxBatchSize: NotRequired[int]
    runtime: NotRequired[AppSyncRuntimeTypeDef]
    code: NotRequired[str]
    metricsConfig: NotRequired[ResolverLevelMetricsConfigType]


class UpdateFunctionRequestRequestTypeDef(TypedDict):
    apiId: str
    name: str
    functionId: str
    dataSourceName: str
    description: NotRequired[str]
    requestMappingTemplate: NotRequired[str]
    responseMappingTemplate: NotRequired[str]
    functionVersion: NotRequired[str]
    syncConfig: NotRequired[SyncConfigTypeDef]
    maxBatchSize: NotRequired[int]
    runtime: NotRequired[AppSyncRuntimeTypeDef]
    code: NotRequired[str]


class UpdateResolverRequestRequestTypeDef(TypedDict):
    apiId: str
    typeName: str
    fieldName: str
    dataSourceName: NotRequired[str]
    requestMappingTemplate: NotRequired[str]
    responseMappingTemplate: NotRequired[str]
    kind: NotRequired[ResolverKindType]
    pipelineConfig: NotRequired[PipelineConfigTypeDef]
    syncConfig: NotRequired[SyncConfigTypeDef]
    cachingConfig: NotRequired[CachingConfigTypeDef]
    maxBatchSize: NotRequired[int]
    runtime: NotRequired[AppSyncRuntimeTypeDef]
    code: NotRequired[str]
    metricsConfig: NotRequired[ResolverLevelMetricsConfigType]


class CreateGraphqlApiResponseTypeDef(TypedDict):
    graphqlApi: GraphqlApiTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetGraphqlApiResponseTypeDef(TypedDict):
    graphqlApi: GraphqlApiTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListGraphqlApisResponseTypeDef(TypedDict):
    graphqlApis: List[GraphqlApiTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateGraphqlApiResponseTypeDef(TypedDict):
    graphqlApi: GraphqlApiTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ApiTypeDef(TypedDict):
    apiId: NotRequired[str]
    name: NotRequired[str]
    ownerContact: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    dns: NotRequired[Dict[str, str]]
    apiArn: NotRequired[str]
    created: NotRequired[datetime]
    xrayEnabled: NotRequired[bool]
    wafWebAclArn: NotRequired[str]
    eventConfig: NotRequired[EventConfigOutputTypeDef]


class CreateApiRequestRequestTypeDef(TypedDict):
    name: str
    ownerContact: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    eventConfig: NotRequired[EventConfigTypeDef]


class UpdateApiRequestRequestTypeDef(TypedDict):
    apiId: str
    name: str
    ownerContact: NotRequired[str]
    eventConfig: NotRequired[EventConfigTypeDef]


CreateDataSourceRequestRequestTypeDef = TypedDict(
    "CreateDataSourceRequestRequestTypeDef",
    {
        "apiId": str,
        "name": str,
        "type": DataSourceTypeType,
        "description": NotRequired[str],
        "serviceRoleArn": NotRequired[str],
        "dynamodbConfig": NotRequired[DynamodbDataSourceConfigTypeDef],
        "lambdaConfig": NotRequired[LambdaDataSourceConfigTypeDef],
        "elasticsearchConfig": NotRequired[ElasticsearchDataSourceConfigTypeDef],
        "openSearchServiceConfig": NotRequired[OpenSearchServiceDataSourceConfigTypeDef],
        "httpConfig": NotRequired[HttpDataSourceConfigTypeDef],
        "relationalDatabaseConfig": NotRequired[RelationalDatabaseDataSourceConfigTypeDef],
        "eventBridgeConfig": NotRequired[EventBridgeDataSourceConfigTypeDef],
        "metricsConfig": NotRequired[DataSourceLevelMetricsConfigType],
    },
)
DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "dataSourceArn": NotRequired[str],
        "name": NotRequired[str],
        "description": NotRequired[str],
        "type": NotRequired[DataSourceTypeType],
        "serviceRoleArn": NotRequired[str],
        "dynamodbConfig": NotRequired[DynamodbDataSourceConfigTypeDef],
        "lambdaConfig": NotRequired[LambdaDataSourceConfigTypeDef],
        "elasticsearchConfig": NotRequired[ElasticsearchDataSourceConfigTypeDef],
        "openSearchServiceConfig": NotRequired[OpenSearchServiceDataSourceConfigTypeDef],
        "httpConfig": NotRequired[HttpDataSourceConfigTypeDef],
        "relationalDatabaseConfig": NotRequired[RelationalDatabaseDataSourceConfigTypeDef],
        "eventBridgeConfig": NotRequired[EventBridgeDataSourceConfigTypeDef],
        "metricsConfig": NotRequired[DataSourceLevelMetricsConfigType],
    },
)
UpdateDataSourceRequestRequestTypeDef = TypedDict(
    "UpdateDataSourceRequestRequestTypeDef",
    {
        "apiId": str,
        "name": str,
        "type": DataSourceTypeType,
        "description": NotRequired[str],
        "serviceRoleArn": NotRequired[str],
        "dynamodbConfig": NotRequired[DynamodbDataSourceConfigTypeDef],
        "lambdaConfig": NotRequired[LambdaDataSourceConfigTypeDef],
        "elasticsearchConfig": NotRequired[ElasticsearchDataSourceConfigTypeDef],
        "openSearchServiceConfig": NotRequired[OpenSearchServiceDataSourceConfigTypeDef],
        "httpConfig": NotRequired[HttpDataSourceConfigTypeDef],
        "relationalDatabaseConfig": NotRequired[RelationalDatabaseDataSourceConfigTypeDef],
        "eventBridgeConfig": NotRequired[EventBridgeDataSourceConfigTypeDef],
        "metricsConfig": NotRequired[DataSourceLevelMetricsConfigType],
    },
)


class EvaluateCodeResponseTypeDef(TypedDict):
    evaluationResult: str
    error: EvaluateCodeErrorDetailTypeDef
    logs: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class DataSourceIntrospectionResultTypeDef(TypedDict):
    models: NotRequired[List[DataSourceIntrospectionModelTypeDef]]
    nextToken: NotRequired[str]


class CreateFunctionResponseTypeDef(TypedDict):
    functionConfiguration: FunctionConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetFunctionResponseTypeDef(TypedDict):
    functionConfiguration: FunctionConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListFunctionsResponseTypeDef(TypedDict):
    functions: List[FunctionConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateFunctionResponseTypeDef(TypedDict):
    functionConfiguration: FunctionConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateResolverResponseTypeDef(TypedDict):
    resolver: ResolverTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetResolverResponseTypeDef(TypedDict):
    resolver: ResolverTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListResolversByFunctionResponseTypeDef(TypedDict):
    resolvers: List[ResolverTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListResolversResponseTypeDef(TypedDict):
    resolvers: List[ResolverTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateResolverResponseTypeDef(TypedDict):
    resolver: ResolverTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateApiResponseTypeDef(TypedDict):
    api: ApiTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetApiResponseTypeDef(TypedDict):
    api: ApiTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListApisResponseTypeDef(TypedDict):
    apis: List[ApiTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateApiResponseTypeDef(TypedDict):
    api: ApiTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataSourceResponseTypeDef(TypedDict):
    dataSource: DataSourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDataSourceResponseTypeDef(TypedDict):
    dataSource: DataSourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDataSourcesResponseTypeDef(TypedDict):
    dataSources: List[DataSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateDataSourceResponseTypeDef(TypedDict):
    dataSource: DataSourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDataSourceIntrospectionResponseTypeDef(TypedDict):
    introspectionId: str
    introspectionStatus: DataSourceIntrospectionStatusType
    introspectionStatusDetail: str
    introspectionResult: DataSourceIntrospectionResultTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
