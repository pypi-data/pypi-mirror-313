"""
Type annotations for storagegateway service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/type_defs/)

Usage::

    ```python
    from mypy_boto3_storagegateway.type_defs import TagTypeDef

    data: TagTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    ActiveDirectoryStatusType,
    AutomaticUpdatePolicyType,
    AvailabilityMonitorTestStatusType,
    CaseSensitivityType,
    EncryptionTypeType,
    FileShareTypeType,
    GatewayCapacityType,
    HostEnvironmentType,
    ObjectACLType,
    PoolStatusType,
    RetentionLockTypeType,
    SMBSecurityStrategyType,
    TapeStorageClassType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "ActivateGatewayInputRequestTypeDef",
    "ActivateGatewayOutputTypeDef",
    "AddCacheInputRequestTypeDef",
    "AddCacheOutputTypeDef",
    "AddTagsToResourceInputRequestTypeDef",
    "AddTagsToResourceOutputTypeDef",
    "AddUploadBufferInputRequestTypeDef",
    "AddUploadBufferOutputTypeDef",
    "AddWorkingStorageInputRequestTypeDef",
    "AddWorkingStorageOutputTypeDef",
    "AssignTapePoolInputRequestTypeDef",
    "AssignTapePoolOutputTypeDef",
    "AssociateFileSystemInputRequestTypeDef",
    "AssociateFileSystemOutputTypeDef",
    "AttachVolumeInputRequestTypeDef",
    "AttachVolumeOutputTypeDef",
    "AutomaticTapeCreationPolicyInfoTypeDef",
    "AutomaticTapeCreationRuleTypeDef",
    "BandwidthRateLimitIntervalOutputTypeDef",
    "BandwidthRateLimitIntervalTypeDef",
    "BandwidthRateLimitIntervalUnionTypeDef",
    "CacheAttributesTypeDef",
    "CachediSCSIVolumeTypeDef",
    "CancelArchivalInputRequestTypeDef",
    "CancelArchivalOutputTypeDef",
    "CancelRetrievalInputRequestTypeDef",
    "CancelRetrievalOutputTypeDef",
    "ChapInfoTypeDef",
    "CreateCachediSCSIVolumeInputRequestTypeDef",
    "CreateCachediSCSIVolumeOutputTypeDef",
    "CreateNFSFileShareInputRequestTypeDef",
    "CreateNFSFileShareOutputTypeDef",
    "CreateSMBFileShareInputRequestTypeDef",
    "CreateSMBFileShareOutputTypeDef",
    "CreateSnapshotFromVolumeRecoveryPointInputRequestTypeDef",
    "CreateSnapshotFromVolumeRecoveryPointOutputTypeDef",
    "CreateSnapshotInputRequestTypeDef",
    "CreateSnapshotOutputTypeDef",
    "CreateStorediSCSIVolumeInputRequestTypeDef",
    "CreateStorediSCSIVolumeOutputTypeDef",
    "CreateTapePoolInputRequestTypeDef",
    "CreateTapePoolOutputTypeDef",
    "CreateTapeWithBarcodeInputRequestTypeDef",
    "CreateTapeWithBarcodeOutputTypeDef",
    "CreateTapesInputRequestTypeDef",
    "CreateTapesOutputTypeDef",
    "DeleteAutomaticTapeCreationPolicyInputRequestTypeDef",
    "DeleteAutomaticTapeCreationPolicyOutputTypeDef",
    "DeleteBandwidthRateLimitInputRequestTypeDef",
    "DeleteBandwidthRateLimitOutputTypeDef",
    "DeleteChapCredentialsInputRequestTypeDef",
    "DeleteChapCredentialsOutputTypeDef",
    "DeleteFileShareInputRequestTypeDef",
    "DeleteFileShareOutputTypeDef",
    "DeleteGatewayInputRequestTypeDef",
    "DeleteGatewayOutputTypeDef",
    "DeleteSnapshotScheduleInputRequestTypeDef",
    "DeleteSnapshotScheduleOutputTypeDef",
    "DeleteTapeArchiveInputRequestTypeDef",
    "DeleteTapeArchiveOutputTypeDef",
    "DeleteTapeInputRequestTypeDef",
    "DeleteTapeOutputTypeDef",
    "DeleteTapePoolInputRequestTypeDef",
    "DeleteTapePoolOutputTypeDef",
    "DeleteVolumeInputRequestTypeDef",
    "DeleteVolumeOutputTypeDef",
    "DescribeAvailabilityMonitorTestInputRequestTypeDef",
    "DescribeAvailabilityMonitorTestOutputTypeDef",
    "DescribeBandwidthRateLimitInputRequestTypeDef",
    "DescribeBandwidthRateLimitOutputTypeDef",
    "DescribeBandwidthRateLimitScheduleInputRequestTypeDef",
    "DescribeBandwidthRateLimitScheduleOutputTypeDef",
    "DescribeCacheInputRequestTypeDef",
    "DescribeCacheOutputTypeDef",
    "DescribeCachediSCSIVolumesInputRequestTypeDef",
    "DescribeCachediSCSIVolumesOutputTypeDef",
    "DescribeChapCredentialsInputRequestTypeDef",
    "DescribeChapCredentialsOutputTypeDef",
    "DescribeFileSystemAssociationsInputRequestTypeDef",
    "DescribeFileSystemAssociationsOutputTypeDef",
    "DescribeGatewayInformationInputRequestTypeDef",
    "DescribeGatewayInformationOutputTypeDef",
    "DescribeMaintenanceStartTimeInputRequestTypeDef",
    "DescribeMaintenanceStartTimeOutputTypeDef",
    "DescribeNFSFileSharesInputRequestTypeDef",
    "DescribeNFSFileSharesOutputTypeDef",
    "DescribeSMBFileSharesInputRequestTypeDef",
    "DescribeSMBFileSharesOutputTypeDef",
    "DescribeSMBSettingsInputRequestTypeDef",
    "DescribeSMBSettingsOutputTypeDef",
    "DescribeSnapshotScheduleInputRequestTypeDef",
    "DescribeSnapshotScheduleOutputTypeDef",
    "DescribeStorediSCSIVolumesInputRequestTypeDef",
    "DescribeStorediSCSIVolumesOutputTypeDef",
    "DescribeTapeArchivesInputDescribeTapeArchivesPaginateTypeDef",
    "DescribeTapeArchivesInputRequestTypeDef",
    "DescribeTapeArchivesOutputTypeDef",
    "DescribeTapeRecoveryPointsInputDescribeTapeRecoveryPointsPaginateTypeDef",
    "DescribeTapeRecoveryPointsInputRequestTypeDef",
    "DescribeTapeRecoveryPointsOutputTypeDef",
    "DescribeTapesInputDescribeTapesPaginateTypeDef",
    "DescribeTapesInputRequestTypeDef",
    "DescribeTapesOutputTypeDef",
    "DescribeUploadBufferInputRequestTypeDef",
    "DescribeUploadBufferOutputTypeDef",
    "DescribeVTLDevicesInputDescribeVTLDevicesPaginateTypeDef",
    "DescribeVTLDevicesInputRequestTypeDef",
    "DescribeVTLDevicesOutputTypeDef",
    "DescribeWorkingStorageInputRequestTypeDef",
    "DescribeWorkingStorageOutputTypeDef",
    "DetachVolumeInputRequestTypeDef",
    "DetachVolumeOutputTypeDef",
    "DeviceiSCSIAttributesTypeDef",
    "DisableGatewayInputRequestTypeDef",
    "DisableGatewayOutputTypeDef",
    "DisassociateFileSystemInputRequestTypeDef",
    "DisassociateFileSystemOutputTypeDef",
    "DiskTypeDef",
    "EndpointNetworkConfigurationOutputTypeDef",
    "EndpointNetworkConfigurationTypeDef",
    "FileShareInfoTypeDef",
    "FileSystemAssociationInfoTypeDef",
    "FileSystemAssociationStatusDetailTypeDef",
    "FileSystemAssociationSummaryTypeDef",
    "GatewayInfoTypeDef",
    "JoinDomainInputRequestTypeDef",
    "JoinDomainOutputTypeDef",
    "ListAutomaticTapeCreationPoliciesInputRequestTypeDef",
    "ListAutomaticTapeCreationPoliciesOutputTypeDef",
    "ListFileSharesInputListFileSharesPaginateTypeDef",
    "ListFileSharesInputRequestTypeDef",
    "ListFileSharesOutputTypeDef",
    "ListFileSystemAssociationsInputListFileSystemAssociationsPaginateTypeDef",
    "ListFileSystemAssociationsInputRequestTypeDef",
    "ListFileSystemAssociationsOutputTypeDef",
    "ListGatewaysInputListGatewaysPaginateTypeDef",
    "ListGatewaysInputRequestTypeDef",
    "ListGatewaysOutputTypeDef",
    "ListLocalDisksInputRequestTypeDef",
    "ListLocalDisksOutputTypeDef",
    "ListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListTapePoolsInputListTapePoolsPaginateTypeDef",
    "ListTapePoolsInputRequestTypeDef",
    "ListTapePoolsOutputTypeDef",
    "ListTapesInputListTapesPaginateTypeDef",
    "ListTapesInputRequestTypeDef",
    "ListTapesOutputTypeDef",
    "ListVolumeInitiatorsInputRequestTypeDef",
    "ListVolumeInitiatorsOutputTypeDef",
    "ListVolumeRecoveryPointsInputRequestTypeDef",
    "ListVolumeRecoveryPointsOutputTypeDef",
    "ListVolumesInputListVolumesPaginateTypeDef",
    "ListVolumesInputRequestTypeDef",
    "ListVolumesOutputTypeDef",
    "NFSFileShareDefaultsTypeDef",
    "NFSFileShareInfoTypeDef",
    "NetworkInterfaceTypeDef",
    "NotifyWhenUploadedInputRequestTypeDef",
    "NotifyWhenUploadedOutputTypeDef",
    "PaginatorConfigTypeDef",
    "PoolInfoTypeDef",
    "RefreshCacheInputRequestTypeDef",
    "RefreshCacheOutputTypeDef",
    "RemoveTagsFromResourceInputRequestTypeDef",
    "RemoveTagsFromResourceOutputTypeDef",
    "ResetCacheInputRequestTypeDef",
    "ResetCacheOutputTypeDef",
    "ResponseMetadataTypeDef",
    "RetrieveTapeArchiveInputRequestTypeDef",
    "RetrieveTapeArchiveOutputTypeDef",
    "RetrieveTapeRecoveryPointInputRequestTypeDef",
    "RetrieveTapeRecoveryPointOutputTypeDef",
    "SMBFileShareInfoTypeDef",
    "SMBLocalGroupsOutputTypeDef",
    "SMBLocalGroupsTypeDef",
    "SetLocalConsolePasswordInputRequestTypeDef",
    "SetLocalConsolePasswordOutputTypeDef",
    "SetSMBGuestPasswordInputRequestTypeDef",
    "SetSMBGuestPasswordOutputTypeDef",
    "ShutdownGatewayInputRequestTypeDef",
    "ShutdownGatewayOutputTypeDef",
    "SoftwareUpdatePreferencesTypeDef",
    "StartAvailabilityMonitorTestInputRequestTypeDef",
    "StartAvailabilityMonitorTestOutputTypeDef",
    "StartGatewayInputRequestTypeDef",
    "StartGatewayOutputTypeDef",
    "StorediSCSIVolumeTypeDef",
    "TagTypeDef",
    "TapeArchiveTypeDef",
    "TapeInfoTypeDef",
    "TapeRecoveryPointInfoTypeDef",
    "TapeTypeDef",
    "UpdateAutomaticTapeCreationPolicyInputRequestTypeDef",
    "UpdateAutomaticTapeCreationPolicyOutputTypeDef",
    "UpdateBandwidthRateLimitInputRequestTypeDef",
    "UpdateBandwidthRateLimitOutputTypeDef",
    "UpdateBandwidthRateLimitScheduleInputRequestTypeDef",
    "UpdateBandwidthRateLimitScheduleOutputTypeDef",
    "UpdateChapCredentialsInputRequestTypeDef",
    "UpdateChapCredentialsOutputTypeDef",
    "UpdateFileSystemAssociationInputRequestTypeDef",
    "UpdateFileSystemAssociationOutputTypeDef",
    "UpdateGatewayInformationInputRequestTypeDef",
    "UpdateGatewayInformationOutputTypeDef",
    "UpdateGatewaySoftwareNowInputRequestTypeDef",
    "UpdateGatewaySoftwareNowOutputTypeDef",
    "UpdateMaintenanceStartTimeInputRequestTypeDef",
    "UpdateMaintenanceStartTimeOutputTypeDef",
    "UpdateNFSFileShareInputRequestTypeDef",
    "UpdateNFSFileShareOutputTypeDef",
    "UpdateSMBFileShareInputRequestTypeDef",
    "UpdateSMBFileShareOutputTypeDef",
    "UpdateSMBFileShareVisibilityInputRequestTypeDef",
    "UpdateSMBFileShareVisibilityOutputTypeDef",
    "UpdateSMBLocalGroupsInputRequestTypeDef",
    "UpdateSMBLocalGroupsOutputTypeDef",
    "UpdateSMBSecurityStrategyInputRequestTypeDef",
    "UpdateSMBSecurityStrategyOutputTypeDef",
    "UpdateSnapshotScheduleInputRequestTypeDef",
    "UpdateSnapshotScheduleOutputTypeDef",
    "UpdateVTLDeviceTypeInputRequestTypeDef",
    "UpdateVTLDeviceTypeOutputTypeDef",
    "VTLDeviceTypeDef",
    "VolumeInfoTypeDef",
    "VolumeRecoveryPointInfoTypeDef",
    "VolumeiSCSIAttributesTypeDef",
)


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AddCacheInputRequestTypeDef(TypedDict):
    GatewayARN: str
    DiskIds: Sequence[str]


class AddUploadBufferInputRequestTypeDef(TypedDict):
    GatewayARN: str
    DiskIds: Sequence[str]


class AddWorkingStorageInputRequestTypeDef(TypedDict):
    GatewayARN: str
    DiskIds: Sequence[str]


class AssignTapePoolInputRequestTypeDef(TypedDict):
    TapeARN: str
    PoolId: str
    BypassGovernanceRetention: NotRequired[bool]


class CacheAttributesTypeDef(TypedDict):
    CacheStaleTimeoutInSeconds: NotRequired[int]


class EndpointNetworkConfigurationTypeDef(TypedDict):
    IpAddresses: NotRequired[Sequence[str]]


class AttachVolumeInputRequestTypeDef(TypedDict):
    GatewayARN: str
    VolumeARN: str
    NetworkInterfaceId: str
    TargetName: NotRequired[str]
    DiskId: NotRequired[str]


class AutomaticTapeCreationRuleTypeDef(TypedDict):
    TapeBarcodePrefix: str
    PoolId: str
    TapeSizeInBytes: int
    MinimumNumTapes: int
    Worm: NotRequired[bool]


class BandwidthRateLimitIntervalOutputTypeDef(TypedDict):
    StartHourOfDay: int
    StartMinuteOfHour: int
    EndHourOfDay: int
    EndMinuteOfHour: int
    DaysOfWeek: List[int]
    AverageUploadRateLimitInBitsPerSec: NotRequired[int]
    AverageDownloadRateLimitInBitsPerSec: NotRequired[int]


class BandwidthRateLimitIntervalTypeDef(TypedDict):
    StartHourOfDay: int
    StartMinuteOfHour: int
    EndHourOfDay: int
    EndMinuteOfHour: int
    DaysOfWeek: Sequence[int]
    AverageUploadRateLimitInBitsPerSec: NotRequired[int]
    AverageDownloadRateLimitInBitsPerSec: NotRequired[int]


class VolumeiSCSIAttributesTypeDef(TypedDict):
    TargetARN: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]
    NetworkInterfacePort: NotRequired[int]
    LunNumber: NotRequired[int]
    ChapEnabled: NotRequired[bool]


class CancelArchivalInputRequestTypeDef(TypedDict):
    GatewayARN: str
    TapeARN: str


class CancelRetrievalInputRequestTypeDef(TypedDict):
    GatewayARN: str
    TapeARN: str


class ChapInfoTypeDef(TypedDict):
    TargetARN: NotRequired[str]
    SecretToAuthenticateInitiator: NotRequired[str]
    InitiatorName: NotRequired[str]
    SecretToAuthenticateTarget: NotRequired[str]


class NFSFileShareDefaultsTypeDef(TypedDict):
    FileMode: NotRequired[str]
    DirectoryMode: NotRequired[str]
    GroupId: NotRequired[int]
    OwnerId: NotRequired[int]


class DeleteAutomaticTapeCreationPolicyInputRequestTypeDef(TypedDict):
    GatewayARN: str


class DeleteBandwidthRateLimitInputRequestTypeDef(TypedDict):
    GatewayARN: str
    BandwidthType: str


class DeleteChapCredentialsInputRequestTypeDef(TypedDict):
    TargetARN: str
    InitiatorName: str


class DeleteFileShareInputRequestTypeDef(TypedDict):
    FileShareARN: str
    ForceDelete: NotRequired[bool]


class DeleteGatewayInputRequestTypeDef(TypedDict):
    GatewayARN: str


class DeleteSnapshotScheduleInputRequestTypeDef(TypedDict):
    VolumeARN: str


class DeleteTapeArchiveInputRequestTypeDef(TypedDict):
    TapeARN: str
    BypassGovernanceRetention: NotRequired[bool]


class DeleteTapeInputRequestTypeDef(TypedDict):
    GatewayARN: str
    TapeARN: str
    BypassGovernanceRetention: NotRequired[bool]


class DeleteTapePoolInputRequestTypeDef(TypedDict):
    PoolARN: str


class DeleteVolumeInputRequestTypeDef(TypedDict):
    VolumeARN: str


class DescribeAvailabilityMonitorTestInputRequestTypeDef(TypedDict):
    GatewayARN: str


class DescribeBandwidthRateLimitInputRequestTypeDef(TypedDict):
    GatewayARN: str


class DescribeBandwidthRateLimitScheduleInputRequestTypeDef(TypedDict):
    GatewayARN: str


class DescribeCacheInputRequestTypeDef(TypedDict):
    GatewayARN: str


class DescribeCachediSCSIVolumesInputRequestTypeDef(TypedDict):
    VolumeARNs: Sequence[str]


class DescribeChapCredentialsInputRequestTypeDef(TypedDict):
    TargetARN: str


class DescribeFileSystemAssociationsInputRequestTypeDef(TypedDict):
    FileSystemAssociationARNList: Sequence[str]


class DescribeGatewayInformationInputRequestTypeDef(TypedDict):
    GatewayARN: str


class NetworkInterfaceTypeDef(TypedDict):
    Ipv4Address: NotRequired[str]
    MacAddress: NotRequired[str]
    Ipv6Address: NotRequired[str]


class DescribeMaintenanceStartTimeInputRequestTypeDef(TypedDict):
    GatewayARN: str


class SoftwareUpdatePreferencesTypeDef(TypedDict):
    AutomaticUpdatePolicy: NotRequired[AutomaticUpdatePolicyType]


class DescribeNFSFileSharesInputRequestTypeDef(TypedDict):
    FileShareARNList: Sequence[str]


class DescribeSMBFileSharesInputRequestTypeDef(TypedDict):
    FileShareARNList: Sequence[str]


class DescribeSMBSettingsInputRequestTypeDef(TypedDict):
    GatewayARN: str


class SMBLocalGroupsOutputTypeDef(TypedDict):
    GatewayAdmins: NotRequired[List[str]]


class DescribeSnapshotScheduleInputRequestTypeDef(TypedDict):
    VolumeARN: str


class DescribeStorediSCSIVolumesInputRequestTypeDef(TypedDict):
    VolumeARNs: Sequence[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeTapeArchivesInputRequestTypeDef(TypedDict):
    TapeARNs: NotRequired[Sequence[str]]
    Marker: NotRequired[str]
    Limit: NotRequired[int]


class TapeArchiveTypeDef(TypedDict):
    TapeARN: NotRequired[str]
    TapeBarcode: NotRequired[str]
    TapeCreatedDate: NotRequired[datetime]
    TapeSizeInBytes: NotRequired[int]
    CompletionTime: NotRequired[datetime]
    RetrievedTo: NotRequired[str]
    TapeStatus: NotRequired[str]
    TapeUsedInBytes: NotRequired[int]
    KMSKey: NotRequired[str]
    PoolId: NotRequired[str]
    Worm: NotRequired[bool]
    RetentionStartDate: NotRequired[datetime]
    PoolEntryDate: NotRequired[datetime]


class DescribeTapeRecoveryPointsInputRequestTypeDef(TypedDict):
    GatewayARN: str
    Marker: NotRequired[str]
    Limit: NotRequired[int]


class TapeRecoveryPointInfoTypeDef(TypedDict):
    TapeARN: NotRequired[str]
    TapeRecoveryPointTime: NotRequired[datetime]
    TapeSizeInBytes: NotRequired[int]
    TapeStatus: NotRequired[str]


class DescribeTapesInputRequestTypeDef(TypedDict):
    GatewayARN: str
    TapeARNs: NotRequired[Sequence[str]]
    Marker: NotRequired[str]
    Limit: NotRequired[int]


class TapeTypeDef(TypedDict):
    TapeARN: NotRequired[str]
    TapeBarcode: NotRequired[str]
    TapeCreatedDate: NotRequired[datetime]
    TapeSizeInBytes: NotRequired[int]
    TapeStatus: NotRequired[str]
    VTLDevice: NotRequired[str]
    Progress: NotRequired[float]
    TapeUsedInBytes: NotRequired[int]
    KMSKey: NotRequired[str]
    PoolId: NotRequired[str]
    Worm: NotRequired[bool]
    RetentionStartDate: NotRequired[datetime]
    PoolEntryDate: NotRequired[datetime]


class DescribeUploadBufferInputRequestTypeDef(TypedDict):
    GatewayARN: str


class DescribeVTLDevicesInputRequestTypeDef(TypedDict):
    GatewayARN: str
    VTLDeviceARNs: NotRequired[Sequence[str]]
    Marker: NotRequired[str]
    Limit: NotRequired[int]


class DescribeWorkingStorageInputRequestTypeDef(TypedDict):
    GatewayARN: str


class DetachVolumeInputRequestTypeDef(TypedDict):
    VolumeARN: str
    ForceDetach: NotRequired[bool]


class DeviceiSCSIAttributesTypeDef(TypedDict):
    TargetARN: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]
    NetworkInterfacePort: NotRequired[int]
    ChapEnabled: NotRequired[bool]


class DisableGatewayInputRequestTypeDef(TypedDict):
    GatewayARN: str


class DisassociateFileSystemInputRequestTypeDef(TypedDict):
    FileSystemAssociationARN: str
    ForceDelete: NotRequired[bool]


class DiskTypeDef(TypedDict):
    DiskId: NotRequired[str]
    DiskPath: NotRequired[str]
    DiskNode: NotRequired[str]
    DiskStatus: NotRequired[str]
    DiskSizeInBytes: NotRequired[int]
    DiskAllocationType: NotRequired[str]
    DiskAllocationResource: NotRequired[str]
    DiskAttributeList: NotRequired[List[str]]


class EndpointNetworkConfigurationOutputTypeDef(TypedDict):
    IpAddresses: NotRequired[List[str]]


class FileShareInfoTypeDef(TypedDict):
    FileShareType: NotRequired[FileShareTypeType]
    FileShareARN: NotRequired[str]
    FileShareId: NotRequired[str]
    FileShareStatus: NotRequired[str]
    GatewayARN: NotRequired[str]


class FileSystemAssociationStatusDetailTypeDef(TypedDict):
    ErrorCode: NotRequired[str]


class FileSystemAssociationSummaryTypeDef(TypedDict):
    FileSystemAssociationId: NotRequired[str]
    FileSystemAssociationARN: NotRequired[str]
    FileSystemAssociationStatus: NotRequired[str]
    GatewayARN: NotRequired[str]


class GatewayInfoTypeDef(TypedDict):
    GatewayId: NotRequired[str]
    GatewayARN: NotRequired[str]
    GatewayType: NotRequired[str]
    GatewayOperationalState: NotRequired[str]
    GatewayName: NotRequired[str]
    Ec2InstanceId: NotRequired[str]
    Ec2InstanceRegion: NotRequired[str]
    HostEnvironment: NotRequired[HostEnvironmentType]
    HostEnvironmentId: NotRequired[str]
    DeprecationDate: NotRequired[str]
    SoftwareVersion: NotRequired[str]


class JoinDomainInputRequestTypeDef(TypedDict):
    GatewayARN: str
    DomainName: str
    UserName: str
    Password: str
    OrganizationalUnit: NotRequired[str]
    DomainControllers: NotRequired[Sequence[str]]
    TimeoutInSeconds: NotRequired[int]


class ListAutomaticTapeCreationPoliciesInputRequestTypeDef(TypedDict):
    GatewayARN: NotRequired[str]


class ListFileSharesInputRequestTypeDef(TypedDict):
    GatewayARN: NotRequired[str]
    Limit: NotRequired[int]
    Marker: NotRequired[str]


class ListFileSystemAssociationsInputRequestTypeDef(TypedDict):
    GatewayARN: NotRequired[str]
    Limit: NotRequired[int]
    Marker: NotRequired[str]


class ListGatewaysInputRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    Limit: NotRequired[int]


class ListLocalDisksInputRequestTypeDef(TypedDict):
    GatewayARN: str


class ListTagsForResourceInputRequestTypeDef(TypedDict):
    ResourceARN: str
    Marker: NotRequired[str]
    Limit: NotRequired[int]


class ListTapePoolsInputRequestTypeDef(TypedDict):
    PoolARNs: NotRequired[Sequence[str]]
    Marker: NotRequired[str]
    Limit: NotRequired[int]


class PoolInfoTypeDef(TypedDict):
    PoolARN: NotRequired[str]
    PoolName: NotRequired[str]
    StorageClass: NotRequired[TapeStorageClassType]
    RetentionLockType: NotRequired[RetentionLockTypeType]
    RetentionLockTimeInDays: NotRequired[int]
    PoolStatus: NotRequired[PoolStatusType]


class ListTapesInputRequestTypeDef(TypedDict):
    TapeARNs: NotRequired[Sequence[str]]
    Marker: NotRequired[str]
    Limit: NotRequired[int]


class TapeInfoTypeDef(TypedDict):
    TapeARN: NotRequired[str]
    TapeBarcode: NotRequired[str]
    TapeSizeInBytes: NotRequired[int]
    TapeStatus: NotRequired[str]
    GatewayARN: NotRequired[str]
    PoolId: NotRequired[str]
    RetentionStartDate: NotRequired[datetime]
    PoolEntryDate: NotRequired[datetime]


class ListVolumeInitiatorsInputRequestTypeDef(TypedDict):
    VolumeARN: str


class ListVolumeRecoveryPointsInputRequestTypeDef(TypedDict):
    GatewayARN: str


class VolumeRecoveryPointInfoTypeDef(TypedDict):
    VolumeARN: NotRequired[str]
    VolumeSizeInBytes: NotRequired[int]
    VolumeUsageInBytes: NotRequired[int]
    VolumeRecoveryPointTime: NotRequired[str]


class ListVolumesInputRequestTypeDef(TypedDict):
    GatewayARN: NotRequired[str]
    Marker: NotRequired[str]
    Limit: NotRequired[int]


class VolumeInfoTypeDef(TypedDict):
    VolumeARN: NotRequired[str]
    VolumeId: NotRequired[str]
    GatewayARN: NotRequired[str]
    GatewayId: NotRequired[str]
    VolumeType: NotRequired[str]
    VolumeSizeInBytes: NotRequired[int]
    VolumeAttachmentStatus: NotRequired[str]


class NotifyWhenUploadedInputRequestTypeDef(TypedDict):
    FileShareARN: str


class RefreshCacheInputRequestTypeDef(TypedDict):
    FileShareARN: str
    FolderList: NotRequired[Sequence[str]]
    Recursive: NotRequired[bool]


class RemoveTagsFromResourceInputRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


class ResetCacheInputRequestTypeDef(TypedDict):
    GatewayARN: str


class RetrieveTapeArchiveInputRequestTypeDef(TypedDict):
    TapeARN: str
    GatewayARN: str


class RetrieveTapeRecoveryPointInputRequestTypeDef(TypedDict):
    TapeARN: str
    GatewayARN: str


class SMBLocalGroupsTypeDef(TypedDict):
    GatewayAdmins: NotRequired[Sequence[str]]


class SetLocalConsolePasswordInputRequestTypeDef(TypedDict):
    GatewayARN: str
    LocalConsolePassword: str


class SetSMBGuestPasswordInputRequestTypeDef(TypedDict):
    GatewayARN: str
    Password: str


class ShutdownGatewayInputRequestTypeDef(TypedDict):
    GatewayARN: str


class StartAvailabilityMonitorTestInputRequestTypeDef(TypedDict):
    GatewayARN: str


class StartGatewayInputRequestTypeDef(TypedDict):
    GatewayARN: str


class UpdateBandwidthRateLimitInputRequestTypeDef(TypedDict):
    GatewayARN: str
    AverageUploadRateLimitInBitsPerSec: NotRequired[int]
    AverageDownloadRateLimitInBitsPerSec: NotRequired[int]


class UpdateChapCredentialsInputRequestTypeDef(TypedDict):
    TargetARN: str
    SecretToAuthenticateInitiator: str
    InitiatorName: str
    SecretToAuthenticateTarget: NotRequired[str]


class UpdateGatewayInformationInputRequestTypeDef(TypedDict):
    GatewayARN: str
    GatewayName: NotRequired[str]
    GatewayTimezone: NotRequired[str]
    CloudWatchLogGroupARN: NotRequired[str]
    GatewayCapacity: NotRequired[GatewayCapacityType]


class UpdateGatewaySoftwareNowInputRequestTypeDef(TypedDict):
    GatewayARN: str


class UpdateSMBFileShareVisibilityInputRequestTypeDef(TypedDict):
    GatewayARN: str
    FileSharesVisible: bool


class UpdateSMBSecurityStrategyInputRequestTypeDef(TypedDict):
    GatewayARN: str
    SMBSecurityStrategy: SMBSecurityStrategyType


class UpdateVTLDeviceTypeInputRequestTypeDef(TypedDict):
    VTLDeviceARN: str
    DeviceType: str


class ActivateGatewayInputRequestTypeDef(TypedDict):
    ActivationKey: str
    GatewayName: str
    GatewayTimezone: str
    GatewayRegion: str
    GatewayType: NotRequired[str]
    TapeDriveType: NotRequired[str]
    MediumChangerType: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class AddTagsToResourceInputRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]


class CreateCachediSCSIVolumeInputRequestTypeDef(TypedDict):
    GatewayARN: str
    VolumeSizeInBytes: int
    TargetName: str
    NetworkInterfaceId: str
    ClientToken: str
    SnapshotId: NotRequired[str]
    SourceVolumeARN: NotRequired[str]
    KMSEncrypted: NotRequired[bool]
    KMSKey: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateSnapshotFromVolumeRecoveryPointInputRequestTypeDef(TypedDict):
    VolumeARN: str
    SnapshotDescription: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateSnapshotInputRequestTypeDef(TypedDict):
    VolumeARN: str
    SnapshotDescription: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateStorediSCSIVolumeInputRequestTypeDef(TypedDict):
    GatewayARN: str
    DiskId: str
    PreserveExistingData: bool
    TargetName: str
    NetworkInterfaceId: str
    SnapshotId: NotRequired[str]
    KMSEncrypted: NotRequired[bool]
    KMSKey: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateTapePoolInputRequestTypeDef(TypedDict):
    PoolName: str
    StorageClass: TapeStorageClassType
    RetentionLockType: NotRequired[RetentionLockTypeType]
    RetentionLockTimeInDays: NotRequired[int]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateTapeWithBarcodeInputRequestTypeDef(TypedDict):
    GatewayARN: str
    TapeSizeInBytes: int
    TapeBarcode: str
    KMSEncrypted: NotRequired[bool]
    KMSKey: NotRequired[str]
    PoolId: NotRequired[str]
    Worm: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateTapesInputRequestTypeDef(TypedDict):
    GatewayARN: str
    TapeSizeInBytes: int
    ClientToken: str
    NumTapesToCreate: int
    TapeBarcodePrefix: str
    KMSEncrypted: NotRequired[bool]
    KMSKey: NotRequired[str]
    PoolId: NotRequired[str]
    Worm: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateSnapshotScheduleInputRequestTypeDef(TypedDict):
    VolumeARN: str
    StartAt: int
    RecurrenceInHours: int
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class ActivateGatewayOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class AddCacheOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class AddTagsToResourceOutputTypeDef(TypedDict):
    ResourceARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class AddUploadBufferOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class AddWorkingStorageOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssignTapePoolOutputTypeDef(TypedDict):
    TapeARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateFileSystemOutputTypeDef(TypedDict):
    FileSystemAssociationARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class AttachVolumeOutputTypeDef(TypedDict):
    VolumeARN: str
    TargetARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class CancelArchivalOutputTypeDef(TypedDict):
    TapeARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class CancelRetrievalOutputTypeDef(TypedDict):
    TapeARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCachediSCSIVolumeOutputTypeDef(TypedDict):
    VolumeARN: str
    TargetARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateNFSFileShareOutputTypeDef(TypedDict):
    FileShareARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSMBFileShareOutputTypeDef(TypedDict):
    FileShareARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSnapshotFromVolumeRecoveryPointOutputTypeDef(TypedDict):
    SnapshotId: str
    VolumeARN: str
    VolumeRecoveryPointTime: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSnapshotOutputTypeDef(TypedDict):
    VolumeARN: str
    SnapshotId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateStorediSCSIVolumeOutputTypeDef(TypedDict):
    VolumeARN: str
    VolumeSizeInBytes: int
    TargetARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTapePoolOutputTypeDef(TypedDict):
    PoolARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTapeWithBarcodeOutputTypeDef(TypedDict):
    TapeARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTapesOutputTypeDef(TypedDict):
    TapeARNs: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteAutomaticTapeCreationPolicyOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteBandwidthRateLimitOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteChapCredentialsOutputTypeDef(TypedDict):
    TargetARN: str
    InitiatorName: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteFileShareOutputTypeDef(TypedDict):
    FileShareARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteGatewayOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSnapshotScheduleOutputTypeDef(TypedDict):
    VolumeARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTapeArchiveOutputTypeDef(TypedDict):
    TapeARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTapeOutputTypeDef(TypedDict):
    TapeARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTapePoolOutputTypeDef(TypedDict):
    PoolARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVolumeOutputTypeDef(TypedDict):
    VolumeARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAvailabilityMonitorTestOutputTypeDef(TypedDict):
    GatewayARN: str
    Status: AvailabilityMonitorTestStatusType
    StartTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeBandwidthRateLimitOutputTypeDef(TypedDict):
    GatewayARN: str
    AverageUploadRateLimitInBitsPerSec: int
    AverageDownloadRateLimitInBitsPerSec: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCacheOutputTypeDef(TypedDict):
    GatewayARN: str
    DiskIds: List[str]
    CacheAllocatedInBytes: int
    CacheUsedPercentage: float
    CacheDirtyPercentage: float
    CacheHitPercentage: float
    CacheMissPercentage: float
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSnapshotScheduleOutputTypeDef(TypedDict):
    VolumeARN: str
    StartAt: int
    RecurrenceInHours: int
    Description: str
    Timezone: str
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeUploadBufferOutputTypeDef(TypedDict):
    GatewayARN: str
    DiskIds: List[str]
    UploadBufferUsedInBytes: int
    UploadBufferAllocatedInBytes: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeWorkingStorageOutputTypeDef(TypedDict):
    GatewayARN: str
    DiskIds: List[str]
    WorkingStorageUsedInBytes: int
    WorkingStorageAllocatedInBytes: int
    ResponseMetadata: ResponseMetadataTypeDef


class DetachVolumeOutputTypeDef(TypedDict):
    VolumeARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisableGatewayOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateFileSystemOutputTypeDef(TypedDict):
    FileSystemAssociationARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class JoinDomainOutputTypeDef(TypedDict):
    GatewayARN: str
    ActiveDirectoryStatus: ActiveDirectoryStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceOutputTypeDef(TypedDict):
    ResourceARN: str
    Marker: str
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListVolumeInitiatorsOutputTypeDef(TypedDict):
    Initiators: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class NotifyWhenUploadedOutputTypeDef(TypedDict):
    FileShareARN: str
    NotificationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class RefreshCacheOutputTypeDef(TypedDict):
    FileShareARN: str
    NotificationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class RemoveTagsFromResourceOutputTypeDef(TypedDict):
    ResourceARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class ResetCacheOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class RetrieveTapeArchiveOutputTypeDef(TypedDict):
    TapeARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class RetrieveTapeRecoveryPointOutputTypeDef(TypedDict):
    TapeARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class SetLocalConsolePasswordOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class SetSMBGuestPasswordOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class ShutdownGatewayOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartAvailabilityMonitorTestOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartGatewayOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAutomaticTapeCreationPolicyOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBandwidthRateLimitOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBandwidthRateLimitScheduleOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateChapCredentialsOutputTypeDef(TypedDict):
    TargetARN: str
    InitiatorName: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFileSystemAssociationOutputTypeDef(TypedDict):
    FileSystemAssociationARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateGatewayInformationOutputTypeDef(TypedDict):
    GatewayARN: str
    GatewayName: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateGatewaySoftwareNowOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMaintenanceStartTimeOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateNFSFileShareOutputTypeDef(TypedDict):
    FileShareARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSMBFileShareOutputTypeDef(TypedDict):
    FileShareARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSMBFileShareVisibilityOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSMBLocalGroupsOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSMBSecurityStrategyOutputTypeDef(TypedDict):
    GatewayARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSnapshotScheduleOutputTypeDef(TypedDict):
    VolumeARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateVTLDeviceTypeOutputTypeDef(TypedDict):
    VTLDeviceARN: str
    ResponseMetadata: ResponseMetadataTypeDef


CreateSMBFileShareInputRequestTypeDef = TypedDict(
    "CreateSMBFileShareInputRequestTypeDef",
    {
        "ClientToken": str,
        "GatewayARN": str,
        "Role": str,
        "LocationARN": str,
        "EncryptionType": NotRequired[EncryptionTypeType],
        "KMSEncrypted": NotRequired[bool],
        "KMSKey": NotRequired[str],
        "DefaultStorageClass": NotRequired[str],
        "ObjectACL": NotRequired[ObjectACLType],
        "ReadOnly": NotRequired[bool],
        "GuessMIMETypeEnabled": NotRequired[bool],
        "RequesterPays": NotRequired[bool],
        "SMBACLEnabled": NotRequired[bool],
        "AccessBasedEnumeration": NotRequired[bool],
        "AdminUserList": NotRequired[Sequence[str]],
        "ValidUserList": NotRequired[Sequence[str]],
        "InvalidUserList": NotRequired[Sequence[str]],
        "AuditDestinationARN": NotRequired[str],
        "Authentication": NotRequired[str],
        "CaseSensitivity": NotRequired[CaseSensitivityType],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "FileShareName": NotRequired[str],
        "CacheAttributes": NotRequired[CacheAttributesTypeDef],
        "NotificationPolicy": NotRequired[str],
        "VPCEndpointDNSName": NotRequired[str],
        "BucketRegion": NotRequired[str],
        "OplocksEnabled": NotRequired[bool],
    },
)
SMBFileShareInfoTypeDef = TypedDict(
    "SMBFileShareInfoTypeDef",
    {
        "FileShareARN": NotRequired[str],
        "FileShareId": NotRequired[str],
        "FileShareStatus": NotRequired[str],
        "GatewayARN": NotRequired[str],
        "EncryptionType": NotRequired[EncryptionTypeType],
        "KMSEncrypted": NotRequired[bool],
        "KMSKey": NotRequired[str],
        "Path": NotRequired[str],
        "Role": NotRequired[str],
        "LocationARN": NotRequired[str],
        "DefaultStorageClass": NotRequired[str],
        "ObjectACL": NotRequired[ObjectACLType],
        "ReadOnly": NotRequired[bool],
        "GuessMIMETypeEnabled": NotRequired[bool],
        "RequesterPays": NotRequired[bool],
        "SMBACLEnabled": NotRequired[bool],
        "AccessBasedEnumeration": NotRequired[bool],
        "AdminUserList": NotRequired[List[str]],
        "ValidUserList": NotRequired[List[str]],
        "InvalidUserList": NotRequired[List[str]],
        "AuditDestinationARN": NotRequired[str],
        "Authentication": NotRequired[str],
        "CaseSensitivity": NotRequired[CaseSensitivityType],
        "Tags": NotRequired[List[TagTypeDef]],
        "FileShareName": NotRequired[str],
        "CacheAttributes": NotRequired[CacheAttributesTypeDef],
        "NotificationPolicy": NotRequired[str],
        "VPCEndpointDNSName": NotRequired[str],
        "BucketRegion": NotRequired[str],
        "OplocksEnabled": NotRequired[bool],
    },
)


class UpdateFileSystemAssociationInputRequestTypeDef(TypedDict):
    FileSystemAssociationARN: str
    UserName: NotRequired[str]
    Password: NotRequired[str]
    AuditDestinationARN: NotRequired[str]
    CacheAttributes: NotRequired[CacheAttributesTypeDef]


UpdateSMBFileShareInputRequestTypeDef = TypedDict(
    "UpdateSMBFileShareInputRequestTypeDef",
    {
        "FileShareARN": str,
        "EncryptionType": NotRequired[EncryptionTypeType],
        "KMSEncrypted": NotRequired[bool],
        "KMSKey": NotRequired[str],
        "DefaultStorageClass": NotRequired[str],
        "ObjectACL": NotRequired[ObjectACLType],
        "ReadOnly": NotRequired[bool],
        "GuessMIMETypeEnabled": NotRequired[bool],
        "RequesterPays": NotRequired[bool],
        "SMBACLEnabled": NotRequired[bool],
        "AccessBasedEnumeration": NotRequired[bool],
        "AdminUserList": NotRequired[Sequence[str]],
        "ValidUserList": NotRequired[Sequence[str]],
        "InvalidUserList": NotRequired[Sequence[str]],
        "AuditDestinationARN": NotRequired[str],
        "CaseSensitivity": NotRequired[CaseSensitivityType],
        "FileShareName": NotRequired[str],
        "CacheAttributes": NotRequired[CacheAttributesTypeDef],
        "NotificationPolicy": NotRequired[str],
        "OplocksEnabled": NotRequired[bool],
    },
)


class AssociateFileSystemInputRequestTypeDef(TypedDict):
    UserName: str
    Password: str
    ClientToken: str
    GatewayARN: str
    LocationARN: str
    Tags: NotRequired[Sequence[TagTypeDef]]
    AuditDestinationARN: NotRequired[str]
    CacheAttributes: NotRequired[CacheAttributesTypeDef]
    EndpointNetworkConfiguration: NotRequired[EndpointNetworkConfigurationTypeDef]


class AutomaticTapeCreationPolicyInfoTypeDef(TypedDict):
    AutomaticTapeCreationRules: NotRequired[List[AutomaticTapeCreationRuleTypeDef]]
    GatewayARN: NotRequired[str]


class UpdateAutomaticTapeCreationPolicyInputRequestTypeDef(TypedDict):
    AutomaticTapeCreationRules: Sequence[AutomaticTapeCreationRuleTypeDef]
    GatewayARN: str


class DescribeBandwidthRateLimitScheduleOutputTypeDef(TypedDict):
    GatewayARN: str
    BandwidthRateLimitIntervals: List[BandwidthRateLimitIntervalOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


BandwidthRateLimitIntervalUnionTypeDef = Union[
    BandwidthRateLimitIntervalTypeDef, BandwidthRateLimitIntervalOutputTypeDef
]


class CachediSCSIVolumeTypeDef(TypedDict):
    VolumeARN: NotRequired[str]
    VolumeId: NotRequired[str]
    VolumeType: NotRequired[str]
    VolumeStatus: NotRequired[str]
    VolumeAttachmentStatus: NotRequired[str]
    VolumeSizeInBytes: NotRequired[int]
    VolumeProgress: NotRequired[float]
    SourceSnapshotId: NotRequired[str]
    VolumeiSCSIAttributes: NotRequired[VolumeiSCSIAttributesTypeDef]
    CreatedDate: NotRequired[datetime]
    VolumeUsedInBytes: NotRequired[int]
    KMSKey: NotRequired[str]
    TargetName: NotRequired[str]


class StorediSCSIVolumeTypeDef(TypedDict):
    VolumeARN: NotRequired[str]
    VolumeId: NotRequired[str]
    VolumeType: NotRequired[str]
    VolumeStatus: NotRequired[str]
    VolumeAttachmentStatus: NotRequired[str]
    VolumeSizeInBytes: NotRequired[int]
    VolumeProgress: NotRequired[float]
    VolumeDiskId: NotRequired[str]
    SourceSnapshotId: NotRequired[str]
    PreservedExistingData: NotRequired[bool]
    VolumeiSCSIAttributes: NotRequired[VolumeiSCSIAttributesTypeDef]
    CreatedDate: NotRequired[datetime]
    VolumeUsedInBytes: NotRequired[int]
    KMSKey: NotRequired[str]
    TargetName: NotRequired[str]


class DescribeChapCredentialsOutputTypeDef(TypedDict):
    ChapCredentials: List[ChapInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


CreateNFSFileShareInputRequestTypeDef = TypedDict(
    "CreateNFSFileShareInputRequestTypeDef",
    {
        "ClientToken": str,
        "GatewayARN": str,
        "Role": str,
        "LocationARN": str,
        "NFSFileShareDefaults": NotRequired[NFSFileShareDefaultsTypeDef],
        "EncryptionType": NotRequired[EncryptionTypeType],
        "KMSEncrypted": NotRequired[bool],
        "KMSKey": NotRequired[str],
        "DefaultStorageClass": NotRequired[str],
        "ObjectACL": NotRequired[ObjectACLType],
        "ClientList": NotRequired[Sequence[str]],
        "Squash": NotRequired[str],
        "ReadOnly": NotRequired[bool],
        "GuessMIMETypeEnabled": NotRequired[bool],
        "RequesterPays": NotRequired[bool],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "FileShareName": NotRequired[str],
        "CacheAttributes": NotRequired[CacheAttributesTypeDef],
        "NotificationPolicy": NotRequired[str],
        "VPCEndpointDNSName": NotRequired[str],
        "BucketRegion": NotRequired[str],
        "AuditDestinationARN": NotRequired[str],
    },
)
NFSFileShareInfoTypeDef = TypedDict(
    "NFSFileShareInfoTypeDef",
    {
        "NFSFileShareDefaults": NotRequired[NFSFileShareDefaultsTypeDef],
        "FileShareARN": NotRequired[str],
        "FileShareId": NotRequired[str],
        "FileShareStatus": NotRequired[str],
        "GatewayARN": NotRequired[str],
        "EncryptionType": NotRequired[EncryptionTypeType],
        "KMSEncrypted": NotRequired[bool],
        "KMSKey": NotRequired[str],
        "Path": NotRequired[str],
        "Role": NotRequired[str],
        "LocationARN": NotRequired[str],
        "DefaultStorageClass": NotRequired[str],
        "ObjectACL": NotRequired[ObjectACLType],
        "ClientList": NotRequired[List[str]],
        "Squash": NotRequired[str],
        "ReadOnly": NotRequired[bool],
        "GuessMIMETypeEnabled": NotRequired[bool],
        "RequesterPays": NotRequired[bool],
        "Tags": NotRequired[List[TagTypeDef]],
        "FileShareName": NotRequired[str],
        "CacheAttributes": NotRequired[CacheAttributesTypeDef],
        "NotificationPolicy": NotRequired[str],
        "VPCEndpointDNSName": NotRequired[str],
        "BucketRegion": NotRequired[str],
        "AuditDestinationARN": NotRequired[str],
    },
)
UpdateNFSFileShareInputRequestTypeDef = TypedDict(
    "UpdateNFSFileShareInputRequestTypeDef",
    {
        "FileShareARN": str,
        "EncryptionType": NotRequired[EncryptionTypeType],
        "KMSEncrypted": NotRequired[bool],
        "KMSKey": NotRequired[str],
        "NFSFileShareDefaults": NotRequired[NFSFileShareDefaultsTypeDef],
        "DefaultStorageClass": NotRequired[str],
        "ObjectACL": NotRequired[ObjectACLType],
        "ClientList": NotRequired[Sequence[str]],
        "Squash": NotRequired[str],
        "ReadOnly": NotRequired[bool],
        "GuessMIMETypeEnabled": NotRequired[bool],
        "RequesterPays": NotRequired[bool],
        "FileShareName": NotRequired[str],
        "CacheAttributes": NotRequired[CacheAttributesTypeDef],
        "NotificationPolicy": NotRequired[str],
        "AuditDestinationARN": NotRequired[str],
    },
)


class DescribeGatewayInformationOutputTypeDef(TypedDict):
    GatewayARN: str
    GatewayId: str
    GatewayName: str
    GatewayTimezone: str
    GatewayState: str
    GatewayNetworkInterfaces: List[NetworkInterfaceTypeDef]
    GatewayType: str
    NextUpdateAvailabilityDate: str
    LastSoftwareUpdate: str
    Ec2InstanceId: str
    Ec2InstanceRegion: str
    Tags: List[TagTypeDef]
    VPCEndpoint: str
    CloudWatchLogGroupARN: str
    HostEnvironment: HostEnvironmentType
    EndpointType: str
    SoftwareUpdatesEndDate: str
    DeprecationDate: str
    GatewayCapacity: GatewayCapacityType
    SupportedGatewayCapacities: List[GatewayCapacityType]
    HostEnvironmentId: str
    SoftwareVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeMaintenanceStartTimeOutputTypeDef(TypedDict):
    GatewayARN: str
    HourOfDay: int
    MinuteOfHour: int
    DayOfWeek: int
    DayOfMonth: int
    Timezone: str
    SoftwareUpdatePreferences: SoftwareUpdatePreferencesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMaintenanceStartTimeInputRequestTypeDef(TypedDict):
    GatewayARN: str
    HourOfDay: NotRequired[int]
    MinuteOfHour: NotRequired[int]
    DayOfWeek: NotRequired[int]
    DayOfMonth: NotRequired[int]
    SoftwareUpdatePreferences: NotRequired[SoftwareUpdatePreferencesTypeDef]


class DescribeSMBSettingsOutputTypeDef(TypedDict):
    GatewayARN: str
    DomainName: str
    ActiveDirectoryStatus: ActiveDirectoryStatusType
    SMBGuestPasswordSet: bool
    SMBSecurityStrategy: SMBSecurityStrategyType
    FileSharesVisible: bool
    SMBLocalGroups: SMBLocalGroupsOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTapeArchivesInputDescribeTapeArchivesPaginateTypeDef(TypedDict):
    TapeARNs: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTapeRecoveryPointsInputDescribeTapeRecoveryPointsPaginateTypeDef(TypedDict):
    GatewayARN: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTapesInputDescribeTapesPaginateTypeDef(TypedDict):
    GatewayARN: str
    TapeARNs: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVTLDevicesInputDescribeVTLDevicesPaginateTypeDef(TypedDict):
    GatewayARN: str
    VTLDeviceARNs: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFileSharesInputListFileSharesPaginateTypeDef(TypedDict):
    GatewayARN: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFileSystemAssociationsInputListFileSystemAssociationsPaginateTypeDef(TypedDict):
    GatewayARN: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGatewaysInputListGatewaysPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagsForResourceInputListTagsForResourcePaginateTypeDef(TypedDict):
    ResourceARN: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTapePoolsInputListTapePoolsPaginateTypeDef(TypedDict):
    PoolARNs: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTapesInputListTapesPaginateTypeDef(TypedDict):
    TapeARNs: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListVolumesInputListVolumesPaginateTypeDef(TypedDict):
    GatewayARN: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTapeArchivesOutputTypeDef(TypedDict):
    TapeArchives: List[TapeArchiveTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTapeRecoveryPointsOutputTypeDef(TypedDict):
    GatewayARN: str
    TapeRecoveryPointInfos: List[TapeRecoveryPointInfoTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTapesOutputTypeDef(TypedDict):
    Tapes: List[TapeTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class VTLDeviceTypeDef(TypedDict):
    VTLDeviceARN: NotRequired[str]
    VTLDeviceType: NotRequired[str]
    VTLDeviceVendor: NotRequired[str]
    VTLDeviceProductIdentifier: NotRequired[str]
    DeviceiSCSIAttributes: NotRequired[DeviceiSCSIAttributesTypeDef]


class ListLocalDisksOutputTypeDef(TypedDict):
    GatewayARN: str
    Disks: List[DiskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListFileSharesOutputTypeDef(TypedDict):
    Marker: str
    NextMarker: str
    FileShareInfoList: List[FileShareInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class FileSystemAssociationInfoTypeDef(TypedDict):
    FileSystemAssociationARN: NotRequired[str]
    LocationARN: NotRequired[str]
    FileSystemAssociationStatus: NotRequired[str]
    AuditDestinationARN: NotRequired[str]
    GatewayARN: NotRequired[str]
    Tags: NotRequired[List[TagTypeDef]]
    CacheAttributes: NotRequired[CacheAttributesTypeDef]
    EndpointNetworkConfiguration: NotRequired[EndpointNetworkConfigurationOutputTypeDef]
    FileSystemAssociationStatusDetails: NotRequired[List[FileSystemAssociationStatusDetailTypeDef]]


class ListFileSystemAssociationsOutputTypeDef(TypedDict):
    Marker: str
    NextMarker: str
    FileSystemAssociationSummaryList: List[FileSystemAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListGatewaysOutputTypeDef(TypedDict):
    Gateways: List[GatewayInfoTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTapePoolsOutputTypeDef(TypedDict):
    PoolInfos: List[PoolInfoTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTapesOutputTypeDef(TypedDict):
    TapeInfos: List[TapeInfoTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListVolumeRecoveryPointsOutputTypeDef(TypedDict):
    GatewayARN: str
    VolumeRecoveryPointInfos: List[VolumeRecoveryPointInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListVolumesOutputTypeDef(TypedDict):
    GatewayARN: str
    Marker: str
    VolumeInfos: List[VolumeInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSMBLocalGroupsInputRequestTypeDef(TypedDict):
    GatewayARN: str
    SMBLocalGroups: SMBLocalGroupsTypeDef


class DescribeSMBFileSharesOutputTypeDef(TypedDict):
    SMBFileShareInfoList: List[SMBFileShareInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListAutomaticTapeCreationPoliciesOutputTypeDef(TypedDict):
    AutomaticTapeCreationPolicyInfos: List[AutomaticTapeCreationPolicyInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBandwidthRateLimitScheduleInputRequestTypeDef(TypedDict):
    GatewayARN: str
    BandwidthRateLimitIntervals: Sequence[BandwidthRateLimitIntervalUnionTypeDef]


class DescribeCachediSCSIVolumesOutputTypeDef(TypedDict):
    CachediSCSIVolumes: List[CachediSCSIVolumeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeStorediSCSIVolumesOutputTypeDef(TypedDict):
    StorediSCSIVolumes: List[StorediSCSIVolumeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeNFSFileSharesOutputTypeDef(TypedDict):
    NFSFileShareInfoList: List[NFSFileShareInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVTLDevicesOutputTypeDef(TypedDict):
    GatewayARN: str
    VTLDevices: List[VTLDeviceTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFileSystemAssociationsOutputTypeDef(TypedDict):
    FileSystemAssociationInfoList: List[FileSystemAssociationInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
