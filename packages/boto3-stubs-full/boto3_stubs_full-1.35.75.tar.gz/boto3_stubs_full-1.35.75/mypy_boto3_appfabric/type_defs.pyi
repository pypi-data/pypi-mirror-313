"""
Type annotations for appfabric service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/type_defs/)

Usage::

    ```python
    from mypy_boto3_appfabric.type_defs import ApiKeyCredentialTypeDef

    data: ApiKeyCredentialTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AppAuthorizationStatusType,
    AuthTypeType,
    FormatType,
    IngestionDestinationStatusType,
    IngestionStateType,
    PersonaType,
    ResultStatusType,
    SchemaType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "ApiKeyCredentialTypeDef",
    "AppAuthorizationSummaryTypeDef",
    "AppAuthorizationTypeDef",
    "AppBundleSummaryTypeDef",
    "AppBundleTypeDef",
    "AuditLogDestinationConfigurationTypeDef",
    "AuditLogProcessingConfigurationTypeDef",
    "AuthRequestTypeDef",
    "BatchGetUserAccessTasksRequestRequestTypeDef",
    "BatchGetUserAccessTasksResponseTypeDef",
    "ConnectAppAuthorizationRequestRequestTypeDef",
    "ConnectAppAuthorizationResponseTypeDef",
    "CreateAppAuthorizationRequestRequestTypeDef",
    "CreateAppAuthorizationResponseTypeDef",
    "CreateAppBundleRequestRequestTypeDef",
    "CreateAppBundleResponseTypeDef",
    "CreateIngestionDestinationRequestRequestTypeDef",
    "CreateIngestionDestinationResponseTypeDef",
    "CreateIngestionRequestRequestTypeDef",
    "CreateIngestionResponseTypeDef",
    "CredentialTypeDef",
    "DeleteAppAuthorizationRequestRequestTypeDef",
    "DeleteAppBundleRequestRequestTypeDef",
    "DeleteIngestionDestinationRequestRequestTypeDef",
    "DeleteIngestionRequestRequestTypeDef",
    "DestinationConfigurationTypeDef",
    "DestinationTypeDef",
    "FirehoseStreamTypeDef",
    "GetAppAuthorizationRequestRequestTypeDef",
    "GetAppAuthorizationResponseTypeDef",
    "GetAppBundleRequestRequestTypeDef",
    "GetAppBundleResponseTypeDef",
    "GetIngestionDestinationRequestRequestTypeDef",
    "GetIngestionDestinationResponseTypeDef",
    "GetIngestionRequestRequestTypeDef",
    "GetIngestionResponseTypeDef",
    "IngestionDestinationSummaryTypeDef",
    "IngestionDestinationTypeDef",
    "IngestionSummaryTypeDef",
    "IngestionTypeDef",
    "ListAppAuthorizationsRequestListAppAuthorizationsPaginateTypeDef",
    "ListAppAuthorizationsRequestRequestTypeDef",
    "ListAppAuthorizationsResponseTypeDef",
    "ListAppBundlesRequestListAppBundlesPaginateTypeDef",
    "ListAppBundlesRequestRequestTypeDef",
    "ListAppBundlesResponseTypeDef",
    "ListIngestionDestinationsRequestListIngestionDestinationsPaginateTypeDef",
    "ListIngestionDestinationsRequestRequestTypeDef",
    "ListIngestionDestinationsResponseTypeDef",
    "ListIngestionsRequestListIngestionsPaginateTypeDef",
    "ListIngestionsRequestRequestTypeDef",
    "ListIngestionsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "Oauth2CredentialTypeDef",
    "PaginatorConfigTypeDef",
    "ProcessingConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "S3BucketTypeDef",
    "StartIngestionRequestRequestTypeDef",
    "StartUserAccessTasksRequestRequestTypeDef",
    "StartUserAccessTasksResponseTypeDef",
    "StopIngestionRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TaskErrorTypeDef",
    "TenantTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAppAuthorizationRequestRequestTypeDef",
    "UpdateAppAuthorizationResponseTypeDef",
    "UpdateIngestionDestinationRequestRequestTypeDef",
    "UpdateIngestionDestinationResponseTypeDef",
    "UserAccessResultItemTypeDef",
    "UserAccessTaskItemTypeDef",
)

class ApiKeyCredentialTypeDef(TypedDict):
    apiKey: str

class TenantTypeDef(TypedDict):
    tenantIdentifier: str
    tenantDisplayName: str

class AppBundleSummaryTypeDef(TypedDict):
    arn: str

class AppBundleTypeDef(TypedDict):
    arn: str
    customerManagedKeyArn: NotRequired[str]

AuditLogProcessingConfigurationTypeDef = TypedDict(
    "AuditLogProcessingConfigurationTypeDef",
    {
        "schema": SchemaType,
        "format": FormatType,
    },
)

class AuthRequestTypeDef(TypedDict):
    redirectUri: str
    code: str

class BatchGetUserAccessTasksRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str
    taskIdList: Sequence[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class TagTypeDef(TypedDict):
    key: str
    value: str

class IngestionTypeDef(TypedDict):
    arn: str
    appBundleArn: str
    app: str
    tenantId: str
    createdAt: datetime
    updatedAt: datetime
    state: IngestionStateType
    ingestionType: Literal["auditLog"]

class Oauth2CredentialTypeDef(TypedDict):
    clientId: str
    clientSecret: str

class DeleteAppAuthorizationRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str
    appAuthorizationIdentifier: str

class DeleteAppBundleRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str

class DeleteIngestionDestinationRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str
    ingestionIdentifier: str
    ingestionDestinationIdentifier: str

class DeleteIngestionRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str
    ingestionIdentifier: str

class FirehoseStreamTypeDef(TypedDict):
    streamName: str

class S3BucketTypeDef(TypedDict):
    bucketName: str
    prefix: NotRequired[str]

class GetAppAuthorizationRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str
    appAuthorizationIdentifier: str

class GetAppBundleRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str

class GetIngestionDestinationRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str
    ingestionIdentifier: str
    ingestionDestinationIdentifier: str

class GetIngestionRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str
    ingestionIdentifier: str

class IngestionDestinationSummaryTypeDef(TypedDict):
    arn: str

class IngestionSummaryTypeDef(TypedDict):
    arn: str
    app: str
    tenantId: str
    state: IngestionStateType

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAppAuthorizationsRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAppBundlesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListIngestionDestinationsRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str
    ingestionIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListIngestionsRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class StartIngestionRequestRequestTypeDef(TypedDict):
    ingestionIdentifier: str
    appBundleIdentifier: str

class StartUserAccessTasksRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str
    email: str

class StopIngestionRequestRequestTypeDef(TypedDict):
    ingestionIdentifier: str
    appBundleIdentifier: str

class TaskErrorTypeDef(TypedDict):
    errorCode: NotRequired[str]
    errorMessage: NotRequired[str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class AppAuthorizationSummaryTypeDef(TypedDict):
    appAuthorizationArn: str
    appBundleArn: str
    app: str
    tenant: TenantTypeDef
    status: AppAuthorizationStatusType
    updatedAt: datetime

class AppAuthorizationTypeDef(TypedDict):
    appAuthorizationArn: str
    appBundleArn: str
    app: str
    tenant: TenantTypeDef
    authType: AuthTypeType
    status: AppAuthorizationStatusType
    createdAt: datetime
    updatedAt: datetime
    persona: NotRequired[PersonaType]
    authUrl: NotRequired[str]

class ProcessingConfigurationTypeDef(TypedDict):
    auditLog: NotRequired[AuditLogProcessingConfigurationTypeDef]

class ConnectAppAuthorizationRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str
    appAuthorizationIdentifier: str
    authRequest: NotRequired[AuthRequestTypeDef]

class CreateAppBundleResponseTypeDef(TypedDict):
    appBundle: AppBundleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAppBundleResponseTypeDef(TypedDict):
    appBundle: AppBundleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAppBundlesResponseTypeDef(TypedDict):
    appBundleSummaryList: List[AppBundleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateAppBundleRequestRequestTypeDef(TypedDict):
    clientToken: NotRequired[str]
    customerManagedKeyIdentifier: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateIngestionRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str
    app: str
    tenantId: str
    ingestionType: Literal["auditLog"]
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]

class CreateIngestionResponseTypeDef(TypedDict):
    ingestion: IngestionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetIngestionResponseTypeDef(TypedDict):
    ingestion: IngestionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CredentialTypeDef(TypedDict):
    oauth2Credential: NotRequired[Oauth2CredentialTypeDef]
    apiKeyCredential: NotRequired[ApiKeyCredentialTypeDef]

class DestinationTypeDef(TypedDict):
    s3Bucket: NotRequired[S3BucketTypeDef]
    firehoseStream: NotRequired[FirehoseStreamTypeDef]

class ListIngestionDestinationsResponseTypeDef(TypedDict):
    ingestionDestinations: List[IngestionDestinationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListIngestionsResponseTypeDef(TypedDict):
    ingestions: List[IngestionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAppAuthorizationsRequestListAppAuthorizationsPaginateTypeDef(TypedDict):
    appBundleIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAppBundlesRequestListAppBundlesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListIngestionDestinationsRequestListIngestionDestinationsPaginateTypeDef(TypedDict):
    appBundleIdentifier: str
    ingestionIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListIngestionsRequestListIngestionsPaginateTypeDef(TypedDict):
    appBundleIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class UserAccessResultItemTypeDef(TypedDict):
    app: NotRequired[str]
    tenantId: NotRequired[str]
    tenantDisplayName: NotRequired[str]
    taskId: NotRequired[str]
    resultStatus: NotRequired[ResultStatusType]
    email: NotRequired[str]
    userId: NotRequired[str]
    userFullName: NotRequired[str]
    userFirstName: NotRequired[str]
    userLastName: NotRequired[str]
    userStatus: NotRequired[str]
    taskError: NotRequired[TaskErrorTypeDef]

class UserAccessTaskItemTypeDef(TypedDict):
    app: str
    tenantId: str
    taskId: NotRequired[str]
    error: NotRequired[TaskErrorTypeDef]

class ConnectAppAuthorizationResponseTypeDef(TypedDict):
    appAuthorizationSummary: AppAuthorizationSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAppAuthorizationsResponseTypeDef(TypedDict):
    appAuthorizationSummaryList: List[AppAuthorizationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateAppAuthorizationResponseTypeDef(TypedDict):
    appAuthorization: AppAuthorizationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAppAuthorizationResponseTypeDef(TypedDict):
    appAuthorization: AppAuthorizationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAppAuthorizationResponseTypeDef(TypedDict):
    appAuthorization: AppAuthorizationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAppAuthorizationRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str
    app: str
    credential: CredentialTypeDef
    tenant: TenantTypeDef
    authType: AuthTypeType
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class UpdateAppAuthorizationRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str
    appAuthorizationIdentifier: str
    credential: NotRequired[CredentialTypeDef]
    tenant: NotRequired[TenantTypeDef]

class AuditLogDestinationConfigurationTypeDef(TypedDict):
    destination: DestinationTypeDef

class BatchGetUserAccessTasksResponseTypeDef(TypedDict):
    userAccessResultsList: List[UserAccessResultItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StartUserAccessTasksResponseTypeDef(TypedDict):
    userAccessTasksList: List[UserAccessTaskItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DestinationConfigurationTypeDef(TypedDict):
    auditLog: NotRequired[AuditLogDestinationConfigurationTypeDef]

class CreateIngestionDestinationRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str
    ingestionIdentifier: str
    processingConfiguration: ProcessingConfigurationTypeDef
    destinationConfiguration: DestinationConfigurationTypeDef
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class IngestionDestinationTypeDef(TypedDict):
    arn: str
    ingestionArn: str
    processingConfiguration: ProcessingConfigurationTypeDef
    destinationConfiguration: DestinationConfigurationTypeDef
    status: NotRequired[IngestionDestinationStatusType]
    statusReason: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class UpdateIngestionDestinationRequestRequestTypeDef(TypedDict):
    appBundleIdentifier: str
    ingestionIdentifier: str
    ingestionDestinationIdentifier: str
    destinationConfiguration: DestinationConfigurationTypeDef

class CreateIngestionDestinationResponseTypeDef(TypedDict):
    ingestionDestination: IngestionDestinationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetIngestionDestinationResponseTypeDef(TypedDict):
    ingestionDestination: IngestionDestinationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateIngestionDestinationResponseTypeDef(TypedDict):
    ingestionDestination: IngestionDestinationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
