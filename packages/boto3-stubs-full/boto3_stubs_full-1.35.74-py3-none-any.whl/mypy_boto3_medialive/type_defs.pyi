"""
Type annotations for medialive service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/type_defs/)

Usage::

    ```python
    from mypy_boto3_medialive.type_defs import AacSettingsTypeDef

    data: AacSettingsTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AacCodingModeType,
    AacInputTypeType,
    AacProfileType,
    AacRateControlModeType,
    AacRawFormatType,
    AacSpecType,
    AacVbrQualityType,
    Ac3AttenuationControlType,
    Ac3BitstreamModeType,
    Ac3CodingModeType,
    Ac3DrcProfileType,
    Ac3LfeFilterType,
    Ac3MetadataControlType,
    AccessibilityTypeType,
    AfdSignalingType,
    AlgorithmType,
    AudioDescriptionAudioTypeControlType,
    AudioDescriptionLanguageCodeControlType,
    AudioLanguageSelectionPolicyType,
    AudioNormalizationAlgorithmType,
    AudioOnlyHlsSegmentTypeType,
    AudioOnlyHlsTrackTypeType,
    AudioTypeType,
    AuthenticationSchemeType,
    Av1GopSizeUnitsType,
    Av1LevelType,
    Av1LookAheadRateControlType,
    Av1SceneChangeDetectType,
    AvailBlankingStateType,
    BandwidthReductionFilterStrengthType,
    BandwidthReductionPostFilterSharpeningType,
    BlackoutSlateNetworkEndBlackoutType,
    BlackoutSlateStateType,
    BurnInAlignmentType,
    BurnInBackgroundColorType,
    BurnInFontColorType,
    BurnInOutlineColorType,
    BurnInShadowColorType,
    BurnInTeletextGridControlType,
    CdiInputResolutionType,
    ChannelClassType,
    ChannelPipelineIdToRestartType,
    ChannelPlacementGroupStateType,
    ChannelStateType,
    CloudWatchAlarmTemplateComparisonOperatorType,
    CloudWatchAlarmTemplateStatisticType,
    CloudWatchAlarmTemplateTargetResourceTypeType,
    CloudWatchAlarmTemplateTreatMissingDataType,
    ClusterStateType,
    CmafIngestSegmentLengthUnitsType,
    CmafNielsenId3BehaviorType,
    ColorSpaceType,
    DashRoleAudioType,
    DashRoleCaptionType,
    DeviceSettingsSyncStateType,
    DeviceUpdateStatusType,
    DolbyEProgramSelectionType,
    DvbDashAccessibilityType,
    DvbSdtOutputSdtType,
    DvbSubDestinationAlignmentType,
    DvbSubDestinationBackgroundColorType,
    DvbSubDestinationFontColorType,
    DvbSubDestinationOutlineColorType,
    DvbSubDestinationShadowColorType,
    DvbSubDestinationTeletextGridControlType,
    DvbSubOcrLanguageType,
    Eac3AtmosCodingModeType,
    Eac3AtmosDrcLineType,
    Eac3AtmosDrcRfType,
    Eac3AttenuationControlType,
    Eac3BitstreamModeType,
    Eac3CodingModeType,
    Eac3DcFilterType,
    Eac3DrcLineType,
    Eac3DrcRfType,
    Eac3LfeControlType,
    Eac3LfeFilterType,
    Eac3MetadataControlType,
    Eac3PassthroughControlType,
    Eac3PhaseControlType,
    Eac3StereoDownmixType,
    Eac3SurroundExModeType,
    Eac3SurroundModeType,
    EbuTtDDestinationStyleControlType,
    EbuTtDFillLineGapControlType,
    EmbeddedConvert608To708Type,
    EmbeddedScte20DetectionType,
    EventBridgeRuleTemplateEventTypeType,
    FeatureActivationsInputPrepareScheduleActionsType,
    FeatureActivationsOutputStaticImageOverlayScheduleActionsType,
    FecOutputIncludeFecType,
    FixedAfdType,
    Fmp4NielsenId3BehaviorType,
    Fmp4TimedMetadataBehaviorType,
    FollowPointType,
    FrameCaptureIntervalUnitType,
    GlobalConfigurationInputEndActionType,
    GlobalConfigurationLowFramerateInputsType,
    GlobalConfigurationOutputLockingModeType,
    GlobalConfigurationOutputTimingSourceType,
    H264AdaptiveQuantizationType,
    H264ColorMetadataType,
    H264EntropyEncodingType,
    H264FlickerAqType,
    H264ForceFieldPicturesType,
    H264FramerateControlType,
    H264GopBReferenceType,
    H264GopSizeUnitsType,
    H264LevelType,
    H264LookAheadRateControlType,
    H264ParControlType,
    H264ProfileType,
    H264QualityLevelType,
    H264RateControlModeType,
    H264ScanTypeType,
    H264SceneChangeDetectType,
    H264SpatialAqType,
    H264SubGopLengthType,
    H264SyntaxType,
    H264TemporalAqType,
    H264TimecodeInsertionBehaviorType,
    H265AdaptiveQuantizationType,
    H265AlternativeTransferFunctionType,
    H265ColorMetadataType,
    H265FlickerAqType,
    H265GopSizeUnitsType,
    H265LevelType,
    H265LookAheadRateControlType,
    H265MvOverPictureBoundariesType,
    H265MvTemporalPredictorType,
    H265ProfileType,
    H265RateControlModeType,
    H265ScanTypeType,
    H265SceneChangeDetectType,
    H265TierType,
    H265TilePaddingType,
    H265TimecodeInsertionBehaviorType,
    H265TreeblockSizeType,
    HlsAdMarkersType,
    HlsAkamaiHttpTransferModeType,
    HlsCaptionLanguageSettingType,
    HlsClientCacheType,
    HlsCodecSpecificationType,
    HlsDirectoryStructureType,
    HlsDiscontinuityTagsType,
    HlsEncryptionTypeType,
    HlsH265PackagingTypeType,
    HlsId3SegmentTaggingStateType,
    HlsIncompleteSegmentBehaviorType,
    HlsIvInManifestType,
    HlsIvSourceType,
    HlsManifestCompressionType,
    HlsManifestDurationFormatType,
    HlsModeType,
    HlsOutputSelectionType,
    HlsProgramDateTimeClockType,
    HlsProgramDateTimeType,
    HlsRedundantManifestType,
    HlsScte35SourceTypeType,
    HlsSegmentationModeType,
    HlsStreamInfResolutionType,
    HlsTimedMetadataId3FrameType,
    HlsTsFileModeType,
    HlsWebdavHttpTransferModeType,
    IFrameOnlyPlaylistTypeType,
    IncludeFillerNalUnitsType,
    InputClassType,
    InputCodecType,
    InputDeblockFilterType,
    InputDenoiseFilterType,
    InputDeviceActiveInputType,
    InputDeviceCodecType,
    InputDeviceConfigurableAudioChannelPairProfileType,
    InputDeviceConfiguredInputType,
    InputDeviceConnectionStateType,
    InputDeviceIpSchemeType,
    InputDeviceOutputTypeType,
    InputDeviceScanTypeType,
    InputDeviceStateType,
    InputDeviceTransferTypeType,
    InputDeviceTypeType,
    InputDeviceUhdAudioChannelPairProfileType,
    InputFilterType,
    InputLossActionForHlsOutType,
    InputLossActionForMsSmoothOutType,
    InputLossActionForRtmpOutType,
    InputLossActionForUdpOutType,
    InputLossImageTypeType,
    InputMaximumBitrateType,
    InputNetworkLocationType,
    InputPreferenceType,
    InputResolutionType,
    InputSecurityGroupStateType,
    InputSourceEndBehaviorType,
    InputSourceTypeType,
    InputStateType,
    InputTimecodeSourceType,
    InputTypeType,
    LastFrameClippingBehaviorType,
    LogLevelType,
    M2tsAbsentInputAudioBehaviorType,
    M2tsAribCaptionsPidControlType,
    M2tsAribType,
    M2tsAudioBufferModelType,
    M2tsAudioIntervalType,
    M2tsAudioStreamTypeType,
    M2tsBufferModelType,
    M2tsCcDescriptorType,
    M2tsEbifControlType,
    M2tsEbpPlacementType,
    M2tsEsRateInPesType,
    M2tsKlvType,
    M2tsNielsenId3BehaviorType,
    M2tsPcrControlType,
    M2tsRateModeType,
    M2tsScte35ControlType,
    M2tsSegmentationMarkersType,
    M2tsSegmentationStyleType,
    M2tsTimedMetadataBehaviorType,
    M3u8KlvBehaviorType,
    M3u8NielsenId3BehaviorType,
    M3u8PcrControlType,
    M3u8Scte35BehaviorType,
    M3u8TimedMetadataBehaviorType,
    MaintenanceDayType,
    MotionGraphicsInsertionType,
    Mp2CodingModeType,
    Mpeg2AdaptiveQuantizationType,
    Mpeg2ColorMetadataType,
    Mpeg2ColorSpaceType,
    Mpeg2DisplayRatioType,
    Mpeg2GopSizeUnitsType,
    Mpeg2ScanTypeType,
    Mpeg2SubGopLengthType,
    Mpeg2TimecodeInsertionBehaviorType,
    MsSmoothH265PackagingTypeType,
    MultiplexStateType,
    NetworkInputServerValidationType,
    NetworkInterfaceModeType,
    NetworkStateType,
    NielsenPcmToId3TaggingStateType,
    NielsenWatermarksCbetStepasideType,
    NielsenWatermarksDistributionTypesType,
    NielsenWatermarkTimezonesType,
    NodeConnectionStateType,
    NodeRoleType,
    NodeStateType,
    PipelineIdType,
    PreferredChannelPipelineType,
    RebootInputDeviceForceType,
    ReservationAutomaticRenewalType,
    ReservationCodecType,
    ReservationMaximumBitrateType,
    ReservationMaximumFramerateType,
    ReservationResolutionType,
    ReservationResourceTypeType,
    ReservationSpecialFeatureType,
    ReservationStateType,
    ReservationVideoQualityType,
    RtmpCacheFullBehaviorType,
    RtmpCaptionDataType,
    RtmpOutputCertificateModeType,
    S3CannedAclType,
    Scte20Convert608To708Type,
    Scte27OcrLanguageType,
    Scte35AposNoRegionalBlackoutBehaviorType,
    Scte35AposWebDeliveryAllowedBehaviorType,
    Scte35ArchiveAllowedFlagType,
    Scte35DeviceRestrictionsType,
    Scte35InputModeType,
    Scte35NoRegionalBlackoutFlagType,
    Scte35SegmentationCancelIndicatorType,
    Scte35SegmentationScopeType,
    Scte35SpliceInsertNoRegionalBlackoutBehaviorType,
    Scte35SpliceInsertWebDeliveryAllowedBehaviorType,
    Scte35TypeType,
    Scte35WebDeliveryAllowedFlagType,
    SignalMapMonitorDeploymentStatusType,
    SignalMapStatusType,
    SmoothGroupAudioOnlyTimecodeControlType,
    SmoothGroupCertificateModeType,
    SmoothGroupEventIdModeType,
    SmoothGroupEventStopBehaviorType,
    SmoothGroupSegmentationModeType,
    SmoothGroupSparseTrackTypeType,
    SmoothGroupStreamManifestBehaviorType,
    SmoothGroupTimestampOffsetModeType,
    Smpte2038DataPreferenceType,
    SrtEncryptionTypeType,
    TemporalFilterPostFilterSharpeningType,
    TemporalFilterStrengthType,
    ThumbnailStateType,
    ThumbnailTypeType,
    TimecodeBurninFontSizeType,
    TimecodeBurninPositionType,
    TimecodeConfigSourceType,
    TtmlDestinationStyleControlType,
    UdpTimedMetadataId3FrameType,
    UpdateNodeStateType,
    VideoDescriptionRespondToAfdType,
    VideoDescriptionScalingBehaviorType,
    VideoSelectorColorSpaceType,
    VideoSelectorColorSpaceUsageType,
    WavCodingModeType,
    WebvttDestinationStyleControlType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AacSettingsTypeDef",
    "Ac3SettingsTypeDef",
    "AcceptInputDeviceTransferRequestRequestTypeDef",
    "AccountConfigurationTypeDef",
    "AncillarySourceSettingsTypeDef",
    "AnywhereSettingsTypeDef",
    "ArchiveCdnSettingsTypeDef",
    "ArchiveContainerSettingsOutputTypeDef",
    "ArchiveContainerSettingsTypeDef",
    "ArchiveContainerSettingsUnionTypeDef",
    "ArchiveGroupSettingsTypeDef",
    "ArchiveOutputSettingsOutputTypeDef",
    "ArchiveOutputSettingsTypeDef",
    "ArchiveOutputSettingsUnionTypeDef",
    "ArchiveS3SettingsTypeDef",
    "AudioChannelMappingOutputTypeDef",
    "AudioChannelMappingTypeDef",
    "AudioChannelMappingUnionTypeDef",
    "AudioCodecSettingsOutputTypeDef",
    "AudioCodecSettingsTypeDef",
    "AudioCodecSettingsUnionTypeDef",
    "AudioDescriptionOutputTypeDef",
    "AudioDescriptionTypeDef",
    "AudioDescriptionUnionTypeDef",
    "AudioDolbyEDecodeTypeDef",
    "AudioHlsRenditionSelectionTypeDef",
    "AudioLanguageSelectionTypeDef",
    "AudioNormalizationSettingsTypeDef",
    "AudioOnlyHlsSettingsTypeDef",
    "AudioPidSelectionTypeDef",
    "AudioSelectorOutputTypeDef",
    "AudioSelectorSettingsOutputTypeDef",
    "AudioSelectorSettingsTypeDef",
    "AudioSelectorSettingsUnionTypeDef",
    "AudioSelectorTypeDef",
    "AudioSelectorUnionTypeDef",
    "AudioSilenceFailoverSettingsTypeDef",
    "AudioTrackSelectionOutputTypeDef",
    "AudioTrackSelectionTypeDef",
    "AudioTrackSelectionUnionTypeDef",
    "AudioTrackTypeDef",
    "AudioWatermarkSettingsTypeDef",
    "AutomaticInputFailoverSettingsOutputTypeDef",
    "AutomaticInputFailoverSettingsTypeDef",
    "AutomaticInputFailoverSettingsUnionTypeDef",
    "Av1ColorSpaceSettingsOutputTypeDef",
    "Av1ColorSpaceSettingsTypeDef",
    "Av1ColorSpaceSettingsUnionTypeDef",
    "Av1SettingsOutputTypeDef",
    "Av1SettingsTypeDef",
    "Av1SettingsUnionTypeDef",
    "AvailBlankingTypeDef",
    "AvailConfigurationTypeDef",
    "AvailSettingsTypeDef",
    "BandwidthReductionFilterSettingsTypeDef",
    "BatchDeleteRequestRequestTypeDef",
    "BatchDeleteResponseTypeDef",
    "BatchFailedResultModelTypeDef",
    "BatchScheduleActionCreateRequestTypeDef",
    "BatchScheduleActionCreateResultTypeDef",
    "BatchScheduleActionDeleteRequestTypeDef",
    "BatchScheduleActionDeleteResultTypeDef",
    "BatchStartRequestRequestTypeDef",
    "BatchStartResponseTypeDef",
    "BatchStopRequestRequestTypeDef",
    "BatchStopResponseTypeDef",
    "BatchSuccessfulResultModelTypeDef",
    "BatchUpdateScheduleRequestRequestTypeDef",
    "BatchUpdateScheduleResponseTypeDef",
    "BlackoutSlateTypeDef",
    "BurnInDestinationSettingsTypeDef",
    "CancelInputDeviceTransferRequestRequestTypeDef",
    "CaptionDescriptionOutputTypeDef",
    "CaptionDescriptionTypeDef",
    "CaptionDescriptionUnionTypeDef",
    "CaptionDestinationSettingsOutputTypeDef",
    "CaptionDestinationSettingsTypeDef",
    "CaptionDestinationSettingsUnionTypeDef",
    "CaptionLanguageMappingTypeDef",
    "CaptionRectangleTypeDef",
    "CaptionSelectorOutputTypeDef",
    "CaptionSelectorSettingsOutputTypeDef",
    "CaptionSelectorSettingsTypeDef",
    "CaptionSelectorSettingsUnionTypeDef",
    "CaptionSelectorTypeDef",
    "CaptionSelectorUnionTypeDef",
    "CdiInputSpecificationTypeDef",
    "ChannelEgressEndpointTypeDef",
    "ChannelSummaryTypeDef",
    "ChannelTypeDef",
    "ClaimDeviceRequestRequestTypeDef",
    "CloudWatchAlarmTemplateGroupSummaryTypeDef",
    "CloudWatchAlarmTemplateSummaryTypeDef",
    "ClusterNetworkSettingsCreateRequestTypeDef",
    "ClusterNetworkSettingsTypeDef",
    "ClusterNetworkSettingsUpdateRequestTypeDef",
    "CmafIngestGroupSettingsTypeDef",
    "CmafIngestOutputSettingsTypeDef",
    "ColorCorrectionSettingsOutputTypeDef",
    "ColorCorrectionSettingsTypeDef",
    "ColorCorrectionSettingsUnionTypeDef",
    "ColorCorrectionTypeDef",
    "CreateChannelPlacementGroupRequestRequestTypeDef",
    "CreateChannelPlacementGroupResponseTypeDef",
    "CreateChannelRequestRequestTypeDef",
    "CreateChannelResponseTypeDef",
    "CreateCloudWatchAlarmTemplateGroupRequestRequestTypeDef",
    "CreateCloudWatchAlarmTemplateGroupResponseTypeDef",
    "CreateCloudWatchAlarmTemplateRequestRequestTypeDef",
    "CreateCloudWatchAlarmTemplateResponseTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "CreateClusterResponseTypeDef",
    "CreateEventBridgeRuleTemplateGroupRequestRequestTypeDef",
    "CreateEventBridgeRuleTemplateGroupResponseTypeDef",
    "CreateEventBridgeRuleTemplateRequestRequestTypeDef",
    "CreateEventBridgeRuleTemplateResponseTypeDef",
    "CreateInputRequestRequestTypeDef",
    "CreateInputResponseTypeDef",
    "CreateInputSecurityGroupRequestRequestTypeDef",
    "CreateInputSecurityGroupResponseTypeDef",
    "CreateMultiplexProgramRequestRequestTypeDef",
    "CreateMultiplexProgramResponseTypeDef",
    "CreateMultiplexRequestRequestTypeDef",
    "CreateMultiplexResponseTypeDef",
    "CreateNetworkRequestRequestTypeDef",
    "CreateNetworkResponseTypeDef",
    "CreateNodeRegistrationScriptRequestRequestTypeDef",
    "CreateNodeRegistrationScriptResponseTypeDef",
    "CreateNodeRequestRequestTypeDef",
    "CreateNodeResponseTypeDef",
    "CreatePartnerInputRequestRequestTypeDef",
    "CreatePartnerInputResponseTypeDef",
    "CreateSignalMapRequestRequestTypeDef",
    "CreateSignalMapResponseTypeDef",
    "CreateTagsRequestRequestTypeDef",
    "DeleteChannelPlacementGroupRequestRequestTypeDef",
    "DeleteChannelPlacementGroupResponseTypeDef",
    "DeleteChannelRequestRequestTypeDef",
    "DeleteChannelResponseTypeDef",
    "DeleteCloudWatchAlarmTemplateGroupRequestRequestTypeDef",
    "DeleteCloudWatchAlarmTemplateRequestRequestTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteClusterResponseTypeDef",
    "DeleteEventBridgeRuleTemplateGroupRequestRequestTypeDef",
    "DeleteEventBridgeRuleTemplateRequestRequestTypeDef",
    "DeleteInputRequestRequestTypeDef",
    "DeleteInputSecurityGroupRequestRequestTypeDef",
    "DeleteMultiplexProgramRequestRequestTypeDef",
    "DeleteMultiplexProgramResponseTypeDef",
    "DeleteMultiplexRequestRequestTypeDef",
    "DeleteMultiplexResponseTypeDef",
    "DeleteNetworkRequestRequestTypeDef",
    "DeleteNetworkResponseTypeDef",
    "DeleteNodeRequestRequestTypeDef",
    "DeleteNodeResponseTypeDef",
    "DeleteReservationRequestRequestTypeDef",
    "DeleteReservationResponseTypeDef",
    "DeleteScheduleRequestRequestTypeDef",
    "DeleteSignalMapRequestRequestTypeDef",
    "DeleteTagsRequestRequestTypeDef",
    "DescribeAccountConfigurationResponseTypeDef",
    "DescribeAnywhereSettingsTypeDef",
    "DescribeChannelPlacementGroupRequestChannelPlacementGroupAssignedWaitTypeDef",
    "DescribeChannelPlacementGroupRequestChannelPlacementGroupDeletedWaitTypeDef",
    "DescribeChannelPlacementGroupRequestChannelPlacementGroupUnassignedWaitTypeDef",
    "DescribeChannelPlacementGroupRequestRequestTypeDef",
    "DescribeChannelPlacementGroupResponseTypeDef",
    "DescribeChannelPlacementGroupSummaryTypeDef",
    "DescribeChannelRequestChannelCreatedWaitTypeDef",
    "DescribeChannelRequestChannelDeletedWaitTypeDef",
    "DescribeChannelRequestChannelRunningWaitTypeDef",
    "DescribeChannelRequestChannelStoppedWaitTypeDef",
    "DescribeChannelRequestRequestTypeDef",
    "DescribeChannelResponseTypeDef",
    "DescribeClusterRequestClusterCreatedWaitTypeDef",
    "DescribeClusterRequestClusterDeletedWaitTypeDef",
    "DescribeClusterRequestRequestTypeDef",
    "DescribeClusterResponseTypeDef",
    "DescribeClusterSummaryTypeDef",
    "DescribeInputDeviceRequestRequestTypeDef",
    "DescribeInputDeviceResponseTypeDef",
    "DescribeInputDeviceThumbnailRequestRequestTypeDef",
    "DescribeInputDeviceThumbnailResponseTypeDef",
    "DescribeInputRequestInputAttachedWaitTypeDef",
    "DescribeInputRequestInputDeletedWaitTypeDef",
    "DescribeInputRequestInputDetachedWaitTypeDef",
    "DescribeInputRequestRequestTypeDef",
    "DescribeInputResponseTypeDef",
    "DescribeInputSecurityGroupRequestRequestTypeDef",
    "DescribeInputSecurityGroupResponseTypeDef",
    "DescribeMultiplexProgramRequestRequestTypeDef",
    "DescribeMultiplexProgramResponseTypeDef",
    "DescribeMultiplexRequestMultiplexCreatedWaitTypeDef",
    "DescribeMultiplexRequestMultiplexDeletedWaitTypeDef",
    "DescribeMultiplexRequestMultiplexRunningWaitTypeDef",
    "DescribeMultiplexRequestMultiplexStoppedWaitTypeDef",
    "DescribeMultiplexRequestRequestTypeDef",
    "DescribeMultiplexResponseTypeDef",
    "DescribeNetworkRequestRequestTypeDef",
    "DescribeNetworkResponseTypeDef",
    "DescribeNetworkSummaryTypeDef",
    "DescribeNodeRequestNodeDeregisteredWaitTypeDef",
    "DescribeNodeRequestNodeRegisteredWaitTypeDef",
    "DescribeNodeRequestRequestTypeDef",
    "DescribeNodeResponseTypeDef",
    "DescribeNodeSummaryTypeDef",
    "DescribeOfferingRequestRequestTypeDef",
    "DescribeOfferingResponseTypeDef",
    "DescribeReservationRequestRequestTypeDef",
    "DescribeReservationResponseTypeDef",
    "DescribeScheduleRequestDescribeSchedulePaginateTypeDef",
    "DescribeScheduleRequestRequestTypeDef",
    "DescribeScheduleResponseTypeDef",
    "DescribeThumbnailsRequestRequestTypeDef",
    "DescribeThumbnailsResponseTypeDef",
    "DvbNitSettingsTypeDef",
    "DvbSdtSettingsTypeDef",
    "DvbSubDestinationSettingsTypeDef",
    "DvbSubSourceSettingsTypeDef",
    "DvbTdtSettingsTypeDef",
    "Eac3AtmosSettingsTypeDef",
    "Eac3SettingsTypeDef",
    "EbuTtDDestinationSettingsTypeDef",
    "EmbeddedSourceSettingsTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncoderSettingsOutputTypeDef",
    "EncoderSettingsTypeDef",
    "EpochLockingSettingsTypeDef",
    "EsamTypeDef",
    "EventBridgeRuleTemplateGroupSummaryTypeDef",
    "EventBridgeRuleTemplateSummaryTypeDef",
    "EventBridgeRuleTemplateTargetTypeDef",
    "ExtraOutputTypeDef",
    "FailoverConditionSettingsTypeDef",
    "FailoverConditionTypeDef",
    "FeatureActivationsTypeDef",
    "FecOutputSettingsTypeDef",
    "FixedModeScheduleActionStartSettingsTypeDef",
    "Fmp4HlsSettingsTypeDef",
    "FollowModeScheduleActionStartSettingsTypeDef",
    "FrameCaptureCdnSettingsTypeDef",
    "FrameCaptureGroupSettingsTypeDef",
    "FrameCaptureOutputSettingsTypeDef",
    "FrameCaptureS3SettingsTypeDef",
    "FrameCaptureSettingsTypeDef",
    "GetCloudWatchAlarmTemplateGroupRequestRequestTypeDef",
    "GetCloudWatchAlarmTemplateGroupResponseTypeDef",
    "GetCloudWatchAlarmTemplateRequestRequestTypeDef",
    "GetCloudWatchAlarmTemplateResponseTypeDef",
    "GetEventBridgeRuleTemplateGroupRequestRequestTypeDef",
    "GetEventBridgeRuleTemplateGroupResponseTypeDef",
    "GetEventBridgeRuleTemplateRequestRequestTypeDef",
    "GetEventBridgeRuleTemplateResponseTypeDef",
    "GetSignalMapRequestRequestTypeDef",
    "GetSignalMapRequestSignalMapCreatedWaitTypeDef",
    "GetSignalMapRequestSignalMapMonitorDeletedWaitTypeDef",
    "GetSignalMapRequestSignalMapMonitorDeployedWaitTypeDef",
    "GetSignalMapRequestSignalMapUpdatedWaitTypeDef",
    "GetSignalMapResponseTypeDef",
    "GlobalConfigurationOutputTypeDef",
    "GlobalConfigurationTypeDef",
    "GlobalConfigurationUnionTypeDef",
    "H264ColorSpaceSettingsOutputTypeDef",
    "H264ColorSpaceSettingsTypeDef",
    "H264ColorSpaceSettingsUnionTypeDef",
    "H264FilterSettingsTypeDef",
    "H264SettingsOutputTypeDef",
    "H264SettingsTypeDef",
    "H264SettingsUnionTypeDef",
    "H265ColorSpaceSettingsOutputTypeDef",
    "H265ColorSpaceSettingsTypeDef",
    "H265ColorSpaceSettingsUnionTypeDef",
    "H265FilterSettingsTypeDef",
    "H265SettingsOutputTypeDef",
    "H265SettingsTypeDef",
    "H265SettingsUnionTypeDef",
    "Hdr10SettingsTypeDef",
    "HlsAkamaiSettingsTypeDef",
    "HlsBasicPutSettingsTypeDef",
    "HlsCdnSettingsTypeDef",
    "HlsGroupSettingsOutputTypeDef",
    "HlsGroupSettingsTypeDef",
    "HlsGroupSettingsUnionTypeDef",
    "HlsId3SegmentTaggingScheduleActionSettingsTypeDef",
    "HlsInputSettingsTypeDef",
    "HlsMediaStoreSettingsTypeDef",
    "HlsOutputSettingsOutputTypeDef",
    "HlsOutputSettingsTypeDef",
    "HlsOutputSettingsUnionTypeDef",
    "HlsS3SettingsTypeDef",
    "HlsSettingsOutputTypeDef",
    "HlsSettingsTypeDef",
    "HlsSettingsUnionTypeDef",
    "HlsTimedMetadataScheduleActionSettingsTypeDef",
    "HlsWebdavSettingsTypeDef",
    "InputAttachmentOutputTypeDef",
    "InputAttachmentTypeDef",
    "InputAttachmentUnionTypeDef",
    "InputChannelLevelTypeDef",
    "InputClippingSettingsTypeDef",
    "InputDestinationRequestTypeDef",
    "InputDestinationRouteTypeDef",
    "InputDestinationTypeDef",
    "InputDestinationVpcTypeDef",
    "InputDeviceConfigurableAudioChannelPairConfigTypeDef",
    "InputDeviceConfigurableSettingsTypeDef",
    "InputDeviceHdSettingsTypeDef",
    "InputDeviceMediaConnectConfigurableSettingsTypeDef",
    "InputDeviceMediaConnectSettingsTypeDef",
    "InputDeviceNetworkSettingsTypeDef",
    "InputDeviceRequestTypeDef",
    "InputDeviceSettingsTypeDef",
    "InputDeviceSummaryTypeDef",
    "InputDeviceUhdAudioChannelPairConfigTypeDef",
    "InputDeviceUhdSettingsTypeDef",
    "InputLocationTypeDef",
    "InputLossBehaviorTypeDef",
    "InputLossFailoverSettingsTypeDef",
    "InputPrepareScheduleActionSettingsOutputTypeDef",
    "InputPrepareScheduleActionSettingsTypeDef",
    "InputPrepareScheduleActionSettingsUnionTypeDef",
    "InputRequestDestinationRouteTypeDef",
    "InputSecurityGroupTypeDef",
    "InputSettingsOutputTypeDef",
    "InputSettingsTypeDef",
    "InputSettingsUnionTypeDef",
    "InputSourceRequestTypeDef",
    "InputSourceTypeDef",
    "InputSpecificationTypeDef",
    "InputSwitchScheduleActionSettingsOutputTypeDef",
    "InputSwitchScheduleActionSettingsTypeDef",
    "InputSwitchScheduleActionSettingsUnionTypeDef",
    "InputTypeDef",
    "InputVpcRequestTypeDef",
    "InputWhitelistRuleCidrTypeDef",
    "InputWhitelistRuleTypeDef",
    "InterfaceMappingCreateRequestTypeDef",
    "InterfaceMappingTypeDef",
    "InterfaceMappingUpdateRequestTypeDef",
    "IpPoolCreateRequestTypeDef",
    "IpPoolTypeDef",
    "IpPoolUpdateRequestTypeDef",
    "KeyProviderSettingsTypeDef",
    "ListChannelPlacementGroupsRequestListChannelPlacementGroupsPaginateTypeDef",
    "ListChannelPlacementGroupsRequestRequestTypeDef",
    "ListChannelPlacementGroupsResponseTypeDef",
    "ListChannelsRequestListChannelsPaginateTypeDef",
    "ListChannelsRequestRequestTypeDef",
    "ListChannelsResponseTypeDef",
    "ListCloudWatchAlarmTemplateGroupsRequestListCloudWatchAlarmTemplateGroupsPaginateTypeDef",
    "ListCloudWatchAlarmTemplateGroupsRequestRequestTypeDef",
    "ListCloudWatchAlarmTemplateGroupsResponseTypeDef",
    "ListCloudWatchAlarmTemplatesRequestListCloudWatchAlarmTemplatesPaginateTypeDef",
    "ListCloudWatchAlarmTemplatesRequestRequestTypeDef",
    "ListCloudWatchAlarmTemplatesResponseTypeDef",
    "ListClustersRequestListClustersPaginateTypeDef",
    "ListClustersRequestRequestTypeDef",
    "ListClustersResponseTypeDef",
    "ListEventBridgeRuleTemplateGroupsRequestListEventBridgeRuleTemplateGroupsPaginateTypeDef",
    "ListEventBridgeRuleTemplateGroupsRequestRequestTypeDef",
    "ListEventBridgeRuleTemplateGroupsResponseTypeDef",
    "ListEventBridgeRuleTemplatesRequestListEventBridgeRuleTemplatesPaginateTypeDef",
    "ListEventBridgeRuleTemplatesRequestRequestTypeDef",
    "ListEventBridgeRuleTemplatesResponseTypeDef",
    "ListInputDeviceTransfersRequestListInputDeviceTransfersPaginateTypeDef",
    "ListInputDeviceTransfersRequestRequestTypeDef",
    "ListInputDeviceTransfersResponseTypeDef",
    "ListInputDevicesRequestListInputDevicesPaginateTypeDef",
    "ListInputDevicesRequestRequestTypeDef",
    "ListInputDevicesResponseTypeDef",
    "ListInputSecurityGroupsRequestListInputSecurityGroupsPaginateTypeDef",
    "ListInputSecurityGroupsRequestRequestTypeDef",
    "ListInputSecurityGroupsResponseTypeDef",
    "ListInputsRequestListInputsPaginateTypeDef",
    "ListInputsRequestRequestTypeDef",
    "ListInputsResponseTypeDef",
    "ListMultiplexProgramsRequestListMultiplexProgramsPaginateTypeDef",
    "ListMultiplexProgramsRequestRequestTypeDef",
    "ListMultiplexProgramsResponseTypeDef",
    "ListMultiplexesRequestListMultiplexesPaginateTypeDef",
    "ListMultiplexesRequestRequestTypeDef",
    "ListMultiplexesResponseTypeDef",
    "ListNetworksRequestListNetworksPaginateTypeDef",
    "ListNetworksRequestRequestTypeDef",
    "ListNetworksResponseTypeDef",
    "ListNodesRequestListNodesPaginateTypeDef",
    "ListNodesRequestRequestTypeDef",
    "ListNodesResponseTypeDef",
    "ListOfferingsRequestListOfferingsPaginateTypeDef",
    "ListOfferingsRequestRequestTypeDef",
    "ListOfferingsResponseTypeDef",
    "ListReservationsRequestListReservationsPaginateTypeDef",
    "ListReservationsRequestRequestTypeDef",
    "ListReservationsResponseTypeDef",
    "ListSignalMapsRequestListSignalMapsPaginateTypeDef",
    "ListSignalMapsRequestRequestTypeDef",
    "ListSignalMapsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "M2tsSettingsTypeDef",
    "M3u8SettingsTypeDef",
    "MaintenanceCreateSettingsTypeDef",
    "MaintenanceStatusTypeDef",
    "MaintenanceUpdateSettingsTypeDef",
    "MediaConnectFlowRequestTypeDef",
    "MediaConnectFlowTypeDef",
    "MediaPackageGroupSettingsTypeDef",
    "MediaPackageOutputDestinationSettingsTypeDef",
    "MediaResourceNeighborTypeDef",
    "MediaResourceTypeDef",
    "MonitorDeploymentTypeDef",
    "MotionGraphicsActivateScheduleActionSettingsTypeDef",
    "MotionGraphicsConfigurationOutputTypeDef",
    "MotionGraphicsConfigurationTypeDef",
    "MotionGraphicsConfigurationUnionTypeDef",
    "MotionGraphicsSettingsOutputTypeDef",
    "MotionGraphicsSettingsTypeDef",
    "MotionGraphicsSettingsUnionTypeDef",
    "Mp2SettingsTypeDef",
    "Mpeg2FilterSettingsTypeDef",
    "Mpeg2SettingsTypeDef",
    "MsSmoothGroupSettingsTypeDef",
    "MsSmoothOutputSettingsTypeDef",
    "MulticastInputSettingsTypeDef",
    "MulticastSettingsCreateRequestTypeDef",
    "MulticastSettingsTypeDef",
    "MulticastSettingsUpdateRequestTypeDef",
    "MulticastSourceCreateRequestTypeDef",
    "MulticastSourceTypeDef",
    "MulticastSourceUpdateRequestTypeDef",
    "MultiplexContainerSettingsTypeDef",
    "MultiplexM2tsSettingsTypeDef",
    "MultiplexMediaConnectOutputDestinationSettingsTypeDef",
    "MultiplexOutputDestinationTypeDef",
    "MultiplexOutputSettingsTypeDef",
    "MultiplexProgramChannelDestinationSettingsTypeDef",
    "MultiplexProgramPacketIdentifiersMapOutputTypeDef",
    "MultiplexProgramPacketIdentifiersMapTypeDef",
    "MultiplexProgramPacketIdentifiersMapUnionTypeDef",
    "MultiplexProgramPipelineDetailTypeDef",
    "MultiplexProgramServiceDescriptorTypeDef",
    "MultiplexProgramSettingsTypeDef",
    "MultiplexProgramSummaryTypeDef",
    "MultiplexProgramTypeDef",
    "MultiplexSettingsSummaryTypeDef",
    "MultiplexSettingsTypeDef",
    "MultiplexStatmuxVideoSettingsTypeDef",
    "MultiplexSummaryTypeDef",
    "MultiplexTypeDef",
    "MultiplexVideoSettingsTypeDef",
    "NetworkInputSettingsTypeDef",
    "NielsenCBETTypeDef",
    "NielsenConfigurationTypeDef",
    "NielsenNaesIiNwTypeDef",
    "NielsenWatermarksSettingsTypeDef",
    "NodeInterfaceMappingCreateRequestTypeDef",
    "NodeInterfaceMappingTypeDef",
    "OfferingTypeDef",
    "OutputDestinationOutputTypeDef",
    "OutputDestinationSettingsTypeDef",
    "OutputDestinationTypeDef",
    "OutputDestinationUnionTypeDef",
    "OutputGroupOutputTypeDef",
    "OutputGroupSettingsOutputTypeDef",
    "OutputGroupSettingsTypeDef",
    "OutputGroupSettingsUnionTypeDef",
    "OutputGroupTypeDef",
    "OutputGroupUnionTypeDef",
    "OutputLocationRefTypeDef",
    "OutputLockingSettingsOutputTypeDef",
    "OutputLockingSettingsTypeDef",
    "OutputLockingSettingsUnionTypeDef",
    "OutputSettingsOutputTypeDef",
    "OutputSettingsTypeDef",
    "OutputSettingsUnionTypeDef",
    "OutputTypeDef",
    "PaginatorConfigTypeDef",
    "PauseStateScheduleActionSettingsOutputTypeDef",
    "PauseStateScheduleActionSettingsTypeDef",
    "PauseStateScheduleActionSettingsUnionTypeDef",
    "PipelineDetailTypeDef",
    "PipelinePauseStateSettingsTypeDef",
    "PurchaseOfferingRequestRequestTypeDef",
    "PurchaseOfferingResponseTypeDef",
    "RebootInputDeviceRequestRequestTypeDef",
    "RejectInputDeviceTransferRequestRequestTypeDef",
    "RemixSettingsOutputTypeDef",
    "RemixSettingsTypeDef",
    "RemixSettingsUnionTypeDef",
    "RenewalSettingsTypeDef",
    "ReservationResourceSpecificationTypeDef",
    "ReservationTypeDef",
    "ResponseMetadataTypeDef",
    "RestartChannelPipelinesRequestRequestTypeDef",
    "RestartChannelPipelinesResponseTypeDef",
    "RouteCreateRequestTypeDef",
    "RouteTypeDef",
    "RouteUpdateRequestTypeDef",
    "RtmpGroupSettingsOutputTypeDef",
    "RtmpGroupSettingsTypeDef",
    "RtmpGroupSettingsUnionTypeDef",
    "RtmpOutputSettingsTypeDef",
    "ScheduleActionOutputTypeDef",
    "ScheduleActionSettingsOutputTypeDef",
    "ScheduleActionSettingsTypeDef",
    "ScheduleActionSettingsUnionTypeDef",
    "ScheduleActionStartSettingsOutputTypeDef",
    "ScheduleActionStartSettingsTypeDef",
    "ScheduleActionStartSettingsUnionTypeDef",
    "ScheduleActionTypeDef",
    "ScheduleActionUnionTypeDef",
    "Scte20SourceSettingsTypeDef",
    "Scte27SourceSettingsTypeDef",
    "Scte35DeliveryRestrictionsTypeDef",
    "Scte35DescriptorSettingsTypeDef",
    "Scte35DescriptorTypeDef",
    "Scte35InputScheduleActionSettingsTypeDef",
    "Scte35ReturnToNetworkScheduleActionSettingsTypeDef",
    "Scte35SegmentationDescriptorTypeDef",
    "Scte35SpliceInsertScheduleActionSettingsTypeDef",
    "Scte35SpliceInsertTypeDef",
    "Scte35TimeSignalAposTypeDef",
    "Scte35TimeSignalScheduleActionSettingsOutputTypeDef",
    "Scte35TimeSignalScheduleActionSettingsTypeDef",
    "Scte35TimeSignalScheduleActionSettingsUnionTypeDef",
    "SignalMapSummaryTypeDef",
    "SrtCallerDecryptionRequestTypeDef",
    "SrtCallerDecryptionTypeDef",
    "SrtCallerSourceRequestTypeDef",
    "SrtCallerSourceTypeDef",
    "SrtGroupSettingsTypeDef",
    "SrtOutputDestinationSettingsTypeDef",
    "SrtOutputSettingsTypeDef",
    "SrtSettingsRequestTypeDef",
    "SrtSettingsTypeDef",
    "StandardHlsSettingsTypeDef",
    "StartChannelRequestRequestTypeDef",
    "StartChannelResponseTypeDef",
    "StartDeleteMonitorDeploymentRequestRequestTypeDef",
    "StartDeleteMonitorDeploymentResponseTypeDef",
    "StartInputDeviceMaintenanceWindowRequestRequestTypeDef",
    "StartInputDeviceRequestRequestTypeDef",
    "StartMonitorDeploymentRequestRequestTypeDef",
    "StartMonitorDeploymentResponseTypeDef",
    "StartMultiplexRequestRequestTypeDef",
    "StartMultiplexResponseTypeDef",
    "StartTimecodeTypeDef",
    "StartUpdateSignalMapRequestRequestTypeDef",
    "StartUpdateSignalMapResponseTypeDef",
    "StaticImageActivateScheduleActionSettingsTypeDef",
    "StaticImageDeactivateScheduleActionSettingsTypeDef",
    "StaticImageOutputActivateScheduleActionSettingsOutputTypeDef",
    "StaticImageOutputActivateScheduleActionSettingsTypeDef",
    "StaticImageOutputActivateScheduleActionSettingsUnionTypeDef",
    "StaticImageOutputDeactivateScheduleActionSettingsOutputTypeDef",
    "StaticImageOutputDeactivateScheduleActionSettingsTypeDef",
    "StaticImageOutputDeactivateScheduleActionSettingsUnionTypeDef",
    "StaticKeySettingsTypeDef",
    "StopChannelRequestRequestTypeDef",
    "StopChannelResponseTypeDef",
    "StopInputDeviceRequestRequestTypeDef",
    "StopMultiplexRequestRequestTypeDef",
    "StopMultiplexResponseTypeDef",
    "StopTimecodeTypeDef",
    "SuccessfulMonitorDeploymentTypeDef",
    "TeletextSourceSettingsTypeDef",
    "TemporalFilterSettingsTypeDef",
    "ThumbnailConfigurationTypeDef",
    "ThumbnailDetailTypeDef",
    "ThumbnailTypeDef",
    "TimecodeBurninSettingsTypeDef",
    "TimecodeConfigTypeDef",
    "TransferInputDeviceRequestRequestTypeDef",
    "TransferringInputDeviceSummaryTypeDef",
    "TtmlDestinationSettingsTypeDef",
    "UdpContainerSettingsTypeDef",
    "UdpGroupSettingsTypeDef",
    "UdpOutputSettingsTypeDef",
    "UnionTypeDef",
    "UpdateAccountConfigurationRequestRequestTypeDef",
    "UpdateAccountConfigurationResponseTypeDef",
    "UpdateChannelClassRequestRequestTypeDef",
    "UpdateChannelClassResponseTypeDef",
    "UpdateChannelPlacementGroupRequestRequestTypeDef",
    "UpdateChannelPlacementGroupResponseTypeDef",
    "UpdateChannelRequestRequestTypeDef",
    "UpdateChannelResponseTypeDef",
    "UpdateCloudWatchAlarmTemplateGroupRequestRequestTypeDef",
    "UpdateCloudWatchAlarmTemplateGroupResponseTypeDef",
    "UpdateCloudWatchAlarmTemplateRequestRequestTypeDef",
    "UpdateCloudWatchAlarmTemplateResponseTypeDef",
    "UpdateClusterRequestRequestTypeDef",
    "UpdateClusterResponseTypeDef",
    "UpdateEventBridgeRuleTemplateGroupRequestRequestTypeDef",
    "UpdateEventBridgeRuleTemplateGroupResponseTypeDef",
    "UpdateEventBridgeRuleTemplateRequestRequestTypeDef",
    "UpdateEventBridgeRuleTemplateResponseTypeDef",
    "UpdateInputDeviceRequestRequestTypeDef",
    "UpdateInputDeviceResponseTypeDef",
    "UpdateInputRequestRequestTypeDef",
    "UpdateInputResponseTypeDef",
    "UpdateInputSecurityGroupRequestRequestTypeDef",
    "UpdateInputSecurityGroupResponseTypeDef",
    "UpdateMultiplexProgramRequestRequestTypeDef",
    "UpdateMultiplexProgramResponseTypeDef",
    "UpdateMultiplexRequestRequestTypeDef",
    "UpdateMultiplexResponseTypeDef",
    "UpdateNetworkRequestRequestTypeDef",
    "UpdateNetworkResponseTypeDef",
    "UpdateNodeRequestRequestTypeDef",
    "UpdateNodeResponseTypeDef",
    "UpdateNodeStateRequestRequestTypeDef",
    "UpdateNodeStateResponseTypeDef",
    "UpdateReservationRequestRequestTypeDef",
    "UpdateReservationResponseTypeDef",
    "VideoBlackFailoverSettingsTypeDef",
    "VideoCodecSettingsOutputTypeDef",
    "VideoCodecSettingsTypeDef",
    "VideoCodecSettingsUnionTypeDef",
    "VideoDescriptionOutputTypeDef",
    "VideoDescriptionTypeDef",
    "VideoDescriptionUnionTypeDef",
    "VideoSelectorColorSpaceSettingsTypeDef",
    "VideoSelectorPidTypeDef",
    "VideoSelectorProgramIdTypeDef",
    "VideoSelectorSettingsTypeDef",
    "VideoSelectorTypeDef",
    "VpcOutputSettingsDescriptionTypeDef",
    "VpcOutputSettingsTypeDef",
    "WaiterConfigTypeDef",
    "WavSettingsTypeDef",
    "WebvttDestinationSettingsTypeDef",
)

class AacSettingsTypeDef(TypedDict):
    Bitrate: NotRequired[float]
    CodingMode: NotRequired[AacCodingModeType]
    InputType: NotRequired[AacInputTypeType]
    Profile: NotRequired[AacProfileType]
    RateControlMode: NotRequired[AacRateControlModeType]
    RawFormat: NotRequired[AacRawFormatType]
    SampleRate: NotRequired[float]
    Spec: NotRequired[AacSpecType]
    VbrQuality: NotRequired[AacVbrQualityType]

class Ac3SettingsTypeDef(TypedDict):
    Bitrate: NotRequired[float]
    BitstreamMode: NotRequired[Ac3BitstreamModeType]
    CodingMode: NotRequired[Ac3CodingModeType]
    Dialnorm: NotRequired[int]
    DrcProfile: NotRequired[Ac3DrcProfileType]
    LfeFilter: NotRequired[Ac3LfeFilterType]
    MetadataControl: NotRequired[Ac3MetadataControlType]
    AttenuationControl: NotRequired[Ac3AttenuationControlType]

class AcceptInputDeviceTransferRequestRequestTypeDef(TypedDict):
    InputDeviceId: str

class AccountConfigurationTypeDef(TypedDict):
    KmsKeyId: NotRequired[str]

class AncillarySourceSettingsTypeDef(TypedDict):
    SourceAncillaryChannelNumber: NotRequired[int]

class AnywhereSettingsTypeDef(TypedDict):
    ChannelPlacementGroupId: NotRequired[str]
    ClusterId: NotRequired[str]

class ArchiveS3SettingsTypeDef(TypedDict):
    CannedAcl: NotRequired[S3CannedAclType]

class OutputLocationRefTypeDef(TypedDict):
    DestinationRefId: NotRequired[str]

class InputChannelLevelTypeDef(TypedDict):
    Gain: int
    InputChannel: int

class Eac3AtmosSettingsTypeDef(TypedDict):
    Bitrate: NotRequired[float]
    CodingMode: NotRequired[Eac3AtmosCodingModeType]
    Dialnorm: NotRequired[int]
    DrcLine: NotRequired[Eac3AtmosDrcLineType]
    DrcRf: NotRequired[Eac3AtmosDrcRfType]
    HeightTrim: NotRequired[float]
    SurroundTrim: NotRequired[float]

class Eac3SettingsTypeDef(TypedDict):
    AttenuationControl: NotRequired[Eac3AttenuationControlType]
    Bitrate: NotRequired[float]
    BitstreamMode: NotRequired[Eac3BitstreamModeType]
    CodingMode: NotRequired[Eac3CodingModeType]
    DcFilter: NotRequired[Eac3DcFilterType]
    Dialnorm: NotRequired[int]
    DrcLine: NotRequired[Eac3DrcLineType]
    DrcRf: NotRequired[Eac3DrcRfType]
    LfeControl: NotRequired[Eac3LfeControlType]
    LfeFilter: NotRequired[Eac3LfeFilterType]
    LoRoCenterMixLevel: NotRequired[float]
    LoRoSurroundMixLevel: NotRequired[float]
    LtRtCenterMixLevel: NotRequired[float]
    LtRtSurroundMixLevel: NotRequired[float]
    MetadataControl: NotRequired[Eac3MetadataControlType]
    PassthroughControl: NotRequired[Eac3PassthroughControlType]
    PhaseControl: NotRequired[Eac3PhaseControlType]
    StereoDownmix: NotRequired[Eac3StereoDownmixType]
    SurroundExMode: NotRequired[Eac3SurroundExModeType]
    SurroundMode: NotRequired[Eac3SurroundModeType]

class Mp2SettingsTypeDef(TypedDict):
    Bitrate: NotRequired[float]
    CodingMode: NotRequired[Mp2CodingModeType]
    SampleRate: NotRequired[float]

class WavSettingsTypeDef(TypedDict):
    BitDepth: NotRequired[float]
    CodingMode: NotRequired[WavCodingModeType]
    SampleRate: NotRequired[float]

class AudioNormalizationSettingsTypeDef(TypedDict):
    Algorithm: NotRequired[AudioNormalizationAlgorithmType]
    AlgorithmControl: NotRequired[Literal["CORRECT_AUDIO"]]
    TargetLkfs: NotRequired[float]

class AudioDolbyEDecodeTypeDef(TypedDict):
    ProgramSelection: DolbyEProgramSelectionType

class AudioHlsRenditionSelectionTypeDef(TypedDict):
    GroupId: str
    Name: str

class AudioLanguageSelectionTypeDef(TypedDict):
    LanguageCode: str
    LanguageSelectionPolicy: NotRequired[AudioLanguageSelectionPolicyType]

class InputLocationTypeDef(TypedDict):
    Uri: str
    PasswordParam: NotRequired[str]
    Username: NotRequired[str]

class AudioPidSelectionTypeDef(TypedDict):
    Pid: int

class AudioSilenceFailoverSettingsTypeDef(TypedDict):
    AudioSelectorName: str
    AudioSilenceThresholdMsec: NotRequired[int]

class AudioTrackTypeDef(TypedDict):
    Track: int

class Hdr10SettingsTypeDef(TypedDict):
    MaxCll: NotRequired[int]
    MaxFall: NotRequired[int]

class TimecodeBurninSettingsTypeDef(TypedDict):
    FontSize: TimecodeBurninFontSizeType
    Position: TimecodeBurninPositionType
    Prefix: NotRequired[str]

class EsamTypeDef(TypedDict):
    AcquisitionPointId: str
    PoisEndpoint: str
    AdAvailOffset: NotRequired[int]
    PasswordParam: NotRequired[str]
    Username: NotRequired[str]
    ZoneIdentity: NotRequired[str]

class Scte35SpliceInsertTypeDef(TypedDict):
    AdAvailOffset: NotRequired[int]
    NoRegionalBlackoutFlag: NotRequired[Scte35SpliceInsertNoRegionalBlackoutBehaviorType]
    WebDeliveryAllowedFlag: NotRequired[Scte35SpliceInsertWebDeliveryAllowedBehaviorType]

class Scte35TimeSignalAposTypeDef(TypedDict):
    AdAvailOffset: NotRequired[int]
    NoRegionalBlackoutFlag: NotRequired[Scte35AposNoRegionalBlackoutBehaviorType]
    WebDeliveryAllowedFlag: NotRequired[Scte35AposWebDeliveryAllowedBehaviorType]

class BandwidthReductionFilterSettingsTypeDef(TypedDict):
    PostFilterSharpening: NotRequired[BandwidthReductionPostFilterSharpeningType]
    Strength: NotRequired[BandwidthReductionFilterStrengthType]

class BatchDeleteRequestRequestTypeDef(TypedDict):
    ChannelIds: NotRequired[Sequence[str]]
    InputIds: NotRequired[Sequence[str]]
    InputSecurityGroupIds: NotRequired[Sequence[str]]
    MultiplexIds: NotRequired[Sequence[str]]

class BatchFailedResultModelTypeDef(TypedDict):
    Arn: NotRequired[str]
    Code: NotRequired[str]
    Id: NotRequired[str]
    Message: NotRequired[str]

class BatchSuccessfulResultModelTypeDef(TypedDict):
    Arn: NotRequired[str]
    Id: NotRequired[str]
    State: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BatchScheduleActionDeleteRequestTypeDef(TypedDict):
    ActionNames: Sequence[str]

class BatchStartRequestRequestTypeDef(TypedDict):
    ChannelIds: NotRequired[Sequence[str]]
    MultiplexIds: NotRequired[Sequence[str]]

class BatchStopRequestRequestTypeDef(TypedDict):
    ChannelIds: NotRequired[Sequence[str]]
    MultiplexIds: NotRequired[Sequence[str]]

class CancelInputDeviceTransferRequestRequestTypeDef(TypedDict):
    InputDeviceId: str

class EbuTtDDestinationSettingsTypeDef(TypedDict):
    CopyrightHolder: NotRequired[str]
    FillLineGap: NotRequired[EbuTtDFillLineGapControlType]
    FontFamily: NotRequired[str]
    StyleControl: NotRequired[EbuTtDDestinationStyleControlType]

class TtmlDestinationSettingsTypeDef(TypedDict):
    StyleControl: NotRequired[TtmlDestinationStyleControlType]

class WebvttDestinationSettingsTypeDef(TypedDict):
    StyleControl: NotRequired[WebvttDestinationStyleControlType]

class CaptionLanguageMappingTypeDef(TypedDict):
    CaptionChannel: int
    LanguageCode: str
    LanguageDescription: str

class CaptionRectangleTypeDef(TypedDict):
    Height: float
    LeftOffset: float
    TopOffset: float
    Width: float

class DvbSubSourceSettingsTypeDef(TypedDict):
    OcrLanguage: NotRequired[DvbSubOcrLanguageType]
    Pid: NotRequired[int]

class EmbeddedSourceSettingsTypeDef(TypedDict):
    Convert608To708: NotRequired[EmbeddedConvert608To708Type]
    Scte20Detection: NotRequired[EmbeddedScte20DetectionType]
    Source608ChannelNumber: NotRequired[int]
    Source608TrackNumber: NotRequired[int]

class Scte20SourceSettingsTypeDef(TypedDict):
    Convert608To708: NotRequired[Scte20Convert608To708Type]
    Source608ChannelNumber: NotRequired[int]

class Scte27SourceSettingsTypeDef(TypedDict):
    OcrLanguage: NotRequired[Scte27OcrLanguageType]
    Pid: NotRequired[int]

class CdiInputSpecificationTypeDef(TypedDict):
    Resolution: NotRequired[CdiInputResolutionType]

class ChannelEgressEndpointTypeDef(TypedDict):
    SourceIp: NotRequired[str]

class DescribeAnywhereSettingsTypeDef(TypedDict):
    ChannelPlacementGroupId: NotRequired[str]
    ClusterId: NotRequired[str]

class InputSpecificationTypeDef(TypedDict):
    Codec: NotRequired[InputCodecType]
    MaximumBitrate: NotRequired[InputMaximumBitrateType]
    Resolution: NotRequired[InputResolutionType]

class MaintenanceStatusTypeDef(TypedDict):
    MaintenanceDay: NotRequired[MaintenanceDayType]
    MaintenanceDeadline: NotRequired[str]
    MaintenanceScheduledDate: NotRequired[str]
    MaintenanceStartTime: NotRequired[str]

class VpcOutputSettingsDescriptionTypeDef(TypedDict):
    AvailabilityZones: NotRequired[List[str]]
    NetworkInterfaceIds: NotRequired[List[str]]
    SecurityGroupIds: NotRequired[List[str]]
    SubnetIds: NotRequired[List[str]]

class PipelineDetailTypeDef(TypedDict):
    ActiveInputAttachmentName: NotRequired[str]
    ActiveInputSwitchActionName: NotRequired[str]
    ActiveMotionGraphicsActionName: NotRequired[str]
    ActiveMotionGraphicsUri: NotRequired[str]
    PipelineId: NotRequired[str]

class ClaimDeviceRequestRequestTypeDef(TypedDict):
    Id: NotRequired[str]

class CloudWatchAlarmTemplateGroupSummaryTypeDef(TypedDict):
    Arn: str
    CreatedAt: datetime
    Id: str
    Name: str
    TemplateCount: int
    Description: NotRequired[str]
    ModifiedAt: NotRequired[datetime]
    Tags: NotRequired[Dict[str, str]]

class CloudWatchAlarmTemplateSummaryTypeDef(TypedDict):
    Arn: str
    ComparisonOperator: CloudWatchAlarmTemplateComparisonOperatorType
    CreatedAt: datetime
    EvaluationPeriods: int
    GroupId: str
    Id: str
    MetricName: str
    Name: str
    Period: int
    Statistic: CloudWatchAlarmTemplateStatisticType
    TargetResourceType: CloudWatchAlarmTemplateTargetResourceTypeType
    Threshold: float
    TreatMissingData: CloudWatchAlarmTemplateTreatMissingDataType
    DatapointsToAlarm: NotRequired[int]
    Description: NotRequired[str]
    ModifiedAt: NotRequired[datetime]
    Tags: NotRequired[Dict[str, str]]

class InterfaceMappingCreateRequestTypeDef(TypedDict):
    LogicalInterfaceName: NotRequired[str]
    NetworkId: NotRequired[str]

class InterfaceMappingTypeDef(TypedDict):
    LogicalInterfaceName: NotRequired[str]
    NetworkId: NotRequired[str]

class InterfaceMappingUpdateRequestTypeDef(TypedDict):
    LogicalInterfaceName: NotRequired[str]
    NetworkId: NotRequired[str]

class CmafIngestOutputSettingsTypeDef(TypedDict):
    NameModifier: NotRequired[str]

class ColorCorrectionTypeDef(TypedDict):
    InputColorSpace: ColorSpaceType
    OutputColorSpace: ColorSpaceType
    Uri: str

class CreateChannelPlacementGroupRequestRequestTypeDef(TypedDict):
    ClusterId: str
    Name: NotRequired[str]
    Nodes: NotRequired[Sequence[str]]
    RequestId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class MaintenanceCreateSettingsTypeDef(TypedDict):
    MaintenanceDay: NotRequired[MaintenanceDayType]
    MaintenanceStartTime: NotRequired[str]

class VpcOutputSettingsTypeDef(TypedDict):
    SubnetIds: Sequence[str]
    PublicAddressAllocationIds: NotRequired[Sequence[str]]
    SecurityGroupIds: NotRequired[Sequence[str]]

class CreateCloudWatchAlarmTemplateGroupRequestRequestTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class CreateCloudWatchAlarmTemplateRequestRequestTypeDef(TypedDict):
    ComparisonOperator: CloudWatchAlarmTemplateComparisonOperatorType
    EvaluationPeriods: int
    GroupIdentifier: str
    MetricName: str
    Name: str
    Period: int
    Statistic: CloudWatchAlarmTemplateStatisticType
    TargetResourceType: CloudWatchAlarmTemplateTargetResourceTypeType
    Threshold: float
    TreatMissingData: CloudWatchAlarmTemplateTreatMissingDataType
    DatapointsToAlarm: NotRequired[int]
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class CreateEventBridgeRuleTemplateGroupRequestRequestTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class EventBridgeRuleTemplateTargetTypeDef(TypedDict):
    Arn: str

class InputDeviceSettingsTypeDef(TypedDict):
    Id: NotRequired[str]

class InputSourceRequestTypeDef(TypedDict):
    PasswordParam: NotRequired[str]
    Url: NotRequired[str]
    Username: NotRequired[str]

class InputVpcRequestTypeDef(TypedDict):
    SubnetIds: Sequence[str]
    SecurityGroupIds: NotRequired[Sequence[str]]

class MediaConnectFlowRequestTypeDef(TypedDict):
    FlowArn: NotRequired[str]

class InputWhitelistRuleCidrTypeDef(TypedDict):
    Cidr: NotRequired[str]

class MultiplexSettingsTypeDef(TypedDict):
    TransportStreamBitrate: int
    TransportStreamId: int
    MaximumVideoBufferDelayMilliseconds: NotRequired[int]
    TransportStreamReservedBitrate: NotRequired[int]

class IpPoolCreateRequestTypeDef(TypedDict):
    Cidr: NotRequired[str]

class RouteCreateRequestTypeDef(TypedDict):
    Cidr: NotRequired[str]
    Gateway: NotRequired[str]

class IpPoolTypeDef(TypedDict):
    Cidr: NotRequired[str]

class RouteTypeDef(TypedDict):
    Cidr: NotRequired[str]
    Gateway: NotRequired[str]

class NodeInterfaceMappingTypeDef(TypedDict):
    LogicalInterfaceName: NotRequired[str]
    NetworkInterfaceMode: NotRequired[NetworkInterfaceModeType]
    PhysicalInterfaceName: NotRequired[str]

class NodeInterfaceMappingCreateRequestTypeDef(TypedDict):
    LogicalInterfaceName: NotRequired[str]
    NetworkInterfaceMode: NotRequired[NetworkInterfaceModeType]
    PhysicalInterfaceName: NotRequired[str]

class CreatePartnerInputRequestRequestTypeDef(TypedDict):
    InputId: str
    RequestId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class CreateSignalMapRequestRequestTypeDef(TypedDict):
    DiscoveryEntryPointArn: str
    Name: str
    CloudWatchAlarmTemplateGroupIdentifiers: NotRequired[Sequence[str]]
    Description: NotRequired[str]
    EventBridgeRuleTemplateGroupIdentifiers: NotRequired[Sequence[str]]
    Tags: NotRequired[Mapping[str, str]]

class MonitorDeploymentTypeDef(TypedDict):
    Status: SignalMapMonitorDeploymentStatusType
    DetailsUri: NotRequired[str]
    ErrorMessage: NotRequired[str]

class SuccessfulMonitorDeploymentTypeDef(TypedDict):
    DetailsUri: str
    Status: SignalMapMonitorDeploymentStatusType

class CreateTagsRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: NotRequired[Mapping[str, str]]

class DeleteChannelPlacementGroupRequestRequestTypeDef(TypedDict):
    ChannelPlacementGroupId: str
    ClusterId: str

class DeleteChannelRequestRequestTypeDef(TypedDict):
    ChannelId: str

class DeleteCloudWatchAlarmTemplateGroupRequestRequestTypeDef(TypedDict):
    Identifier: str

class DeleteCloudWatchAlarmTemplateRequestRequestTypeDef(TypedDict):
    Identifier: str

class DeleteClusterRequestRequestTypeDef(TypedDict):
    ClusterId: str

class DeleteEventBridgeRuleTemplateGroupRequestRequestTypeDef(TypedDict):
    Identifier: str

class DeleteEventBridgeRuleTemplateRequestRequestTypeDef(TypedDict):
    Identifier: str

class DeleteInputRequestRequestTypeDef(TypedDict):
    InputId: str

class DeleteInputSecurityGroupRequestRequestTypeDef(TypedDict):
    InputSecurityGroupId: str

class DeleteMultiplexProgramRequestRequestTypeDef(TypedDict):
    MultiplexId: str
    ProgramName: str

class MultiplexProgramPacketIdentifiersMapOutputTypeDef(TypedDict):
    AudioPids: NotRequired[List[int]]
    DvbSubPids: NotRequired[List[int]]
    DvbTeletextPid: NotRequired[int]
    EtvPlatformPid: NotRequired[int]
    EtvSignalPid: NotRequired[int]
    KlvDataPids: NotRequired[List[int]]
    PcrPid: NotRequired[int]
    PmtPid: NotRequired[int]
    PrivateMetadataPid: NotRequired[int]
    Scte27Pids: NotRequired[List[int]]
    Scte35Pid: NotRequired[int]
    TimedMetadataPid: NotRequired[int]
    VideoPid: NotRequired[int]
    AribCaptionsPid: NotRequired[int]
    DvbTeletextPids: NotRequired[List[int]]
    EcmPid: NotRequired[int]
    Smpte2038Pid: NotRequired[int]

class MultiplexProgramPipelineDetailTypeDef(TypedDict):
    ActiveChannelPipeline: NotRequired[str]
    PipelineId: NotRequired[str]

class DeleteMultiplexRequestRequestTypeDef(TypedDict):
    MultiplexId: str

class DeleteNetworkRequestRequestTypeDef(TypedDict):
    NetworkId: str

class DeleteNodeRequestRequestTypeDef(TypedDict):
    ClusterId: str
    NodeId: str

class DeleteReservationRequestRequestTypeDef(TypedDict):
    ReservationId: str

class RenewalSettingsTypeDef(TypedDict):
    AutomaticRenewal: NotRequired[ReservationAutomaticRenewalType]
    RenewalCount: NotRequired[int]

class ReservationResourceSpecificationTypeDef(TypedDict):
    ChannelClass: NotRequired[ChannelClassType]
    Codec: NotRequired[ReservationCodecType]
    MaximumBitrate: NotRequired[ReservationMaximumBitrateType]
    MaximumFramerate: NotRequired[ReservationMaximumFramerateType]
    Resolution: NotRequired[ReservationResolutionType]
    ResourceType: NotRequired[ReservationResourceTypeType]
    SpecialFeature: NotRequired[ReservationSpecialFeatureType]
    VideoQuality: NotRequired[ReservationVideoQualityType]

class DeleteScheduleRequestRequestTypeDef(TypedDict):
    ChannelId: str

class DeleteSignalMapRequestRequestTypeDef(TypedDict):
    Identifier: str

class DeleteTagsRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class DescribeChannelPlacementGroupRequestRequestTypeDef(TypedDict):
    ChannelPlacementGroupId: str
    ClusterId: str

class DescribeChannelPlacementGroupSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    Channels: NotRequired[List[str]]
    ClusterId: NotRequired[str]
    Id: NotRequired[str]
    Name: NotRequired[str]
    Nodes: NotRequired[List[str]]
    State: NotRequired[ChannelPlacementGroupStateType]

class DescribeChannelRequestRequestTypeDef(TypedDict):
    ChannelId: str

class DescribeClusterRequestRequestTypeDef(TypedDict):
    ClusterId: str

class DescribeInputDeviceRequestRequestTypeDef(TypedDict):
    InputDeviceId: str

class InputDeviceHdSettingsTypeDef(TypedDict):
    ActiveInput: NotRequired[InputDeviceActiveInputType]
    ConfiguredInput: NotRequired[InputDeviceConfiguredInputType]
    DeviceState: NotRequired[InputDeviceStateType]
    Framerate: NotRequired[float]
    Height: NotRequired[int]
    MaxBitrate: NotRequired[int]
    ScanType: NotRequired[InputDeviceScanTypeType]
    Width: NotRequired[int]
    LatencyMs: NotRequired[int]

class InputDeviceNetworkSettingsTypeDef(TypedDict):
    DnsAddresses: NotRequired[List[str]]
    Gateway: NotRequired[str]
    IpAddress: NotRequired[str]
    IpScheme: NotRequired[InputDeviceIpSchemeType]
    SubnetMask: NotRequired[str]

class DescribeInputDeviceThumbnailRequestRequestTypeDef(TypedDict):
    InputDeviceId: str
    Accept: Literal["image/jpeg"]

class DescribeInputRequestRequestTypeDef(TypedDict):
    InputId: str

class InputSourceTypeDef(TypedDict):
    PasswordParam: NotRequired[str]
    Url: NotRequired[str]
    Username: NotRequired[str]

class MediaConnectFlowTypeDef(TypedDict):
    FlowArn: NotRequired[str]

class DescribeInputSecurityGroupRequestRequestTypeDef(TypedDict):
    InputSecurityGroupId: str

class InputWhitelistRuleTypeDef(TypedDict):
    Cidr: NotRequired[str]

class DescribeMultiplexProgramRequestRequestTypeDef(TypedDict):
    MultiplexId: str
    ProgramName: str

class DescribeMultiplexRequestRequestTypeDef(TypedDict):
    MultiplexId: str

class DescribeNetworkRequestRequestTypeDef(TypedDict):
    NetworkId: str

class DescribeNodeRequestRequestTypeDef(TypedDict):
    ClusterId: str
    NodeId: str

class DescribeOfferingRequestRequestTypeDef(TypedDict):
    OfferingId: str

class DescribeReservationRequestRequestTypeDef(TypedDict):
    ReservationId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeScheduleRequestRequestTypeDef(TypedDict):
    ChannelId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeThumbnailsRequestRequestTypeDef(TypedDict):
    ChannelId: str
    PipelineId: str
    ThumbnailType: str

class DvbNitSettingsTypeDef(TypedDict):
    NetworkId: int
    NetworkName: str
    RepInterval: NotRequired[int]

DvbSdtSettingsTypeDef = TypedDict(
    "DvbSdtSettingsTypeDef",
    {
        "OutputSdt": NotRequired[DvbSdtOutputSdtType],
        "RepInterval": NotRequired[int],
        "ServiceName": NotRequired[str],
        "ServiceProviderName": NotRequired[str],
    },
)

class DvbTdtSettingsTypeDef(TypedDict):
    RepInterval: NotRequired[int]

class FeatureActivationsTypeDef(TypedDict):
    InputPrepareScheduleActions: NotRequired[FeatureActivationsInputPrepareScheduleActionsType]
    OutputStaticImageOverlayScheduleActions: NotRequired[
        FeatureActivationsOutputStaticImageOverlayScheduleActionsType
    ]

class NielsenConfigurationTypeDef(TypedDict):
    DistributorId: NotRequired[str]
    NielsenPcmToId3Tagging: NotRequired[NielsenPcmToId3TaggingStateType]

class ThumbnailConfigurationTypeDef(TypedDict):
    State: ThumbnailStateType

class TimecodeConfigTypeDef(TypedDict):
    Source: TimecodeConfigSourceType
    SyncThreshold: NotRequired[int]

class EpochLockingSettingsTypeDef(TypedDict):
    CustomEpoch: NotRequired[str]
    JamSyncTime: NotRequired[str]

class EventBridgeRuleTemplateGroupSummaryTypeDef(TypedDict):
    Arn: str
    CreatedAt: datetime
    Id: str
    Name: str
    TemplateCount: int
    Description: NotRequired[str]
    ModifiedAt: NotRequired[datetime]
    Tags: NotRequired[Dict[str, str]]

class EventBridgeRuleTemplateSummaryTypeDef(TypedDict):
    Arn: str
    CreatedAt: datetime
    EventTargetCount: int
    EventType: EventBridgeRuleTemplateEventTypeType
    GroupId: str
    Id: str
    Name: str
    Description: NotRequired[str]
    ModifiedAt: NotRequired[datetime]
    Tags: NotRequired[Dict[str, str]]

class InputLossFailoverSettingsTypeDef(TypedDict):
    InputLossThresholdMsec: NotRequired[int]

class VideoBlackFailoverSettingsTypeDef(TypedDict):
    BlackDetectThreshold: NotRequired[float]
    VideoBlackThresholdMsec: NotRequired[int]

class FecOutputSettingsTypeDef(TypedDict):
    ColumnDepth: NotRequired[int]
    IncludeFec: NotRequired[FecOutputIncludeFecType]
    RowLength: NotRequired[int]

class FixedModeScheduleActionStartSettingsTypeDef(TypedDict):
    Time: str

class Fmp4HlsSettingsTypeDef(TypedDict):
    AudioRenditionSets: NotRequired[str]
    NielsenId3Behavior: NotRequired[Fmp4NielsenId3BehaviorType]
    TimedMetadataBehavior: NotRequired[Fmp4TimedMetadataBehaviorType]

class FollowModeScheduleActionStartSettingsTypeDef(TypedDict):
    FollowPoint: FollowPointType
    ReferenceActionName: str

class FrameCaptureS3SettingsTypeDef(TypedDict):
    CannedAcl: NotRequired[S3CannedAclType]

class FrameCaptureOutputSettingsTypeDef(TypedDict):
    NameModifier: NotRequired[str]

class GetCloudWatchAlarmTemplateGroupRequestRequestTypeDef(TypedDict):
    Identifier: str

class GetCloudWatchAlarmTemplateRequestRequestTypeDef(TypedDict):
    Identifier: str

class GetEventBridgeRuleTemplateGroupRequestRequestTypeDef(TypedDict):
    Identifier: str

class GetEventBridgeRuleTemplateRequestRequestTypeDef(TypedDict):
    Identifier: str

class GetSignalMapRequestRequestTypeDef(TypedDict):
    Identifier: str

class H264ColorSpaceSettingsOutputTypeDef(TypedDict):
    ColorSpacePassthroughSettings: NotRequired[Dict[str, Any]]
    Rec601Settings: NotRequired[Dict[str, Any]]
    Rec709Settings: NotRequired[Dict[str, Any]]

class H264ColorSpaceSettingsTypeDef(TypedDict):
    ColorSpacePassthroughSettings: NotRequired[Mapping[str, Any]]
    Rec601Settings: NotRequired[Mapping[str, Any]]
    Rec709Settings: NotRequired[Mapping[str, Any]]

class TemporalFilterSettingsTypeDef(TypedDict):
    PostFilterSharpening: NotRequired[TemporalFilterPostFilterSharpeningType]
    Strength: NotRequired[TemporalFilterStrengthType]

class HlsAkamaiSettingsTypeDef(TypedDict):
    ConnectionRetryInterval: NotRequired[int]
    FilecacheDuration: NotRequired[int]
    HttpTransferMode: NotRequired[HlsAkamaiHttpTransferModeType]
    NumRetries: NotRequired[int]
    RestartDelay: NotRequired[int]
    Salt: NotRequired[str]
    Token: NotRequired[str]

class HlsBasicPutSettingsTypeDef(TypedDict):
    ConnectionRetryInterval: NotRequired[int]
    FilecacheDuration: NotRequired[int]
    NumRetries: NotRequired[int]
    RestartDelay: NotRequired[int]

class HlsMediaStoreSettingsTypeDef(TypedDict):
    ConnectionRetryInterval: NotRequired[int]
    FilecacheDuration: NotRequired[int]
    MediaStoreStorageClass: NotRequired[Literal["TEMPORAL"]]
    NumRetries: NotRequired[int]
    RestartDelay: NotRequired[int]

class HlsS3SettingsTypeDef(TypedDict):
    CannedAcl: NotRequired[S3CannedAclType]

class HlsWebdavSettingsTypeDef(TypedDict):
    ConnectionRetryInterval: NotRequired[int]
    FilecacheDuration: NotRequired[int]
    HttpTransferMode: NotRequired[HlsWebdavHttpTransferModeType]
    NumRetries: NotRequired[int]
    RestartDelay: NotRequired[int]

class HlsId3SegmentTaggingScheduleActionSettingsTypeDef(TypedDict):
    Tag: NotRequired[str]
    Id3: NotRequired[str]

class HlsInputSettingsTypeDef(TypedDict):
    Bandwidth: NotRequired[int]
    BufferSegments: NotRequired[int]
    Retries: NotRequired[int]
    RetryInterval: NotRequired[int]
    Scte35Source: NotRequired[HlsScte35SourceTypeType]

class HlsTimedMetadataScheduleActionSettingsTypeDef(TypedDict):
    Id3: str

class StartTimecodeTypeDef(TypedDict):
    Timecode: NotRequired[str]

class StopTimecodeTypeDef(TypedDict):
    LastFrameClippingBehavior: NotRequired[LastFrameClippingBehaviorType]
    Timecode: NotRequired[str]

class InputRequestDestinationRouteTypeDef(TypedDict):
    Cidr: NotRequired[str]
    Gateway: NotRequired[str]

class InputDestinationRouteTypeDef(TypedDict):
    Cidr: NotRequired[str]
    Gateway: NotRequired[str]

class InputDestinationVpcTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]

class InputDeviceConfigurableAudioChannelPairConfigTypeDef(TypedDict):
    Id: NotRequired[int]
    Profile: NotRequired[InputDeviceConfigurableAudioChannelPairProfileType]

class InputDeviceMediaConnectConfigurableSettingsTypeDef(TypedDict):
    FlowArn: NotRequired[str]
    RoleArn: NotRequired[str]
    SecretArn: NotRequired[str]
    SourceName: NotRequired[str]

class InputDeviceMediaConnectSettingsTypeDef(TypedDict):
    FlowArn: NotRequired[str]
    RoleArn: NotRequired[str]
    SecretArn: NotRequired[str]
    SourceName: NotRequired[str]

class InputDeviceRequestTypeDef(TypedDict):
    Id: NotRequired[str]

class InputDeviceUhdAudioChannelPairConfigTypeDef(TypedDict):
    Id: NotRequired[int]
    Profile: NotRequired[InputDeviceUhdAudioChannelPairProfileType]

class IpPoolUpdateRequestTypeDef(TypedDict):
    Cidr: NotRequired[str]

class ListChannelPlacementGroupsRequestRequestTypeDef(TypedDict):
    ClusterId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListChannelsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListCloudWatchAlarmTemplateGroupsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Scope: NotRequired[str]
    SignalMapIdentifier: NotRequired[str]

class ListCloudWatchAlarmTemplatesRequestRequestTypeDef(TypedDict):
    GroupIdentifier: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Scope: NotRequired[str]
    SignalMapIdentifier: NotRequired[str]

class ListClustersRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListEventBridgeRuleTemplateGroupsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    SignalMapIdentifier: NotRequired[str]

class ListEventBridgeRuleTemplatesRequestRequestTypeDef(TypedDict):
    GroupIdentifier: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    SignalMapIdentifier: NotRequired[str]

class ListInputDeviceTransfersRequestRequestTypeDef(TypedDict):
    TransferType: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class TransferringInputDeviceSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Message: NotRequired[str]
    TargetCustomerId: NotRequired[str]
    TransferType: NotRequired[InputDeviceTransferTypeType]

class ListInputDevicesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListInputSecurityGroupsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListInputsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListMultiplexProgramsRequestRequestTypeDef(TypedDict):
    MultiplexId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class MultiplexProgramSummaryTypeDef(TypedDict):
    ChannelId: NotRequired[str]
    ProgramName: NotRequired[str]

class ListMultiplexesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListNetworksRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListNodesRequestRequestTypeDef(TypedDict):
    ClusterId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListOfferingsRequestRequestTypeDef(TypedDict):
    ChannelClass: NotRequired[str]
    ChannelConfiguration: NotRequired[str]
    Codec: NotRequired[str]
    Duration: NotRequired[str]
    MaxResults: NotRequired[int]
    MaximumBitrate: NotRequired[str]
    MaximumFramerate: NotRequired[str]
    NextToken: NotRequired[str]
    Resolution: NotRequired[str]
    ResourceType: NotRequired[str]
    SpecialFeature: NotRequired[str]
    VideoQuality: NotRequired[str]

class ListReservationsRequestRequestTypeDef(TypedDict):
    ChannelClass: NotRequired[str]
    Codec: NotRequired[str]
    MaxResults: NotRequired[int]
    MaximumBitrate: NotRequired[str]
    MaximumFramerate: NotRequired[str]
    NextToken: NotRequired[str]
    Resolution: NotRequired[str]
    ResourceType: NotRequired[str]
    SpecialFeature: NotRequired[str]
    VideoQuality: NotRequired[str]

class ListSignalMapsRequestRequestTypeDef(TypedDict):
    CloudWatchAlarmTemplateGroupIdentifier: NotRequired[str]
    EventBridgeRuleTemplateGroupIdentifier: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class SignalMapSummaryTypeDef(TypedDict):
    Arn: str
    CreatedAt: datetime
    Id: str
    MonitorDeploymentStatus: SignalMapMonitorDeploymentStatusType
    Name: str
    Status: SignalMapStatusType
    Description: NotRequired[str]
    ModifiedAt: NotRequired[datetime]
    Tags: NotRequired[Dict[str, str]]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class M3u8SettingsTypeDef(TypedDict):
    AudioFramesPerPes: NotRequired[int]
    AudioPids: NotRequired[str]
    EcmPid: NotRequired[str]
    NielsenId3Behavior: NotRequired[M3u8NielsenId3BehaviorType]
    PatInterval: NotRequired[int]
    PcrControl: NotRequired[M3u8PcrControlType]
    PcrPeriod: NotRequired[int]
    PcrPid: NotRequired[str]
    PmtInterval: NotRequired[int]
    PmtPid: NotRequired[str]
    ProgramNum: NotRequired[int]
    Scte35Behavior: NotRequired[M3u8Scte35BehaviorType]
    Scte35Pid: NotRequired[str]
    TimedMetadataBehavior: NotRequired[M3u8TimedMetadataBehaviorType]
    TimedMetadataPid: NotRequired[str]
    TransportStreamId: NotRequired[int]
    VideoPid: NotRequired[str]
    KlvBehavior: NotRequired[M3u8KlvBehaviorType]
    KlvDataPids: NotRequired[str]

class MaintenanceUpdateSettingsTypeDef(TypedDict):
    MaintenanceDay: NotRequired[MaintenanceDayType]
    MaintenanceScheduledDate: NotRequired[str]
    MaintenanceStartTime: NotRequired[str]

class MediaPackageOutputDestinationSettingsTypeDef(TypedDict):
    ChannelId: NotRequired[str]

class MediaResourceNeighborTypeDef(TypedDict):
    Arn: str
    Name: NotRequired[str]

class MotionGraphicsActivateScheduleActionSettingsTypeDef(TypedDict):
    Duration: NotRequired[int]
    PasswordParam: NotRequired[str]
    Url: NotRequired[str]
    Username: NotRequired[str]

class MotionGraphicsSettingsOutputTypeDef(TypedDict):
    HtmlMotionGraphicsSettings: NotRequired[Dict[str, Any]]

class MotionGraphicsSettingsTypeDef(TypedDict):
    HtmlMotionGraphicsSettings: NotRequired[Mapping[str, Any]]

class MsSmoothOutputSettingsTypeDef(TypedDict):
    H265PackagingType: NotRequired[MsSmoothH265PackagingTypeType]
    NameModifier: NotRequired[str]

class MulticastInputSettingsTypeDef(TypedDict):
    SourceIpAddress: NotRequired[str]

class MulticastSourceCreateRequestTypeDef(TypedDict):
    Url: str
    SourceIp: NotRequired[str]

class MulticastSourceTypeDef(TypedDict):
    Url: str
    SourceIp: NotRequired[str]

class MulticastSourceUpdateRequestTypeDef(TypedDict):
    Url: str
    SourceIp: NotRequired[str]

class MultiplexM2tsSettingsTypeDef(TypedDict):
    AbsentInputAudioBehavior: NotRequired[M2tsAbsentInputAudioBehaviorType]
    Arib: NotRequired[M2tsAribType]
    AudioBufferModel: NotRequired[M2tsAudioBufferModelType]
    AudioFramesPerPes: NotRequired[int]
    AudioStreamType: NotRequired[M2tsAudioStreamTypeType]
    CcDescriptor: NotRequired[M2tsCcDescriptorType]
    Ebif: NotRequired[M2tsEbifControlType]
    EsRateInPes: NotRequired[M2tsEsRateInPesType]
    Klv: NotRequired[M2tsKlvType]
    NielsenId3Behavior: NotRequired[M2tsNielsenId3BehaviorType]
    PcrControl: NotRequired[M2tsPcrControlType]
    PcrPeriod: NotRequired[int]
    Scte35Control: NotRequired[M2tsScte35ControlType]
    Scte35PrerollPullupMilliseconds: NotRequired[float]

class MultiplexMediaConnectOutputDestinationSettingsTypeDef(TypedDict):
    EntitlementArn: NotRequired[str]

class MultiplexProgramChannelDestinationSettingsTypeDef(TypedDict):
    MultiplexId: NotRequired[str]
    ProgramName: NotRequired[str]

class MultiplexProgramPacketIdentifiersMapTypeDef(TypedDict):
    AudioPids: NotRequired[Sequence[int]]
    DvbSubPids: NotRequired[Sequence[int]]
    DvbTeletextPid: NotRequired[int]
    EtvPlatformPid: NotRequired[int]
    EtvSignalPid: NotRequired[int]
    KlvDataPids: NotRequired[Sequence[int]]
    PcrPid: NotRequired[int]
    PmtPid: NotRequired[int]
    PrivateMetadataPid: NotRequired[int]
    Scte27Pids: NotRequired[Sequence[int]]
    Scte35Pid: NotRequired[int]
    TimedMetadataPid: NotRequired[int]
    VideoPid: NotRequired[int]
    AribCaptionsPid: NotRequired[int]
    DvbTeletextPids: NotRequired[Sequence[int]]
    EcmPid: NotRequired[int]
    Smpte2038Pid: NotRequired[int]

MultiplexProgramServiceDescriptorTypeDef = TypedDict(
    "MultiplexProgramServiceDescriptorTypeDef",
    {
        "ProviderName": str,
        "ServiceName": str,
    },
)

class MultiplexSettingsSummaryTypeDef(TypedDict):
    TransportStreamBitrate: NotRequired[int]

class MultiplexStatmuxVideoSettingsTypeDef(TypedDict):
    MaximumBitrate: NotRequired[int]
    MinimumBitrate: NotRequired[int]
    Priority: NotRequired[int]

class NielsenCBETTypeDef(TypedDict):
    CbetCheckDigitString: str
    CbetStepaside: NielsenWatermarksCbetStepasideType
    Csid: str

class NielsenNaesIiNwTypeDef(TypedDict):
    CheckDigitString: str
    Sid: float
    Timezone: NotRequired[NielsenWatermarkTimezonesType]

class OutputDestinationSettingsTypeDef(TypedDict):
    PasswordParam: NotRequired[str]
    StreamName: NotRequired[str]
    Url: NotRequired[str]
    Username: NotRequired[str]

class SrtOutputDestinationSettingsTypeDef(TypedDict):
    EncryptionPassphraseSecretArn: NotRequired[str]
    StreamId: NotRequired[str]
    Url: NotRequired[str]

class RtmpGroupSettingsOutputTypeDef(TypedDict):
    AdMarkers: NotRequired[List[Literal["ON_CUE_POINT_SCTE35"]]]
    AuthenticationScheme: NotRequired[AuthenticationSchemeType]
    CacheFullBehavior: NotRequired[RtmpCacheFullBehaviorType]
    CacheLength: NotRequired[int]
    CaptionData: NotRequired[RtmpCaptionDataType]
    InputLossAction: NotRequired[InputLossActionForRtmpOutType]
    RestartDelay: NotRequired[int]
    IncludeFillerNalUnits: NotRequired[IncludeFillerNalUnitsType]

class SrtGroupSettingsTypeDef(TypedDict):
    InputLossAction: NotRequired[InputLossActionForUdpOutType]

class UdpGroupSettingsTypeDef(TypedDict):
    InputLossAction: NotRequired[InputLossActionForUdpOutType]
    TimedMetadataId3Frame: NotRequired[UdpTimedMetadataId3FrameType]
    TimedMetadataId3Period: NotRequired[int]

class PipelinePauseStateSettingsTypeDef(TypedDict):
    PipelineId: PipelineIdType

class RebootInputDeviceRequestRequestTypeDef(TypedDict):
    InputDeviceId: str
    Force: NotRequired[RebootInputDeviceForceType]

class RejectInputDeviceTransferRequestRequestTypeDef(TypedDict):
    InputDeviceId: str

class RestartChannelPipelinesRequestRequestTypeDef(TypedDict):
    ChannelId: str
    PipelineIds: NotRequired[Sequence[ChannelPipelineIdToRestartType]]

class RouteUpdateRequestTypeDef(TypedDict):
    Cidr: NotRequired[str]
    Gateway: NotRequired[str]

class RtmpGroupSettingsTypeDef(TypedDict):
    AdMarkers: NotRequired[Sequence[Literal["ON_CUE_POINT_SCTE35"]]]
    AuthenticationScheme: NotRequired[AuthenticationSchemeType]
    CacheFullBehavior: NotRequired[RtmpCacheFullBehaviorType]
    CacheLength: NotRequired[int]
    CaptionData: NotRequired[RtmpCaptionDataType]
    InputLossAction: NotRequired[InputLossActionForRtmpOutType]
    RestartDelay: NotRequired[int]
    IncludeFillerNalUnits: NotRequired[IncludeFillerNalUnitsType]

class Scte35InputScheduleActionSettingsTypeDef(TypedDict):
    Mode: Scte35InputModeType
    InputAttachmentNameReference: NotRequired[str]

class Scte35ReturnToNetworkScheduleActionSettingsTypeDef(TypedDict):
    SpliceEventId: int

class Scte35SpliceInsertScheduleActionSettingsTypeDef(TypedDict):
    SpliceEventId: int
    Duration: NotRequired[int]

class StaticImageDeactivateScheduleActionSettingsTypeDef(TypedDict):
    FadeOut: NotRequired[int]
    Layer: NotRequired[int]

class StaticImageOutputDeactivateScheduleActionSettingsOutputTypeDef(TypedDict):
    OutputNames: List[str]
    FadeOut: NotRequired[int]
    Layer: NotRequired[int]

class Scte35DeliveryRestrictionsTypeDef(TypedDict):
    ArchiveAllowedFlag: Scte35ArchiveAllowedFlagType
    DeviceRestrictions: Scte35DeviceRestrictionsType
    NoRegionalBlackoutFlag: Scte35NoRegionalBlackoutFlagType
    WebDeliveryAllowedFlag: Scte35WebDeliveryAllowedFlagType

class SrtCallerDecryptionRequestTypeDef(TypedDict):
    Algorithm: NotRequired[AlgorithmType]
    PassphraseSecretArn: NotRequired[str]

class SrtCallerDecryptionTypeDef(TypedDict):
    Algorithm: NotRequired[AlgorithmType]
    PassphraseSecretArn: NotRequired[str]

class StartChannelRequestRequestTypeDef(TypedDict):
    ChannelId: str

class StartDeleteMonitorDeploymentRequestRequestTypeDef(TypedDict):
    Identifier: str

class StartInputDeviceMaintenanceWindowRequestRequestTypeDef(TypedDict):
    InputDeviceId: str

class StartInputDeviceRequestRequestTypeDef(TypedDict):
    InputDeviceId: str

class StartMonitorDeploymentRequestRequestTypeDef(TypedDict):
    Identifier: str
    DryRun: NotRequired[bool]

class StartMultiplexRequestRequestTypeDef(TypedDict):
    MultiplexId: str

class StartUpdateSignalMapRequestRequestTypeDef(TypedDict):
    Identifier: str
    CloudWatchAlarmTemplateGroupIdentifiers: NotRequired[Sequence[str]]
    Description: NotRequired[str]
    DiscoveryEntryPointArn: NotRequired[str]
    EventBridgeRuleTemplateGroupIdentifiers: NotRequired[Sequence[str]]
    ForceRediscovery: NotRequired[bool]
    Name: NotRequired[str]

class StaticImageOutputDeactivateScheduleActionSettingsTypeDef(TypedDict):
    OutputNames: Sequence[str]
    FadeOut: NotRequired[int]
    Layer: NotRequired[int]

class StopChannelRequestRequestTypeDef(TypedDict):
    ChannelId: str

class StopInputDeviceRequestRequestTypeDef(TypedDict):
    InputDeviceId: str

class StopMultiplexRequestRequestTypeDef(TypedDict):
    MultiplexId: str

class ThumbnailTypeDef(TypedDict):
    Body: NotRequired[str]
    ContentType: NotRequired[str]
    ThumbnailType: NotRequired[ThumbnailTypeType]
    TimeStamp: NotRequired[datetime]

class TransferInputDeviceRequestRequestTypeDef(TypedDict):
    InputDeviceId: str
    TargetCustomerId: NotRequired[str]
    TargetRegion: NotRequired[str]
    TransferMessage: NotRequired[str]

class UpdateChannelPlacementGroupRequestRequestTypeDef(TypedDict):
    ChannelPlacementGroupId: str
    ClusterId: str
    Name: NotRequired[str]
    Nodes: NotRequired[Sequence[str]]

class UpdateCloudWatchAlarmTemplateGroupRequestRequestTypeDef(TypedDict):
    Identifier: str
    Description: NotRequired[str]

class UpdateCloudWatchAlarmTemplateRequestRequestTypeDef(TypedDict):
    Identifier: str
    ComparisonOperator: NotRequired[CloudWatchAlarmTemplateComparisonOperatorType]
    DatapointsToAlarm: NotRequired[int]
    Description: NotRequired[str]
    EvaluationPeriods: NotRequired[int]
    GroupIdentifier: NotRequired[str]
    MetricName: NotRequired[str]
    Name: NotRequired[str]
    Period: NotRequired[int]
    Statistic: NotRequired[CloudWatchAlarmTemplateStatisticType]
    TargetResourceType: NotRequired[CloudWatchAlarmTemplateTargetResourceTypeType]
    Threshold: NotRequired[float]
    TreatMissingData: NotRequired[CloudWatchAlarmTemplateTreatMissingDataType]

class UpdateEventBridgeRuleTemplateGroupRequestRequestTypeDef(TypedDict):
    Identifier: str
    Description: NotRequired[str]

class UpdateNodeRequestRequestTypeDef(TypedDict):
    ClusterId: str
    NodeId: str
    Name: NotRequired[str]
    Role: NotRequired[NodeRoleType]

class UpdateNodeStateRequestRequestTypeDef(TypedDict):
    ClusterId: str
    NodeId: str
    State: NotRequired[UpdateNodeStateType]

class VideoSelectorPidTypeDef(TypedDict):
    Pid: NotRequired[int]

class VideoSelectorProgramIdTypeDef(TypedDict):
    ProgramId: NotRequired[int]

class UpdateAccountConfigurationRequestRequestTypeDef(TypedDict):
    AccountConfiguration: NotRequired[AccountConfigurationTypeDef]

class ArchiveCdnSettingsTypeDef(TypedDict):
    ArchiveS3Settings: NotRequired[ArchiveS3SettingsTypeDef]

class CmafIngestGroupSettingsTypeDef(TypedDict):
    Destination: OutputLocationRefTypeDef
    NielsenId3Behavior: NotRequired[CmafNielsenId3BehaviorType]
    Scte35Type: NotRequired[Scte35TypeType]
    SegmentLength: NotRequired[int]
    SegmentLengthUnits: NotRequired[CmafIngestSegmentLengthUnitsType]
    SendDelayMs: NotRequired[int]

class MediaPackageGroupSettingsTypeDef(TypedDict):
    Destination: OutputLocationRefTypeDef

class MsSmoothGroupSettingsTypeDef(TypedDict):
    Destination: OutputLocationRefTypeDef
    AcquisitionPointId: NotRequired[str]
    AudioOnlyTimecodeControl: NotRequired[SmoothGroupAudioOnlyTimecodeControlType]
    CertificateMode: NotRequired[SmoothGroupCertificateModeType]
    ConnectionRetryInterval: NotRequired[int]
    EventId: NotRequired[str]
    EventIdMode: NotRequired[SmoothGroupEventIdModeType]
    EventStopBehavior: NotRequired[SmoothGroupEventStopBehaviorType]
    FilecacheDuration: NotRequired[int]
    FragmentLength: NotRequired[int]
    InputLossAction: NotRequired[InputLossActionForMsSmoothOutType]
    NumRetries: NotRequired[int]
    RestartDelay: NotRequired[int]
    SegmentationMode: NotRequired[SmoothGroupSegmentationModeType]
    SendDelayMs: NotRequired[int]
    SparseTrackType: NotRequired[SmoothGroupSparseTrackTypeType]
    StreamManifestBehavior: NotRequired[SmoothGroupStreamManifestBehaviorType]
    TimestampOffset: NotRequired[str]
    TimestampOffsetMode: NotRequired[SmoothGroupTimestampOffsetModeType]

class RtmpOutputSettingsTypeDef(TypedDict):
    Destination: OutputLocationRefTypeDef
    CertificateMode: NotRequired[RtmpOutputCertificateModeType]
    ConnectionRetryInterval: NotRequired[int]
    NumRetries: NotRequired[int]

class AudioChannelMappingOutputTypeDef(TypedDict):
    InputChannelLevels: List[InputChannelLevelTypeDef]
    OutputChannel: int

class AudioChannelMappingTypeDef(TypedDict):
    InputChannelLevels: Sequence[InputChannelLevelTypeDef]
    OutputChannel: int

class AudioCodecSettingsOutputTypeDef(TypedDict):
    AacSettings: NotRequired[AacSettingsTypeDef]
    Ac3Settings: NotRequired[Ac3SettingsTypeDef]
    Eac3AtmosSettings: NotRequired[Eac3AtmosSettingsTypeDef]
    Eac3Settings: NotRequired[Eac3SettingsTypeDef]
    Mp2Settings: NotRequired[Mp2SettingsTypeDef]
    PassThroughSettings: NotRequired[Dict[str, Any]]
    WavSettings: NotRequired[WavSettingsTypeDef]

class AudioCodecSettingsTypeDef(TypedDict):
    AacSettings: NotRequired[AacSettingsTypeDef]
    Ac3Settings: NotRequired[Ac3SettingsTypeDef]
    Eac3AtmosSettings: NotRequired[Eac3AtmosSettingsTypeDef]
    Eac3Settings: NotRequired[Eac3SettingsTypeDef]
    Mp2Settings: NotRequired[Mp2SettingsTypeDef]
    PassThroughSettings: NotRequired[Mapping[str, Any]]
    WavSettings: NotRequired[WavSettingsTypeDef]

class AudioOnlyHlsSettingsTypeDef(TypedDict):
    AudioGroupId: NotRequired[str]
    AudioOnlyImage: NotRequired[InputLocationTypeDef]
    AudioTrackType: NotRequired[AudioOnlyHlsTrackTypeType]
    SegmentType: NotRequired[AudioOnlyHlsSegmentTypeType]

class AvailBlankingTypeDef(TypedDict):
    AvailBlankingImage: NotRequired[InputLocationTypeDef]
    State: NotRequired[AvailBlankingStateType]

class BlackoutSlateTypeDef(TypedDict):
    BlackoutSlateImage: NotRequired[InputLocationTypeDef]
    NetworkEndBlackout: NotRequired[BlackoutSlateNetworkEndBlackoutType]
    NetworkEndBlackoutImage: NotRequired[InputLocationTypeDef]
    NetworkId: NotRequired[str]
    State: NotRequired[BlackoutSlateStateType]

class BurnInDestinationSettingsTypeDef(TypedDict):
    Alignment: NotRequired[BurnInAlignmentType]
    BackgroundColor: NotRequired[BurnInBackgroundColorType]
    BackgroundOpacity: NotRequired[int]
    Font: NotRequired[InputLocationTypeDef]
    FontColor: NotRequired[BurnInFontColorType]
    FontOpacity: NotRequired[int]
    FontResolution: NotRequired[int]
    FontSize: NotRequired[str]
    OutlineColor: NotRequired[BurnInOutlineColorType]
    OutlineSize: NotRequired[int]
    ShadowColor: NotRequired[BurnInShadowColorType]
    ShadowOpacity: NotRequired[int]
    ShadowXOffset: NotRequired[int]
    ShadowYOffset: NotRequired[int]
    TeletextGridControl: NotRequired[BurnInTeletextGridControlType]
    XPosition: NotRequired[int]
    YPosition: NotRequired[int]

class DvbSubDestinationSettingsTypeDef(TypedDict):
    Alignment: NotRequired[DvbSubDestinationAlignmentType]
    BackgroundColor: NotRequired[DvbSubDestinationBackgroundColorType]
    BackgroundOpacity: NotRequired[int]
    Font: NotRequired[InputLocationTypeDef]
    FontColor: NotRequired[DvbSubDestinationFontColorType]
    FontOpacity: NotRequired[int]
    FontResolution: NotRequired[int]
    FontSize: NotRequired[str]
    OutlineColor: NotRequired[DvbSubDestinationOutlineColorType]
    OutlineSize: NotRequired[int]
    ShadowColor: NotRequired[DvbSubDestinationShadowColorType]
    ShadowOpacity: NotRequired[int]
    ShadowXOffset: NotRequired[int]
    ShadowYOffset: NotRequired[int]
    TeletextGridControl: NotRequired[DvbSubDestinationTeletextGridControlType]
    XPosition: NotRequired[int]
    YPosition: NotRequired[int]

class InputLossBehaviorTypeDef(TypedDict):
    BlackFrameMsec: NotRequired[int]
    InputLossImageColor: NotRequired[str]
    InputLossImageSlate: NotRequired[InputLocationTypeDef]
    InputLossImageType: NotRequired[InputLossImageTypeType]
    RepeatFrameMsec: NotRequired[int]

class StaticImageActivateScheduleActionSettingsTypeDef(TypedDict):
    Image: InputLocationTypeDef
    Duration: NotRequired[int]
    FadeIn: NotRequired[int]
    FadeOut: NotRequired[int]
    Height: NotRequired[int]
    ImageX: NotRequired[int]
    ImageY: NotRequired[int]
    Layer: NotRequired[int]
    Opacity: NotRequired[int]
    Width: NotRequired[int]

class StaticImageOutputActivateScheduleActionSettingsOutputTypeDef(TypedDict):
    Image: InputLocationTypeDef
    OutputNames: List[str]
    Duration: NotRequired[int]
    FadeIn: NotRequired[int]
    FadeOut: NotRequired[int]
    Height: NotRequired[int]
    ImageX: NotRequired[int]
    ImageY: NotRequired[int]
    Layer: NotRequired[int]
    Opacity: NotRequired[int]
    Width: NotRequired[int]

class StaticImageOutputActivateScheduleActionSettingsTypeDef(TypedDict):
    Image: InputLocationTypeDef
    OutputNames: Sequence[str]
    Duration: NotRequired[int]
    FadeIn: NotRequired[int]
    FadeOut: NotRequired[int]
    Height: NotRequired[int]
    ImageX: NotRequired[int]
    ImageY: NotRequired[int]
    Layer: NotRequired[int]
    Opacity: NotRequired[int]
    Width: NotRequired[int]

class StaticKeySettingsTypeDef(TypedDict):
    StaticKeyValue: str
    KeyProviderServer: NotRequired[InputLocationTypeDef]

class AudioTrackSelectionOutputTypeDef(TypedDict):
    Tracks: List[AudioTrackTypeDef]
    DolbyEDecode: NotRequired[AudioDolbyEDecodeTypeDef]

class AudioTrackSelectionTypeDef(TypedDict):
    Tracks: Sequence[AudioTrackTypeDef]
    DolbyEDecode: NotRequired[AudioDolbyEDecodeTypeDef]

class Av1ColorSpaceSettingsOutputTypeDef(TypedDict):
    ColorSpacePassthroughSettings: NotRequired[Dict[str, Any]]
    Hdr10Settings: NotRequired[Hdr10SettingsTypeDef]
    Rec601Settings: NotRequired[Dict[str, Any]]
    Rec709Settings: NotRequired[Dict[str, Any]]

class Av1ColorSpaceSettingsTypeDef(TypedDict):
    ColorSpacePassthroughSettings: NotRequired[Mapping[str, Any]]
    Hdr10Settings: NotRequired[Hdr10SettingsTypeDef]
    Rec601Settings: NotRequired[Mapping[str, Any]]
    Rec709Settings: NotRequired[Mapping[str, Any]]

class H265ColorSpaceSettingsOutputTypeDef(TypedDict):
    ColorSpacePassthroughSettings: NotRequired[Dict[str, Any]]
    DolbyVision81Settings: NotRequired[Dict[str, Any]]
    Hdr10Settings: NotRequired[Hdr10SettingsTypeDef]
    Rec601Settings: NotRequired[Dict[str, Any]]
    Rec709Settings: NotRequired[Dict[str, Any]]

class H265ColorSpaceSettingsTypeDef(TypedDict):
    ColorSpacePassthroughSettings: NotRequired[Mapping[str, Any]]
    DolbyVision81Settings: NotRequired[Mapping[str, Any]]
    Hdr10Settings: NotRequired[Hdr10SettingsTypeDef]
    Rec601Settings: NotRequired[Mapping[str, Any]]
    Rec709Settings: NotRequired[Mapping[str, Any]]

class VideoSelectorColorSpaceSettingsTypeDef(TypedDict):
    Hdr10Settings: NotRequired[Hdr10SettingsTypeDef]

class FrameCaptureSettingsTypeDef(TypedDict):
    CaptureInterval: NotRequired[int]
    CaptureIntervalUnits: NotRequired[FrameCaptureIntervalUnitType]
    TimecodeBurninSettings: NotRequired[TimecodeBurninSettingsTypeDef]

class AvailSettingsTypeDef(TypedDict):
    Esam: NotRequired[EsamTypeDef]
    Scte35SpliceInsert: NotRequired[Scte35SpliceInsertTypeDef]
    Scte35TimeSignalApos: NotRequired[Scte35TimeSignalAposTypeDef]

class BatchDeleteResponseTypeDef(TypedDict):
    Failed: List[BatchFailedResultModelTypeDef]
    Successful: List[BatchSuccessfulResultModelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchStartResponseTypeDef(TypedDict):
    Failed: List[BatchFailedResultModelTypeDef]
    Successful: List[BatchSuccessfulResultModelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchStopResponseTypeDef(TypedDict):
    Failed: List[BatchFailedResultModelTypeDef]
    Successful: List[BatchSuccessfulResultModelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateChannelPlacementGroupResponseTypeDef(TypedDict):
    Arn: str
    Channels: List[str]
    ClusterId: str
    Id: str
    Name: str
    Nodes: List[str]
    State: ChannelPlacementGroupStateType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCloudWatchAlarmTemplateGroupResponseTypeDef(TypedDict):
    Arn: str
    CreatedAt: datetime
    Description: str
    Id: str
    ModifiedAt: datetime
    Name: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCloudWatchAlarmTemplateResponseTypeDef(TypedDict):
    Arn: str
    ComparisonOperator: CloudWatchAlarmTemplateComparisonOperatorType
    CreatedAt: datetime
    DatapointsToAlarm: int
    Description: str
    EvaluationPeriods: int
    GroupId: str
    Id: str
    MetricName: str
    ModifiedAt: datetime
    Name: str
    Period: int
    Statistic: CloudWatchAlarmTemplateStatisticType
    Tags: Dict[str, str]
    TargetResourceType: CloudWatchAlarmTemplateTargetResourceTypeType
    Threshold: float
    TreatMissingData: CloudWatchAlarmTemplateTreatMissingDataType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEventBridgeRuleTemplateGroupResponseTypeDef(TypedDict):
    Arn: str
    CreatedAt: datetime
    Description: str
    Id: str
    ModifiedAt: datetime
    Name: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateNodeRegistrationScriptResponseTypeDef(TypedDict):
    NodeRegistrationScript: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteChannelPlacementGroupResponseTypeDef(TypedDict):
    Arn: str
    Channels: List[str]
    ClusterId: str
    Id: str
    Name: str
    Nodes: List[str]
    State: ChannelPlacementGroupStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAccountConfigurationResponseTypeDef(TypedDict):
    AccountConfiguration: AccountConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeChannelPlacementGroupResponseTypeDef(TypedDict):
    Arn: str
    Channels: List[str]
    ClusterId: str
    Id: str
    Name: str
    Nodes: List[str]
    State: ChannelPlacementGroupStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeInputDeviceThumbnailResponseTypeDef(TypedDict):
    Body: StreamingBody
    ContentType: Literal["image/jpeg"]
    ContentLength: int
    ETag: str
    LastModified: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetCloudWatchAlarmTemplateGroupResponseTypeDef(TypedDict):
    Arn: str
    CreatedAt: datetime
    Description: str
    Id: str
    ModifiedAt: datetime
    Name: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetCloudWatchAlarmTemplateResponseTypeDef(TypedDict):
    Arn: str
    ComparisonOperator: CloudWatchAlarmTemplateComparisonOperatorType
    CreatedAt: datetime
    DatapointsToAlarm: int
    Description: str
    EvaluationPeriods: int
    GroupId: str
    Id: str
    MetricName: str
    ModifiedAt: datetime
    Name: str
    Period: int
    Statistic: CloudWatchAlarmTemplateStatisticType
    Tags: Dict[str, str]
    TargetResourceType: CloudWatchAlarmTemplateTargetResourceTypeType
    Threshold: float
    TreatMissingData: CloudWatchAlarmTemplateTreatMissingDataType
    ResponseMetadata: ResponseMetadataTypeDef

class GetEventBridgeRuleTemplateGroupResponseTypeDef(TypedDict):
    Arn: str
    CreatedAt: datetime
    Description: str
    Id: str
    ModifiedAt: datetime
    Name: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAccountConfigurationResponseTypeDef(TypedDict):
    AccountConfiguration: AccountConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateChannelPlacementGroupResponseTypeDef(TypedDict):
    Arn: str
    Channels: List[str]
    ClusterId: str
    Id: str
    Name: str
    Nodes: List[str]
    State: ChannelPlacementGroupStateType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateCloudWatchAlarmTemplateGroupResponseTypeDef(TypedDict):
    Arn: str
    CreatedAt: datetime
    Description: str
    Id: str
    ModifiedAt: datetime
    Name: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateCloudWatchAlarmTemplateResponseTypeDef(TypedDict):
    Arn: str
    ComparisonOperator: CloudWatchAlarmTemplateComparisonOperatorType
    CreatedAt: datetime
    DatapointsToAlarm: int
    Description: str
    EvaluationPeriods: int
    GroupId: str
    Id: str
    MetricName: str
    ModifiedAt: datetime
    Name: str
    Period: int
    Statistic: CloudWatchAlarmTemplateStatisticType
    Tags: Dict[str, str]
    TargetResourceType: CloudWatchAlarmTemplateTargetResourceTypeType
    Threshold: float
    TreatMissingData: CloudWatchAlarmTemplateTreatMissingDataType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEventBridgeRuleTemplateGroupResponseTypeDef(TypedDict):
    Arn: str
    CreatedAt: datetime
    Description: str
    Id: str
    ModifiedAt: datetime
    Name: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class TeletextSourceSettingsTypeDef(TypedDict):
    OutputRectangle: NotRequired[CaptionRectangleTypeDef]
    PageNumber: NotRequired[str]

class ListCloudWatchAlarmTemplateGroupsResponseTypeDef(TypedDict):
    CloudWatchAlarmTemplateGroups: List[CloudWatchAlarmTemplateGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListCloudWatchAlarmTemplatesResponseTypeDef(TypedDict):
    CloudWatchAlarmTemplates: List[CloudWatchAlarmTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ClusterNetworkSettingsCreateRequestTypeDef(TypedDict):
    DefaultRoute: NotRequired[str]
    InterfaceMappings: NotRequired[Sequence[InterfaceMappingCreateRequestTypeDef]]

class ClusterNetworkSettingsTypeDef(TypedDict):
    DefaultRoute: NotRequired[str]
    InterfaceMappings: NotRequired[List[InterfaceMappingTypeDef]]

class ClusterNetworkSettingsUpdateRequestTypeDef(TypedDict):
    DefaultRoute: NotRequired[str]
    InterfaceMappings: NotRequired[Sequence[InterfaceMappingUpdateRequestTypeDef]]

class ColorCorrectionSettingsOutputTypeDef(TypedDict):
    GlobalColorCorrections: List[ColorCorrectionTypeDef]

class ColorCorrectionSettingsTypeDef(TypedDict):
    GlobalColorCorrections: Sequence[ColorCorrectionTypeDef]

class CreateEventBridgeRuleTemplateRequestRequestTypeDef(TypedDict):
    EventType: EventBridgeRuleTemplateEventTypeType
    GroupIdentifier: str
    Name: str
    Description: NotRequired[str]
    EventTargets: NotRequired[Sequence[EventBridgeRuleTemplateTargetTypeDef]]
    Tags: NotRequired[Mapping[str, str]]

class CreateEventBridgeRuleTemplateResponseTypeDef(TypedDict):
    Arn: str
    CreatedAt: datetime
    Description: str
    EventTargets: List[EventBridgeRuleTemplateTargetTypeDef]
    EventType: EventBridgeRuleTemplateEventTypeType
    GroupId: str
    Id: str
    ModifiedAt: datetime
    Name: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetEventBridgeRuleTemplateResponseTypeDef(TypedDict):
    Arn: str
    CreatedAt: datetime
    Description: str
    EventTargets: List[EventBridgeRuleTemplateTargetTypeDef]
    EventType: EventBridgeRuleTemplateEventTypeType
    GroupId: str
    Id: str
    ModifiedAt: datetime
    Name: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEventBridgeRuleTemplateRequestRequestTypeDef(TypedDict):
    Identifier: str
    Description: NotRequired[str]
    EventTargets: NotRequired[Sequence[EventBridgeRuleTemplateTargetTypeDef]]
    EventType: NotRequired[EventBridgeRuleTemplateEventTypeType]
    GroupIdentifier: NotRequired[str]
    Name: NotRequired[str]

class UpdateEventBridgeRuleTemplateResponseTypeDef(TypedDict):
    Arn: str
    CreatedAt: datetime
    Description: str
    EventTargets: List[EventBridgeRuleTemplateTargetTypeDef]
    EventType: EventBridgeRuleTemplateEventTypeType
    GroupId: str
    Id: str
    ModifiedAt: datetime
    Name: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateInputSecurityGroupRequestRequestTypeDef(TypedDict):
    Tags: NotRequired[Mapping[str, str]]
    WhitelistRules: NotRequired[Sequence[InputWhitelistRuleCidrTypeDef]]

class UpdateInputSecurityGroupRequestRequestTypeDef(TypedDict):
    InputSecurityGroupId: str
    Tags: NotRequired[Mapping[str, str]]
    WhitelistRules: NotRequired[Sequence[InputWhitelistRuleCidrTypeDef]]

class CreateMultiplexRequestRequestTypeDef(TypedDict):
    AvailabilityZones: Sequence[str]
    MultiplexSettings: MultiplexSettingsTypeDef
    Name: str
    RequestId: str
    Tags: NotRequired[Mapping[str, str]]

class CreateNetworkRequestRequestTypeDef(TypedDict):
    IpPools: NotRequired[Sequence[IpPoolCreateRequestTypeDef]]
    Name: NotRequired[str]
    RequestId: NotRequired[str]
    Routes: NotRequired[Sequence[RouteCreateRequestTypeDef]]
    Tags: NotRequired[Mapping[str, str]]

class CreateNetworkResponseTypeDef(TypedDict):
    Arn: str
    AssociatedClusterIds: List[str]
    Id: str
    IpPools: List[IpPoolTypeDef]
    Name: str
    Routes: List[RouteTypeDef]
    State: NetworkStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteNetworkResponseTypeDef(TypedDict):
    Arn: str
    AssociatedClusterIds: List[str]
    Id: str
    IpPools: List[IpPoolTypeDef]
    Name: str
    Routes: List[RouteTypeDef]
    State: NetworkStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeNetworkResponseTypeDef(TypedDict):
    Arn: str
    AssociatedClusterIds: List[str]
    Id: str
    IpPools: List[IpPoolTypeDef]
    Name: str
    Routes: List[RouteTypeDef]
    State: NetworkStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeNetworkSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    AssociatedClusterIds: NotRequired[List[str]]
    Id: NotRequired[str]
    IpPools: NotRequired[List[IpPoolTypeDef]]
    Name: NotRequired[str]
    Routes: NotRequired[List[RouteTypeDef]]
    State: NotRequired[NetworkStateType]

class UpdateNetworkResponseTypeDef(TypedDict):
    Arn: str
    AssociatedClusterIds: List[str]
    Id: str
    IpPools: List[IpPoolTypeDef]
    Name: str
    Routes: List[RouteTypeDef]
    State: NetworkStateType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateNodeRegistrationScriptRequestRequestTypeDef(TypedDict):
    ClusterId: str
    Id: NotRequired[str]
    Name: NotRequired[str]
    NodeInterfaceMappings: NotRequired[Sequence[NodeInterfaceMappingTypeDef]]
    RequestId: NotRequired[str]
    Role: NotRequired[NodeRoleType]

class CreateNodeResponseTypeDef(TypedDict):
    Arn: str
    ChannelPlacementGroups: List[str]
    ClusterId: str
    ConnectionState: NodeConnectionStateType
    Id: str
    InstanceArn: str
    Name: str
    NodeInterfaceMappings: List[NodeInterfaceMappingTypeDef]
    Role: NodeRoleType
    State: NodeStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteNodeResponseTypeDef(TypedDict):
    Arn: str
    ChannelPlacementGroups: List[str]
    ClusterId: str
    ConnectionState: NodeConnectionStateType
    Id: str
    InstanceArn: str
    Name: str
    NodeInterfaceMappings: List[NodeInterfaceMappingTypeDef]
    Role: NodeRoleType
    State: NodeStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeNodeResponseTypeDef(TypedDict):
    Arn: str
    ChannelPlacementGroups: List[str]
    ClusterId: str
    ConnectionState: NodeConnectionStateType
    Id: str
    InstanceArn: str
    Name: str
    NodeInterfaceMappings: List[NodeInterfaceMappingTypeDef]
    Role: NodeRoleType
    State: NodeStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeNodeSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    ChannelPlacementGroups: NotRequired[List[str]]
    ClusterId: NotRequired[str]
    ConnectionState: NotRequired[NodeConnectionStateType]
    Id: NotRequired[str]
    InstanceArn: NotRequired[str]
    ManagedInstanceId: NotRequired[str]
    Name: NotRequired[str]
    NodeInterfaceMappings: NotRequired[List[NodeInterfaceMappingTypeDef]]
    Role: NotRequired[NodeRoleType]
    State: NotRequired[NodeStateType]

class UpdateNodeResponseTypeDef(TypedDict):
    Arn: str
    ChannelPlacementGroups: List[str]
    ClusterId: str
    ConnectionState: NodeConnectionStateType
    Id: str
    InstanceArn: str
    Name: str
    NodeInterfaceMappings: List[NodeInterfaceMappingTypeDef]
    Role: NodeRoleType
    State: NodeStateType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateNodeStateResponseTypeDef(TypedDict):
    Arn: str
    ChannelPlacementGroups: List[str]
    ClusterId: str
    ConnectionState: NodeConnectionStateType
    Id: str
    InstanceArn: str
    Name: str
    NodeInterfaceMappings: List[NodeInterfaceMappingTypeDef]
    Role: NodeRoleType
    State: NodeStateType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateNodeRequestRequestTypeDef(TypedDict):
    ClusterId: str
    Name: NotRequired[str]
    NodeInterfaceMappings: NotRequired[Sequence[NodeInterfaceMappingCreateRequestTypeDef]]
    RequestId: NotRequired[str]
    Role: NotRequired[NodeRoleType]
    Tags: NotRequired[Mapping[str, str]]

class PurchaseOfferingRequestRequestTypeDef(TypedDict):
    Count: int
    OfferingId: str
    Name: NotRequired[str]
    RenewalSettings: NotRequired[RenewalSettingsTypeDef]
    RequestId: NotRequired[str]
    Start: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class UpdateReservationRequestRequestTypeDef(TypedDict):
    ReservationId: str
    Name: NotRequired[str]
    RenewalSettings: NotRequired[RenewalSettingsTypeDef]

class DeleteReservationResponseTypeDef(TypedDict):
    Arn: str
    Count: int
    CurrencyCode: str
    Duration: int
    DurationUnits: Literal["MONTHS"]
    End: str
    FixedPrice: float
    Name: str
    OfferingDescription: str
    OfferingId: str
    OfferingType: Literal["NO_UPFRONT"]
    Region: str
    RenewalSettings: RenewalSettingsTypeDef
    ReservationId: str
    ResourceSpecification: ReservationResourceSpecificationTypeDef
    Start: str
    State: ReservationStateType
    Tags: Dict[str, str]
    UsagePrice: float
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeOfferingResponseTypeDef(TypedDict):
    Arn: str
    CurrencyCode: str
    Duration: int
    DurationUnits: Literal["MONTHS"]
    FixedPrice: float
    OfferingDescription: str
    OfferingId: str
    OfferingType: Literal["NO_UPFRONT"]
    Region: str
    ResourceSpecification: ReservationResourceSpecificationTypeDef
    UsagePrice: float
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeReservationResponseTypeDef(TypedDict):
    Arn: str
    Count: int
    CurrencyCode: str
    Duration: int
    DurationUnits: Literal["MONTHS"]
    End: str
    FixedPrice: float
    Name: str
    OfferingDescription: str
    OfferingId: str
    OfferingType: Literal["NO_UPFRONT"]
    Region: str
    RenewalSettings: RenewalSettingsTypeDef
    ReservationId: str
    ResourceSpecification: ReservationResourceSpecificationTypeDef
    Start: str
    State: ReservationStateType
    Tags: Dict[str, str]
    UsagePrice: float
    ResponseMetadata: ResponseMetadataTypeDef

class OfferingTypeDef(TypedDict):
    Arn: NotRequired[str]
    CurrencyCode: NotRequired[str]
    Duration: NotRequired[int]
    DurationUnits: NotRequired[Literal["MONTHS"]]
    FixedPrice: NotRequired[float]
    OfferingDescription: NotRequired[str]
    OfferingId: NotRequired[str]
    OfferingType: NotRequired[Literal["NO_UPFRONT"]]
    Region: NotRequired[str]
    ResourceSpecification: NotRequired[ReservationResourceSpecificationTypeDef]
    UsagePrice: NotRequired[float]

class ReservationTypeDef(TypedDict):
    Arn: NotRequired[str]
    Count: NotRequired[int]
    CurrencyCode: NotRequired[str]
    Duration: NotRequired[int]
    DurationUnits: NotRequired[Literal["MONTHS"]]
    End: NotRequired[str]
    FixedPrice: NotRequired[float]
    Name: NotRequired[str]
    OfferingDescription: NotRequired[str]
    OfferingId: NotRequired[str]
    OfferingType: NotRequired[Literal["NO_UPFRONT"]]
    Region: NotRequired[str]
    RenewalSettings: NotRequired[RenewalSettingsTypeDef]
    ReservationId: NotRequired[str]
    ResourceSpecification: NotRequired[ReservationResourceSpecificationTypeDef]
    Start: NotRequired[str]
    State: NotRequired[ReservationStateType]
    Tags: NotRequired[Dict[str, str]]
    UsagePrice: NotRequired[float]

class DescribeChannelPlacementGroupRequestChannelPlacementGroupAssignedWaitTypeDef(TypedDict):
    ChannelPlacementGroupId: str
    ClusterId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeChannelPlacementGroupRequestChannelPlacementGroupDeletedWaitTypeDef(TypedDict):
    ChannelPlacementGroupId: str
    ClusterId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeChannelPlacementGroupRequestChannelPlacementGroupUnassignedWaitTypeDef(TypedDict):
    ChannelPlacementGroupId: str
    ClusterId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeChannelRequestChannelCreatedWaitTypeDef(TypedDict):
    ChannelId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeChannelRequestChannelDeletedWaitTypeDef(TypedDict):
    ChannelId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeChannelRequestChannelRunningWaitTypeDef(TypedDict):
    ChannelId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeChannelRequestChannelStoppedWaitTypeDef(TypedDict):
    ChannelId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeClusterRequestClusterCreatedWaitTypeDef(TypedDict):
    ClusterId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeClusterRequestClusterDeletedWaitTypeDef(TypedDict):
    ClusterId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeInputRequestInputAttachedWaitTypeDef(TypedDict):
    InputId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeInputRequestInputDeletedWaitTypeDef(TypedDict):
    InputId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeInputRequestInputDetachedWaitTypeDef(TypedDict):
    InputId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeMultiplexRequestMultiplexCreatedWaitTypeDef(TypedDict):
    MultiplexId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeMultiplexRequestMultiplexDeletedWaitTypeDef(TypedDict):
    MultiplexId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeMultiplexRequestMultiplexRunningWaitTypeDef(TypedDict):
    MultiplexId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeMultiplexRequestMultiplexStoppedWaitTypeDef(TypedDict):
    MultiplexId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeNodeRequestNodeDeregisteredWaitTypeDef(TypedDict):
    ClusterId: str
    NodeId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeNodeRequestNodeRegisteredWaitTypeDef(TypedDict):
    ClusterId: str
    NodeId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetSignalMapRequestSignalMapCreatedWaitTypeDef(TypedDict):
    Identifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetSignalMapRequestSignalMapMonitorDeletedWaitTypeDef(TypedDict):
    Identifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetSignalMapRequestSignalMapMonitorDeployedWaitTypeDef(TypedDict):
    Identifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetSignalMapRequestSignalMapUpdatedWaitTypeDef(TypedDict):
    Identifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class ListChannelPlacementGroupsResponseTypeDef(TypedDict):
    ChannelPlacementGroups: List[DescribeChannelPlacementGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeInputSecurityGroupResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    Inputs: List[str]
    State: InputSecurityGroupStateType
    Tags: Dict[str, str]
    WhitelistRules: List[InputWhitelistRuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class InputSecurityGroupTypeDef(TypedDict):
    Arn: NotRequired[str]
    Id: NotRequired[str]
    Inputs: NotRequired[List[str]]
    State: NotRequired[InputSecurityGroupStateType]
    Tags: NotRequired[Dict[str, str]]
    WhitelistRules: NotRequired[List[InputWhitelistRuleTypeDef]]

class DescribeScheduleRequestDescribeSchedulePaginateTypeDef(TypedDict):
    ChannelId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListChannelPlacementGroupsRequestListChannelPlacementGroupsPaginateTypeDef(TypedDict):
    ClusterId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListChannelsRequestListChannelsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCloudWatchAlarmTemplateGroupsRequestListCloudWatchAlarmTemplateGroupsPaginateTypeDef(
    TypedDict
):
    Scope: NotRequired[str]
    SignalMapIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCloudWatchAlarmTemplatesRequestListCloudWatchAlarmTemplatesPaginateTypeDef(TypedDict):
    GroupIdentifier: NotRequired[str]
    Scope: NotRequired[str]
    SignalMapIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListClustersRequestListClustersPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEventBridgeRuleTemplateGroupsRequestListEventBridgeRuleTemplateGroupsPaginateTypeDef(
    TypedDict
):
    SignalMapIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEventBridgeRuleTemplatesRequestListEventBridgeRuleTemplatesPaginateTypeDef(TypedDict):
    GroupIdentifier: NotRequired[str]
    SignalMapIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListInputDeviceTransfersRequestListInputDeviceTransfersPaginateTypeDef(TypedDict):
    TransferType: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListInputDevicesRequestListInputDevicesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListInputSecurityGroupsRequestListInputSecurityGroupsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListInputsRequestListInputsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMultiplexProgramsRequestListMultiplexProgramsPaginateTypeDef(TypedDict):
    MultiplexId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMultiplexesRequestListMultiplexesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListNetworksRequestListNetworksPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListNodesRequestListNodesPaginateTypeDef(TypedDict):
    ClusterId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOfferingsRequestListOfferingsPaginateTypeDef(TypedDict):
    ChannelClass: NotRequired[str]
    ChannelConfiguration: NotRequired[str]
    Codec: NotRequired[str]
    Duration: NotRequired[str]
    MaximumBitrate: NotRequired[str]
    MaximumFramerate: NotRequired[str]
    Resolution: NotRequired[str]
    ResourceType: NotRequired[str]
    SpecialFeature: NotRequired[str]
    VideoQuality: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListReservationsRequestListReservationsPaginateTypeDef(TypedDict):
    ChannelClass: NotRequired[str]
    Codec: NotRequired[str]
    MaximumBitrate: NotRequired[str]
    MaximumFramerate: NotRequired[str]
    Resolution: NotRequired[str]
    ResourceType: NotRequired[str]
    SpecialFeature: NotRequired[str]
    VideoQuality: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSignalMapsRequestListSignalMapsPaginateTypeDef(TypedDict):
    CloudWatchAlarmTemplateGroupIdentifier: NotRequired[str]
    EventBridgeRuleTemplateGroupIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class M2tsSettingsTypeDef(TypedDict):
    AbsentInputAudioBehavior: NotRequired[M2tsAbsentInputAudioBehaviorType]
    Arib: NotRequired[M2tsAribType]
    AribCaptionsPid: NotRequired[str]
    AribCaptionsPidControl: NotRequired[M2tsAribCaptionsPidControlType]
    AudioBufferModel: NotRequired[M2tsAudioBufferModelType]
    AudioFramesPerPes: NotRequired[int]
    AudioPids: NotRequired[str]
    AudioStreamType: NotRequired[M2tsAudioStreamTypeType]
    Bitrate: NotRequired[int]
    BufferModel: NotRequired[M2tsBufferModelType]
    CcDescriptor: NotRequired[M2tsCcDescriptorType]
    DvbNitSettings: NotRequired[DvbNitSettingsTypeDef]
    DvbSdtSettings: NotRequired[DvbSdtSettingsTypeDef]
    DvbSubPids: NotRequired[str]
    DvbTdtSettings: NotRequired[DvbTdtSettingsTypeDef]
    DvbTeletextPid: NotRequired[str]
    Ebif: NotRequired[M2tsEbifControlType]
    EbpAudioInterval: NotRequired[M2tsAudioIntervalType]
    EbpLookaheadMs: NotRequired[int]
    EbpPlacement: NotRequired[M2tsEbpPlacementType]
    EcmPid: NotRequired[str]
    EsRateInPes: NotRequired[M2tsEsRateInPesType]
    EtvPlatformPid: NotRequired[str]
    EtvSignalPid: NotRequired[str]
    FragmentTime: NotRequired[float]
    Klv: NotRequired[M2tsKlvType]
    KlvDataPids: NotRequired[str]
    NielsenId3Behavior: NotRequired[M2tsNielsenId3BehaviorType]
    NullPacketBitrate: NotRequired[float]
    PatInterval: NotRequired[int]
    PcrControl: NotRequired[M2tsPcrControlType]
    PcrPeriod: NotRequired[int]
    PcrPid: NotRequired[str]
    PmtInterval: NotRequired[int]
    PmtPid: NotRequired[str]
    ProgramNum: NotRequired[int]
    RateMode: NotRequired[M2tsRateModeType]
    Scte27Pids: NotRequired[str]
    Scte35Control: NotRequired[M2tsScte35ControlType]
    Scte35Pid: NotRequired[str]
    SegmentationMarkers: NotRequired[M2tsSegmentationMarkersType]
    SegmentationStyle: NotRequired[M2tsSegmentationStyleType]
    SegmentationTime: NotRequired[float]
    TimedMetadataBehavior: NotRequired[M2tsTimedMetadataBehaviorType]
    TimedMetadataPid: NotRequired[str]
    TransportStreamId: NotRequired[int]
    VideoPid: NotRequired[str]
    Scte35PrerollPullupMilliseconds: NotRequired[float]

class OutputLockingSettingsOutputTypeDef(TypedDict):
    EpochLockingSettings: NotRequired[EpochLockingSettingsTypeDef]
    PipelineLockingSettings: NotRequired[Dict[str, Any]]

class OutputLockingSettingsTypeDef(TypedDict):
    EpochLockingSettings: NotRequired[EpochLockingSettingsTypeDef]
    PipelineLockingSettings: NotRequired[Mapping[str, Any]]

class ListEventBridgeRuleTemplateGroupsResponseTypeDef(TypedDict):
    EventBridgeRuleTemplateGroups: List[EventBridgeRuleTemplateGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListEventBridgeRuleTemplatesResponseTypeDef(TypedDict):
    EventBridgeRuleTemplates: List[EventBridgeRuleTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class FailoverConditionSettingsTypeDef(TypedDict):
    AudioSilenceSettings: NotRequired[AudioSilenceFailoverSettingsTypeDef]
    InputLossSettings: NotRequired[InputLossFailoverSettingsTypeDef]
    VideoBlackSettings: NotRequired[VideoBlackFailoverSettingsTypeDef]

class ScheduleActionStartSettingsOutputTypeDef(TypedDict):
    FixedModeScheduleActionStartSettings: NotRequired[FixedModeScheduleActionStartSettingsTypeDef]
    FollowModeScheduleActionStartSettings: NotRequired[FollowModeScheduleActionStartSettingsTypeDef]
    ImmediateModeScheduleActionStartSettings: NotRequired[Dict[str, Any]]

class ScheduleActionStartSettingsTypeDef(TypedDict):
    FixedModeScheduleActionStartSettings: NotRequired[FixedModeScheduleActionStartSettingsTypeDef]
    FollowModeScheduleActionStartSettings: NotRequired[FollowModeScheduleActionStartSettingsTypeDef]
    ImmediateModeScheduleActionStartSettings: NotRequired[Mapping[str, Any]]

class FrameCaptureCdnSettingsTypeDef(TypedDict):
    FrameCaptureS3Settings: NotRequired[FrameCaptureS3SettingsTypeDef]

H264ColorSpaceSettingsUnionTypeDef = Union[
    H264ColorSpaceSettingsTypeDef, H264ColorSpaceSettingsOutputTypeDef
]

class H264FilterSettingsTypeDef(TypedDict):
    TemporalFilterSettings: NotRequired[TemporalFilterSettingsTypeDef]
    BandwidthReductionFilterSettings: NotRequired[BandwidthReductionFilterSettingsTypeDef]

class H265FilterSettingsTypeDef(TypedDict):
    TemporalFilterSettings: NotRequired[TemporalFilterSettingsTypeDef]
    BandwidthReductionFilterSettings: NotRequired[BandwidthReductionFilterSettingsTypeDef]

class Mpeg2FilterSettingsTypeDef(TypedDict):
    TemporalFilterSettings: NotRequired[TemporalFilterSettingsTypeDef]

class HlsCdnSettingsTypeDef(TypedDict):
    HlsAkamaiSettings: NotRequired[HlsAkamaiSettingsTypeDef]
    HlsBasicPutSettings: NotRequired[HlsBasicPutSettingsTypeDef]
    HlsMediaStoreSettings: NotRequired[HlsMediaStoreSettingsTypeDef]
    HlsS3Settings: NotRequired[HlsS3SettingsTypeDef]
    HlsWebdavSettings: NotRequired[HlsWebdavSettingsTypeDef]

class InputClippingSettingsTypeDef(TypedDict):
    InputTimecodeSource: InputTimecodeSourceType
    StartTimecode: NotRequired[StartTimecodeTypeDef]
    StopTimecode: NotRequired[StopTimecodeTypeDef]

class InputDestinationRequestTypeDef(TypedDict):
    StreamName: NotRequired[str]
    Network: NotRequired[str]
    NetworkRoutes: NotRequired[Sequence[InputRequestDestinationRouteTypeDef]]
    StaticIpAddress: NotRequired[str]

class InputDestinationTypeDef(TypedDict):
    Ip: NotRequired[str]
    Port: NotRequired[str]
    Url: NotRequired[str]
    Vpc: NotRequired[InputDestinationVpcTypeDef]
    Network: NotRequired[str]
    NetworkRoutes: NotRequired[List[InputDestinationRouteTypeDef]]

class InputDeviceConfigurableSettingsTypeDef(TypedDict):
    ConfiguredInput: NotRequired[InputDeviceConfiguredInputType]
    MaxBitrate: NotRequired[int]
    LatencyMs: NotRequired[int]
    Codec: NotRequired[InputDeviceCodecType]
    MediaconnectSettings: NotRequired[InputDeviceMediaConnectConfigurableSettingsTypeDef]
    AudioChannelPairs: NotRequired[Sequence[InputDeviceConfigurableAudioChannelPairConfigTypeDef]]

class InputDeviceUhdSettingsTypeDef(TypedDict):
    ActiveInput: NotRequired[InputDeviceActiveInputType]
    ConfiguredInput: NotRequired[InputDeviceConfiguredInputType]
    DeviceState: NotRequired[InputDeviceStateType]
    Framerate: NotRequired[float]
    Height: NotRequired[int]
    MaxBitrate: NotRequired[int]
    ScanType: NotRequired[InputDeviceScanTypeType]
    Width: NotRequired[int]
    LatencyMs: NotRequired[int]
    Codec: NotRequired[InputDeviceCodecType]
    MediaconnectSettings: NotRequired[InputDeviceMediaConnectSettingsTypeDef]
    AudioChannelPairs: NotRequired[List[InputDeviceUhdAudioChannelPairConfigTypeDef]]

class ListInputDeviceTransfersResponseTypeDef(TypedDict):
    InputDeviceTransfers: List[TransferringInputDeviceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListMultiplexProgramsResponseTypeDef(TypedDict):
    MultiplexPrograms: List[MultiplexProgramSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListSignalMapsResponseTypeDef(TypedDict):
    SignalMaps: List[SignalMapSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class StandardHlsSettingsTypeDef(TypedDict):
    M3u8Settings: M3u8SettingsTypeDef
    AudioRenditionSets: NotRequired[str]

class MediaResourceTypeDef(TypedDict):
    Destinations: NotRequired[List[MediaResourceNeighborTypeDef]]
    Name: NotRequired[str]
    Sources: NotRequired[List[MediaResourceNeighborTypeDef]]

class MotionGraphicsConfigurationOutputTypeDef(TypedDict):
    MotionGraphicsSettings: MotionGraphicsSettingsOutputTypeDef
    MotionGraphicsInsertion: NotRequired[MotionGraphicsInsertionType]

MotionGraphicsSettingsUnionTypeDef = Union[
    MotionGraphicsSettingsTypeDef, MotionGraphicsSettingsOutputTypeDef
]

class NetworkInputSettingsTypeDef(TypedDict):
    HlsInputSettings: NotRequired[HlsInputSettingsTypeDef]
    ServerValidation: NotRequired[NetworkInputServerValidationType]
    MulticastInputSettings: NotRequired[MulticastInputSettingsTypeDef]

class MulticastSettingsCreateRequestTypeDef(TypedDict):
    Sources: NotRequired[Sequence[MulticastSourceCreateRequestTypeDef]]

class MulticastSettingsTypeDef(TypedDict):
    Sources: NotRequired[List[MulticastSourceTypeDef]]

class MulticastSettingsUpdateRequestTypeDef(TypedDict):
    Sources: NotRequired[Sequence[MulticastSourceUpdateRequestTypeDef]]

class MultiplexContainerSettingsTypeDef(TypedDict):
    MultiplexM2tsSettings: NotRequired[MultiplexM2tsSettingsTypeDef]

class MultiplexOutputDestinationTypeDef(TypedDict):
    MediaConnectSettings: NotRequired[MultiplexMediaConnectOutputDestinationSettingsTypeDef]

MultiplexProgramPacketIdentifiersMapUnionTypeDef = Union[
    MultiplexProgramPacketIdentifiersMapTypeDef, MultiplexProgramPacketIdentifiersMapOutputTypeDef
]

class MultiplexSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    AvailabilityZones: NotRequired[List[str]]
    Id: NotRequired[str]
    MultiplexSettings: NotRequired[MultiplexSettingsSummaryTypeDef]
    Name: NotRequired[str]
    PipelinesRunningCount: NotRequired[int]
    ProgramCount: NotRequired[int]
    State: NotRequired[MultiplexStateType]
    Tags: NotRequired[Dict[str, str]]

class MultiplexVideoSettingsTypeDef(TypedDict):
    ConstantBitrate: NotRequired[int]
    StatmuxSettings: NotRequired[MultiplexStatmuxVideoSettingsTypeDef]

class NielsenWatermarksSettingsTypeDef(TypedDict):
    NielsenCbetSettings: NotRequired[NielsenCBETTypeDef]
    NielsenDistributionType: NotRequired[NielsenWatermarksDistributionTypesType]
    NielsenNaesIiNwSettings: NotRequired[NielsenNaesIiNwTypeDef]

class OutputDestinationOutputTypeDef(TypedDict):
    Id: NotRequired[str]
    MediaPackageSettings: NotRequired[List[MediaPackageOutputDestinationSettingsTypeDef]]
    MultiplexSettings: NotRequired[MultiplexProgramChannelDestinationSettingsTypeDef]
    Settings: NotRequired[List[OutputDestinationSettingsTypeDef]]
    SrtSettings: NotRequired[List[SrtOutputDestinationSettingsTypeDef]]

class OutputDestinationTypeDef(TypedDict):
    Id: NotRequired[str]
    MediaPackageSettings: NotRequired[Sequence[MediaPackageOutputDestinationSettingsTypeDef]]
    MultiplexSettings: NotRequired[MultiplexProgramChannelDestinationSettingsTypeDef]
    Settings: NotRequired[Sequence[OutputDestinationSettingsTypeDef]]
    SrtSettings: NotRequired[Sequence[SrtOutputDestinationSettingsTypeDef]]

class PauseStateScheduleActionSettingsOutputTypeDef(TypedDict):
    Pipelines: NotRequired[List[PipelinePauseStateSettingsTypeDef]]

class PauseStateScheduleActionSettingsTypeDef(TypedDict):
    Pipelines: NotRequired[Sequence[PipelinePauseStateSettingsTypeDef]]

class UpdateNetworkRequestRequestTypeDef(TypedDict):
    NetworkId: str
    IpPools: NotRequired[Sequence[IpPoolUpdateRequestTypeDef]]
    Name: NotRequired[str]
    Routes: NotRequired[Sequence[RouteUpdateRequestTypeDef]]

RtmpGroupSettingsUnionTypeDef = Union[RtmpGroupSettingsTypeDef, RtmpGroupSettingsOutputTypeDef]

class Scte35SegmentationDescriptorTypeDef(TypedDict):
    SegmentationCancelIndicator: Scte35SegmentationCancelIndicatorType
    SegmentationEventId: int
    DeliveryRestrictions: NotRequired[Scte35DeliveryRestrictionsTypeDef]
    SegmentNum: NotRequired[int]
    SegmentationDuration: NotRequired[int]
    SegmentationTypeId: NotRequired[int]
    SegmentationUpid: NotRequired[str]
    SegmentationUpidType: NotRequired[int]
    SegmentsExpected: NotRequired[int]
    SubSegmentNum: NotRequired[int]
    SubSegmentsExpected: NotRequired[int]

class SrtCallerSourceRequestTypeDef(TypedDict):
    Decryption: NotRequired[SrtCallerDecryptionRequestTypeDef]
    MinimumLatency: NotRequired[int]
    SrtListenerAddress: NotRequired[str]
    SrtListenerPort: NotRequired[str]
    StreamId: NotRequired[str]

class SrtCallerSourceTypeDef(TypedDict):
    Decryption: NotRequired[SrtCallerDecryptionTypeDef]
    MinimumLatency: NotRequired[int]
    SrtListenerAddress: NotRequired[str]
    SrtListenerPort: NotRequired[str]
    StreamId: NotRequired[str]

StaticImageOutputDeactivateScheduleActionSettingsUnionTypeDef = Union[
    StaticImageOutputDeactivateScheduleActionSettingsTypeDef,
    StaticImageOutputDeactivateScheduleActionSettingsOutputTypeDef,
]

class ThumbnailDetailTypeDef(TypedDict):
    PipelineId: NotRequired[str]
    Thumbnails: NotRequired[List[ThumbnailTypeDef]]

class VideoSelectorSettingsTypeDef(TypedDict):
    VideoSelectorPid: NotRequired[VideoSelectorPidTypeDef]
    VideoSelectorProgramId: NotRequired[VideoSelectorProgramIdTypeDef]

class ArchiveGroupSettingsTypeDef(TypedDict):
    Destination: OutputLocationRefTypeDef
    ArchiveCdnSettings: NotRequired[ArchiveCdnSettingsTypeDef]
    RolloverInterval: NotRequired[int]

class RemixSettingsOutputTypeDef(TypedDict):
    ChannelMappings: List[AudioChannelMappingOutputTypeDef]
    ChannelsIn: NotRequired[int]
    ChannelsOut: NotRequired[int]

AudioChannelMappingUnionTypeDef = Union[
    AudioChannelMappingTypeDef, AudioChannelMappingOutputTypeDef
]
AudioCodecSettingsUnionTypeDef = Union[AudioCodecSettingsTypeDef, AudioCodecSettingsOutputTypeDef]

class CaptionDestinationSettingsOutputTypeDef(TypedDict):
    AribDestinationSettings: NotRequired[Dict[str, Any]]
    BurnInDestinationSettings: NotRequired[BurnInDestinationSettingsTypeDef]
    DvbSubDestinationSettings: NotRequired[DvbSubDestinationSettingsTypeDef]
    EbuTtDDestinationSettings: NotRequired[EbuTtDDestinationSettingsTypeDef]
    EmbeddedDestinationSettings: NotRequired[Dict[str, Any]]
    EmbeddedPlusScte20DestinationSettings: NotRequired[Dict[str, Any]]
    RtmpCaptionInfoDestinationSettings: NotRequired[Dict[str, Any]]
    Scte20PlusEmbeddedDestinationSettings: NotRequired[Dict[str, Any]]
    Scte27DestinationSettings: NotRequired[Dict[str, Any]]
    SmpteTtDestinationSettings: NotRequired[Dict[str, Any]]
    TeletextDestinationSettings: NotRequired[Dict[str, Any]]
    TtmlDestinationSettings: NotRequired[TtmlDestinationSettingsTypeDef]
    WebvttDestinationSettings: NotRequired[WebvttDestinationSettingsTypeDef]

class CaptionDestinationSettingsTypeDef(TypedDict):
    AribDestinationSettings: NotRequired[Mapping[str, Any]]
    BurnInDestinationSettings: NotRequired[BurnInDestinationSettingsTypeDef]
    DvbSubDestinationSettings: NotRequired[DvbSubDestinationSettingsTypeDef]
    EbuTtDDestinationSettings: NotRequired[EbuTtDDestinationSettingsTypeDef]
    EmbeddedDestinationSettings: NotRequired[Mapping[str, Any]]
    EmbeddedPlusScte20DestinationSettings: NotRequired[Mapping[str, Any]]
    RtmpCaptionInfoDestinationSettings: NotRequired[Mapping[str, Any]]
    Scte20PlusEmbeddedDestinationSettings: NotRequired[Mapping[str, Any]]
    Scte27DestinationSettings: NotRequired[Mapping[str, Any]]
    SmpteTtDestinationSettings: NotRequired[Mapping[str, Any]]
    TeletextDestinationSettings: NotRequired[Mapping[str, Any]]
    TtmlDestinationSettings: NotRequired[TtmlDestinationSettingsTypeDef]
    WebvttDestinationSettings: NotRequired[WebvttDestinationSettingsTypeDef]

StaticImageOutputActivateScheduleActionSettingsUnionTypeDef = Union[
    StaticImageOutputActivateScheduleActionSettingsTypeDef,
    StaticImageOutputActivateScheduleActionSettingsOutputTypeDef,
]

class KeyProviderSettingsTypeDef(TypedDict):
    StaticKeySettings: NotRequired[StaticKeySettingsTypeDef]

class AudioSelectorSettingsOutputTypeDef(TypedDict):
    AudioHlsRenditionSelection: NotRequired[AudioHlsRenditionSelectionTypeDef]
    AudioLanguageSelection: NotRequired[AudioLanguageSelectionTypeDef]
    AudioPidSelection: NotRequired[AudioPidSelectionTypeDef]
    AudioTrackSelection: NotRequired[AudioTrackSelectionOutputTypeDef]

AudioTrackSelectionUnionTypeDef = Union[
    AudioTrackSelectionTypeDef, AudioTrackSelectionOutputTypeDef
]

class Av1SettingsOutputTypeDef(TypedDict):
    FramerateDenominator: int
    FramerateNumerator: int
    AfdSignaling: NotRequired[AfdSignalingType]
    BufSize: NotRequired[int]
    ColorSpaceSettings: NotRequired[Av1ColorSpaceSettingsOutputTypeDef]
    FixedAfd: NotRequired[FixedAfdType]
    GopSize: NotRequired[float]
    GopSizeUnits: NotRequired[Av1GopSizeUnitsType]
    Level: NotRequired[Av1LevelType]
    LookAheadRateControl: NotRequired[Av1LookAheadRateControlType]
    MaxBitrate: NotRequired[int]
    MinIInterval: NotRequired[int]
    ParDenominator: NotRequired[int]
    ParNumerator: NotRequired[int]
    QvbrQualityLevel: NotRequired[int]
    SceneChangeDetect: NotRequired[Av1SceneChangeDetectType]
    TimecodeBurninSettings: NotRequired[TimecodeBurninSettingsTypeDef]

Av1ColorSpaceSettingsUnionTypeDef = Union[
    Av1ColorSpaceSettingsTypeDef, Av1ColorSpaceSettingsOutputTypeDef
]
H265ColorSpaceSettingsUnionTypeDef = Union[
    H265ColorSpaceSettingsTypeDef, H265ColorSpaceSettingsOutputTypeDef
]

class AvailConfigurationTypeDef(TypedDict):
    AvailSettings: NotRequired[AvailSettingsTypeDef]
    Scte35SegmentationScope: NotRequired[Scte35SegmentationScopeType]

class CaptionSelectorSettingsOutputTypeDef(TypedDict):
    AncillarySourceSettings: NotRequired[AncillarySourceSettingsTypeDef]
    AribSourceSettings: NotRequired[Dict[str, Any]]
    DvbSubSourceSettings: NotRequired[DvbSubSourceSettingsTypeDef]
    EmbeddedSourceSettings: NotRequired[EmbeddedSourceSettingsTypeDef]
    Scte20SourceSettings: NotRequired[Scte20SourceSettingsTypeDef]
    Scte27SourceSettings: NotRequired[Scte27SourceSettingsTypeDef]
    TeletextSourceSettings: NotRequired[TeletextSourceSettingsTypeDef]

class CaptionSelectorSettingsTypeDef(TypedDict):
    AncillarySourceSettings: NotRequired[AncillarySourceSettingsTypeDef]
    AribSourceSettings: NotRequired[Mapping[str, Any]]
    DvbSubSourceSettings: NotRequired[DvbSubSourceSettingsTypeDef]
    EmbeddedSourceSettings: NotRequired[EmbeddedSourceSettingsTypeDef]
    Scte20SourceSettings: NotRequired[Scte20SourceSettingsTypeDef]
    Scte27SourceSettings: NotRequired[Scte27SourceSettingsTypeDef]
    TeletextSourceSettings: NotRequired[TeletextSourceSettingsTypeDef]

class CreateClusterRequestRequestTypeDef(TypedDict):
    ClusterType: NotRequired[Literal["ON_PREMISES"]]
    InstanceRoleArn: NotRequired[str]
    Name: NotRequired[str]
    NetworkSettings: NotRequired[ClusterNetworkSettingsCreateRequestTypeDef]
    RequestId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class CreateClusterResponseTypeDef(TypedDict):
    Arn: str
    ChannelIds: List[str]
    ClusterType: Literal["ON_PREMISES"]
    Id: str
    InstanceRoleArn: str
    Name: str
    NetworkSettings: ClusterNetworkSettingsTypeDef
    State: ClusterStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteClusterResponseTypeDef(TypedDict):
    Arn: str
    ChannelIds: List[str]
    ClusterType: Literal["ON_PREMISES"]
    Id: str
    InstanceRoleArn: str
    Name: str
    NetworkSettings: ClusterNetworkSettingsTypeDef
    State: ClusterStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeClusterResponseTypeDef(TypedDict):
    Arn: str
    ChannelIds: List[str]
    ClusterType: Literal["ON_PREMISES"]
    Id: str
    InstanceRoleArn: str
    Name: str
    NetworkSettings: ClusterNetworkSettingsTypeDef
    State: ClusterStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeClusterSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    ChannelIds: NotRequired[List[str]]
    ClusterType: NotRequired[Literal["ON_PREMISES"]]
    Id: NotRequired[str]
    InstanceRoleArn: NotRequired[str]
    Name: NotRequired[str]
    NetworkSettings: NotRequired[ClusterNetworkSettingsTypeDef]
    State: NotRequired[ClusterStateType]

class UpdateClusterResponseTypeDef(TypedDict):
    Arn: str
    ChannelIds: List[str]
    ClusterType: Literal["ON_PREMISES"]
    Id: str
    Name: str
    NetworkSettings: ClusterNetworkSettingsTypeDef
    State: ClusterStateType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateClusterRequestRequestTypeDef(TypedDict):
    ClusterId: str
    Name: NotRequired[str]
    NetworkSettings: NotRequired[ClusterNetworkSettingsUpdateRequestTypeDef]

ColorCorrectionSettingsUnionTypeDef = Union[
    ColorCorrectionSettingsTypeDef, ColorCorrectionSettingsOutputTypeDef
]

class ListNetworksResponseTypeDef(TypedDict):
    Networks: List[DescribeNetworkSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListNodesResponseTypeDef(TypedDict):
    Nodes: List[DescribeNodeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListOfferingsResponseTypeDef(TypedDict):
    Offerings: List[OfferingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListReservationsResponseTypeDef(TypedDict):
    Reservations: List[ReservationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PurchaseOfferingResponseTypeDef(TypedDict):
    Reservation: ReservationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateReservationResponseTypeDef(TypedDict):
    Reservation: ReservationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateInputSecurityGroupResponseTypeDef(TypedDict):
    SecurityGroup: InputSecurityGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListInputSecurityGroupsResponseTypeDef(TypedDict):
    InputSecurityGroups: List[InputSecurityGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateInputSecurityGroupResponseTypeDef(TypedDict):
    SecurityGroup: InputSecurityGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ArchiveContainerSettingsOutputTypeDef(TypedDict):
    M2tsSettings: NotRequired[M2tsSettingsTypeDef]
    RawSettings: NotRequired[Dict[str, Any]]

class ArchiveContainerSettingsTypeDef(TypedDict):
    M2tsSettings: NotRequired[M2tsSettingsTypeDef]
    RawSettings: NotRequired[Mapping[str, Any]]

class UdpContainerSettingsTypeDef(TypedDict):
    M2tsSettings: NotRequired[M2tsSettingsTypeDef]

class GlobalConfigurationOutputTypeDef(TypedDict):
    InitialAudioGain: NotRequired[int]
    InputEndAction: NotRequired[GlobalConfigurationInputEndActionType]
    InputLossBehavior: NotRequired[InputLossBehaviorTypeDef]
    OutputLockingMode: NotRequired[GlobalConfigurationOutputLockingModeType]
    OutputTimingSource: NotRequired[GlobalConfigurationOutputTimingSourceType]
    SupportLowFramerateInputs: NotRequired[GlobalConfigurationLowFramerateInputsType]
    OutputLockingSettings: NotRequired[OutputLockingSettingsOutputTypeDef]

OutputLockingSettingsUnionTypeDef = Union[
    OutputLockingSettingsTypeDef, OutputLockingSettingsOutputTypeDef
]

class FailoverConditionTypeDef(TypedDict):
    FailoverConditionSettings: NotRequired[FailoverConditionSettingsTypeDef]

ScheduleActionStartSettingsUnionTypeDef = Union[
    ScheduleActionStartSettingsTypeDef, ScheduleActionStartSettingsOutputTypeDef
]

class FrameCaptureGroupSettingsTypeDef(TypedDict):
    Destination: OutputLocationRefTypeDef
    FrameCaptureCdnSettings: NotRequired[FrameCaptureCdnSettingsTypeDef]

class H264SettingsOutputTypeDef(TypedDict):
    AdaptiveQuantization: NotRequired[H264AdaptiveQuantizationType]
    AfdSignaling: NotRequired[AfdSignalingType]
    Bitrate: NotRequired[int]
    BufFillPct: NotRequired[int]
    BufSize: NotRequired[int]
    ColorMetadata: NotRequired[H264ColorMetadataType]
    ColorSpaceSettings: NotRequired[H264ColorSpaceSettingsOutputTypeDef]
    EntropyEncoding: NotRequired[H264EntropyEncodingType]
    FilterSettings: NotRequired[H264FilterSettingsTypeDef]
    FixedAfd: NotRequired[FixedAfdType]
    FlickerAq: NotRequired[H264FlickerAqType]
    ForceFieldPictures: NotRequired[H264ForceFieldPicturesType]
    FramerateControl: NotRequired[H264FramerateControlType]
    FramerateDenominator: NotRequired[int]
    FramerateNumerator: NotRequired[int]
    GopBReference: NotRequired[H264GopBReferenceType]
    GopClosedCadence: NotRequired[int]
    GopNumBFrames: NotRequired[int]
    GopSize: NotRequired[float]
    GopSizeUnits: NotRequired[H264GopSizeUnitsType]
    Level: NotRequired[H264LevelType]
    LookAheadRateControl: NotRequired[H264LookAheadRateControlType]
    MaxBitrate: NotRequired[int]
    MinIInterval: NotRequired[int]
    NumRefFrames: NotRequired[int]
    ParControl: NotRequired[H264ParControlType]
    ParDenominator: NotRequired[int]
    ParNumerator: NotRequired[int]
    Profile: NotRequired[H264ProfileType]
    QualityLevel: NotRequired[H264QualityLevelType]
    QvbrQualityLevel: NotRequired[int]
    RateControlMode: NotRequired[H264RateControlModeType]
    ScanType: NotRequired[H264ScanTypeType]
    SceneChangeDetect: NotRequired[H264SceneChangeDetectType]
    Slices: NotRequired[int]
    Softness: NotRequired[int]
    SpatialAq: NotRequired[H264SpatialAqType]
    SubgopLength: NotRequired[H264SubGopLengthType]
    Syntax: NotRequired[H264SyntaxType]
    TemporalAq: NotRequired[H264TemporalAqType]
    TimecodeInsertion: NotRequired[H264TimecodeInsertionBehaviorType]
    TimecodeBurninSettings: NotRequired[TimecodeBurninSettingsTypeDef]
    MinQp: NotRequired[int]

class H264SettingsTypeDef(TypedDict):
    AdaptiveQuantization: NotRequired[H264AdaptiveQuantizationType]
    AfdSignaling: NotRequired[AfdSignalingType]
    Bitrate: NotRequired[int]
    BufFillPct: NotRequired[int]
    BufSize: NotRequired[int]
    ColorMetadata: NotRequired[H264ColorMetadataType]
    ColorSpaceSettings: NotRequired[H264ColorSpaceSettingsUnionTypeDef]
    EntropyEncoding: NotRequired[H264EntropyEncodingType]
    FilterSettings: NotRequired[H264FilterSettingsTypeDef]
    FixedAfd: NotRequired[FixedAfdType]
    FlickerAq: NotRequired[H264FlickerAqType]
    ForceFieldPictures: NotRequired[H264ForceFieldPicturesType]
    FramerateControl: NotRequired[H264FramerateControlType]
    FramerateDenominator: NotRequired[int]
    FramerateNumerator: NotRequired[int]
    GopBReference: NotRequired[H264GopBReferenceType]
    GopClosedCadence: NotRequired[int]
    GopNumBFrames: NotRequired[int]
    GopSize: NotRequired[float]
    GopSizeUnits: NotRequired[H264GopSizeUnitsType]
    Level: NotRequired[H264LevelType]
    LookAheadRateControl: NotRequired[H264LookAheadRateControlType]
    MaxBitrate: NotRequired[int]
    MinIInterval: NotRequired[int]
    NumRefFrames: NotRequired[int]
    ParControl: NotRequired[H264ParControlType]
    ParDenominator: NotRequired[int]
    ParNumerator: NotRequired[int]
    Profile: NotRequired[H264ProfileType]
    QualityLevel: NotRequired[H264QualityLevelType]
    QvbrQualityLevel: NotRequired[int]
    RateControlMode: NotRequired[H264RateControlModeType]
    ScanType: NotRequired[H264ScanTypeType]
    SceneChangeDetect: NotRequired[H264SceneChangeDetectType]
    Slices: NotRequired[int]
    Softness: NotRequired[int]
    SpatialAq: NotRequired[H264SpatialAqType]
    SubgopLength: NotRequired[H264SubGopLengthType]
    Syntax: NotRequired[H264SyntaxType]
    TemporalAq: NotRequired[H264TemporalAqType]
    TimecodeInsertion: NotRequired[H264TimecodeInsertionBehaviorType]
    TimecodeBurninSettings: NotRequired[TimecodeBurninSettingsTypeDef]
    MinQp: NotRequired[int]

class H265SettingsOutputTypeDef(TypedDict):
    FramerateDenominator: int
    FramerateNumerator: int
    AdaptiveQuantization: NotRequired[H265AdaptiveQuantizationType]
    AfdSignaling: NotRequired[AfdSignalingType]
    AlternativeTransferFunction: NotRequired[H265AlternativeTransferFunctionType]
    Bitrate: NotRequired[int]
    BufSize: NotRequired[int]
    ColorMetadata: NotRequired[H265ColorMetadataType]
    ColorSpaceSettings: NotRequired[H265ColorSpaceSettingsOutputTypeDef]
    FilterSettings: NotRequired[H265FilterSettingsTypeDef]
    FixedAfd: NotRequired[FixedAfdType]
    FlickerAq: NotRequired[H265FlickerAqType]
    GopClosedCadence: NotRequired[int]
    GopSize: NotRequired[float]
    GopSizeUnits: NotRequired[H265GopSizeUnitsType]
    Level: NotRequired[H265LevelType]
    LookAheadRateControl: NotRequired[H265LookAheadRateControlType]
    MaxBitrate: NotRequired[int]
    MinIInterval: NotRequired[int]
    ParDenominator: NotRequired[int]
    ParNumerator: NotRequired[int]
    Profile: NotRequired[H265ProfileType]
    QvbrQualityLevel: NotRequired[int]
    RateControlMode: NotRequired[H265RateControlModeType]
    ScanType: NotRequired[H265ScanTypeType]
    SceneChangeDetect: NotRequired[H265SceneChangeDetectType]
    Slices: NotRequired[int]
    Tier: NotRequired[H265TierType]
    TimecodeInsertion: NotRequired[H265TimecodeInsertionBehaviorType]
    TimecodeBurninSettings: NotRequired[TimecodeBurninSettingsTypeDef]
    MvOverPictureBoundaries: NotRequired[H265MvOverPictureBoundariesType]
    MvTemporalPredictor: NotRequired[H265MvTemporalPredictorType]
    TileHeight: NotRequired[int]
    TilePadding: NotRequired[H265TilePaddingType]
    TileWidth: NotRequired[int]
    TreeblockSize: NotRequired[H265TreeblockSizeType]
    MinQp: NotRequired[int]

class Mpeg2SettingsTypeDef(TypedDict):
    FramerateDenominator: int
    FramerateNumerator: int
    AdaptiveQuantization: NotRequired[Mpeg2AdaptiveQuantizationType]
    AfdSignaling: NotRequired[AfdSignalingType]
    ColorMetadata: NotRequired[Mpeg2ColorMetadataType]
    ColorSpace: NotRequired[Mpeg2ColorSpaceType]
    DisplayAspectRatio: NotRequired[Mpeg2DisplayRatioType]
    FilterSettings: NotRequired[Mpeg2FilterSettingsTypeDef]
    FixedAfd: NotRequired[FixedAfdType]
    GopClosedCadence: NotRequired[int]
    GopNumBFrames: NotRequired[int]
    GopSize: NotRequired[float]
    GopSizeUnits: NotRequired[Mpeg2GopSizeUnitsType]
    ScanType: NotRequired[Mpeg2ScanTypeType]
    SubgopLength: NotRequired[Mpeg2SubGopLengthType]
    TimecodeInsertion: NotRequired[Mpeg2TimecodeInsertionBehaviorType]
    TimecodeBurninSettings: NotRequired[TimecodeBurninSettingsTypeDef]

class InputPrepareScheduleActionSettingsOutputTypeDef(TypedDict):
    InputAttachmentNameReference: NotRequired[str]
    InputClippingSettings: NotRequired[InputClippingSettingsTypeDef]
    UrlPath: NotRequired[List[str]]

class InputPrepareScheduleActionSettingsTypeDef(TypedDict):
    InputAttachmentNameReference: NotRequired[str]
    InputClippingSettings: NotRequired[InputClippingSettingsTypeDef]
    UrlPath: NotRequired[Sequence[str]]

class InputSwitchScheduleActionSettingsOutputTypeDef(TypedDict):
    InputAttachmentNameReference: str
    InputClippingSettings: NotRequired[InputClippingSettingsTypeDef]
    UrlPath: NotRequired[List[str]]

class InputSwitchScheduleActionSettingsTypeDef(TypedDict):
    InputAttachmentNameReference: str
    InputClippingSettings: NotRequired[InputClippingSettingsTypeDef]
    UrlPath: NotRequired[Sequence[str]]

class UpdateInputDeviceRequestRequestTypeDef(TypedDict):
    InputDeviceId: str
    HdDeviceSettings: NotRequired[InputDeviceConfigurableSettingsTypeDef]
    Name: NotRequired[str]
    UhdDeviceSettings: NotRequired[InputDeviceConfigurableSettingsTypeDef]
    AvailabilityZone: NotRequired[str]

DescribeInputDeviceResponseTypeDef = TypedDict(
    "DescribeInputDeviceResponseTypeDef",
    {
        "Arn": str,
        "ConnectionState": InputDeviceConnectionStateType,
        "DeviceSettingsSyncState": DeviceSettingsSyncStateType,
        "DeviceUpdateStatus": DeviceUpdateStatusType,
        "HdDeviceSettings": InputDeviceHdSettingsTypeDef,
        "Id": str,
        "MacAddress": str,
        "Name": str,
        "NetworkSettings": InputDeviceNetworkSettingsTypeDef,
        "SerialNumber": str,
        "Type": InputDeviceTypeType,
        "UhdDeviceSettings": InputDeviceUhdSettingsTypeDef,
        "Tags": Dict[str, str],
        "AvailabilityZone": str,
        "MedialiveInputArns": List[str],
        "OutputType": InputDeviceOutputTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
InputDeviceSummaryTypeDef = TypedDict(
    "InputDeviceSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "ConnectionState": NotRequired[InputDeviceConnectionStateType],
        "DeviceSettingsSyncState": NotRequired[DeviceSettingsSyncStateType],
        "DeviceUpdateStatus": NotRequired[DeviceUpdateStatusType],
        "HdDeviceSettings": NotRequired[InputDeviceHdSettingsTypeDef],
        "Id": NotRequired[str],
        "MacAddress": NotRequired[str],
        "Name": NotRequired[str],
        "NetworkSettings": NotRequired[InputDeviceNetworkSettingsTypeDef],
        "SerialNumber": NotRequired[str],
        "Type": NotRequired[InputDeviceTypeType],
        "UhdDeviceSettings": NotRequired[InputDeviceUhdSettingsTypeDef],
        "Tags": NotRequired[Dict[str, str]],
        "AvailabilityZone": NotRequired[str],
        "MedialiveInputArns": NotRequired[List[str]],
        "OutputType": NotRequired[InputDeviceOutputTypeType],
    },
)
UpdateInputDeviceResponseTypeDef = TypedDict(
    "UpdateInputDeviceResponseTypeDef",
    {
        "Arn": str,
        "ConnectionState": InputDeviceConnectionStateType,
        "DeviceSettingsSyncState": DeviceSettingsSyncStateType,
        "DeviceUpdateStatus": DeviceUpdateStatusType,
        "HdDeviceSettings": InputDeviceHdSettingsTypeDef,
        "Id": str,
        "MacAddress": str,
        "Name": str,
        "NetworkSettings": InputDeviceNetworkSettingsTypeDef,
        "SerialNumber": str,
        "Type": InputDeviceTypeType,
        "UhdDeviceSettings": InputDeviceUhdSettingsTypeDef,
        "Tags": Dict[str, str],
        "AvailabilityZone": str,
        "MedialiveInputArns": List[str],
        "OutputType": InputDeviceOutputTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class HlsSettingsOutputTypeDef(TypedDict):
    AudioOnlyHlsSettings: NotRequired[AudioOnlyHlsSettingsTypeDef]
    Fmp4HlsSettings: NotRequired[Fmp4HlsSettingsTypeDef]
    FrameCaptureHlsSettings: NotRequired[Dict[str, Any]]
    StandardHlsSettings: NotRequired[StandardHlsSettingsTypeDef]

class HlsSettingsTypeDef(TypedDict):
    AudioOnlyHlsSettings: NotRequired[AudioOnlyHlsSettingsTypeDef]
    Fmp4HlsSettings: NotRequired[Fmp4HlsSettingsTypeDef]
    FrameCaptureHlsSettings: NotRequired[Mapping[str, Any]]
    StandardHlsSettings: NotRequired[StandardHlsSettingsTypeDef]

class CreateSignalMapResponseTypeDef(TypedDict):
    Arn: str
    CloudWatchAlarmTemplateGroupIds: List[str]
    CreatedAt: datetime
    Description: str
    DiscoveryEntryPointArn: str
    ErrorMessage: str
    EventBridgeRuleTemplateGroupIds: List[str]
    FailedMediaResourceMap: Dict[str, MediaResourceTypeDef]
    Id: str
    LastDiscoveredAt: datetime
    LastSuccessfulMonitorDeployment: SuccessfulMonitorDeploymentTypeDef
    MediaResourceMap: Dict[str, MediaResourceTypeDef]
    ModifiedAt: datetime
    MonitorChangesPendingDeployment: bool
    MonitorDeployment: MonitorDeploymentTypeDef
    Name: str
    Status: SignalMapStatusType
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetSignalMapResponseTypeDef(TypedDict):
    Arn: str
    CloudWatchAlarmTemplateGroupIds: List[str]
    CreatedAt: datetime
    Description: str
    DiscoveryEntryPointArn: str
    ErrorMessage: str
    EventBridgeRuleTemplateGroupIds: List[str]
    FailedMediaResourceMap: Dict[str, MediaResourceTypeDef]
    Id: str
    LastDiscoveredAt: datetime
    LastSuccessfulMonitorDeployment: SuccessfulMonitorDeploymentTypeDef
    MediaResourceMap: Dict[str, MediaResourceTypeDef]
    ModifiedAt: datetime
    MonitorChangesPendingDeployment: bool
    MonitorDeployment: MonitorDeploymentTypeDef
    Name: str
    Status: SignalMapStatusType
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class StartDeleteMonitorDeploymentResponseTypeDef(TypedDict):
    Arn: str
    CloudWatchAlarmTemplateGroupIds: List[str]
    CreatedAt: datetime
    Description: str
    DiscoveryEntryPointArn: str
    ErrorMessage: str
    EventBridgeRuleTemplateGroupIds: List[str]
    FailedMediaResourceMap: Dict[str, MediaResourceTypeDef]
    Id: str
    LastDiscoveredAt: datetime
    LastSuccessfulMonitorDeployment: SuccessfulMonitorDeploymentTypeDef
    MediaResourceMap: Dict[str, MediaResourceTypeDef]
    ModifiedAt: datetime
    MonitorChangesPendingDeployment: bool
    MonitorDeployment: MonitorDeploymentTypeDef
    Name: str
    Status: SignalMapStatusType
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class StartMonitorDeploymentResponseTypeDef(TypedDict):
    Arn: str
    CloudWatchAlarmTemplateGroupIds: List[str]
    CreatedAt: datetime
    Description: str
    DiscoveryEntryPointArn: str
    ErrorMessage: str
    EventBridgeRuleTemplateGroupIds: List[str]
    FailedMediaResourceMap: Dict[str, MediaResourceTypeDef]
    Id: str
    LastDiscoveredAt: datetime
    LastSuccessfulMonitorDeployment: SuccessfulMonitorDeploymentTypeDef
    MediaResourceMap: Dict[str, MediaResourceTypeDef]
    ModifiedAt: datetime
    MonitorChangesPendingDeployment: bool
    MonitorDeployment: MonitorDeploymentTypeDef
    Name: str
    Status: SignalMapStatusType
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class StartUpdateSignalMapResponseTypeDef(TypedDict):
    Arn: str
    CloudWatchAlarmTemplateGroupIds: List[str]
    CreatedAt: datetime
    Description: str
    DiscoveryEntryPointArn: str
    ErrorMessage: str
    EventBridgeRuleTemplateGroupIds: List[str]
    FailedMediaResourceMap: Dict[str, MediaResourceTypeDef]
    Id: str
    LastDiscoveredAt: datetime
    LastSuccessfulMonitorDeployment: SuccessfulMonitorDeploymentTypeDef
    MediaResourceMap: Dict[str, MediaResourceTypeDef]
    ModifiedAt: datetime
    MonitorChangesPendingDeployment: bool
    MonitorDeployment: MonitorDeploymentTypeDef
    Name: str
    Status: SignalMapStatusType
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class MotionGraphicsConfigurationTypeDef(TypedDict):
    MotionGraphicsSettings: MotionGraphicsSettingsUnionTypeDef
    MotionGraphicsInsertion: NotRequired[MotionGraphicsInsertionType]

class MultiplexOutputSettingsTypeDef(TypedDict):
    Destination: OutputLocationRefTypeDef
    ContainerSettings: NotRequired[MultiplexContainerSettingsTypeDef]

class DeleteMultiplexResponseTypeDef(TypedDict):
    Arn: str
    AvailabilityZones: List[str]
    Destinations: List[MultiplexOutputDestinationTypeDef]
    Id: str
    MultiplexSettings: MultiplexSettingsTypeDef
    Name: str
    PipelinesRunningCount: int
    ProgramCount: int
    State: MultiplexStateType
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeMultiplexResponseTypeDef(TypedDict):
    Arn: str
    AvailabilityZones: List[str]
    Destinations: List[MultiplexOutputDestinationTypeDef]
    Id: str
    MultiplexSettings: MultiplexSettingsTypeDef
    Name: str
    PipelinesRunningCount: int
    ProgramCount: int
    State: MultiplexStateType
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class MultiplexTypeDef(TypedDict):
    Arn: NotRequired[str]
    AvailabilityZones: NotRequired[List[str]]
    Destinations: NotRequired[List[MultiplexOutputDestinationTypeDef]]
    Id: NotRequired[str]
    MultiplexSettings: NotRequired[MultiplexSettingsTypeDef]
    Name: NotRequired[str]
    PipelinesRunningCount: NotRequired[int]
    ProgramCount: NotRequired[int]
    State: NotRequired[MultiplexStateType]
    Tags: NotRequired[Dict[str, str]]

class StartMultiplexResponseTypeDef(TypedDict):
    Arn: str
    AvailabilityZones: List[str]
    Destinations: List[MultiplexOutputDestinationTypeDef]
    Id: str
    MultiplexSettings: MultiplexSettingsTypeDef
    Name: str
    PipelinesRunningCount: int
    ProgramCount: int
    State: MultiplexStateType
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class StopMultiplexResponseTypeDef(TypedDict):
    Arn: str
    AvailabilityZones: List[str]
    Destinations: List[MultiplexOutputDestinationTypeDef]
    Id: str
    MultiplexSettings: MultiplexSettingsTypeDef
    Name: str
    PipelinesRunningCount: int
    ProgramCount: int
    State: MultiplexStateType
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateMultiplexRequestRequestTypeDef(TypedDict):
    MultiplexId: str
    MultiplexSettings: NotRequired[MultiplexSettingsTypeDef]
    Name: NotRequired[str]
    PacketIdentifiersMapping: NotRequired[
        Mapping[str, MultiplexProgramPacketIdentifiersMapUnionTypeDef]
    ]

class ListMultiplexesResponseTypeDef(TypedDict):
    Multiplexes: List[MultiplexSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class MultiplexProgramSettingsTypeDef(TypedDict):
    ProgramNumber: int
    PreferredChannelPipeline: NotRequired[PreferredChannelPipelineType]
    ServiceDescriptor: NotRequired[MultiplexProgramServiceDescriptorTypeDef]
    VideoSettings: NotRequired[MultiplexVideoSettingsTypeDef]

class AudioWatermarkSettingsTypeDef(TypedDict):
    NielsenWatermarksSettings: NotRequired[NielsenWatermarksSettingsTypeDef]

OutputDestinationUnionTypeDef = Union[OutputDestinationTypeDef, OutputDestinationOutputTypeDef]

class UpdateChannelClassRequestRequestTypeDef(TypedDict):
    ChannelClass: ChannelClassType
    ChannelId: str
    Destinations: NotRequired[Sequence[OutputDestinationTypeDef]]

PauseStateScheduleActionSettingsUnionTypeDef = Union[
    PauseStateScheduleActionSettingsTypeDef, PauseStateScheduleActionSettingsOutputTypeDef
]

class Scte35DescriptorSettingsTypeDef(TypedDict):
    SegmentationDescriptorScte35DescriptorSettings: Scte35SegmentationDescriptorTypeDef

class SrtSettingsRequestTypeDef(TypedDict):
    SrtCallerSources: NotRequired[Sequence[SrtCallerSourceRequestTypeDef]]

class SrtSettingsTypeDef(TypedDict):
    SrtCallerSources: NotRequired[List[SrtCallerSourceTypeDef]]

class DescribeThumbnailsResponseTypeDef(TypedDict):
    ThumbnailDetails: List[ThumbnailDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class VideoSelectorTypeDef(TypedDict):
    ColorSpace: NotRequired[VideoSelectorColorSpaceType]
    ColorSpaceSettings: NotRequired[VideoSelectorColorSpaceSettingsTypeDef]
    ColorSpaceUsage: NotRequired[VideoSelectorColorSpaceUsageType]
    SelectorSettings: NotRequired[VideoSelectorSettingsTypeDef]

class RemixSettingsTypeDef(TypedDict):
    ChannelMappings: Sequence[AudioChannelMappingUnionTypeDef]
    ChannelsIn: NotRequired[int]
    ChannelsOut: NotRequired[int]

class CaptionDescriptionOutputTypeDef(TypedDict):
    CaptionSelectorName: str
    Name: str
    Accessibility: NotRequired[AccessibilityTypeType]
    DestinationSettings: NotRequired[CaptionDestinationSettingsOutputTypeDef]
    LanguageCode: NotRequired[str]
    LanguageDescription: NotRequired[str]
    CaptionDashRoles: NotRequired[List[DashRoleCaptionType]]
    DvbDashAccessibility: NotRequired[DvbDashAccessibilityType]

CaptionDestinationSettingsUnionTypeDef = Union[
    CaptionDestinationSettingsTypeDef, CaptionDestinationSettingsOutputTypeDef
]

class HlsGroupSettingsOutputTypeDef(TypedDict):
    Destination: OutputLocationRefTypeDef
    AdMarkers: NotRequired[List[HlsAdMarkersType]]
    BaseUrlContent: NotRequired[str]
    BaseUrlContent1: NotRequired[str]
    BaseUrlManifest: NotRequired[str]
    BaseUrlManifest1: NotRequired[str]
    CaptionLanguageMappings: NotRequired[List[CaptionLanguageMappingTypeDef]]
    CaptionLanguageSetting: NotRequired[HlsCaptionLanguageSettingType]
    ClientCache: NotRequired[HlsClientCacheType]
    CodecSpecification: NotRequired[HlsCodecSpecificationType]
    ConstantIv: NotRequired[str]
    DirectoryStructure: NotRequired[HlsDirectoryStructureType]
    DiscontinuityTags: NotRequired[HlsDiscontinuityTagsType]
    EncryptionType: NotRequired[HlsEncryptionTypeType]
    HlsCdnSettings: NotRequired[HlsCdnSettingsTypeDef]
    HlsId3SegmentTagging: NotRequired[HlsId3SegmentTaggingStateType]
    IFrameOnlyPlaylists: NotRequired[IFrameOnlyPlaylistTypeType]
    IncompleteSegmentBehavior: NotRequired[HlsIncompleteSegmentBehaviorType]
    IndexNSegments: NotRequired[int]
    InputLossAction: NotRequired[InputLossActionForHlsOutType]
    IvInManifest: NotRequired[HlsIvInManifestType]
    IvSource: NotRequired[HlsIvSourceType]
    KeepSegments: NotRequired[int]
    KeyFormat: NotRequired[str]
    KeyFormatVersions: NotRequired[str]
    KeyProviderSettings: NotRequired[KeyProviderSettingsTypeDef]
    ManifestCompression: NotRequired[HlsManifestCompressionType]
    ManifestDurationFormat: NotRequired[HlsManifestDurationFormatType]
    MinSegmentLength: NotRequired[int]
    Mode: NotRequired[HlsModeType]
    OutputSelection: NotRequired[HlsOutputSelectionType]
    ProgramDateTime: NotRequired[HlsProgramDateTimeType]
    ProgramDateTimeClock: NotRequired[HlsProgramDateTimeClockType]
    ProgramDateTimePeriod: NotRequired[int]
    RedundantManifest: NotRequired[HlsRedundantManifestType]
    SegmentLength: NotRequired[int]
    SegmentationMode: NotRequired[HlsSegmentationModeType]
    SegmentsPerSubdirectory: NotRequired[int]
    StreamInfResolution: NotRequired[HlsStreamInfResolutionType]
    TimedMetadataId3Frame: NotRequired[HlsTimedMetadataId3FrameType]
    TimedMetadataId3Period: NotRequired[int]
    TimestampDeltaMilliseconds: NotRequired[int]
    TsFileMode: NotRequired[HlsTsFileModeType]

class HlsGroupSettingsTypeDef(TypedDict):
    Destination: OutputLocationRefTypeDef
    AdMarkers: NotRequired[Sequence[HlsAdMarkersType]]
    BaseUrlContent: NotRequired[str]
    BaseUrlContent1: NotRequired[str]
    BaseUrlManifest: NotRequired[str]
    BaseUrlManifest1: NotRequired[str]
    CaptionLanguageMappings: NotRequired[Sequence[CaptionLanguageMappingTypeDef]]
    CaptionLanguageSetting: NotRequired[HlsCaptionLanguageSettingType]
    ClientCache: NotRequired[HlsClientCacheType]
    CodecSpecification: NotRequired[HlsCodecSpecificationType]
    ConstantIv: NotRequired[str]
    DirectoryStructure: NotRequired[HlsDirectoryStructureType]
    DiscontinuityTags: NotRequired[HlsDiscontinuityTagsType]
    EncryptionType: NotRequired[HlsEncryptionTypeType]
    HlsCdnSettings: NotRequired[HlsCdnSettingsTypeDef]
    HlsId3SegmentTagging: NotRequired[HlsId3SegmentTaggingStateType]
    IFrameOnlyPlaylists: NotRequired[IFrameOnlyPlaylistTypeType]
    IncompleteSegmentBehavior: NotRequired[HlsIncompleteSegmentBehaviorType]
    IndexNSegments: NotRequired[int]
    InputLossAction: NotRequired[InputLossActionForHlsOutType]
    IvInManifest: NotRequired[HlsIvInManifestType]
    IvSource: NotRequired[HlsIvSourceType]
    KeepSegments: NotRequired[int]
    KeyFormat: NotRequired[str]
    KeyFormatVersions: NotRequired[str]
    KeyProviderSettings: NotRequired[KeyProviderSettingsTypeDef]
    ManifestCompression: NotRequired[HlsManifestCompressionType]
    ManifestDurationFormat: NotRequired[HlsManifestDurationFormatType]
    MinSegmentLength: NotRequired[int]
    Mode: NotRequired[HlsModeType]
    OutputSelection: NotRequired[HlsOutputSelectionType]
    ProgramDateTime: NotRequired[HlsProgramDateTimeType]
    ProgramDateTimeClock: NotRequired[HlsProgramDateTimeClockType]
    ProgramDateTimePeriod: NotRequired[int]
    RedundantManifest: NotRequired[HlsRedundantManifestType]
    SegmentLength: NotRequired[int]
    SegmentationMode: NotRequired[HlsSegmentationModeType]
    SegmentsPerSubdirectory: NotRequired[int]
    StreamInfResolution: NotRequired[HlsStreamInfResolutionType]
    TimedMetadataId3Frame: NotRequired[HlsTimedMetadataId3FrameType]
    TimedMetadataId3Period: NotRequired[int]
    TimestampDeltaMilliseconds: NotRequired[int]
    TsFileMode: NotRequired[HlsTsFileModeType]

class AudioSelectorOutputTypeDef(TypedDict):
    Name: str
    SelectorSettings: NotRequired[AudioSelectorSettingsOutputTypeDef]

class AudioSelectorSettingsTypeDef(TypedDict):
    AudioHlsRenditionSelection: NotRequired[AudioHlsRenditionSelectionTypeDef]
    AudioLanguageSelection: NotRequired[AudioLanguageSelectionTypeDef]
    AudioPidSelection: NotRequired[AudioPidSelectionTypeDef]
    AudioTrackSelection: NotRequired[AudioTrackSelectionUnionTypeDef]

class Av1SettingsTypeDef(TypedDict):
    FramerateDenominator: int
    FramerateNumerator: int
    AfdSignaling: NotRequired[AfdSignalingType]
    BufSize: NotRequired[int]
    ColorSpaceSettings: NotRequired[Av1ColorSpaceSettingsUnionTypeDef]
    FixedAfd: NotRequired[FixedAfdType]
    GopSize: NotRequired[float]
    GopSizeUnits: NotRequired[Av1GopSizeUnitsType]
    Level: NotRequired[Av1LevelType]
    LookAheadRateControl: NotRequired[Av1LookAheadRateControlType]
    MaxBitrate: NotRequired[int]
    MinIInterval: NotRequired[int]
    ParDenominator: NotRequired[int]
    ParNumerator: NotRequired[int]
    QvbrQualityLevel: NotRequired[int]
    SceneChangeDetect: NotRequired[Av1SceneChangeDetectType]
    TimecodeBurninSettings: NotRequired[TimecodeBurninSettingsTypeDef]

class H265SettingsTypeDef(TypedDict):
    FramerateDenominator: int
    FramerateNumerator: int
    AdaptiveQuantization: NotRequired[H265AdaptiveQuantizationType]
    AfdSignaling: NotRequired[AfdSignalingType]
    AlternativeTransferFunction: NotRequired[H265AlternativeTransferFunctionType]
    Bitrate: NotRequired[int]
    BufSize: NotRequired[int]
    ColorMetadata: NotRequired[H265ColorMetadataType]
    ColorSpaceSettings: NotRequired[H265ColorSpaceSettingsUnionTypeDef]
    FilterSettings: NotRequired[H265FilterSettingsTypeDef]
    FixedAfd: NotRequired[FixedAfdType]
    FlickerAq: NotRequired[H265FlickerAqType]
    GopClosedCadence: NotRequired[int]
    GopSize: NotRequired[float]
    GopSizeUnits: NotRequired[H265GopSizeUnitsType]
    Level: NotRequired[H265LevelType]
    LookAheadRateControl: NotRequired[H265LookAheadRateControlType]
    MaxBitrate: NotRequired[int]
    MinIInterval: NotRequired[int]
    ParDenominator: NotRequired[int]
    ParNumerator: NotRequired[int]
    Profile: NotRequired[H265ProfileType]
    QvbrQualityLevel: NotRequired[int]
    RateControlMode: NotRequired[H265RateControlModeType]
    ScanType: NotRequired[H265ScanTypeType]
    SceneChangeDetect: NotRequired[H265SceneChangeDetectType]
    Slices: NotRequired[int]
    Tier: NotRequired[H265TierType]
    TimecodeInsertion: NotRequired[H265TimecodeInsertionBehaviorType]
    TimecodeBurninSettings: NotRequired[TimecodeBurninSettingsTypeDef]
    MvOverPictureBoundaries: NotRequired[H265MvOverPictureBoundariesType]
    MvTemporalPredictor: NotRequired[H265MvTemporalPredictorType]
    TileHeight: NotRequired[int]
    TilePadding: NotRequired[H265TilePaddingType]
    TileWidth: NotRequired[int]
    TreeblockSize: NotRequired[H265TreeblockSizeType]
    MinQp: NotRequired[int]

class CaptionSelectorOutputTypeDef(TypedDict):
    Name: str
    LanguageCode: NotRequired[str]
    SelectorSettings: NotRequired[CaptionSelectorSettingsOutputTypeDef]

CaptionSelectorSettingsUnionTypeDef = Union[
    CaptionSelectorSettingsTypeDef, CaptionSelectorSettingsOutputTypeDef
]

class ListClustersResponseTypeDef(TypedDict):
    Clusters: List[DescribeClusterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ArchiveOutputSettingsOutputTypeDef(TypedDict):
    ContainerSettings: ArchiveContainerSettingsOutputTypeDef
    Extension: NotRequired[str]
    NameModifier: NotRequired[str]

ArchiveContainerSettingsUnionTypeDef = Union[
    ArchiveContainerSettingsTypeDef, ArchiveContainerSettingsOutputTypeDef
]

class SrtOutputSettingsTypeDef(TypedDict):
    ContainerSettings: UdpContainerSettingsTypeDef
    Destination: OutputLocationRefTypeDef
    BufferMsec: NotRequired[int]
    EncryptionType: NotRequired[SrtEncryptionTypeType]
    Latency: NotRequired[int]

class UdpOutputSettingsTypeDef(TypedDict):
    ContainerSettings: UdpContainerSettingsTypeDef
    Destination: OutputLocationRefTypeDef
    BufferMsec: NotRequired[int]
    FecOutputSettings: NotRequired[FecOutputSettingsTypeDef]

class GlobalConfigurationTypeDef(TypedDict):
    InitialAudioGain: NotRequired[int]
    InputEndAction: NotRequired[GlobalConfigurationInputEndActionType]
    InputLossBehavior: NotRequired[InputLossBehaviorTypeDef]
    OutputLockingMode: NotRequired[GlobalConfigurationOutputLockingModeType]
    OutputTimingSource: NotRequired[GlobalConfigurationOutputTimingSourceType]
    SupportLowFramerateInputs: NotRequired[GlobalConfigurationLowFramerateInputsType]
    OutputLockingSettings: NotRequired[OutputLockingSettingsUnionTypeDef]

class AutomaticInputFailoverSettingsOutputTypeDef(TypedDict):
    SecondaryInputId: str
    ErrorClearTimeMsec: NotRequired[int]
    FailoverConditions: NotRequired[List[FailoverConditionTypeDef]]
    InputPreference: NotRequired[InputPreferenceType]

class AutomaticInputFailoverSettingsTypeDef(TypedDict):
    SecondaryInputId: str
    ErrorClearTimeMsec: NotRequired[int]
    FailoverConditions: NotRequired[Sequence[FailoverConditionTypeDef]]
    InputPreference: NotRequired[InputPreferenceType]

H264SettingsUnionTypeDef = Union[H264SettingsTypeDef, H264SettingsOutputTypeDef]

class VideoCodecSettingsOutputTypeDef(TypedDict):
    FrameCaptureSettings: NotRequired[FrameCaptureSettingsTypeDef]
    H264Settings: NotRequired[H264SettingsOutputTypeDef]
    H265Settings: NotRequired[H265SettingsOutputTypeDef]
    Mpeg2Settings: NotRequired[Mpeg2SettingsTypeDef]
    Av1Settings: NotRequired[Av1SettingsOutputTypeDef]

InputPrepareScheduleActionSettingsUnionTypeDef = Union[
    InputPrepareScheduleActionSettingsTypeDef, InputPrepareScheduleActionSettingsOutputTypeDef
]
InputSwitchScheduleActionSettingsUnionTypeDef = Union[
    InputSwitchScheduleActionSettingsTypeDef, InputSwitchScheduleActionSettingsOutputTypeDef
]

class ListInputDevicesResponseTypeDef(TypedDict):
    InputDevices: List[InputDeviceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class HlsOutputSettingsOutputTypeDef(TypedDict):
    HlsSettings: HlsSettingsOutputTypeDef
    H265PackagingType: NotRequired[HlsH265PackagingTypeType]
    NameModifier: NotRequired[str]
    SegmentModifier: NotRequired[str]

HlsSettingsUnionTypeDef = Union[HlsSettingsTypeDef, HlsSettingsOutputTypeDef]
MotionGraphicsConfigurationUnionTypeDef = Union[
    MotionGraphicsConfigurationTypeDef, MotionGraphicsConfigurationOutputTypeDef
]

class CreateMultiplexResponseTypeDef(TypedDict):
    Multiplex: MultiplexTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateMultiplexResponseTypeDef(TypedDict):
    Multiplex: MultiplexTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMultiplexProgramRequestRequestTypeDef(TypedDict):
    MultiplexId: str
    MultiplexProgramSettings: MultiplexProgramSettingsTypeDef
    ProgramName: str
    RequestId: str

class DeleteMultiplexProgramResponseTypeDef(TypedDict):
    ChannelId: str
    MultiplexProgramSettings: MultiplexProgramSettingsTypeDef
    PacketIdentifiersMap: MultiplexProgramPacketIdentifiersMapOutputTypeDef
    PipelineDetails: List[MultiplexProgramPipelineDetailTypeDef]
    ProgramName: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeMultiplexProgramResponseTypeDef(TypedDict):
    ChannelId: str
    MultiplexProgramSettings: MultiplexProgramSettingsTypeDef
    PacketIdentifiersMap: MultiplexProgramPacketIdentifiersMapOutputTypeDef
    PipelineDetails: List[MultiplexProgramPipelineDetailTypeDef]
    ProgramName: str
    ResponseMetadata: ResponseMetadataTypeDef

class MultiplexProgramTypeDef(TypedDict):
    ChannelId: NotRequired[str]
    MultiplexProgramSettings: NotRequired[MultiplexProgramSettingsTypeDef]
    PacketIdentifiersMap: NotRequired[MultiplexProgramPacketIdentifiersMapOutputTypeDef]
    PipelineDetails: NotRequired[List[MultiplexProgramPipelineDetailTypeDef]]
    ProgramName: NotRequired[str]

class UpdateMultiplexProgramRequestRequestTypeDef(TypedDict):
    MultiplexId: str
    ProgramName: str
    MultiplexProgramSettings: NotRequired[MultiplexProgramSettingsTypeDef]

class AudioDescriptionOutputTypeDef(TypedDict):
    AudioSelectorName: str
    Name: str
    AudioNormalizationSettings: NotRequired[AudioNormalizationSettingsTypeDef]
    AudioType: NotRequired[AudioTypeType]
    AudioTypeControl: NotRequired[AudioDescriptionAudioTypeControlType]
    AudioWatermarkingSettings: NotRequired[AudioWatermarkSettingsTypeDef]
    CodecSettings: NotRequired[AudioCodecSettingsOutputTypeDef]
    LanguageCode: NotRequired[str]
    LanguageCodeControl: NotRequired[AudioDescriptionLanguageCodeControlType]
    RemixSettings: NotRequired[RemixSettingsOutputTypeDef]
    StreamName: NotRequired[str]
    AudioDashRoles: NotRequired[List[DashRoleAudioType]]
    DvbDashAccessibility: NotRequired[DvbDashAccessibilityType]

class Scte35DescriptorTypeDef(TypedDict):
    Scte35DescriptorSettings: Scte35DescriptorSettingsTypeDef

CreateInputRequestRequestTypeDef = TypedDict(
    "CreateInputRequestRequestTypeDef",
    {
        "Destinations": NotRequired[Sequence[InputDestinationRequestTypeDef]],
        "InputDevices": NotRequired[Sequence[InputDeviceSettingsTypeDef]],
        "InputSecurityGroups": NotRequired[Sequence[str]],
        "MediaConnectFlows": NotRequired[Sequence[MediaConnectFlowRequestTypeDef]],
        "Name": NotRequired[str],
        "RequestId": NotRequired[str],
        "RoleArn": NotRequired[str],
        "Sources": NotRequired[Sequence[InputSourceRequestTypeDef]],
        "Tags": NotRequired[Mapping[str, str]],
        "Type": NotRequired[InputTypeType],
        "Vpc": NotRequired[InputVpcRequestTypeDef],
        "SrtSettings": NotRequired[SrtSettingsRequestTypeDef],
        "InputNetworkLocation": NotRequired[InputNetworkLocationType],
        "MulticastSettings": NotRequired[MulticastSettingsCreateRequestTypeDef],
    },
)

class UpdateInputRequestRequestTypeDef(TypedDict):
    InputId: str
    Destinations: NotRequired[Sequence[InputDestinationRequestTypeDef]]
    InputDevices: NotRequired[Sequence[InputDeviceRequestTypeDef]]
    InputSecurityGroups: NotRequired[Sequence[str]]
    MediaConnectFlows: NotRequired[Sequence[MediaConnectFlowRequestTypeDef]]
    Name: NotRequired[str]
    RoleArn: NotRequired[str]
    Sources: NotRequired[Sequence[InputSourceRequestTypeDef]]
    SrtSettings: NotRequired[SrtSettingsRequestTypeDef]
    MulticastSettings: NotRequired[MulticastSettingsUpdateRequestTypeDef]

DescribeInputResponseTypeDef = TypedDict(
    "DescribeInputResponseTypeDef",
    {
        "Arn": str,
        "AttachedChannels": List[str],
        "Destinations": List[InputDestinationTypeDef],
        "Id": str,
        "InputClass": InputClassType,
        "InputDevices": List[InputDeviceSettingsTypeDef],
        "InputPartnerIds": List[str],
        "InputSourceType": InputSourceTypeType,
        "MediaConnectFlows": List[MediaConnectFlowTypeDef],
        "Name": str,
        "RoleArn": str,
        "SecurityGroups": List[str],
        "Sources": List[InputSourceTypeDef],
        "State": InputStateType,
        "Tags": Dict[str, str],
        "Type": InputTypeType,
        "SrtSettings": SrtSettingsTypeDef,
        "InputNetworkLocation": InputNetworkLocationType,
        "MulticastSettings": MulticastSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
InputTypeDef = TypedDict(
    "InputTypeDef",
    {
        "Arn": NotRequired[str],
        "AttachedChannels": NotRequired[List[str]],
        "Destinations": NotRequired[List[InputDestinationTypeDef]],
        "Id": NotRequired[str],
        "InputClass": NotRequired[InputClassType],
        "InputDevices": NotRequired[List[InputDeviceSettingsTypeDef]],
        "InputPartnerIds": NotRequired[List[str]],
        "InputSourceType": NotRequired[InputSourceTypeType],
        "MediaConnectFlows": NotRequired[List[MediaConnectFlowTypeDef]],
        "Name": NotRequired[str],
        "RoleArn": NotRequired[str],
        "SecurityGroups": NotRequired[List[str]],
        "Sources": NotRequired[List[InputSourceTypeDef]],
        "State": NotRequired[InputStateType],
        "Tags": NotRequired[Dict[str, str]],
        "Type": NotRequired[InputTypeType],
        "SrtSettings": NotRequired[SrtSettingsTypeDef],
        "InputNetworkLocation": NotRequired[InputNetworkLocationType],
        "MulticastSettings": NotRequired[MulticastSettingsTypeDef],
    },
)
RemixSettingsUnionTypeDef = Union[RemixSettingsTypeDef, RemixSettingsOutputTypeDef]

class CaptionDescriptionTypeDef(TypedDict):
    CaptionSelectorName: str
    Name: str
    Accessibility: NotRequired[AccessibilityTypeType]
    DestinationSettings: NotRequired[CaptionDestinationSettingsUnionTypeDef]
    LanguageCode: NotRequired[str]
    LanguageDescription: NotRequired[str]
    CaptionDashRoles: NotRequired[Sequence[DashRoleCaptionType]]
    DvbDashAccessibility: NotRequired[DvbDashAccessibilityType]

class OutputGroupSettingsOutputTypeDef(TypedDict):
    ArchiveGroupSettings: NotRequired[ArchiveGroupSettingsTypeDef]
    FrameCaptureGroupSettings: NotRequired[FrameCaptureGroupSettingsTypeDef]
    HlsGroupSettings: NotRequired[HlsGroupSettingsOutputTypeDef]
    MediaPackageGroupSettings: NotRequired[MediaPackageGroupSettingsTypeDef]
    MsSmoothGroupSettings: NotRequired[MsSmoothGroupSettingsTypeDef]
    MultiplexGroupSettings: NotRequired[Dict[str, Any]]
    RtmpGroupSettings: NotRequired[RtmpGroupSettingsOutputTypeDef]
    UdpGroupSettings: NotRequired[UdpGroupSettingsTypeDef]
    CmafIngestGroupSettings: NotRequired[CmafIngestGroupSettingsTypeDef]
    SrtGroupSettings: NotRequired[SrtGroupSettingsTypeDef]

HlsGroupSettingsUnionTypeDef = Union[HlsGroupSettingsTypeDef, HlsGroupSettingsOutputTypeDef]
AudioSelectorSettingsUnionTypeDef = Union[
    AudioSelectorSettingsTypeDef, AudioSelectorSettingsOutputTypeDef
]
Av1SettingsUnionTypeDef = Union[Av1SettingsTypeDef, Av1SettingsOutputTypeDef]
H265SettingsUnionTypeDef = Union[H265SettingsTypeDef, H265SettingsOutputTypeDef]

class InputSettingsOutputTypeDef(TypedDict):
    AudioSelectors: NotRequired[List[AudioSelectorOutputTypeDef]]
    CaptionSelectors: NotRequired[List[CaptionSelectorOutputTypeDef]]
    DeblockFilter: NotRequired[InputDeblockFilterType]
    DenoiseFilter: NotRequired[InputDenoiseFilterType]
    FilterStrength: NotRequired[int]
    InputFilter: NotRequired[InputFilterType]
    NetworkInputSettings: NotRequired[NetworkInputSettingsTypeDef]
    Scte35Pid: NotRequired[int]
    Smpte2038DataPreference: NotRequired[Smpte2038DataPreferenceType]
    SourceEndBehavior: NotRequired[InputSourceEndBehaviorType]
    VideoSelector: NotRequired[VideoSelectorTypeDef]

class CaptionSelectorTypeDef(TypedDict):
    Name: str
    LanguageCode: NotRequired[str]
    SelectorSettings: NotRequired[CaptionSelectorSettingsUnionTypeDef]

class ArchiveOutputSettingsTypeDef(TypedDict):
    ContainerSettings: ArchiveContainerSettingsUnionTypeDef
    Extension: NotRequired[str]
    NameModifier: NotRequired[str]

GlobalConfigurationUnionTypeDef = Union[
    GlobalConfigurationTypeDef, GlobalConfigurationOutputTypeDef
]
AutomaticInputFailoverSettingsUnionTypeDef = Union[
    AutomaticInputFailoverSettingsTypeDef, AutomaticInputFailoverSettingsOutputTypeDef
]

class VideoDescriptionOutputTypeDef(TypedDict):
    Name: str
    CodecSettings: NotRequired[VideoCodecSettingsOutputTypeDef]
    Height: NotRequired[int]
    RespondToAfd: NotRequired[VideoDescriptionRespondToAfdType]
    ScalingBehavior: NotRequired[VideoDescriptionScalingBehaviorType]
    Sharpness: NotRequired[int]
    Width: NotRequired[int]

class OutputSettingsOutputTypeDef(TypedDict):
    ArchiveOutputSettings: NotRequired[ArchiveOutputSettingsOutputTypeDef]
    FrameCaptureOutputSettings: NotRequired[FrameCaptureOutputSettingsTypeDef]
    HlsOutputSettings: NotRequired[HlsOutputSettingsOutputTypeDef]
    MediaPackageOutputSettings: NotRequired[Dict[str, Any]]
    MsSmoothOutputSettings: NotRequired[MsSmoothOutputSettingsTypeDef]
    MultiplexOutputSettings: NotRequired[MultiplexOutputSettingsTypeDef]
    RtmpOutputSettings: NotRequired[RtmpOutputSettingsTypeDef]
    UdpOutputSettings: NotRequired[UdpOutputSettingsTypeDef]
    CmafIngestOutputSettings: NotRequired[CmafIngestOutputSettingsTypeDef]
    SrtOutputSettings: NotRequired[SrtOutputSettingsTypeDef]

class HlsOutputSettingsTypeDef(TypedDict):
    HlsSettings: HlsSettingsUnionTypeDef
    H265PackagingType: NotRequired[HlsH265PackagingTypeType]
    NameModifier: NotRequired[str]
    SegmentModifier: NotRequired[str]

class CreateMultiplexProgramResponseTypeDef(TypedDict):
    MultiplexProgram: MultiplexProgramTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateMultiplexProgramResponseTypeDef(TypedDict):
    MultiplexProgram: MultiplexProgramTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class Scte35TimeSignalScheduleActionSettingsOutputTypeDef(TypedDict):
    Scte35Descriptors: List[Scte35DescriptorTypeDef]

class Scte35TimeSignalScheduleActionSettingsTypeDef(TypedDict):
    Scte35Descriptors: Sequence[Scte35DescriptorTypeDef]

class CreateInputResponseTypeDef(TypedDict):
    Input: InputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePartnerInputResponseTypeDef(TypedDict):
    Input: InputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListInputsResponseTypeDef(TypedDict):
    Inputs: List[InputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateInputResponseTypeDef(TypedDict):
    Input: InputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AudioDescriptionTypeDef(TypedDict):
    AudioSelectorName: str
    Name: str
    AudioNormalizationSettings: NotRequired[AudioNormalizationSettingsTypeDef]
    AudioType: NotRequired[AudioTypeType]
    AudioTypeControl: NotRequired[AudioDescriptionAudioTypeControlType]
    AudioWatermarkingSettings: NotRequired[AudioWatermarkSettingsTypeDef]
    CodecSettings: NotRequired[AudioCodecSettingsUnionTypeDef]
    LanguageCode: NotRequired[str]
    LanguageCodeControl: NotRequired[AudioDescriptionLanguageCodeControlType]
    RemixSettings: NotRequired[RemixSettingsUnionTypeDef]
    StreamName: NotRequired[str]
    AudioDashRoles: NotRequired[Sequence[DashRoleAudioType]]
    DvbDashAccessibility: NotRequired[DvbDashAccessibilityType]

CaptionDescriptionUnionTypeDef = Union[CaptionDescriptionTypeDef, CaptionDescriptionOutputTypeDef]

class OutputGroupSettingsTypeDef(TypedDict):
    ArchiveGroupSettings: NotRequired[ArchiveGroupSettingsTypeDef]
    FrameCaptureGroupSettings: NotRequired[FrameCaptureGroupSettingsTypeDef]
    HlsGroupSettings: NotRequired[HlsGroupSettingsUnionTypeDef]
    MediaPackageGroupSettings: NotRequired[MediaPackageGroupSettingsTypeDef]
    MsSmoothGroupSettings: NotRequired[MsSmoothGroupSettingsTypeDef]
    MultiplexGroupSettings: NotRequired[Mapping[str, Any]]
    RtmpGroupSettings: NotRequired[RtmpGroupSettingsUnionTypeDef]
    UdpGroupSettings: NotRequired[UdpGroupSettingsTypeDef]
    CmafIngestGroupSettings: NotRequired[CmafIngestGroupSettingsTypeDef]
    SrtGroupSettings: NotRequired[SrtGroupSettingsTypeDef]

class AudioSelectorTypeDef(TypedDict):
    Name: str
    SelectorSettings: NotRequired[AudioSelectorSettingsUnionTypeDef]

class VideoCodecSettingsTypeDef(TypedDict):
    FrameCaptureSettings: NotRequired[FrameCaptureSettingsTypeDef]
    H264Settings: NotRequired[H264SettingsUnionTypeDef]
    H265Settings: NotRequired[H265SettingsUnionTypeDef]
    Mpeg2Settings: NotRequired[Mpeg2SettingsTypeDef]
    Av1Settings: NotRequired[Av1SettingsUnionTypeDef]

class InputAttachmentOutputTypeDef(TypedDict):
    AutomaticInputFailoverSettings: NotRequired[AutomaticInputFailoverSettingsOutputTypeDef]
    InputAttachmentName: NotRequired[str]
    InputId: NotRequired[str]
    InputSettings: NotRequired[InputSettingsOutputTypeDef]
    LogicalInterfaceNames: NotRequired[List[str]]

CaptionSelectorUnionTypeDef = Union[CaptionSelectorTypeDef, CaptionSelectorOutputTypeDef]
ArchiveOutputSettingsUnionTypeDef = Union[
    ArchiveOutputSettingsTypeDef, ArchiveOutputSettingsOutputTypeDef
]

class ExtraOutputTypeDef(TypedDict):
    OutputSettings: OutputSettingsOutputTypeDef
    AudioDescriptionNames: NotRequired[List[str]]
    CaptionDescriptionNames: NotRequired[List[str]]
    OutputName: NotRequired[str]
    VideoDescriptionName: NotRequired[str]

HlsOutputSettingsUnionTypeDef = Union[HlsOutputSettingsTypeDef, HlsOutputSettingsOutputTypeDef]

class ScheduleActionSettingsOutputTypeDef(TypedDict):
    HlsId3SegmentTaggingSettings: NotRequired[HlsId3SegmentTaggingScheduleActionSettingsTypeDef]
    HlsTimedMetadataSettings: NotRequired[HlsTimedMetadataScheduleActionSettingsTypeDef]
    InputPrepareSettings: NotRequired[InputPrepareScheduleActionSettingsOutputTypeDef]
    InputSwitchSettings: NotRequired[InputSwitchScheduleActionSettingsOutputTypeDef]
    MotionGraphicsImageActivateSettings: NotRequired[
        MotionGraphicsActivateScheduleActionSettingsTypeDef
    ]
    MotionGraphicsImageDeactivateSettings: NotRequired[Dict[str, Any]]
    PauseStateSettings: NotRequired[PauseStateScheduleActionSettingsOutputTypeDef]
    Scte35InputSettings: NotRequired[Scte35InputScheduleActionSettingsTypeDef]
    Scte35ReturnToNetworkSettings: NotRequired[Scte35ReturnToNetworkScheduleActionSettingsTypeDef]
    Scte35SpliceInsertSettings: NotRequired[Scte35SpliceInsertScheduleActionSettingsTypeDef]
    Scte35TimeSignalSettings: NotRequired[Scte35TimeSignalScheduleActionSettingsOutputTypeDef]
    StaticImageActivateSettings: NotRequired[StaticImageActivateScheduleActionSettingsTypeDef]
    StaticImageDeactivateSettings: NotRequired[StaticImageDeactivateScheduleActionSettingsTypeDef]
    StaticImageOutputActivateSettings: NotRequired[
        StaticImageOutputActivateScheduleActionSettingsOutputTypeDef
    ]
    StaticImageOutputDeactivateSettings: NotRequired[
        StaticImageOutputDeactivateScheduleActionSettingsOutputTypeDef
    ]

Scte35TimeSignalScheduleActionSettingsUnionTypeDef = Union[
    Scte35TimeSignalScheduleActionSettingsTypeDef,
    Scte35TimeSignalScheduleActionSettingsOutputTypeDef,
]
AudioDescriptionUnionTypeDef = Union[AudioDescriptionTypeDef, AudioDescriptionOutputTypeDef]
OutputGroupSettingsUnionTypeDef = Union[
    OutputGroupSettingsTypeDef, OutputGroupSettingsOutputTypeDef
]
AudioSelectorUnionTypeDef = Union[AudioSelectorTypeDef, AudioSelectorOutputTypeDef]
VideoCodecSettingsUnionTypeDef = Union[VideoCodecSettingsTypeDef, VideoCodecSettingsOutputTypeDef]

class ChannelSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    CdiInputSpecification: NotRequired[CdiInputSpecificationTypeDef]
    ChannelClass: NotRequired[ChannelClassType]
    Destinations: NotRequired[List[OutputDestinationOutputTypeDef]]
    EgressEndpoints: NotRequired[List[ChannelEgressEndpointTypeDef]]
    Id: NotRequired[str]
    InputAttachments: NotRequired[List[InputAttachmentOutputTypeDef]]
    InputSpecification: NotRequired[InputSpecificationTypeDef]
    LogLevel: NotRequired[LogLevelType]
    Maintenance: NotRequired[MaintenanceStatusTypeDef]
    Name: NotRequired[str]
    PipelinesRunningCount: NotRequired[int]
    RoleArn: NotRequired[str]
    State: NotRequired[ChannelStateType]
    Tags: NotRequired[Dict[str, str]]
    Vpc: NotRequired[VpcOutputSettingsDescriptionTypeDef]
    AnywhereSettings: NotRequired[DescribeAnywhereSettingsTypeDef]

class OutputGroupOutputTypeDef(TypedDict):
    OutputGroupSettings: OutputGroupSettingsOutputTypeDef
    Outputs: List[ExtraOutputTypeDef]
    Name: NotRequired[str]

class OutputSettingsTypeDef(TypedDict):
    ArchiveOutputSettings: NotRequired[ArchiveOutputSettingsUnionTypeDef]
    FrameCaptureOutputSettings: NotRequired[FrameCaptureOutputSettingsTypeDef]
    HlsOutputSettings: NotRequired[HlsOutputSettingsUnionTypeDef]
    MediaPackageOutputSettings: NotRequired[Mapping[str, Any]]
    MsSmoothOutputSettings: NotRequired[MsSmoothOutputSettingsTypeDef]
    MultiplexOutputSettings: NotRequired[MultiplexOutputSettingsTypeDef]
    RtmpOutputSettings: NotRequired[RtmpOutputSettingsTypeDef]
    UdpOutputSettings: NotRequired[UdpOutputSettingsTypeDef]
    CmafIngestOutputSettings: NotRequired[CmafIngestOutputSettingsTypeDef]
    SrtOutputSettings: NotRequired[SrtOutputSettingsTypeDef]

class ScheduleActionOutputTypeDef(TypedDict):
    ActionName: str
    ScheduleActionSettings: ScheduleActionSettingsOutputTypeDef
    ScheduleActionStartSettings: ScheduleActionStartSettingsOutputTypeDef

class ScheduleActionSettingsTypeDef(TypedDict):
    HlsId3SegmentTaggingSettings: NotRequired[HlsId3SegmentTaggingScheduleActionSettingsTypeDef]
    HlsTimedMetadataSettings: NotRequired[HlsTimedMetadataScheduleActionSettingsTypeDef]
    InputPrepareSettings: NotRequired[InputPrepareScheduleActionSettingsUnionTypeDef]
    InputSwitchSettings: NotRequired[InputSwitchScheduleActionSettingsUnionTypeDef]
    MotionGraphicsImageActivateSettings: NotRequired[
        MotionGraphicsActivateScheduleActionSettingsTypeDef
    ]
    MotionGraphicsImageDeactivateSettings: NotRequired[Mapping[str, Any]]
    PauseStateSettings: NotRequired[PauseStateScheduleActionSettingsUnionTypeDef]
    Scte35InputSettings: NotRequired[Scte35InputScheduleActionSettingsTypeDef]
    Scte35ReturnToNetworkSettings: NotRequired[Scte35ReturnToNetworkScheduleActionSettingsTypeDef]
    Scte35SpliceInsertSettings: NotRequired[Scte35SpliceInsertScheduleActionSettingsTypeDef]
    Scte35TimeSignalSettings: NotRequired[Scte35TimeSignalScheduleActionSettingsUnionTypeDef]
    StaticImageActivateSettings: NotRequired[StaticImageActivateScheduleActionSettingsTypeDef]
    StaticImageDeactivateSettings: NotRequired[StaticImageDeactivateScheduleActionSettingsTypeDef]
    StaticImageOutputActivateSettings: NotRequired[
        StaticImageOutputActivateScheduleActionSettingsUnionTypeDef
    ]
    StaticImageOutputDeactivateSettings: NotRequired[
        StaticImageOutputDeactivateScheduleActionSettingsUnionTypeDef
    ]

class InputSettingsTypeDef(TypedDict):
    AudioSelectors: NotRequired[Sequence[AudioSelectorUnionTypeDef]]
    CaptionSelectors: NotRequired[Sequence[CaptionSelectorUnionTypeDef]]
    DeblockFilter: NotRequired[InputDeblockFilterType]
    DenoiseFilter: NotRequired[InputDenoiseFilterType]
    FilterStrength: NotRequired[int]
    InputFilter: NotRequired[InputFilterType]
    NetworkInputSettings: NotRequired[NetworkInputSettingsTypeDef]
    Scte35Pid: NotRequired[int]
    Smpte2038DataPreference: NotRequired[Smpte2038DataPreferenceType]
    SourceEndBehavior: NotRequired[InputSourceEndBehaviorType]
    VideoSelector: NotRequired[VideoSelectorTypeDef]

class VideoDescriptionTypeDef(TypedDict):
    Name: str
    CodecSettings: NotRequired[VideoCodecSettingsUnionTypeDef]
    Height: NotRequired[int]
    RespondToAfd: NotRequired[VideoDescriptionRespondToAfdType]
    ScalingBehavior: NotRequired[VideoDescriptionScalingBehaviorType]
    Sharpness: NotRequired[int]
    Width: NotRequired[int]

class ListChannelsResponseTypeDef(TypedDict):
    Channels: List[ChannelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class EncoderSettingsOutputTypeDef(TypedDict):
    AudioDescriptions: List[AudioDescriptionOutputTypeDef]
    OutputGroups: List[OutputGroupOutputTypeDef]
    TimecodeConfig: TimecodeConfigTypeDef
    VideoDescriptions: List[VideoDescriptionOutputTypeDef]
    AvailBlanking: NotRequired[AvailBlankingTypeDef]
    AvailConfiguration: NotRequired[AvailConfigurationTypeDef]
    BlackoutSlate: NotRequired[BlackoutSlateTypeDef]
    CaptionDescriptions: NotRequired[List[CaptionDescriptionOutputTypeDef]]
    FeatureActivations: NotRequired[FeatureActivationsTypeDef]
    GlobalConfiguration: NotRequired[GlobalConfigurationOutputTypeDef]
    MotionGraphicsConfiguration: NotRequired[MotionGraphicsConfigurationOutputTypeDef]
    NielsenConfiguration: NotRequired[NielsenConfigurationTypeDef]
    ThumbnailConfiguration: NotRequired[ThumbnailConfigurationTypeDef]
    ColorCorrectionSettings: NotRequired[ColorCorrectionSettingsOutputTypeDef]

OutputSettingsUnionTypeDef = Union[OutputSettingsTypeDef, OutputSettingsOutputTypeDef]

class BatchScheduleActionCreateResultTypeDef(TypedDict):
    ScheduleActions: List[ScheduleActionOutputTypeDef]

class BatchScheduleActionDeleteResultTypeDef(TypedDict):
    ScheduleActions: List[ScheduleActionOutputTypeDef]

class DescribeScheduleResponseTypeDef(TypedDict):
    ScheduleActions: List[ScheduleActionOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

ScheduleActionSettingsUnionTypeDef = Union[
    ScheduleActionSettingsTypeDef, ScheduleActionSettingsOutputTypeDef
]
InputSettingsUnionTypeDef = Union[InputSettingsTypeDef, InputSettingsOutputTypeDef]
VideoDescriptionUnionTypeDef = Union[VideoDescriptionTypeDef, VideoDescriptionOutputTypeDef]

class ChannelTypeDef(TypedDict):
    Arn: NotRequired[str]
    CdiInputSpecification: NotRequired[CdiInputSpecificationTypeDef]
    ChannelClass: NotRequired[ChannelClassType]
    Destinations: NotRequired[List[OutputDestinationOutputTypeDef]]
    EgressEndpoints: NotRequired[List[ChannelEgressEndpointTypeDef]]
    EncoderSettings: NotRequired[EncoderSettingsOutputTypeDef]
    Id: NotRequired[str]
    InputAttachments: NotRequired[List[InputAttachmentOutputTypeDef]]
    InputSpecification: NotRequired[InputSpecificationTypeDef]
    LogLevel: NotRequired[LogLevelType]
    Maintenance: NotRequired[MaintenanceStatusTypeDef]
    Name: NotRequired[str]
    PipelineDetails: NotRequired[List[PipelineDetailTypeDef]]
    PipelinesRunningCount: NotRequired[int]
    RoleArn: NotRequired[str]
    State: NotRequired[ChannelStateType]
    Tags: NotRequired[Dict[str, str]]
    Vpc: NotRequired[VpcOutputSettingsDescriptionTypeDef]
    AnywhereSettings: NotRequired[DescribeAnywhereSettingsTypeDef]

class DeleteChannelResponseTypeDef(TypedDict):
    Arn: str
    CdiInputSpecification: CdiInputSpecificationTypeDef
    ChannelClass: ChannelClassType
    Destinations: List[OutputDestinationOutputTypeDef]
    EgressEndpoints: List[ChannelEgressEndpointTypeDef]
    EncoderSettings: EncoderSettingsOutputTypeDef
    Id: str
    InputAttachments: List[InputAttachmentOutputTypeDef]
    InputSpecification: InputSpecificationTypeDef
    LogLevel: LogLevelType
    Maintenance: MaintenanceStatusTypeDef
    Name: str
    PipelineDetails: List[PipelineDetailTypeDef]
    PipelinesRunningCount: int
    RoleArn: str
    State: ChannelStateType
    Tags: Dict[str, str]
    Vpc: VpcOutputSettingsDescriptionTypeDef
    AnywhereSettings: DescribeAnywhereSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeChannelResponseTypeDef(TypedDict):
    Arn: str
    CdiInputSpecification: CdiInputSpecificationTypeDef
    ChannelClass: ChannelClassType
    Destinations: List[OutputDestinationOutputTypeDef]
    EgressEndpoints: List[ChannelEgressEndpointTypeDef]
    EncoderSettings: EncoderSettingsOutputTypeDef
    Id: str
    InputAttachments: List[InputAttachmentOutputTypeDef]
    InputSpecification: InputSpecificationTypeDef
    LogLevel: LogLevelType
    Maintenance: MaintenanceStatusTypeDef
    Name: str
    PipelineDetails: List[PipelineDetailTypeDef]
    PipelinesRunningCount: int
    RoleArn: str
    State: ChannelStateType
    Tags: Dict[str, str]
    Vpc: VpcOutputSettingsDescriptionTypeDef
    AnywhereSettings: DescribeAnywhereSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class RestartChannelPipelinesResponseTypeDef(TypedDict):
    Arn: str
    CdiInputSpecification: CdiInputSpecificationTypeDef
    ChannelClass: ChannelClassType
    Destinations: List[OutputDestinationOutputTypeDef]
    EgressEndpoints: List[ChannelEgressEndpointTypeDef]
    EncoderSettings: EncoderSettingsOutputTypeDef
    Id: str
    InputAttachments: List[InputAttachmentOutputTypeDef]
    InputSpecification: InputSpecificationTypeDef
    LogLevel: LogLevelType
    Maintenance: MaintenanceStatusTypeDef
    MaintenanceStatus: str
    Name: str
    PipelineDetails: List[PipelineDetailTypeDef]
    PipelinesRunningCount: int
    RoleArn: str
    State: ChannelStateType
    Tags: Dict[str, str]
    Vpc: VpcOutputSettingsDescriptionTypeDef
    AnywhereSettings: DescribeAnywhereSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartChannelResponseTypeDef(TypedDict):
    Arn: str
    CdiInputSpecification: CdiInputSpecificationTypeDef
    ChannelClass: ChannelClassType
    Destinations: List[OutputDestinationOutputTypeDef]
    EgressEndpoints: List[ChannelEgressEndpointTypeDef]
    EncoderSettings: EncoderSettingsOutputTypeDef
    Id: str
    InputAttachments: List[InputAttachmentOutputTypeDef]
    InputSpecification: InputSpecificationTypeDef
    LogLevel: LogLevelType
    Maintenance: MaintenanceStatusTypeDef
    Name: str
    PipelineDetails: List[PipelineDetailTypeDef]
    PipelinesRunningCount: int
    RoleArn: str
    State: ChannelStateType
    Tags: Dict[str, str]
    Vpc: VpcOutputSettingsDescriptionTypeDef
    AnywhereSettings: DescribeAnywhereSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StopChannelResponseTypeDef(TypedDict):
    Arn: str
    CdiInputSpecification: CdiInputSpecificationTypeDef
    ChannelClass: ChannelClassType
    Destinations: List[OutputDestinationOutputTypeDef]
    EgressEndpoints: List[ChannelEgressEndpointTypeDef]
    EncoderSettings: EncoderSettingsOutputTypeDef
    Id: str
    InputAttachments: List[InputAttachmentOutputTypeDef]
    InputSpecification: InputSpecificationTypeDef
    LogLevel: LogLevelType
    Maintenance: MaintenanceStatusTypeDef
    Name: str
    PipelineDetails: List[PipelineDetailTypeDef]
    PipelinesRunningCount: int
    RoleArn: str
    State: ChannelStateType
    Tags: Dict[str, str]
    Vpc: VpcOutputSettingsDescriptionTypeDef
    AnywhereSettings: DescribeAnywhereSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class OutputTypeDef(TypedDict):
    OutputSettings: OutputSettingsUnionTypeDef
    AudioDescriptionNames: NotRequired[Sequence[str]]
    CaptionDescriptionNames: NotRequired[Sequence[str]]
    OutputName: NotRequired[str]
    VideoDescriptionName: NotRequired[str]

class BatchUpdateScheduleResponseTypeDef(TypedDict):
    Creates: BatchScheduleActionCreateResultTypeDef
    Deletes: BatchScheduleActionDeleteResultTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ScheduleActionTypeDef(TypedDict):
    ActionName: str
    ScheduleActionSettings: ScheduleActionSettingsUnionTypeDef
    ScheduleActionStartSettings: ScheduleActionStartSettingsUnionTypeDef

class InputAttachmentTypeDef(TypedDict):
    AutomaticInputFailoverSettings: NotRequired[AutomaticInputFailoverSettingsUnionTypeDef]
    InputAttachmentName: NotRequired[str]
    InputId: NotRequired[str]
    InputSettings: NotRequired[InputSettingsUnionTypeDef]
    LogicalInterfaceNames: NotRequired[Sequence[str]]

class CreateChannelResponseTypeDef(TypedDict):
    Channel: ChannelTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateChannelClassResponseTypeDef(TypedDict):
    Channel: ChannelTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateChannelResponseTypeDef(TypedDict):
    Channel: ChannelTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

UnionTypeDef = Union[OutputTypeDef, ExtraOutputTypeDef]
ScheduleActionUnionTypeDef = Union[ScheduleActionTypeDef, ScheduleActionOutputTypeDef]
InputAttachmentUnionTypeDef = Union[InputAttachmentTypeDef, InputAttachmentOutputTypeDef]

class OutputGroupTypeDef(TypedDict):
    OutputGroupSettings: OutputGroupSettingsUnionTypeDef
    Outputs: Sequence[UnionTypeDef]
    Name: NotRequired[str]

class BatchScheduleActionCreateRequestTypeDef(TypedDict):
    ScheduleActions: Sequence[ScheduleActionUnionTypeDef]

OutputGroupUnionTypeDef = Union[OutputGroupTypeDef, OutputGroupOutputTypeDef]

class BatchUpdateScheduleRequestRequestTypeDef(TypedDict):
    ChannelId: str
    Creates: NotRequired[BatchScheduleActionCreateRequestTypeDef]
    Deletes: NotRequired[BatchScheduleActionDeleteRequestTypeDef]

class EncoderSettingsTypeDef(TypedDict):
    AudioDescriptions: Sequence[AudioDescriptionUnionTypeDef]
    OutputGroups: Sequence[OutputGroupUnionTypeDef]
    TimecodeConfig: TimecodeConfigTypeDef
    VideoDescriptions: Sequence[VideoDescriptionUnionTypeDef]
    AvailBlanking: NotRequired[AvailBlankingTypeDef]
    AvailConfiguration: NotRequired[AvailConfigurationTypeDef]
    BlackoutSlate: NotRequired[BlackoutSlateTypeDef]
    CaptionDescriptions: NotRequired[Sequence[CaptionDescriptionUnionTypeDef]]
    FeatureActivations: NotRequired[FeatureActivationsTypeDef]
    GlobalConfiguration: NotRequired[GlobalConfigurationUnionTypeDef]
    MotionGraphicsConfiguration: NotRequired[MotionGraphicsConfigurationUnionTypeDef]
    NielsenConfiguration: NotRequired[NielsenConfigurationTypeDef]
    ThumbnailConfiguration: NotRequired[ThumbnailConfigurationTypeDef]
    ColorCorrectionSettings: NotRequired[ColorCorrectionSettingsUnionTypeDef]

class CreateChannelRequestRequestTypeDef(TypedDict):
    CdiInputSpecification: NotRequired[CdiInputSpecificationTypeDef]
    ChannelClass: NotRequired[ChannelClassType]
    Destinations: NotRequired[Sequence[OutputDestinationUnionTypeDef]]
    EncoderSettings: NotRequired[EncoderSettingsTypeDef]
    InputAttachments: NotRequired[Sequence[InputAttachmentUnionTypeDef]]
    InputSpecification: NotRequired[InputSpecificationTypeDef]
    LogLevel: NotRequired[LogLevelType]
    Maintenance: NotRequired[MaintenanceCreateSettingsTypeDef]
    Name: NotRequired[str]
    RequestId: NotRequired[str]
    Reserved: NotRequired[str]
    RoleArn: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    Vpc: NotRequired[VpcOutputSettingsTypeDef]
    AnywhereSettings: NotRequired[AnywhereSettingsTypeDef]

class UpdateChannelRequestRequestTypeDef(TypedDict):
    ChannelId: str
    CdiInputSpecification: NotRequired[CdiInputSpecificationTypeDef]
    Destinations: NotRequired[Sequence[OutputDestinationTypeDef]]
    EncoderSettings: NotRequired[EncoderSettingsTypeDef]
    InputAttachments: NotRequired[Sequence[InputAttachmentTypeDef]]
    InputSpecification: NotRequired[InputSpecificationTypeDef]
    LogLevel: NotRequired[LogLevelType]
    Maintenance: NotRequired[MaintenanceUpdateSettingsTypeDef]
    Name: NotRequired[str]
    RoleArn: NotRequired[str]
