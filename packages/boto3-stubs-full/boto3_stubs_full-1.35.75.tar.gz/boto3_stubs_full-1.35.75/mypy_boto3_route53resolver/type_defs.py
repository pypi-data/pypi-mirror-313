"""
Type annotations for route53resolver service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/type_defs/)

Usage::

    ```python
    from mypy_boto3_route53resolver.type_defs import TagTypeDef

    data: TagTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Sequence

from .literals import (
    ActionType,
    AutodefinedReverseFlagType,
    BlockResponseType,
    ConfidenceThresholdType,
    DnsThreatProtectionType,
    FirewallDomainListStatusType,
    FirewallDomainRedirectionActionType,
    FirewallDomainUpdateOperationType,
    FirewallFailOpenStatusType,
    FirewallRuleGroupAssociationStatusType,
    FirewallRuleGroupStatusType,
    IpAddressStatusType,
    MutationProtectionStatusType,
    OutpostResolverStatusType,
    ProtocolType,
    ResolverAutodefinedReverseStatusType,
    ResolverDNSSECValidationStatusType,
    ResolverEndpointDirectionType,
    ResolverEndpointStatusType,
    ResolverEndpointTypeType,
    ResolverQueryLogConfigAssociationErrorType,
    ResolverQueryLogConfigAssociationStatusType,
    ResolverQueryLogConfigStatusType,
    ResolverRuleAssociationStatusType,
    ResolverRuleStatusType,
    RuleTypeOptionType,
    ShareStatusType,
    SortOrderType,
    ValidationType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AssociateFirewallRuleGroupRequestRequestTypeDef",
    "AssociateFirewallRuleGroupResponseTypeDef",
    "AssociateResolverEndpointIpAddressRequestRequestTypeDef",
    "AssociateResolverEndpointIpAddressResponseTypeDef",
    "AssociateResolverQueryLogConfigRequestRequestTypeDef",
    "AssociateResolverQueryLogConfigResponseTypeDef",
    "AssociateResolverRuleRequestRequestTypeDef",
    "AssociateResolverRuleResponseTypeDef",
    "CreateFirewallDomainListRequestRequestTypeDef",
    "CreateFirewallDomainListResponseTypeDef",
    "CreateFirewallRuleGroupRequestRequestTypeDef",
    "CreateFirewallRuleGroupResponseTypeDef",
    "CreateFirewallRuleRequestRequestTypeDef",
    "CreateFirewallRuleResponseTypeDef",
    "CreateOutpostResolverRequestRequestTypeDef",
    "CreateOutpostResolverResponseTypeDef",
    "CreateResolverEndpointRequestRequestTypeDef",
    "CreateResolverEndpointResponseTypeDef",
    "CreateResolverQueryLogConfigRequestRequestTypeDef",
    "CreateResolverQueryLogConfigResponseTypeDef",
    "CreateResolverRuleRequestRequestTypeDef",
    "CreateResolverRuleResponseTypeDef",
    "DeleteFirewallDomainListRequestRequestTypeDef",
    "DeleteFirewallDomainListResponseTypeDef",
    "DeleteFirewallRuleGroupRequestRequestTypeDef",
    "DeleteFirewallRuleGroupResponseTypeDef",
    "DeleteFirewallRuleRequestRequestTypeDef",
    "DeleteFirewallRuleResponseTypeDef",
    "DeleteOutpostResolverRequestRequestTypeDef",
    "DeleteOutpostResolverResponseTypeDef",
    "DeleteResolverEndpointRequestRequestTypeDef",
    "DeleteResolverEndpointResponseTypeDef",
    "DeleteResolverQueryLogConfigRequestRequestTypeDef",
    "DeleteResolverQueryLogConfigResponseTypeDef",
    "DeleteResolverRuleRequestRequestTypeDef",
    "DeleteResolverRuleResponseTypeDef",
    "DisassociateFirewallRuleGroupRequestRequestTypeDef",
    "DisassociateFirewallRuleGroupResponseTypeDef",
    "DisassociateResolverEndpointIpAddressRequestRequestTypeDef",
    "DisassociateResolverEndpointIpAddressResponseTypeDef",
    "DisassociateResolverQueryLogConfigRequestRequestTypeDef",
    "DisassociateResolverQueryLogConfigResponseTypeDef",
    "DisassociateResolverRuleRequestRequestTypeDef",
    "DisassociateResolverRuleResponseTypeDef",
    "FilterTypeDef",
    "FirewallConfigTypeDef",
    "FirewallDomainListMetadataTypeDef",
    "FirewallDomainListTypeDef",
    "FirewallRuleGroupAssociationTypeDef",
    "FirewallRuleGroupMetadataTypeDef",
    "FirewallRuleGroupTypeDef",
    "FirewallRuleTypeDef",
    "GetFirewallConfigRequestRequestTypeDef",
    "GetFirewallConfigResponseTypeDef",
    "GetFirewallDomainListRequestRequestTypeDef",
    "GetFirewallDomainListResponseTypeDef",
    "GetFirewallRuleGroupAssociationRequestRequestTypeDef",
    "GetFirewallRuleGroupAssociationResponseTypeDef",
    "GetFirewallRuleGroupPolicyRequestRequestTypeDef",
    "GetFirewallRuleGroupPolicyResponseTypeDef",
    "GetFirewallRuleGroupRequestRequestTypeDef",
    "GetFirewallRuleGroupResponseTypeDef",
    "GetOutpostResolverRequestRequestTypeDef",
    "GetOutpostResolverResponseTypeDef",
    "GetResolverConfigRequestRequestTypeDef",
    "GetResolverConfigResponseTypeDef",
    "GetResolverDnssecConfigRequestRequestTypeDef",
    "GetResolverDnssecConfigResponseTypeDef",
    "GetResolverEndpointRequestRequestTypeDef",
    "GetResolverEndpointResponseTypeDef",
    "GetResolverQueryLogConfigAssociationRequestRequestTypeDef",
    "GetResolverQueryLogConfigAssociationResponseTypeDef",
    "GetResolverQueryLogConfigPolicyRequestRequestTypeDef",
    "GetResolverQueryLogConfigPolicyResponseTypeDef",
    "GetResolverQueryLogConfigRequestRequestTypeDef",
    "GetResolverQueryLogConfigResponseTypeDef",
    "GetResolverRuleAssociationRequestRequestTypeDef",
    "GetResolverRuleAssociationResponseTypeDef",
    "GetResolverRulePolicyRequestRequestTypeDef",
    "GetResolverRulePolicyResponseTypeDef",
    "GetResolverRuleRequestRequestTypeDef",
    "GetResolverRuleResponseTypeDef",
    "ImportFirewallDomainsRequestRequestTypeDef",
    "ImportFirewallDomainsResponseTypeDef",
    "IpAddressRequestTypeDef",
    "IpAddressResponseTypeDef",
    "IpAddressUpdateTypeDef",
    "ListFirewallConfigsRequestListFirewallConfigsPaginateTypeDef",
    "ListFirewallConfigsRequestRequestTypeDef",
    "ListFirewallConfigsResponseTypeDef",
    "ListFirewallDomainListsRequestListFirewallDomainListsPaginateTypeDef",
    "ListFirewallDomainListsRequestRequestTypeDef",
    "ListFirewallDomainListsResponseTypeDef",
    "ListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef",
    "ListFirewallDomainsRequestRequestTypeDef",
    "ListFirewallDomainsResponseTypeDef",
    "ListFirewallRuleGroupAssociationsRequestListFirewallRuleGroupAssociationsPaginateTypeDef",
    "ListFirewallRuleGroupAssociationsRequestRequestTypeDef",
    "ListFirewallRuleGroupAssociationsResponseTypeDef",
    "ListFirewallRuleGroupsRequestListFirewallRuleGroupsPaginateTypeDef",
    "ListFirewallRuleGroupsRequestRequestTypeDef",
    "ListFirewallRuleGroupsResponseTypeDef",
    "ListFirewallRulesRequestListFirewallRulesPaginateTypeDef",
    "ListFirewallRulesRequestRequestTypeDef",
    "ListFirewallRulesResponseTypeDef",
    "ListOutpostResolversRequestListOutpostResolversPaginateTypeDef",
    "ListOutpostResolversRequestRequestTypeDef",
    "ListOutpostResolversResponseTypeDef",
    "ListResolverConfigsRequestListResolverConfigsPaginateTypeDef",
    "ListResolverConfigsRequestRequestTypeDef",
    "ListResolverConfigsResponseTypeDef",
    "ListResolverDnssecConfigsRequestListResolverDnssecConfigsPaginateTypeDef",
    "ListResolverDnssecConfigsRequestRequestTypeDef",
    "ListResolverDnssecConfigsResponseTypeDef",
    "ListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef",
    "ListResolverEndpointIpAddressesRequestRequestTypeDef",
    "ListResolverEndpointIpAddressesResponseTypeDef",
    "ListResolverEndpointsRequestListResolverEndpointsPaginateTypeDef",
    "ListResolverEndpointsRequestRequestTypeDef",
    "ListResolverEndpointsResponseTypeDef",
    "ListResolverQueryLogConfigAssociationsRequestListResolverQueryLogConfigAssociationsPaginateTypeDef",
    "ListResolverQueryLogConfigAssociationsRequestRequestTypeDef",
    "ListResolverQueryLogConfigAssociationsResponseTypeDef",
    "ListResolverQueryLogConfigsRequestListResolverQueryLogConfigsPaginateTypeDef",
    "ListResolverQueryLogConfigsRequestRequestTypeDef",
    "ListResolverQueryLogConfigsResponseTypeDef",
    "ListResolverRuleAssociationsRequestListResolverRuleAssociationsPaginateTypeDef",
    "ListResolverRuleAssociationsRequestRequestTypeDef",
    "ListResolverRuleAssociationsResponseTypeDef",
    "ListResolverRulesRequestListResolverRulesPaginateTypeDef",
    "ListResolverRulesRequestRequestTypeDef",
    "ListResolverRulesResponseTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "OutpostResolverTypeDef",
    "PaginatorConfigTypeDef",
    "PutFirewallRuleGroupPolicyRequestRequestTypeDef",
    "PutFirewallRuleGroupPolicyResponseTypeDef",
    "PutResolverQueryLogConfigPolicyRequestRequestTypeDef",
    "PutResolverQueryLogConfigPolicyResponseTypeDef",
    "PutResolverRulePolicyRequestRequestTypeDef",
    "PutResolverRulePolicyResponseTypeDef",
    "ResolverConfigTypeDef",
    "ResolverDnssecConfigTypeDef",
    "ResolverEndpointTypeDef",
    "ResolverQueryLogConfigAssociationTypeDef",
    "ResolverQueryLogConfigTypeDef",
    "ResolverRuleAssociationTypeDef",
    "ResolverRuleConfigTypeDef",
    "ResolverRuleTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TargetAddressTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFirewallConfigRequestRequestTypeDef",
    "UpdateFirewallConfigResponseTypeDef",
    "UpdateFirewallDomainsRequestRequestTypeDef",
    "UpdateFirewallDomainsResponseTypeDef",
    "UpdateFirewallRuleGroupAssociationRequestRequestTypeDef",
    "UpdateFirewallRuleGroupAssociationResponseTypeDef",
    "UpdateFirewallRuleRequestRequestTypeDef",
    "UpdateFirewallRuleResponseTypeDef",
    "UpdateIpAddressTypeDef",
    "UpdateOutpostResolverRequestRequestTypeDef",
    "UpdateOutpostResolverResponseTypeDef",
    "UpdateResolverConfigRequestRequestTypeDef",
    "UpdateResolverConfigResponseTypeDef",
    "UpdateResolverDnssecConfigRequestRequestTypeDef",
    "UpdateResolverDnssecConfigResponseTypeDef",
    "UpdateResolverEndpointRequestRequestTypeDef",
    "UpdateResolverEndpointResponseTypeDef",
    "UpdateResolverRuleRequestRequestTypeDef",
    "UpdateResolverRuleResponseTypeDef",
)


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class FirewallRuleGroupAssociationTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    FirewallRuleGroupId: NotRequired[str]
    VpcId: NotRequired[str]
    Name: NotRequired[str]
    Priority: NotRequired[int]
    MutationProtection: NotRequired[MutationProtectionStatusType]
    ManagedOwnerName: NotRequired[str]
    Status: NotRequired[FirewallRuleGroupAssociationStatusType]
    StatusMessage: NotRequired[str]
    CreatorRequestId: NotRequired[str]
    CreationTime: NotRequired[str]
    ModificationTime: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class IpAddressUpdateTypeDef(TypedDict):
    IpId: NotRequired[str]
    SubnetId: NotRequired[str]
    Ip: NotRequired[str]
    Ipv6: NotRequired[str]


class ResolverEndpointTypeDef(TypedDict):
    Id: NotRequired[str]
    CreatorRequestId: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    SecurityGroupIds: NotRequired[List[str]]
    Direction: NotRequired[ResolverEndpointDirectionType]
    IpAddressCount: NotRequired[int]
    HostVPCId: NotRequired[str]
    Status: NotRequired[ResolverEndpointStatusType]
    StatusMessage: NotRequired[str]
    CreationTime: NotRequired[str]
    ModificationTime: NotRequired[str]
    OutpostArn: NotRequired[str]
    PreferredInstanceType: NotRequired[str]
    ResolverEndpointType: NotRequired[ResolverEndpointTypeType]
    Protocols: NotRequired[List[ProtocolType]]


class AssociateResolverQueryLogConfigRequestRequestTypeDef(TypedDict):
    ResolverQueryLogConfigId: str
    ResourceId: str


class ResolverQueryLogConfigAssociationTypeDef(TypedDict):
    Id: NotRequired[str]
    ResolverQueryLogConfigId: NotRequired[str]
    ResourceId: NotRequired[str]
    Status: NotRequired[ResolverQueryLogConfigAssociationStatusType]
    Error: NotRequired[ResolverQueryLogConfigAssociationErrorType]
    ErrorMessage: NotRequired[str]
    CreationTime: NotRequired[str]


class AssociateResolverRuleRequestRequestTypeDef(TypedDict):
    ResolverRuleId: str
    VPCId: str
    Name: NotRequired[str]


class ResolverRuleAssociationTypeDef(TypedDict):
    Id: NotRequired[str]
    ResolverRuleId: NotRequired[str]
    Name: NotRequired[str]
    VPCId: NotRequired[str]
    Status: NotRequired[ResolverRuleAssociationStatusType]
    StatusMessage: NotRequired[str]


class FirewallDomainListTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    DomainCount: NotRequired[int]
    Status: NotRequired[FirewallDomainListStatusType]
    StatusMessage: NotRequired[str]
    ManagedOwnerName: NotRequired[str]
    CreatorRequestId: NotRequired[str]
    CreationTime: NotRequired[str]
    ModificationTime: NotRequired[str]


class FirewallRuleGroupTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    RuleCount: NotRequired[int]
    Status: NotRequired[FirewallRuleGroupStatusType]
    StatusMessage: NotRequired[str]
    OwnerId: NotRequired[str]
    CreatorRequestId: NotRequired[str]
    ShareStatus: NotRequired[ShareStatusType]
    CreationTime: NotRequired[str]
    ModificationTime: NotRequired[str]


class CreateFirewallRuleRequestRequestTypeDef(TypedDict):
    CreatorRequestId: str
    FirewallRuleGroupId: str
    Priority: int
    Action: ActionType
    Name: str
    FirewallDomainListId: NotRequired[str]
    BlockResponse: NotRequired[BlockResponseType]
    BlockOverrideDomain: NotRequired[str]
    BlockOverrideDnsType: NotRequired[Literal["CNAME"]]
    BlockOverrideTtl: NotRequired[int]
    FirewallDomainRedirectionAction: NotRequired[FirewallDomainRedirectionActionType]
    Qtype: NotRequired[str]
    DnsThreatProtection: NotRequired[DnsThreatProtectionType]
    ConfidenceThreshold: NotRequired[ConfidenceThresholdType]


class FirewallRuleTypeDef(TypedDict):
    FirewallRuleGroupId: NotRequired[str]
    FirewallDomainListId: NotRequired[str]
    FirewallThreatProtectionId: NotRequired[str]
    Name: NotRequired[str]
    Priority: NotRequired[int]
    Action: NotRequired[ActionType]
    BlockResponse: NotRequired[BlockResponseType]
    BlockOverrideDomain: NotRequired[str]
    BlockOverrideDnsType: NotRequired[Literal["CNAME"]]
    BlockOverrideTtl: NotRequired[int]
    CreatorRequestId: NotRequired[str]
    CreationTime: NotRequired[str]
    ModificationTime: NotRequired[str]
    FirewallDomainRedirectionAction: NotRequired[FirewallDomainRedirectionActionType]
    Qtype: NotRequired[str]
    DnsThreatProtection: NotRequired[DnsThreatProtectionType]
    ConfidenceThreshold: NotRequired[ConfidenceThresholdType]


class OutpostResolverTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreationTime: NotRequired[str]
    ModificationTime: NotRequired[str]
    CreatorRequestId: NotRequired[str]
    Id: NotRequired[str]
    InstanceCount: NotRequired[int]
    PreferredInstanceType: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[OutpostResolverStatusType]
    StatusMessage: NotRequired[str]
    OutpostArn: NotRequired[str]


class IpAddressRequestTypeDef(TypedDict):
    SubnetId: str
    Ip: NotRequired[str]
    Ipv6: NotRequired[str]


class ResolverQueryLogConfigTypeDef(TypedDict):
    Id: NotRequired[str]
    OwnerId: NotRequired[str]
    Status: NotRequired[ResolverQueryLogConfigStatusType]
    ShareStatus: NotRequired[ShareStatusType]
    AssociationCount: NotRequired[int]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    DestinationArn: NotRequired[str]
    CreatorRequestId: NotRequired[str]
    CreationTime: NotRequired[str]


TargetAddressTypeDef = TypedDict(
    "TargetAddressTypeDef",
    {
        "Ip": NotRequired[str],
        "Port": NotRequired[int],
        "Ipv6": NotRequired[str],
        "Protocol": NotRequired[ProtocolType],
        "ServerNameIndication": NotRequired[str],
    },
)


class DeleteFirewallDomainListRequestRequestTypeDef(TypedDict):
    FirewallDomainListId: str


class DeleteFirewallRuleGroupRequestRequestTypeDef(TypedDict):
    FirewallRuleGroupId: str


class DeleteFirewallRuleRequestRequestTypeDef(TypedDict):
    FirewallRuleGroupId: str
    FirewallDomainListId: NotRequired[str]
    FirewallThreatProtectionId: NotRequired[str]
    Qtype: NotRequired[str]


class DeleteOutpostResolverRequestRequestTypeDef(TypedDict):
    Id: str


class DeleteResolverEndpointRequestRequestTypeDef(TypedDict):
    ResolverEndpointId: str


class DeleteResolverQueryLogConfigRequestRequestTypeDef(TypedDict):
    ResolverQueryLogConfigId: str


class DeleteResolverRuleRequestRequestTypeDef(TypedDict):
    ResolverRuleId: str


class DisassociateFirewallRuleGroupRequestRequestTypeDef(TypedDict):
    FirewallRuleGroupAssociationId: str


class DisassociateResolverQueryLogConfigRequestRequestTypeDef(TypedDict):
    ResolverQueryLogConfigId: str
    ResourceId: str


class DisassociateResolverRuleRequestRequestTypeDef(TypedDict):
    VPCId: str
    ResolverRuleId: str


class FilterTypeDef(TypedDict):
    Name: NotRequired[str]
    Values: NotRequired[Sequence[str]]


class FirewallConfigTypeDef(TypedDict):
    Id: NotRequired[str]
    ResourceId: NotRequired[str]
    OwnerId: NotRequired[str]
    FirewallFailOpen: NotRequired[FirewallFailOpenStatusType]


class FirewallDomainListMetadataTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    CreatorRequestId: NotRequired[str]
    ManagedOwnerName: NotRequired[str]


class FirewallRuleGroupMetadataTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    OwnerId: NotRequired[str]
    CreatorRequestId: NotRequired[str]
    ShareStatus: NotRequired[ShareStatusType]


class GetFirewallConfigRequestRequestTypeDef(TypedDict):
    ResourceId: str


class GetFirewallDomainListRequestRequestTypeDef(TypedDict):
    FirewallDomainListId: str


class GetFirewallRuleGroupAssociationRequestRequestTypeDef(TypedDict):
    FirewallRuleGroupAssociationId: str


class GetFirewallRuleGroupPolicyRequestRequestTypeDef(TypedDict):
    Arn: str


class GetFirewallRuleGroupRequestRequestTypeDef(TypedDict):
    FirewallRuleGroupId: str


class GetOutpostResolverRequestRequestTypeDef(TypedDict):
    Id: str


class GetResolverConfigRequestRequestTypeDef(TypedDict):
    ResourceId: str


class ResolverConfigTypeDef(TypedDict):
    Id: NotRequired[str]
    ResourceId: NotRequired[str]
    OwnerId: NotRequired[str]
    AutodefinedReverse: NotRequired[ResolverAutodefinedReverseStatusType]


class GetResolverDnssecConfigRequestRequestTypeDef(TypedDict):
    ResourceId: str


class ResolverDnssecConfigTypeDef(TypedDict):
    Id: NotRequired[str]
    OwnerId: NotRequired[str]
    ResourceId: NotRequired[str]
    ValidationStatus: NotRequired[ResolverDNSSECValidationStatusType]


class GetResolverEndpointRequestRequestTypeDef(TypedDict):
    ResolverEndpointId: str


class GetResolverQueryLogConfigAssociationRequestRequestTypeDef(TypedDict):
    ResolverQueryLogConfigAssociationId: str


class GetResolverQueryLogConfigPolicyRequestRequestTypeDef(TypedDict):
    Arn: str


class GetResolverQueryLogConfigRequestRequestTypeDef(TypedDict):
    ResolverQueryLogConfigId: str


class GetResolverRuleAssociationRequestRequestTypeDef(TypedDict):
    ResolverRuleAssociationId: str


class GetResolverRulePolicyRequestRequestTypeDef(TypedDict):
    Arn: str


class GetResolverRuleRequestRequestTypeDef(TypedDict):
    ResolverRuleId: str


class ImportFirewallDomainsRequestRequestTypeDef(TypedDict):
    FirewallDomainListId: str
    Operation: Literal["REPLACE"]
    DomainFileUrl: str


class IpAddressResponseTypeDef(TypedDict):
    IpId: NotRequired[str]
    SubnetId: NotRequired[str]
    Ip: NotRequired[str]
    Ipv6: NotRequired[str]
    Status: NotRequired[IpAddressStatusType]
    StatusMessage: NotRequired[str]
    CreationTime: NotRequired[str]
    ModificationTime: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListFirewallConfigsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListFirewallDomainListsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListFirewallDomainsRequestRequestTypeDef(TypedDict):
    FirewallDomainListId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListFirewallRuleGroupAssociationsRequestRequestTypeDef(TypedDict):
    FirewallRuleGroupId: NotRequired[str]
    VpcId: NotRequired[str]
    Priority: NotRequired[int]
    Status: NotRequired[FirewallRuleGroupAssociationStatusType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListFirewallRuleGroupsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListFirewallRulesRequestRequestTypeDef(TypedDict):
    FirewallRuleGroupId: str
    Priority: NotRequired[int]
    Action: NotRequired[ActionType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListOutpostResolversRequestRequestTypeDef(TypedDict):
    OutpostArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListResolverConfigsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListResolverEndpointIpAddressesRequestRequestTypeDef(TypedDict):
    ResolverEndpointId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class PutFirewallRuleGroupPolicyRequestRequestTypeDef(TypedDict):
    Arn: str
    FirewallRuleGroupPolicy: str


class PutResolverQueryLogConfigPolicyRequestRequestTypeDef(TypedDict):
    Arn: str
    ResolverQueryLogConfigPolicy: str


class PutResolverRulePolicyRequestRequestTypeDef(TypedDict):
    Arn: str
    ResolverRulePolicy: str


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateFirewallConfigRequestRequestTypeDef(TypedDict):
    ResourceId: str
    FirewallFailOpen: FirewallFailOpenStatusType


class UpdateFirewallDomainsRequestRequestTypeDef(TypedDict):
    FirewallDomainListId: str
    Operation: FirewallDomainUpdateOperationType
    Domains: Sequence[str]


class UpdateFirewallRuleGroupAssociationRequestRequestTypeDef(TypedDict):
    FirewallRuleGroupAssociationId: str
    Priority: NotRequired[int]
    MutationProtection: NotRequired[MutationProtectionStatusType]
    Name: NotRequired[str]


class UpdateFirewallRuleRequestRequestTypeDef(TypedDict):
    FirewallRuleGroupId: str
    FirewallDomainListId: NotRequired[str]
    FirewallThreatProtectionId: NotRequired[str]
    Priority: NotRequired[int]
    Action: NotRequired[ActionType]
    BlockResponse: NotRequired[BlockResponseType]
    BlockOverrideDomain: NotRequired[str]
    BlockOverrideDnsType: NotRequired[Literal["CNAME"]]
    BlockOverrideTtl: NotRequired[int]
    Name: NotRequired[str]
    FirewallDomainRedirectionAction: NotRequired[FirewallDomainRedirectionActionType]
    Qtype: NotRequired[str]
    DnsThreatProtection: NotRequired[DnsThreatProtectionType]
    ConfidenceThreshold: NotRequired[ConfidenceThresholdType]


class UpdateIpAddressTypeDef(TypedDict):
    IpId: str
    Ipv6: str


class UpdateOutpostResolverRequestRequestTypeDef(TypedDict):
    Id: str
    Name: NotRequired[str]
    InstanceCount: NotRequired[int]
    PreferredInstanceType: NotRequired[str]


class UpdateResolverConfigRequestRequestTypeDef(TypedDict):
    ResourceId: str
    AutodefinedReverseFlag: AutodefinedReverseFlagType


class UpdateResolverDnssecConfigRequestRequestTypeDef(TypedDict):
    ResourceId: str
    Validation: ValidationType


class AssociateFirewallRuleGroupRequestRequestTypeDef(TypedDict):
    CreatorRequestId: str
    FirewallRuleGroupId: str
    VpcId: str
    Priority: int
    Name: str
    MutationProtection: NotRequired[MutationProtectionStatusType]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateFirewallDomainListRequestRequestTypeDef(TypedDict):
    CreatorRequestId: str
    Name: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateFirewallRuleGroupRequestRequestTypeDef(TypedDict):
    CreatorRequestId: str
    Name: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateOutpostResolverRequestRequestTypeDef(TypedDict):
    CreatorRequestId: str
    Name: str
    PreferredInstanceType: str
    OutpostArn: str
    InstanceCount: NotRequired[int]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateResolverQueryLogConfigRequestRequestTypeDef(TypedDict):
    Name: str
    DestinationArn: str
    CreatorRequestId: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]


class AssociateFirewallRuleGroupResponseTypeDef(TypedDict):
    FirewallRuleGroupAssociation: FirewallRuleGroupAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateFirewallRuleGroupResponseTypeDef(TypedDict):
    FirewallRuleGroupAssociation: FirewallRuleGroupAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetFirewallRuleGroupAssociationResponseTypeDef(TypedDict):
    FirewallRuleGroupAssociation: FirewallRuleGroupAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetFirewallRuleGroupPolicyResponseTypeDef(TypedDict):
    FirewallRuleGroupPolicy: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetResolverQueryLogConfigPolicyResponseTypeDef(TypedDict):
    ResolverQueryLogConfigPolicy: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetResolverRulePolicyResponseTypeDef(TypedDict):
    ResolverRulePolicy: str
    ResponseMetadata: ResponseMetadataTypeDef


class ImportFirewallDomainsResponseTypeDef(TypedDict):
    Id: str
    Name: str
    Status: FirewallDomainListStatusType
    StatusMessage: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListFirewallDomainsResponseTypeDef(TypedDict):
    Domains: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListFirewallRuleGroupAssociationsResponseTypeDef(TypedDict):
    FirewallRuleGroupAssociations: List[FirewallRuleGroupAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PutFirewallRuleGroupPolicyResponseTypeDef(TypedDict):
    ReturnValue: bool
    ResponseMetadata: ResponseMetadataTypeDef


class PutResolverQueryLogConfigPolicyResponseTypeDef(TypedDict):
    ReturnValue: bool
    ResponseMetadata: ResponseMetadataTypeDef


class PutResolverRulePolicyResponseTypeDef(TypedDict):
    ReturnValue: bool
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFirewallDomainsResponseTypeDef(TypedDict):
    Id: str
    Name: str
    Status: FirewallDomainListStatusType
    StatusMessage: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFirewallRuleGroupAssociationResponseTypeDef(TypedDict):
    FirewallRuleGroupAssociation: FirewallRuleGroupAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateResolverEndpointIpAddressRequestRequestTypeDef(TypedDict):
    ResolverEndpointId: str
    IpAddress: IpAddressUpdateTypeDef


class DisassociateResolverEndpointIpAddressRequestRequestTypeDef(TypedDict):
    ResolverEndpointId: str
    IpAddress: IpAddressUpdateTypeDef


class AssociateResolverEndpointIpAddressResponseTypeDef(TypedDict):
    ResolverEndpoint: ResolverEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateResolverEndpointResponseTypeDef(TypedDict):
    ResolverEndpoint: ResolverEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteResolverEndpointResponseTypeDef(TypedDict):
    ResolverEndpoint: ResolverEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateResolverEndpointIpAddressResponseTypeDef(TypedDict):
    ResolverEndpoint: ResolverEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetResolverEndpointResponseTypeDef(TypedDict):
    ResolverEndpoint: ResolverEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListResolverEndpointsResponseTypeDef(TypedDict):
    MaxResults: int
    ResolverEndpoints: List[ResolverEndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateResolverEndpointResponseTypeDef(TypedDict):
    ResolverEndpoint: ResolverEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateResolverQueryLogConfigResponseTypeDef(TypedDict):
    ResolverQueryLogConfigAssociation: ResolverQueryLogConfigAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateResolverQueryLogConfigResponseTypeDef(TypedDict):
    ResolverQueryLogConfigAssociation: ResolverQueryLogConfigAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetResolverQueryLogConfigAssociationResponseTypeDef(TypedDict):
    ResolverQueryLogConfigAssociation: ResolverQueryLogConfigAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListResolverQueryLogConfigAssociationsResponseTypeDef(TypedDict):
    TotalCount: int
    TotalFilteredCount: int
    ResolverQueryLogConfigAssociations: List[ResolverQueryLogConfigAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AssociateResolverRuleResponseTypeDef(TypedDict):
    ResolverRuleAssociation: ResolverRuleAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateResolverRuleResponseTypeDef(TypedDict):
    ResolverRuleAssociation: ResolverRuleAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetResolverRuleAssociationResponseTypeDef(TypedDict):
    ResolverRuleAssociation: ResolverRuleAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListResolverRuleAssociationsResponseTypeDef(TypedDict):
    MaxResults: int
    ResolverRuleAssociations: List[ResolverRuleAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateFirewallDomainListResponseTypeDef(TypedDict):
    FirewallDomainList: FirewallDomainListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteFirewallDomainListResponseTypeDef(TypedDict):
    FirewallDomainList: FirewallDomainListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetFirewallDomainListResponseTypeDef(TypedDict):
    FirewallDomainList: FirewallDomainListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFirewallRuleGroupResponseTypeDef(TypedDict):
    FirewallRuleGroup: FirewallRuleGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteFirewallRuleGroupResponseTypeDef(TypedDict):
    FirewallRuleGroup: FirewallRuleGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetFirewallRuleGroupResponseTypeDef(TypedDict):
    FirewallRuleGroup: FirewallRuleGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFirewallRuleResponseTypeDef(TypedDict):
    FirewallRule: FirewallRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteFirewallRuleResponseTypeDef(TypedDict):
    FirewallRule: FirewallRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListFirewallRulesResponseTypeDef(TypedDict):
    FirewallRules: List[FirewallRuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateFirewallRuleResponseTypeDef(TypedDict):
    FirewallRule: FirewallRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateOutpostResolverResponseTypeDef(TypedDict):
    OutpostResolver: OutpostResolverTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteOutpostResolverResponseTypeDef(TypedDict):
    OutpostResolver: OutpostResolverTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetOutpostResolverResponseTypeDef(TypedDict):
    OutpostResolver: OutpostResolverTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListOutpostResolversResponseTypeDef(TypedDict):
    OutpostResolvers: List[OutpostResolverTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateOutpostResolverResponseTypeDef(TypedDict):
    OutpostResolver: OutpostResolverTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateResolverEndpointRequestRequestTypeDef(TypedDict):
    CreatorRequestId: str
    SecurityGroupIds: Sequence[str]
    Direction: ResolverEndpointDirectionType
    IpAddresses: Sequence[IpAddressRequestTypeDef]
    Name: NotRequired[str]
    OutpostArn: NotRequired[str]
    PreferredInstanceType: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ResolverEndpointType: NotRequired[ResolverEndpointTypeType]
    Protocols: NotRequired[Sequence[ProtocolType]]


class CreateResolverQueryLogConfigResponseTypeDef(TypedDict):
    ResolverQueryLogConfig: ResolverQueryLogConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteResolverQueryLogConfigResponseTypeDef(TypedDict):
    ResolverQueryLogConfig: ResolverQueryLogConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetResolverQueryLogConfigResponseTypeDef(TypedDict):
    ResolverQueryLogConfig: ResolverQueryLogConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListResolverQueryLogConfigsResponseTypeDef(TypedDict):
    TotalCount: int
    TotalFilteredCount: int
    ResolverQueryLogConfigs: List[ResolverQueryLogConfigTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateResolverRuleRequestRequestTypeDef(TypedDict):
    CreatorRequestId: str
    RuleType: RuleTypeOptionType
    Name: NotRequired[str]
    DomainName: NotRequired[str]
    TargetIps: NotRequired[Sequence[TargetAddressTypeDef]]
    ResolverEndpointId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class ResolverRuleConfigTypeDef(TypedDict):
    Name: NotRequired[str]
    TargetIps: NotRequired[Sequence[TargetAddressTypeDef]]
    ResolverEndpointId: NotRequired[str]


class ResolverRuleTypeDef(TypedDict):
    Id: NotRequired[str]
    CreatorRequestId: NotRequired[str]
    Arn: NotRequired[str]
    DomainName: NotRequired[str]
    Status: NotRequired[ResolverRuleStatusType]
    StatusMessage: NotRequired[str]
    RuleType: NotRequired[RuleTypeOptionType]
    Name: NotRequired[str]
    TargetIps: NotRequired[List[TargetAddressTypeDef]]
    ResolverEndpointId: NotRequired[str]
    OwnerId: NotRequired[str]
    ShareStatus: NotRequired[ShareStatusType]
    CreationTime: NotRequired[str]
    ModificationTime: NotRequired[str]


class ListResolverDnssecConfigsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class ListResolverEndpointsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class ListResolverQueryLogConfigAssociationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    SortBy: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]


class ListResolverQueryLogConfigsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    SortBy: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]


class ListResolverRuleAssociationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class ListResolverRulesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class GetFirewallConfigResponseTypeDef(TypedDict):
    FirewallConfig: FirewallConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListFirewallConfigsResponseTypeDef(TypedDict):
    FirewallConfigs: List[FirewallConfigTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateFirewallConfigResponseTypeDef(TypedDict):
    FirewallConfig: FirewallConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListFirewallDomainListsResponseTypeDef(TypedDict):
    FirewallDomainLists: List[FirewallDomainListMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListFirewallRuleGroupsResponseTypeDef(TypedDict):
    FirewallRuleGroups: List[FirewallRuleGroupMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetResolverConfigResponseTypeDef(TypedDict):
    ResolverConfig: ResolverConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListResolverConfigsResponseTypeDef(TypedDict):
    ResolverConfigs: List[ResolverConfigTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateResolverConfigResponseTypeDef(TypedDict):
    ResolverConfig: ResolverConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetResolverDnssecConfigResponseTypeDef(TypedDict):
    ResolverDNSSECConfig: ResolverDnssecConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListResolverDnssecConfigsResponseTypeDef(TypedDict):
    ResolverDnssecConfigs: List[ResolverDnssecConfigTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateResolverDnssecConfigResponseTypeDef(TypedDict):
    ResolverDNSSECConfig: ResolverDnssecConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListResolverEndpointIpAddressesResponseTypeDef(TypedDict):
    MaxResults: int
    IpAddresses: List[IpAddressResponseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListFirewallConfigsRequestListFirewallConfigsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFirewallDomainListsRequestListFirewallDomainListsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef(TypedDict):
    FirewallDomainListId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFirewallRuleGroupAssociationsRequestListFirewallRuleGroupAssociationsPaginateTypeDef(
    TypedDict
):
    FirewallRuleGroupId: NotRequired[str]
    VpcId: NotRequired[str]
    Priority: NotRequired[int]
    Status: NotRequired[FirewallRuleGroupAssociationStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFirewallRuleGroupsRequestListFirewallRuleGroupsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFirewallRulesRequestListFirewallRulesPaginateTypeDef(TypedDict):
    FirewallRuleGroupId: str
    Priority: NotRequired[int]
    Action: NotRequired[ActionType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOutpostResolversRequestListOutpostResolversPaginateTypeDef(TypedDict):
    OutpostArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResolverConfigsRequestListResolverConfigsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResolverDnssecConfigsRequestListResolverDnssecConfigsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef(
    TypedDict
):
    ResolverEndpointId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResolverEndpointsRequestListResolverEndpointsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResolverQueryLogConfigAssociationsRequestListResolverQueryLogConfigAssociationsPaginateTypeDef(
    TypedDict
):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    SortBy: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResolverQueryLogConfigsRequestListResolverQueryLogConfigsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    SortBy: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResolverRuleAssociationsRequestListResolverRuleAssociationsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResolverRulesRequestListResolverRulesPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(TypedDict):
    ResourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class UpdateResolverEndpointRequestRequestTypeDef(TypedDict):
    ResolverEndpointId: str
    Name: NotRequired[str]
    ResolverEndpointType: NotRequired[ResolverEndpointTypeType]
    UpdateIpAddresses: NotRequired[Sequence[UpdateIpAddressTypeDef]]
    Protocols: NotRequired[Sequence[ProtocolType]]


class UpdateResolverRuleRequestRequestTypeDef(TypedDict):
    ResolverRuleId: str
    Config: ResolverRuleConfigTypeDef


class CreateResolverRuleResponseTypeDef(TypedDict):
    ResolverRule: ResolverRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteResolverRuleResponseTypeDef(TypedDict):
    ResolverRule: ResolverRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetResolverRuleResponseTypeDef(TypedDict):
    ResolverRule: ResolverRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListResolverRulesResponseTypeDef(TypedDict):
    MaxResults: int
    ResolverRules: List[ResolverRuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateResolverRuleResponseTypeDef(TypedDict):
    ResolverRule: ResolverRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
