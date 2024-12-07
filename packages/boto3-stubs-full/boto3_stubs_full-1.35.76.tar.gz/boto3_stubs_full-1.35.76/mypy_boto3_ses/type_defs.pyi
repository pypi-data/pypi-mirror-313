"""
Type annotations for ses service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ses/type_defs/)

Usage::

    ```python
    from mypy_boto3_ses.type_defs import AddHeaderActionTypeDef

    data: AddHeaderActionTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    BehaviorOnMXFailureType,
    BounceTypeType,
    BulkEmailStatusType,
    ConfigurationSetAttributeType,
    CustomMailFromStatusType,
    DimensionValueSourceType,
    DsnActionType,
    EventTypeType,
    IdentityTypeType,
    InvocationTypeType,
    NotificationTypeType,
    ReceiptFilterPolicyType,
    SNSActionEncodingType,
    TlsPolicyType,
    VerificationStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AddHeaderActionTypeDef",
    "BlobTypeDef",
    "BodyTypeDef",
    "BounceActionTypeDef",
    "BouncedRecipientInfoTypeDef",
    "BulkEmailDestinationStatusTypeDef",
    "BulkEmailDestinationTypeDef",
    "CloneReceiptRuleSetRequestRequestTypeDef",
    "CloudWatchDestinationOutputTypeDef",
    "CloudWatchDestinationTypeDef",
    "CloudWatchDestinationUnionTypeDef",
    "CloudWatchDimensionConfigurationTypeDef",
    "ConfigurationSetTypeDef",
    "ConnectActionTypeDef",
    "ContentTypeDef",
    "CreateConfigurationSetEventDestinationRequestRequestTypeDef",
    "CreateConfigurationSetRequestRequestTypeDef",
    "CreateConfigurationSetTrackingOptionsRequestRequestTypeDef",
    "CreateCustomVerificationEmailTemplateRequestRequestTypeDef",
    "CreateReceiptFilterRequestRequestTypeDef",
    "CreateReceiptRuleRequestRequestTypeDef",
    "CreateReceiptRuleSetRequestRequestTypeDef",
    "CreateTemplateRequestRequestTypeDef",
    "CustomVerificationEmailTemplateTypeDef",
    "DeleteConfigurationSetEventDestinationRequestRequestTypeDef",
    "DeleteConfigurationSetRequestRequestTypeDef",
    "DeleteConfigurationSetTrackingOptionsRequestRequestTypeDef",
    "DeleteCustomVerificationEmailTemplateRequestRequestTypeDef",
    "DeleteIdentityPolicyRequestRequestTypeDef",
    "DeleteIdentityRequestRequestTypeDef",
    "DeleteReceiptFilterRequestRequestTypeDef",
    "DeleteReceiptRuleRequestRequestTypeDef",
    "DeleteReceiptRuleSetRequestRequestTypeDef",
    "DeleteTemplateRequestRequestTypeDef",
    "DeleteVerifiedEmailAddressRequestRequestTypeDef",
    "DeliveryOptionsTypeDef",
    "DescribeActiveReceiptRuleSetResponseTypeDef",
    "DescribeConfigurationSetRequestRequestTypeDef",
    "DescribeConfigurationSetResponseTypeDef",
    "DescribeReceiptRuleRequestRequestTypeDef",
    "DescribeReceiptRuleResponseTypeDef",
    "DescribeReceiptRuleSetRequestRequestTypeDef",
    "DescribeReceiptRuleSetResponseTypeDef",
    "DestinationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EventDestinationOutputTypeDef",
    "EventDestinationTypeDef",
    "ExtensionFieldTypeDef",
    "GetAccountSendingEnabledResponseTypeDef",
    "GetCustomVerificationEmailTemplateRequestRequestTypeDef",
    "GetCustomVerificationEmailTemplateResponseTypeDef",
    "GetIdentityDkimAttributesRequestRequestTypeDef",
    "GetIdentityDkimAttributesResponseTypeDef",
    "GetIdentityMailFromDomainAttributesRequestRequestTypeDef",
    "GetIdentityMailFromDomainAttributesResponseTypeDef",
    "GetIdentityNotificationAttributesRequestRequestTypeDef",
    "GetIdentityNotificationAttributesResponseTypeDef",
    "GetIdentityPoliciesRequestRequestTypeDef",
    "GetIdentityPoliciesResponseTypeDef",
    "GetIdentityVerificationAttributesRequestIdentityExistsWaitTypeDef",
    "GetIdentityVerificationAttributesRequestRequestTypeDef",
    "GetIdentityVerificationAttributesResponseTypeDef",
    "GetSendQuotaResponseTypeDef",
    "GetSendStatisticsResponseTypeDef",
    "GetTemplateRequestRequestTypeDef",
    "GetTemplateResponseTypeDef",
    "IdentityDkimAttributesTypeDef",
    "IdentityMailFromDomainAttributesTypeDef",
    "IdentityNotificationAttributesTypeDef",
    "IdentityVerificationAttributesTypeDef",
    "KinesisFirehoseDestinationTypeDef",
    "LambdaActionTypeDef",
    "ListConfigurationSetsRequestListConfigurationSetsPaginateTypeDef",
    "ListConfigurationSetsRequestRequestTypeDef",
    "ListConfigurationSetsResponseTypeDef",
    "ListCustomVerificationEmailTemplatesRequestListCustomVerificationEmailTemplatesPaginateTypeDef",
    "ListCustomVerificationEmailTemplatesRequestRequestTypeDef",
    "ListCustomVerificationEmailTemplatesResponseTypeDef",
    "ListIdentitiesRequestListIdentitiesPaginateTypeDef",
    "ListIdentitiesRequestRequestTypeDef",
    "ListIdentitiesResponseTypeDef",
    "ListIdentityPoliciesRequestRequestTypeDef",
    "ListIdentityPoliciesResponseTypeDef",
    "ListReceiptFiltersResponseTypeDef",
    "ListReceiptRuleSetsRequestListReceiptRuleSetsPaginateTypeDef",
    "ListReceiptRuleSetsRequestRequestTypeDef",
    "ListReceiptRuleSetsResponseTypeDef",
    "ListTemplatesRequestListTemplatesPaginateTypeDef",
    "ListTemplatesRequestRequestTypeDef",
    "ListTemplatesResponseTypeDef",
    "ListVerifiedEmailAddressesResponseTypeDef",
    "MessageDsnTypeDef",
    "MessageTagTypeDef",
    "MessageTypeDef",
    "PaginatorConfigTypeDef",
    "PutConfigurationSetDeliveryOptionsRequestRequestTypeDef",
    "PutIdentityPolicyRequestRequestTypeDef",
    "RawMessageTypeDef",
    "ReceiptActionTypeDef",
    "ReceiptFilterTypeDef",
    "ReceiptIpFilterTypeDef",
    "ReceiptRuleOutputTypeDef",
    "ReceiptRuleSetMetadataTypeDef",
    "ReceiptRuleTypeDef",
    "RecipientDsnFieldsTypeDef",
    "ReorderReceiptRuleSetRequestRequestTypeDef",
    "ReputationOptionsTypeDef",
    "ResponseMetadataTypeDef",
    "S3ActionTypeDef",
    "SNSActionTypeDef",
    "SNSDestinationTypeDef",
    "SendBounceRequestRequestTypeDef",
    "SendBounceResponseTypeDef",
    "SendBulkTemplatedEmailRequestRequestTypeDef",
    "SendBulkTemplatedEmailResponseTypeDef",
    "SendCustomVerificationEmailRequestRequestTypeDef",
    "SendCustomVerificationEmailResponseTypeDef",
    "SendDataPointTypeDef",
    "SendEmailRequestRequestTypeDef",
    "SendEmailResponseTypeDef",
    "SendRawEmailRequestRequestTypeDef",
    "SendRawEmailResponseTypeDef",
    "SendTemplatedEmailRequestRequestTypeDef",
    "SendTemplatedEmailResponseTypeDef",
    "SetActiveReceiptRuleSetRequestRequestTypeDef",
    "SetIdentityDkimEnabledRequestRequestTypeDef",
    "SetIdentityFeedbackForwardingEnabledRequestRequestTypeDef",
    "SetIdentityHeadersInNotificationsEnabledRequestRequestTypeDef",
    "SetIdentityMailFromDomainRequestRequestTypeDef",
    "SetIdentityNotificationTopicRequestRequestTypeDef",
    "SetReceiptRulePositionRequestRequestTypeDef",
    "StopActionTypeDef",
    "TemplateMetadataTypeDef",
    "TemplateTypeDef",
    "TestRenderTemplateRequestRequestTypeDef",
    "TestRenderTemplateResponseTypeDef",
    "TimestampTypeDef",
    "TrackingOptionsTypeDef",
    "UpdateAccountSendingEnabledRequestRequestTypeDef",
    "UpdateConfigurationSetEventDestinationRequestRequestTypeDef",
    "UpdateConfigurationSetReputationMetricsEnabledRequestRequestTypeDef",
    "UpdateConfigurationSetSendingEnabledRequestRequestTypeDef",
    "UpdateConfigurationSetTrackingOptionsRequestRequestTypeDef",
    "UpdateCustomVerificationEmailTemplateRequestRequestTypeDef",
    "UpdateReceiptRuleRequestRequestTypeDef",
    "UpdateTemplateRequestRequestTypeDef",
    "VerifyDomainDkimRequestRequestTypeDef",
    "VerifyDomainDkimResponseTypeDef",
    "VerifyDomainIdentityRequestRequestTypeDef",
    "VerifyDomainIdentityResponseTypeDef",
    "VerifyEmailAddressRequestRequestTypeDef",
    "VerifyEmailIdentityRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "WorkmailActionTypeDef",
)

class AddHeaderActionTypeDef(TypedDict):
    HeaderName: str
    HeaderValue: str

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class ContentTypeDef(TypedDict):
    Data: str
    Charset: NotRequired[str]

class BounceActionTypeDef(TypedDict):
    SmtpReplyCode: str
    Message: str
    Sender: str
    TopicArn: NotRequired[str]
    StatusCode: NotRequired[str]

class BulkEmailDestinationStatusTypeDef(TypedDict):
    Status: NotRequired[BulkEmailStatusType]
    Error: NotRequired[str]
    MessageId: NotRequired[str]

class DestinationTypeDef(TypedDict):
    ToAddresses: NotRequired[Sequence[str]]
    CcAddresses: NotRequired[Sequence[str]]
    BccAddresses: NotRequired[Sequence[str]]

class MessageTagTypeDef(TypedDict):
    Name: str
    Value: str

class CloneReceiptRuleSetRequestRequestTypeDef(TypedDict):
    RuleSetName: str
    OriginalRuleSetName: str

class CloudWatchDimensionConfigurationTypeDef(TypedDict):
    DimensionName: str
    DimensionValueSource: DimensionValueSourceType
    DefaultDimensionValue: str

class ConfigurationSetTypeDef(TypedDict):
    Name: str

class ConnectActionTypeDef(TypedDict):
    InstanceARN: str
    IAMRoleARN: str

class TrackingOptionsTypeDef(TypedDict):
    CustomRedirectDomain: NotRequired[str]

class CreateCustomVerificationEmailTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    FromEmailAddress: str
    TemplateSubject: str
    TemplateContent: str
    SuccessRedirectionURL: str
    FailureRedirectionURL: str

class CreateReceiptRuleSetRequestRequestTypeDef(TypedDict):
    RuleSetName: str

class TemplateTypeDef(TypedDict):
    TemplateName: str
    SubjectPart: NotRequired[str]
    TextPart: NotRequired[str]
    HtmlPart: NotRequired[str]

class CustomVerificationEmailTemplateTypeDef(TypedDict):
    TemplateName: NotRequired[str]
    FromEmailAddress: NotRequired[str]
    TemplateSubject: NotRequired[str]
    SuccessRedirectionURL: NotRequired[str]
    FailureRedirectionURL: NotRequired[str]

class DeleteConfigurationSetEventDestinationRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    EventDestinationName: str

class DeleteConfigurationSetRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str

class DeleteConfigurationSetTrackingOptionsRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str

class DeleteCustomVerificationEmailTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str

class DeleteIdentityPolicyRequestRequestTypeDef(TypedDict):
    Identity: str
    PolicyName: str

class DeleteIdentityRequestRequestTypeDef(TypedDict):
    Identity: str

class DeleteReceiptFilterRequestRequestTypeDef(TypedDict):
    FilterName: str

class DeleteReceiptRuleRequestRequestTypeDef(TypedDict):
    RuleSetName: str
    RuleName: str

class DeleteReceiptRuleSetRequestRequestTypeDef(TypedDict):
    RuleSetName: str

class DeleteTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str

class DeleteVerifiedEmailAddressRequestRequestTypeDef(TypedDict):
    EmailAddress: str

class DeliveryOptionsTypeDef(TypedDict):
    TlsPolicy: NotRequired[TlsPolicyType]

class ReceiptRuleSetMetadataTypeDef(TypedDict):
    Name: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DescribeConfigurationSetRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    ConfigurationSetAttributeNames: NotRequired[Sequence[ConfigurationSetAttributeType]]

class ReputationOptionsTypeDef(TypedDict):
    SendingEnabled: NotRequired[bool]
    ReputationMetricsEnabled: NotRequired[bool]
    LastFreshStart: NotRequired[datetime]

class DescribeReceiptRuleRequestRequestTypeDef(TypedDict):
    RuleSetName: str
    RuleName: str

class DescribeReceiptRuleSetRequestRequestTypeDef(TypedDict):
    RuleSetName: str

class KinesisFirehoseDestinationTypeDef(TypedDict):
    IAMRoleARN: str
    DeliveryStreamARN: str

class SNSDestinationTypeDef(TypedDict):
    TopicARN: str

class ExtensionFieldTypeDef(TypedDict):
    Name: str
    Value: str

class GetCustomVerificationEmailTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str

class GetIdentityDkimAttributesRequestRequestTypeDef(TypedDict):
    Identities: Sequence[str]

class IdentityDkimAttributesTypeDef(TypedDict):
    DkimEnabled: bool
    DkimVerificationStatus: VerificationStatusType
    DkimTokens: NotRequired[List[str]]

class GetIdentityMailFromDomainAttributesRequestRequestTypeDef(TypedDict):
    Identities: Sequence[str]

class IdentityMailFromDomainAttributesTypeDef(TypedDict):
    MailFromDomain: str
    MailFromDomainStatus: CustomMailFromStatusType
    BehaviorOnMXFailure: BehaviorOnMXFailureType

class GetIdentityNotificationAttributesRequestRequestTypeDef(TypedDict):
    Identities: Sequence[str]

class IdentityNotificationAttributesTypeDef(TypedDict):
    BounceTopic: str
    ComplaintTopic: str
    DeliveryTopic: str
    ForwardingEnabled: bool
    HeadersInBounceNotificationsEnabled: NotRequired[bool]
    HeadersInComplaintNotificationsEnabled: NotRequired[bool]
    HeadersInDeliveryNotificationsEnabled: NotRequired[bool]

class GetIdentityPoliciesRequestRequestTypeDef(TypedDict):
    Identity: str
    PolicyNames: Sequence[str]

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class GetIdentityVerificationAttributesRequestRequestTypeDef(TypedDict):
    Identities: Sequence[str]

class IdentityVerificationAttributesTypeDef(TypedDict):
    VerificationStatus: VerificationStatusType
    VerificationToken: NotRequired[str]

class SendDataPointTypeDef(TypedDict):
    Timestamp: NotRequired[datetime]
    DeliveryAttempts: NotRequired[int]
    Bounces: NotRequired[int]
    Complaints: NotRequired[int]
    Rejects: NotRequired[int]

class GetTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str

class LambdaActionTypeDef(TypedDict):
    FunctionArn: str
    TopicArn: NotRequired[str]
    InvocationType: NotRequired[InvocationTypeType]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListConfigurationSetsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxItems: NotRequired[int]

class ListCustomVerificationEmailTemplatesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListIdentitiesRequestRequestTypeDef(TypedDict):
    IdentityType: NotRequired[IdentityTypeType]
    NextToken: NotRequired[str]
    MaxItems: NotRequired[int]

class ListIdentityPoliciesRequestRequestTypeDef(TypedDict):
    Identity: str

class ListReceiptRuleSetsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]

class ListTemplatesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxItems: NotRequired[int]

class TemplateMetadataTypeDef(TypedDict):
    Name: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]

TimestampTypeDef = Union[datetime, str]

class PutIdentityPolicyRequestRequestTypeDef(TypedDict):
    Identity: str
    PolicyName: str
    Policy: str

class S3ActionTypeDef(TypedDict):
    BucketName: str
    TopicArn: NotRequired[str]
    ObjectKeyPrefix: NotRequired[str]
    KmsKeyArn: NotRequired[str]
    IamRoleArn: NotRequired[str]

class SNSActionTypeDef(TypedDict):
    TopicArn: str
    Encoding: NotRequired[SNSActionEncodingType]

class StopActionTypeDef(TypedDict):
    Scope: Literal["RuleSet"]
    TopicArn: NotRequired[str]

class WorkmailActionTypeDef(TypedDict):
    OrganizationArn: str
    TopicArn: NotRequired[str]

class ReceiptIpFilterTypeDef(TypedDict):
    Policy: ReceiptFilterPolicyType
    Cidr: str

class ReorderReceiptRuleSetRequestRequestTypeDef(TypedDict):
    RuleSetName: str
    RuleNames: Sequence[str]

class SendCustomVerificationEmailRequestRequestTypeDef(TypedDict):
    EmailAddress: str
    TemplateName: str
    ConfigurationSetName: NotRequired[str]

class SetActiveReceiptRuleSetRequestRequestTypeDef(TypedDict):
    RuleSetName: NotRequired[str]

class SetIdentityDkimEnabledRequestRequestTypeDef(TypedDict):
    Identity: str
    DkimEnabled: bool

class SetIdentityFeedbackForwardingEnabledRequestRequestTypeDef(TypedDict):
    Identity: str
    ForwardingEnabled: bool

class SetIdentityHeadersInNotificationsEnabledRequestRequestTypeDef(TypedDict):
    Identity: str
    NotificationType: NotificationTypeType
    Enabled: bool

class SetIdentityMailFromDomainRequestRequestTypeDef(TypedDict):
    Identity: str
    MailFromDomain: NotRequired[str]
    BehaviorOnMXFailure: NotRequired[BehaviorOnMXFailureType]

class SetIdentityNotificationTopicRequestRequestTypeDef(TypedDict):
    Identity: str
    NotificationType: NotificationTypeType
    SnsTopic: NotRequired[str]

class SetReceiptRulePositionRequestRequestTypeDef(TypedDict):
    RuleSetName: str
    RuleName: str
    After: NotRequired[str]

class TestRenderTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    TemplateData: str

class UpdateAccountSendingEnabledRequestRequestTypeDef(TypedDict):
    Enabled: NotRequired[bool]

class UpdateConfigurationSetReputationMetricsEnabledRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    Enabled: bool

class UpdateConfigurationSetSendingEnabledRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    Enabled: bool

class UpdateCustomVerificationEmailTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    FromEmailAddress: NotRequired[str]
    TemplateSubject: NotRequired[str]
    TemplateContent: NotRequired[str]
    SuccessRedirectionURL: NotRequired[str]
    FailureRedirectionURL: NotRequired[str]

class VerifyDomainDkimRequestRequestTypeDef(TypedDict):
    Domain: str

class VerifyDomainIdentityRequestRequestTypeDef(TypedDict):
    Domain: str

class VerifyEmailAddressRequestRequestTypeDef(TypedDict):
    EmailAddress: str

class VerifyEmailIdentityRequestRequestTypeDef(TypedDict):
    EmailAddress: str

class RawMessageTypeDef(TypedDict):
    Data: BlobTypeDef

BodyTypeDef = TypedDict(
    "BodyTypeDef",
    {
        "Text": NotRequired[ContentTypeDef],
        "Html": NotRequired[ContentTypeDef],
    },
)

class BulkEmailDestinationTypeDef(TypedDict):
    Destination: DestinationTypeDef
    ReplacementTags: NotRequired[Sequence[MessageTagTypeDef]]
    ReplacementTemplateData: NotRequired[str]

class SendTemplatedEmailRequestRequestTypeDef(TypedDict):
    Source: str
    Destination: DestinationTypeDef
    Template: str
    TemplateData: str
    ReplyToAddresses: NotRequired[Sequence[str]]
    ReturnPath: NotRequired[str]
    SourceArn: NotRequired[str]
    ReturnPathArn: NotRequired[str]
    Tags: NotRequired[Sequence[MessageTagTypeDef]]
    ConfigurationSetName: NotRequired[str]
    TemplateArn: NotRequired[str]

class CloudWatchDestinationOutputTypeDef(TypedDict):
    DimensionConfigurations: List[CloudWatchDimensionConfigurationTypeDef]

class CloudWatchDestinationTypeDef(TypedDict):
    DimensionConfigurations: Sequence[CloudWatchDimensionConfigurationTypeDef]

class CreateConfigurationSetRequestRequestTypeDef(TypedDict):
    ConfigurationSet: ConfigurationSetTypeDef

class CreateConfigurationSetTrackingOptionsRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    TrackingOptions: TrackingOptionsTypeDef

class UpdateConfigurationSetTrackingOptionsRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    TrackingOptions: TrackingOptionsTypeDef

class CreateTemplateRequestRequestTypeDef(TypedDict):
    Template: TemplateTypeDef

class UpdateTemplateRequestRequestTypeDef(TypedDict):
    Template: TemplateTypeDef

class PutConfigurationSetDeliveryOptionsRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    DeliveryOptions: NotRequired[DeliveryOptionsTypeDef]

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetAccountSendingEnabledResponseTypeDef(TypedDict):
    Enabled: bool
    ResponseMetadata: ResponseMetadataTypeDef

class GetCustomVerificationEmailTemplateResponseTypeDef(TypedDict):
    TemplateName: str
    FromEmailAddress: str
    TemplateSubject: str
    TemplateContent: str
    SuccessRedirectionURL: str
    FailureRedirectionURL: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetIdentityPoliciesResponseTypeDef(TypedDict):
    Policies: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetSendQuotaResponseTypeDef(TypedDict):
    Max24HourSend: float
    MaxSendRate: float
    SentLast24Hours: float
    ResponseMetadata: ResponseMetadataTypeDef

class GetTemplateResponseTypeDef(TypedDict):
    Template: TemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListConfigurationSetsResponseTypeDef(TypedDict):
    ConfigurationSets: List[ConfigurationSetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListCustomVerificationEmailTemplatesResponseTypeDef(TypedDict):
    CustomVerificationEmailTemplates: List[CustomVerificationEmailTemplateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListIdentitiesResponseTypeDef(TypedDict):
    Identities: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListIdentityPoliciesResponseTypeDef(TypedDict):
    PolicyNames: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListReceiptRuleSetsResponseTypeDef(TypedDict):
    RuleSets: List[ReceiptRuleSetMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListVerifiedEmailAddressesResponseTypeDef(TypedDict):
    VerifiedEmailAddresses: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class SendBounceResponseTypeDef(TypedDict):
    MessageId: str
    ResponseMetadata: ResponseMetadataTypeDef

class SendBulkTemplatedEmailResponseTypeDef(TypedDict):
    Status: List[BulkEmailDestinationStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class SendCustomVerificationEmailResponseTypeDef(TypedDict):
    MessageId: str
    ResponseMetadata: ResponseMetadataTypeDef

class SendEmailResponseTypeDef(TypedDict):
    MessageId: str
    ResponseMetadata: ResponseMetadataTypeDef

class SendRawEmailResponseTypeDef(TypedDict):
    MessageId: str
    ResponseMetadata: ResponseMetadataTypeDef

class SendTemplatedEmailResponseTypeDef(TypedDict):
    MessageId: str
    ResponseMetadata: ResponseMetadataTypeDef

class TestRenderTemplateResponseTypeDef(TypedDict):
    RenderedTemplate: str
    ResponseMetadata: ResponseMetadataTypeDef

class VerifyDomainDkimResponseTypeDef(TypedDict):
    DkimTokens: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class VerifyDomainIdentityResponseTypeDef(TypedDict):
    VerificationToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetIdentityDkimAttributesResponseTypeDef(TypedDict):
    DkimAttributes: Dict[str, IdentityDkimAttributesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetIdentityMailFromDomainAttributesResponseTypeDef(TypedDict):
    MailFromDomainAttributes: Dict[str, IdentityMailFromDomainAttributesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetIdentityNotificationAttributesResponseTypeDef(TypedDict):
    NotificationAttributes: Dict[str, IdentityNotificationAttributesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetIdentityVerificationAttributesRequestIdentityExistsWaitTypeDef(TypedDict):
    Identities: Sequence[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetIdentityVerificationAttributesResponseTypeDef(TypedDict):
    VerificationAttributes: Dict[str, IdentityVerificationAttributesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetSendStatisticsResponseTypeDef(TypedDict):
    SendDataPoints: List[SendDataPointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListConfigurationSetsRequestListConfigurationSetsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCustomVerificationEmailTemplatesRequestListCustomVerificationEmailTemplatesPaginateTypeDef(
    TypedDict
):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListIdentitiesRequestListIdentitiesPaginateTypeDef(TypedDict):
    IdentityType: NotRequired[IdentityTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListReceiptRuleSetsRequestListReceiptRuleSetsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTemplatesRequestListTemplatesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTemplatesResponseTypeDef(TypedDict):
    TemplatesMetadata: List[TemplateMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class MessageDsnTypeDef(TypedDict):
    ReportingMta: str
    ArrivalDate: NotRequired[TimestampTypeDef]
    ExtensionFields: NotRequired[Sequence[ExtensionFieldTypeDef]]

class RecipientDsnFieldsTypeDef(TypedDict):
    Action: DsnActionType
    Status: str
    FinalRecipient: NotRequired[str]
    RemoteMta: NotRequired[str]
    DiagnosticCode: NotRequired[str]
    LastAttemptDate: NotRequired[TimestampTypeDef]
    ExtensionFields: NotRequired[Sequence[ExtensionFieldTypeDef]]

class ReceiptActionTypeDef(TypedDict):
    S3Action: NotRequired[S3ActionTypeDef]
    BounceAction: NotRequired[BounceActionTypeDef]
    WorkmailAction: NotRequired[WorkmailActionTypeDef]
    LambdaAction: NotRequired[LambdaActionTypeDef]
    StopAction: NotRequired[StopActionTypeDef]
    AddHeaderAction: NotRequired[AddHeaderActionTypeDef]
    SNSAction: NotRequired[SNSActionTypeDef]
    ConnectAction: NotRequired[ConnectActionTypeDef]

class ReceiptFilterTypeDef(TypedDict):
    Name: str
    IpFilter: ReceiptIpFilterTypeDef

class SendRawEmailRequestRequestTypeDef(TypedDict):
    RawMessage: RawMessageTypeDef
    Source: NotRequired[str]
    Destinations: NotRequired[Sequence[str]]
    FromArn: NotRequired[str]
    SourceArn: NotRequired[str]
    ReturnPathArn: NotRequired[str]
    Tags: NotRequired[Sequence[MessageTagTypeDef]]
    ConfigurationSetName: NotRequired[str]

class MessageTypeDef(TypedDict):
    Subject: ContentTypeDef
    Body: BodyTypeDef

class SendBulkTemplatedEmailRequestRequestTypeDef(TypedDict):
    Source: str
    Template: str
    DefaultTemplateData: str
    Destinations: Sequence[BulkEmailDestinationTypeDef]
    SourceArn: NotRequired[str]
    ReplyToAddresses: NotRequired[Sequence[str]]
    ReturnPath: NotRequired[str]
    ReturnPathArn: NotRequired[str]
    ConfigurationSetName: NotRequired[str]
    DefaultTags: NotRequired[Sequence[MessageTagTypeDef]]
    TemplateArn: NotRequired[str]

class EventDestinationOutputTypeDef(TypedDict):
    Name: str
    MatchingEventTypes: List[EventTypeType]
    Enabled: NotRequired[bool]
    KinesisFirehoseDestination: NotRequired[KinesisFirehoseDestinationTypeDef]
    CloudWatchDestination: NotRequired[CloudWatchDestinationOutputTypeDef]
    SNSDestination: NotRequired[SNSDestinationTypeDef]

CloudWatchDestinationUnionTypeDef = Union[
    CloudWatchDestinationTypeDef, CloudWatchDestinationOutputTypeDef
]

class BouncedRecipientInfoTypeDef(TypedDict):
    Recipient: str
    RecipientArn: NotRequired[str]
    BounceType: NotRequired[BounceTypeType]
    RecipientDsnFields: NotRequired[RecipientDsnFieldsTypeDef]

class ReceiptRuleOutputTypeDef(TypedDict):
    Name: str
    Enabled: NotRequired[bool]
    TlsPolicy: NotRequired[TlsPolicyType]
    Recipients: NotRequired[List[str]]
    Actions: NotRequired[List[ReceiptActionTypeDef]]
    ScanEnabled: NotRequired[bool]

class ReceiptRuleTypeDef(TypedDict):
    Name: str
    Enabled: NotRequired[bool]
    TlsPolicy: NotRequired[TlsPolicyType]
    Recipients: NotRequired[Sequence[str]]
    Actions: NotRequired[Sequence[ReceiptActionTypeDef]]
    ScanEnabled: NotRequired[bool]

class CreateReceiptFilterRequestRequestTypeDef(TypedDict):
    Filter: ReceiptFilterTypeDef

class ListReceiptFiltersResponseTypeDef(TypedDict):
    Filters: List[ReceiptFilterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class SendEmailRequestRequestTypeDef(TypedDict):
    Source: str
    Destination: DestinationTypeDef
    Message: MessageTypeDef
    ReplyToAddresses: NotRequired[Sequence[str]]
    ReturnPath: NotRequired[str]
    SourceArn: NotRequired[str]
    ReturnPathArn: NotRequired[str]
    Tags: NotRequired[Sequence[MessageTagTypeDef]]
    ConfigurationSetName: NotRequired[str]

class DescribeConfigurationSetResponseTypeDef(TypedDict):
    ConfigurationSet: ConfigurationSetTypeDef
    EventDestinations: List[EventDestinationOutputTypeDef]
    TrackingOptions: TrackingOptionsTypeDef
    DeliveryOptions: DeliveryOptionsTypeDef
    ReputationOptions: ReputationOptionsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class EventDestinationTypeDef(TypedDict):
    Name: str
    MatchingEventTypes: Sequence[EventTypeType]
    Enabled: NotRequired[bool]
    KinesisFirehoseDestination: NotRequired[KinesisFirehoseDestinationTypeDef]
    CloudWatchDestination: NotRequired[CloudWatchDestinationUnionTypeDef]
    SNSDestination: NotRequired[SNSDestinationTypeDef]

class SendBounceRequestRequestTypeDef(TypedDict):
    OriginalMessageId: str
    BounceSender: str
    BouncedRecipientInfoList: Sequence[BouncedRecipientInfoTypeDef]
    Explanation: NotRequired[str]
    MessageDsn: NotRequired[MessageDsnTypeDef]
    BounceSenderArn: NotRequired[str]

class DescribeActiveReceiptRuleSetResponseTypeDef(TypedDict):
    Metadata: ReceiptRuleSetMetadataTypeDef
    Rules: List[ReceiptRuleOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeReceiptRuleResponseTypeDef(TypedDict):
    Rule: ReceiptRuleOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeReceiptRuleSetResponseTypeDef(TypedDict):
    Metadata: ReceiptRuleSetMetadataTypeDef
    Rules: List[ReceiptRuleOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateReceiptRuleRequestRequestTypeDef(TypedDict):
    RuleSetName: str
    Rule: ReceiptRuleTypeDef
    After: NotRequired[str]

class UpdateReceiptRuleRequestRequestTypeDef(TypedDict):
    RuleSetName: str
    Rule: ReceiptRuleTypeDef

class CreateConfigurationSetEventDestinationRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    EventDestination: EventDestinationTypeDef

class UpdateConfigurationSetEventDestinationRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    EventDestination: EventDestinationTypeDef
