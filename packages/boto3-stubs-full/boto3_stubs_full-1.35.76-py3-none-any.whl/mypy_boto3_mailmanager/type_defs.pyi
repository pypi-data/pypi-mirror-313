"""
Type annotations for mailmanager service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/type_defs/)

Usage::

    ```python
    from mypy_boto3_mailmanager.type_defs import AddHeaderActionTypeDef

    data: AddHeaderActionTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AcceptActionType,
    ActionFailurePolicyType,
    ArchiveBooleanOperatorType,
    ArchiveStateType,
    ArchiveStringEmailAttributeType,
    ExportStateType,
    IngressBooleanOperatorType,
    IngressIpOperatorType,
    IngressPointStatusToUpdateType,
    IngressPointStatusType,
    IngressPointTypeType,
    IngressStringOperatorType,
    IngressTlsProtocolAttributeType,
    IngressTlsProtocolOperatorType,
    MailFromType,
    RetentionPeriodType,
    RuleBooleanEmailAttributeType,
    RuleBooleanOperatorType,
    RuleDmarcOperatorType,
    RuleDmarcPolicyType,
    RuleIpOperatorType,
    RuleNumberOperatorType,
    RuleStringEmailAttributeType,
    RuleStringOperatorType,
    RuleVerdictAttributeType,
    RuleVerdictOperatorType,
    RuleVerdictType,
    SearchStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AddHeaderActionTypeDef",
    "AddonInstanceTypeDef",
    "AddonSubscriptionTypeDef",
    "AnalysisTypeDef",
    "ArchiveActionTypeDef",
    "ArchiveBooleanExpressionTypeDef",
    "ArchiveBooleanToEvaluateTypeDef",
    "ArchiveFilterConditionOutputTypeDef",
    "ArchiveFilterConditionTypeDef",
    "ArchiveFilterConditionUnionTypeDef",
    "ArchiveFiltersOutputTypeDef",
    "ArchiveFiltersTypeDef",
    "ArchiveRetentionTypeDef",
    "ArchiveStringExpressionOutputTypeDef",
    "ArchiveStringExpressionTypeDef",
    "ArchiveStringExpressionUnionTypeDef",
    "ArchiveStringToEvaluateTypeDef",
    "ArchiveTypeDef",
    "CreateAddonInstanceRequestRequestTypeDef",
    "CreateAddonInstanceResponseTypeDef",
    "CreateAddonSubscriptionRequestRequestTypeDef",
    "CreateAddonSubscriptionResponseTypeDef",
    "CreateArchiveRequestRequestTypeDef",
    "CreateArchiveResponseTypeDef",
    "CreateIngressPointRequestRequestTypeDef",
    "CreateIngressPointResponseTypeDef",
    "CreateRelayRequestRequestTypeDef",
    "CreateRelayResponseTypeDef",
    "CreateRuleSetRequestRequestTypeDef",
    "CreateRuleSetResponseTypeDef",
    "CreateTrafficPolicyRequestRequestTypeDef",
    "CreateTrafficPolicyResponseTypeDef",
    "DeleteAddonInstanceRequestRequestTypeDef",
    "DeleteAddonSubscriptionRequestRequestTypeDef",
    "DeleteArchiveRequestRequestTypeDef",
    "DeleteIngressPointRequestRequestTypeDef",
    "DeleteRelayRequestRequestTypeDef",
    "DeleteRuleSetRequestRequestTypeDef",
    "DeleteTrafficPolicyRequestRequestTypeDef",
    "DeliverToMailboxActionTypeDef",
    "DeliverToQBusinessActionTypeDef",
    "EnvelopeTypeDef",
    "ExportDestinationConfigurationTypeDef",
    "ExportStatusTypeDef",
    "ExportSummaryTypeDef",
    "GetAddonInstanceRequestRequestTypeDef",
    "GetAddonInstanceResponseTypeDef",
    "GetAddonSubscriptionRequestRequestTypeDef",
    "GetAddonSubscriptionResponseTypeDef",
    "GetArchiveExportRequestRequestTypeDef",
    "GetArchiveExportResponseTypeDef",
    "GetArchiveMessageContentRequestRequestTypeDef",
    "GetArchiveMessageContentResponseTypeDef",
    "GetArchiveMessageRequestRequestTypeDef",
    "GetArchiveMessageResponseTypeDef",
    "GetArchiveRequestRequestTypeDef",
    "GetArchiveResponseTypeDef",
    "GetArchiveSearchRequestRequestTypeDef",
    "GetArchiveSearchResponseTypeDef",
    "GetArchiveSearchResultsRequestRequestTypeDef",
    "GetArchiveSearchResultsResponseTypeDef",
    "GetIngressPointRequestRequestTypeDef",
    "GetIngressPointResponseTypeDef",
    "GetRelayRequestRequestTypeDef",
    "GetRelayResponseTypeDef",
    "GetRuleSetRequestRequestTypeDef",
    "GetRuleSetResponseTypeDef",
    "GetTrafficPolicyRequestRequestTypeDef",
    "GetTrafficPolicyResponseTypeDef",
    "IngressAnalysisTypeDef",
    "IngressBooleanExpressionTypeDef",
    "IngressBooleanToEvaluateTypeDef",
    "IngressIpToEvaluateTypeDef",
    "IngressIpv4ExpressionOutputTypeDef",
    "IngressIpv4ExpressionTypeDef",
    "IngressIpv4ExpressionUnionTypeDef",
    "IngressPointAuthConfigurationTypeDef",
    "IngressPointConfigurationTypeDef",
    "IngressPointPasswordConfigurationTypeDef",
    "IngressPointTypeDef",
    "IngressStringExpressionOutputTypeDef",
    "IngressStringExpressionTypeDef",
    "IngressStringExpressionUnionTypeDef",
    "IngressStringToEvaluateTypeDef",
    "IngressTlsProtocolExpressionTypeDef",
    "IngressTlsProtocolToEvaluateTypeDef",
    "ListAddonInstancesRequestListAddonInstancesPaginateTypeDef",
    "ListAddonInstancesRequestRequestTypeDef",
    "ListAddonInstancesResponseTypeDef",
    "ListAddonSubscriptionsRequestListAddonSubscriptionsPaginateTypeDef",
    "ListAddonSubscriptionsRequestRequestTypeDef",
    "ListAddonSubscriptionsResponseTypeDef",
    "ListArchiveExportsRequestListArchiveExportsPaginateTypeDef",
    "ListArchiveExportsRequestRequestTypeDef",
    "ListArchiveExportsResponseTypeDef",
    "ListArchiveSearchesRequestListArchiveSearchesPaginateTypeDef",
    "ListArchiveSearchesRequestRequestTypeDef",
    "ListArchiveSearchesResponseTypeDef",
    "ListArchivesRequestListArchivesPaginateTypeDef",
    "ListArchivesRequestRequestTypeDef",
    "ListArchivesResponseTypeDef",
    "ListIngressPointsRequestListIngressPointsPaginateTypeDef",
    "ListIngressPointsRequestRequestTypeDef",
    "ListIngressPointsResponseTypeDef",
    "ListRelaysRequestListRelaysPaginateTypeDef",
    "ListRelaysRequestRequestTypeDef",
    "ListRelaysResponseTypeDef",
    "ListRuleSetsRequestListRuleSetsPaginateTypeDef",
    "ListRuleSetsRequestRequestTypeDef",
    "ListRuleSetsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTrafficPoliciesRequestListTrafficPoliciesPaginateTypeDef",
    "ListTrafficPoliciesRequestRequestTypeDef",
    "ListTrafficPoliciesResponseTypeDef",
    "MessageBodyTypeDef",
    "MetadataTypeDef",
    "PaginatorConfigTypeDef",
    "PolicyConditionOutputTypeDef",
    "PolicyConditionTypeDef",
    "PolicyConditionUnionTypeDef",
    "PolicyStatementOutputTypeDef",
    "PolicyStatementTypeDef",
    "PolicyStatementUnionTypeDef",
    "RelayActionTypeDef",
    "RelayAuthenticationOutputTypeDef",
    "RelayAuthenticationTypeDef",
    "RelayTypeDef",
    "ReplaceRecipientActionOutputTypeDef",
    "ReplaceRecipientActionTypeDef",
    "ReplaceRecipientActionUnionTypeDef",
    "ResponseMetadataTypeDef",
    "RowTypeDef",
    "RuleActionOutputTypeDef",
    "RuleActionTypeDef",
    "RuleActionUnionTypeDef",
    "RuleBooleanExpressionTypeDef",
    "RuleBooleanToEvaluateTypeDef",
    "RuleConditionOutputTypeDef",
    "RuleConditionTypeDef",
    "RuleConditionUnionTypeDef",
    "RuleDmarcExpressionOutputTypeDef",
    "RuleDmarcExpressionTypeDef",
    "RuleDmarcExpressionUnionTypeDef",
    "RuleIpExpressionOutputTypeDef",
    "RuleIpExpressionTypeDef",
    "RuleIpExpressionUnionTypeDef",
    "RuleIpToEvaluateTypeDef",
    "RuleNumberExpressionTypeDef",
    "RuleNumberToEvaluateTypeDef",
    "RuleOutputTypeDef",
    "RuleSetTypeDef",
    "RuleStringExpressionOutputTypeDef",
    "RuleStringExpressionTypeDef",
    "RuleStringExpressionUnionTypeDef",
    "RuleStringToEvaluateTypeDef",
    "RuleTypeDef",
    "RuleUnionTypeDef",
    "RuleVerdictExpressionOutputTypeDef",
    "RuleVerdictExpressionTypeDef",
    "RuleVerdictExpressionUnionTypeDef",
    "RuleVerdictToEvaluateTypeDef",
    "S3ActionTypeDef",
    "S3ExportDestinationConfigurationTypeDef",
    "SearchStatusTypeDef",
    "SearchSummaryTypeDef",
    "SendActionTypeDef",
    "StartArchiveExportRequestRequestTypeDef",
    "StartArchiveExportResponseTypeDef",
    "StartArchiveSearchRequestRequestTypeDef",
    "StartArchiveSearchResponseTypeDef",
    "StopArchiveExportRequestRequestTypeDef",
    "StopArchiveSearchRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TimestampTypeDef",
    "TrafficPolicyTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateArchiveRequestRequestTypeDef",
    "UpdateIngressPointRequestRequestTypeDef",
    "UpdateRelayRequestRequestTypeDef",
    "UpdateRuleSetRequestRequestTypeDef",
    "UpdateTrafficPolicyRequestRequestTypeDef",
)

class AddHeaderActionTypeDef(TypedDict):
    HeaderName: str
    HeaderValue: str

class AddonInstanceTypeDef(TypedDict):
    AddonInstanceArn: NotRequired[str]
    AddonInstanceId: NotRequired[str]
    AddonName: NotRequired[str]
    AddonSubscriptionId: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]

class AddonSubscriptionTypeDef(TypedDict):
    AddonName: NotRequired[str]
    AddonSubscriptionArn: NotRequired[str]
    AddonSubscriptionId: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]

class AnalysisTypeDef(TypedDict):
    Analyzer: str
    ResultField: str

class ArchiveActionTypeDef(TypedDict):
    TargetArchive: str
    ActionFailurePolicy: NotRequired[ActionFailurePolicyType]

class ArchiveBooleanToEvaluateTypeDef(TypedDict):
    Attribute: NotRequired[Literal["HAS_ATTACHMENTS"]]

class ArchiveRetentionTypeDef(TypedDict):
    RetentionPeriod: NotRequired[RetentionPeriodType]

class ArchiveStringToEvaluateTypeDef(TypedDict):
    Attribute: NotRequired[ArchiveStringEmailAttributeType]

class ArchiveTypeDef(TypedDict):
    ArchiveId: str
    ArchiveName: NotRequired[str]
    ArchiveState: NotRequired[ArchiveStateType]
    LastUpdatedTimestamp: NotRequired[datetime]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class IngressPointConfigurationTypeDef(TypedDict):
    SecretArn: NotRequired[str]
    SmtpPassword: NotRequired[str]

class RelayAuthenticationTypeDef(TypedDict):
    NoAuthentication: NotRequired[Mapping[str, Any]]
    SecretArn: NotRequired[str]

class DeleteAddonInstanceRequestRequestTypeDef(TypedDict):
    AddonInstanceId: str

class DeleteAddonSubscriptionRequestRequestTypeDef(TypedDict):
    AddonSubscriptionId: str

class DeleteArchiveRequestRequestTypeDef(TypedDict):
    ArchiveId: str

class DeleteIngressPointRequestRequestTypeDef(TypedDict):
    IngressPointId: str

class DeleteRelayRequestRequestTypeDef(TypedDict):
    RelayId: str

class DeleteRuleSetRequestRequestTypeDef(TypedDict):
    RuleSetId: str

class DeleteTrafficPolicyRequestRequestTypeDef(TypedDict):
    TrafficPolicyId: str

class DeliverToMailboxActionTypeDef(TypedDict):
    MailboxArn: str
    RoleArn: str
    ActionFailurePolicy: NotRequired[ActionFailurePolicyType]

class DeliverToQBusinessActionTypeDef(TypedDict):
    ApplicationId: str
    IndexId: str
    RoleArn: str
    ActionFailurePolicy: NotRequired[ActionFailurePolicyType]

class EnvelopeTypeDef(TypedDict):
    From: NotRequired[str]
    Helo: NotRequired[str]
    To: NotRequired[List[str]]

class S3ExportDestinationConfigurationTypeDef(TypedDict):
    S3Location: NotRequired[str]

class ExportStatusTypeDef(TypedDict):
    CompletionTimestamp: NotRequired[datetime]
    ErrorMessage: NotRequired[str]
    State: NotRequired[ExportStateType]
    SubmissionTimestamp: NotRequired[datetime]

class GetAddonInstanceRequestRequestTypeDef(TypedDict):
    AddonInstanceId: str

class GetAddonSubscriptionRequestRequestTypeDef(TypedDict):
    AddonSubscriptionId: str

class GetArchiveExportRequestRequestTypeDef(TypedDict):
    ExportId: str

class GetArchiveMessageContentRequestRequestTypeDef(TypedDict):
    ArchivedMessageId: str

MessageBodyTypeDef = TypedDict(
    "MessageBodyTypeDef",
    {
        "Html": NotRequired[str],
        "MessageMalformed": NotRequired[bool],
        "Text": NotRequired[str],
    },
)

class GetArchiveMessageRequestRequestTypeDef(TypedDict):
    ArchivedMessageId: str

class MetadataTypeDef(TypedDict):
    IngressPointId: NotRequired[str]
    RuleSetId: NotRequired[str]
    SenderHostname: NotRequired[str]
    SenderIpAddress: NotRequired[str]
    Timestamp: NotRequired[datetime]
    TlsCipherSuite: NotRequired[str]
    TlsProtocol: NotRequired[str]
    TrafficPolicyId: NotRequired[str]

class GetArchiveRequestRequestTypeDef(TypedDict):
    ArchiveId: str

class GetArchiveSearchRequestRequestTypeDef(TypedDict):
    SearchId: str

class SearchStatusTypeDef(TypedDict):
    CompletionTimestamp: NotRequired[datetime]
    ErrorMessage: NotRequired[str]
    State: NotRequired[SearchStateType]
    SubmissionTimestamp: NotRequired[datetime]

class GetArchiveSearchResultsRequestRequestTypeDef(TypedDict):
    SearchId: str

class GetIngressPointRequestRequestTypeDef(TypedDict):
    IngressPointId: str

class GetRelayRequestRequestTypeDef(TypedDict):
    RelayId: str

class RelayAuthenticationOutputTypeDef(TypedDict):
    NoAuthentication: NotRequired[Dict[str, Any]]
    SecretArn: NotRequired[str]

class GetRuleSetRequestRequestTypeDef(TypedDict):
    RuleSetId: str

class GetTrafficPolicyRequestRequestTypeDef(TypedDict):
    TrafficPolicyId: str

class IngressAnalysisTypeDef(TypedDict):
    Analyzer: str
    ResultField: str

class IngressIpToEvaluateTypeDef(TypedDict):
    Attribute: NotRequired[Literal["SENDER_IP"]]

class IngressPointPasswordConfigurationTypeDef(TypedDict):
    PreviousSmtpPasswordExpiryTimestamp: NotRequired[datetime]
    PreviousSmtpPasswordVersion: NotRequired[str]
    SmtpPasswordVersion: NotRequired[str]

IngressPointTypeDef = TypedDict(
    "IngressPointTypeDef",
    {
        "IngressPointId": str,
        "IngressPointName": str,
        "Status": IngressPointStatusType,
        "Type": IngressPointTypeType,
        "ARecord": NotRequired[str],
    },
)

class IngressStringToEvaluateTypeDef(TypedDict):
    Attribute: NotRequired[Literal["RECIPIENT"]]

class IngressTlsProtocolToEvaluateTypeDef(TypedDict):
    Attribute: NotRequired[Literal["TLS_PROTOCOL"]]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAddonInstancesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]

class ListAddonSubscriptionsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]

class ListArchiveExportsRequestRequestTypeDef(TypedDict):
    ArchiveId: str
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]

class ListArchiveSearchesRequestRequestTypeDef(TypedDict):
    ArchiveId: str
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]

class ListArchivesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]

class ListIngressPointsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]

class ListRelaysRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]

class RelayTypeDef(TypedDict):
    LastModifiedTimestamp: NotRequired[datetime]
    RelayId: NotRequired[str]
    RelayName: NotRequired[str]

class ListRuleSetsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]

class RuleSetTypeDef(TypedDict):
    LastModificationDate: NotRequired[datetime]
    RuleSetId: NotRequired[str]
    RuleSetName: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class ListTrafficPoliciesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]

class TrafficPolicyTypeDef(TypedDict):
    DefaultAction: AcceptActionType
    TrafficPolicyId: str
    TrafficPolicyName: str

class RelayActionTypeDef(TypedDict):
    Relay: str
    ActionFailurePolicy: NotRequired[ActionFailurePolicyType]
    MailFrom: NotRequired[MailFromType]

class ReplaceRecipientActionOutputTypeDef(TypedDict):
    ReplaceWith: NotRequired[List[str]]

class ReplaceRecipientActionTypeDef(TypedDict):
    ReplaceWith: NotRequired[Sequence[str]]

class S3ActionTypeDef(TypedDict):
    RoleArn: str
    S3Bucket: str
    ActionFailurePolicy: NotRequired[ActionFailurePolicyType]
    S3Prefix: NotRequired[str]
    S3SseKmsKeyId: NotRequired[str]

class SendActionTypeDef(TypedDict):
    RoleArn: str
    ActionFailurePolicy: NotRequired[ActionFailurePolicyType]

class RuleBooleanToEvaluateTypeDef(TypedDict):
    Attribute: NotRequired[RuleBooleanEmailAttributeType]

class RuleDmarcExpressionOutputTypeDef(TypedDict):
    Operator: RuleDmarcOperatorType
    Values: List[RuleDmarcPolicyType]

class RuleDmarcExpressionTypeDef(TypedDict):
    Operator: RuleDmarcOperatorType
    Values: Sequence[RuleDmarcPolicyType]

class RuleIpToEvaluateTypeDef(TypedDict):
    Attribute: NotRequired[Literal["SOURCE_IP"]]

class RuleNumberToEvaluateTypeDef(TypedDict):
    Attribute: NotRequired[Literal["MESSAGE_SIZE"]]

class RuleStringToEvaluateTypeDef(TypedDict):
    Attribute: NotRequired[RuleStringEmailAttributeType]
    MimeHeaderAttribute: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class StopArchiveExportRequestRequestTypeDef(TypedDict):
    ExportId: str

class StopArchiveSearchRequestRequestTypeDef(TypedDict):
    SearchId: str

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class RuleVerdictToEvaluateTypeDef(TypedDict):
    Analysis: NotRequired[AnalysisTypeDef]
    Attribute: NotRequired[RuleVerdictAttributeType]

class ArchiveBooleanExpressionTypeDef(TypedDict):
    Evaluate: ArchiveBooleanToEvaluateTypeDef
    Operator: ArchiveBooleanOperatorType

class UpdateArchiveRequestRequestTypeDef(TypedDict):
    ArchiveId: str
    ArchiveName: NotRequired[str]
    Retention: NotRequired[ArchiveRetentionTypeDef]

class ArchiveStringExpressionOutputTypeDef(TypedDict):
    Evaluate: ArchiveStringToEvaluateTypeDef
    Operator: Literal["CONTAINS"]
    Values: List[str]

class ArchiveStringExpressionTypeDef(TypedDict):
    Evaluate: ArchiveStringToEvaluateTypeDef
    Operator: Literal["CONTAINS"]
    Values: Sequence[str]

class CreateAddonInstanceRequestRequestTypeDef(TypedDict):
    AddonSubscriptionId: str
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateAddonSubscriptionRequestRequestTypeDef(TypedDict):
    AddonName: str
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateArchiveRequestRequestTypeDef(TypedDict):
    ArchiveName: str
    ClientToken: NotRequired[str]
    KmsKeyArn: NotRequired[str]
    Retention: NotRequired[ArchiveRetentionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]

class CreateAddonInstanceResponseTypeDef(TypedDict):
    AddonInstanceId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAddonSubscriptionResponseTypeDef(TypedDict):
    AddonSubscriptionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateArchiveResponseTypeDef(TypedDict):
    ArchiveId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateIngressPointResponseTypeDef(TypedDict):
    IngressPointId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRelayResponseTypeDef(TypedDict):
    RelayId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRuleSetResponseTypeDef(TypedDict):
    RuleSetId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTrafficPolicyResponseTypeDef(TypedDict):
    TrafficPolicyId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetAddonInstanceResponseTypeDef(TypedDict):
    AddonInstanceArn: str
    AddonName: str
    AddonSubscriptionId: str
    CreatedTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetAddonSubscriptionResponseTypeDef(TypedDict):
    AddonName: str
    AddonSubscriptionArn: str
    CreatedTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetArchiveResponseTypeDef(TypedDict):
    ArchiveArn: str
    ArchiveId: str
    ArchiveName: str
    ArchiveState: ArchiveStateType
    CreatedTimestamp: datetime
    KmsKeyArn: str
    LastUpdatedTimestamp: datetime
    Retention: ArchiveRetentionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAddonInstancesResponseTypeDef(TypedDict):
    AddonInstances: List[AddonInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAddonSubscriptionsResponseTypeDef(TypedDict):
    AddonSubscriptions: List[AddonSubscriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListArchivesResponseTypeDef(TypedDict):
    Archives: List[ArchiveTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StartArchiveExportResponseTypeDef(TypedDict):
    ExportId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartArchiveSearchResponseTypeDef(TypedDict):
    SearchId: str
    ResponseMetadata: ResponseMetadataTypeDef

CreateIngressPointRequestRequestTypeDef = TypedDict(
    "CreateIngressPointRequestRequestTypeDef",
    {
        "IngressPointName": str,
        "RuleSetId": str,
        "TrafficPolicyId": str,
        "Type": IngressPointTypeType,
        "ClientToken": NotRequired[str],
        "IngressPointConfiguration": NotRequired[IngressPointConfigurationTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

class UpdateIngressPointRequestRequestTypeDef(TypedDict):
    IngressPointId: str
    IngressPointConfiguration: NotRequired[IngressPointConfigurationTypeDef]
    IngressPointName: NotRequired[str]
    RuleSetId: NotRequired[str]
    StatusToUpdate: NotRequired[IngressPointStatusToUpdateType]
    TrafficPolicyId: NotRequired[str]

class CreateRelayRequestRequestTypeDef(TypedDict):
    Authentication: RelayAuthenticationTypeDef
    RelayName: str
    ServerName: str
    ServerPort: int
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class UpdateRelayRequestRequestTypeDef(TypedDict):
    RelayId: str
    Authentication: NotRequired[RelayAuthenticationTypeDef]
    RelayName: NotRequired[str]
    ServerName: NotRequired[str]
    ServerPort: NotRequired[int]

class RowTypeDef(TypedDict):
    ArchivedMessageId: NotRequired[str]
    Cc: NotRequired[str]
    Date: NotRequired[str]
    Envelope: NotRequired[EnvelopeTypeDef]
    From: NotRequired[str]
    HasAttachments: NotRequired[bool]
    InReplyTo: NotRequired[str]
    IngressPointId: NotRequired[str]
    MessageId: NotRequired[str]
    ReceivedHeaders: NotRequired[List[str]]
    ReceivedTimestamp: NotRequired[datetime]
    SenderHostname: NotRequired[str]
    SenderIpAddress: NotRequired[str]
    Subject: NotRequired[str]
    To: NotRequired[str]
    XMailer: NotRequired[str]
    XOriginalMailer: NotRequired[str]
    XPriority: NotRequired[str]

class ExportDestinationConfigurationTypeDef(TypedDict):
    S3: NotRequired[S3ExportDestinationConfigurationTypeDef]

class ExportSummaryTypeDef(TypedDict):
    ExportId: NotRequired[str]
    Status: NotRequired[ExportStatusTypeDef]

class GetArchiveMessageContentResponseTypeDef(TypedDict):
    Body: MessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetArchiveMessageResponseTypeDef(TypedDict):
    Envelope: EnvelopeTypeDef
    MessageDownloadLink: str
    Metadata: MetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SearchSummaryTypeDef(TypedDict):
    SearchId: NotRequired[str]
    Status: NotRequired[SearchStatusTypeDef]

class GetRelayResponseTypeDef(TypedDict):
    Authentication: RelayAuthenticationOutputTypeDef
    CreatedTimestamp: datetime
    LastModifiedTimestamp: datetime
    RelayArn: str
    RelayId: str
    RelayName: str
    ServerName: str
    ServerPort: int
    ResponseMetadata: ResponseMetadataTypeDef

class IngressBooleanToEvaluateTypeDef(TypedDict):
    Analysis: NotRequired[IngressAnalysisTypeDef]

class IngressIpv4ExpressionOutputTypeDef(TypedDict):
    Evaluate: IngressIpToEvaluateTypeDef
    Operator: IngressIpOperatorType
    Values: List[str]

class IngressIpv4ExpressionTypeDef(TypedDict):
    Evaluate: IngressIpToEvaluateTypeDef
    Operator: IngressIpOperatorType
    Values: Sequence[str]

class IngressPointAuthConfigurationTypeDef(TypedDict):
    IngressPointPasswordConfiguration: NotRequired[IngressPointPasswordConfigurationTypeDef]
    SecretArn: NotRequired[str]

class ListIngressPointsResponseTypeDef(TypedDict):
    IngressPoints: List[IngressPointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class IngressStringExpressionOutputTypeDef(TypedDict):
    Evaluate: IngressStringToEvaluateTypeDef
    Operator: IngressStringOperatorType
    Values: List[str]

class IngressStringExpressionTypeDef(TypedDict):
    Evaluate: IngressStringToEvaluateTypeDef
    Operator: IngressStringOperatorType
    Values: Sequence[str]

class IngressTlsProtocolExpressionTypeDef(TypedDict):
    Evaluate: IngressTlsProtocolToEvaluateTypeDef
    Operator: IngressTlsProtocolOperatorType
    Value: IngressTlsProtocolAttributeType

class ListAddonInstancesRequestListAddonInstancesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAddonSubscriptionsRequestListAddonSubscriptionsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListArchiveExportsRequestListArchiveExportsPaginateTypeDef(TypedDict):
    ArchiveId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListArchiveSearchesRequestListArchiveSearchesPaginateTypeDef(TypedDict):
    ArchiveId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListArchivesRequestListArchivesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListIngressPointsRequestListIngressPointsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRelaysRequestListRelaysPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRuleSetsRequestListRuleSetsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTrafficPoliciesRequestListTrafficPoliciesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRelaysResponseTypeDef(TypedDict):
    Relays: List[RelayTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListRuleSetsResponseTypeDef(TypedDict):
    RuleSets: List[RuleSetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTrafficPoliciesResponseTypeDef(TypedDict):
    TrafficPolicies: List[TrafficPolicyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

ReplaceRecipientActionUnionTypeDef = Union[
    ReplaceRecipientActionTypeDef, ReplaceRecipientActionOutputTypeDef
]

class RuleActionOutputTypeDef(TypedDict):
    AddHeader: NotRequired[AddHeaderActionTypeDef]
    Archive: NotRequired[ArchiveActionTypeDef]
    DeliverToMailbox: NotRequired[DeliverToMailboxActionTypeDef]
    DeliverToQBusiness: NotRequired[DeliverToQBusinessActionTypeDef]
    Drop: NotRequired[Dict[str, Any]]
    Relay: NotRequired[RelayActionTypeDef]
    ReplaceRecipient: NotRequired[ReplaceRecipientActionOutputTypeDef]
    Send: NotRequired[SendActionTypeDef]
    WriteToS3: NotRequired[S3ActionTypeDef]

class RuleBooleanExpressionTypeDef(TypedDict):
    Evaluate: RuleBooleanToEvaluateTypeDef
    Operator: RuleBooleanOperatorType

RuleDmarcExpressionUnionTypeDef = Union[
    RuleDmarcExpressionTypeDef, RuleDmarcExpressionOutputTypeDef
]

class RuleIpExpressionOutputTypeDef(TypedDict):
    Evaluate: RuleIpToEvaluateTypeDef
    Operator: RuleIpOperatorType
    Values: List[str]

class RuleIpExpressionTypeDef(TypedDict):
    Evaluate: RuleIpToEvaluateTypeDef
    Operator: RuleIpOperatorType
    Values: Sequence[str]

class RuleNumberExpressionTypeDef(TypedDict):
    Evaluate: RuleNumberToEvaluateTypeDef
    Operator: RuleNumberOperatorType
    Value: float

class RuleStringExpressionOutputTypeDef(TypedDict):
    Evaluate: RuleStringToEvaluateTypeDef
    Operator: RuleStringOperatorType
    Values: List[str]

class RuleStringExpressionTypeDef(TypedDict):
    Evaluate: RuleStringToEvaluateTypeDef
    Operator: RuleStringOperatorType
    Values: Sequence[str]

class RuleVerdictExpressionOutputTypeDef(TypedDict):
    Evaluate: RuleVerdictToEvaluateTypeDef
    Operator: RuleVerdictOperatorType
    Values: List[RuleVerdictType]

class RuleVerdictExpressionTypeDef(TypedDict):
    Evaluate: RuleVerdictToEvaluateTypeDef
    Operator: RuleVerdictOperatorType
    Values: Sequence[RuleVerdictType]

class ArchiveFilterConditionOutputTypeDef(TypedDict):
    BooleanExpression: NotRequired[ArchiveBooleanExpressionTypeDef]
    StringExpression: NotRequired[ArchiveStringExpressionOutputTypeDef]

ArchiveStringExpressionUnionTypeDef = Union[
    ArchiveStringExpressionTypeDef, ArchiveStringExpressionOutputTypeDef
]

class GetArchiveSearchResultsResponseTypeDef(TypedDict):
    Rows: List[RowTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListArchiveExportsResponseTypeDef(TypedDict):
    Exports: List[ExportSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListArchiveSearchesResponseTypeDef(TypedDict):
    Searches: List[SearchSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class IngressBooleanExpressionTypeDef(TypedDict):
    Evaluate: IngressBooleanToEvaluateTypeDef
    Operator: IngressBooleanOperatorType

IngressIpv4ExpressionUnionTypeDef = Union[
    IngressIpv4ExpressionTypeDef, IngressIpv4ExpressionOutputTypeDef
]
GetIngressPointResponseTypeDef = TypedDict(
    "GetIngressPointResponseTypeDef",
    {
        "ARecord": str,
        "CreatedTimestamp": datetime,
        "IngressPointArn": str,
        "IngressPointAuthConfiguration": IngressPointAuthConfigurationTypeDef,
        "IngressPointId": str,
        "IngressPointName": str,
        "LastUpdatedTimestamp": datetime,
        "RuleSetId": str,
        "Status": IngressPointStatusType,
        "TrafficPolicyId": str,
        "Type": IngressPointTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
IngressStringExpressionUnionTypeDef = Union[
    IngressStringExpressionTypeDef, IngressStringExpressionOutputTypeDef
]

class RuleActionTypeDef(TypedDict):
    AddHeader: NotRequired[AddHeaderActionTypeDef]
    Archive: NotRequired[ArchiveActionTypeDef]
    DeliverToMailbox: NotRequired[DeliverToMailboxActionTypeDef]
    DeliverToQBusiness: NotRequired[DeliverToQBusinessActionTypeDef]
    Drop: NotRequired[Mapping[str, Any]]
    Relay: NotRequired[RelayActionTypeDef]
    ReplaceRecipient: NotRequired[ReplaceRecipientActionUnionTypeDef]
    Send: NotRequired[SendActionTypeDef]
    WriteToS3: NotRequired[S3ActionTypeDef]

RuleIpExpressionUnionTypeDef = Union[RuleIpExpressionTypeDef, RuleIpExpressionOutputTypeDef]
RuleStringExpressionUnionTypeDef = Union[
    RuleStringExpressionTypeDef, RuleStringExpressionOutputTypeDef
]

class RuleConditionOutputTypeDef(TypedDict):
    BooleanExpression: NotRequired[RuleBooleanExpressionTypeDef]
    DmarcExpression: NotRequired[RuleDmarcExpressionOutputTypeDef]
    IpExpression: NotRequired[RuleIpExpressionOutputTypeDef]
    NumberExpression: NotRequired[RuleNumberExpressionTypeDef]
    StringExpression: NotRequired[RuleStringExpressionOutputTypeDef]
    VerdictExpression: NotRequired[RuleVerdictExpressionOutputTypeDef]

RuleVerdictExpressionUnionTypeDef = Union[
    RuleVerdictExpressionTypeDef, RuleVerdictExpressionOutputTypeDef
]

class ArchiveFiltersOutputTypeDef(TypedDict):
    Include: NotRequired[List[ArchiveFilterConditionOutputTypeDef]]
    Unless: NotRequired[List[ArchiveFilterConditionOutputTypeDef]]

class ArchiveFilterConditionTypeDef(TypedDict):
    BooleanExpression: NotRequired[ArchiveBooleanExpressionTypeDef]
    StringExpression: NotRequired[ArchiveStringExpressionUnionTypeDef]

class PolicyConditionOutputTypeDef(TypedDict):
    BooleanExpression: NotRequired[IngressBooleanExpressionTypeDef]
    IpExpression: NotRequired[IngressIpv4ExpressionOutputTypeDef]
    StringExpression: NotRequired[IngressStringExpressionOutputTypeDef]
    TlsExpression: NotRequired[IngressTlsProtocolExpressionTypeDef]

class PolicyConditionTypeDef(TypedDict):
    BooleanExpression: NotRequired[IngressBooleanExpressionTypeDef]
    IpExpression: NotRequired[IngressIpv4ExpressionUnionTypeDef]
    StringExpression: NotRequired[IngressStringExpressionUnionTypeDef]
    TlsExpression: NotRequired[IngressTlsProtocolExpressionTypeDef]

RuleActionUnionTypeDef = Union[RuleActionTypeDef, RuleActionOutputTypeDef]

class RuleOutputTypeDef(TypedDict):
    Actions: List[RuleActionOutputTypeDef]
    Conditions: NotRequired[List[RuleConditionOutputTypeDef]]
    Name: NotRequired[str]
    Unless: NotRequired[List[RuleConditionOutputTypeDef]]

class RuleConditionTypeDef(TypedDict):
    BooleanExpression: NotRequired[RuleBooleanExpressionTypeDef]
    DmarcExpression: NotRequired[RuleDmarcExpressionUnionTypeDef]
    IpExpression: NotRequired[RuleIpExpressionUnionTypeDef]
    NumberExpression: NotRequired[RuleNumberExpressionTypeDef]
    StringExpression: NotRequired[RuleStringExpressionUnionTypeDef]
    VerdictExpression: NotRequired[RuleVerdictExpressionUnionTypeDef]

class GetArchiveExportResponseTypeDef(TypedDict):
    ArchiveId: str
    ExportDestinationConfiguration: ExportDestinationConfigurationTypeDef
    Filters: ArchiveFiltersOutputTypeDef
    FromTimestamp: datetime
    MaxResults: int
    Status: ExportStatusTypeDef
    ToTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetArchiveSearchResponseTypeDef(TypedDict):
    ArchiveId: str
    Filters: ArchiveFiltersOutputTypeDef
    FromTimestamp: datetime
    MaxResults: int
    Status: SearchStatusTypeDef
    ToTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

ArchiveFilterConditionUnionTypeDef = Union[
    ArchiveFilterConditionTypeDef, ArchiveFilterConditionOutputTypeDef
]

class PolicyStatementOutputTypeDef(TypedDict):
    Action: AcceptActionType
    Conditions: List[PolicyConditionOutputTypeDef]

PolicyConditionUnionTypeDef = Union[PolicyConditionTypeDef, PolicyConditionOutputTypeDef]

class GetRuleSetResponseTypeDef(TypedDict):
    CreatedDate: datetime
    LastModificationDate: datetime
    RuleSetArn: str
    RuleSetId: str
    RuleSetName: str
    Rules: List[RuleOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

RuleConditionUnionTypeDef = Union[RuleConditionTypeDef, RuleConditionOutputTypeDef]

class ArchiveFiltersTypeDef(TypedDict):
    Include: NotRequired[Sequence[ArchiveFilterConditionUnionTypeDef]]
    Unless: NotRequired[Sequence[ArchiveFilterConditionTypeDef]]

class GetTrafficPolicyResponseTypeDef(TypedDict):
    CreatedTimestamp: datetime
    DefaultAction: AcceptActionType
    LastUpdatedTimestamp: datetime
    MaxMessageSizeBytes: int
    PolicyStatements: List[PolicyStatementOutputTypeDef]
    TrafficPolicyArn: str
    TrafficPolicyId: str
    TrafficPolicyName: str
    ResponseMetadata: ResponseMetadataTypeDef

class PolicyStatementTypeDef(TypedDict):
    Action: AcceptActionType
    Conditions: Sequence[PolicyConditionUnionTypeDef]

class RuleTypeDef(TypedDict):
    Actions: Sequence[RuleActionUnionTypeDef]
    Conditions: NotRequired[Sequence[RuleConditionUnionTypeDef]]
    Name: NotRequired[str]
    Unless: NotRequired[Sequence[RuleConditionTypeDef]]

class StartArchiveExportRequestRequestTypeDef(TypedDict):
    ArchiveId: str
    ExportDestinationConfiguration: ExportDestinationConfigurationTypeDef
    FromTimestamp: TimestampTypeDef
    ToTimestamp: TimestampTypeDef
    Filters: NotRequired[ArchiveFiltersTypeDef]
    IncludeMetadata: NotRequired[bool]
    MaxResults: NotRequired[int]

class StartArchiveSearchRequestRequestTypeDef(TypedDict):
    ArchiveId: str
    FromTimestamp: TimestampTypeDef
    MaxResults: int
    ToTimestamp: TimestampTypeDef
    Filters: NotRequired[ArchiveFiltersTypeDef]

PolicyStatementUnionTypeDef = Union[PolicyStatementTypeDef, PolicyStatementOutputTypeDef]

class UpdateTrafficPolicyRequestRequestTypeDef(TypedDict):
    TrafficPolicyId: str
    DefaultAction: NotRequired[AcceptActionType]
    MaxMessageSizeBytes: NotRequired[int]
    PolicyStatements: NotRequired[Sequence[PolicyStatementTypeDef]]
    TrafficPolicyName: NotRequired[str]

RuleUnionTypeDef = Union[RuleTypeDef, RuleOutputTypeDef]

class UpdateRuleSetRequestRequestTypeDef(TypedDict):
    RuleSetId: str
    RuleSetName: NotRequired[str]
    Rules: NotRequired[Sequence[RuleTypeDef]]

class CreateTrafficPolicyRequestRequestTypeDef(TypedDict):
    DefaultAction: AcceptActionType
    PolicyStatements: Sequence[PolicyStatementUnionTypeDef]
    TrafficPolicyName: str
    ClientToken: NotRequired[str]
    MaxMessageSizeBytes: NotRequired[int]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateRuleSetRequestRequestTypeDef(TypedDict):
    RuleSetName: str
    Rules: Sequence[RuleUnionTypeDef]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
