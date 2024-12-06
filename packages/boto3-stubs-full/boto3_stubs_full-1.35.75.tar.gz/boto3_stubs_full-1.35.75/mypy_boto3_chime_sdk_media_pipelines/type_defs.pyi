"""
Type annotations for chime-sdk-media-pipelines service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/type_defs/)

Usage::

    ```python
    from mypy_boto3_chime_sdk_media_pipelines.type_defs import ActiveSpeakerOnlyConfigurationTypeDef

    data: ActiveSpeakerOnlyConfigurationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ActiveSpeakerPositionType,
    ArtifactsConcatenationStateType,
    ArtifactsStateType,
    AudioChannelsOptionType,
    AudioMuxTypeType,
    BorderColorType,
    CallAnalyticsLanguageCodeType,
    CanvasOrientationType,
    ContentRedactionOutputType,
    ContentShareLayoutOptionType,
    FragmentSelectorTypeType,
    HighlightColorType,
    HorizontalTilePositionType,
    KinesisVideoStreamPoolStatusType,
    LiveConnectorMuxTypeType,
    MediaInsightsPipelineConfigurationElementTypeType,
    MediaPipelineElementStatusType,
    MediaPipelineStatusType,
    MediaPipelineStatusUpdateType,
    MediaPipelineTaskStatusType,
    MediaStreamTypeType,
    PartialResultsStabilityType,
    ParticipantRoleType,
    PresenterPositionType,
    RealTimeAlertRuleTypeType,
    RecordingFileFormatType,
    ResolutionOptionType,
    TileOrderType,
    VerticalTilePositionType,
    VocabularyFilterMethodType,
    VoiceAnalyticsConfigurationStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "ActiveSpeakerOnlyConfigurationTypeDef",
    "AmazonTranscribeCallAnalyticsProcessorConfigurationOutputTypeDef",
    "AmazonTranscribeCallAnalyticsProcessorConfigurationTypeDef",
    "AmazonTranscribeCallAnalyticsProcessorConfigurationUnionTypeDef",
    "AmazonTranscribeProcessorConfigurationTypeDef",
    "ArtifactsConcatenationConfigurationTypeDef",
    "ArtifactsConfigurationTypeDef",
    "AudioArtifactsConfigurationTypeDef",
    "AudioConcatenationConfigurationTypeDef",
    "ChannelDefinitionTypeDef",
    "ChimeSdkMeetingConcatenationConfigurationTypeDef",
    "ChimeSdkMeetingConfigurationOutputTypeDef",
    "ChimeSdkMeetingConfigurationTypeDef",
    "ChimeSdkMeetingLiveConnectorConfigurationOutputTypeDef",
    "ChimeSdkMeetingLiveConnectorConfigurationTypeDef",
    "ChimeSdkMeetingLiveConnectorConfigurationUnionTypeDef",
    "CompositedVideoArtifactsConfigurationTypeDef",
    "CompositedVideoConcatenationConfigurationTypeDef",
    "ConcatenationSinkTypeDef",
    "ConcatenationSourceTypeDef",
    "ContentArtifactsConfigurationTypeDef",
    "ContentConcatenationConfigurationTypeDef",
    "CreateMediaCapturePipelineRequestRequestTypeDef",
    "CreateMediaCapturePipelineResponseTypeDef",
    "CreateMediaConcatenationPipelineRequestRequestTypeDef",
    "CreateMediaConcatenationPipelineResponseTypeDef",
    "CreateMediaInsightsPipelineConfigurationRequestRequestTypeDef",
    "CreateMediaInsightsPipelineConfigurationResponseTypeDef",
    "CreateMediaInsightsPipelineRequestRequestTypeDef",
    "CreateMediaInsightsPipelineResponseTypeDef",
    "CreateMediaLiveConnectorPipelineRequestRequestTypeDef",
    "CreateMediaLiveConnectorPipelineResponseTypeDef",
    "CreateMediaPipelineKinesisVideoStreamPoolRequestRequestTypeDef",
    "CreateMediaPipelineKinesisVideoStreamPoolResponseTypeDef",
    "CreateMediaStreamPipelineRequestRequestTypeDef",
    "CreateMediaStreamPipelineResponseTypeDef",
    "DataChannelConcatenationConfigurationTypeDef",
    "DeleteMediaCapturePipelineRequestRequestTypeDef",
    "DeleteMediaInsightsPipelineConfigurationRequestRequestTypeDef",
    "DeleteMediaPipelineKinesisVideoStreamPoolRequestRequestTypeDef",
    "DeleteMediaPipelineRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "FragmentSelectorOutputTypeDef",
    "FragmentSelectorTypeDef",
    "FragmentSelectorUnionTypeDef",
    "GetMediaCapturePipelineRequestRequestTypeDef",
    "GetMediaCapturePipelineResponseTypeDef",
    "GetMediaInsightsPipelineConfigurationRequestRequestTypeDef",
    "GetMediaInsightsPipelineConfigurationResponseTypeDef",
    "GetMediaPipelineKinesisVideoStreamPoolRequestRequestTypeDef",
    "GetMediaPipelineKinesisVideoStreamPoolResponseTypeDef",
    "GetMediaPipelineRequestRequestTypeDef",
    "GetMediaPipelineResponseTypeDef",
    "GetSpeakerSearchTaskRequestRequestTypeDef",
    "GetSpeakerSearchTaskResponseTypeDef",
    "GetVoiceToneAnalysisTaskRequestRequestTypeDef",
    "GetVoiceToneAnalysisTaskResponseTypeDef",
    "GridViewConfigurationTypeDef",
    "HorizontalLayoutConfigurationTypeDef",
    "IssueDetectionConfigurationTypeDef",
    "KeywordMatchConfigurationOutputTypeDef",
    "KeywordMatchConfigurationTypeDef",
    "KeywordMatchConfigurationUnionTypeDef",
    "KinesisDataStreamSinkConfigurationTypeDef",
    "KinesisVideoStreamConfigurationTypeDef",
    "KinesisVideoStreamConfigurationUpdateTypeDef",
    "KinesisVideoStreamPoolConfigurationTypeDef",
    "KinesisVideoStreamPoolSummaryTypeDef",
    "KinesisVideoStreamRecordingSourceRuntimeConfigurationOutputTypeDef",
    "KinesisVideoStreamRecordingSourceRuntimeConfigurationTypeDef",
    "KinesisVideoStreamSourceRuntimeConfigurationOutputTypeDef",
    "KinesisVideoStreamSourceRuntimeConfigurationTypeDef",
    "KinesisVideoStreamSourceTaskConfigurationTypeDef",
    "LambdaFunctionSinkConfigurationTypeDef",
    "ListMediaCapturePipelinesRequestRequestTypeDef",
    "ListMediaCapturePipelinesResponseTypeDef",
    "ListMediaInsightsPipelineConfigurationsRequestRequestTypeDef",
    "ListMediaInsightsPipelineConfigurationsResponseTypeDef",
    "ListMediaPipelineKinesisVideoStreamPoolsRequestRequestTypeDef",
    "ListMediaPipelineKinesisVideoStreamPoolsResponseTypeDef",
    "ListMediaPipelinesRequestRequestTypeDef",
    "ListMediaPipelinesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LiveConnectorRTMPConfigurationTypeDef",
    "LiveConnectorSinkConfigurationTypeDef",
    "LiveConnectorSourceConfigurationOutputTypeDef",
    "LiveConnectorSourceConfigurationTypeDef",
    "LiveConnectorSourceConfigurationUnionTypeDef",
    "MediaCapturePipelineSourceConfigurationTypeDef",
    "MediaCapturePipelineSummaryTypeDef",
    "MediaCapturePipelineTypeDef",
    "MediaConcatenationPipelineTypeDef",
    "MediaInsightsPipelineConfigurationElementOutputTypeDef",
    "MediaInsightsPipelineConfigurationElementTypeDef",
    "MediaInsightsPipelineConfigurationElementUnionTypeDef",
    "MediaInsightsPipelineConfigurationSummaryTypeDef",
    "MediaInsightsPipelineConfigurationTypeDef",
    "MediaInsightsPipelineElementStatusTypeDef",
    "MediaInsightsPipelineTypeDef",
    "MediaLiveConnectorPipelineTypeDef",
    "MediaPipelineSummaryTypeDef",
    "MediaPipelineTypeDef",
    "MediaStreamPipelineTypeDef",
    "MediaStreamSinkTypeDef",
    "MediaStreamSourceTypeDef",
    "MeetingEventsConcatenationConfigurationTypeDef",
    "PostCallAnalyticsSettingsTypeDef",
    "PresenterOnlyConfigurationTypeDef",
    "RealTimeAlertConfigurationOutputTypeDef",
    "RealTimeAlertConfigurationTypeDef",
    "RealTimeAlertRuleOutputTypeDef",
    "RealTimeAlertRuleTypeDef",
    "RealTimeAlertRuleUnionTypeDef",
    "RecordingStreamConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "S3BucketSinkConfigurationTypeDef",
    "S3RecordingSinkConfigurationTypeDef",
    "S3RecordingSinkRuntimeConfigurationTypeDef",
    "SelectedVideoStreamsOutputTypeDef",
    "SelectedVideoStreamsTypeDef",
    "SelectedVideoStreamsUnionTypeDef",
    "SentimentConfigurationTypeDef",
    "SnsTopicSinkConfigurationTypeDef",
    "SourceConfigurationOutputTypeDef",
    "SourceConfigurationTypeDef",
    "SourceConfigurationUnionTypeDef",
    "SpeakerSearchTaskTypeDef",
    "SqsQueueSinkConfigurationTypeDef",
    "SseAwsKeyManagementParamsTypeDef",
    "StartSpeakerSearchTaskRequestRequestTypeDef",
    "StartSpeakerSearchTaskResponseTypeDef",
    "StartVoiceToneAnalysisTaskRequestRequestTypeDef",
    "StartVoiceToneAnalysisTaskResponseTypeDef",
    "StopSpeakerSearchTaskRequestRequestTypeDef",
    "StopVoiceToneAnalysisTaskRequestRequestTypeDef",
    "StreamChannelDefinitionOutputTypeDef",
    "StreamChannelDefinitionTypeDef",
    "StreamChannelDefinitionUnionTypeDef",
    "StreamConfigurationOutputTypeDef",
    "StreamConfigurationTypeDef",
    "StreamConfigurationUnionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TimestampRangeOutputTypeDef",
    "TimestampRangeTypeDef",
    "TimestampRangeUnionTypeDef",
    "TimestampTypeDef",
    "TranscriptionMessagesConcatenationConfigurationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateMediaInsightsPipelineConfigurationRequestRequestTypeDef",
    "UpdateMediaInsightsPipelineConfigurationResponseTypeDef",
    "UpdateMediaInsightsPipelineStatusRequestRequestTypeDef",
    "UpdateMediaPipelineKinesisVideoStreamPoolRequestRequestTypeDef",
    "UpdateMediaPipelineKinesisVideoStreamPoolResponseTypeDef",
    "VerticalLayoutConfigurationTypeDef",
    "VideoArtifactsConfigurationTypeDef",
    "VideoAttributeTypeDef",
    "VideoConcatenationConfigurationTypeDef",
    "VoiceAnalyticsProcessorConfigurationTypeDef",
    "VoiceEnhancementSinkConfigurationTypeDef",
    "VoiceToneAnalysisTaskTypeDef",
)

class ActiveSpeakerOnlyConfigurationTypeDef(TypedDict):
    ActiveSpeakerPosition: NotRequired[ActiveSpeakerPositionType]

class PostCallAnalyticsSettingsTypeDef(TypedDict):
    OutputLocation: str
    DataAccessRoleArn: str
    ContentRedactionOutput: NotRequired[ContentRedactionOutputType]
    OutputEncryptionKMSKeyId: NotRequired[str]

class AmazonTranscribeProcessorConfigurationTypeDef(TypedDict):
    LanguageCode: NotRequired[CallAnalyticsLanguageCodeType]
    VocabularyName: NotRequired[str]
    VocabularyFilterName: NotRequired[str]
    VocabularyFilterMethod: NotRequired[VocabularyFilterMethodType]
    ShowSpeakerLabel: NotRequired[bool]
    EnablePartialResultsStabilization: NotRequired[bool]
    PartialResultsStability: NotRequired[PartialResultsStabilityType]
    ContentIdentificationType: NotRequired[Literal["PII"]]
    ContentRedactionType: NotRequired[Literal["PII"]]
    PiiEntityTypes: NotRequired[str]
    LanguageModelName: NotRequired[str]
    FilterPartialResults: NotRequired[bool]
    IdentifyLanguage: NotRequired[bool]
    IdentifyMultipleLanguages: NotRequired[bool]
    LanguageOptions: NotRequired[str]
    PreferredLanguage: NotRequired[CallAnalyticsLanguageCodeType]
    VocabularyNames: NotRequired[str]
    VocabularyFilterNames: NotRequired[str]

class AudioConcatenationConfigurationTypeDef(TypedDict):
    State: Literal["Enabled"]

class CompositedVideoConcatenationConfigurationTypeDef(TypedDict):
    State: ArtifactsConcatenationStateType

class ContentConcatenationConfigurationTypeDef(TypedDict):
    State: ArtifactsConcatenationStateType

class DataChannelConcatenationConfigurationTypeDef(TypedDict):
    State: ArtifactsConcatenationStateType

class MeetingEventsConcatenationConfigurationTypeDef(TypedDict):
    State: ArtifactsConcatenationStateType

class TranscriptionMessagesConcatenationConfigurationTypeDef(TypedDict):
    State: ArtifactsConcatenationStateType

class VideoConcatenationConfigurationTypeDef(TypedDict):
    State: ArtifactsConcatenationStateType

class AudioArtifactsConfigurationTypeDef(TypedDict):
    MuxType: AudioMuxTypeType

class ContentArtifactsConfigurationTypeDef(TypedDict):
    State: ArtifactsStateType
    MuxType: NotRequired[Literal["ContentOnly"]]

class VideoArtifactsConfigurationTypeDef(TypedDict):
    State: ArtifactsStateType
    MuxType: NotRequired[Literal["VideoOnly"]]

class ChannelDefinitionTypeDef(TypedDict):
    ChannelId: int
    ParticipantRole: NotRequired[ParticipantRoleType]

class S3BucketSinkConfigurationTypeDef(TypedDict):
    Destination: str

class SseAwsKeyManagementParamsTypeDef(TypedDict):
    AwsKmsKeyId: str
    AwsKmsEncryptionContext: NotRequired[str]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class S3RecordingSinkRuntimeConfigurationTypeDef(TypedDict):
    Destination: str
    RecordingFileFormat: RecordingFileFormatType

class KinesisVideoStreamConfigurationTypeDef(TypedDict):
    Region: str
    DataRetentionInHours: NotRequired[int]

class MediaStreamSinkTypeDef(TypedDict):
    SinkArn: str
    SinkType: Literal["KinesisVideoStreamPool"]
    ReservedStreamCapacity: int
    MediaStreamType: MediaStreamTypeType

class MediaStreamSourceTypeDef(TypedDict):
    SourceType: Literal["ChimeSdkMeeting"]
    SourceArn: str

class DeleteMediaCapturePipelineRequestRequestTypeDef(TypedDict):
    MediaPipelineId: str

class DeleteMediaInsightsPipelineConfigurationRequestRequestTypeDef(TypedDict):
    Identifier: str

class DeleteMediaPipelineKinesisVideoStreamPoolRequestRequestTypeDef(TypedDict):
    Identifier: str

class DeleteMediaPipelineRequestRequestTypeDef(TypedDict):
    MediaPipelineId: str

class TimestampRangeOutputTypeDef(TypedDict):
    StartTimestamp: datetime
    EndTimestamp: datetime

class GetMediaCapturePipelineRequestRequestTypeDef(TypedDict):
    MediaPipelineId: str

class GetMediaInsightsPipelineConfigurationRequestRequestTypeDef(TypedDict):
    Identifier: str

class GetMediaPipelineKinesisVideoStreamPoolRequestRequestTypeDef(TypedDict):
    Identifier: str

class GetMediaPipelineRequestRequestTypeDef(TypedDict):
    MediaPipelineId: str

class GetSpeakerSearchTaskRequestRequestTypeDef(TypedDict):
    Identifier: str
    SpeakerSearchTaskId: str

class SpeakerSearchTaskTypeDef(TypedDict):
    SpeakerSearchTaskId: NotRequired[str]
    SpeakerSearchTaskStatus: NotRequired[MediaPipelineTaskStatusType]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]

class GetVoiceToneAnalysisTaskRequestRequestTypeDef(TypedDict):
    Identifier: str
    VoiceToneAnalysisTaskId: str

class VoiceToneAnalysisTaskTypeDef(TypedDict):
    VoiceToneAnalysisTaskId: NotRequired[str]
    VoiceToneAnalysisTaskStatus: NotRequired[MediaPipelineTaskStatusType]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]

class HorizontalLayoutConfigurationTypeDef(TypedDict):
    TileOrder: NotRequired[TileOrderType]
    TilePosition: NotRequired[HorizontalTilePositionType]
    TileCount: NotRequired[int]
    TileAspectRatio: NotRequired[str]

class PresenterOnlyConfigurationTypeDef(TypedDict):
    PresenterPosition: NotRequired[PresenterPositionType]

class VerticalLayoutConfigurationTypeDef(TypedDict):
    TileOrder: NotRequired[TileOrderType]
    TilePosition: NotRequired[VerticalTilePositionType]
    TileCount: NotRequired[int]
    TileAspectRatio: NotRequired[str]

class VideoAttributeTypeDef(TypedDict):
    CornerRadius: NotRequired[int]
    BorderColor: NotRequired[BorderColorType]
    HighlightColor: NotRequired[HighlightColorType]
    BorderThickness: NotRequired[int]

class IssueDetectionConfigurationTypeDef(TypedDict):
    RuleName: str

class KeywordMatchConfigurationOutputTypeDef(TypedDict):
    RuleName: str
    Keywords: List[str]
    Negate: NotRequired[bool]

class KeywordMatchConfigurationTypeDef(TypedDict):
    RuleName: str
    Keywords: Sequence[str]
    Negate: NotRequired[bool]

class KinesisDataStreamSinkConfigurationTypeDef(TypedDict):
    InsightsTarget: NotRequired[str]

class KinesisVideoStreamConfigurationUpdateTypeDef(TypedDict):
    DataRetentionInHours: NotRequired[int]

class KinesisVideoStreamPoolSummaryTypeDef(TypedDict):
    PoolName: NotRequired[str]
    PoolId: NotRequired[str]
    PoolArn: NotRequired[str]

class RecordingStreamConfigurationTypeDef(TypedDict):
    StreamArn: NotRequired[str]

class KinesisVideoStreamSourceTaskConfigurationTypeDef(TypedDict):
    StreamArn: str
    ChannelId: int
    FragmentNumber: NotRequired[str]

class LambdaFunctionSinkConfigurationTypeDef(TypedDict):
    InsightsTarget: NotRequired[str]

class ListMediaCapturePipelinesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class MediaCapturePipelineSummaryTypeDef(TypedDict):
    MediaPipelineId: NotRequired[str]
    MediaPipelineArn: NotRequired[str]

class ListMediaInsightsPipelineConfigurationsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class MediaInsightsPipelineConfigurationSummaryTypeDef(TypedDict):
    MediaInsightsPipelineConfigurationName: NotRequired[str]
    MediaInsightsPipelineConfigurationId: NotRequired[str]
    MediaInsightsPipelineConfigurationArn: NotRequired[str]

class ListMediaPipelineKinesisVideoStreamPoolsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListMediaPipelinesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class MediaPipelineSummaryTypeDef(TypedDict):
    MediaPipelineId: NotRequired[str]
    MediaPipelineArn: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str

class LiveConnectorRTMPConfigurationTypeDef(TypedDict):
    Url: str
    AudioChannels: NotRequired[AudioChannelsOptionType]
    AudioSampleRate: NotRequired[str]

class S3RecordingSinkConfigurationTypeDef(TypedDict):
    Destination: NotRequired[str]
    RecordingFileFormat: NotRequired[RecordingFileFormatType]

class SnsTopicSinkConfigurationTypeDef(TypedDict):
    InsightsTarget: NotRequired[str]

class SqsQueueSinkConfigurationTypeDef(TypedDict):
    InsightsTarget: NotRequired[str]

class VoiceAnalyticsProcessorConfigurationTypeDef(TypedDict):
    SpeakerSearchStatus: NotRequired[VoiceAnalyticsConfigurationStatusType]
    VoiceToneAnalysisStatus: NotRequired[VoiceAnalyticsConfigurationStatusType]

class VoiceEnhancementSinkConfigurationTypeDef(TypedDict):
    Disabled: NotRequired[bool]

MediaInsightsPipelineElementStatusTypeDef = TypedDict(
    "MediaInsightsPipelineElementStatusTypeDef",
    {
        "Type": NotRequired[MediaInsightsPipelineConfigurationElementTypeType],
        "Status": NotRequired[MediaPipelineElementStatusType],
    },
)

class SentimentConfigurationTypeDef(TypedDict):
    RuleName: str
    SentimentType: Literal["NEGATIVE"]
    TimePeriod: int

class SelectedVideoStreamsOutputTypeDef(TypedDict):
    AttendeeIds: NotRequired[List[str]]
    ExternalUserIds: NotRequired[List[str]]

class SelectedVideoStreamsTypeDef(TypedDict):
    AttendeeIds: NotRequired[Sequence[str]]
    ExternalUserIds: NotRequired[Sequence[str]]

class StopSpeakerSearchTaskRequestRequestTypeDef(TypedDict):
    Identifier: str
    SpeakerSearchTaskId: str

class StopVoiceToneAnalysisTaskRequestRequestTypeDef(TypedDict):
    Identifier: str
    VoiceToneAnalysisTaskId: str

TimestampTypeDef = Union[datetime, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]

class UpdateMediaInsightsPipelineStatusRequestRequestTypeDef(TypedDict):
    Identifier: str
    UpdateStatus: MediaPipelineStatusUpdateType

class AmazonTranscribeCallAnalyticsProcessorConfigurationOutputTypeDef(TypedDict):
    LanguageCode: CallAnalyticsLanguageCodeType
    VocabularyName: NotRequired[str]
    VocabularyFilterName: NotRequired[str]
    VocabularyFilterMethod: NotRequired[VocabularyFilterMethodType]
    LanguageModelName: NotRequired[str]
    EnablePartialResultsStabilization: NotRequired[bool]
    PartialResultsStability: NotRequired[PartialResultsStabilityType]
    ContentIdentificationType: NotRequired[Literal["PII"]]
    ContentRedactionType: NotRequired[Literal["PII"]]
    PiiEntityTypes: NotRequired[str]
    FilterPartialResults: NotRequired[bool]
    PostCallAnalyticsSettings: NotRequired[PostCallAnalyticsSettingsTypeDef]
    CallAnalyticsStreamCategories: NotRequired[List[str]]

class AmazonTranscribeCallAnalyticsProcessorConfigurationTypeDef(TypedDict):
    LanguageCode: CallAnalyticsLanguageCodeType
    VocabularyName: NotRequired[str]
    VocabularyFilterName: NotRequired[str]
    VocabularyFilterMethod: NotRequired[VocabularyFilterMethodType]
    LanguageModelName: NotRequired[str]
    EnablePartialResultsStabilization: NotRequired[bool]
    PartialResultsStability: NotRequired[PartialResultsStabilityType]
    ContentIdentificationType: NotRequired[Literal["PII"]]
    ContentRedactionType: NotRequired[Literal["PII"]]
    PiiEntityTypes: NotRequired[str]
    FilterPartialResults: NotRequired[bool]
    PostCallAnalyticsSettings: NotRequired[PostCallAnalyticsSettingsTypeDef]
    CallAnalyticsStreamCategories: NotRequired[Sequence[str]]

class ArtifactsConcatenationConfigurationTypeDef(TypedDict):
    Audio: AudioConcatenationConfigurationTypeDef
    Video: VideoConcatenationConfigurationTypeDef
    Content: ContentConcatenationConfigurationTypeDef
    DataChannel: DataChannelConcatenationConfigurationTypeDef
    TranscriptionMessages: TranscriptionMessagesConcatenationConfigurationTypeDef
    MeetingEvents: MeetingEventsConcatenationConfigurationTypeDef
    CompositedVideo: CompositedVideoConcatenationConfigurationTypeDef

class StreamChannelDefinitionOutputTypeDef(TypedDict):
    NumberOfChannels: int
    ChannelDefinitions: NotRequired[List[ChannelDefinitionTypeDef]]

class StreamChannelDefinitionTypeDef(TypedDict):
    NumberOfChannels: int
    ChannelDefinitions: NotRequired[Sequence[ChannelDefinitionTypeDef]]

ConcatenationSinkTypeDef = TypedDict(
    "ConcatenationSinkTypeDef",
    {
        "Type": Literal["S3Bucket"],
        "S3BucketSinkConfiguration": S3BucketSinkConfigurationTypeDef,
    },
)

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMediaPipelineKinesisVideoStreamPoolRequestRequestTypeDef(TypedDict):
    StreamConfiguration: KinesisVideoStreamConfigurationTypeDef
    PoolName: str
    ClientRequestToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class KinesisVideoStreamPoolConfigurationTypeDef(TypedDict):
    PoolArn: NotRequired[str]
    PoolName: NotRequired[str]
    PoolId: NotRequired[str]
    PoolStatus: NotRequired[KinesisVideoStreamPoolStatusType]
    PoolSize: NotRequired[int]
    StreamConfiguration: NotRequired[KinesisVideoStreamConfigurationTypeDef]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]

class CreateMediaStreamPipelineRequestRequestTypeDef(TypedDict):
    Sources: Sequence[MediaStreamSourceTypeDef]
    Sinks: Sequence[MediaStreamSinkTypeDef]
    ClientRequestToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class MediaStreamPipelineTypeDef(TypedDict):
    MediaPipelineId: NotRequired[str]
    MediaPipelineArn: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]
    Status: NotRequired[MediaPipelineStatusType]
    Sources: NotRequired[List[MediaStreamSourceTypeDef]]
    Sinks: NotRequired[List[MediaStreamSinkTypeDef]]

class FragmentSelectorOutputTypeDef(TypedDict):
    FragmentSelectorType: FragmentSelectorTypeType
    TimestampRange: TimestampRangeOutputTypeDef

class GetSpeakerSearchTaskResponseTypeDef(TypedDict):
    SpeakerSearchTask: SpeakerSearchTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartSpeakerSearchTaskResponseTypeDef(TypedDict):
    SpeakerSearchTask: SpeakerSearchTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceToneAnalysisTaskResponseTypeDef(TypedDict):
    VoiceToneAnalysisTask: VoiceToneAnalysisTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartVoiceToneAnalysisTaskResponseTypeDef(TypedDict):
    VoiceToneAnalysisTask: VoiceToneAnalysisTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GridViewConfigurationTypeDef(TypedDict):
    ContentShareLayout: ContentShareLayoutOptionType
    PresenterOnlyConfiguration: NotRequired[PresenterOnlyConfigurationTypeDef]
    ActiveSpeakerOnlyConfiguration: NotRequired[ActiveSpeakerOnlyConfigurationTypeDef]
    HorizontalLayoutConfiguration: NotRequired[HorizontalLayoutConfigurationTypeDef]
    VerticalLayoutConfiguration: NotRequired[VerticalLayoutConfigurationTypeDef]
    VideoAttribute: NotRequired[VideoAttributeTypeDef]
    CanvasOrientation: NotRequired[CanvasOrientationType]

KeywordMatchConfigurationUnionTypeDef = Union[
    KeywordMatchConfigurationTypeDef, KeywordMatchConfigurationOutputTypeDef
]

class UpdateMediaPipelineKinesisVideoStreamPoolRequestRequestTypeDef(TypedDict):
    Identifier: str
    StreamConfiguration: NotRequired[KinesisVideoStreamConfigurationUpdateTypeDef]

class ListMediaPipelineKinesisVideoStreamPoolsResponseTypeDef(TypedDict):
    KinesisVideoStreamPools: List[KinesisVideoStreamPoolSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class StartSpeakerSearchTaskRequestRequestTypeDef(TypedDict):
    Identifier: str
    VoiceProfileDomainArn: str
    KinesisVideoStreamSourceTaskConfiguration: NotRequired[
        KinesisVideoStreamSourceTaskConfigurationTypeDef
    ]
    ClientRequestToken: NotRequired[str]

class StartVoiceToneAnalysisTaskRequestRequestTypeDef(TypedDict):
    Identifier: str
    LanguageCode: Literal["en-US"]
    KinesisVideoStreamSourceTaskConfiguration: NotRequired[
        KinesisVideoStreamSourceTaskConfigurationTypeDef
    ]
    ClientRequestToken: NotRequired[str]

class ListMediaCapturePipelinesResponseTypeDef(TypedDict):
    MediaCapturePipelines: List[MediaCapturePipelineSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListMediaInsightsPipelineConfigurationsResponseTypeDef(TypedDict):
    MediaInsightsPipelineConfigurations: List[MediaInsightsPipelineConfigurationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListMediaPipelinesResponseTypeDef(TypedDict):
    MediaPipelines: List[MediaPipelineSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class LiveConnectorSinkConfigurationTypeDef(TypedDict):
    SinkType: Literal["RTMP"]
    RTMPConfiguration: LiveConnectorRTMPConfigurationTypeDef

RealTimeAlertRuleOutputTypeDef = TypedDict(
    "RealTimeAlertRuleOutputTypeDef",
    {
        "Type": RealTimeAlertRuleTypeType,
        "KeywordMatchConfiguration": NotRequired[KeywordMatchConfigurationOutputTypeDef],
        "SentimentConfiguration": NotRequired[SentimentConfigurationTypeDef],
        "IssueDetectionConfiguration": NotRequired[IssueDetectionConfigurationTypeDef],
    },
)

class SourceConfigurationOutputTypeDef(TypedDict):
    SelectedVideoStreams: NotRequired[SelectedVideoStreamsOutputTypeDef]

SelectedVideoStreamsUnionTypeDef = Union[
    SelectedVideoStreamsTypeDef, SelectedVideoStreamsOutputTypeDef
]

class TimestampRangeTypeDef(TypedDict):
    StartTimestamp: TimestampTypeDef
    EndTimestamp: TimestampTypeDef

MediaInsightsPipelineConfigurationElementOutputTypeDef = TypedDict(
    "MediaInsightsPipelineConfigurationElementOutputTypeDef",
    {
        "Type": MediaInsightsPipelineConfigurationElementTypeType,
        "AmazonTranscribeCallAnalyticsProcessorConfiguration": NotRequired[
            AmazonTranscribeCallAnalyticsProcessorConfigurationOutputTypeDef
        ],
        "AmazonTranscribeProcessorConfiguration": NotRequired[
            AmazonTranscribeProcessorConfigurationTypeDef
        ],
        "KinesisDataStreamSinkConfiguration": NotRequired[
            KinesisDataStreamSinkConfigurationTypeDef
        ],
        "S3RecordingSinkConfiguration": NotRequired[S3RecordingSinkConfigurationTypeDef],
        "VoiceAnalyticsProcessorConfiguration": NotRequired[
            VoiceAnalyticsProcessorConfigurationTypeDef
        ],
        "LambdaFunctionSinkConfiguration": NotRequired[LambdaFunctionSinkConfigurationTypeDef],
        "SqsQueueSinkConfiguration": NotRequired[SqsQueueSinkConfigurationTypeDef],
        "SnsTopicSinkConfiguration": NotRequired[SnsTopicSinkConfigurationTypeDef],
        "VoiceEnhancementSinkConfiguration": NotRequired[VoiceEnhancementSinkConfigurationTypeDef],
    },
)
AmazonTranscribeCallAnalyticsProcessorConfigurationUnionTypeDef = Union[
    AmazonTranscribeCallAnalyticsProcessorConfigurationTypeDef,
    AmazonTranscribeCallAnalyticsProcessorConfigurationOutputTypeDef,
]

class ChimeSdkMeetingConcatenationConfigurationTypeDef(TypedDict):
    ArtifactsConfiguration: ArtifactsConcatenationConfigurationTypeDef

class StreamConfigurationOutputTypeDef(TypedDict):
    StreamArn: str
    StreamChannelDefinition: StreamChannelDefinitionOutputTypeDef
    FragmentNumber: NotRequired[str]

StreamChannelDefinitionUnionTypeDef = Union[
    StreamChannelDefinitionTypeDef, StreamChannelDefinitionOutputTypeDef
]

class CreateMediaPipelineKinesisVideoStreamPoolResponseTypeDef(TypedDict):
    KinesisVideoStreamPoolConfiguration: KinesisVideoStreamPoolConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetMediaPipelineKinesisVideoStreamPoolResponseTypeDef(TypedDict):
    KinesisVideoStreamPoolConfiguration: KinesisVideoStreamPoolConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateMediaPipelineKinesisVideoStreamPoolResponseTypeDef(TypedDict):
    KinesisVideoStreamPoolConfiguration: KinesisVideoStreamPoolConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMediaStreamPipelineResponseTypeDef(TypedDict):
    MediaStreamPipeline: MediaStreamPipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class KinesisVideoStreamRecordingSourceRuntimeConfigurationOutputTypeDef(TypedDict):
    Streams: List[RecordingStreamConfigurationTypeDef]
    FragmentSelector: FragmentSelectorOutputTypeDef

class CompositedVideoArtifactsConfigurationTypeDef(TypedDict):
    GridViewConfiguration: GridViewConfigurationTypeDef
    Layout: NotRequired[Literal["GridView"]]
    Resolution: NotRequired[ResolutionOptionType]

RealTimeAlertRuleTypeDef = TypedDict(
    "RealTimeAlertRuleTypeDef",
    {
        "Type": RealTimeAlertRuleTypeType,
        "KeywordMatchConfiguration": NotRequired[KeywordMatchConfigurationUnionTypeDef],
        "SentimentConfiguration": NotRequired[SentimentConfigurationTypeDef],
        "IssueDetectionConfiguration": NotRequired[IssueDetectionConfigurationTypeDef],
    },
)

class RealTimeAlertConfigurationOutputTypeDef(TypedDict):
    Disabled: NotRequired[bool]
    Rules: NotRequired[List[RealTimeAlertRuleOutputTypeDef]]

class SourceConfigurationTypeDef(TypedDict):
    SelectedVideoStreams: NotRequired[SelectedVideoStreamsUnionTypeDef]

TimestampRangeUnionTypeDef = Union[TimestampRangeTypeDef, TimestampRangeOutputTypeDef]
MediaInsightsPipelineConfigurationElementTypeDef = TypedDict(
    "MediaInsightsPipelineConfigurationElementTypeDef",
    {
        "Type": MediaInsightsPipelineConfigurationElementTypeType,
        "AmazonTranscribeCallAnalyticsProcessorConfiguration": NotRequired[
            AmazonTranscribeCallAnalyticsProcessorConfigurationUnionTypeDef
        ],
        "AmazonTranscribeProcessorConfiguration": NotRequired[
            AmazonTranscribeProcessorConfigurationTypeDef
        ],
        "KinesisDataStreamSinkConfiguration": NotRequired[
            KinesisDataStreamSinkConfigurationTypeDef
        ],
        "S3RecordingSinkConfiguration": NotRequired[S3RecordingSinkConfigurationTypeDef],
        "VoiceAnalyticsProcessorConfiguration": NotRequired[
            VoiceAnalyticsProcessorConfigurationTypeDef
        ],
        "LambdaFunctionSinkConfiguration": NotRequired[LambdaFunctionSinkConfigurationTypeDef],
        "SqsQueueSinkConfiguration": NotRequired[SqsQueueSinkConfigurationTypeDef],
        "SnsTopicSinkConfiguration": NotRequired[SnsTopicSinkConfigurationTypeDef],
        "VoiceEnhancementSinkConfiguration": NotRequired[VoiceEnhancementSinkConfigurationTypeDef],
    },
)

class MediaCapturePipelineSourceConfigurationTypeDef(TypedDict):
    MediaPipelineArn: str
    ChimeSdkMeetingConfiguration: ChimeSdkMeetingConcatenationConfigurationTypeDef

class KinesisVideoStreamSourceRuntimeConfigurationOutputTypeDef(TypedDict):
    Streams: List[StreamConfigurationOutputTypeDef]
    MediaEncoding: Literal["pcm"]
    MediaSampleRate: int

class StreamConfigurationTypeDef(TypedDict):
    StreamArn: str
    StreamChannelDefinition: StreamChannelDefinitionUnionTypeDef
    FragmentNumber: NotRequired[str]

class ArtifactsConfigurationTypeDef(TypedDict):
    Audio: AudioArtifactsConfigurationTypeDef
    Video: VideoArtifactsConfigurationTypeDef
    Content: ContentArtifactsConfigurationTypeDef
    CompositedVideo: NotRequired[CompositedVideoArtifactsConfigurationTypeDef]

class ChimeSdkMeetingLiveConnectorConfigurationOutputTypeDef(TypedDict):
    Arn: str
    MuxType: LiveConnectorMuxTypeType
    CompositedVideo: NotRequired[CompositedVideoArtifactsConfigurationTypeDef]
    SourceConfiguration: NotRequired[SourceConfigurationOutputTypeDef]

RealTimeAlertRuleUnionTypeDef = Union[RealTimeAlertRuleTypeDef, RealTimeAlertRuleOutputTypeDef]

class MediaInsightsPipelineConfigurationTypeDef(TypedDict):
    MediaInsightsPipelineConfigurationName: NotRequired[str]
    MediaInsightsPipelineConfigurationArn: NotRequired[str]
    ResourceAccessRoleArn: NotRequired[str]
    RealTimeAlertConfiguration: NotRequired[RealTimeAlertConfigurationOutputTypeDef]
    Elements: NotRequired[List[MediaInsightsPipelineConfigurationElementOutputTypeDef]]
    MediaInsightsPipelineConfigurationId: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]

SourceConfigurationUnionTypeDef = Union[
    SourceConfigurationTypeDef, SourceConfigurationOutputTypeDef
]

class FragmentSelectorTypeDef(TypedDict):
    FragmentSelectorType: FragmentSelectorTypeType
    TimestampRange: TimestampRangeUnionTypeDef

MediaInsightsPipelineConfigurationElementUnionTypeDef = Union[
    MediaInsightsPipelineConfigurationElementTypeDef,
    MediaInsightsPipelineConfigurationElementOutputTypeDef,
]
ConcatenationSourceTypeDef = TypedDict(
    "ConcatenationSourceTypeDef",
    {
        "Type": Literal["MediaCapturePipeline"],
        "MediaCapturePipelineSourceConfiguration": MediaCapturePipelineSourceConfigurationTypeDef,
    },
)

class MediaInsightsPipelineTypeDef(TypedDict):
    MediaPipelineId: NotRequired[str]
    MediaPipelineArn: NotRequired[str]
    MediaInsightsPipelineConfigurationArn: NotRequired[str]
    Status: NotRequired[MediaPipelineStatusType]
    KinesisVideoStreamSourceRuntimeConfiguration: NotRequired[
        KinesisVideoStreamSourceRuntimeConfigurationOutputTypeDef
    ]
    MediaInsightsRuntimeMetadata: NotRequired[Dict[str, str]]
    KinesisVideoStreamRecordingSourceRuntimeConfiguration: NotRequired[
        KinesisVideoStreamRecordingSourceRuntimeConfigurationOutputTypeDef
    ]
    S3RecordingSinkRuntimeConfiguration: NotRequired[S3RecordingSinkRuntimeConfigurationTypeDef]
    CreatedTimestamp: NotRequired[datetime]
    ElementStatuses: NotRequired[List[MediaInsightsPipelineElementStatusTypeDef]]

StreamConfigurationUnionTypeDef = Union[
    StreamConfigurationTypeDef, StreamConfigurationOutputTypeDef
]

class ChimeSdkMeetingConfigurationOutputTypeDef(TypedDict):
    SourceConfiguration: NotRequired[SourceConfigurationOutputTypeDef]
    ArtifactsConfiguration: NotRequired[ArtifactsConfigurationTypeDef]

class LiveConnectorSourceConfigurationOutputTypeDef(TypedDict):
    SourceType: Literal["ChimeSdkMeeting"]
    ChimeSdkMeetingLiveConnectorConfiguration: (
        ChimeSdkMeetingLiveConnectorConfigurationOutputTypeDef
    )

class RealTimeAlertConfigurationTypeDef(TypedDict):
    Disabled: NotRequired[bool]
    Rules: NotRequired[Sequence[RealTimeAlertRuleUnionTypeDef]]

class CreateMediaInsightsPipelineConfigurationResponseTypeDef(TypedDict):
    MediaInsightsPipelineConfiguration: MediaInsightsPipelineConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetMediaInsightsPipelineConfigurationResponseTypeDef(TypedDict):
    MediaInsightsPipelineConfiguration: MediaInsightsPipelineConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateMediaInsightsPipelineConfigurationResponseTypeDef(TypedDict):
    MediaInsightsPipelineConfiguration: MediaInsightsPipelineConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ChimeSdkMeetingConfigurationTypeDef(TypedDict):
    SourceConfiguration: NotRequired[SourceConfigurationUnionTypeDef]
    ArtifactsConfiguration: NotRequired[ArtifactsConfigurationTypeDef]

class ChimeSdkMeetingLiveConnectorConfigurationTypeDef(TypedDict):
    Arn: str
    MuxType: LiveConnectorMuxTypeType
    CompositedVideo: NotRequired[CompositedVideoArtifactsConfigurationTypeDef]
    SourceConfiguration: NotRequired[SourceConfigurationUnionTypeDef]

FragmentSelectorUnionTypeDef = Union[FragmentSelectorTypeDef, FragmentSelectorOutputTypeDef]

class CreateMediaConcatenationPipelineRequestRequestTypeDef(TypedDict):
    Sources: Sequence[ConcatenationSourceTypeDef]
    Sinks: Sequence[ConcatenationSinkTypeDef]
    ClientRequestToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class MediaConcatenationPipelineTypeDef(TypedDict):
    MediaPipelineId: NotRequired[str]
    MediaPipelineArn: NotRequired[str]
    Sources: NotRequired[List[ConcatenationSourceTypeDef]]
    Sinks: NotRequired[List[ConcatenationSinkTypeDef]]
    Status: NotRequired[MediaPipelineStatusType]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]

class CreateMediaInsightsPipelineResponseTypeDef(TypedDict):
    MediaInsightsPipeline: MediaInsightsPipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class KinesisVideoStreamSourceRuntimeConfigurationTypeDef(TypedDict):
    Streams: Sequence[StreamConfigurationUnionTypeDef]
    MediaEncoding: Literal["pcm"]
    MediaSampleRate: int

class MediaCapturePipelineTypeDef(TypedDict):
    MediaPipelineId: NotRequired[str]
    MediaPipelineArn: NotRequired[str]
    SourceType: NotRequired[Literal["ChimeSdkMeeting"]]
    SourceArn: NotRequired[str]
    Status: NotRequired[MediaPipelineStatusType]
    SinkType: NotRequired[Literal["S3Bucket"]]
    SinkArn: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]
    ChimeSdkMeetingConfiguration: NotRequired[ChimeSdkMeetingConfigurationOutputTypeDef]
    SseAwsKeyManagementParams: NotRequired[SseAwsKeyManagementParamsTypeDef]
    SinkIamRoleArn: NotRequired[str]

class MediaLiveConnectorPipelineTypeDef(TypedDict):
    Sources: NotRequired[List[LiveConnectorSourceConfigurationOutputTypeDef]]
    Sinks: NotRequired[List[LiveConnectorSinkConfigurationTypeDef]]
    MediaPipelineId: NotRequired[str]
    MediaPipelineArn: NotRequired[str]
    Status: NotRequired[MediaPipelineStatusType]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]

class CreateMediaInsightsPipelineConfigurationRequestRequestTypeDef(TypedDict):
    MediaInsightsPipelineConfigurationName: str
    ResourceAccessRoleArn: str
    Elements: Sequence[MediaInsightsPipelineConfigurationElementUnionTypeDef]
    RealTimeAlertConfiguration: NotRequired[RealTimeAlertConfigurationTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientRequestToken: NotRequired[str]

class UpdateMediaInsightsPipelineConfigurationRequestRequestTypeDef(TypedDict):
    Identifier: str
    ResourceAccessRoleArn: str
    Elements: Sequence[MediaInsightsPipelineConfigurationElementTypeDef]
    RealTimeAlertConfiguration: NotRequired[RealTimeAlertConfigurationTypeDef]

class CreateMediaCapturePipelineRequestRequestTypeDef(TypedDict):
    SourceType: Literal["ChimeSdkMeeting"]
    SourceArn: str
    SinkType: Literal["S3Bucket"]
    SinkArn: str
    ClientRequestToken: NotRequired[str]
    ChimeSdkMeetingConfiguration: NotRequired[ChimeSdkMeetingConfigurationTypeDef]
    SseAwsKeyManagementParams: NotRequired[SseAwsKeyManagementParamsTypeDef]
    SinkIamRoleArn: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

ChimeSdkMeetingLiveConnectorConfigurationUnionTypeDef = Union[
    ChimeSdkMeetingLiveConnectorConfigurationTypeDef,
    ChimeSdkMeetingLiveConnectorConfigurationOutputTypeDef,
]

class KinesisVideoStreamRecordingSourceRuntimeConfigurationTypeDef(TypedDict):
    Streams: Sequence[RecordingStreamConfigurationTypeDef]
    FragmentSelector: FragmentSelectorUnionTypeDef

class CreateMediaConcatenationPipelineResponseTypeDef(TypedDict):
    MediaConcatenationPipeline: MediaConcatenationPipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMediaCapturePipelineResponseTypeDef(TypedDict):
    MediaCapturePipeline: MediaCapturePipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetMediaCapturePipelineResponseTypeDef(TypedDict):
    MediaCapturePipeline: MediaCapturePipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMediaLiveConnectorPipelineResponseTypeDef(TypedDict):
    MediaLiveConnectorPipeline: MediaLiveConnectorPipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class MediaPipelineTypeDef(TypedDict):
    MediaCapturePipeline: NotRequired[MediaCapturePipelineTypeDef]
    MediaLiveConnectorPipeline: NotRequired[MediaLiveConnectorPipelineTypeDef]
    MediaConcatenationPipeline: NotRequired[MediaConcatenationPipelineTypeDef]
    MediaInsightsPipeline: NotRequired[MediaInsightsPipelineTypeDef]
    MediaStreamPipeline: NotRequired[MediaStreamPipelineTypeDef]

class LiveConnectorSourceConfigurationTypeDef(TypedDict):
    SourceType: Literal["ChimeSdkMeeting"]
    ChimeSdkMeetingLiveConnectorConfiguration: ChimeSdkMeetingLiveConnectorConfigurationUnionTypeDef

class CreateMediaInsightsPipelineRequestRequestTypeDef(TypedDict):
    MediaInsightsPipelineConfigurationArn: str
    KinesisVideoStreamSourceRuntimeConfiguration: NotRequired[
        KinesisVideoStreamSourceRuntimeConfigurationTypeDef
    ]
    MediaInsightsRuntimeMetadata: NotRequired[Mapping[str, str]]
    KinesisVideoStreamRecordingSourceRuntimeConfiguration: NotRequired[
        KinesisVideoStreamRecordingSourceRuntimeConfigurationTypeDef
    ]
    S3RecordingSinkRuntimeConfiguration: NotRequired[S3RecordingSinkRuntimeConfigurationTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientRequestToken: NotRequired[str]

class GetMediaPipelineResponseTypeDef(TypedDict):
    MediaPipeline: MediaPipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

LiveConnectorSourceConfigurationUnionTypeDef = Union[
    LiveConnectorSourceConfigurationTypeDef, LiveConnectorSourceConfigurationOutputTypeDef
]

class CreateMediaLiveConnectorPipelineRequestRequestTypeDef(TypedDict):
    Sources: Sequence[LiveConnectorSourceConfigurationUnionTypeDef]
    Sinks: Sequence[LiveConnectorSinkConfigurationTypeDef]
    ClientRequestToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
