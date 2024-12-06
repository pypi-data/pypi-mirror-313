"""
Type annotations for globalaccelerator service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/type_defs/)

Usage::

    ```python
    from mypy_boto3_globalaccelerator.type_defs import AcceleratorAttributesTypeDef

    data: AcceleratorAttributesTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AcceleratorStatusType,
    ByoipCidrStateType,
    ClientAffinityType,
    CustomRoutingAcceleratorStatusType,
    CustomRoutingDestinationTrafficStateType,
    CustomRoutingProtocolType,
    HealthCheckProtocolType,
    HealthStateType,
    IpAddressFamilyType,
    IpAddressTypeType,
    ProtocolType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AcceleratorAttributesTypeDef",
    "AcceleratorEventTypeDef",
    "AcceleratorTypeDef",
    "AddCustomRoutingEndpointsRequestRequestTypeDef",
    "AddCustomRoutingEndpointsResponseTypeDef",
    "AddEndpointsRequestRequestTypeDef",
    "AddEndpointsResponseTypeDef",
    "AdvertiseByoipCidrRequestRequestTypeDef",
    "AdvertiseByoipCidrResponseTypeDef",
    "AllowCustomRoutingTrafficRequestRequestTypeDef",
    "AttachmentTypeDef",
    "ByoipCidrEventTypeDef",
    "ByoipCidrTypeDef",
    "CidrAuthorizationContextTypeDef",
    "CreateAcceleratorRequestRequestTypeDef",
    "CreateAcceleratorResponseTypeDef",
    "CreateCrossAccountAttachmentRequestRequestTypeDef",
    "CreateCrossAccountAttachmentResponseTypeDef",
    "CreateCustomRoutingAcceleratorRequestRequestTypeDef",
    "CreateCustomRoutingAcceleratorResponseTypeDef",
    "CreateCustomRoutingEndpointGroupRequestRequestTypeDef",
    "CreateCustomRoutingEndpointGroupResponseTypeDef",
    "CreateCustomRoutingListenerRequestRequestTypeDef",
    "CreateCustomRoutingListenerResponseTypeDef",
    "CreateEndpointGroupRequestRequestTypeDef",
    "CreateEndpointGroupResponseTypeDef",
    "CreateListenerRequestRequestTypeDef",
    "CreateListenerResponseTypeDef",
    "CrossAccountResourceTypeDef",
    "CustomRoutingAcceleratorAttributesTypeDef",
    "CustomRoutingAcceleratorTypeDef",
    "CustomRoutingDestinationConfigurationTypeDef",
    "CustomRoutingDestinationDescriptionTypeDef",
    "CustomRoutingEndpointConfigurationTypeDef",
    "CustomRoutingEndpointDescriptionTypeDef",
    "CustomRoutingEndpointGroupTypeDef",
    "CustomRoutingListenerTypeDef",
    "DeleteAcceleratorRequestRequestTypeDef",
    "DeleteCrossAccountAttachmentRequestRequestTypeDef",
    "DeleteCustomRoutingAcceleratorRequestRequestTypeDef",
    "DeleteCustomRoutingEndpointGroupRequestRequestTypeDef",
    "DeleteCustomRoutingListenerRequestRequestTypeDef",
    "DeleteEndpointGroupRequestRequestTypeDef",
    "DeleteListenerRequestRequestTypeDef",
    "DenyCustomRoutingTrafficRequestRequestTypeDef",
    "DeprovisionByoipCidrRequestRequestTypeDef",
    "DeprovisionByoipCidrResponseTypeDef",
    "DescribeAcceleratorAttributesRequestRequestTypeDef",
    "DescribeAcceleratorAttributesResponseTypeDef",
    "DescribeAcceleratorRequestRequestTypeDef",
    "DescribeAcceleratorResponseTypeDef",
    "DescribeCrossAccountAttachmentRequestRequestTypeDef",
    "DescribeCrossAccountAttachmentResponseTypeDef",
    "DescribeCustomRoutingAcceleratorAttributesRequestRequestTypeDef",
    "DescribeCustomRoutingAcceleratorAttributesResponseTypeDef",
    "DescribeCustomRoutingAcceleratorRequestRequestTypeDef",
    "DescribeCustomRoutingAcceleratorResponseTypeDef",
    "DescribeCustomRoutingEndpointGroupRequestRequestTypeDef",
    "DescribeCustomRoutingEndpointGroupResponseTypeDef",
    "DescribeCustomRoutingListenerRequestRequestTypeDef",
    "DescribeCustomRoutingListenerResponseTypeDef",
    "DescribeEndpointGroupRequestRequestTypeDef",
    "DescribeEndpointGroupResponseTypeDef",
    "DescribeListenerRequestRequestTypeDef",
    "DescribeListenerResponseTypeDef",
    "DestinationPortMappingTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EndpointConfigurationTypeDef",
    "EndpointDescriptionTypeDef",
    "EndpointGroupTypeDef",
    "EndpointIdentifierTypeDef",
    "IpSetTypeDef",
    "ListAcceleratorsRequestListAcceleratorsPaginateTypeDef",
    "ListAcceleratorsRequestRequestTypeDef",
    "ListAcceleratorsResponseTypeDef",
    "ListByoipCidrsRequestListByoipCidrsPaginateTypeDef",
    "ListByoipCidrsRequestRequestTypeDef",
    "ListByoipCidrsResponseTypeDef",
    "ListCrossAccountAttachmentsRequestListCrossAccountAttachmentsPaginateTypeDef",
    "ListCrossAccountAttachmentsRequestRequestTypeDef",
    "ListCrossAccountAttachmentsResponseTypeDef",
    "ListCrossAccountResourceAccountsResponseTypeDef",
    "ListCrossAccountResourcesRequestListCrossAccountResourcesPaginateTypeDef",
    "ListCrossAccountResourcesRequestRequestTypeDef",
    "ListCrossAccountResourcesResponseTypeDef",
    "ListCustomRoutingAcceleratorsRequestListCustomRoutingAcceleratorsPaginateTypeDef",
    "ListCustomRoutingAcceleratorsRequestRequestTypeDef",
    "ListCustomRoutingAcceleratorsResponseTypeDef",
    "ListCustomRoutingEndpointGroupsRequestListCustomRoutingEndpointGroupsPaginateTypeDef",
    "ListCustomRoutingEndpointGroupsRequestRequestTypeDef",
    "ListCustomRoutingEndpointGroupsResponseTypeDef",
    "ListCustomRoutingListenersRequestListCustomRoutingListenersPaginateTypeDef",
    "ListCustomRoutingListenersRequestRequestTypeDef",
    "ListCustomRoutingListenersResponseTypeDef",
    "ListCustomRoutingPortMappingsByDestinationRequestListCustomRoutingPortMappingsByDestinationPaginateTypeDef",
    "ListCustomRoutingPortMappingsByDestinationRequestRequestTypeDef",
    "ListCustomRoutingPortMappingsByDestinationResponseTypeDef",
    "ListCustomRoutingPortMappingsRequestListCustomRoutingPortMappingsPaginateTypeDef",
    "ListCustomRoutingPortMappingsRequestRequestTypeDef",
    "ListCustomRoutingPortMappingsResponseTypeDef",
    "ListEndpointGroupsRequestListEndpointGroupsPaginateTypeDef",
    "ListEndpointGroupsRequestRequestTypeDef",
    "ListEndpointGroupsResponseTypeDef",
    "ListListenersRequestListListenersPaginateTypeDef",
    "ListListenersRequestRequestTypeDef",
    "ListListenersResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListenerTypeDef",
    "PaginatorConfigTypeDef",
    "PortMappingTypeDef",
    "PortOverrideTypeDef",
    "PortRangeTypeDef",
    "ProvisionByoipCidrRequestRequestTypeDef",
    "ProvisionByoipCidrResponseTypeDef",
    "RemoveCustomRoutingEndpointsRequestRequestTypeDef",
    "RemoveEndpointsRequestRequestTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "SocketAddressTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAcceleratorAttributesRequestRequestTypeDef",
    "UpdateAcceleratorAttributesResponseTypeDef",
    "UpdateAcceleratorRequestRequestTypeDef",
    "UpdateAcceleratorResponseTypeDef",
    "UpdateCrossAccountAttachmentRequestRequestTypeDef",
    "UpdateCrossAccountAttachmentResponseTypeDef",
    "UpdateCustomRoutingAcceleratorAttributesRequestRequestTypeDef",
    "UpdateCustomRoutingAcceleratorAttributesResponseTypeDef",
    "UpdateCustomRoutingAcceleratorRequestRequestTypeDef",
    "UpdateCustomRoutingAcceleratorResponseTypeDef",
    "UpdateCustomRoutingListenerRequestRequestTypeDef",
    "UpdateCustomRoutingListenerResponseTypeDef",
    "UpdateEndpointGroupRequestRequestTypeDef",
    "UpdateEndpointGroupResponseTypeDef",
    "UpdateListenerRequestRequestTypeDef",
    "UpdateListenerResponseTypeDef",
    "WithdrawByoipCidrRequestRequestTypeDef",
    "WithdrawByoipCidrResponseTypeDef",
)

class AcceleratorAttributesTypeDef(TypedDict):
    FlowLogsEnabled: NotRequired[bool]
    FlowLogsS3Bucket: NotRequired[str]
    FlowLogsS3Prefix: NotRequired[str]

class AcceleratorEventTypeDef(TypedDict):
    Message: NotRequired[str]
    Timestamp: NotRequired[datetime]

class IpSetTypeDef(TypedDict):
    IpFamily: NotRequired[str]
    IpAddresses: NotRequired[List[str]]
    IpAddressFamily: NotRequired[IpAddressFamilyType]

class CustomRoutingEndpointConfigurationTypeDef(TypedDict):
    EndpointId: NotRequired[str]
    AttachmentArn: NotRequired[str]

class CustomRoutingEndpointDescriptionTypeDef(TypedDict):
    EndpointId: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class EndpointConfigurationTypeDef(TypedDict):
    EndpointId: NotRequired[str]
    Weight: NotRequired[int]
    ClientIPPreservationEnabled: NotRequired[bool]
    AttachmentArn: NotRequired[str]

class EndpointDescriptionTypeDef(TypedDict):
    EndpointId: NotRequired[str]
    Weight: NotRequired[int]
    HealthState: NotRequired[HealthStateType]
    HealthReason: NotRequired[str]
    ClientIPPreservationEnabled: NotRequired[bool]

class AdvertiseByoipCidrRequestRequestTypeDef(TypedDict):
    Cidr: str

class AllowCustomRoutingTrafficRequestRequestTypeDef(TypedDict):
    EndpointGroupArn: str
    EndpointId: str
    DestinationAddresses: NotRequired[Sequence[str]]
    DestinationPorts: NotRequired[Sequence[int]]
    AllowAllTrafficToEndpoint: NotRequired[bool]

class ResourceTypeDef(TypedDict):
    EndpointId: NotRequired[str]
    Cidr: NotRequired[str]
    Region: NotRequired[str]

class ByoipCidrEventTypeDef(TypedDict):
    Message: NotRequired[str]
    Timestamp: NotRequired[datetime]

class CidrAuthorizationContextTypeDef(TypedDict):
    Message: str
    Signature: str

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class CustomRoutingDestinationConfigurationTypeDef(TypedDict):
    FromPort: int
    ToPort: int
    Protocols: Sequence[CustomRoutingProtocolType]

class PortRangeTypeDef(TypedDict):
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]

class PortOverrideTypeDef(TypedDict):
    ListenerPort: NotRequired[int]
    EndpointPort: NotRequired[int]

class CrossAccountResourceTypeDef(TypedDict):
    EndpointId: NotRequired[str]
    Cidr: NotRequired[str]
    AttachmentArn: NotRequired[str]

class CustomRoutingAcceleratorAttributesTypeDef(TypedDict):
    FlowLogsEnabled: NotRequired[bool]
    FlowLogsS3Bucket: NotRequired[str]
    FlowLogsS3Prefix: NotRequired[str]

class CustomRoutingDestinationDescriptionTypeDef(TypedDict):
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]
    Protocols: NotRequired[List[ProtocolType]]

class DeleteAcceleratorRequestRequestTypeDef(TypedDict):
    AcceleratorArn: str

class DeleteCrossAccountAttachmentRequestRequestTypeDef(TypedDict):
    AttachmentArn: str

class DeleteCustomRoutingAcceleratorRequestRequestTypeDef(TypedDict):
    AcceleratorArn: str

class DeleteCustomRoutingEndpointGroupRequestRequestTypeDef(TypedDict):
    EndpointGroupArn: str

class DeleteCustomRoutingListenerRequestRequestTypeDef(TypedDict):
    ListenerArn: str

class DeleteEndpointGroupRequestRequestTypeDef(TypedDict):
    EndpointGroupArn: str

class DeleteListenerRequestRequestTypeDef(TypedDict):
    ListenerArn: str

class DenyCustomRoutingTrafficRequestRequestTypeDef(TypedDict):
    EndpointGroupArn: str
    EndpointId: str
    DestinationAddresses: NotRequired[Sequence[str]]
    DestinationPorts: NotRequired[Sequence[int]]
    DenyAllTrafficToEndpoint: NotRequired[bool]

class DeprovisionByoipCidrRequestRequestTypeDef(TypedDict):
    Cidr: str

class DescribeAcceleratorAttributesRequestRequestTypeDef(TypedDict):
    AcceleratorArn: str

class DescribeAcceleratorRequestRequestTypeDef(TypedDict):
    AcceleratorArn: str

class DescribeCrossAccountAttachmentRequestRequestTypeDef(TypedDict):
    AttachmentArn: str

class DescribeCustomRoutingAcceleratorAttributesRequestRequestTypeDef(TypedDict):
    AcceleratorArn: str

class DescribeCustomRoutingAcceleratorRequestRequestTypeDef(TypedDict):
    AcceleratorArn: str

class DescribeCustomRoutingEndpointGroupRequestRequestTypeDef(TypedDict):
    EndpointGroupArn: str

class DescribeCustomRoutingListenerRequestRequestTypeDef(TypedDict):
    ListenerArn: str

class DescribeEndpointGroupRequestRequestTypeDef(TypedDict):
    EndpointGroupArn: str

class DescribeListenerRequestRequestTypeDef(TypedDict):
    ListenerArn: str

class SocketAddressTypeDef(TypedDict):
    IpAddress: NotRequired[str]
    Port: NotRequired[int]

class EndpointIdentifierTypeDef(TypedDict):
    EndpointId: str
    ClientIPPreservationEnabled: NotRequired[bool]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAcceleratorsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListByoipCidrsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListCrossAccountAttachmentsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListCrossAccountResourcesRequestRequestTypeDef(TypedDict):
    ResourceOwnerAwsAccountId: str
    AcceleratorArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListCustomRoutingAcceleratorsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListCustomRoutingEndpointGroupsRequestRequestTypeDef(TypedDict):
    ListenerArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListCustomRoutingListenersRequestRequestTypeDef(TypedDict):
    AcceleratorArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListCustomRoutingPortMappingsByDestinationRequestRequestTypeDef(TypedDict):
    EndpointId: str
    DestinationAddress: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListCustomRoutingPortMappingsRequestRequestTypeDef(TypedDict):
    AcceleratorArn: str
    EndpointGroupArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListEndpointGroupsRequestRequestTypeDef(TypedDict):
    ListenerArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListListenersRequestRequestTypeDef(TypedDict):
    AcceleratorArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class RemoveCustomRoutingEndpointsRequestRequestTypeDef(TypedDict):
    EndpointIds: Sequence[str]
    EndpointGroupArn: str

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateAcceleratorAttributesRequestRequestTypeDef(TypedDict):
    AcceleratorArn: str
    FlowLogsEnabled: NotRequired[bool]
    FlowLogsS3Bucket: NotRequired[str]
    FlowLogsS3Prefix: NotRequired[str]

class UpdateAcceleratorRequestRequestTypeDef(TypedDict):
    AcceleratorArn: str
    Name: NotRequired[str]
    IpAddressType: NotRequired[IpAddressTypeType]
    IpAddresses: NotRequired[Sequence[str]]
    Enabled: NotRequired[bool]

class UpdateCustomRoutingAcceleratorAttributesRequestRequestTypeDef(TypedDict):
    AcceleratorArn: str
    FlowLogsEnabled: NotRequired[bool]
    FlowLogsS3Bucket: NotRequired[str]
    FlowLogsS3Prefix: NotRequired[str]

class UpdateCustomRoutingAcceleratorRequestRequestTypeDef(TypedDict):
    AcceleratorArn: str
    Name: NotRequired[str]
    IpAddressType: NotRequired[IpAddressTypeType]
    IpAddresses: NotRequired[Sequence[str]]
    Enabled: NotRequired[bool]

class WithdrawByoipCidrRequestRequestTypeDef(TypedDict):
    Cidr: str

class AcceleratorTypeDef(TypedDict):
    AcceleratorArn: NotRequired[str]
    Name: NotRequired[str]
    IpAddressType: NotRequired[IpAddressTypeType]
    Enabled: NotRequired[bool]
    IpSets: NotRequired[List[IpSetTypeDef]]
    DnsName: NotRequired[str]
    Status: NotRequired[AcceleratorStatusType]
    CreatedTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    DualStackDnsName: NotRequired[str]
    Events: NotRequired[List[AcceleratorEventTypeDef]]

class CustomRoutingAcceleratorTypeDef(TypedDict):
    AcceleratorArn: NotRequired[str]
    Name: NotRequired[str]
    IpAddressType: NotRequired[IpAddressTypeType]
    Enabled: NotRequired[bool]
    IpSets: NotRequired[List[IpSetTypeDef]]
    DnsName: NotRequired[str]
    Status: NotRequired[CustomRoutingAcceleratorStatusType]
    CreatedTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]

class AddCustomRoutingEndpointsRequestRequestTypeDef(TypedDict):
    EndpointConfigurations: Sequence[CustomRoutingEndpointConfigurationTypeDef]
    EndpointGroupArn: str

class AddCustomRoutingEndpointsResponseTypeDef(TypedDict):
    EndpointDescriptions: List[CustomRoutingEndpointDescriptionTypeDef]
    EndpointGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAcceleratorAttributesResponseTypeDef(TypedDict):
    AcceleratorAttributes: AcceleratorAttributesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ListCrossAccountResourceAccountsResponseTypeDef(TypedDict):
    ResourceOwnerAwsAccountIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAcceleratorAttributesResponseTypeDef(TypedDict):
    AcceleratorAttributes: AcceleratorAttributesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AddEndpointsRequestRequestTypeDef(TypedDict):
    EndpointConfigurations: Sequence[EndpointConfigurationTypeDef]
    EndpointGroupArn: str

class AddEndpointsResponseTypeDef(TypedDict):
    EndpointDescriptions: List[EndpointDescriptionTypeDef]
    EndpointGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class AttachmentTypeDef(TypedDict):
    AttachmentArn: NotRequired[str]
    Name: NotRequired[str]
    Principals: NotRequired[List[str]]
    Resources: NotRequired[List[ResourceTypeDef]]
    LastModifiedTime: NotRequired[datetime]
    CreatedTime: NotRequired[datetime]

class UpdateCrossAccountAttachmentRequestRequestTypeDef(TypedDict):
    AttachmentArn: str
    Name: NotRequired[str]
    AddPrincipals: NotRequired[Sequence[str]]
    RemovePrincipals: NotRequired[Sequence[str]]
    AddResources: NotRequired[Sequence[ResourceTypeDef]]
    RemoveResources: NotRequired[Sequence[ResourceTypeDef]]

class ByoipCidrTypeDef(TypedDict):
    Cidr: NotRequired[str]
    State: NotRequired[ByoipCidrStateType]
    Events: NotRequired[List[ByoipCidrEventTypeDef]]

class ProvisionByoipCidrRequestRequestTypeDef(TypedDict):
    Cidr: str
    CidrAuthorizationContext: CidrAuthorizationContextTypeDef

class CreateAcceleratorRequestRequestTypeDef(TypedDict):
    Name: str
    IdempotencyToken: str
    IpAddressType: NotRequired[IpAddressTypeType]
    IpAddresses: NotRequired[Sequence[str]]
    Enabled: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateCrossAccountAttachmentRequestRequestTypeDef(TypedDict):
    Name: str
    IdempotencyToken: str
    Principals: NotRequired[Sequence[str]]
    Resources: NotRequired[Sequence[ResourceTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateCustomRoutingAcceleratorRequestRequestTypeDef(TypedDict):
    Name: str
    IdempotencyToken: str
    IpAddressType: NotRequired[IpAddressTypeType]
    IpAddresses: NotRequired[Sequence[str]]
    Enabled: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]

class CreateCustomRoutingEndpointGroupRequestRequestTypeDef(TypedDict):
    ListenerArn: str
    EndpointGroupRegion: str
    DestinationConfigurations: Sequence[CustomRoutingDestinationConfigurationTypeDef]
    IdempotencyToken: str

class CreateCustomRoutingListenerRequestRequestTypeDef(TypedDict):
    AcceleratorArn: str
    PortRanges: Sequence[PortRangeTypeDef]
    IdempotencyToken: str

CreateListenerRequestRequestTypeDef = TypedDict(
    "CreateListenerRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
        "PortRanges": Sequence[PortRangeTypeDef],
        "Protocol": ProtocolType,
        "IdempotencyToken": str,
        "ClientAffinity": NotRequired[ClientAffinityType],
    },
)

class CustomRoutingListenerTypeDef(TypedDict):
    ListenerArn: NotRequired[str]
    PortRanges: NotRequired[List[PortRangeTypeDef]]

ListenerTypeDef = TypedDict(
    "ListenerTypeDef",
    {
        "ListenerArn": NotRequired[str],
        "PortRanges": NotRequired[List[PortRangeTypeDef]],
        "Protocol": NotRequired[ProtocolType],
        "ClientAffinity": NotRequired[ClientAffinityType],
    },
)

class UpdateCustomRoutingListenerRequestRequestTypeDef(TypedDict):
    ListenerArn: str
    PortRanges: Sequence[PortRangeTypeDef]

UpdateListenerRequestRequestTypeDef = TypedDict(
    "UpdateListenerRequestRequestTypeDef",
    {
        "ListenerArn": str,
        "PortRanges": NotRequired[Sequence[PortRangeTypeDef]],
        "Protocol": NotRequired[ProtocolType],
        "ClientAffinity": NotRequired[ClientAffinityType],
    },
)

class CreateEndpointGroupRequestRequestTypeDef(TypedDict):
    ListenerArn: str
    EndpointGroupRegion: str
    IdempotencyToken: str
    EndpointConfigurations: NotRequired[Sequence[EndpointConfigurationTypeDef]]
    TrafficDialPercentage: NotRequired[float]
    HealthCheckPort: NotRequired[int]
    HealthCheckProtocol: NotRequired[HealthCheckProtocolType]
    HealthCheckPath: NotRequired[str]
    HealthCheckIntervalSeconds: NotRequired[int]
    ThresholdCount: NotRequired[int]
    PortOverrides: NotRequired[Sequence[PortOverrideTypeDef]]

class EndpointGroupTypeDef(TypedDict):
    EndpointGroupArn: NotRequired[str]
    EndpointGroupRegion: NotRequired[str]
    EndpointDescriptions: NotRequired[List[EndpointDescriptionTypeDef]]
    TrafficDialPercentage: NotRequired[float]
    HealthCheckPort: NotRequired[int]
    HealthCheckProtocol: NotRequired[HealthCheckProtocolType]
    HealthCheckPath: NotRequired[str]
    HealthCheckIntervalSeconds: NotRequired[int]
    ThresholdCount: NotRequired[int]
    PortOverrides: NotRequired[List[PortOverrideTypeDef]]

class UpdateEndpointGroupRequestRequestTypeDef(TypedDict):
    EndpointGroupArn: str
    EndpointConfigurations: NotRequired[Sequence[EndpointConfigurationTypeDef]]
    TrafficDialPercentage: NotRequired[float]
    HealthCheckPort: NotRequired[int]
    HealthCheckProtocol: NotRequired[HealthCheckProtocolType]
    HealthCheckPath: NotRequired[str]
    HealthCheckIntervalSeconds: NotRequired[int]
    ThresholdCount: NotRequired[int]
    PortOverrides: NotRequired[Sequence[PortOverrideTypeDef]]

class ListCrossAccountResourcesResponseTypeDef(TypedDict):
    CrossAccountResources: List[CrossAccountResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeCustomRoutingAcceleratorAttributesResponseTypeDef(TypedDict):
    AcceleratorAttributes: CustomRoutingAcceleratorAttributesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateCustomRoutingAcceleratorAttributesResponseTypeDef(TypedDict):
    AcceleratorAttributes: CustomRoutingAcceleratorAttributesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CustomRoutingEndpointGroupTypeDef(TypedDict):
    EndpointGroupArn: NotRequired[str]
    EndpointGroupRegion: NotRequired[str]
    DestinationDescriptions: NotRequired[List[CustomRoutingDestinationDescriptionTypeDef]]
    EndpointDescriptions: NotRequired[List[CustomRoutingEndpointDescriptionTypeDef]]

class DestinationPortMappingTypeDef(TypedDict):
    AcceleratorArn: NotRequired[str]
    AcceleratorSocketAddresses: NotRequired[List[SocketAddressTypeDef]]
    EndpointGroupArn: NotRequired[str]
    EndpointId: NotRequired[str]
    EndpointGroupRegion: NotRequired[str]
    DestinationSocketAddress: NotRequired[SocketAddressTypeDef]
    IpAddressType: NotRequired[IpAddressTypeType]
    DestinationTrafficState: NotRequired[CustomRoutingDestinationTrafficStateType]

class PortMappingTypeDef(TypedDict):
    AcceleratorPort: NotRequired[int]
    EndpointGroupArn: NotRequired[str]
    EndpointId: NotRequired[str]
    DestinationSocketAddress: NotRequired[SocketAddressTypeDef]
    Protocols: NotRequired[List[CustomRoutingProtocolType]]
    DestinationTrafficState: NotRequired[CustomRoutingDestinationTrafficStateType]

class RemoveEndpointsRequestRequestTypeDef(TypedDict):
    EndpointIdentifiers: Sequence[EndpointIdentifierTypeDef]
    EndpointGroupArn: str

class ListAcceleratorsRequestListAcceleratorsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListByoipCidrsRequestListByoipCidrsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCrossAccountAttachmentsRequestListCrossAccountAttachmentsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCrossAccountResourcesRequestListCrossAccountResourcesPaginateTypeDef(TypedDict):
    ResourceOwnerAwsAccountId: str
    AcceleratorArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCustomRoutingAcceleratorsRequestListCustomRoutingAcceleratorsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCustomRoutingEndpointGroupsRequestListCustomRoutingEndpointGroupsPaginateTypeDef(
    TypedDict
):
    ListenerArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCustomRoutingListenersRequestListCustomRoutingListenersPaginateTypeDef(TypedDict):
    AcceleratorArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCustomRoutingPortMappingsByDestinationRequestListCustomRoutingPortMappingsByDestinationPaginateTypeDef(
    TypedDict
):
    EndpointId: str
    DestinationAddress: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCustomRoutingPortMappingsRequestListCustomRoutingPortMappingsPaginateTypeDef(TypedDict):
    AcceleratorArn: str
    EndpointGroupArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEndpointGroupsRequestListEndpointGroupsPaginateTypeDef(TypedDict):
    ListenerArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListListenersRequestListListenersPaginateTypeDef(TypedDict):
    AcceleratorArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class CreateAcceleratorResponseTypeDef(TypedDict):
    Accelerator: AcceleratorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAcceleratorResponseTypeDef(TypedDict):
    Accelerator: AcceleratorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAcceleratorsResponseTypeDef(TypedDict):
    Accelerators: List[AcceleratorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateAcceleratorResponseTypeDef(TypedDict):
    Accelerator: AcceleratorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCustomRoutingAcceleratorResponseTypeDef(TypedDict):
    Accelerator: CustomRoutingAcceleratorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeCustomRoutingAcceleratorResponseTypeDef(TypedDict):
    Accelerator: CustomRoutingAcceleratorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListCustomRoutingAcceleratorsResponseTypeDef(TypedDict):
    Accelerators: List[CustomRoutingAcceleratorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateCustomRoutingAcceleratorResponseTypeDef(TypedDict):
    Accelerator: CustomRoutingAcceleratorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCrossAccountAttachmentResponseTypeDef(TypedDict):
    CrossAccountAttachment: AttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeCrossAccountAttachmentResponseTypeDef(TypedDict):
    CrossAccountAttachment: AttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListCrossAccountAttachmentsResponseTypeDef(TypedDict):
    CrossAccountAttachments: List[AttachmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateCrossAccountAttachmentResponseTypeDef(TypedDict):
    CrossAccountAttachment: AttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AdvertiseByoipCidrResponseTypeDef(TypedDict):
    ByoipCidr: ByoipCidrTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeprovisionByoipCidrResponseTypeDef(TypedDict):
    ByoipCidr: ByoipCidrTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListByoipCidrsResponseTypeDef(TypedDict):
    ByoipCidrs: List[ByoipCidrTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ProvisionByoipCidrResponseTypeDef(TypedDict):
    ByoipCidr: ByoipCidrTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class WithdrawByoipCidrResponseTypeDef(TypedDict):
    ByoipCidr: ByoipCidrTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCustomRoutingListenerResponseTypeDef(TypedDict):
    Listener: CustomRoutingListenerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeCustomRoutingListenerResponseTypeDef(TypedDict):
    Listener: CustomRoutingListenerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListCustomRoutingListenersResponseTypeDef(TypedDict):
    Listeners: List[CustomRoutingListenerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateCustomRoutingListenerResponseTypeDef(TypedDict):
    Listener: CustomRoutingListenerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateListenerResponseTypeDef(TypedDict):
    Listener: ListenerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeListenerResponseTypeDef(TypedDict):
    Listener: ListenerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListListenersResponseTypeDef(TypedDict):
    Listeners: List[ListenerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateListenerResponseTypeDef(TypedDict):
    Listener: ListenerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEndpointGroupResponseTypeDef(TypedDict):
    EndpointGroup: EndpointGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeEndpointGroupResponseTypeDef(TypedDict):
    EndpointGroup: EndpointGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListEndpointGroupsResponseTypeDef(TypedDict):
    EndpointGroups: List[EndpointGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateEndpointGroupResponseTypeDef(TypedDict):
    EndpointGroup: EndpointGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCustomRoutingEndpointGroupResponseTypeDef(TypedDict):
    EndpointGroup: CustomRoutingEndpointGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeCustomRoutingEndpointGroupResponseTypeDef(TypedDict):
    EndpointGroup: CustomRoutingEndpointGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListCustomRoutingEndpointGroupsResponseTypeDef(TypedDict):
    EndpointGroups: List[CustomRoutingEndpointGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListCustomRoutingPortMappingsByDestinationResponseTypeDef(TypedDict):
    DestinationPortMappings: List[DestinationPortMappingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListCustomRoutingPortMappingsResponseTypeDef(TypedDict):
    PortMappings: List[PortMappingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
