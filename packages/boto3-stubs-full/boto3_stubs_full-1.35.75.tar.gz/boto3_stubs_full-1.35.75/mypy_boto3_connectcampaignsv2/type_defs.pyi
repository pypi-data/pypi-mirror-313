"""
Type annotations for connectcampaignsv2 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/type_defs/)

Usage::

    ```python
    from mypy_boto3_connectcampaignsv2.type_defs import AnswerMachineDetectionConfigTypeDef

    data: AnswerMachineDetectionConfigTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    CampaignDeletionPolicyType,
    CampaignStateType,
    ChannelSubtypeType,
    CommunicationTimeConfigTypeType,
    DayOfWeekType,
    EventTypeType,
    FailureCodeType,
    GetCampaignStateBatchFailureCodeType,
    InstanceOnboardingJobFailureCodeType,
    InstanceOnboardingJobStatusCodeType,
    LocalTimeZoneDetectionTypeType,
    ProfileOutboundRequestFailureCodeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AnswerMachineDetectionConfigTypeDef",
    "CampaignFiltersTypeDef",
    "CampaignSummaryTypeDef",
    "CampaignTypeDef",
    "ChannelSubtypeConfigOutputTypeDef",
    "ChannelSubtypeConfigTypeDef",
    "ChannelSubtypeParametersTypeDef",
    "CommunicationLimitTypeDef",
    "CommunicationLimitsConfigOutputTypeDef",
    "CommunicationLimitsConfigTypeDef",
    "CommunicationLimitsOutputTypeDef",
    "CommunicationLimitsTypeDef",
    "CommunicationLimitsUnionTypeDef",
    "CommunicationTimeConfigOutputTypeDef",
    "CommunicationTimeConfigTypeDef",
    "CreateCampaignRequestRequestTypeDef",
    "CreateCampaignResponseTypeDef",
    "CustomerProfilesIntegrationConfigTypeDef",
    "CustomerProfilesIntegrationIdentifierTypeDef",
    "CustomerProfilesIntegrationSummaryTypeDef",
    "DeleteCampaignChannelSubtypeConfigRequestRequestTypeDef",
    "DeleteCampaignCommunicationLimitsRequestRequestTypeDef",
    "DeleteCampaignCommunicationTimeRequestRequestTypeDef",
    "DeleteCampaignRequestRequestTypeDef",
    "DeleteConnectInstanceConfigRequestRequestTypeDef",
    "DeleteConnectInstanceIntegrationRequestRequestTypeDef",
    "DeleteInstanceOnboardingJobRequestRequestTypeDef",
    "DescribeCampaignRequestRequestTypeDef",
    "DescribeCampaignResponseTypeDef",
    "EmailChannelSubtypeConfigOutputTypeDef",
    "EmailChannelSubtypeConfigTypeDef",
    "EmailChannelSubtypeConfigUnionTypeDef",
    "EmailChannelSubtypeParametersTypeDef",
    "EmailOutboundConfigTypeDef",
    "EmailOutboundModeOutputTypeDef",
    "EmailOutboundModeTypeDef",
    "EmailOutboundModeUnionTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionConfigTypeDef",
    "EventTriggerTypeDef",
    "FailedCampaignStateResponseTypeDef",
    "FailedProfileOutboundRequestTypeDef",
    "FailedRequestTypeDef",
    "GetCampaignStateBatchRequestRequestTypeDef",
    "GetCampaignStateBatchResponseTypeDef",
    "GetCampaignStateRequestRequestTypeDef",
    "GetCampaignStateResponseTypeDef",
    "GetConnectInstanceConfigRequestRequestTypeDef",
    "GetConnectInstanceConfigResponseTypeDef",
    "GetInstanceOnboardingJobStatusRequestRequestTypeDef",
    "GetInstanceOnboardingJobStatusResponseTypeDef",
    "InstanceConfigTypeDef",
    "InstanceIdFilterTypeDef",
    "InstanceOnboardingJobStatusTypeDef",
    "IntegrationConfigTypeDef",
    "IntegrationIdentifierTypeDef",
    "IntegrationSummaryTypeDef",
    "ListCampaignsRequestListCampaignsPaginateTypeDef",
    "ListCampaignsRequestRequestTypeDef",
    "ListCampaignsResponseTypeDef",
    "ListConnectInstanceIntegrationsRequestListConnectInstanceIntegrationsPaginateTypeDef",
    "ListConnectInstanceIntegrationsRequestRequestTypeDef",
    "ListConnectInstanceIntegrationsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LocalTimeZoneConfigOutputTypeDef",
    "LocalTimeZoneConfigTypeDef",
    "LocalTimeZoneConfigUnionTypeDef",
    "OpenHoursOutputTypeDef",
    "OpenHoursTypeDef",
    "OpenHoursUnionTypeDef",
    "OutboundRequestTypeDef",
    "PaginatorConfigTypeDef",
    "PauseCampaignRequestRequestTypeDef",
    "PredictiveConfigTypeDef",
    "ProfileOutboundRequestTypeDef",
    "ProgressiveConfigTypeDef",
    "PutConnectInstanceIntegrationRequestRequestTypeDef",
    "PutOutboundRequestBatchRequestRequestTypeDef",
    "PutOutboundRequestBatchResponseTypeDef",
    "PutProfileOutboundRequestBatchRequestRequestTypeDef",
    "PutProfileOutboundRequestBatchResponseTypeDef",
    "QConnectIntegrationConfigTypeDef",
    "QConnectIntegrationIdentifierTypeDef",
    "QConnectIntegrationSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "RestrictedPeriodTypeDef",
    "RestrictedPeriodsOutputTypeDef",
    "RestrictedPeriodsTypeDef",
    "RestrictedPeriodsUnionTypeDef",
    "ResumeCampaignRequestRequestTypeDef",
    "ScheduleOutputTypeDef",
    "ScheduleTypeDef",
    "SmsChannelSubtypeConfigOutputTypeDef",
    "SmsChannelSubtypeConfigTypeDef",
    "SmsChannelSubtypeConfigUnionTypeDef",
    "SmsChannelSubtypeParametersTypeDef",
    "SmsOutboundConfigTypeDef",
    "SmsOutboundModeOutputTypeDef",
    "SmsOutboundModeTypeDef",
    "SmsOutboundModeUnionTypeDef",
    "SourceTypeDef",
    "StartCampaignRequestRequestTypeDef",
    "StartInstanceOnboardingJobRequestRequestTypeDef",
    "StartInstanceOnboardingJobResponseTypeDef",
    "StopCampaignRequestRequestTypeDef",
    "SuccessfulCampaignStateResponseTypeDef",
    "SuccessfulProfileOutboundRequestTypeDef",
    "SuccessfulRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TelephonyChannelSubtypeConfigOutputTypeDef",
    "TelephonyChannelSubtypeConfigTypeDef",
    "TelephonyChannelSubtypeConfigUnionTypeDef",
    "TelephonyChannelSubtypeParametersTypeDef",
    "TelephonyOutboundConfigTypeDef",
    "TelephonyOutboundModeOutputTypeDef",
    "TelephonyOutboundModeTypeDef",
    "TelephonyOutboundModeUnionTypeDef",
    "TimeRangeTypeDef",
    "TimeWindowOutputTypeDef",
    "TimeWindowTypeDef",
    "TimeWindowUnionTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCampaignChannelSubtypeConfigRequestRequestTypeDef",
    "UpdateCampaignCommunicationLimitsRequestRequestTypeDef",
    "UpdateCampaignCommunicationTimeRequestRequestTypeDef",
    "UpdateCampaignFlowAssociationRequestRequestTypeDef",
    "UpdateCampaignNameRequestRequestTypeDef",
    "UpdateCampaignScheduleRequestRequestTypeDef",
    "UpdateCampaignSourceRequestRequestTypeDef",
)

class AnswerMachineDetectionConfigTypeDef(TypedDict):
    enableAnswerMachineDetection: bool
    awaitAnswerMachinePrompt: NotRequired[bool]

InstanceIdFilterTypeDef = TypedDict(
    "InstanceIdFilterTypeDef",
    {
        "value": str,
        "operator": Literal["Eq"],
    },
)

class ScheduleOutputTypeDef(TypedDict):
    startTime: datetime
    endTime: datetime
    refreshFrequency: NotRequired[str]

class EmailChannelSubtypeParametersTypeDef(TypedDict):
    destinationEmailAddress: str
    templateParameters: Mapping[str, str]
    connectSourceEmailAddress: NotRequired[str]
    templateArn: NotRequired[str]

class SmsChannelSubtypeParametersTypeDef(TypedDict):
    destinationPhoneNumber: str
    templateParameters: Mapping[str, str]
    connectSourcePhoneNumberArn: NotRequired[str]
    templateArn: NotRequired[str]

class CommunicationLimitTypeDef(TypedDict):
    maxCountPerRecipient: int
    frequency: int
    unit: Literal["DAY"]

class LocalTimeZoneConfigOutputTypeDef(TypedDict):
    defaultTimeZone: NotRequired[str]
    localTimeZoneDetection: NotRequired[List[LocalTimeZoneDetectionTypeType]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CustomerProfilesIntegrationConfigTypeDef(TypedDict):
    domainArn: str
    objectTypeNames: Mapping[EventTypeType, str]

class CustomerProfilesIntegrationIdentifierTypeDef(TypedDict):
    domainArn: str

class CustomerProfilesIntegrationSummaryTypeDef(TypedDict):
    domainArn: str
    objectTypeNames: Dict[EventTypeType, str]

DeleteCampaignChannelSubtypeConfigRequestRequestTypeDef = TypedDict(
    "DeleteCampaignChannelSubtypeConfigRequestRequestTypeDef",
    {
        "id": str,
        "channelSubtype": ChannelSubtypeType,
    },
)
DeleteCampaignCommunicationLimitsRequestRequestTypeDef = TypedDict(
    "DeleteCampaignCommunicationLimitsRequestRequestTypeDef",
    {
        "id": str,
        "config": Literal["ALL_CHANNEL_SUBTYPES"],
    },
)
DeleteCampaignCommunicationTimeRequestRequestTypeDef = TypedDict(
    "DeleteCampaignCommunicationTimeRequestRequestTypeDef",
    {
        "id": str,
        "config": CommunicationTimeConfigTypeType,
    },
)
DeleteCampaignRequestRequestTypeDef = TypedDict(
    "DeleteCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

class DeleteConnectInstanceConfigRequestRequestTypeDef(TypedDict):
    connectInstanceId: str
    campaignDeletionPolicy: NotRequired[CampaignDeletionPolicyType]

class DeleteInstanceOnboardingJobRequestRequestTypeDef(TypedDict):
    connectInstanceId: str

DescribeCampaignRequestRequestTypeDef = TypedDict(
    "DescribeCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

class EmailOutboundConfigTypeDef(TypedDict):
    connectSourceEmailAddress: str
    wisdomTemplateArn: str
    sourceEmailAddressDisplayName: NotRequired[str]

class EmailOutboundModeOutputTypeDef(TypedDict):
    agentless: NotRequired[Dict[str, Any]]

class EmailOutboundModeTypeDef(TypedDict):
    agentless: NotRequired[Mapping[str, Any]]

class EncryptionConfigTypeDef(TypedDict):
    enabled: bool
    encryptionType: NotRequired[Literal["KMS"]]
    keyArn: NotRequired[str]

class EventTriggerTypeDef(TypedDict):
    customerProfilesDomainArn: NotRequired[str]

class FailedCampaignStateResponseTypeDef(TypedDict):
    campaignId: NotRequired[str]
    failureCode: NotRequired[GetCampaignStateBatchFailureCodeType]

FailedProfileOutboundRequestTypeDef = TypedDict(
    "FailedProfileOutboundRequestTypeDef",
    {
        "clientToken": NotRequired[str],
        "id": NotRequired[str],
        "failureCode": NotRequired[ProfileOutboundRequestFailureCodeType],
    },
)
FailedRequestTypeDef = TypedDict(
    "FailedRequestTypeDef",
    {
        "clientToken": NotRequired[str],
        "id": NotRequired[str],
        "failureCode": NotRequired[FailureCodeType],
    },
)

class GetCampaignStateBatchRequestRequestTypeDef(TypedDict):
    campaignIds: Sequence[str]

class SuccessfulCampaignStateResponseTypeDef(TypedDict):
    campaignId: NotRequired[str]
    state: NotRequired[CampaignStateType]

GetCampaignStateRequestRequestTypeDef = TypedDict(
    "GetCampaignStateRequestRequestTypeDef",
    {
        "id": str,
    },
)

class GetConnectInstanceConfigRequestRequestTypeDef(TypedDict):
    connectInstanceId: str

class GetInstanceOnboardingJobStatusRequestRequestTypeDef(TypedDict):
    connectInstanceId: str

class InstanceOnboardingJobStatusTypeDef(TypedDict):
    connectInstanceId: str
    status: InstanceOnboardingJobStatusCodeType
    failureCode: NotRequired[InstanceOnboardingJobFailureCodeType]

class QConnectIntegrationConfigTypeDef(TypedDict):
    knowledgeBaseArn: str

class QConnectIntegrationIdentifierTypeDef(TypedDict):
    knowledgeBaseArn: str

class QConnectIntegrationSummaryTypeDef(TypedDict):
    knowledgeBaseArn: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListConnectInstanceIntegrationsRequestRequestTypeDef(TypedDict):
    connectInstanceId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    arn: str

class LocalTimeZoneConfigTypeDef(TypedDict):
    defaultTimeZone: NotRequired[str]
    localTimeZoneDetection: NotRequired[Sequence[LocalTimeZoneDetectionTypeType]]

class TimeRangeTypeDef(TypedDict):
    startTime: str
    endTime: str

TimestampTypeDef = Union[datetime, str]
PauseCampaignRequestRequestTypeDef = TypedDict(
    "PauseCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

class PredictiveConfigTypeDef(TypedDict):
    bandwidthAllocation: float

class ProgressiveConfigTypeDef(TypedDict):
    bandwidthAllocation: float

SuccessfulRequestTypeDef = TypedDict(
    "SuccessfulRequestTypeDef",
    {
        "clientToken": NotRequired[str],
        "id": NotRequired[str],
    },
)
SuccessfulProfileOutboundRequestTypeDef = TypedDict(
    "SuccessfulProfileOutboundRequestTypeDef",
    {
        "clientToken": NotRequired[str],
        "id": NotRequired[str],
    },
)

class RestrictedPeriodTypeDef(TypedDict):
    startDate: str
    endDate: str
    name: NotRequired[str]

ResumeCampaignRequestRequestTypeDef = TypedDict(
    "ResumeCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

class SmsOutboundConfigTypeDef(TypedDict):
    connectSourcePhoneNumberArn: str
    wisdomTemplateArn: str

class SmsOutboundModeOutputTypeDef(TypedDict):
    agentless: NotRequired[Dict[str, Any]]

class SmsOutboundModeTypeDef(TypedDict):
    agentless: NotRequired[Mapping[str, Any]]

StartCampaignRequestRequestTypeDef = TypedDict(
    "StartCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)
StopCampaignRequestRequestTypeDef = TypedDict(
    "StopCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

class TagResourceRequestRequestTypeDef(TypedDict):
    arn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    arn: str
    tagKeys: Sequence[str]

UpdateCampaignFlowAssociationRequestRequestTypeDef = TypedDict(
    "UpdateCampaignFlowAssociationRequestRequestTypeDef",
    {
        "id": str,
        "connectCampaignFlowArn": str,
    },
)
UpdateCampaignNameRequestRequestTypeDef = TypedDict(
    "UpdateCampaignNameRequestRequestTypeDef",
    {
        "id": str,
        "name": str,
    },
)

class TelephonyChannelSubtypeParametersTypeDef(TypedDict):
    destinationPhoneNumber: str
    attributes: Mapping[str, str]
    connectSourcePhoneNumber: NotRequired[str]
    answerMachineDetectionConfig: NotRequired[AnswerMachineDetectionConfigTypeDef]

class TelephonyOutboundConfigTypeDef(TypedDict):
    connectContactFlowId: str
    connectSourcePhoneNumber: NotRequired[str]
    answerMachineDetectionConfig: NotRequired[AnswerMachineDetectionConfigTypeDef]

class CampaignFiltersTypeDef(TypedDict):
    instanceIdFilter: NotRequired[InstanceIdFilterTypeDef]

CampaignSummaryTypeDef = TypedDict(
    "CampaignSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "connectInstanceId": str,
        "channelSubtypes": List[ChannelSubtypeType],
        "schedule": NotRequired[ScheduleOutputTypeDef],
        "connectCampaignFlowArn": NotRequired[str],
    },
)

class CommunicationLimitsOutputTypeDef(TypedDict):
    communicationLimitsList: NotRequired[List[CommunicationLimitTypeDef]]

class CommunicationLimitsTypeDef(TypedDict):
    communicationLimitsList: NotRequired[Sequence[CommunicationLimitTypeDef]]

CreateCampaignResponseTypeDef = TypedDict(
    "CreateCampaignResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetCampaignStateResponseTypeDef(TypedDict):
    state: CampaignStateType
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class EmailChannelSubtypeConfigOutputTypeDef(TypedDict):
    outboundMode: EmailOutboundModeOutputTypeDef
    defaultOutboundConfig: EmailOutboundConfigTypeDef
    capacity: NotRequired[float]

EmailOutboundModeUnionTypeDef = Union[EmailOutboundModeTypeDef, EmailOutboundModeOutputTypeDef]

class InstanceConfigTypeDef(TypedDict):
    connectInstanceId: str
    serviceLinkedRoleArn: str
    encryptionConfig: EncryptionConfigTypeDef

class StartInstanceOnboardingJobRequestRequestTypeDef(TypedDict):
    connectInstanceId: str
    encryptionConfig: EncryptionConfigTypeDef

class SourceTypeDef(TypedDict):
    customerProfilesSegmentArn: NotRequired[str]
    eventTrigger: NotRequired[EventTriggerTypeDef]

class GetCampaignStateBatchResponseTypeDef(TypedDict):
    successfulRequests: List[SuccessfulCampaignStateResponseTypeDef]
    failedRequests: List[FailedCampaignStateResponseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetInstanceOnboardingJobStatusResponseTypeDef(TypedDict):
    connectInstanceOnboardingJobStatus: InstanceOnboardingJobStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartInstanceOnboardingJobResponseTypeDef(TypedDict):
    connectInstanceOnboardingJobStatus: InstanceOnboardingJobStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class IntegrationConfigTypeDef(TypedDict):
    customerProfiles: NotRequired[CustomerProfilesIntegrationConfigTypeDef]
    qConnect: NotRequired[QConnectIntegrationConfigTypeDef]

class IntegrationIdentifierTypeDef(TypedDict):
    customerProfiles: NotRequired[CustomerProfilesIntegrationIdentifierTypeDef]
    qConnect: NotRequired[QConnectIntegrationIdentifierTypeDef]

class IntegrationSummaryTypeDef(TypedDict):
    customerProfiles: NotRequired[CustomerProfilesIntegrationSummaryTypeDef]
    qConnect: NotRequired[QConnectIntegrationSummaryTypeDef]

class ListConnectInstanceIntegrationsRequestListConnectInstanceIntegrationsPaginateTypeDef(
    TypedDict
):
    connectInstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

LocalTimeZoneConfigUnionTypeDef = Union[
    LocalTimeZoneConfigTypeDef, LocalTimeZoneConfigOutputTypeDef
]

class OpenHoursOutputTypeDef(TypedDict):
    dailyHours: NotRequired[Dict[DayOfWeekType, List[TimeRangeTypeDef]]]

class OpenHoursTypeDef(TypedDict):
    dailyHours: NotRequired[Mapping[DayOfWeekType, Sequence[TimeRangeTypeDef]]]

class ProfileOutboundRequestTypeDef(TypedDict):
    clientToken: str
    profileId: str
    expirationTime: NotRequired[TimestampTypeDef]

class ScheduleTypeDef(TypedDict):
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    refreshFrequency: NotRequired[str]

class TelephonyOutboundModeOutputTypeDef(TypedDict):
    progressive: NotRequired[ProgressiveConfigTypeDef]
    predictive: NotRequired[PredictiveConfigTypeDef]
    agentless: NotRequired[Dict[str, Any]]

class TelephonyOutboundModeTypeDef(TypedDict):
    progressive: NotRequired[ProgressiveConfigTypeDef]
    predictive: NotRequired[PredictiveConfigTypeDef]
    agentless: NotRequired[Mapping[str, Any]]

class PutOutboundRequestBatchResponseTypeDef(TypedDict):
    successfulRequests: List[SuccessfulRequestTypeDef]
    failedRequests: List[FailedRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PutProfileOutboundRequestBatchResponseTypeDef(TypedDict):
    successfulRequests: List[SuccessfulProfileOutboundRequestTypeDef]
    failedRequests: List[FailedProfileOutboundRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class RestrictedPeriodsOutputTypeDef(TypedDict):
    restrictedPeriodList: NotRequired[List[RestrictedPeriodTypeDef]]

class RestrictedPeriodsTypeDef(TypedDict):
    restrictedPeriodList: NotRequired[Sequence[RestrictedPeriodTypeDef]]

class SmsChannelSubtypeConfigOutputTypeDef(TypedDict):
    outboundMode: SmsOutboundModeOutputTypeDef
    defaultOutboundConfig: SmsOutboundConfigTypeDef
    capacity: NotRequired[float]

SmsOutboundModeUnionTypeDef = Union[SmsOutboundModeTypeDef, SmsOutboundModeOutputTypeDef]

class ChannelSubtypeParametersTypeDef(TypedDict):
    telephony: NotRequired[TelephonyChannelSubtypeParametersTypeDef]
    sms: NotRequired[SmsChannelSubtypeParametersTypeDef]
    email: NotRequired[EmailChannelSubtypeParametersTypeDef]

class ListCampaignsRequestListCampaignsPaginateTypeDef(TypedDict):
    filters: NotRequired[CampaignFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCampaignsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    filters: NotRequired[CampaignFiltersTypeDef]

class ListCampaignsResponseTypeDef(TypedDict):
    campaignSummaryList: List[CampaignSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CommunicationLimitsConfigOutputTypeDef(TypedDict):
    allChannelSubtypes: NotRequired[CommunicationLimitsOutputTypeDef]

CommunicationLimitsUnionTypeDef = Union[
    CommunicationLimitsTypeDef, CommunicationLimitsOutputTypeDef
]

class EmailChannelSubtypeConfigTypeDef(TypedDict):
    outboundMode: EmailOutboundModeUnionTypeDef
    defaultOutboundConfig: EmailOutboundConfigTypeDef
    capacity: NotRequired[float]

class GetConnectInstanceConfigResponseTypeDef(TypedDict):
    connectInstanceConfig: InstanceConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

UpdateCampaignSourceRequestRequestTypeDef = TypedDict(
    "UpdateCampaignSourceRequestRequestTypeDef",
    {
        "id": str,
        "source": SourceTypeDef,
    },
)

class PutConnectInstanceIntegrationRequestRequestTypeDef(TypedDict):
    connectInstanceId: str
    integrationConfig: IntegrationConfigTypeDef

class DeleteConnectInstanceIntegrationRequestRequestTypeDef(TypedDict):
    connectInstanceId: str
    integrationIdentifier: IntegrationIdentifierTypeDef

class ListConnectInstanceIntegrationsResponseTypeDef(TypedDict):
    integrationSummaryList: List[IntegrationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

OpenHoursUnionTypeDef = Union[OpenHoursTypeDef, OpenHoursOutputTypeDef]
PutProfileOutboundRequestBatchRequestRequestTypeDef = TypedDict(
    "PutProfileOutboundRequestBatchRequestRequestTypeDef",
    {
        "id": str,
        "profileOutboundRequests": Sequence[ProfileOutboundRequestTypeDef],
    },
)
UpdateCampaignScheduleRequestRequestTypeDef = TypedDict(
    "UpdateCampaignScheduleRequestRequestTypeDef",
    {
        "id": str,
        "schedule": ScheduleTypeDef,
    },
)

class TelephonyChannelSubtypeConfigOutputTypeDef(TypedDict):
    outboundMode: TelephonyOutboundModeOutputTypeDef
    defaultOutboundConfig: TelephonyOutboundConfigTypeDef
    capacity: NotRequired[float]
    connectQueueId: NotRequired[str]

TelephonyOutboundModeUnionTypeDef = Union[
    TelephonyOutboundModeTypeDef, TelephonyOutboundModeOutputTypeDef
]

class TimeWindowOutputTypeDef(TypedDict):
    openHours: OpenHoursOutputTypeDef
    restrictedPeriods: NotRequired[RestrictedPeriodsOutputTypeDef]

RestrictedPeriodsUnionTypeDef = Union[RestrictedPeriodsTypeDef, RestrictedPeriodsOutputTypeDef]

class SmsChannelSubtypeConfigTypeDef(TypedDict):
    outboundMode: SmsOutboundModeUnionTypeDef
    defaultOutboundConfig: SmsOutboundConfigTypeDef
    capacity: NotRequired[float]

class OutboundRequestTypeDef(TypedDict):
    clientToken: str
    expirationTime: TimestampTypeDef
    channelSubtypeParameters: ChannelSubtypeParametersTypeDef

class CommunicationLimitsConfigTypeDef(TypedDict):
    allChannelSubtypes: NotRequired[CommunicationLimitsUnionTypeDef]

EmailChannelSubtypeConfigUnionTypeDef = Union[
    EmailChannelSubtypeConfigTypeDef, EmailChannelSubtypeConfigOutputTypeDef
]

class ChannelSubtypeConfigOutputTypeDef(TypedDict):
    telephony: NotRequired[TelephonyChannelSubtypeConfigOutputTypeDef]
    sms: NotRequired[SmsChannelSubtypeConfigOutputTypeDef]
    email: NotRequired[EmailChannelSubtypeConfigOutputTypeDef]

class TelephonyChannelSubtypeConfigTypeDef(TypedDict):
    outboundMode: TelephonyOutboundModeUnionTypeDef
    defaultOutboundConfig: TelephonyOutboundConfigTypeDef
    capacity: NotRequired[float]
    connectQueueId: NotRequired[str]

class CommunicationTimeConfigOutputTypeDef(TypedDict):
    localTimeZoneConfig: LocalTimeZoneConfigOutputTypeDef
    telephony: NotRequired[TimeWindowOutputTypeDef]
    sms: NotRequired[TimeWindowOutputTypeDef]
    email: NotRequired[TimeWindowOutputTypeDef]

class TimeWindowTypeDef(TypedDict):
    openHours: OpenHoursUnionTypeDef
    restrictedPeriods: NotRequired[RestrictedPeriodsUnionTypeDef]

SmsChannelSubtypeConfigUnionTypeDef = Union[
    SmsChannelSubtypeConfigTypeDef, SmsChannelSubtypeConfigOutputTypeDef
]
PutOutboundRequestBatchRequestRequestTypeDef = TypedDict(
    "PutOutboundRequestBatchRequestRequestTypeDef",
    {
        "id": str,
        "outboundRequests": Sequence[OutboundRequestTypeDef],
    },
)
UpdateCampaignCommunicationLimitsRequestRequestTypeDef = TypedDict(
    "UpdateCampaignCommunicationLimitsRequestRequestTypeDef",
    {
        "id": str,
        "communicationLimitsOverride": CommunicationLimitsConfigTypeDef,
    },
)
TelephonyChannelSubtypeConfigUnionTypeDef = Union[
    TelephonyChannelSubtypeConfigTypeDef, TelephonyChannelSubtypeConfigOutputTypeDef
]
CampaignTypeDef = TypedDict(
    "CampaignTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "connectInstanceId": str,
        "channelSubtypeConfig": ChannelSubtypeConfigOutputTypeDef,
        "source": NotRequired[SourceTypeDef],
        "connectCampaignFlowArn": NotRequired[str],
        "schedule": NotRequired[ScheduleOutputTypeDef],
        "communicationTimeConfig": NotRequired[CommunicationTimeConfigOutputTypeDef],
        "communicationLimitsOverride": NotRequired[CommunicationLimitsConfigOutputTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)
TimeWindowUnionTypeDef = Union[TimeWindowTypeDef, TimeWindowOutputTypeDef]

class ChannelSubtypeConfigTypeDef(TypedDict):
    telephony: NotRequired[TelephonyChannelSubtypeConfigUnionTypeDef]
    sms: NotRequired[SmsChannelSubtypeConfigUnionTypeDef]
    email: NotRequired[EmailChannelSubtypeConfigUnionTypeDef]

class DescribeCampaignResponseTypeDef(TypedDict):
    campaign: CampaignTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CommunicationTimeConfigTypeDef(TypedDict):
    localTimeZoneConfig: LocalTimeZoneConfigUnionTypeDef
    telephony: NotRequired[TimeWindowUnionTypeDef]
    sms: NotRequired[TimeWindowUnionTypeDef]
    email: NotRequired[TimeWindowUnionTypeDef]

UpdateCampaignChannelSubtypeConfigRequestRequestTypeDef = TypedDict(
    "UpdateCampaignChannelSubtypeConfigRequestRequestTypeDef",
    {
        "id": str,
        "channelSubtypeConfig": ChannelSubtypeConfigTypeDef,
    },
)

class CreateCampaignRequestRequestTypeDef(TypedDict):
    name: str
    connectInstanceId: str
    channelSubtypeConfig: ChannelSubtypeConfigTypeDef
    source: NotRequired[SourceTypeDef]
    connectCampaignFlowArn: NotRequired[str]
    schedule: NotRequired[ScheduleTypeDef]
    communicationTimeConfig: NotRequired[CommunicationTimeConfigTypeDef]
    communicationLimitsOverride: NotRequired[CommunicationLimitsConfigTypeDef]
    tags: NotRequired[Mapping[str, str]]

UpdateCampaignCommunicationTimeRequestRequestTypeDef = TypedDict(
    "UpdateCampaignCommunicationTimeRequestRequestTypeDef",
    {
        "id": str,
        "communicationTimeConfig": CommunicationTimeConfigTypeDef,
    },
)
