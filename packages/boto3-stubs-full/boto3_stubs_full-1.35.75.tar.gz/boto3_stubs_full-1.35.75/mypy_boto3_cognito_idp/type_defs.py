"""
Type annotations for cognito-idp service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/type_defs/)

Usage::

    ```python
    from mypy_boto3_cognito_idp.type_defs import RecoveryOptionTypeTypeDef

    data: RecoveryOptionTypeTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AccountTakeoverEventActionTypeType,
    AdvancedSecurityEnabledModeTypeType,
    AdvancedSecurityModeTypeType,
    AliasAttributeTypeType,
    AssetCategoryTypeType,
    AssetExtensionTypeType,
    AttributeDataTypeType,
    AuthFactorTypeType,
    AuthFlowTypeType,
    ChallengeNameType,
    ChallengeNameTypeType,
    ChallengeResponseType,
    ColorSchemeModeTypeType,
    CompromisedCredentialsEventActionTypeType,
    DefaultEmailOptionTypeType,
    DeletionProtectionTypeType,
    DeliveryMediumTypeType,
    DeviceRememberedStatusTypeType,
    DomainStatusTypeType,
    EmailSendingAccountTypeType,
    EventFilterTypeType,
    EventResponseTypeType,
    EventSourceNameType,
    EventTypeType,
    ExplicitAuthFlowsTypeType,
    FeedbackValueTypeType,
    IdentityProviderTypeTypeType,
    LogLevelType,
    MessageActionTypeType,
    OAuthFlowTypeType,
    PreTokenGenerationLambdaVersionTypeType,
    PreventUserExistenceErrorTypesType,
    RecoveryOptionNameTypeType,
    RiskDecisionTypeType,
    RiskLevelTypeType,
    StatusTypeType,
    TimeUnitsTypeType,
    UserImportJobStatusTypeType,
    UsernameAttributeTypeType,
    UserPoolMfaTypeType,
    UserPoolTierTypeType,
    UserStatusTypeType,
    UserVerificationTypeType,
    VerifiedAttributeTypeType,
    VerifySoftwareTokenResponseTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccountRecoverySettingTypeOutputTypeDef",
    "AccountRecoverySettingTypeTypeDef",
    "AccountTakeoverActionTypeTypeDef",
    "AccountTakeoverActionsTypeTypeDef",
    "AccountTakeoverRiskConfigurationTypeTypeDef",
    "AddCustomAttributesRequestRequestTypeDef",
    "AdminAddUserToGroupRequestRequestTypeDef",
    "AdminConfirmSignUpRequestRequestTypeDef",
    "AdminCreateUserConfigTypeTypeDef",
    "AdminCreateUserRequestRequestTypeDef",
    "AdminCreateUserResponseTypeDef",
    "AdminDeleteUserAttributesRequestRequestTypeDef",
    "AdminDeleteUserRequestRequestTypeDef",
    "AdminDisableProviderForUserRequestRequestTypeDef",
    "AdminDisableUserRequestRequestTypeDef",
    "AdminEnableUserRequestRequestTypeDef",
    "AdminForgetDeviceRequestRequestTypeDef",
    "AdminGetDeviceRequestRequestTypeDef",
    "AdminGetDeviceResponseTypeDef",
    "AdminGetUserRequestRequestTypeDef",
    "AdminGetUserResponseTypeDef",
    "AdminInitiateAuthRequestRequestTypeDef",
    "AdminInitiateAuthResponseTypeDef",
    "AdminLinkProviderForUserRequestRequestTypeDef",
    "AdminListDevicesRequestRequestTypeDef",
    "AdminListDevicesResponseTypeDef",
    "AdminListGroupsForUserRequestAdminListGroupsForUserPaginateTypeDef",
    "AdminListGroupsForUserRequestRequestTypeDef",
    "AdminListGroupsForUserResponseTypeDef",
    "AdminListUserAuthEventsRequestAdminListUserAuthEventsPaginateTypeDef",
    "AdminListUserAuthEventsRequestRequestTypeDef",
    "AdminListUserAuthEventsResponseTypeDef",
    "AdminRemoveUserFromGroupRequestRequestTypeDef",
    "AdminResetUserPasswordRequestRequestTypeDef",
    "AdminRespondToAuthChallengeRequestRequestTypeDef",
    "AdminRespondToAuthChallengeResponseTypeDef",
    "AdminSetUserMFAPreferenceRequestRequestTypeDef",
    "AdminSetUserPasswordRequestRequestTypeDef",
    "AdminSetUserSettingsRequestRequestTypeDef",
    "AdminUpdateAuthEventFeedbackRequestRequestTypeDef",
    "AdminUpdateDeviceStatusRequestRequestTypeDef",
    "AdminUpdateUserAttributesRequestRequestTypeDef",
    "AdminUserGlobalSignOutRequestRequestTypeDef",
    "AdvancedSecurityAdditionalFlowsTypeTypeDef",
    "AnalyticsConfigurationTypeTypeDef",
    "AnalyticsMetadataTypeTypeDef",
    "AssetTypeOutputTypeDef",
    "AssetTypeTypeDef",
    "AssetTypeUnionTypeDef",
    "AssociateSoftwareTokenRequestRequestTypeDef",
    "AssociateSoftwareTokenResponseTypeDef",
    "AttributeTypeTypeDef",
    "AuthEventTypeTypeDef",
    "AuthenticationResultTypeTypeDef",
    "BlobTypeDef",
    "ChallengeResponseTypeTypeDef",
    "ChangePasswordRequestRequestTypeDef",
    "CloudWatchLogsConfigurationTypeTypeDef",
    "CodeDeliveryDetailsTypeTypeDef",
    "CompleteWebAuthnRegistrationRequestRequestTypeDef",
    "CompromisedCredentialsActionsTypeTypeDef",
    "CompromisedCredentialsRiskConfigurationTypeOutputTypeDef",
    "CompromisedCredentialsRiskConfigurationTypeTypeDef",
    "ConfirmDeviceRequestRequestTypeDef",
    "ConfirmDeviceResponseTypeDef",
    "ConfirmForgotPasswordRequestRequestTypeDef",
    "ConfirmSignUpRequestRequestTypeDef",
    "ConfirmSignUpResponseTypeDef",
    "ContextDataTypeTypeDef",
    "CreateGroupRequestRequestTypeDef",
    "CreateGroupResponseTypeDef",
    "CreateIdentityProviderRequestRequestTypeDef",
    "CreateIdentityProviderResponseTypeDef",
    "CreateManagedLoginBrandingRequestRequestTypeDef",
    "CreateManagedLoginBrandingResponseTypeDef",
    "CreateResourceServerRequestRequestTypeDef",
    "CreateResourceServerResponseTypeDef",
    "CreateUserImportJobRequestRequestTypeDef",
    "CreateUserImportJobResponseTypeDef",
    "CreateUserPoolClientRequestRequestTypeDef",
    "CreateUserPoolClientResponseTypeDef",
    "CreateUserPoolDomainRequestRequestTypeDef",
    "CreateUserPoolDomainResponseTypeDef",
    "CreateUserPoolRequestRequestTypeDef",
    "CreateUserPoolResponseTypeDef",
    "CustomDomainConfigTypeTypeDef",
    "CustomEmailLambdaVersionConfigTypeTypeDef",
    "CustomSMSLambdaVersionConfigTypeTypeDef",
    "DeleteGroupRequestRequestTypeDef",
    "DeleteIdentityProviderRequestRequestTypeDef",
    "DeleteManagedLoginBrandingRequestRequestTypeDef",
    "DeleteResourceServerRequestRequestTypeDef",
    "DeleteUserAttributesRequestRequestTypeDef",
    "DeleteUserPoolClientRequestRequestTypeDef",
    "DeleteUserPoolDomainRequestRequestTypeDef",
    "DeleteUserPoolRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DeleteWebAuthnCredentialRequestRequestTypeDef",
    "DescribeIdentityProviderRequestRequestTypeDef",
    "DescribeIdentityProviderResponseTypeDef",
    "DescribeManagedLoginBrandingByClientRequestRequestTypeDef",
    "DescribeManagedLoginBrandingByClientResponseTypeDef",
    "DescribeManagedLoginBrandingRequestRequestTypeDef",
    "DescribeManagedLoginBrandingResponseTypeDef",
    "DescribeResourceServerRequestRequestTypeDef",
    "DescribeResourceServerResponseTypeDef",
    "DescribeRiskConfigurationRequestRequestTypeDef",
    "DescribeRiskConfigurationResponseTypeDef",
    "DescribeUserImportJobRequestRequestTypeDef",
    "DescribeUserImportJobResponseTypeDef",
    "DescribeUserPoolClientRequestRequestTypeDef",
    "DescribeUserPoolClientResponseTypeDef",
    "DescribeUserPoolDomainRequestRequestTypeDef",
    "DescribeUserPoolDomainResponseTypeDef",
    "DescribeUserPoolRequestRequestTypeDef",
    "DescribeUserPoolResponseTypeDef",
    "DeviceConfigurationTypeTypeDef",
    "DeviceSecretVerifierConfigTypeTypeDef",
    "DeviceTypeTypeDef",
    "DomainDescriptionTypeTypeDef",
    "EmailConfigurationTypeTypeDef",
    "EmailMfaConfigTypeTypeDef",
    "EmailMfaSettingsTypeTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EventContextDataTypeTypeDef",
    "EventFeedbackTypeTypeDef",
    "EventRiskTypeTypeDef",
    "FirehoseConfigurationTypeTypeDef",
    "ForgetDeviceRequestRequestTypeDef",
    "ForgotPasswordRequestRequestTypeDef",
    "ForgotPasswordResponseTypeDef",
    "GetCSVHeaderRequestRequestTypeDef",
    "GetCSVHeaderResponseTypeDef",
    "GetDeviceRequestRequestTypeDef",
    "GetDeviceResponseTypeDef",
    "GetGroupRequestRequestTypeDef",
    "GetGroupResponseTypeDef",
    "GetIdentityProviderByIdentifierRequestRequestTypeDef",
    "GetIdentityProviderByIdentifierResponseTypeDef",
    "GetLogDeliveryConfigurationRequestRequestTypeDef",
    "GetLogDeliveryConfigurationResponseTypeDef",
    "GetSigningCertificateRequestRequestTypeDef",
    "GetSigningCertificateResponseTypeDef",
    "GetUICustomizationRequestRequestTypeDef",
    "GetUICustomizationResponseTypeDef",
    "GetUserAttributeVerificationCodeRequestRequestTypeDef",
    "GetUserAttributeVerificationCodeResponseTypeDef",
    "GetUserAuthFactorsRequestRequestTypeDef",
    "GetUserAuthFactorsResponseTypeDef",
    "GetUserPoolMfaConfigRequestRequestTypeDef",
    "GetUserPoolMfaConfigResponseTypeDef",
    "GetUserRequestRequestTypeDef",
    "GetUserResponseTypeDef",
    "GlobalSignOutRequestRequestTypeDef",
    "GroupTypeTypeDef",
    "HttpHeaderTypeDef",
    "IdentityProviderTypeTypeDef",
    "InitiateAuthRequestRequestTypeDef",
    "InitiateAuthResponseTypeDef",
    "LambdaConfigTypeTypeDef",
    "ListDevicesRequestRequestTypeDef",
    "ListDevicesResponseTypeDef",
    "ListGroupsRequestListGroupsPaginateTypeDef",
    "ListGroupsRequestRequestTypeDef",
    "ListGroupsResponseTypeDef",
    "ListIdentityProvidersRequestListIdentityProvidersPaginateTypeDef",
    "ListIdentityProvidersRequestRequestTypeDef",
    "ListIdentityProvidersResponseTypeDef",
    "ListResourceServersRequestListResourceServersPaginateTypeDef",
    "ListResourceServersRequestRequestTypeDef",
    "ListResourceServersResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListUserImportJobsRequestRequestTypeDef",
    "ListUserImportJobsResponseTypeDef",
    "ListUserPoolClientsRequestListUserPoolClientsPaginateTypeDef",
    "ListUserPoolClientsRequestRequestTypeDef",
    "ListUserPoolClientsResponseTypeDef",
    "ListUserPoolsRequestListUserPoolsPaginateTypeDef",
    "ListUserPoolsRequestRequestTypeDef",
    "ListUserPoolsResponseTypeDef",
    "ListUsersInGroupRequestListUsersInGroupPaginateTypeDef",
    "ListUsersInGroupRequestRequestTypeDef",
    "ListUsersInGroupResponseTypeDef",
    "ListUsersRequestListUsersPaginateTypeDef",
    "ListUsersRequestRequestTypeDef",
    "ListUsersResponseTypeDef",
    "ListWebAuthnCredentialsRequestRequestTypeDef",
    "ListWebAuthnCredentialsResponseTypeDef",
    "LogConfigurationTypeTypeDef",
    "LogDeliveryConfigurationTypeTypeDef",
    "MFAOptionTypeTypeDef",
    "ManagedLoginBrandingTypeTypeDef",
    "MessageTemplateTypeTypeDef",
    "NewDeviceMetadataTypeTypeDef",
    "NotifyConfigurationTypeTypeDef",
    "NotifyEmailTypeTypeDef",
    "NumberAttributeConstraintsTypeTypeDef",
    "PaginatorConfigTypeDef",
    "PasswordPolicyTypeTypeDef",
    "PreTokenGenerationVersionConfigTypeTypeDef",
    "ProviderDescriptionTypeDef",
    "ProviderUserIdentifierTypeTypeDef",
    "RecoveryOptionTypeTypeDef",
    "ResendConfirmationCodeRequestRequestTypeDef",
    "ResendConfirmationCodeResponseTypeDef",
    "ResourceServerScopeTypeTypeDef",
    "ResourceServerTypeTypeDef",
    "RespondToAuthChallengeRequestRequestTypeDef",
    "RespondToAuthChallengeResponseTypeDef",
    "ResponseMetadataTypeDef",
    "RevokeTokenRequestRequestTypeDef",
    "RiskConfigurationTypeTypeDef",
    "RiskExceptionConfigurationTypeOutputTypeDef",
    "RiskExceptionConfigurationTypeTypeDef",
    "S3ConfigurationTypeTypeDef",
    "SMSMfaSettingsTypeTypeDef",
    "SchemaAttributeTypeTypeDef",
    "SetLogDeliveryConfigurationRequestRequestTypeDef",
    "SetLogDeliveryConfigurationResponseTypeDef",
    "SetRiskConfigurationRequestRequestTypeDef",
    "SetRiskConfigurationResponseTypeDef",
    "SetUICustomizationRequestRequestTypeDef",
    "SetUICustomizationResponseTypeDef",
    "SetUserMFAPreferenceRequestRequestTypeDef",
    "SetUserPoolMfaConfigRequestRequestTypeDef",
    "SetUserPoolMfaConfigResponseTypeDef",
    "SetUserSettingsRequestRequestTypeDef",
    "SignInPolicyTypeOutputTypeDef",
    "SignInPolicyTypeTypeDef",
    "SignInPolicyTypeUnionTypeDef",
    "SignUpRequestRequestTypeDef",
    "SignUpResponseTypeDef",
    "SmsConfigurationTypeTypeDef",
    "SmsMfaConfigTypeTypeDef",
    "SoftwareTokenMfaConfigTypeTypeDef",
    "SoftwareTokenMfaSettingsTypeTypeDef",
    "StartUserImportJobRequestRequestTypeDef",
    "StartUserImportJobResponseTypeDef",
    "StartWebAuthnRegistrationRequestRequestTypeDef",
    "StartWebAuthnRegistrationResponseTypeDef",
    "StopUserImportJobRequestRequestTypeDef",
    "StopUserImportJobResponseTypeDef",
    "StringAttributeConstraintsTypeTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TokenValidityUnitsTypeTypeDef",
    "UICustomizationTypeTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAuthEventFeedbackRequestRequestTypeDef",
    "UpdateDeviceStatusRequestRequestTypeDef",
    "UpdateGroupRequestRequestTypeDef",
    "UpdateGroupResponseTypeDef",
    "UpdateIdentityProviderRequestRequestTypeDef",
    "UpdateIdentityProviderResponseTypeDef",
    "UpdateManagedLoginBrandingRequestRequestTypeDef",
    "UpdateManagedLoginBrandingResponseTypeDef",
    "UpdateResourceServerRequestRequestTypeDef",
    "UpdateResourceServerResponseTypeDef",
    "UpdateUserAttributesRequestRequestTypeDef",
    "UpdateUserAttributesResponseTypeDef",
    "UpdateUserPoolClientRequestRequestTypeDef",
    "UpdateUserPoolClientResponseTypeDef",
    "UpdateUserPoolDomainRequestRequestTypeDef",
    "UpdateUserPoolDomainResponseTypeDef",
    "UpdateUserPoolRequestRequestTypeDef",
    "UserAttributeUpdateSettingsTypeOutputTypeDef",
    "UserAttributeUpdateSettingsTypeTypeDef",
    "UserContextDataTypeTypeDef",
    "UserImportJobTypeTypeDef",
    "UserPoolAddOnsTypeTypeDef",
    "UserPoolClientDescriptionTypeDef",
    "UserPoolClientTypeTypeDef",
    "UserPoolDescriptionTypeTypeDef",
    "UserPoolPolicyTypeOutputTypeDef",
    "UserPoolPolicyTypeTypeDef",
    "UserPoolTypeTypeDef",
    "UserTypeTypeDef",
    "UsernameConfigurationTypeTypeDef",
    "VerificationMessageTemplateTypeTypeDef",
    "VerifySoftwareTokenRequestRequestTypeDef",
    "VerifySoftwareTokenResponseTypeDef",
    "VerifyUserAttributeRequestRequestTypeDef",
    "WebAuthnConfigurationTypeTypeDef",
    "WebAuthnCredentialDescriptionTypeDef",
)


class RecoveryOptionTypeTypeDef(TypedDict):
    Priority: int
    Name: RecoveryOptionNameTypeType


class AccountTakeoverActionTypeTypeDef(TypedDict):
    Notify: bool
    EventAction: AccountTakeoverEventActionTypeType


class AdminAddUserToGroupRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str
    GroupName: str


class AdminConfirmSignUpRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str
    ClientMetadata: NotRequired[Mapping[str, str]]


class MessageTemplateTypeTypeDef(TypedDict):
    SMSMessage: NotRequired[str]
    EmailMessage: NotRequired[str]
    EmailSubject: NotRequired[str]


class AttributeTypeTypeDef(TypedDict):
    Name: str
    Value: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AdminDeleteUserAttributesRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str
    UserAttributeNames: Sequence[str]


class AdminDeleteUserRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str


class ProviderUserIdentifierTypeTypeDef(TypedDict):
    ProviderName: NotRequired[str]
    ProviderAttributeName: NotRequired[str]
    ProviderAttributeValue: NotRequired[str]


class AdminDisableUserRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str


class AdminEnableUserRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str


class AdminForgetDeviceRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str
    DeviceKey: str


class AdminGetDeviceRequestRequestTypeDef(TypedDict):
    DeviceKey: str
    UserPoolId: str
    Username: str


class AdminGetUserRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str


class MFAOptionTypeTypeDef(TypedDict):
    DeliveryMedium: NotRequired[DeliveryMediumTypeType]
    AttributeName: NotRequired[str]


class AnalyticsMetadataTypeTypeDef(TypedDict):
    AnalyticsEndpointId: NotRequired[str]


class AdminListDevicesRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str
    Limit: NotRequired[int]
    PaginationToken: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class AdminListGroupsForUserRequestRequestTypeDef(TypedDict):
    Username: str
    UserPoolId: str
    Limit: NotRequired[int]
    NextToken: NotRequired[str]


class GroupTypeTypeDef(TypedDict):
    GroupName: NotRequired[str]
    UserPoolId: NotRequired[str]
    Description: NotRequired[str]
    RoleArn: NotRequired[str]
    Precedence: NotRequired[int]
    LastModifiedDate: NotRequired[datetime]
    CreationDate: NotRequired[datetime]


class AdminListUserAuthEventsRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class AdminRemoveUserFromGroupRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str
    GroupName: str


class AdminResetUserPasswordRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str
    ClientMetadata: NotRequired[Mapping[str, str]]


class EmailMfaSettingsTypeTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    PreferredMfa: NotRequired[bool]


class SMSMfaSettingsTypeTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    PreferredMfa: NotRequired[bool]


class SoftwareTokenMfaSettingsTypeTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    PreferredMfa: NotRequired[bool]


class AdminSetUserPasswordRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str
    Password: str
    Permanent: NotRequired[bool]


class AdminUpdateAuthEventFeedbackRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str
    EventId: str
    FeedbackValue: FeedbackValueTypeType


class AdminUpdateDeviceStatusRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str
    DeviceKey: str
    DeviceRememberedStatus: NotRequired[DeviceRememberedStatusTypeType]


class AdminUserGlobalSignOutRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str


class AdvancedSecurityAdditionalFlowsTypeTypeDef(TypedDict):
    CustomAuthMode: NotRequired[AdvancedSecurityEnabledModeTypeType]


class AnalyticsConfigurationTypeTypeDef(TypedDict):
    ApplicationId: NotRequired[str]
    ApplicationArn: NotRequired[str]
    RoleArn: NotRequired[str]
    ExternalId: NotRequired[str]
    UserDataShared: NotRequired[bool]


class AssetTypeOutputTypeDef(TypedDict):
    Category: AssetCategoryTypeType
    ColorMode: ColorSchemeModeTypeType
    Extension: AssetExtensionTypeType
    Bytes: NotRequired[bytes]
    ResourceId: NotRequired[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class AssociateSoftwareTokenRequestRequestTypeDef(TypedDict):
    AccessToken: NotRequired[str]
    Session: NotRequired[str]


class ChallengeResponseTypeTypeDef(TypedDict):
    ChallengeName: NotRequired[ChallengeNameType]
    ChallengeResponse: NotRequired[ChallengeResponseType]


class EventContextDataTypeTypeDef(TypedDict):
    IpAddress: NotRequired[str]
    DeviceName: NotRequired[str]
    Timezone: NotRequired[str]
    City: NotRequired[str]
    Country: NotRequired[str]


class EventFeedbackTypeTypeDef(TypedDict):
    FeedbackValue: FeedbackValueTypeType
    Provider: str
    FeedbackDate: NotRequired[datetime]


class EventRiskTypeTypeDef(TypedDict):
    RiskDecision: NotRequired[RiskDecisionTypeType]
    RiskLevel: NotRequired[RiskLevelTypeType]
    CompromisedCredentialsDetected: NotRequired[bool]


class NewDeviceMetadataTypeTypeDef(TypedDict):
    DeviceKey: NotRequired[str]
    DeviceGroupKey: NotRequired[str]


class ChangePasswordRequestRequestTypeDef(TypedDict):
    ProposedPassword: str
    AccessToken: str
    PreviousPassword: NotRequired[str]


class CloudWatchLogsConfigurationTypeTypeDef(TypedDict):
    LogGroupArn: NotRequired[str]


class CodeDeliveryDetailsTypeTypeDef(TypedDict):
    Destination: NotRequired[str]
    DeliveryMedium: NotRequired[DeliveryMediumTypeType]
    AttributeName: NotRequired[str]


class CompleteWebAuthnRegistrationRequestRequestTypeDef(TypedDict):
    AccessToken: str
    Credential: Mapping[str, Any]


class CompromisedCredentialsActionsTypeTypeDef(TypedDict):
    EventAction: CompromisedCredentialsEventActionTypeType


class DeviceSecretVerifierConfigTypeTypeDef(TypedDict):
    PasswordVerifier: NotRequired[str]
    Salt: NotRequired[str]


class UserContextDataTypeTypeDef(TypedDict):
    IpAddress: NotRequired[str]
    EncodedData: NotRequired[str]


class HttpHeaderTypeDef(TypedDict):
    headerName: NotRequired[str]
    headerValue: NotRequired[str]


class CreateGroupRequestRequestTypeDef(TypedDict):
    GroupName: str
    UserPoolId: str
    Description: NotRequired[str]
    RoleArn: NotRequired[str]
    Precedence: NotRequired[int]


class CreateIdentityProviderRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    ProviderName: str
    ProviderType: IdentityProviderTypeTypeType
    ProviderDetails: Mapping[str, str]
    AttributeMapping: NotRequired[Mapping[str, str]]
    IdpIdentifiers: NotRequired[Sequence[str]]


class IdentityProviderTypeTypeDef(TypedDict):
    UserPoolId: NotRequired[str]
    ProviderName: NotRequired[str]
    ProviderType: NotRequired[IdentityProviderTypeTypeType]
    ProviderDetails: NotRequired[Dict[str, str]]
    AttributeMapping: NotRequired[Dict[str, str]]
    IdpIdentifiers: NotRequired[List[str]]
    LastModifiedDate: NotRequired[datetime]
    CreationDate: NotRequired[datetime]


class ResourceServerScopeTypeTypeDef(TypedDict):
    ScopeName: str
    ScopeDescription: str


class CreateUserImportJobRequestRequestTypeDef(TypedDict):
    JobName: str
    UserPoolId: str
    CloudWatchLogsRoleArn: str


class UserImportJobTypeTypeDef(TypedDict):
    JobName: NotRequired[str]
    JobId: NotRequired[str]
    UserPoolId: NotRequired[str]
    PreSignedUrl: NotRequired[str]
    CreationDate: NotRequired[datetime]
    StartDate: NotRequired[datetime]
    CompletionDate: NotRequired[datetime]
    Status: NotRequired[UserImportJobStatusTypeType]
    CloudWatchLogsRoleArn: NotRequired[str]
    ImportedUsers: NotRequired[int]
    SkippedUsers: NotRequired[int]
    FailedUsers: NotRequired[int]
    CompletionMessage: NotRequired[str]


class TokenValidityUnitsTypeTypeDef(TypedDict):
    AccessToken: NotRequired[TimeUnitsTypeType]
    IdToken: NotRequired[TimeUnitsTypeType]
    RefreshToken: NotRequired[TimeUnitsTypeType]


class CustomDomainConfigTypeTypeDef(TypedDict):
    CertificateArn: str


class DeviceConfigurationTypeTypeDef(TypedDict):
    ChallengeRequiredOnNewDevice: NotRequired[bool]
    DeviceOnlyRememberedOnUserPrompt: NotRequired[bool]


class EmailConfigurationTypeTypeDef(TypedDict):
    SourceArn: NotRequired[str]
    ReplyToEmailAddress: NotRequired[str]
    EmailSendingAccount: NotRequired[EmailSendingAccountTypeType]
    From: NotRequired[str]
    ConfigurationSet: NotRequired[str]


class SmsConfigurationTypeTypeDef(TypedDict):
    SnsCallerArn: str
    ExternalId: NotRequired[str]
    SnsRegion: NotRequired[str]


class UserAttributeUpdateSettingsTypeTypeDef(TypedDict):
    AttributesRequireVerificationBeforeUpdate: NotRequired[Sequence[VerifiedAttributeTypeType]]


class UsernameConfigurationTypeTypeDef(TypedDict):
    CaseSensitive: bool


class VerificationMessageTemplateTypeTypeDef(TypedDict):
    SmsMessage: NotRequired[str]
    EmailMessage: NotRequired[str]
    EmailSubject: NotRequired[str]
    EmailMessageByLink: NotRequired[str]
    EmailSubjectByLink: NotRequired[str]
    DefaultEmailOption: NotRequired[DefaultEmailOptionTypeType]


class CustomEmailLambdaVersionConfigTypeTypeDef(TypedDict):
    LambdaVersion: Literal["V1_0"]
    LambdaArn: str


class CustomSMSLambdaVersionConfigTypeTypeDef(TypedDict):
    LambdaVersion: Literal["V1_0"]
    LambdaArn: str


class DeleteGroupRequestRequestTypeDef(TypedDict):
    GroupName: str
    UserPoolId: str


class DeleteIdentityProviderRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    ProviderName: str


class DeleteManagedLoginBrandingRequestRequestTypeDef(TypedDict):
    ManagedLoginBrandingId: str
    UserPoolId: str


class DeleteResourceServerRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Identifier: str


class DeleteUserAttributesRequestRequestTypeDef(TypedDict):
    UserAttributeNames: Sequence[str]
    AccessToken: str


class DeleteUserPoolClientRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    ClientId: str


class DeleteUserPoolDomainRequestRequestTypeDef(TypedDict):
    Domain: str
    UserPoolId: str


class DeleteUserPoolRequestRequestTypeDef(TypedDict):
    UserPoolId: str


class DeleteUserRequestRequestTypeDef(TypedDict):
    AccessToken: str


class DeleteWebAuthnCredentialRequestRequestTypeDef(TypedDict):
    AccessToken: str
    CredentialId: str


class DescribeIdentityProviderRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    ProviderName: str


class DescribeManagedLoginBrandingByClientRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    ClientId: str
    ReturnMergedResources: NotRequired[bool]


class DescribeManagedLoginBrandingRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    ManagedLoginBrandingId: str
    ReturnMergedResources: NotRequired[bool]


class DescribeResourceServerRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Identifier: str


class DescribeRiskConfigurationRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    ClientId: NotRequired[str]


class DescribeUserImportJobRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    JobId: str


class DescribeUserPoolClientRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    ClientId: str


class DescribeUserPoolDomainRequestRequestTypeDef(TypedDict):
    Domain: str


class DescribeUserPoolRequestRequestTypeDef(TypedDict):
    UserPoolId: str


class EmailMfaConfigTypeTypeDef(TypedDict):
    Message: NotRequired[str]
    Subject: NotRequired[str]


class FirehoseConfigurationTypeTypeDef(TypedDict):
    StreamArn: NotRequired[str]


class ForgetDeviceRequestRequestTypeDef(TypedDict):
    DeviceKey: str
    AccessToken: NotRequired[str]


class GetCSVHeaderRequestRequestTypeDef(TypedDict):
    UserPoolId: str


class GetDeviceRequestRequestTypeDef(TypedDict):
    DeviceKey: str
    AccessToken: NotRequired[str]


class GetGroupRequestRequestTypeDef(TypedDict):
    GroupName: str
    UserPoolId: str


class GetIdentityProviderByIdentifierRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    IdpIdentifier: str


class GetLogDeliveryConfigurationRequestRequestTypeDef(TypedDict):
    UserPoolId: str


class GetSigningCertificateRequestRequestTypeDef(TypedDict):
    UserPoolId: str


class GetUICustomizationRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    ClientId: NotRequired[str]


class UICustomizationTypeTypeDef(TypedDict):
    UserPoolId: NotRequired[str]
    ClientId: NotRequired[str]
    ImageUrl: NotRequired[str]
    CSS: NotRequired[str]
    CSSVersion: NotRequired[str]
    LastModifiedDate: NotRequired[datetime]
    CreationDate: NotRequired[datetime]


class GetUserAttributeVerificationCodeRequestRequestTypeDef(TypedDict):
    AccessToken: str
    AttributeName: str
    ClientMetadata: NotRequired[Mapping[str, str]]


class GetUserAuthFactorsRequestRequestTypeDef(TypedDict):
    AccessToken: str


class GetUserPoolMfaConfigRequestRequestTypeDef(TypedDict):
    UserPoolId: str


class SoftwareTokenMfaConfigTypeTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class WebAuthnConfigurationTypeTypeDef(TypedDict):
    RelyingPartyId: NotRequired[str]
    UserVerification: NotRequired[UserVerificationTypeType]


class GetUserRequestRequestTypeDef(TypedDict):
    AccessToken: str


class GlobalSignOutRequestRequestTypeDef(TypedDict):
    AccessToken: str


class PreTokenGenerationVersionConfigTypeTypeDef(TypedDict):
    LambdaVersion: PreTokenGenerationLambdaVersionTypeType
    LambdaArn: str


class ListDevicesRequestRequestTypeDef(TypedDict):
    AccessToken: str
    Limit: NotRequired[int]
    PaginationToken: NotRequired[str]


class ListGroupsRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Limit: NotRequired[int]
    NextToken: NotRequired[str]


class ListIdentityProvidersRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ProviderDescriptionTypeDef(TypedDict):
    ProviderName: NotRequired[str]
    ProviderType: NotRequired[IdentityProviderTypeTypeType]
    LastModifiedDate: NotRequired[datetime]
    CreationDate: NotRequired[datetime]


class ListResourceServersRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class ListUserImportJobsRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    MaxResults: int
    PaginationToken: NotRequired[str]


class ListUserPoolClientsRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class UserPoolClientDescriptionTypeDef(TypedDict):
    ClientId: NotRequired[str]
    UserPoolId: NotRequired[str]
    ClientName: NotRequired[str]


class ListUserPoolsRequestRequestTypeDef(TypedDict):
    MaxResults: int
    NextToken: NotRequired[str]


class ListUsersInGroupRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    GroupName: str
    Limit: NotRequired[int]
    NextToken: NotRequired[str]


class ListUsersRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    AttributesToGet: NotRequired[Sequence[str]]
    Limit: NotRequired[int]
    PaginationToken: NotRequired[str]
    Filter: NotRequired[str]


class ListWebAuthnCredentialsRequestRequestTypeDef(TypedDict):
    AccessToken: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class WebAuthnCredentialDescriptionTypeDef(TypedDict):
    CredentialId: str
    FriendlyCredentialName: str
    RelyingPartyId: str
    AuthenticatorTransports: List[str]
    CreatedAt: datetime
    AuthenticatorAttachment: NotRequired[str]


class S3ConfigurationTypeTypeDef(TypedDict):
    BucketArn: NotRequired[str]


class NotifyEmailTypeTypeDef(TypedDict):
    Subject: str
    HtmlBody: NotRequired[str]
    TextBody: NotRequired[str]


class NumberAttributeConstraintsTypeTypeDef(TypedDict):
    MinValue: NotRequired[str]
    MaxValue: NotRequired[str]


class PasswordPolicyTypeTypeDef(TypedDict):
    MinimumLength: NotRequired[int]
    RequireUppercase: NotRequired[bool]
    RequireLowercase: NotRequired[bool]
    RequireNumbers: NotRequired[bool]
    RequireSymbols: NotRequired[bool]
    PasswordHistorySize: NotRequired[int]
    TemporaryPasswordValidityDays: NotRequired[int]


class RevokeTokenRequestRequestTypeDef(TypedDict):
    Token: str
    ClientId: str
    ClientSecret: NotRequired[str]


class RiskExceptionConfigurationTypeOutputTypeDef(TypedDict):
    BlockedIPRangeList: NotRequired[List[str]]
    SkippedIPRangeList: NotRequired[List[str]]


class RiskExceptionConfigurationTypeTypeDef(TypedDict):
    BlockedIPRangeList: NotRequired[Sequence[str]]
    SkippedIPRangeList: NotRequired[Sequence[str]]


class StringAttributeConstraintsTypeTypeDef(TypedDict):
    MinLength: NotRequired[str]
    MaxLength: NotRequired[str]


class SignInPolicyTypeOutputTypeDef(TypedDict):
    AllowedFirstAuthFactors: NotRequired[List[AuthFactorTypeType]]


class SignInPolicyTypeTypeDef(TypedDict):
    AllowedFirstAuthFactors: NotRequired[Sequence[AuthFactorTypeType]]


class StartUserImportJobRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    JobId: str


class StartWebAuthnRegistrationRequestRequestTypeDef(TypedDict):
    AccessToken: str


class StopUserImportJobRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    JobId: str


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateAuthEventFeedbackRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str
    EventId: str
    FeedbackToken: str
    FeedbackValue: FeedbackValueTypeType


class UpdateDeviceStatusRequestRequestTypeDef(TypedDict):
    AccessToken: str
    DeviceKey: str
    DeviceRememberedStatus: NotRequired[DeviceRememberedStatusTypeType]


class UpdateGroupRequestRequestTypeDef(TypedDict):
    GroupName: str
    UserPoolId: str
    Description: NotRequired[str]
    RoleArn: NotRequired[str]
    Precedence: NotRequired[int]


class UpdateIdentityProviderRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    ProviderName: str
    ProviderDetails: NotRequired[Mapping[str, str]]
    AttributeMapping: NotRequired[Mapping[str, str]]
    IdpIdentifiers: NotRequired[Sequence[str]]


class UserAttributeUpdateSettingsTypeOutputTypeDef(TypedDict):
    AttributesRequireVerificationBeforeUpdate: NotRequired[List[VerifiedAttributeTypeType]]


class VerifySoftwareTokenRequestRequestTypeDef(TypedDict):
    UserCode: str
    AccessToken: NotRequired[str]
    Session: NotRequired[str]
    FriendlyDeviceName: NotRequired[str]


class VerifyUserAttributeRequestRequestTypeDef(TypedDict):
    AccessToken: str
    AttributeName: str
    Code: str


class AccountRecoverySettingTypeOutputTypeDef(TypedDict):
    RecoveryMechanisms: NotRequired[List[RecoveryOptionTypeTypeDef]]


class AccountRecoverySettingTypeTypeDef(TypedDict):
    RecoveryMechanisms: NotRequired[Sequence[RecoveryOptionTypeTypeDef]]


class AccountTakeoverActionsTypeTypeDef(TypedDict):
    LowAction: NotRequired[AccountTakeoverActionTypeTypeDef]
    MediumAction: NotRequired[AccountTakeoverActionTypeTypeDef]
    HighAction: NotRequired[AccountTakeoverActionTypeTypeDef]


class AdminCreateUserConfigTypeTypeDef(TypedDict):
    AllowAdminCreateUserOnly: NotRequired[bool]
    UnusedAccountValidityDays: NotRequired[int]
    InviteMessageTemplate: NotRequired[MessageTemplateTypeTypeDef]


class AdminCreateUserRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str
    UserAttributes: NotRequired[Sequence[AttributeTypeTypeDef]]
    ValidationData: NotRequired[Sequence[AttributeTypeTypeDef]]
    TemporaryPassword: NotRequired[str]
    ForceAliasCreation: NotRequired[bool]
    MessageAction: NotRequired[MessageActionTypeType]
    DesiredDeliveryMediums: NotRequired[Sequence[DeliveryMediumTypeType]]
    ClientMetadata: NotRequired[Mapping[str, str]]


class AdminUpdateUserAttributesRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str
    UserAttributes: Sequence[AttributeTypeTypeDef]
    ClientMetadata: NotRequired[Mapping[str, str]]


class DeviceTypeTypeDef(TypedDict):
    DeviceKey: NotRequired[str]
    DeviceAttributes: NotRequired[List[AttributeTypeTypeDef]]
    DeviceCreateDate: NotRequired[datetime]
    DeviceLastModifiedDate: NotRequired[datetime]
    DeviceLastAuthenticatedDate: NotRequired[datetime]


class UpdateUserAttributesRequestRequestTypeDef(TypedDict):
    UserAttributes: Sequence[AttributeTypeTypeDef]
    AccessToken: str
    ClientMetadata: NotRequired[Mapping[str, str]]


class AssociateSoftwareTokenResponseTypeDef(TypedDict):
    SecretCode: str
    Session: str
    ResponseMetadata: ResponseMetadataTypeDef


class ConfirmDeviceResponseTypeDef(TypedDict):
    UserConfirmationNecessary: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ConfirmSignUpResponseTypeDef(TypedDict):
    Session: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUserPoolDomainResponseTypeDef(TypedDict):
    ManagedLoginVersion: int
    CloudFrontDomain: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetCSVHeaderResponseTypeDef(TypedDict):
    UserPoolId: str
    CSVHeader: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetSigningCertificateResponseTypeDef(TypedDict):
    Certificate: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetUserAuthFactorsResponseTypeDef(TypedDict):
    Username: str
    PreferredMfaSetting: str
    UserMFASettingList: List[str]
    ConfiguredUserAuthFactors: List[AuthFactorTypeType]
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class StartWebAuthnRegistrationResponseTypeDef(TypedDict):
    CredentialCreationOptions: Dict[str, Any]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateUserPoolDomainResponseTypeDef(TypedDict):
    ManagedLoginVersion: int
    CloudFrontDomain: str
    ResponseMetadata: ResponseMetadataTypeDef


class VerifySoftwareTokenResponseTypeDef(TypedDict):
    Status: VerifySoftwareTokenResponseTypeType
    Session: str
    ResponseMetadata: ResponseMetadataTypeDef


class AdminDisableProviderForUserRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    User: ProviderUserIdentifierTypeTypeDef


class AdminLinkProviderForUserRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    DestinationUser: ProviderUserIdentifierTypeTypeDef
    SourceUser: ProviderUserIdentifierTypeTypeDef


class AdminGetUserResponseTypeDef(TypedDict):
    Username: str
    UserAttributes: List[AttributeTypeTypeDef]
    UserCreateDate: datetime
    UserLastModifiedDate: datetime
    Enabled: bool
    UserStatus: UserStatusTypeType
    MFAOptions: List[MFAOptionTypeTypeDef]
    PreferredMfaSetting: str
    UserMFASettingList: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class AdminSetUserSettingsRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Username: str
    MFAOptions: Sequence[MFAOptionTypeTypeDef]


class GetUserResponseTypeDef(TypedDict):
    Username: str
    UserAttributes: List[AttributeTypeTypeDef]
    MFAOptions: List[MFAOptionTypeTypeDef]
    PreferredMfaSetting: str
    UserMFASettingList: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class SetUserSettingsRequestRequestTypeDef(TypedDict):
    AccessToken: str
    MFAOptions: Sequence[MFAOptionTypeTypeDef]


class UserTypeTypeDef(TypedDict):
    Username: NotRequired[str]
    Attributes: NotRequired[List[AttributeTypeTypeDef]]
    UserCreateDate: NotRequired[datetime]
    UserLastModifiedDate: NotRequired[datetime]
    Enabled: NotRequired[bool]
    UserStatus: NotRequired[UserStatusTypeType]
    MFAOptions: NotRequired[List[MFAOptionTypeTypeDef]]


class AdminListGroupsForUserRequestAdminListGroupsForUserPaginateTypeDef(TypedDict):
    Username: str
    UserPoolId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class AdminListUserAuthEventsRequestAdminListUserAuthEventsPaginateTypeDef(TypedDict):
    UserPoolId: str
    Username: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupsRequestListGroupsPaginateTypeDef(TypedDict):
    UserPoolId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIdentityProvidersRequestListIdentityProvidersPaginateTypeDef(TypedDict):
    UserPoolId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourceServersRequestListResourceServersPaginateTypeDef(TypedDict):
    UserPoolId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUserPoolClientsRequestListUserPoolClientsPaginateTypeDef(TypedDict):
    UserPoolId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUserPoolsRequestListUserPoolsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUsersInGroupRequestListUsersInGroupPaginateTypeDef(TypedDict):
    UserPoolId: str
    GroupName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUsersRequestListUsersPaginateTypeDef(TypedDict):
    UserPoolId: str
    AttributesToGet: NotRequired[Sequence[str]]
    Filter: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class AdminListGroupsForUserResponseTypeDef(TypedDict):
    Groups: List[GroupTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateGroupResponseTypeDef(TypedDict):
    Group: GroupTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetGroupResponseTypeDef(TypedDict):
    Group: GroupTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListGroupsResponseTypeDef(TypedDict):
    Groups: List[GroupTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateGroupResponseTypeDef(TypedDict):
    Group: GroupTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AdminSetUserMFAPreferenceRequestRequestTypeDef(TypedDict):
    Username: str
    UserPoolId: str
    SMSMfaSettings: NotRequired[SMSMfaSettingsTypeTypeDef]
    SoftwareTokenMfaSettings: NotRequired[SoftwareTokenMfaSettingsTypeTypeDef]
    EmailMfaSettings: NotRequired[EmailMfaSettingsTypeTypeDef]


class SetUserMFAPreferenceRequestRequestTypeDef(TypedDict):
    AccessToken: str
    SMSMfaSettings: NotRequired[SMSMfaSettingsTypeTypeDef]
    SoftwareTokenMfaSettings: NotRequired[SoftwareTokenMfaSettingsTypeTypeDef]
    EmailMfaSettings: NotRequired[EmailMfaSettingsTypeTypeDef]


class UserPoolAddOnsTypeTypeDef(TypedDict):
    AdvancedSecurityMode: AdvancedSecurityModeTypeType
    AdvancedSecurityAdditionalFlows: NotRequired[AdvancedSecurityAdditionalFlowsTypeTypeDef]


class ManagedLoginBrandingTypeTypeDef(TypedDict):
    ManagedLoginBrandingId: NotRequired[str]
    UserPoolId: NotRequired[str]
    UseCognitoProvidedValues: NotRequired[bool]
    Settings: NotRequired[Dict[str, Any]]
    Assets: NotRequired[List[AssetTypeOutputTypeDef]]
    CreationDate: NotRequired[datetime]
    LastModifiedDate: NotRequired[datetime]


class AssetTypeTypeDef(TypedDict):
    Category: AssetCategoryTypeType
    ColorMode: ColorSchemeModeTypeType
    Extension: AssetExtensionTypeType
    Bytes: NotRequired[BlobTypeDef]
    ResourceId: NotRequired[str]


class SetUICustomizationRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    ClientId: NotRequired[str]
    CSS: NotRequired[str]
    ImageFile: NotRequired[BlobTypeDef]


class AuthEventTypeTypeDef(TypedDict):
    EventId: NotRequired[str]
    EventType: NotRequired[EventTypeType]
    CreationDate: NotRequired[datetime]
    EventResponse: NotRequired[EventResponseTypeType]
    EventRisk: NotRequired[EventRiskTypeTypeDef]
    ChallengeResponses: NotRequired[List[ChallengeResponseTypeTypeDef]]
    EventContextData: NotRequired[EventContextDataTypeTypeDef]
    EventFeedback: NotRequired[EventFeedbackTypeTypeDef]


class AuthenticationResultTypeTypeDef(TypedDict):
    AccessToken: NotRequired[str]
    ExpiresIn: NotRequired[int]
    TokenType: NotRequired[str]
    RefreshToken: NotRequired[str]
    IdToken: NotRequired[str]
    NewDeviceMetadata: NotRequired[NewDeviceMetadataTypeTypeDef]


class ForgotPasswordResponseTypeDef(TypedDict):
    CodeDeliveryDetails: CodeDeliveryDetailsTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetUserAttributeVerificationCodeResponseTypeDef(TypedDict):
    CodeDeliveryDetails: CodeDeliveryDetailsTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ResendConfirmationCodeResponseTypeDef(TypedDict):
    CodeDeliveryDetails: CodeDeliveryDetailsTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SignUpResponseTypeDef(TypedDict):
    UserConfirmed: bool
    CodeDeliveryDetails: CodeDeliveryDetailsTypeTypeDef
    UserSub: str
    Session: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateUserAttributesResponseTypeDef(TypedDict):
    CodeDeliveryDetailsList: List[CodeDeliveryDetailsTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CompromisedCredentialsRiskConfigurationTypeOutputTypeDef(TypedDict):
    Actions: CompromisedCredentialsActionsTypeTypeDef
    EventFilter: NotRequired[List[EventFilterTypeType]]


class CompromisedCredentialsRiskConfigurationTypeTypeDef(TypedDict):
    Actions: CompromisedCredentialsActionsTypeTypeDef
    EventFilter: NotRequired[Sequence[EventFilterTypeType]]


class ConfirmDeviceRequestRequestTypeDef(TypedDict):
    AccessToken: str
    DeviceKey: str
    DeviceSecretVerifierConfig: NotRequired[DeviceSecretVerifierConfigTypeTypeDef]
    DeviceName: NotRequired[str]


class ConfirmForgotPasswordRequestRequestTypeDef(TypedDict):
    ClientId: str
    Username: str
    ConfirmationCode: str
    Password: str
    SecretHash: NotRequired[str]
    AnalyticsMetadata: NotRequired[AnalyticsMetadataTypeTypeDef]
    UserContextData: NotRequired[UserContextDataTypeTypeDef]
    ClientMetadata: NotRequired[Mapping[str, str]]


class ConfirmSignUpRequestRequestTypeDef(TypedDict):
    ClientId: str
    Username: str
    ConfirmationCode: str
    SecretHash: NotRequired[str]
    ForceAliasCreation: NotRequired[bool]
    AnalyticsMetadata: NotRequired[AnalyticsMetadataTypeTypeDef]
    UserContextData: NotRequired[UserContextDataTypeTypeDef]
    ClientMetadata: NotRequired[Mapping[str, str]]
    Session: NotRequired[str]


class ForgotPasswordRequestRequestTypeDef(TypedDict):
    ClientId: str
    Username: str
    SecretHash: NotRequired[str]
    UserContextData: NotRequired[UserContextDataTypeTypeDef]
    AnalyticsMetadata: NotRequired[AnalyticsMetadataTypeTypeDef]
    ClientMetadata: NotRequired[Mapping[str, str]]


class InitiateAuthRequestRequestTypeDef(TypedDict):
    AuthFlow: AuthFlowTypeType
    ClientId: str
    AuthParameters: NotRequired[Mapping[str, str]]
    ClientMetadata: NotRequired[Mapping[str, str]]
    AnalyticsMetadata: NotRequired[AnalyticsMetadataTypeTypeDef]
    UserContextData: NotRequired[UserContextDataTypeTypeDef]
    Session: NotRequired[str]


class ResendConfirmationCodeRequestRequestTypeDef(TypedDict):
    ClientId: str
    Username: str
    SecretHash: NotRequired[str]
    UserContextData: NotRequired[UserContextDataTypeTypeDef]
    AnalyticsMetadata: NotRequired[AnalyticsMetadataTypeTypeDef]
    ClientMetadata: NotRequired[Mapping[str, str]]


class RespondToAuthChallengeRequestRequestTypeDef(TypedDict):
    ClientId: str
    ChallengeName: ChallengeNameTypeType
    Session: NotRequired[str]
    ChallengeResponses: NotRequired[Mapping[str, str]]
    AnalyticsMetadata: NotRequired[AnalyticsMetadataTypeTypeDef]
    UserContextData: NotRequired[UserContextDataTypeTypeDef]
    ClientMetadata: NotRequired[Mapping[str, str]]


class SignUpRequestRequestTypeDef(TypedDict):
    ClientId: str
    Username: str
    SecretHash: NotRequired[str]
    Password: NotRequired[str]
    UserAttributes: NotRequired[Sequence[AttributeTypeTypeDef]]
    ValidationData: NotRequired[Sequence[AttributeTypeTypeDef]]
    AnalyticsMetadata: NotRequired[AnalyticsMetadataTypeTypeDef]
    UserContextData: NotRequired[UserContextDataTypeTypeDef]
    ClientMetadata: NotRequired[Mapping[str, str]]


class ContextDataTypeTypeDef(TypedDict):
    IpAddress: str
    ServerName: str
    ServerPath: str
    HttpHeaders: Sequence[HttpHeaderTypeDef]
    EncodedData: NotRequired[str]


class CreateIdentityProviderResponseTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeIdentityProviderResponseTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetIdentityProviderByIdentifierResponseTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateIdentityProviderResponseTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateResourceServerRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Identifier: str
    Name: str
    Scopes: NotRequired[Sequence[ResourceServerScopeTypeTypeDef]]


class ResourceServerTypeTypeDef(TypedDict):
    UserPoolId: NotRequired[str]
    Identifier: NotRequired[str]
    Name: NotRequired[str]
    Scopes: NotRequired[List[ResourceServerScopeTypeTypeDef]]


class UpdateResourceServerRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Identifier: str
    Name: str
    Scopes: NotRequired[Sequence[ResourceServerScopeTypeTypeDef]]


class CreateUserImportJobResponseTypeDef(TypedDict):
    UserImportJob: UserImportJobTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeUserImportJobResponseTypeDef(TypedDict):
    UserImportJob: UserImportJobTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListUserImportJobsResponseTypeDef(TypedDict):
    UserImportJobs: List[UserImportJobTypeTypeDef]
    PaginationToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartUserImportJobResponseTypeDef(TypedDict):
    UserImportJob: UserImportJobTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StopUserImportJobResponseTypeDef(TypedDict):
    UserImportJob: UserImportJobTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUserPoolClientRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    ClientName: str
    GenerateSecret: NotRequired[bool]
    RefreshTokenValidity: NotRequired[int]
    AccessTokenValidity: NotRequired[int]
    IdTokenValidity: NotRequired[int]
    TokenValidityUnits: NotRequired[TokenValidityUnitsTypeTypeDef]
    ReadAttributes: NotRequired[Sequence[str]]
    WriteAttributes: NotRequired[Sequence[str]]
    ExplicitAuthFlows: NotRequired[Sequence[ExplicitAuthFlowsTypeType]]
    SupportedIdentityProviders: NotRequired[Sequence[str]]
    CallbackURLs: NotRequired[Sequence[str]]
    LogoutURLs: NotRequired[Sequence[str]]
    DefaultRedirectURI: NotRequired[str]
    AllowedOAuthFlows: NotRequired[Sequence[OAuthFlowTypeType]]
    AllowedOAuthScopes: NotRequired[Sequence[str]]
    AllowedOAuthFlowsUserPoolClient: NotRequired[bool]
    AnalyticsConfiguration: NotRequired[AnalyticsConfigurationTypeTypeDef]
    PreventUserExistenceErrors: NotRequired[PreventUserExistenceErrorTypesType]
    EnableTokenRevocation: NotRequired[bool]
    EnablePropagateAdditionalUserContextData: NotRequired[bool]
    AuthSessionValidity: NotRequired[int]


class UpdateUserPoolClientRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    ClientId: str
    ClientName: NotRequired[str]
    RefreshTokenValidity: NotRequired[int]
    AccessTokenValidity: NotRequired[int]
    IdTokenValidity: NotRequired[int]
    TokenValidityUnits: NotRequired[TokenValidityUnitsTypeTypeDef]
    ReadAttributes: NotRequired[Sequence[str]]
    WriteAttributes: NotRequired[Sequence[str]]
    ExplicitAuthFlows: NotRequired[Sequence[ExplicitAuthFlowsTypeType]]
    SupportedIdentityProviders: NotRequired[Sequence[str]]
    CallbackURLs: NotRequired[Sequence[str]]
    LogoutURLs: NotRequired[Sequence[str]]
    DefaultRedirectURI: NotRequired[str]
    AllowedOAuthFlows: NotRequired[Sequence[OAuthFlowTypeType]]
    AllowedOAuthScopes: NotRequired[Sequence[str]]
    AllowedOAuthFlowsUserPoolClient: NotRequired[bool]
    AnalyticsConfiguration: NotRequired[AnalyticsConfigurationTypeTypeDef]
    PreventUserExistenceErrors: NotRequired[PreventUserExistenceErrorTypesType]
    EnableTokenRevocation: NotRequired[bool]
    EnablePropagateAdditionalUserContextData: NotRequired[bool]
    AuthSessionValidity: NotRequired[int]


class UserPoolClientTypeTypeDef(TypedDict):
    UserPoolId: NotRequired[str]
    ClientName: NotRequired[str]
    ClientId: NotRequired[str]
    ClientSecret: NotRequired[str]
    LastModifiedDate: NotRequired[datetime]
    CreationDate: NotRequired[datetime]
    RefreshTokenValidity: NotRequired[int]
    AccessTokenValidity: NotRequired[int]
    IdTokenValidity: NotRequired[int]
    TokenValidityUnits: NotRequired[TokenValidityUnitsTypeTypeDef]
    ReadAttributes: NotRequired[List[str]]
    WriteAttributes: NotRequired[List[str]]
    ExplicitAuthFlows: NotRequired[List[ExplicitAuthFlowsTypeType]]
    SupportedIdentityProviders: NotRequired[List[str]]
    CallbackURLs: NotRequired[List[str]]
    LogoutURLs: NotRequired[List[str]]
    DefaultRedirectURI: NotRequired[str]
    AllowedOAuthFlows: NotRequired[List[OAuthFlowTypeType]]
    AllowedOAuthScopes: NotRequired[List[str]]
    AllowedOAuthFlowsUserPoolClient: NotRequired[bool]
    AnalyticsConfiguration: NotRequired[AnalyticsConfigurationTypeTypeDef]
    PreventUserExistenceErrors: NotRequired[PreventUserExistenceErrorTypesType]
    EnableTokenRevocation: NotRequired[bool]
    EnablePropagateAdditionalUserContextData: NotRequired[bool]
    AuthSessionValidity: NotRequired[int]


class CreateUserPoolDomainRequestRequestTypeDef(TypedDict):
    Domain: str
    UserPoolId: str
    ManagedLoginVersion: NotRequired[int]
    CustomDomainConfig: NotRequired[CustomDomainConfigTypeTypeDef]


class DomainDescriptionTypeTypeDef(TypedDict):
    UserPoolId: NotRequired[str]
    AWSAccountId: NotRequired[str]
    Domain: NotRequired[str]
    S3Bucket: NotRequired[str]
    CloudFrontDistribution: NotRequired[str]
    Version: NotRequired[str]
    Status: NotRequired[DomainStatusTypeType]
    CustomDomainConfig: NotRequired[CustomDomainConfigTypeTypeDef]
    ManagedLoginVersion: NotRequired[int]


class UpdateUserPoolDomainRequestRequestTypeDef(TypedDict):
    Domain: str
    UserPoolId: str
    CustomDomainConfig: CustomDomainConfigTypeTypeDef
    ManagedLoginVersion: NotRequired[int]


class SmsMfaConfigTypeTypeDef(TypedDict):
    SmsAuthenticationMessage: NotRequired[str]
    SmsConfiguration: NotRequired[SmsConfigurationTypeTypeDef]


class GetUICustomizationResponseTypeDef(TypedDict):
    UICustomization: UICustomizationTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SetUICustomizationResponseTypeDef(TypedDict):
    UICustomization: UICustomizationTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class LambdaConfigTypeTypeDef(TypedDict):
    PreSignUp: NotRequired[str]
    CustomMessage: NotRequired[str]
    PostConfirmation: NotRequired[str]
    PreAuthentication: NotRequired[str]
    PostAuthentication: NotRequired[str]
    DefineAuthChallenge: NotRequired[str]
    CreateAuthChallenge: NotRequired[str]
    VerifyAuthChallengeResponse: NotRequired[str]
    PreTokenGeneration: NotRequired[str]
    UserMigration: NotRequired[str]
    PreTokenGenerationConfig: NotRequired[PreTokenGenerationVersionConfigTypeTypeDef]
    CustomSMSSender: NotRequired[CustomSMSLambdaVersionConfigTypeTypeDef]
    CustomEmailSender: NotRequired[CustomEmailLambdaVersionConfigTypeTypeDef]
    KMSKeyID: NotRequired[str]


class ListIdentityProvidersResponseTypeDef(TypedDict):
    Providers: List[ProviderDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListUserPoolClientsResponseTypeDef(TypedDict):
    UserPoolClients: List[UserPoolClientDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListWebAuthnCredentialsResponseTypeDef(TypedDict):
    Credentials: List[WebAuthnCredentialDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LogConfigurationTypeTypeDef(TypedDict):
    LogLevel: LogLevelType
    EventSource: EventSourceNameType
    CloudWatchLogsConfiguration: NotRequired[CloudWatchLogsConfigurationTypeTypeDef]
    S3Configuration: NotRequired[S3ConfigurationTypeTypeDef]
    FirehoseConfiguration: NotRequired[FirehoseConfigurationTypeTypeDef]


class NotifyConfigurationTypeTypeDef(TypedDict):
    SourceArn: str
    From: NotRequired[str]
    ReplyTo: NotRequired[str]
    BlockEmail: NotRequired[NotifyEmailTypeTypeDef]
    NoActionEmail: NotRequired[NotifyEmailTypeTypeDef]
    MfaEmail: NotRequired[NotifyEmailTypeTypeDef]


SchemaAttributeTypeTypeDef = TypedDict(
    "SchemaAttributeTypeTypeDef",
    {
        "Name": NotRequired[str],
        "AttributeDataType": NotRequired[AttributeDataTypeType],
        "DeveloperOnlyAttribute": NotRequired[bool],
        "Mutable": NotRequired[bool],
        "Required": NotRequired[bool],
        "NumberAttributeConstraints": NotRequired[NumberAttributeConstraintsTypeTypeDef],
        "StringAttributeConstraints": NotRequired[StringAttributeConstraintsTypeTypeDef],
    },
)


class UserPoolPolicyTypeOutputTypeDef(TypedDict):
    PasswordPolicy: NotRequired[PasswordPolicyTypeTypeDef]
    SignInPolicy: NotRequired[SignInPolicyTypeOutputTypeDef]


SignInPolicyTypeUnionTypeDef = Union[SignInPolicyTypeTypeDef, SignInPolicyTypeOutputTypeDef]


class AdminGetDeviceResponseTypeDef(TypedDict):
    Device: DeviceTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AdminListDevicesResponseTypeDef(TypedDict):
    Devices: List[DeviceTypeTypeDef]
    PaginationToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetDeviceResponseTypeDef(TypedDict):
    Device: DeviceTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDevicesResponseTypeDef(TypedDict):
    Devices: List[DeviceTypeTypeDef]
    PaginationToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class AdminCreateUserResponseTypeDef(TypedDict):
    User: UserTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListUsersInGroupResponseTypeDef(TypedDict):
    Users: List[UserTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListUsersResponseTypeDef(TypedDict):
    Users: List[UserTypeTypeDef]
    PaginationToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateManagedLoginBrandingResponseTypeDef(TypedDict):
    ManagedLoginBranding: ManagedLoginBrandingTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeManagedLoginBrandingByClientResponseTypeDef(TypedDict):
    ManagedLoginBranding: ManagedLoginBrandingTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeManagedLoginBrandingResponseTypeDef(TypedDict):
    ManagedLoginBranding: ManagedLoginBrandingTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateManagedLoginBrandingResponseTypeDef(TypedDict):
    ManagedLoginBranding: ManagedLoginBrandingTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


AssetTypeUnionTypeDef = Union[AssetTypeTypeDef, AssetTypeOutputTypeDef]


class UpdateManagedLoginBrandingRequestRequestTypeDef(TypedDict):
    UserPoolId: NotRequired[str]
    ManagedLoginBrandingId: NotRequired[str]
    UseCognitoProvidedValues: NotRequired[bool]
    Settings: NotRequired[Mapping[str, Any]]
    Assets: NotRequired[Sequence[AssetTypeTypeDef]]


class AdminListUserAuthEventsResponseTypeDef(TypedDict):
    AuthEvents: List[AuthEventTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AdminInitiateAuthResponseTypeDef(TypedDict):
    ChallengeName: ChallengeNameTypeType
    Session: str
    ChallengeParameters: Dict[str, str]
    AuthenticationResult: AuthenticationResultTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AdminRespondToAuthChallengeResponseTypeDef(TypedDict):
    ChallengeName: ChallengeNameTypeType
    Session: str
    ChallengeParameters: Dict[str, str]
    AuthenticationResult: AuthenticationResultTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class InitiateAuthResponseTypeDef(TypedDict):
    ChallengeName: ChallengeNameTypeType
    Session: str
    ChallengeParameters: Dict[str, str]
    AuthenticationResult: AuthenticationResultTypeTypeDef
    AvailableChallenges: List[ChallengeNameTypeType]
    ResponseMetadata: ResponseMetadataTypeDef


class RespondToAuthChallengeResponseTypeDef(TypedDict):
    ChallengeName: ChallengeNameTypeType
    Session: str
    ChallengeParameters: Dict[str, str]
    AuthenticationResult: AuthenticationResultTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AdminInitiateAuthRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    ClientId: str
    AuthFlow: AuthFlowTypeType
    AuthParameters: NotRequired[Mapping[str, str]]
    ClientMetadata: NotRequired[Mapping[str, str]]
    AnalyticsMetadata: NotRequired[AnalyticsMetadataTypeTypeDef]
    ContextData: NotRequired[ContextDataTypeTypeDef]
    Session: NotRequired[str]


class AdminRespondToAuthChallengeRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    ClientId: str
    ChallengeName: ChallengeNameTypeType
    ChallengeResponses: NotRequired[Mapping[str, str]]
    Session: NotRequired[str]
    AnalyticsMetadata: NotRequired[AnalyticsMetadataTypeTypeDef]
    ContextData: NotRequired[ContextDataTypeTypeDef]
    ClientMetadata: NotRequired[Mapping[str, str]]


class CreateResourceServerResponseTypeDef(TypedDict):
    ResourceServer: ResourceServerTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeResourceServerResponseTypeDef(TypedDict):
    ResourceServer: ResourceServerTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListResourceServersResponseTypeDef(TypedDict):
    ResourceServers: List[ResourceServerTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateResourceServerResponseTypeDef(TypedDict):
    ResourceServer: ResourceServerTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUserPoolClientResponseTypeDef(TypedDict):
    UserPoolClient: UserPoolClientTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeUserPoolClientResponseTypeDef(TypedDict):
    UserPoolClient: UserPoolClientTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateUserPoolClientResponseTypeDef(TypedDict):
    UserPoolClient: UserPoolClientTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeUserPoolDomainResponseTypeDef(TypedDict):
    DomainDescription: DomainDescriptionTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetUserPoolMfaConfigResponseTypeDef(TypedDict):
    SmsMfaConfiguration: SmsMfaConfigTypeTypeDef
    SoftwareTokenMfaConfiguration: SoftwareTokenMfaConfigTypeTypeDef
    EmailMfaConfiguration: EmailMfaConfigTypeTypeDef
    MfaConfiguration: UserPoolMfaTypeType
    WebAuthnConfiguration: WebAuthnConfigurationTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SetUserPoolMfaConfigRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    SmsMfaConfiguration: NotRequired[SmsMfaConfigTypeTypeDef]
    SoftwareTokenMfaConfiguration: NotRequired[SoftwareTokenMfaConfigTypeTypeDef]
    EmailMfaConfiguration: NotRequired[EmailMfaConfigTypeTypeDef]
    MfaConfiguration: NotRequired[UserPoolMfaTypeType]
    WebAuthnConfiguration: NotRequired[WebAuthnConfigurationTypeTypeDef]


class SetUserPoolMfaConfigResponseTypeDef(TypedDict):
    SmsMfaConfiguration: SmsMfaConfigTypeTypeDef
    SoftwareTokenMfaConfiguration: SoftwareTokenMfaConfigTypeTypeDef
    EmailMfaConfiguration: EmailMfaConfigTypeTypeDef
    MfaConfiguration: UserPoolMfaTypeType
    WebAuthnConfiguration: WebAuthnConfigurationTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UserPoolDescriptionTypeTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    LambdaConfig: NotRequired[LambdaConfigTypeTypeDef]
    Status: NotRequired[StatusTypeType]
    LastModifiedDate: NotRequired[datetime]
    CreationDate: NotRequired[datetime]


class LogDeliveryConfigurationTypeTypeDef(TypedDict):
    UserPoolId: str
    LogConfigurations: List[LogConfigurationTypeTypeDef]


class SetLogDeliveryConfigurationRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    LogConfigurations: Sequence[LogConfigurationTypeTypeDef]


class AccountTakeoverRiskConfigurationTypeTypeDef(TypedDict):
    Actions: AccountTakeoverActionsTypeTypeDef
    NotifyConfiguration: NotRequired[NotifyConfigurationTypeTypeDef]


class AddCustomAttributesRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    CustomAttributes: Sequence[SchemaAttributeTypeTypeDef]


class UserPoolTypeTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Policies: NotRequired[UserPoolPolicyTypeOutputTypeDef]
    DeletionProtection: NotRequired[DeletionProtectionTypeType]
    LambdaConfig: NotRequired[LambdaConfigTypeTypeDef]
    Status: NotRequired[StatusTypeType]
    LastModifiedDate: NotRequired[datetime]
    CreationDate: NotRequired[datetime]
    SchemaAttributes: NotRequired[List[SchemaAttributeTypeTypeDef]]
    AutoVerifiedAttributes: NotRequired[List[VerifiedAttributeTypeType]]
    AliasAttributes: NotRequired[List[AliasAttributeTypeType]]
    UsernameAttributes: NotRequired[List[UsernameAttributeTypeType]]
    SmsVerificationMessage: NotRequired[str]
    EmailVerificationMessage: NotRequired[str]
    EmailVerificationSubject: NotRequired[str]
    VerificationMessageTemplate: NotRequired[VerificationMessageTemplateTypeTypeDef]
    SmsAuthenticationMessage: NotRequired[str]
    UserAttributeUpdateSettings: NotRequired[UserAttributeUpdateSettingsTypeOutputTypeDef]
    MfaConfiguration: NotRequired[UserPoolMfaTypeType]
    DeviceConfiguration: NotRequired[DeviceConfigurationTypeTypeDef]
    EstimatedNumberOfUsers: NotRequired[int]
    EmailConfiguration: NotRequired[EmailConfigurationTypeTypeDef]
    SmsConfiguration: NotRequired[SmsConfigurationTypeTypeDef]
    UserPoolTags: NotRequired[Dict[str, str]]
    SmsConfigurationFailure: NotRequired[str]
    EmailConfigurationFailure: NotRequired[str]
    Domain: NotRequired[str]
    CustomDomain: NotRequired[str]
    AdminCreateUserConfig: NotRequired[AdminCreateUserConfigTypeTypeDef]
    UserPoolAddOns: NotRequired[UserPoolAddOnsTypeTypeDef]
    UsernameConfiguration: NotRequired[UsernameConfigurationTypeTypeDef]
    Arn: NotRequired[str]
    AccountRecoverySetting: NotRequired[AccountRecoverySettingTypeOutputTypeDef]
    UserPoolTier: NotRequired[UserPoolTierTypeType]


class UserPoolPolicyTypeTypeDef(TypedDict):
    PasswordPolicy: NotRequired[PasswordPolicyTypeTypeDef]
    SignInPolicy: NotRequired[SignInPolicyTypeUnionTypeDef]


class CreateManagedLoginBrandingRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    ClientId: str
    UseCognitoProvidedValues: NotRequired[bool]
    Settings: NotRequired[Mapping[str, Any]]
    Assets: NotRequired[Sequence[AssetTypeUnionTypeDef]]


class ListUserPoolsResponseTypeDef(TypedDict):
    UserPools: List[UserPoolDescriptionTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetLogDeliveryConfigurationResponseTypeDef(TypedDict):
    LogDeliveryConfiguration: LogDeliveryConfigurationTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SetLogDeliveryConfigurationResponseTypeDef(TypedDict):
    LogDeliveryConfiguration: LogDeliveryConfigurationTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RiskConfigurationTypeTypeDef(TypedDict):
    UserPoolId: NotRequired[str]
    ClientId: NotRequired[str]
    CompromisedCredentialsRiskConfiguration: NotRequired[
        CompromisedCredentialsRiskConfigurationTypeOutputTypeDef
    ]
    AccountTakeoverRiskConfiguration: NotRequired[AccountTakeoverRiskConfigurationTypeTypeDef]
    RiskExceptionConfiguration: NotRequired[RiskExceptionConfigurationTypeOutputTypeDef]
    LastModifiedDate: NotRequired[datetime]


class SetRiskConfigurationRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    ClientId: NotRequired[str]
    CompromisedCredentialsRiskConfiguration: NotRequired[
        CompromisedCredentialsRiskConfigurationTypeTypeDef
    ]
    AccountTakeoverRiskConfiguration: NotRequired[AccountTakeoverRiskConfigurationTypeTypeDef]
    RiskExceptionConfiguration: NotRequired[RiskExceptionConfigurationTypeTypeDef]


class CreateUserPoolResponseTypeDef(TypedDict):
    UserPool: UserPoolTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeUserPoolResponseTypeDef(TypedDict):
    UserPool: UserPoolTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUserPoolRequestRequestTypeDef(TypedDict):
    PoolName: str
    Policies: NotRequired[UserPoolPolicyTypeTypeDef]
    DeletionProtection: NotRequired[DeletionProtectionTypeType]
    LambdaConfig: NotRequired[LambdaConfigTypeTypeDef]
    AutoVerifiedAttributes: NotRequired[Sequence[VerifiedAttributeTypeType]]
    AliasAttributes: NotRequired[Sequence[AliasAttributeTypeType]]
    UsernameAttributes: NotRequired[Sequence[UsernameAttributeTypeType]]
    SmsVerificationMessage: NotRequired[str]
    EmailVerificationMessage: NotRequired[str]
    EmailVerificationSubject: NotRequired[str]
    VerificationMessageTemplate: NotRequired[VerificationMessageTemplateTypeTypeDef]
    SmsAuthenticationMessage: NotRequired[str]
    MfaConfiguration: NotRequired[UserPoolMfaTypeType]
    UserAttributeUpdateSettings: NotRequired[UserAttributeUpdateSettingsTypeTypeDef]
    DeviceConfiguration: NotRequired[DeviceConfigurationTypeTypeDef]
    EmailConfiguration: NotRequired[EmailConfigurationTypeTypeDef]
    SmsConfiguration: NotRequired[SmsConfigurationTypeTypeDef]
    UserPoolTags: NotRequired[Mapping[str, str]]
    AdminCreateUserConfig: NotRequired[AdminCreateUserConfigTypeTypeDef]
    Schema: NotRequired[Sequence[SchemaAttributeTypeTypeDef]]
    UserPoolAddOns: NotRequired[UserPoolAddOnsTypeTypeDef]
    UsernameConfiguration: NotRequired[UsernameConfigurationTypeTypeDef]
    AccountRecoverySetting: NotRequired[AccountRecoverySettingTypeTypeDef]
    UserPoolTier: NotRequired[UserPoolTierTypeType]


class UpdateUserPoolRequestRequestTypeDef(TypedDict):
    UserPoolId: str
    Policies: NotRequired[UserPoolPolicyTypeTypeDef]
    DeletionProtection: NotRequired[DeletionProtectionTypeType]
    LambdaConfig: NotRequired[LambdaConfigTypeTypeDef]
    AutoVerifiedAttributes: NotRequired[Sequence[VerifiedAttributeTypeType]]
    SmsVerificationMessage: NotRequired[str]
    EmailVerificationMessage: NotRequired[str]
    EmailVerificationSubject: NotRequired[str]
    VerificationMessageTemplate: NotRequired[VerificationMessageTemplateTypeTypeDef]
    SmsAuthenticationMessage: NotRequired[str]
    UserAttributeUpdateSettings: NotRequired[UserAttributeUpdateSettingsTypeTypeDef]
    MfaConfiguration: NotRequired[UserPoolMfaTypeType]
    DeviceConfiguration: NotRequired[DeviceConfigurationTypeTypeDef]
    EmailConfiguration: NotRequired[EmailConfigurationTypeTypeDef]
    SmsConfiguration: NotRequired[SmsConfigurationTypeTypeDef]
    UserPoolTags: NotRequired[Mapping[str, str]]
    AdminCreateUserConfig: NotRequired[AdminCreateUserConfigTypeTypeDef]
    UserPoolAddOns: NotRequired[UserPoolAddOnsTypeTypeDef]
    AccountRecoverySetting: NotRequired[AccountRecoverySettingTypeTypeDef]
    PoolName: NotRequired[str]
    UserPoolTier: NotRequired[UserPoolTierTypeType]


class DescribeRiskConfigurationResponseTypeDef(TypedDict):
    RiskConfiguration: RiskConfigurationTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SetRiskConfigurationResponseTypeDef(TypedDict):
    RiskConfiguration: RiskConfigurationTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
