"""
Type annotations for workspaces-web service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/type_defs/)

Usage::

    ```python
    from mypy_boto3_workspaces_web.type_defs import AssociateBrowserSettingsRequestRequestTypeDef

    data: AssociateBrowserSettingsRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AuthenticationTypeType,
    EnabledTypeType,
    IdentityProviderTypeType,
    InstanceTypeType,
    PortalStatusType,
    SessionSortByType,
    SessionStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AssociateBrowserSettingsRequestRequestTypeDef",
    "AssociateBrowserSettingsResponseTypeDef",
    "AssociateDataProtectionSettingsRequestRequestTypeDef",
    "AssociateDataProtectionSettingsResponseTypeDef",
    "AssociateIpAccessSettingsRequestRequestTypeDef",
    "AssociateIpAccessSettingsResponseTypeDef",
    "AssociateNetworkSettingsRequestRequestTypeDef",
    "AssociateNetworkSettingsResponseTypeDef",
    "AssociateTrustStoreRequestRequestTypeDef",
    "AssociateTrustStoreResponseTypeDef",
    "AssociateUserAccessLoggingSettingsRequestRequestTypeDef",
    "AssociateUserAccessLoggingSettingsResponseTypeDef",
    "AssociateUserSettingsRequestRequestTypeDef",
    "AssociateUserSettingsResponseTypeDef",
    "BlobTypeDef",
    "BrowserSettingsSummaryTypeDef",
    "BrowserSettingsTypeDef",
    "CertificateSummaryTypeDef",
    "CertificateTypeDef",
    "CookieSpecificationTypeDef",
    "CookieSynchronizationConfigurationOutputTypeDef",
    "CookieSynchronizationConfigurationTypeDef",
    "CreateBrowserSettingsRequestRequestTypeDef",
    "CreateBrowserSettingsResponseTypeDef",
    "CreateDataProtectionSettingsRequestRequestTypeDef",
    "CreateDataProtectionSettingsResponseTypeDef",
    "CreateIdentityProviderRequestRequestTypeDef",
    "CreateIdentityProviderResponseTypeDef",
    "CreateIpAccessSettingsRequestRequestTypeDef",
    "CreateIpAccessSettingsResponseTypeDef",
    "CreateNetworkSettingsRequestRequestTypeDef",
    "CreateNetworkSettingsResponseTypeDef",
    "CreatePortalRequestRequestTypeDef",
    "CreatePortalResponseTypeDef",
    "CreateTrustStoreRequestRequestTypeDef",
    "CreateTrustStoreResponseTypeDef",
    "CreateUserAccessLoggingSettingsRequestRequestTypeDef",
    "CreateUserAccessLoggingSettingsResponseTypeDef",
    "CreateUserSettingsRequestRequestTypeDef",
    "CreateUserSettingsResponseTypeDef",
    "CustomPatternTypeDef",
    "DataProtectionSettingsSummaryTypeDef",
    "DataProtectionSettingsTypeDef",
    "DeleteBrowserSettingsRequestRequestTypeDef",
    "DeleteDataProtectionSettingsRequestRequestTypeDef",
    "DeleteIdentityProviderRequestRequestTypeDef",
    "DeleteIpAccessSettingsRequestRequestTypeDef",
    "DeleteNetworkSettingsRequestRequestTypeDef",
    "DeletePortalRequestRequestTypeDef",
    "DeleteTrustStoreRequestRequestTypeDef",
    "DeleteUserAccessLoggingSettingsRequestRequestTypeDef",
    "DeleteUserSettingsRequestRequestTypeDef",
    "DisassociateBrowserSettingsRequestRequestTypeDef",
    "DisassociateDataProtectionSettingsRequestRequestTypeDef",
    "DisassociateIpAccessSettingsRequestRequestTypeDef",
    "DisassociateNetworkSettingsRequestRequestTypeDef",
    "DisassociateTrustStoreRequestRequestTypeDef",
    "DisassociateUserAccessLoggingSettingsRequestRequestTypeDef",
    "DisassociateUserSettingsRequestRequestTypeDef",
    "ExpireSessionRequestRequestTypeDef",
    "GetBrowserSettingsRequestRequestTypeDef",
    "GetBrowserSettingsResponseTypeDef",
    "GetDataProtectionSettingsRequestRequestTypeDef",
    "GetDataProtectionSettingsResponseTypeDef",
    "GetIdentityProviderRequestRequestTypeDef",
    "GetIdentityProviderResponseTypeDef",
    "GetIpAccessSettingsRequestRequestTypeDef",
    "GetIpAccessSettingsResponseTypeDef",
    "GetNetworkSettingsRequestRequestTypeDef",
    "GetNetworkSettingsResponseTypeDef",
    "GetPortalRequestRequestTypeDef",
    "GetPortalResponseTypeDef",
    "GetPortalServiceProviderMetadataRequestRequestTypeDef",
    "GetPortalServiceProviderMetadataResponseTypeDef",
    "GetSessionRequestRequestTypeDef",
    "GetSessionResponseTypeDef",
    "GetTrustStoreCertificateRequestRequestTypeDef",
    "GetTrustStoreCertificateResponseTypeDef",
    "GetTrustStoreRequestRequestTypeDef",
    "GetTrustStoreResponseTypeDef",
    "GetUserAccessLoggingSettingsRequestRequestTypeDef",
    "GetUserAccessLoggingSettingsResponseTypeDef",
    "GetUserSettingsRequestRequestTypeDef",
    "GetUserSettingsResponseTypeDef",
    "IdentityProviderSummaryTypeDef",
    "IdentityProviderTypeDef",
    "InlineRedactionConfigurationOutputTypeDef",
    "InlineRedactionConfigurationTypeDef",
    "InlineRedactionPatternOutputTypeDef",
    "InlineRedactionPatternTypeDef",
    "InlineRedactionPatternUnionTypeDef",
    "IpAccessSettingsSummaryTypeDef",
    "IpAccessSettingsTypeDef",
    "IpRuleTypeDef",
    "ListBrowserSettingsRequestRequestTypeDef",
    "ListBrowserSettingsResponseTypeDef",
    "ListDataProtectionSettingsRequestListDataProtectionSettingsPaginateTypeDef",
    "ListDataProtectionSettingsRequestRequestTypeDef",
    "ListDataProtectionSettingsResponseTypeDef",
    "ListIdentityProvidersRequestRequestTypeDef",
    "ListIdentityProvidersResponseTypeDef",
    "ListIpAccessSettingsRequestRequestTypeDef",
    "ListIpAccessSettingsResponseTypeDef",
    "ListNetworkSettingsRequestRequestTypeDef",
    "ListNetworkSettingsResponseTypeDef",
    "ListPortalsRequestRequestTypeDef",
    "ListPortalsResponseTypeDef",
    "ListSessionsRequestListSessionsPaginateTypeDef",
    "ListSessionsRequestRequestTypeDef",
    "ListSessionsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTrustStoreCertificatesRequestRequestTypeDef",
    "ListTrustStoreCertificatesResponseTypeDef",
    "ListTrustStoresRequestRequestTypeDef",
    "ListTrustStoresResponseTypeDef",
    "ListUserAccessLoggingSettingsRequestRequestTypeDef",
    "ListUserAccessLoggingSettingsResponseTypeDef",
    "ListUserSettingsRequestRequestTypeDef",
    "ListUserSettingsResponseTypeDef",
    "NetworkSettingsSummaryTypeDef",
    "NetworkSettingsTypeDef",
    "PaginatorConfigTypeDef",
    "PortalSummaryTypeDef",
    "PortalTypeDef",
    "RedactionPlaceHolderTypeDef",
    "ResponseMetadataTypeDef",
    "SessionSummaryTypeDef",
    "SessionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TrustStoreSummaryTypeDef",
    "TrustStoreTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateBrowserSettingsRequestRequestTypeDef",
    "UpdateBrowserSettingsResponseTypeDef",
    "UpdateDataProtectionSettingsRequestRequestTypeDef",
    "UpdateDataProtectionSettingsResponseTypeDef",
    "UpdateIdentityProviderRequestRequestTypeDef",
    "UpdateIdentityProviderResponseTypeDef",
    "UpdateIpAccessSettingsRequestRequestTypeDef",
    "UpdateIpAccessSettingsResponseTypeDef",
    "UpdateNetworkSettingsRequestRequestTypeDef",
    "UpdateNetworkSettingsResponseTypeDef",
    "UpdatePortalRequestRequestTypeDef",
    "UpdatePortalResponseTypeDef",
    "UpdateTrustStoreRequestRequestTypeDef",
    "UpdateTrustStoreResponseTypeDef",
    "UpdateUserAccessLoggingSettingsRequestRequestTypeDef",
    "UpdateUserAccessLoggingSettingsResponseTypeDef",
    "UpdateUserSettingsRequestRequestTypeDef",
    "UpdateUserSettingsResponseTypeDef",
    "UserAccessLoggingSettingsSummaryTypeDef",
    "UserAccessLoggingSettingsTypeDef",
    "UserSettingsSummaryTypeDef",
    "UserSettingsTypeDef",
)


class AssociateBrowserSettingsRequestRequestTypeDef(TypedDict):
    browserSettingsArn: str
    portalArn: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AssociateDataProtectionSettingsRequestRequestTypeDef(TypedDict):
    dataProtectionSettingsArn: str
    portalArn: str


class AssociateIpAccessSettingsRequestRequestTypeDef(TypedDict):
    ipAccessSettingsArn: str
    portalArn: str


class AssociateNetworkSettingsRequestRequestTypeDef(TypedDict):
    networkSettingsArn: str
    portalArn: str


class AssociateTrustStoreRequestRequestTypeDef(TypedDict):
    portalArn: str
    trustStoreArn: str


class AssociateUserAccessLoggingSettingsRequestRequestTypeDef(TypedDict):
    portalArn: str
    userAccessLoggingSettingsArn: str


class AssociateUserSettingsRequestRequestTypeDef(TypedDict):
    portalArn: str
    userSettingsArn: str


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class BrowserSettingsSummaryTypeDef(TypedDict):
    browserSettingsArn: str


class BrowserSettingsTypeDef(TypedDict):
    browserSettingsArn: str
    additionalEncryptionContext: NotRequired[Dict[str, str]]
    associatedPortalArns: NotRequired[List[str]]
    browserPolicy: NotRequired[str]
    customerManagedKey: NotRequired[str]


class CertificateSummaryTypeDef(TypedDict):
    issuer: NotRequired[str]
    notValidAfter: NotRequired[datetime]
    notValidBefore: NotRequired[datetime]
    subject: NotRequired[str]
    thumbprint: NotRequired[str]


class CertificateTypeDef(TypedDict):
    body: NotRequired[bytes]
    issuer: NotRequired[str]
    notValidAfter: NotRequired[datetime]
    notValidBefore: NotRequired[datetime]
    subject: NotRequired[str]
    thumbprint: NotRequired[str]


class CookieSpecificationTypeDef(TypedDict):
    domain: str
    name: NotRequired[str]
    path: NotRequired[str]


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class IpRuleTypeDef(TypedDict):
    ipRange: str
    description: NotRequired[str]


class CustomPatternTypeDef(TypedDict):
    patternName: str
    patternRegex: str
    keywordRegex: NotRequired[str]
    patternDescription: NotRequired[str]


class DataProtectionSettingsSummaryTypeDef(TypedDict):
    dataProtectionSettingsArn: str
    creationDate: NotRequired[datetime]
    description: NotRequired[str]
    displayName: NotRequired[str]


class DeleteBrowserSettingsRequestRequestTypeDef(TypedDict):
    browserSettingsArn: str


class DeleteDataProtectionSettingsRequestRequestTypeDef(TypedDict):
    dataProtectionSettingsArn: str


class DeleteIdentityProviderRequestRequestTypeDef(TypedDict):
    identityProviderArn: str


class DeleteIpAccessSettingsRequestRequestTypeDef(TypedDict):
    ipAccessSettingsArn: str


class DeleteNetworkSettingsRequestRequestTypeDef(TypedDict):
    networkSettingsArn: str


class DeletePortalRequestRequestTypeDef(TypedDict):
    portalArn: str


class DeleteTrustStoreRequestRequestTypeDef(TypedDict):
    trustStoreArn: str


class DeleteUserAccessLoggingSettingsRequestRequestTypeDef(TypedDict):
    userAccessLoggingSettingsArn: str


class DeleteUserSettingsRequestRequestTypeDef(TypedDict):
    userSettingsArn: str


class DisassociateBrowserSettingsRequestRequestTypeDef(TypedDict):
    portalArn: str


class DisassociateDataProtectionSettingsRequestRequestTypeDef(TypedDict):
    portalArn: str


class DisassociateIpAccessSettingsRequestRequestTypeDef(TypedDict):
    portalArn: str


class DisassociateNetworkSettingsRequestRequestTypeDef(TypedDict):
    portalArn: str


class DisassociateTrustStoreRequestRequestTypeDef(TypedDict):
    portalArn: str


class DisassociateUserAccessLoggingSettingsRequestRequestTypeDef(TypedDict):
    portalArn: str


class DisassociateUserSettingsRequestRequestTypeDef(TypedDict):
    portalArn: str


class ExpireSessionRequestRequestTypeDef(TypedDict):
    portalId: str
    sessionId: str


class GetBrowserSettingsRequestRequestTypeDef(TypedDict):
    browserSettingsArn: str


class GetDataProtectionSettingsRequestRequestTypeDef(TypedDict):
    dataProtectionSettingsArn: str


class GetIdentityProviderRequestRequestTypeDef(TypedDict):
    identityProviderArn: str


class IdentityProviderTypeDef(TypedDict):
    identityProviderArn: str
    identityProviderDetails: NotRequired[Dict[str, str]]
    identityProviderName: NotRequired[str]
    identityProviderType: NotRequired[IdentityProviderTypeType]


class GetIpAccessSettingsRequestRequestTypeDef(TypedDict):
    ipAccessSettingsArn: str


class GetNetworkSettingsRequestRequestTypeDef(TypedDict):
    networkSettingsArn: str


class NetworkSettingsTypeDef(TypedDict):
    networkSettingsArn: str
    associatedPortalArns: NotRequired[List[str]]
    securityGroupIds: NotRequired[List[str]]
    subnetIds: NotRequired[List[str]]
    vpcId: NotRequired[str]


class GetPortalRequestRequestTypeDef(TypedDict):
    portalArn: str


class PortalTypeDef(TypedDict):
    portalArn: str
    additionalEncryptionContext: NotRequired[Dict[str, str]]
    authenticationType: NotRequired[AuthenticationTypeType]
    browserSettingsArn: NotRequired[str]
    browserType: NotRequired[Literal["Chrome"]]
    creationDate: NotRequired[datetime]
    customerManagedKey: NotRequired[str]
    dataProtectionSettingsArn: NotRequired[str]
    displayName: NotRequired[str]
    instanceType: NotRequired[InstanceTypeType]
    ipAccessSettingsArn: NotRequired[str]
    maxConcurrentSessions: NotRequired[int]
    networkSettingsArn: NotRequired[str]
    portalEndpoint: NotRequired[str]
    portalStatus: NotRequired[PortalStatusType]
    rendererType: NotRequired[Literal["AppStream"]]
    statusReason: NotRequired[str]
    trustStoreArn: NotRequired[str]
    userAccessLoggingSettingsArn: NotRequired[str]
    userSettingsArn: NotRequired[str]


class GetPortalServiceProviderMetadataRequestRequestTypeDef(TypedDict):
    portalArn: str


class GetSessionRequestRequestTypeDef(TypedDict):
    portalId: str
    sessionId: str


class SessionTypeDef(TypedDict):
    clientIpAddresses: NotRequired[List[str]]
    endTime: NotRequired[datetime]
    portalArn: NotRequired[str]
    sessionId: NotRequired[str]
    startTime: NotRequired[datetime]
    status: NotRequired[SessionStatusType]
    username: NotRequired[str]


class GetTrustStoreCertificateRequestRequestTypeDef(TypedDict):
    thumbprint: str
    trustStoreArn: str


class GetTrustStoreRequestRequestTypeDef(TypedDict):
    trustStoreArn: str


class TrustStoreTypeDef(TypedDict):
    trustStoreArn: str
    associatedPortalArns: NotRequired[List[str]]


class GetUserAccessLoggingSettingsRequestRequestTypeDef(TypedDict):
    userAccessLoggingSettingsArn: str


class UserAccessLoggingSettingsTypeDef(TypedDict):
    userAccessLoggingSettingsArn: str
    associatedPortalArns: NotRequired[List[str]]
    kinesisStreamArn: NotRequired[str]


class GetUserSettingsRequestRequestTypeDef(TypedDict):
    userSettingsArn: str


class IdentityProviderSummaryTypeDef(TypedDict):
    identityProviderArn: str
    identityProviderName: NotRequired[str]
    identityProviderType: NotRequired[IdentityProviderTypeType]


class RedactionPlaceHolderTypeDef(TypedDict):
    redactionPlaceHolderType: Literal["CustomText"]
    redactionPlaceHolderText: NotRequired[str]


class IpAccessSettingsSummaryTypeDef(TypedDict):
    ipAccessSettingsArn: str
    creationDate: NotRequired[datetime]
    description: NotRequired[str]
    displayName: NotRequired[str]


class ListBrowserSettingsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListDataProtectionSettingsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListIdentityProvidersRequestRequestTypeDef(TypedDict):
    portalArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListIpAccessSettingsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListNetworkSettingsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class NetworkSettingsSummaryTypeDef(TypedDict):
    networkSettingsArn: str
    vpcId: NotRequired[str]


class ListPortalsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class PortalSummaryTypeDef(TypedDict):
    portalArn: str
    authenticationType: NotRequired[AuthenticationTypeType]
    browserSettingsArn: NotRequired[str]
    browserType: NotRequired[Literal["Chrome"]]
    creationDate: NotRequired[datetime]
    dataProtectionSettingsArn: NotRequired[str]
    displayName: NotRequired[str]
    instanceType: NotRequired[InstanceTypeType]
    ipAccessSettingsArn: NotRequired[str]
    maxConcurrentSessions: NotRequired[int]
    networkSettingsArn: NotRequired[str]
    portalEndpoint: NotRequired[str]
    portalStatus: NotRequired[PortalStatusType]
    rendererType: NotRequired[Literal["AppStream"]]
    trustStoreArn: NotRequired[str]
    userAccessLoggingSettingsArn: NotRequired[str]
    userSettingsArn: NotRequired[str]


class ListSessionsRequestRequestTypeDef(TypedDict):
    portalId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sessionId: NotRequired[str]
    sortBy: NotRequired[SessionSortByType]
    status: NotRequired[SessionStatusType]
    username: NotRequired[str]


class SessionSummaryTypeDef(TypedDict):
    endTime: NotRequired[datetime]
    portalArn: NotRequired[str]
    sessionId: NotRequired[str]
    startTime: NotRequired[datetime]
    status: NotRequired[SessionStatusType]
    username: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class ListTrustStoreCertificatesRequestRequestTypeDef(TypedDict):
    trustStoreArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListTrustStoresRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class TrustStoreSummaryTypeDef(TypedDict):
    trustStoreArn: NotRequired[str]


class ListUserAccessLoggingSettingsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class UserAccessLoggingSettingsSummaryTypeDef(TypedDict):
    userAccessLoggingSettingsArn: str
    kinesisStreamArn: NotRequired[str]


class ListUserSettingsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateBrowserSettingsRequestRequestTypeDef(TypedDict):
    browserSettingsArn: str
    browserPolicy: NotRequired[str]
    clientToken: NotRequired[str]


class UpdateIdentityProviderRequestRequestTypeDef(TypedDict):
    identityProviderArn: str
    clientToken: NotRequired[str]
    identityProviderDetails: NotRequired[Mapping[str, str]]
    identityProviderName: NotRequired[str]
    identityProviderType: NotRequired[IdentityProviderTypeType]


class UpdateNetworkSettingsRequestRequestTypeDef(TypedDict):
    networkSettingsArn: str
    clientToken: NotRequired[str]
    securityGroupIds: NotRequired[Sequence[str]]
    subnetIds: NotRequired[Sequence[str]]
    vpcId: NotRequired[str]


class UpdatePortalRequestRequestTypeDef(TypedDict):
    portalArn: str
    authenticationType: NotRequired[AuthenticationTypeType]
    displayName: NotRequired[str]
    instanceType: NotRequired[InstanceTypeType]
    maxConcurrentSessions: NotRequired[int]


class UpdateUserAccessLoggingSettingsRequestRequestTypeDef(TypedDict):
    userAccessLoggingSettingsArn: str
    clientToken: NotRequired[str]
    kinesisStreamArn: NotRequired[str]


class AssociateBrowserSettingsResponseTypeDef(TypedDict):
    browserSettingsArn: str
    portalArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateDataProtectionSettingsResponseTypeDef(TypedDict):
    dataProtectionSettingsArn: str
    portalArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateIpAccessSettingsResponseTypeDef(TypedDict):
    ipAccessSettingsArn: str
    portalArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateNetworkSettingsResponseTypeDef(TypedDict):
    networkSettingsArn: str
    portalArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateTrustStoreResponseTypeDef(TypedDict):
    portalArn: str
    trustStoreArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateUserAccessLoggingSettingsResponseTypeDef(TypedDict):
    portalArn: str
    userAccessLoggingSettingsArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateUserSettingsResponseTypeDef(TypedDict):
    portalArn: str
    userSettingsArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBrowserSettingsResponseTypeDef(TypedDict):
    browserSettingsArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataProtectionSettingsResponseTypeDef(TypedDict):
    dataProtectionSettingsArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateIdentityProviderResponseTypeDef(TypedDict):
    identityProviderArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateIpAccessSettingsResponseTypeDef(TypedDict):
    ipAccessSettingsArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateNetworkSettingsResponseTypeDef(TypedDict):
    networkSettingsArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePortalResponseTypeDef(TypedDict):
    portalArn: str
    portalEndpoint: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTrustStoreResponseTypeDef(TypedDict):
    trustStoreArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUserAccessLoggingSettingsResponseTypeDef(TypedDict):
    userAccessLoggingSettingsArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUserSettingsResponseTypeDef(TypedDict):
    userSettingsArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetPortalServiceProviderMetadataResponseTypeDef(TypedDict):
    portalArn: str
    serviceProviderSamlMetadata: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTrustStoreResponseTypeDef(TypedDict):
    trustStoreArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTrustStoreRequestRequestTypeDef(TypedDict):
    trustStoreArn: str
    certificatesToAdd: NotRequired[Sequence[BlobTypeDef]]
    certificatesToDelete: NotRequired[Sequence[str]]
    clientToken: NotRequired[str]


class ListBrowserSettingsResponseTypeDef(TypedDict):
    browserSettings: List[BrowserSettingsSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetBrowserSettingsResponseTypeDef(TypedDict):
    browserSettings: BrowserSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBrowserSettingsResponseTypeDef(TypedDict):
    browserSettings: BrowserSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListTrustStoreCertificatesResponseTypeDef(TypedDict):
    certificateList: List[CertificateSummaryTypeDef]
    trustStoreArn: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetTrustStoreCertificateResponseTypeDef(TypedDict):
    certificate: CertificateTypeDef
    trustStoreArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CookieSynchronizationConfigurationOutputTypeDef(TypedDict):
    allowlist: List[CookieSpecificationTypeDef]
    blocklist: NotRequired[List[CookieSpecificationTypeDef]]


class CookieSynchronizationConfigurationTypeDef(TypedDict):
    allowlist: Sequence[CookieSpecificationTypeDef]
    blocklist: NotRequired[Sequence[CookieSpecificationTypeDef]]


class CreateBrowserSettingsRequestRequestTypeDef(TypedDict):
    browserPolicy: str
    additionalEncryptionContext: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]
    customerManagedKey: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateIdentityProviderRequestRequestTypeDef(TypedDict):
    identityProviderDetails: Mapping[str, str]
    identityProviderName: str
    identityProviderType: IdentityProviderTypeType
    portalArn: str
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateNetworkSettingsRequestRequestTypeDef(TypedDict):
    securityGroupIds: Sequence[str]
    subnetIds: Sequence[str]
    vpcId: str
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreatePortalRequestRequestTypeDef(TypedDict):
    additionalEncryptionContext: NotRequired[Mapping[str, str]]
    authenticationType: NotRequired[AuthenticationTypeType]
    clientToken: NotRequired[str]
    customerManagedKey: NotRequired[str]
    displayName: NotRequired[str]
    instanceType: NotRequired[InstanceTypeType]
    maxConcurrentSessions: NotRequired[int]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateTrustStoreRequestRequestTypeDef(TypedDict):
    certificateList: Sequence[BlobTypeDef]
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateUserAccessLoggingSettingsRequestRequestTypeDef(TypedDict):
    kinesisStreamArn: str
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]
    clientToken: NotRequired[str]


class CreateIpAccessSettingsRequestRequestTypeDef(TypedDict):
    ipRules: Sequence[IpRuleTypeDef]
    additionalEncryptionContext: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]
    customerManagedKey: NotRequired[str]
    description: NotRequired[str]
    displayName: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class IpAccessSettingsTypeDef(TypedDict):
    ipAccessSettingsArn: str
    additionalEncryptionContext: NotRequired[Dict[str, str]]
    associatedPortalArns: NotRequired[List[str]]
    creationDate: NotRequired[datetime]
    customerManagedKey: NotRequired[str]
    description: NotRequired[str]
    displayName: NotRequired[str]
    ipRules: NotRequired[List[IpRuleTypeDef]]


class UpdateIpAccessSettingsRequestRequestTypeDef(TypedDict):
    ipAccessSettingsArn: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    displayName: NotRequired[str]
    ipRules: NotRequired[Sequence[IpRuleTypeDef]]


class ListDataProtectionSettingsResponseTypeDef(TypedDict):
    dataProtectionSettings: List[DataProtectionSettingsSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetIdentityProviderResponseTypeDef(TypedDict):
    identityProvider: IdentityProviderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateIdentityProviderResponseTypeDef(TypedDict):
    identityProvider: IdentityProviderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetNetworkSettingsResponseTypeDef(TypedDict):
    networkSettings: NetworkSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateNetworkSettingsResponseTypeDef(TypedDict):
    networkSettings: NetworkSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetPortalResponseTypeDef(TypedDict):
    portal: PortalTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePortalResponseTypeDef(TypedDict):
    portal: PortalTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetSessionResponseTypeDef(TypedDict):
    session: SessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetTrustStoreResponseTypeDef(TypedDict):
    trustStore: TrustStoreTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetUserAccessLoggingSettingsResponseTypeDef(TypedDict):
    userAccessLoggingSettings: UserAccessLoggingSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateUserAccessLoggingSettingsResponseTypeDef(TypedDict):
    userAccessLoggingSettings: UserAccessLoggingSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListIdentityProvidersResponseTypeDef(TypedDict):
    identityProviders: List[IdentityProviderSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class InlineRedactionPatternOutputTypeDef(TypedDict):
    redactionPlaceHolder: RedactionPlaceHolderTypeDef
    builtInPatternId: NotRequired[str]
    confidenceLevel: NotRequired[int]
    customPattern: NotRequired[CustomPatternTypeDef]
    enforcedUrls: NotRequired[List[str]]
    exemptUrls: NotRequired[List[str]]


class InlineRedactionPatternTypeDef(TypedDict):
    redactionPlaceHolder: RedactionPlaceHolderTypeDef
    builtInPatternId: NotRequired[str]
    confidenceLevel: NotRequired[int]
    customPattern: NotRequired[CustomPatternTypeDef]
    enforcedUrls: NotRequired[Sequence[str]]
    exemptUrls: NotRequired[Sequence[str]]


class ListIpAccessSettingsResponseTypeDef(TypedDict):
    ipAccessSettings: List[IpAccessSettingsSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListDataProtectionSettingsRequestListDataProtectionSettingsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSessionsRequestListSessionsPaginateTypeDef(TypedDict):
    portalId: str
    sessionId: NotRequired[str]
    sortBy: NotRequired[SessionSortByType]
    status: NotRequired[SessionStatusType]
    username: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListNetworkSettingsResponseTypeDef(TypedDict):
    networkSettings: List[NetworkSettingsSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListPortalsResponseTypeDef(TypedDict):
    portals: List[PortalSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSessionsResponseTypeDef(TypedDict):
    sessions: List[SessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTrustStoresResponseTypeDef(TypedDict):
    trustStores: List[TrustStoreSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListUserAccessLoggingSettingsResponseTypeDef(TypedDict):
    userAccessLoggingSettings: List[UserAccessLoggingSettingsSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UserSettingsSummaryTypeDef(TypedDict):
    userSettingsArn: str
    cookieSynchronizationConfiguration: NotRequired[CookieSynchronizationConfigurationOutputTypeDef]
    copyAllowed: NotRequired[EnabledTypeType]
    deepLinkAllowed: NotRequired[EnabledTypeType]
    disconnectTimeoutInMinutes: NotRequired[int]
    downloadAllowed: NotRequired[EnabledTypeType]
    idleDisconnectTimeoutInMinutes: NotRequired[int]
    pasteAllowed: NotRequired[EnabledTypeType]
    printAllowed: NotRequired[EnabledTypeType]
    uploadAllowed: NotRequired[EnabledTypeType]


class UserSettingsTypeDef(TypedDict):
    userSettingsArn: str
    additionalEncryptionContext: NotRequired[Dict[str, str]]
    associatedPortalArns: NotRequired[List[str]]
    cookieSynchronizationConfiguration: NotRequired[CookieSynchronizationConfigurationOutputTypeDef]
    copyAllowed: NotRequired[EnabledTypeType]
    customerManagedKey: NotRequired[str]
    deepLinkAllowed: NotRequired[EnabledTypeType]
    disconnectTimeoutInMinutes: NotRequired[int]
    downloadAllowed: NotRequired[EnabledTypeType]
    idleDisconnectTimeoutInMinutes: NotRequired[int]
    pasteAllowed: NotRequired[EnabledTypeType]
    printAllowed: NotRequired[EnabledTypeType]
    uploadAllowed: NotRequired[EnabledTypeType]


class CreateUserSettingsRequestRequestTypeDef(TypedDict):
    copyAllowed: EnabledTypeType
    downloadAllowed: EnabledTypeType
    pasteAllowed: EnabledTypeType
    printAllowed: EnabledTypeType
    uploadAllowed: EnabledTypeType
    additionalEncryptionContext: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]
    cookieSynchronizationConfiguration: NotRequired[CookieSynchronizationConfigurationTypeDef]
    customerManagedKey: NotRequired[str]
    deepLinkAllowed: NotRequired[EnabledTypeType]
    disconnectTimeoutInMinutes: NotRequired[int]
    idleDisconnectTimeoutInMinutes: NotRequired[int]
    tags: NotRequired[Sequence[TagTypeDef]]


class UpdateUserSettingsRequestRequestTypeDef(TypedDict):
    userSettingsArn: str
    clientToken: NotRequired[str]
    cookieSynchronizationConfiguration: NotRequired[CookieSynchronizationConfigurationTypeDef]
    copyAllowed: NotRequired[EnabledTypeType]
    deepLinkAllowed: NotRequired[EnabledTypeType]
    disconnectTimeoutInMinutes: NotRequired[int]
    downloadAllowed: NotRequired[EnabledTypeType]
    idleDisconnectTimeoutInMinutes: NotRequired[int]
    pasteAllowed: NotRequired[EnabledTypeType]
    printAllowed: NotRequired[EnabledTypeType]
    uploadAllowed: NotRequired[EnabledTypeType]


class GetIpAccessSettingsResponseTypeDef(TypedDict):
    ipAccessSettings: IpAccessSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateIpAccessSettingsResponseTypeDef(TypedDict):
    ipAccessSettings: IpAccessSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class InlineRedactionConfigurationOutputTypeDef(TypedDict):
    inlineRedactionPatterns: List[InlineRedactionPatternOutputTypeDef]
    globalConfidenceLevel: NotRequired[int]
    globalEnforcedUrls: NotRequired[List[str]]
    globalExemptUrls: NotRequired[List[str]]


InlineRedactionPatternUnionTypeDef = Union[
    InlineRedactionPatternTypeDef, InlineRedactionPatternOutputTypeDef
]


class ListUserSettingsResponseTypeDef(TypedDict):
    userSettings: List[UserSettingsSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetUserSettingsResponseTypeDef(TypedDict):
    userSettings: UserSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateUserSettingsResponseTypeDef(TypedDict):
    userSettings: UserSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DataProtectionSettingsTypeDef(TypedDict):
    dataProtectionSettingsArn: str
    additionalEncryptionContext: NotRequired[Dict[str, str]]
    associatedPortalArns: NotRequired[List[str]]
    creationDate: NotRequired[datetime]
    customerManagedKey: NotRequired[str]
    description: NotRequired[str]
    displayName: NotRequired[str]
    inlineRedactionConfiguration: NotRequired[InlineRedactionConfigurationOutputTypeDef]


class InlineRedactionConfigurationTypeDef(TypedDict):
    inlineRedactionPatterns: Sequence[InlineRedactionPatternUnionTypeDef]
    globalConfidenceLevel: NotRequired[int]
    globalEnforcedUrls: NotRequired[Sequence[str]]
    globalExemptUrls: NotRequired[Sequence[str]]


class GetDataProtectionSettingsResponseTypeDef(TypedDict):
    dataProtectionSettings: DataProtectionSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDataProtectionSettingsResponseTypeDef(TypedDict):
    dataProtectionSettings: DataProtectionSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataProtectionSettingsRequestRequestTypeDef(TypedDict):
    additionalEncryptionContext: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]
    customerManagedKey: NotRequired[str]
    description: NotRequired[str]
    displayName: NotRequired[str]
    inlineRedactionConfiguration: NotRequired[InlineRedactionConfigurationTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]


class UpdateDataProtectionSettingsRequestRequestTypeDef(TypedDict):
    dataProtectionSettingsArn: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    displayName: NotRequired[str]
    inlineRedactionConfiguration: NotRequired[InlineRedactionConfigurationTypeDef]
