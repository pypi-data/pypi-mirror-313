"""
Type annotations for kinesisvideo service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/type_defs/)

Usage::

    ```python
    from mypy_boto3_kinesisvideo.type_defs import SingleMasterConfigurationTypeDef

    data: SingleMasterConfigurationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    APINameType,
    ChannelProtocolType,
    ChannelRoleType,
    ChannelTypeType,
    ConfigurationStatusType,
    FormatType,
    ImageSelectorTypeType,
    MediaStorageConfigurationStatusType,
    MediaUriTypeType,
    RecorderStatusType,
    StatusType,
    StrategyOnFullSizeType,
    SyncStatusType,
    UpdateDataRetentionOperationType,
    UploaderStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ChannelInfoTypeDef",
    "ChannelNameConditionTypeDef",
    "CreateSignalingChannelInputRequestTypeDef",
    "CreateSignalingChannelOutputTypeDef",
    "CreateStreamInputRequestTypeDef",
    "CreateStreamOutputTypeDef",
    "DeleteEdgeConfigurationInputRequestTypeDef",
    "DeleteSignalingChannelInputRequestTypeDef",
    "DeleteStreamInputRequestTypeDef",
    "DeletionConfigTypeDef",
    "DescribeEdgeConfigurationInputRequestTypeDef",
    "DescribeEdgeConfigurationOutputTypeDef",
    "DescribeImageGenerationConfigurationInputRequestTypeDef",
    "DescribeImageGenerationConfigurationOutputTypeDef",
    "DescribeMappedResourceConfigurationInputDescribeMappedResourceConfigurationPaginateTypeDef",
    "DescribeMappedResourceConfigurationInputRequestTypeDef",
    "DescribeMappedResourceConfigurationOutputTypeDef",
    "DescribeMediaStorageConfigurationInputRequestTypeDef",
    "DescribeMediaStorageConfigurationOutputTypeDef",
    "DescribeNotificationConfigurationInputRequestTypeDef",
    "DescribeNotificationConfigurationOutputTypeDef",
    "DescribeSignalingChannelInputRequestTypeDef",
    "DescribeSignalingChannelOutputTypeDef",
    "DescribeStreamInputRequestTypeDef",
    "DescribeStreamOutputTypeDef",
    "EdgeAgentStatusTypeDef",
    "EdgeConfigTypeDef",
    "GetDataEndpointInputRequestTypeDef",
    "GetDataEndpointOutputTypeDef",
    "GetSignalingChannelEndpointInputRequestTypeDef",
    "GetSignalingChannelEndpointOutputTypeDef",
    "ImageGenerationConfigurationOutputTypeDef",
    "ImageGenerationConfigurationTypeDef",
    "ImageGenerationDestinationConfigTypeDef",
    "LastRecorderStatusTypeDef",
    "LastUploaderStatusTypeDef",
    "ListEdgeAgentConfigurationsEdgeConfigTypeDef",
    "ListEdgeAgentConfigurationsInputListEdgeAgentConfigurationsPaginateTypeDef",
    "ListEdgeAgentConfigurationsInputRequestTypeDef",
    "ListEdgeAgentConfigurationsOutputTypeDef",
    "ListSignalingChannelsInputListSignalingChannelsPaginateTypeDef",
    "ListSignalingChannelsInputRequestTypeDef",
    "ListSignalingChannelsOutputTypeDef",
    "ListStreamsInputListStreamsPaginateTypeDef",
    "ListStreamsInputRequestTypeDef",
    "ListStreamsOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListTagsForStreamInputRequestTypeDef",
    "ListTagsForStreamOutputTypeDef",
    "LocalSizeConfigTypeDef",
    "MappedResourceConfigurationListItemTypeDef",
    "MediaSourceConfigTypeDef",
    "MediaStorageConfigurationTypeDef",
    "NotificationConfigurationTypeDef",
    "NotificationDestinationConfigTypeDef",
    "PaginatorConfigTypeDef",
    "RecorderConfigTypeDef",
    "ResourceEndpointListItemTypeDef",
    "ResponseMetadataTypeDef",
    "ScheduleConfigTypeDef",
    "SingleMasterChannelEndpointConfigurationTypeDef",
    "SingleMasterConfigurationTypeDef",
    "StartEdgeConfigurationUpdateInputRequestTypeDef",
    "StartEdgeConfigurationUpdateOutputTypeDef",
    "StreamInfoTypeDef",
    "StreamNameConditionTypeDef",
    "TagResourceInputRequestTypeDef",
    "TagStreamInputRequestTypeDef",
    "TagTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UntagStreamInputRequestTypeDef",
    "UpdateDataRetentionInputRequestTypeDef",
    "UpdateImageGenerationConfigurationInputRequestTypeDef",
    "UpdateMediaStorageConfigurationInputRequestTypeDef",
    "UpdateNotificationConfigurationInputRequestTypeDef",
    "UpdateSignalingChannelInputRequestTypeDef",
    "UpdateStreamInputRequestTypeDef",
    "UploaderConfigTypeDef",
)


class SingleMasterConfigurationTypeDef(TypedDict):
    MessageTtlSeconds: NotRequired[int]


class ChannelNameConditionTypeDef(TypedDict):
    ComparisonOperator: NotRequired[Literal["BEGINS_WITH"]]
    ComparisonValue: NotRequired[str]


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateStreamInputRequestTypeDef(TypedDict):
    StreamName: str
    DeviceName: NotRequired[str]
    MediaType: NotRequired[str]
    KmsKeyId: NotRequired[str]
    DataRetentionInHours: NotRequired[int]
    Tags: NotRequired[Mapping[str, str]]


class DeleteEdgeConfigurationInputRequestTypeDef(TypedDict):
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]


class DeleteSignalingChannelInputRequestTypeDef(TypedDict):
    ChannelARN: str
    CurrentVersion: NotRequired[str]


class DeleteStreamInputRequestTypeDef(TypedDict):
    StreamARN: str
    CurrentVersion: NotRequired[str]


class LocalSizeConfigTypeDef(TypedDict):
    MaxLocalMediaSizeInMB: NotRequired[int]
    StrategyOnFullSize: NotRequired[StrategyOnFullSizeType]


class DescribeEdgeConfigurationInputRequestTypeDef(TypedDict):
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]


class DescribeImageGenerationConfigurationInputRequestTypeDef(TypedDict):
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeMappedResourceConfigurationInputRequestTypeDef(TypedDict):
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


MappedResourceConfigurationListItemTypeDef = TypedDict(
    "MappedResourceConfigurationListItemTypeDef",
    {
        "Type": NotRequired[str],
        "ARN": NotRequired[str],
    },
)


class DescribeMediaStorageConfigurationInputRequestTypeDef(TypedDict):
    ChannelName: NotRequired[str]
    ChannelARN: NotRequired[str]


class MediaStorageConfigurationTypeDef(TypedDict):
    Status: MediaStorageConfigurationStatusType
    StreamARN: NotRequired[str]


class DescribeNotificationConfigurationInputRequestTypeDef(TypedDict):
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]


class DescribeSignalingChannelInputRequestTypeDef(TypedDict):
    ChannelName: NotRequired[str]
    ChannelARN: NotRequired[str]


class DescribeStreamInputRequestTypeDef(TypedDict):
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]


class StreamInfoTypeDef(TypedDict):
    DeviceName: NotRequired[str]
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    MediaType: NotRequired[str]
    KmsKeyId: NotRequired[str]
    Version: NotRequired[str]
    Status: NotRequired[StatusType]
    CreationTime: NotRequired[datetime]
    DataRetentionInHours: NotRequired[int]


class LastRecorderStatusTypeDef(TypedDict):
    JobStatusDetails: NotRequired[str]
    LastCollectedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    RecorderStatus: NotRequired[RecorderStatusType]


class LastUploaderStatusTypeDef(TypedDict):
    JobStatusDetails: NotRequired[str]
    LastCollectedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    UploaderStatus: NotRequired[UploaderStatusType]


class GetDataEndpointInputRequestTypeDef(TypedDict):
    APIName: APINameType
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]


class SingleMasterChannelEndpointConfigurationTypeDef(TypedDict):
    Protocols: NotRequired[Sequence[ChannelProtocolType]]
    Role: NotRequired[ChannelRoleType]


ResourceEndpointListItemTypeDef = TypedDict(
    "ResourceEndpointListItemTypeDef",
    {
        "Protocol": NotRequired[ChannelProtocolType],
        "ResourceEndpoint": NotRequired[str],
    },
)


class ImageGenerationDestinationConfigTypeDef(TypedDict):
    Uri: str
    DestinationRegion: str


class ListEdgeAgentConfigurationsInputRequestTypeDef(TypedDict):
    HubDeviceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class StreamNameConditionTypeDef(TypedDict):
    ComparisonOperator: NotRequired[Literal["BEGINS_WITH"]]
    ComparisonValue: NotRequired[str]


class ListTagsForResourceInputRequestTypeDef(TypedDict):
    ResourceARN: str
    NextToken: NotRequired[str]


class ListTagsForStreamInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamName: NotRequired[str]


class MediaSourceConfigTypeDef(TypedDict):
    MediaUriSecretArn: str
    MediaUriType: MediaUriTypeType


class NotificationDestinationConfigTypeDef(TypedDict):
    Uri: str


class ScheduleConfigTypeDef(TypedDict):
    ScheduleExpression: str
    DurationInSeconds: int


class TagStreamInputRequestTypeDef(TypedDict):
    Tags: Mapping[str, str]
    StreamARN: NotRequired[str]
    StreamName: NotRequired[str]


class UntagResourceInputRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeyList: Sequence[str]


class UntagStreamInputRequestTypeDef(TypedDict):
    TagKeyList: Sequence[str]
    StreamARN: NotRequired[str]
    StreamName: NotRequired[str]


class UpdateDataRetentionInputRequestTypeDef(TypedDict):
    CurrentVersion: str
    Operation: UpdateDataRetentionOperationType
    DataRetentionChangeInHours: int
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]


class UpdateStreamInputRequestTypeDef(TypedDict):
    CurrentVersion: str
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    DeviceName: NotRequired[str]
    MediaType: NotRequired[str]


class ChannelInfoTypeDef(TypedDict):
    ChannelName: NotRequired[str]
    ChannelARN: NotRequired[str]
    ChannelType: NotRequired[ChannelTypeType]
    ChannelStatus: NotRequired[StatusType]
    CreationTime: NotRequired[datetime]
    SingleMasterConfiguration: NotRequired[SingleMasterConfigurationTypeDef]
    Version: NotRequired[str]


class UpdateSignalingChannelInputRequestTypeDef(TypedDict):
    ChannelARN: str
    CurrentVersion: str
    SingleMasterConfiguration: NotRequired[SingleMasterConfigurationTypeDef]


class ListSignalingChannelsInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ChannelNameCondition: NotRequired[ChannelNameConditionTypeDef]


class CreateSignalingChannelInputRequestTypeDef(TypedDict):
    ChannelName: str
    ChannelType: NotRequired[ChannelTypeType]
    SingleMasterConfiguration: NotRequired[SingleMasterConfigurationTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class TagResourceInputRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]


class CreateSignalingChannelOutputTypeDef(TypedDict):
    ChannelARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateStreamOutputTypeDef(TypedDict):
    StreamARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetDataEndpointOutputTypeDef(TypedDict):
    DataEndpoint: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceOutputTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForStreamOutputTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DeletionConfigTypeDef(TypedDict):
    EdgeRetentionInHours: NotRequired[int]
    LocalSizeConfig: NotRequired[LocalSizeConfigTypeDef]
    DeleteAfterUpload: NotRequired[bool]


class DescribeMappedResourceConfigurationInputDescribeMappedResourceConfigurationPaginateTypeDef(
    TypedDict
):
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEdgeAgentConfigurationsInputListEdgeAgentConfigurationsPaginateTypeDef(TypedDict):
    HubDeviceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSignalingChannelsInputListSignalingChannelsPaginateTypeDef(TypedDict):
    ChannelNameCondition: NotRequired[ChannelNameConditionTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeMappedResourceConfigurationOutputTypeDef(TypedDict):
    MappedResourceConfigurationList: List[MappedResourceConfigurationListItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeMediaStorageConfigurationOutputTypeDef(TypedDict):
    MediaStorageConfiguration: MediaStorageConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMediaStorageConfigurationInputRequestTypeDef(TypedDict):
    ChannelARN: str
    MediaStorageConfiguration: MediaStorageConfigurationTypeDef


class DescribeStreamOutputTypeDef(TypedDict):
    StreamInfo: StreamInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListStreamsOutputTypeDef(TypedDict):
    StreamInfoList: List[StreamInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class EdgeAgentStatusTypeDef(TypedDict):
    LastRecorderStatus: NotRequired[LastRecorderStatusTypeDef]
    LastUploaderStatus: NotRequired[LastUploaderStatusTypeDef]


class GetSignalingChannelEndpointInputRequestTypeDef(TypedDict):
    ChannelARN: str
    SingleMasterChannelEndpointConfiguration: NotRequired[
        SingleMasterChannelEndpointConfigurationTypeDef
    ]


class GetSignalingChannelEndpointOutputTypeDef(TypedDict):
    ResourceEndpointList: List[ResourceEndpointListItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ImageGenerationConfigurationOutputTypeDef(TypedDict):
    Status: ConfigurationStatusType
    ImageSelectorType: ImageSelectorTypeType
    DestinationConfig: ImageGenerationDestinationConfigTypeDef
    SamplingInterval: int
    Format: FormatType
    FormatConfig: NotRequired[Dict[Literal["JPEGQuality"], str]]
    WidthPixels: NotRequired[int]
    HeightPixels: NotRequired[int]


class ImageGenerationConfigurationTypeDef(TypedDict):
    Status: ConfigurationStatusType
    ImageSelectorType: ImageSelectorTypeType
    DestinationConfig: ImageGenerationDestinationConfigTypeDef
    SamplingInterval: int
    Format: FormatType
    FormatConfig: NotRequired[Mapping[Literal["JPEGQuality"], str]]
    WidthPixels: NotRequired[int]
    HeightPixels: NotRequired[int]


class ListStreamsInputListStreamsPaginateTypeDef(TypedDict):
    StreamNameCondition: NotRequired[StreamNameConditionTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStreamsInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    StreamNameCondition: NotRequired[StreamNameConditionTypeDef]


class NotificationConfigurationTypeDef(TypedDict):
    Status: ConfigurationStatusType
    DestinationConfig: NotificationDestinationConfigTypeDef


class RecorderConfigTypeDef(TypedDict):
    MediaSourceConfig: MediaSourceConfigTypeDef
    ScheduleConfig: NotRequired[ScheduleConfigTypeDef]


class UploaderConfigTypeDef(TypedDict):
    ScheduleConfig: ScheduleConfigTypeDef


class DescribeSignalingChannelOutputTypeDef(TypedDict):
    ChannelInfo: ChannelInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListSignalingChannelsOutputTypeDef(TypedDict):
    ChannelInfoList: List[ChannelInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeImageGenerationConfigurationOutputTypeDef(TypedDict):
    ImageGenerationConfiguration: ImageGenerationConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateImageGenerationConfigurationInputRequestTypeDef(TypedDict):
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    ImageGenerationConfiguration: NotRequired[ImageGenerationConfigurationTypeDef]


class DescribeNotificationConfigurationOutputTypeDef(TypedDict):
    NotificationConfiguration: NotificationConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateNotificationConfigurationInputRequestTypeDef(TypedDict):
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    NotificationConfiguration: NotRequired[NotificationConfigurationTypeDef]


class EdgeConfigTypeDef(TypedDict):
    HubDeviceArn: str
    RecorderConfig: RecorderConfigTypeDef
    UploaderConfig: NotRequired[UploaderConfigTypeDef]
    DeletionConfig: NotRequired[DeletionConfigTypeDef]


class DescribeEdgeConfigurationOutputTypeDef(TypedDict):
    StreamName: str
    StreamARN: str
    CreationTime: datetime
    LastUpdatedTime: datetime
    SyncStatus: SyncStatusType
    FailedStatusDetails: str
    EdgeConfig: EdgeConfigTypeDef
    EdgeAgentStatus: EdgeAgentStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListEdgeAgentConfigurationsEdgeConfigTypeDef(TypedDict):
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    SyncStatus: NotRequired[SyncStatusType]
    FailedStatusDetails: NotRequired[str]
    EdgeConfig: NotRequired[EdgeConfigTypeDef]


class StartEdgeConfigurationUpdateInputRequestTypeDef(TypedDict):
    EdgeConfig: EdgeConfigTypeDef
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]


class StartEdgeConfigurationUpdateOutputTypeDef(TypedDict):
    StreamName: str
    StreamARN: str
    CreationTime: datetime
    LastUpdatedTime: datetime
    SyncStatus: SyncStatusType
    FailedStatusDetails: str
    EdgeConfig: EdgeConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListEdgeAgentConfigurationsOutputTypeDef(TypedDict):
    EdgeConfigs: List[ListEdgeAgentConfigurationsEdgeConfigTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
