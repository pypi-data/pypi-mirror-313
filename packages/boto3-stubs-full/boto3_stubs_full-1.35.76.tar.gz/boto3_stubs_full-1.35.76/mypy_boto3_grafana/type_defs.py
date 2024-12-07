"""
Type annotations for grafana service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/type_defs/)

Usage::

    ```python
    from mypy_boto3_grafana.type_defs import AssertionAttributesTypeDef

    data: AssertionAttributesTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AccountAccessTypeType,
    AuthenticationProviderTypesType,
    DataSourceTypeType,
    LicenseTypeType,
    PermissionTypeType,
    RoleType,
    SamlConfigurationStatusType,
    UpdateActionType,
    UserTypeType,
    WorkspaceStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AssertionAttributesTypeDef",
    "AssociateLicenseRequestRequestTypeDef",
    "AssociateLicenseResponseTypeDef",
    "AuthenticationDescriptionTypeDef",
    "AuthenticationSummaryTypeDef",
    "AwsSsoAuthenticationTypeDef",
    "CreateWorkspaceApiKeyRequestRequestTypeDef",
    "CreateWorkspaceApiKeyResponseTypeDef",
    "CreateWorkspaceRequestRequestTypeDef",
    "CreateWorkspaceResponseTypeDef",
    "CreateWorkspaceServiceAccountRequestRequestTypeDef",
    "CreateWorkspaceServiceAccountResponseTypeDef",
    "CreateWorkspaceServiceAccountTokenRequestRequestTypeDef",
    "CreateWorkspaceServiceAccountTokenResponseTypeDef",
    "DeleteWorkspaceApiKeyRequestRequestTypeDef",
    "DeleteWorkspaceApiKeyResponseTypeDef",
    "DeleteWorkspaceRequestRequestTypeDef",
    "DeleteWorkspaceResponseTypeDef",
    "DeleteWorkspaceServiceAccountRequestRequestTypeDef",
    "DeleteWorkspaceServiceAccountResponseTypeDef",
    "DeleteWorkspaceServiceAccountTokenRequestRequestTypeDef",
    "DeleteWorkspaceServiceAccountTokenResponseTypeDef",
    "DescribeWorkspaceAuthenticationRequestRequestTypeDef",
    "DescribeWorkspaceAuthenticationResponseTypeDef",
    "DescribeWorkspaceConfigurationRequestRequestTypeDef",
    "DescribeWorkspaceConfigurationResponseTypeDef",
    "DescribeWorkspaceRequestRequestTypeDef",
    "DescribeWorkspaceResponseTypeDef",
    "DisassociateLicenseRequestRequestTypeDef",
    "DisassociateLicenseResponseTypeDef",
    "IdpMetadataTypeDef",
    "ListPermissionsRequestListPermissionsPaginateTypeDef",
    "ListPermissionsRequestRequestTypeDef",
    "ListPermissionsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListVersionsRequestListVersionsPaginateTypeDef",
    "ListVersionsRequestRequestTypeDef",
    "ListVersionsResponseTypeDef",
    "ListWorkspaceServiceAccountTokensRequestListWorkspaceServiceAccountTokensPaginateTypeDef",
    "ListWorkspaceServiceAccountTokensRequestRequestTypeDef",
    "ListWorkspaceServiceAccountTokensResponseTypeDef",
    "ListWorkspaceServiceAccountsRequestListWorkspaceServiceAccountsPaginateTypeDef",
    "ListWorkspaceServiceAccountsRequestRequestTypeDef",
    "ListWorkspaceServiceAccountsResponseTypeDef",
    "ListWorkspacesRequestListWorkspacesPaginateTypeDef",
    "ListWorkspacesRequestRequestTypeDef",
    "ListWorkspacesResponseTypeDef",
    "NetworkAccessConfigurationOutputTypeDef",
    "NetworkAccessConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PermissionEntryTypeDef",
    "ResponseMetadataTypeDef",
    "RoleValuesOutputTypeDef",
    "RoleValuesTypeDef",
    "RoleValuesUnionTypeDef",
    "SamlAuthenticationTypeDef",
    "SamlConfigurationOutputTypeDef",
    "SamlConfigurationTypeDef",
    "ServiceAccountSummaryTypeDef",
    "ServiceAccountTokenSummaryTypeDef",
    "ServiceAccountTokenSummaryWithKeyTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateErrorTypeDef",
    "UpdateInstructionOutputTypeDef",
    "UpdateInstructionTypeDef",
    "UpdateInstructionUnionTypeDef",
    "UpdatePermissionsRequestRequestTypeDef",
    "UpdatePermissionsResponseTypeDef",
    "UpdateWorkspaceAuthenticationRequestRequestTypeDef",
    "UpdateWorkspaceAuthenticationResponseTypeDef",
    "UpdateWorkspaceConfigurationRequestRequestTypeDef",
    "UpdateWorkspaceRequestRequestTypeDef",
    "UpdateWorkspaceResponseTypeDef",
    "UserTypeDef",
    "VpcConfigurationOutputTypeDef",
    "VpcConfigurationTypeDef",
    "WorkspaceDescriptionTypeDef",
    "WorkspaceSummaryTypeDef",
)


class AssertionAttributesTypeDef(TypedDict):
    email: NotRequired[str]
    groups: NotRequired[str]
    login: NotRequired[str]
    name: NotRequired[str]
    org: NotRequired[str]
    role: NotRequired[str]


class AssociateLicenseRequestRequestTypeDef(TypedDict):
    licenseType: LicenseTypeType
    workspaceId: str
    grafanaToken: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AwsSsoAuthenticationTypeDef(TypedDict):
    ssoClientId: NotRequired[str]


class AuthenticationSummaryTypeDef(TypedDict):
    providers: List[AuthenticationProviderTypesType]
    samlConfigurationStatus: NotRequired[SamlConfigurationStatusType]


class CreateWorkspaceApiKeyRequestRequestTypeDef(TypedDict):
    keyName: str
    keyRole: str
    secondsToLive: int
    workspaceId: str


class NetworkAccessConfigurationTypeDef(TypedDict):
    prefixListIds: Sequence[str]
    vpceIds: Sequence[str]


class VpcConfigurationTypeDef(TypedDict):
    securityGroupIds: Sequence[str]
    subnetIds: Sequence[str]


class CreateWorkspaceServiceAccountRequestRequestTypeDef(TypedDict):
    grafanaRole: RoleType
    name: str
    workspaceId: str


class CreateWorkspaceServiceAccountTokenRequestRequestTypeDef(TypedDict):
    name: str
    secondsToLive: int
    serviceAccountId: str
    workspaceId: str


ServiceAccountTokenSummaryWithKeyTypeDef = TypedDict(
    "ServiceAccountTokenSummaryWithKeyTypeDef",
    {
        "id": str,
        "key": str,
        "name": str,
    },
)


class DeleteWorkspaceApiKeyRequestRequestTypeDef(TypedDict):
    keyName: str
    workspaceId: str


class DeleteWorkspaceRequestRequestTypeDef(TypedDict):
    workspaceId: str


class DeleteWorkspaceServiceAccountRequestRequestTypeDef(TypedDict):
    serviceAccountId: str
    workspaceId: str


class DeleteWorkspaceServiceAccountTokenRequestRequestTypeDef(TypedDict):
    serviceAccountId: str
    tokenId: str
    workspaceId: str


class DescribeWorkspaceAuthenticationRequestRequestTypeDef(TypedDict):
    workspaceId: str


class DescribeWorkspaceConfigurationRequestRequestTypeDef(TypedDict):
    workspaceId: str


class DescribeWorkspaceRequestRequestTypeDef(TypedDict):
    workspaceId: str


class DisassociateLicenseRequestRequestTypeDef(TypedDict):
    licenseType: LicenseTypeType
    workspaceId: str


class IdpMetadataTypeDef(TypedDict):
    url: NotRequired[str]
    xml: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListPermissionsRequestRequestTypeDef(TypedDict):
    workspaceId: str
    groupId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    userId: NotRequired[str]
    userType: NotRequired[UserTypeType]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class ListVersionsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    workspaceId: NotRequired[str]


class ListWorkspaceServiceAccountTokensRequestRequestTypeDef(TypedDict):
    serviceAccountId: str
    workspaceId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


ServiceAccountTokenSummaryTypeDef = TypedDict(
    "ServiceAccountTokenSummaryTypeDef",
    {
        "createdAt": datetime,
        "expiresAt": datetime,
        "id": str,
        "name": str,
        "lastUsedAt": NotRequired[datetime],
    },
)


class ListWorkspaceServiceAccountsRequestRequestTypeDef(TypedDict):
    workspaceId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


ServiceAccountSummaryTypeDef = TypedDict(
    "ServiceAccountSummaryTypeDef",
    {
        "grafanaRole": RoleType,
        "id": str,
        "isDisabled": str,
        "name": str,
    },
)


class ListWorkspacesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class NetworkAccessConfigurationOutputTypeDef(TypedDict):
    prefixListIds: List[str]
    vpceIds: List[str]


UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "id": str,
        "type": UserTypeType,
    },
)


class RoleValuesOutputTypeDef(TypedDict):
    admin: NotRequired[List[str]]
    editor: NotRequired[List[str]]


class RoleValuesTypeDef(TypedDict):
    admin: NotRequired[Sequence[str]]
    editor: NotRequired[Sequence[str]]


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateWorkspaceConfigurationRequestRequestTypeDef(TypedDict):
    configuration: str
    workspaceId: str
    grafanaVersion: NotRequired[str]


class VpcConfigurationOutputTypeDef(TypedDict):
    securityGroupIds: List[str]
    subnetIds: List[str]


class CreateWorkspaceApiKeyResponseTypeDef(TypedDict):
    key: str
    keyName: str
    workspaceId: str
    ResponseMetadata: ResponseMetadataTypeDef


CreateWorkspaceServiceAccountResponseTypeDef = TypedDict(
    "CreateWorkspaceServiceAccountResponseTypeDef",
    {
        "grafanaRole": RoleType,
        "id": str,
        "name": str,
        "workspaceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class DeleteWorkspaceApiKeyResponseTypeDef(TypedDict):
    keyName: str
    workspaceId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteWorkspaceServiceAccountResponseTypeDef(TypedDict):
    serviceAccountId: str
    workspaceId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteWorkspaceServiceAccountTokenResponseTypeDef(TypedDict):
    serviceAccountId: str
    tokenId: str
    workspaceId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeWorkspaceConfigurationResponseTypeDef(TypedDict):
    configuration: str
    grafanaVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListVersionsResponseTypeDef(TypedDict):
    grafanaVersions: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


WorkspaceSummaryTypeDef = TypedDict(
    "WorkspaceSummaryTypeDef",
    {
        "authentication": AuthenticationSummaryTypeDef,
        "created": datetime,
        "endpoint": str,
        "grafanaVersion": str,
        "id": str,
        "modified": datetime,
        "status": WorkspaceStatusType,
        "description": NotRequired[str],
        "grafanaToken": NotRequired[str],
        "licenseType": NotRequired[LicenseTypeType],
        "name": NotRequired[str],
        "notificationDestinations": NotRequired[List[Literal["SNS"]]],
        "tags": NotRequired[Dict[str, str]],
    },
)


class CreateWorkspaceRequestRequestTypeDef(TypedDict):
    accountAccessType: AccountAccessTypeType
    authenticationProviders: Sequence[AuthenticationProviderTypesType]
    permissionType: PermissionTypeType
    clientToken: NotRequired[str]
    configuration: NotRequired[str]
    grafanaVersion: NotRequired[str]
    networkAccessControl: NotRequired[NetworkAccessConfigurationTypeDef]
    organizationRoleName: NotRequired[str]
    stackSetName: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    vpcConfiguration: NotRequired[VpcConfigurationTypeDef]
    workspaceDataSources: NotRequired[Sequence[DataSourceTypeType]]
    workspaceDescription: NotRequired[str]
    workspaceName: NotRequired[str]
    workspaceNotificationDestinations: NotRequired[Sequence[Literal["SNS"]]]
    workspaceOrganizationalUnits: NotRequired[Sequence[str]]
    workspaceRoleArn: NotRequired[str]


class UpdateWorkspaceRequestRequestTypeDef(TypedDict):
    workspaceId: str
    accountAccessType: NotRequired[AccountAccessTypeType]
    networkAccessControl: NotRequired[NetworkAccessConfigurationTypeDef]
    organizationRoleName: NotRequired[str]
    permissionType: NotRequired[PermissionTypeType]
    removeNetworkAccessConfiguration: NotRequired[bool]
    removeVpcConfiguration: NotRequired[bool]
    stackSetName: NotRequired[str]
    vpcConfiguration: NotRequired[VpcConfigurationTypeDef]
    workspaceDataSources: NotRequired[Sequence[DataSourceTypeType]]
    workspaceDescription: NotRequired[str]
    workspaceName: NotRequired[str]
    workspaceNotificationDestinations: NotRequired[Sequence[Literal["SNS"]]]
    workspaceOrganizationalUnits: NotRequired[Sequence[str]]
    workspaceRoleArn: NotRequired[str]


class CreateWorkspaceServiceAccountTokenResponseTypeDef(TypedDict):
    serviceAccountId: str
    serviceAccountToken: ServiceAccountTokenSummaryWithKeyTypeDef
    workspaceId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListPermissionsRequestListPermissionsPaginateTypeDef(TypedDict):
    workspaceId: str
    groupId: NotRequired[str]
    userId: NotRequired[str]
    userType: NotRequired[UserTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListVersionsRequestListVersionsPaginateTypeDef(TypedDict):
    workspaceId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkspaceServiceAccountTokensRequestListWorkspaceServiceAccountTokensPaginateTypeDef(
    TypedDict
):
    serviceAccountId: str
    workspaceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkspaceServiceAccountsRequestListWorkspaceServiceAccountsPaginateTypeDef(TypedDict):
    workspaceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkspacesRequestListWorkspacesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkspaceServiceAccountTokensResponseTypeDef(TypedDict):
    serviceAccountId: str
    serviceAccountTokens: List[ServiceAccountTokenSummaryTypeDef]
    workspaceId: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListWorkspaceServiceAccountsResponseTypeDef(TypedDict):
    serviceAccounts: List[ServiceAccountSummaryTypeDef]
    workspaceId: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class PermissionEntryTypeDef(TypedDict):
    role: RoleType
    user: UserTypeDef


class UpdateInstructionOutputTypeDef(TypedDict):
    action: UpdateActionType
    role: RoleType
    users: List[UserTypeDef]


class UpdateInstructionTypeDef(TypedDict):
    action: UpdateActionType
    role: RoleType
    users: Sequence[UserTypeDef]


class SamlConfigurationOutputTypeDef(TypedDict):
    idpMetadata: IdpMetadataTypeDef
    allowedOrganizations: NotRequired[List[str]]
    assertionAttributes: NotRequired[AssertionAttributesTypeDef]
    loginValidityDuration: NotRequired[int]
    roleValues: NotRequired[RoleValuesOutputTypeDef]


RoleValuesUnionTypeDef = Union[RoleValuesTypeDef, RoleValuesOutputTypeDef]
WorkspaceDescriptionTypeDef = TypedDict(
    "WorkspaceDescriptionTypeDef",
    {
        "authentication": AuthenticationSummaryTypeDef,
        "created": datetime,
        "dataSources": List[DataSourceTypeType],
        "endpoint": str,
        "grafanaVersion": str,
        "id": str,
        "modified": datetime,
        "status": WorkspaceStatusType,
        "accountAccessType": NotRequired[AccountAccessTypeType],
        "description": NotRequired[str],
        "freeTrialConsumed": NotRequired[bool],
        "freeTrialExpiration": NotRequired[datetime],
        "grafanaToken": NotRequired[str],
        "licenseExpiration": NotRequired[datetime],
        "licenseType": NotRequired[LicenseTypeType],
        "name": NotRequired[str],
        "networkAccessControl": NotRequired[NetworkAccessConfigurationOutputTypeDef],
        "notificationDestinations": NotRequired[List[Literal["SNS"]]],
        "organizationRoleName": NotRequired[str],
        "organizationalUnits": NotRequired[List[str]],
        "permissionType": NotRequired[PermissionTypeType],
        "stackSetName": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "vpcConfiguration": NotRequired[VpcConfigurationOutputTypeDef],
        "workspaceRoleArn": NotRequired[str],
    },
)


class ListWorkspacesResponseTypeDef(TypedDict):
    workspaces: List[WorkspaceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListPermissionsResponseTypeDef(TypedDict):
    permissions: List[PermissionEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateErrorTypeDef(TypedDict):
    causedBy: UpdateInstructionOutputTypeDef
    code: int
    message: str


UpdateInstructionUnionTypeDef = Union[UpdateInstructionTypeDef, UpdateInstructionOutputTypeDef]


class SamlAuthenticationTypeDef(TypedDict):
    status: SamlConfigurationStatusType
    configuration: NotRequired[SamlConfigurationOutputTypeDef]


class SamlConfigurationTypeDef(TypedDict):
    idpMetadata: IdpMetadataTypeDef
    allowedOrganizations: NotRequired[Sequence[str]]
    assertionAttributes: NotRequired[AssertionAttributesTypeDef]
    loginValidityDuration: NotRequired[int]
    roleValues: NotRequired[RoleValuesUnionTypeDef]


class AssociateLicenseResponseTypeDef(TypedDict):
    workspace: WorkspaceDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateWorkspaceResponseTypeDef(TypedDict):
    workspace: WorkspaceDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteWorkspaceResponseTypeDef(TypedDict):
    workspace: WorkspaceDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeWorkspaceResponseTypeDef(TypedDict):
    workspace: WorkspaceDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateLicenseResponseTypeDef(TypedDict):
    workspace: WorkspaceDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateWorkspaceResponseTypeDef(TypedDict):
    workspace: WorkspaceDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePermissionsResponseTypeDef(TypedDict):
    errors: List[UpdateErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePermissionsRequestRequestTypeDef(TypedDict):
    updateInstructionBatch: Sequence[UpdateInstructionUnionTypeDef]
    workspaceId: str


class AuthenticationDescriptionTypeDef(TypedDict):
    providers: List[AuthenticationProviderTypesType]
    awsSso: NotRequired[AwsSsoAuthenticationTypeDef]
    saml: NotRequired[SamlAuthenticationTypeDef]


class UpdateWorkspaceAuthenticationRequestRequestTypeDef(TypedDict):
    authenticationProviders: Sequence[AuthenticationProviderTypesType]
    workspaceId: str
    samlConfiguration: NotRequired[SamlConfigurationTypeDef]


class DescribeWorkspaceAuthenticationResponseTypeDef(TypedDict):
    authentication: AuthenticationDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateWorkspaceAuthenticationResponseTypeDef(TypedDict):
    authentication: AuthenticationDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
