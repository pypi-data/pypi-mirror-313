"""
Type annotations for pcs service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/type_defs/)

Usage::

    ```python
    from mypy_boto3_pcs.type_defs import SlurmCustomSettingTypeDef

    data: SlurmCustomSettingTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ClusterStatusType,
    ComputeNodeGroupStatusType,
    EndpointTypeType,
    PurchaseOptionType,
    QueueStatusType,
    SizeType,
    SpotAllocationStrategyType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ClusterSlurmConfigurationRequestTypeDef",
    "ClusterSlurmConfigurationTypeDef",
    "ClusterSummaryTypeDef",
    "ClusterTypeDef",
    "ComputeNodeGroupConfigurationTypeDef",
    "ComputeNodeGroupSlurmConfigurationRequestTypeDef",
    "ComputeNodeGroupSlurmConfigurationTypeDef",
    "ComputeNodeGroupSummaryTypeDef",
    "ComputeNodeGroupTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "CreateClusterResponseTypeDef",
    "CreateComputeNodeGroupRequestRequestTypeDef",
    "CreateComputeNodeGroupResponseTypeDef",
    "CreateQueueRequestRequestTypeDef",
    "CreateQueueResponseTypeDef",
    "CustomLaunchTemplateTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteComputeNodeGroupRequestRequestTypeDef",
    "DeleteQueueRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EndpointTypeDef",
    "ErrorInfoTypeDef",
    "GetClusterRequestRequestTypeDef",
    "GetClusterResponseTypeDef",
    "GetComputeNodeGroupRequestRequestTypeDef",
    "GetComputeNodeGroupResponseTypeDef",
    "GetQueueRequestRequestTypeDef",
    "GetQueueResponseTypeDef",
    "InstanceConfigTypeDef",
    "ListClustersRequestListClustersPaginateTypeDef",
    "ListClustersRequestRequestTypeDef",
    "ListClustersResponseTypeDef",
    "ListComputeNodeGroupsRequestListComputeNodeGroupsPaginateTypeDef",
    "ListComputeNodeGroupsRequestRequestTypeDef",
    "ListComputeNodeGroupsResponseTypeDef",
    "ListQueuesRequestListQueuesPaginateTypeDef",
    "ListQueuesRequestRequestTypeDef",
    "ListQueuesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NetworkingRequestTypeDef",
    "NetworkingTypeDef",
    "PaginatorConfigTypeDef",
    "QueueSummaryTypeDef",
    "QueueTypeDef",
    "RegisterComputeNodeGroupInstanceRequestRequestTypeDef",
    "RegisterComputeNodeGroupInstanceResponseTypeDef",
    "ResponseMetadataTypeDef",
    "ScalingConfigurationRequestTypeDef",
    "ScalingConfigurationTypeDef",
    "SchedulerRequestTypeDef",
    "SchedulerTypeDef",
    "SlurmAuthKeyTypeDef",
    "SlurmCustomSettingTypeDef",
    "SpotOptionsTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateComputeNodeGroupRequestRequestTypeDef",
    "UpdateComputeNodeGroupResponseTypeDef",
    "UpdateComputeNodeGroupSlurmConfigurationRequestTypeDef",
    "UpdateQueueRequestRequestTypeDef",
    "UpdateQueueResponseTypeDef",
)


class SlurmCustomSettingTypeDef(TypedDict):
    parameterName: str
    parameterValue: str


class SlurmAuthKeyTypeDef(TypedDict):
    secretArn: str
    secretVersion: str


ClusterSummaryTypeDef = TypedDict(
    "ClusterSummaryTypeDef",
    {
        "name": str,
        "id": str,
        "arn": str,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "status": ClusterStatusType,
    },
)
EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "type": EndpointTypeType,
        "privateIpAddress": str,
        "port": str,
        "publicIpAddress": NotRequired[str],
    },
)


class ErrorInfoTypeDef(TypedDict):
    code: NotRequired[str]
    message: NotRequired[str]


class NetworkingTypeDef(TypedDict):
    subnetIds: NotRequired[List[str]]
    securityGroupIds: NotRequired[List[str]]


SchedulerTypeDef = TypedDict(
    "SchedulerTypeDef",
    {
        "type": Literal["SLURM"],
        "version": str,
    },
)


class ComputeNodeGroupConfigurationTypeDef(TypedDict):
    computeNodeGroupId: NotRequired[str]


ComputeNodeGroupSummaryTypeDef = TypedDict(
    "ComputeNodeGroupSummaryTypeDef",
    {
        "name": str,
        "id": str,
        "arn": str,
        "clusterId": str,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "status": ComputeNodeGroupStatusType,
    },
)
CustomLaunchTemplateTypeDef = TypedDict(
    "CustomLaunchTemplateTypeDef",
    {
        "id": str,
        "version": str,
    },
)


class InstanceConfigTypeDef(TypedDict):
    instanceType: NotRequired[str]


class ScalingConfigurationTypeDef(TypedDict):
    minInstanceCount: int
    maxInstanceCount: int


class SpotOptionsTypeDef(TypedDict):
    allocationStrategy: NotRequired[SpotAllocationStrategyType]


class NetworkingRequestTypeDef(TypedDict):
    subnetIds: NotRequired[Sequence[str]]
    securityGroupIds: NotRequired[Sequence[str]]


SchedulerRequestTypeDef = TypedDict(
    "SchedulerRequestTypeDef",
    {
        "type": Literal["SLURM"],
        "version": str,
    },
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class ScalingConfigurationRequestTypeDef(TypedDict):
    minInstanceCount: int
    maxInstanceCount: int


class DeleteClusterRequestRequestTypeDef(TypedDict):
    clusterIdentifier: str
    clientToken: NotRequired[str]


class DeleteComputeNodeGroupRequestRequestTypeDef(TypedDict):
    clusterIdentifier: str
    computeNodeGroupIdentifier: str
    clientToken: NotRequired[str]


class DeleteQueueRequestRequestTypeDef(TypedDict):
    clusterIdentifier: str
    queueIdentifier: str
    clientToken: NotRequired[str]


class GetClusterRequestRequestTypeDef(TypedDict):
    clusterIdentifier: str


class GetComputeNodeGroupRequestRequestTypeDef(TypedDict):
    clusterIdentifier: str
    computeNodeGroupIdentifier: str


class GetQueueRequestRequestTypeDef(TypedDict):
    clusterIdentifier: str
    queueIdentifier: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListClustersRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListComputeNodeGroupsRequestRequestTypeDef(TypedDict):
    clusterIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListQueuesRequestRequestTypeDef(TypedDict):
    clusterIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


QueueSummaryTypeDef = TypedDict(
    "QueueSummaryTypeDef",
    {
        "name": str,
        "id": str,
        "arn": str,
        "clusterId": str,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "status": QueueStatusType,
    },
)


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class RegisterComputeNodeGroupInstanceRequestRequestTypeDef(TypedDict):
    clusterIdentifier: str
    bootstrapId: str


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class ClusterSlurmConfigurationRequestTypeDef(TypedDict):
    scaleDownIdleTimeInSeconds: NotRequired[int]
    slurmCustomSettings: NotRequired[Sequence[SlurmCustomSettingTypeDef]]


class ComputeNodeGroupSlurmConfigurationRequestTypeDef(TypedDict):
    slurmCustomSettings: NotRequired[Sequence[SlurmCustomSettingTypeDef]]


class ComputeNodeGroupSlurmConfigurationTypeDef(TypedDict):
    slurmCustomSettings: NotRequired[List[SlurmCustomSettingTypeDef]]


class UpdateComputeNodeGroupSlurmConfigurationRequestTypeDef(TypedDict):
    slurmCustomSettings: NotRequired[Sequence[SlurmCustomSettingTypeDef]]


class ClusterSlurmConfigurationTypeDef(TypedDict):
    scaleDownIdleTimeInSeconds: NotRequired[int]
    slurmCustomSettings: NotRequired[List[SlurmCustomSettingTypeDef]]
    authKey: NotRequired[SlurmAuthKeyTypeDef]


class CreateQueueRequestRequestTypeDef(TypedDict):
    clusterIdentifier: str
    queueName: str
    computeNodeGroupConfigurations: NotRequired[Sequence[ComputeNodeGroupConfigurationTypeDef]]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


QueueTypeDef = TypedDict(
    "QueueTypeDef",
    {
        "name": str,
        "id": str,
        "arn": str,
        "clusterId": str,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "status": QueueStatusType,
        "computeNodeGroupConfigurations": List[ComputeNodeGroupConfigurationTypeDef],
        "errorInfo": NotRequired[List[ErrorInfoTypeDef]],
    },
)


class UpdateQueueRequestRequestTypeDef(TypedDict):
    clusterIdentifier: str
    queueIdentifier: str
    computeNodeGroupConfigurations: NotRequired[Sequence[ComputeNodeGroupConfigurationTypeDef]]
    clientToken: NotRequired[str]


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ListClustersResponseTypeDef(TypedDict):
    clusters: List[ClusterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListComputeNodeGroupsResponseTypeDef(TypedDict):
    computeNodeGroups: List[ComputeNodeGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterComputeNodeGroupInstanceResponseTypeDef(TypedDict):
    nodeID: str
    sharedSecret: str
    endpoints: List[EndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListClustersRequestListClustersPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListComputeNodeGroupsRequestListComputeNodeGroupsPaginateTypeDef(TypedDict):
    clusterIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListQueuesRequestListQueuesPaginateTypeDef(TypedDict):
    clusterIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListQueuesResponseTypeDef(TypedDict):
    queues: List[QueueSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateClusterRequestRequestTypeDef(TypedDict):
    clusterName: str
    scheduler: SchedulerRequestTypeDef
    size: SizeType
    networking: NetworkingRequestTypeDef
    slurmConfiguration: NotRequired[ClusterSlurmConfigurationRequestTypeDef]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class CreateComputeNodeGroupRequestRequestTypeDef(TypedDict):
    clusterIdentifier: str
    computeNodeGroupName: str
    subnetIds: Sequence[str]
    customLaunchTemplate: CustomLaunchTemplateTypeDef
    iamInstanceProfileArn: str
    scalingConfiguration: ScalingConfigurationRequestTypeDef
    instanceConfigs: Sequence[InstanceConfigTypeDef]
    amiId: NotRequired[str]
    purchaseOption: NotRequired[PurchaseOptionType]
    spotOptions: NotRequired[SpotOptionsTypeDef]
    slurmConfiguration: NotRequired[ComputeNodeGroupSlurmConfigurationRequestTypeDef]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


ComputeNodeGroupTypeDef = TypedDict(
    "ComputeNodeGroupTypeDef",
    {
        "name": str,
        "id": str,
        "arn": str,
        "clusterId": str,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "status": ComputeNodeGroupStatusType,
        "subnetIds": List[str],
        "customLaunchTemplate": CustomLaunchTemplateTypeDef,
        "iamInstanceProfileArn": str,
        "scalingConfiguration": ScalingConfigurationTypeDef,
        "instanceConfigs": List[InstanceConfigTypeDef],
        "amiId": NotRequired[str],
        "purchaseOption": NotRequired[PurchaseOptionType],
        "spotOptions": NotRequired[SpotOptionsTypeDef],
        "slurmConfiguration": NotRequired[ComputeNodeGroupSlurmConfigurationTypeDef],
        "errorInfo": NotRequired[List[ErrorInfoTypeDef]],
    },
)


class UpdateComputeNodeGroupRequestRequestTypeDef(TypedDict):
    clusterIdentifier: str
    computeNodeGroupIdentifier: str
    amiId: NotRequired[str]
    subnetIds: NotRequired[Sequence[str]]
    customLaunchTemplate: NotRequired[CustomLaunchTemplateTypeDef]
    purchaseOption: NotRequired[PurchaseOptionType]
    spotOptions: NotRequired[SpotOptionsTypeDef]
    scalingConfiguration: NotRequired[ScalingConfigurationRequestTypeDef]
    iamInstanceProfileArn: NotRequired[str]
    slurmConfiguration: NotRequired[UpdateComputeNodeGroupSlurmConfigurationRequestTypeDef]
    clientToken: NotRequired[str]


ClusterTypeDef = TypedDict(
    "ClusterTypeDef",
    {
        "name": str,
        "id": str,
        "arn": str,
        "status": ClusterStatusType,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "scheduler": SchedulerTypeDef,
        "size": SizeType,
        "networking": NetworkingTypeDef,
        "slurmConfiguration": NotRequired[ClusterSlurmConfigurationTypeDef],
        "endpoints": NotRequired[List[EndpointTypeDef]],
        "errorInfo": NotRequired[List[ErrorInfoTypeDef]],
    },
)


class CreateQueueResponseTypeDef(TypedDict):
    queue: QueueTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetQueueResponseTypeDef(TypedDict):
    queue: QueueTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateQueueResponseTypeDef(TypedDict):
    queue: QueueTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateComputeNodeGroupResponseTypeDef(TypedDict):
    computeNodeGroup: ComputeNodeGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetComputeNodeGroupResponseTypeDef(TypedDict):
    computeNodeGroup: ComputeNodeGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateComputeNodeGroupResponseTypeDef(TypedDict):
    computeNodeGroup: ComputeNodeGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateClusterResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetClusterResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
