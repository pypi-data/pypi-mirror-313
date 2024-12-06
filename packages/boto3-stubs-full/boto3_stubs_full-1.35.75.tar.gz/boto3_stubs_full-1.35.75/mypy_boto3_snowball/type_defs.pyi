"""
Type annotations for snowball service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snowball/type_defs/)

Usage::

    ```python
    from mypy_boto3_snowball.type_defs import AddressTypeDef

    data: AddressTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AddressTypeType,
    ClusterStateType,
    DeviceServiceNameType,
    ImpactLevelType,
    JobStateType,
    JobTypeType,
    LongTermPricingTypeType,
    RemoteManagementType,
    ServiceNameType,
    ShipmentStateType,
    ShippingLabelStatusType,
    ShippingOptionType,
    SnowballCapacityType,
    SnowballTypeType,
    TransferOptionType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AddressTypeDef",
    "CancelClusterRequestRequestTypeDef",
    "CancelJobRequestRequestTypeDef",
    "ClusterListEntryTypeDef",
    "ClusterMetadataTypeDef",
    "CompatibleImageTypeDef",
    "CreateAddressRequestRequestTypeDef",
    "CreateAddressResultTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "CreateClusterResultTypeDef",
    "CreateJobRequestRequestTypeDef",
    "CreateJobResultTypeDef",
    "CreateLongTermPricingRequestRequestTypeDef",
    "CreateLongTermPricingResultTypeDef",
    "CreateReturnShippingLabelRequestRequestTypeDef",
    "CreateReturnShippingLabelResultTypeDef",
    "DataTransferTypeDef",
    "DependentServiceTypeDef",
    "DescribeAddressRequestRequestTypeDef",
    "DescribeAddressResultTypeDef",
    "DescribeAddressesRequestDescribeAddressesPaginateTypeDef",
    "DescribeAddressesRequestRequestTypeDef",
    "DescribeAddressesResultTypeDef",
    "DescribeClusterRequestRequestTypeDef",
    "DescribeClusterResultTypeDef",
    "DescribeJobRequestRequestTypeDef",
    "DescribeJobResultTypeDef",
    "DescribeReturnShippingLabelRequestRequestTypeDef",
    "DescribeReturnShippingLabelResultTypeDef",
    "DeviceConfigurationTypeDef",
    "EKSOnDeviceServiceConfigurationTypeDef",
    "Ec2AmiResourceTypeDef",
    "EventTriggerDefinitionTypeDef",
    "GetJobManifestRequestRequestTypeDef",
    "GetJobManifestResultTypeDef",
    "GetJobUnlockCodeRequestRequestTypeDef",
    "GetJobUnlockCodeResultTypeDef",
    "GetSnowballUsageResultTypeDef",
    "GetSoftwareUpdatesRequestRequestTypeDef",
    "GetSoftwareUpdatesResultTypeDef",
    "INDTaxDocumentsTypeDef",
    "JobListEntryTypeDef",
    "JobLogsTypeDef",
    "JobMetadataTypeDef",
    "JobResourceOutputTypeDef",
    "JobResourceTypeDef",
    "KeyRangeTypeDef",
    "LambdaResourceOutputTypeDef",
    "LambdaResourceTypeDef",
    "LambdaResourceUnionTypeDef",
    "ListClusterJobsRequestListClusterJobsPaginateTypeDef",
    "ListClusterJobsRequestRequestTypeDef",
    "ListClusterJobsResultTypeDef",
    "ListClustersRequestListClustersPaginateTypeDef",
    "ListClustersRequestRequestTypeDef",
    "ListClustersResultTypeDef",
    "ListCompatibleImagesRequestListCompatibleImagesPaginateTypeDef",
    "ListCompatibleImagesRequestRequestTypeDef",
    "ListCompatibleImagesResultTypeDef",
    "ListJobsRequestListJobsPaginateTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListJobsResultTypeDef",
    "ListLongTermPricingRequestListLongTermPricingPaginateTypeDef",
    "ListLongTermPricingRequestRequestTypeDef",
    "ListLongTermPricingResultTypeDef",
    "ListPickupLocationsRequestRequestTypeDef",
    "ListPickupLocationsResultTypeDef",
    "ListServiceVersionsRequestRequestTypeDef",
    "ListServiceVersionsResultTypeDef",
    "LongTermPricingListEntryTypeDef",
    "NFSOnDeviceServiceConfigurationTypeDef",
    "NotificationOutputTypeDef",
    "NotificationTypeDef",
    "OnDeviceServiceConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PickupDetailsOutputTypeDef",
    "PickupDetailsTypeDef",
    "ResponseMetadataTypeDef",
    "S3OnDeviceServiceConfigurationTypeDef",
    "S3ResourceOutputTypeDef",
    "S3ResourceTypeDef",
    "S3ResourceUnionTypeDef",
    "ServiceVersionTypeDef",
    "ShipmentTypeDef",
    "ShippingDetailsTypeDef",
    "SnowconeDeviceConfigurationTypeDef",
    "TGWOnDeviceServiceConfigurationTypeDef",
    "TargetOnDeviceServiceTypeDef",
    "TaxDocumentsTypeDef",
    "TimestampTypeDef",
    "UpdateClusterRequestRequestTypeDef",
    "UpdateJobRequestRequestTypeDef",
    "UpdateJobShipmentStateRequestRequestTypeDef",
    "UpdateLongTermPricingRequestRequestTypeDef",
    "WirelessConnectionTypeDef",
)

AddressTypeDef = TypedDict(
    "AddressTypeDef",
    {
        "AddressId": NotRequired[str],
        "Name": NotRequired[str],
        "Company": NotRequired[str],
        "Street1": NotRequired[str],
        "Street2": NotRequired[str],
        "Street3": NotRequired[str],
        "City": NotRequired[str],
        "StateOrProvince": NotRequired[str],
        "PrefectureOrDistrict": NotRequired[str],
        "Landmark": NotRequired[str],
        "Country": NotRequired[str],
        "PostalCode": NotRequired[str],
        "PhoneNumber": NotRequired[str],
        "IsRestricted": NotRequired[bool],
        "Type": NotRequired[AddressTypeType],
    },
)

class CancelClusterRequestRequestTypeDef(TypedDict):
    ClusterId: str

class CancelJobRequestRequestTypeDef(TypedDict):
    JobId: str

class ClusterListEntryTypeDef(TypedDict):
    ClusterId: NotRequired[str]
    ClusterState: NotRequired[ClusterStateType]
    CreationDate: NotRequired[datetime]
    Description: NotRequired[str]

class NotificationOutputTypeDef(TypedDict):
    SnsTopicARN: NotRequired[str]
    JobStatesToNotify: NotRequired[List[JobStateType]]
    NotifyAll: NotRequired[bool]
    DevicePickupSnsTopicARN: NotRequired[str]

class CompatibleImageTypeDef(TypedDict):
    AmiId: NotRequired[str]
    Name: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class NotificationTypeDef(TypedDict):
    SnsTopicARN: NotRequired[str]
    JobStatesToNotify: NotRequired[Sequence[JobStateType]]
    NotifyAll: NotRequired[bool]
    DevicePickupSnsTopicARN: NotRequired[str]

class JobListEntryTypeDef(TypedDict):
    JobId: NotRequired[str]
    JobState: NotRequired[JobStateType]
    IsMaster: NotRequired[bool]
    JobType: NotRequired[JobTypeType]
    SnowballType: NotRequired[SnowballTypeType]
    CreationDate: NotRequired[datetime]
    Description: NotRequired[str]

class CreateLongTermPricingRequestRequestTypeDef(TypedDict):
    LongTermPricingType: LongTermPricingTypeType
    SnowballType: SnowballTypeType
    IsLongTermPricingAutoRenew: NotRequired[bool]

class CreateReturnShippingLabelRequestRequestTypeDef(TypedDict):
    JobId: str
    ShippingOption: NotRequired[ShippingOptionType]

class DataTransferTypeDef(TypedDict):
    BytesTransferred: NotRequired[int]
    ObjectsTransferred: NotRequired[int]
    TotalBytes: NotRequired[int]
    TotalObjects: NotRequired[int]

class ServiceVersionTypeDef(TypedDict):
    Version: NotRequired[str]

class DescribeAddressRequestRequestTypeDef(TypedDict):
    AddressId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeAddressesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeClusterRequestRequestTypeDef(TypedDict):
    ClusterId: str

class DescribeJobRequestRequestTypeDef(TypedDict):
    JobId: str

class DescribeReturnShippingLabelRequestRequestTypeDef(TypedDict):
    JobId: str

class EKSOnDeviceServiceConfigurationTypeDef(TypedDict):
    KubernetesVersion: NotRequired[str]
    EKSAnywhereVersion: NotRequired[str]

class Ec2AmiResourceTypeDef(TypedDict):
    AmiId: str
    SnowballAmiId: NotRequired[str]

class EventTriggerDefinitionTypeDef(TypedDict):
    EventResourceARN: NotRequired[str]

class GetJobManifestRequestRequestTypeDef(TypedDict):
    JobId: str

class GetJobUnlockCodeRequestRequestTypeDef(TypedDict):
    JobId: str

class GetSoftwareUpdatesRequestRequestTypeDef(TypedDict):
    JobId: str

class INDTaxDocumentsTypeDef(TypedDict):
    GSTIN: NotRequired[str]

class JobLogsTypeDef(TypedDict):
    JobCompletionReportURI: NotRequired[str]
    JobSuccessLogURI: NotRequired[str]
    JobFailureLogURI: NotRequired[str]

class PickupDetailsOutputTypeDef(TypedDict):
    Name: NotRequired[str]
    PhoneNumber: NotRequired[str]
    Email: NotRequired[str]
    IdentificationNumber: NotRequired[str]
    IdentificationExpirationDate: NotRequired[datetime]
    IdentificationIssuingOrg: NotRequired[str]
    DevicePickupId: NotRequired[str]

class KeyRangeTypeDef(TypedDict):
    BeginMarker: NotRequired[str]
    EndMarker: NotRequired[str]

class ListClusterJobsRequestRequestTypeDef(TypedDict):
    ClusterId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListClustersRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListCompatibleImagesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListJobsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListLongTermPricingRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class LongTermPricingListEntryTypeDef(TypedDict):
    LongTermPricingId: NotRequired[str]
    LongTermPricingEndDate: NotRequired[datetime]
    LongTermPricingStartDate: NotRequired[datetime]
    LongTermPricingType: NotRequired[LongTermPricingTypeType]
    CurrentActiveJob: NotRequired[str]
    ReplacementJob: NotRequired[str]
    IsLongTermPricingAutoRenew: NotRequired[bool]
    LongTermPricingStatus: NotRequired[str]
    SnowballType: NotRequired[SnowballTypeType]
    JobIds: NotRequired[List[str]]

class ListPickupLocationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class NFSOnDeviceServiceConfigurationTypeDef(TypedDict):
    StorageLimit: NotRequired[int]
    StorageUnit: NotRequired[Literal["TB"]]

class S3OnDeviceServiceConfigurationTypeDef(TypedDict):
    StorageLimit: NotRequired[float]
    StorageUnit: NotRequired[Literal["TB"]]
    ServiceSize: NotRequired[int]
    FaultTolerance: NotRequired[int]

class TGWOnDeviceServiceConfigurationTypeDef(TypedDict):
    StorageLimit: NotRequired[int]
    StorageUnit: NotRequired[Literal["TB"]]

TimestampTypeDef = Union[datetime, str]
TargetOnDeviceServiceTypeDef = TypedDict(
    "TargetOnDeviceServiceTypeDef",
    {
        "ServiceName": NotRequired[DeviceServiceNameType],
        "TransferOption": NotRequired[TransferOptionType],
    },
)

class ShipmentTypeDef(TypedDict):
    Status: NotRequired[str]
    TrackingNumber: NotRequired[str]

class WirelessConnectionTypeDef(TypedDict):
    IsWifiEnabled: NotRequired[bool]

class UpdateJobShipmentStateRequestRequestTypeDef(TypedDict):
    JobId: str
    ShipmentState: ShipmentStateType

class UpdateLongTermPricingRequestRequestTypeDef(TypedDict):
    LongTermPricingId: str
    ReplacementJob: NotRequired[str]
    IsLongTermPricingAutoRenew: NotRequired[bool]

class CreateAddressRequestRequestTypeDef(TypedDict):
    Address: AddressTypeDef

class CreateAddressResultTypeDef(TypedDict):
    AddressId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateJobResultTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLongTermPricingResultTypeDef(TypedDict):
    LongTermPricingId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateReturnShippingLabelResultTypeDef(TypedDict):
    Status: ShippingLabelStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAddressResultTypeDef(TypedDict):
    Address: AddressTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAddressesResultTypeDef(TypedDict):
    Addresses: List[AddressTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeReturnShippingLabelResultTypeDef(TypedDict):
    Status: ShippingLabelStatusType
    ExpirationDate: datetime
    ReturnShippingLabelURI: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetJobManifestResultTypeDef(TypedDict):
    ManifestURI: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetJobUnlockCodeResultTypeDef(TypedDict):
    UnlockCode: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetSnowballUsageResultTypeDef(TypedDict):
    SnowballLimit: int
    SnowballsInUse: int
    ResponseMetadata: ResponseMetadataTypeDef

class GetSoftwareUpdatesResultTypeDef(TypedDict):
    UpdatesURI: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListClustersResultTypeDef(TypedDict):
    ClusterListEntries: List[ClusterListEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListCompatibleImagesResultTypeDef(TypedDict):
    CompatibleImages: List[CompatibleImageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListPickupLocationsResultTypeDef(TypedDict):
    Addresses: List[AddressTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateClusterResultTypeDef(TypedDict):
    ClusterId: str
    JobListEntries: List[JobListEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListClusterJobsResultTypeDef(TypedDict):
    JobListEntries: List[JobListEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListJobsResultTypeDef(TypedDict):
    JobListEntries: List[JobListEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

DependentServiceTypeDef = TypedDict(
    "DependentServiceTypeDef",
    {
        "ServiceName": NotRequired[ServiceNameType],
        "ServiceVersion": NotRequired[ServiceVersionTypeDef],
    },
)

class DescribeAddressesRequestDescribeAddressesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListClusterJobsRequestListClusterJobsPaginateTypeDef(TypedDict):
    ClusterId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListClustersRequestListClustersPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCompatibleImagesRequestListCompatibleImagesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListJobsRequestListJobsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLongTermPricingRequestListLongTermPricingPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class LambdaResourceOutputTypeDef(TypedDict):
    LambdaArn: NotRequired[str]
    EventTriggers: NotRequired[List[EventTriggerDefinitionTypeDef]]

class LambdaResourceTypeDef(TypedDict):
    LambdaArn: NotRequired[str]
    EventTriggers: NotRequired[Sequence[EventTriggerDefinitionTypeDef]]

class TaxDocumentsTypeDef(TypedDict):
    IND: NotRequired[INDTaxDocumentsTypeDef]

class ListLongTermPricingResultTypeDef(TypedDict):
    LongTermPricingEntries: List[LongTermPricingListEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class OnDeviceServiceConfigurationTypeDef(TypedDict):
    NFSOnDeviceService: NotRequired[NFSOnDeviceServiceConfigurationTypeDef]
    TGWOnDeviceService: NotRequired[TGWOnDeviceServiceConfigurationTypeDef]
    EKSOnDeviceService: NotRequired[EKSOnDeviceServiceConfigurationTypeDef]
    S3OnDeviceService: NotRequired[S3OnDeviceServiceConfigurationTypeDef]

class PickupDetailsTypeDef(TypedDict):
    Name: NotRequired[str]
    PhoneNumber: NotRequired[str]
    Email: NotRequired[str]
    IdentificationNumber: NotRequired[str]
    IdentificationExpirationDate: NotRequired[TimestampTypeDef]
    IdentificationIssuingOrg: NotRequired[str]
    DevicePickupId: NotRequired[str]

class S3ResourceOutputTypeDef(TypedDict):
    BucketArn: NotRequired[str]
    KeyRange: NotRequired[KeyRangeTypeDef]
    TargetOnDeviceServices: NotRequired[List[TargetOnDeviceServiceTypeDef]]

class S3ResourceTypeDef(TypedDict):
    BucketArn: NotRequired[str]
    KeyRange: NotRequired[KeyRangeTypeDef]
    TargetOnDeviceServices: NotRequired[Sequence[TargetOnDeviceServiceTypeDef]]

class ShippingDetailsTypeDef(TypedDict):
    ShippingOption: NotRequired[ShippingOptionType]
    InboundShipment: NotRequired[ShipmentTypeDef]
    OutboundShipment: NotRequired[ShipmentTypeDef]

class SnowconeDeviceConfigurationTypeDef(TypedDict):
    WirelessConnection: NotRequired[WirelessConnectionTypeDef]

ListServiceVersionsRequestRequestTypeDef = TypedDict(
    "ListServiceVersionsRequestRequestTypeDef",
    {
        "ServiceName": ServiceNameType,
        "DependentServices": NotRequired[Sequence[DependentServiceTypeDef]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
ListServiceVersionsResultTypeDef = TypedDict(
    "ListServiceVersionsResultTypeDef",
    {
        "ServiceVersions": List[ServiceVersionTypeDef],
        "ServiceName": ServiceNameType,
        "DependentServices": List[DependentServiceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
LambdaResourceUnionTypeDef = Union[LambdaResourceTypeDef, LambdaResourceOutputTypeDef]

class JobResourceOutputTypeDef(TypedDict):
    S3Resources: NotRequired[List[S3ResourceOutputTypeDef]]
    LambdaResources: NotRequired[List[LambdaResourceOutputTypeDef]]
    Ec2AmiResources: NotRequired[List[Ec2AmiResourceTypeDef]]

S3ResourceUnionTypeDef = Union[S3ResourceTypeDef, S3ResourceOutputTypeDef]

class DeviceConfigurationTypeDef(TypedDict):
    SnowconeDeviceConfiguration: NotRequired[SnowconeDeviceConfigurationTypeDef]

class ClusterMetadataTypeDef(TypedDict):
    ClusterId: NotRequired[str]
    Description: NotRequired[str]
    KmsKeyARN: NotRequired[str]
    RoleARN: NotRequired[str]
    ClusterState: NotRequired[ClusterStateType]
    JobType: NotRequired[JobTypeType]
    SnowballType: NotRequired[SnowballTypeType]
    CreationDate: NotRequired[datetime]
    Resources: NotRequired[JobResourceOutputTypeDef]
    AddressId: NotRequired[str]
    ShippingOption: NotRequired[ShippingOptionType]
    Notification: NotRequired[NotificationOutputTypeDef]
    ForwardingAddressId: NotRequired[str]
    TaxDocuments: NotRequired[TaxDocumentsTypeDef]
    OnDeviceServiceConfiguration: NotRequired[OnDeviceServiceConfigurationTypeDef]

class JobResourceTypeDef(TypedDict):
    S3Resources: NotRequired[Sequence[S3ResourceUnionTypeDef]]
    LambdaResources: NotRequired[Sequence[LambdaResourceUnionTypeDef]]
    Ec2AmiResources: NotRequired[Sequence[Ec2AmiResourceTypeDef]]

class JobMetadataTypeDef(TypedDict):
    JobId: NotRequired[str]
    JobState: NotRequired[JobStateType]
    JobType: NotRequired[JobTypeType]
    SnowballType: NotRequired[SnowballTypeType]
    CreationDate: NotRequired[datetime]
    Resources: NotRequired[JobResourceOutputTypeDef]
    Description: NotRequired[str]
    KmsKeyARN: NotRequired[str]
    RoleARN: NotRequired[str]
    AddressId: NotRequired[str]
    ShippingDetails: NotRequired[ShippingDetailsTypeDef]
    SnowballCapacityPreference: NotRequired[SnowballCapacityType]
    Notification: NotRequired[NotificationOutputTypeDef]
    DataTransferProgress: NotRequired[DataTransferTypeDef]
    JobLogInfo: NotRequired[JobLogsTypeDef]
    ClusterId: NotRequired[str]
    ForwardingAddressId: NotRequired[str]
    TaxDocuments: NotRequired[TaxDocumentsTypeDef]
    DeviceConfiguration: NotRequired[DeviceConfigurationTypeDef]
    RemoteManagement: NotRequired[RemoteManagementType]
    LongTermPricingId: NotRequired[str]
    OnDeviceServiceConfiguration: NotRequired[OnDeviceServiceConfigurationTypeDef]
    ImpactLevel: NotRequired[ImpactLevelType]
    PickupDetails: NotRequired[PickupDetailsOutputTypeDef]
    SnowballId: NotRequired[str]

class DescribeClusterResultTypeDef(TypedDict):
    ClusterMetadata: ClusterMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateClusterRequestRequestTypeDef(TypedDict):
    JobType: JobTypeType
    AddressId: str
    SnowballType: SnowballTypeType
    ShippingOption: ShippingOptionType
    Resources: NotRequired[JobResourceTypeDef]
    OnDeviceServiceConfiguration: NotRequired[OnDeviceServiceConfigurationTypeDef]
    Description: NotRequired[str]
    KmsKeyARN: NotRequired[str]
    RoleARN: NotRequired[str]
    Notification: NotRequired[NotificationTypeDef]
    ForwardingAddressId: NotRequired[str]
    TaxDocuments: NotRequired[TaxDocumentsTypeDef]
    RemoteManagement: NotRequired[RemoteManagementType]
    InitialClusterSize: NotRequired[int]
    ForceCreateJobs: NotRequired[bool]
    LongTermPricingIds: NotRequired[Sequence[str]]
    SnowballCapacityPreference: NotRequired[SnowballCapacityType]

class CreateJobRequestRequestTypeDef(TypedDict):
    JobType: NotRequired[JobTypeType]
    Resources: NotRequired[JobResourceTypeDef]
    OnDeviceServiceConfiguration: NotRequired[OnDeviceServiceConfigurationTypeDef]
    Description: NotRequired[str]
    AddressId: NotRequired[str]
    KmsKeyARN: NotRequired[str]
    RoleARN: NotRequired[str]
    SnowballCapacityPreference: NotRequired[SnowballCapacityType]
    ShippingOption: NotRequired[ShippingOptionType]
    Notification: NotRequired[NotificationTypeDef]
    ClusterId: NotRequired[str]
    SnowballType: NotRequired[SnowballTypeType]
    ForwardingAddressId: NotRequired[str]
    TaxDocuments: NotRequired[TaxDocumentsTypeDef]
    DeviceConfiguration: NotRequired[DeviceConfigurationTypeDef]
    RemoteManagement: NotRequired[RemoteManagementType]
    LongTermPricingId: NotRequired[str]
    ImpactLevel: NotRequired[ImpactLevelType]
    PickupDetails: NotRequired[PickupDetailsTypeDef]

class UpdateClusterRequestRequestTypeDef(TypedDict):
    ClusterId: str
    RoleARN: NotRequired[str]
    Description: NotRequired[str]
    Resources: NotRequired[JobResourceTypeDef]
    OnDeviceServiceConfiguration: NotRequired[OnDeviceServiceConfigurationTypeDef]
    AddressId: NotRequired[str]
    ShippingOption: NotRequired[ShippingOptionType]
    Notification: NotRequired[NotificationTypeDef]
    ForwardingAddressId: NotRequired[str]

class UpdateJobRequestRequestTypeDef(TypedDict):
    JobId: str
    RoleARN: NotRequired[str]
    Notification: NotRequired[NotificationTypeDef]
    Resources: NotRequired[JobResourceTypeDef]
    OnDeviceServiceConfiguration: NotRequired[OnDeviceServiceConfigurationTypeDef]
    AddressId: NotRequired[str]
    ShippingOption: NotRequired[ShippingOptionType]
    Description: NotRequired[str]
    SnowballCapacityPreference: NotRequired[SnowballCapacityType]
    ForwardingAddressId: NotRequired[str]
    PickupDetails: NotRequired[PickupDetailsTypeDef]

class DescribeJobResultTypeDef(TypedDict):
    JobMetadata: JobMetadataTypeDef
    SubJobMetadata: List[JobMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
