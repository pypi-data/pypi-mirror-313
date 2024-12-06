"""
Type annotations for sso-admin service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/type_defs/)

Usage::

    ```python
    from mypy_boto3_sso_admin.type_defs import AccessControlAttributeValueOutputTypeDef

    data: AccessControlAttributeValueOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    ApplicationStatusType,
    ApplicationVisibilityType,
    FederationProtocolType,
    GrantTypeType,
    InstanceAccessControlAttributeConfigurationStatusType,
    InstanceStatusType,
    PrincipalTypeType,
    ProvisioningStatusType,
    ProvisionTargetTypeType,
    SignInOriginType,
    StatusValuesType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccessControlAttributeOutputTypeDef",
    "AccessControlAttributeTypeDef",
    "AccessControlAttributeUnionTypeDef",
    "AccessControlAttributeValueOutputTypeDef",
    "AccessControlAttributeValueTypeDef",
    "AccessControlAttributeValueUnionTypeDef",
    "AccountAssignmentForPrincipalTypeDef",
    "AccountAssignmentOperationStatusMetadataTypeDef",
    "AccountAssignmentOperationStatusTypeDef",
    "AccountAssignmentTypeDef",
    "ApplicationAssignmentForPrincipalTypeDef",
    "ApplicationAssignmentTypeDef",
    "ApplicationProviderTypeDef",
    "ApplicationTypeDef",
    "AttachCustomerManagedPolicyReferenceToPermissionSetRequestRequestTypeDef",
    "AttachManagedPolicyToPermissionSetRequestRequestTypeDef",
    "AttachedManagedPolicyTypeDef",
    "AuthenticationMethodItemTypeDef",
    "AuthenticationMethodOutputTypeDef",
    "AuthenticationMethodTypeDef",
    "AuthorizationCodeGrantOutputTypeDef",
    "AuthorizationCodeGrantTypeDef",
    "AuthorizationCodeGrantUnionTypeDef",
    "AuthorizedTokenIssuerOutputTypeDef",
    "AuthorizedTokenIssuerTypeDef",
    "AuthorizedTokenIssuerUnionTypeDef",
    "CreateAccountAssignmentRequestRequestTypeDef",
    "CreateAccountAssignmentResponseTypeDef",
    "CreateApplicationAssignmentRequestRequestTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    "CreateInstanceRequestRequestTypeDef",
    "CreateInstanceResponseTypeDef",
    "CreatePermissionSetRequestRequestTypeDef",
    "CreatePermissionSetResponseTypeDef",
    "CreateTrustedTokenIssuerRequestRequestTypeDef",
    "CreateTrustedTokenIssuerResponseTypeDef",
    "CustomerManagedPolicyReferenceTypeDef",
    "DeleteAccountAssignmentRequestRequestTypeDef",
    "DeleteAccountAssignmentResponseTypeDef",
    "DeleteApplicationAccessScopeRequestRequestTypeDef",
    "DeleteApplicationAssignmentRequestRequestTypeDef",
    "DeleteApplicationAuthenticationMethodRequestRequestTypeDef",
    "DeleteApplicationGrantRequestRequestTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteInlinePolicyFromPermissionSetRequestRequestTypeDef",
    "DeleteInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    "DeleteInstanceRequestRequestTypeDef",
    "DeletePermissionSetRequestRequestTypeDef",
    "DeletePermissionsBoundaryFromPermissionSetRequestRequestTypeDef",
    "DeleteTrustedTokenIssuerRequestRequestTypeDef",
    "DescribeAccountAssignmentCreationStatusRequestRequestTypeDef",
    "DescribeAccountAssignmentCreationStatusResponseTypeDef",
    "DescribeAccountAssignmentDeletionStatusRequestRequestTypeDef",
    "DescribeAccountAssignmentDeletionStatusResponseTypeDef",
    "DescribeApplicationAssignmentRequestRequestTypeDef",
    "DescribeApplicationAssignmentResponseTypeDef",
    "DescribeApplicationProviderRequestRequestTypeDef",
    "DescribeApplicationProviderResponseTypeDef",
    "DescribeApplicationRequestRequestTypeDef",
    "DescribeApplicationResponseTypeDef",
    "DescribeInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    "DescribeInstanceAccessControlAttributeConfigurationResponseTypeDef",
    "DescribeInstanceRequestRequestTypeDef",
    "DescribeInstanceResponseTypeDef",
    "DescribePermissionSetProvisioningStatusRequestRequestTypeDef",
    "DescribePermissionSetProvisioningStatusResponseTypeDef",
    "DescribePermissionSetRequestRequestTypeDef",
    "DescribePermissionSetResponseTypeDef",
    "DescribeTrustedTokenIssuerRequestRequestTypeDef",
    "DescribeTrustedTokenIssuerResponseTypeDef",
    "DetachCustomerManagedPolicyReferenceFromPermissionSetRequestRequestTypeDef",
    "DetachManagedPolicyFromPermissionSetRequestRequestTypeDef",
    "DisplayDataTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetApplicationAccessScopeRequestRequestTypeDef",
    "GetApplicationAccessScopeResponseTypeDef",
    "GetApplicationAssignmentConfigurationRequestRequestTypeDef",
    "GetApplicationAssignmentConfigurationResponseTypeDef",
    "GetApplicationAuthenticationMethodRequestRequestTypeDef",
    "GetApplicationAuthenticationMethodResponseTypeDef",
    "GetApplicationGrantRequestRequestTypeDef",
    "GetApplicationGrantResponseTypeDef",
    "GetInlinePolicyForPermissionSetRequestRequestTypeDef",
    "GetInlinePolicyForPermissionSetResponseTypeDef",
    "GetPermissionsBoundaryForPermissionSetRequestRequestTypeDef",
    "GetPermissionsBoundaryForPermissionSetResponseTypeDef",
    "GrantItemTypeDef",
    "GrantOutputTypeDef",
    "GrantTypeDef",
    "IamAuthenticationMethodOutputTypeDef",
    "IamAuthenticationMethodTypeDef",
    "IamAuthenticationMethodUnionTypeDef",
    "InstanceAccessControlAttributeConfigurationOutputTypeDef",
    "InstanceAccessControlAttributeConfigurationTypeDef",
    "InstanceMetadataTypeDef",
    "JwtBearerGrantOutputTypeDef",
    "JwtBearerGrantTypeDef",
    "JwtBearerGrantUnionTypeDef",
    "ListAccountAssignmentCreationStatusRequestListAccountAssignmentCreationStatusPaginateTypeDef",
    "ListAccountAssignmentCreationStatusRequestRequestTypeDef",
    "ListAccountAssignmentCreationStatusResponseTypeDef",
    "ListAccountAssignmentDeletionStatusRequestListAccountAssignmentDeletionStatusPaginateTypeDef",
    "ListAccountAssignmentDeletionStatusRequestRequestTypeDef",
    "ListAccountAssignmentDeletionStatusResponseTypeDef",
    "ListAccountAssignmentsFilterTypeDef",
    "ListAccountAssignmentsForPrincipalRequestListAccountAssignmentsForPrincipalPaginateTypeDef",
    "ListAccountAssignmentsForPrincipalRequestRequestTypeDef",
    "ListAccountAssignmentsForPrincipalResponseTypeDef",
    "ListAccountAssignmentsRequestListAccountAssignmentsPaginateTypeDef",
    "ListAccountAssignmentsRequestRequestTypeDef",
    "ListAccountAssignmentsResponseTypeDef",
    "ListAccountsForProvisionedPermissionSetRequestListAccountsForProvisionedPermissionSetPaginateTypeDef",
    "ListAccountsForProvisionedPermissionSetRequestRequestTypeDef",
    "ListAccountsForProvisionedPermissionSetResponseTypeDef",
    "ListApplicationAccessScopesRequestListApplicationAccessScopesPaginateTypeDef",
    "ListApplicationAccessScopesRequestRequestTypeDef",
    "ListApplicationAccessScopesResponseTypeDef",
    "ListApplicationAssignmentsFilterTypeDef",
    "ListApplicationAssignmentsForPrincipalRequestListApplicationAssignmentsForPrincipalPaginateTypeDef",
    "ListApplicationAssignmentsForPrincipalRequestRequestTypeDef",
    "ListApplicationAssignmentsForPrincipalResponseTypeDef",
    "ListApplicationAssignmentsRequestListApplicationAssignmentsPaginateTypeDef",
    "ListApplicationAssignmentsRequestRequestTypeDef",
    "ListApplicationAssignmentsResponseTypeDef",
    "ListApplicationAuthenticationMethodsRequestListApplicationAuthenticationMethodsPaginateTypeDef",
    "ListApplicationAuthenticationMethodsRequestRequestTypeDef",
    "ListApplicationAuthenticationMethodsResponseTypeDef",
    "ListApplicationGrantsRequestListApplicationGrantsPaginateTypeDef",
    "ListApplicationGrantsRequestRequestTypeDef",
    "ListApplicationGrantsResponseTypeDef",
    "ListApplicationProvidersRequestListApplicationProvidersPaginateTypeDef",
    "ListApplicationProvidersRequestRequestTypeDef",
    "ListApplicationProvidersResponseTypeDef",
    "ListApplicationsFilterTypeDef",
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListCustomerManagedPolicyReferencesInPermissionSetRequestListCustomerManagedPolicyReferencesInPermissionSetPaginateTypeDef",
    "ListCustomerManagedPolicyReferencesInPermissionSetRequestRequestTypeDef",
    "ListCustomerManagedPolicyReferencesInPermissionSetResponseTypeDef",
    "ListInstancesRequestListInstancesPaginateTypeDef",
    "ListInstancesRequestRequestTypeDef",
    "ListInstancesResponseTypeDef",
    "ListManagedPoliciesInPermissionSetRequestListManagedPoliciesInPermissionSetPaginateTypeDef",
    "ListManagedPoliciesInPermissionSetRequestRequestTypeDef",
    "ListManagedPoliciesInPermissionSetResponseTypeDef",
    "ListPermissionSetProvisioningStatusRequestListPermissionSetProvisioningStatusPaginateTypeDef",
    "ListPermissionSetProvisioningStatusRequestRequestTypeDef",
    "ListPermissionSetProvisioningStatusResponseTypeDef",
    "ListPermissionSetsProvisionedToAccountRequestListPermissionSetsProvisionedToAccountPaginateTypeDef",
    "ListPermissionSetsProvisionedToAccountRequestRequestTypeDef",
    "ListPermissionSetsProvisionedToAccountResponseTypeDef",
    "ListPermissionSetsRequestListPermissionSetsPaginateTypeDef",
    "ListPermissionSetsRequestRequestTypeDef",
    "ListPermissionSetsResponseTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTrustedTokenIssuersRequestListTrustedTokenIssuersPaginateTypeDef",
    "ListTrustedTokenIssuersRequestRequestTypeDef",
    "ListTrustedTokenIssuersResponseTypeDef",
    "OidcJwtConfigurationTypeDef",
    "OidcJwtUpdateConfigurationTypeDef",
    "OperationStatusFilterTypeDef",
    "PaginatorConfigTypeDef",
    "PermissionSetProvisioningStatusMetadataTypeDef",
    "PermissionSetProvisioningStatusTypeDef",
    "PermissionSetTypeDef",
    "PermissionsBoundaryTypeDef",
    "PortalOptionsTypeDef",
    "ProvisionPermissionSetRequestRequestTypeDef",
    "ProvisionPermissionSetResponseTypeDef",
    "PutApplicationAccessScopeRequestRequestTypeDef",
    "PutApplicationAssignmentConfigurationRequestRequestTypeDef",
    "PutApplicationAuthenticationMethodRequestRequestTypeDef",
    "PutApplicationGrantRequestRequestTypeDef",
    "PutInlinePolicyToPermissionSetRequestRequestTypeDef",
    "PutPermissionsBoundaryToPermissionSetRequestRequestTypeDef",
    "ResourceServerConfigTypeDef",
    "ResourceServerScopeDetailsTypeDef",
    "ResponseMetadataTypeDef",
    "ScopeDetailsTypeDef",
    "SignInOptionsTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TrustedTokenIssuerConfigurationTypeDef",
    "TrustedTokenIssuerMetadataTypeDef",
    "TrustedTokenIssuerUpdateConfigurationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationPortalOptionsTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    "UpdateInstanceRequestRequestTypeDef",
    "UpdatePermissionSetRequestRequestTypeDef",
    "UpdateTrustedTokenIssuerRequestRequestTypeDef",
)

class AccessControlAttributeValueOutputTypeDef(TypedDict):
    Source: List[str]

class AccessControlAttributeValueTypeDef(TypedDict):
    Source: Sequence[str]

class AccountAssignmentForPrincipalTypeDef(TypedDict):
    AccountId: NotRequired[str]
    PermissionSetArn: NotRequired[str]
    PrincipalId: NotRequired[str]
    PrincipalType: NotRequired[PrincipalTypeType]

class AccountAssignmentOperationStatusMetadataTypeDef(TypedDict):
    CreatedDate: NotRequired[datetime]
    RequestId: NotRequired[str]
    Status: NotRequired[StatusValuesType]

class AccountAssignmentOperationStatusTypeDef(TypedDict):
    CreatedDate: NotRequired[datetime]
    FailureReason: NotRequired[str]
    PermissionSetArn: NotRequired[str]
    PrincipalId: NotRequired[str]
    PrincipalType: NotRequired[PrincipalTypeType]
    RequestId: NotRequired[str]
    Status: NotRequired[StatusValuesType]
    TargetId: NotRequired[str]
    TargetType: NotRequired[Literal["AWS_ACCOUNT"]]

class AccountAssignmentTypeDef(TypedDict):
    AccountId: NotRequired[str]
    PermissionSetArn: NotRequired[str]
    PrincipalId: NotRequired[str]
    PrincipalType: NotRequired[PrincipalTypeType]

class ApplicationAssignmentForPrincipalTypeDef(TypedDict):
    ApplicationArn: NotRequired[str]
    PrincipalId: NotRequired[str]
    PrincipalType: NotRequired[PrincipalTypeType]

class ApplicationAssignmentTypeDef(TypedDict):
    ApplicationArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType

class DisplayDataTypeDef(TypedDict):
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    IconUrl: NotRequired[str]

class CustomerManagedPolicyReferenceTypeDef(TypedDict):
    Name: str
    Path: NotRequired[str]

class AttachManagedPolicyToPermissionSetRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    ManagedPolicyArn: str
    PermissionSetArn: str

class AttachedManagedPolicyTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]

class IamAuthenticationMethodOutputTypeDef(TypedDict):
    ActorPolicy: Dict[str, Any]

class AuthorizationCodeGrantOutputTypeDef(TypedDict):
    RedirectUris: NotRequired[List[str]]

class AuthorizationCodeGrantTypeDef(TypedDict):
    RedirectUris: NotRequired[Sequence[str]]

class AuthorizedTokenIssuerOutputTypeDef(TypedDict):
    AuthorizedAudiences: NotRequired[List[str]]
    TrustedTokenIssuerArn: NotRequired[str]

class AuthorizedTokenIssuerTypeDef(TypedDict):
    AuthorizedAudiences: NotRequired[Sequence[str]]
    TrustedTokenIssuerArn: NotRequired[str]

class CreateAccountAssignmentRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType
    TargetId: str
    TargetType: Literal["AWS_ACCOUNT"]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateApplicationAssignmentRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class PermissionSetTypeDef(TypedDict):
    CreatedDate: NotRequired[datetime]
    Description: NotRequired[str]
    Name: NotRequired[str]
    PermissionSetArn: NotRequired[str]
    RelayState: NotRequired[str]
    SessionDuration: NotRequired[str]

class DeleteAccountAssignmentRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType
    TargetId: str
    TargetType: Literal["AWS_ACCOUNT"]

class DeleteApplicationAccessScopeRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    Scope: str

class DeleteApplicationAssignmentRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType

class DeleteApplicationAuthenticationMethodRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    AuthenticationMethodType: Literal["IAM"]

class DeleteApplicationGrantRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    GrantType: GrantTypeType

class DeleteApplicationRequestRequestTypeDef(TypedDict):
    ApplicationArn: str

class DeleteInlinePolicyFromPermissionSetRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str

class DeleteInstanceAccessControlAttributeConfigurationRequestRequestTypeDef(TypedDict):
    InstanceArn: str

class DeleteInstanceRequestRequestTypeDef(TypedDict):
    InstanceArn: str

class DeletePermissionSetRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str

class DeletePermissionsBoundaryFromPermissionSetRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str

class DeleteTrustedTokenIssuerRequestRequestTypeDef(TypedDict):
    TrustedTokenIssuerArn: str

class DescribeAccountAssignmentCreationStatusRequestRequestTypeDef(TypedDict):
    AccountAssignmentCreationRequestId: str
    InstanceArn: str

class DescribeAccountAssignmentDeletionStatusRequestRequestTypeDef(TypedDict):
    AccountAssignmentDeletionRequestId: str
    InstanceArn: str

class DescribeApplicationAssignmentRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType

class DescribeApplicationProviderRequestRequestTypeDef(TypedDict):
    ApplicationProviderArn: str

class DescribeApplicationRequestRequestTypeDef(TypedDict):
    ApplicationArn: str

class DescribeInstanceAccessControlAttributeConfigurationRequestRequestTypeDef(TypedDict):
    InstanceArn: str

class DescribeInstanceRequestRequestTypeDef(TypedDict):
    InstanceArn: str

class DescribePermissionSetProvisioningStatusRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    ProvisionPermissionSetRequestId: str

class PermissionSetProvisioningStatusTypeDef(TypedDict):
    AccountId: NotRequired[str]
    CreatedDate: NotRequired[datetime]
    FailureReason: NotRequired[str]
    PermissionSetArn: NotRequired[str]
    RequestId: NotRequired[str]
    Status: NotRequired[StatusValuesType]

class DescribePermissionSetRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str

class DescribeTrustedTokenIssuerRequestRequestTypeDef(TypedDict):
    TrustedTokenIssuerArn: str

class DetachManagedPolicyFromPermissionSetRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    ManagedPolicyArn: str
    PermissionSetArn: str

class GetApplicationAccessScopeRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    Scope: str

class GetApplicationAssignmentConfigurationRequestRequestTypeDef(TypedDict):
    ApplicationArn: str

class GetApplicationAuthenticationMethodRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    AuthenticationMethodType: Literal["IAM"]

class GetApplicationGrantRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    GrantType: GrantTypeType

class GetInlinePolicyForPermissionSetRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str

class GetPermissionsBoundaryForPermissionSetRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str

class IamAuthenticationMethodTypeDef(TypedDict):
    ActorPolicy: Mapping[str, Any]

class InstanceMetadataTypeDef(TypedDict):
    CreatedDate: NotRequired[datetime]
    IdentityStoreId: NotRequired[str]
    InstanceArn: NotRequired[str]
    Name: NotRequired[str]
    OwnerAccountId: NotRequired[str]
    Status: NotRequired[InstanceStatusType]

class OperationStatusFilterTypeDef(TypedDict):
    Status: NotRequired[StatusValuesType]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAccountAssignmentsFilterTypeDef(TypedDict):
    AccountId: NotRequired[str]

class ListAccountAssignmentsRequestRequestTypeDef(TypedDict):
    AccountId: str
    InstanceArn: str
    PermissionSetArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListAccountsForProvisionedPermissionSetRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ProvisioningStatus: NotRequired[ProvisioningStatusType]

class ListApplicationAccessScopesRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ScopeDetailsTypeDef(TypedDict):
    Scope: str
    AuthorizedTargets: NotRequired[List[str]]

class ListApplicationAssignmentsFilterTypeDef(TypedDict):
    ApplicationArn: NotRequired[str]

class ListApplicationAssignmentsRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListApplicationAuthenticationMethodsRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    NextToken: NotRequired[str]

class ListApplicationGrantsRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    NextToken: NotRequired[str]

class ListApplicationProvidersRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListApplicationsFilterTypeDef(TypedDict):
    ApplicationAccount: NotRequired[str]
    ApplicationProvider: NotRequired[str]

class ListCustomerManagedPolicyReferencesInPermissionSetRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListInstancesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListManagedPoliciesInPermissionSetRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class PermissionSetProvisioningStatusMetadataTypeDef(TypedDict):
    CreatedDate: NotRequired[datetime]
    RequestId: NotRequired[str]
    Status: NotRequired[StatusValuesType]

class ListPermissionSetsProvisionedToAccountRequestRequestTypeDef(TypedDict):
    AccountId: str
    InstanceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ProvisioningStatus: NotRequired[ProvisioningStatusType]

class ListPermissionSetsRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    InstanceArn: NotRequired[str]
    NextToken: NotRequired[str]

class ListTrustedTokenIssuersRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class TrustedTokenIssuerMetadataTypeDef(TypedDict):
    Name: NotRequired[str]
    TrustedTokenIssuerArn: NotRequired[str]
    TrustedTokenIssuerType: NotRequired[Literal["OIDC_JWT"]]

class OidcJwtConfigurationTypeDef(TypedDict):
    ClaimAttributePath: str
    IdentityStoreAttributePath: str
    IssuerUrl: str
    JwksRetrievalOption: Literal["OPEN_ID_DISCOVERY"]

class OidcJwtUpdateConfigurationTypeDef(TypedDict):
    ClaimAttributePath: NotRequired[str]
    IdentityStoreAttributePath: NotRequired[str]
    JwksRetrievalOption: NotRequired[Literal["OPEN_ID_DISCOVERY"]]

class SignInOptionsTypeDef(TypedDict):
    Origin: SignInOriginType
    ApplicationUrl: NotRequired[str]

class ProvisionPermissionSetRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    TargetType: ProvisionTargetTypeType
    TargetId: NotRequired[str]

class PutApplicationAccessScopeRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    Scope: str
    AuthorizedTargets: NotRequired[Sequence[str]]

class PutApplicationAssignmentConfigurationRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    AssignmentRequired: bool

class PutInlinePolicyToPermissionSetRequestRequestTypeDef(TypedDict):
    InlinePolicy: str
    InstanceArn: str
    PermissionSetArn: str

class ResourceServerScopeDetailsTypeDef(TypedDict):
    DetailedTitle: NotRequired[str]
    LongDescription: NotRequired[str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]
    InstanceArn: NotRequired[str]

class UpdateInstanceRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    Name: str

class UpdatePermissionSetRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    Description: NotRequired[str]
    RelayState: NotRequired[str]
    SessionDuration: NotRequired[str]

class AccessControlAttributeOutputTypeDef(TypedDict):
    Key: str
    Value: AccessControlAttributeValueOutputTypeDef

AccessControlAttributeValueUnionTypeDef = Union[
    AccessControlAttributeValueTypeDef, AccessControlAttributeValueOutputTypeDef
]

class AttachCustomerManagedPolicyReferenceToPermissionSetRequestRequestTypeDef(TypedDict):
    CustomerManagedPolicyReference: CustomerManagedPolicyReferenceTypeDef
    InstanceArn: str
    PermissionSetArn: str

class DetachCustomerManagedPolicyReferenceFromPermissionSetRequestRequestTypeDef(TypedDict):
    CustomerManagedPolicyReference: CustomerManagedPolicyReferenceTypeDef
    InstanceArn: str
    PermissionSetArn: str

class PermissionsBoundaryTypeDef(TypedDict):
    CustomerManagedPolicyReference: NotRequired[CustomerManagedPolicyReferenceTypeDef]
    ManagedPolicyArn: NotRequired[str]

class AuthenticationMethodOutputTypeDef(TypedDict):
    Iam: NotRequired[IamAuthenticationMethodOutputTypeDef]

AuthorizationCodeGrantUnionTypeDef = Union[
    AuthorizationCodeGrantTypeDef, AuthorizationCodeGrantOutputTypeDef
]

class JwtBearerGrantOutputTypeDef(TypedDict):
    AuthorizedTokenIssuers: NotRequired[List[AuthorizedTokenIssuerOutputTypeDef]]

AuthorizedTokenIssuerUnionTypeDef = Union[
    AuthorizedTokenIssuerTypeDef, AuthorizedTokenIssuerOutputTypeDef
]

class CreateAccountAssignmentResponseTypeDef(TypedDict):
    AccountAssignmentCreationStatus: AccountAssignmentOperationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateApplicationResponseTypeDef(TypedDict):
    ApplicationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateInstanceResponseTypeDef(TypedDict):
    InstanceArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTrustedTokenIssuerResponseTypeDef(TypedDict):
    TrustedTokenIssuerArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAccountAssignmentResponseTypeDef(TypedDict):
    AccountAssignmentDeletionStatus: AccountAssignmentOperationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAccountAssignmentCreationStatusResponseTypeDef(TypedDict):
    AccountAssignmentCreationStatus: AccountAssignmentOperationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAccountAssignmentDeletionStatusResponseTypeDef(TypedDict):
    AccountAssignmentDeletionStatus: AccountAssignmentOperationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeApplicationAssignmentResponseTypeDef(TypedDict):
    ApplicationArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeInstanceResponseTypeDef(TypedDict):
    CreatedDate: datetime
    IdentityStoreId: str
    InstanceArn: str
    Name: str
    OwnerAccountId: str
    Status: InstanceStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetApplicationAccessScopeResponseTypeDef(TypedDict):
    AuthorizedTargets: List[str]
    Scope: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetApplicationAssignmentConfigurationResponseTypeDef(TypedDict):
    AssignmentRequired: bool
    ResponseMetadata: ResponseMetadataTypeDef

class GetInlinePolicyForPermissionSetResponseTypeDef(TypedDict):
    InlinePolicy: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListAccountAssignmentCreationStatusResponseTypeDef(TypedDict):
    AccountAssignmentsCreationStatus: List[AccountAssignmentOperationStatusMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAccountAssignmentDeletionStatusResponseTypeDef(TypedDict):
    AccountAssignmentsDeletionStatus: List[AccountAssignmentOperationStatusMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAccountAssignmentsForPrincipalResponseTypeDef(TypedDict):
    AccountAssignments: List[AccountAssignmentForPrincipalTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAccountAssignmentsResponseTypeDef(TypedDict):
    AccountAssignments: List[AccountAssignmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAccountsForProvisionedPermissionSetResponseTypeDef(TypedDict):
    AccountIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListApplicationAssignmentsForPrincipalResponseTypeDef(TypedDict):
    ApplicationAssignments: List[ApplicationAssignmentForPrincipalTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListApplicationAssignmentsResponseTypeDef(TypedDict):
    ApplicationAssignments: List[ApplicationAssignmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListCustomerManagedPolicyReferencesInPermissionSetResponseTypeDef(TypedDict):
    CustomerManagedPolicyReferences: List[CustomerManagedPolicyReferenceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListManagedPoliciesInPermissionSetResponseTypeDef(TypedDict):
    AttachedManagedPolicies: List[AttachedManagedPolicyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListPermissionSetsProvisionedToAccountResponseTypeDef(TypedDict):
    PermissionSets: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListPermissionSetsResponseTypeDef(TypedDict):
    PermissionSets: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateInstanceRequestRequestTypeDef(TypedDict):
    ClientToken: NotRequired[str]
    Name: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreatePermissionSetRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    Name: str
    Description: NotRequired[str]
    RelayState: NotRequired[str]
    SessionDuration: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]
    InstanceArn: NotRequired[str]

class CreatePermissionSetResponseTypeDef(TypedDict):
    PermissionSet: PermissionSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribePermissionSetResponseTypeDef(TypedDict):
    PermissionSet: PermissionSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribePermissionSetProvisioningStatusResponseTypeDef(TypedDict):
    PermissionSetProvisioningStatus: PermissionSetProvisioningStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ProvisionPermissionSetResponseTypeDef(TypedDict):
    PermissionSetProvisioningStatus: PermissionSetProvisioningStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

IamAuthenticationMethodUnionTypeDef = Union[
    IamAuthenticationMethodTypeDef, IamAuthenticationMethodOutputTypeDef
]

class ListInstancesResponseTypeDef(TypedDict):
    Instances: List[InstanceMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAccountAssignmentCreationStatusRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    Filter: NotRequired[OperationStatusFilterTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListAccountAssignmentDeletionStatusRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    Filter: NotRequired[OperationStatusFilterTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListPermissionSetProvisioningStatusRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    Filter: NotRequired[OperationStatusFilterTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListAccountAssignmentCreationStatusRequestListAccountAssignmentCreationStatusPaginateTypeDef(
    TypedDict
):
    InstanceArn: str
    Filter: NotRequired[OperationStatusFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAccountAssignmentDeletionStatusRequestListAccountAssignmentDeletionStatusPaginateTypeDef(
    TypedDict
):
    InstanceArn: str
    Filter: NotRequired[OperationStatusFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAccountAssignmentsRequestListAccountAssignmentsPaginateTypeDef(TypedDict):
    AccountId: str
    InstanceArn: str
    PermissionSetArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAccountsForProvisionedPermissionSetRequestListAccountsForProvisionedPermissionSetPaginateTypeDef(
    TypedDict
):
    InstanceArn: str
    PermissionSetArn: str
    ProvisioningStatus: NotRequired[ProvisioningStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationAccessScopesRequestListApplicationAccessScopesPaginateTypeDef(TypedDict):
    ApplicationArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationAssignmentsRequestListApplicationAssignmentsPaginateTypeDef(TypedDict):
    ApplicationArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationAuthenticationMethodsRequestListApplicationAuthenticationMethodsPaginateTypeDef(
    TypedDict
):
    ApplicationArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationGrantsRequestListApplicationGrantsPaginateTypeDef(TypedDict):
    ApplicationArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationProvidersRequestListApplicationProvidersPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCustomerManagedPolicyReferencesInPermissionSetRequestListCustomerManagedPolicyReferencesInPermissionSetPaginateTypeDef(
    TypedDict
):
    InstanceArn: str
    PermissionSetArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListInstancesRequestListInstancesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListManagedPoliciesInPermissionSetRequestListManagedPoliciesInPermissionSetPaginateTypeDef(
    TypedDict
):
    InstanceArn: str
    PermissionSetArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPermissionSetProvisioningStatusRequestListPermissionSetProvisioningStatusPaginateTypeDef(
    TypedDict
):
    InstanceArn: str
    Filter: NotRequired[OperationStatusFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPermissionSetsProvisionedToAccountRequestListPermissionSetsProvisionedToAccountPaginateTypeDef(
    TypedDict
):
    AccountId: str
    InstanceArn: str
    ProvisioningStatus: NotRequired[ProvisioningStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPermissionSetsRequestListPermissionSetsPaginateTypeDef(TypedDict):
    InstanceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(TypedDict):
    ResourceArn: str
    InstanceArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTrustedTokenIssuersRequestListTrustedTokenIssuersPaginateTypeDef(TypedDict):
    InstanceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAccountAssignmentsForPrincipalRequestListAccountAssignmentsForPrincipalPaginateTypeDef(
    TypedDict
):
    InstanceArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType
    Filter: NotRequired[ListAccountAssignmentsFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAccountAssignmentsForPrincipalRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType
    Filter: NotRequired[ListAccountAssignmentsFilterTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListApplicationAccessScopesResponseTypeDef(TypedDict):
    Scopes: List[ScopeDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListApplicationAssignmentsForPrincipalRequestListApplicationAssignmentsForPrincipalPaginateTypeDef(
    TypedDict
):
    InstanceArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType
    Filter: NotRequired[ListApplicationAssignmentsFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationAssignmentsForPrincipalRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType
    Filter: NotRequired[ListApplicationAssignmentsFilterTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListApplicationsRequestListApplicationsPaginateTypeDef(TypedDict):
    InstanceArn: str
    Filter: NotRequired[ListApplicationsFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationsRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    Filter: NotRequired[ListApplicationsFilterTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListPermissionSetProvisioningStatusResponseTypeDef(TypedDict):
    PermissionSetsProvisioningStatus: List[PermissionSetProvisioningStatusMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTrustedTokenIssuersResponseTypeDef(TypedDict):
    TrustedTokenIssuers: List[TrustedTokenIssuerMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class TrustedTokenIssuerConfigurationTypeDef(TypedDict):
    OidcJwtConfiguration: NotRequired[OidcJwtConfigurationTypeDef]

class TrustedTokenIssuerUpdateConfigurationTypeDef(TypedDict):
    OidcJwtConfiguration: NotRequired[OidcJwtUpdateConfigurationTypeDef]

class PortalOptionsTypeDef(TypedDict):
    SignInOptions: NotRequired[SignInOptionsTypeDef]
    Visibility: NotRequired[ApplicationVisibilityType]

class UpdateApplicationPortalOptionsTypeDef(TypedDict):
    SignInOptions: NotRequired[SignInOptionsTypeDef]

class ResourceServerConfigTypeDef(TypedDict):
    Scopes: NotRequired[Dict[str, ResourceServerScopeDetailsTypeDef]]

class InstanceAccessControlAttributeConfigurationOutputTypeDef(TypedDict):
    AccessControlAttributes: List[AccessControlAttributeOutputTypeDef]

class AccessControlAttributeTypeDef(TypedDict):
    Key: str
    Value: AccessControlAttributeValueUnionTypeDef

class GetPermissionsBoundaryForPermissionSetResponseTypeDef(TypedDict):
    PermissionsBoundary: PermissionsBoundaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutPermissionsBoundaryToPermissionSetRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    PermissionsBoundary: PermissionsBoundaryTypeDef

class AuthenticationMethodItemTypeDef(TypedDict):
    AuthenticationMethod: NotRequired[AuthenticationMethodOutputTypeDef]
    AuthenticationMethodType: NotRequired[Literal["IAM"]]

class GetApplicationAuthenticationMethodResponseTypeDef(TypedDict):
    AuthenticationMethod: AuthenticationMethodOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GrantOutputTypeDef(TypedDict):
    AuthorizationCode: NotRequired[AuthorizationCodeGrantOutputTypeDef]
    JwtBearer: NotRequired[JwtBearerGrantOutputTypeDef]
    RefreshToken: NotRequired[Dict[str, Any]]
    TokenExchange: NotRequired[Dict[str, Any]]

class JwtBearerGrantTypeDef(TypedDict):
    AuthorizedTokenIssuers: NotRequired[Sequence[AuthorizedTokenIssuerUnionTypeDef]]

class AuthenticationMethodTypeDef(TypedDict):
    Iam: NotRequired[IamAuthenticationMethodUnionTypeDef]

class CreateTrustedTokenIssuerRequestRequestTypeDef(TypedDict):
    InstanceArn: str
    Name: str
    TrustedTokenIssuerConfiguration: TrustedTokenIssuerConfigurationTypeDef
    TrustedTokenIssuerType: Literal["OIDC_JWT"]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class DescribeTrustedTokenIssuerResponseTypeDef(TypedDict):
    Name: str
    TrustedTokenIssuerArn: str
    TrustedTokenIssuerConfiguration: TrustedTokenIssuerConfigurationTypeDef
    TrustedTokenIssuerType: Literal["OIDC_JWT"]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTrustedTokenIssuerRequestRequestTypeDef(TypedDict):
    TrustedTokenIssuerArn: str
    Name: NotRequired[str]
    TrustedTokenIssuerConfiguration: NotRequired[TrustedTokenIssuerUpdateConfigurationTypeDef]

class ApplicationTypeDef(TypedDict):
    ApplicationAccount: NotRequired[str]
    ApplicationArn: NotRequired[str]
    ApplicationProviderArn: NotRequired[str]
    CreatedDate: NotRequired[datetime]
    Description: NotRequired[str]
    InstanceArn: NotRequired[str]
    Name: NotRequired[str]
    PortalOptions: NotRequired[PortalOptionsTypeDef]
    Status: NotRequired[ApplicationStatusType]

class CreateApplicationRequestRequestTypeDef(TypedDict):
    ApplicationProviderArn: str
    InstanceArn: str
    Name: str
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    PortalOptions: NotRequired[PortalOptionsTypeDef]
    Status: NotRequired[ApplicationStatusType]
    Tags: NotRequired[Sequence[TagTypeDef]]

class DescribeApplicationResponseTypeDef(TypedDict):
    ApplicationAccount: str
    ApplicationArn: str
    ApplicationProviderArn: str
    CreatedDate: datetime
    Description: str
    InstanceArn: str
    Name: str
    PortalOptions: PortalOptionsTypeDef
    Status: ApplicationStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateApplicationRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    Description: NotRequired[str]
    Name: NotRequired[str]
    PortalOptions: NotRequired[UpdateApplicationPortalOptionsTypeDef]
    Status: NotRequired[ApplicationStatusType]

class ApplicationProviderTypeDef(TypedDict):
    ApplicationProviderArn: str
    DisplayData: NotRequired[DisplayDataTypeDef]
    FederationProtocol: NotRequired[FederationProtocolType]
    ResourceServerConfig: NotRequired[ResourceServerConfigTypeDef]

class DescribeApplicationProviderResponseTypeDef(TypedDict):
    ApplicationProviderArn: str
    DisplayData: DisplayDataTypeDef
    FederationProtocol: FederationProtocolType
    ResourceServerConfig: ResourceServerConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeInstanceAccessControlAttributeConfigurationResponseTypeDef(TypedDict):
    InstanceAccessControlAttributeConfiguration: (
        InstanceAccessControlAttributeConfigurationOutputTypeDef
    )
    Status: InstanceAccessControlAttributeConfigurationStatusType
    StatusReason: str
    ResponseMetadata: ResponseMetadataTypeDef

AccessControlAttributeUnionTypeDef = Union[
    AccessControlAttributeTypeDef, AccessControlAttributeOutputTypeDef
]

class ListApplicationAuthenticationMethodsResponseTypeDef(TypedDict):
    AuthenticationMethods: List[AuthenticationMethodItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetApplicationGrantResponseTypeDef(TypedDict):
    Grant: GrantOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GrantItemTypeDef(TypedDict):
    Grant: GrantOutputTypeDef
    GrantType: GrantTypeType

JwtBearerGrantUnionTypeDef = Union[JwtBearerGrantTypeDef, JwtBearerGrantOutputTypeDef]

class PutApplicationAuthenticationMethodRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    AuthenticationMethod: AuthenticationMethodTypeDef
    AuthenticationMethodType: Literal["IAM"]

class ListApplicationsResponseTypeDef(TypedDict):
    Applications: List[ApplicationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListApplicationProvidersResponseTypeDef(TypedDict):
    ApplicationProviders: List[ApplicationProviderTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class InstanceAccessControlAttributeConfigurationTypeDef(TypedDict):
    AccessControlAttributes: Sequence[AccessControlAttributeUnionTypeDef]

class ListApplicationGrantsResponseTypeDef(TypedDict):
    Grants: List[GrantItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GrantTypeDef(TypedDict):
    AuthorizationCode: NotRequired[AuthorizationCodeGrantUnionTypeDef]
    JwtBearer: NotRequired[JwtBearerGrantUnionTypeDef]
    RefreshToken: NotRequired[Mapping[str, Any]]
    TokenExchange: NotRequired[Mapping[str, Any]]

class CreateInstanceAccessControlAttributeConfigurationRequestRequestTypeDef(TypedDict):
    InstanceAccessControlAttributeConfiguration: InstanceAccessControlAttributeConfigurationTypeDef
    InstanceArn: str

class UpdateInstanceAccessControlAttributeConfigurationRequestRequestTypeDef(TypedDict):
    InstanceAccessControlAttributeConfiguration: InstanceAccessControlAttributeConfigurationTypeDef
    InstanceArn: str

class PutApplicationGrantRequestRequestTypeDef(TypedDict):
    ApplicationArn: str
    Grant: GrantTypeDef
    GrantType: GrantTypeType
