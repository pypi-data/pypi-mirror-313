"""
Type annotations for cognito-identity service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_identity/type_defs/)

Usage::

    ```python
    from mypy_boto3_cognito_identity.type_defs import CognitoIdentityProviderTypeDef

    data: CognitoIdentityProviderTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AmbiguousRoleResolutionTypeType,
    ErrorCodeType,
    MappingRuleMatchTypeType,
    RoleMappingTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "CognitoIdentityProviderTypeDef",
    "CreateIdentityPoolInputRequestTypeDef",
    "CredentialsTypeDef",
    "DeleteIdentitiesInputRequestTypeDef",
    "DeleteIdentitiesResponseTypeDef",
    "DeleteIdentityPoolInputRequestTypeDef",
    "DescribeIdentityInputRequestTypeDef",
    "DescribeIdentityPoolInputRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetCredentialsForIdentityInputRequestTypeDef",
    "GetCredentialsForIdentityResponseTypeDef",
    "GetIdInputRequestTypeDef",
    "GetIdResponseTypeDef",
    "GetIdentityPoolRolesInputRequestTypeDef",
    "GetIdentityPoolRolesResponseTypeDef",
    "GetOpenIdTokenForDeveloperIdentityInputRequestTypeDef",
    "GetOpenIdTokenForDeveloperIdentityResponseTypeDef",
    "GetOpenIdTokenInputRequestTypeDef",
    "GetOpenIdTokenResponseTypeDef",
    "GetPrincipalTagAttributeMapInputRequestTypeDef",
    "GetPrincipalTagAttributeMapResponseTypeDef",
    "IdentityDescriptionResponseTypeDef",
    "IdentityDescriptionTypeDef",
    "IdentityPoolRequestTypeDef",
    "IdentityPoolShortDescriptionTypeDef",
    "IdentityPoolTypeDef",
    "ListIdentitiesInputRequestTypeDef",
    "ListIdentitiesResponseTypeDef",
    "ListIdentityPoolsInputListIdentityPoolsPaginateTypeDef",
    "ListIdentityPoolsInputRequestTypeDef",
    "ListIdentityPoolsResponseTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LookupDeveloperIdentityInputRequestTypeDef",
    "LookupDeveloperIdentityResponseTypeDef",
    "MappingRuleTypeDef",
    "MergeDeveloperIdentitiesInputRequestTypeDef",
    "MergeDeveloperIdentitiesResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "RoleMappingOutputTypeDef",
    "RoleMappingTypeDef",
    "RoleMappingUnionTypeDef",
    "RulesConfigurationTypeOutputTypeDef",
    "RulesConfigurationTypeTypeDef",
    "RulesConfigurationTypeUnionTypeDef",
    "SetIdentityPoolRolesInputRequestTypeDef",
    "SetPrincipalTagAttributeMapInputRequestTypeDef",
    "SetPrincipalTagAttributeMapResponseTypeDef",
    "TagResourceInputRequestTypeDef",
    "UnlinkDeveloperIdentityInputRequestTypeDef",
    "UnlinkIdentityInputRequestTypeDef",
    "UnprocessedIdentityIdTypeDef",
    "UntagResourceInputRequestTypeDef",
)


class CognitoIdentityProviderTypeDef(TypedDict):
    ProviderName: NotRequired[str]
    ClientId: NotRequired[str]
    ServerSideTokenCheck: NotRequired[bool]


class CredentialsTypeDef(TypedDict):
    AccessKeyId: NotRequired[str]
    SecretKey: NotRequired[str]
    SessionToken: NotRequired[str]
    Expiration: NotRequired[datetime]


class DeleteIdentitiesInputRequestTypeDef(TypedDict):
    IdentityIdsToDelete: Sequence[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class UnprocessedIdentityIdTypeDef(TypedDict):
    IdentityId: NotRequired[str]
    ErrorCode: NotRequired[ErrorCodeType]


class DeleteIdentityPoolInputRequestTypeDef(TypedDict):
    IdentityPoolId: str


class DescribeIdentityInputRequestTypeDef(TypedDict):
    IdentityId: str


class DescribeIdentityPoolInputRequestTypeDef(TypedDict):
    IdentityPoolId: str


class GetCredentialsForIdentityInputRequestTypeDef(TypedDict):
    IdentityId: str
    Logins: NotRequired[Mapping[str, str]]
    CustomRoleArn: NotRequired[str]


class GetIdInputRequestTypeDef(TypedDict):
    IdentityPoolId: str
    AccountId: NotRequired[str]
    Logins: NotRequired[Mapping[str, str]]


class GetIdentityPoolRolesInputRequestTypeDef(TypedDict):
    IdentityPoolId: str


class GetOpenIdTokenForDeveloperIdentityInputRequestTypeDef(TypedDict):
    IdentityPoolId: str
    Logins: Mapping[str, str]
    IdentityId: NotRequired[str]
    PrincipalTags: NotRequired[Mapping[str, str]]
    TokenDuration: NotRequired[int]


class GetOpenIdTokenInputRequestTypeDef(TypedDict):
    IdentityId: str
    Logins: NotRequired[Mapping[str, str]]


class GetPrincipalTagAttributeMapInputRequestTypeDef(TypedDict):
    IdentityPoolId: str
    IdentityProviderName: str


class IdentityDescriptionTypeDef(TypedDict):
    IdentityId: NotRequired[str]
    Logins: NotRequired[List[str]]
    CreationDate: NotRequired[datetime]
    LastModifiedDate: NotRequired[datetime]


class IdentityPoolShortDescriptionTypeDef(TypedDict):
    IdentityPoolId: NotRequired[str]
    IdentityPoolName: NotRequired[str]


class ListIdentitiesInputRequestTypeDef(TypedDict):
    IdentityPoolId: str
    MaxResults: int
    NextToken: NotRequired[str]
    HideDisabled: NotRequired[bool]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListIdentityPoolsInputRequestTypeDef(TypedDict):
    MaxResults: int
    NextToken: NotRequired[str]


class ListTagsForResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str


class LookupDeveloperIdentityInputRequestTypeDef(TypedDict):
    IdentityPoolId: str
    IdentityId: NotRequired[str]
    DeveloperUserIdentifier: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class MappingRuleTypeDef(TypedDict):
    Claim: str
    MatchType: MappingRuleMatchTypeType
    Value: str
    RoleARN: str


class MergeDeveloperIdentitiesInputRequestTypeDef(TypedDict):
    SourceUserIdentifier: str
    DestinationUserIdentifier: str
    DeveloperProviderName: str
    IdentityPoolId: str


class SetPrincipalTagAttributeMapInputRequestTypeDef(TypedDict):
    IdentityPoolId: str
    IdentityProviderName: str
    UseDefaults: NotRequired[bool]
    PrincipalTags: NotRequired[Mapping[str, str]]


class TagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UnlinkDeveloperIdentityInputRequestTypeDef(TypedDict):
    IdentityId: str
    IdentityPoolId: str
    DeveloperProviderName: str
    DeveloperUserIdentifier: str


class UnlinkIdentityInputRequestTypeDef(TypedDict):
    IdentityId: str
    Logins: Mapping[str, str]
    LoginsToRemove: Sequence[str]


class UntagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class CreateIdentityPoolInputRequestTypeDef(TypedDict):
    IdentityPoolName: str
    AllowUnauthenticatedIdentities: bool
    AllowClassicFlow: NotRequired[bool]
    SupportedLoginProviders: NotRequired[Mapping[str, str]]
    DeveloperProviderName: NotRequired[str]
    OpenIdConnectProviderARNs: NotRequired[Sequence[str]]
    CognitoIdentityProviders: NotRequired[Sequence[CognitoIdentityProviderTypeDef]]
    SamlProviderARNs: NotRequired[Sequence[str]]
    IdentityPoolTags: NotRequired[Mapping[str, str]]


class IdentityPoolRequestTypeDef(TypedDict):
    IdentityPoolId: str
    IdentityPoolName: str
    AllowUnauthenticatedIdentities: bool
    AllowClassicFlow: NotRequired[bool]
    SupportedLoginProviders: NotRequired[Mapping[str, str]]
    DeveloperProviderName: NotRequired[str]
    OpenIdConnectProviderARNs: NotRequired[Sequence[str]]
    CognitoIdentityProviders: NotRequired[Sequence[CognitoIdentityProviderTypeDef]]
    SamlProviderARNs: NotRequired[Sequence[str]]
    IdentityPoolTags: NotRequired[Mapping[str, str]]


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetCredentialsForIdentityResponseTypeDef(TypedDict):
    IdentityId: str
    Credentials: CredentialsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetIdResponseTypeDef(TypedDict):
    IdentityId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetOpenIdTokenForDeveloperIdentityResponseTypeDef(TypedDict):
    IdentityId: str
    Token: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetOpenIdTokenResponseTypeDef(TypedDict):
    IdentityId: str
    Token: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetPrincipalTagAttributeMapResponseTypeDef(TypedDict):
    IdentityPoolId: str
    IdentityProviderName: str
    UseDefaults: bool
    PrincipalTags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class IdentityDescriptionResponseTypeDef(TypedDict):
    IdentityId: str
    Logins: List[str]
    CreationDate: datetime
    LastModifiedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class IdentityPoolTypeDef(TypedDict):
    IdentityPoolId: str
    IdentityPoolName: str
    AllowUnauthenticatedIdentities: bool
    AllowClassicFlow: bool
    SupportedLoginProviders: Dict[str, str]
    DeveloperProviderName: str
    OpenIdConnectProviderARNs: List[str]
    CognitoIdentityProviders: List[CognitoIdentityProviderTypeDef]
    SamlProviderARNs: List[str]
    IdentityPoolTags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class LookupDeveloperIdentityResponseTypeDef(TypedDict):
    IdentityId: str
    DeveloperUserIdentifierList: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class MergeDeveloperIdentitiesResponseTypeDef(TypedDict):
    IdentityId: str
    ResponseMetadata: ResponseMetadataTypeDef


class SetPrincipalTagAttributeMapResponseTypeDef(TypedDict):
    IdentityPoolId: str
    IdentityProviderName: str
    UseDefaults: bool
    PrincipalTags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteIdentitiesResponseTypeDef(TypedDict):
    UnprocessedIdentityIds: List[UnprocessedIdentityIdTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListIdentitiesResponseTypeDef(TypedDict):
    IdentityPoolId: str
    Identities: List[IdentityDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListIdentityPoolsResponseTypeDef(TypedDict):
    IdentityPools: List[IdentityPoolShortDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListIdentityPoolsInputListIdentityPoolsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class RulesConfigurationTypeOutputTypeDef(TypedDict):
    Rules: List[MappingRuleTypeDef]


class RulesConfigurationTypeTypeDef(TypedDict):
    Rules: Sequence[MappingRuleTypeDef]


RoleMappingOutputTypeDef = TypedDict(
    "RoleMappingOutputTypeDef",
    {
        "Type": RoleMappingTypeType,
        "AmbiguousRoleResolution": NotRequired[AmbiguousRoleResolutionTypeType],
        "RulesConfiguration": NotRequired[RulesConfigurationTypeOutputTypeDef],
    },
)
RulesConfigurationTypeUnionTypeDef = Union[
    RulesConfigurationTypeTypeDef, RulesConfigurationTypeOutputTypeDef
]


class GetIdentityPoolRolesResponseTypeDef(TypedDict):
    IdentityPoolId: str
    Roles: Dict[str, str]
    RoleMappings: Dict[str, RoleMappingOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


RoleMappingTypeDef = TypedDict(
    "RoleMappingTypeDef",
    {
        "Type": RoleMappingTypeType,
        "AmbiguousRoleResolution": NotRequired[AmbiguousRoleResolutionTypeType],
        "RulesConfiguration": NotRequired[RulesConfigurationTypeUnionTypeDef],
    },
)
RoleMappingUnionTypeDef = Union[RoleMappingTypeDef, RoleMappingOutputTypeDef]


class SetIdentityPoolRolesInputRequestTypeDef(TypedDict):
    IdentityPoolId: str
    Roles: Mapping[str, str]
    RoleMappings: NotRequired[Mapping[str, RoleMappingUnionTypeDef]]
