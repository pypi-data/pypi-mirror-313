"""
Type annotations for identitystore service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/type_defs/)

Usage::

    ```python
    from mypy_boto3_identitystore.type_defs import AddressTypeDef

    data: AddressTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, List, Mapping, Sequence

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AddressTypeDef",
    "AlternateIdentifierTypeDef",
    "AttributeOperationTypeDef",
    "CreateGroupMembershipRequestRequestTypeDef",
    "CreateGroupMembershipResponseTypeDef",
    "CreateGroupRequestRequestTypeDef",
    "CreateGroupResponseTypeDef",
    "CreateUserRequestRequestTypeDef",
    "CreateUserResponseTypeDef",
    "DeleteGroupMembershipRequestRequestTypeDef",
    "DeleteGroupRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DescribeGroupMembershipRequestRequestTypeDef",
    "DescribeGroupMembershipResponseTypeDef",
    "DescribeGroupRequestRequestTypeDef",
    "DescribeGroupResponseTypeDef",
    "DescribeUserRequestRequestTypeDef",
    "DescribeUserResponseTypeDef",
    "EmailTypeDef",
    "ExternalIdTypeDef",
    "FilterTypeDef",
    "GetGroupIdRequestRequestTypeDef",
    "GetGroupIdResponseTypeDef",
    "GetGroupMembershipIdRequestRequestTypeDef",
    "GetGroupMembershipIdResponseTypeDef",
    "GetUserIdRequestRequestTypeDef",
    "GetUserIdResponseTypeDef",
    "GroupMembershipExistenceResultTypeDef",
    "GroupMembershipTypeDef",
    "GroupTypeDef",
    "IsMemberInGroupsRequestRequestTypeDef",
    "IsMemberInGroupsResponseTypeDef",
    "ListGroupMembershipsForMemberRequestListGroupMembershipsForMemberPaginateTypeDef",
    "ListGroupMembershipsForMemberRequestRequestTypeDef",
    "ListGroupMembershipsForMemberResponseTypeDef",
    "ListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef",
    "ListGroupMembershipsRequestRequestTypeDef",
    "ListGroupMembershipsResponseTypeDef",
    "ListGroupsRequestListGroupsPaginateTypeDef",
    "ListGroupsRequestRequestTypeDef",
    "ListGroupsResponseTypeDef",
    "ListUsersRequestListUsersPaginateTypeDef",
    "ListUsersRequestRequestTypeDef",
    "ListUsersResponseTypeDef",
    "MemberIdTypeDef",
    "NameTypeDef",
    "PaginatorConfigTypeDef",
    "PhoneNumberTypeDef",
    "ResponseMetadataTypeDef",
    "UniqueAttributeTypeDef",
    "UpdateGroupRequestRequestTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "UserTypeDef",
)

AddressTypeDef = TypedDict(
    "AddressTypeDef",
    {
        "StreetAddress": NotRequired[str],
        "Locality": NotRequired[str],
        "Region": NotRequired[str],
        "PostalCode": NotRequired[str],
        "Country": NotRequired[str],
        "Formatted": NotRequired[str],
        "Type": NotRequired[str],
        "Primary": NotRequired[bool],
    },
)


class ExternalIdTypeDef(TypedDict):
    Issuer: str
    Id: str


class UniqueAttributeTypeDef(TypedDict):
    AttributePath: str
    AttributeValue: Mapping[str, Any]


class AttributeOperationTypeDef(TypedDict):
    AttributePath: str
    AttributeValue: NotRequired[Mapping[str, Any]]


class MemberIdTypeDef(TypedDict):
    UserId: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateGroupRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    DisplayName: NotRequired[str]
    Description: NotRequired[str]


EmailTypeDef = TypedDict(
    "EmailTypeDef",
    {
        "Value": NotRequired[str],
        "Type": NotRequired[str],
        "Primary": NotRequired[bool],
    },
)


class NameTypeDef(TypedDict):
    Formatted: NotRequired[str]
    FamilyName: NotRequired[str]
    GivenName: NotRequired[str]
    MiddleName: NotRequired[str]
    HonorificPrefix: NotRequired[str]
    HonorificSuffix: NotRequired[str]


PhoneNumberTypeDef = TypedDict(
    "PhoneNumberTypeDef",
    {
        "Value": NotRequired[str],
        "Type": NotRequired[str],
        "Primary": NotRequired[bool],
    },
)


class DeleteGroupMembershipRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    MembershipId: str


class DeleteGroupRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    GroupId: str


class DeleteUserRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    UserId: str


class DescribeGroupMembershipRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    MembershipId: str


class DescribeGroupRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    GroupId: str


class DescribeUserRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    UserId: str


class FilterTypeDef(TypedDict):
    AttributePath: str
    AttributeValue: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListGroupMembershipsRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    GroupId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GroupTypeDef(TypedDict):
    GroupId: str
    IdentityStoreId: str
    DisplayName: NotRequired[str]
    ExternalIds: NotRequired[List[ExternalIdTypeDef]]
    Description: NotRequired[str]


class AlternateIdentifierTypeDef(TypedDict):
    ExternalId: NotRequired[ExternalIdTypeDef]
    UniqueAttribute: NotRequired[UniqueAttributeTypeDef]


class UpdateGroupRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    GroupId: str
    Operations: Sequence[AttributeOperationTypeDef]


class UpdateUserRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    UserId: str
    Operations: Sequence[AttributeOperationTypeDef]


class CreateGroupMembershipRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    GroupId: str
    MemberId: MemberIdTypeDef


class GetGroupMembershipIdRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    GroupId: str
    MemberId: MemberIdTypeDef


class GroupMembershipExistenceResultTypeDef(TypedDict):
    GroupId: NotRequired[str]
    MemberId: NotRequired[MemberIdTypeDef]
    MembershipExists: NotRequired[bool]


class GroupMembershipTypeDef(TypedDict):
    IdentityStoreId: str
    MembershipId: NotRequired[str]
    GroupId: NotRequired[str]
    MemberId: NotRequired[MemberIdTypeDef]


class IsMemberInGroupsRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    MemberId: MemberIdTypeDef
    GroupIds: Sequence[str]


class ListGroupMembershipsForMemberRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    MemberId: MemberIdTypeDef
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class CreateGroupMembershipResponseTypeDef(TypedDict):
    MembershipId: str
    IdentityStoreId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateGroupResponseTypeDef(TypedDict):
    GroupId: str
    IdentityStoreId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUserResponseTypeDef(TypedDict):
    UserId: str
    IdentityStoreId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeGroupMembershipResponseTypeDef(TypedDict):
    IdentityStoreId: str
    MembershipId: str
    GroupId: str
    MemberId: MemberIdTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeGroupResponseTypeDef(TypedDict):
    GroupId: str
    DisplayName: str
    ExternalIds: List[ExternalIdTypeDef]
    Description: str
    IdentityStoreId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetGroupIdResponseTypeDef(TypedDict):
    GroupId: str
    IdentityStoreId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetGroupMembershipIdResponseTypeDef(TypedDict):
    MembershipId: str
    IdentityStoreId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetUserIdResponseTypeDef(TypedDict):
    UserId: str
    IdentityStoreId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUserRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    UserName: NotRequired[str]
    Name: NotRequired[NameTypeDef]
    DisplayName: NotRequired[str]
    NickName: NotRequired[str]
    ProfileUrl: NotRequired[str]
    Emails: NotRequired[Sequence[EmailTypeDef]]
    Addresses: NotRequired[Sequence[AddressTypeDef]]
    PhoneNumbers: NotRequired[Sequence[PhoneNumberTypeDef]]
    UserType: NotRequired[str]
    Title: NotRequired[str]
    PreferredLanguage: NotRequired[str]
    Locale: NotRequired[str]
    Timezone: NotRequired[str]


class DescribeUserResponseTypeDef(TypedDict):
    UserName: str
    UserId: str
    ExternalIds: List[ExternalIdTypeDef]
    Name: NameTypeDef
    DisplayName: str
    NickName: str
    ProfileUrl: str
    Emails: List[EmailTypeDef]
    Addresses: List[AddressTypeDef]
    PhoneNumbers: List[PhoneNumberTypeDef]
    UserType: str
    Title: str
    PreferredLanguage: str
    Locale: str
    Timezone: str
    IdentityStoreId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UserTypeDef(TypedDict):
    UserId: str
    IdentityStoreId: str
    UserName: NotRequired[str]
    ExternalIds: NotRequired[List[ExternalIdTypeDef]]
    Name: NotRequired[NameTypeDef]
    DisplayName: NotRequired[str]
    NickName: NotRequired[str]
    ProfileUrl: NotRequired[str]
    Emails: NotRequired[List[EmailTypeDef]]
    Addresses: NotRequired[List[AddressTypeDef]]
    PhoneNumbers: NotRequired[List[PhoneNumberTypeDef]]
    UserType: NotRequired[str]
    Title: NotRequired[str]
    PreferredLanguage: NotRequired[str]
    Locale: NotRequired[str]
    Timezone: NotRequired[str]


class ListGroupsRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class ListUsersRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class ListGroupMembershipsForMemberRequestListGroupMembershipsForMemberPaginateTypeDef(TypedDict):
    IdentityStoreId: str
    MemberId: MemberIdTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef(TypedDict):
    IdentityStoreId: str
    GroupId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupsRequestListGroupsPaginateTypeDef(TypedDict):
    IdentityStoreId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUsersRequestListUsersPaginateTypeDef(TypedDict):
    IdentityStoreId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupsResponseTypeDef(TypedDict):
    Groups: List[GroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetGroupIdRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    AlternateIdentifier: AlternateIdentifierTypeDef


class GetUserIdRequestRequestTypeDef(TypedDict):
    IdentityStoreId: str
    AlternateIdentifier: AlternateIdentifierTypeDef


class IsMemberInGroupsResponseTypeDef(TypedDict):
    Results: List[GroupMembershipExistenceResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListGroupMembershipsForMemberResponseTypeDef(TypedDict):
    GroupMemberships: List[GroupMembershipTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListGroupMembershipsResponseTypeDef(TypedDict):
    GroupMemberships: List[GroupMembershipTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListUsersResponseTypeDef(TypedDict):
    Users: List[UserTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
