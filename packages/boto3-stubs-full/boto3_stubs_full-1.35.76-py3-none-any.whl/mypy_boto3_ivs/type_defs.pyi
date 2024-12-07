"""
Type annotations for ivs service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/type_defs/)

Usage::

    ```python
    from mypy_boto3_ivs.type_defs import AudioConfigurationTypeDef

    data: AudioConfigurationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ChannelLatencyModeType,
    ChannelTypeType,
    ContainerFormatType,
    MultitrackMaximumResolutionType,
    MultitrackPolicyType,
    RecordingConfigurationStateType,
    RecordingModeType,
    RenditionConfigurationRenditionSelectionType,
    RenditionConfigurationRenditionType,
    StreamHealthType,
    StreamStateType,
    ThumbnailConfigurationResolutionType,
    ThumbnailConfigurationStorageType,
    TranscodePresetType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AudioConfigurationTypeDef",
    "BatchErrorTypeDef",
    "BatchGetChannelRequestRequestTypeDef",
    "BatchGetChannelResponseTypeDef",
    "BatchGetStreamKeyRequestRequestTypeDef",
    "BatchGetStreamKeyResponseTypeDef",
    "BatchStartViewerSessionRevocationErrorTypeDef",
    "BatchStartViewerSessionRevocationRequestRequestTypeDef",
    "BatchStartViewerSessionRevocationResponseTypeDef",
    "BatchStartViewerSessionRevocationViewerSessionTypeDef",
    "ChannelSummaryTypeDef",
    "ChannelTypeDef",
    "CreateChannelRequestRequestTypeDef",
    "CreateChannelResponseTypeDef",
    "CreatePlaybackRestrictionPolicyRequestRequestTypeDef",
    "CreatePlaybackRestrictionPolicyResponseTypeDef",
    "CreateRecordingConfigurationRequestRequestTypeDef",
    "CreateRecordingConfigurationResponseTypeDef",
    "CreateStreamKeyRequestRequestTypeDef",
    "CreateStreamKeyResponseTypeDef",
    "DeleteChannelRequestRequestTypeDef",
    "DeletePlaybackKeyPairRequestRequestTypeDef",
    "DeletePlaybackRestrictionPolicyRequestRequestTypeDef",
    "DeleteRecordingConfigurationRequestRequestTypeDef",
    "DeleteStreamKeyRequestRequestTypeDef",
    "DestinationConfigurationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetChannelRequestRequestTypeDef",
    "GetChannelResponseTypeDef",
    "GetPlaybackKeyPairRequestRequestTypeDef",
    "GetPlaybackKeyPairResponseTypeDef",
    "GetPlaybackRestrictionPolicyRequestRequestTypeDef",
    "GetPlaybackRestrictionPolicyResponseTypeDef",
    "GetRecordingConfigurationRequestRequestTypeDef",
    "GetRecordingConfigurationResponseTypeDef",
    "GetStreamKeyRequestRequestTypeDef",
    "GetStreamKeyResponseTypeDef",
    "GetStreamRequestRequestTypeDef",
    "GetStreamResponseTypeDef",
    "GetStreamSessionRequestRequestTypeDef",
    "GetStreamSessionResponseTypeDef",
    "ImportPlaybackKeyPairRequestRequestTypeDef",
    "ImportPlaybackKeyPairResponseTypeDef",
    "IngestConfigurationTypeDef",
    "IngestConfigurationsTypeDef",
    "ListChannelsRequestListChannelsPaginateTypeDef",
    "ListChannelsRequestRequestTypeDef",
    "ListChannelsResponseTypeDef",
    "ListPlaybackKeyPairsRequestListPlaybackKeyPairsPaginateTypeDef",
    "ListPlaybackKeyPairsRequestRequestTypeDef",
    "ListPlaybackKeyPairsResponseTypeDef",
    "ListPlaybackRestrictionPoliciesRequestRequestTypeDef",
    "ListPlaybackRestrictionPoliciesResponseTypeDef",
    "ListRecordingConfigurationsRequestListRecordingConfigurationsPaginateTypeDef",
    "ListRecordingConfigurationsRequestRequestTypeDef",
    "ListRecordingConfigurationsResponseTypeDef",
    "ListStreamKeysRequestListStreamKeysPaginateTypeDef",
    "ListStreamKeysRequestRequestTypeDef",
    "ListStreamKeysResponseTypeDef",
    "ListStreamSessionsRequestRequestTypeDef",
    "ListStreamSessionsResponseTypeDef",
    "ListStreamsRequestListStreamsPaginateTypeDef",
    "ListStreamsRequestRequestTypeDef",
    "ListStreamsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MultitrackInputConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PlaybackKeyPairSummaryTypeDef",
    "PlaybackKeyPairTypeDef",
    "PlaybackRestrictionPolicySummaryTypeDef",
    "PlaybackRestrictionPolicyTypeDef",
    "PutMetadataRequestRequestTypeDef",
    "RecordingConfigurationSummaryTypeDef",
    "RecordingConfigurationTypeDef",
    "RenditionConfigurationOutputTypeDef",
    "RenditionConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "S3DestinationConfigurationTypeDef",
    "SrtTypeDef",
    "StartViewerSessionRevocationRequestRequestTypeDef",
    "StopStreamRequestRequestTypeDef",
    "StreamEventTypeDef",
    "StreamFiltersTypeDef",
    "StreamKeySummaryTypeDef",
    "StreamKeyTypeDef",
    "StreamSessionSummaryTypeDef",
    "StreamSessionTypeDef",
    "StreamSummaryTypeDef",
    "StreamTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ThumbnailConfigurationOutputTypeDef",
    "ThumbnailConfigurationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateChannelRequestRequestTypeDef",
    "UpdateChannelResponseTypeDef",
    "UpdatePlaybackRestrictionPolicyRequestRequestTypeDef",
    "UpdatePlaybackRestrictionPolicyResponseTypeDef",
    "VideoConfigurationTypeDef",
)

class AudioConfigurationTypeDef(TypedDict):
    channels: NotRequired[int]
    codec: NotRequired[str]
    sampleRate: NotRequired[int]
    targetBitrate: NotRequired[int]
    track: NotRequired[str]

class BatchErrorTypeDef(TypedDict):
    arn: NotRequired[str]
    code: NotRequired[str]
    message: NotRequired[str]

class BatchGetChannelRequestRequestTypeDef(TypedDict):
    arns: Sequence[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BatchGetStreamKeyRequestRequestTypeDef(TypedDict):
    arns: Sequence[str]

class StreamKeyTypeDef(TypedDict):
    arn: NotRequired[str]
    channelArn: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    value: NotRequired[str]

class BatchStartViewerSessionRevocationErrorTypeDef(TypedDict):
    channelArn: str
    viewerId: str
    code: NotRequired[str]
    message: NotRequired[str]

class BatchStartViewerSessionRevocationViewerSessionTypeDef(TypedDict):
    channelArn: str
    viewerId: str
    viewerSessionVersionsLessThanOrEqualTo: NotRequired[int]

ChannelSummaryTypeDef = TypedDict(
    "ChannelSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "authorized": NotRequired[bool],
        "insecureIngest": NotRequired[bool],
        "latencyMode": NotRequired[ChannelLatencyModeType],
        "name": NotRequired[str],
        "playbackRestrictionPolicyArn": NotRequired[str],
        "preset": NotRequired[TranscodePresetType],
        "recordingConfigurationArn": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "type": NotRequired[ChannelTypeType],
    },
)

class MultitrackInputConfigurationTypeDef(TypedDict):
    enabled: NotRequired[bool]
    maximumResolution: NotRequired[MultitrackMaximumResolutionType]
    policy: NotRequired[MultitrackPolicyType]

class SrtTypeDef(TypedDict):
    endpoint: NotRequired[str]
    passphrase: NotRequired[str]

class CreatePlaybackRestrictionPolicyRequestRequestTypeDef(TypedDict):
    allowedCountries: NotRequired[Sequence[str]]
    allowedOrigins: NotRequired[Sequence[str]]
    enableStrictOriginEnforcement: NotRequired[bool]
    name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class PlaybackRestrictionPolicyTypeDef(TypedDict):
    allowedCountries: List[str]
    allowedOrigins: List[str]
    arn: str
    enableStrictOriginEnforcement: NotRequired[bool]
    name: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

class RenditionConfigurationTypeDef(TypedDict):
    renditionSelection: NotRequired[RenditionConfigurationRenditionSelectionType]
    renditions: NotRequired[Sequence[RenditionConfigurationRenditionType]]

class ThumbnailConfigurationTypeDef(TypedDict):
    recordingMode: NotRequired[RecordingModeType]
    resolution: NotRequired[ThumbnailConfigurationResolutionType]
    storage: NotRequired[Sequence[ThumbnailConfigurationStorageType]]
    targetIntervalSeconds: NotRequired[int]

class CreateStreamKeyRequestRequestTypeDef(TypedDict):
    channelArn: str
    tags: NotRequired[Mapping[str, str]]

class DeleteChannelRequestRequestTypeDef(TypedDict):
    arn: str

class DeletePlaybackKeyPairRequestRequestTypeDef(TypedDict):
    arn: str

class DeletePlaybackRestrictionPolicyRequestRequestTypeDef(TypedDict):
    arn: str

class DeleteRecordingConfigurationRequestRequestTypeDef(TypedDict):
    arn: str

class DeleteStreamKeyRequestRequestTypeDef(TypedDict):
    arn: str

class S3DestinationConfigurationTypeDef(TypedDict):
    bucketName: str

class GetChannelRequestRequestTypeDef(TypedDict):
    arn: str

class GetPlaybackKeyPairRequestRequestTypeDef(TypedDict):
    arn: str

class PlaybackKeyPairTypeDef(TypedDict):
    arn: NotRequired[str]
    fingerprint: NotRequired[str]
    name: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

class GetPlaybackRestrictionPolicyRequestRequestTypeDef(TypedDict):
    arn: str

class GetRecordingConfigurationRequestRequestTypeDef(TypedDict):
    arn: str

class GetStreamKeyRequestRequestTypeDef(TypedDict):
    arn: str

class GetStreamRequestRequestTypeDef(TypedDict):
    channelArn: str

class StreamTypeDef(TypedDict):
    channelArn: NotRequired[str]
    health: NotRequired[StreamHealthType]
    playbackUrl: NotRequired[str]
    startTime: NotRequired[datetime]
    state: NotRequired[StreamStateType]
    streamId: NotRequired[str]
    viewerCount: NotRequired[int]

class GetStreamSessionRequestRequestTypeDef(TypedDict):
    channelArn: str
    streamId: NotRequired[str]

class ImportPlaybackKeyPairRequestRequestTypeDef(TypedDict):
    publicKeyMaterial: str
    name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class VideoConfigurationTypeDef(TypedDict):
    avcLevel: NotRequired[str]
    avcProfile: NotRequired[str]
    codec: NotRequired[str]
    encoder: NotRequired[str]
    level: NotRequired[str]
    profile: NotRequired[str]
    targetBitrate: NotRequired[int]
    targetFramerate: NotRequired[int]
    track: NotRequired[str]
    videoHeight: NotRequired[int]
    videoWidth: NotRequired[int]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListChannelsRequestRequestTypeDef(TypedDict):
    filterByName: NotRequired[str]
    filterByPlaybackRestrictionPolicyArn: NotRequired[str]
    filterByRecordingConfigurationArn: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListPlaybackKeyPairsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class PlaybackKeyPairSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

class ListPlaybackRestrictionPoliciesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class PlaybackRestrictionPolicySummaryTypeDef(TypedDict):
    allowedCountries: List[str]
    allowedOrigins: List[str]
    arn: str
    enableStrictOriginEnforcement: NotRequired[bool]
    name: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

class ListRecordingConfigurationsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListStreamKeysRequestRequestTypeDef(TypedDict):
    channelArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class StreamKeySummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    channelArn: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

class ListStreamSessionsRequestRequestTypeDef(TypedDict):
    channelArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class StreamSessionSummaryTypeDef(TypedDict):
    endTime: NotRequired[datetime]
    hasErrorEvent: NotRequired[bool]
    startTime: NotRequired[datetime]
    streamId: NotRequired[str]

class StreamFiltersTypeDef(TypedDict):
    health: NotRequired[StreamHealthType]

class StreamSummaryTypeDef(TypedDict):
    channelArn: NotRequired[str]
    health: NotRequired[StreamHealthType]
    startTime: NotRequired[datetime]
    state: NotRequired[StreamStateType]
    streamId: NotRequired[str]
    viewerCount: NotRequired[int]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class PutMetadataRequestRequestTypeDef(TypedDict):
    channelArn: str
    metadata: str

class RenditionConfigurationOutputTypeDef(TypedDict):
    renditionSelection: NotRequired[RenditionConfigurationRenditionSelectionType]
    renditions: NotRequired[List[RenditionConfigurationRenditionType]]

class ThumbnailConfigurationOutputTypeDef(TypedDict):
    recordingMode: NotRequired[RecordingModeType]
    resolution: NotRequired[ThumbnailConfigurationResolutionType]
    storage: NotRequired[List[ThumbnailConfigurationStorageType]]
    targetIntervalSeconds: NotRequired[int]

class StartViewerSessionRevocationRequestRequestTypeDef(TypedDict):
    channelArn: str
    viewerId: str
    viewerSessionVersionsLessThanOrEqualTo: NotRequired[int]

class StopStreamRequestRequestTypeDef(TypedDict):
    channelArn: str

StreamEventTypeDef = TypedDict(
    "StreamEventTypeDef",
    {
        "code": NotRequired[str],
        "eventTime": NotRequired[datetime],
        "name": NotRequired[str],
        "type": NotRequired[str],
    },
)

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdatePlaybackRestrictionPolicyRequestRequestTypeDef(TypedDict):
    arn: str
    allowedCountries: NotRequired[Sequence[str]]
    allowedOrigins: NotRequired[Sequence[str]]
    enableStrictOriginEnforcement: NotRequired[bool]
    name: NotRequired[str]

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetStreamKeyResponseTypeDef(TypedDict):
    errors: List[BatchErrorTypeDef]
    streamKeys: List[StreamKeyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateStreamKeyResponseTypeDef(TypedDict):
    streamKey: StreamKeyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetStreamKeyResponseTypeDef(TypedDict):
    streamKey: StreamKeyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class BatchStartViewerSessionRevocationResponseTypeDef(TypedDict):
    errors: List[BatchStartViewerSessionRevocationErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchStartViewerSessionRevocationRequestRequestTypeDef(TypedDict):
    viewerSessions: Sequence[BatchStartViewerSessionRevocationViewerSessionTypeDef]

class ListChannelsResponseTypeDef(TypedDict):
    channels: List[ChannelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

CreateChannelRequestRequestTypeDef = TypedDict(
    "CreateChannelRequestRequestTypeDef",
    {
        "authorized": NotRequired[bool],
        "containerFormat": NotRequired[ContainerFormatType],
        "insecureIngest": NotRequired[bool],
        "latencyMode": NotRequired[ChannelLatencyModeType],
        "multitrackInputConfiguration": NotRequired[MultitrackInputConfigurationTypeDef],
        "name": NotRequired[str],
        "playbackRestrictionPolicyArn": NotRequired[str],
        "preset": NotRequired[TranscodePresetType],
        "recordingConfigurationArn": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
        "type": NotRequired[ChannelTypeType],
    },
)
UpdateChannelRequestRequestTypeDef = TypedDict(
    "UpdateChannelRequestRequestTypeDef",
    {
        "arn": str,
        "authorized": NotRequired[bool],
        "containerFormat": NotRequired[ContainerFormatType],
        "insecureIngest": NotRequired[bool],
        "latencyMode": NotRequired[ChannelLatencyModeType],
        "multitrackInputConfiguration": NotRequired[MultitrackInputConfigurationTypeDef],
        "name": NotRequired[str],
        "playbackRestrictionPolicyArn": NotRequired[str],
        "preset": NotRequired[TranscodePresetType],
        "recordingConfigurationArn": NotRequired[str],
        "type": NotRequired[ChannelTypeType],
    },
)
ChannelTypeDef = TypedDict(
    "ChannelTypeDef",
    {
        "arn": NotRequired[str],
        "authorized": NotRequired[bool],
        "containerFormat": NotRequired[ContainerFormatType],
        "ingestEndpoint": NotRequired[str],
        "insecureIngest": NotRequired[bool],
        "latencyMode": NotRequired[ChannelLatencyModeType],
        "multitrackInputConfiguration": NotRequired[MultitrackInputConfigurationTypeDef],
        "name": NotRequired[str],
        "playbackRestrictionPolicyArn": NotRequired[str],
        "playbackUrl": NotRequired[str],
        "preset": NotRequired[TranscodePresetType],
        "recordingConfigurationArn": NotRequired[str],
        "srt": NotRequired[SrtTypeDef],
        "tags": NotRequired[Dict[str, str]],
        "type": NotRequired[ChannelTypeType],
    },
)

class CreatePlaybackRestrictionPolicyResponseTypeDef(TypedDict):
    playbackRestrictionPolicy: PlaybackRestrictionPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetPlaybackRestrictionPolicyResponseTypeDef(TypedDict):
    playbackRestrictionPolicy: PlaybackRestrictionPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePlaybackRestrictionPolicyResponseTypeDef(TypedDict):
    playbackRestrictionPolicy: PlaybackRestrictionPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DestinationConfigurationTypeDef(TypedDict):
    s3: NotRequired[S3DestinationConfigurationTypeDef]

class GetPlaybackKeyPairResponseTypeDef(TypedDict):
    keyPair: PlaybackKeyPairTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ImportPlaybackKeyPairResponseTypeDef(TypedDict):
    keyPair: PlaybackKeyPairTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetStreamResponseTypeDef(TypedDict):
    stream: StreamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class IngestConfigurationTypeDef(TypedDict):
    audio: NotRequired[AudioConfigurationTypeDef]
    video: NotRequired[VideoConfigurationTypeDef]

class IngestConfigurationsTypeDef(TypedDict):
    audioConfigurations: List[AudioConfigurationTypeDef]
    videoConfigurations: List[VideoConfigurationTypeDef]

class ListChannelsRequestListChannelsPaginateTypeDef(TypedDict):
    filterByName: NotRequired[str]
    filterByPlaybackRestrictionPolicyArn: NotRequired[str]
    filterByRecordingConfigurationArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPlaybackKeyPairsRequestListPlaybackKeyPairsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRecordingConfigurationsRequestListRecordingConfigurationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListStreamKeysRequestListStreamKeysPaginateTypeDef(TypedDict):
    channelArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPlaybackKeyPairsResponseTypeDef(TypedDict):
    keyPairs: List[PlaybackKeyPairSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPlaybackRestrictionPoliciesResponseTypeDef(TypedDict):
    playbackRestrictionPolicies: List[PlaybackRestrictionPolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListStreamKeysResponseTypeDef(TypedDict):
    streamKeys: List[StreamKeySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListStreamSessionsResponseTypeDef(TypedDict):
    streamSessions: List[StreamSessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListStreamsRequestListStreamsPaginateTypeDef(TypedDict):
    filterBy: NotRequired[StreamFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListStreamsRequestRequestTypeDef(TypedDict):
    filterBy: NotRequired[StreamFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListStreamsResponseTypeDef(TypedDict):
    streams: List[StreamSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class BatchGetChannelResponseTypeDef(TypedDict):
    channels: List[ChannelTypeDef]
    errors: List[BatchErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateChannelResponseTypeDef(TypedDict):
    channel: ChannelTypeDef
    streamKey: StreamKeyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetChannelResponseTypeDef(TypedDict):
    channel: ChannelTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateChannelResponseTypeDef(TypedDict):
    channel: ChannelTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRecordingConfigurationRequestRequestTypeDef(TypedDict):
    destinationConfiguration: DestinationConfigurationTypeDef
    name: NotRequired[str]
    recordingReconnectWindowSeconds: NotRequired[int]
    renditionConfiguration: NotRequired[RenditionConfigurationTypeDef]
    tags: NotRequired[Mapping[str, str]]
    thumbnailConfiguration: NotRequired[ThumbnailConfigurationTypeDef]

class RecordingConfigurationSummaryTypeDef(TypedDict):
    arn: str
    destinationConfiguration: DestinationConfigurationTypeDef
    state: RecordingConfigurationStateType
    name: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

class RecordingConfigurationTypeDef(TypedDict):
    arn: str
    destinationConfiguration: DestinationConfigurationTypeDef
    state: RecordingConfigurationStateType
    name: NotRequired[str]
    recordingReconnectWindowSeconds: NotRequired[int]
    renditionConfiguration: NotRequired[RenditionConfigurationOutputTypeDef]
    tags: NotRequired[Dict[str, str]]
    thumbnailConfiguration: NotRequired[ThumbnailConfigurationOutputTypeDef]

class ListRecordingConfigurationsResponseTypeDef(TypedDict):
    recordingConfigurations: List[RecordingConfigurationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateRecordingConfigurationResponseTypeDef(TypedDict):
    recordingConfiguration: RecordingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetRecordingConfigurationResponseTypeDef(TypedDict):
    recordingConfiguration: RecordingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StreamSessionTypeDef(TypedDict):
    channel: NotRequired[ChannelTypeDef]
    endTime: NotRequired[datetime]
    ingestConfiguration: NotRequired[IngestConfigurationTypeDef]
    ingestConfigurations: NotRequired[IngestConfigurationsTypeDef]
    recordingConfiguration: NotRequired[RecordingConfigurationTypeDef]
    startTime: NotRequired[datetime]
    streamId: NotRequired[str]
    truncatedEvents: NotRequired[List[StreamEventTypeDef]]

class GetStreamSessionResponseTypeDef(TypedDict):
    streamSession: StreamSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
