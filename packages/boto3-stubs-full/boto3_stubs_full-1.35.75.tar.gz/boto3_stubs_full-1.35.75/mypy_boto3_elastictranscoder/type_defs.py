"""
Type annotations for elastictranscoder service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/type_defs/)

Usage::

    ```python
    from mypy_boto3_elastictranscoder.type_defs import EncryptionTypeDef

    data: EncryptionTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Mapping, Sequence, Union

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "ArtworkTypeDef",
    "AudioCodecOptionsTypeDef",
    "AudioParametersTypeDef",
    "CancelJobRequestRequestTypeDef",
    "CaptionFormatTypeDef",
    "CaptionSourceTypeDef",
    "CaptionsOutputTypeDef",
    "CaptionsTypeDef",
    "CaptionsUnionTypeDef",
    "ClipTypeDef",
    "CreateJobOutputTypeDef",
    "CreateJobPlaylistTypeDef",
    "CreateJobRequestRequestTypeDef",
    "CreateJobResponseTypeDef",
    "CreatePipelineRequestRequestTypeDef",
    "CreatePipelineResponseTypeDef",
    "CreatePresetRequestRequestTypeDef",
    "CreatePresetResponseTypeDef",
    "DeletePipelineRequestRequestTypeDef",
    "DeletePresetRequestRequestTypeDef",
    "DetectedPropertiesTypeDef",
    "EncryptionTypeDef",
    "HlsContentProtectionTypeDef",
    "InputCaptionsOutputTypeDef",
    "InputCaptionsTypeDef",
    "InputCaptionsUnionTypeDef",
    "JobAlbumArtOutputTypeDef",
    "JobAlbumArtTypeDef",
    "JobAlbumArtUnionTypeDef",
    "JobInputOutputTypeDef",
    "JobInputTypeDef",
    "JobInputUnionTypeDef",
    "JobOutputTypeDef",
    "JobTypeDef",
    "JobWatermarkTypeDef",
    "ListJobsByPipelineRequestListJobsByPipelinePaginateTypeDef",
    "ListJobsByPipelineRequestRequestTypeDef",
    "ListJobsByPipelineResponseTypeDef",
    "ListJobsByStatusRequestListJobsByStatusPaginateTypeDef",
    "ListJobsByStatusRequestRequestTypeDef",
    "ListJobsByStatusResponseTypeDef",
    "ListPipelinesRequestListPipelinesPaginateTypeDef",
    "ListPipelinesRequestRequestTypeDef",
    "ListPipelinesResponseTypeDef",
    "ListPresetsRequestListPresetsPaginateTypeDef",
    "ListPresetsRequestRequestTypeDef",
    "ListPresetsResponseTypeDef",
    "NotificationsTypeDef",
    "PaginatorConfigTypeDef",
    "PermissionOutputTypeDef",
    "PermissionTypeDef",
    "PermissionUnionTypeDef",
    "PipelineOutputConfigOutputTypeDef",
    "PipelineOutputConfigTypeDef",
    "PipelineTypeDef",
    "PlayReadyDrmTypeDef",
    "PlaylistTypeDef",
    "PresetTypeDef",
    "PresetWatermarkTypeDef",
    "ReadJobRequestJobCompleteWaitTypeDef",
    "ReadJobRequestRequestTypeDef",
    "ReadJobResponseTypeDef",
    "ReadPipelineRequestRequestTypeDef",
    "ReadPipelineResponseTypeDef",
    "ReadPresetRequestRequestTypeDef",
    "ReadPresetResponseTypeDef",
    "ResponseMetadataTypeDef",
    "TestRoleRequestRequestTypeDef",
    "TestRoleResponseTypeDef",
    "ThumbnailsTypeDef",
    "TimeSpanTypeDef",
    "TimingTypeDef",
    "UpdatePipelineNotificationsRequestRequestTypeDef",
    "UpdatePipelineNotificationsResponseTypeDef",
    "UpdatePipelineRequestRequestTypeDef",
    "UpdatePipelineResponseTypeDef",
    "UpdatePipelineStatusRequestRequestTypeDef",
    "UpdatePipelineStatusResponseTypeDef",
    "VideoParametersOutputTypeDef",
    "VideoParametersTypeDef",
    "WaiterConfigTypeDef",
    "WarningTypeDef",
)


class EncryptionTypeDef(TypedDict):
    Mode: NotRequired[str]
    Key: NotRequired[str]
    KeyMd5: NotRequired[str]
    InitializationVector: NotRequired[str]


class AudioCodecOptionsTypeDef(TypedDict):
    Profile: NotRequired[str]
    BitDepth: NotRequired[str]
    BitOrder: NotRequired[str]
    Signed: NotRequired[str]


class CancelJobRequestRequestTypeDef(TypedDict):
    Id: str


class TimeSpanTypeDef(TypedDict):
    StartTime: NotRequired[str]
    Duration: NotRequired[str]


class HlsContentProtectionTypeDef(TypedDict):
    Method: NotRequired[str]
    Key: NotRequired[str]
    KeyMd5: NotRequired[str]
    InitializationVector: NotRequired[str]
    LicenseAcquisitionUrl: NotRequired[str]
    KeyStoragePolicy: NotRequired[str]


class PlayReadyDrmTypeDef(TypedDict):
    Format: NotRequired[str]
    Key: NotRequired[str]
    KeyMd5: NotRequired[str]
    KeyId: NotRequired[str]
    InitializationVector: NotRequired[str]
    LicenseAcquisitionUrl: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


NotificationsTypeDef = TypedDict(
    "NotificationsTypeDef",
    {
        "Progressing": NotRequired[str],
        "Completed": NotRequired[str],
        "Warning": NotRequired[str],
        "Error": NotRequired[str],
    },
)


class WarningTypeDef(TypedDict):
    Code: NotRequired[str]
    Message: NotRequired[str]


class ThumbnailsTypeDef(TypedDict):
    Format: NotRequired[str]
    Interval: NotRequired[str]
    Resolution: NotRequired[str]
    AspectRatio: NotRequired[str]
    MaxWidth: NotRequired[str]
    MaxHeight: NotRequired[str]
    SizingPolicy: NotRequired[str]
    PaddingPolicy: NotRequired[str]


class DeletePipelineRequestRequestTypeDef(TypedDict):
    Id: str


class DeletePresetRequestRequestTypeDef(TypedDict):
    Id: str


class DetectedPropertiesTypeDef(TypedDict):
    Width: NotRequired[int]
    Height: NotRequired[int]
    FrameRate: NotRequired[str]
    FileSize: NotRequired[int]
    DurationMillis: NotRequired[int]


class TimingTypeDef(TypedDict):
    SubmitTimeMillis: NotRequired[int]
    StartTimeMillis: NotRequired[int]
    FinishTimeMillis: NotRequired[int]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListJobsByPipelineRequestRequestTypeDef(TypedDict):
    PipelineId: str
    Ascending: NotRequired[str]
    PageToken: NotRequired[str]


class ListJobsByStatusRequestRequestTypeDef(TypedDict):
    Status: str
    Ascending: NotRequired[str]
    PageToken: NotRequired[str]


class ListPipelinesRequestRequestTypeDef(TypedDict):
    Ascending: NotRequired[str]
    PageToken: NotRequired[str]


class ListPresetsRequestRequestTypeDef(TypedDict):
    Ascending: NotRequired[str]
    PageToken: NotRequired[str]


class PermissionOutputTypeDef(TypedDict):
    GranteeType: NotRequired[str]
    Grantee: NotRequired[str]
    Access: NotRequired[List[str]]


class PermissionTypeDef(TypedDict):
    GranteeType: NotRequired[str]
    Grantee: NotRequired[str]
    Access: NotRequired[Sequence[str]]


class PresetWatermarkTypeDef(TypedDict):
    Id: NotRequired[str]
    MaxWidth: NotRequired[str]
    MaxHeight: NotRequired[str]
    SizingPolicy: NotRequired[str]
    HorizontalAlign: NotRequired[str]
    HorizontalOffset: NotRequired[str]
    VerticalAlign: NotRequired[str]
    VerticalOffset: NotRequired[str]
    Opacity: NotRequired[str]
    Target: NotRequired[str]


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class ReadJobRequestRequestTypeDef(TypedDict):
    Id: str


class ReadPipelineRequestRequestTypeDef(TypedDict):
    Id: str


class ReadPresetRequestRequestTypeDef(TypedDict):
    Id: str


class TestRoleRequestRequestTypeDef(TypedDict):
    Role: str
    InputBucket: str
    OutputBucket: str
    Topics: Sequence[str]


class UpdatePipelineStatusRequestRequestTypeDef(TypedDict):
    Id: str
    Status: str


class ArtworkTypeDef(TypedDict):
    InputKey: NotRequired[str]
    MaxWidth: NotRequired[str]
    MaxHeight: NotRequired[str]
    SizingPolicy: NotRequired[str]
    PaddingPolicy: NotRequired[str]
    AlbumArtFormat: NotRequired[str]
    Encryption: NotRequired[EncryptionTypeDef]


class CaptionFormatTypeDef(TypedDict):
    Format: NotRequired[str]
    Pattern: NotRequired[str]
    Encryption: NotRequired[EncryptionTypeDef]


class CaptionSourceTypeDef(TypedDict):
    Key: NotRequired[str]
    Language: NotRequired[str]
    TimeOffset: NotRequired[str]
    Label: NotRequired[str]
    Encryption: NotRequired[EncryptionTypeDef]


class JobWatermarkTypeDef(TypedDict):
    PresetWatermarkId: NotRequired[str]
    InputKey: NotRequired[str]
    Encryption: NotRequired[EncryptionTypeDef]


class AudioParametersTypeDef(TypedDict):
    Codec: NotRequired[str]
    SampleRate: NotRequired[str]
    BitRate: NotRequired[str]
    Channels: NotRequired[str]
    AudioPackingMode: NotRequired[str]
    CodecOptions: NotRequired[AudioCodecOptionsTypeDef]


class ClipTypeDef(TypedDict):
    TimeSpan: NotRequired[TimeSpanTypeDef]


class CreateJobPlaylistTypeDef(TypedDict):
    Name: NotRequired[str]
    Format: NotRequired[str]
    OutputKeys: NotRequired[Sequence[str]]
    HlsContentProtection: NotRequired[HlsContentProtectionTypeDef]
    PlayReadyDrm: NotRequired[PlayReadyDrmTypeDef]


class PlaylistTypeDef(TypedDict):
    Name: NotRequired[str]
    Format: NotRequired[str]
    OutputKeys: NotRequired[List[str]]
    HlsContentProtection: NotRequired[HlsContentProtectionTypeDef]
    PlayReadyDrm: NotRequired[PlayReadyDrmTypeDef]
    Status: NotRequired[str]
    StatusDetail: NotRequired[str]


class TestRoleResponseTypeDef(TypedDict):
    Success: str
    Messages: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePipelineNotificationsRequestRequestTypeDef(TypedDict):
    Id: str
    Notifications: NotificationsTypeDef


class ListJobsByPipelineRequestListJobsByPipelinePaginateTypeDef(TypedDict):
    PipelineId: str
    Ascending: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListJobsByStatusRequestListJobsByStatusPaginateTypeDef(TypedDict):
    Status: str
    Ascending: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPipelinesRequestListPipelinesPaginateTypeDef(TypedDict):
    Ascending: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPresetsRequestListPresetsPaginateTypeDef(TypedDict):
    Ascending: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class PipelineOutputConfigOutputTypeDef(TypedDict):
    Bucket: NotRequired[str]
    StorageClass: NotRequired[str]
    Permissions: NotRequired[List[PermissionOutputTypeDef]]


PermissionUnionTypeDef = Union[PermissionTypeDef, PermissionOutputTypeDef]


class VideoParametersOutputTypeDef(TypedDict):
    Codec: NotRequired[str]
    CodecOptions: NotRequired[Dict[str, str]]
    KeyframesMaxDist: NotRequired[str]
    FixedGOP: NotRequired[str]
    BitRate: NotRequired[str]
    FrameRate: NotRequired[str]
    MaxFrameRate: NotRequired[str]
    Resolution: NotRequired[str]
    AspectRatio: NotRequired[str]
    MaxWidth: NotRequired[str]
    MaxHeight: NotRequired[str]
    DisplayAspectRatio: NotRequired[str]
    SizingPolicy: NotRequired[str]
    PaddingPolicy: NotRequired[str]
    Watermarks: NotRequired[List[PresetWatermarkTypeDef]]


class VideoParametersTypeDef(TypedDict):
    Codec: NotRequired[str]
    CodecOptions: NotRequired[Mapping[str, str]]
    KeyframesMaxDist: NotRequired[str]
    FixedGOP: NotRequired[str]
    BitRate: NotRequired[str]
    FrameRate: NotRequired[str]
    MaxFrameRate: NotRequired[str]
    Resolution: NotRequired[str]
    AspectRatio: NotRequired[str]
    MaxWidth: NotRequired[str]
    MaxHeight: NotRequired[str]
    DisplayAspectRatio: NotRequired[str]
    SizingPolicy: NotRequired[str]
    PaddingPolicy: NotRequired[str]
    Watermarks: NotRequired[Sequence[PresetWatermarkTypeDef]]


class ReadJobRequestJobCompleteWaitTypeDef(TypedDict):
    Id: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class JobAlbumArtOutputTypeDef(TypedDict):
    MergePolicy: NotRequired[str]
    Artwork: NotRequired[List[ArtworkTypeDef]]


class JobAlbumArtTypeDef(TypedDict):
    MergePolicy: NotRequired[str]
    Artwork: NotRequired[Sequence[ArtworkTypeDef]]


class CaptionsOutputTypeDef(TypedDict):
    MergePolicy: NotRequired[str]
    CaptionSources: NotRequired[List[CaptionSourceTypeDef]]
    CaptionFormats: NotRequired[List[CaptionFormatTypeDef]]


class CaptionsTypeDef(TypedDict):
    MergePolicy: NotRequired[str]
    CaptionSources: NotRequired[Sequence[CaptionSourceTypeDef]]
    CaptionFormats: NotRequired[Sequence[CaptionFormatTypeDef]]


class InputCaptionsOutputTypeDef(TypedDict):
    MergePolicy: NotRequired[str]
    CaptionSources: NotRequired[List[CaptionSourceTypeDef]]


class InputCaptionsTypeDef(TypedDict):
    MergePolicy: NotRequired[str]
    CaptionSources: NotRequired[Sequence[CaptionSourceTypeDef]]


class PipelineTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[str]
    InputBucket: NotRequired[str]
    OutputBucket: NotRequired[str]
    Role: NotRequired[str]
    AwsKmsKeyArn: NotRequired[str]
    Notifications: NotRequired[NotificationsTypeDef]
    ContentConfig: NotRequired[PipelineOutputConfigOutputTypeDef]
    ThumbnailConfig: NotRequired[PipelineOutputConfigOutputTypeDef]


class PipelineOutputConfigTypeDef(TypedDict):
    Bucket: NotRequired[str]
    StorageClass: NotRequired[str]
    Permissions: NotRequired[Sequence[PermissionUnionTypeDef]]


PresetTypeDef = TypedDict(
    "PresetTypeDef",
    {
        "Id": NotRequired[str],
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "Container": NotRequired[str],
        "Audio": NotRequired[AudioParametersTypeDef],
        "Video": NotRequired[VideoParametersOutputTypeDef],
        "Thumbnails": NotRequired[ThumbnailsTypeDef],
        "Type": NotRequired[str],
    },
)
CreatePresetRequestRequestTypeDef = TypedDict(
    "CreatePresetRequestRequestTypeDef",
    {
        "Name": str,
        "Container": str,
        "Description": NotRequired[str],
        "Video": NotRequired[VideoParametersTypeDef],
        "Audio": NotRequired[AudioParametersTypeDef],
        "Thumbnails": NotRequired[ThumbnailsTypeDef],
    },
)
JobAlbumArtUnionTypeDef = Union[JobAlbumArtTypeDef, JobAlbumArtOutputTypeDef]


class JobOutputTypeDef(TypedDict):
    Id: NotRequired[str]
    Key: NotRequired[str]
    ThumbnailPattern: NotRequired[str]
    ThumbnailEncryption: NotRequired[EncryptionTypeDef]
    Rotate: NotRequired[str]
    PresetId: NotRequired[str]
    SegmentDuration: NotRequired[str]
    Status: NotRequired[str]
    StatusDetail: NotRequired[str]
    Duration: NotRequired[int]
    Width: NotRequired[int]
    Height: NotRequired[int]
    FrameRate: NotRequired[str]
    FileSize: NotRequired[int]
    DurationMillis: NotRequired[int]
    Watermarks: NotRequired[List[JobWatermarkTypeDef]]
    AlbumArt: NotRequired[JobAlbumArtOutputTypeDef]
    Composition: NotRequired[List[ClipTypeDef]]
    Captions: NotRequired[CaptionsOutputTypeDef]
    Encryption: NotRequired[EncryptionTypeDef]
    AppliedColorSpaceConversion: NotRequired[str]


CaptionsUnionTypeDef = Union[CaptionsTypeDef, CaptionsOutputTypeDef]
JobInputOutputTypeDef = TypedDict(
    "JobInputOutputTypeDef",
    {
        "Key": NotRequired[str],
        "FrameRate": NotRequired[str],
        "Resolution": NotRequired[str],
        "AspectRatio": NotRequired[str],
        "Interlaced": NotRequired[str],
        "Container": NotRequired[str],
        "Encryption": NotRequired[EncryptionTypeDef],
        "TimeSpan": NotRequired[TimeSpanTypeDef],
        "InputCaptions": NotRequired[InputCaptionsOutputTypeDef],
        "DetectedProperties": NotRequired[DetectedPropertiesTypeDef],
    },
)
InputCaptionsUnionTypeDef = Union[InputCaptionsTypeDef, InputCaptionsOutputTypeDef]


class CreatePipelineResponseTypeDef(TypedDict):
    Pipeline: PipelineTypeDef
    Warnings: List[WarningTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListPipelinesResponseTypeDef(TypedDict):
    Pipelines: List[PipelineTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class ReadPipelineResponseTypeDef(TypedDict):
    Pipeline: PipelineTypeDef
    Warnings: List[WarningTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePipelineNotificationsResponseTypeDef(TypedDict):
    Pipeline: PipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePipelineResponseTypeDef(TypedDict):
    Pipeline: PipelineTypeDef
    Warnings: List[WarningTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePipelineStatusResponseTypeDef(TypedDict):
    Pipeline: PipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePipelineRequestRequestTypeDef(TypedDict):
    Name: str
    InputBucket: str
    Role: str
    OutputBucket: NotRequired[str]
    AwsKmsKeyArn: NotRequired[str]
    Notifications: NotRequired[NotificationsTypeDef]
    ContentConfig: NotRequired[PipelineOutputConfigTypeDef]
    ThumbnailConfig: NotRequired[PipelineOutputConfigTypeDef]


class UpdatePipelineRequestRequestTypeDef(TypedDict):
    Id: str
    Name: NotRequired[str]
    InputBucket: NotRequired[str]
    Role: NotRequired[str]
    AwsKmsKeyArn: NotRequired[str]
    Notifications: NotRequired[NotificationsTypeDef]
    ContentConfig: NotRequired[PipelineOutputConfigTypeDef]
    ThumbnailConfig: NotRequired[PipelineOutputConfigTypeDef]


CreatePresetResponseTypeDef = TypedDict(
    "CreatePresetResponseTypeDef",
    {
        "Preset": PresetTypeDef,
        "Warning": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ListPresetsResponseTypeDef(TypedDict):
    Presets: List[PresetTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class ReadPresetResponseTypeDef(TypedDict):
    Preset: PresetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateJobOutputTypeDef(TypedDict):
    Key: NotRequired[str]
    ThumbnailPattern: NotRequired[str]
    ThumbnailEncryption: NotRequired[EncryptionTypeDef]
    Rotate: NotRequired[str]
    PresetId: NotRequired[str]
    SegmentDuration: NotRequired[str]
    Watermarks: NotRequired[Sequence[JobWatermarkTypeDef]]
    AlbumArt: NotRequired[JobAlbumArtUnionTypeDef]
    Composition: NotRequired[Sequence[ClipTypeDef]]
    Captions: NotRequired[CaptionsUnionTypeDef]
    Encryption: NotRequired[EncryptionTypeDef]


class JobTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    PipelineId: NotRequired[str]
    Input: NotRequired[JobInputOutputTypeDef]
    Inputs: NotRequired[List[JobInputOutputTypeDef]]
    Output: NotRequired[JobOutputTypeDef]
    Outputs: NotRequired[List[JobOutputTypeDef]]
    OutputKeyPrefix: NotRequired[str]
    Playlists: NotRequired[List[PlaylistTypeDef]]
    Status: NotRequired[str]
    UserMetadata: NotRequired[Dict[str, str]]
    Timing: NotRequired[TimingTypeDef]


JobInputTypeDef = TypedDict(
    "JobInputTypeDef",
    {
        "Key": NotRequired[str],
        "FrameRate": NotRequired[str],
        "Resolution": NotRequired[str],
        "AspectRatio": NotRequired[str],
        "Interlaced": NotRequired[str],
        "Container": NotRequired[str],
        "Encryption": NotRequired[EncryptionTypeDef],
        "TimeSpan": NotRequired[TimeSpanTypeDef],
        "InputCaptions": NotRequired[InputCaptionsUnionTypeDef],
        "DetectedProperties": NotRequired[DetectedPropertiesTypeDef],
    },
)


class CreateJobResponseTypeDef(TypedDict):
    Job: JobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListJobsByPipelineResponseTypeDef(TypedDict):
    Jobs: List[JobTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListJobsByStatusResponseTypeDef(TypedDict):
    Jobs: List[JobTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class ReadJobResponseTypeDef(TypedDict):
    Job: JobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


JobInputUnionTypeDef = Union[JobInputTypeDef, JobInputOutputTypeDef]


class CreateJobRequestRequestTypeDef(TypedDict):
    PipelineId: str
    Input: NotRequired[JobInputTypeDef]
    Inputs: NotRequired[Sequence[JobInputUnionTypeDef]]
    Output: NotRequired[CreateJobOutputTypeDef]
    Outputs: NotRequired[Sequence[CreateJobOutputTypeDef]]
    OutputKeyPrefix: NotRequired[str]
    Playlists: NotRequired[Sequence[CreateJobPlaylistTypeDef]]
    UserMetadata: NotRequired[Mapping[str, str]]
