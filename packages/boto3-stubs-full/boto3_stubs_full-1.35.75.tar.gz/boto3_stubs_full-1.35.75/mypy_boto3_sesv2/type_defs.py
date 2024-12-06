"""
Type annotations for sesv2 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/type_defs/)

Usage::

    ```python
    from mypy_boto3_sesv2.type_defs import ReviewDetailsTypeDef

    data: ReviewDetailsTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    BehaviorOnMxFailureType,
    BounceTypeType,
    BulkEmailStatusType,
    ContactLanguageType,
    ContactListImportActionType,
    DataFormatType,
    DeliverabilityDashboardAccountStatusType,
    DeliverabilityTestStatusType,
    DeliveryEventTypeType,
    DimensionValueSourceType,
    DkimSigningAttributesOriginType,
    DkimSigningKeyLengthType,
    DkimStatusType,
    EngagementEventTypeType,
    EventTypeType,
    ExportSourceTypeType,
    FeatureStatusType,
    HttpsPolicyType,
    IdentityTypeType,
    ImportDestinationTypeType,
    JobStatusType,
    ListRecommendationsFilterKeyType,
    MailFromDomainStatusType,
    MailTypeType,
    MetricAggregationType,
    MetricDimensionNameType,
    MetricType,
    QueryErrorCodeType,
    RecommendationImpactType,
    RecommendationStatusType,
    RecommendationTypeType,
    ReviewStatusType,
    ScalingModeType,
    SubscriptionStatusType,
    SuppressionListImportActionType,
    SuppressionListReasonType,
    TlsPolicyType,
    VerificationErrorType,
    VerificationStatusType,
    WarmupStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccountDetailsTypeDef",
    "BatchGetMetricDataQueryTypeDef",
    "BatchGetMetricDataRequestRequestTypeDef",
    "BatchGetMetricDataResponseTypeDef",
    "BlacklistEntryTypeDef",
    "BlobTypeDef",
    "BodyTypeDef",
    "BounceTypeDef",
    "BulkEmailContentTypeDef",
    "BulkEmailEntryResultTypeDef",
    "BulkEmailEntryTypeDef",
    "CancelExportJobRequestRequestTypeDef",
    "CloudWatchDestinationOutputTypeDef",
    "CloudWatchDestinationTypeDef",
    "CloudWatchDestinationUnionTypeDef",
    "CloudWatchDimensionConfigurationTypeDef",
    "ComplaintTypeDef",
    "ContactListDestinationTypeDef",
    "ContactListTypeDef",
    "ContactTypeDef",
    "ContentTypeDef",
    "CreateConfigurationSetEventDestinationRequestRequestTypeDef",
    "CreateConfigurationSetRequestRequestTypeDef",
    "CreateContactListRequestRequestTypeDef",
    "CreateContactRequestRequestTypeDef",
    "CreateCustomVerificationEmailTemplateRequestRequestTypeDef",
    "CreateDedicatedIpPoolRequestRequestTypeDef",
    "CreateDeliverabilityTestReportRequestRequestTypeDef",
    "CreateDeliverabilityTestReportResponseTypeDef",
    "CreateEmailIdentityPolicyRequestRequestTypeDef",
    "CreateEmailIdentityRequestRequestTypeDef",
    "CreateEmailIdentityResponseTypeDef",
    "CreateEmailTemplateRequestRequestTypeDef",
    "CreateExportJobRequestRequestTypeDef",
    "CreateExportJobResponseTypeDef",
    "CreateImportJobRequestRequestTypeDef",
    "CreateImportJobResponseTypeDef",
    "CustomVerificationEmailTemplateMetadataTypeDef",
    "DailyVolumeTypeDef",
    "DashboardAttributesTypeDef",
    "DashboardOptionsTypeDef",
    "DedicatedIpPoolTypeDef",
    "DedicatedIpTypeDef",
    "DeleteConfigurationSetEventDestinationRequestRequestTypeDef",
    "DeleteConfigurationSetRequestRequestTypeDef",
    "DeleteContactListRequestRequestTypeDef",
    "DeleteContactRequestRequestTypeDef",
    "DeleteCustomVerificationEmailTemplateRequestRequestTypeDef",
    "DeleteDedicatedIpPoolRequestRequestTypeDef",
    "DeleteEmailIdentityPolicyRequestRequestTypeDef",
    "DeleteEmailIdentityRequestRequestTypeDef",
    "DeleteEmailTemplateRequestRequestTypeDef",
    "DeleteSuppressedDestinationRequestRequestTypeDef",
    "DeliverabilityTestReportTypeDef",
    "DeliveryOptionsTypeDef",
    "DestinationTypeDef",
    "DkimAttributesTypeDef",
    "DkimSigningAttributesTypeDef",
    "DomainDeliverabilityCampaignTypeDef",
    "DomainDeliverabilityTrackingOptionOutputTypeDef",
    "DomainDeliverabilityTrackingOptionTypeDef",
    "DomainDeliverabilityTrackingOptionUnionTypeDef",
    "DomainIspPlacementTypeDef",
    "EmailContentTypeDef",
    "EmailInsightsTypeDef",
    "EmailTemplateContentTypeDef",
    "EmailTemplateMetadataTypeDef",
    "EventBridgeDestinationTypeDef",
    "EventDestinationDefinitionTypeDef",
    "EventDestinationTypeDef",
    "EventDetailsTypeDef",
    "ExportDataSourceOutputTypeDef",
    "ExportDataSourceTypeDef",
    "ExportDestinationTypeDef",
    "ExportJobSummaryTypeDef",
    "ExportMetricTypeDef",
    "ExportStatisticsTypeDef",
    "FailureInfoTypeDef",
    "GetAccountResponseTypeDef",
    "GetBlacklistReportsRequestRequestTypeDef",
    "GetBlacklistReportsResponseTypeDef",
    "GetConfigurationSetEventDestinationsRequestRequestTypeDef",
    "GetConfigurationSetEventDestinationsResponseTypeDef",
    "GetConfigurationSetRequestRequestTypeDef",
    "GetConfigurationSetResponseTypeDef",
    "GetContactListRequestRequestTypeDef",
    "GetContactListResponseTypeDef",
    "GetContactRequestRequestTypeDef",
    "GetContactResponseTypeDef",
    "GetCustomVerificationEmailTemplateRequestRequestTypeDef",
    "GetCustomVerificationEmailTemplateResponseTypeDef",
    "GetDedicatedIpPoolRequestRequestTypeDef",
    "GetDedicatedIpPoolResponseTypeDef",
    "GetDedicatedIpRequestRequestTypeDef",
    "GetDedicatedIpResponseTypeDef",
    "GetDedicatedIpsRequestRequestTypeDef",
    "GetDedicatedIpsResponseTypeDef",
    "GetDeliverabilityDashboardOptionsResponseTypeDef",
    "GetDeliverabilityTestReportRequestRequestTypeDef",
    "GetDeliverabilityTestReportResponseTypeDef",
    "GetDomainDeliverabilityCampaignRequestRequestTypeDef",
    "GetDomainDeliverabilityCampaignResponseTypeDef",
    "GetDomainStatisticsReportRequestRequestTypeDef",
    "GetDomainStatisticsReportResponseTypeDef",
    "GetEmailIdentityPoliciesRequestRequestTypeDef",
    "GetEmailIdentityPoliciesResponseTypeDef",
    "GetEmailIdentityRequestRequestTypeDef",
    "GetEmailIdentityResponseTypeDef",
    "GetEmailTemplateRequestRequestTypeDef",
    "GetEmailTemplateResponseTypeDef",
    "GetExportJobRequestRequestTypeDef",
    "GetExportJobResponseTypeDef",
    "GetImportJobRequestRequestTypeDef",
    "GetImportJobResponseTypeDef",
    "GetMessageInsightsRequestRequestTypeDef",
    "GetMessageInsightsResponseTypeDef",
    "GetSuppressedDestinationRequestRequestTypeDef",
    "GetSuppressedDestinationResponseTypeDef",
    "GuardianAttributesTypeDef",
    "GuardianOptionsTypeDef",
    "IdentityInfoTypeDef",
    "ImportDataSourceTypeDef",
    "ImportDestinationTypeDef",
    "ImportJobSummaryTypeDef",
    "InboxPlacementTrackingOptionOutputTypeDef",
    "InboxPlacementTrackingOptionTypeDef",
    "InboxPlacementTrackingOptionUnionTypeDef",
    "InsightsEventTypeDef",
    "IspPlacementTypeDef",
    "KinesisFirehoseDestinationTypeDef",
    "ListConfigurationSetsRequestRequestTypeDef",
    "ListConfigurationSetsResponseTypeDef",
    "ListContactListsRequestRequestTypeDef",
    "ListContactListsResponseTypeDef",
    "ListContactsFilterTypeDef",
    "ListContactsRequestRequestTypeDef",
    "ListContactsResponseTypeDef",
    "ListCustomVerificationEmailTemplatesRequestRequestTypeDef",
    "ListCustomVerificationEmailTemplatesResponseTypeDef",
    "ListDedicatedIpPoolsRequestRequestTypeDef",
    "ListDedicatedIpPoolsResponseTypeDef",
    "ListDeliverabilityTestReportsRequestRequestTypeDef",
    "ListDeliverabilityTestReportsResponseTypeDef",
    "ListDomainDeliverabilityCampaignsRequestRequestTypeDef",
    "ListDomainDeliverabilityCampaignsResponseTypeDef",
    "ListEmailIdentitiesRequestRequestTypeDef",
    "ListEmailIdentitiesResponseTypeDef",
    "ListEmailTemplatesRequestRequestTypeDef",
    "ListEmailTemplatesResponseTypeDef",
    "ListExportJobsRequestRequestTypeDef",
    "ListExportJobsResponseTypeDef",
    "ListImportJobsRequestRequestTypeDef",
    "ListImportJobsResponseTypeDef",
    "ListManagementOptionsTypeDef",
    "ListRecommendationsRequestRequestTypeDef",
    "ListRecommendationsResponseTypeDef",
    "ListSuppressedDestinationsRequestRequestTypeDef",
    "ListSuppressedDestinationsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MailFromAttributesTypeDef",
    "MessageHeaderTypeDef",
    "MessageInsightsDataSourceOutputTypeDef",
    "MessageInsightsDataSourceTypeDef",
    "MessageInsightsDataSourceUnionTypeDef",
    "MessageInsightsFiltersOutputTypeDef",
    "MessageInsightsFiltersTypeDef",
    "MessageInsightsFiltersUnionTypeDef",
    "MessageTagTypeDef",
    "MessageTypeDef",
    "MetricDataErrorTypeDef",
    "MetricDataResultTypeDef",
    "MetricsDataSourceOutputTypeDef",
    "MetricsDataSourceTypeDef",
    "MetricsDataSourceUnionTypeDef",
    "OverallVolumeTypeDef",
    "PinpointDestinationTypeDef",
    "PlacementStatisticsTypeDef",
    "PutAccountDedicatedIpWarmupAttributesRequestRequestTypeDef",
    "PutAccountDetailsRequestRequestTypeDef",
    "PutAccountSendingAttributesRequestRequestTypeDef",
    "PutAccountSuppressionAttributesRequestRequestTypeDef",
    "PutAccountVdmAttributesRequestRequestTypeDef",
    "PutConfigurationSetDeliveryOptionsRequestRequestTypeDef",
    "PutConfigurationSetReputationOptionsRequestRequestTypeDef",
    "PutConfigurationSetSendingOptionsRequestRequestTypeDef",
    "PutConfigurationSetSuppressionOptionsRequestRequestTypeDef",
    "PutConfigurationSetTrackingOptionsRequestRequestTypeDef",
    "PutConfigurationSetVdmOptionsRequestRequestTypeDef",
    "PutDedicatedIpInPoolRequestRequestTypeDef",
    "PutDedicatedIpPoolScalingAttributesRequestRequestTypeDef",
    "PutDedicatedIpWarmupAttributesRequestRequestTypeDef",
    "PutDeliverabilityDashboardOptionRequestRequestTypeDef",
    "PutEmailIdentityConfigurationSetAttributesRequestRequestTypeDef",
    "PutEmailIdentityDkimAttributesRequestRequestTypeDef",
    "PutEmailIdentityDkimSigningAttributesRequestRequestTypeDef",
    "PutEmailIdentityDkimSigningAttributesResponseTypeDef",
    "PutEmailIdentityFeedbackAttributesRequestRequestTypeDef",
    "PutEmailIdentityMailFromAttributesRequestRequestTypeDef",
    "PutSuppressedDestinationRequestRequestTypeDef",
    "RawMessageTypeDef",
    "RecommendationTypeDef",
    "ReplacementEmailContentTypeDef",
    "ReplacementTemplateTypeDef",
    "ReputationOptionsOutputTypeDef",
    "ReputationOptionsTypeDef",
    "ResponseMetadataTypeDef",
    "ReviewDetailsTypeDef",
    "SOARecordTypeDef",
    "SendBulkEmailRequestRequestTypeDef",
    "SendBulkEmailResponseTypeDef",
    "SendCustomVerificationEmailRequestRequestTypeDef",
    "SendCustomVerificationEmailResponseTypeDef",
    "SendEmailRequestRequestTypeDef",
    "SendEmailResponseTypeDef",
    "SendQuotaTypeDef",
    "SendingOptionsTypeDef",
    "SnsDestinationTypeDef",
    "SuppressedDestinationAttributesTypeDef",
    "SuppressedDestinationSummaryTypeDef",
    "SuppressedDestinationTypeDef",
    "SuppressionAttributesTypeDef",
    "SuppressionListDestinationTypeDef",
    "SuppressionOptionsOutputTypeDef",
    "SuppressionOptionsTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TemplateTypeDef",
    "TestRenderEmailTemplateRequestRequestTypeDef",
    "TestRenderEmailTemplateResponseTypeDef",
    "TimestampTypeDef",
    "TopicFilterTypeDef",
    "TopicPreferenceTypeDef",
    "TopicTypeDef",
    "TrackingOptionsTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateConfigurationSetEventDestinationRequestRequestTypeDef",
    "UpdateContactListRequestRequestTypeDef",
    "UpdateContactRequestRequestTypeDef",
    "UpdateCustomVerificationEmailTemplateRequestRequestTypeDef",
    "UpdateEmailIdentityPolicyRequestRequestTypeDef",
    "UpdateEmailTemplateRequestRequestTypeDef",
    "VdmAttributesTypeDef",
    "VdmOptionsTypeDef",
    "VerificationInfoTypeDef",
    "VolumeStatisticsTypeDef",
)


class ReviewDetailsTypeDef(TypedDict):
    Status: NotRequired[ReviewStatusType]
    CaseId: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class MetricDataErrorTypeDef(TypedDict):
    Id: NotRequired[str]
    Code: NotRequired[QueryErrorCodeType]
    Message: NotRequired[str]


class MetricDataResultTypeDef(TypedDict):
    Id: NotRequired[str]
    Timestamps: NotRequired[List[datetime]]
    Values: NotRequired[List[int]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class BlacklistEntryTypeDef(TypedDict):
    RblName: NotRequired[str]
    ListingTime: NotRequired[datetime]
    Description: NotRequired[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class ContentTypeDef(TypedDict):
    Data: str
    Charset: NotRequired[str]


class BounceTypeDef(TypedDict):
    BounceType: NotRequired[BounceTypeType]
    BounceSubType: NotRequired[str]
    DiagnosticCode: NotRequired[str]


class BulkEmailEntryResultTypeDef(TypedDict):
    Status: NotRequired[BulkEmailStatusType]
    Error: NotRequired[str]
    MessageId: NotRequired[str]


class DestinationTypeDef(TypedDict):
    ToAddresses: NotRequired[Sequence[str]]
    CcAddresses: NotRequired[Sequence[str]]
    BccAddresses: NotRequired[Sequence[str]]


class MessageHeaderTypeDef(TypedDict):
    Name: str
    Value: str


class MessageTagTypeDef(TypedDict):
    Name: str
    Value: str


class CancelExportJobRequestRequestTypeDef(TypedDict):
    JobId: str


class CloudWatchDimensionConfigurationTypeDef(TypedDict):
    DimensionName: str
    DimensionValueSource: DimensionValueSourceType
    DefaultDimensionValue: str


class ComplaintTypeDef(TypedDict):
    ComplaintSubType: NotRequired[str]
    ComplaintFeedbackType: NotRequired[str]


class ContactListDestinationTypeDef(TypedDict):
    ContactListName: str
    ContactListImportAction: ContactListImportActionType


class ContactListTypeDef(TypedDict):
    ContactListName: NotRequired[str]
    LastUpdatedTimestamp: NotRequired[datetime]


class TopicPreferenceTypeDef(TypedDict):
    TopicName: str
    SubscriptionStatus: SubscriptionStatusType


class DeliveryOptionsTypeDef(TypedDict):
    TlsPolicy: NotRequired[TlsPolicyType]
    SendingPoolName: NotRequired[str]
    MaxDeliverySeconds: NotRequired[int]


class SendingOptionsTypeDef(TypedDict):
    SendingEnabled: NotRequired[bool]


class SuppressionOptionsTypeDef(TypedDict):
    SuppressedReasons: NotRequired[Sequence[SuppressionListReasonType]]


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class TrackingOptionsTypeDef(TypedDict):
    CustomRedirectDomain: str
    HttpsPolicy: NotRequired[HttpsPolicyType]


class TopicTypeDef(TypedDict):
    TopicName: str
    DisplayName: str
    DefaultSubscriptionStatus: SubscriptionStatusType
    Description: NotRequired[str]


class CreateCustomVerificationEmailTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    FromEmailAddress: str
    TemplateSubject: str
    TemplateContent: str
    SuccessRedirectionURL: str
    FailureRedirectionURL: str


class CreateEmailIdentityPolicyRequestRequestTypeDef(TypedDict):
    EmailIdentity: str
    PolicyName: str
    Policy: str


class DkimSigningAttributesTypeDef(TypedDict):
    DomainSigningSelector: NotRequired[str]
    DomainSigningPrivateKey: NotRequired[str]
    NextSigningKeyLength: NotRequired[DkimSigningKeyLengthType]


class DkimAttributesTypeDef(TypedDict):
    SigningEnabled: NotRequired[bool]
    Status: NotRequired[DkimStatusType]
    Tokens: NotRequired[List[str]]
    SigningAttributesOrigin: NotRequired[DkimSigningAttributesOriginType]
    NextSigningKeyLength: NotRequired[DkimSigningKeyLengthType]
    CurrentSigningKeyLength: NotRequired[DkimSigningKeyLengthType]
    LastKeyGenerationTimestamp: NotRequired[datetime]


EmailTemplateContentTypeDef = TypedDict(
    "EmailTemplateContentTypeDef",
    {
        "Subject": NotRequired[str],
        "Text": NotRequired[str],
        "Html": NotRequired[str],
    },
)


class ExportDestinationTypeDef(TypedDict):
    DataFormat: DataFormatType
    S3Url: NotRequired[str]


class ImportDataSourceTypeDef(TypedDict):
    S3Url: str
    DataFormat: DataFormatType


class CustomVerificationEmailTemplateMetadataTypeDef(TypedDict):
    TemplateName: NotRequired[str]
    FromEmailAddress: NotRequired[str]
    TemplateSubject: NotRequired[str]
    SuccessRedirectionURL: NotRequired[str]
    FailureRedirectionURL: NotRequired[str]


class DomainIspPlacementTypeDef(TypedDict):
    IspName: NotRequired[str]
    InboxRawCount: NotRequired[int]
    SpamRawCount: NotRequired[int]
    InboxPercentage: NotRequired[float]
    SpamPercentage: NotRequired[float]


class VolumeStatisticsTypeDef(TypedDict):
    InboxRawCount: NotRequired[int]
    SpamRawCount: NotRequired[int]
    ProjectedInbox: NotRequired[int]
    ProjectedSpam: NotRequired[int]


class DashboardAttributesTypeDef(TypedDict):
    EngagementMetrics: NotRequired[FeatureStatusType]


class DashboardOptionsTypeDef(TypedDict):
    EngagementMetrics: NotRequired[FeatureStatusType]


class DedicatedIpPoolTypeDef(TypedDict):
    PoolName: str
    ScalingMode: ScalingModeType


class DedicatedIpTypeDef(TypedDict):
    Ip: str
    WarmupStatus: WarmupStatusType
    WarmupPercentage: int
    PoolName: NotRequired[str]


class DeleteConfigurationSetEventDestinationRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    EventDestinationName: str


class DeleteConfigurationSetRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str


class DeleteContactListRequestRequestTypeDef(TypedDict):
    ContactListName: str


class DeleteContactRequestRequestTypeDef(TypedDict):
    ContactListName: str
    EmailAddress: str


class DeleteCustomVerificationEmailTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str


class DeleteDedicatedIpPoolRequestRequestTypeDef(TypedDict):
    PoolName: str


class DeleteEmailIdentityPolicyRequestRequestTypeDef(TypedDict):
    EmailIdentity: str
    PolicyName: str


class DeleteEmailIdentityRequestRequestTypeDef(TypedDict):
    EmailIdentity: str


class DeleteEmailTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str


class DeleteSuppressedDestinationRequestRequestTypeDef(TypedDict):
    EmailAddress: str


class DeliverabilityTestReportTypeDef(TypedDict):
    ReportId: NotRequired[str]
    ReportName: NotRequired[str]
    Subject: NotRequired[str]
    FromEmailAddress: NotRequired[str]
    CreateDate: NotRequired[datetime]
    DeliverabilityTestStatus: NotRequired[DeliverabilityTestStatusType]


class DomainDeliverabilityCampaignTypeDef(TypedDict):
    CampaignId: NotRequired[str]
    ImageUrl: NotRequired[str]
    Subject: NotRequired[str]
    FromAddress: NotRequired[str]
    SendingIps: NotRequired[List[str]]
    FirstSeenDateTime: NotRequired[datetime]
    LastSeenDateTime: NotRequired[datetime]
    InboxCount: NotRequired[int]
    SpamCount: NotRequired[int]
    ReadRate: NotRequired[float]
    DeleteRate: NotRequired[float]
    ReadDeleteRate: NotRequired[float]
    ProjectedVolume: NotRequired[int]
    Esps: NotRequired[List[str]]


class InboxPlacementTrackingOptionOutputTypeDef(TypedDict):
    Global: NotRequired[bool]
    TrackedIsps: NotRequired[List[str]]


class EmailTemplateMetadataTypeDef(TypedDict):
    TemplateName: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]


class EventBridgeDestinationTypeDef(TypedDict):
    EventBusArn: str


class KinesisFirehoseDestinationTypeDef(TypedDict):
    IamRoleArn: str
    DeliveryStreamArn: str


class PinpointDestinationTypeDef(TypedDict):
    ApplicationArn: NotRequired[str]


class SnsDestinationTypeDef(TypedDict):
    TopicArn: str


class ExportJobSummaryTypeDef(TypedDict):
    JobId: NotRequired[str]
    ExportSourceType: NotRequired[ExportSourceTypeType]
    JobStatus: NotRequired[JobStatusType]
    CreatedTimestamp: NotRequired[datetime]
    CompletedTimestamp: NotRequired[datetime]


class ExportMetricTypeDef(TypedDict):
    Name: NotRequired[MetricType]
    Aggregation: NotRequired[MetricAggregationType]


class ExportStatisticsTypeDef(TypedDict):
    ProcessedRecordsCount: NotRequired[int]
    ExportedRecordsCount: NotRequired[int]


class FailureInfoTypeDef(TypedDict):
    FailedRecordsS3Url: NotRequired[str]
    ErrorMessage: NotRequired[str]


class SendQuotaTypeDef(TypedDict):
    Max24HourSend: NotRequired[float]
    MaxSendRate: NotRequired[float]
    SentLast24Hours: NotRequired[float]


class SuppressionAttributesTypeDef(TypedDict):
    SuppressedReasons: NotRequired[List[SuppressionListReasonType]]


class GetBlacklistReportsRequestRequestTypeDef(TypedDict):
    BlacklistItemNames: Sequence[str]


class GetConfigurationSetEventDestinationsRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str


class GetConfigurationSetRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str


class ReputationOptionsOutputTypeDef(TypedDict):
    ReputationMetricsEnabled: NotRequired[bool]
    LastFreshStart: NotRequired[datetime]


class SuppressionOptionsOutputTypeDef(TypedDict):
    SuppressedReasons: NotRequired[List[SuppressionListReasonType]]


class GetContactListRequestRequestTypeDef(TypedDict):
    ContactListName: str


class GetContactRequestRequestTypeDef(TypedDict):
    ContactListName: str
    EmailAddress: str


class GetCustomVerificationEmailTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str


class GetDedicatedIpPoolRequestRequestTypeDef(TypedDict):
    PoolName: str


class GetDedicatedIpRequestRequestTypeDef(TypedDict):
    Ip: str


class GetDedicatedIpsRequestRequestTypeDef(TypedDict):
    PoolName: NotRequired[str]
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]


class GetDeliverabilityTestReportRequestRequestTypeDef(TypedDict):
    ReportId: str


class PlacementStatisticsTypeDef(TypedDict):
    InboxPercentage: NotRequired[float]
    SpamPercentage: NotRequired[float]
    MissingPercentage: NotRequired[float]
    SpfPercentage: NotRequired[float]
    DkimPercentage: NotRequired[float]


class GetDomainDeliverabilityCampaignRequestRequestTypeDef(TypedDict):
    CampaignId: str


class GetEmailIdentityPoliciesRequestRequestTypeDef(TypedDict):
    EmailIdentity: str


class GetEmailIdentityRequestRequestTypeDef(TypedDict):
    EmailIdentity: str


class MailFromAttributesTypeDef(TypedDict):
    MailFromDomain: str
    MailFromDomainStatus: MailFromDomainStatusType
    BehaviorOnMxFailure: BehaviorOnMxFailureType


class GetEmailTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str


class GetExportJobRequestRequestTypeDef(TypedDict):
    JobId: str


class GetImportJobRequestRequestTypeDef(TypedDict):
    JobId: str


class GetMessageInsightsRequestRequestTypeDef(TypedDict):
    MessageId: str


class GetSuppressedDestinationRequestRequestTypeDef(TypedDict):
    EmailAddress: str


class GuardianAttributesTypeDef(TypedDict):
    OptimizedSharedDelivery: NotRequired[FeatureStatusType]


class GuardianOptionsTypeDef(TypedDict):
    OptimizedSharedDelivery: NotRequired[FeatureStatusType]


class IdentityInfoTypeDef(TypedDict):
    IdentityType: NotRequired[IdentityTypeType]
    IdentityName: NotRequired[str]
    SendingEnabled: NotRequired[bool]
    VerificationStatus: NotRequired[VerificationStatusType]


class SuppressionListDestinationTypeDef(TypedDict):
    SuppressionListImportAction: SuppressionListImportActionType


class InboxPlacementTrackingOptionTypeDef(TypedDict):
    Global: NotRequired[bool]
    TrackedIsps: NotRequired[Sequence[str]]


class ListConfigurationSetsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]


class ListContactListsRequestRequestTypeDef(TypedDict):
    PageSize: NotRequired[int]
    NextToken: NotRequired[str]


class TopicFilterTypeDef(TypedDict):
    TopicName: NotRequired[str]
    UseDefaultIfPreferenceUnavailable: NotRequired[bool]


class ListCustomVerificationEmailTemplatesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]


class ListDedicatedIpPoolsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]


class ListDeliverabilityTestReportsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]


class ListEmailIdentitiesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]


class ListEmailTemplatesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]


class ListExportJobsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]
    ExportSourceType: NotRequired[ExportSourceTypeType]
    JobStatus: NotRequired[JobStatusType]


class ListImportJobsRequestRequestTypeDef(TypedDict):
    ImportDestinationType: NotRequired[ImportDestinationTypeType]
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]


class ListManagementOptionsTypeDef(TypedDict):
    ContactListName: str
    TopicName: NotRequired[str]


class ListRecommendationsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[Mapping[ListRecommendationsFilterKeyType, str]]
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]


RecommendationTypeDef = TypedDict(
    "RecommendationTypeDef",
    {
        "ResourceArn": NotRequired[str],
        "Type": NotRequired[RecommendationTypeType],
        "Description": NotRequired[str],
        "Status": NotRequired[RecommendationStatusType],
        "CreatedTimestamp": NotRequired[datetime],
        "LastUpdatedTimestamp": NotRequired[datetime],
        "Impact": NotRequired[RecommendationImpactType],
    },
)


class SuppressedDestinationSummaryTypeDef(TypedDict):
    EmailAddress: str
    Reason: SuppressionListReasonType
    LastUpdateTime: datetime


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class MessageInsightsFiltersOutputTypeDef(TypedDict):
    FromEmailAddress: NotRequired[List[str]]
    Destination: NotRequired[List[str]]
    Subject: NotRequired[List[str]]
    Isp: NotRequired[List[str]]
    LastDeliveryEvent: NotRequired[List[DeliveryEventTypeType]]
    LastEngagementEvent: NotRequired[List[EngagementEventTypeType]]


class MessageInsightsFiltersTypeDef(TypedDict):
    FromEmailAddress: NotRequired[Sequence[str]]
    Destination: NotRequired[Sequence[str]]
    Subject: NotRequired[Sequence[str]]
    Isp: NotRequired[Sequence[str]]
    LastDeliveryEvent: NotRequired[Sequence[DeliveryEventTypeType]]
    LastEngagementEvent: NotRequired[Sequence[EngagementEventTypeType]]


class PutAccountDedicatedIpWarmupAttributesRequestRequestTypeDef(TypedDict):
    AutoWarmupEnabled: NotRequired[bool]


class PutAccountDetailsRequestRequestTypeDef(TypedDict):
    MailType: MailTypeType
    WebsiteURL: str
    ContactLanguage: NotRequired[ContactLanguageType]
    UseCaseDescription: NotRequired[str]
    AdditionalContactEmailAddresses: NotRequired[Sequence[str]]
    ProductionAccessEnabled: NotRequired[bool]


class PutAccountSendingAttributesRequestRequestTypeDef(TypedDict):
    SendingEnabled: NotRequired[bool]


class PutAccountSuppressionAttributesRequestRequestTypeDef(TypedDict):
    SuppressedReasons: NotRequired[Sequence[SuppressionListReasonType]]


class PutConfigurationSetDeliveryOptionsRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    TlsPolicy: NotRequired[TlsPolicyType]
    SendingPoolName: NotRequired[str]
    MaxDeliverySeconds: NotRequired[int]


class PutConfigurationSetReputationOptionsRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    ReputationMetricsEnabled: NotRequired[bool]


class PutConfigurationSetSendingOptionsRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    SendingEnabled: NotRequired[bool]


class PutConfigurationSetSuppressionOptionsRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    SuppressedReasons: NotRequired[Sequence[SuppressionListReasonType]]


class PutConfigurationSetTrackingOptionsRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    CustomRedirectDomain: NotRequired[str]
    HttpsPolicy: NotRequired[HttpsPolicyType]


class PutDedicatedIpInPoolRequestRequestTypeDef(TypedDict):
    Ip: str
    DestinationPoolName: str


class PutDedicatedIpPoolScalingAttributesRequestRequestTypeDef(TypedDict):
    PoolName: str
    ScalingMode: ScalingModeType


class PutDedicatedIpWarmupAttributesRequestRequestTypeDef(TypedDict):
    Ip: str
    WarmupPercentage: int


class PutEmailIdentityConfigurationSetAttributesRequestRequestTypeDef(TypedDict):
    EmailIdentity: str
    ConfigurationSetName: NotRequired[str]


class PutEmailIdentityDkimAttributesRequestRequestTypeDef(TypedDict):
    EmailIdentity: str
    SigningEnabled: NotRequired[bool]


class PutEmailIdentityFeedbackAttributesRequestRequestTypeDef(TypedDict):
    EmailIdentity: str
    EmailForwardingEnabled: NotRequired[bool]


class PutEmailIdentityMailFromAttributesRequestRequestTypeDef(TypedDict):
    EmailIdentity: str
    MailFromDomain: NotRequired[str]
    BehaviorOnMxFailure: NotRequired[BehaviorOnMxFailureType]


class PutSuppressedDestinationRequestRequestTypeDef(TypedDict):
    EmailAddress: str
    Reason: SuppressionListReasonType


class ReplacementTemplateTypeDef(TypedDict):
    ReplacementTemplateData: NotRequired[str]


class SOARecordTypeDef(TypedDict):
    PrimaryNameServer: NotRequired[str]
    AdminEmail: NotRequired[str]
    SerialNumber: NotRequired[int]


class SendCustomVerificationEmailRequestRequestTypeDef(TypedDict):
    EmailAddress: str
    TemplateName: str
    ConfigurationSetName: NotRequired[str]


class SuppressedDestinationAttributesTypeDef(TypedDict):
    MessageId: NotRequired[str]
    FeedbackId: NotRequired[str]


class TestRenderEmailTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    TemplateData: str


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateCustomVerificationEmailTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    FromEmailAddress: str
    TemplateSubject: str
    TemplateContent: str
    SuccessRedirectionURL: str
    FailureRedirectionURL: str


class UpdateEmailIdentityPolicyRequestRequestTypeDef(TypedDict):
    EmailIdentity: str
    PolicyName: str
    Policy: str


class AccountDetailsTypeDef(TypedDict):
    MailType: NotRequired[MailTypeType]
    WebsiteURL: NotRequired[str]
    ContactLanguage: NotRequired[ContactLanguageType]
    UseCaseDescription: NotRequired[str]
    AdditionalContactEmailAddresses: NotRequired[List[str]]
    ReviewDetails: NotRequired[ReviewDetailsTypeDef]


class BatchGetMetricDataQueryTypeDef(TypedDict):
    Id: str
    Namespace: Literal["VDM"]
    Metric: MetricType
    StartDate: TimestampTypeDef
    EndDate: TimestampTypeDef
    Dimensions: NotRequired[Mapping[MetricDimensionNameType, str]]


class GetDomainStatisticsReportRequestRequestTypeDef(TypedDict):
    Domain: str
    StartDate: TimestampTypeDef
    EndDate: TimestampTypeDef


class ListDomainDeliverabilityCampaignsRequestRequestTypeDef(TypedDict):
    StartDate: TimestampTypeDef
    EndDate: TimestampTypeDef
    SubscribedDomain: str
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]


class ListSuppressedDestinationsRequestRequestTypeDef(TypedDict):
    Reasons: NotRequired[Sequence[SuppressionListReasonType]]
    StartDate: NotRequired[TimestampTypeDef]
    EndDate: NotRequired[TimestampTypeDef]
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]


class ReputationOptionsTypeDef(TypedDict):
    ReputationMetricsEnabled: NotRequired[bool]
    LastFreshStart: NotRequired[TimestampTypeDef]


class BatchGetMetricDataResponseTypeDef(TypedDict):
    Results: List[MetricDataResultTypeDef]
    Errors: List[MetricDataErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDeliverabilityTestReportResponseTypeDef(TypedDict):
    ReportId: str
    DeliverabilityTestStatus: DeliverabilityTestStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateExportJobResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateImportJobResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetCustomVerificationEmailTemplateResponseTypeDef(TypedDict):
    TemplateName: str
    FromEmailAddress: str
    TemplateSubject: str
    TemplateContent: str
    SuccessRedirectionURL: str
    FailureRedirectionURL: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetEmailIdentityPoliciesResponseTypeDef(TypedDict):
    Policies: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListConfigurationSetsResponseTypeDef(TypedDict):
    ConfigurationSets: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListDedicatedIpPoolsResponseTypeDef(TypedDict):
    DedicatedIpPools: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PutEmailIdentityDkimSigningAttributesResponseTypeDef(TypedDict):
    DkimStatus: DkimStatusType
    DkimTokens: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class SendCustomVerificationEmailResponseTypeDef(TypedDict):
    MessageId: str
    ResponseMetadata: ResponseMetadataTypeDef


class SendEmailResponseTypeDef(TypedDict):
    MessageId: str
    ResponseMetadata: ResponseMetadataTypeDef


class TestRenderEmailTemplateResponseTypeDef(TypedDict):
    RenderedTemplate: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetBlacklistReportsResponseTypeDef(TypedDict):
    BlacklistReport: Dict[str, List[BlacklistEntryTypeDef]]
    ResponseMetadata: ResponseMetadataTypeDef


class RawMessageTypeDef(TypedDict):
    Data: BlobTypeDef


BodyTypeDef = TypedDict(
    "BodyTypeDef",
    {
        "Text": NotRequired[ContentTypeDef],
        "Html": NotRequired[ContentTypeDef],
    },
)


class SendBulkEmailResponseTypeDef(TypedDict):
    BulkEmailEntryResults: List[BulkEmailEntryResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CloudWatchDestinationOutputTypeDef(TypedDict):
    DimensionConfigurations: List[CloudWatchDimensionConfigurationTypeDef]


class CloudWatchDestinationTypeDef(TypedDict):
    DimensionConfigurations: Sequence[CloudWatchDimensionConfigurationTypeDef]


class EventDetailsTypeDef(TypedDict):
    Bounce: NotRequired[BounceTypeDef]
    Complaint: NotRequired[ComplaintTypeDef]


class ListContactListsResponseTypeDef(TypedDict):
    ContactLists: List[ContactListTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ContactTypeDef(TypedDict):
    EmailAddress: NotRequired[str]
    TopicPreferences: NotRequired[List[TopicPreferenceTypeDef]]
    TopicDefaultPreferences: NotRequired[List[TopicPreferenceTypeDef]]
    UnsubscribeAll: NotRequired[bool]
    LastUpdatedTimestamp: NotRequired[datetime]


class CreateContactRequestRequestTypeDef(TypedDict):
    ContactListName: str
    EmailAddress: str
    TopicPreferences: NotRequired[Sequence[TopicPreferenceTypeDef]]
    UnsubscribeAll: NotRequired[bool]
    AttributesData: NotRequired[str]


class GetContactResponseTypeDef(TypedDict):
    ContactListName: str
    EmailAddress: str
    TopicPreferences: List[TopicPreferenceTypeDef]
    TopicDefaultPreferences: List[TopicPreferenceTypeDef]
    UnsubscribeAll: bool
    AttributesData: str
    CreatedTimestamp: datetime
    LastUpdatedTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateContactRequestRequestTypeDef(TypedDict):
    ContactListName: str
    EmailAddress: str
    TopicPreferences: NotRequired[Sequence[TopicPreferenceTypeDef]]
    UnsubscribeAll: NotRequired[bool]
    AttributesData: NotRequired[str]


class CreateDedicatedIpPoolRequestRequestTypeDef(TypedDict):
    PoolName: str
    Tags: NotRequired[Sequence[TagTypeDef]]
    ScalingMode: NotRequired[ScalingModeType]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]


class CreateContactListRequestRequestTypeDef(TypedDict):
    ContactListName: str
    Topics: NotRequired[Sequence[TopicTypeDef]]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class GetContactListResponseTypeDef(TypedDict):
    ContactListName: str
    Topics: List[TopicTypeDef]
    Description: str
    CreatedTimestamp: datetime
    LastUpdatedTimestamp: datetime
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateContactListRequestRequestTypeDef(TypedDict):
    ContactListName: str
    Topics: NotRequired[Sequence[TopicTypeDef]]
    Description: NotRequired[str]


class CreateEmailIdentityRequestRequestTypeDef(TypedDict):
    EmailIdentity: str
    Tags: NotRequired[Sequence[TagTypeDef]]
    DkimSigningAttributes: NotRequired[DkimSigningAttributesTypeDef]
    ConfigurationSetName: NotRequired[str]


class PutEmailIdentityDkimSigningAttributesRequestRequestTypeDef(TypedDict):
    EmailIdentity: str
    SigningAttributesOrigin: DkimSigningAttributesOriginType
    SigningAttributes: NotRequired[DkimSigningAttributesTypeDef]


class CreateEmailIdentityResponseTypeDef(TypedDict):
    IdentityType: IdentityTypeType
    VerifiedForSendingStatus: bool
    DkimAttributes: DkimAttributesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEmailTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    TemplateContent: EmailTemplateContentTypeDef


class GetEmailTemplateResponseTypeDef(TypedDict):
    TemplateName: str
    TemplateContent: EmailTemplateContentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class TemplateTypeDef(TypedDict):
    TemplateName: NotRequired[str]
    TemplateArn: NotRequired[str]
    TemplateContent: NotRequired[EmailTemplateContentTypeDef]
    TemplateData: NotRequired[str]
    Headers: NotRequired[Sequence[MessageHeaderTypeDef]]


class UpdateEmailTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    TemplateContent: EmailTemplateContentTypeDef


class ListCustomVerificationEmailTemplatesResponseTypeDef(TypedDict):
    CustomVerificationEmailTemplates: List[CustomVerificationEmailTemplateMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DailyVolumeTypeDef(TypedDict):
    StartDate: NotRequired[datetime]
    VolumeStatistics: NotRequired[VolumeStatisticsTypeDef]
    DomainIspPlacements: NotRequired[List[DomainIspPlacementTypeDef]]


class OverallVolumeTypeDef(TypedDict):
    VolumeStatistics: NotRequired[VolumeStatisticsTypeDef]
    ReadRatePercent: NotRequired[float]
    DomainIspPlacements: NotRequired[List[DomainIspPlacementTypeDef]]


class GetDedicatedIpPoolResponseTypeDef(TypedDict):
    DedicatedIpPool: DedicatedIpPoolTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDedicatedIpResponseTypeDef(TypedDict):
    DedicatedIp: DedicatedIpTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDedicatedIpsResponseTypeDef(TypedDict):
    DedicatedIps: List[DedicatedIpTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListDeliverabilityTestReportsResponseTypeDef(TypedDict):
    DeliverabilityTestReports: List[DeliverabilityTestReportTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetDomainDeliverabilityCampaignResponseTypeDef(TypedDict):
    DomainDeliverabilityCampaign: DomainDeliverabilityCampaignTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDomainDeliverabilityCampaignsResponseTypeDef(TypedDict):
    DomainDeliverabilityCampaigns: List[DomainDeliverabilityCampaignTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DomainDeliverabilityTrackingOptionOutputTypeDef(TypedDict):
    Domain: NotRequired[str]
    SubscriptionStartDate: NotRequired[datetime]
    InboxPlacementTrackingOption: NotRequired[InboxPlacementTrackingOptionOutputTypeDef]


class ListEmailTemplatesResponseTypeDef(TypedDict):
    TemplatesMetadata: List[EmailTemplateMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListExportJobsResponseTypeDef(TypedDict):
    ExportJobs: List[ExportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class MetricsDataSourceOutputTypeDef(TypedDict):
    Dimensions: Dict[MetricDimensionNameType, List[str]]
    Namespace: Literal["VDM"]
    Metrics: List[ExportMetricTypeDef]
    StartDate: datetime
    EndDate: datetime


class MetricsDataSourceTypeDef(TypedDict):
    Dimensions: Mapping[MetricDimensionNameType, Sequence[str]]
    Namespace: Literal["VDM"]
    Metrics: Sequence[ExportMetricTypeDef]
    StartDate: TimestampTypeDef
    EndDate: TimestampTypeDef


class IspPlacementTypeDef(TypedDict):
    IspName: NotRequired[str]
    PlacementStatistics: NotRequired[PlacementStatisticsTypeDef]


class VdmAttributesTypeDef(TypedDict):
    VdmEnabled: FeatureStatusType
    DashboardAttributes: NotRequired[DashboardAttributesTypeDef]
    GuardianAttributes: NotRequired[GuardianAttributesTypeDef]


class VdmOptionsTypeDef(TypedDict):
    DashboardOptions: NotRequired[DashboardOptionsTypeDef]
    GuardianOptions: NotRequired[GuardianOptionsTypeDef]


class ListEmailIdentitiesResponseTypeDef(TypedDict):
    EmailIdentities: List[IdentityInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ImportDestinationTypeDef(TypedDict):
    SuppressionListDestination: NotRequired[SuppressionListDestinationTypeDef]
    ContactListDestination: NotRequired[ContactListDestinationTypeDef]


InboxPlacementTrackingOptionUnionTypeDef = Union[
    InboxPlacementTrackingOptionTypeDef, InboxPlacementTrackingOptionOutputTypeDef
]


class ListContactsFilterTypeDef(TypedDict):
    FilteredStatus: NotRequired[SubscriptionStatusType]
    TopicFilter: NotRequired[TopicFilterTypeDef]


class ListRecommendationsResponseTypeDef(TypedDict):
    Recommendations: List[RecommendationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListSuppressedDestinationsResponseTypeDef(TypedDict):
    SuppressedDestinationSummaries: List[SuppressedDestinationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class MessageInsightsDataSourceOutputTypeDef(TypedDict):
    StartDate: datetime
    EndDate: datetime
    Include: NotRequired[MessageInsightsFiltersOutputTypeDef]
    Exclude: NotRequired[MessageInsightsFiltersOutputTypeDef]
    MaxResults: NotRequired[int]


MessageInsightsFiltersUnionTypeDef = Union[
    MessageInsightsFiltersTypeDef, MessageInsightsFiltersOutputTypeDef
]


class ReplacementEmailContentTypeDef(TypedDict):
    ReplacementTemplate: NotRequired[ReplacementTemplateTypeDef]


class VerificationInfoTypeDef(TypedDict):
    LastCheckedTimestamp: NotRequired[datetime]
    LastSuccessTimestamp: NotRequired[datetime]
    ErrorType: NotRequired[VerificationErrorType]
    SOARecord: NotRequired[SOARecordTypeDef]


class SuppressedDestinationTypeDef(TypedDict):
    EmailAddress: str
    Reason: SuppressionListReasonType
    LastUpdateTime: datetime
    Attributes: NotRequired[SuppressedDestinationAttributesTypeDef]


class BatchGetMetricDataRequestRequestTypeDef(TypedDict):
    Queries: Sequence[BatchGetMetricDataQueryTypeDef]


class MessageTypeDef(TypedDict):
    Subject: ContentTypeDef
    Body: BodyTypeDef
    Headers: NotRequired[Sequence[MessageHeaderTypeDef]]


class EventDestinationTypeDef(TypedDict):
    Name: str
    MatchingEventTypes: List[EventTypeType]
    Enabled: NotRequired[bool]
    KinesisFirehoseDestination: NotRequired[KinesisFirehoseDestinationTypeDef]
    CloudWatchDestination: NotRequired[CloudWatchDestinationOutputTypeDef]
    SnsDestination: NotRequired[SnsDestinationTypeDef]
    EventBridgeDestination: NotRequired[EventBridgeDestinationTypeDef]
    PinpointDestination: NotRequired[PinpointDestinationTypeDef]


CloudWatchDestinationUnionTypeDef = Union[
    CloudWatchDestinationTypeDef, CloudWatchDestinationOutputTypeDef
]
InsightsEventTypeDef = TypedDict(
    "InsightsEventTypeDef",
    {
        "Timestamp": NotRequired[datetime],
        "Type": NotRequired[EventTypeType],
        "Details": NotRequired[EventDetailsTypeDef],
    },
)


class ListContactsResponseTypeDef(TypedDict):
    Contacts: List[ContactTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class BulkEmailContentTypeDef(TypedDict):
    Template: NotRequired[TemplateTypeDef]


class GetDomainStatisticsReportResponseTypeDef(TypedDict):
    OverallVolume: OverallVolumeTypeDef
    DailyVolumes: List[DailyVolumeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetDeliverabilityDashboardOptionsResponseTypeDef(TypedDict):
    DashboardEnabled: bool
    SubscriptionExpiryDate: datetime
    AccountStatus: DeliverabilityDashboardAccountStatusType
    ActiveSubscribedDomains: List[DomainDeliverabilityTrackingOptionOutputTypeDef]
    PendingExpirationSubscribedDomains: List[DomainDeliverabilityTrackingOptionOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


MetricsDataSourceUnionTypeDef = Union[MetricsDataSourceTypeDef, MetricsDataSourceOutputTypeDef]


class GetDeliverabilityTestReportResponseTypeDef(TypedDict):
    DeliverabilityTestReport: DeliverabilityTestReportTypeDef
    OverallPlacement: PlacementStatisticsTypeDef
    IspPlacements: List[IspPlacementTypeDef]
    Message: str
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetAccountResponseTypeDef(TypedDict):
    DedicatedIpAutoWarmupEnabled: bool
    EnforcementStatus: str
    ProductionAccessEnabled: bool
    SendQuota: SendQuotaTypeDef
    SendingEnabled: bool
    SuppressionAttributes: SuppressionAttributesTypeDef
    Details: AccountDetailsTypeDef
    VdmAttributes: VdmAttributesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutAccountVdmAttributesRequestRequestTypeDef(TypedDict):
    VdmAttributes: VdmAttributesTypeDef


class CreateConfigurationSetRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    TrackingOptions: NotRequired[TrackingOptionsTypeDef]
    DeliveryOptions: NotRequired[DeliveryOptionsTypeDef]
    ReputationOptions: NotRequired[ReputationOptionsTypeDef]
    SendingOptions: NotRequired[SendingOptionsTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    SuppressionOptions: NotRequired[SuppressionOptionsTypeDef]
    VdmOptions: NotRequired[VdmOptionsTypeDef]


class GetConfigurationSetResponseTypeDef(TypedDict):
    ConfigurationSetName: str
    TrackingOptions: TrackingOptionsTypeDef
    DeliveryOptions: DeliveryOptionsTypeDef
    ReputationOptions: ReputationOptionsOutputTypeDef
    SendingOptions: SendingOptionsTypeDef
    Tags: List[TagTypeDef]
    SuppressionOptions: SuppressionOptionsOutputTypeDef
    VdmOptions: VdmOptionsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutConfigurationSetVdmOptionsRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    VdmOptions: NotRequired[VdmOptionsTypeDef]


class CreateImportJobRequestRequestTypeDef(TypedDict):
    ImportDestination: ImportDestinationTypeDef
    ImportDataSource: ImportDataSourceTypeDef


class GetImportJobResponseTypeDef(TypedDict):
    JobId: str
    ImportDestination: ImportDestinationTypeDef
    ImportDataSource: ImportDataSourceTypeDef
    FailureInfo: FailureInfoTypeDef
    JobStatus: JobStatusType
    CreatedTimestamp: datetime
    CompletedTimestamp: datetime
    ProcessedRecordsCount: int
    FailedRecordsCount: int
    ResponseMetadata: ResponseMetadataTypeDef


class ImportJobSummaryTypeDef(TypedDict):
    JobId: NotRequired[str]
    ImportDestination: NotRequired[ImportDestinationTypeDef]
    JobStatus: NotRequired[JobStatusType]
    CreatedTimestamp: NotRequired[datetime]
    ProcessedRecordsCount: NotRequired[int]
    FailedRecordsCount: NotRequired[int]


class DomainDeliverabilityTrackingOptionTypeDef(TypedDict):
    Domain: NotRequired[str]
    SubscriptionStartDate: NotRequired[TimestampTypeDef]
    InboxPlacementTrackingOption: NotRequired[InboxPlacementTrackingOptionUnionTypeDef]


class ListContactsRequestRequestTypeDef(TypedDict):
    ContactListName: str
    Filter: NotRequired[ListContactsFilterTypeDef]
    PageSize: NotRequired[int]
    NextToken: NotRequired[str]


class ExportDataSourceOutputTypeDef(TypedDict):
    MetricsDataSource: NotRequired[MetricsDataSourceOutputTypeDef]
    MessageInsightsDataSource: NotRequired[MessageInsightsDataSourceOutputTypeDef]


class MessageInsightsDataSourceTypeDef(TypedDict):
    StartDate: TimestampTypeDef
    EndDate: TimestampTypeDef
    Include: NotRequired[MessageInsightsFiltersUnionTypeDef]
    Exclude: NotRequired[MessageInsightsFiltersUnionTypeDef]
    MaxResults: NotRequired[int]


class BulkEmailEntryTypeDef(TypedDict):
    Destination: DestinationTypeDef
    ReplacementTags: NotRequired[Sequence[MessageTagTypeDef]]
    ReplacementEmailContent: NotRequired[ReplacementEmailContentTypeDef]
    ReplacementHeaders: NotRequired[Sequence[MessageHeaderTypeDef]]


class GetEmailIdentityResponseTypeDef(TypedDict):
    IdentityType: IdentityTypeType
    FeedbackForwardingStatus: bool
    VerifiedForSendingStatus: bool
    DkimAttributes: DkimAttributesTypeDef
    MailFromAttributes: MailFromAttributesTypeDef
    Policies: Dict[str, str]
    Tags: List[TagTypeDef]
    ConfigurationSetName: str
    VerificationStatus: VerificationStatusType
    VerificationInfo: VerificationInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetSuppressedDestinationResponseTypeDef(TypedDict):
    SuppressedDestination: SuppressedDestinationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class EmailContentTypeDef(TypedDict):
    Simple: NotRequired[MessageTypeDef]
    Raw: NotRequired[RawMessageTypeDef]
    Template: NotRequired[TemplateTypeDef]


class GetConfigurationSetEventDestinationsResponseTypeDef(TypedDict):
    EventDestinations: List[EventDestinationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class EventDestinationDefinitionTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    MatchingEventTypes: NotRequired[Sequence[EventTypeType]]
    KinesisFirehoseDestination: NotRequired[KinesisFirehoseDestinationTypeDef]
    CloudWatchDestination: NotRequired[CloudWatchDestinationUnionTypeDef]
    SnsDestination: NotRequired[SnsDestinationTypeDef]
    EventBridgeDestination: NotRequired[EventBridgeDestinationTypeDef]
    PinpointDestination: NotRequired[PinpointDestinationTypeDef]


class EmailInsightsTypeDef(TypedDict):
    Destination: NotRequired[str]
    Isp: NotRequired[str]
    Events: NotRequired[List[InsightsEventTypeDef]]


class ListImportJobsResponseTypeDef(TypedDict):
    ImportJobs: List[ImportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


DomainDeliverabilityTrackingOptionUnionTypeDef = Union[
    DomainDeliverabilityTrackingOptionTypeDef, DomainDeliverabilityTrackingOptionOutputTypeDef
]


class GetExportJobResponseTypeDef(TypedDict):
    JobId: str
    ExportSourceType: ExportSourceTypeType
    JobStatus: JobStatusType
    ExportDestination: ExportDestinationTypeDef
    ExportDataSource: ExportDataSourceOutputTypeDef
    CreatedTimestamp: datetime
    CompletedTimestamp: datetime
    FailureInfo: FailureInfoTypeDef
    Statistics: ExportStatisticsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


MessageInsightsDataSourceUnionTypeDef = Union[
    MessageInsightsDataSourceTypeDef, MessageInsightsDataSourceOutputTypeDef
]


class SendBulkEmailRequestRequestTypeDef(TypedDict):
    DefaultContent: BulkEmailContentTypeDef
    BulkEmailEntries: Sequence[BulkEmailEntryTypeDef]
    FromEmailAddress: NotRequired[str]
    FromEmailAddressIdentityArn: NotRequired[str]
    ReplyToAddresses: NotRequired[Sequence[str]]
    FeedbackForwardingEmailAddress: NotRequired[str]
    FeedbackForwardingEmailAddressIdentityArn: NotRequired[str]
    DefaultEmailTags: NotRequired[Sequence[MessageTagTypeDef]]
    ConfigurationSetName: NotRequired[str]


class CreateDeliverabilityTestReportRequestRequestTypeDef(TypedDict):
    FromEmailAddress: str
    Content: EmailContentTypeDef
    ReportName: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class SendEmailRequestRequestTypeDef(TypedDict):
    Content: EmailContentTypeDef
    FromEmailAddress: NotRequired[str]
    FromEmailAddressIdentityArn: NotRequired[str]
    Destination: NotRequired[DestinationTypeDef]
    ReplyToAddresses: NotRequired[Sequence[str]]
    FeedbackForwardingEmailAddress: NotRequired[str]
    FeedbackForwardingEmailAddressIdentityArn: NotRequired[str]
    EmailTags: NotRequired[Sequence[MessageTagTypeDef]]
    ConfigurationSetName: NotRequired[str]
    ListManagementOptions: NotRequired[ListManagementOptionsTypeDef]


class CreateConfigurationSetEventDestinationRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    EventDestinationName: str
    EventDestination: EventDestinationDefinitionTypeDef


class UpdateConfigurationSetEventDestinationRequestRequestTypeDef(TypedDict):
    ConfigurationSetName: str
    EventDestinationName: str
    EventDestination: EventDestinationDefinitionTypeDef


class GetMessageInsightsResponseTypeDef(TypedDict):
    MessageId: str
    FromEmailAddress: str
    Subject: str
    EmailTags: List[MessageTagTypeDef]
    Insights: List[EmailInsightsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class PutDeliverabilityDashboardOptionRequestRequestTypeDef(TypedDict):
    DashboardEnabled: bool
    SubscribedDomains: NotRequired[Sequence[DomainDeliverabilityTrackingOptionUnionTypeDef]]


class ExportDataSourceTypeDef(TypedDict):
    MetricsDataSource: NotRequired[MetricsDataSourceUnionTypeDef]
    MessageInsightsDataSource: NotRequired[MessageInsightsDataSourceUnionTypeDef]


class CreateExportJobRequestRequestTypeDef(TypedDict):
    ExportDataSource: ExportDataSourceTypeDef
    ExportDestination: ExportDestinationTypeDef
