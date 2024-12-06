"""
Type annotations for workdocs service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/type_defs/)

Usage::

    ```python
    from mypy_boto3_workdocs.type_defs import AbortDocumentVersionUploadRequestRequestTypeDef

    data: AbortDocumentVersionUploadRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ActivityTypeType,
    BooleanEnumTypeType,
    CommentStatusTypeType,
    CommentVisibilityTypeType,
    ContentCategoryTypeType,
    DocumentSourceTypeType,
    DocumentStatusTypeType,
    DocumentThumbnailTypeType,
    FolderContentTypeType,
    LanguageCodeTypeType,
    LocaleTypeType,
    OrderByFieldTypeType,
    OrderTypeType,
    PrincipalRoleTypeType,
    PrincipalTypeType,
    ResourceSortTypeType,
    ResourceStateTypeType,
    ResourceTypeType,
    ResponseItemTypeType,
    RolePermissionTypeType,
    RoleTypeType,
    SearchCollectionTypeType,
    SearchQueryScopeTypeType,
    SearchResourceTypeType,
    ShareStatusTypeType,
    SortOrderType,
    StorageTypeType,
    SubscriptionProtocolTypeType,
    UserFilterTypeType,
    UserSortTypeType,
    UserStatusTypeType,
    UserTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AbortDocumentVersionUploadRequestRequestTypeDef",
    "ActivateUserRequestRequestTypeDef",
    "ActivateUserResponseTypeDef",
    "ActivityTypeDef",
    "AddResourcePermissionsRequestRequestTypeDef",
    "AddResourcePermissionsResponseTypeDef",
    "CommentMetadataTypeDef",
    "CommentTypeDef",
    "CreateCommentRequestRequestTypeDef",
    "CreateCommentResponseTypeDef",
    "CreateCustomMetadataRequestRequestTypeDef",
    "CreateFolderRequestRequestTypeDef",
    "CreateFolderResponseTypeDef",
    "CreateLabelsRequestRequestTypeDef",
    "CreateNotificationSubscriptionRequestRequestTypeDef",
    "CreateNotificationSubscriptionResponseTypeDef",
    "CreateUserRequestRequestTypeDef",
    "CreateUserResponseTypeDef",
    "DateRangeTypeTypeDef",
    "DeactivateUserRequestRequestTypeDef",
    "DeleteCommentRequestRequestTypeDef",
    "DeleteCustomMetadataRequestRequestTypeDef",
    "DeleteDocumentRequestRequestTypeDef",
    "DeleteDocumentVersionRequestRequestTypeDef",
    "DeleteFolderContentsRequestRequestTypeDef",
    "DeleteFolderRequestRequestTypeDef",
    "DeleteLabelsRequestRequestTypeDef",
    "DeleteNotificationSubscriptionRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DescribeActivitiesRequestDescribeActivitiesPaginateTypeDef",
    "DescribeActivitiesRequestRequestTypeDef",
    "DescribeActivitiesResponseTypeDef",
    "DescribeCommentsRequestDescribeCommentsPaginateTypeDef",
    "DescribeCommentsRequestRequestTypeDef",
    "DescribeCommentsResponseTypeDef",
    "DescribeDocumentVersionsRequestDescribeDocumentVersionsPaginateTypeDef",
    "DescribeDocumentVersionsRequestRequestTypeDef",
    "DescribeDocumentVersionsResponseTypeDef",
    "DescribeFolderContentsRequestDescribeFolderContentsPaginateTypeDef",
    "DescribeFolderContentsRequestRequestTypeDef",
    "DescribeFolderContentsResponseTypeDef",
    "DescribeGroupsRequestDescribeGroupsPaginateTypeDef",
    "DescribeGroupsRequestRequestTypeDef",
    "DescribeGroupsResponseTypeDef",
    "DescribeNotificationSubscriptionsRequestDescribeNotificationSubscriptionsPaginateTypeDef",
    "DescribeNotificationSubscriptionsRequestRequestTypeDef",
    "DescribeNotificationSubscriptionsResponseTypeDef",
    "DescribeResourcePermissionsRequestDescribeResourcePermissionsPaginateTypeDef",
    "DescribeResourcePermissionsRequestRequestTypeDef",
    "DescribeResourcePermissionsResponseTypeDef",
    "DescribeRootFoldersRequestDescribeRootFoldersPaginateTypeDef",
    "DescribeRootFoldersRequestRequestTypeDef",
    "DescribeRootFoldersResponseTypeDef",
    "DescribeUsersRequestDescribeUsersPaginateTypeDef",
    "DescribeUsersRequestRequestTypeDef",
    "DescribeUsersResponseTypeDef",
    "DocumentMetadataTypeDef",
    "DocumentVersionMetadataTypeDef",
    "EmptyResponseMetadataTypeDef",
    "FiltersTypeDef",
    "FolderMetadataTypeDef",
    "GetCurrentUserRequestRequestTypeDef",
    "GetCurrentUserResponseTypeDef",
    "GetDocumentPathRequestRequestTypeDef",
    "GetDocumentPathResponseTypeDef",
    "GetDocumentRequestRequestTypeDef",
    "GetDocumentResponseTypeDef",
    "GetDocumentVersionRequestRequestTypeDef",
    "GetDocumentVersionResponseTypeDef",
    "GetFolderPathRequestRequestTypeDef",
    "GetFolderPathResponseTypeDef",
    "GetFolderRequestRequestTypeDef",
    "GetFolderResponseTypeDef",
    "GetResourcesRequestRequestTypeDef",
    "GetResourcesResponseTypeDef",
    "GroupMetadataTypeDef",
    "InitiateDocumentVersionUploadRequestRequestTypeDef",
    "InitiateDocumentVersionUploadResponseTypeDef",
    "LongRangeTypeTypeDef",
    "NotificationOptionsTypeDef",
    "PaginatorConfigTypeDef",
    "ParticipantsTypeDef",
    "PermissionInfoTypeDef",
    "PrincipalTypeDef",
    "RemoveAllResourcePermissionsRequestRequestTypeDef",
    "RemoveResourcePermissionRequestRequestTypeDef",
    "ResourceMetadataTypeDef",
    "ResourcePathComponentTypeDef",
    "ResourcePathTypeDef",
    "ResponseItemTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreDocumentVersionsRequestRequestTypeDef",
    "SearchPrincipalTypeTypeDef",
    "SearchResourcesRequestRequestTypeDef",
    "SearchResourcesRequestSearchResourcesPaginateTypeDef",
    "SearchResourcesResponseTypeDef",
    "SearchSortResultTypeDef",
    "SharePrincipalTypeDef",
    "ShareResultTypeDef",
    "StorageRuleTypeTypeDef",
    "SubscriptionTypeDef",
    "TimestampTypeDef",
    "UpdateDocumentRequestRequestTypeDef",
    "UpdateDocumentVersionRequestRequestTypeDef",
    "UpdateFolderRequestRequestTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "UpdateUserResponseTypeDef",
    "UploadMetadataTypeDef",
    "UserMetadataTypeDef",
    "UserStorageMetadataTypeDef",
    "UserTypeDef",
)

class AbortDocumentVersionUploadRequestRequestTypeDef(TypedDict):
    DocumentId: str
    VersionId: str
    AuthenticationToken: NotRequired[str]

class ActivateUserRequestRequestTypeDef(TypedDict):
    UserId: str
    AuthenticationToken: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class UserMetadataTypeDef(TypedDict):
    Id: NotRequired[str]
    Username: NotRequired[str]
    GivenName: NotRequired[str]
    Surname: NotRequired[str]
    EmailAddress: NotRequired[str]

class NotificationOptionsTypeDef(TypedDict):
    SendEmail: NotRequired[bool]
    EmailMessage: NotRequired[str]

SharePrincipalTypeDef = TypedDict(
    "SharePrincipalTypeDef",
    {
        "Id": str,
        "Type": PrincipalTypeType,
        "Role": RoleTypeType,
    },
)

class ShareResultTypeDef(TypedDict):
    PrincipalId: NotRequired[str]
    InviteePrincipalId: NotRequired[str]
    Role: NotRequired[RoleTypeType]
    Status: NotRequired[ShareStatusTypeType]
    ShareId: NotRequired[str]
    StatusMessage: NotRequired[str]

CreateCommentRequestRequestTypeDef = TypedDict(
    "CreateCommentRequestRequestTypeDef",
    {
        "DocumentId": str,
        "VersionId": str,
        "Text": str,
        "AuthenticationToken": NotRequired[str],
        "ParentId": NotRequired[str],
        "ThreadId": NotRequired[str],
        "Visibility": NotRequired[CommentVisibilityTypeType],
        "NotifyCollaborators": NotRequired[bool],
    },
)

class CreateCustomMetadataRequestRequestTypeDef(TypedDict):
    ResourceId: str
    CustomMetadata: Mapping[str, str]
    AuthenticationToken: NotRequired[str]
    VersionId: NotRequired[str]

class CreateFolderRequestRequestTypeDef(TypedDict):
    ParentFolderId: str
    AuthenticationToken: NotRequired[str]
    Name: NotRequired[str]

class FolderMetadataTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    CreatorId: NotRequired[str]
    ParentFolderId: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]
    ModifiedTimestamp: NotRequired[datetime]
    ResourceState: NotRequired[ResourceStateTypeType]
    Signature: NotRequired[str]
    Labels: NotRequired[List[str]]
    Size: NotRequired[int]
    LatestVersionSize: NotRequired[int]

class CreateLabelsRequestRequestTypeDef(TypedDict):
    ResourceId: str
    Labels: Sequence[str]
    AuthenticationToken: NotRequired[str]

CreateNotificationSubscriptionRequestRequestTypeDef = TypedDict(
    "CreateNotificationSubscriptionRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "Endpoint": str,
        "Protocol": SubscriptionProtocolTypeType,
        "SubscriptionType": Literal["ALL"],
    },
)
SubscriptionTypeDef = TypedDict(
    "SubscriptionTypeDef",
    {
        "SubscriptionId": NotRequired[str],
        "EndPoint": NotRequired[str],
        "Protocol": NotRequired[SubscriptionProtocolTypeType],
    },
)

class StorageRuleTypeTypeDef(TypedDict):
    StorageAllocatedInBytes: NotRequired[int]
    StorageType: NotRequired[StorageTypeType]

TimestampTypeDef = Union[datetime, str]

class DeactivateUserRequestRequestTypeDef(TypedDict):
    UserId: str
    AuthenticationToken: NotRequired[str]

class DeleteCommentRequestRequestTypeDef(TypedDict):
    DocumentId: str
    VersionId: str
    CommentId: str
    AuthenticationToken: NotRequired[str]

class DeleteCustomMetadataRequestRequestTypeDef(TypedDict):
    ResourceId: str
    AuthenticationToken: NotRequired[str]
    VersionId: NotRequired[str]
    Keys: NotRequired[Sequence[str]]
    DeleteAll: NotRequired[bool]

class DeleteDocumentRequestRequestTypeDef(TypedDict):
    DocumentId: str
    AuthenticationToken: NotRequired[str]

class DeleteDocumentVersionRequestRequestTypeDef(TypedDict):
    DocumentId: str
    VersionId: str
    DeletePriorVersions: bool
    AuthenticationToken: NotRequired[str]

class DeleteFolderContentsRequestRequestTypeDef(TypedDict):
    FolderId: str
    AuthenticationToken: NotRequired[str]

class DeleteFolderRequestRequestTypeDef(TypedDict):
    FolderId: str
    AuthenticationToken: NotRequired[str]

class DeleteLabelsRequestRequestTypeDef(TypedDict):
    ResourceId: str
    AuthenticationToken: NotRequired[str]
    Labels: NotRequired[Sequence[str]]
    DeleteAll: NotRequired[bool]

class DeleteNotificationSubscriptionRequestRequestTypeDef(TypedDict):
    SubscriptionId: str
    OrganizationId: str

class DeleteUserRequestRequestTypeDef(TypedDict):
    UserId: str
    AuthenticationToken: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeCommentsRequestRequestTypeDef(TypedDict):
    DocumentId: str
    VersionId: str
    AuthenticationToken: NotRequired[str]
    Limit: NotRequired[int]
    Marker: NotRequired[str]

class DescribeDocumentVersionsRequestRequestTypeDef(TypedDict):
    DocumentId: str
    AuthenticationToken: NotRequired[str]
    Marker: NotRequired[str]
    Limit: NotRequired[int]
    Include: NotRequired[str]
    Fields: NotRequired[str]

class DocumentVersionMetadataTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    ContentType: NotRequired[str]
    Size: NotRequired[int]
    Signature: NotRequired[str]
    Status: NotRequired[DocumentStatusTypeType]
    CreatedTimestamp: NotRequired[datetime]
    ModifiedTimestamp: NotRequired[datetime]
    ContentCreatedTimestamp: NotRequired[datetime]
    ContentModifiedTimestamp: NotRequired[datetime]
    CreatorId: NotRequired[str]
    Thumbnail: NotRequired[Dict[DocumentThumbnailTypeType, str]]
    Source: NotRequired[Dict[DocumentSourceTypeType, str]]

DescribeFolderContentsRequestRequestTypeDef = TypedDict(
    "DescribeFolderContentsRequestRequestTypeDef",
    {
        "FolderId": str,
        "AuthenticationToken": NotRequired[str],
        "Sort": NotRequired[ResourceSortTypeType],
        "Order": NotRequired[OrderTypeType],
        "Limit": NotRequired[int],
        "Marker": NotRequired[str],
        "Type": NotRequired[FolderContentTypeType],
        "Include": NotRequired[str],
    },
)

class DescribeGroupsRequestRequestTypeDef(TypedDict):
    SearchQuery: str
    AuthenticationToken: NotRequired[str]
    OrganizationId: NotRequired[str]
    Marker: NotRequired[str]
    Limit: NotRequired[int]

class GroupMetadataTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]

class DescribeNotificationSubscriptionsRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    Marker: NotRequired[str]
    Limit: NotRequired[int]

class DescribeResourcePermissionsRequestRequestTypeDef(TypedDict):
    ResourceId: str
    AuthenticationToken: NotRequired[str]
    PrincipalId: NotRequired[str]
    Limit: NotRequired[int]
    Marker: NotRequired[str]

class DescribeRootFoldersRequestRequestTypeDef(TypedDict):
    AuthenticationToken: str
    Limit: NotRequired[int]
    Marker: NotRequired[str]

class DescribeUsersRequestRequestTypeDef(TypedDict):
    AuthenticationToken: NotRequired[str]
    OrganizationId: NotRequired[str]
    UserIds: NotRequired[str]
    Query: NotRequired[str]
    Include: NotRequired[UserFilterTypeType]
    Order: NotRequired[OrderTypeType]
    Sort: NotRequired[UserSortTypeType]
    Marker: NotRequired[str]
    Limit: NotRequired[int]
    Fields: NotRequired[str]

class LongRangeTypeTypeDef(TypedDict):
    StartValue: NotRequired[int]
    EndValue: NotRequired[int]

class SearchPrincipalTypeTypeDef(TypedDict):
    Id: str
    Roles: NotRequired[Sequence[PrincipalRoleTypeType]]

class GetCurrentUserRequestRequestTypeDef(TypedDict):
    AuthenticationToken: str

class GetDocumentPathRequestRequestTypeDef(TypedDict):
    DocumentId: str
    AuthenticationToken: NotRequired[str]
    Limit: NotRequired[int]
    Fields: NotRequired[str]
    Marker: NotRequired[str]

class GetDocumentRequestRequestTypeDef(TypedDict):
    DocumentId: str
    AuthenticationToken: NotRequired[str]
    IncludeCustomMetadata: NotRequired[bool]

class GetDocumentVersionRequestRequestTypeDef(TypedDict):
    DocumentId: str
    VersionId: str
    AuthenticationToken: NotRequired[str]
    Fields: NotRequired[str]
    IncludeCustomMetadata: NotRequired[bool]

class GetFolderPathRequestRequestTypeDef(TypedDict):
    FolderId: str
    AuthenticationToken: NotRequired[str]
    Limit: NotRequired[int]
    Fields: NotRequired[str]
    Marker: NotRequired[str]

class GetFolderRequestRequestTypeDef(TypedDict):
    FolderId: str
    AuthenticationToken: NotRequired[str]
    IncludeCustomMetadata: NotRequired[bool]

class GetResourcesRequestRequestTypeDef(TypedDict):
    AuthenticationToken: NotRequired[str]
    UserId: NotRequired[str]
    CollectionType: NotRequired[Literal["SHARED_WITH_ME"]]
    Limit: NotRequired[int]
    Marker: NotRequired[str]

class UploadMetadataTypeDef(TypedDict):
    UploadUrl: NotRequired[str]
    SignedHeaders: NotRequired[Dict[str, str]]

PermissionInfoTypeDef = TypedDict(
    "PermissionInfoTypeDef",
    {
        "Role": NotRequired[RoleTypeType],
        "Type": NotRequired[RolePermissionTypeType],
    },
)

class RemoveAllResourcePermissionsRequestRequestTypeDef(TypedDict):
    ResourceId: str
    AuthenticationToken: NotRequired[str]

class RemoveResourcePermissionRequestRequestTypeDef(TypedDict):
    ResourceId: str
    PrincipalId: str
    AuthenticationToken: NotRequired[str]
    PrincipalType: NotRequired[PrincipalTypeType]

class ResourcePathComponentTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]

class RestoreDocumentVersionsRequestRequestTypeDef(TypedDict):
    DocumentId: str
    AuthenticationToken: NotRequired[str]

class SearchSortResultTypeDef(TypedDict):
    Field: NotRequired[OrderByFieldTypeType]
    Order: NotRequired[SortOrderType]

class UpdateDocumentRequestRequestTypeDef(TypedDict):
    DocumentId: str
    AuthenticationToken: NotRequired[str]
    Name: NotRequired[str]
    ParentFolderId: NotRequired[str]
    ResourceState: NotRequired[ResourceStateTypeType]

class UpdateDocumentVersionRequestRequestTypeDef(TypedDict):
    DocumentId: str
    VersionId: str
    AuthenticationToken: NotRequired[str]
    VersionStatus: NotRequired[Literal["ACTIVE"]]

class UpdateFolderRequestRequestTypeDef(TypedDict):
    FolderId: str
    AuthenticationToken: NotRequired[str]
    Name: NotRequired[str]
    ParentFolderId: NotRequired[str]
    ResourceState: NotRequired[ResourceStateTypeType]

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

ResourceMetadataTypeDef = TypedDict(
    "ResourceMetadataTypeDef",
    {
        "Type": NotRequired[ResourceTypeType],
        "Name": NotRequired[str],
        "OriginalName": NotRequired[str],
        "Id": NotRequired[str],
        "VersionId": NotRequired[str],
        "Owner": NotRequired[UserMetadataTypeDef],
        "ParentId": NotRequired[str],
    },
)

class AddResourcePermissionsRequestRequestTypeDef(TypedDict):
    ResourceId: str
    Principals: Sequence[SharePrincipalTypeDef]
    AuthenticationToken: NotRequired[str]
    NotificationOptions: NotRequired[NotificationOptionsTypeDef]

class AddResourcePermissionsResponseTypeDef(TypedDict):
    ShareResults: List[ShareResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFolderResponseTypeDef(TypedDict):
    Metadata: FolderMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeRootFoldersResponseTypeDef(TypedDict):
    Folders: List[FolderMetadataTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetFolderResponseTypeDef(TypedDict):
    Metadata: FolderMetadataTypeDef
    CustomMetadata: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateNotificationSubscriptionResponseTypeDef(TypedDict):
    Subscription: SubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeNotificationSubscriptionsResponseTypeDef(TypedDict):
    Subscriptions: List[SubscriptionTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateUserRequestRequestTypeDef(TypedDict):
    Username: str
    GivenName: str
    Surname: str
    Password: str
    OrganizationId: NotRequired[str]
    EmailAddress: NotRequired[str]
    TimeZoneId: NotRequired[str]
    StorageRule: NotRequired[StorageRuleTypeTypeDef]
    AuthenticationToken: NotRequired[str]

UpdateUserRequestRequestTypeDef = TypedDict(
    "UpdateUserRequestRequestTypeDef",
    {
        "UserId": str,
        "AuthenticationToken": NotRequired[str],
        "GivenName": NotRequired[str],
        "Surname": NotRequired[str],
        "Type": NotRequired[UserTypeType],
        "StorageRule": NotRequired[StorageRuleTypeTypeDef],
        "TimeZoneId": NotRequired[str],
        "Locale": NotRequired[LocaleTypeType],
        "GrantPoweruserPrivileges": NotRequired[BooleanEnumTypeType],
    },
)

class UserStorageMetadataTypeDef(TypedDict):
    StorageUtilizedInBytes: NotRequired[int]
    StorageRule: NotRequired[StorageRuleTypeTypeDef]

class DateRangeTypeTypeDef(TypedDict):
    StartValue: NotRequired[TimestampTypeDef]
    EndValue: NotRequired[TimestampTypeDef]

class DescribeActivitiesRequestRequestTypeDef(TypedDict):
    AuthenticationToken: NotRequired[str]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    OrganizationId: NotRequired[str]
    ActivityTypes: NotRequired[str]
    ResourceId: NotRequired[str]
    UserId: NotRequired[str]
    IncludeIndirectActivities: NotRequired[bool]
    Limit: NotRequired[int]
    Marker: NotRequired[str]

class InitiateDocumentVersionUploadRequestRequestTypeDef(TypedDict):
    AuthenticationToken: NotRequired[str]
    Id: NotRequired[str]
    Name: NotRequired[str]
    ContentCreatedTimestamp: NotRequired[TimestampTypeDef]
    ContentModifiedTimestamp: NotRequired[TimestampTypeDef]
    ContentType: NotRequired[str]
    DocumentSizeInBytes: NotRequired[int]
    ParentFolderId: NotRequired[str]

class DescribeActivitiesRequestDescribeActivitiesPaginateTypeDef(TypedDict):
    AuthenticationToken: NotRequired[str]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    OrganizationId: NotRequired[str]
    ActivityTypes: NotRequired[str]
    ResourceId: NotRequired[str]
    UserId: NotRequired[str]
    IncludeIndirectActivities: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeCommentsRequestDescribeCommentsPaginateTypeDef(TypedDict):
    DocumentId: str
    VersionId: str
    AuthenticationToken: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeDocumentVersionsRequestDescribeDocumentVersionsPaginateTypeDef(TypedDict):
    DocumentId: str
    AuthenticationToken: NotRequired[str]
    Include: NotRequired[str]
    Fields: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

DescribeFolderContentsRequestDescribeFolderContentsPaginateTypeDef = TypedDict(
    "DescribeFolderContentsRequestDescribeFolderContentsPaginateTypeDef",
    {
        "FolderId": str,
        "AuthenticationToken": NotRequired[str],
        "Sort": NotRequired[ResourceSortTypeType],
        "Order": NotRequired[OrderTypeType],
        "Type": NotRequired[FolderContentTypeType],
        "Include": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class DescribeGroupsRequestDescribeGroupsPaginateTypeDef(TypedDict):
    SearchQuery: str
    AuthenticationToken: NotRequired[str]
    OrganizationId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeNotificationSubscriptionsRequestDescribeNotificationSubscriptionsPaginateTypeDef(
    TypedDict
):
    OrganizationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeResourcePermissionsRequestDescribeResourcePermissionsPaginateTypeDef(TypedDict):
    ResourceId: str
    AuthenticationToken: NotRequired[str]
    PrincipalId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeRootFoldersRequestDescribeRootFoldersPaginateTypeDef(TypedDict):
    AuthenticationToken: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeUsersRequestDescribeUsersPaginateTypeDef(TypedDict):
    AuthenticationToken: NotRequired[str]
    OrganizationId: NotRequired[str]
    UserIds: NotRequired[str]
    Query: NotRequired[str]
    Include: NotRequired[UserFilterTypeType]
    Order: NotRequired[OrderTypeType]
    Sort: NotRequired[UserSortTypeType]
    Fields: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeDocumentVersionsResponseTypeDef(TypedDict):
    DocumentVersions: List[DocumentVersionMetadataTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class DocumentMetadataTypeDef(TypedDict):
    Id: NotRequired[str]
    CreatorId: NotRequired[str]
    ParentFolderId: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]
    ModifiedTimestamp: NotRequired[datetime]
    LatestVersionMetadata: NotRequired[DocumentVersionMetadataTypeDef]
    ResourceState: NotRequired[ResourceStateTypeType]
    Labels: NotRequired[List[str]]

class GetDocumentVersionResponseTypeDef(TypedDict):
    Metadata: DocumentVersionMetadataTypeDef
    CustomMetadata: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeGroupsResponseTypeDef(TypedDict):
    Groups: List[GroupMetadataTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class ParticipantsTypeDef(TypedDict):
    Users: NotRequired[List[UserMetadataTypeDef]]
    Groups: NotRequired[List[GroupMetadataTypeDef]]

PrincipalTypeDef = TypedDict(
    "PrincipalTypeDef",
    {
        "Id": NotRequired[str],
        "Type": NotRequired[PrincipalTypeType],
        "Roles": NotRequired[List[PermissionInfoTypeDef]],
    },
)

class ResourcePathTypeDef(TypedDict):
    Components: NotRequired[List[ResourcePathComponentTypeDef]]

UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "Id": NotRequired[str],
        "Username": NotRequired[str],
        "EmailAddress": NotRequired[str],
        "GivenName": NotRequired[str],
        "Surname": NotRequired[str],
        "OrganizationId": NotRequired[str],
        "RootFolderId": NotRequired[str],
        "RecycleBinFolderId": NotRequired[str],
        "Status": NotRequired[UserStatusTypeType],
        "Type": NotRequired[UserTypeType],
        "CreatedTimestamp": NotRequired[datetime],
        "ModifiedTimestamp": NotRequired[datetime],
        "TimeZoneId": NotRequired[str],
        "Locale": NotRequired[LocaleTypeType],
        "Storage": NotRequired[UserStorageMetadataTypeDef],
    },
)

class FiltersTypeDef(TypedDict):
    TextLocales: NotRequired[Sequence[LanguageCodeTypeType]]
    ContentCategories: NotRequired[Sequence[ContentCategoryTypeType]]
    ResourceTypes: NotRequired[Sequence[SearchResourceTypeType]]
    Labels: NotRequired[Sequence[str]]
    Principals: NotRequired[Sequence[SearchPrincipalTypeTypeDef]]
    AncestorIds: NotRequired[Sequence[str]]
    SearchCollectionTypes: NotRequired[Sequence[SearchCollectionTypeType]]
    SizeRange: NotRequired[LongRangeTypeTypeDef]
    CreatedRange: NotRequired[DateRangeTypeTypeDef]
    ModifiedRange: NotRequired[DateRangeTypeTypeDef]

class DescribeFolderContentsResponseTypeDef(TypedDict):
    Folders: List[FolderMetadataTypeDef]
    Documents: List[DocumentMetadataTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetDocumentResponseTypeDef(TypedDict):
    Metadata: DocumentMetadataTypeDef
    CustomMetadata: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourcesResponseTypeDef(TypedDict):
    Folders: List[FolderMetadataTypeDef]
    Documents: List[DocumentMetadataTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class InitiateDocumentVersionUploadResponseTypeDef(TypedDict):
    Metadata: DocumentMetadataTypeDef
    UploadMetadata: UploadMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeResourcePermissionsResponseTypeDef(TypedDict):
    Principals: List[PrincipalTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetDocumentPathResponseTypeDef(TypedDict):
    Path: ResourcePathTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetFolderPathResponseTypeDef(TypedDict):
    Path: ResourcePathTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ActivateUserResponseTypeDef(TypedDict):
    User: UserTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CommentMetadataTypeDef(TypedDict):
    CommentId: NotRequired[str]
    Contributor: NotRequired[UserTypeDef]
    CreatedTimestamp: NotRequired[datetime]
    CommentStatus: NotRequired[CommentStatusTypeType]
    RecipientId: NotRequired[str]
    ContributorId: NotRequired[str]

CommentTypeDef = TypedDict(
    "CommentTypeDef",
    {
        "CommentId": str,
        "ParentId": NotRequired[str],
        "ThreadId": NotRequired[str],
        "Text": NotRequired[str],
        "Contributor": NotRequired[UserTypeDef],
        "CreatedTimestamp": NotRequired[datetime],
        "Status": NotRequired[CommentStatusTypeType],
        "Visibility": NotRequired[CommentVisibilityTypeType],
        "RecipientId": NotRequired[str],
    },
)

class CreateUserResponseTypeDef(TypedDict):
    User: UserTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeUsersResponseTypeDef(TypedDict):
    Users: List[UserTypeDef]
    TotalNumberOfUsers: int
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetCurrentUserResponseTypeDef(TypedDict):
    User: UserTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateUserResponseTypeDef(TypedDict):
    User: UserTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SearchResourcesRequestRequestTypeDef(TypedDict):
    AuthenticationToken: NotRequired[str]
    QueryText: NotRequired[str]
    QueryScopes: NotRequired[Sequence[SearchQueryScopeTypeType]]
    OrganizationId: NotRequired[str]
    AdditionalResponseFields: NotRequired[Sequence[Literal["WEBURL"]]]
    Filters: NotRequired[FiltersTypeDef]
    OrderBy: NotRequired[Sequence[SearchSortResultTypeDef]]
    Limit: NotRequired[int]
    Marker: NotRequired[str]

class SearchResourcesRequestSearchResourcesPaginateTypeDef(TypedDict):
    AuthenticationToken: NotRequired[str]
    QueryText: NotRequired[str]
    QueryScopes: NotRequired[Sequence[SearchQueryScopeTypeType]]
    OrganizationId: NotRequired[str]
    AdditionalResponseFields: NotRequired[Sequence[Literal["WEBURL"]]]
    Filters: NotRequired[FiltersTypeDef]
    OrderBy: NotRequired[Sequence[SearchSortResultTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ActivityTypeDef = TypedDict(
    "ActivityTypeDef",
    {
        "Type": NotRequired[ActivityTypeType],
        "TimeStamp": NotRequired[datetime],
        "IsIndirectActivity": NotRequired[bool],
        "OrganizationId": NotRequired[str],
        "Initiator": NotRequired[UserMetadataTypeDef],
        "Participants": NotRequired[ParticipantsTypeDef],
        "ResourceMetadata": NotRequired[ResourceMetadataTypeDef],
        "OriginalParent": NotRequired[ResourceMetadataTypeDef],
        "CommentMetadata": NotRequired[CommentMetadataTypeDef],
    },
)

class ResponseItemTypeDef(TypedDict):
    ResourceType: NotRequired[ResponseItemTypeType]
    WebUrl: NotRequired[str]
    DocumentMetadata: NotRequired[DocumentMetadataTypeDef]
    FolderMetadata: NotRequired[FolderMetadataTypeDef]
    CommentMetadata: NotRequired[CommentMetadataTypeDef]
    DocumentVersionMetadata: NotRequired[DocumentVersionMetadataTypeDef]

class CreateCommentResponseTypeDef(TypedDict):
    Comment: CommentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeCommentsResponseTypeDef(TypedDict):
    Comments: List[CommentTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeActivitiesResponseTypeDef(TypedDict):
    UserActivities: List[ActivityTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class SearchResourcesResponseTypeDef(TypedDict):
    Items: List[ResponseItemTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef
