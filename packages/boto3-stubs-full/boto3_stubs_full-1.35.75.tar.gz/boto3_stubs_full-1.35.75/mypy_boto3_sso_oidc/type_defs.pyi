"""
Type annotations for sso-oidc service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_oidc/type_defs/)

Usage::

    ```python
    from mypy_boto3_sso_oidc.type_defs import CreateTokenRequestRequestTypeDef

    data: CreateTokenRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Sequence

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "CreateTokenRequestRequestTypeDef",
    "CreateTokenResponseTypeDef",
    "CreateTokenWithIAMRequestRequestTypeDef",
    "CreateTokenWithIAMResponseTypeDef",
    "RegisterClientRequestRequestTypeDef",
    "RegisterClientResponseTypeDef",
    "ResponseMetadataTypeDef",
    "StartDeviceAuthorizationRequestRequestTypeDef",
    "StartDeviceAuthorizationResponseTypeDef",
)

class CreateTokenRequestRequestTypeDef(TypedDict):
    clientId: str
    clientSecret: str
    grantType: str
    deviceCode: NotRequired[str]
    code: NotRequired[str]
    refreshToken: NotRequired[str]
    scope: NotRequired[Sequence[str]]
    redirectUri: NotRequired[str]
    codeVerifier: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateTokenWithIAMRequestRequestTypeDef(TypedDict):
    clientId: str
    grantType: str
    code: NotRequired[str]
    refreshToken: NotRequired[str]
    assertion: NotRequired[str]
    scope: NotRequired[Sequence[str]]
    redirectUri: NotRequired[str]
    subjectToken: NotRequired[str]
    subjectTokenType: NotRequired[str]
    requestedTokenType: NotRequired[str]
    codeVerifier: NotRequired[str]

class RegisterClientRequestRequestTypeDef(TypedDict):
    clientName: str
    clientType: str
    scopes: NotRequired[Sequence[str]]
    redirectUris: NotRequired[Sequence[str]]
    grantTypes: NotRequired[Sequence[str]]
    issuerUrl: NotRequired[str]
    entitledApplicationArn: NotRequired[str]

class StartDeviceAuthorizationRequestRequestTypeDef(TypedDict):
    clientId: str
    clientSecret: str
    startUrl: str

class CreateTokenResponseTypeDef(TypedDict):
    accessToken: str
    tokenType: str
    expiresIn: int
    refreshToken: str
    idToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTokenWithIAMResponseTypeDef(TypedDict):
    accessToken: str
    tokenType: str
    expiresIn: int
    refreshToken: str
    idToken: str
    issuedTokenType: str
    scope: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class RegisterClientResponseTypeDef(TypedDict):
    clientId: str
    clientSecret: str
    clientIdIssuedAt: int
    clientSecretExpiresAt: int
    authorizationEndpoint: str
    tokenEndpoint: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartDeviceAuthorizationResponseTypeDef(TypedDict):
    deviceCode: str
    userCode: str
    verificationUri: str
    verificationUriComplete: str
    expiresIn: int
    interval: int
    ResponseMetadata: ResponseMetadataTypeDef
