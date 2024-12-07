"""
Type annotations for mediapackage service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackage/type_defs/)

Usage::

    ```python
    from mypy_boto3_mediapackage.type_defs import AuthorizationTypeDef

    data: AuthorizationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AdMarkersType,
    AdsOnDeliveryRestrictionsType,
    AdTriggersElementType,
    CmafEncryptionMethodType,
    EncryptionMethodType,
    ManifestLayoutType,
    OriginationType,
    PlaylistTypeType,
    PresetSpeke20AudioType,
    PresetSpeke20VideoType,
    ProfileType,
    SegmentTemplateFormatType,
    StatusType,
    StreamOrderType,
    UtcTimingType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AuthorizationTypeDef",
    "ChannelTypeDef",
    "CmafEncryptionOutputTypeDef",
    "CmafEncryptionTypeDef",
    "CmafEncryptionUnionTypeDef",
    "CmafPackageCreateOrUpdateParametersTypeDef",
    "CmafPackageTypeDef",
    "ConfigureLogsRequestRequestTypeDef",
    "ConfigureLogsResponseTypeDef",
    "CreateChannelRequestRequestTypeDef",
    "CreateChannelResponseTypeDef",
    "CreateHarvestJobRequestRequestTypeDef",
    "CreateHarvestJobResponseTypeDef",
    "CreateOriginEndpointRequestRequestTypeDef",
    "CreateOriginEndpointResponseTypeDef",
    "DashEncryptionOutputTypeDef",
    "DashEncryptionTypeDef",
    "DashEncryptionUnionTypeDef",
    "DashPackageOutputTypeDef",
    "DashPackageTypeDef",
    "DeleteChannelRequestRequestTypeDef",
    "DeleteOriginEndpointRequestRequestTypeDef",
    "DescribeChannelRequestRequestTypeDef",
    "DescribeChannelResponseTypeDef",
    "DescribeHarvestJobRequestRequestTypeDef",
    "DescribeHarvestJobResponseTypeDef",
    "DescribeOriginEndpointRequestRequestTypeDef",
    "DescribeOriginEndpointResponseTypeDef",
    "EgressAccessLogsTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionContractConfigurationTypeDef",
    "HarvestJobTypeDef",
    "HlsEncryptionOutputTypeDef",
    "HlsEncryptionTypeDef",
    "HlsEncryptionUnionTypeDef",
    "HlsIngestTypeDef",
    "HlsManifestCreateOrUpdateParametersTypeDef",
    "HlsManifestTypeDef",
    "HlsPackageOutputTypeDef",
    "HlsPackageTypeDef",
    "IngestEndpointTypeDef",
    "IngressAccessLogsTypeDef",
    "ListChannelsRequestListChannelsPaginateTypeDef",
    "ListChannelsRequestRequestTypeDef",
    "ListChannelsResponseTypeDef",
    "ListHarvestJobsRequestListHarvestJobsPaginateTypeDef",
    "ListHarvestJobsRequestRequestTypeDef",
    "ListHarvestJobsResponseTypeDef",
    "ListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef",
    "ListOriginEndpointsRequestRequestTypeDef",
    "ListOriginEndpointsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MssEncryptionOutputTypeDef",
    "MssEncryptionTypeDef",
    "MssEncryptionUnionTypeDef",
    "MssPackageOutputTypeDef",
    "MssPackageTypeDef",
    "OriginEndpointTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "RotateChannelCredentialsRequestRequestTypeDef",
    "RotateChannelCredentialsResponseTypeDef",
    "RotateIngestEndpointCredentialsRequestRequestTypeDef",
    "RotateIngestEndpointCredentialsResponseTypeDef",
    "S3DestinationTypeDef",
    "SpekeKeyProviderOutputTypeDef",
    "SpekeKeyProviderTypeDef",
    "SpekeKeyProviderUnionTypeDef",
    "StreamSelectionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateChannelRequestRequestTypeDef",
    "UpdateChannelResponseTypeDef",
    "UpdateOriginEndpointRequestRequestTypeDef",
    "UpdateOriginEndpointResponseTypeDef",
)

class AuthorizationTypeDef(TypedDict):
    CdnIdentifierSecret: str
    SecretsRoleArn: str

class EgressAccessLogsTypeDef(TypedDict):
    LogGroupName: NotRequired[str]

class IngressAccessLogsTypeDef(TypedDict):
    LogGroupName: NotRequired[str]

class HlsManifestCreateOrUpdateParametersTypeDef(TypedDict):
    Id: str
    AdMarkers: NotRequired[AdMarkersType]
    AdTriggers: NotRequired[Sequence[AdTriggersElementType]]
    AdsOnDeliveryRestrictions: NotRequired[AdsOnDeliveryRestrictionsType]
    IncludeIframeOnlyStream: NotRequired[bool]
    ManifestName: NotRequired[str]
    PlaylistType: NotRequired[PlaylistTypeType]
    PlaylistWindowSeconds: NotRequired[int]
    ProgramDateTimeIntervalSeconds: NotRequired[int]

class StreamSelectionTypeDef(TypedDict):
    MaxVideoBitsPerSecond: NotRequired[int]
    MinVideoBitsPerSecond: NotRequired[int]
    StreamOrder: NotRequired[StreamOrderType]

class HlsManifestTypeDef(TypedDict):
    Id: str
    AdMarkers: NotRequired[AdMarkersType]
    IncludeIframeOnlyStream: NotRequired[bool]
    ManifestName: NotRequired[str]
    PlaylistType: NotRequired[PlaylistTypeType]
    PlaylistWindowSeconds: NotRequired[int]
    ProgramDateTimeIntervalSeconds: NotRequired[int]
    Url: NotRequired[str]
    AdTriggers: NotRequired[List[AdTriggersElementType]]
    AdsOnDeliveryRestrictions: NotRequired[AdsOnDeliveryRestrictionsType]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateChannelRequestRequestTypeDef(TypedDict):
    Id: str
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class S3DestinationTypeDef(TypedDict):
    BucketName: str
    ManifestKey: str
    RoleArn: str

class DeleteChannelRequestRequestTypeDef(TypedDict):
    Id: str

class DeleteOriginEndpointRequestRequestTypeDef(TypedDict):
    Id: str

class DescribeChannelRequestRequestTypeDef(TypedDict):
    Id: str

class DescribeHarvestJobRequestRequestTypeDef(TypedDict):
    Id: str

class DescribeOriginEndpointRequestRequestTypeDef(TypedDict):
    Id: str

class EncryptionContractConfigurationTypeDef(TypedDict):
    PresetSpeke20Audio: PresetSpeke20AudioType
    PresetSpeke20Video: PresetSpeke20VideoType

class IngestEndpointTypeDef(TypedDict):
    Id: NotRequired[str]
    Password: NotRequired[str]
    Url: NotRequired[str]
    Username: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListChannelsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListHarvestJobsRequestRequestTypeDef(TypedDict):
    IncludeChannelId: NotRequired[str]
    IncludeStatus: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListOriginEndpointsRequestRequestTypeDef(TypedDict):
    ChannelId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class RotateChannelCredentialsRequestRequestTypeDef(TypedDict):
    Id: str

class RotateIngestEndpointCredentialsRequestRequestTypeDef(TypedDict):
    Id: str
    IngestEndpointId: str

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateChannelRequestRequestTypeDef(TypedDict):
    Id: str
    Description: NotRequired[str]

class ConfigureLogsRequestRequestTypeDef(TypedDict):
    Id: str
    EgressAccessLogs: NotRequired[EgressAccessLogsTypeDef]
    IngressAccessLogs: NotRequired[IngressAccessLogsTypeDef]

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateHarvestJobRequestRequestTypeDef(TypedDict):
    EndTime: str
    Id: str
    OriginEndpointId: str
    S3Destination: S3DestinationTypeDef
    StartTime: str

class CreateHarvestJobResponseTypeDef(TypedDict):
    Arn: str
    ChannelId: str
    CreatedAt: str
    EndTime: str
    Id: str
    OriginEndpointId: str
    S3Destination: S3DestinationTypeDef
    StartTime: str
    Status: StatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeHarvestJobResponseTypeDef(TypedDict):
    Arn: str
    ChannelId: str
    CreatedAt: str
    EndTime: str
    Id: str
    OriginEndpointId: str
    S3Destination: S3DestinationTypeDef
    StartTime: str
    Status: StatusType
    ResponseMetadata: ResponseMetadataTypeDef

class HarvestJobTypeDef(TypedDict):
    Arn: NotRequired[str]
    ChannelId: NotRequired[str]
    CreatedAt: NotRequired[str]
    EndTime: NotRequired[str]
    Id: NotRequired[str]
    OriginEndpointId: NotRequired[str]
    S3Destination: NotRequired[S3DestinationTypeDef]
    StartTime: NotRequired[str]
    Status: NotRequired[StatusType]

class SpekeKeyProviderOutputTypeDef(TypedDict):
    ResourceId: str
    RoleArn: str
    SystemIds: List[str]
    Url: str
    CertificateArn: NotRequired[str]
    EncryptionContractConfiguration: NotRequired[EncryptionContractConfigurationTypeDef]

class SpekeKeyProviderTypeDef(TypedDict):
    ResourceId: str
    RoleArn: str
    SystemIds: Sequence[str]
    Url: str
    CertificateArn: NotRequired[str]
    EncryptionContractConfiguration: NotRequired[EncryptionContractConfigurationTypeDef]

class HlsIngestTypeDef(TypedDict):
    IngestEndpoints: NotRequired[List[IngestEndpointTypeDef]]

class ListChannelsRequestListChannelsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListHarvestJobsRequestListHarvestJobsPaginateTypeDef(TypedDict):
    IncludeChannelId: NotRequired[str]
    IncludeStatus: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef(TypedDict):
    ChannelId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListHarvestJobsResponseTypeDef(TypedDict):
    HarvestJobs: List[HarvestJobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CmafEncryptionOutputTypeDef(TypedDict):
    SpekeKeyProvider: SpekeKeyProviderOutputTypeDef
    ConstantInitializationVector: NotRequired[str]
    EncryptionMethod: NotRequired[CmafEncryptionMethodType]
    KeyRotationIntervalSeconds: NotRequired[int]

class DashEncryptionOutputTypeDef(TypedDict):
    SpekeKeyProvider: SpekeKeyProviderOutputTypeDef
    KeyRotationIntervalSeconds: NotRequired[int]

class HlsEncryptionOutputTypeDef(TypedDict):
    SpekeKeyProvider: SpekeKeyProviderOutputTypeDef
    ConstantInitializationVector: NotRequired[str]
    EncryptionMethod: NotRequired[EncryptionMethodType]
    KeyRotationIntervalSeconds: NotRequired[int]
    RepeatExtXKey: NotRequired[bool]

class MssEncryptionOutputTypeDef(TypedDict):
    SpekeKeyProvider: SpekeKeyProviderOutputTypeDef

SpekeKeyProviderUnionTypeDef = Union[SpekeKeyProviderTypeDef, SpekeKeyProviderOutputTypeDef]

class ChannelTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreatedAt: NotRequired[str]
    Description: NotRequired[str]
    EgressAccessLogs: NotRequired[EgressAccessLogsTypeDef]
    HlsIngest: NotRequired[HlsIngestTypeDef]
    Id: NotRequired[str]
    IngressAccessLogs: NotRequired[IngressAccessLogsTypeDef]
    Tags: NotRequired[Dict[str, str]]

class ConfigureLogsResponseTypeDef(TypedDict):
    Arn: str
    CreatedAt: str
    Description: str
    EgressAccessLogs: EgressAccessLogsTypeDef
    HlsIngest: HlsIngestTypeDef
    Id: str
    IngressAccessLogs: IngressAccessLogsTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateChannelResponseTypeDef(TypedDict):
    Arn: str
    CreatedAt: str
    Description: str
    EgressAccessLogs: EgressAccessLogsTypeDef
    HlsIngest: HlsIngestTypeDef
    Id: str
    IngressAccessLogs: IngressAccessLogsTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeChannelResponseTypeDef(TypedDict):
    Arn: str
    CreatedAt: str
    Description: str
    EgressAccessLogs: EgressAccessLogsTypeDef
    HlsIngest: HlsIngestTypeDef
    Id: str
    IngressAccessLogs: IngressAccessLogsTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class RotateChannelCredentialsResponseTypeDef(TypedDict):
    Arn: str
    CreatedAt: str
    Description: str
    EgressAccessLogs: EgressAccessLogsTypeDef
    HlsIngest: HlsIngestTypeDef
    Id: str
    IngressAccessLogs: IngressAccessLogsTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class RotateIngestEndpointCredentialsResponseTypeDef(TypedDict):
    Arn: str
    CreatedAt: str
    Description: str
    EgressAccessLogs: EgressAccessLogsTypeDef
    HlsIngest: HlsIngestTypeDef
    Id: str
    IngressAccessLogs: IngressAccessLogsTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateChannelResponseTypeDef(TypedDict):
    Arn: str
    CreatedAt: str
    Description: str
    EgressAccessLogs: EgressAccessLogsTypeDef
    HlsIngest: HlsIngestTypeDef
    Id: str
    IngressAccessLogs: IngressAccessLogsTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CmafPackageTypeDef(TypedDict):
    Encryption: NotRequired[CmafEncryptionOutputTypeDef]
    HlsManifests: NotRequired[List[HlsManifestTypeDef]]
    SegmentDurationSeconds: NotRequired[int]
    SegmentPrefix: NotRequired[str]
    StreamSelection: NotRequired[StreamSelectionTypeDef]

class DashPackageOutputTypeDef(TypedDict):
    AdTriggers: NotRequired[List[AdTriggersElementType]]
    AdsOnDeliveryRestrictions: NotRequired[AdsOnDeliveryRestrictionsType]
    Encryption: NotRequired[DashEncryptionOutputTypeDef]
    IncludeIframeOnlyStream: NotRequired[bool]
    ManifestLayout: NotRequired[ManifestLayoutType]
    ManifestWindowSeconds: NotRequired[int]
    MinBufferTimeSeconds: NotRequired[int]
    MinUpdatePeriodSeconds: NotRequired[int]
    PeriodTriggers: NotRequired[List[Literal["ADS"]]]
    Profile: NotRequired[ProfileType]
    SegmentDurationSeconds: NotRequired[int]
    SegmentTemplateFormat: NotRequired[SegmentTemplateFormatType]
    StreamSelection: NotRequired[StreamSelectionTypeDef]
    SuggestedPresentationDelaySeconds: NotRequired[int]
    UtcTiming: NotRequired[UtcTimingType]
    UtcTimingUri: NotRequired[str]

class HlsPackageOutputTypeDef(TypedDict):
    AdMarkers: NotRequired[AdMarkersType]
    AdTriggers: NotRequired[List[AdTriggersElementType]]
    AdsOnDeliveryRestrictions: NotRequired[AdsOnDeliveryRestrictionsType]
    Encryption: NotRequired[HlsEncryptionOutputTypeDef]
    IncludeDvbSubtitles: NotRequired[bool]
    IncludeIframeOnlyStream: NotRequired[bool]
    PlaylistType: NotRequired[PlaylistTypeType]
    PlaylistWindowSeconds: NotRequired[int]
    ProgramDateTimeIntervalSeconds: NotRequired[int]
    SegmentDurationSeconds: NotRequired[int]
    StreamSelection: NotRequired[StreamSelectionTypeDef]
    UseAudioRenditionGroup: NotRequired[bool]

class MssPackageOutputTypeDef(TypedDict):
    Encryption: NotRequired[MssEncryptionOutputTypeDef]
    ManifestWindowSeconds: NotRequired[int]
    SegmentDurationSeconds: NotRequired[int]
    StreamSelection: NotRequired[StreamSelectionTypeDef]

class CmafEncryptionTypeDef(TypedDict):
    SpekeKeyProvider: SpekeKeyProviderUnionTypeDef
    ConstantInitializationVector: NotRequired[str]
    EncryptionMethod: NotRequired[CmafEncryptionMethodType]
    KeyRotationIntervalSeconds: NotRequired[int]

class DashEncryptionTypeDef(TypedDict):
    SpekeKeyProvider: SpekeKeyProviderUnionTypeDef
    KeyRotationIntervalSeconds: NotRequired[int]

class HlsEncryptionTypeDef(TypedDict):
    SpekeKeyProvider: SpekeKeyProviderUnionTypeDef
    ConstantInitializationVector: NotRequired[str]
    EncryptionMethod: NotRequired[EncryptionMethodType]
    KeyRotationIntervalSeconds: NotRequired[int]
    RepeatExtXKey: NotRequired[bool]

class MssEncryptionTypeDef(TypedDict):
    SpekeKeyProvider: SpekeKeyProviderUnionTypeDef

class ListChannelsResponseTypeDef(TypedDict):
    Channels: List[ChannelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateOriginEndpointResponseTypeDef(TypedDict):
    Arn: str
    Authorization: AuthorizationTypeDef
    ChannelId: str
    CmafPackage: CmafPackageTypeDef
    CreatedAt: str
    DashPackage: DashPackageOutputTypeDef
    Description: str
    HlsPackage: HlsPackageOutputTypeDef
    Id: str
    ManifestName: str
    MssPackage: MssPackageOutputTypeDef
    Origination: OriginationType
    StartoverWindowSeconds: int
    Tags: Dict[str, str]
    TimeDelaySeconds: int
    Url: str
    Whitelist: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeOriginEndpointResponseTypeDef(TypedDict):
    Arn: str
    Authorization: AuthorizationTypeDef
    ChannelId: str
    CmafPackage: CmafPackageTypeDef
    CreatedAt: str
    DashPackage: DashPackageOutputTypeDef
    Description: str
    HlsPackage: HlsPackageOutputTypeDef
    Id: str
    ManifestName: str
    MssPackage: MssPackageOutputTypeDef
    Origination: OriginationType
    StartoverWindowSeconds: int
    Tags: Dict[str, str]
    TimeDelaySeconds: int
    Url: str
    Whitelist: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class OriginEndpointTypeDef(TypedDict):
    Arn: NotRequired[str]
    Authorization: NotRequired[AuthorizationTypeDef]
    ChannelId: NotRequired[str]
    CmafPackage: NotRequired[CmafPackageTypeDef]
    CreatedAt: NotRequired[str]
    DashPackage: NotRequired[DashPackageOutputTypeDef]
    Description: NotRequired[str]
    HlsPackage: NotRequired[HlsPackageOutputTypeDef]
    Id: NotRequired[str]
    ManifestName: NotRequired[str]
    MssPackage: NotRequired[MssPackageOutputTypeDef]
    Origination: NotRequired[OriginationType]
    StartoverWindowSeconds: NotRequired[int]
    Tags: NotRequired[Dict[str, str]]
    TimeDelaySeconds: NotRequired[int]
    Url: NotRequired[str]
    Whitelist: NotRequired[List[str]]

class UpdateOriginEndpointResponseTypeDef(TypedDict):
    Arn: str
    Authorization: AuthorizationTypeDef
    ChannelId: str
    CmafPackage: CmafPackageTypeDef
    CreatedAt: str
    DashPackage: DashPackageOutputTypeDef
    Description: str
    HlsPackage: HlsPackageOutputTypeDef
    Id: str
    ManifestName: str
    MssPackage: MssPackageOutputTypeDef
    Origination: OriginationType
    StartoverWindowSeconds: int
    Tags: Dict[str, str]
    TimeDelaySeconds: int
    Url: str
    Whitelist: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

CmafEncryptionUnionTypeDef = Union[CmafEncryptionTypeDef, CmafEncryptionOutputTypeDef]
DashEncryptionUnionTypeDef = Union[DashEncryptionTypeDef, DashEncryptionOutputTypeDef]
HlsEncryptionUnionTypeDef = Union[HlsEncryptionTypeDef, HlsEncryptionOutputTypeDef]
MssEncryptionUnionTypeDef = Union[MssEncryptionTypeDef, MssEncryptionOutputTypeDef]

class ListOriginEndpointsResponseTypeDef(TypedDict):
    OriginEndpoints: List[OriginEndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CmafPackageCreateOrUpdateParametersTypeDef(TypedDict):
    Encryption: NotRequired[CmafEncryptionUnionTypeDef]
    HlsManifests: NotRequired[Sequence[HlsManifestCreateOrUpdateParametersTypeDef]]
    SegmentDurationSeconds: NotRequired[int]
    SegmentPrefix: NotRequired[str]
    StreamSelection: NotRequired[StreamSelectionTypeDef]

class DashPackageTypeDef(TypedDict):
    AdTriggers: NotRequired[Sequence[AdTriggersElementType]]
    AdsOnDeliveryRestrictions: NotRequired[AdsOnDeliveryRestrictionsType]
    Encryption: NotRequired[DashEncryptionUnionTypeDef]
    IncludeIframeOnlyStream: NotRequired[bool]
    ManifestLayout: NotRequired[ManifestLayoutType]
    ManifestWindowSeconds: NotRequired[int]
    MinBufferTimeSeconds: NotRequired[int]
    MinUpdatePeriodSeconds: NotRequired[int]
    PeriodTriggers: NotRequired[Sequence[Literal["ADS"]]]
    Profile: NotRequired[ProfileType]
    SegmentDurationSeconds: NotRequired[int]
    SegmentTemplateFormat: NotRequired[SegmentTemplateFormatType]
    StreamSelection: NotRequired[StreamSelectionTypeDef]
    SuggestedPresentationDelaySeconds: NotRequired[int]
    UtcTiming: NotRequired[UtcTimingType]
    UtcTimingUri: NotRequired[str]

class HlsPackageTypeDef(TypedDict):
    AdMarkers: NotRequired[AdMarkersType]
    AdTriggers: NotRequired[Sequence[AdTriggersElementType]]
    AdsOnDeliveryRestrictions: NotRequired[AdsOnDeliveryRestrictionsType]
    Encryption: NotRequired[HlsEncryptionUnionTypeDef]
    IncludeDvbSubtitles: NotRequired[bool]
    IncludeIframeOnlyStream: NotRequired[bool]
    PlaylistType: NotRequired[PlaylistTypeType]
    PlaylistWindowSeconds: NotRequired[int]
    ProgramDateTimeIntervalSeconds: NotRequired[int]
    SegmentDurationSeconds: NotRequired[int]
    StreamSelection: NotRequired[StreamSelectionTypeDef]
    UseAudioRenditionGroup: NotRequired[bool]

class MssPackageTypeDef(TypedDict):
    Encryption: NotRequired[MssEncryptionUnionTypeDef]
    ManifestWindowSeconds: NotRequired[int]
    SegmentDurationSeconds: NotRequired[int]
    StreamSelection: NotRequired[StreamSelectionTypeDef]

class CreateOriginEndpointRequestRequestTypeDef(TypedDict):
    ChannelId: str
    Id: str
    Authorization: NotRequired[AuthorizationTypeDef]
    CmafPackage: NotRequired[CmafPackageCreateOrUpdateParametersTypeDef]
    DashPackage: NotRequired[DashPackageTypeDef]
    Description: NotRequired[str]
    HlsPackage: NotRequired[HlsPackageTypeDef]
    ManifestName: NotRequired[str]
    MssPackage: NotRequired[MssPackageTypeDef]
    Origination: NotRequired[OriginationType]
    StartoverWindowSeconds: NotRequired[int]
    Tags: NotRequired[Mapping[str, str]]
    TimeDelaySeconds: NotRequired[int]
    Whitelist: NotRequired[Sequence[str]]

class UpdateOriginEndpointRequestRequestTypeDef(TypedDict):
    Id: str
    Authorization: NotRequired[AuthorizationTypeDef]
    CmafPackage: NotRequired[CmafPackageCreateOrUpdateParametersTypeDef]
    DashPackage: NotRequired[DashPackageTypeDef]
    Description: NotRequired[str]
    HlsPackage: NotRequired[HlsPackageTypeDef]
    ManifestName: NotRequired[str]
    MssPackage: NotRequired[MssPackageTypeDef]
    Origination: NotRequired[OriginationType]
    StartoverWindowSeconds: NotRequired[int]
    TimeDelaySeconds: NotRequired[int]
    Whitelist: NotRequired[Sequence[str]]
