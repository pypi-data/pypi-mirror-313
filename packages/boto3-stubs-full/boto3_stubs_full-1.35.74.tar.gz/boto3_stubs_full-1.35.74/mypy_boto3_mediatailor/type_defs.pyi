"""
Type annotations for mediatailor service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/type_defs/)

Usage::

    ```python
    from mypy_boto3_mediatailor.type_defs import SecretsManagerAccessTokenConfigurationTypeDef

    data: SecretsManagerAccessTokenConfigurationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AccessTypeType,
    AdMarkupTypeType,
    AlertCategoryType,
    ChannelStateType,
    FillPolicyType,
    InsertionModeType,
    MessageTypeType,
    ModeType,
    OriginManifestTypeType,
    PlaybackModeType,
    RelativePositionType,
    ScheduleEntryTypeType,
    TierType,
    TypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccessConfigurationTypeDef",
    "AdBreakOpportunityTypeDef",
    "AdBreakOutputTypeDef",
    "AdBreakTypeDef",
    "AdBreakUnionTypeDef",
    "AdMarkerPassthroughTypeDef",
    "AlertTypeDef",
    "AlternateMediaOutputTypeDef",
    "AlternateMediaTypeDef",
    "AlternateMediaUnionTypeDef",
    "AudienceMediaOutputTypeDef",
    "AudienceMediaTypeDef",
    "AudienceMediaUnionTypeDef",
    "AvailMatchingCriteriaTypeDef",
    "AvailSuppressionTypeDef",
    "BumperTypeDef",
    "CdnConfigurationTypeDef",
    "ChannelTypeDef",
    "ClipRangeTypeDef",
    "ConfigureLogsForChannelRequestRequestTypeDef",
    "ConfigureLogsForChannelResponseTypeDef",
    "ConfigureLogsForPlaybackConfigurationRequestRequestTypeDef",
    "ConfigureLogsForPlaybackConfigurationResponseTypeDef",
    "CreateChannelRequestRequestTypeDef",
    "CreateChannelResponseTypeDef",
    "CreateLiveSourceRequestRequestTypeDef",
    "CreateLiveSourceResponseTypeDef",
    "CreatePrefetchScheduleRequestRequestTypeDef",
    "CreatePrefetchScheduleResponseTypeDef",
    "CreateProgramRequestRequestTypeDef",
    "CreateProgramResponseTypeDef",
    "CreateSourceLocationRequestRequestTypeDef",
    "CreateSourceLocationResponseTypeDef",
    "CreateVodSourceRequestRequestTypeDef",
    "CreateVodSourceResponseTypeDef",
    "DashConfigurationForPutTypeDef",
    "DashConfigurationTypeDef",
    "DashPlaylistSettingsTypeDef",
    "DefaultSegmentDeliveryConfigurationTypeDef",
    "DeleteChannelPolicyRequestRequestTypeDef",
    "DeleteChannelRequestRequestTypeDef",
    "DeleteLiveSourceRequestRequestTypeDef",
    "DeletePlaybackConfigurationRequestRequestTypeDef",
    "DeletePrefetchScheduleRequestRequestTypeDef",
    "DeleteProgramRequestRequestTypeDef",
    "DeleteSourceLocationRequestRequestTypeDef",
    "DeleteVodSourceRequestRequestTypeDef",
    "DescribeChannelRequestRequestTypeDef",
    "DescribeChannelResponseTypeDef",
    "DescribeLiveSourceRequestRequestTypeDef",
    "DescribeLiveSourceResponseTypeDef",
    "DescribeProgramRequestRequestTypeDef",
    "DescribeProgramResponseTypeDef",
    "DescribeSourceLocationRequestRequestTypeDef",
    "DescribeSourceLocationResponseTypeDef",
    "DescribeVodSourceRequestRequestTypeDef",
    "DescribeVodSourceResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetChannelPolicyRequestRequestTypeDef",
    "GetChannelPolicyResponseTypeDef",
    "GetChannelScheduleRequestGetChannelSchedulePaginateTypeDef",
    "GetChannelScheduleRequestRequestTypeDef",
    "GetChannelScheduleResponseTypeDef",
    "GetPlaybackConfigurationRequestRequestTypeDef",
    "GetPlaybackConfigurationResponseTypeDef",
    "GetPrefetchScheduleRequestRequestTypeDef",
    "GetPrefetchScheduleResponseTypeDef",
    "HlsConfigurationTypeDef",
    "HlsPlaylistSettingsOutputTypeDef",
    "HlsPlaylistSettingsTypeDef",
    "HlsPlaylistSettingsUnionTypeDef",
    "HttpConfigurationTypeDef",
    "HttpPackageConfigurationTypeDef",
    "KeyValuePairTypeDef",
    "ListAlertsRequestListAlertsPaginateTypeDef",
    "ListAlertsRequestRequestTypeDef",
    "ListAlertsResponseTypeDef",
    "ListChannelsRequestListChannelsPaginateTypeDef",
    "ListChannelsRequestRequestTypeDef",
    "ListChannelsResponseTypeDef",
    "ListLiveSourcesRequestListLiveSourcesPaginateTypeDef",
    "ListLiveSourcesRequestRequestTypeDef",
    "ListLiveSourcesResponseTypeDef",
    "ListPlaybackConfigurationsRequestListPlaybackConfigurationsPaginateTypeDef",
    "ListPlaybackConfigurationsRequestRequestTypeDef",
    "ListPlaybackConfigurationsResponseTypeDef",
    "ListPrefetchSchedulesRequestListPrefetchSchedulesPaginateTypeDef",
    "ListPrefetchSchedulesRequestRequestTypeDef",
    "ListPrefetchSchedulesResponseTypeDef",
    "ListSourceLocationsRequestListSourceLocationsPaginateTypeDef",
    "ListSourceLocationsRequestRequestTypeDef",
    "ListSourceLocationsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListVodSourcesRequestListVodSourcesPaginateTypeDef",
    "ListVodSourcesRequestRequestTypeDef",
    "ListVodSourcesResponseTypeDef",
    "LivePreRollConfigurationTypeDef",
    "LiveSourceTypeDef",
    "LogConfigurationForChannelTypeDef",
    "LogConfigurationTypeDef",
    "ManifestProcessingRulesTypeDef",
    "PaginatorConfigTypeDef",
    "PlaybackConfigurationTypeDef",
    "PrefetchConsumptionOutputTypeDef",
    "PrefetchConsumptionTypeDef",
    "PrefetchRetrievalOutputTypeDef",
    "PrefetchRetrievalTypeDef",
    "PrefetchScheduleTypeDef",
    "PutChannelPolicyRequestRequestTypeDef",
    "PutPlaybackConfigurationRequestRequestTypeDef",
    "PutPlaybackConfigurationResponseTypeDef",
    "RequestOutputItemTypeDef",
    "ResponseMetadataTypeDef",
    "ResponseOutputItemTypeDef",
    "ScheduleAdBreakTypeDef",
    "ScheduleConfigurationTypeDef",
    "ScheduleEntryTypeDef",
    "SecretsManagerAccessTokenConfigurationTypeDef",
    "SegmentDeliveryConfigurationTypeDef",
    "SegmentationDescriptorTypeDef",
    "SlateSourceTypeDef",
    "SourceLocationTypeDef",
    "SpliceInsertMessageTypeDef",
    "StartChannelRequestRequestTypeDef",
    "StopChannelRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimeShiftConfigurationTypeDef",
    "TimeSignalMessageOutputTypeDef",
    "TimeSignalMessageTypeDef",
    "TimeSignalMessageUnionTypeDef",
    "TimestampTypeDef",
    "TransitionTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateChannelRequestRequestTypeDef",
    "UpdateChannelResponseTypeDef",
    "UpdateLiveSourceRequestRequestTypeDef",
    "UpdateLiveSourceResponseTypeDef",
    "UpdateProgramRequestRequestTypeDef",
    "UpdateProgramResponseTypeDef",
    "UpdateProgramScheduleConfigurationTypeDef",
    "UpdateProgramTransitionTypeDef",
    "UpdateSourceLocationRequestRequestTypeDef",
    "UpdateSourceLocationResponseTypeDef",
    "UpdateVodSourceRequestRequestTypeDef",
    "UpdateVodSourceResponseTypeDef",
    "VodSourceTypeDef",
)

class SecretsManagerAccessTokenConfigurationTypeDef(TypedDict):
    HeaderName: NotRequired[str]
    SecretArn: NotRequired[str]
    SecretStringKey: NotRequired[str]

class AdBreakOpportunityTypeDef(TypedDict):
    OffsetMillis: int

class KeyValuePairTypeDef(TypedDict):
    Key: str
    Value: str

class SlateSourceTypeDef(TypedDict):
    SourceLocationName: NotRequired[str]
    VodSourceName: NotRequired[str]

class SpliceInsertMessageTypeDef(TypedDict):
    AvailNum: NotRequired[int]
    AvailsExpected: NotRequired[int]
    SpliceEventId: NotRequired[int]
    UniqueProgramId: NotRequired[int]

class AdMarkerPassthroughTypeDef(TypedDict):
    Enabled: NotRequired[bool]

class AlertTypeDef(TypedDict):
    AlertCode: str
    AlertMessage: str
    LastModifiedTime: datetime
    RelatedResourceArns: List[str]
    ResourceArn: str
    Category: NotRequired[AlertCategoryType]

class ClipRangeTypeDef(TypedDict):
    EndOffsetMillis: NotRequired[int]
    StartOffsetMillis: NotRequired[int]

class AvailMatchingCriteriaTypeDef(TypedDict):
    DynamicVariable: str
    Operator: Literal["EQUALS"]

class AvailSuppressionTypeDef(TypedDict):
    FillPolicy: NotRequired[FillPolicyType]
    Mode: NotRequired[ModeType]
    Value: NotRequired[str]

class BumperTypeDef(TypedDict):
    EndUrl: NotRequired[str]
    StartUrl: NotRequired[str]

class CdnConfigurationTypeDef(TypedDict):
    AdSegmentUrlPrefix: NotRequired[str]
    ContentSegmentUrlPrefix: NotRequired[str]

class LogConfigurationForChannelTypeDef(TypedDict):
    LogTypes: NotRequired[List[Literal["AS_RUN"]]]

class ConfigureLogsForChannelRequestRequestTypeDef(TypedDict):
    ChannelName: str
    LogTypes: Sequence[Literal["AS_RUN"]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ConfigureLogsForPlaybackConfigurationRequestRequestTypeDef(TypedDict):
    PercentEnabled: int
    PlaybackConfigurationName: str

class TimeShiftConfigurationTypeDef(TypedDict):
    MaxTimeDelaySeconds: int

HttpPackageConfigurationTypeDef = TypedDict(
    "HttpPackageConfigurationTypeDef",
    {
        "Path": str,
        "SourceGroup": str,
        "Type": TypeType,
    },
)

class PrefetchRetrievalOutputTypeDef(TypedDict):
    EndTime: datetime
    DynamicVariables: NotRequired[Dict[str, str]]
    StartTime: NotRequired[datetime]

class DefaultSegmentDeliveryConfigurationTypeDef(TypedDict):
    BaseUrl: NotRequired[str]

class HttpConfigurationTypeDef(TypedDict):
    BaseUrl: str

class SegmentDeliveryConfigurationTypeDef(TypedDict):
    BaseUrl: NotRequired[str]
    Name: NotRequired[str]

class DashConfigurationForPutTypeDef(TypedDict):
    MpdLocation: NotRequired[str]
    OriginManifestType: NotRequired[OriginManifestTypeType]

class DashConfigurationTypeDef(TypedDict):
    ManifestEndpointPrefix: NotRequired[str]
    MpdLocation: NotRequired[str]
    OriginManifestType: NotRequired[OriginManifestTypeType]

class DashPlaylistSettingsTypeDef(TypedDict):
    ManifestWindowSeconds: NotRequired[int]
    MinBufferTimeSeconds: NotRequired[int]
    MinUpdatePeriodSeconds: NotRequired[int]
    SuggestedPresentationDelaySeconds: NotRequired[int]

class DeleteChannelPolicyRequestRequestTypeDef(TypedDict):
    ChannelName: str

class DeleteChannelRequestRequestTypeDef(TypedDict):
    ChannelName: str

class DeleteLiveSourceRequestRequestTypeDef(TypedDict):
    LiveSourceName: str
    SourceLocationName: str

class DeletePlaybackConfigurationRequestRequestTypeDef(TypedDict):
    Name: str

class DeletePrefetchScheduleRequestRequestTypeDef(TypedDict):
    Name: str
    PlaybackConfigurationName: str

class DeleteProgramRequestRequestTypeDef(TypedDict):
    ChannelName: str
    ProgramName: str

class DeleteSourceLocationRequestRequestTypeDef(TypedDict):
    SourceLocationName: str

class DeleteVodSourceRequestRequestTypeDef(TypedDict):
    SourceLocationName: str
    VodSourceName: str

class DescribeChannelRequestRequestTypeDef(TypedDict):
    ChannelName: str

class DescribeLiveSourceRequestRequestTypeDef(TypedDict):
    LiveSourceName: str
    SourceLocationName: str

class DescribeProgramRequestRequestTypeDef(TypedDict):
    ChannelName: str
    ProgramName: str

class DescribeSourceLocationRequestRequestTypeDef(TypedDict):
    SourceLocationName: str

class DescribeVodSourceRequestRequestTypeDef(TypedDict):
    SourceLocationName: str
    VodSourceName: str

class GetChannelPolicyRequestRequestTypeDef(TypedDict):
    ChannelName: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class GetChannelScheduleRequestRequestTypeDef(TypedDict):
    ChannelName: str
    Audience: NotRequired[str]
    DurationMinutes: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class GetPlaybackConfigurationRequestRequestTypeDef(TypedDict):
    Name: str

class HlsConfigurationTypeDef(TypedDict):
    ManifestEndpointPrefix: NotRequired[str]

class LivePreRollConfigurationTypeDef(TypedDict):
    AdDecisionServerUrl: NotRequired[str]
    MaxDurationSeconds: NotRequired[int]

class LogConfigurationTypeDef(TypedDict):
    PercentEnabled: int

class GetPrefetchScheduleRequestRequestTypeDef(TypedDict):
    Name: str
    PlaybackConfigurationName: str

class HlsPlaylistSettingsOutputTypeDef(TypedDict):
    AdMarkupType: NotRequired[List[AdMarkupTypeType]]
    ManifestWindowSeconds: NotRequired[int]

class HlsPlaylistSettingsTypeDef(TypedDict):
    AdMarkupType: NotRequired[Sequence[AdMarkupTypeType]]
    ManifestWindowSeconds: NotRequired[int]

class ListAlertsRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListChannelsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListLiveSourcesRequestRequestTypeDef(TypedDict):
    SourceLocationName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListPlaybackConfigurationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListPrefetchSchedulesRequestRequestTypeDef(TypedDict):
    PlaybackConfigurationName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    StreamId: NotRequired[str]

class ListSourceLocationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class ListVodSourcesRequestRequestTypeDef(TypedDict):
    SourceLocationName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class PutChannelPolicyRequestRequestTypeDef(TypedDict):
    ChannelName: str
    Policy: str

class ScheduleAdBreakTypeDef(TypedDict):
    ApproximateDurationSeconds: NotRequired[int]
    ApproximateStartTime: NotRequired[datetime]
    SourceLocationName: NotRequired[str]
    VodSourceName: NotRequired[str]

TransitionTypeDef = TypedDict(
    "TransitionTypeDef",
    {
        "RelativePosition": RelativePositionType,
        "Type": str,
        "DurationMillis": NotRequired[int],
        "RelativeProgram": NotRequired[str],
        "ScheduledStartTimeMillis": NotRequired[int],
    },
)

class SegmentationDescriptorTypeDef(TypedDict):
    SegmentNum: NotRequired[int]
    SegmentationEventId: NotRequired[int]
    SegmentationTypeId: NotRequired[int]
    SegmentationUpid: NotRequired[str]
    SegmentationUpidType: NotRequired[int]
    SegmentsExpected: NotRequired[int]
    SubSegmentNum: NotRequired[int]
    SubSegmentsExpected: NotRequired[int]

class StartChannelRequestRequestTypeDef(TypedDict):
    ChannelName: str

class StopChannelRequestRequestTypeDef(TypedDict):
    ChannelName: str

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateProgramTransitionTypeDef(TypedDict):
    DurationMillis: NotRequired[int]
    ScheduledStartTimeMillis: NotRequired[int]

class AccessConfigurationTypeDef(TypedDict):
    AccessType: NotRequired[AccessTypeType]
    SecretsManagerAccessTokenConfiguration: NotRequired[
        SecretsManagerAccessTokenConfigurationTypeDef
    ]

class ManifestProcessingRulesTypeDef(TypedDict):
    AdMarkerPassthrough: NotRequired[AdMarkerPassthroughTypeDef]

class PrefetchConsumptionOutputTypeDef(TypedDict):
    EndTime: datetime
    AvailMatchingCriteria: NotRequired[List[AvailMatchingCriteriaTypeDef]]
    StartTime: NotRequired[datetime]

class ConfigureLogsForChannelResponseTypeDef(TypedDict):
    ChannelName: str
    LogTypes: List[Literal["AS_RUN"]]
    ResponseMetadata: ResponseMetadataTypeDef

class ConfigureLogsForPlaybackConfigurationResponseTypeDef(TypedDict):
    PercentEnabled: int
    PlaybackConfigurationName: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetChannelPolicyResponseTypeDef(TypedDict):
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListAlertsResponseTypeDef(TypedDict):
    Items: List[AlertTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLiveSourceRequestRequestTypeDef(TypedDict):
    HttpPackageConfigurations: Sequence[HttpPackageConfigurationTypeDef]
    LiveSourceName: str
    SourceLocationName: str
    Tags: NotRequired[Mapping[str, str]]

class CreateLiveSourceResponseTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    HttpPackageConfigurations: List[HttpPackageConfigurationTypeDef]
    LastModifiedTime: datetime
    LiveSourceName: str
    SourceLocationName: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateVodSourceRequestRequestTypeDef(TypedDict):
    HttpPackageConfigurations: Sequence[HttpPackageConfigurationTypeDef]
    SourceLocationName: str
    VodSourceName: str
    Tags: NotRequired[Mapping[str, str]]

class CreateVodSourceResponseTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    HttpPackageConfigurations: List[HttpPackageConfigurationTypeDef]
    LastModifiedTime: datetime
    SourceLocationName: str
    Tags: Dict[str, str]
    VodSourceName: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeLiveSourceResponseTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    HttpPackageConfigurations: List[HttpPackageConfigurationTypeDef]
    LastModifiedTime: datetime
    LiveSourceName: str
    SourceLocationName: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeVodSourceResponseTypeDef(TypedDict):
    AdBreakOpportunities: List[AdBreakOpportunityTypeDef]
    Arn: str
    CreationTime: datetime
    HttpPackageConfigurations: List[HttpPackageConfigurationTypeDef]
    LastModifiedTime: datetime
    SourceLocationName: str
    Tags: Dict[str, str]
    VodSourceName: str
    ResponseMetadata: ResponseMetadataTypeDef

class LiveSourceTypeDef(TypedDict):
    Arn: str
    HttpPackageConfigurations: List[HttpPackageConfigurationTypeDef]
    LiveSourceName: str
    SourceLocationName: str
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    Tags: NotRequired[Dict[str, str]]

class UpdateLiveSourceRequestRequestTypeDef(TypedDict):
    HttpPackageConfigurations: Sequence[HttpPackageConfigurationTypeDef]
    LiveSourceName: str
    SourceLocationName: str

class UpdateLiveSourceResponseTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    HttpPackageConfigurations: List[HttpPackageConfigurationTypeDef]
    LastModifiedTime: datetime
    LiveSourceName: str
    SourceLocationName: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateVodSourceRequestRequestTypeDef(TypedDict):
    HttpPackageConfigurations: Sequence[HttpPackageConfigurationTypeDef]
    SourceLocationName: str
    VodSourceName: str

class UpdateVodSourceResponseTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    HttpPackageConfigurations: List[HttpPackageConfigurationTypeDef]
    LastModifiedTime: datetime
    SourceLocationName: str
    Tags: Dict[str, str]
    VodSourceName: str
    ResponseMetadata: ResponseMetadataTypeDef

class VodSourceTypeDef(TypedDict):
    Arn: str
    HttpPackageConfigurations: List[HttpPackageConfigurationTypeDef]
    SourceLocationName: str
    VodSourceName: str
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    Tags: NotRequired[Dict[str, str]]

class GetChannelScheduleRequestGetChannelSchedulePaginateTypeDef(TypedDict):
    ChannelName: str
    Audience: NotRequired[str]
    DurationMinutes: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAlertsRequestListAlertsPaginateTypeDef(TypedDict):
    ResourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListChannelsRequestListChannelsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLiveSourcesRequestListLiveSourcesPaginateTypeDef(TypedDict):
    SourceLocationName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPlaybackConfigurationsRequestListPlaybackConfigurationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPrefetchSchedulesRequestListPrefetchSchedulesPaginateTypeDef(TypedDict):
    PlaybackConfigurationName: str
    StreamId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSourceLocationsRequestListSourceLocationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListVodSourcesRequestListVodSourcesPaginateTypeDef(TypedDict):
    SourceLocationName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ResponseOutputItemTypeDef(TypedDict):
    ManifestName: str
    PlaybackUrl: str
    SourceGroup: str
    DashPlaylistSettings: NotRequired[DashPlaylistSettingsTypeDef]
    HlsPlaylistSettings: NotRequired[HlsPlaylistSettingsOutputTypeDef]

HlsPlaylistSettingsUnionTypeDef = Union[
    HlsPlaylistSettingsTypeDef, HlsPlaylistSettingsOutputTypeDef
]

class PrefetchConsumptionTypeDef(TypedDict):
    EndTime: TimestampTypeDef
    AvailMatchingCriteria: NotRequired[Sequence[AvailMatchingCriteriaTypeDef]]
    StartTime: NotRequired[TimestampTypeDef]

class PrefetchRetrievalTypeDef(TypedDict):
    EndTime: TimestampTypeDef
    DynamicVariables: NotRequired[Mapping[str, str]]
    StartTime: NotRequired[TimestampTypeDef]

class ScheduleEntryTypeDef(TypedDict):
    Arn: str
    ChannelName: str
    ProgramName: str
    SourceLocationName: str
    ApproximateDurationSeconds: NotRequired[int]
    ApproximateStartTime: NotRequired[datetime]
    Audiences: NotRequired[List[str]]
    LiveSourceName: NotRequired[str]
    ScheduleAdBreaks: NotRequired[List[ScheduleAdBreakTypeDef]]
    ScheduleEntryType: NotRequired[ScheduleEntryTypeType]
    VodSourceName: NotRequired[str]

class ScheduleConfigurationTypeDef(TypedDict):
    Transition: TransitionTypeDef
    ClipRange: NotRequired[ClipRangeTypeDef]

class TimeSignalMessageOutputTypeDef(TypedDict):
    SegmentationDescriptors: NotRequired[List[SegmentationDescriptorTypeDef]]

class TimeSignalMessageTypeDef(TypedDict):
    SegmentationDescriptors: NotRequired[Sequence[SegmentationDescriptorTypeDef]]

class UpdateProgramScheduleConfigurationTypeDef(TypedDict):
    ClipRange: NotRequired[ClipRangeTypeDef]
    Transition: NotRequired[UpdateProgramTransitionTypeDef]

class CreateSourceLocationRequestRequestTypeDef(TypedDict):
    HttpConfiguration: HttpConfigurationTypeDef
    SourceLocationName: str
    AccessConfiguration: NotRequired[AccessConfigurationTypeDef]
    DefaultSegmentDeliveryConfiguration: NotRequired[DefaultSegmentDeliveryConfigurationTypeDef]
    SegmentDeliveryConfigurations: NotRequired[Sequence[SegmentDeliveryConfigurationTypeDef]]
    Tags: NotRequired[Mapping[str, str]]

class CreateSourceLocationResponseTypeDef(TypedDict):
    AccessConfiguration: AccessConfigurationTypeDef
    Arn: str
    CreationTime: datetime
    DefaultSegmentDeliveryConfiguration: DefaultSegmentDeliveryConfigurationTypeDef
    HttpConfiguration: HttpConfigurationTypeDef
    LastModifiedTime: datetime
    SegmentDeliveryConfigurations: List[SegmentDeliveryConfigurationTypeDef]
    SourceLocationName: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeSourceLocationResponseTypeDef(TypedDict):
    AccessConfiguration: AccessConfigurationTypeDef
    Arn: str
    CreationTime: datetime
    DefaultSegmentDeliveryConfiguration: DefaultSegmentDeliveryConfigurationTypeDef
    HttpConfiguration: HttpConfigurationTypeDef
    LastModifiedTime: datetime
    SegmentDeliveryConfigurations: List[SegmentDeliveryConfigurationTypeDef]
    SourceLocationName: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class SourceLocationTypeDef(TypedDict):
    Arn: str
    HttpConfiguration: HttpConfigurationTypeDef
    SourceLocationName: str
    AccessConfiguration: NotRequired[AccessConfigurationTypeDef]
    CreationTime: NotRequired[datetime]
    DefaultSegmentDeliveryConfiguration: NotRequired[DefaultSegmentDeliveryConfigurationTypeDef]
    LastModifiedTime: NotRequired[datetime]
    SegmentDeliveryConfigurations: NotRequired[List[SegmentDeliveryConfigurationTypeDef]]
    Tags: NotRequired[Dict[str, str]]

class UpdateSourceLocationRequestRequestTypeDef(TypedDict):
    HttpConfiguration: HttpConfigurationTypeDef
    SourceLocationName: str
    AccessConfiguration: NotRequired[AccessConfigurationTypeDef]
    DefaultSegmentDeliveryConfiguration: NotRequired[DefaultSegmentDeliveryConfigurationTypeDef]
    SegmentDeliveryConfigurations: NotRequired[Sequence[SegmentDeliveryConfigurationTypeDef]]

class UpdateSourceLocationResponseTypeDef(TypedDict):
    AccessConfiguration: AccessConfigurationTypeDef
    Arn: str
    CreationTime: datetime
    DefaultSegmentDeliveryConfiguration: DefaultSegmentDeliveryConfigurationTypeDef
    HttpConfiguration: HttpConfigurationTypeDef
    LastModifiedTime: datetime
    SegmentDeliveryConfigurations: List[SegmentDeliveryConfigurationTypeDef]
    SourceLocationName: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetPlaybackConfigurationResponseTypeDef(TypedDict):
    AdDecisionServerUrl: str
    AvailSuppression: AvailSuppressionTypeDef
    Bumper: BumperTypeDef
    CdnConfiguration: CdnConfigurationTypeDef
    ConfigurationAliases: Dict[str, Dict[str, str]]
    DashConfiguration: DashConfigurationTypeDef
    HlsConfiguration: HlsConfigurationTypeDef
    InsertionMode: InsertionModeType
    LivePreRollConfiguration: LivePreRollConfigurationTypeDef
    LogConfiguration: LogConfigurationTypeDef
    ManifestProcessingRules: ManifestProcessingRulesTypeDef
    Name: str
    PersonalizationThresholdSeconds: int
    PlaybackConfigurationArn: str
    PlaybackEndpointPrefix: str
    SessionInitializationEndpointPrefix: str
    SlateAdUrl: str
    Tags: Dict[str, str]
    TranscodeProfileName: str
    VideoContentSourceUrl: str
    ResponseMetadata: ResponseMetadataTypeDef

class PlaybackConfigurationTypeDef(TypedDict):
    AdDecisionServerUrl: NotRequired[str]
    AvailSuppression: NotRequired[AvailSuppressionTypeDef]
    Bumper: NotRequired[BumperTypeDef]
    CdnConfiguration: NotRequired[CdnConfigurationTypeDef]
    ConfigurationAliases: NotRequired[Dict[str, Dict[str, str]]]
    DashConfiguration: NotRequired[DashConfigurationTypeDef]
    HlsConfiguration: NotRequired[HlsConfigurationTypeDef]
    InsertionMode: NotRequired[InsertionModeType]
    LivePreRollConfiguration: NotRequired[LivePreRollConfigurationTypeDef]
    LogConfiguration: NotRequired[LogConfigurationTypeDef]
    ManifestProcessingRules: NotRequired[ManifestProcessingRulesTypeDef]
    Name: NotRequired[str]
    PersonalizationThresholdSeconds: NotRequired[int]
    PlaybackConfigurationArn: NotRequired[str]
    PlaybackEndpointPrefix: NotRequired[str]
    SessionInitializationEndpointPrefix: NotRequired[str]
    SlateAdUrl: NotRequired[str]
    Tags: NotRequired[Dict[str, str]]
    TranscodeProfileName: NotRequired[str]
    VideoContentSourceUrl: NotRequired[str]

class PutPlaybackConfigurationRequestRequestTypeDef(TypedDict):
    Name: str
    AdDecisionServerUrl: NotRequired[str]
    AvailSuppression: NotRequired[AvailSuppressionTypeDef]
    Bumper: NotRequired[BumperTypeDef]
    CdnConfiguration: NotRequired[CdnConfigurationTypeDef]
    ConfigurationAliases: NotRequired[Mapping[str, Mapping[str, str]]]
    DashConfiguration: NotRequired[DashConfigurationForPutTypeDef]
    InsertionMode: NotRequired[InsertionModeType]
    LivePreRollConfiguration: NotRequired[LivePreRollConfigurationTypeDef]
    ManifestProcessingRules: NotRequired[ManifestProcessingRulesTypeDef]
    PersonalizationThresholdSeconds: NotRequired[int]
    SlateAdUrl: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    TranscodeProfileName: NotRequired[str]
    VideoContentSourceUrl: NotRequired[str]

class PutPlaybackConfigurationResponseTypeDef(TypedDict):
    AdDecisionServerUrl: str
    AvailSuppression: AvailSuppressionTypeDef
    Bumper: BumperTypeDef
    CdnConfiguration: CdnConfigurationTypeDef
    ConfigurationAliases: Dict[str, Dict[str, str]]
    DashConfiguration: DashConfigurationTypeDef
    HlsConfiguration: HlsConfigurationTypeDef
    InsertionMode: InsertionModeType
    LivePreRollConfiguration: LivePreRollConfigurationTypeDef
    LogConfiguration: LogConfigurationTypeDef
    ManifestProcessingRules: ManifestProcessingRulesTypeDef
    Name: str
    PersonalizationThresholdSeconds: int
    PlaybackConfigurationArn: str
    PlaybackEndpointPrefix: str
    SessionInitializationEndpointPrefix: str
    SlateAdUrl: str
    Tags: Dict[str, str]
    TranscodeProfileName: str
    VideoContentSourceUrl: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePrefetchScheduleResponseTypeDef(TypedDict):
    Arn: str
    Consumption: PrefetchConsumptionOutputTypeDef
    Name: str
    PlaybackConfigurationName: str
    Retrieval: PrefetchRetrievalOutputTypeDef
    StreamId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetPrefetchScheduleResponseTypeDef(TypedDict):
    Arn: str
    Consumption: PrefetchConsumptionOutputTypeDef
    Name: str
    PlaybackConfigurationName: str
    Retrieval: PrefetchRetrievalOutputTypeDef
    StreamId: str
    ResponseMetadata: ResponseMetadataTypeDef

class PrefetchScheduleTypeDef(TypedDict):
    Arn: str
    Consumption: PrefetchConsumptionOutputTypeDef
    Name: str
    PlaybackConfigurationName: str
    Retrieval: PrefetchRetrievalOutputTypeDef
    StreamId: NotRequired[str]

class ListLiveSourcesResponseTypeDef(TypedDict):
    Items: List[LiveSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListVodSourcesResponseTypeDef(TypedDict):
    Items: List[VodSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ChannelTypeDef(TypedDict):
    Arn: str
    ChannelName: str
    ChannelState: str
    LogConfiguration: LogConfigurationForChannelTypeDef
    Outputs: List[ResponseOutputItemTypeDef]
    PlaybackMode: str
    Tier: str
    Audiences: NotRequired[List[str]]
    CreationTime: NotRequired[datetime]
    FillerSlate: NotRequired[SlateSourceTypeDef]
    LastModifiedTime: NotRequired[datetime]
    Tags: NotRequired[Dict[str, str]]

class CreateChannelResponseTypeDef(TypedDict):
    Arn: str
    Audiences: List[str]
    ChannelName: str
    ChannelState: ChannelStateType
    CreationTime: datetime
    FillerSlate: SlateSourceTypeDef
    LastModifiedTime: datetime
    Outputs: List[ResponseOutputItemTypeDef]
    PlaybackMode: str
    Tags: Dict[str, str]
    Tier: str
    TimeShiftConfiguration: TimeShiftConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeChannelResponseTypeDef(TypedDict):
    Arn: str
    Audiences: List[str]
    ChannelName: str
    ChannelState: ChannelStateType
    CreationTime: datetime
    FillerSlate: SlateSourceTypeDef
    LastModifiedTime: datetime
    LogConfiguration: LogConfigurationForChannelTypeDef
    Outputs: List[ResponseOutputItemTypeDef]
    PlaybackMode: str
    Tags: Dict[str, str]
    Tier: str
    TimeShiftConfiguration: TimeShiftConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateChannelResponseTypeDef(TypedDict):
    Arn: str
    Audiences: List[str]
    ChannelName: str
    ChannelState: ChannelStateType
    CreationTime: datetime
    FillerSlate: SlateSourceTypeDef
    LastModifiedTime: datetime
    Outputs: List[ResponseOutputItemTypeDef]
    PlaybackMode: str
    Tags: Dict[str, str]
    Tier: str
    TimeShiftConfiguration: TimeShiftConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class RequestOutputItemTypeDef(TypedDict):
    ManifestName: str
    SourceGroup: str
    DashPlaylistSettings: NotRequired[DashPlaylistSettingsTypeDef]
    HlsPlaylistSettings: NotRequired[HlsPlaylistSettingsUnionTypeDef]

class CreatePrefetchScheduleRequestRequestTypeDef(TypedDict):
    Consumption: PrefetchConsumptionTypeDef
    Name: str
    PlaybackConfigurationName: str
    Retrieval: PrefetchRetrievalTypeDef
    StreamId: NotRequired[str]

class GetChannelScheduleResponseTypeDef(TypedDict):
    Items: List[ScheduleEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class AdBreakOutputTypeDef(TypedDict):
    OffsetMillis: int
    AdBreakMetadata: NotRequired[List[KeyValuePairTypeDef]]
    MessageType: NotRequired[MessageTypeType]
    Slate: NotRequired[SlateSourceTypeDef]
    SpliceInsertMessage: NotRequired[SpliceInsertMessageTypeDef]
    TimeSignalMessage: NotRequired[TimeSignalMessageOutputTypeDef]

TimeSignalMessageUnionTypeDef = Union[TimeSignalMessageTypeDef, TimeSignalMessageOutputTypeDef]

class ListSourceLocationsResponseTypeDef(TypedDict):
    Items: List[SourceLocationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListPlaybackConfigurationsResponseTypeDef(TypedDict):
    Items: List[PlaybackConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListPrefetchSchedulesResponseTypeDef(TypedDict):
    Items: List[PrefetchScheduleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListChannelsResponseTypeDef(TypedDict):
    Items: List[ChannelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateChannelRequestRequestTypeDef(TypedDict):
    ChannelName: str
    Outputs: Sequence[RequestOutputItemTypeDef]
    PlaybackMode: PlaybackModeType
    Audiences: NotRequired[Sequence[str]]
    FillerSlate: NotRequired[SlateSourceTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    Tier: NotRequired[TierType]
    TimeShiftConfiguration: NotRequired[TimeShiftConfigurationTypeDef]

class UpdateChannelRequestRequestTypeDef(TypedDict):
    ChannelName: str
    Outputs: Sequence[RequestOutputItemTypeDef]
    Audiences: NotRequired[Sequence[str]]
    FillerSlate: NotRequired[SlateSourceTypeDef]
    TimeShiftConfiguration: NotRequired[TimeShiftConfigurationTypeDef]

class AlternateMediaOutputTypeDef(TypedDict):
    AdBreaks: NotRequired[List[AdBreakOutputTypeDef]]
    ClipRange: NotRequired[ClipRangeTypeDef]
    DurationMillis: NotRequired[int]
    LiveSourceName: NotRequired[str]
    ScheduledStartTimeMillis: NotRequired[int]
    SourceLocationName: NotRequired[str]
    VodSourceName: NotRequired[str]

class AdBreakTypeDef(TypedDict):
    OffsetMillis: int
    AdBreakMetadata: NotRequired[Sequence[KeyValuePairTypeDef]]
    MessageType: NotRequired[MessageTypeType]
    Slate: NotRequired[SlateSourceTypeDef]
    SpliceInsertMessage: NotRequired[SpliceInsertMessageTypeDef]
    TimeSignalMessage: NotRequired[TimeSignalMessageUnionTypeDef]

class AudienceMediaOutputTypeDef(TypedDict):
    AlternateMedia: NotRequired[List[AlternateMediaOutputTypeDef]]
    Audience: NotRequired[str]

AdBreakUnionTypeDef = Union[AdBreakTypeDef, AdBreakOutputTypeDef]

class CreateProgramResponseTypeDef(TypedDict):
    AdBreaks: List[AdBreakOutputTypeDef]
    Arn: str
    AudienceMedia: List[AudienceMediaOutputTypeDef]
    ChannelName: str
    ClipRange: ClipRangeTypeDef
    CreationTime: datetime
    DurationMillis: int
    LiveSourceName: str
    ProgramName: str
    ScheduledStartTime: datetime
    SourceLocationName: str
    VodSourceName: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeProgramResponseTypeDef(TypedDict):
    AdBreaks: List[AdBreakOutputTypeDef]
    Arn: str
    AudienceMedia: List[AudienceMediaOutputTypeDef]
    ChannelName: str
    ClipRange: ClipRangeTypeDef
    CreationTime: datetime
    DurationMillis: int
    LiveSourceName: str
    ProgramName: str
    ScheduledStartTime: datetime
    SourceLocationName: str
    VodSourceName: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateProgramResponseTypeDef(TypedDict):
    AdBreaks: List[AdBreakOutputTypeDef]
    Arn: str
    AudienceMedia: List[AudienceMediaOutputTypeDef]
    ChannelName: str
    ClipRange: ClipRangeTypeDef
    CreationTime: datetime
    DurationMillis: int
    LiveSourceName: str
    ProgramName: str
    ScheduledStartTime: datetime
    SourceLocationName: str
    VodSourceName: str
    ResponseMetadata: ResponseMetadataTypeDef

class AlternateMediaTypeDef(TypedDict):
    AdBreaks: NotRequired[Sequence[AdBreakUnionTypeDef]]
    ClipRange: NotRequired[ClipRangeTypeDef]
    DurationMillis: NotRequired[int]
    LiveSourceName: NotRequired[str]
    ScheduledStartTimeMillis: NotRequired[int]
    SourceLocationName: NotRequired[str]
    VodSourceName: NotRequired[str]

AlternateMediaUnionTypeDef = Union[AlternateMediaTypeDef, AlternateMediaOutputTypeDef]

class AudienceMediaTypeDef(TypedDict):
    AlternateMedia: NotRequired[Sequence[AlternateMediaUnionTypeDef]]
    Audience: NotRequired[str]

AudienceMediaUnionTypeDef = Union[AudienceMediaTypeDef, AudienceMediaOutputTypeDef]

class UpdateProgramRequestRequestTypeDef(TypedDict):
    ChannelName: str
    ProgramName: str
    ScheduleConfiguration: UpdateProgramScheduleConfigurationTypeDef
    AdBreaks: NotRequired[Sequence[AdBreakTypeDef]]
    AudienceMedia: NotRequired[Sequence[AudienceMediaTypeDef]]

class CreateProgramRequestRequestTypeDef(TypedDict):
    ChannelName: str
    ProgramName: str
    ScheduleConfiguration: ScheduleConfigurationTypeDef
    SourceLocationName: str
    AdBreaks: NotRequired[Sequence[AdBreakUnionTypeDef]]
    AudienceMedia: NotRequired[Sequence[AudienceMediaUnionTypeDef]]
    LiveSourceName: NotRequired[str]
    VodSourceName: NotRequired[str]
