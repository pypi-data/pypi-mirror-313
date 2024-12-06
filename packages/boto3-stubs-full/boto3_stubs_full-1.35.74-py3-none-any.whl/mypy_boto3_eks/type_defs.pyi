"""
Type annotations for eks service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/type_defs/)

Usage::

    ```python
    from mypy_boto3_eks.type_defs import AccessConfigResponseTypeDef

    data: AccessConfigResponseTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AccessScopeTypeType,
    AddonIssueCodeType,
    AddonStatusType,
    AMITypesType,
    AuthenticationModeType,
    CapacityTypesType,
    ClusterIssueCodeType,
    ClusterStatusType,
    ConfigStatusType,
    ConnectorConfigProviderType,
    EksAnywhereSubscriptionStatusType,
    ErrorCodeType,
    FargateProfileIssueCodeType,
    FargateProfileStatusType,
    InsightStatusValueType,
    IpFamilyType,
    LogTypeType,
    NodegroupIssueCodeType,
    NodegroupStatusType,
    ResolveConflictsType,
    SupportTypeType,
    TaintEffectType,
    UpdateParamTypeType,
    UpdateStatusType,
    UpdateTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccessConfigResponseTypeDef",
    "AccessEntryTypeDef",
    "AccessPolicyTypeDef",
    "AccessScopeOutputTypeDef",
    "AccessScopeTypeDef",
    "AddonHealthTypeDef",
    "AddonInfoTypeDef",
    "AddonIssueTypeDef",
    "AddonPodIdentityAssociationsTypeDef",
    "AddonPodIdentityConfigurationTypeDef",
    "AddonTypeDef",
    "AddonVersionInfoTypeDef",
    "AssociateAccessPolicyRequestRequestTypeDef",
    "AssociateAccessPolicyResponseTypeDef",
    "AssociateEncryptionConfigRequestRequestTypeDef",
    "AssociateEncryptionConfigResponseTypeDef",
    "AssociateIdentityProviderConfigRequestRequestTypeDef",
    "AssociateIdentityProviderConfigResponseTypeDef",
    "AssociatedAccessPolicyTypeDef",
    "AutoScalingGroupTypeDef",
    "BlockStorageTypeDef",
    "CertificateTypeDef",
    "ClientStatTypeDef",
    "ClusterHealthTypeDef",
    "ClusterIssueTypeDef",
    "ClusterTypeDef",
    "CompatibilityTypeDef",
    "ComputeConfigRequestTypeDef",
    "ComputeConfigResponseTypeDef",
    "ConnectorConfigRequestTypeDef",
    "ConnectorConfigResponseTypeDef",
    "ControlPlanePlacementRequestTypeDef",
    "ControlPlanePlacementResponseTypeDef",
    "CreateAccessConfigRequestTypeDef",
    "CreateAccessEntryRequestRequestTypeDef",
    "CreateAccessEntryResponseTypeDef",
    "CreateAddonRequestRequestTypeDef",
    "CreateAddonResponseTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "CreateClusterResponseTypeDef",
    "CreateEksAnywhereSubscriptionRequestRequestTypeDef",
    "CreateEksAnywhereSubscriptionResponseTypeDef",
    "CreateFargateProfileRequestRequestTypeDef",
    "CreateFargateProfileResponseTypeDef",
    "CreateNodegroupRequestRequestTypeDef",
    "CreateNodegroupResponseTypeDef",
    "CreatePodIdentityAssociationRequestRequestTypeDef",
    "CreatePodIdentityAssociationResponseTypeDef",
    "DeleteAccessEntryRequestRequestTypeDef",
    "DeleteAddonRequestRequestTypeDef",
    "DeleteAddonResponseTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteClusterResponseTypeDef",
    "DeleteEksAnywhereSubscriptionRequestRequestTypeDef",
    "DeleteEksAnywhereSubscriptionResponseTypeDef",
    "DeleteFargateProfileRequestRequestTypeDef",
    "DeleteFargateProfileResponseTypeDef",
    "DeleteNodegroupRequestRequestTypeDef",
    "DeleteNodegroupResponseTypeDef",
    "DeletePodIdentityAssociationRequestRequestTypeDef",
    "DeletePodIdentityAssociationResponseTypeDef",
    "DeprecationDetailTypeDef",
    "DeregisterClusterRequestRequestTypeDef",
    "DeregisterClusterResponseTypeDef",
    "DescribeAccessEntryRequestRequestTypeDef",
    "DescribeAccessEntryResponseTypeDef",
    "DescribeAddonConfigurationRequestRequestTypeDef",
    "DescribeAddonConfigurationResponseTypeDef",
    "DescribeAddonRequestAddonActiveWaitTypeDef",
    "DescribeAddonRequestAddonDeletedWaitTypeDef",
    "DescribeAddonRequestRequestTypeDef",
    "DescribeAddonResponseTypeDef",
    "DescribeAddonVersionsRequestDescribeAddonVersionsPaginateTypeDef",
    "DescribeAddonVersionsRequestRequestTypeDef",
    "DescribeAddonVersionsResponseTypeDef",
    "DescribeClusterRequestClusterActiveWaitTypeDef",
    "DescribeClusterRequestClusterDeletedWaitTypeDef",
    "DescribeClusterRequestRequestTypeDef",
    "DescribeClusterResponseTypeDef",
    "DescribeEksAnywhereSubscriptionRequestRequestTypeDef",
    "DescribeEksAnywhereSubscriptionResponseTypeDef",
    "DescribeFargateProfileRequestFargateProfileActiveWaitTypeDef",
    "DescribeFargateProfileRequestFargateProfileDeletedWaitTypeDef",
    "DescribeFargateProfileRequestRequestTypeDef",
    "DescribeFargateProfileResponseTypeDef",
    "DescribeIdentityProviderConfigRequestRequestTypeDef",
    "DescribeIdentityProviderConfigResponseTypeDef",
    "DescribeInsightRequestRequestTypeDef",
    "DescribeInsightResponseTypeDef",
    "DescribeNodegroupRequestNodegroupActiveWaitTypeDef",
    "DescribeNodegroupRequestNodegroupDeletedWaitTypeDef",
    "DescribeNodegroupRequestRequestTypeDef",
    "DescribeNodegroupResponseTypeDef",
    "DescribePodIdentityAssociationRequestRequestTypeDef",
    "DescribePodIdentityAssociationResponseTypeDef",
    "DescribeUpdateRequestRequestTypeDef",
    "DescribeUpdateResponseTypeDef",
    "DisassociateAccessPolicyRequestRequestTypeDef",
    "DisassociateIdentityProviderConfigRequestRequestTypeDef",
    "DisassociateIdentityProviderConfigResponseTypeDef",
    "EksAnywhereSubscriptionTermTypeDef",
    "EksAnywhereSubscriptionTypeDef",
    "ElasticLoadBalancingTypeDef",
    "EncryptionConfigOutputTypeDef",
    "EncryptionConfigTypeDef",
    "EncryptionConfigUnionTypeDef",
    "ErrorDetailTypeDef",
    "FargateProfileHealthTypeDef",
    "FargateProfileIssueTypeDef",
    "FargateProfileSelectorOutputTypeDef",
    "FargateProfileSelectorTypeDef",
    "FargateProfileSelectorUnionTypeDef",
    "FargateProfileTypeDef",
    "IdentityProviderConfigResponseTypeDef",
    "IdentityProviderConfigTypeDef",
    "IdentityTypeDef",
    "InsightCategorySpecificSummaryTypeDef",
    "InsightResourceDetailTypeDef",
    "InsightStatusTypeDef",
    "InsightSummaryTypeDef",
    "InsightTypeDef",
    "InsightsFilterTypeDef",
    "IssueTypeDef",
    "KubernetesNetworkConfigRequestTypeDef",
    "KubernetesNetworkConfigResponseTypeDef",
    "LaunchTemplateSpecificationTypeDef",
    "ListAccessEntriesRequestListAccessEntriesPaginateTypeDef",
    "ListAccessEntriesRequestRequestTypeDef",
    "ListAccessEntriesResponseTypeDef",
    "ListAccessPoliciesRequestListAccessPoliciesPaginateTypeDef",
    "ListAccessPoliciesRequestRequestTypeDef",
    "ListAccessPoliciesResponseTypeDef",
    "ListAddonsRequestListAddonsPaginateTypeDef",
    "ListAddonsRequestRequestTypeDef",
    "ListAddonsResponseTypeDef",
    "ListAssociatedAccessPoliciesRequestListAssociatedAccessPoliciesPaginateTypeDef",
    "ListAssociatedAccessPoliciesRequestRequestTypeDef",
    "ListAssociatedAccessPoliciesResponseTypeDef",
    "ListClustersRequestListClustersPaginateTypeDef",
    "ListClustersRequestRequestTypeDef",
    "ListClustersResponseTypeDef",
    "ListEksAnywhereSubscriptionsRequestListEksAnywhereSubscriptionsPaginateTypeDef",
    "ListEksAnywhereSubscriptionsRequestRequestTypeDef",
    "ListEksAnywhereSubscriptionsResponseTypeDef",
    "ListFargateProfilesRequestListFargateProfilesPaginateTypeDef",
    "ListFargateProfilesRequestRequestTypeDef",
    "ListFargateProfilesResponseTypeDef",
    "ListIdentityProviderConfigsRequestListIdentityProviderConfigsPaginateTypeDef",
    "ListIdentityProviderConfigsRequestRequestTypeDef",
    "ListIdentityProviderConfigsResponseTypeDef",
    "ListInsightsRequestListInsightsPaginateTypeDef",
    "ListInsightsRequestRequestTypeDef",
    "ListInsightsResponseTypeDef",
    "ListNodegroupsRequestListNodegroupsPaginateTypeDef",
    "ListNodegroupsRequestRequestTypeDef",
    "ListNodegroupsResponseTypeDef",
    "ListPodIdentityAssociationsRequestListPodIdentityAssociationsPaginateTypeDef",
    "ListPodIdentityAssociationsRequestRequestTypeDef",
    "ListPodIdentityAssociationsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListUpdatesRequestListUpdatesPaginateTypeDef",
    "ListUpdatesRequestRequestTypeDef",
    "ListUpdatesResponseTypeDef",
    "LogSetupOutputTypeDef",
    "LogSetupTypeDef",
    "LogSetupUnionTypeDef",
    "LoggingOutputTypeDef",
    "LoggingTypeDef",
    "MarketplaceInformationTypeDef",
    "NodegroupHealthTypeDef",
    "NodegroupResourcesTypeDef",
    "NodegroupScalingConfigTypeDef",
    "NodegroupTypeDef",
    "NodegroupUpdateConfigTypeDef",
    "OIDCTypeDef",
    "OidcIdentityProviderConfigRequestTypeDef",
    "OidcIdentityProviderConfigTypeDef",
    "OutpostConfigRequestTypeDef",
    "OutpostConfigResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PodIdentityAssociationSummaryTypeDef",
    "PodIdentityAssociationTypeDef",
    "ProviderTypeDef",
    "RegisterClusterRequestRequestTypeDef",
    "RegisterClusterResponseTypeDef",
    "RemoteAccessConfigOutputTypeDef",
    "RemoteAccessConfigTypeDef",
    "RemoteNetworkConfigRequestTypeDef",
    "RemoteNetworkConfigResponseTypeDef",
    "RemoteNodeNetworkOutputTypeDef",
    "RemoteNodeNetworkTypeDef",
    "RemoteNodeNetworkUnionTypeDef",
    "RemotePodNetworkOutputTypeDef",
    "RemotePodNetworkTypeDef",
    "RemotePodNetworkUnionTypeDef",
    "ResponseMetadataTypeDef",
    "StorageConfigRequestTypeDef",
    "StorageConfigResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TaintTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAccessConfigRequestTypeDef",
    "UpdateAccessEntryRequestRequestTypeDef",
    "UpdateAccessEntryResponseTypeDef",
    "UpdateAddonRequestRequestTypeDef",
    "UpdateAddonResponseTypeDef",
    "UpdateClusterConfigRequestRequestTypeDef",
    "UpdateClusterConfigResponseTypeDef",
    "UpdateClusterVersionRequestRequestTypeDef",
    "UpdateClusterVersionResponseTypeDef",
    "UpdateEksAnywhereSubscriptionRequestRequestTypeDef",
    "UpdateEksAnywhereSubscriptionResponseTypeDef",
    "UpdateLabelsPayloadTypeDef",
    "UpdateNodegroupConfigRequestRequestTypeDef",
    "UpdateNodegroupConfigResponseTypeDef",
    "UpdateNodegroupVersionRequestRequestTypeDef",
    "UpdateNodegroupVersionResponseTypeDef",
    "UpdateParamTypeDef",
    "UpdatePodIdentityAssociationRequestRequestTypeDef",
    "UpdatePodIdentityAssociationResponseTypeDef",
    "UpdateTaintsPayloadTypeDef",
    "UpdateTypeDef",
    "UpgradePolicyRequestTypeDef",
    "UpgradePolicyResponseTypeDef",
    "VpcConfigRequestTypeDef",
    "VpcConfigResponseTypeDef",
    "WaiterConfigTypeDef",
    "ZonalShiftConfigRequestTypeDef",
    "ZonalShiftConfigResponseTypeDef",
)

class AccessConfigResponseTypeDef(TypedDict):
    bootstrapClusterCreatorAdminPermissions: NotRequired[bool]
    authenticationMode: NotRequired[AuthenticationModeType]

AccessEntryTypeDef = TypedDict(
    "AccessEntryTypeDef",
    {
        "clusterName": NotRequired[str],
        "principalArn": NotRequired[str],
        "kubernetesGroups": NotRequired[List[str]],
        "accessEntryArn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "modifiedAt": NotRequired[datetime],
        "tags": NotRequired[Dict[str, str]],
        "username": NotRequired[str],
        "type": NotRequired[str],
    },
)

class AccessPolicyTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]

AccessScopeOutputTypeDef = TypedDict(
    "AccessScopeOutputTypeDef",
    {
        "type": NotRequired[AccessScopeTypeType],
        "namespaces": NotRequired[List[str]],
    },
)
AccessScopeTypeDef = TypedDict(
    "AccessScopeTypeDef",
    {
        "type": NotRequired[AccessScopeTypeType],
        "namespaces": NotRequired[Sequence[str]],
    },
)

class AddonIssueTypeDef(TypedDict):
    code: NotRequired[AddonIssueCodeType]
    message: NotRequired[str]
    resourceIds: NotRequired[List[str]]

class MarketplaceInformationTypeDef(TypedDict):
    productId: NotRequired[str]
    productUrl: NotRequired[str]

class AddonPodIdentityAssociationsTypeDef(TypedDict):
    serviceAccount: str
    roleArn: str

class AddonPodIdentityConfigurationTypeDef(TypedDict):
    serviceAccount: NotRequired[str]
    recommendedManagedPolicies: NotRequired[List[str]]

class CompatibilityTypeDef(TypedDict):
    clusterVersion: NotRequired[str]
    platformVersions: NotRequired[List[str]]
    defaultVersion: NotRequired[bool]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class OidcIdentityProviderConfigRequestTypeDef(TypedDict):
    identityProviderConfigName: str
    issuerUrl: str
    clientId: str
    usernameClaim: NotRequired[str]
    usernamePrefix: NotRequired[str]
    groupsClaim: NotRequired[str]
    groupsPrefix: NotRequired[str]
    requiredClaims: NotRequired[Mapping[str, str]]

class AutoScalingGroupTypeDef(TypedDict):
    name: NotRequired[str]

class BlockStorageTypeDef(TypedDict):
    enabled: NotRequired[bool]

class CertificateTypeDef(TypedDict):
    data: NotRequired[str]

class ClientStatTypeDef(TypedDict):
    userAgent: NotRequired[str]
    numberOfRequestsLast30Days: NotRequired[int]
    lastRequestTime: NotRequired[datetime]

class ClusterIssueTypeDef(TypedDict):
    code: NotRequired[ClusterIssueCodeType]
    message: NotRequired[str]
    resourceIds: NotRequired[List[str]]

class ComputeConfigResponseTypeDef(TypedDict):
    enabled: NotRequired[bool]
    nodePools: NotRequired[List[str]]
    nodeRoleArn: NotRequired[str]

class ConnectorConfigResponseTypeDef(TypedDict):
    activationId: NotRequired[str]
    activationCode: NotRequired[str]
    activationExpiry: NotRequired[datetime]
    provider: NotRequired[str]
    roleArn: NotRequired[str]

class UpgradePolicyResponseTypeDef(TypedDict):
    supportType: NotRequired[SupportTypeType]

class VpcConfigResponseTypeDef(TypedDict):
    subnetIds: NotRequired[List[str]]
    securityGroupIds: NotRequired[List[str]]
    clusterSecurityGroupId: NotRequired[str]
    vpcId: NotRequired[str]
    endpointPublicAccess: NotRequired[bool]
    endpointPrivateAccess: NotRequired[bool]
    publicAccessCidrs: NotRequired[List[str]]

class ZonalShiftConfigResponseTypeDef(TypedDict):
    enabled: NotRequired[bool]

class ComputeConfigRequestTypeDef(TypedDict):
    enabled: NotRequired[bool]
    nodePools: NotRequired[Sequence[str]]
    nodeRoleArn: NotRequired[str]

class ConnectorConfigRequestTypeDef(TypedDict):
    roleArn: str
    provider: ConnectorConfigProviderType

class ControlPlanePlacementRequestTypeDef(TypedDict):
    groupName: NotRequired[str]

class ControlPlanePlacementResponseTypeDef(TypedDict):
    groupName: NotRequired[str]

class CreateAccessConfigRequestTypeDef(TypedDict):
    bootstrapClusterCreatorAdminPermissions: NotRequired[bool]
    authenticationMode: NotRequired[AuthenticationModeType]

CreateAccessEntryRequestRequestTypeDef = TypedDict(
    "CreateAccessEntryRequestRequestTypeDef",
    {
        "clusterName": str,
        "principalArn": str,
        "kubernetesGroups": NotRequired[Sequence[str]],
        "tags": NotRequired[Mapping[str, str]],
        "clientRequestToken": NotRequired[str],
        "username": NotRequired[str],
        "type": NotRequired[str],
    },
)

class UpgradePolicyRequestTypeDef(TypedDict):
    supportType: NotRequired[SupportTypeType]

class VpcConfigRequestTypeDef(TypedDict):
    subnetIds: NotRequired[Sequence[str]]
    securityGroupIds: NotRequired[Sequence[str]]
    endpointPublicAccess: NotRequired[bool]
    endpointPrivateAccess: NotRequired[bool]
    publicAccessCidrs: NotRequired[Sequence[str]]

class ZonalShiftConfigRequestTypeDef(TypedDict):
    enabled: NotRequired[bool]

class EksAnywhereSubscriptionTermTypeDef(TypedDict):
    duration: NotRequired[int]
    unit: NotRequired[Literal["MONTHS"]]

LaunchTemplateSpecificationTypeDef = TypedDict(
    "LaunchTemplateSpecificationTypeDef",
    {
        "name": NotRequired[str],
        "version": NotRequired[str],
        "id": NotRequired[str],
    },
)

class NodegroupScalingConfigTypeDef(TypedDict):
    minSize: NotRequired[int]
    maxSize: NotRequired[int]
    desiredSize: NotRequired[int]

class NodegroupUpdateConfigTypeDef(TypedDict):
    maxUnavailable: NotRequired[int]
    maxUnavailablePercentage: NotRequired[int]

class RemoteAccessConfigTypeDef(TypedDict):
    ec2SshKey: NotRequired[str]
    sourceSecurityGroups: NotRequired[Sequence[str]]

class TaintTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[str]
    effect: NotRequired[TaintEffectType]

class CreatePodIdentityAssociationRequestRequestTypeDef(TypedDict):
    clusterName: str
    namespace: str
    serviceAccount: str
    roleArn: str
    clientRequestToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class PodIdentityAssociationTypeDef(TypedDict):
    clusterName: NotRequired[str]
    namespace: NotRequired[str]
    serviceAccount: NotRequired[str]
    roleArn: NotRequired[str]
    associationArn: NotRequired[str]
    associationId: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    createdAt: NotRequired[datetime]
    modifiedAt: NotRequired[datetime]
    ownerArn: NotRequired[str]

class DeleteAccessEntryRequestRequestTypeDef(TypedDict):
    clusterName: str
    principalArn: str

class DeleteAddonRequestRequestTypeDef(TypedDict):
    clusterName: str
    addonName: str
    preserve: NotRequired[bool]

class DeleteClusterRequestRequestTypeDef(TypedDict):
    name: str

DeleteEksAnywhereSubscriptionRequestRequestTypeDef = TypedDict(
    "DeleteEksAnywhereSubscriptionRequestRequestTypeDef",
    {
        "id": str,
    },
)

class DeleteFargateProfileRequestRequestTypeDef(TypedDict):
    clusterName: str
    fargateProfileName: str

class DeleteNodegroupRequestRequestTypeDef(TypedDict):
    clusterName: str
    nodegroupName: str

class DeletePodIdentityAssociationRequestRequestTypeDef(TypedDict):
    clusterName: str
    associationId: str

class DeregisterClusterRequestRequestTypeDef(TypedDict):
    name: str

class DescribeAccessEntryRequestRequestTypeDef(TypedDict):
    clusterName: str
    principalArn: str

class DescribeAddonConfigurationRequestRequestTypeDef(TypedDict):
    addonName: str
    addonVersion: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class DescribeAddonRequestRequestTypeDef(TypedDict):
    clusterName: str
    addonName: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

DescribeAddonVersionsRequestRequestTypeDef = TypedDict(
    "DescribeAddonVersionsRequestRequestTypeDef",
    {
        "kubernetesVersion": NotRequired[str],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "addonName": NotRequired[str],
        "types": NotRequired[Sequence[str]],
        "publishers": NotRequired[Sequence[str]],
        "owners": NotRequired[Sequence[str]],
    },
)

class DescribeClusterRequestRequestTypeDef(TypedDict):
    name: str

DescribeEksAnywhereSubscriptionRequestRequestTypeDef = TypedDict(
    "DescribeEksAnywhereSubscriptionRequestRequestTypeDef",
    {
        "id": str,
    },
)

class DescribeFargateProfileRequestRequestTypeDef(TypedDict):
    clusterName: str
    fargateProfileName: str

IdentityProviderConfigTypeDef = TypedDict(
    "IdentityProviderConfigTypeDef",
    {
        "type": str,
        "name": str,
    },
)
DescribeInsightRequestRequestTypeDef = TypedDict(
    "DescribeInsightRequestRequestTypeDef",
    {
        "clusterName": str,
        "id": str,
    },
)

class DescribeNodegroupRequestRequestTypeDef(TypedDict):
    clusterName: str
    nodegroupName: str

class DescribePodIdentityAssociationRequestRequestTypeDef(TypedDict):
    clusterName: str
    associationId: str

class DescribeUpdateRequestRequestTypeDef(TypedDict):
    name: str
    updateId: str
    nodegroupName: NotRequired[str]
    addonName: NotRequired[str]

class DisassociateAccessPolicyRequestRequestTypeDef(TypedDict):
    clusterName: str
    principalArn: str
    policyArn: str

class ElasticLoadBalancingTypeDef(TypedDict):
    enabled: NotRequired[bool]

class ProviderTypeDef(TypedDict):
    keyArn: NotRequired[str]

class ErrorDetailTypeDef(TypedDict):
    errorCode: NotRequired[ErrorCodeType]
    errorMessage: NotRequired[str]
    resourceIds: NotRequired[List[str]]

class FargateProfileIssueTypeDef(TypedDict):
    code: NotRequired[FargateProfileIssueCodeType]
    message: NotRequired[str]
    resourceIds: NotRequired[List[str]]

class FargateProfileSelectorOutputTypeDef(TypedDict):
    namespace: NotRequired[str]
    labels: NotRequired[Dict[str, str]]

class FargateProfileSelectorTypeDef(TypedDict):
    namespace: NotRequired[str]
    labels: NotRequired[Mapping[str, str]]

class OidcIdentityProviderConfigTypeDef(TypedDict):
    identityProviderConfigName: NotRequired[str]
    identityProviderConfigArn: NotRequired[str]
    clusterName: NotRequired[str]
    issuerUrl: NotRequired[str]
    clientId: NotRequired[str]
    usernameClaim: NotRequired[str]
    usernamePrefix: NotRequired[str]
    groupsClaim: NotRequired[str]
    groupsPrefix: NotRequired[str]
    requiredClaims: NotRequired[Dict[str, str]]
    tags: NotRequired[Dict[str, str]]
    status: NotRequired[ConfigStatusType]

class OIDCTypeDef(TypedDict):
    issuer: NotRequired[str]

class InsightStatusTypeDef(TypedDict):
    status: NotRequired[InsightStatusValueType]
    reason: NotRequired[str]

class InsightsFilterTypeDef(TypedDict):
    categories: NotRequired[Sequence[Literal["UPGRADE_READINESS"]]]
    kubernetesVersions: NotRequired[Sequence[str]]
    statuses: NotRequired[Sequence[InsightStatusValueType]]

class IssueTypeDef(TypedDict):
    code: NotRequired[NodegroupIssueCodeType]
    message: NotRequired[str]
    resourceIds: NotRequired[List[str]]

class ListAccessEntriesRequestRequestTypeDef(TypedDict):
    clusterName: str
    associatedPolicyArn: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAccessPoliciesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAddonsRequestRequestTypeDef(TypedDict):
    clusterName: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAssociatedAccessPoliciesRequestRequestTypeDef(TypedDict):
    clusterName: str
    principalArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListClustersRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    include: NotRequired[Sequence[str]]

class ListEksAnywhereSubscriptionsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    includeStatus: NotRequired[Sequence[EksAnywhereSubscriptionStatusType]]

class ListFargateProfilesRequestRequestTypeDef(TypedDict):
    clusterName: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListIdentityProviderConfigsRequestRequestTypeDef(TypedDict):
    clusterName: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListNodegroupsRequestRequestTypeDef(TypedDict):
    clusterName: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListPodIdentityAssociationsRequestRequestTypeDef(TypedDict):
    clusterName: str
    namespace: NotRequired[str]
    serviceAccount: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class PodIdentityAssociationSummaryTypeDef(TypedDict):
    clusterName: NotRequired[str]
    namespace: NotRequired[str]
    serviceAccount: NotRequired[str]
    associationArn: NotRequired[str]
    associationId: NotRequired[str]
    ownerArn: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class ListUpdatesRequestRequestTypeDef(TypedDict):
    name: str
    nodegroupName: NotRequired[str]
    addonName: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

LogSetupOutputTypeDef = TypedDict(
    "LogSetupOutputTypeDef",
    {
        "types": NotRequired[List[LogTypeType]],
        "enabled": NotRequired[bool],
    },
)
LogSetupTypeDef = TypedDict(
    "LogSetupTypeDef",
    {
        "types": NotRequired[Sequence[LogTypeType]],
        "enabled": NotRequired[bool],
    },
)

class RemoteAccessConfigOutputTypeDef(TypedDict):
    ec2SshKey: NotRequired[str]
    sourceSecurityGroups: NotRequired[List[str]]

class RemoteNodeNetworkOutputTypeDef(TypedDict):
    cidrs: NotRequired[List[str]]

class RemotePodNetworkOutputTypeDef(TypedDict):
    cidrs: NotRequired[List[str]]

class RemoteNodeNetworkTypeDef(TypedDict):
    cidrs: NotRequired[Sequence[str]]

class RemotePodNetworkTypeDef(TypedDict):
    cidrs: NotRequired[Sequence[str]]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateAccessConfigRequestTypeDef(TypedDict):
    authenticationMode: NotRequired[AuthenticationModeType]

class UpdateAccessEntryRequestRequestTypeDef(TypedDict):
    clusterName: str
    principalArn: str
    kubernetesGroups: NotRequired[Sequence[str]]
    clientRequestToken: NotRequired[str]
    username: NotRequired[str]

class UpdateClusterVersionRequestRequestTypeDef(TypedDict):
    name: str
    version: str
    clientRequestToken: NotRequired[str]

UpdateEksAnywhereSubscriptionRequestRequestTypeDef = TypedDict(
    "UpdateEksAnywhereSubscriptionRequestRequestTypeDef",
    {
        "id": str,
        "autoRenew": bool,
        "clientRequestToken": NotRequired[str],
    },
)

class UpdateLabelsPayloadTypeDef(TypedDict):
    addOrUpdateLabels: NotRequired[Mapping[str, str]]
    removeLabels: NotRequired[Sequence[str]]

UpdateParamTypeDef = TypedDict(
    "UpdateParamTypeDef",
    {
        "type": NotRequired[UpdateParamTypeType],
        "value": NotRequired[str],
    },
)

class UpdatePodIdentityAssociationRequestRequestTypeDef(TypedDict):
    clusterName: str
    associationId: str
    roleArn: NotRequired[str]
    clientRequestToken: NotRequired[str]

class AssociatedAccessPolicyTypeDef(TypedDict):
    policyArn: NotRequired[str]
    accessScope: NotRequired[AccessScopeOutputTypeDef]
    associatedAt: NotRequired[datetime]
    modifiedAt: NotRequired[datetime]

class AssociateAccessPolicyRequestRequestTypeDef(TypedDict):
    clusterName: str
    principalArn: str
    policyArn: str
    accessScope: AccessScopeTypeDef

class AddonHealthTypeDef(TypedDict):
    issues: NotRequired[List[AddonIssueTypeDef]]

class CreateAddonRequestRequestTypeDef(TypedDict):
    clusterName: str
    addonName: str
    addonVersion: NotRequired[str]
    serviceAccountRoleArn: NotRequired[str]
    resolveConflicts: NotRequired[ResolveConflictsType]
    clientRequestToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    configurationValues: NotRequired[str]
    podIdentityAssociations: NotRequired[Sequence[AddonPodIdentityAssociationsTypeDef]]

class UpdateAddonRequestRequestTypeDef(TypedDict):
    clusterName: str
    addonName: str
    addonVersion: NotRequired[str]
    serviceAccountRoleArn: NotRequired[str]
    resolveConflicts: NotRequired[ResolveConflictsType]
    clientRequestToken: NotRequired[str]
    configurationValues: NotRequired[str]
    podIdentityAssociations: NotRequired[Sequence[AddonPodIdentityAssociationsTypeDef]]

class AddonVersionInfoTypeDef(TypedDict):
    addonVersion: NotRequired[str]
    architecture: NotRequired[List[str]]
    computeTypes: NotRequired[List[str]]
    compatibilities: NotRequired[List[CompatibilityTypeDef]]
    requiresConfiguration: NotRequired[bool]
    requiresIamPermissions: NotRequired[bool]

class CreateAccessEntryResponseTypeDef(TypedDict):
    accessEntry: AccessEntryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAccessEntryResponseTypeDef(TypedDict):
    accessEntry: AccessEntryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAddonConfigurationResponseTypeDef(TypedDict):
    addonName: str
    addonVersion: str
    configurationSchema: str
    podIdentityConfiguration: List[AddonPodIdentityConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListAccessEntriesResponseTypeDef(TypedDict):
    accessEntries: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAccessPoliciesResponseTypeDef(TypedDict):
    accessPolicies: List[AccessPolicyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAddonsResponseTypeDef(TypedDict):
    addons: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListClustersResponseTypeDef(TypedDict):
    clusters: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListFargateProfilesResponseTypeDef(TypedDict):
    fargateProfileNames: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListNodegroupsResponseTypeDef(TypedDict):
    nodegroups: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListUpdatesResponseTypeDef(TypedDict):
    updateIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateAccessEntryResponseTypeDef(TypedDict):
    accessEntry: AccessEntryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AssociateIdentityProviderConfigRequestRequestTypeDef(TypedDict):
    clusterName: str
    oidc: OidcIdentityProviderConfigRequestTypeDef
    tags: NotRequired[Mapping[str, str]]
    clientRequestToken: NotRequired[str]

class NodegroupResourcesTypeDef(TypedDict):
    autoScalingGroups: NotRequired[List[AutoScalingGroupTypeDef]]
    remoteAccessSecurityGroup: NotRequired[str]

class StorageConfigRequestTypeDef(TypedDict):
    blockStorage: NotRequired[BlockStorageTypeDef]

class StorageConfigResponseTypeDef(TypedDict):
    blockStorage: NotRequired[BlockStorageTypeDef]

class DeprecationDetailTypeDef(TypedDict):
    usage: NotRequired[str]
    replacedWith: NotRequired[str]
    stopServingVersion: NotRequired[str]
    startServingReplacementVersion: NotRequired[str]
    clientStats: NotRequired[List[ClientStatTypeDef]]

class ClusterHealthTypeDef(TypedDict):
    issues: NotRequired[List[ClusterIssueTypeDef]]

class RegisterClusterRequestRequestTypeDef(TypedDict):
    name: str
    connectorConfig: ConnectorConfigRequestTypeDef
    clientRequestToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class OutpostConfigRequestTypeDef(TypedDict):
    outpostArns: Sequence[str]
    controlPlaneInstanceType: str
    controlPlanePlacement: NotRequired[ControlPlanePlacementRequestTypeDef]

class OutpostConfigResponseTypeDef(TypedDict):
    outpostArns: List[str]
    controlPlaneInstanceType: str
    controlPlanePlacement: NotRequired[ControlPlanePlacementResponseTypeDef]

class CreateEksAnywhereSubscriptionRequestRequestTypeDef(TypedDict):
    name: str
    term: EksAnywhereSubscriptionTermTypeDef
    licenseQuantity: NotRequired[int]
    licenseType: NotRequired[Literal["Cluster"]]
    autoRenew: NotRequired[bool]
    clientRequestToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

EksAnywhereSubscriptionTypeDef = TypedDict(
    "EksAnywhereSubscriptionTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "effectiveDate": NotRequired[datetime],
        "expirationDate": NotRequired[datetime],
        "licenseQuantity": NotRequired[int],
        "licenseType": NotRequired[Literal["Cluster"]],
        "term": NotRequired[EksAnywhereSubscriptionTermTypeDef],
        "status": NotRequired[str],
        "autoRenew": NotRequired[bool],
        "licenseArns": NotRequired[List[str]],
        "tags": NotRequired[Dict[str, str]],
    },
)

class UpdateNodegroupVersionRequestRequestTypeDef(TypedDict):
    clusterName: str
    nodegroupName: str
    version: NotRequired[str]
    releaseVersion: NotRequired[str]
    launchTemplate: NotRequired[LaunchTemplateSpecificationTypeDef]
    force: NotRequired[bool]
    clientRequestToken: NotRequired[str]

class CreateNodegroupRequestRequestTypeDef(TypedDict):
    clusterName: str
    nodegroupName: str
    subnets: Sequence[str]
    nodeRole: str
    scalingConfig: NotRequired[NodegroupScalingConfigTypeDef]
    diskSize: NotRequired[int]
    instanceTypes: NotRequired[Sequence[str]]
    amiType: NotRequired[AMITypesType]
    remoteAccess: NotRequired[RemoteAccessConfigTypeDef]
    labels: NotRequired[Mapping[str, str]]
    taints: NotRequired[Sequence[TaintTypeDef]]
    tags: NotRequired[Mapping[str, str]]
    clientRequestToken: NotRequired[str]
    launchTemplate: NotRequired[LaunchTemplateSpecificationTypeDef]
    updateConfig: NotRequired[NodegroupUpdateConfigTypeDef]
    capacityType: NotRequired[CapacityTypesType]
    version: NotRequired[str]
    releaseVersion: NotRequired[str]

class UpdateTaintsPayloadTypeDef(TypedDict):
    addOrUpdateTaints: NotRequired[Sequence[TaintTypeDef]]
    removeTaints: NotRequired[Sequence[TaintTypeDef]]

class CreatePodIdentityAssociationResponseTypeDef(TypedDict):
    association: PodIdentityAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeletePodIdentityAssociationResponseTypeDef(TypedDict):
    association: PodIdentityAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribePodIdentityAssociationResponseTypeDef(TypedDict):
    association: PodIdentityAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePodIdentityAssociationResponseTypeDef(TypedDict):
    association: PodIdentityAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAddonRequestAddonActiveWaitTypeDef(TypedDict):
    clusterName: str
    addonName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeAddonRequestAddonDeletedWaitTypeDef(TypedDict):
    clusterName: str
    addonName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeClusterRequestClusterActiveWaitTypeDef(TypedDict):
    name: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeClusterRequestClusterDeletedWaitTypeDef(TypedDict):
    name: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeFargateProfileRequestFargateProfileActiveWaitTypeDef(TypedDict):
    clusterName: str
    fargateProfileName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeFargateProfileRequestFargateProfileDeletedWaitTypeDef(TypedDict):
    clusterName: str
    fargateProfileName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeNodegroupRequestNodegroupActiveWaitTypeDef(TypedDict):
    clusterName: str
    nodegroupName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeNodegroupRequestNodegroupDeletedWaitTypeDef(TypedDict):
    clusterName: str
    nodegroupName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

DescribeAddonVersionsRequestDescribeAddonVersionsPaginateTypeDef = TypedDict(
    "DescribeAddonVersionsRequestDescribeAddonVersionsPaginateTypeDef",
    {
        "kubernetesVersion": NotRequired[str],
        "addonName": NotRequired[str],
        "types": NotRequired[Sequence[str]],
        "publishers": NotRequired[Sequence[str]],
        "owners": NotRequired[Sequence[str]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListAccessEntriesRequestListAccessEntriesPaginateTypeDef(TypedDict):
    clusterName: str
    associatedPolicyArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAccessPoliciesRequestListAccessPoliciesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAddonsRequestListAddonsPaginateTypeDef(TypedDict):
    clusterName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAssociatedAccessPoliciesRequestListAssociatedAccessPoliciesPaginateTypeDef(TypedDict):
    clusterName: str
    principalArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListClustersRequestListClustersPaginateTypeDef(TypedDict):
    include: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEksAnywhereSubscriptionsRequestListEksAnywhereSubscriptionsPaginateTypeDef(TypedDict):
    includeStatus: NotRequired[Sequence[EksAnywhereSubscriptionStatusType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFargateProfilesRequestListFargateProfilesPaginateTypeDef(TypedDict):
    clusterName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListIdentityProviderConfigsRequestListIdentityProviderConfigsPaginateTypeDef(TypedDict):
    clusterName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListNodegroupsRequestListNodegroupsPaginateTypeDef(TypedDict):
    clusterName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPodIdentityAssociationsRequestListPodIdentityAssociationsPaginateTypeDef(TypedDict):
    clusterName: str
    namespace: NotRequired[str]
    serviceAccount: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListUpdatesRequestListUpdatesPaginateTypeDef(TypedDict):
    name: str
    nodegroupName: NotRequired[str]
    addonName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeIdentityProviderConfigRequestRequestTypeDef(TypedDict):
    clusterName: str
    identityProviderConfig: IdentityProviderConfigTypeDef

class DisassociateIdentityProviderConfigRequestRequestTypeDef(TypedDict):
    clusterName: str
    identityProviderConfig: IdentityProviderConfigTypeDef
    clientRequestToken: NotRequired[str]

class ListIdentityProviderConfigsResponseTypeDef(TypedDict):
    identityProviderConfigs: List[IdentityProviderConfigTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class KubernetesNetworkConfigRequestTypeDef(TypedDict):
    serviceIpv4Cidr: NotRequired[str]
    ipFamily: NotRequired[IpFamilyType]
    elasticLoadBalancing: NotRequired[ElasticLoadBalancingTypeDef]

class KubernetesNetworkConfigResponseTypeDef(TypedDict):
    serviceIpv4Cidr: NotRequired[str]
    serviceIpv6Cidr: NotRequired[str]
    ipFamily: NotRequired[IpFamilyType]
    elasticLoadBalancing: NotRequired[ElasticLoadBalancingTypeDef]

class EncryptionConfigOutputTypeDef(TypedDict):
    resources: NotRequired[List[str]]
    provider: NotRequired[ProviderTypeDef]

class EncryptionConfigTypeDef(TypedDict):
    resources: NotRequired[Sequence[str]]
    provider: NotRequired[ProviderTypeDef]

class FargateProfileHealthTypeDef(TypedDict):
    issues: NotRequired[List[FargateProfileIssueTypeDef]]

FargateProfileSelectorUnionTypeDef = Union[
    FargateProfileSelectorTypeDef, FargateProfileSelectorOutputTypeDef
]

class IdentityProviderConfigResponseTypeDef(TypedDict):
    oidc: NotRequired[OidcIdentityProviderConfigTypeDef]

class IdentityTypeDef(TypedDict):
    oidc: NotRequired[OIDCTypeDef]

class InsightResourceDetailTypeDef(TypedDict):
    insightStatus: NotRequired[InsightStatusTypeDef]
    kubernetesResourceUri: NotRequired[str]
    arn: NotRequired[str]

InsightSummaryTypeDef = TypedDict(
    "InsightSummaryTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "category": NotRequired[Literal["UPGRADE_READINESS"]],
        "kubernetesVersion": NotRequired[str],
        "lastRefreshTime": NotRequired[datetime],
        "lastTransitionTime": NotRequired[datetime],
        "description": NotRequired[str],
        "insightStatus": NotRequired[InsightStatusTypeDef],
    },
)
ListInsightsRequestListInsightsPaginateTypeDef = TypedDict(
    "ListInsightsRequestListInsightsPaginateTypeDef",
    {
        "clusterName": str,
        "filter": NotRequired[InsightsFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListInsightsRequestRequestTypeDef = TypedDict(
    "ListInsightsRequestRequestTypeDef",
    {
        "clusterName": str,
        "filter": NotRequired[InsightsFilterTypeDef],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

class NodegroupHealthTypeDef(TypedDict):
    issues: NotRequired[List[IssueTypeDef]]

class ListPodIdentityAssociationsResponseTypeDef(TypedDict):
    associations: List[PodIdentityAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class LoggingOutputTypeDef(TypedDict):
    clusterLogging: NotRequired[List[LogSetupOutputTypeDef]]

LogSetupUnionTypeDef = Union[LogSetupTypeDef, LogSetupOutputTypeDef]

class RemoteNetworkConfigResponseTypeDef(TypedDict):
    remoteNodeNetworks: NotRequired[List[RemoteNodeNetworkOutputTypeDef]]
    remotePodNetworks: NotRequired[List[RemotePodNetworkOutputTypeDef]]

RemoteNodeNetworkUnionTypeDef = Union[RemoteNodeNetworkTypeDef, RemoteNodeNetworkOutputTypeDef]
RemotePodNetworkUnionTypeDef = Union[RemotePodNetworkTypeDef, RemotePodNetworkOutputTypeDef]
UpdateTypeDef = TypedDict(
    "UpdateTypeDef",
    {
        "id": NotRequired[str],
        "status": NotRequired[UpdateStatusType],
        "type": NotRequired[UpdateTypeType],
        "params": NotRequired[List[UpdateParamTypeDef]],
        "createdAt": NotRequired[datetime],
        "errors": NotRequired[List[ErrorDetailTypeDef]],
    },
)

class AssociateAccessPolicyResponseTypeDef(TypedDict):
    clusterName: str
    principalArn: str
    associatedAccessPolicy: AssociatedAccessPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAssociatedAccessPoliciesResponseTypeDef(TypedDict):
    clusterName: str
    principalArn: str
    associatedAccessPolicies: List[AssociatedAccessPolicyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class AddonTypeDef(TypedDict):
    addonName: NotRequired[str]
    clusterName: NotRequired[str]
    status: NotRequired[AddonStatusType]
    addonVersion: NotRequired[str]
    health: NotRequired[AddonHealthTypeDef]
    addonArn: NotRequired[str]
    createdAt: NotRequired[datetime]
    modifiedAt: NotRequired[datetime]
    serviceAccountRoleArn: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    publisher: NotRequired[str]
    owner: NotRequired[str]
    marketplaceInformation: NotRequired[MarketplaceInformationTypeDef]
    configurationValues: NotRequired[str]
    podIdentityAssociations: NotRequired[List[str]]

AddonInfoTypeDef = TypedDict(
    "AddonInfoTypeDef",
    {
        "addonName": NotRequired[str],
        "type": NotRequired[str],
        "addonVersions": NotRequired[List[AddonVersionInfoTypeDef]],
        "publisher": NotRequired[str],
        "owner": NotRequired[str],
        "marketplaceInformation": NotRequired[MarketplaceInformationTypeDef],
    },
)

class InsightCategorySpecificSummaryTypeDef(TypedDict):
    deprecationDetails: NotRequired[List[DeprecationDetailTypeDef]]

class CreateEksAnywhereSubscriptionResponseTypeDef(TypedDict):
    subscription: EksAnywhereSubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteEksAnywhereSubscriptionResponseTypeDef(TypedDict):
    subscription: EksAnywhereSubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeEksAnywhereSubscriptionResponseTypeDef(TypedDict):
    subscription: EksAnywhereSubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListEksAnywhereSubscriptionsResponseTypeDef(TypedDict):
    subscriptions: List[EksAnywhereSubscriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateEksAnywhereSubscriptionResponseTypeDef(TypedDict):
    subscription: EksAnywhereSubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateNodegroupConfigRequestRequestTypeDef(TypedDict):
    clusterName: str
    nodegroupName: str
    labels: NotRequired[UpdateLabelsPayloadTypeDef]
    taints: NotRequired[UpdateTaintsPayloadTypeDef]
    scalingConfig: NotRequired[NodegroupScalingConfigTypeDef]
    updateConfig: NotRequired[NodegroupUpdateConfigTypeDef]
    clientRequestToken: NotRequired[str]

EncryptionConfigUnionTypeDef = Union[EncryptionConfigTypeDef, EncryptionConfigOutputTypeDef]

class FargateProfileTypeDef(TypedDict):
    fargateProfileName: NotRequired[str]
    fargateProfileArn: NotRequired[str]
    clusterName: NotRequired[str]
    createdAt: NotRequired[datetime]
    podExecutionRoleArn: NotRequired[str]
    subnets: NotRequired[List[str]]
    selectors: NotRequired[List[FargateProfileSelectorOutputTypeDef]]
    status: NotRequired[FargateProfileStatusType]
    tags: NotRequired[Dict[str, str]]
    health: NotRequired[FargateProfileHealthTypeDef]

class CreateFargateProfileRequestRequestTypeDef(TypedDict):
    fargateProfileName: str
    clusterName: str
    podExecutionRoleArn: str
    subnets: NotRequired[Sequence[str]]
    selectors: NotRequired[Sequence[FargateProfileSelectorUnionTypeDef]]
    clientRequestToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class DescribeIdentityProviderConfigResponseTypeDef(TypedDict):
    identityProviderConfig: IdentityProviderConfigResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListInsightsResponseTypeDef(TypedDict):
    insights: List[InsightSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class NodegroupTypeDef(TypedDict):
    nodegroupName: NotRequired[str]
    nodegroupArn: NotRequired[str]
    clusterName: NotRequired[str]
    version: NotRequired[str]
    releaseVersion: NotRequired[str]
    createdAt: NotRequired[datetime]
    modifiedAt: NotRequired[datetime]
    status: NotRequired[NodegroupStatusType]
    capacityType: NotRequired[CapacityTypesType]
    scalingConfig: NotRequired[NodegroupScalingConfigTypeDef]
    instanceTypes: NotRequired[List[str]]
    subnets: NotRequired[List[str]]
    remoteAccess: NotRequired[RemoteAccessConfigOutputTypeDef]
    amiType: NotRequired[AMITypesType]
    nodeRole: NotRequired[str]
    labels: NotRequired[Dict[str, str]]
    taints: NotRequired[List[TaintTypeDef]]
    resources: NotRequired[NodegroupResourcesTypeDef]
    diskSize: NotRequired[int]
    health: NotRequired[NodegroupHealthTypeDef]
    updateConfig: NotRequired[NodegroupUpdateConfigTypeDef]
    launchTemplate: NotRequired[LaunchTemplateSpecificationTypeDef]
    tags: NotRequired[Dict[str, str]]

class LoggingTypeDef(TypedDict):
    clusterLogging: NotRequired[Sequence[LogSetupUnionTypeDef]]

ClusterTypeDef = TypedDict(
    "ClusterTypeDef",
    {
        "name": NotRequired[str],
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "version": NotRequired[str],
        "endpoint": NotRequired[str],
        "roleArn": NotRequired[str],
        "resourcesVpcConfig": NotRequired[VpcConfigResponseTypeDef],
        "kubernetesNetworkConfig": NotRequired[KubernetesNetworkConfigResponseTypeDef],
        "logging": NotRequired[LoggingOutputTypeDef],
        "identity": NotRequired[IdentityTypeDef],
        "status": NotRequired[ClusterStatusType],
        "certificateAuthority": NotRequired[CertificateTypeDef],
        "clientRequestToken": NotRequired[str],
        "platformVersion": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "encryptionConfig": NotRequired[List[EncryptionConfigOutputTypeDef]],
        "connectorConfig": NotRequired[ConnectorConfigResponseTypeDef],
        "id": NotRequired[str],
        "health": NotRequired[ClusterHealthTypeDef],
        "outpostConfig": NotRequired[OutpostConfigResponseTypeDef],
        "accessConfig": NotRequired[AccessConfigResponseTypeDef],
        "upgradePolicy": NotRequired[UpgradePolicyResponseTypeDef],
        "zonalShiftConfig": NotRequired[ZonalShiftConfigResponseTypeDef],
        "remoteNetworkConfig": NotRequired[RemoteNetworkConfigResponseTypeDef],
        "computeConfig": NotRequired[ComputeConfigResponseTypeDef],
        "storageConfig": NotRequired[StorageConfigResponseTypeDef],
    },
)

class RemoteNetworkConfigRequestTypeDef(TypedDict):
    remoteNodeNetworks: NotRequired[Sequence[RemoteNodeNetworkUnionTypeDef]]
    remotePodNetworks: NotRequired[Sequence[RemotePodNetworkUnionTypeDef]]

class AssociateEncryptionConfigResponseTypeDef(TypedDict):
    update: UpdateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AssociateIdentityProviderConfigResponseTypeDef(TypedDict):
    update: UpdateTypeDef
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeUpdateResponseTypeDef(TypedDict):
    update: UpdateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociateIdentityProviderConfigResponseTypeDef(TypedDict):
    update: UpdateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAddonResponseTypeDef(TypedDict):
    update: UpdateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateClusterConfigResponseTypeDef(TypedDict):
    update: UpdateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateClusterVersionResponseTypeDef(TypedDict):
    update: UpdateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateNodegroupConfigResponseTypeDef(TypedDict):
    update: UpdateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateNodegroupVersionResponseTypeDef(TypedDict):
    update: UpdateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAddonResponseTypeDef(TypedDict):
    addon: AddonTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAddonResponseTypeDef(TypedDict):
    addon: AddonTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAddonResponseTypeDef(TypedDict):
    addon: AddonTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAddonVersionsResponseTypeDef(TypedDict):
    addons: List[AddonInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

InsightTypeDef = TypedDict(
    "InsightTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "category": NotRequired[Literal["UPGRADE_READINESS"]],
        "kubernetesVersion": NotRequired[str],
        "lastRefreshTime": NotRequired[datetime],
        "lastTransitionTime": NotRequired[datetime],
        "description": NotRequired[str],
        "insightStatus": NotRequired[InsightStatusTypeDef],
        "recommendation": NotRequired[str],
        "additionalInfo": NotRequired[Dict[str, str]],
        "resources": NotRequired[List[InsightResourceDetailTypeDef]],
        "categorySpecificSummary": NotRequired[InsightCategorySpecificSummaryTypeDef],
    },
)

class AssociateEncryptionConfigRequestRequestTypeDef(TypedDict):
    clusterName: str
    encryptionConfig: Sequence[EncryptionConfigUnionTypeDef]
    clientRequestToken: NotRequired[str]

class CreateFargateProfileResponseTypeDef(TypedDict):
    fargateProfile: FargateProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteFargateProfileResponseTypeDef(TypedDict):
    fargateProfile: FargateProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeFargateProfileResponseTypeDef(TypedDict):
    fargateProfile: FargateProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateNodegroupResponseTypeDef(TypedDict):
    nodegroup: NodegroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteNodegroupResponseTypeDef(TypedDict):
    nodegroup: NodegroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeNodegroupResponseTypeDef(TypedDict):
    nodegroup: NodegroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateClusterConfigRequestRequestTypeDef(TypedDict):
    name: str
    resourcesVpcConfig: NotRequired[VpcConfigRequestTypeDef]
    logging: NotRequired[LoggingTypeDef]
    clientRequestToken: NotRequired[str]
    accessConfig: NotRequired[UpdateAccessConfigRequestTypeDef]
    upgradePolicy: NotRequired[UpgradePolicyRequestTypeDef]
    zonalShiftConfig: NotRequired[ZonalShiftConfigRequestTypeDef]
    computeConfig: NotRequired[ComputeConfigRequestTypeDef]
    kubernetesNetworkConfig: NotRequired[KubernetesNetworkConfigRequestTypeDef]
    storageConfig: NotRequired[StorageConfigRequestTypeDef]

class CreateClusterResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteClusterResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeregisterClusterResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeClusterResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class RegisterClusterResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateClusterRequestRequestTypeDef(TypedDict):
    name: str
    roleArn: str
    resourcesVpcConfig: VpcConfigRequestTypeDef
    version: NotRequired[str]
    kubernetesNetworkConfig: NotRequired[KubernetesNetworkConfigRequestTypeDef]
    logging: NotRequired[LoggingTypeDef]
    clientRequestToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    encryptionConfig: NotRequired[Sequence[EncryptionConfigTypeDef]]
    outpostConfig: NotRequired[OutpostConfigRequestTypeDef]
    accessConfig: NotRequired[CreateAccessConfigRequestTypeDef]
    bootstrapSelfManagedAddons: NotRequired[bool]
    upgradePolicy: NotRequired[UpgradePolicyRequestTypeDef]
    zonalShiftConfig: NotRequired[ZonalShiftConfigRequestTypeDef]
    remoteNetworkConfig: NotRequired[RemoteNetworkConfigRequestTypeDef]
    computeConfig: NotRequired[ComputeConfigRequestTypeDef]
    storageConfig: NotRequired[StorageConfigRequestTypeDef]

class DescribeInsightResponseTypeDef(TypedDict):
    insight: InsightTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
