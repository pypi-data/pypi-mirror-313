"""
Type annotations for organizations service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_organizations/type_defs/)

Usage::

    ```python
    from mypy_boto3_organizations.type_defs import AcceptHandshakeRequestRequestTypeDef

    data: AcceptHandshakeRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Sequence

from .literals import (
    AccountJoinedMethodType,
    AccountStatusType,
    ActionTypeType,
    ChildTypeType,
    CreateAccountFailureReasonType,
    CreateAccountStateType,
    EffectivePolicyTypeType,
    HandshakePartyTypeType,
    HandshakeResourceTypeType,
    HandshakeStateType,
    IAMUserAccessToBillingType,
    OrganizationFeatureSetType,
    ParentTypeType,
    PolicyTypeStatusType,
    PolicyTypeType,
    TargetTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AcceptHandshakeRequestRequestTypeDef",
    "AcceptHandshakeResponseTypeDef",
    "AccountTypeDef",
    "AttachPolicyRequestRequestTypeDef",
    "CancelHandshakeRequestRequestTypeDef",
    "CancelHandshakeResponseTypeDef",
    "ChildTypeDef",
    "CloseAccountRequestRequestTypeDef",
    "CreateAccountRequestRequestTypeDef",
    "CreateAccountResponseTypeDef",
    "CreateAccountStatusTypeDef",
    "CreateGovCloudAccountRequestRequestTypeDef",
    "CreateGovCloudAccountResponseTypeDef",
    "CreateOrganizationRequestRequestTypeDef",
    "CreateOrganizationResponseTypeDef",
    "CreateOrganizationalUnitRequestRequestTypeDef",
    "CreateOrganizationalUnitResponseTypeDef",
    "CreatePolicyRequestRequestTypeDef",
    "CreatePolicyResponseTypeDef",
    "DeclineHandshakeRequestRequestTypeDef",
    "DeclineHandshakeResponseTypeDef",
    "DelegatedAdministratorTypeDef",
    "DelegatedServiceTypeDef",
    "DeleteOrganizationalUnitRequestRequestTypeDef",
    "DeletePolicyRequestRequestTypeDef",
    "DeregisterDelegatedAdministratorRequestRequestTypeDef",
    "DescribeAccountRequestRequestTypeDef",
    "DescribeAccountResponseTypeDef",
    "DescribeCreateAccountStatusRequestRequestTypeDef",
    "DescribeCreateAccountStatusResponseTypeDef",
    "DescribeEffectivePolicyRequestRequestTypeDef",
    "DescribeEffectivePolicyResponseTypeDef",
    "DescribeHandshakeRequestRequestTypeDef",
    "DescribeHandshakeResponseTypeDef",
    "DescribeOrganizationResponseTypeDef",
    "DescribeOrganizationalUnitRequestRequestTypeDef",
    "DescribeOrganizationalUnitResponseTypeDef",
    "DescribePolicyRequestRequestTypeDef",
    "DescribePolicyResponseTypeDef",
    "DescribeResourcePolicyResponseTypeDef",
    "DetachPolicyRequestRequestTypeDef",
    "DisableAWSServiceAccessRequestRequestTypeDef",
    "DisablePolicyTypeRequestRequestTypeDef",
    "DisablePolicyTypeResponseTypeDef",
    "EffectivePolicyTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnableAWSServiceAccessRequestRequestTypeDef",
    "EnableAllFeaturesResponseTypeDef",
    "EnablePolicyTypeRequestRequestTypeDef",
    "EnablePolicyTypeResponseTypeDef",
    "EnabledServicePrincipalTypeDef",
    "HandshakeFilterTypeDef",
    "HandshakePaginatorTypeDef",
    "HandshakePartyTypeDef",
    "HandshakeResourcePaginatorTypeDef",
    "HandshakeResourceTypeDef",
    "HandshakeTypeDef",
    "InviteAccountToOrganizationRequestRequestTypeDef",
    "InviteAccountToOrganizationResponseTypeDef",
    "ListAWSServiceAccessForOrganizationRequestListAWSServiceAccessForOrganizationPaginateTypeDef",
    "ListAWSServiceAccessForOrganizationRequestRequestTypeDef",
    "ListAWSServiceAccessForOrganizationResponseTypeDef",
    "ListAccountsForParentRequestListAccountsForParentPaginateTypeDef",
    "ListAccountsForParentRequestRequestTypeDef",
    "ListAccountsForParentResponseTypeDef",
    "ListAccountsRequestListAccountsPaginateTypeDef",
    "ListAccountsRequestRequestTypeDef",
    "ListAccountsResponseTypeDef",
    "ListChildrenRequestListChildrenPaginateTypeDef",
    "ListChildrenRequestRequestTypeDef",
    "ListChildrenResponseTypeDef",
    "ListCreateAccountStatusRequestListCreateAccountStatusPaginateTypeDef",
    "ListCreateAccountStatusRequestRequestTypeDef",
    "ListCreateAccountStatusResponseTypeDef",
    "ListDelegatedAdministratorsRequestListDelegatedAdministratorsPaginateTypeDef",
    "ListDelegatedAdministratorsRequestRequestTypeDef",
    "ListDelegatedAdministratorsResponseTypeDef",
    "ListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef",
    "ListDelegatedServicesForAccountRequestRequestTypeDef",
    "ListDelegatedServicesForAccountResponseTypeDef",
    "ListHandshakesForAccountRequestListHandshakesForAccountPaginateTypeDef",
    "ListHandshakesForAccountRequestRequestTypeDef",
    "ListHandshakesForAccountResponsePaginatorTypeDef",
    "ListHandshakesForAccountResponseTypeDef",
    "ListHandshakesForOrganizationRequestListHandshakesForOrganizationPaginateTypeDef",
    "ListHandshakesForOrganizationRequestRequestTypeDef",
    "ListHandshakesForOrganizationResponsePaginatorTypeDef",
    "ListHandshakesForOrganizationResponseTypeDef",
    "ListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef",
    "ListOrganizationalUnitsForParentRequestRequestTypeDef",
    "ListOrganizationalUnitsForParentResponseTypeDef",
    "ListParentsRequestListParentsPaginateTypeDef",
    "ListParentsRequestRequestTypeDef",
    "ListParentsResponseTypeDef",
    "ListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef",
    "ListPoliciesForTargetRequestRequestTypeDef",
    "ListPoliciesForTargetResponseTypeDef",
    "ListPoliciesRequestListPoliciesPaginateTypeDef",
    "ListPoliciesRequestRequestTypeDef",
    "ListPoliciesResponseTypeDef",
    "ListRootsRequestListRootsPaginateTypeDef",
    "ListRootsRequestRequestTypeDef",
    "ListRootsResponseTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef",
    "ListTargetsForPolicyRequestRequestTypeDef",
    "ListTargetsForPolicyResponseTypeDef",
    "MoveAccountRequestRequestTypeDef",
    "OrganizationTypeDef",
    "OrganizationalUnitTypeDef",
    "PaginatorConfigTypeDef",
    "ParentTypeDef",
    "PolicySummaryTypeDef",
    "PolicyTargetSummaryTypeDef",
    "PolicyTypeDef",
    "PolicyTypeSummaryTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "PutResourcePolicyResponseTypeDef",
    "RegisterDelegatedAdministratorRequestRequestTypeDef",
    "RemoveAccountFromOrganizationRequestRequestTypeDef",
    "ResourcePolicySummaryTypeDef",
    "ResourcePolicyTypeDef",
    "ResponseMetadataTypeDef",
    "RootTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateOrganizationalUnitRequestRequestTypeDef",
    "UpdateOrganizationalUnitResponseTypeDef",
    "UpdatePolicyRequestRequestTypeDef",
    "UpdatePolicyResponseTypeDef",
)


class AcceptHandshakeRequestRequestTypeDef(TypedDict):
    HandshakeId: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AccountTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Email: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[AccountStatusType]
    JoinedMethod: NotRequired[AccountJoinedMethodType]
    JoinedTimestamp: NotRequired[datetime]


class AttachPolicyRequestRequestTypeDef(TypedDict):
    PolicyId: str
    TargetId: str


class CancelHandshakeRequestRequestTypeDef(TypedDict):
    HandshakeId: str


ChildTypeDef = TypedDict(
    "ChildTypeDef",
    {
        "Id": NotRequired[str],
        "Type": NotRequired[ChildTypeType],
    },
)


class CloseAccountRequestRequestTypeDef(TypedDict):
    AccountId: str


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class CreateAccountStatusTypeDef(TypedDict):
    Id: NotRequired[str]
    AccountName: NotRequired[str]
    State: NotRequired[CreateAccountStateType]
    RequestedTimestamp: NotRequired[datetime]
    CompletedTimestamp: NotRequired[datetime]
    AccountId: NotRequired[str]
    GovCloudAccountId: NotRequired[str]
    FailureReason: NotRequired[CreateAccountFailureReasonType]


class CreateOrganizationRequestRequestTypeDef(TypedDict):
    FeatureSet: NotRequired[OrganizationFeatureSetType]


class OrganizationalUnitTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]


class DeclineHandshakeRequestRequestTypeDef(TypedDict):
    HandshakeId: str


class DelegatedAdministratorTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Email: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[AccountStatusType]
    JoinedMethod: NotRequired[AccountJoinedMethodType]
    JoinedTimestamp: NotRequired[datetime]
    DelegationEnabledDate: NotRequired[datetime]


class DelegatedServiceTypeDef(TypedDict):
    ServicePrincipal: NotRequired[str]
    DelegationEnabledDate: NotRequired[datetime]


class DeleteOrganizationalUnitRequestRequestTypeDef(TypedDict):
    OrganizationalUnitId: str


class DeletePolicyRequestRequestTypeDef(TypedDict):
    PolicyId: str


class DeregisterDelegatedAdministratorRequestRequestTypeDef(TypedDict):
    AccountId: str
    ServicePrincipal: str


class DescribeAccountRequestRequestTypeDef(TypedDict):
    AccountId: str


class DescribeCreateAccountStatusRequestRequestTypeDef(TypedDict):
    CreateAccountRequestId: str


class DescribeEffectivePolicyRequestRequestTypeDef(TypedDict):
    PolicyType: EffectivePolicyTypeType
    TargetId: NotRequired[str]


class EffectivePolicyTypeDef(TypedDict):
    PolicyContent: NotRequired[str]
    LastUpdatedTimestamp: NotRequired[datetime]
    TargetId: NotRequired[str]
    PolicyType: NotRequired[EffectivePolicyTypeType]


class DescribeHandshakeRequestRequestTypeDef(TypedDict):
    HandshakeId: str


class DescribeOrganizationalUnitRequestRequestTypeDef(TypedDict):
    OrganizationalUnitId: str


class DescribePolicyRequestRequestTypeDef(TypedDict):
    PolicyId: str


class DetachPolicyRequestRequestTypeDef(TypedDict):
    PolicyId: str
    TargetId: str


class DisableAWSServiceAccessRequestRequestTypeDef(TypedDict):
    ServicePrincipal: str


class DisablePolicyTypeRequestRequestTypeDef(TypedDict):
    RootId: str
    PolicyType: PolicyTypeType


class EnableAWSServiceAccessRequestRequestTypeDef(TypedDict):
    ServicePrincipal: str


class EnablePolicyTypeRequestRequestTypeDef(TypedDict):
    RootId: str
    PolicyType: PolicyTypeType


class EnabledServicePrincipalTypeDef(TypedDict):
    ServicePrincipal: NotRequired[str]
    DateEnabled: NotRequired[datetime]


class HandshakeFilterTypeDef(TypedDict):
    ActionType: NotRequired[ActionTypeType]
    ParentHandshakeId: NotRequired[str]


HandshakePartyTypeDef = TypedDict(
    "HandshakePartyTypeDef",
    {
        "Id": str,
        "Type": HandshakePartyTypeType,
    },
)
HandshakeResourcePaginatorTypeDef = TypedDict(
    "HandshakeResourcePaginatorTypeDef",
    {
        "Value": NotRequired[str],
        "Type": NotRequired[HandshakeResourceTypeType],
        "Resources": NotRequired[List[Dict[str, Any]]],
    },
)
HandshakeResourceTypeDef = TypedDict(
    "HandshakeResourceTypeDef",
    {
        "Value": NotRequired[str],
        "Type": NotRequired[HandshakeResourceTypeType],
        "Resources": NotRequired[List[Dict[str, Any]]],
    },
)


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAWSServiceAccessForOrganizationRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListAccountsForParentRequestRequestTypeDef(TypedDict):
    ParentId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListAccountsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListChildrenRequestRequestTypeDef(TypedDict):
    ParentId: str
    ChildType: ChildTypeType
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListCreateAccountStatusRequestRequestTypeDef(TypedDict):
    States: NotRequired[Sequence[CreateAccountStateType]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDelegatedAdministratorsRequestRequestTypeDef(TypedDict):
    ServicePrincipal: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDelegatedServicesForAccountRequestRequestTypeDef(TypedDict):
    AccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListOrganizationalUnitsForParentRequestRequestTypeDef(TypedDict):
    ParentId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListParentsRequestRequestTypeDef(TypedDict):
    ChildId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


ParentTypeDef = TypedDict(
    "ParentTypeDef",
    {
        "Id": NotRequired[str],
        "Type": NotRequired[ParentTypeType],
    },
)


class ListPoliciesForTargetRequestRequestTypeDef(TypedDict):
    TargetId: str
    Filter: PolicyTypeType
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


PolicySummaryTypeDef = TypedDict(
    "PolicySummaryTypeDef",
    {
        "Id": NotRequired[str],
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "Type": NotRequired[PolicyTypeType],
        "AwsManaged": NotRequired[bool],
    },
)


class ListPoliciesRequestRequestTypeDef(TypedDict):
    Filter: PolicyTypeType
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListRootsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceId: str
    NextToken: NotRequired[str]


class ListTargetsForPolicyRequestRequestTypeDef(TypedDict):
    PolicyId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


PolicyTargetSummaryTypeDef = TypedDict(
    "PolicyTargetSummaryTypeDef",
    {
        "TargetId": NotRequired[str],
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[TargetTypeType],
    },
)


class MoveAccountRequestRequestTypeDef(TypedDict):
    AccountId: str
    SourceParentId: str
    DestinationParentId: str


PolicyTypeSummaryTypeDef = TypedDict(
    "PolicyTypeSummaryTypeDef",
    {
        "Type": NotRequired[PolicyTypeType],
        "Status": NotRequired[PolicyTypeStatusType],
    },
)


class RegisterDelegatedAdministratorRequestRequestTypeDef(TypedDict):
    AccountId: str
    ServicePrincipal: str


class RemoveAccountFromOrganizationRequestRequestTypeDef(TypedDict):
    AccountId: str


class ResourcePolicySummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceId: str
    TagKeys: Sequence[str]


class UpdateOrganizationalUnitRequestRequestTypeDef(TypedDict):
    OrganizationalUnitId: str
    Name: NotRequired[str]


class UpdatePolicyRequestRequestTypeDef(TypedDict):
    PolicyId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    Content: NotRequired[str]


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAccountResponseTypeDef(TypedDict):
    Account: AccountTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAccountsForParentResponseTypeDef(TypedDict):
    Accounts: List[AccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListAccountsResponseTypeDef(TypedDict):
    Accounts: List[AccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListChildrenResponseTypeDef(TypedDict):
    Children: List[ChildTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateAccountRequestRequestTypeDef(TypedDict):
    Email: str
    AccountName: str
    RoleName: NotRequired[str]
    IamUserAccessToBilling: NotRequired[IAMUserAccessToBillingType]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateGovCloudAccountRequestRequestTypeDef(TypedDict):
    Email: str
    AccountName: str
    RoleName: NotRequired[str]
    IamUserAccessToBilling: NotRequired[IAMUserAccessToBillingType]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateOrganizationalUnitRequestRequestTypeDef(TypedDict):
    ParentId: str
    Name: str
    Tags: NotRequired[Sequence[TagTypeDef]]


CreatePolicyRequestRequestTypeDef = TypedDict(
    "CreatePolicyRequestRequestTypeDef",
    {
        "Content": str,
        "Description": str,
        "Name": str,
        "Type": PolicyTypeType,
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PutResourcePolicyRequestRequestTypeDef(TypedDict):
    Content: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceId: str
    Tags: Sequence[TagTypeDef]


class CreateAccountResponseTypeDef(TypedDict):
    CreateAccountStatus: CreateAccountStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateGovCloudAccountResponseTypeDef(TypedDict):
    CreateAccountStatus: CreateAccountStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCreateAccountStatusResponseTypeDef(TypedDict):
    CreateAccountStatus: CreateAccountStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListCreateAccountStatusResponseTypeDef(TypedDict):
    CreateAccountStatuses: List[CreateAccountStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateOrganizationalUnitResponseTypeDef(TypedDict):
    OrganizationalUnit: OrganizationalUnitTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeOrganizationalUnitResponseTypeDef(TypedDict):
    OrganizationalUnit: OrganizationalUnitTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListOrganizationalUnitsForParentResponseTypeDef(TypedDict):
    OrganizationalUnits: List[OrganizationalUnitTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateOrganizationalUnitResponseTypeDef(TypedDict):
    OrganizationalUnit: OrganizationalUnitTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDelegatedAdministratorsResponseTypeDef(TypedDict):
    DelegatedAdministrators: List[DelegatedAdministratorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListDelegatedServicesForAccountResponseTypeDef(TypedDict):
    DelegatedServices: List[DelegatedServiceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeEffectivePolicyResponseTypeDef(TypedDict):
    EffectivePolicy: EffectivePolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAWSServiceAccessForOrganizationResponseTypeDef(TypedDict):
    EnabledServicePrincipals: List[EnabledServicePrincipalTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListHandshakesForAccountRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[HandshakeFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListHandshakesForOrganizationRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[HandshakeFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class InviteAccountToOrganizationRequestRequestTypeDef(TypedDict):
    Target: HandshakePartyTypeDef
    Notes: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class HandshakePaginatorTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Parties: NotRequired[List[HandshakePartyTypeDef]]
    State: NotRequired[HandshakeStateType]
    RequestedTimestamp: NotRequired[datetime]
    ExpirationTimestamp: NotRequired[datetime]
    Action: NotRequired[ActionTypeType]
    Resources: NotRequired[List[HandshakeResourcePaginatorTypeDef]]


class HandshakeTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Parties: NotRequired[List[HandshakePartyTypeDef]]
    State: NotRequired[HandshakeStateType]
    RequestedTimestamp: NotRequired[datetime]
    ExpirationTimestamp: NotRequired[datetime]
    Action: NotRequired[ActionTypeType]
    Resources: NotRequired[List[HandshakeResourceTypeDef]]


class ListAWSServiceAccessForOrganizationRequestListAWSServiceAccessForOrganizationPaginateTypeDef(
    TypedDict
):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAccountsForParentRequestListAccountsForParentPaginateTypeDef(TypedDict):
    ParentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAccountsRequestListAccountsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListChildrenRequestListChildrenPaginateTypeDef(TypedDict):
    ParentId: str
    ChildType: ChildTypeType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCreateAccountStatusRequestListCreateAccountStatusPaginateTypeDef(TypedDict):
    States: NotRequired[Sequence[CreateAccountStateType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDelegatedAdministratorsRequestListDelegatedAdministratorsPaginateTypeDef(TypedDict):
    ServicePrincipal: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef(
    TypedDict
):
    AccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListHandshakesForAccountRequestListHandshakesForAccountPaginateTypeDef(TypedDict):
    Filter: NotRequired[HandshakeFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListHandshakesForOrganizationRequestListHandshakesForOrganizationPaginateTypeDef(TypedDict):
    Filter: NotRequired[HandshakeFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef(
    TypedDict
):
    ParentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListParentsRequestListParentsPaginateTypeDef(TypedDict):
    ChildId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef(TypedDict):
    TargetId: str
    Filter: PolicyTypeType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPoliciesRequestListPoliciesPaginateTypeDef(TypedDict):
    Filter: PolicyTypeType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRootsRequestListRootsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(TypedDict):
    ResourceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef(TypedDict):
    PolicyId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListParentsResponseTypeDef(TypedDict):
    Parents: List[ParentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPoliciesForTargetResponseTypeDef(TypedDict):
    Policies: List[PolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPoliciesResponseTypeDef(TypedDict):
    Policies: List[PolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PolicyTypeDef(TypedDict):
    PolicySummary: NotRequired[PolicySummaryTypeDef]
    Content: NotRequired[str]


class ListTargetsForPolicyResponseTypeDef(TypedDict):
    Targets: List[PolicyTargetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class OrganizationTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    FeatureSet: NotRequired[OrganizationFeatureSetType]
    MasterAccountArn: NotRequired[str]
    MasterAccountId: NotRequired[str]
    MasterAccountEmail: NotRequired[str]
    AvailablePolicyTypes: NotRequired[List[PolicyTypeSummaryTypeDef]]


class RootTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    PolicyTypes: NotRequired[List[PolicyTypeSummaryTypeDef]]


class ResourcePolicyTypeDef(TypedDict):
    ResourcePolicySummary: NotRequired[ResourcePolicySummaryTypeDef]
    Content: NotRequired[str]


class ListHandshakesForAccountResponsePaginatorTypeDef(TypedDict):
    Handshakes: List[HandshakePaginatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListHandshakesForOrganizationResponsePaginatorTypeDef(TypedDict):
    Handshakes: List[HandshakePaginatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AcceptHandshakeResponseTypeDef(TypedDict):
    Handshake: HandshakeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CancelHandshakeResponseTypeDef(TypedDict):
    Handshake: HandshakeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeclineHandshakeResponseTypeDef(TypedDict):
    Handshake: HandshakeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeHandshakeResponseTypeDef(TypedDict):
    Handshake: HandshakeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class EnableAllFeaturesResponseTypeDef(TypedDict):
    Handshake: HandshakeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class InviteAccountToOrganizationResponseTypeDef(TypedDict):
    Handshake: HandshakeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListHandshakesForAccountResponseTypeDef(TypedDict):
    Handshakes: List[HandshakeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListHandshakesForOrganizationResponseTypeDef(TypedDict):
    Handshakes: List[HandshakeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreatePolicyResponseTypeDef(TypedDict):
    Policy: PolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePolicyResponseTypeDef(TypedDict):
    Policy: PolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePolicyResponseTypeDef(TypedDict):
    Policy: PolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateOrganizationResponseTypeDef(TypedDict):
    Organization: OrganizationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeOrganizationResponseTypeDef(TypedDict):
    Organization: OrganizationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisablePolicyTypeResponseTypeDef(TypedDict):
    Root: RootTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class EnablePolicyTypeResponseTypeDef(TypedDict):
    Root: RootTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListRootsResponseTypeDef(TypedDict):
    Roots: List[RootTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeResourcePolicyResponseTypeDef(TypedDict):
    ResourcePolicy: ResourcePolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutResourcePolicyResponseTypeDef(TypedDict):
    ResourcePolicy: ResourcePolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
