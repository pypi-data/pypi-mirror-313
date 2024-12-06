"""
Type annotations for mediaconnect service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/type_defs/)

Usage::

    ```python
    from mypy_boto3_mediaconnect.type_defs import VpcInterfaceAttachmentTypeDef

    data: VpcInterfaceAttachmentTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AlgorithmType,
    BridgePlacementType,
    BridgeStateType,
    ColorimetryType,
    ConnectionStatusType,
    DesiredStateType,
    EncoderProfileType,
    EncodingNameType,
    EntitlementStatusType,
    FailoverModeType,
    GatewayStateType,
    InstanceStateType,
    KeyTypeType,
    MaintenanceDayType,
    MediaStreamTypeType,
    NetworkInterfaceTypeType,
    OutputStatusType,
    ProtocolType,
    RangeType,
    ReservationStateType,
    ScanModeType,
    SourceTypeType,
    StateType,
    StatusType,
    TcsType,
    ThumbnailStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AddBridgeFlowSourceRequestTypeDef",
    "AddBridgeNetworkOutputRequestTypeDef",
    "AddBridgeNetworkSourceRequestTypeDef",
    "AddBridgeOutputRequestTypeDef",
    "AddBridgeOutputsRequestRequestTypeDef",
    "AddBridgeOutputsResponseTypeDef",
    "AddBridgeSourceRequestTypeDef",
    "AddBridgeSourcesRequestRequestTypeDef",
    "AddBridgeSourcesResponseTypeDef",
    "AddEgressGatewayBridgeRequestTypeDef",
    "AddFlowMediaStreamsRequestRequestTypeDef",
    "AddFlowMediaStreamsResponseTypeDef",
    "AddFlowOutputsRequestRequestTypeDef",
    "AddFlowOutputsResponseTypeDef",
    "AddFlowSourcesRequestRequestTypeDef",
    "AddFlowSourcesResponseTypeDef",
    "AddFlowVpcInterfacesRequestRequestTypeDef",
    "AddFlowVpcInterfacesResponseTypeDef",
    "AddIngressGatewayBridgeRequestTypeDef",
    "AddMaintenanceTypeDef",
    "AddMediaStreamRequestTypeDef",
    "AddOutputRequestTypeDef",
    "BridgeFlowOutputTypeDef",
    "BridgeFlowSourceTypeDef",
    "BridgeNetworkOutputTypeDef",
    "BridgeNetworkSourceTypeDef",
    "BridgeOutputTypeDef",
    "BridgeSourceTypeDef",
    "BridgeTypeDef",
    "CreateBridgeRequestRequestTypeDef",
    "CreateBridgeResponseTypeDef",
    "CreateFlowRequestRequestTypeDef",
    "CreateFlowResponseTypeDef",
    "CreateGatewayRequestRequestTypeDef",
    "CreateGatewayResponseTypeDef",
    "DeleteBridgeRequestRequestTypeDef",
    "DeleteBridgeResponseTypeDef",
    "DeleteFlowRequestRequestTypeDef",
    "DeleteFlowResponseTypeDef",
    "DeleteGatewayRequestRequestTypeDef",
    "DeleteGatewayResponseTypeDef",
    "DeregisterGatewayInstanceRequestRequestTypeDef",
    "DeregisterGatewayInstanceResponseTypeDef",
    "DescribeBridgeRequestRequestTypeDef",
    "DescribeBridgeResponseTypeDef",
    "DescribeFlowRequestFlowActiveWaitTypeDef",
    "DescribeFlowRequestFlowDeletedWaitTypeDef",
    "DescribeFlowRequestFlowStandbyWaitTypeDef",
    "DescribeFlowRequestRequestTypeDef",
    "DescribeFlowResponseTypeDef",
    "DescribeFlowSourceMetadataRequestRequestTypeDef",
    "DescribeFlowSourceMetadataResponseTypeDef",
    "DescribeFlowSourceThumbnailRequestRequestTypeDef",
    "DescribeFlowSourceThumbnailResponseTypeDef",
    "DescribeGatewayInstanceRequestRequestTypeDef",
    "DescribeGatewayInstanceResponseTypeDef",
    "DescribeGatewayRequestRequestTypeDef",
    "DescribeGatewayResponseTypeDef",
    "DescribeOfferingRequestRequestTypeDef",
    "DescribeOfferingResponseTypeDef",
    "DescribeReservationRequestRequestTypeDef",
    "DescribeReservationResponseTypeDef",
    "DestinationConfigurationRequestTypeDef",
    "DestinationConfigurationTypeDef",
    "EgressGatewayBridgeTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncodingParametersRequestTypeDef",
    "EncodingParametersTypeDef",
    "EncryptionTypeDef",
    "EntitlementTypeDef",
    "FailoverConfigTypeDef",
    "FlowTypeDef",
    "FmtpRequestTypeDef",
    "FmtpTypeDef",
    "FrameResolutionTypeDef",
    "GatewayBridgeSourceTypeDef",
    "GatewayInstanceTypeDef",
    "GatewayNetworkTypeDef",
    "GatewayTypeDef",
    "GrantEntitlementRequestTypeDef",
    "GrantFlowEntitlementsRequestRequestTypeDef",
    "GrantFlowEntitlementsResponseTypeDef",
    "IngressGatewayBridgeTypeDef",
    "InputConfigurationRequestTypeDef",
    "InputConfigurationTypeDef",
    "InterfaceRequestTypeDef",
    "InterfaceTypeDef",
    "ListBridgesRequestListBridgesPaginateTypeDef",
    "ListBridgesRequestRequestTypeDef",
    "ListBridgesResponseTypeDef",
    "ListEntitlementsRequestListEntitlementsPaginateTypeDef",
    "ListEntitlementsRequestRequestTypeDef",
    "ListEntitlementsResponseTypeDef",
    "ListFlowsRequestListFlowsPaginateTypeDef",
    "ListFlowsRequestRequestTypeDef",
    "ListFlowsResponseTypeDef",
    "ListGatewayInstancesRequestListGatewayInstancesPaginateTypeDef",
    "ListGatewayInstancesRequestRequestTypeDef",
    "ListGatewayInstancesResponseTypeDef",
    "ListGatewaysRequestListGatewaysPaginateTypeDef",
    "ListGatewaysRequestRequestTypeDef",
    "ListGatewaysResponseTypeDef",
    "ListOfferingsRequestListOfferingsPaginateTypeDef",
    "ListOfferingsRequestRequestTypeDef",
    "ListOfferingsResponseTypeDef",
    "ListReservationsRequestListReservationsPaginateTypeDef",
    "ListReservationsRequestRequestTypeDef",
    "ListReservationsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListedBridgeTypeDef",
    "ListedEntitlementTypeDef",
    "ListedFlowTypeDef",
    "ListedGatewayInstanceTypeDef",
    "ListedGatewayTypeDef",
    "MaintenanceTypeDef",
    "MediaStreamAttributesRequestTypeDef",
    "MediaStreamAttributesTypeDef",
    "MediaStreamOutputConfigurationRequestTypeDef",
    "MediaStreamOutputConfigurationTypeDef",
    "MediaStreamSourceConfigurationRequestTypeDef",
    "MediaStreamSourceConfigurationTypeDef",
    "MediaStreamTypeDef",
    "MessageDetailTypeDef",
    "MessagesTypeDef",
    "MonitoringConfigTypeDef",
    "OfferingTypeDef",
    "OutputTypeDef",
    "PaginatorConfigTypeDef",
    "PurchaseOfferingRequestRequestTypeDef",
    "PurchaseOfferingResponseTypeDef",
    "RemoveBridgeOutputRequestRequestTypeDef",
    "RemoveBridgeOutputResponseTypeDef",
    "RemoveBridgeSourceRequestRequestTypeDef",
    "RemoveBridgeSourceResponseTypeDef",
    "RemoveFlowMediaStreamRequestRequestTypeDef",
    "RemoveFlowMediaStreamResponseTypeDef",
    "RemoveFlowOutputRequestRequestTypeDef",
    "RemoveFlowOutputResponseTypeDef",
    "RemoveFlowSourceRequestRequestTypeDef",
    "RemoveFlowSourceResponseTypeDef",
    "RemoveFlowVpcInterfaceRequestRequestTypeDef",
    "RemoveFlowVpcInterfaceResponseTypeDef",
    "ReservationTypeDef",
    "ResourceSpecificationTypeDef",
    "ResponseMetadataTypeDef",
    "RevokeFlowEntitlementRequestRequestTypeDef",
    "RevokeFlowEntitlementResponseTypeDef",
    "SetGatewayBridgeSourceRequestTypeDef",
    "SetSourceRequestTypeDef",
    "SourcePriorityTypeDef",
    "SourceTypeDef",
    "StartFlowRequestRequestTypeDef",
    "StartFlowResponseTypeDef",
    "StopFlowRequestRequestTypeDef",
    "StopFlowResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ThumbnailDetailsTypeDef",
    "TransportMediaInfoTypeDef",
    "TransportStreamProgramTypeDef",
    "TransportStreamTypeDef",
    "TransportTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateBridgeFlowSourceRequestTypeDef",
    "UpdateBridgeNetworkOutputRequestTypeDef",
    "UpdateBridgeNetworkSourceRequestTypeDef",
    "UpdateBridgeOutputRequestRequestTypeDef",
    "UpdateBridgeOutputResponseTypeDef",
    "UpdateBridgeRequestRequestTypeDef",
    "UpdateBridgeResponseTypeDef",
    "UpdateBridgeSourceRequestRequestTypeDef",
    "UpdateBridgeSourceResponseTypeDef",
    "UpdateBridgeStateRequestRequestTypeDef",
    "UpdateBridgeStateResponseTypeDef",
    "UpdateEgressGatewayBridgeRequestTypeDef",
    "UpdateEncryptionTypeDef",
    "UpdateFailoverConfigTypeDef",
    "UpdateFlowEntitlementRequestRequestTypeDef",
    "UpdateFlowEntitlementResponseTypeDef",
    "UpdateFlowMediaStreamRequestRequestTypeDef",
    "UpdateFlowMediaStreamResponseTypeDef",
    "UpdateFlowOutputRequestRequestTypeDef",
    "UpdateFlowOutputResponseTypeDef",
    "UpdateFlowRequestRequestTypeDef",
    "UpdateFlowResponseTypeDef",
    "UpdateFlowSourceRequestRequestTypeDef",
    "UpdateFlowSourceResponseTypeDef",
    "UpdateGatewayBridgeSourceRequestTypeDef",
    "UpdateGatewayInstanceRequestRequestTypeDef",
    "UpdateGatewayInstanceResponseTypeDef",
    "UpdateIngressGatewayBridgeRequestTypeDef",
    "UpdateMaintenanceTypeDef",
    "VpcInterfaceAttachmentTypeDef",
    "VpcInterfaceRequestTypeDef",
    "VpcInterfaceTypeDef",
    "WaiterConfigTypeDef",
)


class VpcInterfaceAttachmentTypeDef(TypedDict):
    VpcInterfaceName: NotRequired[str]


AddBridgeNetworkOutputRequestTypeDef = TypedDict(
    "AddBridgeNetworkOutputRequestTypeDef",
    {
        "IpAddress": str,
        "Name": str,
        "NetworkName": str,
        "Port": int,
        "Protocol": ProtocolType,
        "Ttl": int,
    },
)
AddBridgeNetworkSourceRequestTypeDef = TypedDict(
    "AddBridgeNetworkSourceRequestTypeDef",
    {
        "MulticastIp": str,
        "Name": str,
        "NetworkName": str,
        "Port": int,
        "Protocol": ProtocolType,
    },
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AddEgressGatewayBridgeRequestTypeDef(TypedDict):
    MaxBitrate: int


class VpcInterfaceRequestTypeDef(TypedDict):
    Name: str
    RoleArn: str
    SecurityGroupIds: Sequence[str]
    SubnetId: str
    NetworkInterfaceType: NotRequired[NetworkInterfaceTypeType]


class VpcInterfaceTypeDef(TypedDict):
    Name: str
    NetworkInterfaceIds: List[str]
    NetworkInterfaceType: NetworkInterfaceTypeType
    RoleArn: str
    SecurityGroupIds: List[str]
    SubnetId: str


class AddIngressGatewayBridgeRequestTypeDef(TypedDict):
    MaxBitrate: int
    MaxOutputs: int


class AddMaintenanceTypeDef(TypedDict):
    MaintenanceDay: MaintenanceDayType
    MaintenanceStartHour: str


class EncryptionTypeDef(TypedDict):
    RoleArn: str
    Algorithm: NotRequired[AlgorithmType]
    ConstantInitializationVector: NotRequired[str]
    DeviceId: NotRequired[str]
    KeyType: NotRequired[KeyTypeType]
    Region: NotRequired[str]
    ResourceId: NotRequired[str]
    SecretArn: NotRequired[str]
    Url: NotRequired[str]


class BridgeFlowOutputTypeDef(TypedDict):
    FlowArn: str
    FlowSourceArn: str
    Name: str


BridgeNetworkOutputTypeDef = TypedDict(
    "BridgeNetworkOutputTypeDef",
    {
        "IpAddress": str,
        "Name": str,
        "NetworkName": str,
        "Port": int,
        "Protocol": ProtocolType,
        "Ttl": int,
    },
)
BridgeNetworkSourceTypeDef = TypedDict(
    "BridgeNetworkSourceTypeDef",
    {
        "MulticastIp": str,
        "Name": str,
        "NetworkName": str,
        "Port": int,
        "Protocol": ProtocolType,
    },
)


class EgressGatewayBridgeTypeDef(TypedDict):
    MaxBitrate: int
    InstanceId: NotRequired[str]


class IngressGatewayBridgeTypeDef(TypedDict):
    MaxBitrate: int
    MaxOutputs: int
    InstanceId: NotRequired[str]


class MessageDetailTypeDef(TypedDict):
    Code: str
    Message: str
    ResourceName: NotRequired[str]


class MonitoringConfigTypeDef(TypedDict):
    ThumbnailState: NotRequired[ThumbnailStateType]


class GatewayNetworkTypeDef(TypedDict):
    CidrBlock: str
    Name: str


class DeleteBridgeRequestRequestTypeDef(TypedDict):
    BridgeArn: str


class DeleteFlowRequestRequestTypeDef(TypedDict):
    FlowArn: str


class DeleteGatewayRequestRequestTypeDef(TypedDict):
    GatewayArn: str


class DeregisterGatewayInstanceRequestRequestTypeDef(TypedDict):
    GatewayInstanceArn: str
    Force: NotRequired[bool]


class DescribeBridgeRequestRequestTypeDef(TypedDict):
    BridgeArn: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class DescribeFlowRequestRequestTypeDef(TypedDict):
    FlowArn: str


class MessagesTypeDef(TypedDict):
    Errors: List[str]


class DescribeFlowSourceMetadataRequestRequestTypeDef(TypedDict):
    FlowArn: str


class DescribeFlowSourceThumbnailRequestRequestTypeDef(TypedDict):
    FlowArn: str


class DescribeGatewayInstanceRequestRequestTypeDef(TypedDict):
    GatewayInstanceArn: str


class DescribeGatewayRequestRequestTypeDef(TypedDict):
    GatewayArn: str


class DescribeOfferingRequestRequestTypeDef(TypedDict):
    OfferingArn: str


class DescribeReservationRequestRequestTypeDef(TypedDict):
    ReservationArn: str


class InterfaceRequestTypeDef(TypedDict):
    Name: str


class InterfaceTypeDef(TypedDict):
    Name: str


class EncodingParametersRequestTypeDef(TypedDict):
    CompressionFactor: float
    EncoderProfile: EncoderProfileType


class EncodingParametersTypeDef(TypedDict):
    CompressionFactor: float
    EncoderProfile: EncoderProfileType


class SourcePriorityTypeDef(TypedDict):
    PrimarySource: NotRequired[str]


class MaintenanceTypeDef(TypedDict):
    MaintenanceDay: NotRequired[MaintenanceDayType]
    MaintenanceDeadline: NotRequired[str]
    MaintenanceScheduledDate: NotRequired[str]
    MaintenanceStartHour: NotRequired[str]


class FmtpRequestTypeDef(TypedDict):
    ChannelOrder: NotRequired[str]
    Colorimetry: NotRequired[ColorimetryType]
    ExactFramerate: NotRequired[str]
    Par: NotRequired[str]
    Range: NotRequired[RangeType]
    ScanMode: NotRequired[ScanModeType]
    Tcs: NotRequired[TcsType]


class FmtpTypeDef(TypedDict):
    ChannelOrder: NotRequired[str]
    Colorimetry: NotRequired[ColorimetryType]
    ExactFramerate: NotRequired[str]
    Par: NotRequired[str]
    Range: NotRequired[RangeType]
    ScanMode: NotRequired[ScanModeType]
    Tcs: NotRequired[TcsType]


class FrameResolutionTypeDef(TypedDict):
    FrameHeight: int
    FrameWidth: int


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListBridgesRequestRequestTypeDef(TypedDict):
    FilterArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListedBridgeTypeDef(TypedDict):
    BridgeArn: str
    BridgeState: BridgeStateType
    BridgeType: str
    Name: str
    PlacementArn: str


class ListEntitlementsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListedEntitlementTypeDef(TypedDict):
    EntitlementArn: str
    EntitlementName: str
    DataTransferSubscriberFeePercent: NotRequired[int]


class ListFlowsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListGatewayInstancesRequestRequestTypeDef(TypedDict):
    FilterArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListedGatewayInstanceTypeDef(TypedDict):
    GatewayArn: str
    GatewayInstanceArn: str
    InstanceId: str
    InstanceState: NotRequired[InstanceStateType]


class ListGatewaysRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListedGatewayTypeDef(TypedDict):
    GatewayArn: str
    GatewayState: GatewayStateType
    Name: str


class ListOfferingsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListReservationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class ResourceSpecificationTypeDef(TypedDict):
    ResourceType: Literal["Mbps_Outbound_Bandwidth"]
    ReservedBitrate: NotRequired[int]


TransportTypeDef = TypedDict(
    "TransportTypeDef",
    {
        "Protocol": ProtocolType,
        "CidrAllowList": NotRequired[List[str]],
        "MaxBitrate": NotRequired[int],
        "MaxLatency": NotRequired[int],
        "MaxSyncBuffer": NotRequired[int],
        "MinLatency": NotRequired[int],
        "RemoteId": NotRequired[str],
        "SenderControlPort": NotRequired[int],
        "SenderIpAddress": NotRequired[str],
        "SmoothingLatency": NotRequired[int],
        "SourceListenerAddress": NotRequired[str],
        "SourceListenerPort": NotRequired[int],
        "StreamId": NotRequired[str],
    },
)


class PurchaseOfferingRequestRequestTypeDef(TypedDict):
    OfferingArn: str
    ReservationName: str
    Start: str


class RemoveBridgeOutputRequestRequestTypeDef(TypedDict):
    BridgeArn: str
    OutputName: str


class RemoveBridgeSourceRequestRequestTypeDef(TypedDict):
    BridgeArn: str
    SourceName: str


class RemoveFlowMediaStreamRequestRequestTypeDef(TypedDict):
    FlowArn: str
    MediaStreamName: str


class RemoveFlowOutputRequestRequestTypeDef(TypedDict):
    FlowArn: str
    OutputArn: str


class RemoveFlowSourceRequestRequestTypeDef(TypedDict):
    FlowArn: str
    SourceArn: str


class RemoveFlowVpcInterfaceRequestRequestTypeDef(TypedDict):
    FlowArn: str
    VpcInterfaceName: str


class RevokeFlowEntitlementRequestRequestTypeDef(TypedDict):
    EntitlementArn: str
    FlowArn: str


class StartFlowRequestRequestTypeDef(TypedDict):
    FlowArn: str


class StopFlowRequestRequestTypeDef(TypedDict):
    FlowArn: str


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


UpdateBridgeNetworkOutputRequestTypeDef = TypedDict(
    "UpdateBridgeNetworkOutputRequestTypeDef",
    {
        "IpAddress": NotRequired[str],
        "NetworkName": NotRequired[str],
        "Port": NotRequired[int],
        "Protocol": NotRequired[ProtocolType],
        "Ttl": NotRequired[int],
    },
)
UpdateBridgeNetworkSourceRequestTypeDef = TypedDict(
    "UpdateBridgeNetworkSourceRequestTypeDef",
    {
        "MulticastIp": NotRequired[str],
        "NetworkName": NotRequired[str],
        "Port": NotRequired[int],
        "Protocol": NotRequired[ProtocolType],
    },
)


class UpdateEgressGatewayBridgeRequestTypeDef(TypedDict):
    MaxBitrate: NotRequired[int]


class UpdateIngressGatewayBridgeRequestTypeDef(TypedDict):
    MaxBitrate: NotRequired[int]
    MaxOutputs: NotRequired[int]


class UpdateBridgeStateRequestRequestTypeDef(TypedDict):
    BridgeArn: str
    DesiredState: DesiredStateType


class UpdateEncryptionTypeDef(TypedDict):
    Algorithm: NotRequired[AlgorithmType]
    ConstantInitializationVector: NotRequired[str]
    DeviceId: NotRequired[str]
    KeyType: NotRequired[KeyTypeType]
    Region: NotRequired[str]
    ResourceId: NotRequired[str]
    RoleArn: NotRequired[str]
    SecretArn: NotRequired[str]
    Url: NotRequired[str]


class UpdateMaintenanceTypeDef(TypedDict):
    MaintenanceDay: NotRequired[MaintenanceDayType]
    MaintenanceScheduledDate: NotRequired[str]
    MaintenanceStartHour: NotRequired[str]


class UpdateGatewayInstanceRequestRequestTypeDef(TypedDict):
    GatewayInstanceArn: str
    BridgePlacement: NotRequired[BridgePlacementType]


class AddBridgeFlowSourceRequestTypeDef(TypedDict):
    FlowArn: str
    Name: str
    FlowVpcInterfaceAttachment: NotRequired[VpcInterfaceAttachmentTypeDef]


class BridgeFlowSourceTypeDef(TypedDict):
    FlowArn: str
    Name: str
    FlowVpcInterfaceAttachment: NotRequired[VpcInterfaceAttachmentTypeDef]
    OutputArn: NotRequired[str]


class GatewayBridgeSourceTypeDef(TypedDict):
    BridgeArn: str
    VpcInterfaceAttachment: NotRequired[VpcInterfaceAttachmentTypeDef]


class SetGatewayBridgeSourceRequestTypeDef(TypedDict):
    BridgeArn: str
    VpcInterfaceAttachment: NotRequired[VpcInterfaceAttachmentTypeDef]


class UpdateBridgeFlowSourceRequestTypeDef(TypedDict):
    FlowArn: NotRequired[str]
    FlowVpcInterfaceAttachment: NotRequired[VpcInterfaceAttachmentTypeDef]


class UpdateGatewayBridgeSourceRequestTypeDef(TypedDict):
    BridgeArn: NotRequired[str]
    VpcInterfaceAttachment: NotRequired[VpcInterfaceAttachmentTypeDef]


class AddBridgeOutputRequestTypeDef(TypedDict):
    NetworkOutput: NotRequired[AddBridgeNetworkOutputRequestTypeDef]


class DeleteBridgeResponseTypeDef(TypedDict):
    BridgeArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteFlowResponseTypeDef(TypedDict):
    FlowArn: str
    Status: StatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteGatewayResponseTypeDef(TypedDict):
    GatewayArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeregisterGatewayInstanceResponseTypeDef(TypedDict):
    GatewayInstanceArn: str
    InstanceState: InstanceStateType
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class RemoveBridgeOutputResponseTypeDef(TypedDict):
    BridgeArn: str
    OutputName: str
    ResponseMetadata: ResponseMetadataTypeDef


class RemoveBridgeSourceResponseTypeDef(TypedDict):
    BridgeArn: str
    SourceName: str
    ResponseMetadata: ResponseMetadataTypeDef


class RemoveFlowMediaStreamResponseTypeDef(TypedDict):
    FlowArn: str
    MediaStreamName: str
    ResponseMetadata: ResponseMetadataTypeDef


class RemoveFlowOutputResponseTypeDef(TypedDict):
    FlowArn: str
    OutputArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class RemoveFlowSourceResponseTypeDef(TypedDict):
    FlowArn: str
    SourceArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class RemoveFlowVpcInterfaceResponseTypeDef(TypedDict):
    FlowArn: str
    NonDeletedNetworkInterfaceIds: List[str]
    VpcInterfaceName: str
    ResponseMetadata: ResponseMetadataTypeDef


class RevokeFlowEntitlementResponseTypeDef(TypedDict):
    EntitlementArn: str
    FlowArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartFlowResponseTypeDef(TypedDict):
    FlowArn: str
    Status: StatusType
    ResponseMetadata: ResponseMetadataTypeDef


class StopFlowResponseTypeDef(TypedDict):
    FlowArn: str
    Status: StatusType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBridgeStateResponseTypeDef(TypedDict):
    BridgeArn: str
    DesiredState: DesiredStateType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateGatewayInstanceResponseTypeDef(TypedDict):
    BridgePlacement: BridgePlacementType
    GatewayInstanceArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class AddFlowVpcInterfacesRequestRequestTypeDef(TypedDict):
    FlowArn: str
    VpcInterfaces: Sequence[VpcInterfaceRequestTypeDef]


class AddFlowVpcInterfacesResponseTypeDef(TypedDict):
    FlowArn: str
    VpcInterfaces: List[VpcInterfaceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class EntitlementTypeDef(TypedDict):
    EntitlementArn: str
    Name: str
    Subscribers: List[str]
    DataTransferSubscriberFeePercent: NotRequired[int]
    Description: NotRequired[str]
    Encryption: NotRequired[EncryptionTypeDef]
    EntitlementStatus: NotRequired[EntitlementStatusType]


class GrantEntitlementRequestTypeDef(TypedDict):
    Subscribers: Sequence[str]
    DataTransferSubscriberFeePercent: NotRequired[int]
    Description: NotRequired[str]
    Encryption: NotRequired[EncryptionTypeDef]
    EntitlementStatus: NotRequired[EntitlementStatusType]
    Name: NotRequired[str]


class BridgeOutputTypeDef(TypedDict):
    FlowOutput: NotRequired[BridgeFlowOutputTypeDef]
    NetworkOutput: NotRequired[BridgeNetworkOutputTypeDef]


class GatewayInstanceTypeDef(TypedDict):
    BridgePlacement: BridgePlacementType
    ConnectionStatus: ConnectionStatusType
    GatewayArn: str
    GatewayInstanceArn: str
    InstanceId: str
    InstanceState: InstanceStateType
    RunningBridgeCount: int
    InstanceMessages: NotRequired[List[MessageDetailTypeDef]]


class ThumbnailDetailsTypeDef(TypedDict):
    FlowArn: str
    ThumbnailMessages: List[MessageDetailTypeDef]
    Thumbnail: NotRequired[str]
    Timecode: NotRequired[str]
    Timestamp: NotRequired[datetime]


class CreateGatewayRequestRequestTypeDef(TypedDict):
    EgressCidrBlocks: Sequence[str]
    Name: str
    Networks: Sequence[GatewayNetworkTypeDef]


class GatewayTypeDef(TypedDict):
    EgressCidrBlocks: List[str]
    GatewayArn: str
    Name: str
    Networks: List[GatewayNetworkTypeDef]
    GatewayMessages: NotRequired[List[MessageDetailTypeDef]]
    GatewayState: NotRequired[GatewayStateType]


class DescribeFlowRequestFlowActiveWaitTypeDef(TypedDict):
    FlowArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeFlowRequestFlowDeletedWaitTypeDef(TypedDict):
    FlowArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeFlowRequestFlowStandbyWaitTypeDef(TypedDict):
    FlowArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DestinationConfigurationRequestTypeDef(TypedDict):
    DestinationIp: str
    DestinationPort: int
    Interface: InterfaceRequestTypeDef


class InputConfigurationRequestTypeDef(TypedDict):
    InputPort: int
    Interface: InterfaceRequestTypeDef


class DestinationConfigurationTypeDef(TypedDict):
    DestinationIp: str
    DestinationPort: int
    Interface: InterfaceTypeDef
    OutboundIp: str


class InputConfigurationTypeDef(TypedDict):
    InputIp: str
    InputPort: int
    Interface: InterfaceTypeDef


class FailoverConfigTypeDef(TypedDict):
    FailoverMode: NotRequired[FailoverModeType]
    RecoveryWindow: NotRequired[int]
    SourcePriority: NotRequired[SourcePriorityTypeDef]
    State: NotRequired[StateType]


class UpdateFailoverConfigTypeDef(TypedDict):
    FailoverMode: NotRequired[FailoverModeType]
    RecoveryWindow: NotRequired[int]
    SourcePriority: NotRequired[SourcePriorityTypeDef]
    State: NotRequired[StateType]


class ListedFlowTypeDef(TypedDict):
    AvailabilityZone: str
    Description: str
    FlowArn: str
    Name: str
    SourceType: SourceTypeType
    Status: StatusType
    Maintenance: NotRequired[MaintenanceTypeDef]


class MediaStreamAttributesRequestTypeDef(TypedDict):
    Fmtp: NotRequired[FmtpRequestTypeDef]
    Lang: NotRequired[str]


class MediaStreamAttributesTypeDef(TypedDict):
    Fmtp: FmtpTypeDef
    Lang: NotRequired[str]


class TransportStreamTypeDef(TypedDict):
    Pid: int
    StreamType: str
    Channels: NotRequired[int]
    Codec: NotRequired[str]
    FrameRate: NotRequired[str]
    FrameResolution: NotRequired[FrameResolutionTypeDef]
    SampleRate: NotRequired[int]
    SampleSize: NotRequired[int]


class ListBridgesRequestListBridgesPaginateTypeDef(TypedDict):
    FilterArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEntitlementsRequestListEntitlementsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFlowsRequestListFlowsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGatewayInstancesRequestListGatewayInstancesPaginateTypeDef(TypedDict):
    FilterArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGatewaysRequestListGatewaysPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOfferingsRequestListOfferingsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListReservationsRequestListReservationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBridgesResponseTypeDef(TypedDict):
    Bridges: List[ListedBridgeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListEntitlementsResponseTypeDef(TypedDict):
    Entitlements: List[ListedEntitlementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListGatewayInstancesResponseTypeDef(TypedDict):
    Instances: List[ListedGatewayInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListGatewaysResponseTypeDef(TypedDict):
    Gateways: List[ListedGatewayTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class OfferingTypeDef(TypedDict):
    CurrencyCode: str
    Duration: int
    DurationUnits: Literal["MONTHS"]
    OfferingArn: str
    OfferingDescription: str
    PricePerUnit: str
    PriceUnits: Literal["HOURLY"]
    ResourceSpecification: ResourceSpecificationTypeDef


class ReservationTypeDef(TypedDict):
    CurrencyCode: str
    Duration: int
    DurationUnits: Literal["MONTHS"]
    End: str
    OfferingArn: str
    OfferingDescription: str
    PricePerUnit: str
    PriceUnits: Literal["HOURLY"]
    ReservationArn: str
    ReservationName: str
    ReservationState: ReservationStateType
    ResourceSpecification: ResourceSpecificationTypeDef
    Start: str


class UpdateBridgeOutputRequestRequestTypeDef(TypedDict):
    BridgeArn: str
    OutputName: str
    NetworkOutput: NotRequired[UpdateBridgeNetworkOutputRequestTypeDef]


class UpdateFlowEntitlementRequestRequestTypeDef(TypedDict):
    EntitlementArn: str
    FlowArn: str
    Description: NotRequired[str]
    Encryption: NotRequired[UpdateEncryptionTypeDef]
    EntitlementStatus: NotRequired[EntitlementStatusType]
    Subscribers: NotRequired[Sequence[str]]


class AddBridgeSourceRequestTypeDef(TypedDict):
    FlowSource: NotRequired[AddBridgeFlowSourceRequestTypeDef]
    NetworkSource: NotRequired[AddBridgeNetworkSourceRequestTypeDef]


class BridgeSourceTypeDef(TypedDict):
    FlowSource: NotRequired[BridgeFlowSourceTypeDef]
    NetworkSource: NotRequired[BridgeNetworkSourceTypeDef]


class UpdateBridgeSourceRequestRequestTypeDef(TypedDict):
    BridgeArn: str
    SourceName: str
    FlowSource: NotRequired[UpdateBridgeFlowSourceRequestTypeDef]
    NetworkSource: NotRequired[UpdateBridgeNetworkSourceRequestTypeDef]


class AddBridgeOutputsRequestRequestTypeDef(TypedDict):
    BridgeArn: str
    Outputs: Sequence[AddBridgeOutputRequestTypeDef]


class GrantFlowEntitlementsResponseTypeDef(TypedDict):
    Entitlements: List[EntitlementTypeDef]
    FlowArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFlowEntitlementResponseTypeDef(TypedDict):
    Entitlement: EntitlementTypeDef
    FlowArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class GrantFlowEntitlementsRequestRequestTypeDef(TypedDict):
    Entitlements: Sequence[GrantEntitlementRequestTypeDef]
    FlowArn: str


class AddBridgeOutputsResponseTypeDef(TypedDict):
    BridgeArn: str
    Outputs: List[BridgeOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBridgeOutputResponseTypeDef(TypedDict):
    BridgeArn: str
    Output: BridgeOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeGatewayInstanceResponseTypeDef(TypedDict):
    GatewayInstance: GatewayInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFlowSourceThumbnailResponseTypeDef(TypedDict):
    ThumbnailDetails: ThumbnailDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateGatewayResponseTypeDef(TypedDict):
    Gateway: GatewayTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeGatewayResponseTypeDef(TypedDict):
    Gateway: GatewayTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class MediaStreamOutputConfigurationRequestTypeDef(TypedDict):
    EncodingName: EncodingNameType
    MediaStreamName: str
    DestinationConfigurations: NotRequired[Sequence[DestinationConfigurationRequestTypeDef]]
    EncodingParameters: NotRequired[EncodingParametersRequestTypeDef]


class MediaStreamSourceConfigurationRequestTypeDef(TypedDict):
    EncodingName: EncodingNameType
    MediaStreamName: str
    InputConfigurations: NotRequired[Sequence[InputConfigurationRequestTypeDef]]


class MediaStreamOutputConfigurationTypeDef(TypedDict):
    EncodingName: EncodingNameType
    MediaStreamName: str
    DestinationConfigurations: NotRequired[List[DestinationConfigurationTypeDef]]
    EncodingParameters: NotRequired[EncodingParametersTypeDef]


class MediaStreamSourceConfigurationTypeDef(TypedDict):
    EncodingName: EncodingNameType
    MediaStreamName: str
    InputConfigurations: NotRequired[List[InputConfigurationTypeDef]]


class UpdateBridgeRequestRequestTypeDef(TypedDict):
    BridgeArn: str
    EgressGatewayBridge: NotRequired[UpdateEgressGatewayBridgeRequestTypeDef]
    IngressGatewayBridge: NotRequired[UpdateIngressGatewayBridgeRequestTypeDef]
    SourceFailoverConfig: NotRequired[UpdateFailoverConfigTypeDef]


class UpdateFlowRequestRequestTypeDef(TypedDict):
    FlowArn: str
    SourceFailoverConfig: NotRequired[UpdateFailoverConfigTypeDef]
    Maintenance: NotRequired[UpdateMaintenanceTypeDef]
    SourceMonitoringConfig: NotRequired[MonitoringConfigTypeDef]


class ListFlowsResponseTypeDef(TypedDict):
    Flows: List[ListedFlowTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AddMediaStreamRequestTypeDef(TypedDict):
    MediaStreamId: int
    MediaStreamName: str
    MediaStreamType: MediaStreamTypeType
    Attributes: NotRequired[MediaStreamAttributesRequestTypeDef]
    ClockRate: NotRequired[int]
    Description: NotRequired[str]
    VideoFormat: NotRequired[str]


class UpdateFlowMediaStreamRequestRequestTypeDef(TypedDict):
    FlowArn: str
    MediaStreamName: str
    Attributes: NotRequired[MediaStreamAttributesRequestTypeDef]
    ClockRate: NotRequired[int]
    Description: NotRequired[str]
    MediaStreamType: NotRequired[MediaStreamTypeType]
    VideoFormat: NotRequired[str]


class MediaStreamTypeDef(TypedDict):
    Fmt: int
    MediaStreamId: int
    MediaStreamName: str
    MediaStreamType: MediaStreamTypeType
    Attributes: NotRequired[MediaStreamAttributesTypeDef]
    ClockRate: NotRequired[int]
    Description: NotRequired[str]
    VideoFormat: NotRequired[str]


class TransportStreamProgramTypeDef(TypedDict):
    PcrPid: int
    ProgramNumber: int
    ProgramPid: int
    Streams: List[TransportStreamTypeDef]
    ProgramName: NotRequired[str]


class DescribeOfferingResponseTypeDef(TypedDict):
    Offering: OfferingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListOfferingsResponseTypeDef(TypedDict):
    Offerings: List[OfferingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeReservationResponseTypeDef(TypedDict):
    Reservation: ReservationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListReservationsResponseTypeDef(TypedDict):
    Reservations: List[ReservationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PurchaseOfferingResponseTypeDef(TypedDict):
    Reservation: ReservationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AddBridgeSourcesRequestRequestTypeDef(TypedDict):
    BridgeArn: str
    Sources: Sequence[AddBridgeSourceRequestTypeDef]


class CreateBridgeRequestRequestTypeDef(TypedDict):
    Name: str
    PlacementArn: str
    Sources: Sequence[AddBridgeSourceRequestTypeDef]
    EgressGatewayBridge: NotRequired[AddEgressGatewayBridgeRequestTypeDef]
    IngressGatewayBridge: NotRequired[AddIngressGatewayBridgeRequestTypeDef]
    Outputs: NotRequired[Sequence[AddBridgeOutputRequestTypeDef]]
    SourceFailoverConfig: NotRequired[FailoverConfigTypeDef]


class AddBridgeSourcesResponseTypeDef(TypedDict):
    BridgeArn: str
    Sources: List[BridgeSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BridgeTypeDef(TypedDict):
    BridgeArn: str
    BridgeState: BridgeStateType
    Name: str
    PlacementArn: str
    BridgeMessages: NotRequired[List[MessageDetailTypeDef]]
    EgressGatewayBridge: NotRequired[EgressGatewayBridgeTypeDef]
    IngressGatewayBridge: NotRequired[IngressGatewayBridgeTypeDef]
    Outputs: NotRequired[List[BridgeOutputTypeDef]]
    SourceFailoverConfig: NotRequired[FailoverConfigTypeDef]
    Sources: NotRequired[List[BridgeSourceTypeDef]]


class UpdateBridgeSourceResponseTypeDef(TypedDict):
    BridgeArn: str
    Source: BridgeSourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


AddOutputRequestTypeDef = TypedDict(
    "AddOutputRequestTypeDef",
    {
        "Protocol": ProtocolType,
        "CidrAllowList": NotRequired[Sequence[str]],
        "Description": NotRequired[str],
        "Destination": NotRequired[str],
        "Encryption": NotRequired[EncryptionTypeDef],
        "MaxLatency": NotRequired[int],
        "MediaStreamOutputConfigurations": NotRequired[
            Sequence[MediaStreamOutputConfigurationRequestTypeDef]
        ],
        "MinLatency": NotRequired[int],
        "Name": NotRequired[str],
        "Port": NotRequired[int],
        "RemoteId": NotRequired[str],
        "SenderControlPort": NotRequired[int],
        "SmoothingLatency": NotRequired[int],
        "StreamId": NotRequired[str],
        "VpcInterfaceAttachment": NotRequired[VpcInterfaceAttachmentTypeDef],
        "OutputStatus": NotRequired[OutputStatusType],
    },
)
UpdateFlowOutputRequestRequestTypeDef = TypedDict(
    "UpdateFlowOutputRequestRequestTypeDef",
    {
        "FlowArn": str,
        "OutputArn": str,
        "CidrAllowList": NotRequired[Sequence[str]],
        "Description": NotRequired[str],
        "Destination": NotRequired[str],
        "Encryption": NotRequired[UpdateEncryptionTypeDef],
        "MaxLatency": NotRequired[int],
        "MediaStreamOutputConfigurations": NotRequired[
            Sequence[MediaStreamOutputConfigurationRequestTypeDef]
        ],
        "MinLatency": NotRequired[int],
        "Port": NotRequired[int],
        "Protocol": NotRequired[ProtocolType],
        "RemoteId": NotRequired[str],
        "SenderControlPort": NotRequired[int],
        "SenderIpAddress": NotRequired[str],
        "SmoothingLatency": NotRequired[int],
        "StreamId": NotRequired[str],
        "VpcInterfaceAttachment": NotRequired[VpcInterfaceAttachmentTypeDef],
        "OutputStatus": NotRequired[OutputStatusType],
    },
)
SetSourceRequestTypeDef = TypedDict(
    "SetSourceRequestTypeDef",
    {
        "Decryption": NotRequired[EncryptionTypeDef],
        "Description": NotRequired[str],
        "EntitlementArn": NotRequired[str],
        "IngestPort": NotRequired[int],
        "MaxBitrate": NotRequired[int],
        "MaxLatency": NotRequired[int],
        "MaxSyncBuffer": NotRequired[int],
        "MediaStreamSourceConfigurations": NotRequired[
            Sequence[MediaStreamSourceConfigurationRequestTypeDef]
        ],
        "MinLatency": NotRequired[int],
        "Name": NotRequired[str],
        "Protocol": NotRequired[ProtocolType],
        "SenderControlPort": NotRequired[int],
        "SenderIpAddress": NotRequired[str],
        "SourceListenerAddress": NotRequired[str],
        "SourceListenerPort": NotRequired[int],
        "StreamId": NotRequired[str],
        "VpcInterfaceName": NotRequired[str],
        "WhitelistCidr": NotRequired[str],
        "GatewayBridgeSource": NotRequired[SetGatewayBridgeSourceRequestTypeDef],
    },
)
UpdateFlowSourceRequestRequestTypeDef = TypedDict(
    "UpdateFlowSourceRequestRequestTypeDef",
    {
        "FlowArn": str,
        "SourceArn": str,
        "Decryption": NotRequired[UpdateEncryptionTypeDef],
        "Description": NotRequired[str],
        "EntitlementArn": NotRequired[str],
        "IngestPort": NotRequired[int],
        "MaxBitrate": NotRequired[int],
        "MaxLatency": NotRequired[int],
        "MaxSyncBuffer": NotRequired[int],
        "MediaStreamSourceConfigurations": NotRequired[
            Sequence[MediaStreamSourceConfigurationRequestTypeDef]
        ],
        "MinLatency": NotRequired[int],
        "Protocol": NotRequired[ProtocolType],
        "SenderControlPort": NotRequired[int],
        "SenderIpAddress": NotRequired[str],
        "SourceListenerAddress": NotRequired[str],
        "SourceListenerPort": NotRequired[int],
        "StreamId": NotRequired[str],
        "VpcInterfaceName": NotRequired[str],
        "WhitelistCidr": NotRequired[str],
        "GatewayBridgeSource": NotRequired[UpdateGatewayBridgeSourceRequestTypeDef],
    },
)


class OutputTypeDef(TypedDict):
    Name: str
    OutputArn: str
    DataTransferSubscriberFeePercent: NotRequired[int]
    Description: NotRequired[str]
    Destination: NotRequired[str]
    Encryption: NotRequired[EncryptionTypeDef]
    EntitlementArn: NotRequired[str]
    ListenerAddress: NotRequired[str]
    MediaLiveInputArn: NotRequired[str]
    MediaStreamOutputConfigurations: NotRequired[List[MediaStreamOutputConfigurationTypeDef]]
    Port: NotRequired[int]
    Transport: NotRequired[TransportTypeDef]
    VpcInterfaceAttachment: NotRequired[VpcInterfaceAttachmentTypeDef]
    BridgeArn: NotRequired[str]
    BridgePorts: NotRequired[List[int]]
    OutputStatus: NotRequired[OutputStatusType]


class SourceTypeDef(TypedDict):
    Name: str
    SourceArn: str
    DataTransferSubscriberFeePercent: NotRequired[int]
    Decryption: NotRequired[EncryptionTypeDef]
    Description: NotRequired[str]
    EntitlementArn: NotRequired[str]
    IngestIp: NotRequired[str]
    IngestPort: NotRequired[int]
    MediaStreamSourceConfigurations: NotRequired[List[MediaStreamSourceConfigurationTypeDef]]
    SenderControlPort: NotRequired[int]
    SenderIpAddress: NotRequired[str]
    Transport: NotRequired[TransportTypeDef]
    VpcInterfaceName: NotRequired[str]
    WhitelistCidr: NotRequired[str]
    GatewayBridgeSource: NotRequired[GatewayBridgeSourceTypeDef]


class AddFlowMediaStreamsRequestRequestTypeDef(TypedDict):
    FlowArn: str
    MediaStreams: Sequence[AddMediaStreamRequestTypeDef]


class AddFlowMediaStreamsResponseTypeDef(TypedDict):
    FlowArn: str
    MediaStreams: List[MediaStreamTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFlowMediaStreamResponseTypeDef(TypedDict):
    FlowArn: str
    MediaStream: MediaStreamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class TransportMediaInfoTypeDef(TypedDict):
    Programs: List[TransportStreamProgramTypeDef]


class CreateBridgeResponseTypeDef(TypedDict):
    Bridge: BridgeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeBridgeResponseTypeDef(TypedDict):
    Bridge: BridgeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBridgeResponseTypeDef(TypedDict):
    Bridge: BridgeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AddFlowOutputsRequestRequestTypeDef(TypedDict):
    FlowArn: str
    Outputs: Sequence[AddOutputRequestTypeDef]


class AddFlowSourcesRequestRequestTypeDef(TypedDict):
    FlowArn: str
    Sources: Sequence[SetSourceRequestTypeDef]


class CreateFlowRequestRequestTypeDef(TypedDict):
    Name: str
    AvailabilityZone: NotRequired[str]
    Entitlements: NotRequired[Sequence[GrantEntitlementRequestTypeDef]]
    MediaStreams: NotRequired[Sequence[AddMediaStreamRequestTypeDef]]
    Outputs: NotRequired[Sequence[AddOutputRequestTypeDef]]
    Source: NotRequired[SetSourceRequestTypeDef]
    SourceFailoverConfig: NotRequired[FailoverConfigTypeDef]
    Sources: NotRequired[Sequence[SetSourceRequestTypeDef]]
    VpcInterfaces: NotRequired[Sequence[VpcInterfaceRequestTypeDef]]
    Maintenance: NotRequired[AddMaintenanceTypeDef]
    SourceMonitoringConfig: NotRequired[MonitoringConfigTypeDef]


class AddFlowOutputsResponseTypeDef(TypedDict):
    FlowArn: str
    Outputs: List[OutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFlowOutputResponseTypeDef(TypedDict):
    FlowArn: str
    Output: OutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AddFlowSourcesResponseTypeDef(TypedDict):
    FlowArn: str
    Sources: List[SourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class FlowTypeDef(TypedDict):
    AvailabilityZone: str
    Entitlements: List[EntitlementTypeDef]
    FlowArn: str
    Name: str
    Outputs: List[OutputTypeDef]
    Source: SourceTypeDef
    Status: StatusType
    Description: NotRequired[str]
    EgressIp: NotRequired[str]
    MediaStreams: NotRequired[List[MediaStreamTypeDef]]
    SourceFailoverConfig: NotRequired[FailoverConfigTypeDef]
    Sources: NotRequired[List[SourceTypeDef]]
    VpcInterfaces: NotRequired[List[VpcInterfaceTypeDef]]
    Maintenance: NotRequired[MaintenanceTypeDef]
    SourceMonitoringConfig: NotRequired[MonitoringConfigTypeDef]


class UpdateFlowSourceResponseTypeDef(TypedDict):
    FlowArn: str
    Source: SourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFlowSourceMetadataResponseTypeDef(TypedDict):
    FlowArn: str
    Messages: List[MessageDetailTypeDef]
    Timestamp: datetime
    TransportMediaInfo: TransportMediaInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFlowResponseTypeDef(TypedDict):
    Flow: FlowTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFlowResponseTypeDef(TypedDict):
    Flow: FlowTypeDef
    Messages: MessagesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFlowResponseTypeDef(TypedDict):
    Flow: FlowTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
