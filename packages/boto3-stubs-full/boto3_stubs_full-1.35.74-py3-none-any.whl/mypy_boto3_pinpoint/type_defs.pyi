"""
Type annotations for pinpoint service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/type_defs/)

Usage::

    ```python
    from mypy_boto3_pinpoint.type_defs import ADMChannelRequestTypeDef

    data: ADMChannelRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ActionType,
    AlignmentType,
    AttributeTypeType,
    ButtonActionType,
    CampaignStatusType,
    ChannelTypeType,
    DayOfWeekType,
    DeliveryStatusType,
    DimensionTypeType,
    DurationType,
    EndpointTypesElementType,
    FilterTypeType,
    FormatType,
    FrequencyType,
    IncludeType,
    JobStatusType,
    JourneyRunStatusType,
    LayoutType,
    MessageTypeType,
    ModeType,
    OperatorType,
    RecencyTypeType,
    SegmentTypeType,
    SourceTypeType,
    StateType,
    TemplateTypeType,
    TimezoneEstimationMethodsElementType,
    TypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ADMChannelRequestTypeDef",
    "ADMChannelResponseTypeDef",
    "ADMMessageTypeDef",
    "APNSChannelRequestTypeDef",
    "APNSChannelResponseTypeDef",
    "APNSMessageTypeDef",
    "APNSPushNotificationTemplateTypeDef",
    "APNSSandboxChannelRequestTypeDef",
    "APNSSandboxChannelResponseTypeDef",
    "APNSVoipChannelRequestTypeDef",
    "APNSVoipChannelResponseTypeDef",
    "APNSVoipSandboxChannelRequestTypeDef",
    "APNSVoipSandboxChannelResponseTypeDef",
    "ActivitiesResponseTypeDef",
    "ActivityOutputTypeDef",
    "ActivityResponseTypeDef",
    "ActivityTypeDef",
    "ActivityUnionTypeDef",
    "AddressConfigurationTypeDef",
    "AndroidPushNotificationTemplateTypeDef",
    "ApplicationDateRangeKpiResponseTypeDef",
    "ApplicationResponseTypeDef",
    "ApplicationSettingsJourneyLimitsTypeDef",
    "ApplicationSettingsResourceTypeDef",
    "ApplicationsResponseTypeDef",
    "AttributeDimensionOutputTypeDef",
    "AttributeDimensionTypeDef",
    "AttributeDimensionUnionTypeDef",
    "AttributesResourceTypeDef",
    "BaiduChannelRequestTypeDef",
    "BaiduChannelResponseTypeDef",
    "BaiduMessageTypeDef",
    "BaseKpiResultTypeDef",
    "BlobTypeDef",
    "CampaignCustomMessageTypeDef",
    "CampaignDateRangeKpiResponseTypeDef",
    "CampaignEmailMessageOutputTypeDef",
    "CampaignEmailMessageTypeDef",
    "CampaignEmailMessageUnionTypeDef",
    "CampaignEventFilterOutputTypeDef",
    "CampaignEventFilterTypeDef",
    "CampaignEventFilterUnionTypeDef",
    "CampaignHookTypeDef",
    "CampaignInAppMessageOutputTypeDef",
    "CampaignInAppMessageTypeDef",
    "CampaignInAppMessageUnionTypeDef",
    "CampaignLimitsTypeDef",
    "CampaignResponseTypeDef",
    "CampaignSmsMessageTypeDef",
    "CampaignStateTypeDef",
    "CampaignsResponseTypeDef",
    "ChannelResponseTypeDef",
    "ChannelsResponseTypeDef",
    "ClosedDaysOutputTypeDef",
    "ClosedDaysRuleTypeDef",
    "ClosedDaysTypeDef",
    "ClosedDaysUnionTypeDef",
    "ConditionOutputTypeDef",
    "ConditionTypeDef",
    "ConditionUnionTypeDef",
    "ConditionalSplitActivityOutputTypeDef",
    "ConditionalSplitActivityTypeDef",
    "ConditionalSplitActivityUnionTypeDef",
    "ContactCenterActivityTypeDef",
    "CreateAppRequestRequestTypeDef",
    "CreateAppResponseTypeDef",
    "CreateApplicationRequestTypeDef",
    "CreateCampaignRequestRequestTypeDef",
    "CreateCampaignResponseTypeDef",
    "CreateEmailTemplateRequestRequestTypeDef",
    "CreateEmailTemplateResponseTypeDef",
    "CreateExportJobRequestRequestTypeDef",
    "CreateExportJobResponseTypeDef",
    "CreateImportJobRequestRequestTypeDef",
    "CreateImportJobResponseTypeDef",
    "CreateInAppTemplateRequestRequestTypeDef",
    "CreateInAppTemplateResponseTypeDef",
    "CreateJourneyRequestRequestTypeDef",
    "CreateJourneyResponseTypeDef",
    "CreatePushTemplateRequestRequestTypeDef",
    "CreatePushTemplateResponseTypeDef",
    "CreateRecommenderConfigurationRequestRequestTypeDef",
    "CreateRecommenderConfigurationResponseTypeDef",
    "CreateRecommenderConfigurationTypeDef",
    "CreateSegmentRequestRequestTypeDef",
    "CreateSegmentResponseTypeDef",
    "CreateSmsTemplateRequestRequestTypeDef",
    "CreateSmsTemplateResponseTypeDef",
    "CreateTemplateMessageBodyTypeDef",
    "CreateVoiceTemplateRequestRequestTypeDef",
    "CreateVoiceTemplateResponseTypeDef",
    "CustomDeliveryConfigurationOutputTypeDef",
    "CustomDeliveryConfigurationTypeDef",
    "CustomDeliveryConfigurationUnionTypeDef",
    "CustomMessageActivityOutputTypeDef",
    "CustomMessageActivityTypeDef",
    "CustomMessageActivityUnionTypeDef",
    "DefaultButtonConfigurationTypeDef",
    "DefaultMessageTypeDef",
    "DefaultPushNotificationMessageTypeDef",
    "DefaultPushNotificationTemplateTypeDef",
    "DeleteAdmChannelRequestRequestTypeDef",
    "DeleteAdmChannelResponseTypeDef",
    "DeleteApnsChannelRequestRequestTypeDef",
    "DeleteApnsChannelResponseTypeDef",
    "DeleteApnsSandboxChannelRequestRequestTypeDef",
    "DeleteApnsSandboxChannelResponseTypeDef",
    "DeleteApnsVoipChannelRequestRequestTypeDef",
    "DeleteApnsVoipChannelResponseTypeDef",
    "DeleteApnsVoipSandboxChannelRequestRequestTypeDef",
    "DeleteApnsVoipSandboxChannelResponseTypeDef",
    "DeleteAppRequestRequestTypeDef",
    "DeleteAppResponseTypeDef",
    "DeleteBaiduChannelRequestRequestTypeDef",
    "DeleteBaiduChannelResponseTypeDef",
    "DeleteCampaignRequestRequestTypeDef",
    "DeleteCampaignResponseTypeDef",
    "DeleteEmailChannelRequestRequestTypeDef",
    "DeleteEmailChannelResponseTypeDef",
    "DeleteEmailTemplateRequestRequestTypeDef",
    "DeleteEmailTemplateResponseTypeDef",
    "DeleteEndpointRequestRequestTypeDef",
    "DeleteEndpointResponseTypeDef",
    "DeleteEventStreamRequestRequestTypeDef",
    "DeleteEventStreamResponseTypeDef",
    "DeleteGcmChannelRequestRequestTypeDef",
    "DeleteGcmChannelResponseTypeDef",
    "DeleteInAppTemplateRequestRequestTypeDef",
    "DeleteInAppTemplateResponseTypeDef",
    "DeleteJourneyRequestRequestTypeDef",
    "DeleteJourneyResponseTypeDef",
    "DeletePushTemplateRequestRequestTypeDef",
    "DeletePushTemplateResponseTypeDef",
    "DeleteRecommenderConfigurationRequestRequestTypeDef",
    "DeleteRecommenderConfigurationResponseTypeDef",
    "DeleteSegmentRequestRequestTypeDef",
    "DeleteSegmentResponseTypeDef",
    "DeleteSmsChannelRequestRequestTypeDef",
    "DeleteSmsChannelResponseTypeDef",
    "DeleteSmsTemplateRequestRequestTypeDef",
    "DeleteSmsTemplateResponseTypeDef",
    "DeleteUserEndpointsRequestRequestTypeDef",
    "DeleteUserEndpointsResponseTypeDef",
    "DeleteVoiceChannelRequestRequestTypeDef",
    "DeleteVoiceChannelResponseTypeDef",
    "DeleteVoiceTemplateRequestRequestTypeDef",
    "DeleteVoiceTemplateResponseTypeDef",
    "DirectMessageConfigurationTypeDef",
    "EmailChannelRequestTypeDef",
    "EmailChannelResponseTypeDef",
    "EmailMessageActivityTypeDef",
    "EmailMessageTypeDef",
    "EmailTemplateRequestTypeDef",
    "EmailTemplateResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EndpointBatchItemTypeDef",
    "EndpointBatchRequestTypeDef",
    "EndpointDemographicTypeDef",
    "EndpointItemResponseTypeDef",
    "EndpointLocationTypeDef",
    "EndpointMessageResultTypeDef",
    "EndpointRequestTypeDef",
    "EndpointResponseTypeDef",
    "EndpointSendConfigurationTypeDef",
    "EndpointUserOutputTypeDef",
    "EndpointUserTypeDef",
    "EndpointUserUnionTypeDef",
    "EndpointsResponseTypeDef",
    "EventConditionOutputTypeDef",
    "EventConditionTypeDef",
    "EventConditionUnionTypeDef",
    "EventDimensionsOutputTypeDef",
    "EventDimensionsTypeDef",
    "EventDimensionsUnionTypeDef",
    "EventFilterOutputTypeDef",
    "EventFilterTypeDef",
    "EventFilterUnionTypeDef",
    "EventItemResponseTypeDef",
    "EventStartConditionOutputTypeDef",
    "EventStartConditionTypeDef",
    "EventStartConditionUnionTypeDef",
    "EventStreamTypeDef",
    "EventTypeDef",
    "EventsBatchTypeDef",
    "EventsRequestTypeDef",
    "EventsResponseTypeDef",
    "ExportJobRequestTypeDef",
    "ExportJobResourceTypeDef",
    "ExportJobResponseTypeDef",
    "ExportJobsResponseTypeDef",
    "GCMChannelRequestTypeDef",
    "GCMChannelResponseTypeDef",
    "GCMMessageTypeDef",
    "GPSCoordinatesTypeDef",
    "GPSPointDimensionTypeDef",
    "GetAdmChannelRequestRequestTypeDef",
    "GetAdmChannelResponseTypeDef",
    "GetApnsChannelRequestRequestTypeDef",
    "GetApnsChannelResponseTypeDef",
    "GetApnsSandboxChannelRequestRequestTypeDef",
    "GetApnsSandboxChannelResponseTypeDef",
    "GetApnsVoipChannelRequestRequestTypeDef",
    "GetApnsVoipChannelResponseTypeDef",
    "GetApnsVoipSandboxChannelRequestRequestTypeDef",
    "GetApnsVoipSandboxChannelResponseTypeDef",
    "GetAppRequestRequestTypeDef",
    "GetAppResponseTypeDef",
    "GetApplicationDateRangeKpiRequestRequestTypeDef",
    "GetApplicationDateRangeKpiResponseTypeDef",
    "GetApplicationSettingsRequestRequestTypeDef",
    "GetApplicationSettingsResponseTypeDef",
    "GetAppsRequestRequestTypeDef",
    "GetAppsResponseTypeDef",
    "GetBaiduChannelRequestRequestTypeDef",
    "GetBaiduChannelResponseTypeDef",
    "GetCampaignActivitiesRequestRequestTypeDef",
    "GetCampaignActivitiesResponseTypeDef",
    "GetCampaignDateRangeKpiRequestRequestTypeDef",
    "GetCampaignDateRangeKpiResponseTypeDef",
    "GetCampaignRequestRequestTypeDef",
    "GetCampaignResponseTypeDef",
    "GetCampaignVersionRequestRequestTypeDef",
    "GetCampaignVersionResponseTypeDef",
    "GetCampaignVersionsRequestRequestTypeDef",
    "GetCampaignVersionsResponseTypeDef",
    "GetCampaignsRequestRequestTypeDef",
    "GetCampaignsResponseTypeDef",
    "GetChannelsRequestRequestTypeDef",
    "GetChannelsResponseTypeDef",
    "GetEmailChannelRequestRequestTypeDef",
    "GetEmailChannelResponseTypeDef",
    "GetEmailTemplateRequestRequestTypeDef",
    "GetEmailTemplateResponseTypeDef",
    "GetEndpointRequestRequestTypeDef",
    "GetEndpointResponseTypeDef",
    "GetEventStreamRequestRequestTypeDef",
    "GetEventStreamResponseTypeDef",
    "GetExportJobRequestRequestTypeDef",
    "GetExportJobResponseTypeDef",
    "GetExportJobsRequestRequestTypeDef",
    "GetExportJobsResponseTypeDef",
    "GetGcmChannelRequestRequestTypeDef",
    "GetGcmChannelResponseTypeDef",
    "GetImportJobRequestRequestTypeDef",
    "GetImportJobResponseTypeDef",
    "GetImportJobsRequestRequestTypeDef",
    "GetImportJobsResponseTypeDef",
    "GetInAppMessagesRequestRequestTypeDef",
    "GetInAppMessagesResponseTypeDef",
    "GetInAppTemplateRequestRequestTypeDef",
    "GetInAppTemplateResponseTypeDef",
    "GetJourneyDateRangeKpiRequestRequestTypeDef",
    "GetJourneyDateRangeKpiResponseTypeDef",
    "GetJourneyExecutionActivityMetricsRequestRequestTypeDef",
    "GetJourneyExecutionActivityMetricsResponseTypeDef",
    "GetJourneyExecutionMetricsRequestRequestTypeDef",
    "GetJourneyExecutionMetricsResponseTypeDef",
    "GetJourneyRequestRequestTypeDef",
    "GetJourneyResponseTypeDef",
    "GetJourneyRunExecutionActivityMetricsRequestRequestTypeDef",
    "GetJourneyRunExecutionActivityMetricsResponseTypeDef",
    "GetJourneyRunExecutionMetricsRequestRequestTypeDef",
    "GetJourneyRunExecutionMetricsResponseTypeDef",
    "GetJourneyRunsRequestRequestTypeDef",
    "GetJourneyRunsResponseTypeDef",
    "GetPushTemplateRequestRequestTypeDef",
    "GetPushTemplateResponseTypeDef",
    "GetRecommenderConfigurationRequestRequestTypeDef",
    "GetRecommenderConfigurationResponseTypeDef",
    "GetRecommenderConfigurationsRequestRequestTypeDef",
    "GetRecommenderConfigurationsResponseTypeDef",
    "GetSegmentExportJobsRequestRequestTypeDef",
    "GetSegmentExportJobsResponseTypeDef",
    "GetSegmentImportJobsRequestRequestTypeDef",
    "GetSegmentImportJobsResponseTypeDef",
    "GetSegmentRequestRequestTypeDef",
    "GetSegmentResponseTypeDef",
    "GetSegmentVersionRequestRequestTypeDef",
    "GetSegmentVersionResponseTypeDef",
    "GetSegmentVersionsRequestRequestTypeDef",
    "GetSegmentVersionsResponseTypeDef",
    "GetSegmentsRequestRequestTypeDef",
    "GetSegmentsResponseTypeDef",
    "GetSmsChannelRequestRequestTypeDef",
    "GetSmsChannelResponseTypeDef",
    "GetSmsTemplateRequestRequestTypeDef",
    "GetSmsTemplateResponseTypeDef",
    "GetUserEndpointsRequestRequestTypeDef",
    "GetUserEndpointsResponseTypeDef",
    "GetVoiceChannelRequestRequestTypeDef",
    "GetVoiceChannelResponseTypeDef",
    "GetVoiceTemplateRequestRequestTypeDef",
    "GetVoiceTemplateResponseTypeDef",
    "HoldoutActivityTypeDef",
    "ImportJobRequestTypeDef",
    "ImportJobResourceTypeDef",
    "ImportJobResponseTypeDef",
    "ImportJobsResponseTypeDef",
    "InAppCampaignScheduleTypeDef",
    "InAppMessageBodyConfigTypeDef",
    "InAppMessageButtonTypeDef",
    "InAppMessageCampaignTypeDef",
    "InAppMessageContentTypeDef",
    "InAppMessageHeaderConfigTypeDef",
    "InAppMessageTypeDef",
    "InAppMessagesResponseTypeDef",
    "InAppTemplateRequestTypeDef",
    "InAppTemplateResponseTypeDef",
    "ItemResponseTypeDef",
    "JourneyChannelSettingsTypeDef",
    "JourneyCustomMessageTypeDef",
    "JourneyDateRangeKpiResponseTypeDef",
    "JourneyEmailMessageTypeDef",
    "JourneyExecutionActivityMetricsResponseTypeDef",
    "JourneyExecutionMetricsResponseTypeDef",
    "JourneyLimitsTypeDef",
    "JourneyPushMessageTypeDef",
    "JourneyResponseTypeDef",
    "JourneyRunExecutionActivityMetricsResponseTypeDef",
    "JourneyRunExecutionMetricsResponseTypeDef",
    "JourneyRunResponseTypeDef",
    "JourneyRunsResponseTypeDef",
    "JourneySMSMessageTypeDef",
    "JourneyScheduleOutputTypeDef",
    "JourneyScheduleTypeDef",
    "JourneyScheduleUnionTypeDef",
    "JourneyStateRequestTypeDef",
    "JourneyTimeframeCapTypeDef",
    "JourneysResponseTypeDef",
    "ListJourneysRequestRequestTypeDef",
    "ListJourneysResponseTypeDef",
    "ListRecommenderConfigurationsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTemplateVersionsRequestRequestTypeDef",
    "ListTemplateVersionsResponseTypeDef",
    "ListTemplatesRequestRequestTypeDef",
    "ListTemplatesResponseTypeDef",
    "MessageBodyTypeDef",
    "MessageConfigurationOutputTypeDef",
    "MessageConfigurationTypeDef",
    "MessageConfigurationUnionTypeDef",
    "MessageHeaderTypeDef",
    "MessageRequestTypeDef",
    "MessageResponseTypeDef",
    "MessageResultTypeDef",
    "MessageTypeDef",
    "MetricDimensionTypeDef",
    "MultiConditionalBranchOutputTypeDef",
    "MultiConditionalBranchTypeDef",
    "MultiConditionalBranchUnionTypeDef",
    "MultiConditionalSplitActivityOutputTypeDef",
    "MultiConditionalSplitActivityTypeDef",
    "MultiConditionalSplitActivityUnionTypeDef",
    "NumberValidateRequestTypeDef",
    "NumberValidateResponseTypeDef",
    "OpenHoursOutputTypeDef",
    "OpenHoursRuleTypeDef",
    "OpenHoursTypeDef",
    "OpenHoursUnionTypeDef",
    "OverrideButtonConfigurationTypeDef",
    "PhoneNumberValidateRequestRequestTypeDef",
    "PhoneNumberValidateResponseTypeDef",
    "PublicEndpointTypeDef",
    "PushMessageActivityTypeDef",
    "PushNotificationTemplateRequestTypeDef",
    "PushNotificationTemplateResponseTypeDef",
    "PutEventStreamRequestRequestTypeDef",
    "PutEventStreamResponseTypeDef",
    "PutEventsRequestRequestTypeDef",
    "PutEventsResponseTypeDef",
    "QuietTimeTypeDef",
    "RandomSplitActivityOutputTypeDef",
    "RandomSplitActivityTypeDef",
    "RandomSplitActivityUnionTypeDef",
    "RandomSplitEntryTypeDef",
    "RawEmailTypeDef",
    "RecencyDimensionTypeDef",
    "RecommenderConfigurationResponseTypeDef",
    "RemoveAttributesRequestRequestTypeDef",
    "RemoveAttributesResponseTypeDef",
    "ResponseMetadataTypeDef",
    "ResultRowTypeDef",
    "ResultRowValueTypeDef",
    "SMSChannelRequestTypeDef",
    "SMSChannelResponseTypeDef",
    "SMSMessageActivityTypeDef",
    "SMSMessageTypeDef",
    "SMSTemplateRequestTypeDef",
    "SMSTemplateResponseTypeDef",
    "ScheduleOutputTypeDef",
    "ScheduleTypeDef",
    "ScheduleUnionTypeDef",
    "SegmentBehaviorsTypeDef",
    "SegmentConditionTypeDef",
    "SegmentDemographicsOutputTypeDef",
    "SegmentDemographicsTypeDef",
    "SegmentDemographicsUnionTypeDef",
    "SegmentDimensionsOutputTypeDef",
    "SegmentDimensionsTypeDef",
    "SegmentDimensionsUnionTypeDef",
    "SegmentGroupListOutputTypeDef",
    "SegmentGroupListTypeDef",
    "SegmentGroupListUnionTypeDef",
    "SegmentGroupOutputTypeDef",
    "SegmentGroupTypeDef",
    "SegmentGroupUnionTypeDef",
    "SegmentImportResourceTypeDef",
    "SegmentLocationOutputTypeDef",
    "SegmentLocationTypeDef",
    "SegmentLocationUnionTypeDef",
    "SegmentReferenceTypeDef",
    "SegmentResponseTypeDef",
    "SegmentsResponseTypeDef",
    "SendMessagesRequestRequestTypeDef",
    "SendMessagesResponseTypeDef",
    "SendOTPMessageRequestParametersTypeDef",
    "SendOTPMessageRequestRequestTypeDef",
    "SendOTPMessageResponseTypeDef",
    "SendUsersMessageRequestTypeDef",
    "SendUsersMessageResponseTypeDef",
    "SendUsersMessagesRequestRequestTypeDef",
    "SendUsersMessagesResponseTypeDef",
    "SessionTypeDef",
    "SetDimensionOutputTypeDef",
    "SetDimensionTypeDef",
    "SetDimensionUnionTypeDef",
    "SimpleConditionOutputTypeDef",
    "SimpleConditionTypeDef",
    "SimpleConditionUnionTypeDef",
    "SimpleEmailPartTypeDef",
    "SimpleEmailTypeDef",
    "StartConditionOutputTypeDef",
    "StartConditionTypeDef",
    "StartConditionUnionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagsModelOutputTypeDef",
    "TagsModelTypeDef",
    "TemplateActiveVersionRequestTypeDef",
    "TemplateConfigurationTypeDef",
    "TemplateCreateMessageBodyTypeDef",
    "TemplateResponseTypeDef",
    "TemplateTypeDef",
    "TemplateVersionResponseTypeDef",
    "TemplateVersionsResponseTypeDef",
    "TemplatesResponseTypeDef",
    "TimestampTypeDef",
    "TreatmentResourceTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAdmChannelRequestRequestTypeDef",
    "UpdateAdmChannelResponseTypeDef",
    "UpdateApnsChannelRequestRequestTypeDef",
    "UpdateApnsChannelResponseTypeDef",
    "UpdateApnsSandboxChannelRequestRequestTypeDef",
    "UpdateApnsSandboxChannelResponseTypeDef",
    "UpdateApnsVoipChannelRequestRequestTypeDef",
    "UpdateApnsVoipChannelResponseTypeDef",
    "UpdateApnsVoipSandboxChannelRequestRequestTypeDef",
    "UpdateApnsVoipSandboxChannelResponseTypeDef",
    "UpdateApplicationSettingsRequestRequestTypeDef",
    "UpdateApplicationSettingsResponseTypeDef",
    "UpdateAttributesRequestTypeDef",
    "UpdateBaiduChannelRequestRequestTypeDef",
    "UpdateBaiduChannelResponseTypeDef",
    "UpdateCampaignRequestRequestTypeDef",
    "UpdateCampaignResponseTypeDef",
    "UpdateEmailChannelRequestRequestTypeDef",
    "UpdateEmailChannelResponseTypeDef",
    "UpdateEmailTemplateRequestRequestTypeDef",
    "UpdateEmailTemplateResponseTypeDef",
    "UpdateEndpointRequestRequestTypeDef",
    "UpdateEndpointResponseTypeDef",
    "UpdateEndpointsBatchRequestRequestTypeDef",
    "UpdateEndpointsBatchResponseTypeDef",
    "UpdateGcmChannelRequestRequestTypeDef",
    "UpdateGcmChannelResponseTypeDef",
    "UpdateInAppTemplateRequestRequestTypeDef",
    "UpdateInAppTemplateResponseTypeDef",
    "UpdateJourneyRequestRequestTypeDef",
    "UpdateJourneyResponseTypeDef",
    "UpdateJourneyStateRequestRequestTypeDef",
    "UpdateJourneyStateResponseTypeDef",
    "UpdatePushTemplateRequestRequestTypeDef",
    "UpdatePushTemplateResponseTypeDef",
    "UpdateRecommenderConfigurationRequestRequestTypeDef",
    "UpdateRecommenderConfigurationResponseTypeDef",
    "UpdateRecommenderConfigurationTypeDef",
    "UpdateSegmentRequestRequestTypeDef",
    "UpdateSegmentResponseTypeDef",
    "UpdateSmsChannelRequestRequestTypeDef",
    "UpdateSmsChannelResponseTypeDef",
    "UpdateSmsTemplateRequestRequestTypeDef",
    "UpdateSmsTemplateResponseTypeDef",
    "UpdateTemplateActiveVersionRequestRequestTypeDef",
    "UpdateTemplateActiveVersionResponseTypeDef",
    "UpdateVoiceChannelRequestRequestTypeDef",
    "UpdateVoiceChannelResponseTypeDef",
    "UpdateVoiceTemplateRequestRequestTypeDef",
    "UpdateVoiceTemplateResponseTypeDef",
    "VerificationResponseTypeDef",
    "VerifyOTPMessageRequestParametersTypeDef",
    "VerifyOTPMessageRequestRequestTypeDef",
    "VerifyOTPMessageResponseTypeDef",
    "VoiceChannelRequestTypeDef",
    "VoiceChannelResponseTypeDef",
    "VoiceMessageTypeDef",
    "VoiceTemplateRequestTypeDef",
    "VoiceTemplateResponseTypeDef",
    "WaitActivityTypeDef",
    "WaitTimeTypeDef",
    "WriteApplicationSettingsRequestTypeDef",
    "WriteCampaignRequestTypeDef",
    "WriteEventStreamTypeDef",
    "WriteJourneyRequestTypeDef",
    "WriteSegmentRequestTypeDef",
    "WriteTreatmentResourceTypeDef",
)

class ADMChannelRequestTypeDef(TypedDict):
    ClientId: str
    ClientSecret: str
    Enabled: NotRequired[bool]

class ADMChannelResponseTypeDef(TypedDict):
    Platform: str
    ApplicationId: NotRequired[str]
    CreationDate: NotRequired[str]
    Enabled: NotRequired[bool]
    HasCredential: NotRequired[bool]
    Id: NotRequired[str]
    IsArchived: NotRequired[bool]
    LastModifiedBy: NotRequired[str]
    LastModifiedDate: NotRequired[str]
    Version: NotRequired[int]

class ADMMessageTypeDef(TypedDict):
    Action: NotRequired[ActionType]
    Body: NotRequired[str]
    ConsolidationKey: NotRequired[str]
    Data: NotRequired[Mapping[str, str]]
    ExpiresAfter: NotRequired[str]
    IconReference: NotRequired[str]
    ImageIconUrl: NotRequired[str]
    ImageUrl: NotRequired[str]
    MD5: NotRequired[str]
    RawContent: NotRequired[str]
    SilentPush: NotRequired[bool]
    SmallImageIconUrl: NotRequired[str]
    Sound: NotRequired[str]
    Substitutions: NotRequired[Mapping[str, Sequence[str]]]
    Title: NotRequired[str]
    Url: NotRequired[str]

class APNSChannelRequestTypeDef(TypedDict):
    BundleId: NotRequired[str]
    Certificate: NotRequired[str]
    DefaultAuthenticationMethod: NotRequired[str]
    Enabled: NotRequired[bool]
    PrivateKey: NotRequired[str]
    TeamId: NotRequired[str]
    TokenKey: NotRequired[str]
    TokenKeyId: NotRequired[str]

class APNSChannelResponseTypeDef(TypedDict):
    Platform: str
    ApplicationId: NotRequired[str]
    CreationDate: NotRequired[str]
    DefaultAuthenticationMethod: NotRequired[str]
    Enabled: NotRequired[bool]
    HasCredential: NotRequired[bool]
    HasTokenKey: NotRequired[bool]
    Id: NotRequired[str]
    IsArchived: NotRequired[bool]
    LastModifiedBy: NotRequired[str]
    LastModifiedDate: NotRequired[str]
    Version: NotRequired[int]

class APNSMessageTypeDef(TypedDict):
    APNSPushType: NotRequired[str]
    Action: NotRequired[ActionType]
    Badge: NotRequired[int]
    Body: NotRequired[str]
    Category: NotRequired[str]
    CollapseId: NotRequired[str]
    Data: NotRequired[Mapping[str, str]]
    MediaUrl: NotRequired[str]
    PreferredAuthenticationMethod: NotRequired[str]
    Priority: NotRequired[str]
    RawContent: NotRequired[str]
    SilentPush: NotRequired[bool]
    Sound: NotRequired[str]
    Substitutions: NotRequired[Mapping[str, Sequence[str]]]
    ThreadId: NotRequired[str]
    TimeToLive: NotRequired[int]
    Title: NotRequired[str]
    Url: NotRequired[str]

class APNSPushNotificationTemplateTypeDef(TypedDict):
    Action: NotRequired[ActionType]
    Body: NotRequired[str]
    MediaUrl: NotRequired[str]
    RawContent: NotRequired[str]
    Sound: NotRequired[str]
    Title: NotRequired[str]
    Url: NotRequired[str]

class APNSSandboxChannelRequestTypeDef(TypedDict):
    BundleId: NotRequired[str]
    Certificate: NotRequired[str]
    DefaultAuthenticationMethod: NotRequired[str]
    Enabled: NotRequired[bool]
    PrivateKey: NotRequired[str]
    TeamId: NotRequired[str]
    TokenKey: NotRequired[str]
    TokenKeyId: NotRequired[str]

class APNSSandboxChannelResponseTypeDef(TypedDict):
    Platform: str
    ApplicationId: NotRequired[str]
    CreationDate: NotRequired[str]
    DefaultAuthenticationMethod: NotRequired[str]
    Enabled: NotRequired[bool]
    HasCredential: NotRequired[bool]
    HasTokenKey: NotRequired[bool]
    Id: NotRequired[str]
    IsArchived: NotRequired[bool]
    LastModifiedBy: NotRequired[str]
    LastModifiedDate: NotRequired[str]
    Version: NotRequired[int]

class APNSVoipChannelRequestTypeDef(TypedDict):
    BundleId: NotRequired[str]
    Certificate: NotRequired[str]
    DefaultAuthenticationMethod: NotRequired[str]
    Enabled: NotRequired[bool]
    PrivateKey: NotRequired[str]
    TeamId: NotRequired[str]
    TokenKey: NotRequired[str]
    TokenKeyId: NotRequired[str]

class APNSVoipChannelResponseTypeDef(TypedDict):
    Platform: str
    ApplicationId: NotRequired[str]
    CreationDate: NotRequired[str]
    DefaultAuthenticationMethod: NotRequired[str]
    Enabled: NotRequired[bool]
    HasCredential: NotRequired[bool]
    HasTokenKey: NotRequired[bool]
    Id: NotRequired[str]
    IsArchived: NotRequired[bool]
    LastModifiedBy: NotRequired[str]
    LastModifiedDate: NotRequired[str]
    Version: NotRequired[int]

class APNSVoipSandboxChannelRequestTypeDef(TypedDict):
    BundleId: NotRequired[str]
    Certificate: NotRequired[str]
    DefaultAuthenticationMethod: NotRequired[str]
    Enabled: NotRequired[bool]
    PrivateKey: NotRequired[str]
    TeamId: NotRequired[str]
    TokenKey: NotRequired[str]
    TokenKeyId: NotRequired[str]

class APNSVoipSandboxChannelResponseTypeDef(TypedDict):
    Platform: str
    ApplicationId: NotRequired[str]
    CreationDate: NotRequired[str]
    DefaultAuthenticationMethod: NotRequired[str]
    Enabled: NotRequired[bool]
    HasCredential: NotRequired[bool]
    HasTokenKey: NotRequired[bool]
    Id: NotRequired[str]
    IsArchived: NotRequired[bool]
    LastModifiedBy: NotRequired[str]
    LastModifiedDate: NotRequired[str]
    Version: NotRequired[int]

class ActivityResponseTypeDef(TypedDict):
    ApplicationId: str
    CampaignId: str
    Id: str
    End: NotRequired[str]
    Result: NotRequired[str]
    ScheduledStart: NotRequired[str]
    Start: NotRequired[str]
    State: NotRequired[str]
    SuccessfulEndpointCount: NotRequired[int]
    TimezonesCompletedCount: NotRequired[int]
    TimezonesTotalCount: NotRequired[int]
    TotalEndpointCount: NotRequired[int]
    TreatmentId: NotRequired[str]
    ExecutionMetrics: NotRequired[Dict[str, str]]

class ContactCenterActivityTypeDef(TypedDict):
    NextActivity: NotRequired[str]

class HoldoutActivityTypeDef(TypedDict):
    Percentage: int
    NextActivity: NotRequired[str]

class AddressConfigurationTypeDef(TypedDict):
    BodyOverride: NotRequired[str]
    ChannelType: NotRequired[ChannelTypeType]
    Context: NotRequired[Mapping[str, str]]
    RawContent: NotRequired[str]
    Substitutions: NotRequired[Mapping[str, Sequence[str]]]
    TitleOverride: NotRequired[str]

class AndroidPushNotificationTemplateTypeDef(TypedDict):
    Action: NotRequired[ActionType]
    Body: NotRequired[str]
    ImageIconUrl: NotRequired[str]
    ImageUrl: NotRequired[str]
    RawContent: NotRequired[str]
    SmallImageIconUrl: NotRequired[str]
    Sound: NotRequired[str]
    Title: NotRequired[str]
    Url: NotRequired[str]

class ApplicationResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    Name: str
    tags: NotRequired[Dict[str, str]]
    CreationDate: NotRequired[str]

class JourneyTimeframeCapTypeDef(TypedDict):
    Cap: NotRequired[int]
    Days: NotRequired[int]

class CampaignHookTypeDef(TypedDict):
    LambdaFunctionName: NotRequired[str]
    Mode: NotRequired[ModeType]
    WebUrl: NotRequired[str]

class CampaignLimitsTypeDef(TypedDict):
    Daily: NotRequired[int]
    MaximumDuration: NotRequired[int]
    MessagesPerSecond: NotRequired[int]
    Total: NotRequired[int]
    Session: NotRequired[int]

class QuietTimeTypeDef(TypedDict):
    End: NotRequired[str]
    Start: NotRequired[str]

class AttributeDimensionOutputTypeDef(TypedDict):
    Values: List[str]
    AttributeType: NotRequired[AttributeTypeType]

class AttributeDimensionTypeDef(TypedDict):
    Values: Sequence[str]
    AttributeType: NotRequired[AttributeTypeType]

class AttributesResourceTypeDef(TypedDict):
    ApplicationId: str
    AttributeType: str
    Attributes: NotRequired[List[str]]

class BaiduChannelRequestTypeDef(TypedDict):
    ApiKey: str
    SecretKey: str
    Enabled: NotRequired[bool]

class BaiduChannelResponseTypeDef(TypedDict):
    Credential: str
    Platform: str
    ApplicationId: NotRequired[str]
    CreationDate: NotRequired[str]
    Enabled: NotRequired[bool]
    HasCredential: NotRequired[bool]
    Id: NotRequired[str]
    IsArchived: NotRequired[bool]
    LastModifiedBy: NotRequired[str]
    LastModifiedDate: NotRequired[str]
    Version: NotRequired[int]

class BaiduMessageTypeDef(TypedDict):
    Action: NotRequired[ActionType]
    Body: NotRequired[str]
    Data: NotRequired[Mapping[str, str]]
    IconReference: NotRequired[str]
    ImageIconUrl: NotRequired[str]
    ImageUrl: NotRequired[str]
    RawContent: NotRequired[str]
    SilentPush: NotRequired[bool]
    SmallImageIconUrl: NotRequired[str]
    Sound: NotRequired[str]
    Substitutions: NotRequired[Mapping[str, Sequence[str]]]
    TimeToLive: NotRequired[int]
    Title: NotRequired[str]
    Url: NotRequired[str]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class CampaignCustomMessageTypeDef(TypedDict):
    Data: NotRequired[str]

class MessageHeaderTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]

class CampaignStateTypeDef(TypedDict):
    CampaignStatus: NotRequired[CampaignStatusType]

class CustomDeliveryConfigurationOutputTypeDef(TypedDict):
    DeliveryUri: str
    EndpointTypes: NotRequired[List[EndpointTypesElementType]]

class CampaignSmsMessageTypeDef(TypedDict):
    Body: NotRequired[str]
    MessageType: NotRequired[MessageTypeType]
    OriginationNumber: NotRequired[str]
    SenderId: NotRequired[str]
    EntityId: NotRequired[str]
    TemplateId: NotRequired[str]

class ChannelResponseTypeDef(TypedDict):
    ApplicationId: NotRequired[str]
    CreationDate: NotRequired[str]
    Enabled: NotRequired[bool]
    HasCredential: NotRequired[bool]
    Id: NotRequired[str]
    IsArchived: NotRequired[bool]
    LastModifiedBy: NotRequired[str]
    LastModifiedDate: NotRequired[str]
    Version: NotRequired[int]

class ClosedDaysRuleTypeDef(TypedDict):
    Name: NotRequired[str]
    StartDateTime: NotRequired[str]
    EndDateTime: NotRequired[str]

class WaitTimeTypeDef(TypedDict):
    WaitFor: NotRequired[str]
    WaitUntil: NotRequired[str]

class CreateApplicationRequestTypeDef(TypedDict):
    Name: str
    tags: NotRequired[Mapping[str, str]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateTemplateMessageBodyTypeDef(TypedDict):
    Arn: NotRequired[str]
    Message: NotRequired[str]
    RequestID: NotRequired[str]

class ExportJobRequestTypeDef(TypedDict):
    RoleArn: str
    S3UrlPrefix: str
    SegmentId: NotRequired[str]
    SegmentVersion: NotRequired[int]

class ImportJobRequestTypeDef(TypedDict):
    Format: FormatType
    RoleArn: str
    S3Url: str
    DefineSegment: NotRequired[bool]
    ExternalId: NotRequired[str]
    RegisterEndpoints: NotRequired[bool]
    SegmentId: NotRequired[str]
    SegmentName: NotRequired[str]

class TemplateCreateMessageBodyTypeDef(TypedDict):
    Arn: NotRequired[str]
    Message: NotRequired[str]
    RequestID: NotRequired[str]

class CreateRecommenderConfigurationTypeDef(TypedDict):
    RecommendationProviderRoleArn: str
    RecommendationProviderUri: str
    Attributes: NotRequired[Mapping[str, str]]
    Description: NotRequired[str]
    Name: NotRequired[str]
    RecommendationProviderIdType: NotRequired[str]
    RecommendationTransformerUri: NotRequired[str]
    RecommendationsDisplayName: NotRequired[str]
    RecommendationsPerMessage: NotRequired[int]

class RecommenderConfigurationResponseTypeDef(TypedDict):
    CreationDate: str
    Id: str
    LastModifiedDate: str
    RecommendationProviderRoleArn: str
    RecommendationProviderUri: str
    Attributes: NotRequired[Dict[str, str]]
    Description: NotRequired[str]
    Name: NotRequired[str]
    RecommendationProviderIdType: NotRequired[str]
    RecommendationTransformerUri: NotRequired[str]
    RecommendationsDisplayName: NotRequired[str]
    RecommendationsPerMessage: NotRequired[int]

class SMSTemplateRequestTypeDef(TypedDict):
    Body: NotRequired[str]
    DefaultSubstitutions: NotRequired[str]
    RecommenderId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    TemplateDescription: NotRequired[str]

class VoiceTemplateRequestTypeDef(TypedDict):
    Body: NotRequired[str]
    DefaultSubstitutions: NotRequired[str]
    LanguageCode: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    TemplateDescription: NotRequired[str]
    VoiceId: NotRequired[str]

class CustomDeliveryConfigurationTypeDef(TypedDict):
    DeliveryUri: str
    EndpointTypes: NotRequired[Sequence[EndpointTypesElementType]]

class JourneyCustomMessageTypeDef(TypedDict):
    Data: NotRequired[str]

DefaultButtonConfigurationTypeDef = TypedDict(
    "DefaultButtonConfigurationTypeDef",
    {
        "ButtonAction": ButtonActionType,
        "Text": str,
        "BackgroundColor": NotRequired[str],
        "BorderRadius": NotRequired[int],
        "Link": NotRequired[str],
        "TextColor": NotRequired[str],
    },
)

class DefaultMessageTypeDef(TypedDict):
    Body: NotRequired[str]
    Substitutions: NotRequired[Mapping[str, Sequence[str]]]

class DefaultPushNotificationMessageTypeDef(TypedDict):
    Action: NotRequired[ActionType]
    Body: NotRequired[str]
    Data: NotRequired[Mapping[str, str]]
    SilentPush: NotRequired[bool]
    Substitutions: NotRequired[Mapping[str, Sequence[str]]]
    Title: NotRequired[str]
    Url: NotRequired[str]

class DefaultPushNotificationTemplateTypeDef(TypedDict):
    Action: NotRequired[ActionType]
    Body: NotRequired[str]
    Sound: NotRequired[str]
    Title: NotRequired[str]
    Url: NotRequired[str]

class DeleteAdmChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class DeleteApnsChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class DeleteApnsSandboxChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class DeleteApnsVoipChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class DeleteApnsVoipSandboxChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class DeleteAppRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class DeleteBaiduChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class DeleteCampaignRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    CampaignId: str

class DeleteEmailChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class EmailChannelResponseTypeDef(TypedDict):
    Platform: str
    ApplicationId: NotRequired[str]
    ConfigurationSet: NotRequired[str]
    CreationDate: NotRequired[str]
    Enabled: NotRequired[bool]
    FromAddress: NotRequired[str]
    HasCredential: NotRequired[bool]
    Id: NotRequired[str]
    Identity: NotRequired[str]
    IsArchived: NotRequired[bool]
    LastModifiedBy: NotRequired[str]
    LastModifiedDate: NotRequired[str]
    MessagesPerSecond: NotRequired[int]
    RoleArn: NotRequired[str]
    OrchestrationSendingRoleArn: NotRequired[str]
    Version: NotRequired[int]

class DeleteEmailTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    Version: NotRequired[str]

class MessageBodyTypeDef(TypedDict):
    Message: NotRequired[str]
    RequestID: NotRequired[str]

class DeleteEndpointRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    EndpointId: str

class DeleteEventStreamRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class EventStreamTypeDef(TypedDict):
    ApplicationId: str
    DestinationStreamArn: str
    RoleArn: str
    ExternalId: NotRequired[str]
    LastModifiedDate: NotRequired[str]
    LastUpdatedBy: NotRequired[str]

class DeleteGcmChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class GCMChannelResponseTypeDef(TypedDict):
    Platform: str
    ApplicationId: NotRequired[str]
    CreationDate: NotRequired[str]
    Credential: NotRequired[str]
    DefaultAuthenticationMethod: NotRequired[str]
    Enabled: NotRequired[bool]
    HasCredential: NotRequired[bool]
    HasFcmServiceCredentials: NotRequired[bool]
    Id: NotRequired[str]
    IsArchived: NotRequired[bool]
    LastModifiedBy: NotRequired[str]
    LastModifiedDate: NotRequired[str]
    Version: NotRequired[int]

class DeleteInAppTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    Version: NotRequired[str]

class DeleteJourneyRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    JourneyId: str

class DeletePushTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    Version: NotRequired[str]

class DeleteRecommenderConfigurationRequestRequestTypeDef(TypedDict):
    RecommenderId: str

class DeleteSegmentRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    SegmentId: str

class DeleteSmsChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class SMSChannelResponseTypeDef(TypedDict):
    Platform: str
    ApplicationId: NotRequired[str]
    CreationDate: NotRequired[str]
    Enabled: NotRequired[bool]
    HasCredential: NotRequired[bool]
    Id: NotRequired[str]
    IsArchived: NotRequired[bool]
    LastModifiedBy: NotRequired[str]
    LastModifiedDate: NotRequired[str]
    PromotionalMessagesPerSecond: NotRequired[int]
    SenderId: NotRequired[str]
    ShortCode: NotRequired[str]
    TransactionalMessagesPerSecond: NotRequired[int]
    Version: NotRequired[int]

class DeleteSmsTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    Version: NotRequired[str]

class DeleteUserEndpointsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    UserId: str

class DeleteVoiceChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class VoiceChannelResponseTypeDef(TypedDict):
    Platform: str
    ApplicationId: NotRequired[str]
    CreationDate: NotRequired[str]
    Enabled: NotRequired[bool]
    HasCredential: NotRequired[bool]
    Id: NotRequired[str]
    IsArchived: NotRequired[bool]
    LastModifiedBy: NotRequired[str]
    LastModifiedDate: NotRequired[str]
    Version: NotRequired[int]

class DeleteVoiceTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    Version: NotRequired[str]

class GCMMessageTypeDef(TypedDict):
    Action: NotRequired[ActionType]
    Body: NotRequired[str]
    CollapseKey: NotRequired[str]
    Data: NotRequired[Mapping[str, str]]
    IconReference: NotRequired[str]
    ImageIconUrl: NotRequired[str]
    ImageUrl: NotRequired[str]
    PreferredAuthenticationMethod: NotRequired[str]
    Priority: NotRequired[str]
    RawContent: NotRequired[str]
    RestrictedPackageName: NotRequired[str]
    SilentPush: NotRequired[bool]
    SmallImageIconUrl: NotRequired[str]
    Sound: NotRequired[str]
    Substitutions: NotRequired[Mapping[str, Sequence[str]]]
    TimeToLive: NotRequired[int]
    Title: NotRequired[str]
    Url: NotRequired[str]

class SMSMessageTypeDef(TypedDict):
    Body: NotRequired[str]
    Keyword: NotRequired[str]
    MediaUrl: NotRequired[str]
    MessageType: NotRequired[MessageTypeType]
    OriginationNumber: NotRequired[str]
    SenderId: NotRequired[str]
    Substitutions: NotRequired[Mapping[str, Sequence[str]]]
    EntityId: NotRequired[str]
    TemplateId: NotRequired[str]

class VoiceMessageTypeDef(TypedDict):
    Body: NotRequired[str]
    LanguageCode: NotRequired[str]
    OriginationNumber: NotRequired[str]
    Substitutions: NotRequired[Mapping[str, Sequence[str]]]
    VoiceId: NotRequired[str]

class EmailChannelRequestTypeDef(TypedDict):
    FromAddress: str
    Identity: str
    ConfigurationSet: NotRequired[str]
    Enabled: NotRequired[bool]
    RoleArn: NotRequired[str]
    OrchestrationSendingRoleArn: NotRequired[str]

class JourneyEmailMessageTypeDef(TypedDict):
    FromAddress: NotRequired[str]

class EndpointDemographicTypeDef(TypedDict):
    AppVersion: NotRequired[str]
    Locale: NotRequired[str]
    Make: NotRequired[str]
    Model: NotRequired[str]
    ModelVersion: NotRequired[str]
    Platform: NotRequired[str]
    PlatformVersion: NotRequired[str]
    Timezone: NotRequired[str]

class EndpointLocationTypeDef(TypedDict):
    City: NotRequired[str]
    Country: NotRequired[str]
    Latitude: NotRequired[float]
    Longitude: NotRequired[float]
    PostalCode: NotRequired[str]
    Region: NotRequired[str]

class EndpointItemResponseTypeDef(TypedDict):
    Message: NotRequired[str]
    StatusCode: NotRequired[int]

class EndpointMessageResultTypeDef(TypedDict):
    DeliveryStatus: DeliveryStatusType
    StatusCode: int
    Address: NotRequired[str]
    MessageId: NotRequired[str]
    StatusMessage: NotRequired[str]
    UpdatedToken: NotRequired[str]

class EndpointUserOutputTypeDef(TypedDict):
    UserAttributes: NotRequired[Dict[str, List[str]]]
    UserId: NotRequired[str]

class EndpointSendConfigurationTypeDef(TypedDict):
    BodyOverride: NotRequired[str]
    Context: NotRequired[Mapping[str, str]]
    RawContent: NotRequired[str]
    Substitutions: NotRequired[Mapping[str, Sequence[str]]]
    TitleOverride: NotRequired[str]

class EndpointUserTypeDef(TypedDict):
    UserAttributes: NotRequired[Mapping[str, Sequence[str]]]
    UserId: NotRequired[str]

class MetricDimensionTypeDef(TypedDict):
    ComparisonOperator: str
    Value: float

class SetDimensionOutputTypeDef(TypedDict):
    Values: List[str]
    DimensionType: NotRequired[DimensionTypeType]

class EventItemResponseTypeDef(TypedDict):
    Message: NotRequired[str]
    StatusCode: NotRequired[int]

class SessionTypeDef(TypedDict):
    Id: str
    StartTimestamp: str
    Duration: NotRequired[int]
    StopTimestamp: NotRequired[str]

class ExportJobResourceTypeDef(TypedDict):
    RoleArn: str
    S3UrlPrefix: str
    SegmentId: NotRequired[str]
    SegmentVersion: NotRequired[int]

class GCMChannelRequestTypeDef(TypedDict):
    ApiKey: NotRequired[str]
    DefaultAuthenticationMethod: NotRequired[str]
    Enabled: NotRequired[bool]
    ServiceJson: NotRequired[str]

class GPSCoordinatesTypeDef(TypedDict):
    Latitude: float
    Longitude: float

class GetAdmChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class GetApnsChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class GetApnsSandboxChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class GetApnsVoipChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class GetApnsVoipSandboxChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class GetAppRequestRequestTypeDef(TypedDict):
    ApplicationId: str

TimestampTypeDef = Union[datetime, str]

class GetApplicationSettingsRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class GetAppsRequestRequestTypeDef(TypedDict):
    PageSize: NotRequired[str]
    Token: NotRequired[str]

class GetBaiduChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class GetCampaignActivitiesRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    CampaignId: str
    PageSize: NotRequired[str]
    Token: NotRequired[str]

class GetCampaignRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    CampaignId: str

class GetCampaignVersionRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    CampaignId: str
    Version: str

class GetCampaignVersionsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    CampaignId: str
    PageSize: NotRequired[str]
    Token: NotRequired[str]

class GetCampaignsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    PageSize: NotRequired[str]
    Token: NotRequired[str]

class GetChannelsRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class GetEmailChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class GetEmailTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    Version: NotRequired[str]

class GetEndpointRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    EndpointId: str

class GetEventStreamRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class GetExportJobRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    JobId: str

class GetExportJobsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    PageSize: NotRequired[str]
    Token: NotRequired[str]

class GetGcmChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class GetImportJobRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    JobId: str

class GetImportJobsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    PageSize: NotRequired[str]
    Token: NotRequired[str]

class GetInAppMessagesRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    EndpointId: str

class GetInAppTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    Version: NotRequired[str]

class GetJourneyExecutionActivityMetricsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    JourneyActivityId: str
    JourneyId: str
    NextToken: NotRequired[str]
    PageSize: NotRequired[str]

class JourneyExecutionActivityMetricsResponseTypeDef(TypedDict):
    ActivityType: str
    ApplicationId: str
    JourneyActivityId: str
    JourneyId: str
    LastEvaluatedTime: str
    Metrics: Dict[str, str]

class GetJourneyExecutionMetricsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    JourneyId: str
    NextToken: NotRequired[str]
    PageSize: NotRequired[str]

class JourneyExecutionMetricsResponseTypeDef(TypedDict):
    ApplicationId: str
    JourneyId: str
    LastEvaluatedTime: str
    Metrics: Dict[str, str]

class GetJourneyRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    JourneyId: str

class GetJourneyRunExecutionActivityMetricsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    JourneyActivityId: str
    JourneyId: str
    RunId: str
    NextToken: NotRequired[str]
    PageSize: NotRequired[str]

class JourneyRunExecutionActivityMetricsResponseTypeDef(TypedDict):
    ActivityType: str
    ApplicationId: str
    JourneyActivityId: str
    JourneyId: str
    LastEvaluatedTime: str
    Metrics: Dict[str, str]
    RunId: str

class GetJourneyRunExecutionMetricsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    JourneyId: str
    RunId: str
    NextToken: NotRequired[str]
    PageSize: NotRequired[str]

class JourneyRunExecutionMetricsResponseTypeDef(TypedDict):
    ApplicationId: str
    JourneyId: str
    LastEvaluatedTime: str
    Metrics: Dict[str, str]
    RunId: str

class GetJourneyRunsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    JourneyId: str
    PageSize: NotRequired[str]
    Token: NotRequired[str]

class GetPushTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    Version: NotRequired[str]

class GetRecommenderConfigurationRequestRequestTypeDef(TypedDict):
    RecommenderId: str

class GetRecommenderConfigurationsRequestRequestTypeDef(TypedDict):
    PageSize: NotRequired[str]
    Token: NotRequired[str]

class GetSegmentExportJobsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    SegmentId: str
    PageSize: NotRequired[str]
    Token: NotRequired[str]

class GetSegmentImportJobsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    SegmentId: str
    PageSize: NotRequired[str]
    Token: NotRequired[str]

class GetSegmentRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    SegmentId: str

class GetSegmentVersionRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    SegmentId: str
    Version: str

class GetSegmentVersionsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    SegmentId: str
    PageSize: NotRequired[str]
    Token: NotRequired[str]

class GetSegmentsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    PageSize: NotRequired[str]
    Token: NotRequired[str]

class GetSmsChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class GetSmsTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    Version: NotRequired[str]

class SMSTemplateResponseTypeDef(TypedDict):
    CreationDate: str
    LastModifiedDate: str
    TemplateName: str
    TemplateType: TemplateTypeType
    Arn: NotRequired[str]
    Body: NotRequired[str]
    DefaultSubstitutions: NotRequired[str]
    RecommenderId: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    TemplateDescription: NotRequired[str]
    Version: NotRequired[str]

class GetUserEndpointsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    UserId: str

class GetVoiceChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class GetVoiceTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    Version: NotRequired[str]

class VoiceTemplateResponseTypeDef(TypedDict):
    CreationDate: str
    LastModifiedDate: str
    TemplateName: str
    TemplateType: TemplateTypeType
    Arn: NotRequired[str]
    Body: NotRequired[str]
    DefaultSubstitutions: NotRequired[str]
    LanguageCode: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    TemplateDescription: NotRequired[str]
    Version: NotRequired[str]
    VoiceId: NotRequired[str]

class ImportJobResourceTypeDef(TypedDict):
    Format: FormatType
    RoleArn: str
    S3Url: str
    DefineSegment: NotRequired[bool]
    ExternalId: NotRequired[str]
    RegisterEndpoints: NotRequired[bool]
    SegmentId: NotRequired[str]
    SegmentName: NotRequired[str]

class InAppMessageBodyConfigTypeDef(TypedDict):
    Alignment: AlignmentType
    Body: str
    TextColor: str

class OverrideButtonConfigurationTypeDef(TypedDict):
    ButtonAction: ButtonActionType
    Link: NotRequired[str]

class InAppMessageHeaderConfigTypeDef(TypedDict):
    Alignment: AlignmentType
    Header: str
    TextColor: str

class JourneyChannelSettingsTypeDef(TypedDict):
    ConnectCampaignArn: NotRequired[str]
    ConnectCampaignExecutionRoleArn: NotRequired[str]

class JourneyPushMessageTypeDef(TypedDict):
    TimeToLive: NotRequired[str]

class JourneyScheduleOutputTypeDef(TypedDict):
    EndTime: NotRequired[datetime]
    StartTime: NotRequired[datetime]
    Timezone: NotRequired[str]

class JourneyRunResponseTypeDef(TypedDict):
    CreationTime: str
    LastUpdateTime: str
    RunId: str
    Status: JourneyRunStatusType

class JourneySMSMessageTypeDef(TypedDict):
    MessageType: NotRequired[MessageTypeType]
    OriginationNumber: NotRequired[str]
    SenderId: NotRequired[str]
    EntityId: NotRequired[str]
    TemplateId: NotRequired[str]

class JourneyStateRequestTypeDef(TypedDict):
    State: NotRequired[StateType]

class ListJourneysRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    PageSize: NotRequired[str]
    Token: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class TagsModelOutputTypeDef(TypedDict):
    tags: Dict[str, str]

class ListTemplateVersionsRequestRequestTypeDef(TypedDict):
    TemplateName: str
    TemplateType: str
    NextToken: NotRequired[str]
    PageSize: NotRequired[str]

class ListTemplatesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    PageSize: NotRequired[str]
    Prefix: NotRequired[str]
    TemplateType: NotRequired[str]

class MessageTypeDef(TypedDict):
    Action: NotRequired[ActionType]
    Body: NotRequired[str]
    ImageIconUrl: NotRequired[str]
    ImageSmallIconUrl: NotRequired[str]
    ImageUrl: NotRequired[str]
    JsonBody: NotRequired[str]
    MediaUrl: NotRequired[str]
    RawContent: NotRequired[str]
    SilentPush: NotRequired[bool]
    TimeToLive: NotRequired[int]
    Title: NotRequired[str]
    Url: NotRequired[str]

class MessageResultTypeDef(TypedDict):
    DeliveryStatus: DeliveryStatusType
    StatusCode: int
    MessageId: NotRequired[str]
    StatusMessage: NotRequired[str]
    UpdatedToken: NotRequired[str]

class NumberValidateRequestTypeDef(TypedDict):
    IsoCountryCode: NotRequired[str]
    PhoneNumber: NotRequired[str]

class NumberValidateResponseTypeDef(TypedDict):
    Carrier: NotRequired[str]
    City: NotRequired[str]
    CleansedPhoneNumberE164: NotRequired[str]
    CleansedPhoneNumberNational: NotRequired[str]
    Country: NotRequired[str]
    CountryCodeIso2: NotRequired[str]
    CountryCodeNumeric: NotRequired[str]
    County: NotRequired[str]
    OriginalCountryCodeIso2: NotRequired[str]
    OriginalPhoneNumber: NotRequired[str]
    PhoneType: NotRequired[str]
    PhoneTypeCode: NotRequired[int]
    Timezone: NotRequired[str]
    ZipCode: NotRequired[str]

class OpenHoursRuleTypeDef(TypedDict):
    StartTime: NotRequired[str]
    EndTime: NotRequired[str]

class WriteEventStreamTypeDef(TypedDict):
    DestinationStreamArn: str
    RoleArn: str

class RandomSplitEntryTypeDef(TypedDict):
    NextActivity: NotRequired[str]
    Percentage: NotRequired[int]

class RecencyDimensionTypeDef(TypedDict):
    Duration: DurationType
    RecencyType: RecencyTypeType

class UpdateAttributesRequestTypeDef(TypedDict):
    Blacklist: NotRequired[Sequence[str]]

ResultRowValueTypeDef = TypedDict(
    "ResultRowValueTypeDef",
    {
        "Key": str,
        "Type": str,
        "Value": str,
    },
)

class SMSChannelRequestTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    SenderId: NotRequired[str]
    ShortCode: NotRequired[str]

class SegmentConditionTypeDef(TypedDict):
    SegmentId: str

class SegmentReferenceTypeDef(TypedDict):
    Id: str
    Version: NotRequired[int]

class SegmentImportResourceTypeDef(TypedDict):
    ExternalId: str
    Format: FormatType
    RoleArn: str
    S3Url: str
    Size: int
    ChannelCounts: NotRequired[Dict[str, int]]

class SendOTPMessageRequestParametersTypeDef(TypedDict):
    BrandName: str
    Channel: str
    DestinationIdentity: str
    OriginationIdentity: str
    ReferenceId: str
    AllowedAttempts: NotRequired[int]
    CodeLength: NotRequired[int]
    EntityId: NotRequired[str]
    Language: NotRequired[str]
    TemplateId: NotRequired[str]
    ValidityPeriod: NotRequired[int]

class SetDimensionTypeDef(TypedDict):
    Values: Sequence[str]
    DimensionType: NotRequired[DimensionTypeType]

class SimpleEmailPartTypeDef(TypedDict):
    Charset: NotRequired[str]
    Data: NotRequired[str]

class TagsModelTypeDef(TypedDict):
    tags: Mapping[str, str]

class TemplateActiveVersionRequestTypeDef(TypedDict):
    Version: NotRequired[str]

class TemplateTypeDef(TypedDict):
    Name: NotRequired[str]
    Version: NotRequired[str]

class TemplateResponseTypeDef(TypedDict):
    CreationDate: str
    LastModifiedDate: str
    TemplateName: str
    TemplateType: TemplateTypeType
    Arn: NotRequired[str]
    DefaultSubstitutions: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    TemplateDescription: NotRequired[str]
    Version: NotRequired[str]

class TemplateVersionResponseTypeDef(TypedDict):
    CreationDate: str
    LastModifiedDate: str
    TemplateName: str
    TemplateType: str
    DefaultSubstitutions: NotRequired[str]
    TemplateDescription: NotRequired[str]
    Version: NotRequired[str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateRecommenderConfigurationTypeDef(TypedDict):
    RecommendationProviderRoleArn: str
    RecommendationProviderUri: str
    Attributes: NotRequired[Mapping[str, str]]
    Description: NotRequired[str]
    Name: NotRequired[str]
    RecommendationProviderIdType: NotRequired[str]
    RecommendationTransformerUri: NotRequired[str]
    RecommendationsDisplayName: NotRequired[str]
    RecommendationsPerMessage: NotRequired[int]

class VoiceChannelRequestTypeDef(TypedDict):
    Enabled: NotRequired[bool]

class VerificationResponseTypeDef(TypedDict):
    Valid: NotRequired[bool]

class VerifyOTPMessageRequestParametersTypeDef(TypedDict):
    DestinationIdentity: str
    Otp: str
    ReferenceId: str

class UpdateAdmChannelRequestRequestTypeDef(TypedDict):
    ADMChannelRequest: ADMChannelRequestTypeDef
    ApplicationId: str

class UpdateApnsChannelRequestRequestTypeDef(TypedDict):
    APNSChannelRequest: APNSChannelRequestTypeDef
    ApplicationId: str

class UpdateApnsSandboxChannelRequestRequestTypeDef(TypedDict):
    APNSSandboxChannelRequest: APNSSandboxChannelRequestTypeDef
    ApplicationId: str

class UpdateApnsVoipChannelRequestRequestTypeDef(TypedDict):
    APNSVoipChannelRequest: APNSVoipChannelRequestTypeDef
    ApplicationId: str

class UpdateApnsVoipSandboxChannelRequestRequestTypeDef(TypedDict):
    APNSVoipSandboxChannelRequest: APNSVoipSandboxChannelRequestTypeDef
    ApplicationId: str

class ActivitiesResponseTypeDef(TypedDict):
    Item: List[ActivityResponseTypeDef]
    NextToken: NotRequired[str]

class ApplicationsResponseTypeDef(TypedDict):
    Item: NotRequired[List[ApplicationResponseTypeDef]]
    NextToken: NotRequired[str]

class ApplicationSettingsJourneyLimitsTypeDef(TypedDict):
    DailyCap: NotRequired[int]
    TimeframeCap: NotRequired[JourneyTimeframeCapTypeDef]
    TotalCap: NotRequired[int]

class JourneyLimitsTypeDef(TypedDict):
    DailyCap: NotRequired[int]
    EndpointReentryCap: NotRequired[int]
    MessagesPerSecond: NotRequired[int]
    EndpointReentryInterval: NotRequired[str]
    TimeframeCap: NotRequired[JourneyTimeframeCapTypeDef]
    TotalCap: NotRequired[int]

AttributeDimensionUnionTypeDef = Union[AttributeDimensionTypeDef, AttributeDimensionOutputTypeDef]

class UpdateBaiduChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    BaiduChannelRequest: BaiduChannelRequestTypeDef

class RawEmailTypeDef(TypedDict):
    Data: NotRequired[BlobTypeDef]

class CampaignEmailMessageOutputTypeDef(TypedDict):
    Body: NotRequired[str]
    FromAddress: NotRequired[str]
    Headers: NotRequired[List[MessageHeaderTypeDef]]
    HtmlBody: NotRequired[str]
    Title: NotRequired[str]

class CampaignEmailMessageTypeDef(TypedDict):
    Body: NotRequired[str]
    FromAddress: NotRequired[str]
    Headers: NotRequired[Sequence[MessageHeaderTypeDef]]
    HtmlBody: NotRequired[str]
    Title: NotRequired[str]

class EmailTemplateRequestTypeDef(TypedDict):
    DefaultSubstitutions: NotRequired[str]
    HtmlPart: NotRequired[str]
    RecommenderId: NotRequired[str]
    Subject: NotRequired[str]
    Headers: NotRequired[Sequence[MessageHeaderTypeDef]]
    tags: NotRequired[Mapping[str, str]]
    TemplateDescription: NotRequired[str]
    TextPart: NotRequired[str]

class EmailTemplateResponseTypeDef(TypedDict):
    CreationDate: str
    LastModifiedDate: str
    TemplateName: str
    TemplateType: TemplateTypeType
    Arn: NotRequired[str]
    DefaultSubstitutions: NotRequired[str]
    HtmlPart: NotRequired[str]
    RecommenderId: NotRequired[str]
    Subject: NotRequired[str]
    Headers: NotRequired[List[MessageHeaderTypeDef]]
    tags: NotRequired[Dict[str, str]]
    TemplateDescription: NotRequired[str]
    TextPart: NotRequired[str]
    Version: NotRequired[str]

class ChannelsResponseTypeDef(TypedDict):
    Channels: Dict[str, ChannelResponseTypeDef]

class ClosedDaysOutputTypeDef(TypedDict):
    EMAIL: NotRequired[List[ClosedDaysRuleTypeDef]]
    SMS: NotRequired[List[ClosedDaysRuleTypeDef]]
    PUSH: NotRequired[List[ClosedDaysRuleTypeDef]]
    VOICE: NotRequired[List[ClosedDaysRuleTypeDef]]
    CUSTOM: NotRequired[List[ClosedDaysRuleTypeDef]]

class ClosedDaysTypeDef(TypedDict):
    EMAIL: NotRequired[Sequence[ClosedDaysRuleTypeDef]]
    SMS: NotRequired[Sequence[ClosedDaysRuleTypeDef]]
    PUSH: NotRequired[Sequence[ClosedDaysRuleTypeDef]]
    VOICE: NotRequired[Sequence[ClosedDaysRuleTypeDef]]
    CUSTOM: NotRequired[Sequence[ClosedDaysRuleTypeDef]]

class WaitActivityTypeDef(TypedDict):
    NextActivity: NotRequired[str]
    WaitTime: NotRequired[WaitTimeTypeDef]

class CreateAppRequestRequestTypeDef(TypedDict):
    CreateApplicationRequest: CreateApplicationRequestTypeDef

class CreateAppResponseTypeDef(TypedDict):
    ApplicationResponse: ApplicationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAdmChannelResponseTypeDef(TypedDict):
    ADMChannelResponse: ADMChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteApnsChannelResponseTypeDef(TypedDict):
    APNSChannelResponse: APNSChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteApnsSandboxChannelResponseTypeDef(TypedDict):
    APNSSandboxChannelResponse: APNSSandboxChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteApnsVoipChannelResponseTypeDef(TypedDict):
    APNSVoipChannelResponse: APNSVoipChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteApnsVoipSandboxChannelResponseTypeDef(TypedDict):
    APNSVoipSandboxChannelResponse: APNSVoipSandboxChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAppResponseTypeDef(TypedDict):
    ApplicationResponse: ApplicationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBaiduChannelResponseTypeDef(TypedDict):
    BaiduChannelResponse: BaiduChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetAdmChannelResponseTypeDef(TypedDict):
    ADMChannelResponse: ADMChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetApnsChannelResponseTypeDef(TypedDict):
    APNSChannelResponse: APNSChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetApnsSandboxChannelResponseTypeDef(TypedDict):
    APNSSandboxChannelResponse: APNSSandboxChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetApnsVoipChannelResponseTypeDef(TypedDict):
    APNSVoipChannelResponse: APNSVoipChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetApnsVoipSandboxChannelResponseTypeDef(TypedDict):
    APNSVoipSandboxChannelResponse: APNSVoipSandboxChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAppResponseTypeDef(TypedDict):
    ApplicationResponse: ApplicationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetBaiduChannelResponseTypeDef(TypedDict):
    BaiduChannelResponse: BaiduChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class RemoveAttributesResponseTypeDef(TypedDict):
    AttributesResource: AttributesResourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAdmChannelResponseTypeDef(TypedDict):
    ADMChannelResponse: ADMChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateApnsChannelResponseTypeDef(TypedDict):
    APNSChannelResponse: APNSChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateApnsSandboxChannelResponseTypeDef(TypedDict):
    APNSSandboxChannelResponse: APNSSandboxChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateApnsVoipChannelResponseTypeDef(TypedDict):
    APNSVoipChannelResponse: APNSVoipChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateApnsVoipSandboxChannelResponseTypeDef(TypedDict):
    APNSVoipSandboxChannelResponse: APNSVoipSandboxChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBaiduChannelResponseTypeDef(TypedDict):
    BaiduChannelResponse: BaiduChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEmailTemplateResponseTypeDef(TypedDict):
    CreateTemplateMessageBody: CreateTemplateMessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePushTemplateResponseTypeDef(TypedDict):
    CreateTemplateMessageBody: CreateTemplateMessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSmsTemplateResponseTypeDef(TypedDict):
    CreateTemplateMessageBody: CreateTemplateMessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateVoiceTemplateResponseTypeDef(TypedDict):
    CreateTemplateMessageBody: CreateTemplateMessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateExportJobRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    ExportJobRequest: ExportJobRequestTypeDef

class CreateImportJobRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    ImportJobRequest: ImportJobRequestTypeDef

class CreateInAppTemplateResponseTypeDef(TypedDict):
    TemplateCreateMessageBody: TemplateCreateMessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRecommenderConfigurationRequestRequestTypeDef(TypedDict):
    CreateRecommenderConfiguration: CreateRecommenderConfigurationTypeDef

class CreateRecommenderConfigurationResponseTypeDef(TypedDict):
    RecommenderConfigurationResponse: RecommenderConfigurationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteRecommenderConfigurationResponseTypeDef(TypedDict):
    RecommenderConfigurationResponse: RecommenderConfigurationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetRecommenderConfigurationResponseTypeDef(TypedDict):
    RecommenderConfigurationResponse: RecommenderConfigurationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListRecommenderConfigurationsResponseTypeDef(TypedDict):
    Item: List[RecommenderConfigurationResponseTypeDef]
    NextToken: NotRequired[str]

class UpdateRecommenderConfigurationResponseTypeDef(TypedDict):
    RecommenderConfigurationResponse: RecommenderConfigurationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSmsTemplateRequestRequestTypeDef(TypedDict):
    SMSTemplateRequest: SMSTemplateRequestTypeDef
    TemplateName: str

class UpdateSmsTemplateRequestRequestTypeDef(TypedDict):
    SMSTemplateRequest: SMSTemplateRequestTypeDef
    TemplateName: str
    CreateNewVersion: NotRequired[bool]
    Version: NotRequired[str]

class CreateVoiceTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    VoiceTemplateRequest: VoiceTemplateRequestTypeDef

class UpdateVoiceTemplateRequestRequestTypeDef(TypedDict):
    TemplateName: str
    VoiceTemplateRequest: VoiceTemplateRequestTypeDef
    CreateNewVersion: NotRequired[bool]
    Version: NotRequired[str]

CustomDeliveryConfigurationUnionTypeDef = Union[
    CustomDeliveryConfigurationTypeDef, CustomDeliveryConfigurationOutputTypeDef
]

class CustomMessageActivityOutputTypeDef(TypedDict):
    DeliveryUri: NotRequired[str]
    EndpointTypes: NotRequired[List[EndpointTypesElementType]]
    MessageConfig: NotRequired[JourneyCustomMessageTypeDef]
    NextActivity: NotRequired[str]
    TemplateName: NotRequired[str]
    TemplateVersion: NotRequired[str]

class CustomMessageActivityTypeDef(TypedDict):
    DeliveryUri: NotRequired[str]
    EndpointTypes: NotRequired[Sequence[EndpointTypesElementType]]
    MessageConfig: NotRequired[JourneyCustomMessageTypeDef]
    NextActivity: NotRequired[str]
    TemplateName: NotRequired[str]
    TemplateVersion: NotRequired[str]

class PushNotificationTemplateRequestTypeDef(TypedDict):
    ADM: NotRequired[AndroidPushNotificationTemplateTypeDef]
    APNS: NotRequired[APNSPushNotificationTemplateTypeDef]
    Baidu: NotRequired[AndroidPushNotificationTemplateTypeDef]
    Default: NotRequired[DefaultPushNotificationTemplateTypeDef]
    DefaultSubstitutions: NotRequired[str]
    GCM: NotRequired[AndroidPushNotificationTemplateTypeDef]
    RecommenderId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    TemplateDescription: NotRequired[str]

class PushNotificationTemplateResponseTypeDef(TypedDict):
    CreationDate: str
    LastModifiedDate: str
    TemplateName: str
    TemplateType: TemplateTypeType
    ADM: NotRequired[AndroidPushNotificationTemplateTypeDef]
    APNS: NotRequired[APNSPushNotificationTemplateTypeDef]
    Arn: NotRequired[str]
    Baidu: NotRequired[AndroidPushNotificationTemplateTypeDef]
    Default: NotRequired[DefaultPushNotificationTemplateTypeDef]
    DefaultSubstitutions: NotRequired[str]
    GCM: NotRequired[AndroidPushNotificationTemplateTypeDef]
    RecommenderId: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    TemplateDescription: NotRequired[str]
    Version: NotRequired[str]

class DeleteEmailChannelResponseTypeDef(TypedDict):
    EmailChannelResponse: EmailChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetEmailChannelResponseTypeDef(TypedDict):
    EmailChannelResponse: EmailChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEmailChannelResponseTypeDef(TypedDict):
    EmailChannelResponse: EmailChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteEmailTemplateResponseTypeDef(TypedDict):
    MessageBody: MessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteInAppTemplateResponseTypeDef(TypedDict):
    MessageBody: MessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeletePushTemplateResponseTypeDef(TypedDict):
    MessageBody: MessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteSmsTemplateResponseTypeDef(TypedDict):
    MessageBody: MessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteVoiceTemplateResponseTypeDef(TypedDict):
    MessageBody: MessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEmailTemplateResponseTypeDef(TypedDict):
    MessageBody: MessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEndpointResponseTypeDef(TypedDict):
    MessageBody: MessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEndpointsBatchResponseTypeDef(TypedDict):
    MessageBody: MessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateInAppTemplateResponseTypeDef(TypedDict):
    MessageBody: MessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePushTemplateResponseTypeDef(TypedDict):
    MessageBody: MessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSmsTemplateResponseTypeDef(TypedDict):
    MessageBody: MessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTemplateActiveVersionResponseTypeDef(TypedDict):
    MessageBody: MessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateVoiceTemplateResponseTypeDef(TypedDict):
    MessageBody: MessageBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteEventStreamResponseTypeDef(TypedDict):
    EventStream: EventStreamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetEventStreamResponseTypeDef(TypedDict):
    EventStream: EventStreamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutEventStreamResponseTypeDef(TypedDict):
    EventStream: EventStreamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteGcmChannelResponseTypeDef(TypedDict):
    GCMChannelResponse: GCMChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetGcmChannelResponseTypeDef(TypedDict):
    GCMChannelResponse: GCMChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGcmChannelResponseTypeDef(TypedDict):
    GCMChannelResponse: GCMChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteSmsChannelResponseTypeDef(TypedDict):
    SMSChannelResponse: SMSChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSmsChannelResponseTypeDef(TypedDict):
    SMSChannelResponse: SMSChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSmsChannelResponseTypeDef(TypedDict):
    SMSChannelResponse: SMSChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteVoiceChannelResponseTypeDef(TypedDict):
    VoiceChannelResponse: VoiceChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceChannelResponseTypeDef(TypedDict):
    VoiceChannelResponse: VoiceChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateVoiceChannelResponseTypeDef(TypedDict):
    VoiceChannelResponse: VoiceChannelResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEmailChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    EmailChannelRequest: EmailChannelRequestTypeDef

class EmailMessageActivityTypeDef(TypedDict):
    MessageConfig: NotRequired[JourneyEmailMessageTypeDef]
    NextActivity: NotRequired[str]
    TemplateName: NotRequired[str]
    TemplateVersion: NotRequired[str]

class SendUsersMessageResponseTypeDef(TypedDict):
    ApplicationId: str
    RequestId: NotRequired[str]
    Result: NotRequired[Dict[str, Dict[str, EndpointMessageResultTypeDef]]]

class EndpointResponseTypeDef(TypedDict):
    Address: NotRequired[str]
    ApplicationId: NotRequired[str]
    Attributes: NotRequired[Dict[str, List[str]]]
    ChannelType: NotRequired[ChannelTypeType]
    CohortId: NotRequired[str]
    CreationDate: NotRequired[str]
    Demographic: NotRequired[EndpointDemographicTypeDef]
    EffectiveDate: NotRequired[str]
    EndpointStatus: NotRequired[str]
    Id: NotRequired[str]
    Location: NotRequired[EndpointLocationTypeDef]
    Metrics: NotRequired[Dict[str, float]]
    OptOut: NotRequired[str]
    RequestId: NotRequired[str]
    User: NotRequired[EndpointUserOutputTypeDef]

EndpointUserUnionTypeDef = Union[EndpointUserTypeDef, EndpointUserOutputTypeDef]

class EventDimensionsOutputTypeDef(TypedDict):
    Attributes: NotRequired[Dict[str, AttributeDimensionOutputTypeDef]]
    EventType: NotRequired[SetDimensionOutputTypeDef]
    Metrics: NotRequired[Dict[str, MetricDimensionTypeDef]]

class SegmentDemographicsOutputTypeDef(TypedDict):
    AppVersion: NotRequired[SetDimensionOutputTypeDef]
    Channel: NotRequired[SetDimensionOutputTypeDef]
    DeviceType: NotRequired[SetDimensionOutputTypeDef]
    Make: NotRequired[SetDimensionOutputTypeDef]
    Model: NotRequired[SetDimensionOutputTypeDef]
    Platform: NotRequired[SetDimensionOutputTypeDef]

class ItemResponseTypeDef(TypedDict):
    EndpointItemResponse: NotRequired[EndpointItemResponseTypeDef]
    EventsItemResponse: NotRequired[Dict[str, EventItemResponseTypeDef]]

class EventTypeDef(TypedDict):
    EventType: str
    Timestamp: str
    AppPackageName: NotRequired[str]
    AppTitle: NotRequired[str]
    AppVersionCode: NotRequired[str]
    Attributes: NotRequired[Mapping[str, str]]
    ClientSdkVersion: NotRequired[str]
    Metrics: NotRequired[Mapping[str, float]]
    SdkName: NotRequired[str]
    Session: NotRequired[SessionTypeDef]

ExportJobResponseTypeDef = TypedDict(
    "ExportJobResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Definition": ExportJobResourceTypeDef,
        "Id": str,
        "JobStatus": JobStatusType,
        "Type": str,
        "CompletedPieces": NotRequired[int],
        "CompletionDate": NotRequired[str],
        "FailedPieces": NotRequired[int],
        "Failures": NotRequired[List[str]],
        "TotalFailures": NotRequired[int],
        "TotalPieces": NotRequired[int],
        "TotalProcessed": NotRequired[int],
    },
)

class UpdateGcmChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    GCMChannelRequest: GCMChannelRequestTypeDef

class GPSPointDimensionTypeDef(TypedDict):
    Coordinates: GPSCoordinatesTypeDef
    RangeInKilometers: NotRequired[float]

class GetApplicationDateRangeKpiRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    KpiName: str
    EndTime: NotRequired[TimestampTypeDef]
    NextToken: NotRequired[str]
    PageSize: NotRequired[str]
    StartTime: NotRequired[TimestampTypeDef]

class GetCampaignDateRangeKpiRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    CampaignId: str
    KpiName: str
    EndTime: NotRequired[TimestampTypeDef]
    NextToken: NotRequired[str]
    PageSize: NotRequired[str]
    StartTime: NotRequired[TimestampTypeDef]

class GetJourneyDateRangeKpiRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    JourneyId: str
    KpiName: str
    EndTime: NotRequired[TimestampTypeDef]
    NextToken: NotRequired[str]
    PageSize: NotRequired[str]
    StartTime: NotRequired[TimestampTypeDef]

class JourneyScheduleTypeDef(TypedDict):
    EndTime: NotRequired[TimestampTypeDef]
    StartTime: NotRequired[TimestampTypeDef]
    Timezone: NotRequired[str]

class GetJourneyExecutionActivityMetricsResponseTypeDef(TypedDict):
    JourneyExecutionActivityMetricsResponse: JourneyExecutionActivityMetricsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetJourneyExecutionMetricsResponseTypeDef(TypedDict):
    JourneyExecutionMetricsResponse: JourneyExecutionMetricsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetJourneyRunExecutionActivityMetricsResponseTypeDef(TypedDict):
    JourneyRunExecutionActivityMetricsResponse: JourneyRunExecutionActivityMetricsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetJourneyRunExecutionMetricsResponseTypeDef(TypedDict):
    JourneyRunExecutionMetricsResponse: JourneyRunExecutionMetricsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSmsTemplateResponseTypeDef(TypedDict):
    SMSTemplateResponse: SMSTemplateResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceTemplateResponseTypeDef(TypedDict):
    VoiceTemplateResponse: VoiceTemplateResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ImportJobResponseTypeDef = TypedDict(
    "ImportJobResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Definition": ImportJobResourceTypeDef,
        "Id": str,
        "JobStatus": JobStatusType,
        "Type": str,
        "CompletedPieces": NotRequired[int],
        "CompletionDate": NotRequired[str],
        "FailedPieces": NotRequired[int],
        "Failures": NotRequired[List[str]],
        "TotalFailures": NotRequired[int],
        "TotalPieces": NotRequired[int],
        "TotalProcessed": NotRequired[int],
    },
)

class InAppMessageButtonTypeDef(TypedDict):
    Android: NotRequired[OverrideButtonConfigurationTypeDef]
    DefaultConfig: NotRequired[DefaultButtonConfigurationTypeDef]
    IOS: NotRequired[OverrideButtonConfigurationTypeDef]
    Web: NotRequired[OverrideButtonConfigurationTypeDef]

class PushMessageActivityTypeDef(TypedDict):
    MessageConfig: NotRequired[JourneyPushMessageTypeDef]
    NextActivity: NotRequired[str]
    TemplateName: NotRequired[str]
    TemplateVersion: NotRequired[str]

class JourneyRunsResponseTypeDef(TypedDict):
    Item: List[JourneyRunResponseTypeDef]
    NextToken: NotRequired[str]

class SMSMessageActivityTypeDef(TypedDict):
    MessageConfig: NotRequired[JourneySMSMessageTypeDef]
    NextActivity: NotRequired[str]
    TemplateName: NotRequired[str]
    TemplateVersion: NotRequired[str]

class UpdateJourneyStateRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    JourneyId: str
    JourneyStateRequest: JourneyStateRequestTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    TagsModel: TagsModelOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class MessageResponseTypeDef(TypedDict):
    ApplicationId: str
    EndpointResult: NotRequired[Dict[str, EndpointMessageResultTypeDef]]
    RequestId: NotRequired[str]
    Result: NotRequired[Dict[str, MessageResultTypeDef]]

class PhoneNumberValidateRequestRequestTypeDef(TypedDict):
    NumberValidateRequest: NumberValidateRequestTypeDef

class PhoneNumberValidateResponseTypeDef(TypedDict):
    NumberValidateResponse: NumberValidateResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class OpenHoursOutputTypeDef(TypedDict):
    EMAIL: NotRequired[Dict[DayOfWeekType, List[OpenHoursRuleTypeDef]]]
    SMS: NotRequired[Dict[DayOfWeekType, List[OpenHoursRuleTypeDef]]]
    PUSH: NotRequired[Dict[DayOfWeekType, List[OpenHoursRuleTypeDef]]]
    VOICE: NotRequired[Dict[DayOfWeekType, List[OpenHoursRuleTypeDef]]]
    CUSTOM: NotRequired[Dict[DayOfWeekType, List[OpenHoursRuleTypeDef]]]

class OpenHoursTypeDef(TypedDict):
    EMAIL: NotRequired[Mapping[DayOfWeekType, Sequence[OpenHoursRuleTypeDef]]]
    SMS: NotRequired[Mapping[DayOfWeekType, Sequence[OpenHoursRuleTypeDef]]]
    PUSH: NotRequired[Mapping[DayOfWeekType, Sequence[OpenHoursRuleTypeDef]]]
    VOICE: NotRequired[Mapping[DayOfWeekType, Sequence[OpenHoursRuleTypeDef]]]
    CUSTOM: NotRequired[Mapping[DayOfWeekType, Sequence[OpenHoursRuleTypeDef]]]

class PutEventStreamRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    WriteEventStream: WriteEventStreamTypeDef

class RandomSplitActivityOutputTypeDef(TypedDict):
    Branches: NotRequired[List[RandomSplitEntryTypeDef]]

class RandomSplitActivityTypeDef(TypedDict):
    Branches: NotRequired[Sequence[RandomSplitEntryTypeDef]]

class SegmentBehaviorsTypeDef(TypedDict):
    Recency: NotRequired[RecencyDimensionTypeDef]

class RemoveAttributesRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    AttributeType: str
    UpdateAttributesRequest: UpdateAttributesRequestTypeDef

class ResultRowTypeDef(TypedDict):
    GroupedBys: List[ResultRowValueTypeDef]
    Values: List[ResultRowValueTypeDef]

class UpdateSmsChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    SMSChannelRequest: SMSChannelRequestTypeDef

class SendOTPMessageRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    SendOTPMessageRequestParameters: SendOTPMessageRequestParametersTypeDef

SetDimensionUnionTypeDef = Union[SetDimensionTypeDef, SetDimensionOutputTypeDef]

class SimpleEmailTypeDef(TypedDict):
    HtmlPart: NotRequired[SimpleEmailPartTypeDef]
    Subject: NotRequired[SimpleEmailPartTypeDef]
    TextPart: NotRequired[SimpleEmailPartTypeDef]
    Headers: NotRequired[Sequence[MessageHeaderTypeDef]]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagsModel: TagsModelTypeDef

class UpdateTemplateActiveVersionRequestRequestTypeDef(TypedDict):
    TemplateActiveVersionRequest: TemplateActiveVersionRequestTypeDef
    TemplateName: str
    TemplateType: str

class TemplateConfigurationTypeDef(TypedDict):
    EmailTemplate: NotRequired[TemplateTypeDef]
    PushTemplate: NotRequired[TemplateTypeDef]
    SMSTemplate: NotRequired[TemplateTypeDef]
    VoiceTemplate: NotRequired[TemplateTypeDef]
    InAppTemplate: NotRequired[TemplateTypeDef]

class TemplatesResponseTypeDef(TypedDict):
    Item: List[TemplateResponseTypeDef]
    NextToken: NotRequired[str]

class TemplateVersionsResponseTypeDef(TypedDict):
    Item: List[TemplateVersionResponseTypeDef]
    Message: NotRequired[str]
    NextToken: NotRequired[str]
    RequestID: NotRequired[str]

class UpdateRecommenderConfigurationRequestRequestTypeDef(TypedDict):
    RecommenderId: str
    UpdateRecommenderConfiguration: UpdateRecommenderConfigurationTypeDef

class UpdateVoiceChannelRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    VoiceChannelRequest: VoiceChannelRequestTypeDef

class VerifyOTPMessageResponseTypeDef(TypedDict):
    VerificationResponse: VerificationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class VerifyOTPMessageRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    VerifyOTPMessageRequestParameters: VerifyOTPMessageRequestParametersTypeDef

class GetCampaignActivitiesResponseTypeDef(TypedDict):
    ActivitiesResponse: ActivitiesResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAppsResponseTypeDef(TypedDict):
    ApplicationsResponse: ApplicationsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ApplicationSettingsResourceTypeDef(TypedDict):
    ApplicationId: str
    CampaignHook: NotRequired[CampaignHookTypeDef]
    LastModifiedDate: NotRequired[str]
    Limits: NotRequired[CampaignLimitsTypeDef]
    QuietTime: NotRequired[QuietTimeTypeDef]
    JourneyLimits: NotRequired[ApplicationSettingsJourneyLimitsTypeDef]

class WriteApplicationSettingsRequestTypeDef(TypedDict):
    CampaignHook: NotRequired[CampaignHookTypeDef]
    CloudWatchMetricsEnabled: NotRequired[bool]
    EventTaggingEnabled: NotRequired[bool]
    Limits: NotRequired[CampaignLimitsTypeDef]
    QuietTime: NotRequired[QuietTimeTypeDef]
    JourneyLimits: NotRequired[ApplicationSettingsJourneyLimitsTypeDef]

CampaignEmailMessageUnionTypeDef = Union[
    CampaignEmailMessageTypeDef, CampaignEmailMessageOutputTypeDef
]

class CreateEmailTemplateRequestRequestTypeDef(TypedDict):
    EmailTemplateRequest: EmailTemplateRequestTypeDef
    TemplateName: str

class UpdateEmailTemplateRequestRequestTypeDef(TypedDict):
    EmailTemplateRequest: EmailTemplateRequestTypeDef
    TemplateName: str
    CreateNewVersion: NotRequired[bool]
    Version: NotRequired[str]

class GetEmailTemplateResponseTypeDef(TypedDict):
    EmailTemplateResponse: EmailTemplateResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetChannelsResponseTypeDef(TypedDict):
    ChannelsResponse: ChannelsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ClosedDaysUnionTypeDef = Union[ClosedDaysTypeDef, ClosedDaysOutputTypeDef]

class GetRecommenderConfigurationsResponseTypeDef(TypedDict):
    ListRecommenderConfigurationsResponse: ListRecommenderConfigurationsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

CustomMessageActivityUnionTypeDef = Union[
    CustomMessageActivityTypeDef, CustomMessageActivityOutputTypeDef
]

class CreatePushTemplateRequestRequestTypeDef(TypedDict):
    PushNotificationTemplateRequest: PushNotificationTemplateRequestTypeDef
    TemplateName: str

class UpdatePushTemplateRequestRequestTypeDef(TypedDict):
    PushNotificationTemplateRequest: PushNotificationTemplateRequestTypeDef
    TemplateName: str
    CreateNewVersion: NotRequired[bool]
    Version: NotRequired[str]

class GetPushTemplateResponseTypeDef(TypedDict):
    PushNotificationTemplateResponse: PushNotificationTemplateResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SendUsersMessagesResponseTypeDef(TypedDict):
    SendUsersMessageResponse: SendUsersMessageResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteEndpointResponseTypeDef(TypedDict):
    EndpointResponse: EndpointResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class EndpointsResponseTypeDef(TypedDict):
    Item: List[EndpointResponseTypeDef]

class GetEndpointResponseTypeDef(TypedDict):
    EndpointResponse: EndpointResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class EndpointBatchItemTypeDef(TypedDict):
    Address: NotRequired[str]
    Attributes: NotRequired[Mapping[str, Sequence[str]]]
    ChannelType: NotRequired[ChannelTypeType]
    Demographic: NotRequired[EndpointDemographicTypeDef]
    EffectiveDate: NotRequired[str]
    EndpointStatus: NotRequired[str]
    Id: NotRequired[str]
    Location: NotRequired[EndpointLocationTypeDef]
    Metrics: NotRequired[Mapping[str, float]]
    OptOut: NotRequired[str]
    RequestId: NotRequired[str]
    User: NotRequired[EndpointUserUnionTypeDef]

class EndpointRequestTypeDef(TypedDict):
    Address: NotRequired[str]
    Attributes: NotRequired[Mapping[str, Sequence[str]]]
    ChannelType: NotRequired[ChannelTypeType]
    Demographic: NotRequired[EndpointDemographicTypeDef]
    EffectiveDate: NotRequired[str]
    EndpointStatus: NotRequired[str]
    Location: NotRequired[EndpointLocationTypeDef]
    Metrics: NotRequired[Mapping[str, float]]
    OptOut: NotRequired[str]
    RequestId: NotRequired[str]
    User: NotRequired[EndpointUserUnionTypeDef]

class PublicEndpointTypeDef(TypedDict):
    Address: NotRequired[str]
    Attributes: NotRequired[Mapping[str, Sequence[str]]]
    ChannelType: NotRequired[ChannelTypeType]
    Demographic: NotRequired[EndpointDemographicTypeDef]
    EffectiveDate: NotRequired[str]
    EndpointStatus: NotRequired[str]
    Location: NotRequired[EndpointLocationTypeDef]
    Metrics: NotRequired[Mapping[str, float]]
    OptOut: NotRequired[str]
    RequestId: NotRequired[str]
    User: NotRequired[EndpointUserUnionTypeDef]

class CampaignEventFilterOutputTypeDef(TypedDict):
    Dimensions: EventDimensionsOutputTypeDef
    FilterType: FilterTypeType

class EventConditionOutputTypeDef(TypedDict):
    Dimensions: NotRequired[EventDimensionsOutputTypeDef]
    MessageActivity: NotRequired[str]

class EventFilterOutputTypeDef(TypedDict):
    Dimensions: EventDimensionsOutputTypeDef
    FilterType: FilterTypeType

class EventsResponseTypeDef(TypedDict):
    Results: NotRequired[Dict[str, ItemResponseTypeDef]]

class CreateExportJobResponseTypeDef(TypedDict):
    ExportJobResponse: ExportJobResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ExportJobsResponseTypeDef(TypedDict):
    Item: List[ExportJobResponseTypeDef]
    NextToken: NotRequired[str]

class GetExportJobResponseTypeDef(TypedDict):
    ExportJobResponse: ExportJobResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SegmentLocationOutputTypeDef(TypedDict):
    Country: NotRequired[SetDimensionOutputTypeDef]
    GPSPoint: NotRequired[GPSPointDimensionTypeDef]

JourneyScheduleUnionTypeDef = Union[JourneyScheduleTypeDef, JourneyScheduleOutputTypeDef]

class CreateImportJobResponseTypeDef(TypedDict):
    ImportJobResponse: ImportJobResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetImportJobResponseTypeDef(TypedDict):
    ImportJobResponse: ImportJobResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ImportJobsResponseTypeDef(TypedDict):
    Item: List[ImportJobResponseTypeDef]
    NextToken: NotRequired[str]

class InAppMessageContentTypeDef(TypedDict):
    BackgroundColor: NotRequired[str]
    BodyConfig: NotRequired[InAppMessageBodyConfigTypeDef]
    HeaderConfig: NotRequired[InAppMessageHeaderConfigTypeDef]
    ImageUrl: NotRequired[str]
    PrimaryBtn: NotRequired[InAppMessageButtonTypeDef]
    SecondaryBtn: NotRequired[InAppMessageButtonTypeDef]

class GetJourneyRunsResponseTypeDef(TypedDict):
    JourneyRunsResponse: JourneyRunsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SendMessagesResponseTypeDef(TypedDict):
    MessageResponse: MessageResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SendOTPMessageResponseTypeDef(TypedDict):
    MessageResponse: MessageResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

OpenHoursUnionTypeDef = Union[OpenHoursTypeDef, OpenHoursOutputTypeDef]
RandomSplitActivityUnionTypeDef = Union[
    RandomSplitActivityTypeDef, RandomSplitActivityOutputTypeDef
]

class BaseKpiResultTypeDef(TypedDict):
    Rows: List[ResultRowTypeDef]

class EventDimensionsTypeDef(TypedDict):
    Attributes: NotRequired[Mapping[str, AttributeDimensionUnionTypeDef]]
    EventType: NotRequired[SetDimensionUnionTypeDef]
    Metrics: NotRequired[Mapping[str, MetricDimensionTypeDef]]

class SegmentDemographicsTypeDef(TypedDict):
    AppVersion: NotRequired[SetDimensionUnionTypeDef]
    Channel: NotRequired[SetDimensionUnionTypeDef]
    DeviceType: NotRequired[SetDimensionUnionTypeDef]
    Make: NotRequired[SetDimensionUnionTypeDef]
    Model: NotRequired[SetDimensionUnionTypeDef]
    Platform: NotRequired[SetDimensionUnionTypeDef]

class SegmentLocationTypeDef(TypedDict):
    Country: NotRequired[SetDimensionUnionTypeDef]
    GPSPoint: NotRequired[GPSPointDimensionTypeDef]

class EmailMessageTypeDef(TypedDict):
    Body: NotRequired[str]
    FeedbackForwardingAddress: NotRequired[str]
    FromAddress: NotRequired[str]
    RawEmail: NotRequired[RawEmailTypeDef]
    ReplyToAddresses: NotRequired[Sequence[str]]
    SimpleEmail: NotRequired[SimpleEmailTypeDef]
    Substitutions: NotRequired[Mapping[str, Sequence[str]]]

class ListTemplatesResponseTypeDef(TypedDict):
    TemplatesResponse: TemplatesResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListTemplateVersionsResponseTypeDef(TypedDict):
    TemplateVersionsResponse: TemplateVersionsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetApplicationSettingsResponseTypeDef(TypedDict):
    ApplicationSettingsResource: ApplicationSettingsResourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateApplicationSettingsResponseTypeDef(TypedDict):
    ApplicationSettingsResource: ApplicationSettingsResourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateApplicationSettingsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    WriteApplicationSettingsRequest: WriteApplicationSettingsRequestTypeDef

class DeleteUserEndpointsResponseTypeDef(TypedDict):
    EndpointsResponse: EndpointsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetUserEndpointsResponseTypeDef(TypedDict):
    EndpointsResponse: EndpointsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class EndpointBatchRequestTypeDef(TypedDict):
    Item: Sequence[EndpointBatchItemTypeDef]

class UpdateEndpointRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    EndpointId: str
    EndpointRequest: EndpointRequestTypeDef

class EventsBatchTypeDef(TypedDict):
    Endpoint: PublicEndpointTypeDef
    Events: Mapping[str, EventTypeDef]

class InAppCampaignScheduleTypeDef(TypedDict):
    EndDate: NotRequired[str]
    EventFilter: NotRequired[CampaignEventFilterOutputTypeDef]
    QuietTime: NotRequired[QuietTimeTypeDef]

class ScheduleOutputTypeDef(TypedDict):
    StartTime: str
    EndTime: NotRequired[str]
    EventFilter: NotRequired[CampaignEventFilterOutputTypeDef]
    Frequency: NotRequired[FrequencyType]
    IsLocalTime: NotRequired[bool]
    QuietTime: NotRequired[QuietTimeTypeDef]
    Timezone: NotRequired[str]

class EventStartConditionOutputTypeDef(TypedDict):
    EventFilter: NotRequired[EventFilterOutputTypeDef]
    SegmentId: NotRequired[str]

class PutEventsResponseTypeDef(TypedDict):
    EventsResponse: EventsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetExportJobsResponseTypeDef(TypedDict):
    ExportJobsResponse: ExportJobsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSegmentExportJobsResponseTypeDef(TypedDict):
    ExportJobsResponse: ExportJobsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SegmentDimensionsOutputTypeDef(TypedDict):
    Attributes: NotRequired[Dict[str, AttributeDimensionOutputTypeDef]]
    Behavior: NotRequired[SegmentBehaviorsTypeDef]
    Demographic: NotRequired[SegmentDemographicsOutputTypeDef]
    Location: NotRequired[SegmentLocationOutputTypeDef]
    Metrics: NotRequired[Dict[str, MetricDimensionTypeDef]]
    UserAttributes: NotRequired[Dict[str, AttributeDimensionOutputTypeDef]]

class GetImportJobsResponseTypeDef(TypedDict):
    ImportJobsResponse: ImportJobsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSegmentImportJobsResponseTypeDef(TypedDict):
    ImportJobsResponse: ImportJobsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CampaignInAppMessageOutputTypeDef(TypedDict):
    Body: NotRequired[str]
    Content: NotRequired[List[InAppMessageContentTypeDef]]
    CustomConfig: NotRequired[Dict[str, str]]
    Layout: NotRequired[LayoutType]

class CampaignInAppMessageTypeDef(TypedDict):
    Body: NotRequired[str]
    Content: NotRequired[Sequence[InAppMessageContentTypeDef]]
    CustomConfig: NotRequired[Mapping[str, str]]
    Layout: NotRequired[LayoutType]

class InAppMessageTypeDef(TypedDict):
    Content: NotRequired[List[InAppMessageContentTypeDef]]
    CustomConfig: NotRequired[Dict[str, str]]
    Layout: NotRequired[LayoutType]

class InAppTemplateRequestTypeDef(TypedDict):
    Content: NotRequired[Sequence[InAppMessageContentTypeDef]]
    CustomConfig: NotRequired[Mapping[str, str]]
    Layout: NotRequired[LayoutType]
    tags: NotRequired[Mapping[str, str]]
    TemplateDescription: NotRequired[str]

class InAppTemplateResponseTypeDef(TypedDict):
    CreationDate: str
    LastModifiedDate: str
    TemplateName: str
    TemplateType: TemplateTypeType
    Arn: NotRequired[str]
    Content: NotRequired[List[InAppMessageContentTypeDef]]
    CustomConfig: NotRequired[Dict[str, str]]
    Layout: NotRequired[LayoutType]
    tags: NotRequired[Dict[str, str]]
    TemplateDescription: NotRequired[str]
    Version: NotRequired[str]

class ApplicationDateRangeKpiResponseTypeDef(TypedDict):
    ApplicationId: str
    EndTime: datetime
    KpiName: str
    KpiResult: BaseKpiResultTypeDef
    StartTime: datetime
    NextToken: NotRequired[str]

class CampaignDateRangeKpiResponseTypeDef(TypedDict):
    ApplicationId: str
    CampaignId: str
    EndTime: datetime
    KpiName: str
    KpiResult: BaseKpiResultTypeDef
    StartTime: datetime
    NextToken: NotRequired[str]

class JourneyDateRangeKpiResponseTypeDef(TypedDict):
    ApplicationId: str
    EndTime: datetime
    JourneyId: str
    KpiName: str
    KpiResult: BaseKpiResultTypeDef
    StartTime: datetime
    NextToken: NotRequired[str]

EventDimensionsUnionTypeDef = Union[EventDimensionsTypeDef, EventDimensionsOutputTypeDef]
SegmentDemographicsUnionTypeDef = Union[
    SegmentDemographicsTypeDef, SegmentDemographicsOutputTypeDef
]
SegmentLocationUnionTypeDef = Union[SegmentLocationTypeDef, SegmentLocationOutputTypeDef]

class DirectMessageConfigurationTypeDef(TypedDict):
    ADMMessage: NotRequired[ADMMessageTypeDef]
    APNSMessage: NotRequired[APNSMessageTypeDef]
    BaiduMessage: NotRequired[BaiduMessageTypeDef]
    DefaultMessage: NotRequired[DefaultMessageTypeDef]
    DefaultPushNotificationMessage: NotRequired[DefaultPushNotificationMessageTypeDef]
    EmailMessage: NotRequired[EmailMessageTypeDef]
    GCMMessage: NotRequired[GCMMessageTypeDef]
    SMSMessage: NotRequired[SMSMessageTypeDef]
    VoiceMessage: NotRequired[VoiceMessageTypeDef]

class UpdateEndpointsBatchRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    EndpointBatchRequest: EndpointBatchRequestTypeDef

class EventsRequestTypeDef(TypedDict):
    BatchItem: Mapping[str, EventsBatchTypeDef]

class StartConditionOutputTypeDef(TypedDict):
    Description: NotRequired[str]
    EventStartCondition: NotRequired[EventStartConditionOutputTypeDef]
    SegmentStartCondition: NotRequired[SegmentConditionTypeDef]

SegmentGroupOutputTypeDef = TypedDict(
    "SegmentGroupOutputTypeDef",
    {
        "Dimensions": NotRequired[List[SegmentDimensionsOutputTypeDef]],
        "SourceSegments": NotRequired[List[SegmentReferenceTypeDef]],
        "SourceType": NotRequired[SourceTypeType],
        "Type": NotRequired[TypeType],
    },
)

class SimpleConditionOutputTypeDef(TypedDict):
    EventCondition: NotRequired[EventConditionOutputTypeDef]
    SegmentCondition: NotRequired[SegmentConditionTypeDef]
    SegmentDimensions: NotRequired[SegmentDimensionsOutputTypeDef]

class MessageConfigurationOutputTypeDef(TypedDict):
    ADMMessage: NotRequired[MessageTypeDef]
    APNSMessage: NotRequired[MessageTypeDef]
    BaiduMessage: NotRequired[MessageTypeDef]
    CustomMessage: NotRequired[CampaignCustomMessageTypeDef]
    DefaultMessage: NotRequired[MessageTypeDef]
    EmailMessage: NotRequired[CampaignEmailMessageOutputTypeDef]
    GCMMessage: NotRequired[MessageTypeDef]
    SMSMessage: NotRequired[CampaignSmsMessageTypeDef]
    InAppMessage: NotRequired[CampaignInAppMessageOutputTypeDef]

CampaignInAppMessageUnionTypeDef = Union[
    CampaignInAppMessageTypeDef, CampaignInAppMessageOutputTypeDef
]

class InAppMessageCampaignTypeDef(TypedDict):
    CampaignId: NotRequired[str]
    DailyCap: NotRequired[int]
    InAppMessage: NotRequired[InAppMessageTypeDef]
    Priority: NotRequired[int]
    Schedule: NotRequired[InAppCampaignScheduleTypeDef]
    SessionCap: NotRequired[int]
    TotalCap: NotRequired[int]
    TreatmentId: NotRequired[str]

class CreateInAppTemplateRequestRequestTypeDef(TypedDict):
    InAppTemplateRequest: InAppTemplateRequestTypeDef
    TemplateName: str

class UpdateInAppTemplateRequestRequestTypeDef(TypedDict):
    InAppTemplateRequest: InAppTemplateRequestTypeDef
    TemplateName: str
    CreateNewVersion: NotRequired[bool]
    Version: NotRequired[str]

class GetInAppTemplateResponseTypeDef(TypedDict):
    InAppTemplateResponse: InAppTemplateResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetApplicationDateRangeKpiResponseTypeDef(TypedDict):
    ApplicationDateRangeKpiResponse: ApplicationDateRangeKpiResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetCampaignDateRangeKpiResponseTypeDef(TypedDict):
    CampaignDateRangeKpiResponse: CampaignDateRangeKpiResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetJourneyDateRangeKpiResponseTypeDef(TypedDict):
    JourneyDateRangeKpiResponse: JourneyDateRangeKpiResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CampaignEventFilterTypeDef(TypedDict):
    Dimensions: EventDimensionsUnionTypeDef
    FilterType: FilterTypeType

class EventConditionTypeDef(TypedDict):
    Dimensions: NotRequired[EventDimensionsUnionTypeDef]
    MessageActivity: NotRequired[str]

class EventFilterTypeDef(TypedDict):
    Dimensions: EventDimensionsUnionTypeDef
    FilterType: FilterTypeType

class SegmentDimensionsTypeDef(TypedDict):
    Attributes: NotRequired[Mapping[str, AttributeDimensionUnionTypeDef]]
    Behavior: NotRequired[SegmentBehaviorsTypeDef]
    Demographic: NotRequired[SegmentDemographicsUnionTypeDef]
    Location: NotRequired[SegmentLocationUnionTypeDef]
    Metrics: NotRequired[Mapping[str, MetricDimensionTypeDef]]
    UserAttributes: NotRequired[Mapping[str, AttributeDimensionUnionTypeDef]]

class MessageRequestTypeDef(TypedDict):
    MessageConfiguration: DirectMessageConfigurationTypeDef
    Addresses: NotRequired[Mapping[str, AddressConfigurationTypeDef]]
    Context: NotRequired[Mapping[str, str]]
    Endpoints: NotRequired[Mapping[str, EndpointSendConfigurationTypeDef]]
    TemplateConfiguration: NotRequired[TemplateConfigurationTypeDef]
    TraceId: NotRequired[str]

class SendUsersMessageRequestTypeDef(TypedDict):
    MessageConfiguration: DirectMessageConfigurationTypeDef
    Users: Mapping[str, EndpointSendConfigurationTypeDef]
    Context: NotRequired[Mapping[str, str]]
    TemplateConfiguration: NotRequired[TemplateConfigurationTypeDef]
    TraceId: NotRequired[str]

class PutEventsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    EventsRequest: EventsRequestTypeDef

class SegmentGroupListOutputTypeDef(TypedDict):
    Groups: NotRequired[List[SegmentGroupOutputTypeDef]]
    Include: NotRequired[IncludeType]

class ConditionOutputTypeDef(TypedDict):
    Conditions: NotRequired[List[SimpleConditionOutputTypeDef]]
    Operator: NotRequired[OperatorType]

class MultiConditionalBranchOutputTypeDef(TypedDict):
    Condition: NotRequired[SimpleConditionOutputTypeDef]
    NextActivity: NotRequired[str]

class TreatmentResourceTypeDef(TypedDict):
    Id: str
    SizePercent: int
    CustomDeliveryConfiguration: NotRequired[CustomDeliveryConfigurationOutputTypeDef]
    MessageConfiguration: NotRequired[MessageConfigurationOutputTypeDef]
    Schedule: NotRequired[ScheduleOutputTypeDef]
    State: NotRequired[CampaignStateTypeDef]
    TemplateConfiguration: NotRequired[TemplateConfigurationTypeDef]
    TreatmentDescription: NotRequired[str]
    TreatmentName: NotRequired[str]

class MessageConfigurationTypeDef(TypedDict):
    ADMMessage: NotRequired[MessageTypeDef]
    APNSMessage: NotRequired[MessageTypeDef]
    BaiduMessage: NotRequired[MessageTypeDef]
    CustomMessage: NotRequired[CampaignCustomMessageTypeDef]
    DefaultMessage: NotRequired[MessageTypeDef]
    EmailMessage: NotRequired[CampaignEmailMessageUnionTypeDef]
    GCMMessage: NotRequired[MessageTypeDef]
    SMSMessage: NotRequired[CampaignSmsMessageTypeDef]
    InAppMessage: NotRequired[CampaignInAppMessageUnionTypeDef]

class InAppMessagesResponseTypeDef(TypedDict):
    InAppMessageCampaigns: NotRequired[List[InAppMessageCampaignTypeDef]]

CampaignEventFilterUnionTypeDef = Union[
    CampaignEventFilterTypeDef, CampaignEventFilterOutputTypeDef
]
EventConditionUnionTypeDef = Union[EventConditionTypeDef, EventConditionOutputTypeDef]
EventFilterUnionTypeDef = Union[EventFilterTypeDef, EventFilterOutputTypeDef]
SegmentDimensionsUnionTypeDef = Union[SegmentDimensionsTypeDef, SegmentDimensionsOutputTypeDef]

class SendMessagesRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    MessageRequest: MessageRequestTypeDef

class SendUsersMessagesRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    SendUsersMessageRequest: SendUsersMessageRequestTypeDef

class SegmentResponseTypeDef(TypedDict):
    ApplicationId: str
    Arn: str
    CreationDate: str
    Id: str
    SegmentType: SegmentTypeType
    Dimensions: NotRequired[SegmentDimensionsOutputTypeDef]
    ImportDefinition: NotRequired[SegmentImportResourceTypeDef]
    LastModifiedDate: NotRequired[str]
    Name: NotRequired[str]
    SegmentGroups: NotRequired[SegmentGroupListOutputTypeDef]
    tags: NotRequired[Dict[str, str]]
    Version: NotRequired[int]

class ConditionalSplitActivityOutputTypeDef(TypedDict):
    Condition: NotRequired[ConditionOutputTypeDef]
    EvaluationWaitTime: NotRequired[WaitTimeTypeDef]
    FalseActivity: NotRequired[str]
    TrueActivity: NotRequired[str]

class MultiConditionalSplitActivityOutputTypeDef(TypedDict):
    Branches: NotRequired[List[MultiConditionalBranchOutputTypeDef]]
    DefaultActivity: NotRequired[str]
    EvaluationWaitTime: NotRequired[WaitTimeTypeDef]

class CampaignResponseTypeDef(TypedDict):
    ApplicationId: str
    Arn: str
    CreationDate: str
    Id: str
    LastModifiedDate: str
    SegmentId: str
    SegmentVersion: int
    AdditionalTreatments: NotRequired[List[TreatmentResourceTypeDef]]
    CustomDeliveryConfiguration: NotRequired[CustomDeliveryConfigurationOutputTypeDef]
    DefaultState: NotRequired[CampaignStateTypeDef]
    Description: NotRequired[str]
    HoldoutPercent: NotRequired[int]
    Hook: NotRequired[CampaignHookTypeDef]
    IsPaused: NotRequired[bool]
    Limits: NotRequired[CampaignLimitsTypeDef]
    MessageConfiguration: NotRequired[MessageConfigurationOutputTypeDef]
    Name: NotRequired[str]
    Schedule: NotRequired[ScheduleOutputTypeDef]
    State: NotRequired[CampaignStateTypeDef]
    tags: NotRequired[Dict[str, str]]
    TemplateConfiguration: NotRequired[TemplateConfigurationTypeDef]
    TreatmentDescription: NotRequired[str]
    TreatmentName: NotRequired[str]
    Version: NotRequired[int]
    Priority: NotRequired[int]

MessageConfigurationUnionTypeDef = Union[
    MessageConfigurationTypeDef, MessageConfigurationOutputTypeDef
]

class GetInAppMessagesResponseTypeDef(TypedDict):
    InAppMessagesResponse: InAppMessagesResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ScheduleTypeDef(TypedDict):
    StartTime: str
    EndTime: NotRequired[str]
    EventFilter: NotRequired[CampaignEventFilterUnionTypeDef]
    Frequency: NotRequired[FrequencyType]
    IsLocalTime: NotRequired[bool]
    QuietTime: NotRequired[QuietTimeTypeDef]
    Timezone: NotRequired[str]

class EventStartConditionTypeDef(TypedDict):
    EventFilter: NotRequired[EventFilterUnionTypeDef]
    SegmentId: NotRequired[str]

SegmentGroupTypeDef = TypedDict(
    "SegmentGroupTypeDef",
    {
        "Dimensions": NotRequired[Sequence[SegmentDimensionsUnionTypeDef]],
        "SourceSegments": NotRequired[Sequence[SegmentReferenceTypeDef]],
        "SourceType": NotRequired[SourceTypeType],
        "Type": NotRequired[TypeType],
    },
)

class SimpleConditionTypeDef(TypedDict):
    EventCondition: NotRequired[EventConditionUnionTypeDef]
    SegmentCondition: NotRequired[SegmentConditionTypeDef]
    SegmentDimensions: NotRequired[SegmentDimensionsUnionTypeDef]

class CreateSegmentResponseTypeDef(TypedDict):
    SegmentResponse: SegmentResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteSegmentResponseTypeDef(TypedDict):
    SegmentResponse: SegmentResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSegmentResponseTypeDef(TypedDict):
    SegmentResponse: SegmentResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSegmentVersionResponseTypeDef(TypedDict):
    SegmentResponse: SegmentResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SegmentsResponseTypeDef(TypedDict):
    Item: List[SegmentResponseTypeDef]
    NextToken: NotRequired[str]

class UpdateSegmentResponseTypeDef(TypedDict):
    SegmentResponse: SegmentResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ActivityOutputTypeDef(TypedDict):
    CUSTOM: NotRequired[CustomMessageActivityOutputTypeDef]
    ConditionalSplit: NotRequired[ConditionalSplitActivityOutputTypeDef]
    Description: NotRequired[str]
    EMAIL: NotRequired[EmailMessageActivityTypeDef]
    Holdout: NotRequired[HoldoutActivityTypeDef]
    MultiCondition: NotRequired[MultiConditionalSplitActivityOutputTypeDef]
    PUSH: NotRequired[PushMessageActivityTypeDef]
    RandomSplit: NotRequired[RandomSplitActivityOutputTypeDef]
    SMS: NotRequired[SMSMessageActivityTypeDef]
    Wait: NotRequired[WaitActivityTypeDef]
    ContactCenter: NotRequired[ContactCenterActivityTypeDef]

class CampaignsResponseTypeDef(TypedDict):
    Item: List[CampaignResponseTypeDef]
    NextToken: NotRequired[str]

class CreateCampaignResponseTypeDef(TypedDict):
    CampaignResponse: CampaignResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteCampaignResponseTypeDef(TypedDict):
    CampaignResponse: CampaignResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetCampaignResponseTypeDef(TypedDict):
    CampaignResponse: CampaignResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetCampaignVersionResponseTypeDef(TypedDict):
    CampaignResponse: CampaignResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateCampaignResponseTypeDef(TypedDict):
    CampaignResponse: CampaignResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ScheduleUnionTypeDef = Union[ScheduleTypeDef, ScheduleOutputTypeDef]
EventStartConditionUnionTypeDef = Union[
    EventStartConditionTypeDef, EventStartConditionOutputTypeDef
]
SegmentGroupUnionTypeDef = Union[SegmentGroupTypeDef, SegmentGroupOutputTypeDef]
SimpleConditionUnionTypeDef = Union[SimpleConditionTypeDef, SimpleConditionOutputTypeDef]

class GetSegmentVersionsResponseTypeDef(TypedDict):
    SegmentsResponse: SegmentsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSegmentsResponseTypeDef(TypedDict):
    SegmentsResponse: SegmentsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class JourneyResponseTypeDef(TypedDict):
    ApplicationId: str
    Id: str
    Name: str
    Activities: NotRequired[Dict[str, ActivityOutputTypeDef]]
    CreationDate: NotRequired[str]
    LastModifiedDate: NotRequired[str]
    Limits: NotRequired[JourneyLimitsTypeDef]
    LocalTime: NotRequired[bool]
    QuietTime: NotRequired[QuietTimeTypeDef]
    RefreshFrequency: NotRequired[str]
    Schedule: NotRequired[JourneyScheduleOutputTypeDef]
    StartActivity: NotRequired[str]
    StartCondition: NotRequired[StartConditionOutputTypeDef]
    State: NotRequired[StateType]
    tags: NotRequired[Dict[str, str]]
    WaitForQuietTime: NotRequired[bool]
    RefreshOnSegmentUpdate: NotRequired[bool]
    JourneyChannelSettings: NotRequired[JourneyChannelSettingsTypeDef]
    SendingSchedule: NotRequired[bool]
    OpenHours: NotRequired[OpenHoursOutputTypeDef]
    ClosedDays: NotRequired[ClosedDaysOutputTypeDef]
    TimezoneEstimationMethods: NotRequired[List[TimezoneEstimationMethodsElementType]]

class GetCampaignVersionsResponseTypeDef(TypedDict):
    CampaignsResponse: CampaignsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetCampaignsResponseTypeDef(TypedDict):
    CampaignsResponse: CampaignsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class WriteTreatmentResourceTypeDef(TypedDict):
    SizePercent: int
    CustomDeliveryConfiguration: NotRequired[CustomDeliveryConfigurationUnionTypeDef]
    MessageConfiguration: NotRequired[MessageConfigurationUnionTypeDef]
    Schedule: NotRequired[ScheduleUnionTypeDef]
    TemplateConfiguration: NotRequired[TemplateConfigurationTypeDef]
    TreatmentDescription: NotRequired[str]
    TreatmentName: NotRequired[str]

class StartConditionTypeDef(TypedDict):
    Description: NotRequired[str]
    EventStartCondition: NotRequired[EventStartConditionUnionTypeDef]
    SegmentStartCondition: NotRequired[SegmentConditionTypeDef]

class SegmentGroupListTypeDef(TypedDict):
    Groups: NotRequired[Sequence[SegmentGroupUnionTypeDef]]
    Include: NotRequired[IncludeType]

class ConditionTypeDef(TypedDict):
    Conditions: NotRequired[Sequence[SimpleConditionUnionTypeDef]]
    Operator: NotRequired[OperatorType]

class MultiConditionalBranchTypeDef(TypedDict):
    Condition: NotRequired[SimpleConditionUnionTypeDef]
    NextActivity: NotRequired[str]

class CreateJourneyResponseTypeDef(TypedDict):
    JourneyResponse: JourneyResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteJourneyResponseTypeDef(TypedDict):
    JourneyResponse: JourneyResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetJourneyResponseTypeDef(TypedDict):
    JourneyResponse: JourneyResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class JourneysResponseTypeDef(TypedDict):
    Item: List[JourneyResponseTypeDef]
    NextToken: NotRequired[str]

class UpdateJourneyResponseTypeDef(TypedDict):
    JourneyResponse: JourneyResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateJourneyStateResponseTypeDef(TypedDict):
    JourneyResponse: JourneyResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class WriteCampaignRequestTypeDef(TypedDict):
    AdditionalTreatments: NotRequired[Sequence[WriteTreatmentResourceTypeDef]]
    CustomDeliveryConfiguration: NotRequired[CustomDeliveryConfigurationUnionTypeDef]
    Description: NotRequired[str]
    HoldoutPercent: NotRequired[int]
    Hook: NotRequired[CampaignHookTypeDef]
    IsPaused: NotRequired[bool]
    Limits: NotRequired[CampaignLimitsTypeDef]
    MessageConfiguration: NotRequired[MessageConfigurationUnionTypeDef]
    Name: NotRequired[str]
    Schedule: NotRequired[ScheduleUnionTypeDef]
    SegmentId: NotRequired[str]
    SegmentVersion: NotRequired[int]
    tags: NotRequired[Mapping[str, str]]
    TemplateConfiguration: NotRequired[TemplateConfigurationTypeDef]
    TreatmentDescription: NotRequired[str]
    TreatmentName: NotRequired[str]
    Priority: NotRequired[int]

StartConditionUnionTypeDef = Union[StartConditionTypeDef, StartConditionOutputTypeDef]
SegmentGroupListUnionTypeDef = Union[SegmentGroupListTypeDef, SegmentGroupListOutputTypeDef]
ConditionUnionTypeDef = Union[ConditionTypeDef, ConditionOutputTypeDef]
MultiConditionalBranchUnionTypeDef = Union[
    MultiConditionalBranchTypeDef, MultiConditionalBranchOutputTypeDef
]

class ListJourneysResponseTypeDef(TypedDict):
    JourneysResponse: JourneysResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCampaignRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    WriteCampaignRequest: WriteCampaignRequestTypeDef

class UpdateCampaignRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    CampaignId: str
    WriteCampaignRequest: WriteCampaignRequestTypeDef

class WriteSegmentRequestTypeDef(TypedDict):
    Dimensions: NotRequired[SegmentDimensionsUnionTypeDef]
    Name: NotRequired[str]
    SegmentGroups: NotRequired[SegmentGroupListUnionTypeDef]
    tags: NotRequired[Mapping[str, str]]

class ConditionalSplitActivityTypeDef(TypedDict):
    Condition: NotRequired[ConditionUnionTypeDef]
    EvaluationWaitTime: NotRequired[WaitTimeTypeDef]
    FalseActivity: NotRequired[str]
    TrueActivity: NotRequired[str]

class MultiConditionalSplitActivityTypeDef(TypedDict):
    Branches: NotRequired[Sequence[MultiConditionalBranchUnionTypeDef]]
    DefaultActivity: NotRequired[str]
    EvaluationWaitTime: NotRequired[WaitTimeTypeDef]

class CreateSegmentRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    WriteSegmentRequest: WriteSegmentRequestTypeDef

class UpdateSegmentRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    SegmentId: str
    WriteSegmentRequest: WriteSegmentRequestTypeDef

ConditionalSplitActivityUnionTypeDef = Union[
    ConditionalSplitActivityTypeDef, ConditionalSplitActivityOutputTypeDef
]
MultiConditionalSplitActivityUnionTypeDef = Union[
    MultiConditionalSplitActivityTypeDef, MultiConditionalSplitActivityOutputTypeDef
]

class ActivityTypeDef(TypedDict):
    CUSTOM: NotRequired[CustomMessageActivityUnionTypeDef]
    ConditionalSplit: NotRequired[ConditionalSplitActivityUnionTypeDef]
    Description: NotRequired[str]
    EMAIL: NotRequired[EmailMessageActivityTypeDef]
    Holdout: NotRequired[HoldoutActivityTypeDef]
    MultiCondition: NotRequired[MultiConditionalSplitActivityUnionTypeDef]
    PUSH: NotRequired[PushMessageActivityTypeDef]
    RandomSplit: NotRequired[RandomSplitActivityUnionTypeDef]
    SMS: NotRequired[SMSMessageActivityTypeDef]
    Wait: NotRequired[WaitActivityTypeDef]
    ContactCenter: NotRequired[ContactCenterActivityTypeDef]

ActivityUnionTypeDef = Union[ActivityTypeDef, ActivityOutputTypeDef]

class WriteJourneyRequestTypeDef(TypedDict):
    Name: str
    Activities: NotRequired[Mapping[str, ActivityUnionTypeDef]]
    CreationDate: NotRequired[str]
    LastModifiedDate: NotRequired[str]
    Limits: NotRequired[JourneyLimitsTypeDef]
    LocalTime: NotRequired[bool]
    QuietTime: NotRequired[QuietTimeTypeDef]
    RefreshFrequency: NotRequired[str]
    Schedule: NotRequired[JourneyScheduleUnionTypeDef]
    StartActivity: NotRequired[str]
    StartCondition: NotRequired[StartConditionUnionTypeDef]
    State: NotRequired[StateType]
    WaitForQuietTime: NotRequired[bool]
    RefreshOnSegmentUpdate: NotRequired[bool]
    JourneyChannelSettings: NotRequired[JourneyChannelSettingsTypeDef]
    SendingSchedule: NotRequired[bool]
    OpenHours: NotRequired[OpenHoursUnionTypeDef]
    ClosedDays: NotRequired[ClosedDaysUnionTypeDef]
    TimezoneEstimationMethods: NotRequired[Sequence[TimezoneEstimationMethodsElementType]]

class CreateJourneyRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    WriteJourneyRequest: WriteJourneyRequestTypeDef

class UpdateJourneyRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    JourneyId: str
    WriteJourneyRequest: WriteJourneyRequestTypeDef
