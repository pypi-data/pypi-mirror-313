"""
Type annotations for qapps service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qapps/type_defs/)

Usage::

    ```python
    from mypy_boto3_qapps.type_defs import AssociateLibraryItemReviewInputRequestTypeDef

    data: AssociateLibraryItemReviewInputRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AppRequiredCapabilityType,
    AppStatusType,
    CardOutputSourceType,
    CardTypeType,
    DocumentScopeType,
    ExecutionStatusType,
    InputCardComputeModeType,
    LibraryItemStatusType,
    PermissionInputActionEnumType,
    PermissionOutputActionEnumType,
    PluginTypeType,
    PrincipalOutputUserTypeEnumType,
    SenderType,
    SubmissionMutationKindType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AppDefinitionInputOutputTypeDef",
    "AppDefinitionInputTypeDef",
    "AppDefinitionTypeDef",
    "AssociateLibraryItemReviewInputRequestTypeDef",
    "AssociateQAppWithUserInputRequestTypeDef",
    "AttributeFilterOutputTypeDef",
    "AttributeFilterTypeDef",
    "AttributeFilterUnionTypeDef",
    "BatchCreateCategoryInputCategoryTypeDef",
    "BatchCreateCategoryInputRequestTypeDef",
    "BatchDeleteCategoryInputRequestTypeDef",
    "BatchUpdateCategoryInputRequestTypeDef",
    "CardInputOutputTypeDef",
    "CardInputTypeDef",
    "CardInputUnionTypeDef",
    "CardStatusTypeDef",
    "CardTypeDef",
    "CardValueTypeDef",
    "CategoryInputTypeDef",
    "CategoryTypeDef",
    "ConversationMessageTypeDef",
    "CreateLibraryItemInputRequestTypeDef",
    "CreateLibraryItemOutputTypeDef",
    "CreatePresignedUrlInputRequestTypeDef",
    "CreatePresignedUrlOutputTypeDef",
    "CreateQAppInputRequestTypeDef",
    "CreateQAppOutputTypeDef",
    "DeleteLibraryItemInputRequestTypeDef",
    "DeleteQAppInputRequestTypeDef",
    "DescribeQAppPermissionsInputRequestTypeDef",
    "DescribeQAppPermissionsOutputTypeDef",
    "DisassociateLibraryItemReviewInputRequestTypeDef",
    "DisassociateQAppFromUserInputRequestTypeDef",
    "DocumentAttributeOutputTypeDef",
    "DocumentAttributeTypeDef",
    "DocumentAttributeUnionTypeDef",
    "DocumentAttributeValueOutputTypeDef",
    "DocumentAttributeValueTypeDef",
    "DocumentAttributeValueUnionTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExportQAppSessionDataInputRequestTypeDef",
    "ExportQAppSessionDataOutputTypeDef",
    "FileUploadCardInputTypeDef",
    "FileUploadCardTypeDef",
    "FormInputCardInputOutputTypeDef",
    "FormInputCardInputTypeDef",
    "FormInputCardInputUnionTypeDef",
    "FormInputCardMetadataOutputTypeDef",
    "FormInputCardMetadataTypeDef",
    "FormInputCardMetadataUnionTypeDef",
    "FormInputCardTypeDef",
    "GetLibraryItemInputRequestTypeDef",
    "GetLibraryItemOutputTypeDef",
    "GetQAppInputRequestTypeDef",
    "GetQAppOutputTypeDef",
    "GetQAppSessionInputRequestTypeDef",
    "GetQAppSessionMetadataInputRequestTypeDef",
    "GetQAppSessionMetadataOutputTypeDef",
    "GetQAppSessionOutputTypeDef",
    "ImportDocumentInputRequestTypeDef",
    "ImportDocumentOutputTypeDef",
    "LibraryItemMemberTypeDef",
    "ListCategoriesInputRequestTypeDef",
    "ListCategoriesOutputTypeDef",
    "ListLibraryItemsInputListLibraryItemsPaginateTypeDef",
    "ListLibraryItemsInputRequestTypeDef",
    "ListLibraryItemsOutputTypeDef",
    "ListQAppSessionDataInputRequestTypeDef",
    "ListQAppSessionDataOutputTypeDef",
    "ListQAppsInputListQAppsPaginateTypeDef",
    "ListQAppsInputRequestTypeDef",
    "ListQAppsOutputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PermissionInputTypeDef",
    "PermissionOutputTypeDef",
    "PredictAppDefinitionTypeDef",
    "PredictQAppInputOptionsTypeDef",
    "PredictQAppInputRequestTypeDef",
    "PredictQAppOutputTypeDef",
    "PrincipalOutputTypeDef",
    "QAppSessionDataTypeDef",
    "QPluginCardInputTypeDef",
    "QPluginCardTypeDef",
    "QQueryCardInputOutputTypeDef",
    "QQueryCardInputTypeDef",
    "QQueryCardInputUnionTypeDef",
    "QQueryCardTypeDef",
    "ResponseMetadataTypeDef",
    "SessionSharingConfigurationTypeDef",
    "StartQAppSessionInputRequestTypeDef",
    "StartQAppSessionOutputTypeDef",
    "StopQAppSessionInputRequestTypeDef",
    "SubmissionMutationTypeDef",
    "SubmissionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TextInputCardInputTypeDef",
    "TextInputCardTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateLibraryItemInputRequestTypeDef",
    "UpdateLibraryItemMetadataInputRequestTypeDef",
    "UpdateLibraryItemOutputTypeDef",
    "UpdateQAppInputRequestTypeDef",
    "UpdateQAppOutputTypeDef",
    "UpdateQAppPermissionsInputRequestTypeDef",
    "UpdateQAppPermissionsOutputTypeDef",
    "UpdateQAppSessionInputRequestTypeDef",
    "UpdateQAppSessionMetadataInputRequestTypeDef",
    "UpdateQAppSessionMetadataOutputTypeDef",
    "UpdateQAppSessionOutputTypeDef",
    "UserAppItemTypeDef",
    "UserTypeDef",
)

class AssociateLibraryItemReviewInputRequestTypeDef(TypedDict):
    instanceId: str
    libraryItemId: str

class AssociateQAppWithUserInputRequestTypeDef(TypedDict):
    instanceId: str
    appId: str

BatchCreateCategoryInputCategoryTypeDef = TypedDict(
    "BatchCreateCategoryInputCategoryTypeDef",
    {
        "title": str,
        "id": NotRequired[str],
        "color": NotRequired[str],
    },
)

class BatchDeleteCategoryInputRequestTypeDef(TypedDict):
    instanceId: str
    categories: Sequence[str]

CategoryInputTypeDef = TypedDict(
    "CategoryInputTypeDef",
    {
        "id": str,
        "title": str,
        "color": NotRequired[str],
    },
)
FileUploadCardInputTypeDef = TypedDict(
    "FileUploadCardInputTypeDef",
    {
        "title": str,
        "id": str,
        "type": CardTypeType,
        "filename": NotRequired[str],
        "fileId": NotRequired[str],
        "allowOverride": NotRequired[bool],
    },
)
QPluginCardInputTypeDef = TypedDict(
    "QPluginCardInputTypeDef",
    {
        "title": str,
        "id": str,
        "type": CardTypeType,
        "prompt": str,
        "pluginId": str,
        "actionIdentifier": NotRequired[str],
    },
)
TextInputCardInputTypeDef = TypedDict(
    "TextInputCardInputTypeDef",
    {
        "title": str,
        "id": str,
        "type": CardTypeType,
        "placeholder": NotRequired[str],
        "defaultValue": NotRequired[str],
    },
)

class SubmissionTypeDef(TypedDict):
    value: NotRequired[Dict[str, Any]]
    submissionId: NotRequired[str]
    timestamp: NotRequired[datetime]

FileUploadCardTypeDef = TypedDict(
    "FileUploadCardTypeDef",
    {
        "id": str,
        "title": str,
        "dependencies": List[str],
        "type": CardTypeType,
        "filename": NotRequired[str],
        "fileId": NotRequired[str],
        "allowOverride": NotRequired[bool],
    },
)
QPluginCardTypeDef = TypedDict(
    "QPluginCardTypeDef",
    {
        "id": str,
        "title": str,
        "dependencies": List[str],
        "type": CardTypeType,
        "prompt": str,
        "pluginType": PluginTypeType,
        "pluginId": str,
        "actionIdentifier": NotRequired[str],
    },
)
TextInputCardTypeDef = TypedDict(
    "TextInputCardTypeDef",
    {
        "id": str,
        "title": str,
        "dependencies": List[str],
        "type": CardTypeType,
        "placeholder": NotRequired[str],
        "defaultValue": NotRequired[str],
    },
)

class SubmissionMutationTypeDef(TypedDict):
    submissionId: str
    mutationType: SubmissionMutationKindType

CategoryTypeDef = TypedDict(
    "CategoryTypeDef",
    {
        "id": str,
        "title": str,
        "color": NotRequired[str],
        "appCount": NotRequired[int],
    },
)
ConversationMessageTypeDef = TypedDict(
    "ConversationMessageTypeDef",
    {
        "body": str,
        "type": SenderType,
    },
)

class CreateLibraryItemInputRequestTypeDef(TypedDict):
    instanceId: str
    appId: str
    appVersion: int
    categories: Sequence[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreatePresignedUrlInputRequestTypeDef(TypedDict):
    instanceId: str
    cardId: str
    appId: str
    fileContentsSha256: str
    fileName: str
    scope: DocumentScopeType
    sessionId: NotRequired[str]

class DeleteLibraryItemInputRequestTypeDef(TypedDict):
    instanceId: str
    libraryItemId: str

class DeleteQAppInputRequestTypeDef(TypedDict):
    instanceId: str
    appId: str

class DescribeQAppPermissionsInputRequestTypeDef(TypedDict):
    instanceId: str
    appId: str

class DisassociateLibraryItemReviewInputRequestTypeDef(TypedDict):
    instanceId: str
    libraryItemId: str

class DisassociateQAppFromUserInputRequestTypeDef(TypedDict):
    instanceId: str
    appId: str

class DocumentAttributeValueOutputTypeDef(TypedDict):
    stringValue: NotRequired[str]
    stringListValue: NotRequired[List[str]]
    longValue: NotRequired[int]
    dateValue: NotRequired[datetime]

TimestampTypeDef = Union[datetime, str]

class ExportQAppSessionDataInputRequestTypeDef(TypedDict):
    instanceId: str
    sessionId: str

class FormInputCardMetadataOutputTypeDef(TypedDict):
    schema: Dict[str, Any]

class FormInputCardMetadataTypeDef(TypedDict):
    schema: Mapping[str, Any]

class GetLibraryItemInputRequestTypeDef(TypedDict):
    instanceId: str
    libraryItemId: str
    appId: NotRequired[str]

class GetQAppInputRequestTypeDef(TypedDict):
    instanceId: str
    appId: str
    appVersion: NotRequired[int]

class GetQAppSessionInputRequestTypeDef(TypedDict):
    instanceId: str
    sessionId: str

class GetQAppSessionMetadataInputRequestTypeDef(TypedDict):
    instanceId: str
    sessionId: str

class SessionSharingConfigurationTypeDef(TypedDict):
    enabled: bool
    acceptResponses: NotRequired[bool]
    revealCards: NotRequired[bool]

class ImportDocumentInputRequestTypeDef(TypedDict):
    instanceId: str
    cardId: str
    appId: str
    fileContentsBase64: str
    fileName: str
    scope: DocumentScopeType
    sessionId: NotRequired[str]

class ListCategoriesInputRequestTypeDef(TypedDict):
    instanceId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListLibraryItemsInputRequestTypeDef(TypedDict):
    instanceId: str
    limit: NotRequired[int]
    nextToken: NotRequired[str]
    categoryId: NotRequired[str]

class ListQAppSessionDataInputRequestTypeDef(TypedDict):
    instanceId: str
    sessionId: str

class ListQAppsInputRequestTypeDef(TypedDict):
    instanceId: str
    limit: NotRequired[int]
    nextToken: NotRequired[str]

class UserAppItemTypeDef(TypedDict):
    appId: str
    appArn: str
    title: str
    createdAt: datetime
    description: NotRequired[str]
    canEdit: NotRequired[bool]
    status: NotRequired[str]
    isVerified: NotRequired[bool]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str

class PermissionInputTypeDef(TypedDict):
    action: PermissionInputActionEnumType
    principal: str

class PrincipalOutputTypeDef(TypedDict):
    userId: NotRequired[str]
    userType: NotRequired[PrincipalOutputUserTypeEnumType]
    email: NotRequired[str]

class UserTypeDef(TypedDict):
    userId: NotRequired[str]

class StopQAppSessionInputRequestTypeDef(TypedDict):
    instanceId: str
    sessionId: str

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str
    tagKeys: Sequence[str]

class UpdateLibraryItemInputRequestTypeDef(TypedDict):
    instanceId: str
    libraryItemId: str
    status: NotRequired[LibraryItemStatusType]
    categories: NotRequired[Sequence[str]]

class UpdateLibraryItemMetadataInputRequestTypeDef(TypedDict):
    instanceId: str
    libraryItemId: str
    isVerified: NotRequired[bool]

class BatchCreateCategoryInputRequestTypeDef(TypedDict):
    instanceId: str
    categories: Sequence[BatchCreateCategoryInputCategoryTypeDef]

class BatchUpdateCategoryInputRequestTypeDef(TypedDict):
    instanceId: str
    categories: Sequence[CategoryInputTypeDef]

class CardStatusTypeDef(TypedDict):
    currentState: ExecutionStatusType
    currentValue: str
    submissions: NotRequired[List[SubmissionTypeDef]]

class CardValueTypeDef(TypedDict):
    cardId: str
    value: str
    submissionMutation: NotRequired[SubmissionMutationTypeDef]

class LibraryItemMemberTypeDef(TypedDict):
    libraryItemId: str
    appId: str
    appVersion: int
    categories: List[CategoryTypeDef]
    status: str
    createdAt: datetime
    createdBy: str
    ratingCount: int
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]
    isRatedByUser: NotRequired[bool]
    userCount: NotRequired[int]
    isVerified: NotRequired[bool]

class PredictQAppInputOptionsTypeDef(TypedDict):
    conversation: NotRequired[Sequence[ConversationMessageTypeDef]]
    problemStatement: NotRequired[str]

class CreateLibraryItemOutputTypeDef(TypedDict):
    libraryItemId: str
    status: str
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    ratingCount: int
    isVerified: bool
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePresignedUrlOutputTypeDef(TypedDict):
    fileId: str
    presignedUrl: str
    presignedUrlFields: Dict[str, str]
    presignedUrlExpiration: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateQAppOutputTypeDef(TypedDict):
    appId: str
    appArn: str
    title: str
    description: str
    initialPrompt: str
    appVersion: int
    status: AppStatusType
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    requiredCapabilities: List[AppRequiredCapabilityType]
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ExportQAppSessionDataOutputTypeDef(TypedDict):
    csvFileLink: str
    expiresAt: datetime
    sessionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetLibraryItemOutputTypeDef(TypedDict):
    libraryItemId: str
    appId: str
    appVersion: int
    categories: List[CategoryTypeDef]
    status: str
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    ratingCount: int
    isRatedByUser: bool
    userCount: int
    isVerified: bool
    ResponseMetadata: ResponseMetadataTypeDef

class ImportDocumentOutputTypeDef(TypedDict):
    fileId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListCategoriesOutputTypeDef(TypedDict):
    categories: List[CategoryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class StartQAppSessionOutputTypeDef(TypedDict):
    sessionId: str
    sessionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateLibraryItemOutputTypeDef(TypedDict):
    libraryItemId: str
    appId: str
    appVersion: int
    categories: List[CategoryTypeDef]
    status: str
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    ratingCount: int
    isRatedByUser: bool
    userCount: int
    isVerified: bool
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateQAppOutputTypeDef(TypedDict):
    appId: str
    appArn: str
    title: str
    description: str
    initialPrompt: str
    appVersion: int
    status: AppStatusType
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    requiredCapabilities: List[AppRequiredCapabilityType]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateQAppSessionOutputTypeDef(TypedDict):
    sessionId: str
    sessionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DocumentAttributeOutputTypeDef(TypedDict):
    name: str
    value: DocumentAttributeValueOutputTypeDef

class DocumentAttributeValueTypeDef(TypedDict):
    stringValue: NotRequired[str]
    stringListValue: NotRequired[Sequence[str]]
    longValue: NotRequired[int]
    dateValue: NotRequired[TimestampTypeDef]

FormInputCardInputOutputTypeDef = TypedDict(
    "FormInputCardInputOutputTypeDef",
    {
        "title": str,
        "id": str,
        "type": CardTypeType,
        "metadata": FormInputCardMetadataOutputTypeDef,
        "computeMode": NotRequired[InputCardComputeModeType],
    },
)
FormInputCardTypeDef = TypedDict(
    "FormInputCardTypeDef",
    {
        "id": str,
        "title": str,
        "dependencies": List[str],
        "type": CardTypeType,
        "metadata": FormInputCardMetadataOutputTypeDef,
        "computeMode": NotRequired[InputCardComputeModeType],
    },
)
FormInputCardMetadataUnionTypeDef = Union[
    FormInputCardMetadataTypeDef, FormInputCardMetadataOutputTypeDef
]

class GetQAppSessionMetadataOutputTypeDef(TypedDict):
    sessionId: str
    sessionArn: str
    sessionName: str
    sharingConfiguration: SessionSharingConfigurationTypeDef
    sessionOwner: bool
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateQAppSessionMetadataInputRequestTypeDef(TypedDict):
    instanceId: str
    sessionId: str
    sharingConfiguration: SessionSharingConfigurationTypeDef
    sessionName: NotRequired[str]

class UpdateQAppSessionMetadataOutputTypeDef(TypedDict):
    sessionId: str
    sessionArn: str
    sessionName: str
    sharingConfiguration: SessionSharingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListLibraryItemsInputListLibraryItemsPaginateTypeDef(TypedDict):
    instanceId: str
    categoryId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListQAppsInputListQAppsPaginateTypeDef(TypedDict):
    instanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListQAppsOutputTypeDef(TypedDict):
    apps: List[UserAppItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateQAppPermissionsInputRequestTypeDef(TypedDict):
    instanceId: str
    appId: str
    grantPermissions: NotRequired[Sequence[PermissionInputTypeDef]]
    revokePermissions: NotRequired[Sequence[PermissionInputTypeDef]]

class PermissionOutputTypeDef(TypedDict):
    action: PermissionOutputActionEnumType
    principal: PrincipalOutputTypeDef

class QAppSessionDataTypeDef(TypedDict):
    cardId: str
    user: UserTypeDef
    value: NotRequired[Dict[str, Any]]
    submissionId: NotRequired[str]
    timestamp: NotRequired[datetime]

class GetQAppSessionOutputTypeDef(TypedDict):
    sessionId: str
    sessionArn: str
    sessionName: str
    appVersion: int
    latestPublishedAppVersion: int
    status: ExecutionStatusType
    cardStatus: Dict[str, CardStatusTypeDef]
    userIsHost: bool
    ResponseMetadata: ResponseMetadataTypeDef

class StartQAppSessionInputRequestTypeDef(TypedDict):
    instanceId: str
    appId: str
    appVersion: int
    initialValues: NotRequired[Sequence[CardValueTypeDef]]
    sessionId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class UpdateQAppSessionInputRequestTypeDef(TypedDict):
    instanceId: str
    sessionId: str
    values: NotRequired[Sequence[CardValueTypeDef]]

class ListLibraryItemsOutputTypeDef(TypedDict):
    libraryItems: List[LibraryItemMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PredictQAppInputRequestTypeDef(TypedDict):
    instanceId: str
    options: NotRequired[PredictQAppInputOptionsTypeDef]

class AttributeFilterOutputTypeDef(TypedDict):
    andAllFilters: NotRequired[List[Dict[str, Any]]]
    orAllFilters: NotRequired[List[Dict[str, Any]]]
    notFilter: NotRequired[Dict[str, Any]]
    equalsTo: NotRequired[DocumentAttributeOutputTypeDef]
    containsAll: NotRequired[DocumentAttributeOutputTypeDef]
    containsAny: NotRequired[DocumentAttributeOutputTypeDef]
    greaterThan: NotRequired[DocumentAttributeOutputTypeDef]
    greaterThanOrEquals: NotRequired[DocumentAttributeOutputTypeDef]
    lessThan: NotRequired[DocumentAttributeOutputTypeDef]
    lessThanOrEquals: NotRequired[DocumentAttributeOutputTypeDef]

DocumentAttributeValueUnionTypeDef = Union[
    DocumentAttributeValueTypeDef, DocumentAttributeValueOutputTypeDef
]
FormInputCardInputTypeDef = TypedDict(
    "FormInputCardInputTypeDef",
    {
        "title": str,
        "id": str,
        "type": CardTypeType,
        "metadata": FormInputCardMetadataUnionTypeDef,
        "computeMode": NotRequired[InputCardComputeModeType],
    },
)

class DescribeQAppPermissionsOutputTypeDef(TypedDict):
    resourceArn: str
    appId: str
    permissions: List[PermissionOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateQAppPermissionsOutputTypeDef(TypedDict):
    resourceArn: str
    appId: str
    permissions: List[PermissionOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListQAppSessionDataOutputTypeDef(TypedDict):
    sessionId: str
    sessionArn: str
    sessionData: List[QAppSessionDataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

QQueryCardInputOutputTypeDef = TypedDict(
    "QQueryCardInputOutputTypeDef",
    {
        "title": str,
        "id": str,
        "type": CardTypeType,
        "prompt": str,
        "outputSource": NotRequired[CardOutputSourceType],
        "attributeFilter": NotRequired[AttributeFilterOutputTypeDef],
    },
)
QQueryCardTypeDef = TypedDict(
    "QQueryCardTypeDef",
    {
        "id": str,
        "title": str,
        "dependencies": List[str],
        "type": CardTypeType,
        "prompt": str,
        "outputSource": CardOutputSourceType,
        "attributeFilter": NotRequired[AttributeFilterOutputTypeDef],
        "memoryReferences": NotRequired[List[str]],
    },
)

class DocumentAttributeTypeDef(TypedDict):
    name: str
    value: DocumentAttributeValueUnionTypeDef

FormInputCardInputUnionTypeDef = Union[FormInputCardInputTypeDef, FormInputCardInputOutputTypeDef]

class CardInputOutputTypeDef(TypedDict):
    textInput: NotRequired[TextInputCardInputTypeDef]
    qQuery: NotRequired[QQueryCardInputOutputTypeDef]
    qPlugin: NotRequired[QPluginCardInputTypeDef]
    fileUpload: NotRequired[FileUploadCardInputTypeDef]
    formInput: NotRequired[FormInputCardInputOutputTypeDef]

class CardTypeDef(TypedDict):
    textInput: NotRequired[TextInputCardTypeDef]
    qQuery: NotRequired[QQueryCardTypeDef]
    qPlugin: NotRequired[QPluginCardTypeDef]
    fileUpload: NotRequired[FileUploadCardTypeDef]
    formInput: NotRequired[FormInputCardTypeDef]

DocumentAttributeUnionTypeDef = Union[DocumentAttributeTypeDef, DocumentAttributeOutputTypeDef]

class AppDefinitionInputOutputTypeDef(TypedDict):
    cards: List[CardInputOutputTypeDef]
    initialPrompt: NotRequired[str]

class AppDefinitionTypeDef(TypedDict):
    appDefinitionVersion: str
    cards: List[CardTypeDef]
    canEdit: NotRequired[bool]

class AttributeFilterTypeDef(TypedDict):
    andAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    orAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    notFilter: NotRequired[Mapping[str, Any]]
    equalsTo: NotRequired[DocumentAttributeUnionTypeDef]
    containsAll: NotRequired[DocumentAttributeUnionTypeDef]
    containsAny: NotRequired[DocumentAttributeUnionTypeDef]
    greaterThan: NotRequired[DocumentAttributeUnionTypeDef]
    greaterThanOrEquals: NotRequired[DocumentAttributeUnionTypeDef]
    lessThan: NotRequired[DocumentAttributeUnionTypeDef]
    lessThanOrEquals: NotRequired[DocumentAttributeUnionTypeDef]

class PredictAppDefinitionTypeDef(TypedDict):
    title: str
    appDefinition: AppDefinitionInputOutputTypeDef
    description: NotRequired[str]

class GetQAppOutputTypeDef(TypedDict):
    appId: str
    appArn: str
    title: str
    description: str
    initialPrompt: str
    appVersion: int
    status: AppStatusType
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    requiredCapabilities: List[AppRequiredCapabilityType]
    appDefinition: AppDefinitionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

AttributeFilterUnionTypeDef = Union[AttributeFilterTypeDef, AttributeFilterOutputTypeDef]

class PredictQAppOutputTypeDef(TypedDict):
    app: PredictAppDefinitionTypeDef
    problemStatement: str
    ResponseMetadata: ResponseMetadataTypeDef

QQueryCardInputTypeDef = TypedDict(
    "QQueryCardInputTypeDef",
    {
        "title": str,
        "id": str,
        "type": CardTypeType,
        "prompt": str,
        "outputSource": NotRequired[CardOutputSourceType],
        "attributeFilter": NotRequired[AttributeFilterUnionTypeDef],
    },
)
QQueryCardInputUnionTypeDef = Union[QQueryCardInputTypeDef, QQueryCardInputOutputTypeDef]

class CardInputTypeDef(TypedDict):
    textInput: NotRequired[TextInputCardInputTypeDef]
    qQuery: NotRequired[QQueryCardInputUnionTypeDef]
    qPlugin: NotRequired[QPluginCardInputTypeDef]
    fileUpload: NotRequired[FileUploadCardInputTypeDef]
    formInput: NotRequired[FormInputCardInputUnionTypeDef]

CardInputUnionTypeDef = Union[CardInputTypeDef, CardInputOutputTypeDef]

class AppDefinitionInputTypeDef(TypedDict):
    cards: Sequence[CardInputUnionTypeDef]
    initialPrompt: NotRequired[str]

class CreateQAppInputRequestTypeDef(TypedDict):
    instanceId: str
    title: str
    appDefinition: AppDefinitionInputTypeDef
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class UpdateQAppInputRequestTypeDef(TypedDict):
    instanceId: str
    appId: str
    title: NotRequired[str]
    description: NotRequired[str]
    appDefinition: NotRequired[AppDefinitionInputTypeDef]
