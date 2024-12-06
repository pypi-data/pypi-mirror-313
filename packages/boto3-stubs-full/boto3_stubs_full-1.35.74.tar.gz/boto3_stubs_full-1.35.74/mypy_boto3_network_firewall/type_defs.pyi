"""
Type annotations for network-firewall service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_network_firewall/type_defs/)

Usage::

    ```python
    from mypy_boto3_network_firewall.type_defs import AddressTypeDef

    data: AddressTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AttachmentStatusType,
    ConfigurationSyncStateType,
    EncryptionTypeType,
    FirewallStatusValueType,
    GeneratedRulesTypeType,
    IdentifiedTypeType,
    IPAddressTypeType,
    LogDestinationTypeType,
    LogTypeType,
    PerObjectSyncStatusType,
    ResourceManagedStatusType,
    ResourceManagedTypeType,
    ResourceStatusType,
    RevocationCheckActionType,
    RuleGroupTypeType,
    RuleOrderType,
    StatefulActionType,
    StatefulRuleDirectionType,
    StatefulRuleProtocolType,
    StreamExceptionPolicyType,
    TargetTypeType,
    TCPFlagType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "ActionDefinitionOutputTypeDef",
    "ActionDefinitionTypeDef",
    "ActionDefinitionUnionTypeDef",
    "AddressTypeDef",
    "AnalysisResultTypeDef",
    "AssociateFirewallPolicyRequestRequestTypeDef",
    "AssociateFirewallPolicyResponseTypeDef",
    "AssociateSubnetsRequestRequestTypeDef",
    "AssociateSubnetsResponseTypeDef",
    "AttachmentTypeDef",
    "CIDRSummaryTypeDef",
    "CapacityUsageSummaryTypeDef",
    "CheckCertificateRevocationStatusActionsTypeDef",
    "CreateFirewallPolicyRequestRequestTypeDef",
    "CreateFirewallPolicyResponseTypeDef",
    "CreateFirewallRequestRequestTypeDef",
    "CreateFirewallResponseTypeDef",
    "CreateRuleGroupRequestRequestTypeDef",
    "CreateRuleGroupResponseTypeDef",
    "CreateTLSInspectionConfigurationRequestRequestTypeDef",
    "CreateTLSInspectionConfigurationResponseTypeDef",
    "CustomActionOutputTypeDef",
    "CustomActionTypeDef",
    "CustomActionUnionTypeDef",
    "DeleteFirewallPolicyRequestRequestTypeDef",
    "DeleteFirewallPolicyResponseTypeDef",
    "DeleteFirewallRequestRequestTypeDef",
    "DeleteFirewallResponseTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DeleteRuleGroupRequestRequestTypeDef",
    "DeleteRuleGroupResponseTypeDef",
    "DeleteTLSInspectionConfigurationRequestRequestTypeDef",
    "DeleteTLSInspectionConfigurationResponseTypeDef",
    "DescribeFirewallPolicyRequestRequestTypeDef",
    "DescribeFirewallPolicyResponseTypeDef",
    "DescribeFirewallRequestRequestTypeDef",
    "DescribeFirewallResponseTypeDef",
    "DescribeLoggingConfigurationRequestRequestTypeDef",
    "DescribeLoggingConfigurationResponseTypeDef",
    "DescribeResourcePolicyRequestRequestTypeDef",
    "DescribeResourcePolicyResponseTypeDef",
    "DescribeRuleGroupMetadataRequestRequestTypeDef",
    "DescribeRuleGroupMetadataResponseTypeDef",
    "DescribeRuleGroupRequestRequestTypeDef",
    "DescribeRuleGroupResponseTypeDef",
    "DescribeTLSInspectionConfigurationRequestRequestTypeDef",
    "DescribeTLSInspectionConfigurationResponseTypeDef",
    "DimensionTypeDef",
    "DisassociateSubnetsRequestRequestTypeDef",
    "DisassociateSubnetsResponseTypeDef",
    "EncryptionConfigurationTypeDef",
    "FirewallMetadataTypeDef",
    "FirewallPolicyMetadataTypeDef",
    "FirewallPolicyOutputTypeDef",
    "FirewallPolicyResponseTypeDef",
    "FirewallPolicyTypeDef",
    "FirewallStatusTypeDef",
    "FirewallTypeDef",
    "FlowTimeoutsTypeDef",
    "HeaderTypeDef",
    "IPSetMetadataTypeDef",
    "IPSetOutputTypeDef",
    "IPSetReferenceTypeDef",
    "IPSetTypeDef",
    "IPSetUnionTypeDef",
    "ListFirewallPoliciesRequestListFirewallPoliciesPaginateTypeDef",
    "ListFirewallPoliciesRequestRequestTypeDef",
    "ListFirewallPoliciesResponseTypeDef",
    "ListFirewallsRequestListFirewallsPaginateTypeDef",
    "ListFirewallsRequestRequestTypeDef",
    "ListFirewallsResponseTypeDef",
    "ListRuleGroupsRequestListRuleGroupsPaginateTypeDef",
    "ListRuleGroupsRequestRequestTypeDef",
    "ListRuleGroupsResponseTypeDef",
    "ListTLSInspectionConfigurationsRequestListTLSInspectionConfigurationsPaginateTypeDef",
    "ListTLSInspectionConfigurationsRequestRequestTypeDef",
    "ListTLSInspectionConfigurationsResponseTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LogDestinationConfigOutputTypeDef",
    "LogDestinationConfigTypeDef",
    "LogDestinationConfigUnionTypeDef",
    "LoggingConfigurationOutputTypeDef",
    "LoggingConfigurationTypeDef",
    "MatchAttributesOutputTypeDef",
    "MatchAttributesTypeDef",
    "MatchAttributesUnionTypeDef",
    "PaginatorConfigTypeDef",
    "PerObjectStatusTypeDef",
    "PolicyVariablesOutputTypeDef",
    "PolicyVariablesTypeDef",
    "PolicyVariablesUnionTypeDef",
    "PortRangeTypeDef",
    "PortSetOutputTypeDef",
    "PortSetTypeDef",
    "PortSetUnionTypeDef",
    "PublishMetricActionOutputTypeDef",
    "PublishMetricActionTypeDef",
    "PublishMetricActionUnionTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "ReferenceSetsOutputTypeDef",
    "ReferenceSetsTypeDef",
    "ReferenceSetsUnionTypeDef",
    "ResponseMetadataTypeDef",
    "RuleDefinitionOutputTypeDef",
    "RuleDefinitionTypeDef",
    "RuleDefinitionUnionTypeDef",
    "RuleGroupMetadataTypeDef",
    "RuleGroupOutputTypeDef",
    "RuleGroupResponseTypeDef",
    "RuleGroupTypeDef",
    "RuleOptionOutputTypeDef",
    "RuleOptionTypeDef",
    "RuleOptionUnionTypeDef",
    "RuleVariablesOutputTypeDef",
    "RuleVariablesTypeDef",
    "RuleVariablesUnionTypeDef",
    "RulesSourceListOutputTypeDef",
    "RulesSourceListTypeDef",
    "RulesSourceListUnionTypeDef",
    "RulesSourceOutputTypeDef",
    "RulesSourceTypeDef",
    "RulesSourceUnionTypeDef",
    "ServerCertificateConfigurationOutputTypeDef",
    "ServerCertificateConfigurationTypeDef",
    "ServerCertificateConfigurationUnionTypeDef",
    "ServerCertificateScopeOutputTypeDef",
    "ServerCertificateScopeTypeDef",
    "ServerCertificateScopeUnionTypeDef",
    "ServerCertificateTypeDef",
    "SourceMetadataTypeDef",
    "StatefulEngineOptionsTypeDef",
    "StatefulRuleGroupOverrideTypeDef",
    "StatefulRuleGroupReferenceTypeDef",
    "StatefulRuleOptionsTypeDef",
    "StatefulRuleOutputTypeDef",
    "StatefulRuleTypeDef",
    "StatefulRuleUnionTypeDef",
    "StatelessRuleGroupReferenceTypeDef",
    "StatelessRuleOutputTypeDef",
    "StatelessRuleTypeDef",
    "StatelessRuleUnionTypeDef",
    "StatelessRulesAndCustomActionsOutputTypeDef",
    "StatelessRulesAndCustomActionsTypeDef",
    "StatelessRulesAndCustomActionsUnionTypeDef",
    "SubnetMappingTypeDef",
    "SyncStateTypeDef",
    "TCPFlagFieldOutputTypeDef",
    "TCPFlagFieldTypeDef",
    "TCPFlagFieldUnionTypeDef",
    "TLSInspectionConfigurationMetadataTypeDef",
    "TLSInspectionConfigurationOutputTypeDef",
    "TLSInspectionConfigurationResponseTypeDef",
    "TLSInspectionConfigurationTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TlsCertificateDataTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFirewallDeleteProtectionRequestRequestTypeDef",
    "UpdateFirewallDeleteProtectionResponseTypeDef",
    "UpdateFirewallDescriptionRequestRequestTypeDef",
    "UpdateFirewallDescriptionResponseTypeDef",
    "UpdateFirewallEncryptionConfigurationRequestRequestTypeDef",
    "UpdateFirewallEncryptionConfigurationResponseTypeDef",
    "UpdateFirewallPolicyChangeProtectionRequestRequestTypeDef",
    "UpdateFirewallPolicyChangeProtectionResponseTypeDef",
    "UpdateFirewallPolicyRequestRequestTypeDef",
    "UpdateFirewallPolicyResponseTypeDef",
    "UpdateLoggingConfigurationRequestRequestTypeDef",
    "UpdateLoggingConfigurationResponseTypeDef",
    "UpdateRuleGroupRequestRequestTypeDef",
    "UpdateRuleGroupResponseTypeDef",
    "UpdateSubnetChangeProtectionRequestRequestTypeDef",
    "UpdateSubnetChangeProtectionResponseTypeDef",
    "UpdateTLSInspectionConfigurationRequestRequestTypeDef",
    "UpdateTLSInspectionConfigurationResponseTypeDef",
)

class AddressTypeDef(TypedDict):
    AddressDefinition: str

class AnalysisResultTypeDef(TypedDict):
    IdentifiedRuleIds: NotRequired[List[str]]
    IdentifiedType: NotRequired[IdentifiedTypeType]
    AnalysisDetail: NotRequired[str]

class AssociateFirewallPolicyRequestRequestTypeDef(TypedDict):
    FirewallPolicyArn: str
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class SubnetMappingTypeDef(TypedDict):
    SubnetId: str
    IPAddressType: NotRequired[IPAddressTypeType]

class AttachmentTypeDef(TypedDict):
    SubnetId: NotRequired[str]
    EndpointId: NotRequired[str]
    Status: NotRequired[AttachmentStatusType]
    StatusMessage: NotRequired[str]

class IPSetMetadataTypeDef(TypedDict):
    ResolvedCIDRCount: NotRequired[int]

class CheckCertificateRevocationStatusActionsTypeDef(TypedDict):
    RevokedStatusAction: NotRequired[RevocationCheckActionType]
    UnknownStatusAction: NotRequired[RevocationCheckActionType]

EncryptionConfigurationTypeDef = TypedDict(
    "EncryptionConfigurationTypeDef",
    {
        "Type": EncryptionTypeType,
        "KeyId": NotRequired[str],
    },
)

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class SourceMetadataTypeDef(TypedDict):
    SourceArn: NotRequired[str]
    SourceUpdateToken: NotRequired[str]

class DeleteFirewallPolicyRequestRequestTypeDef(TypedDict):
    FirewallPolicyName: NotRequired[str]
    FirewallPolicyArn: NotRequired[str]

class DeleteFirewallRequestRequestTypeDef(TypedDict):
    FirewallName: NotRequired[str]
    FirewallArn: NotRequired[str]

class DeleteResourcePolicyRequestRequestTypeDef(TypedDict):
    ResourceArn: str

DeleteRuleGroupRequestRequestTypeDef = TypedDict(
    "DeleteRuleGroupRequestRequestTypeDef",
    {
        "RuleGroupName": NotRequired[str],
        "RuleGroupArn": NotRequired[str],
        "Type": NotRequired[RuleGroupTypeType],
    },
)

class DeleteTLSInspectionConfigurationRequestRequestTypeDef(TypedDict):
    TLSInspectionConfigurationArn: NotRequired[str]
    TLSInspectionConfigurationName: NotRequired[str]

class DescribeFirewallPolicyRequestRequestTypeDef(TypedDict):
    FirewallPolicyName: NotRequired[str]
    FirewallPolicyArn: NotRequired[str]

class DescribeFirewallRequestRequestTypeDef(TypedDict):
    FirewallName: NotRequired[str]
    FirewallArn: NotRequired[str]

class DescribeLoggingConfigurationRequestRequestTypeDef(TypedDict):
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]

class DescribeResourcePolicyRequestRequestTypeDef(TypedDict):
    ResourceArn: str

DescribeRuleGroupMetadataRequestRequestTypeDef = TypedDict(
    "DescribeRuleGroupMetadataRequestRequestTypeDef",
    {
        "RuleGroupName": NotRequired[str],
        "RuleGroupArn": NotRequired[str],
        "Type": NotRequired[RuleGroupTypeType],
    },
)

class StatefulRuleOptionsTypeDef(TypedDict):
    RuleOrder: NotRequired[RuleOrderType]

DescribeRuleGroupRequestRequestTypeDef = TypedDict(
    "DescribeRuleGroupRequestRequestTypeDef",
    {
        "RuleGroupName": NotRequired[str],
        "RuleGroupArn": NotRequired[str],
        "Type": NotRequired[RuleGroupTypeType],
        "AnalyzeRuleGroup": NotRequired[bool],
    },
)

class DescribeTLSInspectionConfigurationRequestRequestTypeDef(TypedDict):
    TLSInspectionConfigurationArn: NotRequired[str]
    TLSInspectionConfigurationName: NotRequired[str]

class DimensionTypeDef(TypedDict):
    Value: str

class DisassociateSubnetsRequestRequestTypeDef(TypedDict):
    SubnetIds: Sequence[str]
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]

class FirewallMetadataTypeDef(TypedDict):
    FirewallName: NotRequired[str]
    FirewallArn: NotRequired[str]

class FirewallPolicyMetadataTypeDef(TypedDict):
    Name: NotRequired[str]
    Arn: NotRequired[str]

class StatelessRuleGroupReferenceTypeDef(TypedDict):
    ResourceArn: str
    Priority: int

class FlowTimeoutsTypeDef(TypedDict):
    TcpIdleTimeoutSeconds: NotRequired[int]

HeaderTypeDef = TypedDict(
    "HeaderTypeDef",
    {
        "Protocol": StatefulRuleProtocolType,
        "Source": str,
        "SourcePort": str,
        "Direction": StatefulRuleDirectionType,
        "Destination": str,
        "DestinationPort": str,
    },
)

class IPSetOutputTypeDef(TypedDict):
    Definition: List[str]

class IPSetReferenceTypeDef(TypedDict):
    ReferenceArn: NotRequired[str]

class IPSetTypeDef(TypedDict):
    Definition: Sequence[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListFirewallPoliciesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListFirewallsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    VpcIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]

ListRuleGroupsRequestRequestTypeDef = TypedDict(
    "ListRuleGroupsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Scope": NotRequired[ResourceManagedStatusType],
        "ManagedType": NotRequired[ResourceManagedTypeType],
        "Type": NotRequired[RuleGroupTypeType],
    },
)

class RuleGroupMetadataTypeDef(TypedDict):
    Name: NotRequired[str]
    Arn: NotRequired[str]

class ListTLSInspectionConfigurationsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class TLSInspectionConfigurationMetadataTypeDef(TypedDict):
    Name: NotRequired[str]
    Arn: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class LogDestinationConfigOutputTypeDef(TypedDict):
    LogType: LogTypeType
    LogDestinationType: LogDestinationTypeType
    LogDestination: Dict[str, str]

class LogDestinationConfigTypeDef(TypedDict):
    LogType: LogTypeType
    LogDestinationType: LogDestinationTypeType
    LogDestination: Mapping[str, str]

class PortRangeTypeDef(TypedDict):
    FromPort: int
    ToPort: int

class TCPFlagFieldOutputTypeDef(TypedDict):
    Flags: List[TCPFlagType]
    Masks: NotRequired[List[TCPFlagType]]

class PerObjectStatusTypeDef(TypedDict):
    SyncStatus: NotRequired[PerObjectSyncStatusType]
    UpdateToken: NotRequired[str]

class PortSetOutputTypeDef(TypedDict):
    Definition: NotRequired[List[str]]

class PortSetTypeDef(TypedDict):
    Definition: NotRequired[Sequence[str]]

class PutResourcePolicyRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Policy: str

class RuleOptionOutputTypeDef(TypedDict):
    Keyword: str
    Settings: NotRequired[List[str]]

class RuleOptionTypeDef(TypedDict):
    Keyword: str
    Settings: NotRequired[Sequence[str]]

class RulesSourceListOutputTypeDef(TypedDict):
    Targets: List[str]
    TargetTypes: List[TargetTypeType]
    GeneratedRulesType: GeneratedRulesTypeType

class RulesSourceListTypeDef(TypedDict):
    Targets: Sequence[str]
    TargetTypes: Sequence[TargetTypeType]
    GeneratedRulesType: GeneratedRulesTypeType

class ServerCertificateTypeDef(TypedDict):
    ResourceArn: NotRequired[str]

class StatefulRuleGroupOverrideTypeDef(TypedDict):
    Action: NotRequired[Literal["DROP_TO_ALERT"]]

class TCPFlagFieldTypeDef(TypedDict):
    Flags: Sequence[TCPFlagType]
    Masks: NotRequired[Sequence[TCPFlagType]]

class TlsCertificateDataTypeDef(TypedDict):
    CertificateArn: NotRequired[str]
    CertificateSerial: NotRequired[str]
    Status: NotRequired[str]
    StatusMessage: NotRequired[str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateFirewallDeleteProtectionRequestRequestTypeDef(TypedDict):
    DeleteProtection: bool
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]

class UpdateFirewallDescriptionRequestRequestTypeDef(TypedDict):
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]
    Description: NotRequired[str]

class UpdateFirewallPolicyChangeProtectionRequestRequestTypeDef(TypedDict):
    FirewallPolicyChangeProtection: bool
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]

class UpdateSubnetChangeProtectionRequestRequestTypeDef(TypedDict):
    SubnetChangeProtection: bool
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]

class AssociateFirewallPolicyResponseTypeDef(TypedDict):
    FirewallArn: str
    FirewallName: str
    FirewallPolicyArn: str
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeResourcePolicyResponseTypeDef(TypedDict):
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateFirewallDeleteProtectionResponseTypeDef(TypedDict):
    FirewallArn: str
    FirewallName: str
    DeleteProtection: bool
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateFirewallDescriptionResponseTypeDef(TypedDict):
    FirewallArn: str
    FirewallName: str
    Description: str
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateFirewallPolicyChangeProtectionResponseTypeDef(TypedDict):
    UpdateToken: str
    FirewallArn: str
    FirewallName: str
    FirewallPolicyChangeProtection: bool
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSubnetChangeProtectionResponseTypeDef(TypedDict):
    UpdateToken: str
    FirewallArn: str
    FirewallName: str
    SubnetChangeProtection: bool
    ResponseMetadata: ResponseMetadataTypeDef

class AssociateSubnetsRequestRequestTypeDef(TypedDict):
    SubnetMappings: Sequence[SubnetMappingTypeDef]
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]

class AssociateSubnetsResponseTypeDef(TypedDict):
    FirewallArn: str
    FirewallName: str
    SubnetMappings: List[SubnetMappingTypeDef]
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociateSubnetsResponseTypeDef(TypedDict):
    FirewallArn: str
    FirewallName: str
    SubnetMappings: List[SubnetMappingTypeDef]
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class CIDRSummaryTypeDef(TypedDict):
    AvailableCIDRCount: NotRequired[int]
    UtilizedCIDRCount: NotRequired[int]
    IPSetReferences: NotRequired[Dict[str, IPSetMetadataTypeDef]]

class UpdateFirewallEncryptionConfigurationRequestRequestTypeDef(TypedDict):
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]

class UpdateFirewallEncryptionConfigurationResponseTypeDef(TypedDict):
    FirewallArn: str
    FirewallName: str
    UpdateToken: str
    EncryptionConfiguration: EncryptionConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFirewallRequestRequestTypeDef(TypedDict):
    FirewallName: str
    FirewallPolicyArn: str
    VpcId: str
    SubnetMappings: Sequence[SubnetMappingTypeDef]
    DeleteProtection: NotRequired[bool]
    SubnetChangeProtection: NotRequired[bool]
    FirewallPolicyChangeProtection: NotRequired[bool]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]

class FirewallPolicyResponseTypeDef(TypedDict):
    FirewallPolicyName: str
    FirewallPolicyArn: str
    FirewallPolicyId: str
    Description: NotRequired[str]
    FirewallPolicyStatus: NotRequired[ResourceStatusType]
    Tags: NotRequired[List[TagTypeDef]]
    ConsumedStatelessRuleCapacity: NotRequired[int]
    ConsumedStatefulRuleCapacity: NotRequired[int]
    NumberOfAssociations: NotRequired[int]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    LastModifiedTime: NotRequired[datetime]

class FirewallTypeDef(TypedDict):
    FirewallPolicyArn: str
    VpcId: str
    SubnetMappings: List[SubnetMappingTypeDef]
    FirewallId: str
    FirewallName: NotRequired[str]
    FirewallArn: NotRequired[str]
    DeleteProtection: NotRequired[bool]
    SubnetChangeProtection: NotRequired[bool]
    FirewallPolicyChangeProtection: NotRequired[bool]
    Description: NotRequired[str]
    Tags: NotRequired[List[TagTypeDef]]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]

RuleGroupResponseTypeDef = TypedDict(
    "RuleGroupResponseTypeDef",
    {
        "RuleGroupArn": str,
        "RuleGroupName": str,
        "RuleGroupId": str,
        "Description": NotRequired[str],
        "Type": NotRequired[RuleGroupTypeType],
        "Capacity": NotRequired[int],
        "RuleGroupStatus": NotRequired[ResourceStatusType],
        "Tags": NotRequired[List[TagTypeDef]],
        "ConsumedCapacity": NotRequired[int],
        "NumberOfAssociations": NotRequired[int],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
        "SourceMetadata": NotRequired[SourceMetadataTypeDef],
        "SnsTopic": NotRequired[str],
        "LastModifiedTime": NotRequired[datetime],
        "AnalysisResults": NotRequired[List[AnalysisResultTypeDef]],
    },
)
DescribeRuleGroupMetadataResponseTypeDef = TypedDict(
    "DescribeRuleGroupMetadataResponseTypeDef",
    {
        "RuleGroupArn": str,
        "RuleGroupName": str,
        "Description": str,
        "Type": RuleGroupTypeType,
        "Capacity": int,
        "StatefulRuleOptions": StatefulRuleOptionsTypeDef,
        "LastModifiedTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class PublishMetricActionOutputTypeDef(TypedDict):
    Dimensions: List[DimensionTypeDef]

class PublishMetricActionTypeDef(TypedDict):
    Dimensions: Sequence[DimensionTypeDef]

class ListFirewallsResponseTypeDef(TypedDict):
    Firewalls: List[FirewallMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListFirewallPoliciesResponseTypeDef(TypedDict):
    FirewallPolicies: List[FirewallPolicyMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class StatefulEngineOptionsTypeDef(TypedDict):
    RuleOrder: NotRequired[RuleOrderType]
    StreamExceptionPolicy: NotRequired[StreamExceptionPolicyType]
    FlowTimeouts: NotRequired[FlowTimeoutsTypeDef]

class PolicyVariablesOutputTypeDef(TypedDict):
    RuleVariables: NotRequired[Dict[str, IPSetOutputTypeDef]]

class ReferenceSetsOutputTypeDef(TypedDict):
    IPSetReferences: NotRequired[Dict[str, IPSetReferenceTypeDef]]

class ReferenceSetsTypeDef(TypedDict):
    IPSetReferences: NotRequired[Mapping[str, IPSetReferenceTypeDef]]

IPSetUnionTypeDef = Union[IPSetTypeDef, IPSetOutputTypeDef]

class ListFirewallPoliciesRequestListFirewallPoliciesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFirewallsRequestListFirewallsPaginateTypeDef(TypedDict):
    VpcIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListRuleGroupsRequestListRuleGroupsPaginateTypeDef = TypedDict(
    "ListRuleGroupsRequestListRuleGroupsPaginateTypeDef",
    {
        "Scope": NotRequired[ResourceManagedStatusType],
        "ManagedType": NotRequired[ResourceManagedTypeType],
        "Type": NotRequired[RuleGroupTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListTLSInspectionConfigurationsRequestListTLSInspectionConfigurationsPaginateTypeDef(
    TypedDict
):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(TypedDict):
    ResourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRuleGroupsResponseTypeDef(TypedDict):
    RuleGroups: List[RuleGroupMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTLSInspectionConfigurationsResponseTypeDef(TypedDict):
    TLSInspectionConfigurations: List[TLSInspectionConfigurationMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class LoggingConfigurationOutputTypeDef(TypedDict):
    LogDestinationConfigs: List[LogDestinationConfigOutputTypeDef]

LogDestinationConfigUnionTypeDef = Union[
    LogDestinationConfigTypeDef, LogDestinationConfigOutputTypeDef
]

class ServerCertificateScopeOutputTypeDef(TypedDict):
    Sources: NotRequired[List[AddressTypeDef]]
    Destinations: NotRequired[List[AddressTypeDef]]
    SourcePorts: NotRequired[List[PortRangeTypeDef]]
    DestinationPorts: NotRequired[List[PortRangeTypeDef]]
    Protocols: NotRequired[List[int]]

class ServerCertificateScopeTypeDef(TypedDict):
    Sources: NotRequired[Sequence[AddressTypeDef]]
    Destinations: NotRequired[Sequence[AddressTypeDef]]
    SourcePorts: NotRequired[Sequence[PortRangeTypeDef]]
    DestinationPorts: NotRequired[Sequence[PortRangeTypeDef]]
    Protocols: NotRequired[Sequence[int]]

class MatchAttributesOutputTypeDef(TypedDict):
    Sources: NotRequired[List[AddressTypeDef]]
    Destinations: NotRequired[List[AddressTypeDef]]
    SourcePorts: NotRequired[List[PortRangeTypeDef]]
    DestinationPorts: NotRequired[List[PortRangeTypeDef]]
    Protocols: NotRequired[List[int]]
    TCPFlags: NotRequired[List[TCPFlagFieldOutputTypeDef]]

class SyncStateTypeDef(TypedDict):
    Attachment: NotRequired[AttachmentTypeDef]
    Config: NotRequired[Dict[str, PerObjectStatusTypeDef]]

class RuleVariablesOutputTypeDef(TypedDict):
    IPSets: NotRequired[Dict[str, IPSetOutputTypeDef]]
    PortSets: NotRequired[Dict[str, PortSetOutputTypeDef]]

PortSetUnionTypeDef = Union[PortSetTypeDef, PortSetOutputTypeDef]

class StatefulRuleOutputTypeDef(TypedDict):
    Action: StatefulActionType
    Header: HeaderTypeDef
    RuleOptions: List[RuleOptionOutputTypeDef]

RuleOptionUnionTypeDef = Union[RuleOptionTypeDef, RuleOptionOutputTypeDef]
RulesSourceListUnionTypeDef = Union[RulesSourceListTypeDef, RulesSourceListOutputTypeDef]

class StatefulRuleGroupReferenceTypeDef(TypedDict):
    ResourceArn: str
    Priority: NotRequired[int]
    Override: NotRequired[StatefulRuleGroupOverrideTypeDef]

TCPFlagFieldUnionTypeDef = Union[TCPFlagFieldTypeDef, TCPFlagFieldOutputTypeDef]

class TLSInspectionConfigurationResponseTypeDef(TypedDict):
    TLSInspectionConfigurationArn: str
    TLSInspectionConfigurationName: str
    TLSInspectionConfigurationId: str
    TLSInspectionConfigurationStatus: NotRequired[ResourceStatusType]
    Description: NotRequired[str]
    Tags: NotRequired[List[TagTypeDef]]
    LastModifiedTime: NotRequired[datetime]
    NumberOfAssociations: NotRequired[int]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    Certificates: NotRequired[List[TlsCertificateDataTypeDef]]
    CertificateAuthority: NotRequired[TlsCertificateDataTypeDef]

class CapacityUsageSummaryTypeDef(TypedDict):
    CIDRs: NotRequired[CIDRSummaryTypeDef]

class CreateFirewallPolicyResponseTypeDef(TypedDict):
    UpdateToken: str
    FirewallPolicyResponse: FirewallPolicyResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteFirewallPolicyResponseTypeDef(TypedDict):
    FirewallPolicyResponse: FirewallPolicyResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateFirewallPolicyResponseTypeDef(TypedDict):
    UpdateToken: str
    FirewallPolicyResponse: FirewallPolicyResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRuleGroupResponseTypeDef(TypedDict):
    UpdateToken: str
    RuleGroupResponse: RuleGroupResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteRuleGroupResponseTypeDef(TypedDict):
    RuleGroupResponse: RuleGroupResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRuleGroupResponseTypeDef(TypedDict):
    UpdateToken: str
    RuleGroupResponse: RuleGroupResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ActionDefinitionOutputTypeDef(TypedDict):
    PublishMetricAction: NotRequired[PublishMetricActionOutputTypeDef]

PublishMetricActionUnionTypeDef = Union[
    PublishMetricActionTypeDef, PublishMetricActionOutputTypeDef
]
ReferenceSetsUnionTypeDef = Union[ReferenceSetsTypeDef, ReferenceSetsOutputTypeDef]

class PolicyVariablesTypeDef(TypedDict):
    RuleVariables: NotRequired[Mapping[str, IPSetUnionTypeDef]]

class DescribeLoggingConfigurationResponseTypeDef(TypedDict):
    FirewallArn: str
    LoggingConfiguration: LoggingConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateLoggingConfigurationResponseTypeDef(TypedDict):
    FirewallArn: str
    FirewallName: str
    LoggingConfiguration: LoggingConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class LoggingConfigurationTypeDef(TypedDict):
    LogDestinationConfigs: Sequence[LogDestinationConfigUnionTypeDef]

class ServerCertificateConfigurationOutputTypeDef(TypedDict):
    ServerCertificates: NotRequired[List[ServerCertificateTypeDef]]
    Scopes: NotRequired[List[ServerCertificateScopeOutputTypeDef]]
    CertificateAuthorityArn: NotRequired[str]
    CheckCertificateRevocationStatus: NotRequired[CheckCertificateRevocationStatusActionsTypeDef]

ServerCertificateScopeUnionTypeDef = Union[
    ServerCertificateScopeTypeDef, ServerCertificateScopeOutputTypeDef
]

class RuleDefinitionOutputTypeDef(TypedDict):
    MatchAttributes: MatchAttributesOutputTypeDef
    Actions: List[str]

class RuleVariablesTypeDef(TypedDict):
    IPSets: NotRequired[Mapping[str, IPSetUnionTypeDef]]
    PortSets: NotRequired[Mapping[str, PortSetUnionTypeDef]]

class StatefulRuleTypeDef(TypedDict):
    Action: StatefulActionType
    Header: HeaderTypeDef
    RuleOptions: Sequence[RuleOptionUnionTypeDef]

class MatchAttributesTypeDef(TypedDict):
    Sources: NotRequired[Sequence[AddressTypeDef]]
    Destinations: NotRequired[Sequence[AddressTypeDef]]
    SourcePorts: NotRequired[Sequence[PortRangeTypeDef]]
    DestinationPorts: NotRequired[Sequence[PortRangeTypeDef]]
    Protocols: NotRequired[Sequence[int]]
    TCPFlags: NotRequired[Sequence[TCPFlagFieldUnionTypeDef]]

class CreateTLSInspectionConfigurationResponseTypeDef(TypedDict):
    UpdateToken: str
    TLSInspectionConfigurationResponse: TLSInspectionConfigurationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteTLSInspectionConfigurationResponseTypeDef(TypedDict):
    TLSInspectionConfigurationResponse: TLSInspectionConfigurationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTLSInspectionConfigurationResponseTypeDef(TypedDict):
    UpdateToken: str
    TLSInspectionConfigurationResponse: TLSInspectionConfigurationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class FirewallStatusTypeDef(TypedDict):
    Status: FirewallStatusValueType
    ConfigurationSyncStateSummary: ConfigurationSyncStateType
    SyncStates: NotRequired[Dict[str, SyncStateTypeDef]]
    CapacityUsageSummary: NotRequired[CapacityUsageSummaryTypeDef]

class CustomActionOutputTypeDef(TypedDict):
    ActionName: str
    ActionDefinition: ActionDefinitionOutputTypeDef

class ActionDefinitionTypeDef(TypedDict):
    PublishMetricAction: NotRequired[PublishMetricActionUnionTypeDef]

PolicyVariablesUnionTypeDef = Union[PolicyVariablesTypeDef, PolicyVariablesOutputTypeDef]

class UpdateLoggingConfigurationRequestRequestTypeDef(TypedDict):
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]
    LoggingConfiguration: NotRequired[LoggingConfigurationTypeDef]

class TLSInspectionConfigurationOutputTypeDef(TypedDict):
    ServerCertificateConfigurations: NotRequired[List[ServerCertificateConfigurationOutputTypeDef]]

class ServerCertificateConfigurationTypeDef(TypedDict):
    ServerCertificates: NotRequired[Sequence[ServerCertificateTypeDef]]
    Scopes: NotRequired[Sequence[ServerCertificateScopeUnionTypeDef]]
    CertificateAuthorityArn: NotRequired[str]
    CheckCertificateRevocationStatus: NotRequired[CheckCertificateRevocationStatusActionsTypeDef]

class StatelessRuleOutputTypeDef(TypedDict):
    RuleDefinition: RuleDefinitionOutputTypeDef
    Priority: int

RuleVariablesUnionTypeDef = Union[RuleVariablesTypeDef, RuleVariablesOutputTypeDef]
StatefulRuleUnionTypeDef = Union[StatefulRuleTypeDef, StatefulRuleOutputTypeDef]
MatchAttributesUnionTypeDef = Union[MatchAttributesTypeDef, MatchAttributesOutputTypeDef]

class CreateFirewallResponseTypeDef(TypedDict):
    Firewall: FirewallTypeDef
    FirewallStatus: FirewallStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteFirewallResponseTypeDef(TypedDict):
    Firewall: FirewallTypeDef
    FirewallStatus: FirewallStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeFirewallResponseTypeDef(TypedDict):
    UpdateToken: str
    Firewall: FirewallTypeDef
    FirewallStatus: FirewallStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class FirewallPolicyOutputTypeDef(TypedDict):
    StatelessDefaultActions: List[str]
    StatelessFragmentDefaultActions: List[str]
    StatelessRuleGroupReferences: NotRequired[List[StatelessRuleGroupReferenceTypeDef]]
    StatelessCustomActions: NotRequired[List[CustomActionOutputTypeDef]]
    StatefulRuleGroupReferences: NotRequired[List[StatefulRuleGroupReferenceTypeDef]]
    StatefulDefaultActions: NotRequired[List[str]]
    StatefulEngineOptions: NotRequired[StatefulEngineOptionsTypeDef]
    TLSInspectionConfigurationArn: NotRequired[str]
    PolicyVariables: NotRequired[PolicyVariablesOutputTypeDef]

ActionDefinitionUnionTypeDef = Union[ActionDefinitionTypeDef, ActionDefinitionOutputTypeDef]

class DescribeTLSInspectionConfigurationResponseTypeDef(TypedDict):
    UpdateToken: str
    TLSInspectionConfiguration: TLSInspectionConfigurationOutputTypeDef
    TLSInspectionConfigurationResponse: TLSInspectionConfigurationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ServerCertificateConfigurationUnionTypeDef = Union[
    ServerCertificateConfigurationTypeDef, ServerCertificateConfigurationOutputTypeDef
]

class StatelessRulesAndCustomActionsOutputTypeDef(TypedDict):
    StatelessRules: List[StatelessRuleOutputTypeDef]
    CustomActions: NotRequired[List[CustomActionOutputTypeDef]]

class RuleDefinitionTypeDef(TypedDict):
    MatchAttributes: MatchAttributesUnionTypeDef
    Actions: Sequence[str]

class DescribeFirewallPolicyResponseTypeDef(TypedDict):
    UpdateToken: str
    FirewallPolicyResponse: FirewallPolicyResponseTypeDef
    FirewallPolicy: FirewallPolicyOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CustomActionTypeDef(TypedDict):
    ActionName: str
    ActionDefinition: ActionDefinitionUnionTypeDef

class TLSInspectionConfigurationTypeDef(TypedDict):
    ServerCertificateConfigurations: NotRequired[
        Sequence[ServerCertificateConfigurationUnionTypeDef]
    ]

class RulesSourceOutputTypeDef(TypedDict):
    RulesString: NotRequired[str]
    RulesSourceList: NotRequired[RulesSourceListOutputTypeDef]
    StatefulRules: NotRequired[List[StatefulRuleOutputTypeDef]]
    StatelessRulesAndCustomActions: NotRequired[StatelessRulesAndCustomActionsOutputTypeDef]

RuleDefinitionUnionTypeDef = Union[RuleDefinitionTypeDef, RuleDefinitionOutputTypeDef]
CustomActionUnionTypeDef = Union[CustomActionTypeDef, CustomActionOutputTypeDef]

class CreateTLSInspectionConfigurationRequestRequestTypeDef(TypedDict):
    TLSInspectionConfigurationName: str
    TLSInspectionConfiguration: TLSInspectionConfigurationTypeDef
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]

class UpdateTLSInspectionConfigurationRequestRequestTypeDef(TypedDict):
    TLSInspectionConfiguration: TLSInspectionConfigurationTypeDef
    UpdateToken: str
    TLSInspectionConfigurationArn: NotRequired[str]
    TLSInspectionConfigurationName: NotRequired[str]
    Description: NotRequired[str]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]

class RuleGroupOutputTypeDef(TypedDict):
    RulesSource: RulesSourceOutputTypeDef
    RuleVariables: NotRequired[RuleVariablesOutputTypeDef]
    ReferenceSets: NotRequired[ReferenceSetsOutputTypeDef]
    StatefulRuleOptions: NotRequired[StatefulRuleOptionsTypeDef]

class StatelessRuleTypeDef(TypedDict):
    RuleDefinition: RuleDefinitionUnionTypeDef
    Priority: int

class FirewallPolicyTypeDef(TypedDict):
    StatelessDefaultActions: Sequence[str]
    StatelessFragmentDefaultActions: Sequence[str]
    StatelessRuleGroupReferences: NotRequired[Sequence[StatelessRuleGroupReferenceTypeDef]]
    StatelessCustomActions: NotRequired[Sequence[CustomActionUnionTypeDef]]
    StatefulRuleGroupReferences: NotRequired[Sequence[StatefulRuleGroupReferenceTypeDef]]
    StatefulDefaultActions: NotRequired[Sequence[str]]
    StatefulEngineOptions: NotRequired[StatefulEngineOptionsTypeDef]
    TLSInspectionConfigurationArn: NotRequired[str]
    PolicyVariables: NotRequired[PolicyVariablesUnionTypeDef]

class DescribeRuleGroupResponseTypeDef(TypedDict):
    UpdateToken: str
    RuleGroup: RuleGroupOutputTypeDef
    RuleGroupResponse: RuleGroupResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

StatelessRuleUnionTypeDef = Union[StatelessRuleTypeDef, StatelessRuleOutputTypeDef]

class CreateFirewallPolicyRequestRequestTypeDef(TypedDict):
    FirewallPolicyName: str
    FirewallPolicy: FirewallPolicyTypeDef
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    DryRun: NotRequired[bool]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]

class UpdateFirewallPolicyRequestRequestTypeDef(TypedDict):
    UpdateToken: str
    FirewallPolicy: FirewallPolicyTypeDef
    FirewallPolicyArn: NotRequired[str]
    FirewallPolicyName: NotRequired[str]
    Description: NotRequired[str]
    DryRun: NotRequired[bool]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]

class StatelessRulesAndCustomActionsTypeDef(TypedDict):
    StatelessRules: Sequence[StatelessRuleUnionTypeDef]
    CustomActions: NotRequired[Sequence[CustomActionUnionTypeDef]]

StatelessRulesAndCustomActionsUnionTypeDef = Union[
    StatelessRulesAndCustomActionsTypeDef, StatelessRulesAndCustomActionsOutputTypeDef
]

class RulesSourceTypeDef(TypedDict):
    RulesString: NotRequired[str]
    RulesSourceList: NotRequired[RulesSourceListUnionTypeDef]
    StatefulRules: NotRequired[Sequence[StatefulRuleUnionTypeDef]]
    StatelessRulesAndCustomActions: NotRequired[StatelessRulesAndCustomActionsUnionTypeDef]

RulesSourceUnionTypeDef = Union[RulesSourceTypeDef, RulesSourceOutputTypeDef]

class RuleGroupTypeDef(TypedDict):
    RulesSource: RulesSourceUnionTypeDef
    RuleVariables: NotRequired[RuleVariablesUnionTypeDef]
    ReferenceSets: NotRequired[ReferenceSetsUnionTypeDef]
    StatefulRuleOptions: NotRequired[StatefulRuleOptionsTypeDef]

CreateRuleGroupRequestRequestTypeDef = TypedDict(
    "CreateRuleGroupRequestRequestTypeDef",
    {
        "RuleGroupName": str,
        "Type": RuleGroupTypeType,
        "Capacity": int,
        "RuleGroup": NotRequired[RuleGroupTypeDef],
        "Rules": NotRequired[str],
        "Description": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "DryRun": NotRequired[bool],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
        "SourceMetadata": NotRequired[SourceMetadataTypeDef],
        "AnalyzeRuleGroup": NotRequired[bool],
    },
)
UpdateRuleGroupRequestRequestTypeDef = TypedDict(
    "UpdateRuleGroupRequestRequestTypeDef",
    {
        "UpdateToken": str,
        "RuleGroupArn": NotRequired[str],
        "RuleGroupName": NotRequired[str],
        "RuleGroup": NotRequired[RuleGroupTypeDef],
        "Rules": NotRequired[str],
        "Type": NotRequired[RuleGroupTypeType],
        "Description": NotRequired[str],
        "DryRun": NotRequired[bool],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
        "SourceMetadata": NotRequired[SourceMetadataTypeDef],
        "AnalyzeRuleGroup": NotRequired[bool],
    },
)
