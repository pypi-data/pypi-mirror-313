"""
Type annotations for license-manager-user-subscriptions service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager_user_subscriptions/type_defs/)

Usage::

    ```python
    from mypy_boto3_license_manager_user_subscriptions.type_defs import DomainNetworkSettingsOutputTypeDef

    data: DomainNetworkSettingsOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ActiveDirectoryTypeType,
    LicenseServerEndpointProvisioningStatusType,
    LicenseServerHealthStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ActiveDirectoryIdentityProviderOutputTypeDef",
    "ActiveDirectoryIdentityProviderTypeDef",
    "ActiveDirectoryIdentityProviderUnionTypeDef",
    "ActiveDirectorySettingsOutputTypeDef",
    "ActiveDirectorySettingsTypeDef",
    "AssociateUserRequestRequestTypeDef",
    "AssociateUserResponseTypeDef",
    "CreateLicenseServerEndpointRequestRequestTypeDef",
    "CreateLicenseServerEndpointResponseTypeDef",
    "CredentialsProviderTypeDef",
    "DeleteLicenseServerEndpointRequestRequestTypeDef",
    "DeleteLicenseServerEndpointResponseTypeDef",
    "DeregisterIdentityProviderRequestRequestTypeDef",
    "DeregisterIdentityProviderResponseTypeDef",
    "DisassociateUserRequestRequestTypeDef",
    "DisassociateUserResponseTypeDef",
    "DomainNetworkSettingsOutputTypeDef",
    "DomainNetworkSettingsTypeDef",
    "FilterTypeDef",
    "IdentityProviderOutputTypeDef",
    "IdentityProviderSummaryTypeDef",
    "IdentityProviderTypeDef",
    "InstanceSummaryTypeDef",
    "InstanceUserSummaryTypeDef",
    "LicenseServerEndpointTypeDef",
    "LicenseServerSettingsTypeDef",
    "LicenseServerTypeDef",
    "ListIdentityProvidersRequestListIdentityProvidersPaginateTypeDef",
    "ListIdentityProvidersRequestRequestTypeDef",
    "ListIdentityProvidersResponseTypeDef",
    "ListInstancesRequestListInstancesPaginateTypeDef",
    "ListInstancesRequestRequestTypeDef",
    "ListInstancesResponseTypeDef",
    "ListLicenseServerEndpointsRequestListLicenseServerEndpointsPaginateTypeDef",
    "ListLicenseServerEndpointsRequestRequestTypeDef",
    "ListLicenseServerEndpointsResponseTypeDef",
    "ListProductSubscriptionsRequestListProductSubscriptionsPaginateTypeDef",
    "ListProductSubscriptionsRequestRequestTypeDef",
    "ListProductSubscriptionsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListUserAssociationsRequestListUserAssociationsPaginateTypeDef",
    "ListUserAssociationsRequestRequestTypeDef",
    "ListUserAssociationsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ProductUserSummaryTypeDef",
    "RdsSalSettingsTypeDef",
    "RegisterIdentityProviderRequestRequestTypeDef",
    "RegisterIdentityProviderResponseTypeDef",
    "ResponseMetadataTypeDef",
    "SecretsManagerCredentialsProviderTypeDef",
    "ServerEndpointTypeDef",
    "ServerSettingsTypeDef",
    "SettingsOutputTypeDef",
    "SettingsTypeDef",
    "StartProductSubscriptionRequestRequestTypeDef",
    "StartProductSubscriptionResponseTypeDef",
    "StopProductSubscriptionRequestRequestTypeDef",
    "StopProductSubscriptionResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateIdentityProviderSettingsRequestRequestTypeDef",
    "UpdateIdentityProviderSettingsResponseTypeDef",
    "UpdateSettingsTypeDef",
)


class DomainNetworkSettingsOutputTypeDef(TypedDict):
    Subnets: List[str]


class DomainNetworkSettingsTypeDef(TypedDict):
    Subnets: Sequence[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class SecretsManagerCredentialsProviderTypeDef(TypedDict):
    SecretId: NotRequired[str]


class DeleteLicenseServerEndpointRequestRequestTypeDef(TypedDict):
    LicenseServerEndpointArn: str
    ServerType: Literal["RDS_SAL"]


class FilterTypeDef(TypedDict):
    Attribute: NotRequired[str]
    Operation: NotRequired[str]
    Value: NotRequired[str]


class SettingsOutputTypeDef(TypedDict):
    SecurityGroupId: str
    Subnets: List[str]


class InstanceSummaryTypeDef(TypedDict):
    InstanceId: str
    Products: List[str]
    Status: str
    LastStatusCheckDate: NotRequired[str]
    StatusMessage: NotRequired[str]


class LicenseServerTypeDef(TypedDict):
    HealthStatus: NotRequired[LicenseServerHealthStatusType]
    Ipv4Address: NotRequired[str]
    ProvisioningStatus: NotRequired[LicenseServerEndpointProvisioningStatusType]


class ServerEndpointTypeDef(TypedDict):
    Endpoint: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class SettingsTypeDef(TypedDict):
    SecurityGroupId: str
    Subnets: Sequence[str]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateSettingsTypeDef(TypedDict):
    AddSubnets: Sequence[str]
    RemoveSubnets: Sequence[str]
    SecurityGroupId: NotRequired[str]


class CreateLicenseServerEndpointResponseTypeDef(TypedDict):
    IdentityProviderArn: str
    LicenseServerEndpointArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CredentialsProviderTypeDef(TypedDict):
    SecretsManagerCredentialsProvider: NotRequired[SecretsManagerCredentialsProviderTypeDef]


class ListIdentityProvidersRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListInstancesRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListLicenseServerEndpointsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListInstancesResponseTypeDef(TypedDict):
    InstanceSummaries: List[InstanceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LicenseServerEndpointTypeDef(TypedDict):
    CreationTime: NotRequired[datetime]
    IdentityProviderArn: NotRequired[str]
    LicenseServerEndpointArn: NotRequired[str]
    LicenseServerEndpointId: NotRequired[str]
    LicenseServerEndpointProvisioningStatus: NotRequired[
        LicenseServerEndpointProvisioningStatusType
    ]
    LicenseServers: NotRequired[List[LicenseServerTypeDef]]
    ServerEndpoint: NotRequired[ServerEndpointTypeDef]
    ServerType: NotRequired[Literal["RDS_SAL"]]
    StatusMessage: NotRequired[str]


class ListIdentityProvidersRequestListIdentityProvidersPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListInstancesRequestListInstancesPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLicenseServerEndpointsRequestListLicenseServerEndpointsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ActiveDirectorySettingsOutputTypeDef(TypedDict):
    DomainCredentialsProvider: NotRequired[CredentialsProviderTypeDef]
    DomainIpv4List: NotRequired[List[str]]
    DomainName: NotRequired[str]
    DomainNetworkSettings: NotRequired[DomainNetworkSettingsOutputTypeDef]


class ActiveDirectorySettingsTypeDef(TypedDict):
    DomainCredentialsProvider: NotRequired[CredentialsProviderTypeDef]
    DomainIpv4List: NotRequired[Sequence[str]]
    DomainName: NotRequired[str]
    DomainNetworkSettings: NotRequired[DomainNetworkSettingsTypeDef]


class RdsSalSettingsTypeDef(TypedDict):
    RdsSalCredentialsProvider: CredentialsProviderTypeDef


class DeleteLicenseServerEndpointResponseTypeDef(TypedDict):
    LicenseServerEndpoint: LicenseServerEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListLicenseServerEndpointsResponseTypeDef(TypedDict):
    LicenseServerEndpoints: List[LicenseServerEndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ActiveDirectoryIdentityProviderOutputTypeDef(TypedDict):
    ActiveDirectorySettings: NotRequired[ActiveDirectorySettingsOutputTypeDef]
    ActiveDirectoryType: NotRequired[ActiveDirectoryTypeType]
    DirectoryId: NotRequired[str]


class ActiveDirectoryIdentityProviderTypeDef(TypedDict):
    ActiveDirectorySettings: NotRequired[ActiveDirectorySettingsTypeDef]
    ActiveDirectoryType: NotRequired[ActiveDirectoryTypeType]
    DirectoryId: NotRequired[str]


class ServerSettingsTypeDef(TypedDict):
    RdsSalSettings: NotRequired[RdsSalSettingsTypeDef]


class IdentityProviderOutputTypeDef(TypedDict):
    ActiveDirectoryIdentityProvider: NotRequired[ActiveDirectoryIdentityProviderOutputTypeDef]


ActiveDirectoryIdentityProviderUnionTypeDef = Union[
    ActiveDirectoryIdentityProviderTypeDef, ActiveDirectoryIdentityProviderOutputTypeDef
]


class LicenseServerSettingsTypeDef(TypedDict):
    ServerSettings: ServerSettingsTypeDef
    ServerType: Literal["RDS_SAL"]


class IdentityProviderSummaryTypeDef(TypedDict):
    IdentityProvider: IdentityProviderOutputTypeDef
    Product: str
    Settings: SettingsOutputTypeDef
    Status: str
    FailureMessage: NotRequired[str]
    IdentityProviderArn: NotRequired[str]


class InstanceUserSummaryTypeDef(TypedDict):
    IdentityProvider: IdentityProviderOutputTypeDef
    InstanceId: str
    Status: str
    Username: str
    AssociationDate: NotRequired[str]
    DisassociationDate: NotRequired[str]
    Domain: NotRequired[str]
    InstanceUserArn: NotRequired[str]
    StatusMessage: NotRequired[str]


class ProductUserSummaryTypeDef(TypedDict):
    IdentityProvider: IdentityProviderOutputTypeDef
    Product: str
    Status: str
    Username: str
    Domain: NotRequired[str]
    ProductUserArn: NotRequired[str]
    StatusMessage: NotRequired[str]
    SubscriptionEndDate: NotRequired[str]
    SubscriptionStartDate: NotRequired[str]


class IdentityProviderTypeDef(TypedDict):
    ActiveDirectoryIdentityProvider: NotRequired[ActiveDirectoryIdentityProviderUnionTypeDef]


class CreateLicenseServerEndpointRequestRequestTypeDef(TypedDict):
    IdentityProviderArn: str
    LicenseServerSettings: LicenseServerSettingsTypeDef
    Tags: NotRequired[Mapping[str, str]]


class DeregisterIdentityProviderResponseTypeDef(TypedDict):
    IdentityProviderSummary: IdentityProviderSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListIdentityProvidersResponseTypeDef(TypedDict):
    IdentityProviderSummaries: List[IdentityProviderSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class RegisterIdentityProviderResponseTypeDef(TypedDict):
    IdentityProviderSummary: IdentityProviderSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateIdentityProviderSettingsResponseTypeDef(TypedDict):
    IdentityProviderSummary: IdentityProviderSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateUserResponseTypeDef(TypedDict):
    InstanceUserSummary: InstanceUserSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateUserResponseTypeDef(TypedDict):
    InstanceUserSummary: InstanceUserSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListUserAssociationsResponseTypeDef(TypedDict):
    InstanceUserSummaries: List[InstanceUserSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListProductSubscriptionsResponseTypeDef(TypedDict):
    ProductUserSummaries: List[ProductUserSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StartProductSubscriptionResponseTypeDef(TypedDict):
    ProductUserSummary: ProductUserSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StopProductSubscriptionResponseTypeDef(TypedDict):
    ProductUserSummary: ProductUserSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateUserRequestRequestTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    InstanceId: str
    Username: str
    Domain: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class DeregisterIdentityProviderRequestRequestTypeDef(TypedDict):
    IdentityProvider: NotRequired[IdentityProviderTypeDef]
    IdentityProviderArn: NotRequired[str]
    Product: NotRequired[str]


class DisassociateUserRequestRequestTypeDef(TypedDict):
    Domain: NotRequired[str]
    IdentityProvider: NotRequired[IdentityProviderTypeDef]
    InstanceId: NotRequired[str]
    InstanceUserArn: NotRequired[str]
    Username: NotRequired[str]


class ListProductSubscriptionsRequestListProductSubscriptionsPaginateTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Product: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProductSubscriptionsRequestRequestTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Product: NotRequired[str]


class ListUserAssociationsRequestListUserAssociationsPaginateTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    InstanceId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUserAssociationsRequestRequestTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    InstanceId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class RegisterIdentityProviderRequestRequestTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    Product: str
    Settings: NotRequired[SettingsTypeDef]
    Tags: NotRequired[Mapping[str, str]]


class StartProductSubscriptionRequestRequestTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    Product: str
    Username: str
    Domain: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class StopProductSubscriptionRequestRequestTypeDef(TypedDict):
    Domain: NotRequired[str]
    IdentityProvider: NotRequired[IdentityProviderTypeDef]
    Product: NotRequired[str]
    ProductUserArn: NotRequired[str]
    Username: NotRequired[str]


class UpdateIdentityProviderSettingsRequestRequestTypeDef(TypedDict):
    UpdateSettings: UpdateSettingsTypeDef
    IdentityProvider: NotRequired[IdentityProviderTypeDef]
    IdentityProviderArn: NotRequired[str]
    Product: NotRequired[str]
