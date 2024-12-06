"""
Type annotations for chime service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/type_defs/)

Usage::

    ```python
    from mypy_boto3_chime.type_defs import AccountSettingsTypeDef

    data: AccountSettingsTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AccountStatusType,
    AccountTypeType,
    AppInstanceDataTypeType,
    ArtifactsStateType,
    AudioMuxTypeType,
    CallingNameStatusType,
    CapabilityType,
    ChannelMembershipTypeType,
    ChannelMessagePersistenceTypeType,
    ChannelMessageTypeType,
    ChannelModeType,
    ChannelPrivacyType,
    EmailStatusType,
    ErrorCodeType,
    GeoMatchLevelType,
    InviteStatusType,
    LicenseType,
    MediaPipelineStatusType,
    MemberTypeType,
    NotificationTargetType,
    NumberSelectionBehaviorType,
    OrderedPhoneNumberStatusType,
    OriginationRouteProtocolType,
    PhoneNumberAssociationNameType,
    PhoneNumberOrderStatusType,
    PhoneNumberProductTypeType,
    PhoneNumberStatusType,
    PhoneNumberTypeType,
    ProxySessionStatusType,
    RegistrationStatusType,
    RoomMembershipRoleType,
    SipRuleTriggerTypeType,
    SortOrderType,
    TranscribeLanguageCodeType,
    TranscribeMedicalRegionType,
    TranscribeMedicalSpecialtyType,
    TranscribeMedicalTypeType,
    TranscribePartialResultsStabilityType,
    TranscribeRegionType,
    TranscribeVocabularyFilterMethodType,
    UserTypeType,
    VoiceConnectorAwsRegionType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccountSettingsTypeDef",
    "AccountTypeDef",
    "AddressTypeDef",
    "AlexaForBusinessMetadataTypeDef",
    "AppInstanceAdminSummaryTypeDef",
    "AppInstanceAdminTypeDef",
    "AppInstanceRetentionSettingsTypeDef",
    "AppInstanceStreamingConfigurationTypeDef",
    "AppInstanceSummaryTypeDef",
    "AppInstanceTypeDef",
    "AppInstanceUserMembershipSummaryTypeDef",
    "AppInstanceUserSummaryTypeDef",
    "AppInstanceUserTypeDef",
    "ArtifactsConfigurationTypeDef",
    "AssociatePhoneNumberWithUserRequestRequestTypeDef",
    "AssociatePhoneNumbersWithVoiceConnectorGroupRequestRequestTypeDef",
    "AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef",
    "AssociatePhoneNumbersWithVoiceConnectorRequestRequestTypeDef",
    "AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef",
    "AssociateSigninDelegateGroupsWithAccountRequestRequestTypeDef",
    "AttendeeTypeDef",
    "AudioArtifactsConfigurationTypeDef",
    "BatchChannelMembershipsTypeDef",
    "BatchCreateAttendeeRequestRequestTypeDef",
    "BatchCreateAttendeeResponseTypeDef",
    "BatchCreateChannelMembershipErrorTypeDef",
    "BatchCreateChannelMembershipRequestRequestTypeDef",
    "BatchCreateChannelMembershipResponseTypeDef",
    "BatchCreateRoomMembershipRequestRequestTypeDef",
    "BatchCreateRoomMembershipResponseTypeDef",
    "BatchDeletePhoneNumberRequestRequestTypeDef",
    "BatchDeletePhoneNumberResponseTypeDef",
    "BatchSuspendUserRequestRequestTypeDef",
    "BatchSuspendUserResponseTypeDef",
    "BatchUnsuspendUserRequestRequestTypeDef",
    "BatchUnsuspendUserResponseTypeDef",
    "BatchUpdatePhoneNumberRequestRequestTypeDef",
    "BatchUpdatePhoneNumberResponseTypeDef",
    "BatchUpdateUserRequestRequestTypeDef",
    "BatchUpdateUserResponseTypeDef",
    "BotTypeDef",
    "BusinessCallingSettingsTypeDef",
    "CandidateAddressTypeDef",
    "ChannelBanSummaryTypeDef",
    "ChannelBanTypeDef",
    "ChannelMembershipForAppInstanceUserSummaryTypeDef",
    "ChannelMembershipSummaryTypeDef",
    "ChannelMembershipTypeDef",
    "ChannelMessageSummaryTypeDef",
    "ChannelMessageTypeDef",
    "ChannelModeratedByAppInstanceUserSummaryTypeDef",
    "ChannelModeratorSummaryTypeDef",
    "ChannelModeratorTypeDef",
    "ChannelRetentionSettingsTypeDef",
    "ChannelSummaryTypeDef",
    "ChannelTypeDef",
    "ChimeSdkMeetingConfigurationOutputTypeDef",
    "ChimeSdkMeetingConfigurationTypeDef",
    "ContentArtifactsConfigurationTypeDef",
    "ConversationRetentionSettingsTypeDef",
    "CreateAccountRequestRequestTypeDef",
    "CreateAccountResponseTypeDef",
    "CreateAppInstanceAdminRequestRequestTypeDef",
    "CreateAppInstanceAdminResponseTypeDef",
    "CreateAppInstanceRequestRequestTypeDef",
    "CreateAppInstanceResponseTypeDef",
    "CreateAppInstanceUserRequestRequestTypeDef",
    "CreateAppInstanceUserResponseTypeDef",
    "CreateAttendeeErrorTypeDef",
    "CreateAttendeeRequestItemTypeDef",
    "CreateAttendeeRequestRequestTypeDef",
    "CreateAttendeeResponseTypeDef",
    "CreateBotRequestRequestTypeDef",
    "CreateBotResponseTypeDef",
    "CreateChannelBanRequestRequestTypeDef",
    "CreateChannelBanResponseTypeDef",
    "CreateChannelMembershipRequestRequestTypeDef",
    "CreateChannelMembershipResponseTypeDef",
    "CreateChannelModeratorRequestRequestTypeDef",
    "CreateChannelModeratorResponseTypeDef",
    "CreateChannelRequestRequestTypeDef",
    "CreateChannelResponseTypeDef",
    "CreateMediaCapturePipelineRequestRequestTypeDef",
    "CreateMediaCapturePipelineResponseTypeDef",
    "CreateMeetingDialOutRequestRequestTypeDef",
    "CreateMeetingDialOutResponseTypeDef",
    "CreateMeetingRequestRequestTypeDef",
    "CreateMeetingResponseTypeDef",
    "CreateMeetingWithAttendeesRequestRequestTypeDef",
    "CreateMeetingWithAttendeesResponseTypeDef",
    "CreatePhoneNumberOrderRequestRequestTypeDef",
    "CreatePhoneNumberOrderResponseTypeDef",
    "CreateProxySessionRequestRequestTypeDef",
    "CreateProxySessionResponseTypeDef",
    "CreateRoomMembershipRequestRequestTypeDef",
    "CreateRoomMembershipResponseTypeDef",
    "CreateRoomRequestRequestTypeDef",
    "CreateRoomResponseTypeDef",
    "CreateSipMediaApplicationCallRequestRequestTypeDef",
    "CreateSipMediaApplicationCallResponseTypeDef",
    "CreateSipMediaApplicationRequestRequestTypeDef",
    "CreateSipMediaApplicationResponseTypeDef",
    "CreateSipRuleRequestRequestTypeDef",
    "CreateSipRuleResponseTypeDef",
    "CreateUserRequestRequestTypeDef",
    "CreateUserResponseTypeDef",
    "CreateVoiceConnectorGroupRequestRequestTypeDef",
    "CreateVoiceConnectorGroupResponseTypeDef",
    "CreateVoiceConnectorRequestRequestTypeDef",
    "CreateVoiceConnectorResponseTypeDef",
    "CredentialTypeDef",
    "DNISEmergencyCallingConfigurationTypeDef",
    "DeleteAccountRequestRequestTypeDef",
    "DeleteAppInstanceAdminRequestRequestTypeDef",
    "DeleteAppInstanceRequestRequestTypeDef",
    "DeleteAppInstanceStreamingConfigurationsRequestRequestTypeDef",
    "DeleteAppInstanceUserRequestRequestTypeDef",
    "DeleteAttendeeRequestRequestTypeDef",
    "DeleteChannelBanRequestRequestTypeDef",
    "DeleteChannelMembershipRequestRequestTypeDef",
    "DeleteChannelMessageRequestRequestTypeDef",
    "DeleteChannelModeratorRequestRequestTypeDef",
    "DeleteChannelRequestRequestTypeDef",
    "DeleteEventsConfigurationRequestRequestTypeDef",
    "DeleteMediaCapturePipelineRequestRequestTypeDef",
    "DeleteMeetingRequestRequestTypeDef",
    "DeletePhoneNumberRequestRequestTypeDef",
    "DeleteProxySessionRequestRequestTypeDef",
    "DeleteRoomMembershipRequestRequestTypeDef",
    "DeleteRoomRequestRequestTypeDef",
    "DeleteSipMediaApplicationRequestRequestTypeDef",
    "DeleteSipRuleRequestRequestTypeDef",
    "DeleteVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef",
    "DeleteVoiceConnectorGroupRequestRequestTypeDef",
    "DeleteVoiceConnectorOriginationRequestRequestTypeDef",
    "DeleteVoiceConnectorProxyRequestRequestTypeDef",
    "DeleteVoiceConnectorRequestRequestTypeDef",
    "DeleteVoiceConnectorStreamingConfigurationRequestRequestTypeDef",
    "DeleteVoiceConnectorTerminationCredentialsRequestRequestTypeDef",
    "DeleteVoiceConnectorTerminationRequestRequestTypeDef",
    "DescribeAppInstanceAdminRequestRequestTypeDef",
    "DescribeAppInstanceAdminResponseTypeDef",
    "DescribeAppInstanceRequestRequestTypeDef",
    "DescribeAppInstanceResponseTypeDef",
    "DescribeAppInstanceUserRequestRequestTypeDef",
    "DescribeAppInstanceUserResponseTypeDef",
    "DescribeChannelBanRequestRequestTypeDef",
    "DescribeChannelBanResponseTypeDef",
    "DescribeChannelMembershipForAppInstanceUserRequestRequestTypeDef",
    "DescribeChannelMembershipForAppInstanceUserResponseTypeDef",
    "DescribeChannelMembershipRequestRequestTypeDef",
    "DescribeChannelMembershipResponseTypeDef",
    "DescribeChannelModeratedByAppInstanceUserRequestRequestTypeDef",
    "DescribeChannelModeratedByAppInstanceUserResponseTypeDef",
    "DescribeChannelModeratorRequestRequestTypeDef",
    "DescribeChannelModeratorResponseTypeDef",
    "DescribeChannelRequestRequestTypeDef",
    "DescribeChannelResponseTypeDef",
    "DisassociatePhoneNumberFromUserRequestRequestTypeDef",
    "DisassociatePhoneNumbersFromVoiceConnectorGroupRequestRequestTypeDef",
    "DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef",
    "DisassociatePhoneNumbersFromVoiceConnectorRequestRequestTypeDef",
    "DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef",
    "DisassociateSigninDelegateGroupsFromAccountRequestRequestTypeDef",
    "EmergencyCallingConfigurationOutputTypeDef",
    "EmergencyCallingConfigurationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EngineTranscribeMedicalSettingsTypeDef",
    "EngineTranscribeSettingsTypeDef",
    "EventsConfigurationTypeDef",
    "GeoMatchParamsTypeDef",
    "GetAccountRequestRequestTypeDef",
    "GetAccountResponseTypeDef",
    "GetAccountSettingsRequestRequestTypeDef",
    "GetAccountSettingsResponseTypeDef",
    "GetAppInstanceRetentionSettingsRequestRequestTypeDef",
    "GetAppInstanceRetentionSettingsResponseTypeDef",
    "GetAppInstanceStreamingConfigurationsRequestRequestTypeDef",
    "GetAppInstanceStreamingConfigurationsResponseTypeDef",
    "GetAttendeeRequestRequestTypeDef",
    "GetAttendeeResponseTypeDef",
    "GetBotRequestRequestTypeDef",
    "GetBotResponseTypeDef",
    "GetChannelMessageRequestRequestTypeDef",
    "GetChannelMessageResponseTypeDef",
    "GetEventsConfigurationRequestRequestTypeDef",
    "GetEventsConfigurationResponseTypeDef",
    "GetGlobalSettingsResponseTypeDef",
    "GetMediaCapturePipelineRequestRequestTypeDef",
    "GetMediaCapturePipelineResponseTypeDef",
    "GetMeetingRequestRequestTypeDef",
    "GetMeetingResponseTypeDef",
    "GetMessagingSessionEndpointResponseTypeDef",
    "GetPhoneNumberOrderRequestRequestTypeDef",
    "GetPhoneNumberOrderResponseTypeDef",
    "GetPhoneNumberRequestRequestTypeDef",
    "GetPhoneNumberResponseTypeDef",
    "GetPhoneNumberSettingsResponseTypeDef",
    "GetProxySessionRequestRequestTypeDef",
    "GetProxySessionResponseTypeDef",
    "GetRetentionSettingsRequestRequestTypeDef",
    "GetRetentionSettingsResponseTypeDef",
    "GetRoomRequestRequestTypeDef",
    "GetRoomResponseTypeDef",
    "GetSipMediaApplicationLoggingConfigurationRequestRequestTypeDef",
    "GetSipMediaApplicationLoggingConfigurationResponseTypeDef",
    "GetSipMediaApplicationRequestRequestTypeDef",
    "GetSipMediaApplicationResponseTypeDef",
    "GetSipRuleRequestRequestTypeDef",
    "GetSipRuleResponseTypeDef",
    "GetUserRequestRequestTypeDef",
    "GetUserResponseTypeDef",
    "GetUserSettingsRequestRequestTypeDef",
    "GetUserSettingsResponseTypeDef",
    "GetVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef",
    "GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef",
    "GetVoiceConnectorGroupRequestRequestTypeDef",
    "GetVoiceConnectorGroupResponseTypeDef",
    "GetVoiceConnectorLoggingConfigurationRequestRequestTypeDef",
    "GetVoiceConnectorLoggingConfigurationResponseTypeDef",
    "GetVoiceConnectorOriginationRequestRequestTypeDef",
    "GetVoiceConnectorOriginationResponseTypeDef",
    "GetVoiceConnectorProxyRequestRequestTypeDef",
    "GetVoiceConnectorProxyResponseTypeDef",
    "GetVoiceConnectorRequestRequestTypeDef",
    "GetVoiceConnectorResponseTypeDef",
    "GetVoiceConnectorStreamingConfigurationRequestRequestTypeDef",
    "GetVoiceConnectorStreamingConfigurationResponseTypeDef",
    "GetVoiceConnectorTerminationHealthRequestRequestTypeDef",
    "GetVoiceConnectorTerminationHealthResponseTypeDef",
    "GetVoiceConnectorTerminationRequestRequestTypeDef",
    "GetVoiceConnectorTerminationResponseTypeDef",
    "IdentityTypeDef",
    "InviteTypeDef",
    "InviteUsersRequestRequestTypeDef",
    "InviteUsersResponseTypeDef",
    "ListAccountsRequestListAccountsPaginateTypeDef",
    "ListAccountsRequestRequestTypeDef",
    "ListAccountsResponseTypeDef",
    "ListAppInstanceAdminsRequestRequestTypeDef",
    "ListAppInstanceAdminsResponseTypeDef",
    "ListAppInstanceUsersRequestRequestTypeDef",
    "ListAppInstanceUsersResponseTypeDef",
    "ListAppInstancesRequestRequestTypeDef",
    "ListAppInstancesResponseTypeDef",
    "ListAttendeeTagsRequestRequestTypeDef",
    "ListAttendeeTagsResponseTypeDef",
    "ListAttendeesRequestRequestTypeDef",
    "ListAttendeesResponseTypeDef",
    "ListBotsRequestRequestTypeDef",
    "ListBotsResponseTypeDef",
    "ListChannelBansRequestRequestTypeDef",
    "ListChannelBansResponseTypeDef",
    "ListChannelMembershipsForAppInstanceUserRequestRequestTypeDef",
    "ListChannelMembershipsForAppInstanceUserResponseTypeDef",
    "ListChannelMembershipsRequestRequestTypeDef",
    "ListChannelMembershipsResponseTypeDef",
    "ListChannelMessagesRequestRequestTypeDef",
    "ListChannelMessagesResponseTypeDef",
    "ListChannelModeratorsRequestRequestTypeDef",
    "ListChannelModeratorsResponseTypeDef",
    "ListChannelsModeratedByAppInstanceUserRequestRequestTypeDef",
    "ListChannelsModeratedByAppInstanceUserResponseTypeDef",
    "ListChannelsRequestRequestTypeDef",
    "ListChannelsResponseTypeDef",
    "ListMediaCapturePipelinesRequestRequestTypeDef",
    "ListMediaCapturePipelinesResponseTypeDef",
    "ListMeetingTagsRequestRequestTypeDef",
    "ListMeetingTagsResponseTypeDef",
    "ListMeetingsRequestRequestTypeDef",
    "ListMeetingsResponseTypeDef",
    "ListPhoneNumberOrdersRequestRequestTypeDef",
    "ListPhoneNumberOrdersResponseTypeDef",
    "ListPhoneNumbersRequestRequestTypeDef",
    "ListPhoneNumbersResponseTypeDef",
    "ListProxySessionsRequestRequestTypeDef",
    "ListProxySessionsResponseTypeDef",
    "ListRoomMembershipsRequestRequestTypeDef",
    "ListRoomMembershipsResponseTypeDef",
    "ListRoomsRequestRequestTypeDef",
    "ListRoomsResponseTypeDef",
    "ListSipMediaApplicationsRequestRequestTypeDef",
    "ListSipMediaApplicationsResponseTypeDef",
    "ListSipRulesRequestRequestTypeDef",
    "ListSipRulesResponseTypeDef",
    "ListSupportedPhoneNumberCountriesRequestRequestTypeDef",
    "ListSupportedPhoneNumberCountriesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListUsersRequestListUsersPaginateTypeDef",
    "ListUsersRequestRequestTypeDef",
    "ListUsersResponseTypeDef",
    "ListVoiceConnectorGroupsRequestRequestTypeDef",
    "ListVoiceConnectorGroupsResponseTypeDef",
    "ListVoiceConnectorTerminationCredentialsRequestRequestTypeDef",
    "ListVoiceConnectorTerminationCredentialsResponseTypeDef",
    "ListVoiceConnectorsRequestRequestTypeDef",
    "ListVoiceConnectorsResponseTypeDef",
    "LoggingConfigurationTypeDef",
    "LogoutUserRequestRequestTypeDef",
    "MediaCapturePipelineTypeDef",
    "MediaPlacementTypeDef",
    "MeetingNotificationConfigurationTypeDef",
    "MeetingTypeDef",
    "MemberErrorTypeDef",
    "MemberTypeDef",
    "MembershipItemTypeDef",
    "MessagingSessionEndpointTypeDef",
    "OrderedPhoneNumberTypeDef",
    "OriginationOutputTypeDef",
    "OriginationRouteTypeDef",
    "OriginationTypeDef",
    "PaginatorConfigTypeDef",
    "ParticipantTypeDef",
    "PhoneNumberAssociationTypeDef",
    "PhoneNumberCapabilitiesTypeDef",
    "PhoneNumberCountryTypeDef",
    "PhoneNumberErrorTypeDef",
    "PhoneNumberOrderTypeDef",
    "PhoneNumberTypeDef",
    "ProxySessionTypeDef",
    "ProxyTypeDef",
    "PutAppInstanceRetentionSettingsRequestRequestTypeDef",
    "PutAppInstanceRetentionSettingsResponseTypeDef",
    "PutAppInstanceStreamingConfigurationsRequestRequestTypeDef",
    "PutAppInstanceStreamingConfigurationsResponseTypeDef",
    "PutEventsConfigurationRequestRequestTypeDef",
    "PutEventsConfigurationResponseTypeDef",
    "PutRetentionSettingsRequestRequestTypeDef",
    "PutRetentionSettingsResponseTypeDef",
    "PutSipMediaApplicationLoggingConfigurationRequestRequestTypeDef",
    "PutSipMediaApplicationLoggingConfigurationResponseTypeDef",
    "PutVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef",
    "PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef",
    "PutVoiceConnectorLoggingConfigurationRequestRequestTypeDef",
    "PutVoiceConnectorLoggingConfigurationResponseTypeDef",
    "PutVoiceConnectorOriginationRequestRequestTypeDef",
    "PutVoiceConnectorOriginationResponseTypeDef",
    "PutVoiceConnectorProxyRequestRequestTypeDef",
    "PutVoiceConnectorProxyResponseTypeDef",
    "PutVoiceConnectorStreamingConfigurationRequestRequestTypeDef",
    "PutVoiceConnectorStreamingConfigurationResponseTypeDef",
    "PutVoiceConnectorTerminationCredentialsRequestRequestTypeDef",
    "PutVoiceConnectorTerminationRequestRequestTypeDef",
    "PutVoiceConnectorTerminationResponseTypeDef",
    "RedactChannelMessageRequestRequestTypeDef",
    "RedactChannelMessageResponseTypeDef",
    "RedactConversationMessageRequestRequestTypeDef",
    "RedactRoomMessageRequestRequestTypeDef",
    "RegenerateSecurityTokenRequestRequestTypeDef",
    "RegenerateSecurityTokenResponseTypeDef",
    "ResetPersonalPINRequestRequestTypeDef",
    "ResetPersonalPINResponseTypeDef",
    "ResponseMetadataTypeDef",
    "RestorePhoneNumberRequestRequestTypeDef",
    "RestorePhoneNumberResponseTypeDef",
    "RetentionSettingsTypeDef",
    "RoomMembershipTypeDef",
    "RoomRetentionSettingsTypeDef",
    "RoomTypeDef",
    "SearchAvailablePhoneNumbersRequestRequestTypeDef",
    "SearchAvailablePhoneNumbersResponseTypeDef",
    "SelectedVideoStreamsOutputTypeDef",
    "SelectedVideoStreamsTypeDef",
    "SelectedVideoStreamsUnionTypeDef",
    "SendChannelMessageRequestRequestTypeDef",
    "SendChannelMessageResponseTypeDef",
    "SigninDelegateGroupTypeDef",
    "SipMediaApplicationCallTypeDef",
    "SipMediaApplicationEndpointTypeDef",
    "SipMediaApplicationLoggingConfigurationTypeDef",
    "SipMediaApplicationTypeDef",
    "SipRuleTargetApplicationTypeDef",
    "SipRuleTypeDef",
    "SourceConfigurationOutputTypeDef",
    "SourceConfigurationTypeDef",
    "SourceConfigurationUnionTypeDef",
    "StartMeetingTranscriptionRequestRequestTypeDef",
    "StopMeetingTranscriptionRequestRequestTypeDef",
    "StreamingConfigurationOutputTypeDef",
    "StreamingConfigurationTypeDef",
    "StreamingNotificationTargetTypeDef",
    "TagAttendeeRequestRequestTypeDef",
    "TagMeetingRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TelephonySettingsTypeDef",
    "TerminationHealthTypeDef",
    "TerminationOutputTypeDef",
    "TerminationTypeDef",
    "TimestampTypeDef",
    "TranscriptionConfigurationTypeDef",
    "UntagAttendeeRequestRequestTypeDef",
    "UntagMeetingRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAccountRequestRequestTypeDef",
    "UpdateAccountResponseTypeDef",
    "UpdateAccountSettingsRequestRequestTypeDef",
    "UpdateAppInstanceRequestRequestTypeDef",
    "UpdateAppInstanceResponseTypeDef",
    "UpdateAppInstanceUserRequestRequestTypeDef",
    "UpdateAppInstanceUserResponseTypeDef",
    "UpdateBotRequestRequestTypeDef",
    "UpdateBotResponseTypeDef",
    "UpdateChannelMessageRequestRequestTypeDef",
    "UpdateChannelMessageResponseTypeDef",
    "UpdateChannelReadMarkerRequestRequestTypeDef",
    "UpdateChannelReadMarkerResponseTypeDef",
    "UpdateChannelRequestRequestTypeDef",
    "UpdateChannelResponseTypeDef",
    "UpdateGlobalSettingsRequestRequestTypeDef",
    "UpdatePhoneNumberRequestItemTypeDef",
    "UpdatePhoneNumberRequestRequestTypeDef",
    "UpdatePhoneNumberResponseTypeDef",
    "UpdatePhoneNumberSettingsRequestRequestTypeDef",
    "UpdateProxySessionRequestRequestTypeDef",
    "UpdateProxySessionResponseTypeDef",
    "UpdateRoomMembershipRequestRequestTypeDef",
    "UpdateRoomMembershipResponseTypeDef",
    "UpdateRoomRequestRequestTypeDef",
    "UpdateRoomResponseTypeDef",
    "UpdateSipMediaApplicationCallRequestRequestTypeDef",
    "UpdateSipMediaApplicationCallResponseTypeDef",
    "UpdateSipMediaApplicationRequestRequestTypeDef",
    "UpdateSipMediaApplicationResponseTypeDef",
    "UpdateSipRuleRequestRequestTypeDef",
    "UpdateSipRuleResponseTypeDef",
    "UpdateUserRequestItemTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "UpdateUserResponseTypeDef",
    "UpdateUserSettingsRequestRequestTypeDef",
    "UpdateVoiceConnectorGroupRequestRequestTypeDef",
    "UpdateVoiceConnectorGroupResponseTypeDef",
    "UpdateVoiceConnectorRequestRequestTypeDef",
    "UpdateVoiceConnectorResponseTypeDef",
    "UserErrorTypeDef",
    "UserSettingsTypeDef",
    "UserTypeDef",
    "ValidateE911AddressRequestRequestTypeDef",
    "ValidateE911AddressResponseTypeDef",
    "VideoArtifactsConfigurationTypeDef",
    "VoiceConnectorGroupTypeDef",
    "VoiceConnectorItemTypeDef",
    "VoiceConnectorSettingsTypeDef",
    "VoiceConnectorTypeDef",
)

class AccountSettingsTypeDef(TypedDict):
    DisableRemoteControl: NotRequired[bool]
    EnableDialOut: NotRequired[bool]

class SigninDelegateGroupTypeDef(TypedDict):
    GroupName: NotRequired[str]

class AddressTypeDef(TypedDict):
    streetName: NotRequired[str]
    streetSuffix: NotRequired[str]
    postDirectional: NotRequired[str]
    preDirectional: NotRequired[str]
    streetNumber: NotRequired[str]
    city: NotRequired[str]
    state: NotRequired[str]
    postalCode: NotRequired[str]
    postalCodePlus4: NotRequired[str]
    country: NotRequired[str]

class AlexaForBusinessMetadataTypeDef(TypedDict):
    IsAlexaForBusinessEnabled: NotRequired[bool]
    AlexaForBusinessRoomArn: NotRequired[str]

class IdentityTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]

class ChannelRetentionSettingsTypeDef(TypedDict):
    RetentionDays: NotRequired[int]

class AppInstanceStreamingConfigurationTypeDef(TypedDict):
    AppInstanceDataType: AppInstanceDataTypeType
    ResourceArn: str

class AppInstanceSummaryTypeDef(TypedDict):
    AppInstanceArn: NotRequired[str]
    Name: NotRequired[str]
    Metadata: NotRequired[str]

class AppInstanceTypeDef(TypedDict):
    AppInstanceArn: NotRequired[str]
    Name: NotRequired[str]
    Metadata: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]
    LastUpdatedTimestamp: NotRequired[datetime]

AppInstanceUserMembershipSummaryTypeDef = TypedDict(
    "AppInstanceUserMembershipSummaryTypeDef",
    {
        "Type": NotRequired[ChannelMembershipTypeType],
        "ReadMarkerTimestamp": NotRequired[datetime],
    },
)

class AppInstanceUserSummaryTypeDef(TypedDict):
    AppInstanceUserArn: NotRequired[str]
    Name: NotRequired[str]
    Metadata: NotRequired[str]

class AppInstanceUserTypeDef(TypedDict):
    AppInstanceUserArn: NotRequired[str]
    Name: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]
    Metadata: NotRequired[str]
    LastUpdatedTimestamp: NotRequired[datetime]

class AudioArtifactsConfigurationTypeDef(TypedDict):
    MuxType: AudioMuxTypeType

class ContentArtifactsConfigurationTypeDef(TypedDict):
    State: ArtifactsStateType
    MuxType: NotRequired[Literal["ContentOnly"]]

class VideoArtifactsConfigurationTypeDef(TypedDict):
    State: ArtifactsStateType
    MuxType: NotRequired[Literal["VideoOnly"]]

class AssociatePhoneNumberWithUserRequestRequestTypeDef(TypedDict):
    AccountId: str
    UserId: str
    E164PhoneNumber: str

class AssociatePhoneNumbersWithVoiceConnectorGroupRequestRequestTypeDef(TypedDict):
    VoiceConnectorGroupId: str
    E164PhoneNumbers: Sequence[str]
    ForceAssociate: NotRequired[bool]

class PhoneNumberErrorTypeDef(TypedDict):
    PhoneNumberId: NotRequired[str]
    ErrorCode: NotRequired[ErrorCodeType]
    ErrorMessage: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AssociatePhoneNumbersWithVoiceConnectorRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    E164PhoneNumbers: Sequence[str]
    ForceAssociate: NotRequired[bool]

class AttendeeTypeDef(TypedDict):
    ExternalUserId: NotRequired[str]
    AttendeeId: NotRequired[str]
    JoinToken: NotRequired[str]

class CreateAttendeeErrorTypeDef(TypedDict):
    ExternalUserId: NotRequired[str]
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]

class BatchCreateChannelMembershipErrorTypeDef(TypedDict):
    MemberArn: NotRequired[str]
    ErrorCode: NotRequired[ErrorCodeType]
    ErrorMessage: NotRequired[str]

BatchCreateChannelMembershipRequestRequestTypeDef = TypedDict(
    "BatchCreateChannelMembershipRequestRequestTypeDef",
    {
        "ChannelArn": str,
        "MemberArns": Sequence[str],
        "Type": NotRequired[ChannelMembershipTypeType],
        "ChimeBearer": NotRequired[str],
    },
)

class MembershipItemTypeDef(TypedDict):
    MemberId: NotRequired[str]
    Role: NotRequired[RoomMembershipRoleType]

class MemberErrorTypeDef(TypedDict):
    MemberId: NotRequired[str]
    ErrorCode: NotRequired[ErrorCodeType]
    ErrorMessage: NotRequired[str]

class BatchDeletePhoneNumberRequestRequestTypeDef(TypedDict):
    PhoneNumberIds: Sequence[str]

class BatchSuspendUserRequestRequestTypeDef(TypedDict):
    AccountId: str
    UserIdList: Sequence[str]

class UserErrorTypeDef(TypedDict):
    UserId: NotRequired[str]
    ErrorCode: NotRequired[ErrorCodeType]
    ErrorMessage: NotRequired[str]

class BatchUnsuspendUserRequestRequestTypeDef(TypedDict):
    AccountId: str
    UserIdList: Sequence[str]

class UpdatePhoneNumberRequestItemTypeDef(TypedDict):
    PhoneNumberId: str
    ProductType: NotRequired[PhoneNumberProductTypeType]
    CallingName: NotRequired[str]

class BotTypeDef(TypedDict):
    BotId: NotRequired[str]
    UserId: NotRequired[str]
    DisplayName: NotRequired[str]
    BotType: NotRequired[Literal["ChatBot"]]
    Disabled: NotRequired[bool]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]
    BotEmail: NotRequired[str]
    SecurityToken: NotRequired[str]

class BusinessCallingSettingsTypeDef(TypedDict):
    CdrBucket: NotRequired[str]

class CandidateAddressTypeDef(TypedDict):
    streetInfo: NotRequired[str]
    streetNumber: NotRequired[str]
    city: NotRequired[str]
    state: NotRequired[str]
    postalCode: NotRequired[str]
    postalCodePlus4: NotRequired[str]
    country: NotRequired[str]

class ChannelSummaryTypeDef(TypedDict):
    Name: NotRequired[str]
    ChannelArn: NotRequired[str]
    Mode: NotRequired[ChannelModeType]
    Privacy: NotRequired[ChannelPrivacyType]
    Metadata: NotRequired[str]
    LastMessageTimestamp: NotRequired[datetime]

class ConversationRetentionSettingsTypeDef(TypedDict):
    RetentionDays: NotRequired[int]

class CreateAccountRequestRequestTypeDef(TypedDict):
    Name: str

class CreateAppInstanceAdminRequestRequestTypeDef(TypedDict):
    AppInstanceAdminArn: str
    AppInstanceArn: str

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class CreateBotRequestRequestTypeDef(TypedDict):
    AccountId: str
    DisplayName: str
    Domain: NotRequired[str]

class CreateChannelBanRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    MemberArn: str
    ChimeBearer: NotRequired[str]

CreateChannelMembershipRequestRequestTypeDef = TypedDict(
    "CreateChannelMembershipRequestRequestTypeDef",
    {
        "ChannelArn": str,
        "MemberArn": str,
        "Type": ChannelMembershipTypeType,
        "ChimeBearer": NotRequired[str],
    },
)

class CreateChannelModeratorRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    ChannelModeratorArn: str
    ChimeBearer: NotRequired[str]

class CreateMeetingDialOutRequestRequestTypeDef(TypedDict):
    MeetingId: str
    FromPhoneNumber: str
    ToPhoneNumber: str
    JoinToken: str

class MeetingNotificationConfigurationTypeDef(TypedDict):
    SnsTopicArn: NotRequired[str]
    SqsQueueArn: NotRequired[str]

class CreatePhoneNumberOrderRequestRequestTypeDef(TypedDict):
    ProductType: PhoneNumberProductTypeType
    E164PhoneNumbers: Sequence[str]

class GeoMatchParamsTypeDef(TypedDict):
    Country: str
    AreaCode: str

class CreateRoomMembershipRequestRequestTypeDef(TypedDict):
    AccountId: str
    RoomId: str
    MemberId: str
    Role: NotRequired[RoomMembershipRoleType]

class CreateRoomRequestRequestTypeDef(TypedDict):
    AccountId: str
    Name: str
    ClientRequestToken: NotRequired[str]

class RoomTypeDef(TypedDict):
    RoomId: NotRequired[str]
    Name: NotRequired[str]
    AccountId: NotRequired[str]
    CreatedBy: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]

class CreateSipMediaApplicationCallRequestRequestTypeDef(TypedDict):
    FromPhoneNumber: str
    ToPhoneNumber: str
    SipMediaApplicationId: str
    SipHeaders: NotRequired[Mapping[str, str]]

class SipMediaApplicationCallTypeDef(TypedDict):
    TransactionId: NotRequired[str]

class SipMediaApplicationEndpointTypeDef(TypedDict):
    LambdaArn: NotRequired[str]

class SipRuleTargetApplicationTypeDef(TypedDict):
    SipMediaApplicationId: NotRequired[str]
    Priority: NotRequired[int]
    AwsRegion: NotRequired[str]

class CreateUserRequestRequestTypeDef(TypedDict):
    AccountId: str
    Username: NotRequired[str]
    Email: NotRequired[str]
    UserType: NotRequired[UserTypeType]

class VoiceConnectorItemTypeDef(TypedDict):
    VoiceConnectorId: str
    Priority: int

class CreateVoiceConnectorRequestRequestTypeDef(TypedDict):
    Name: str
    RequireEncryption: bool
    AwsRegion: NotRequired[VoiceConnectorAwsRegionType]

class VoiceConnectorTypeDef(TypedDict):
    VoiceConnectorId: NotRequired[str]
    AwsRegion: NotRequired[VoiceConnectorAwsRegionType]
    Name: NotRequired[str]
    OutboundHostName: NotRequired[str]
    RequireEncryption: NotRequired[bool]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]
    VoiceConnectorArn: NotRequired[str]

class CredentialTypeDef(TypedDict):
    Username: NotRequired[str]
    Password: NotRequired[str]

class DNISEmergencyCallingConfigurationTypeDef(TypedDict):
    EmergencyPhoneNumber: str
    CallingCountry: str
    TestPhoneNumber: NotRequired[str]

class DeleteAccountRequestRequestTypeDef(TypedDict):
    AccountId: str

class DeleteAppInstanceAdminRequestRequestTypeDef(TypedDict):
    AppInstanceAdminArn: str
    AppInstanceArn: str

class DeleteAppInstanceRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str

class DeleteAppInstanceStreamingConfigurationsRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str

class DeleteAppInstanceUserRequestRequestTypeDef(TypedDict):
    AppInstanceUserArn: str

class DeleteAttendeeRequestRequestTypeDef(TypedDict):
    MeetingId: str
    AttendeeId: str

class DeleteChannelBanRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    MemberArn: str
    ChimeBearer: NotRequired[str]

class DeleteChannelMembershipRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    MemberArn: str
    ChimeBearer: NotRequired[str]

class DeleteChannelMessageRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    MessageId: str
    ChimeBearer: NotRequired[str]

class DeleteChannelModeratorRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    ChannelModeratorArn: str
    ChimeBearer: NotRequired[str]

class DeleteChannelRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    ChimeBearer: NotRequired[str]

class DeleteEventsConfigurationRequestRequestTypeDef(TypedDict):
    AccountId: str
    BotId: str

class DeleteMediaCapturePipelineRequestRequestTypeDef(TypedDict):
    MediaPipelineId: str

class DeleteMeetingRequestRequestTypeDef(TypedDict):
    MeetingId: str

class DeletePhoneNumberRequestRequestTypeDef(TypedDict):
    PhoneNumberId: str

class DeleteProxySessionRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    ProxySessionId: str

class DeleteRoomMembershipRequestRequestTypeDef(TypedDict):
    AccountId: str
    RoomId: str
    MemberId: str

class DeleteRoomRequestRequestTypeDef(TypedDict):
    AccountId: str
    RoomId: str

class DeleteSipMediaApplicationRequestRequestTypeDef(TypedDict):
    SipMediaApplicationId: str

class DeleteSipRuleRequestRequestTypeDef(TypedDict):
    SipRuleId: str

class DeleteVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class DeleteVoiceConnectorGroupRequestRequestTypeDef(TypedDict):
    VoiceConnectorGroupId: str

class DeleteVoiceConnectorOriginationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class DeleteVoiceConnectorProxyRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class DeleteVoiceConnectorRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class DeleteVoiceConnectorStreamingConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class DeleteVoiceConnectorTerminationCredentialsRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    Usernames: Sequence[str]

class DeleteVoiceConnectorTerminationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class DescribeAppInstanceAdminRequestRequestTypeDef(TypedDict):
    AppInstanceAdminArn: str
    AppInstanceArn: str

class DescribeAppInstanceRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str

class DescribeAppInstanceUserRequestRequestTypeDef(TypedDict):
    AppInstanceUserArn: str

class DescribeChannelBanRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    MemberArn: str
    ChimeBearer: NotRequired[str]

class DescribeChannelMembershipForAppInstanceUserRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    AppInstanceUserArn: str
    ChimeBearer: NotRequired[str]

class DescribeChannelMembershipRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    MemberArn: str
    ChimeBearer: NotRequired[str]

class DescribeChannelModeratedByAppInstanceUserRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    AppInstanceUserArn: str
    ChimeBearer: NotRequired[str]

class DescribeChannelModeratorRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    ChannelModeratorArn: str
    ChimeBearer: NotRequired[str]

class DescribeChannelRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    ChimeBearer: NotRequired[str]

class DisassociatePhoneNumberFromUserRequestRequestTypeDef(TypedDict):
    AccountId: str
    UserId: str

class DisassociatePhoneNumbersFromVoiceConnectorGroupRequestRequestTypeDef(TypedDict):
    VoiceConnectorGroupId: str
    E164PhoneNumbers: Sequence[str]

class DisassociatePhoneNumbersFromVoiceConnectorRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    E164PhoneNumbers: Sequence[str]

class DisassociateSigninDelegateGroupsFromAccountRequestRequestTypeDef(TypedDict):
    AccountId: str
    GroupNames: Sequence[str]

EngineTranscribeMedicalSettingsTypeDef = TypedDict(
    "EngineTranscribeMedicalSettingsTypeDef",
    {
        "LanguageCode": Literal["en-US"],
        "Specialty": TranscribeMedicalSpecialtyType,
        "Type": TranscribeMedicalTypeType,
        "VocabularyName": NotRequired[str],
        "Region": NotRequired[TranscribeMedicalRegionType],
        "ContentIdentificationType": NotRequired[Literal["PHI"]],
    },
)

class EngineTranscribeSettingsTypeDef(TypedDict):
    LanguageCode: NotRequired[TranscribeLanguageCodeType]
    VocabularyFilterMethod: NotRequired[TranscribeVocabularyFilterMethodType]
    VocabularyFilterName: NotRequired[str]
    VocabularyName: NotRequired[str]
    Region: NotRequired[TranscribeRegionType]
    EnablePartialResultsStabilization: NotRequired[bool]
    PartialResultsStability: NotRequired[TranscribePartialResultsStabilityType]
    ContentIdentificationType: NotRequired[Literal["PII"]]
    ContentRedactionType: NotRequired[Literal["PII"]]
    PiiEntityTypes: NotRequired[str]
    LanguageModelName: NotRequired[str]
    IdentifyLanguage: NotRequired[bool]
    LanguageOptions: NotRequired[str]
    PreferredLanguage: NotRequired[TranscribeLanguageCodeType]
    VocabularyNames: NotRequired[str]
    VocabularyFilterNames: NotRequired[str]

class EventsConfigurationTypeDef(TypedDict):
    BotId: NotRequired[str]
    OutboundEventsHTTPSEndpoint: NotRequired[str]
    LambdaFunctionArn: NotRequired[str]

class GetAccountRequestRequestTypeDef(TypedDict):
    AccountId: str

class GetAccountSettingsRequestRequestTypeDef(TypedDict):
    AccountId: str

class GetAppInstanceRetentionSettingsRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str

class GetAppInstanceStreamingConfigurationsRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str

class GetAttendeeRequestRequestTypeDef(TypedDict):
    MeetingId: str
    AttendeeId: str

class GetBotRequestRequestTypeDef(TypedDict):
    AccountId: str
    BotId: str

class GetChannelMessageRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    MessageId: str
    ChimeBearer: NotRequired[str]

class GetEventsConfigurationRequestRequestTypeDef(TypedDict):
    AccountId: str
    BotId: str

class VoiceConnectorSettingsTypeDef(TypedDict):
    CdrBucket: NotRequired[str]

class GetMediaCapturePipelineRequestRequestTypeDef(TypedDict):
    MediaPipelineId: str

class GetMeetingRequestRequestTypeDef(TypedDict):
    MeetingId: str

class MessagingSessionEndpointTypeDef(TypedDict):
    Url: NotRequired[str]

class GetPhoneNumberOrderRequestRequestTypeDef(TypedDict):
    PhoneNumberOrderId: str

class GetPhoneNumberRequestRequestTypeDef(TypedDict):
    PhoneNumberId: str

class GetProxySessionRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    ProxySessionId: str

class GetRetentionSettingsRequestRequestTypeDef(TypedDict):
    AccountId: str

class GetRoomRequestRequestTypeDef(TypedDict):
    AccountId: str
    RoomId: str

class GetSipMediaApplicationLoggingConfigurationRequestRequestTypeDef(TypedDict):
    SipMediaApplicationId: str

class SipMediaApplicationLoggingConfigurationTypeDef(TypedDict):
    EnableSipMediaApplicationMessageLogs: NotRequired[bool]

class GetSipMediaApplicationRequestRequestTypeDef(TypedDict):
    SipMediaApplicationId: str

class GetSipRuleRequestRequestTypeDef(TypedDict):
    SipRuleId: str

class GetUserRequestRequestTypeDef(TypedDict):
    AccountId: str
    UserId: str

class GetUserSettingsRequestRequestTypeDef(TypedDict):
    AccountId: str
    UserId: str

class GetVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class GetVoiceConnectorGroupRequestRequestTypeDef(TypedDict):
    VoiceConnectorGroupId: str

class GetVoiceConnectorLoggingConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class LoggingConfigurationTypeDef(TypedDict):
    EnableSIPLogs: NotRequired[bool]
    EnableMediaMetricLogs: NotRequired[bool]

class GetVoiceConnectorOriginationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class GetVoiceConnectorProxyRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class ProxyTypeDef(TypedDict):
    DefaultSessionExpiryMinutes: NotRequired[int]
    Disabled: NotRequired[bool]
    FallBackPhoneNumber: NotRequired[str]
    PhoneNumberCountries: NotRequired[List[str]]

class GetVoiceConnectorRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class GetVoiceConnectorStreamingConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class GetVoiceConnectorTerminationHealthRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class TerminationHealthTypeDef(TypedDict):
    Timestamp: NotRequired[datetime]
    Source: NotRequired[str]

class GetVoiceConnectorTerminationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class TerminationOutputTypeDef(TypedDict):
    CpsLimit: NotRequired[int]
    DefaultPhoneNumber: NotRequired[str]
    CallingRegions: NotRequired[List[str]]
    CidrAllowedList: NotRequired[List[str]]
    Disabled: NotRequired[bool]

class InviteTypeDef(TypedDict):
    InviteId: NotRequired[str]
    Status: NotRequired[InviteStatusType]
    EmailAddress: NotRequired[str]
    EmailStatus: NotRequired[EmailStatusType]

class InviteUsersRequestRequestTypeDef(TypedDict):
    AccountId: str
    UserEmailList: Sequence[str]
    UserType: NotRequired[UserTypeType]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAccountsRequestRequestTypeDef(TypedDict):
    Name: NotRequired[str]
    UserEmail: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListAppInstanceAdminsRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListAppInstanceUsersRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListAppInstancesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListAttendeeTagsRequestRequestTypeDef(TypedDict):
    MeetingId: str
    AttendeeId: str

class ListAttendeesRequestRequestTypeDef(TypedDict):
    MeetingId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListBotsRequestRequestTypeDef(TypedDict):
    AccountId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListChannelBansRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ChimeBearer: NotRequired[str]

class ListChannelMembershipsForAppInstanceUserRequestRequestTypeDef(TypedDict):
    AppInstanceUserArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ChimeBearer: NotRequired[str]

ListChannelMembershipsRequestRequestTypeDef = TypedDict(
    "ListChannelMembershipsRequestRequestTypeDef",
    {
        "ChannelArn": str,
        "Type": NotRequired[ChannelMembershipTypeType],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "ChimeBearer": NotRequired[str],
    },
)
TimestampTypeDef = Union[datetime, str]

class ListChannelModeratorsRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ChimeBearer: NotRequired[str]

class ListChannelsModeratedByAppInstanceUserRequestRequestTypeDef(TypedDict):
    AppInstanceUserArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ChimeBearer: NotRequired[str]

class ListChannelsRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str
    Privacy: NotRequired[ChannelPrivacyType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ChimeBearer: NotRequired[str]

class ListMediaCapturePipelinesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListMeetingTagsRequestRequestTypeDef(TypedDict):
    MeetingId: str

class ListMeetingsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListPhoneNumberOrdersRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListPhoneNumbersRequestRequestTypeDef(TypedDict):
    Status: NotRequired[PhoneNumberStatusType]
    ProductType: NotRequired[PhoneNumberProductTypeType]
    FilterName: NotRequired[PhoneNumberAssociationNameType]
    FilterValue: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListProxySessionsRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    Status: NotRequired[ProxySessionStatusType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListRoomMembershipsRequestRequestTypeDef(TypedDict):
    AccountId: str
    RoomId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListRoomsRequestRequestTypeDef(TypedDict):
    AccountId: str
    MemberId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListSipMediaApplicationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListSipRulesRequestRequestTypeDef(TypedDict):
    SipMediaApplicationId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListSupportedPhoneNumberCountriesRequestRequestTypeDef(TypedDict):
    ProductType: PhoneNumberProductTypeType

class PhoneNumberCountryTypeDef(TypedDict):
    CountryCode: NotRequired[str]
    SupportedPhoneNumberTypes: NotRequired[List[PhoneNumberTypeType]]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str

class ListUsersRequestRequestTypeDef(TypedDict):
    AccountId: str
    UserEmail: NotRequired[str]
    UserType: NotRequired[UserTypeType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListVoiceConnectorGroupsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListVoiceConnectorTerminationCredentialsRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class ListVoiceConnectorsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class LogoutUserRequestRequestTypeDef(TypedDict):
    AccountId: str
    UserId: str

class MediaPlacementTypeDef(TypedDict):
    AudioHostUrl: NotRequired[str]
    AudioFallbackUrl: NotRequired[str]
    ScreenDataUrl: NotRequired[str]
    ScreenSharingUrl: NotRequired[str]
    ScreenViewingUrl: NotRequired[str]
    SignalingUrl: NotRequired[str]
    TurnControlUrl: NotRequired[str]
    EventIngestionUrl: NotRequired[str]

class MemberTypeDef(TypedDict):
    MemberId: NotRequired[str]
    MemberType: NotRequired[MemberTypeType]
    Email: NotRequired[str]
    FullName: NotRequired[str]
    AccountId: NotRequired[str]

class OrderedPhoneNumberTypeDef(TypedDict):
    E164PhoneNumber: NotRequired[str]
    Status: NotRequired[OrderedPhoneNumberStatusType]

OriginationRouteTypeDef = TypedDict(
    "OriginationRouteTypeDef",
    {
        "Host": NotRequired[str],
        "Port": NotRequired[int],
        "Protocol": NotRequired[OriginationRouteProtocolType],
        "Priority": NotRequired[int],
        "Weight": NotRequired[int],
    },
)

class ParticipantTypeDef(TypedDict):
    PhoneNumber: NotRequired[str]
    ProxyPhoneNumber: NotRequired[str]

class PhoneNumberAssociationTypeDef(TypedDict):
    Value: NotRequired[str]
    Name: NotRequired[PhoneNumberAssociationNameType]
    AssociatedTimestamp: NotRequired[datetime]

class PhoneNumberCapabilitiesTypeDef(TypedDict):
    InboundCall: NotRequired[bool]
    OutboundCall: NotRequired[bool]
    InboundSMS: NotRequired[bool]
    OutboundSMS: NotRequired[bool]
    InboundMMS: NotRequired[bool]
    OutboundMMS: NotRequired[bool]

class PutEventsConfigurationRequestRequestTypeDef(TypedDict):
    AccountId: str
    BotId: str
    OutboundEventsHTTPSEndpoint: NotRequired[str]
    LambdaFunctionArn: NotRequired[str]

class PutVoiceConnectorProxyRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    DefaultSessionExpiryMinutes: int
    PhoneNumberPoolCountries: Sequence[str]
    FallBackPhoneNumber: NotRequired[str]
    Disabled: NotRequired[bool]

class TerminationTypeDef(TypedDict):
    CpsLimit: NotRequired[int]
    DefaultPhoneNumber: NotRequired[str]
    CallingRegions: NotRequired[Sequence[str]]
    CidrAllowedList: NotRequired[Sequence[str]]
    Disabled: NotRequired[bool]

class RedactChannelMessageRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    MessageId: str
    ChimeBearer: NotRequired[str]

class RedactConversationMessageRequestRequestTypeDef(TypedDict):
    AccountId: str
    ConversationId: str
    MessageId: str

class RedactRoomMessageRequestRequestTypeDef(TypedDict):
    AccountId: str
    RoomId: str
    MessageId: str

class RegenerateSecurityTokenRequestRequestTypeDef(TypedDict):
    AccountId: str
    BotId: str

class ResetPersonalPINRequestRequestTypeDef(TypedDict):
    AccountId: str
    UserId: str

class RestorePhoneNumberRequestRequestTypeDef(TypedDict):
    PhoneNumberId: str

class RoomRetentionSettingsTypeDef(TypedDict):
    RetentionDays: NotRequired[int]

class SearchAvailablePhoneNumbersRequestRequestTypeDef(TypedDict):
    AreaCode: NotRequired[str]
    City: NotRequired[str]
    Country: NotRequired[str]
    State: NotRequired[str]
    TollFreePrefix: NotRequired[str]
    PhoneNumberType: NotRequired[PhoneNumberTypeType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class SelectedVideoStreamsOutputTypeDef(TypedDict):
    AttendeeIds: NotRequired[List[str]]
    ExternalUserIds: NotRequired[List[str]]

class SelectedVideoStreamsTypeDef(TypedDict):
    AttendeeIds: NotRequired[Sequence[str]]
    ExternalUserIds: NotRequired[Sequence[str]]

SendChannelMessageRequestRequestTypeDef = TypedDict(
    "SendChannelMessageRequestRequestTypeDef",
    {
        "ChannelArn": str,
        "Content": str,
        "Type": ChannelMessageTypeType,
        "Persistence": ChannelMessagePersistenceTypeType,
        "ClientRequestToken": str,
        "Metadata": NotRequired[str],
        "ChimeBearer": NotRequired[str],
    },
)

class StopMeetingTranscriptionRequestRequestTypeDef(TypedDict):
    MeetingId: str

class StreamingNotificationTargetTypeDef(TypedDict):
    NotificationTarget: NotificationTargetType

class TelephonySettingsTypeDef(TypedDict):
    InboundCalling: bool
    OutboundCalling: bool
    SMS: bool

class UntagAttendeeRequestRequestTypeDef(TypedDict):
    MeetingId: str
    AttendeeId: str
    TagKeys: Sequence[str]

class UntagMeetingRequestRequestTypeDef(TypedDict):
    MeetingId: str
    TagKeys: Sequence[str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]

class UpdateAccountRequestRequestTypeDef(TypedDict):
    AccountId: str
    Name: NotRequired[str]
    DefaultLicense: NotRequired[LicenseType]

class UpdateAppInstanceRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str
    Name: str
    Metadata: NotRequired[str]

class UpdateAppInstanceUserRequestRequestTypeDef(TypedDict):
    AppInstanceUserArn: str
    Name: str
    Metadata: NotRequired[str]

class UpdateBotRequestRequestTypeDef(TypedDict):
    AccountId: str
    BotId: str
    Disabled: NotRequired[bool]

class UpdateChannelMessageRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    MessageId: str
    Content: NotRequired[str]
    Metadata: NotRequired[str]
    ChimeBearer: NotRequired[str]

class UpdateChannelReadMarkerRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    ChimeBearer: NotRequired[str]

class UpdateChannelRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    Name: str
    Mode: ChannelModeType
    Metadata: NotRequired[str]
    ChimeBearer: NotRequired[str]

class UpdatePhoneNumberRequestRequestTypeDef(TypedDict):
    PhoneNumberId: str
    ProductType: NotRequired[PhoneNumberProductTypeType]
    CallingName: NotRequired[str]

class UpdatePhoneNumberSettingsRequestRequestTypeDef(TypedDict):
    CallingName: str

class UpdateProxySessionRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    ProxySessionId: str
    Capabilities: Sequence[CapabilityType]
    ExpiryMinutes: NotRequired[int]

class UpdateRoomMembershipRequestRequestTypeDef(TypedDict):
    AccountId: str
    RoomId: str
    MemberId: str
    Role: NotRequired[RoomMembershipRoleType]

class UpdateRoomRequestRequestTypeDef(TypedDict):
    AccountId: str
    RoomId: str
    Name: NotRequired[str]

class UpdateSipMediaApplicationCallRequestRequestTypeDef(TypedDict):
    SipMediaApplicationId: str
    TransactionId: str
    Arguments: Mapping[str, str]

class UpdateVoiceConnectorRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    Name: str
    RequireEncryption: bool

class ValidateE911AddressRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    StreetNumber: str
    StreetInfo: str
    City: str
    State: str
    Country: str
    PostalCode: str

class UpdateAccountSettingsRequestRequestTypeDef(TypedDict):
    AccountId: str
    AccountSettings: AccountSettingsTypeDef

class AccountTypeDef(TypedDict):
    AwsAccountId: str
    AccountId: str
    Name: str
    AccountType: NotRequired[AccountTypeType]
    CreatedTimestamp: NotRequired[datetime]
    DefaultLicense: NotRequired[LicenseType]
    SupportedLicenses: NotRequired[List[LicenseType]]
    AccountStatus: NotRequired[AccountStatusType]
    SigninDelegateGroups: NotRequired[List[SigninDelegateGroupTypeDef]]

class AssociateSigninDelegateGroupsWithAccountRequestRequestTypeDef(TypedDict):
    AccountId: str
    SigninDelegateGroups: Sequence[SigninDelegateGroupTypeDef]

UpdateUserRequestItemTypeDef = TypedDict(
    "UpdateUserRequestItemTypeDef",
    {
        "UserId": str,
        "LicenseType": NotRequired[LicenseType],
        "UserType": NotRequired[UserTypeType],
        "AlexaForBusinessMetadata": NotRequired[AlexaForBusinessMetadataTypeDef],
    },
)
UpdateUserRequestRequestTypeDef = TypedDict(
    "UpdateUserRequestRequestTypeDef",
    {
        "AccountId": str,
        "UserId": str,
        "LicenseType": NotRequired[LicenseType],
        "UserType": NotRequired[UserTypeType],
        "AlexaForBusinessMetadata": NotRequired[AlexaForBusinessMetadataTypeDef],
    },
)
UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "UserId": str,
        "AccountId": NotRequired[str],
        "PrimaryEmail": NotRequired[str],
        "PrimaryProvisionedNumber": NotRequired[str],
        "DisplayName": NotRequired[str],
        "LicenseType": NotRequired[LicenseType],
        "UserType": NotRequired[UserTypeType],
        "UserRegistrationStatus": NotRequired[RegistrationStatusType],
        "UserInvitationStatus": NotRequired[InviteStatusType],
        "RegisteredOn": NotRequired[datetime],
        "InvitedOn": NotRequired[datetime],
        "AlexaForBusinessMetadata": NotRequired[AlexaForBusinessMetadataTypeDef],
        "PersonalPIN": NotRequired[str],
    },
)

class AppInstanceAdminSummaryTypeDef(TypedDict):
    Admin: NotRequired[IdentityTypeDef]

class AppInstanceAdminTypeDef(TypedDict):
    Admin: NotRequired[IdentityTypeDef]
    AppInstanceArn: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]

BatchChannelMembershipsTypeDef = TypedDict(
    "BatchChannelMembershipsTypeDef",
    {
        "InvitedBy": NotRequired[IdentityTypeDef],
        "Type": NotRequired[ChannelMembershipTypeType],
        "Members": NotRequired[List[IdentityTypeDef]],
        "ChannelArn": NotRequired[str],
    },
)

class ChannelBanSummaryTypeDef(TypedDict):
    Member: NotRequired[IdentityTypeDef]

class ChannelBanTypeDef(TypedDict):
    Member: NotRequired[IdentityTypeDef]
    ChannelArn: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]
    CreatedBy: NotRequired[IdentityTypeDef]

class ChannelMembershipSummaryTypeDef(TypedDict):
    Member: NotRequired[IdentityTypeDef]

ChannelMembershipTypeDef = TypedDict(
    "ChannelMembershipTypeDef",
    {
        "InvitedBy": NotRequired[IdentityTypeDef],
        "Type": NotRequired[ChannelMembershipTypeType],
        "Member": NotRequired[IdentityTypeDef],
        "ChannelArn": NotRequired[str],
        "CreatedTimestamp": NotRequired[datetime],
        "LastUpdatedTimestamp": NotRequired[datetime],
    },
)
ChannelMessageSummaryTypeDef = TypedDict(
    "ChannelMessageSummaryTypeDef",
    {
        "MessageId": NotRequired[str],
        "Content": NotRequired[str],
        "Metadata": NotRequired[str],
        "Type": NotRequired[ChannelMessageTypeType],
        "CreatedTimestamp": NotRequired[datetime],
        "LastUpdatedTimestamp": NotRequired[datetime],
        "LastEditedTimestamp": NotRequired[datetime],
        "Sender": NotRequired[IdentityTypeDef],
        "Redacted": NotRequired[bool],
    },
)
ChannelMessageTypeDef = TypedDict(
    "ChannelMessageTypeDef",
    {
        "ChannelArn": NotRequired[str],
        "MessageId": NotRequired[str],
        "Content": NotRequired[str],
        "Metadata": NotRequired[str],
        "Type": NotRequired[ChannelMessageTypeType],
        "CreatedTimestamp": NotRequired[datetime],
        "LastEditedTimestamp": NotRequired[datetime],
        "LastUpdatedTimestamp": NotRequired[datetime],
        "Sender": NotRequired[IdentityTypeDef],
        "Redacted": NotRequired[bool],
        "Persistence": NotRequired[ChannelMessagePersistenceTypeType],
    },
)

class ChannelModeratorSummaryTypeDef(TypedDict):
    Moderator: NotRequired[IdentityTypeDef]

class ChannelModeratorTypeDef(TypedDict):
    Moderator: NotRequired[IdentityTypeDef]
    ChannelArn: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]
    CreatedBy: NotRequired[IdentityTypeDef]

class ChannelTypeDef(TypedDict):
    Name: NotRequired[str]
    ChannelArn: NotRequired[str]
    Mode: NotRequired[ChannelModeType]
    Privacy: NotRequired[ChannelPrivacyType]
    Metadata: NotRequired[str]
    CreatedBy: NotRequired[IdentityTypeDef]
    CreatedTimestamp: NotRequired[datetime]
    LastMessageTimestamp: NotRequired[datetime]
    LastUpdatedTimestamp: NotRequired[datetime]

class AppInstanceRetentionSettingsTypeDef(TypedDict):
    ChannelRetentionSettings: NotRequired[ChannelRetentionSettingsTypeDef]

class PutAppInstanceStreamingConfigurationsRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str
    AppInstanceStreamingConfigurations: Sequence[AppInstanceStreamingConfigurationTypeDef]

class ArtifactsConfigurationTypeDef(TypedDict):
    Audio: AudioArtifactsConfigurationTypeDef
    Video: VideoArtifactsConfigurationTypeDef
    Content: ContentArtifactsConfigurationTypeDef

class AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef(TypedDict):
    PhoneNumberErrors: List[PhoneNumberErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef(TypedDict):
    PhoneNumberErrors: List[PhoneNumberErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDeletePhoneNumberResponseTypeDef(TypedDict):
    PhoneNumberErrors: List[PhoneNumberErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchUpdatePhoneNumberResponseTypeDef(TypedDict):
    PhoneNumberErrors: List[PhoneNumberErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAppInstanceAdminResponseTypeDef(TypedDict):
    AppInstanceAdmin: IdentityTypeDef
    AppInstanceArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAppInstanceResponseTypeDef(TypedDict):
    AppInstanceArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAppInstanceUserResponseTypeDef(TypedDict):
    AppInstanceUserArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateChannelBanResponseTypeDef(TypedDict):
    ChannelArn: str
    Member: IdentityTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateChannelMembershipResponseTypeDef(TypedDict):
    ChannelArn: str
    Member: IdentityTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateChannelModeratorResponseTypeDef(TypedDict):
    ChannelArn: str
    ChannelModerator: IdentityTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateChannelResponseTypeDef(TypedDict):
    ChannelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMeetingDialOutResponseTypeDef(TypedDict):
    TransactionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAppInstanceResponseTypeDef(TypedDict):
    AppInstance: AppInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAppInstanceUserResponseTypeDef(TypedDict):
    AppInstanceUser: AppInstanceUserTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef(TypedDict):
    PhoneNumberErrors: List[PhoneNumberErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef(TypedDict):
    PhoneNumberErrors: List[PhoneNumberErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetAccountSettingsResponseTypeDef(TypedDict):
    AccountSettings: AccountSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAppInstanceStreamingConfigurationsResponseTypeDef(TypedDict):
    AppInstanceStreamingConfigurations: List[AppInstanceStreamingConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetPhoneNumberSettingsResponseTypeDef(TypedDict):
    CallingName: str
    CallingNameUpdatedTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ListAppInstanceUsersResponseTypeDef(TypedDict):
    AppInstanceArn: str
    AppInstanceUsers: List[AppInstanceUserSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAppInstancesResponseTypeDef(TypedDict):
    AppInstances: List[AppInstanceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListVoiceConnectorTerminationCredentialsResponseTypeDef(TypedDict):
    Usernames: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class PutAppInstanceStreamingConfigurationsResponseTypeDef(TypedDict):
    AppInstanceStreamingConfigurations: List[AppInstanceStreamingConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class RedactChannelMessageResponseTypeDef(TypedDict):
    ChannelArn: str
    MessageId: str
    ResponseMetadata: ResponseMetadataTypeDef

class SearchAvailablePhoneNumbersResponseTypeDef(TypedDict):
    E164PhoneNumbers: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class SendChannelMessageResponseTypeDef(TypedDict):
    ChannelArn: str
    MessageId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAppInstanceResponseTypeDef(TypedDict):
    AppInstanceArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAppInstanceUserResponseTypeDef(TypedDict):
    AppInstanceUserArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateChannelMessageResponseTypeDef(TypedDict):
    ChannelArn: str
    MessageId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateChannelReadMarkerResponseTypeDef(TypedDict):
    ChannelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateChannelResponseTypeDef(TypedDict):
    ChannelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAttendeeResponseTypeDef(TypedDict):
    Attendee: AttendeeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAttendeeResponseTypeDef(TypedDict):
    Attendee: AttendeeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAttendeesResponseTypeDef(TypedDict):
    Attendees: List[AttendeeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class BatchCreateAttendeeResponseTypeDef(TypedDict):
    Attendees: List[AttendeeTypeDef]
    Errors: List[CreateAttendeeErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchCreateRoomMembershipRequestRequestTypeDef(TypedDict):
    AccountId: str
    RoomId: str
    MembershipItemList: Sequence[MembershipItemTypeDef]

class BatchCreateRoomMembershipResponseTypeDef(TypedDict):
    Errors: List[MemberErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchSuspendUserResponseTypeDef(TypedDict):
    UserErrors: List[UserErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchUnsuspendUserResponseTypeDef(TypedDict):
    UserErrors: List[UserErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchUpdateUserResponseTypeDef(TypedDict):
    UserErrors: List[UserErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchUpdatePhoneNumberRequestRequestTypeDef(TypedDict):
    UpdatePhoneNumberRequestItems: Sequence[UpdatePhoneNumberRequestItemTypeDef]

class CreateBotResponseTypeDef(TypedDict):
    Bot: BotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetBotResponseTypeDef(TypedDict):
    Bot: BotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListBotsResponseTypeDef(TypedDict):
    Bots: List[BotTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class RegenerateSecurityTokenResponseTypeDef(TypedDict):
    Bot: BotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBotResponseTypeDef(TypedDict):
    Bot: BotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ValidateE911AddressResponseTypeDef(TypedDict):
    ValidationResult: int
    AddressExternalId: str
    Address: AddressTypeDef
    CandidateAddressList: List[CandidateAddressTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ChannelMembershipForAppInstanceUserSummaryTypeDef(TypedDict):
    ChannelSummary: NotRequired[ChannelSummaryTypeDef]
    AppInstanceUserMembershipSummary: NotRequired[AppInstanceUserMembershipSummaryTypeDef]

class ChannelModeratedByAppInstanceUserSummaryTypeDef(TypedDict):
    ChannelSummary: NotRequired[ChannelSummaryTypeDef]

class ListChannelsResponseTypeDef(TypedDict):
    Channels: List[ChannelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateAppInstanceRequestRequestTypeDef(TypedDict):
    Name: str
    ClientRequestToken: str
    Metadata: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateAppInstanceUserRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str
    AppInstanceUserId: str
    Name: str
    ClientRequestToken: str
    Metadata: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateAttendeeRequestItemTypeDef(TypedDict):
    ExternalUserId: str
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateAttendeeRequestRequestTypeDef(TypedDict):
    MeetingId: str
    ExternalUserId: str
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateChannelRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str
    Name: str
    ClientRequestToken: str
    Mode: NotRequired[ChannelModeType]
    Privacy: NotRequired[ChannelPrivacyType]
    Metadata: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ChimeBearer: NotRequired[str]

class ListAttendeeTagsResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListMeetingTagsResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagAttendeeRequestRequestTypeDef(TypedDict):
    MeetingId: str
    AttendeeId: str
    Tags: Sequence[TagTypeDef]

class TagMeetingRequestRequestTypeDef(TypedDict):
    MeetingId: str
    Tags: Sequence[TagTypeDef]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]

class CreateMeetingRequestRequestTypeDef(TypedDict):
    ClientRequestToken: str
    ExternalMeetingId: NotRequired[str]
    MeetingHostId: NotRequired[str]
    MediaRegion: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    NotificationsConfiguration: NotRequired[MeetingNotificationConfigurationTypeDef]

class CreateProxySessionRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    ParticipantPhoneNumbers: Sequence[str]
    Capabilities: Sequence[CapabilityType]
    Name: NotRequired[str]
    ExpiryMinutes: NotRequired[int]
    NumberSelectionBehavior: NotRequired[NumberSelectionBehaviorType]
    GeoMatchLevel: NotRequired[GeoMatchLevelType]
    GeoMatchParams: NotRequired[GeoMatchParamsTypeDef]

class CreateRoomResponseTypeDef(TypedDict):
    Room: RoomTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetRoomResponseTypeDef(TypedDict):
    Room: RoomTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListRoomsResponseTypeDef(TypedDict):
    Rooms: List[RoomTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateRoomResponseTypeDef(TypedDict):
    Room: RoomTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSipMediaApplicationCallResponseTypeDef(TypedDict):
    SipMediaApplicationCall: SipMediaApplicationCallTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSipMediaApplicationCallResponseTypeDef(TypedDict):
    SipMediaApplicationCall: SipMediaApplicationCallTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSipMediaApplicationRequestRequestTypeDef(TypedDict):
    AwsRegion: str
    Name: str
    Endpoints: Sequence[SipMediaApplicationEndpointTypeDef]

class SipMediaApplicationTypeDef(TypedDict):
    SipMediaApplicationId: NotRequired[str]
    AwsRegion: NotRequired[str]
    Name: NotRequired[str]
    Endpoints: NotRequired[List[SipMediaApplicationEndpointTypeDef]]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]

class UpdateSipMediaApplicationRequestRequestTypeDef(TypedDict):
    SipMediaApplicationId: str
    Name: NotRequired[str]
    Endpoints: NotRequired[Sequence[SipMediaApplicationEndpointTypeDef]]

class CreateSipRuleRequestRequestTypeDef(TypedDict):
    Name: str
    TriggerType: SipRuleTriggerTypeType
    TriggerValue: str
    TargetApplications: Sequence[SipRuleTargetApplicationTypeDef]
    Disabled: NotRequired[bool]

class SipRuleTypeDef(TypedDict):
    SipRuleId: NotRequired[str]
    Name: NotRequired[str]
    Disabled: NotRequired[bool]
    TriggerType: NotRequired[SipRuleTriggerTypeType]
    TriggerValue: NotRequired[str]
    TargetApplications: NotRequired[List[SipRuleTargetApplicationTypeDef]]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]

class UpdateSipRuleRequestRequestTypeDef(TypedDict):
    SipRuleId: str
    Name: str
    Disabled: NotRequired[bool]
    TargetApplications: NotRequired[Sequence[SipRuleTargetApplicationTypeDef]]

class CreateVoiceConnectorGroupRequestRequestTypeDef(TypedDict):
    Name: str
    VoiceConnectorItems: NotRequired[Sequence[VoiceConnectorItemTypeDef]]

class UpdateVoiceConnectorGroupRequestRequestTypeDef(TypedDict):
    VoiceConnectorGroupId: str
    Name: str
    VoiceConnectorItems: Sequence[VoiceConnectorItemTypeDef]

class VoiceConnectorGroupTypeDef(TypedDict):
    VoiceConnectorGroupId: NotRequired[str]
    Name: NotRequired[str]
    VoiceConnectorItems: NotRequired[List[VoiceConnectorItemTypeDef]]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]
    VoiceConnectorGroupArn: NotRequired[str]

class CreateVoiceConnectorResponseTypeDef(TypedDict):
    VoiceConnector: VoiceConnectorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceConnectorResponseTypeDef(TypedDict):
    VoiceConnector: VoiceConnectorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListVoiceConnectorsResponseTypeDef(TypedDict):
    VoiceConnectors: List[VoiceConnectorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateVoiceConnectorResponseTypeDef(TypedDict):
    VoiceConnector: VoiceConnectorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorTerminationCredentialsRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    Credentials: NotRequired[Sequence[CredentialTypeDef]]

class EmergencyCallingConfigurationOutputTypeDef(TypedDict):
    DNIS: NotRequired[List[DNISEmergencyCallingConfigurationTypeDef]]

class EmergencyCallingConfigurationTypeDef(TypedDict):
    DNIS: NotRequired[Sequence[DNISEmergencyCallingConfigurationTypeDef]]

class TranscriptionConfigurationTypeDef(TypedDict):
    EngineTranscribeSettings: NotRequired[EngineTranscribeSettingsTypeDef]
    EngineTranscribeMedicalSettings: NotRequired[EngineTranscribeMedicalSettingsTypeDef]

class GetEventsConfigurationResponseTypeDef(TypedDict):
    EventsConfiguration: EventsConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutEventsConfigurationResponseTypeDef(TypedDict):
    EventsConfiguration: EventsConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetGlobalSettingsResponseTypeDef(TypedDict):
    BusinessCalling: BusinessCallingSettingsTypeDef
    VoiceConnector: VoiceConnectorSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGlobalSettingsRequestRequestTypeDef(TypedDict):
    BusinessCalling: NotRequired[BusinessCallingSettingsTypeDef]
    VoiceConnector: NotRequired[VoiceConnectorSettingsTypeDef]

class GetMessagingSessionEndpointResponseTypeDef(TypedDict):
    Endpoint: MessagingSessionEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSipMediaApplicationLoggingConfigurationResponseTypeDef(TypedDict):
    SipMediaApplicationLoggingConfiguration: SipMediaApplicationLoggingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutSipMediaApplicationLoggingConfigurationRequestRequestTypeDef(TypedDict):
    SipMediaApplicationId: str
    SipMediaApplicationLoggingConfiguration: NotRequired[
        SipMediaApplicationLoggingConfigurationTypeDef
    ]

class PutSipMediaApplicationLoggingConfigurationResponseTypeDef(TypedDict):
    SipMediaApplicationLoggingConfiguration: SipMediaApplicationLoggingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceConnectorLoggingConfigurationResponseTypeDef(TypedDict):
    LoggingConfiguration: LoggingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorLoggingConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    LoggingConfiguration: LoggingConfigurationTypeDef

class PutVoiceConnectorLoggingConfigurationResponseTypeDef(TypedDict):
    LoggingConfiguration: LoggingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceConnectorProxyResponseTypeDef(TypedDict):
    Proxy: ProxyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorProxyResponseTypeDef(TypedDict):
    Proxy: ProxyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceConnectorTerminationHealthResponseTypeDef(TypedDict):
    TerminationHealth: TerminationHealthTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceConnectorTerminationResponseTypeDef(TypedDict):
    Termination: TerminationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorTerminationResponseTypeDef(TypedDict):
    Termination: TerminationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class InviteUsersResponseTypeDef(TypedDict):
    Invites: List[InviteTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListAccountsRequestListAccountsPaginateTypeDef(TypedDict):
    Name: NotRequired[str]
    UserEmail: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListUsersRequestListUsersPaginateTypeDef(TypedDict):
    AccountId: str
    UserEmail: NotRequired[str]
    UserType: NotRequired[UserTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListChannelMessagesRequestRequestTypeDef(TypedDict):
    ChannelArn: str
    SortOrder: NotRequired[SortOrderType]
    NotBefore: NotRequired[TimestampTypeDef]
    NotAfter: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ChimeBearer: NotRequired[str]

class ListSupportedPhoneNumberCountriesResponseTypeDef(TypedDict):
    PhoneNumberCountries: List[PhoneNumberCountryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class MeetingTypeDef(TypedDict):
    MeetingId: NotRequired[str]
    ExternalMeetingId: NotRequired[str]
    MediaPlacement: NotRequired[MediaPlacementTypeDef]
    MediaRegion: NotRequired[str]

class RoomMembershipTypeDef(TypedDict):
    RoomId: NotRequired[str]
    Member: NotRequired[MemberTypeDef]
    Role: NotRequired[RoomMembershipRoleType]
    InvitedBy: NotRequired[str]
    UpdatedTimestamp: NotRequired[datetime]

class PhoneNumberOrderTypeDef(TypedDict):
    PhoneNumberOrderId: NotRequired[str]
    ProductType: NotRequired[PhoneNumberProductTypeType]
    Status: NotRequired[PhoneNumberOrderStatusType]
    OrderedPhoneNumbers: NotRequired[List[OrderedPhoneNumberTypeDef]]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]

class OriginationOutputTypeDef(TypedDict):
    Routes: NotRequired[List[OriginationRouteTypeDef]]
    Disabled: NotRequired[bool]

class OriginationTypeDef(TypedDict):
    Routes: NotRequired[Sequence[OriginationRouteTypeDef]]
    Disabled: NotRequired[bool]

class ProxySessionTypeDef(TypedDict):
    VoiceConnectorId: NotRequired[str]
    ProxySessionId: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[ProxySessionStatusType]
    ExpiryMinutes: NotRequired[int]
    Capabilities: NotRequired[List[CapabilityType]]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]
    EndedTimestamp: NotRequired[datetime]
    Participants: NotRequired[List[ParticipantTypeDef]]
    NumberSelectionBehavior: NotRequired[NumberSelectionBehaviorType]
    GeoMatchLevel: NotRequired[GeoMatchLevelType]
    GeoMatchParams: NotRequired[GeoMatchParamsTypeDef]

PhoneNumberTypeDef = TypedDict(
    "PhoneNumberTypeDef",
    {
        "PhoneNumberId": NotRequired[str],
        "E164PhoneNumber": NotRequired[str],
        "Country": NotRequired[str],
        "Type": NotRequired[PhoneNumberTypeType],
        "ProductType": NotRequired[PhoneNumberProductTypeType],
        "Status": NotRequired[PhoneNumberStatusType],
        "Capabilities": NotRequired[PhoneNumberCapabilitiesTypeDef],
        "Associations": NotRequired[List[PhoneNumberAssociationTypeDef]],
        "CallingName": NotRequired[str],
        "CallingNameStatus": NotRequired[CallingNameStatusType],
        "CreatedTimestamp": NotRequired[datetime],
        "UpdatedTimestamp": NotRequired[datetime],
        "DeletionTimestamp": NotRequired[datetime],
    },
)

class PutVoiceConnectorTerminationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    Termination: TerminationTypeDef

class RetentionSettingsTypeDef(TypedDict):
    RoomRetentionSettings: NotRequired[RoomRetentionSettingsTypeDef]
    ConversationRetentionSettings: NotRequired[ConversationRetentionSettingsTypeDef]

class SourceConfigurationOutputTypeDef(TypedDict):
    SelectedVideoStreams: NotRequired[SelectedVideoStreamsOutputTypeDef]

SelectedVideoStreamsUnionTypeDef = Union[
    SelectedVideoStreamsTypeDef, SelectedVideoStreamsOutputTypeDef
]

class StreamingConfigurationOutputTypeDef(TypedDict):
    DataRetentionInHours: int
    Disabled: NotRequired[bool]
    StreamingNotificationTargets: NotRequired[List[StreamingNotificationTargetTypeDef]]

class StreamingConfigurationTypeDef(TypedDict):
    DataRetentionInHours: int
    Disabled: NotRequired[bool]
    StreamingNotificationTargets: NotRequired[Sequence[StreamingNotificationTargetTypeDef]]

class UserSettingsTypeDef(TypedDict):
    Telephony: TelephonySettingsTypeDef

class CreateAccountResponseTypeDef(TypedDict):
    Account: AccountTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAccountResponseTypeDef(TypedDict):
    Account: AccountTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAccountsResponseTypeDef(TypedDict):
    Accounts: List[AccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateAccountResponseTypeDef(TypedDict):
    Account: AccountTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class BatchUpdateUserRequestRequestTypeDef(TypedDict):
    AccountId: str
    UpdateUserRequestItems: Sequence[UpdateUserRequestItemTypeDef]

class CreateUserResponseTypeDef(TypedDict):
    User: UserTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetUserResponseTypeDef(TypedDict):
    User: UserTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListUsersResponseTypeDef(TypedDict):
    Users: List[UserTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ResetPersonalPINResponseTypeDef(TypedDict):
    User: UserTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateUserResponseTypeDef(TypedDict):
    User: UserTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAppInstanceAdminsResponseTypeDef(TypedDict):
    AppInstanceArn: str
    AppInstanceAdmins: List[AppInstanceAdminSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeAppInstanceAdminResponseTypeDef(TypedDict):
    AppInstanceAdmin: AppInstanceAdminTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class BatchCreateChannelMembershipResponseTypeDef(TypedDict):
    BatchChannelMemberships: BatchChannelMembershipsTypeDef
    Errors: List[BatchCreateChannelMembershipErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListChannelBansResponseTypeDef(TypedDict):
    ChannelArn: str
    ChannelBans: List[ChannelBanSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeChannelBanResponseTypeDef(TypedDict):
    ChannelBan: ChannelBanTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListChannelMembershipsResponseTypeDef(TypedDict):
    ChannelArn: str
    ChannelMemberships: List[ChannelMembershipSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeChannelMembershipResponseTypeDef(TypedDict):
    ChannelMembership: ChannelMembershipTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListChannelMessagesResponseTypeDef(TypedDict):
    ChannelArn: str
    ChannelMessages: List[ChannelMessageSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetChannelMessageResponseTypeDef(TypedDict):
    ChannelMessage: ChannelMessageTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListChannelModeratorsResponseTypeDef(TypedDict):
    ChannelArn: str
    ChannelModerators: List[ChannelModeratorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeChannelModeratorResponseTypeDef(TypedDict):
    ChannelModerator: ChannelModeratorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeChannelResponseTypeDef(TypedDict):
    Channel: ChannelTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAppInstanceRetentionSettingsResponseTypeDef(TypedDict):
    AppInstanceRetentionSettings: AppInstanceRetentionSettingsTypeDef
    InitiateDeletionTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class PutAppInstanceRetentionSettingsRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str
    AppInstanceRetentionSettings: AppInstanceRetentionSettingsTypeDef

class PutAppInstanceRetentionSettingsResponseTypeDef(TypedDict):
    AppInstanceRetentionSettings: AppInstanceRetentionSettingsTypeDef
    InitiateDeletionTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeChannelMembershipForAppInstanceUserResponseTypeDef(TypedDict):
    ChannelMembership: ChannelMembershipForAppInstanceUserSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListChannelMembershipsForAppInstanceUserResponseTypeDef(TypedDict):
    ChannelMemberships: List[ChannelMembershipForAppInstanceUserSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeChannelModeratedByAppInstanceUserResponseTypeDef(TypedDict):
    Channel: ChannelModeratedByAppInstanceUserSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListChannelsModeratedByAppInstanceUserResponseTypeDef(TypedDict):
    Channels: List[ChannelModeratedByAppInstanceUserSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class BatchCreateAttendeeRequestRequestTypeDef(TypedDict):
    MeetingId: str
    Attendees: Sequence[CreateAttendeeRequestItemTypeDef]

class CreateMeetingWithAttendeesRequestRequestTypeDef(TypedDict):
    ClientRequestToken: str
    ExternalMeetingId: NotRequired[str]
    MeetingHostId: NotRequired[str]
    MediaRegion: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    NotificationsConfiguration: NotRequired[MeetingNotificationConfigurationTypeDef]
    Attendees: NotRequired[Sequence[CreateAttendeeRequestItemTypeDef]]

class CreateSipMediaApplicationResponseTypeDef(TypedDict):
    SipMediaApplication: SipMediaApplicationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSipMediaApplicationResponseTypeDef(TypedDict):
    SipMediaApplication: SipMediaApplicationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListSipMediaApplicationsResponseTypeDef(TypedDict):
    SipMediaApplications: List[SipMediaApplicationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateSipMediaApplicationResponseTypeDef(TypedDict):
    SipMediaApplication: SipMediaApplicationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSipRuleResponseTypeDef(TypedDict):
    SipRule: SipRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSipRuleResponseTypeDef(TypedDict):
    SipRule: SipRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListSipRulesResponseTypeDef(TypedDict):
    SipRules: List[SipRuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateSipRuleResponseTypeDef(TypedDict):
    SipRule: SipRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateVoiceConnectorGroupResponseTypeDef(TypedDict):
    VoiceConnectorGroup: VoiceConnectorGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceConnectorGroupResponseTypeDef(TypedDict):
    VoiceConnectorGroup: VoiceConnectorGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListVoiceConnectorGroupsResponseTypeDef(TypedDict):
    VoiceConnectorGroups: List[VoiceConnectorGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateVoiceConnectorGroupResponseTypeDef(TypedDict):
    VoiceConnectorGroup: VoiceConnectorGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef(TypedDict):
    EmergencyCallingConfiguration: EmergencyCallingConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef(TypedDict):
    EmergencyCallingConfiguration: EmergencyCallingConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    EmergencyCallingConfiguration: EmergencyCallingConfigurationTypeDef

class StartMeetingTranscriptionRequestRequestTypeDef(TypedDict):
    MeetingId: str
    TranscriptionConfiguration: TranscriptionConfigurationTypeDef

class CreateMeetingResponseTypeDef(TypedDict):
    Meeting: MeetingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMeetingWithAttendeesResponseTypeDef(TypedDict):
    Meeting: MeetingTypeDef
    Attendees: List[AttendeeTypeDef]
    Errors: List[CreateAttendeeErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetMeetingResponseTypeDef(TypedDict):
    Meeting: MeetingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListMeetingsResponseTypeDef(TypedDict):
    Meetings: List[MeetingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateRoomMembershipResponseTypeDef(TypedDict):
    RoomMembership: RoomMembershipTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListRoomMembershipsResponseTypeDef(TypedDict):
    RoomMemberships: List[RoomMembershipTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateRoomMembershipResponseTypeDef(TypedDict):
    RoomMembership: RoomMembershipTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePhoneNumberOrderResponseTypeDef(TypedDict):
    PhoneNumberOrder: PhoneNumberOrderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetPhoneNumberOrderResponseTypeDef(TypedDict):
    PhoneNumberOrder: PhoneNumberOrderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListPhoneNumberOrdersResponseTypeDef(TypedDict):
    PhoneNumberOrders: List[PhoneNumberOrderTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetVoiceConnectorOriginationResponseTypeDef(TypedDict):
    Origination: OriginationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorOriginationResponseTypeDef(TypedDict):
    Origination: OriginationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorOriginationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    Origination: OriginationTypeDef

class CreateProxySessionResponseTypeDef(TypedDict):
    ProxySession: ProxySessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetProxySessionResponseTypeDef(TypedDict):
    ProxySession: ProxySessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListProxySessionsResponseTypeDef(TypedDict):
    ProxySessions: List[ProxySessionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateProxySessionResponseTypeDef(TypedDict):
    ProxySession: ProxySessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetPhoneNumberResponseTypeDef(TypedDict):
    PhoneNumber: PhoneNumberTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListPhoneNumbersResponseTypeDef(TypedDict):
    PhoneNumbers: List[PhoneNumberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class RestorePhoneNumberResponseTypeDef(TypedDict):
    PhoneNumber: PhoneNumberTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePhoneNumberResponseTypeDef(TypedDict):
    PhoneNumber: PhoneNumberTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetRetentionSettingsResponseTypeDef(TypedDict):
    RetentionSettings: RetentionSettingsTypeDef
    InitiateDeletionTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class PutRetentionSettingsRequestRequestTypeDef(TypedDict):
    AccountId: str
    RetentionSettings: RetentionSettingsTypeDef

class PutRetentionSettingsResponseTypeDef(TypedDict):
    RetentionSettings: RetentionSettingsTypeDef
    InitiateDeletionTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ChimeSdkMeetingConfigurationOutputTypeDef(TypedDict):
    SourceConfiguration: NotRequired[SourceConfigurationOutputTypeDef]
    ArtifactsConfiguration: NotRequired[ArtifactsConfigurationTypeDef]

class SourceConfigurationTypeDef(TypedDict):
    SelectedVideoStreams: NotRequired[SelectedVideoStreamsUnionTypeDef]

class GetVoiceConnectorStreamingConfigurationResponseTypeDef(TypedDict):
    StreamingConfiguration: StreamingConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorStreamingConfigurationResponseTypeDef(TypedDict):
    StreamingConfiguration: StreamingConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorStreamingConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    StreamingConfiguration: StreamingConfigurationTypeDef

class GetUserSettingsResponseTypeDef(TypedDict):
    UserSettings: UserSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateUserSettingsRequestRequestTypeDef(TypedDict):
    AccountId: str
    UserId: str
    UserSettings: UserSettingsTypeDef

class MediaCapturePipelineTypeDef(TypedDict):
    MediaPipelineId: NotRequired[str]
    SourceType: NotRequired[Literal["ChimeSdkMeeting"]]
    SourceArn: NotRequired[str]
    Status: NotRequired[MediaPipelineStatusType]
    SinkType: NotRequired[Literal["S3Bucket"]]
    SinkArn: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]
    ChimeSdkMeetingConfiguration: NotRequired[ChimeSdkMeetingConfigurationOutputTypeDef]

SourceConfigurationUnionTypeDef = Union[
    SourceConfigurationTypeDef, SourceConfigurationOutputTypeDef
]

class CreateMediaCapturePipelineResponseTypeDef(TypedDict):
    MediaCapturePipeline: MediaCapturePipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetMediaCapturePipelineResponseTypeDef(TypedDict):
    MediaCapturePipeline: MediaCapturePipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListMediaCapturePipelinesResponseTypeDef(TypedDict):
    MediaCapturePipelines: List[MediaCapturePipelineTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ChimeSdkMeetingConfigurationTypeDef(TypedDict):
    SourceConfiguration: NotRequired[SourceConfigurationUnionTypeDef]
    ArtifactsConfiguration: NotRequired[ArtifactsConfigurationTypeDef]

class CreateMediaCapturePipelineRequestRequestTypeDef(TypedDict):
    SourceType: Literal["ChimeSdkMeeting"]
    SourceArn: str
    SinkType: Literal["S3Bucket"]
    SinkArn: str
    ClientRequestToken: NotRequired[str]
    ChimeSdkMeetingConfiguration: NotRequired[ChimeSdkMeetingConfigurationTypeDef]
