"""
Type annotations for memorydb service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/type_defs/)

Usage::

    ```python
    from mypy_boto3_memorydb.type_defs import ACLPendingChangesTypeDef

    data: ACLPendingChangesTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AuthenticationTypeType,
    AZStatusType,
    DataTieringStatusType,
    InputAuthenticationTypeType,
    ServiceUpdateStatusType,
    SourceTypeType,
    UpdateStrategyType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ACLPendingChangesTypeDef",
    "ACLTypeDef",
    "ACLsUpdateStatusTypeDef",
    "AuthenticationModeTypeDef",
    "AuthenticationTypeDef",
    "AvailabilityZoneTypeDef",
    "BatchUpdateClusterRequestRequestTypeDef",
    "BatchUpdateClusterResponseTypeDef",
    "ClusterConfigurationTypeDef",
    "ClusterPendingUpdatesTypeDef",
    "ClusterTypeDef",
    "CopySnapshotRequestRequestTypeDef",
    "CopySnapshotResponseTypeDef",
    "CreateACLRequestRequestTypeDef",
    "CreateACLResponseTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "CreateClusterResponseTypeDef",
    "CreateMultiRegionClusterRequestRequestTypeDef",
    "CreateMultiRegionClusterResponseTypeDef",
    "CreateParameterGroupRequestRequestTypeDef",
    "CreateParameterGroupResponseTypeDef",
    "CreateSnapshotRequestRequestTypeDef",
    "CreateSnapshotResponseTypeDef",
    "CreateSubnetGroupRequestRequestTypeDef",
    "CreateSubnetGroupResponseTypeDef",
    "CreateUserRequestRequestTypeDef",
    "CreateUserResponseTypeDef",
    "DeleteACLRequestRequestTypeDef",
    "DeleteACLResponseTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteClusterResponseTypeDef",
    "DeleteMultiRegionClusterRequestRequestTypeDef",
    "DeleteMultiRegionClusterResponseTypeDef",
    "DeleteParameterGroupRequestRequestTypeDef",
    "DeleteParameterGroupResponseTypeDef",
    "DeleteSnapshotRequestRequestTypeDef",
    "DeleteSnapshotResponseTypeDef",
    "DeleteSubnetGroupRequestRequestTypeDef",
    "DeleteSubnetGroupResponseTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DeleteUserResponseTypeDef",
    "DescribeACLsRequestDescribeACLsPaginateTypeDef",
    "DescribeACLsRequestRequestTypeDef",
    "DescribeACLsResponseTypeDef",
    "DescribeClustersRequestDescribeClustersPaginateTypeDef",
    "DescribeClustersRequestRequestTypeDef",
    "DescribeClustersResponseTypeDef",
    "DescribeEngineVersionsRequestDescribeEngineVersionsPaginateTypeDef",
    "DescribeEngineVersionsRequestRequestTypeDef",
    "DescribeEngineVersionsResponseTypeDef",
    "DescribeEventsRequestDescribeEventsPaginateTypeDef",
    "DescribeEventsRequestRequestTypeDef",
    "DescribeEventsResponseTypeDef",
    "DescribeMultiRegionClustersRequestDescribeMultiRegionClustersPaginateTypeDef",
    "DescribeMultiRegionClustersRequestRequestTypeDef",
    "DescribeMultiRegionClustersResponseTypeDef",
    "DescribeParameterGroupsRequestDescribeParameterGroupsPaginateTypeDef",
    "DescribeParameterGroupsRequestRequestTypeDef",
    "DescribeParameterGroupsResponseTypeDef",
    "DescribeParametersRequestDescribeParametersPaginateTypeDef",
    "DescribeParametersRequestRequestTypeDef",
    "DescribeParametersResponseTypeDef",
    "DescribeReservedNodesOfferingsRequestDescribeReservedNodesOfferingsPaginateTypeDef",
    "DescribeReservedNodesOfferingsRequestRequestTypeDef",
    "DescribeReservedNodesOfferingsResponseTypeDef",
    "DescribeReservedNodesRequestDescribeReservedNodesPaginateTypeDef",
    "DescribeReservedNodesRequestRequestTypeDef",
    "DescribeReservedNodesResponseTypeDef",
    "DescribeServiceUpdatesRequestDescribeServiceUpdatesPaginateTypeDef",
    "DescribeServiceUpdatesRequestRequestTypeDef",
    "DescribeServiceUpdatesResponseTypeDef",
    "DescribeSnapshotsRequestDescribeSnapshotsPaginateTypeDef",
    "DescribeSnapshotsRequestRequestTypeDef",
    "DescribeSnapshotsResponseTypeDef",
    "DescribeSubnetGroupsRequestDescribeSubnetGroupsPaginateTypeDef",
    "DescribeSubnetGroupsRequestRequestTypeDef",
    "DescribeSubnetGroupsResponseTypeDef",
    "DescribeUsersRequestDescribeUsersPaginateTypeDef",
    "DescribeUsersRequestRequestTypeDef",
    "DescribeUsersResponseTypeDef",
    "EndpointTypeDef",
    "EngineVersionInfoTypeDef",
    "EventTypeDef",
    "FailoverShardRequestRequestTypeDef",
    "FailoverShardResponseTypeDef",
    "FilterTypeDef",
    "ListAllowedMultiRegionClusterUpdatesRequestRequestTypeDef",
    "ListAllowedMultiRegionClusterUpdatesResponseTypeDef",
    "ListAllowedNodeTypeUpdatesRequestRequestTypeDef",
    "ListAllowedNodeTypeUpdatesResponseTypeDef",
    "ListTagsRequestRequestTypeDef",
    "ListTagsResponseTypeDef",
    "MultiRegionClusterTypeDef",
    "NodeTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterGroupTypeDef",
    "ParameterNameValueTypeDef",
    "ParameterTypeDef",
    "PendingModifiedServiceUpdateTypeDef",
    "PurchaseReservedNodesOfferingRequestRequestTypeDef",
    "PurchaseReservedNodesOfferingResponseTypeDef",
    "RecurringChargeTypeDef",
    "RegionalClusterTypeDef",
    "ReplicaConfigurationRequestTypeDef",
    "ReservedNodeTypeDef",
    "ReservedNodesOfferingTypeDef",
    "ResetParameterGroupRequestRequestTypeDef",
    "ResetParameterGroupResponseTypeDef",
    "ReshardingStatusTypeDef",
    "ResponseMetadataTypeDef",
    "SecurityGroupMembershipTypeDef",
    "ServiceUpdateRequestTypeDef",
    "ServiceUpdateTypeDef",
    "ShardConfigurationRequestTypeDef",
    "ShardConfigurationTypeDef",
    "ShardDetailTypeDef",
    "ShardTypeDef",
    "SlotMigrationTypeDef",
    "SnapshotTypeDef",
    "SubnetGroupTypeDef",
    "SubnetTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagResourceResponseTypeDef",
    "TagTypeDef",
    "TimestampTypeDef",
    "UnprocessedClusterTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UntagResourceResponseTypeDef",
    "UpdateACLRequestRequestTypeDef",
    "UpdateACLResponseTypeDef",
    "UpdateClusterRequestRequestTypeDef",
    "UpdateClusterResponseTypeDef",
    "UpdateMultiRegionClusterRequestRequestTypeDef",
    "UpdateMultiRegionClusterResponseTypeDef",
    "UpdateParameterGroupRequestRequestTypeDef",
    "UpdateParameterGroupResponseTypeDef",
    "UpdateSubnetGroupRequestRequestTypeDef",
    "UpdateSubnetGroupResponseTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "UpdateUserResponseTypeDef",
    "UserTypeDef",
)


class ACLPendingChangesTypeDef(TypedDict):
    UserNamesToRemove: NotRequired[List[str]]
    UserNamesToAdd: NotRequired[List[str]]


class ACLsUpdateStatusTypeDef(TypedDict):
    ACLToApply: NotRequired[str]


AuthenticationModeTypeDef = TypedDict(
    "AuthenticationModeTypeDef",
    {
        "Type": NotRequired[InputAuthenticationTypeType],
        "Passwords": NotRequired[Sequence[str]],
    },
)
AuthenticationTypeDef = TypedDict(
    "AuthenticationTypeDef",
    {
        "Type": NotRequired[AuthenticationTypeType],
        "PasswordCount": NotRequired[int],
    },
)


class AvailabilityZoneTypeDef(TypedDict):
    Name: NotRequired[str]


class ServiceUpdateRequestTypeDef(TypedDict):
    ServiceUpdateNameToApply: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class UnprocessedClusterTypeDef(TypedDict):
    ClusterName: NotRequired[str]
    ErrorType: NotRequired[str]
    ErrorMessage: NotRequired[str]


class PendingModifiedServiceUpdateTypeDef(TypedDict):
    ServiceUpdateName: NotRequired[str]
    Status: NotRequired[ServiceUpdateStatusType]


class EndpointTypeDef(TypedDict):
    Address: NotRequired[str]
    Port: NotRequired[int]


class SecurityGroupMembershipTypeDef(TypedDict):
    SecurityGroupId: NotRequired[str]
    Status: NotRequired[str]


class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class ParameterGroupTypeDef(TypedDict):
    Name: NotRequired[str]
    Family: NotRequired[str]
    Description: NotRequired[str]
    ARN: NotRequired[str]


class DeleteACLRequestRequestTypeDef(TypedDict):
    ACLName: str


class DeleteClusterRequestRequestTypeDef(TypedDict):
    ClusterName: str
    MultiRegionClusterName: NotRequired[str]
    FinalSnapshotName: NotRequired[str]


class DeleteMultiRegionClusterRequestRequestTypeDef(TypedDict):
    MultiRegionClusterName: str


class DeleteParameterGroupRequestRequestTypeDef(TypedDict):
    ParameterGroupName: str


class DeleteSnapshotRequestRequestTypeDef(TypedDict):
    SnapshotName: str


class DeleteSubnetGroupRequestRequestTypeDef(TypedDict):
    SubnetGroupName: str


class DeleteUserRequestRequestTypeDef(TypedDict):
    UserName: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeACLsRequestRequestTypeDef(TypedDict):
    ACLName: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeClustersRequestRequestTypeDef(TypedDict):
    ClusterName: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ShowShardDetails: NotRequired[bool]


class DescribeEngineVersionsRequestRequestTypeDef(TypedDict):
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    ParameterGroupFamily: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DefaultOnly: NotRequired[bool]


class EngineVersionInfoTypeDef(TypedDict):
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    EnginePatchVersion: NotRequired[str]
    ParameterGroupFamily: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class EventTypeDef(TypedDict):
    SourceName: NotRequired[str]
    SourceType: NotRequired[SourceTypeType]
    Message: NotRequired[str]
    Date: NotRequired[datetime]


class DescribeMultiRegionClustersRequestRequestTypeDef(TypedDict):
    MultiRegionClusterName: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ShowClusterDetails: NotRequired[bool]


class DescribeParameterGroupsRequestRequestTypeDef(TypedDict):
    ParameterGroupName: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeParametersRequestRequestTypeDef(TypedDict):
    ParameterGroupName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ParameterTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]
    Description: NotRequired[str]
    DataType: NotRequired[str]
    AllowedValues: NotRequired[str]
    MinimumEngineVersion: NotRequired[str]


class DescribeReservedNodesOfferingsRequestRequestTypeDef(TypedDict):
    ReservedNodesOfferingId: NotRequired[str]
    NodeType: NotRequired[str]
    Duration: NotRequired[str]
    OfferingType: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeReservedNodesRequestRequestTypeDef(TypedDict):
    ReservationId: NotRequired[str]
    ReservedNodesOfferingId: NotRequired[str]
    NodeType: NotRequired[str]
    Duration: NotRequired[str]
    OfferingType: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeServiceUpdatesRequestRequestTypeDef(TypedDict):
    ServiceUpdateName: NotRequired[str]
    ClusterNames: NotRequired[Sequence[str]]
    Status: NotRequired[Sequence[ServiceUpdateStatusType]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


ServiceUpdateTypeDef = TypedDict(
    "ServiceUpdateTypeDef",
    {
        "ClusterName": NotRequired[str],
        "ServiceUpdateName": NotRequired[str],
        "ReleaseDate": NotRequired[datetime],
        "Description": NotRequired[str],
        "Status": NotRequired[ServiceUpdateStatusType],
        "Type": NotRequired[Literal["security-update"]],
        "Engine": NotRequired[str],
        "NodesUpdated": NotRequired[str],
        "AutoUpdateStartDate": NotRequired[datetime],
    },
)


class DescribeSnapshotsRequestRequestTypeDef(TypedDict):
    ClusterName: NotRequired[str]
    SnapshotName: NotRequired[str]
    Source: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ShowDetail: NotRequired[bool]


class DescribeSubnetGroupsRequestRequestTypeDef(TypedDict):
    SubnetGroupName: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class FilterTypeDef(TypedDict):
    Name: str
    Values: Sequence[str]


class FailoverShardRequestRequestTypeDef(TypedDict):
    ClusterName: str
    ShardName: str


class ListAllowedMultiRegionClusterUpdatesRequestRequestTypeDef(TypedDict):
    MultiRegionClusterName: str


class ListAllowedNodeTypeUpdatesRequestRequestTypeDef(TypedDict):
    ClusterName: str


class ListTagsRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class RegionalClusterTypeDef(TypedDict):
    ClusterName: NotRequired[str]
    Region: NotRequired[str]
    Status: NotRequired[str]
    ARN: NotRequired[str]


class ParameterNameValueTypeDef(TypedDict):
    ParameterName: NotRequired[str]
    ParameterValue: NotRequired[str]


class RecurringChargeTypeDef(TypedDict):
    RecurringChargeAmount: NotRequired[float]
    RecurringChargeFrequency: NotRequired[str]


class ReplicaConfigurationRequestTypeDef(TypedDict):
    ReplicaCount: NotRequired[int]


class ResetParameterGroupRequestRequestTypeDef(TypedDict):
    ParameterGroupName: str
    AllParameters: NotRequired[bool]
    ParameterNames: NotRequired[Sequence[str]]


class SlotMigrationTypeDef(TypedDict):
    ProgressPercentage: NotRequired[float]


class ShardConfigurationRequestTypeDef(TypedDict):
    ShardCount: NotRequired[int]


class ShardConfigurationTypeDef(TypedDict):
    Slots: NotRequired[str]
    ReplicaCount: NotRequired[int]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateACLRequestRequestTypeDef(TypedDict):
    ACLName: str
    UserNamesToAdd: NotRequired[Sequence[str]]
    UserNamesToRemove: NotRequired[Sequence[str]]


class UpdateSubnetGroupRequestRequestTypeDef(TypedDict):
    SubnetGroupName: str
    Description: NotRequired[str]
    SubnetIds: NotRequired[Sequence[str]]


class ACLTypeDef(TypedDict):
    Name: NotRequired[str]
    Status: NotRequired[str]
    UserNames: NotRequired[List[str]]
    MinimumEngineVersion: NotRequired[str]
    PendingChanges: NotRequired[ACLPendingChangesTypeDef]
    Clusters: NotRequired[List[str]]
    ARN: NotRequired[str]


class UpdateUserRequestRequestTypeDef(TypedDict):
    UserName: str
    AuthenticationMode: NotRequired[AuthenticationModeTypeDef]
    AccessString: NotRequired[str]


class UserTypeDef(TypedDict):
    Name: NotRequired[str]
    Status: NotRequired[str]
    AccessString: NotRequired[str]
    ACLNames: NotRequired[List[str]]
    MinimumEngineVersion: NotRequired[str]
    Authentication: NotRequired[AuthenticationTypeDef]
    ARN: NotRequired[str]


class SubnetTypeDef(TypedDict):
    Identifier: NotRequired[str]
    AvailabilityZone: NotRequired[AvailabilityZoneTypeDef]


class BatchUpdateClusterRequestRequestTypeDef(TypedDict):
    ClusterNames: Sequence[str]
    ServiceUpdate: NotRequired[ServiceUpdateRequestTypeDef]


class ListAllowedMultiRegionClusterUpdatesResponseTypeDef(TypedDict):
    ScaleUpNodeTypes: List[str]
    ScaleDownNodeTypes: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListAllowedNodeTypeUpdatesResponseTypeDef(TypedDict):
    ScaleUpNodeTypes: List[str]
    ScaleDownNodeTypes: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class NodeTypeDef(TypedDict):
    Name: NotRequired[str]
    Status: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    CreateTime: NotRequired[datetime]
    Endpoint: NotRequired[EndpointTypeDef]


class CopySnapshotRequestRequestTypeDef(TypedDict):
    SourceSnapshotName: str
    TargetSnapshotName: str
    TargetBucket: NotRequired[str]
    KmsKeyId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateACLRequestRequestTypeDef(TypedDict):
    ACLName: str
    UserNames: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateClusterRequestRequestTypeDef(TypedDict):
    ClusterName: str
    NodeType: str
    ACLName: str
    MultiRegionClusterName: NotRequired[str]
    ParameterGroupName: NotRequired[str]
    Description: NotRequired[str]
    NumShards: NotRequired[int]
    NumReplicasPerShard: NotRequired[int]
    SubnetGroupName: NotRequired[str]
    SecurityGroupIds: NotRequired[Sequence[str]]
    MaintenanceWindow: NotRequired[str]
    Port: NotRequired[int]
    SnsTopicArn: NotRequired[str]
    TLSEnabled: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    SnapshotArns: NotRequired[Sequence[str]]
    SnapshotName: NotRequired[str]
    SnapshotRetentionLimit: NotRequired[int]
    Tags: NotRequired[Sequence[TagTypeDef]]
    SnapshotWindow: NotRequired[str]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    AutoMinorVersionUpgrade: NotRequired[bool]
    DataTiering: NotRequired[bool]


class CreateMultiRegionClusterRequestRequestTypeDef(TypedDict):
    MultiRegionClusterNameSuffix: str
    NodeType: str
    Description: NotRequired[str]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    MultiRegionParameterGroupName: NotRequired[str]
    NumShards: NotRequired[int]
    TLSEnabled: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateParameterGroupRequestRequestTypeDef(TypedDict):
    ParameterGroupName: str
    Family: str
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateSnapshotRequestRequestTypeDef(TypedDict):
    ClusterName: str
    SnapshotName: str
    KmsKeyId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateSubnetGroupRequestRequestTypeDef(TypedDict):
    SubnetGroupName: str
    SubnetIds: Sequence[str]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateUserRequestRequestTypeDef(TypedDict):
    UserName: str
    AuthenticationMode: AuthenticationModeTypeDef
    AccessString: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class ListTagsResponseTypeDef(TypedDict):
    TagList: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class PurchaseReservedNodesOfferingRequestRequestTypeDef(TypedDict):
    ReservedNodesOfferingId: str
    ReservationId: NotRequired[str]
    NodeCount: NotRequired[int]
    Tags: NotRequired[Sequence[TagTypeDef]]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]


class TagResourceResponseTypeDef(TypedDict):
    TagList: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UntagResourceResponseTypeDef(TypedDict):
    TagList: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateParameterGroupResponseTypeDef(TypedDict):
    ParameterGroup: ParameterGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteParameterGroupResponseTypeDef(TypedDict):
    ParameterGroup: ParameterGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeParameterGroupsResponseTypeDef(TypedDict):
    ParameterGroups: List[ParameterGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ResetParameterGroupResponseTypeDef(TypedDict):
    ParameterGroup: ParameterGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateParameterGroupResponseTypeDef(TypedDict):
    ParameterGroup: ParameterGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeACLsRequestDescribeACLsPaginateTypeDef(TypedDict):
    ACLName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeClustersRequestDescribeClustersPaginateTypeDef(TypedDict):
    ClusterName: NotRequired[str]
    ShowShardDetails: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEngineVersionsRequestDescribeEngineVersionsPaginateTypeDef(TypedDict):
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    ParameterGroupFamily: NotRequired[str]
    DefaultOnly: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeMultiRegionClustersRequestDescribeMultiRegionClustersPaginateTypeDef(TypedDict):
    MultiRegionClusterName: NotRequired[str]
    ShowClusterDetails: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeParameterGroupsRequestDescribeParameterGroupsPaginateTypeDef(TypedDict):
    ParameterGroupName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeParametersRequestDescribeParametersPaginateTypeDef(TypedDict):
    ParameterGroupName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeReservedNodesOfferingsRequestDescribeReservedNodesOfferingsPaginateTypeDef(TypedDict):
    ReservedNodesOfferingId: NotRequired[str]
    NodeType: NotRequired[str]
    Duration: NotRequired[str]
    OfferingType: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeReservedNodesRequestDescribeReservedNodesPaginateTypeDef(TypedDict):
    ReservationId: NotRequired[str]
    ReservedNodesOfferingId: NotRequired[str]
    NodeType: NotRequired[str]
    Duration: NotRequired[str]
    OfferingType: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeServiceUpdatesRequestDescribeServiceUpdatesPaginateTypeDef(TypedDict):
    ServiceUpdateName: NotRequired[str]
    ClusterNames: NotRequired[Sequence[str]]
    Status: NotRequired[Sequence[ServiceUpdateStatusType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSnapshotsRequestDescribeSnapshotsPaginateTypeDef(TypedDict):
    ClusterName: NotRequired[str]
    SnapshotName: NotRequired[str]
    Source: NotRequired[str]
    ShowDetail: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSubnetGroupsRequestDescribeSubnetGroupsPaginateTypeDef(TypedDict):
    SubnetGroupName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEngineVersionsResponseTypeDef(TypedDict):
    EngineVersions: List[EngineVersionInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeEventsRequestDescribeEventsPaginateTypeDef(TypedDict):
    SourceName: NotRequired[str]
    SourceType: NotRequired[SourceTypeType]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Duration: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEventsRequestRequestTypeDef(TypedDict):
    SourceName: NotRequired[str]
    SourceType: NotRequired[SourceTypeType]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Duration: NotRequired[int]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeEventsResponseTypeDef(TypedDict):
    Events: List[EventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeParametersResponseTypeDef(TypedDict):
    Parameters: List[ParameterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeServiceUpdatesResponseTypeDef(TypedDict):
    ServiceUpdates: List[ServiceUpdateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeUsersRequestDescribeUsersPaginateTypeDef(TypedDict):
    UserName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeUsersRequestRequestTypeDef(TypedDict):
    UserName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class MultiRegionClusterTypeDef(TypedDict):
    MultiRegionClusterName: NotRequired[str]
    Description: NotRequired[str]
    Status: NotRequired[str]
    NodeType: NotRequired[str]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    NumberOfShards: NotRequired[int]
    Clusters: NotRequired[List[RegionalClusterTypeDef]]
    MultiRegionParameterGroupName: NotRequired[str]
    TLSEnabled: NotRequired[bool]
    ARN: NotRequired[str]


class UpdateParameterGroupRequestRequestTypeDef(TypedDict):
    ParameterGroupName: str
    ParameterNameValues: Sequence[ParameterNameValueTypeDef]


class ReservedNodeTypeDef(TypedDict):
    ReservationId: NotRequired[str]
    ReservedNodesOfferingId: NotRequired[str]
    NodeType: NotRequired[str]
    StartTime: NotRequired[datetime]
    Duration: NotRequired[int]
    FixedPrice: NotRequired[float]
    NodeCount: NotRequired[int]
    OfferingType: NotRequired[str]
    State: NotRequired[str]
    RecurringCharges: NotRequired[List[RecurringChargeTypeDef]]
    ARN: NotRequired[str]


class ReservedNodesOfferingTypeDef(TypedDict):
    ReservedNodesOfferingId: NotRequired[str]
    NodeType: NotRequired[str]
    Duration: NotRequired[int]
    FixedPrice: NotRequired[float]
    OfferingType: NotRequired[str]
    RecurringCharges: NotRequired[List[RecurringChargeTypeDef]]


class ReshardingStatusTypeDef(TypedDict):
    SlotMigration: NotRequired[SlotMigrationTypeDef]


class UpdateClusterRequestRequestTypeDef(TypedDict):
    ClusterName: str
    Description: NotRequired[str]
    SecurityGroupIds: NotRequired[Sequence[str]]
    MaintenanceWindow: NotRequired[str]
    SnsTopicArn: NotRequired[str]
    SnsTopicStatus: NotRequired[str]
    ParameterGroupName: NotRequired[str]
    SnapshotWindow: NotRequired[str]
    SnapshotRetentionLimit: NotRequired[int]
    NodeType: NotRequired[str]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    ReplicaConfiguration: NotRequired[ReplicaConfigurationRequestTypeDef]
    ShardConfiguration: NotRequired[ShardConfigurationRequestTypeDef]
    ACLName: NotRequired[str]


class UpdateMultiRegionClusterRequestRequestTypeDef(TypedDict):
    MultiRegionClusterName: str
    NodeType: NotRequired[str]
    Description: NotRequired[str]
    EngineVersion: NotRequired[str]
    ShardConfiguration: NotRequired[ShardConfigurationRequestTypeDef]
    MultiRegionParameterGroupName: NotRequired[str]
    UpdateStrategy: NotRequired[UpdateStrategyType]


class ShardDetailTypeDef(TypedDict):
    Name: NotRequired[str]
    Configuration: NotRequired[ShardConfigurationTypeDef]
    Size: NotRequired[str]
    SnapshotCreationTime: NotRequired[datetime]


class CreateACLResponseTypeDef(TypedDict):
    ACL: ACLTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteACLResponseTypeDef(TypedDict):
    ACL: ACLTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeACLsResponseTypeDef(TypedDict):
    ACLs: List[ACLTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateACLResponseTypeDef(TypedDict):
    ACL: ACLTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUserResponseTypeDef(TypedDict):
    User: UserTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteUserResponseTypeDef(TypedDict):
    User: UserTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeUsersResponseTypeDef(TypedDict):
    Users: List[UserTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateUserResponseTypeDef(TypedDict):
    User: UserTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SubnetGroupTypeDef(TypedDict):
    Name: NotRequired[str]
    Description: NotRequired[str]
    VpcId: NotRequired[str]
    Subnets: NotRequired[List[SubnetTypeDef]]
    ARN: NotRequired[str]


class ShardTypeDef(TypedDict):
    Name: NotRequired[str]
    Status: NotRequired[str]
    Slots: NotRequired[str]
    Nodes: NotRequired[List[NodeTypeDef]]
    NumberOfNodes: NotRequired[int]


class CreateMultiRegionClusterResponseTypeDef(TypedDict):
    MultiRegionCluster: MultiRegionClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteMultiRegionClusterResponseTypeDef(TypedDict):
    MultiRegionCluster: MultiRegionClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeMultiRegionClustersResponseTypeDef(TypedDict):
    MultiRegionClusters: List[MultiRegionClusterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateMultiRegionClusterResponseTypeDef(TypedDict):
    MultiRegionCluster: MultiRegionClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeReservedNodesResponseTypeDef(TypedDict):
    ReservedNodes: List[ReservedNodeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PurchaseReservedNodesOfferingResponseTypeDef(TypedDict):
    ReservedNode: ReservedNodeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeReservedNodesOfferingsResponseTypeDef(TypedDict):
    ReservedNodesOfferings: List[ReservedNodesOfferingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ClusterPendingUpdatesTypeDef(TypedDict):
    Resharding: NotRequired[ReshardingStatusTypeDef]
    ACLs: NotRequired[ACLsUpdateStatusTypeDef]
    ServiceUpdates: NotRequired[List[PendingModifiedServiceUpdateTypeDef]]


class ClusterConfigurationTypeDef(TypedDict):
    Name: NotRequired[str]
    Description: NotRequired[str]
    NodeType: NotRequired[str]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    MaintenanceWindow: NotRequired[str]
    TopicArn: NotRequired[str]
    Port: NotRequired[int]
    ParameterGroupName: NotRequired[str]
    SubnetGroupName: NotRequired[str]
    VpcId: NotRequired[str]
    SnapshotRetentionLimit: NotRequired[int]
    SnapshotWindow: NotRequired[str]
    NumShards: NotRequired[int]
    Shards: NotRequired[List[ShardDetailTypeDef]]
    MultiRegionParameterGroupName: NotRequired[str]
    MultiRegionClusterName: NotRequired[str]


class CreateSubnetGroupResponseTypeDef(TypedDict):
    SubnetGroup: SubnetGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSubnetGroupResponseTypeDef(TypedDict):
    SubnetGroup: SubnetGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSubnetGroupsResponseTypeDef(TypedDict):
    SubnetGroups: List[SubnetGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateSubnetGroupResponseTypeDef(TypedDict):
    SubnetGroup: SubnetGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ClusterTypeDef(TypedDict):
    Name: NotRequired[str]
    Description: NotRequired[str]
    Status: NotRequired[str]
    PendingUpdates: NotRequired[ClusterPendingUpdatesTypeDef]
    MultiRegionClusterName: NotRequired[str]
    NumberOfShards: NotRequired[int]
    Shards: NotRequired[List[ShardTypeDef]]
    AvailabilityMode: NotRequired[AZStatusType]
    ClusterEndpoint: NotRequired[EndpointTypeDef]
    NodeType: NotRequired[str]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    EnginePatchVersion: NotRequired[str]
    ParameterGroupName: NotRequired[str]
    ParameterGroupStatus: NotRequired[str]
    SecurityGroups: NotRequired[List[SecurityGroupMembershipTypeDef]]
    SubnetGroupName: NotRequired[str]
    TLSEnabled: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    ARN: NotRequired[str]
    SnsTopicArn: NotRequired[str]
    SnsTopicStatus: NotRequired[str]
    SnapshotRetentionLimit: NotRequired[int]
    MaintenanceWindow: NotRequired[str]
    SnapshotWindow: NotRequired[str]
    ACLName: NotRequired[str]
    AutoMinorVersionUpgrade: NotRequired[bool]
    DataTiering: NotRequired[DataTieringStatusType]


class SnapshotTypeDef(TypedDict):
    Name: NotRequired[str]
    Status: NotRequired[str]
    Source: NotRequired[str]
    KmsKeyId: NotRequired[str]
    ARN: NotRequired[str]
    ClusterConfiguration: NotRequired[ClusterConfigurationTypeDef]
    DataTiering: NotRequired[DataTieringStatusType]


class BatchUpdateClusterResponseTypeDef(TypedDict):
    ProcessedClusters: List[ClusterTypeDef]
    UnprocessedClusters: List[UnprocessedClusterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateClusterResponseTypeDef(TypedDict):
    Cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteClusterResponseTypeDef(TypedDict):
    Cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeClustersResponseTypeDef(TypedDict):
    Clusters: List[ClusterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class FailoverShardResponseTypeDef(TypedDict):
    Cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateClusterResponseTypeDef(TypedDict):
    Cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CopySnapshotResponseTypeDef(TypedDict):
    Snapshot: SnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSnapshotResponseTypeDef(TypedDict):
    Snapshot: SnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSnapshotResponseTypeDef(TypedDict):
    Snapshot: SnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSnapshotsResponseTypeDef(TypedDict):
    Snapshots: List[SnapshotTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
