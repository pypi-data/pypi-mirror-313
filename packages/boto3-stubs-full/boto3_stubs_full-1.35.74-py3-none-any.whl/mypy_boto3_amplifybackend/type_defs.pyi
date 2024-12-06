"""
Type annotations for amplifybackend service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifybackend/type_defs/)

Usage::

    ```python
    from mypy_boto3_amplifybackend.type_defs import BackendAPIAppSyncAuthSettingsTypeDef

    data: BackendAPIAppSyncAuthSettingsTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AdditionalConstraintsElementType,
    AuthenticatedElementType,
    AuthResourcesType,
    DeliveryMethodType,
    MFAModeType,
    MfaTypesElementType,
    ModeType,
    OAuthGrantTypeType,
    OAuthScopesElementType,
    RequiredSignUpAttributesElementType,
    ResolutionStrategyType,
    SignInMethodType,
    StatusType,
    UnAuthenticatedElementType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "BackendAPIAppSyncAuthSettingsTypeDef",
    "BackendAPIAuthTypeTypeDef",
    "BackendAPIConflictResolutionTypeDef",
    "BackendAPIResourceConfigOutputTypeDef",
    "BackendAPIResourceConfigTypeDef",
    "BackendAuthAppleProviderConfigTypeDef",
    "BackendAuthSocialProviderConfigTypeDef",
    "BackendJobRespObjTypeDef",
    "BackendStoragePermissionsOutputTypeDef",
    "BackendStoragePermissionsTypeDef",
    "BackendStoragePermissionsUnionTypeDef",
    "CloneBackendRequestRequestTypeDef",
    "CloneBackendResponseTypeDef",
    "CreateBackendAPIRequestRequestTypeDef",
    "CreateBackendAPIResponseTypeDef",
    "CreateBackendAuthForgotPasswordConfigTypeDef",
    "CreateBackendAuthIdentityPoolConfigTypeDef",
    "CreateBackendAuthMFAConfigOutputTypeDef",
    "CreateBackendAuthMFAConfigTypeDef",
    "CreateBackendAuthMFAConfigUnionTypeDef",
    "CreateBackendAuthOAuthConfigOutputTypeDef",
    "CreateBackendAuthOAuthConfigTypeDef",
    "CreateBackendAuthOAuthConfigUnionTypeDef",
    "CreateBackendAuthPasswordPolicyConfigOutputTypeDef",
    "CreateBackendAuthPasswordPolicyConfigTypeDef",
    "CreateBackendAuthPasswordPolicyConfigUnionTypeDef",
    "CreateBackendAuthRequestRequestTypeDef",
    "CreateBackendAuthResourceConfigOutputTypeDef",
    "CreateBackendAuthResourceConfigTypeDef",
    "CreateBackendAuthResponseTypeDef",
    "CreateBackendAuthUserPoolConfigOutputTypeDef",
    "CreateBackendAuthUserPoolConfigTypeDef",
    "CreateBackendAuthUserPoolConfigUnionTypeDef",
    "CreateBackendAuthVerificationMessageConfigTypeDef",
    "CreateBackendConfigRequestRequestTypeDef",
    "CreateBackendConfigResponseTypeDef",
    "CreateBackendRequestRequestTypeDef",
    "CreateBackendResponseTypeDef",
    "CreateBackendStorageRequestRequestTypeDef",
    "CreateBackendStorageResourceConfigTypeDef",
    "CreateBackendStorageResponseTypeDef",
    "CreateTokenRequestRequestTypeDef",
    "CreateTokenResponseTypeDef",
    "DeleteBackendAPIRequestRequestTypeDef",
    "DeleteBackendAPIResponseTypeDef",
    "DeleteBackendAuthRequestRequestTypeDef",
    "DeleteBackendAuthResponseTypeDef",
    "DeleteBackendRequestRequestTypeDef",
    "DeleteBackendResponseTypeDef",
    "DeleteBackendStorageRequestRequestTypeDef",
    "DeleteBackendStorageResponseTypeDef",
    "DeleteTokenRequestRequestTypeDef",
    "DeleteTokenResponseTypeDef",
    "EmailSettingsTypeDef",
    "GenerateBackendAPIModelsRequestRequestTypeDef",
    "GenerateBackendAPIModelsResponseTypeDef",
    "GetBackendAPIModelsRequestRequestTypeDef",
    "GetBackendAPIModelsResponseTypeDef",
    "GetBackendAPIRequestRequestTypeDef",
    "GetBackendAPIResponseTypeDef",
    "GetBackendAuthRequestRequestTypeDef",
    "GetBackendAuthResponseTypeDef",
    "GetBackendJobRequestRequestTypeDef",
    "GetBackendJobResponseTypeDef",
    "GetBackendRequestRequestTypeDef",
    "GetBackendResponseTypeDef",
    "GetBackendStorageRequestRequestTypeDef",
    "GetBackendStorageResourceConfigTypeDef",
    "GetBackendStorageResponseTypeDef",
    "GetTokenRequestRequestTypeDef",
    "GetTokenResponseTypeDef",
    "ImportBackendAuthRequestRequestTypeDef",
    "ImportBackendAuthResponseTypeDef",
    "ImportBackendStorageRequestRequestTypeDef",
    "ImportBackendStorageResponseTypeDef",
    "ListBackendJobsRequestListBackendJobsPaginateTypeDef",
    "ListBackendJobsRequestRequestTypeDef",
    "ListBackendJobsResponseTypeDef",
    "ListS3BucketsRequestRequestTypeDef",
    "ListS3BucketsResponseTypeDef",
    "LoginAuthConfigReqObjTypeDef",
    "PaginatorConfigTypeDef",
    "RemoveAllBackendsRequestRequestTypeDef",
    "RemoveAllBackendsResponseTypeDef",
    "RemoveBackendConfigRequestRequestTypeDef",
    "RemoveBackendConfigResponseTypeDef",
    "ResponseMetadataTypeDef",
    "S3BucketInfoTypeDef",
    "SettingsOutputTypeDef",
    "SettingsTypeDef",
    "SettingsUnionTypeDef",
    "SmsSettingsTypeDef",
    "SocialProviderSettingsTypeDef",
    "UpdateBackendAPIRequestRequestTypeDef",
    "UpdateBackendAPIResponseTypeDef",
    "UpdateBackendAuthForgotPasswordConfigTypeDef",
    "UpdateBackendAuthIdentityPoolConfigTypeDef",
    "UpdateBackendAuthMFAConfigTypeDef",
    "UpdateBackendAuthOAuthConfigTypeDef",
    "UpdateBackendAuthPasswordPolicyConfigTypeDef",
    "UpdateBackendAuthRequestRequestTypeDef",
    "UpdateBackendAuthResourceConfigTypeDef",
    "UpdateBackendAuthResponseTypeDef",
    "UpdateBackendAuthUserPoolConfigTypeDef",
    "UpdateBackendAuthVerificationMessageConfigTypeDef",
    "UpdateBackendConfigRequestRequestTypeDef",
    "UpdateBackendConfigResponseTypeDef",
    "UpdateBackendJobRequestRequestTypeDef",
    "UpdateBackendJobResponseTypeDef",
    "UpdateBackendStorageRequestRequestTypeDef",
    "UpdateBackendStorageResourceConfigTypeDef",
    "UpdateBackendStorageResponseTypeDef",
)

class BackendAPIAppSyncAuthSettingsTypeDef(TypedDict):
    CognitoUserPoolId: NotRequired[str]
    Description: NotRequired[str]
    ExpirationTime: NotRequired[float]
    OpenIDAuthTTL: NotRequired[str]
    OpenIDClientId: NotRequired[str]
    OpenIDIatTTL: NotRequired[str]
    OpenIDIssueURL: NotRequired[str]
    OpenIDProviderName: NotRequired[str]

class BackendAPIConflictResolutionTypeDef(TypedDict):
    ResolutionStrategy: NotRequired[ResolutionStrategyType]

class BackendAuthAppleProviderConfigTypeDef(TypedDict):
    ClientId: NotRequired[str]
    KeyId: NotRequired[str]
    PrivateKey: NotRequired[str]
    TeamId: NotRequired[str]

class BackendAuthSocialProviderConfigTypeDef(TypedDict):
    ClientId: NotRequired[str]
    ClientSecret: NotRequired[str]

class BackendJobRespObjTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    CreateTime: NotRequired[str]
    Error: NotRequired[str]
    JobId: NotRequired[str]
    Operation: NotRequired[str]
    Status: NotRequired[str]
    UpdateTime: NotRequired[str]

class BackendStoragePermissionsOutputTypeDef(TypedDict):
    Authenticated: List[AuthenticatedElementType]
    UnAuthenticated: NotRequired[List[UnAuthenticatedElementType]]

class BackendStoragePermissionsTypeDef(TypedDict):
    Authenticated: Sequence[AuthenticatedElementType]
    UnAuthenticated: NotRequired[Sequence[UnAuthenticatedElementType]]

class CloneBackendRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    TargetEnvironmentName: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class EmailSettingsTypeDef(TypedDict):
    EmailMessage: NotRequired[str]
    EmailSubject: NotRequired[str]

class SmsSettingsTypeDef(TypedDict):
    SmsMessage: NotRequired[str]

class CreateBackendAuthIdentityPoolConfigTypeDef(TypedDict):
    IdentityPoolName: str
    UnauthenticatedLogin: bool

class SettingsOutputTypeDef(TypedDict):
    MfaTypes: NotRequired[List[MfaTypesElementType]]
    SmsMessage: NotRequired[str]

class CreateBackendAuthPasswordPolicyConfigOutputTypeDef(TypedDict):
    MinimumLength: float
    AdditionalConstraints: NotRequired[List[AdditionalConstraintsElementType]]

class CreateBackendAuthPasswordPolicyConfigTypeDef(TypedDict):
    MinimumLength: float
    AdditionalConstraints: NotRequired[Sequence[AdditionalConstraintsElementType]]

class CreateBackendConfigRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendManagerAppId: NotRequired[str]

class CreateBackendRequestRequestTypeDef(TypedDict):
    AppId: str
    AppName: str
    BackendEnvironmentName: str
    ResourceConfig: NotRequired[Mapping[str, Any]]
    ResourceName: NotRequired[str]

class CreateTokenRequestRequestTypeDef(TypedDict):
    AppId: str

class DeleteBackendAuthRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    ResourceName: str

class DeleteBackendRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str

DeleteBackendStorageRequestRequestTypeDef = TypedDict(
    "DeleteBackendStorageRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ResourceName": str,
        "ServiceName": Literal["S3"],
    },
)

class DeleteTokenRequestRequestTypeDef(TypedDict):
    AppId: str
    SessionId: str

class GenerateBackendAPIModelsRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    ResourceName: str

class GetBackendAPIModelsRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    ResourceName: str

class GetBackendAuthRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    ResourceName: str

class GetBackendJobRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    JobId: str

class GetBackendRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: NotRequired[str]

class GetBackendStorageRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    ResourceName: str

class GetTokenRequestRequestTypeDef(TypedDict):
    AppId: str
    SessionId: str

class ImportBackendAuthRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    NativeClientId: str
    UserPoolId: str
    WebClientId: str
    IdentityPoolId: NotRequired[str]

ImportBackendStorageRequestRequestTypeDef = TypedDict(
    "ImportBackendStorageRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ServiceName": Literal["S3"],
        "BucketName": NotRequired[str],
    },
)

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListBackendJobsRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    JobId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Operation: NotRequired[str]
    Status: NotRequired[str]

class ListS3BucketsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]

class S3BucketInfoTypeDef(TypedDict):
    CreationDate: NotRequired[str]
    Name: NotRequired[str]

class LoginAuthConfigReqObjTypeDef(TypedDict):
    AwsCognitoIdentityPoolId: NotRequired[str]
    AwsCognitoRegion: NotRequired[str]
    AwsUserPoolsId: NotRequired[str]
    AwsUserPoolsWebClientId: NotRequired[str]

class RemoveAllBackendsRequestRequestTypeDef(TypedDict):
    AppId: str
    CleanAmplifyApp: NotRequired[bool]

class RemoveBackendConfigRequestRequestTypeDef(TypedDict):
    AppId: str

class SettingsTypeDef(TypedDict):
    MfaTypes: NotRequired[Sequence[MfaTypesElementType]]
    SmsMessage: NotRequired[str]

class UpdateBackendAuthIdentityPoolConfigTypeDef(TypedDict):
    UnauthenticatedLogin: NotRequired[bool]

class UpdateBackendAuthPasswordPolicyConfigTypeDef(TypedDict):
    AdditionalConstraints: NotRequired[Sequence[AdditionalConstraintsElementType]]
    MinimumLength: NotRequired[float]

class UpdateBackendJobRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    JobId: str
    Operation: NotRequired[str]
    Status: NotRequired[str]

class BackendAPIAuthTypeTypeDef(TypedDict):
    Mode: NotRequired[ModeType]
    Settings: NotRequired[BackendAPIAppSyncAuthSettingsTypeDef]

class SocialProviderSettingsTypeDef(TypedDict):
    Facebook: NotRequired[BackendAuthSocialProviderConfigTypeDef]
    Google: NotRequired[BackendAuthSocialProviderConfigTypeDef]
    LoginWithAmazon: NotRequired[BackendAuthSocialProviderConfigTypeDef]
    SignInWithApple: NotRequired[BackendAuthAppleProviderConfigTypeDef]

GetBackendStorageResourceConfigTypeDef = TypedDict(
    "GetBackendStorageResourceConfigTypeDef",
    {
        "Imported": bool,
        "ServiceName": Literal["S3"],
        "BucketName": NotRequired[str],
        "Permissions": NotRequired[BackendStoragePermissionsOutputTypeDef],
    },
)
BackendStoragePermissionsUnionTypeDef = Union[
    BackendStoragePermissionsTypeDef, BackendStoragePermissionsOutputTypeDef
]

class CloneBackendResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    Error: str
    JobId: str
    Operation: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBackendAPIResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    Error: str
    JobId: str
    Operation: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBackendAuthResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    Error: str
    JobId: str
    Operation: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBackendConfigResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    JobId: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBackendResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    Error: str
    JobId: str
    Operation: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBackendStorageResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    JobId: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTokenResponseTypeDef(TypedDict):
    AppId: str
    ChallengeCode: str
    SessionId: str
    Ttl: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBackendAPIResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    Error: str
    JobId: str
    Operation: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBackendAuthResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    Error: str
    JobId: str
    Operation: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBackendResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    Error: str
    JobId: str
    Operation: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBackendStorageResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    JobId: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteTokenResponseTypeDef(TypedDict):
    IsSuccess: bool
    ResponseMetadata: ResponseMetadataTypeDef

class GenerateBackendAPIModelsResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    Error: str
    JobId: str
    Operation: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetBackendAPIModelsResponseTypeDef(TypedDict):
    Models: str
    Status: StatusType
    ModelIntrospectionSchema: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetBackendJobResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    CreateTime: str
    Error: str
    JobId: str
    Operation: str
    Status: str
    UpdateTime: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetBackendResponseTypeDef(TypedDict):
    AmplifyFeatureFlags: str
    AmplifyMetaConfig: str
    AppId: str
    AppName: str
    BackendEnvironmentList: List[str]
    BackendEnvironmentName: str
    Error: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetTokenResponseTypeDef(TypedDict):
    AppId: str
    ChallengeCode: str
    SessionId: str
    Ttl: str
    ResponseMetadata: ResponseMetadataTypeDef

class ImportBackendAuthResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    Error: str
    JobId: str
    Operation: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class ImportBackendStorageResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    JobId: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListBackendJobsResponseTypeDef(TypedDict):
    Jobs: List[BackendJobRespObjTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class RemoveAllBackendsResponseTypeDef(TypedDict):
    AppId: str
    Error: str
    JobId: str
    Operation: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class RemoveBackendConfigResponseTypeDef(TypedDict):
    Error: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBackendAPIResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    Error: str
    JobId: str
    Operation: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBackendAuthResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    Error: str
    JobId: str
    Operation: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBackendJobResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    CreateTime: str
    Error: str
    JobId: str
    Operation: str
    Status: str
    UpdateTime: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBackendStorageResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    JobId: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBackendAuthForgotPasswordConfigTypeDef(TypedDict):
    DeliveryMethod: DeliveryMethodType
    EmailSettings: NotRequired[EmailSettingsTypeDef]
    SmsSettings: NotRequired[SmsSettingsTypeDef]

class CreateBackendAuthVerificationMessageConfigTypeDef(TypedDict):
    DeliveryMethod: DeliveryMethodType
    EmailSettings: NotRequired[EmailSettingsTypeDef]
    SmsSettings: NotRequired[SmsSettingsTypeDef]

class UpdateBackendAuthForgotPasswordConfigTypeDef(TypedDict):
    DeliveryMethod: NotRequired[DeliveryMethodType]
    EmailSettings: NotRequired[EmailSettingsTypeDef]
    SmsSettings: NotRequired[SmsSettingsTypeDef]

class UpdateBackendAuthVerificationMessageConfigTypeDef(TypedDict):
    DeliveryMethod: DeliveryMethodType
    EmailSettings: NotRequired[EmailSettingsTypeDef]
    SmsSettings: NotRequired[SmsSettingsTypeDef]

class CreateBackendAuthMFAConfigOutputTypeDef(TypedDict):
    MFAMode: MFAModeType
    Settings: NotRequired[SettingsOutputTypeDef]

CreateBackendAuthPasswordPolicyConfigUnionTypeDef = Union[
    CreateBackendAuthPasswordPolicyConfigTypeDef, CreateBackendAuthPasswordPolicyConfigOutputTypeDef
]

class ListBackendJobsRequestListBackendJobsPaginateTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    JobId: NotRequired[str]
    Operation: NotRequired[str]
    Status: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListS3BucketsResponseTypeDef(TypedDict):
    Buckets: List[S3BucketInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateBackendConfigRequestRequestTypeDef(TypedDict):
    AppId: str
    LoginAuthConfig: NotRequired[LoginAuthConfigReqObjTypeDef]

class UpdateBackendConfigResponseTypeDef(TypedDict):
    AppId: str
    BackendManagerAppId: str
    Error: str
    LoginAuthConfig: LoginAuthConfigReqObjTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

SettingsUnionTypeDef = Union[SettingsTypeDef, SettingsOutputTypeDef]

class BackendAPIResourceConfigOutputTypeDef(TypedDict):
    AdditionalAuthTypes: NotRequired[List[BackendAPIAuthTypeTypeDef]]
    ApiName: NotRequired[str]
    ConflictResolution: NotRequired[BackendAPIConflictResolutionTypeDef]
    DefaultAuthType: NotRequired[BackendAPIAuthTypeTypeDef]
    Service: NotRequired[str]
    TransformSchema: NotRequired[str]

class BackendAPIResourceConfigTypeDef(TypedDict):
    AdditionalAuthTypes: NotRequired[Sequence[BackendAPIAuthTypeTypeDef]]
    ApiName: NotRequired[str]
    ConflictResolution: NotRequired[BackendAPIConflictResolutionTypeDef]
    DefaultAuthType: NotRequired[BackendAPIAuthTypeTypeDef]
    Service: NotRequired[str]
    TransformSchema: NotRequired[str]

class CreateBackendAuthOAuthConfigOutputTypeDef(TypedDict):
    OAuthGrantType: OAuthGrantTypeType
    OAuthScopes: List[OAuthScopesElementType]
    RedirectSignInURIs: List[str]
    RedirectSignOutURIs: List[str]
    DomainPrefix: NotRequired[str]
    SocialProviderSettings: NotRequired[SocialProviderSettingsTypeDef]

class CreateBackendAuthOAuthConfigTypeDef(TypedDict):
    OAuthGrantType: OAuthGrantTypeType
    OAuthScopes: Sequence[OAuthScopesElementType]
    RedirectSignInURIs: Sequence[str]
    RedirectSignOutURIs: Sequence[str]
    DomainPrefix: NotRequired[str]
    SocialProviderSettings: NotRequired[SocialProviderSettingsTypeDef]

class UpdateBackendAuthOAuthConfigTypeDef(TypedDict):
    DomainPrefix: NotRequired[str]
    OAuthGrantType: NotRequired[OAuthGrantTypeType]
    OAuthScopes: NotRequired[Sequence[OAuthScopesElementType]]
    RedirectSignInURIs: NotRequired[Sequence[str]]
    RedirectSignOutURIs: NotRequired[Sequence[str]]
    SocialProviderSettings: NotRequired[SocialProviderSettingsTypeDef]

class GetBackendStorageResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    ResourceConfig: GetBackendStorageResourceConfigTypeDef
    ResourceName: str
    ResponseMetadata: ResponseMetadataTypeDef

CreateBackendStorageResourceConfigTypeDef = TypedDict(
    "CreateBackendStorageResourceConfigTypeDef",
    {
        "Permissions": BackendStoragePermissionsUnionTypeDef,
        "ServiceName": Literal["S3"],
        "BucketName": NotRequired[str],
    },
)
UpdateBackendStorageResourceConfigTypeDef = TypedDict(
    "UpdateBackendStorageResourceConfigTypeDef",
    {
        "Permissions": BackendStoragePermissionsUnionTypeDef,
        "ServiceName": Literal["S3"],
    },
)

class CreateBackendAuthMFAConfigTypeDef(TypedDict):
    MFAMode: MFAModeType
    Settings: NotRequired[SettingsUnionTypeDef]

class UpdateBackendAuthMFAConfigTypeDef(TypedDict):
    MFAMode: NotRequired[MFAModeType]
    Settings: NotRequired[SettingsUnionTypeDef]

class GetBackendAPIResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    Error: str
    ResourceConfig: BackendAPIResourceConfigOutputTypeDef
    ResourceName: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBackendAPIRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    ResourceConfig: BackendAPIResourceConfigTypeDef
    ResourceName: str

class DeleteBackendAPIRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    ResourceName: str
    ResourceConfig: NotRequired[BackendAPIResourceConfigTypeDef]

class GetBackendAPIRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    ResourceName: str
    ResourceConfig: NotRequired[BackendAPIResourceConfigTypeDef]

class UpdateBackendAPIRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    ResourceName: str
    ResourceConfig: NotRequired[BackendAPIResourceConfigTypeDef]

class CreateBackendAuthUserPoolConfigOutputTypeDef(TypedDict):
    RequiredSignUpAttributes: List[RequiredSignUpAttributesElementType]
    SignInMethod: SignInMethodType
    UserPoolName: str
    ForgotPassword: NotRequired[CreateBackendAuthForgotPasswordConfigTypeDef]
    Mfa: NotRequired[CreateBackendAuthMFAConfigOutputTypeDef]
    OAuth: NotRequired[CreateBackendAuthOAuthConfigOutputTypeDef]
    PasswordPolicy: NotRequired[CreateBackendAuthPasswordPolicyConfigOutputTypeDef]
    VerificationMessage: NotRequired[CreateBackendAuthVerificationMessageConfigTypeDef]

CreateBackendAuthOAuthConfigUnionTypeDef = Union[
    CreateBackendAuthOAuthConfigTypeDef, CreateBackendAuthOAuthConfigOutputTypeDef
]

class CreateBackendStorageRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    ResourceConfig: CreateBackendStorageResourceConfigTypeDef
    ResourceName: str

class UpdateBackendStorageRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    ResourceConfig: UpdateBackendStorageResourceConfigTypeDef
    ResourceName: str

CreateBackendAuthMFAConfigUnionTypeDef = Union[
    CreateBackendAuthMFAConfigTypeDef, CreateBackendAuthMFAConfigOutputTypeDef
]

class UpdateBackendAuthUserPoolConfigTypeDef(TypedDict):
    ForgotPassword: NotRequired[UpdateBackendAuthForgotPasswordConfigTypeDef]
    Mfa: NotRequired[UpdateBackendAuthMFAConfigTypeDef]
    OAuth: NotRequired[UpdateBackendAuthOAuthConfigTypeDef]
    PasswordPolicy: NotRequired[UpdateBackendAuthPasswordPolicyConfigTypeDef]
    VerificationMessage: NotRequired[UpdateBackendAuthVerificationMessageConfigTypeDef]

class CreateBackendAuthResourceConfigOutputTypeDef(TypedDict):
    AuthResources: AuthResourcesType
    Service: Literal["COGNITO"]
    UserPoolConfigs: CreateBackendAuthUserPoolConfigOutputTypeDef
    IdentityPoolConfigs: NotRequired[CreateBackendAuthIdentityPoolConfigTypeDef]

class CreateBackendAuthUserPoolConfigTypeDef(TypedDict):
    RequiredSignUpAttributes: Sequence[RequiredSignUpAttributesElementType]
    SignInMethod: SignInMethodType
    UserPoolName: str
    ForgotPassword: NotRequired[CreateBackendAuthForgotPasswordConfigTypeDef]
    Mfa: NotRequired[CreateBackendAuthMFAConfigUnionTypeDef]
    OAuth: NotRequired[CreateBackendAuthOAuthConfigUnionTypeDef]
    PasswordPolicy: NotRequired[CreateBackendAuthPasswordPolicyConfigUnionTypeDef]
    VerificationMessage: NotRequired[CreateBackendAuthVerificationMessageConfigTypeDef]

class UpdateBackendAuthResourceConfigTypeDef(TypedDict):
    AuthResources: AuthResourcesType
    Service: Literal["COGNITO"]
    UserPoolConfigs: UpdateBackendAuthUserPoolConfigTypeDef
    IdentityPoolConfigs: NotRequired[UpdateBackendAuthIdentityPoolConfigTypeDef]

class GetBackendAuthResponseTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    Error: str
    ResourceConfig: CreateBackendAuthResourceConfigOutputTypeDef
    ResourceName: str
    ResponseMetadata: ResponseMetadataTypeDef

CreateBackendAuthUserPoolConfigUnionTypeDef = Union[
    CreateBackendAuthUserPoolConfigTypeDef, CreateBackendAuthUserPoolConfigOutputTypeDef
]

class UpdateBackendAuthRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    ResourceConfig: UpdateBackendAuthResourceConfigTypeDef
    ResourceName: str

class CreateBackendAuthResourceConfigTypeDef(TypedDict):
    AuthResources: AuthResourcesType
    Service: Literal["COGNITO"]
    UserPoolConfigs: CreateBackendAuthUserPoolConfigUnionTypeDef
    IdentityPoolConfigs: NotRequired[CreateBackendAuthIdentityPoolConfigTypeDef]

class CreateBackendAuthRequestRequestTypeDef(TypedDict):
    AppId: str
    BackendEnvironmentName: str
    ResourceConfig: CreateBackendAuthResourceConfigTypeDef
    ResourceName: str
