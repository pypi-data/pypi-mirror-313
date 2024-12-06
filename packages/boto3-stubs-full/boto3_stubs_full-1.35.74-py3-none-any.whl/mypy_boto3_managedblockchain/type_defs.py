"""
Type annotations for managedblockchain service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain/type_defs/)

Usage::

    ```python
    from mypy_boto3_managedblockchain.type_defs import AccessorSummaryTypeDef

    data: AccessorSummaryTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AccessorNetworkTypeType,
    AccessorStatusType,
    EditionType,
    FrameworkType,
    InvitationStatusType,
    MemberStatusType,
    NetworkStatusType,
    NodeStatusType,
    ProposalStatusType,
    StateDBTypeType,
    ThresholdComparatorType,
    VoteValueType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccessorSummaryTypeDef",
    "AccessorTypeDef",
    "ApprovalThresholdPolicyTypeDef",
    "CreateAccessorInputRequestTypeDef",
    "CreateAccessorOutputTypeDef",
    "CreateMemberInputRequestTypeDef",
    "CreateMemberOutputTypeDef",
    "CreateNetworkInputRequestTypeDef",
    "CreateNetworkOutputTypeDef",
    "CreateNodeInputRequestTypeDef",
    "CreateNodeOutputTypeDef",
    "CreateProposalInputRequestTypeDef",
    "CreateProposalOutputTypeDef",
    "DeleteAccessorInputRequestTypeDef",
    "DeleteMemberInputRequestTypeDef",
    "DeleteNodeInputRequestTypeDef",
    "GetAccessorInputRequestTypeDef",
    "GetAccessorOutputTypeDef",
    "GetMemberInputRequestTypeDef",
    "GetMemberOutputTypeDef",
    "GetNetworkInputRequestTypeDef",
    "GetNetworkOutputTypeDef",
    "GetNodeInputRequestTypeDef",
    "GetNodeOutputTypeDef",
    "GetProposalInputRequestTypeDef",
    "GetProposalOutputTypeDef",
    "InvitationTypeDef",
    "InviteActionTypeDef",
    "ListAccessorsInputListAccessorsPaginateTypeDef",
    "ListAccessorsInputRequestTypeDef",
    "ListAccessorsOutputTypeDef",
    "ListInvitationsInputRequestTypeDef",
    "ListInvitationsOutputTypeDef",
    "ListMembersInputRequestTypeDef",
    "ListMembersOutputTypeDef",
    "ListNetworksInputRequestTypeDef",
    "ListNetworksOutputTypeDef",
    "ListNodesInputRequestTypeDef",
    "ListNodesOutputTypeDef",
    "ListProposalVotesInputRequestTypeDef",
    "ListProposalVotesOutputTypeDef",
    "ListProposalsInputRequestTypeDef",
    "ListProposalsOutputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LogConfigurationTypeDef",
    "LogConfigurationsTypeDef",
    "MemberConfigurationTypeDef",
    "MemberFabricAttributesTypeDef",
    "MemberFabricConfigurationTypeDef",
    "MemberFabricLogPublishingConfigurationTypeDef",
    "MemberFrameworkAttributesTypeDef",
    "MemberFrameworkConfigurationTypeDef",
    "MemberLogPublishingConfigurationTypeDef",
    "MemberSummaryTypeDef",
    "MemberTypeDef",
    "NetworkEthereumAttributesTypeDef",
    "NetworkFabricAttributesTypeDef",
    "NetworkFabricConfigurationTypeDef",
    "NetworkFrameworkAttributesTypeDef",
    "NetworkFrameworkConfigurationTypeDef",
    "NetworkSummaryTypeDef",
    "NetworkTypeDef",
    "NodeConfigurationTypeDef",
    "NodeEthereumAttributesTypeDef",
    "NodeFabricAttributesTypeDef",
    "NodeFabricLogPublishingConfigurationTypeDef",
    "NodeFrameworkAttributesTypeDef",
    "NodeLogPublishingConfigurationTypeDef",
    "NodeSummaryTypeDef",
    "NodeTypeDef",
    "PaginatorConfigTypeDef",
    "ProposalActionsOutputTypeDef",
    "ProposalActionsTypeDef",
    "ProposalSummaryTypeDef",
    "ProposalTypeDef",
    "RejectInvitationInputRequestTypeDef",
    "RemoveActionTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateMemberInputRequestTypeDef",
    "UpdateNodeInputRequestTypeDef",
    "VoteOnProposalInputRequestTypeDef",
    "VoteSummaryTypeDef",
    "VotingPolicyTypeDef",
)

AccessorSummaryTypeDef = TypedDict(
    "AccessorSummaryTypeDef",
    {
        "Id": NotRequired[str],
        "Type": NotRequired[Literal["BILLING_TOKEN"]],
        "Status": NotRequired[AccessorStatusType],
        "CreationDate": NotRequired[datetime],
        "Arn": NotRequired[str],
        "NetworkType": NotRequired[AccessorNetworkTypeType],
    },
)
AccessorTypeDef = TypedDict(
    "AccessorTypeDef",
    {
        "Id": NotRequired[str],
        "Type": NotRequired[Literal["BILLING_TOKEN"]],
        "BillingToken": NotRequired[str],
        "Status": NotRequired[AccessorStatusType],
        "CreationDate": NotRequired[datetime],
        "Arn": NotRequired[str],
        "Tags": NotRequired[Dict[str, str]],
        "NetworkType": NotRequired[AccessorNetworkTypeType],
    },
)


class ApprovalThresholdPolicyTypeDef(TypedDict):
    ThresholdPercentage: NotRequired[int]
    ProposalDurationInHours: NotRequired[int]
    ThresholdComparator: NotRequired[ThresholdComparatorType]


class CreateAccessorInputRequestTypeDef(TypedDict):
    ClientRequestToken: str
    AccessorType: Literal["BILLING_TOKEN"]
    Tags: NotRequired[Mapping[str, str]]
    NetworkType: NotRequired[AccessorNetworkTypeType]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeleteAccessorInputRequestTypeDef(TypedDict):
    AccessorId: str


class DeleteMemberInputRequestTypeDef(TypedDict):
    NetworkId: str
    MemberId: str


class DeleteNodeInputRequestTypeDef(TypedDict):
    NetworkId: str
    NodeId: str
    MemberId: NotRequired[str]


class GetAccessorInputRequestTypeDef(TypedDict):
    AccessorId: str


class GetMemberInputRequestTypeDef(TypedDict):
    NetworkId: str
    MemberId: str


class GetNetworkInputRequestTypeDef(TypedDict):
    NetworkId: str


class GetNodeInputRequestTypeDef(TypedDict):
    NetworkId: str
    NodeId: str
    MemberId: NotRequired[str]


class GetProposalInputRequestTypeDef(TypedDict):
    NetworkId: str
    ProposalId: str


class NetworkSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    Framework: NotRequired[FrameworkType]
    FrameworkVersion: NotRequired[str]
    Status: NotRequired[NetworkStatusType]
    CreationDate: NotRequired[datetime]
    Arn: NotRequired[str]


class InviteActionTypeDef(TypedDict):
    Principal: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAccessorsInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    NetworkType: NotRequired[AccessorNetworkTypeType]


class ListInvitationsInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListMembersInputRequestTypeDef(TypedDict):
    NetworkId: str
    Name: NotRequired[str]
    Status: NotRequired[MemberStatusType]
    IsOwned: NotRequired[bool]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class MemberSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    Status: NotRequired[MemberStatusType]
    CreationDate: NotRequired[datetime]
    IsOwned: NotRequired[bool]
    Arn: NotRequired[str]


class ListNetworksInputRequestTypeDef(TypedDict):
    Name: NotRequired[str]
    Framework: NotRequired[FrameworkType]
    Status: NotRequired[NetworkStatusType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListNodesInputRequestTypeDef(TypedDict):
    NetworkId: str
    MemberId: NotRequired[str]
    Status: NotRequired[NodeStatusType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class NodeSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Status: NotRequired[NodeStatusType]
    CreationDate: NotRequired[datetime]
    AvailabilityZone: NotRequired[str]
    InstanceType: NotRequired[str]
    Arn: NotRequired[str]


class ListProposalVotesInputRequestTypeDef(TypedDict):
    NetworkId: str
    ProposalId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class VoteSummaryTypeDef(TypedDict):
    Vote: NotRequired[VoteValueType]
    MemberName: NotRequired[str]
    MemberId: NotRequired[str]


class ListProposalsInputRequestTypeDef(TypedDict):
    NetworkId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ProposalSummaryTypeDef(TypedDict):
    ProposalId: NotRequired[str]
    Description: NotRequired[str]
    ProposedByMemberId: NotRequired[str]
    ProposedByMemberName: NotRequired[str]
    Status: NotRequired[ProposalStatusType]
    CreationDate: NotRequired[datetime]
    ExpirationDate: NotRequired[datetime]
    Arn: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class LogConfigurationTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class MemberFabricAttributesTypeDef(TypedDict):
    AdminUsername: NotRequired[str]
    CaEndpoint: NotRequired[str]


class MemberFabricConfigurationTypeDef(TypedDict):
    AdminUsername: str
    AdminPassword: str


class NetworkEthereumAttributesTypeDef(TypedDict):
    ChainId: NotRequired[str]


class NetworkFabricAttributesTypeDef(TypedDict):
    OrderingServiceEndpoint: NotRequired[str]
    Edition: NotRequired[EditionType]


class NetworkFabricConfigurationTypeDef(TypedDict):
    Edition: EditionType


class NodeEthereumAttributesTypeDef(TypedDict):
    HttpEndpoint: NotRequired[str]
    WebSocketEndpoint: NotRequired[str]


class NodeFabricAttributesTypeDef(TypedDict):
    PeerEndpoint: NotRequired[str]
    PeerEventEndpoint: NotRequired[str]


class RemoveActionTypeDef(TypedDict):
    MemberId: str


class RejectInvitationInputRequestTypeDef(TypedDict):
    InvitationId: str


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class VoteOnProposalInputRequestTypeDef(TypedDict):
    NetworkId: str
    ProposalId: str
    VoterMemberId: str
    Vote: VoteValueType


class VotingPolicyTypeDef(TypedDict):
    ApprovalThresholdPolicy: NotRequired[ApprovalThresholdPolicyTypeDef]


class CreateAccessorOutputTypeDef(TypedDict):
    AccessorId: str
    BillingToken: str
    NetworkType: AccessorNetworkTypeType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMemberOutputTypeDef(TypedDict):
    MemberId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateNetworkOutputTypeDef(TypedDict):
    NetworkId: str
    MemberId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateNodeOutputTypeDef(TypedDict):
    NodeId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProposalOutputTypeDef(TypedDict):
    ProposalId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetAccessorOutputTypeDef(TypedDict):
    Accessor: AccessorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAccessorsOutputTypeDef(TypedDict):
    Accessors: List[AccessorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class InvitationTypeDef(TypedDict):
    InvitationId: NotRequired[str]
    CreationDate: NotRequired[datetime]
    ExpirationDate: NotRequired[datetime]
    Status: NotRequired[InvitationStatusType]
    NetworkSummary: NotRequired[NetworkSummaryTypeDef]
    Arn: NotRequired[str]


class ListNetworksOutputTypeDef(TypedDict):
    Networks: List[NetworkSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListAccessorsInputListAccessorsPaginateTypeDef(TypedDict):
    NetworkType: NotRequired[AccessorNetworkTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMembersOutputTypeDef(TypedDict):
    Members: List[MemberSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListNodesOutputTypeDef(TypedDict):
    Nodes: List[NodeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListProposalVotesOutputTypeDef(TypedDict):
    ProposalVotes: List[VoteSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListProposalsOutputTypeDef(TypedDict):
    Proposals: List[ProposalSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LogConfigurationsTypeDef(TypedDict):
    Cloudwatch: NotRequired[LogConfigurationTypeDef]


class MemberFrameworkAttributesTypeDef(TypedDict):
    Fabric: NotRequired[MemberFabricAttributesTypeDef]


class MemberFrameworkConfigurationTypeDef(TypedDict):
    Fabric: NotRequired[MemberFabricConfigurationTypeDef]


class NetworkFrameworkAttributesTypeDef(TypedDict):
    Fabric: NotRequired[NetworkFabricAttributesTypeDef]
    Ethereum: NotRequired[NetworkEthereumAttributesTypeDef]


class NetworkFrameworkConfigurationTypeDef(TypedDict):
    Fabric: NotRequired[NetworkFabricConfigurationTypeDef]


class NodeFrameworkAttributesTypeDef(TypedDict):
    Fabric: NotRequired[NodeFabricAttributesTypeDef]
    Ethereum: NotRequired[NodeEthereumAttributesTypeDef]


class ProposalActionsOutputTypeDef(TypedDict):
    Invitations: NotRequired[List[InviteActionTypeDef]]
    Removals: NotRequired[List[RemoveActionTypeDef]]


class ProposalActionsTypeDef(TypedDict):
    Invitations: NotRequired[Sequence[InviteActionTypeDef]]
    Removals: NotRequired[Sequence[RemoveActionTypeDef]]


class ListInvitationsOutputTypeDef(TypedDict):
    Invitations: List[InvitationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class MemberFabricLogPublishingConfigurationTypeDef(TypedDict):
    CaLogs: NotRequired[LogConfigurationsTypeDef]


class NodeFabricLogPublishingConfigurationTypeDef(TypedDict):
    ChaincodeLogs: NotRequired[LogConfigurationsTypeDef]
    PeerLogs: NotRequired[LogConfigurationsTypeDef]


class NetworkTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    Framework: NotRequired[FrameworkType]
    FrameworkVersion: NotRequired[str]
    FrameworkAttributes: NotRequired[NetworkFrameworkAttributesTypeDef]
    VpcEndpointServiceName: NotRequired[str]
    VotingPolicy: NotRequired[VotingPolicyTypeDef]
    Status: NotRequired[NetworkStatusType]
    CreationDate: NotRequired[datetime]
    Tags: NotRequired[Dict[str, str]]
    Arn: NotRequired[str]


class ProposalTypeDef(TypedDict):
    ProposalId: NotRequired[str]
    NetworkId: NotRequired[str]
    Description: NotRequired[str]
    Actions: NotRequired[ProposalActionsOutputTypeDef]
    ProposedByMemberId: NotRequired[str]
    ProposedByMemberName: NotRequired[str]
    Status: NotRequired[ProposalStatusType]
    CreationDate: NotRequired[datetime]
    ExpirationDate: NotRequired[datetime]
    YesVoteCount: NotRequired[int]
    NoVoteCount: NotRequired[int]
    OutstandingVoteCount: NotRequired[int]
    Tags: NotRequired[Dict[str, str]]
    Arn: NotRequired[str]


class CreateProposalInputRequestTypeDef(TypedDict):
    ClientRequestToken: str
    NetworkId: str
    MemberId: str
    Actions: ProposalActionsTypeDef
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class MemberLogPublishingConfigurationTypeDef(TypedDict):
    Fabric: NotRequired[MemberFabricLogPublishingConfigurationTypeDef]


class NodeLogPublishingConfigurationTypeDef(TypedDict):
    Fabric: NotRequired[NodeFabricLogPublishingConfigurationTypeDef]


class GetNetworkOutputTypeDef(TypedDict):
    Network: NetworkTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetProposalOutputTypeDef(TypedDict):
    Proposal: ProposalTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class MemberConfigurationTypeDef(TypedDict):
    Name: str
    FrameworkConfiguration: MemberFrameworkConfigurationTypeDef
    Description: NotRequired[str]
    LogPublishingConfiguration: NotRequired[MemberLogPublishingConfigurationTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    KmsKeyArn: NotRequired[str]


class MemberTypeDef(TypedDict):
    NetworkId: NotRequired[str]
    Id: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    FrameworkAttributes: NotRequired[MemberFrameworkAttributesTypeDef]
    LogPublishingConfiguration: NotRequired[MemberLogPublishingConfigurationTypeDef]
    Status: NotRequired[MemberStatusType]
    CreationDate: NotRequired[datetime]
    Tags: NotRequired[Dict[str, str]]
    Arn: NotRequired[str]
    KmsKeyArn: NotRequired[str]


class UpdateMemberInputRequestTypeDef(TypedDict):
    NetworkId: str
    MemberId: str
    LogPublishingConfiguration: NotRequired[MemberLogPublishingConfigurationTypeDef]


class NodeConfigurationTypeDef(TypedDict):
    InstanceType: str
    AvailabilityZone: NotRequired[str]
    LogPublishingConfiguration: NotRequired[NodeLogPublishingConfigurationTypeDef]
    StateDB: NotRequired[StateDBTypeType]


class NodeTypeDef(TypedDict):
    NetworkId: NotRequired[str]
    MemberId: NotRequired[str]
    Id: NotRequired[str]
    InstanceType: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    FrameworkAttributes: NotRequired[NodeFrameworkAttributesTypeDef]
    LogPublishingConfiguration: NotRequired[NodeLogPublishingConfigurationTypeDef]
    StateDB: NotRequired[StateDBTypeType]
    Status: NotRequired[NodeStatusType]
    CreationDate: NotRequired[datetime]
    Tags: NotRequired[Dict[str, str]]
    Arn: NotRequired[str]
    KmsKeyArn: NotRequired[str]


class UpdateNodeInputRequestTypeDef(TypedDict):
    NetworkId: str
    NodeId: str
    MemberId: NotRequired[str]
    LogPublishingConfiguration: NotRequired[NodeLogPublishingConfigurationTypeDef]


class CreateMemberInputRequestTypeDef(TypedDict):
    ClientRequestToken: str
    InvitationId: str
    NetworkId: str
    MemberConfiguration: MemberConfigurationTypeDef


class CreateNetworkInputRequestTypeDef(TypedDict):
    ClientRequestToken: str
    Name: str
    Framework: FrameworkType
    FrameworkVersion: str
    VotingPolicy: VotingPolicyTypeDef
    MemberConfiguration: MemberConfigurationTypeDef
    Description: NotRequired[str]
    FrameworkConfiguration: NotRequired[NetworkFrameworkConfigurationTypeDef]
    Tags: NotRequired[Mapping[str, str]]


class GetMemberOutputTypeDef(TypedDict):
    Member: MemberTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateNodeInputRequestTypeDef(TypedDict):
    ClientRequestToken: str
    NetworkId: str
    NodeConfiguration: NodeConfigurationTypeDef
    MemberId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class GetNodeOutputTypeDef(TypedDict):
    Node: NodeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
