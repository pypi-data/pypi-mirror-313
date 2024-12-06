"""
Type annotations for ds service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/type_defs/)

Usage::

    ```python
    from mypy_boto3_ds.type_defs import AcceptSharedDirectoryRequestRequestTypeDef

    data: AcceptSharedDirectoryRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    CertificateStateType,
    CertificateTypeType,
    ClientAuthenticationStatusType,
    ClientAuthenticationTypeType,
    DataAccessStatusType,
    DirectoryConfigurationStatusType,
    DirectoryEditionType,
    DirectorySizeType,
    DirectoryStageType,
    DirectoryTypeType,
    DomainControllerStatusType,
    IpRouteStatusMsgType,
    LDAPSStatusType,
    OSVersionType,
    RadiusAuthenticationProtocolType,
    RadiusStatusType,
    RegionTypeType,
    SchemaExtensionStatusType,
    SelectiveAuthType,
    ShareMethodType,
    ShareStatusType,
    SnapshotStatusType,
    SnapshotTypeType,
    TopicStatusType,
    TrustDirectionType,
    TrustStateType,
    TrustTypeType,
    UpdateStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AcceptSharedDirectoryRequestRequestTypeDef",
    "AcceptSharedDirectoryResultTypeDef",
    "AddIpRoutesRequestRequestTypeDef",
    "AddRegionRequestRequestTypeDef",
    "AddTagsToResourceRequestRequestTypeDef",
    "AttributeTypeDef",
    "CancelSchemaExtensionRequestRequestTypeDef",
    "CertificateInfoTypeDef",
    "CertificateTypeDef",
    "ClientAuthenticationSettingInfoTypeDef",
    "ClientCertAuthSettingsTypeDef",
    "ComputerTypeDef",
    "ConditionalForwarderTypeDef",
    "ConnectDirectoryRequestRequestTypeDef",
    "ConnectDirectoryResultTypeDef",
    "CreateAliasRequestRequestTypeDef",
    "CreateAliasResultTypeDef",
    "CreateComputerRequestRequestTypeDef",
    "CreateComputerResultTypeDef",
    "CreateConditionalForwarderRequestRequestTypeDef",
    "CreateDirectoryRequestRequestTypeDef",
    "CreateDirectoryResultTypeDef",
    "CreateLogSubscriptionRequestRequestTypeDef",
    "CreateMicrosoftADRequestRequestTypeDef",
    "CreateMicrosoftADResultTypeDef",
    "CreateSnapshotRequestRequestTypeDef",
    "CreateSnapshotResultTypeDef",
    "CreateTrustRequestRequestTypeDef",
    "CreateTrustResultTypeDef",
    "DeleteConditionalForwarderRequestRequestTypeDef",
    "DeleteDirectoryRequestRequestTypeDef",
    "DeleteDirectoryResultTypeDef",
    "DeleteLogSubscriptionRequestRequestTypeDef",
    "DeleteSnapshotRequestRequestTypeDef",
    "DeleteSnapshotResultTypeDef",
    "DeleteTrustRequestRequestTypeDef",
    "DeleteTrustResultTypeDef",
    "DeregisterCertificateRequestRequestTypeDef",
    "DeregisterEventTopicRequestRequestTypeDef",
    "DescribeCertificateRequestRequestTypeDef",
    "DescribeCertificateResultTypeDef",
    "DescribeClientAuthenticationSettingsRequestDescribeClientAuthenticationSettingsPaginateTypeDef",
    "DescribeClientAuthenticationSettingsRequestRequestTypeDef",
    "DescribeClientAuthenticationSettingsResultTypeDef",
    "DescribeConditionalForwardersRequestRequestTypeDef",
    "DescribeConditionalForwardersResultTypeDef",
    "DescribeDirectoriesRequestDescribeDirectoriesPaginateTypeDef",
    "DescribeDirectoriesRequestRequestTypeDef",
    "DescribeDirectoriesResultTypeDef",
    "DescribeDirectoryDataAccessRequestRequestTypeDef",
    "DescribeDirectoryDataAccessResultTypeDef",
    "DescribeDomainControllersRequestDescribeDomainControllersPaginateTypeDef",
    "DescribeDomainControllersRequestRequestTypeDef",
    "DescribeDomainControllersResultTypeDef",
    "DescribeEventTopicsRequestRequestTypeDef",
    "DescribeEventTopicsResultTypeDef",
    "DescribeLDAPSSettingsRequestDescribeLDAPSSettingsPaginateTypeDef",
    "DescribeLDAPSSettingsRequestRequestTypeDef",
    "DescribeLDAPSSettingsResultTypeDef",
    "DescribeRegionsRequestDescribeRegionsPaginateTypeDef",
    "DescribeRegionsRequestRequestTypeDef",
    "DescribeRegionsResultTypeDef",
    "DescribeSettingsRequestRequestTypeDef",
    "DescribeSettingsResultTypeDef",
    "DescribeSharedDirectoriesRequestDescribeSharedDirectoriesPaginateTypeDef",
    "DescribeSharedDirectoriesRequestRequestTypeDef",
    "DescribeSharedDirectoriesResultTypeDef",
    "DescribeSnapshotsRequestDescribeSnapshotsPaginateTypeDef",
    "DescribeSnapshotsRequestRequestTypeDef",
    "DescribeSnapshotsResultTypeDef",
    "DescribeTrustsRequestDescribeTrustsPaginateTypeDef",
    "DescribeTrustsRequestRequestTypeDef",
    "DescribeTrustsResultTypeDef",
    "DescribeUpdateDirectoryRequestDescribeUpdateDirectoryPaginateTypeDef",
    "DescribeUpdateDirectoryRequestRequestTypeDef",
    "DescribeUpdateDirectoryResultTypeDef",
    "DirectoryConnectSettingsDescriptionTypeDef",
    "DirectoryConnectSettingsTypeDef",
    "DirectoryDescriptionTypeDef",
    "DirectoryLimitsTypeDef",
    "DirectoryVpcSettingsDescriptionTypeDef",
    "DirectoryVpcSettingsOutputTypeDef",
    "DirectoryVpcSettingsTypeDef",
    "DisableClientAuthenticationRequestRequestTypeDef",
    "DisableDirectoryDataAccessRequestRequestTypeDef",
    "DisableLDAPSRequestRequestTypeDef",
    "DisableRadiusRequestRequestTypeDef",
    "DisableSsoRequestRequestTypeDef",
    "DomainControllerTypeDef",
    "EnableClientAuthenticationRequestRequestTypeDef",
    "EnableDirectoryDataAccessRequestRequestTypeDef",
    "EnableLDAPSRequestRequestTypeDef",
    "EnableRadiusRequestRequestTypeDef",
    "EnableSsoRequestRequestTypeDef",
    "EventTopicTypeDef",
    "GetDirectoryLimitsResultTypeDef",
    "GetSnapshotLimitsRequestRequestTypeDef",
    "GetSnapshotLimitsResultTypeDef",
    "IpRouteInfoTypeDef",
    "IpRouteTypeDef",
    "LDAPSSettingInfoTypeDef",
    "ListCertificatesRequestListCertificatesPaginateTypeDef",
    "ListCertificatesRequestRequestTypeDef",
    "ListCertificatesResultTypeDef",
    "ListIpRoutesRequestListIpRoutesPaginateTypeDef",
    "ListIpRoutesRequestRequestTypeDef",
    "ListIpRoutesResultTypeDef",
    "ListLogSubscriptionsRequestListLogSubscriptionsPaginateTypeDef",
    "ListLogSubscriptionsRequestRequestTypeDef",
    "ListLogSubscriptionsResultTypeDef",
    "ListSchemaExtensionsRequestListSchemaExtensionsPaginateTypeDef",
    "ListSchemaExtensionsRequestRequestTypeDef",
    "ListSchemaExtensionsResultTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResultTypeDef",
    "LogSubscriptionTypeDef",
    "OSUpdateSettingsTypeDef",
    "OwnerDirectoryDescriptionTypeDef",
    "PaginatorConfigTypeDef",
    "RadiusSettingsOutputTypeDef",
    "RadiusSettingsTypeDef",
    "RegionDescriptionTypeDef",
    "RegionsInfoTypeDef",
    "RegisterCertificateRequestRequestTypeDef",
    "RegisterCertificateResultTypeDef",
    "RegisterEventTopicRequestRequestTypeDef",
    "RejectSharedDirectoryRequestRequestTypeDef",
    "RejectSharedDirectoryResultTypeDef",
    "RemoveIpRoutesRequestRequestTypeDef",
    "RemoveRegionRequestRequestTypeDef",
    "RemoveTagsFromResourceRequestRequestTypeDef",
    "ResetUserPasswordRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreFromSnapshotRequestRequestTypeDef",
    "SchemaExtensionInfoTypeDef",
    "SettingEntryTypeDef",
    "SettingTypeDef",
    "ShareDirectoryRequestRequestTypeDef",
    "ShareDirectoryResultTypeDef",
    "ShareTargetTypeDef",
    "SharedDirectoryTypeDef",
    "SnapshotLimitsTypeDef",
    "SnapshotTypeDef",
    "StartSchemaExtensionRequestRequestTypeDef",
    "StartSchemaExtensionResultTypeDef",
    "TagTypeDef",
    "TrustTypeDef",
    "UnshareDirectoryRequestRequestTypeDef",
    "UnshareDirectoryResultTypeDef",
    "UnshareTargetTypeDef",
    "UpdateConditionalForwarderRequestRequestTypeDef",
    "UpdateDirectorySetupRequestRequestTypeDef",
    "UpdateInfoEntryTypeDef",
    "UpdateNumberOfDomainControllersRequestRequestTypeDef",
    "UpdateRadiusRequestRequestTypeDef",
    "UpdateSettingsRequestRequestTypeDef",
    "UpdateSettingsResultTypeDef",
    "UpdateTrustRequestRequestTypeDef",
    "UpdateTrustResultTypeDef",
    "UpdateValueTypeDef",
    "VerifyTrustRequestRequestTypeDef",
    "VerifyTrustResultTypeDef",
)


class AcceptSharedDirectoryRequestRequestTypeDef(TypedDict):
    SharedDirectoryId: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class SharedDirectoryTypeDef(TypedDict):
    OwnerAccountId: NotRequired[str]
    OwnerDirectoryId: NotRequired[str]
    ShareMethod: NotRequired[ShareMethodType]
    SharedAccountId: NotRequired[str]
    SharedDirectoryId: NotRequired[str]
    ShareStatus: NotRequired[ShareStatusType]
    ShareNotes: NotRequired[str]
    CreatedDateTime: NotRequired[datetime]
    LastUpdatedDateTime: NotRequired[datetime]


class IpRouteTypeDef(TypedDict):
    CidrIp: NotRequired[str]
    Description: NotRequired[str]


class DirectoryVpcSettingsTypeDef(TypedDict):
    VpcId: str
    SubnetIds: Sequence[str]


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class AttributeTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]


class CancelSchemaExtensionRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    SchemaExtensionId: str


CertificateInfoTypeDef = TypedDict(
    "CertificateInfoTypeDef",
    {
        "CertificateId": NotRequired[str],
        "CommonName": NotRequired[str],
        "State": NotRequired[CertificateStateType],
        "ExpiryDateTime": NotRequired[datetime],
        "Type": NotRequired[CertificateTypeType],
    },
)


class ClientCertAuthSettingsTypeDef(TypedDict):
    OCSPUrl: NotRequired[str]


ClientAuthenticationSettingInfoTypeDef = TypedDict(
    "ClientAuthenticationSettingInfoTypeDef",
    {
        "Type": NotRequired[ClientAuthenticationTypeType],
        "Status": NotRequired[ClientAuthenticationStatusType],
        "LastUpdatedDateTime": NotRequired[datetime],
    },
)


class ConditionalForwarderTypeDef(TypedDict):
    RemoteDomainName: NotRequired[str]
    DnsIpAddrs: NotRequired[List[str]]
    ReplicationScope: NotRequired[Literal["Domain"]]


class DirectoryConnectSettingsTypeDef(TypedDict):
    VpcId: str
    SubnetIds: Sequence[str]
    CustomerDnsIps: Sequence[str]
    CustomerUserName: str


class CreateAliasRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    Alias: str


class CreateConditionalForwarderRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    RemoteDomainName: str
    DnsIpAddrs: Sequence[str]


class CreateLogSubscriptionRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    LogGroupName: str


class CreateSnapshotRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    Name: NotRequired[str]


class CreateTrustRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    RemoteDomainName: str
    TrustPassword: str
    TrustDirection: TrustDirectionType
    TrustType: NotRequired[TrustTypeType]
    ConditionalForwarderIpAddrs: NotRequired[Sequence[str]]
    SelectiveAuth: NotRequired[SelectiveAuthType]


class DeleteConditionalForwarderRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    RemoteDomainName: str


class DeleteDirectoryRequestRequestTypeDef(TypedDict):
    DirectoryId: str


class DeleteLogSubscriptionRequestRequestTypeDef(TypedDict):
    DirectoryId: str


class DeleteSnapshotRequestRequestTypeDef(TypedDict):
    SnapshotId: str


class DeleteTrustRequestRequestTypeDef(TypedDict):
    TrustId: str
    DeleteAssociatedConditionalForwarder: NotRequired[bool]


class DeregisterCertificateRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    CertificateId: str


class DeregisterEventTopicRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    TopicName: str


class DescribeCertificateRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    CertificateId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


DescribeClientAuthenticationSettingsRequestRequestTypeDef = TypedDict(
    "DescribeClientAuthenticationSettingsRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "Type": NotRequired[ClientAuthenticationTypeType],
        "NextToken": NotRequired[str],
        "Limit": NotRequired[int],
    },
)


class DescribeConditionalForwardersRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    RemoteDomainNames: NotRequired[Sequence[str]]


class DescribeDirectoriesRequestRequestTypeDef(TypedDict):
    DirectoryIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]


class DescribeDirectoryDataAccessRequestRequestTypeDef(TypedDict):
    DirectoryId: str


class DescribeDomainControllersRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    DomainControllerIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]


class DomainControllerTypeDef(TypedDict):
    DirectoryId: NotRequired[str]
    DomainControllerId: NotRequired[str]
    DnsIpAddr: NotRequired[str]
    VpcId: NotRequired[str]
    SubnetId: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    Status: NotRequired[DomainControllerStatusType]
    StatusReason: NotRequired[str]
    LaunchTime: NotRequired[datetime]
    StatusLastUpdatedDateTime: NotRequired[datetime]


class DescribeEventTopicsRequestRequestTypeDef(TypedDict):
    DirectoryId: NotRequired[str]
    TopicNames: NotRequired[Sequence[str]]


class EventTopicTypeDef(TypedDict):
    DirectoryId: NotRequired[str]
    TopicName: NotRequired[str]
    TopicArn: NotRequired[str]
    CreatedDateTime: NotRequired[datetime]
    Status: NotRequired[TopicStatusType]


DescribeLDAPSSettingsRequestRequestTypeDef = TypedDict(
    "DescribeLDAPSSettingsRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "Type": NotRequired[Literal["Client"]],
        "NextToken": NotRequired[str],
        "Limit": NotRequired[int],
    },
)


class LDAPSSettingInfoTypeDef(TypedDict):
    LDAPSStatus: NotRequired[LDAPSStatusType]
    LDAPSStatusReason: NotRequired[str]
    LastUpdatedDateTime: NotRequired[datetime]


DescribeRegionsRequestRequestTypeDef = TypedDict(
    "DescribeRegionsRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "RegionName": NotRequired[str],
        "NextToken": NotRequired[str],
    },
)


class DescribeSettingsRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    Status: NotRequired[DirectoryConfigurationStatusType]
    NextToken: NotRequired[str]


SettingEntryTypeDef = TypedDict(
    "SettingEntryTypeDef",
    {
        "Type": NotRequired[str],
        "Name": NotRequired[str],
        "AllowedValues": NotRequired[str],
        "AppliedValue": NotRequired[str],
        "RequestedValue": NotRequired[str],
        "RequestStatus": NotRequired[DirectoryConfigurationStatusType],
        "RequestDetailedStatus": NotRequired[Dict[str, DirectoryConfigurationStatusType]],
        "RequestStatusMessage": NotRequired[str],
        "LastUpdatedDateTime": NotRequired[datetime],
        "LastRequestedDateTime": NotRequired[datetime],
        "DataType": NotRequired[str],
    },
)


class DescribeSharedDirectoriesRequestRequestTypeDef(TypedDict):
    OwnerDirectoryId: str
    SharedDirectoryIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]


class DescribeSnapshotsRequestRequestTypeDef(TypedDict):
    DirectoryId: NotRequired[str]
    SnapshotIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]


SnapshotTypeDef = TypedDict(
    "SnapshotTypeDef",
    {
        "DirectoryId": NotRequired[str],
        "SnapshotId": NotRequired[str],
        "Type": NotRequired[SnapshotTypeType],
        "Name": NotRequired[str],
        "Status": NotRequired[SnapshotStatusType],
        "StartTime": NotRequired[datetime],
    },
)


class DescribeTrustsRequestRequestTypeDef(TypedDict):
    DirectoryId: NotRequired[str]
    TrustIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]


class TrustTypeDef(TypedDict):
    DirectoryId: NotRequired[str]
    TrustId: NotRequired[str]
    RemoteDomainName: NotRequired[str]
    TrustType: NotRequired[TrustTypeType]
    TrustDirection: NotRequired[TrustDirectionType]
    TrustState: NotRequired[TrustStateType]
    CreatedDateTime: NotRequired[datetime]
    LastUpdatedDateTime: NotRequired[datetime]
    StateLastUpdatedDateTime: NotRequired[datetime]
    TrustStateReason: NotRequired[str]
    SelectiveAuth: NotRequired[SelectiveAuthType]


DescribeUpdateDirectoryRequestRequestTypeDef = TypedDict(
    "DescribeUpdateDirectoryRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "UpdateType": Literal["OS"],
        "RegionName": NotRequired[str],
        "NextToken": NotRequired[str],
    },
)


class DirectoryConnectSettingsDescriptionTypeDef(TypedDict):
    VpcId: NotRequired[str]
    SubnetIds: NotRequired[List[str]]
    CustomerUserName: NotRequired[str]
    SecurityGroupId: NotRequired[str]
    AvailabilityZones: NotRequired[List[str]]
    ConnectIps: NotRequired[List[str]]


class DirectoryVpcSettingsDescriptionTypeDef(TypedDict):
    VpcId: NotRequired[str]
    SubnetIds: NotRequired[List[str]]
    SecurityGroupId: NotRequired[str]
    AvailabilityZones: NotRequired[List[str]]


class RadiusSettingsOutputTypeDef(TypedDict):
    RadiusServers: NotRequired[List[str]]
    RadiusPort: NotRequired[int]
    RadiusTimeout: NotRequired[int]
    RadiusRetries: NotRequired[int]
    SharedSecret: NotRequired[str]
    AuthenticationProtocol: NotRequired[RadiusAuthenticationProtocolType]
    DisplayLabel: NotRequired[str]
    UseSameUsername: NotRequired[bool]


class RegionsInfoTypeDef(TypedDict):
    PrimaryRegion: NotRequired[str]
    AdditionalRegions: NotRequired[List[str]]


class DirectoryLimitsTypeDef(TypedDict):
    CloudOnlyDirectoriesLimit: NotRequired[int]
    CloudOnlyDirectoriesCurrentCount: NotRequired[int]
    CloudOnlyDirectoriesLimitReached: NotRequired[bool]
    CloudOnlyMicrosoftADLimit: NotRequired[int]
    CloudOnlyMicrosoftADCurrentCount: NotRequired[int]
    CloudOnlyMicrosoftADLimitReached: NotRequired[bool]
    ConnectedDirectoriesLimit: NotRequired[int]
    ConnectedDirectoriesCurrentCount: NotRequired[int]
    ConnectedDirectoriesLimitReached: NotRequired[bool]


class DirectoryVpcSettingsOutputTypeDef(TypedDict):
    VpcId: str
    SubnetIds: List[str]


DisableClientAuthenticationRequestRequestTypeDef = TypedDict(
    "DisableClientAuthenticationRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "Type": ClientAuthenticationTypeType,
    },
)


class DisableDirectoryDataAccessRequestRequestTypeDef(TypedDict):
    DirectoryId: str


DisableLDAPSRequestRequestTypeDef = TypedDict(
    "DisableLDAPSRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "Type": Literal["Client"],
    },
)


class DisableRadiusRequestRequestTypeDef(TypedDict):
    DirectoryId: str


class DisableSsoRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    UserName: NotRequired[str]
    Password: NotRequired[str]


EnableClientAuthenticationRequestRequestTypeDef = TypedDict(
    "EnableClientAuthenticationRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "Type": ClientAuthenticationTypeType,
    },
)


class EnableDirectoryDataAccessRequestRequestTypeDef(TypedDict):
    DirectoryId: str


EnableLDAPSRequestRequestTypeDef = TypedDict(
    "EnableLDAPSRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "Type": Literal["Client"],
    },
)


class RadiusSettingsTypeDef(TypedDict):
    RadiusServers: NotRequired[Sequence[str]]
    RadiusPort: NotRequired[int]
    RadiusTimeout: NotRequired[int]
    RadiusRetries: NotRequired[int]
    SharedSecret: NotRequired[str]
    AuthenticationProtocol: NotRequired[RadiusAuthenticationProtocolType]
    DisplayLabel: NotRequired[str]
    UseSameUsername: NotRequired[bool]


class EnableSsoRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    UserName: NotRequired[str]
    Password: NotRequired[str]


class GetSnapshotLimitsRequestRequestTypeDef(TypedDict):
    DirectoryId: str


class SnapshotLimitsTypeDef(TypedDict):
    ManualSnapshotsLimit: NotRequired[int]
    ManualSnapshotsCurrentCount: NotRequired[int]
    ManualSnapshotsLimitReached: NotRequired[bool]


class IpRouteInfoTypeDef(TypedDict):
    DirectoryId: NotRequired[str]
    CidrIp: NotRequired[str]
    IpRouteStatusMsg: NotRequired[IpRouteStatusMsgType]
    AddedDateTime: NotRequired[datetime]
    IpRouteStatusReason: NotRequired[str]
    Description: NotRequired[str]


class ListCertificatesRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    NextToken: NotRequired[str]
    Limit: NotRequired[int]


class ListIpRoutesRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    NextToken: NotRequired[str]
    Limit: NotRequired[int]


class ListLogSubscriptionsRequestRequestTypeDef(TypedDict):
    DirectoryId: NotRequired[str]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]


class LogSubscriptionTypeDef(TypedDict):
    DirectoryId: NotRequired[str]
    LogGroupName: NotRequired[str]
    SubscriptionCreatedDateTime: NotRequired[datetime]


class ListSchemaExtensionsRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    NextToken: NotRequired[str]
    Limit: NotRequired[int]


class SchemaExtensionInfoTypeDef(TypedDict):
    DirectoryId: NotRequired[str]
    SchemaExtensionId: NotRequired[str]
    Description: NotRequired[str]
    SchemaExtensionStatus: NotRequired[SchemaExtensionStatusType]
    SchemaExtensionStatusReason: NotRequired[str]
    StartDateTime: NotRequired[datetime]
    EndDateTime: NotRequired[datetime]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceId: str
    NextToken: NotRequired[str]
    Limit: NotRequired[int]


class OSUpdateSettingsTypeDef(TypedDict):
    OSVersion: NotRequired[OSVersionType]


class RegisterEventTopicRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    TopicName: str


class RejectSharedDirectoryRequestRequestTypeDef(TypedDict):
    SharedDirectoryId: str


class RemoveIpRoutesRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    CidrIps: Sequence[str]


class RemoveRegionRequestRequestTypeDef(TypedDict):
    DirectoryId: str


class RemoveTagsFromResourceRequestRequestTypeDef(TypedDict):
    ResourceId: str
    TagKeys: Sequence[str]


class ResetUserPasswordRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    UserName: str
    NewPassword: str


class RestoreFromSnapshotRequestRequestTypeDef(TypedDict):
    SnapshotId: str


class SettingTypeDef(TypedDict):
    Name: str
    Value: str


ShareTargetTypeDef = TypedDict(
    "ShareTargetTypeDef",
    {
        "Id": str,
        "Type": Literal["ACCOUNT"],
    },
)


class StartSchemaExtensionRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    CreateSnapshotBeforeSchemaExtension: bool
    LdifContent: str
    Description: str


UnshareTargetTypeDef = TypedDict(
    "UnshareTargetTypeDef",
    {
        "Id": str,
        "Type": Literal["ACCOUNT"],
    },
)


class UpdateConditionalForwarderRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    RemoteDomainName: str
    DnsIpAddrs: Sequence[str]


class UpdateNumberOfDomainControllersRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    DesiredNumber: int


class UpdateTrustRequestRequestTypeDef(TypedDict):
    TrustId: str
    SelectiveAuth: NotRequired[SelectiveAuthType]


class VerifyTrustRequestRequestTypeDef(TypedDict):
    TrustId: str


class ConnectDirectoryResultTypeDef(TypedDict):
    DirectoryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAliasResultTypeDef(TypedDict):
    DirectoryId: str
    Alias: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDirectoryResultTypeDef(TypedDict):
    DirectoryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMicrosoftADResultTypeDef(TypedDict):
    DirectoryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSnapshotResultTypeDef(TypedDict):
    SnapshotId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTrustResultTypeDef(TypedDict):
    TrustId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDirectoryResultTypeDef(TypedDict):
    DirectoryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSnapshotResultTypeDef(TypedDict):
    SnapshotId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTrustResultTypeDef(TypedDict):
    TrustId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDirectoryDataAccessResultTypeDef(TypedDict):
    DataAccessStatus: DataAccessStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterCertificateResultTypeDef(TypedDict):
    CertificateId: str
    ResponseMetadata: ResponseMetadataTypeDef


class RejectSharedDirectoryResultTypeDef(TypedDict):
    SharedDirectoryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ShareDirectoryResultTypeDef(TypedDict):
    SharedDirectoryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartSchemaExtensionResultTypeDef(TypedDict):
    SchemaExtensionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UnshareDirectoryResultTypeDef(TypedDict):
    SharedDirectoryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSettingsResultTypeDef(TypedDict):
    DirectoryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTrustResultTypeDef(TypedDict):
    RequestId: str
    TrustId: str
    ResponseMetadata: ResponseMetadataTypeDef


class VerifyTrustResultTypeDef(TypedDict):
    TrustId: str
    ResponseMetadata: ResponseMetadataTypeDef


class AcceptSharedDirectoryResultTypeDef(TypedDict):
    SharedDirectory: SharedDirectoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSharedDirectoriesResultTypeDef(TypedDict):
    SharedDirectories: List[SharedDirectoryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AddIpRoutesRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    IpRoutes: Sequence[IpRouteTypeDef]
    UpdateSecurityGroupForDirectoryControllers: NotRequired[bool]


AddRegionRequestRequestTypeDef = TypedDict(
    "AddRegionRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "RegionName": str,
        "VPCSettings": DirectoryVpcSettingsTypeDef,
    },
)


class AddTagsToResourceRequestRequestTypeDef(TypedDict):
    ResourceId: str
    Tags: Sequence[TagTypeDef]


class CreateDirectoryRequestRequestTypeDef(TypedDict):
    Name: str
    Password: str
    Size: DirectorySizeType
    ShortName: NotRequired[str]
    Description: NotRequired[str]
    VpcSettings: NotRequired[DirectoryVpcSettingsTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateMicrosoftADRequestRequestTypeDef(TypedDict):
    Name: str
    Password: str
    VpcSettings: DirectoryVpcSettingsTypeDef
    ShortName: NotRequired[str]
    Description: NotRequired[str]
    Edition: NotRequired[DirectoryEditionType]
    Tags: NotRequired[Sequence[TagTypeDef]]


class ListTagsForResourceResultTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ComputerTypeDef(TypedDict):
    ComputerId: NotRequired[str]
    ComputerName: NotRequired[str]
    ComputerAttributes: NotRequired[List[AttributeTypeDef]]


class CreateComputerRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    ComputerName: str
    Password: str
    OrganizationalUnitDistinguishedName: NotRequired[str]
    ComputerAttributes: NotRequired[Sequence[AttributeTypeDef]]


class ListCertificatesResultTypeDef(TypedDict):
    CertificatesInfo: List[CertificateInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


CertificateTypeDef = TypedDict(
    "CertificateTypeDef",
    {
        "CertificateId": NotRequired[str],
        "State": NotRequired[CertificateStateType],
        "StateReason": NotRequired[str],
        "CommonName": NotRequired[str],
        "RegisteredDateTime": NotRequired[datetime],
        "ExpiryDateTime": NotRequired[datetime],
        "Type": NotRequired[CertificateTypeType],
        "ClientCertAuthSettings": NotRequired[ClientCertAuthSettingsTypeDef],
    },
)
RegisterCertificateRequestRequestTypeDef = TypedDict(
    "RegisterCertificateRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "CertificateData": str,
        "Type": NotRequired[CertificateTypeType],
        "ClientCertAuthSettings": NotRequired[ClientCertAuthSettingsTypeDef],
    },
)


class DescribeClientAuthenticationSettingsResultTypeDef(TypedDict):
    ClientAuthenticationSettingsInfo: List[ClientAuthenticationSettingInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeConditionalForwardersResultTypeDef(TypedDict):
    ConditionalForwarders: List[ConditionalForwarderTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ConnectDirectoryRequestRequestTypeDef(TypedDict):
    Name: str
    Password: str
    Size: DirectorySizeType
    ConnectSettings: DirectoryConnectSettingsTypeDef
    ShortName: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


DescribeClientAuthenticationSettingsRequestDescribeClientAuthenticationSettingsPaginateTypeDef = TypedDict(
    "DescribeClientAuthenticationSettingsRequestDescribeClientAuthenticationSettingsPaginateTypeDef",
    {
        "DirectoryId": str,
        "Type": NotRequired[ClientAuthenticationTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class DescribeDirectoriesRequestDescribeDirectoriesPaginateTypeDef(TypedDict):
    DirectoryIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDomainControllersRequestDescribeDomainControllersPaginateTypeDef(TypedDict):
    DirectoryId: str
    DomainControllerIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


DescribeLDAPSSettingsRequestDescribeLDAPSSettingsPaginateTypeDef = TypedDict(
    "DescribeLDAPSSettingsRequestDescribeLDAPSSettingsPaginateTypeDef",
    {
        "DirectoryId": str,
        "Type": NotRequired[Literal["Client"]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
DescribeRegionsRequestDescribeRegionsPaginateTypeDef = TypedDict(
    "DescribeRegionsRequestDescribeRegionsPaginateTypeDef",
    {
        "DirectoryId": str,
        "RegionName": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class DescribeSharedDirectoriesRequestDescribeSharedDirectoriesPaginateTypeDef(TypedDict):
    OwnerDirectoryId: str
    SharedDirectoryIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSnapshotsRequestDescribeSnapshotsPaginateTypeDef(TypedDict):
    DirectoryId: NotRequired[str]
    SnapshotIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTrustsRequestDescribeTrustsPaginateTypeDef(TypedDict):
    DirectoryId: NotRequired[str]
    TrustIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


DescribeUpdateDirectoryRequestDescribeUpdateDirectoryPaginateTypeDef = TypedDict(
    "DescribeUpdateDirectoryRequestDescribeUpdateDirectoryPaginateTypeDef",
    {
        "DirectoryId": str,
        "UpdateType": Literal["OS"],
        "RegionName": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListCertificatesRequestListCertificatesPaginateTypeDef(TypedDict):
    DirectoryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIpRoutesRequestListIpRoutesPaginateTypeDef(TypedDict):
    DirectoryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLogSubscriptionsRequestListLogSubscriptionsPaginateTypeDef(TypedDict):
    DirectoryId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSchemaExtensionsRequestListSchemaExtensionsPaginateTypeDef(TypedDict):
    DirectoryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(TypedDict):
    ResourceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDomainControllersResultTypeDef(TypedDict):
    DomainControllers: List[DomainControllerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeEventTopicsResultTypeDef(TypedDict):
    EventTopics: List[EventTopicTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLDAPSSettingsResultTypeDef(TypedDict):
    LDAPSSettingsInfo: List[LDAPSSettingInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeSettingsResultTypeDef(TypedDict):
    DirectoryId: str
    SettingEntries: List[SettingEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeSnapshotsResultTypeDef(TypedDict):
    Snapshots: List[SnapshotTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeTrustsResultTypeDef(TypedDict):
    Trusts: List[TrustTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class OwnerDirectoryDescriptionTypeDef(TypedDict):
    DirectoryId: NotRequired[str]
    AccountId: NotRequired[str]
    DnsIpAddrs: NotRequired[List[str]]
    VpcSettings: NotRequired[DirectoryVpcSettingsDescriptionTypeDef]
    RadiusSettings: NotRequired[RadiusSettingsOutputTypeDef]
    RadiusStatus: NotRequired[RadiusStatusType]


class GetDirectoryLimitsResultTypeDef(TypedDict):
    DirectoryLimits: DirectoryLimitsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


RegionDescriptionTypeDef = TypedDict(
    "RegionDescriptionTypeDef",
    {
        "DirectoryId": NotRequired[str],
        "RegionName": NotRequired[str],
        "RegionType": NotRequired[RegionTypeType],
        "Status": NotRequired[DirectoryStageType],
        "VpcSettings": NotRequired[DirectoryVpcSettingsOutputTypeDef],
        "DesiredNumberOfDomainControllers": NotRequired[int],
        "LaunchTime": NotRequired[datetime],
        "StatusLastUpdatedDateTime": NotRequired[datetime],
        "LastUpdatedDateTime": NotRequired[datetime],
    },
)


class EnableRadiusRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    RadiusSettings: RadiusSettingsTypeDef


class UpdateRadiusRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    RadiusSettings: RadiusSettingsTypeDef


class GetSnapshotLimitsResultTypeDef(TypedDict):
    SnapshotLimits: SnapshotLimitsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListIpRoutesResultTypeDef(TypedDict):
    IpRoutesInfo: List[IpRouteInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListLogSubscriptionsResultTypeDef(TypedDict):
    LogSubscriptions: List[LogSubscriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListSchemaExtensionsResultTypeDef(TypedDict):
    SchemaExtensionsInfo: List[SchemaExtensionInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateDirectorySetupRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    UpdateType: Literal["OS"]
    OSUpdateSettings: NotRequired[OSUpdateSettingsTypeDef]
    CreateSnapshotBeforeUpdate: NotRequired[bool]


class UpdateValueTypeDef(TypedDict):
    OSUpdateSettings: NotRequired[OSUpdateSettingsTypeDef]


class UpdateSettingsRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    Settings: Sequence[SettingTypeDef]


class ShareDirectoryRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    ShareTarget: ShareTargetTypeDef
    ShareMethod: ShareMethodType
    ShareNotes: NotRequired[str]


class UnshareDirectoryRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    UnshareTarget: UnshareTargetTypeDef


class CreateComputerResultTypeDef(TypedDict):
    Computer: ComputerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCertificateResultTypeDef(TypedDict):
    Certificate: CertificateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


DirectoryDescriptionTypeDef = TypedDict(
    "DirectoryDescriptionTypeDef",
    {
        "DirectoryId": NotRequired[str],
        "Name": NotRequired[str],
        "ShortName": NotRequired[str],
        "Size": NotRequired[DirectorySizeType],
        "Edition": NotRequired[DirectoryEditionType],
        "Alias": NotRequired[str],
        "AccessUrl": NotRequired[str],
        "Description": NotRequired[str],
        "DnsIpAddrs": NotRequired[List[str]],
        "Stage": NotRequired[DirectoryStageType],
        "ShareStatus": NotRequired[ShareStatusType],
        "ShareMethod": NotRequired[ShareMethodType],
        "ShareNotes": NotRequired[str],
        "LaunchTime": NotRequired[datetime],
        "StageLastUpdatedDateTime": NotRequired[datetime],
        "Type": NotRequired[DirectoryTypeType],
        "VpcSettings": NotRequired[DirectoryVpcSettingsDescriptionTypeDef],
        "ConnectSettings": NotRequired[DirectoryConnectSettingsDescriptionTypeDef],
        "RadiusSettings": NotRequired[RadiusSettingsOutputTypeDef],
        "RadiusStatus": NotRequired[RadiusStatusType],
        "StageReason": NotRequired[str],
        "SsoEnabled": NotRequired[bool],
        "DesiredNumberOfDomainControllers": NotRequired[int],
        "OwnerDirectoryDescription": NotRequired[OwnerDirectoryDescriptionTypeDef],
        "RegionsInfo": NotRequired[RegionsInfoTypeDef],
        "OsVersion": NotRequired[OSVersionType],
    },
)


class DescribeRegionsResultTypeDef(TypedDict):
    RegionsDescription: List[RegionDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateInfoEntryTypeDef(TypedDict):
    Region: NotRequired[str]
    Status: NotRequired[UpdateStatusType]
    StatusReason: NotRequired[str]
    InitiatedBy: NotRequired[str]
    NewValue: NotRequired[UpdateValueTypeDef]
    PreviousValue: NotRequired[UpdateValueTypeDef]
    StartTime: NotRequired[datetime]
    LastUpdatedDateTime: NotRequired[datetime]


class DescribeDirectoriesResultTypeDef(TypedDict):
    DirectoryDescriptions: List[DirectoryDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeUpdateDirectoryResultTypeDef(TypedDict):
    UpdateActivities: List[UpdateInfoEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
