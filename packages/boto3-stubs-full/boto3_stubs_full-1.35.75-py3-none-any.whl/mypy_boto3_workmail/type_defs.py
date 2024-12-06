"""
Type annotations for workmail service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workmail/type_defs/)

Usage::

    ```python
    from mypy_boto3_workmail.type_defs import AccessControlRuleTypeDef

    data: AccessControlRuleTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AccessControlRuleEffectType,
    AccessEffectType,
    AvailabilityProviderTypeType,
    DnsRecordVerificationStatusType,
    EntityStateType,
    EntityTypeType,
    FolderNameType,
    IdentityProviderAuthenticationModeType,
    ImpersonationRoleTypeType,
    MailboxExportJobStateType,
    MemberTypeType,
    MobileDeviceAccessRuleEffectType,
    PermissionTypeType,
    PersonalAccessTokenConfigurationStatusType,
    ResourceTypeType,
    RetentionActionType,
    UserRoleType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AccessControlRuleTypeDef",
    "AssociateDelegateToResourceRequestRequestTypeDef",
    "AssociateMemberToGroupRequestRequestTypeDef",
    "AssumeImpersonationRoleRequestRequestTypeDef",
    "AssumeImpersonationRoleResponseTypeDef",
    "AvailabilityConfigurationTypeDef",
    "BookingOptionsTypeDef",
    "CancelMailboxExportJobRequestRequestTypeDef",
    "CreateAliasRequestRequestTypeDef",
    "CreateAvailabilityConfigurationRequestRequestTypeDef",
    "CreateGroupRequestRequestTypeDef",
    "CreateGroupResponseTypeDef",
    "CreateIdentityCenterApplicationRequestRequestTypeDef",
    "CreateIdentityCenterApplicationResponseTypeDef",
    "CreateImpersonationRoleRequestRequestTypeDef",
    "CreateImpersonationRoleResponseTypeDef",
    "CreateMobileDeviceAccessRuleRequestRequestTypeDef",
    "CreateMobileDeviceAccessRuleResponseTypeDef",
    "CreateOrganizationRequestRequestTypeDef",
    "CreateOrganizationResponseTypeDef",
    "CreateResourceRequestRequestTypeDef",
    "CreateResourceResponseTypeDef",
    "CreateUserRequestRequestTypeDef",
    "CreateUserResponseTypeDef",
    "DelegateTypeDef",
    "DeleteAccessControlRuleRequestRequestTypeDef",
    "DeleteAliasRequestRequestTypeDef",
    "DeleteAvailabilityConfigurationRequestRequestTypeDef",
    "DeleteEmailMonitoringConfigurationRequestRequestTypeDef",
    "DeleteGroupRequestRequestTypeDef",
    "DeleteIdentityCenterApplicationRequestRequestTypeDef",
    "DeleteIdentityProviderConfigurationRequestRequestTypeDef",
    "DeleteImpersonationRoleRequestRequestTypeDef",
    "DeleteMailboxPermissionsRequestRequestTypeDef",
    "DeleteMobileDeviceAccessOverrideRequestRequestTypeDef",
    "DeleteMobileDeviceAccessRuleRequestRequestTypeDef",
    "DeleteOrganizationRequestRequestTypeDef",
    "DeleteOrganizationResponseTypeDef",
    "DeletePersonalAccessTokenRequestRequestTypeDef",
    "DeleteResourceRequestRequestTypeDef",
    "DeleteRetentionPolicyRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DeregisterFromWorkMailRequestRequestTypeDef",
    "DeregisterMailDomainRequestRequestTypeDef",
    "DescribeEmailMonitoringConfigurationRequestRequestTypeDef",
    "DescribeEmailMonitoringConfigurationResponseTypeDef",
    "DescribeEntityRequestRequestTypeDef",
    "DescribeEntityResponseTypeDef",
    "DescribeGroupRequestRequestTypeDef",
    "DescribeGroupResponseTypeDef",
    "DescribeIdentityProviderConfigurationRequestRequestTypeDef",
    "DescribeIdentityProviderConfigurationResponseTypeDef",
    "DescribeInboundDmarcSettingsRequestRequestTypeDef",
    "DescribeInboundDmarcSettingsResponseTypeDef",
    "DescribeMailboxExportJobRequestRequestTypeDef",
    "DescribeMailboxExportJobResponseTypeDef",
    "DescribeOrganizationRequestRequestTypeDef",
    "DescribeOrganizationResponseTypeDef",
    "DescribeResourceRequestRequestTypeDef",
    "DescribeResourceResponseTypeDef",
    "DescribeUserRequestRequestTypeDef",
    "DescribeUserResponseTypeDef",
    "DisassociateDelegateFromResourceRequestRequestTypeDef",
    "DisassociateMemberFromGroupRequestRequestTypeDef",
    "DnsRecordTypeDef",
    "DomainTypeDef",
    "EwsAvailabilityProviderTypeDef",
    "FolderConfigurationTypeDef",
    "GetAccessControlEffectRequestRequestTypeDef",
    "GetAccessControlEffectResponseTypeDef",
    "GetDefaultRetentionPolicyRequestRequestTypeDef",
    "GetDefaultRetentionPolicyResponseTypeDef",
    "GetImpersonationRoleEffectRequestRequestTypeDef",
    "GetImpersonationRoleEffectResponseTypeDef",
    "GetImpersonationRoleRequestRequestTypeDef",
    "GetImpersonationRoleResponseTypeDef",
    "GetMailDomainRequestRequestTypeDef",
    "GetMailDomainResponseTypeDef",
    "GetMailboxDetailsRequestRequestTypeDef",
    "GetMailboxDetailsResponseTypeDef",
    "GetMobileDeviceAccessEffectRequestRequestTypeDef",
    "GetMobileDeviceAccessEffectResponseTypeDef",
    "GetMobileDeviceAccessOverrideRequestRequestTypeDef",
    "GetMobileDeviceAccessOverrideResponseTypeDef",
    "GetPersonalAccessTokenMetadataRequestRequestTypeDef",
    "GetPersonalAccessTokenMetadataResponseTypeDef",
    "GroupIdentifierTypeDef",
    "GroupTypeDef",
    "IdentityCenterConfigurationTypeDef",
    "ImpersonationMatchedRuleTypeDef",
    "ImpersonationRoleTypeDef",
    "ImpersonationRuleOutputTypeDef",
    "ImpersonationRuleTypeDef",
    "ImpersonationRuleUnionTypeDef",
    "LambdaAvailabilityProviderTypeDef",
    "ListAccessControlRulesRequestRequestTypeDef",
    "ListAccessControlRulesResponseTypeDef",
    "ListAliasesRequestListAliasesPaginateTypeDef",
    "ListAliasesRequestRequestTypeDef",
    "ListAliasesResponseTypeDef",
    "ListAvailabilityConfigurationsRequestListAvailabilityConfigurationsPaginateTypeDef",
    "ListAvailabilityConfigurationsRequestRequestTypeDef",
    "ListAvailabilityConfigurationsResponseTypeDef",
    "ListGroupMembersRequestListGroupMembersPaginateTypeDef",
    "ListGroupMembersRequestRequestTypeDef",
    "ListGroupMembersResponseTypeDef",
    "ListGroupsFiltersTypeDef",
    "ListGroupsForEntityFiltersTypeDef",
    "ListGroupsForEntityRequestRequestTypeDef",
    "ListGroupsForEntityResponseTypeDef",
    "ListGroupsRequestListGroupsPaginateTypeDef",
    "ListGroupsRequestRequestTypeDef",
    "ListGroupsResponseTypeDef",
    "ListImpersonationRolesRequestRequestTypeDef",
    "ListImpersonationRolesResponseTypeDef",
    "ListMailDomainsRequestRequestTypeDef",
    "ListMailDomainsResponseTypeDef",
    "ListMailboxExportJobsRequestRequestTypeDef",
    "ListMailboxExportJobsResponseTypeDef",
    "ListMailboxPermissionsRequestListMailboxPermissionsPaginateTypeDef",
    "ListMailboxPermissionsRequestRequestTypeDef",
    "ListMailboxPermissionsResponseTypeDef",
    "ListMobileDeviceAccessOverridesRequestRequestTypeDef",
    "ListMobileDeviceAccessOverridesResponseTypeDef",
    "ListMobileDeviceAccessRulesRequestRequestTypeDef",
    "ListMobileDeviceAccessRulesResponseTypeDef",
    "ListOrganizationsRequestListOrganizationsPaginateTypeDef",
    "ListOrganizationsRequestRequestTypeDef",
    "ListOrganizationsResponseTypeDef",
    "ListPersonalAccessTokensRequestListPersonalAccessTokensPaginateTypeDef",
    "ListPersonalAccessTokensRequestRequestTypeDef",
    "ListPersonalAccessTokensResponseTypeDef",
    "ListResourceDelegatesRequestListResourceDelegatesPaginateTypeDef",
    "ListResourceDelegatesRequestRequestTypeDef",
    "ListResourceDelegatesResponseTypeDef",
    "ListResourcesFiltersTypeDef",
    "ListResourcesRequestListResourcesPaginateTypeDef",
    "ListResourcesRequestRequestTypeDef",
    "ListResourcesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListUsersFiltersTypeDef",
    "ListUsersRequestListUsersPaginateTypeDef",
    "ListUsersRequestRequestTypeDef",
    "ListUsersResponseTypeDef",
    "MailDomainSummaryTypeDef",
    "MailboxExportJobTypeDef",
    "MemberTypeDef",
    "MobileDeviceAccessMatchedRuleTypeDef",
    "MobileDeviceAccessOverrideTypeDef",
    "MobileDeviceAccessRuleTypeDef",
    "OrganizationSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "PermissionTypeDef",
    "PersonalAccessTokenConfigurationTypeDef",
    "PersonalAccessTokenSummaryTypeDef",
    "PutAccessControlRuleRequestRequestTypeDef",
    "PutEmailMonitoringConfigurationRequestRequestTypeDef",
    "PutIdentityProviderConfigurationRequestRequestTypeDef",
    "PutInboundDmarcSettingsRequestRequestTypeDef",
    "PutMailboxPermissionsRequestRequestTypeDef",
    "PutMobileDeviceAccessOverrideRequestRequestTypeDef",
    "PutRetentionPolicyRequestRequestTypeDef",
    "RedactedEwsAvailabilityProviderTypeDef",
    "RegisterMailDomainRequestRequestTypeDef",
    "RegisterToWorkMailRequestRequestTypeDef",
    "ResetPasswordRequestRequestTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "StartMailboxExportJobRequestRequestTypeDef",
    "StartMailboxExportJobResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TestAvailabilityConfigurationRequestRequestTypeDef",
    "TestAvailabilityConfigurationResponseTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAvailabilityConfigurationRequestRequestTypeDef",
    "UpdateDefaultMailDomainRequestRequestTypeDef",
    "UpdateGroupRequestRequestTypeDef",
    "UpdateImpersonationRoleRequestRequestTypeDef",
    "UpdateMailboxQuotaRequestRequestTypeDef",
    "UpdateMobileDeviceAccessRuleRequestRequestTypeDef",
    "UpdatePrimaryEmailAddressRequestRequestTypeDef",
    "UpdateResourceRequestRequestTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "UserTypeDef",
)


class AccessControlRuleTypeDef(TypedDict):
    Name: NotRequired[str]
    Effect: NotRequired[AccessControlRuleEffectType]
    Description: NotRequired[str]
    IpRanges: NotRequired[List[str]]
    NotIpRanges: NotRequired[List[str]]
    Actions: NotRequired[List[str]]
    NotActions: NotRequired[List[str]]
    UserIds: NotRequired[List[str]]
    NotUserIds: NotRequired[List[str]]
    DateCreated: NotRequired[datetime]
    DateModified: NotRequired[datetime]
    ImpersonationRoleIds: NotRequired[List[str]]
    NotImpersonationRoleIds: NotRequired[List[str]]


class AssociateDelegateToResourceRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    ResourceId: str
    EntityId: str


class AssociateMemberToGroupRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    GroupId: str
    MemberId: str


class AssumeImpersonationRoleRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    ImpersonationRoleId: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class LambdaAvailabilityProviderTypeDef(TypedDict):
    LambdaArn: str


class RedactedEwsAvailabilityProviderTypeDef(TypedDict):
    EwsEndpoint: NotRequired[str]
    EwsUsername: NotRequired[str]


class BookingOptionsTypeDef(TypedDict):
    AutoAcceptRequests: NotRequired[bool]
    AutoDeclineRecurringRequests: NotRequired[bool]
    AutoDeclineConflictingRequests: NotRequired[bool]


class CancelMailboxExportJobRequestRequestTypeDef(TypedDict):
    ClientToken: str
    JobId: str
    OrganizationId: str


class CreateAliasRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    EntityId: str
    Alias: str


class EwsAvailabilityProviderTypeDef(TypedDict):
    EwsEndpoint: str
    EwsUsername: str
    EwsPassword: str


class CreateGroupRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    Name: str
    HiddenFromGlobalAddressList: NotRequired[bool]


class CreateIdentityCenterApplicationRequestRequestTypeDef(TypedDict):
    Name: str
    InstanceArn: str
    ClientToken: NotRequired[str]


class CreateMobileDeviceAccessRuleRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    Name: str
    Effect: MobileDeviceAccessRuleEffectType
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    DeviceTypes: NotRequired[Sequence[str]]
    NotDeviceTypes: NotRequired[Sequence[str]]
    DeviceModels: NotRequired[Sequence[str]]
    NotDeviceModels: NotRequired[Sequence[str]]
    DeviceOperatingSystems: NotRequired[Sequence[str]]
    NotDeviceOperatingSystems: NotRequired[Sequence[str]]
    DeviceUserAgents: NotRequired[Sequence[str]]
    NotDeviceUserAgents: NotRequired[Sequence[str]]


class DomainTypeDef(TypedDict):
    DomainName: str
    HostedZoneId: NotRequired[str]


CreateResourceRequestRequestTypeDef = TypedDict(
    "CreateResourceRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "Name": str,
        "Type": ResourceTypeType,
        "Description": NotRequired[str],
        "HiddenFromGlobalAddressList": NotRequired[bool],
    },
)


class CreateUserRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    Name: str
    DisplayName: str
    Password: NotRequired[str]
    Role: NotRequired[UserRoleType]
    FirstName: NotRequired[str]
    LastName: NotRequired[str]
    HiddenFromGlobalAddressList: NotRequired[bool]
    IdentityProviderUserId: NotRequired[str]


DelegateTypeDef = TypedDict(
    "DelegateTypeDef",
    {
        "Id": str,
        "Type": MemberTypeType,
    },
)


class DeleteAccessControlRuleRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    Name: str


class DeleteAliasRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    EntityId: str
    Alias: str


class DeleteAvailabilityConfigurationRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    DomainName: str


class DeleteEmailMonitoringConfigurationRequestRequestTypeDef(TypedDict):
    OrganizationId: str


class DeleteGroupRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    GroupId: str


class DeleteIdentityCenterApplicationRequestRequestTypeDef(TypedDict):
    ApplicationArn: str


class DeleteIdentityProviderConfigurationRequestRequestTypeDef(TypedDict):
    OrganizationId: str


class DeleteImpersonationRoleRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    ImpersonationRoleId: str


class DeleteMailboxPermissionsRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    EntityId: str
    GranteeId: str


class DeleteMobileDeviceAccessOverrideRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    UserId: str
    DeviceId: str


class DeleteMobileDeviceAccessRuleRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    MobileDeviceAccessRuleId: str


class DeleteOrganizationRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    DeleteDirectory: bool
    ClientToken: NotRequired[str]
    ForceDelete: NotRequired[bool]
    DeleteIdentityCenterApplication: NotRequired[bool]


class DeletePersonalAccessTokenRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    PersonalAccessTokenId: str


class DeleteResourceRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    ResourceId: str


class DeleteRetentionPolicyRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    Id: str


class DeleteUserRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    UserId: str


class DeregisterFromWorkMailRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    EntityId: str


class DeregisterMailDomainRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    DomainName: str


class DescribeEmailMonitoringConfigurationRequestRequestTypeDef(TypedDict):
    OrganizationId: str


class DescribeEntityRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    Email: str


class DescribeGroupRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    GroupId: str


class DescribeIdentityProviderConfigurationRequestRequestTypeDef(TypedDict):
    OrganizationId: str


class IdentityCenterConfigurationTypeDef(TypedDict):
    InstanceArn: str
    ApplicationArn: str


class PersonalAccessTokenConfigurationTypeDef(TypedDict):
    Status: PersonalAccessTokenConfigurationStatusType
    LifetimeInDays: NotRequired[int]


class DescribeInboundDmarcSettingsRequestRequestTypeDef(TypedDict):
    OrganizationId: str


class DescribeMailboxExportJobRequestRequestTypeDef(TypedDict):
    JobId: str
    OrganizationId: str


class DescribeOrganizationRequestRequestTypeDef(TypedDict):
    OrganizationId: str


class DescribeResourceRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    ResourceId: str


class DescribeUserRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    UserId: str


class DisassociateDelegateFromResourceRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    ResourceId: str
    EntityId: str


class DisassociateMemberFromGroupRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    GroupId: str
    MemberId: str


DnsRecordTypeDef = TypedDict(
    "DnsRecordTypeDef",
    {
        "Type": NotRequired[str],
        "Hostname": NotRequired[str],
        "Value": NotRequired[str],
    },
)


class FolderConfigurationTypeDef(TypedDict):
    Name: FolderNameType
    Action: RetentionActionType
    Period: NotRequired[int]


class GetAccessControlEffectRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    IpAddress: str
    Action: str
    UserId: NotRequired[str]
    ImpersonationRoleId: NotRequired[str]


class GetDefaultRetentionPolicyRequestRequestTypeDef(TypedDict):
    OrganizationId: str


class GetImpersonationRoleEffectRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    ImpersonationRoleId: str
    TargetUser: str


class ImpersonationMatchedRuleTypeDef(TypedDict):
    ImpersonationRuleId: NotRequired[str]
    Name: NotRequired[str]


class GetImpersonationRoleRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    ImpersonationRoleId: str


class ImpersonationRuleOutputTypeDef(TypedDict):
    ImpersonationRuleId: str
    Effect: AccessEffectType
    Name: NotRequired[str]
    Description: NotRequired[str]
    TargetUsers: NotRequired[List[str]]
    NotTargetUsers: NotRequired[List[str]]


class GetMailDomainRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    DomainName: str


class GetMailboxDetailsRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    UserId: str


class GetMobileDeviceAccessEffectRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    DeviceType: NotRequired[str]
    DeviceModel: NotRequired[str]
    DeviceOperatingSystem: NotRequired[str]
    DeviceUserAgent: NotRequired[str]


class MobileDeviceAccessMatchedRuleTypeDef(TypedDict):
    MobileDeviceAccessRuleId: NotRequired[str]
    Name: NotRequired[str]


class GetMobileDeviceAccessOverrideRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    UserId: str
    DeviceId: str


class GetPersonalAccessTokenMetadataRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    PersonalAccessTokenId: str


class GroupIdentifierTypeDef(TypedDict):
    GroupId: NotRequired[str]
    GroupName: NotRequired[str]


class GroupTypeDef(TypedDict):
    Id: NotRequired[str]
    Email: NotRequired[str]
    Name: NotRequired[str]
    State: NotRequired[EntityStateType]
    EnabledDate: NotRequired[datetime]
    DisabledDate: NotRequired[datetime]


ImpersonationRoleTypeDef = TypedDict(
    "ImpersonationRoleTypeDef",
    {
        "ImpersonationRoleId": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[ImpersonationRoleTypeType],
        "DateCreated": NotRequired[datetime],
        "DateModified": NotRequired[datetime],
    },
)


class ImpersonationRuleTypeDef(TypedDict):
    ImpersonationRuleId: str
    Effect: AccessEffectType
    Name: NotRequired[str]
    Description: NotRequired[str]
    TargetUsers: NotRequired[Sequence[str]]
    NotTargetUsers: NotRequired[Sequence[str]]


class ListAccessControlRulesRequestRequestTypeDef(TypedDict):
    OrganizationId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAliasesRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    EntityId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListAvailabilityConfigurationsRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListGroupMembersRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    GroupId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


MemberTypeDef = TypedDict(
    "MemberTypeDef",
    {
        "Id": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[MemberTypeType],
        "State": NotRequired[EntityStateType],
        "EnabledDate": NotRequired[datetime],
        "DisabledDate": NotRequired[datetime],
    },
)


class ListGroupsFiltersTypeDef(TypedDict):
    NamePrefix: NotRequired[str]
    PrimaryEmailPrefix: NotRequired[str]
    State: NotRequired[EntityStateType]


class ListGroupsForEntityFiltersTypeDef(TypedDict):
    GroupNamePrefix: NotRequired[str]


class ListImpersonationRolesRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListMailDomainsRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class MailDomainSummaryTypeDef(TypedDict):
    DomainName: NotRequired[str]
    DefaultDomain: NotRequired[bool]


class ListMailboxExportJobsRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class MailboxExportJobTypeDef(TypedDict):
    JobId: NotRequired[str]
    EntityId: NotRequired[str]
    Description: NotRequired[str]
    S3BucketName: NotRequired[str]
    S3Path: NotRequired[str]
    EstimatedProgress: NotRequired[int]
    State: NotRequired[MailboxExportJobStateType]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]


class ListMailboxPermissionsRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    EntityId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class PermissionTypeDef(TypedDict):
    GranteeId: str
    GranteeType: MemberTypeType
    PermissionValues: List[PermissionTypeType]


class ListMobileDeviceAccessOverridesRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    UserId: NotRequired[str]
    DeviceId: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class MobileDeviceAccessOverrideTypeDef(TypedDict):
    UserId: NotRequired[str]
    DeviceId: NotRequired[str]
    Effect: NotRequired[MobileDeviceAccessRuleEffectType]
    Description: NotRequired[str]
    DateCreated: NotRequired[datetime]
    DateModified: NotRequired[datetime]


class ListMobileDeviceAccessRulesRequestRequestTypeDef(TypedDict):
    OrganizationId: str


class MobileDeviceAccessRuleTypeDef(TypedDict):
    MobileDeviceAccessRuleId: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    Effect: NotRequired[MobileDeviceAccessRuleEffectType]
    DeviceTypes: NotRequired[List[str]]
    NotDeviceTypes: NotRequired[List[str]]
    DeviceModels: NotRequired[List[str]]
    NotDeviceModels: NotRequired[List[str]]
    DeviceOperatingSystems: NotRequired[List[str]]
    NotDeviceOperatingSystems: NotRequired[List[str]]
    DeviceUserAgents: NotRequired[List[str]]
    NotDeviceUserAgents: NotRequired[List[str]]
    DateCreated: NotRequired[datetime]
    DateModified: NotRequired[datetime]


class ListOrganizationsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class OrganizationSummaryTypeDef(TypedDict):
    OrganizationId: NotRequired[str]
    Alias: NotRequired[str]
    DefaultMailDomain: NotRequired[str]
    ErrorMessage: NotRequired[str]
    State: NotRequired[str]


class ListPersonalAccessTokensRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    UserId: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class PersonalAccessTokenSummaryTypeDef(TypedDict):
    PersonalAccessTokenId: NotRequired[str]
    UserId: NotRequired[str]
    Name: NotRequired[str]
    DateCreated: NotRequired[datetime]
    DateLastUsed: NotRequired[datetime]
    ExpiresTime: NotRequired[datetime]
    Scopes: NotRequired[List[str]]


class ListResourceDelegatesRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    ResourceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListResourcesFiltersTypeDef(TypedDict):
    NamePrefix: NotRequired[str]
    PrimaryEmailPrefix: NotRequired[str]
    State: NotRequired[EntityStateType]


ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "Id": NotRequired[str],
        "Email": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[ResourceTypeType],
        "State": NotRequired[EntityStateType],
        "EnabledDate": NotRequired[datetime],
        "DisabledDate": NotRequired[datetime],
        "Description": NotRequired[str],
    },
)


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class ListUsersFiltersTypeDef(TypedDict):
    UsernamePrefix: NotRequired[str]
    DisplayNamePrefix: NotRequired[str]
    PrimaryEmailPrefix: NotRequired[str]
    State: NotRequired[EntityStateType]
    IdentityProviderUserIdPrefix: NotRequired[str]


class UserTypeDef(TypedDict):
    Id: NotRequired[str]
    Email: NotRequired[str]
    Name: NotRequired[str]
    DisplayName: NotRequired[str]
    State: NotRequired[EntityStateType]
    UserRole: NotRequired[UserRoleType]
    EnabledDate: NotRequired[datetime]
    DisabledDate: NotRequired[datetime]
    IdentityProviderUserId: NotRequired[str]
    IdentityProviderIdentityStoreId: NotRequired[str]


class PutAccessControlRuleRequestRequestTypeDef(TypedDict):
    Name: str
    Effect: AccessControlRuleEffectType
    Description: str
    OrganizationId: str
    IpRanges: NotRequired[Sequence[str]]
    NotIpRanges: NotRequired[Sequence[str]]
    Actions: NotRequired[Sequence[str]]
    NotActions: NotRequired[Sequence[str]]
    UserIds: NotRequired[Sequence[str]]
    NotUserIds: NotRequired[Sequence[str]]
    ImpersonationRoleIds: NotRequired[Sequence[str]]
    NotImpersonationRoleIds: NotRequired[Sequence[str]]


class PutEmailMonitoringConfigurationRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    RoleArn: str
    LogGroupArn: str


class PutInboundDmarcSettingsRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    Enforced: bool


class PutMailboxPermissionsRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    EntityId: str
    GranteeId: str
    PermissionValues: Sequence[PermissionTypeType]


class PutMobileDeviceAccessOverrideRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    UserId: str
    DeviceId: str
    Effect: MobileDeviceAccessRuleEffectType
    Description: NotRequired[str]


class RegisterMailDomainRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    DomainName: str
    ClientToken: NotRequired[str]


class RegisterToWorkMailRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    EntityId: str
    Email: str


class ResetPasswordRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    UserId: str
    Password: str


class StartMailboxExportJobRequestRequestTypeDef(TypedDict):
    ClientToken: str
    OrganizationId: str
    EntityId: str
    RoleArn: str
    KmsKeyArn: str
    S3BucketName: str
    S3Prefix: str
    Description: NotRequired[str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


class UpdateDefaultMailDomainRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    DomainName: str


class UpdateGroupRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    GroupId: str
    HiddenFromGlobalAddressList: NotRequired[bool]


class UpdateMailboxQuotaRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    UserId: str
    MailboxQuota: int


class UpdateMobileDeviceAccessRuleRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    MobileDeviceAccessRuleId: str
    Name: str
    Effect: MobileDeviceAccessRuleEffectType
    Description: NotRequired[str]
    DeviceTypes: NotRequired[Sequence[str]]
    NotDeviceTypes: NotRequired[Sequence[str]]
    DeviceModels: NotRequired[Sequence[str]]
    NotDeviceModels: NotRequired[Sequence[str]]
    DeviceOperatingSystems: NotRequired[Sequence[str]]
    NotDeviceOperatingSystems: NotRequired[Sequence[str]]
    DeviceUserAgents: NotRequired[Sequence[str]]
    NotDeviceUserAgents: NotRequired[Sequence[str]]


class UpdatePrimaryEmailAddressRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    EntityId: str
    Email: str


class UpdateUserRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    UserId: str
    Role: NotRequired[UserRoleType]
    DisplayName: NotRequired[str]
    FirstName: NotRequired[str]
    LastName: NotRequired[str]
    HiddenFromGlobalAddressList: NotRequired[bool]
    Initials: NotRequired[str]
    Telephone: NotRequired[str]
    Street: NotRequired[str]
    JobTitle: NotRequired[str]
    City: NotRequired[str]
    Company: NotRequired[str]
    ZipCode: NotRequired[str]
    Department: NotRequired[str]
    Country: NotRequired[str]
    Office: NotRequired[str]
    IdentityProviderUserId: NotRequired[str]


class AssumeImpersonationRoleResponseTypeDef(TypedDict):
    Token: str
    ExpiresIn: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateGroupResponseTypeDef(TypedDict):
    GroupId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateIdentityCenterApplicationResponseTypeDef(TypedDict):
    ApplicationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateImpersonationRoleResponseTypeDef(TypedDict):
    ImpersonationRoleId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMobileDeviceAccessRuleResponseTypeDef(TypedDict):
    MobileDeviceAccessRuleId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateOrganizationResponseTypeDef(TypedDict):
    OrganizationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateResourceResponseTypeDef(TypedDict):
    ResourceId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUserResponseTypeDef(TypedDict):
    UserId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteOrganizationResponseTypeDef(TypedDict):
    OrganizationId: str
    State: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEmailMonitoringConfigurationResponseTypeDef(TypedDict):
    RoleArn: str
    LogGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


DescribeEntityResponseTypeDef = TypedDict(
    "DescribeEntityResponseTypeDef",
    {
        "EntityId": str,
        "Name": str,
        "Type": EntityTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class DescribeGroupResponseTypeDef(TypedDict):
    GroupId: str
    Name: str
    Email: str
    State: EntityStateType
    EnabledDate: datetime
    DisabledDate: datetime
    HiddenFromGlobalAddressList: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeInboundDmarcSettingsResponseTypeDef(TypedDict):
    Enforced: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeMailboxExportJobResponseTypeDef(TypedDict):
    EntityId: str
    Description: str
    RoleArn: str
    KmsKeyArn: str
    S3BucketName: str
    S3Prefix: str
    S3Path: str
    EstimatedProgress: int
    State: MailboxExportJobStateType
    ErrorInfo: str
    StartTime: datetime
    EndTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeOrganizationResponseTypeDef(TypedDict):
    OrganizationId: str
    Alias: str
    State: str
    DirectoryId: str
    DirectoryType: str
    DefaultMailDomain: str
    CompletedDate: datetime
    ErrorMessage: str
    ARN: str
    MigrationAdmin: str
    InteroperabilityEnabled: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeUserResponseTypeDef(TypedDict):
    UserId: str
    Name: str
    Email: str
    DisplayName: str
    State: EntityStateType
    UserRole: UserRoleType
    EnabledDate: datetime
    DisabledDate: datetime
    MailboxProvisionedDate: datetime
    MailboxDeprovisionedDate: datetime
    FirstName: str
    LastName: str
    HiddenFromGlobalAddressList: bool
    Initials: str
    Telephone: str
    Street: str
    JobTitle: str
    City: str
    Company: str
    ZipCode: str
    Department: str
    Country: str
    Office: str
    IdentityProviderUserId: str
    IdentityProviderIdentityStoreId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetAccessControlEffectResponseTypeDef(TypedDict):
    Effect: AccessControlRuleEffectType
    MatchedRules: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetMailboxDetailsResponseTypeDef(TypedDict):
    MailboxQuota: int
    MailboxSize: float
    ResponseMetadata: ResponseMetadataTypeDef


class GetMobileDeviceAccessOverrideResponseTypeDef(TypedDict):
    UserId: str
    DeviceId: str
    Effect: MobileDeviceAccessRuleEffectType
    Description: str
    DateCreated: datetime
    DateModified: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetPersonalAccessTokenMetadataResponseTypeDef(TypedDict):
    PersonalAccessTokenId: str
    UserId: str
    Name: str
    DateCreated: datetime
    DateLastUsed: datetime
    ExpiresTime: datetime
    Scopes: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListAccessControlRulesResponseTypeDef(TypedDict):
    Rules: List[AccessControlRuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListAliasesResponseTypeDef(TypedDict):
    Aliases: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StartMailboxExportJobResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef


class TestAvailabilityConfigurationResponseTypeDef(TypedDict):
    TestPassed: bool
    FailureReason: str
    ResponseMetadata: ResponseMetadataTypeDef


class AvailabilityConfigurationTypeDef(TypedDict):
    DomainName: NotRequired[str]
    ProviderType: NotRequired[AvailabilityProviderTypeType]
    EwsProvider: NotRequired[RedactedEwsAvailabilityProviderTypeDef]
    LambdaProvider: NotRequired[LambdaAvailabilityProviderTypeDef]
    DateCreated: NotRequired[datetime]
    DateModified: NotRequired[datetime]


DescribeResourceResponseTypeDef = TypedDict(
    "DescribeResourceResponseTypeDef",
    {
        "ResourceId": str,
        "Email": str,
        "Name": str,
        "Type": ResourceTypeType,
        "BookingOptions": BookingOptionsTypeDef,
        "State": EntityStateType,
        "EnabledDate": datetime,
        "DisabledDate": datetime,
        "Description": str,
        "HiddenFromGlobalAddressList": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateResourceRequestRequestTypeDef = TypedDict(
    "UpdateResourceRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "ResourceId": str,
        "Name": NotRequired[str],
        "BookingOptions": NotRequired[BookingOptionsTypeDef],
        "Description": NotRequired[str],
        "Type": NotRequired[ResourceTypeType],
        "HiddenFromGlobalAddressList": NotRequired[bool],
    },
)


class CreateAvailabilityConfigurationRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    DomainName: str
    ClientToken: NotRequired[str]
    EwsProvider: NotRequired[EwsAvailabilityProviderTypeDef]
    LambdaProvider: NotRequired[LambdaAvailabilityProviderTypeDef]


class TestAvailabilityConfigurationRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    DomainName: NotRequired[str]
    EwsProvider: NotRequired[EwsAvailabilityProviderTypeDef]
    LambdaProvider: NotRequired[LambdaAvailabilityProviderTypeDef]


class UpdateAvailabilityConfigurationRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    DomainName: str
    EwsProvider: NotRequired[EwsAvailabilityProviderTypeDef]
    LambdaProvider: NotRequired[LambdaAvailabilityProviderTypeDef]


class CreateOrganizationRequestRequestTypeDef(TypedDict):
    Alias: str
    DirectoryId: NotRequired[str]
    ClientToken: NotRequired[str]
    Domains: NotRequired[Sequence[DomainTypeDef]]
    KmsKeyArn: NotRequired[str]
    EnableInteroperability: NotRequired[bool]


class ListResourceDelegatesResponseTypeDef(TypedDict):
    Delegates: List[DelegateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeIdentityProviderConfigurationResponseTypeDef(TypedDict):
    AuthenticationMode: IdentityProviderAuthenticationModeType
    IdentityCenterConfiguration: IdentityCenterConfigurationTypeDef
    PersonalAccessTokenConfiguration: PersonalAccessTokenConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutIdentityProviderConfigurationRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    AuthenticationMode: IdentityProviderAuthenticationModeType
    IdentityCenterConfiguration: IdentityCenterConfigurationTypeDef
    PersonalAccessTokenConfiguration: PersonalAccessTokenConfigurationTypeDef


class GetMailDomainResponseTypeDef(TypedDict):
    Records: List[DnsRecordTypeDef]
    IsTestDomain: bool
    IsDefault: bool
    OwnershipVerificationStatus: DnsRecordVerificationStatusType
    DkimVerificationStatus: DnsRecordVerificationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetDefaultRetentionPolicyResponseTypeDef(TypedDict):
    Id: str
    Name: str
    Description: str
    FolderConfigurations: List[FolderConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class PutRetentionPolicyRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    Name: str
    FolderConfigurations: Sequence[FolderConfigurationTypeDef]
    Id: NotRequired[str]
    Description: NotRequired[str]


GetImpersonationRoleEffectResponseTypeDef = TypedDict(
    "GetImpersonationRoleEffectResponseTypeDef",
    {
        "Type": ImpersonationRoleTypeType,
        "Effect": AccessEffectType,
        "MatchedRules": List[ImpersonationMatchedRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetImpersonationRoleResponseTypeDef = TypedDict(
    "GetImpersonationRoleResponseTypeDef",
    {
        "ImpersonationRoleId": str,
        "Name": str,
        "Type": ImpersonationRoleTypeType,
        "Description": str,
        "Rules": List[ImpersonationRuleOutputTypeDef],
        "DateCreated": datetime,
        "DateModified": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class GetMobileDeviceAccessEffectResponseTypeDef(TypedDict):
    Effect: MobileDeviceAccessRuleEffectType
    MatchedRules: List[MobileDeviceAccessMatchedRuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListGroupsForEntityResponseTypeDef(TypedDict):
    Groups: List[GroupIdentifierTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListGroupsResponseTypeDef(TypedDict):
    Groups: List[GroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListImpersonationRolesResponseTypeDef(TypedDict):
    Roles: List[ImpersonationRoleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


ImpersonationRuleUnionTypeDef = Union[ImpersonationRuleTypeDef, ImpersonationRuleOutputTypeDef]
UpdateImpersonationRoleRequestRequestTypeDef = TypedDict(
    "UpdateImpersonationRoleRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "ImpersonationRoleId": str,
        "Name": str,
        "Type": ImpersonationRoleTypeType,
        "Rules": Sequence[ImpersonationRuleTypeDef],
        "Description": NotRequired[str],
    },
)


class ListAliasesRequestListAliasesPaginateTypeDef(TypedDict):
    OrganizationId: str
    EntityId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAvailabilityConfigurationsRequestListAvailabilityConfigurationsPaginateTypeDef(TypedDict):
    OrganizationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupMembersRequestListGroupMembersPaginateTypeDef(TypedDict):
    OrganizationId: str
    GroupId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMailboxPermissionsRequestListMailboxPermissionsPaginateTypeDef(TypedDict):
    OrganizationId: str
    EntityId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOrganizationsRequestListOrganizationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPersonalAccessTokensRequestListPersonalAccessTokensPaginateTypeDef(TypedDict):
    OrganizationId: str
    UserId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourceDelegatesRequestListResourceDelegatesPaginateTypeDef(TypedDict):
    OrganizationId: str
    ResourceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupMembersResponseTypeDef(TypedDict):
    Members: List[MemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListGroupsRequestListGroupsPaginateTypeDef(TypedDict):
    OrganizationId: str
    Filters: NotRequired[ListGroupsFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupsRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[ListGroupsFiltersTypeDef]


class ListGroupsForEntityRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    EntityId: str
    Filters: NotRequired[ListGroupsForEntityFiltersTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListMailDomainsResponseTypeDef(TypedDict):
    MailDomains: List[MailDomainSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListMailboxExportJobsResponseTypeDef(TypedDict):
    Jobs: List[MailboxExportJobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListMailboxPermissionsResponseTypeDef(TypedDict):
    Permissions: List[PermissionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListMobileDeviceAccessOverridesResponseTypeDef(TypedDict):
    Overrides: List[MobileDeviceAccessOverrideTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListMobileDeviceAccessRulesResponseTypeDef(TypedDict):
    Rules: List[MobileDeviceAccessRuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListOrganizationsResponseTypeDef(TypedDict):
    OrganizationSummaries: List[OrganizationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPersonalAccessTokensResponseTypeDef(TypedDict):
    PersonalAccessTokenSummaries: List[PersonalAccessTokenSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListResourcesRequestListResourcesPaginateTypeDef(TypedDict):
    OrganizationId: str
    Filters: NotRequired[ListResourcesFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourcesRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[ListResourcesFiltersTypeDef]


class ListResourcesResponseTypeDef(TypedDict):
    Resources: List[ResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]


class ListUsersRequestListUsersPaginateTypeDef(TypedDict):
    OrganizationId: str
    Filters: NotRequired[ListUsersFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUsersRequestRequestTypeDef(TypedDict):
    OrganizationId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[ListUsersFiltersTypeDef]


class ListUsersResponseTypeDef(TypedDict):
    Users: List[UserTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListAvailabilityConfigurationsResponseTypeDef(TypedDict):
    AvailabilityConfigurations: List[AvailabilityConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


CreateImpersonationRoleRequestRequestTypeDef = TypedDict(
    "CreateImpersonationRoleRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "Name": str,
        "Type": ImpersonationRoleTypeType,
        "Rules": Sequence[ImpersonationRuleUnionTypeDef],
        "ClientToken": NotRequired[str],
        "Description": NotRequired[str],
    },
)
