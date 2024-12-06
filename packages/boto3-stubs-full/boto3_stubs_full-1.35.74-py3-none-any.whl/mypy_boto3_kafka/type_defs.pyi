"""
Type annotations for kafka service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/type_defs/)

Usage::

    ```python
    from mypy_boto3_kafka.type_defs import AmazonMskClusterTypeDef

    data: AmazonMskClusterTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ClientBrokerType,
    ClusterStateType,
    ClusterTypeType,
    ConfigurationStateType,
    CustomerActionStatusType,
    EnhancedMonitoringType,
    KafkaVersionStatusType,
    ReplicationStartingPositionTypeType,
    ReplicationTopicNameConfigurationTypeType,
    ReplicatorStateType,
    StorageModeType,
    TargetCompressionTypeType,
    UserIdentityTypeType,
    VpcConnectionStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AmazonMskClusterTypeDef",
    "BatchAssociateScramSecretRequestRequestTypeDef",
    "BatchAssociateScramSecretResponseTypeDef",
    "BatchDisassociateScramSecretRequestRequestTypeDef",
    "BatchDisassociateScramSecretResponseTypeDef",
    "BlobTypeDef",
    "BrokerCountUpdateInfoTypeDef",
    "BrokerEBSVolumeInfoTypeDef",
    "BrokerLogsTypeDef",
    "BrokerNodeGroupInfoOutputTypeDef",
    "BrokerNodeGroupInfoTypeDef",
    "BrokerNodeGroupInfoUnionTypeDef",
    "BrokerNodeInfoTypeDef",
    "BrokerSoftwareInfoTypeDef",
    "ClientAuthenticationOutputTypeDef",
    "ClientAuthenticationTypeDef",
    "ClientAuthenticationUnionTypeDef",
    "ClientVpcConnectionTypeDef",
    "CloudWatchLogsTypeDef",
    "ClusterInfoTypeDef",
    "ClusterOperationInfoTypeDef",
    "ClusterOperationStepInfoTypeDef",
    "ClusterOperationStepTypeDef",
    "ClusterOperationV2ProvisionedTypeDef",
    "ClusterOperationV2ServerlessTypeDef",
    "ClusterOperationV2SummaryTypeDef",
    "ClusterOperationV2TypeDef",
    "ClusterTypeDef",
    "CompatibleKafkaVersionTypeDef",
    "ConfigurationInfoTypeDef",
    "ConfigurationRevisionTypeDef",
    "ConfigurationTypeDef",
    "ConnectivityInfoTypeDef",
    "ConsumerGroupReplicationOutputTypeDef",
    "ConsumerGroupReplicationTypeDef",
    "ConsumerGroupReplicationUnionTypeDef",
    "ConsumerGroupReplicationUpdateTypeDef",
    "ControllerNodeInfoTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "CreateClusterResponseTypeDef",
    "CreateClusterV2RequestRequestTypeDef",
    "CreateClusterV2ResponseTypeDef",
    "CreateConfigurationRequestRequestTypeDef",
    "CreateConfigurationResponseTypeDef",
    "CreateReplicatorRequestRequestTypeDef",
    "CreateReplicatorResponseTypeDef",
    "CreateVpcConnectionRequestRequestTypeDef",
    "CreateVpcConnectionResponseTypeDef",
    "DeleteClusterPolicyRequestRequestTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteClusterResponseTypeDef",
    "DeleteConfigurationRequestRequestTypeDef",
    "DeleteConfigurationResponseTypeDef",
    "DeleteReplicatorRequestRequestTypeDef",
    "DeleteReplicatorResponseTypeDef",
    "DeleteVpcConnectionRequestRequestTypeDef",
    "DeleteVpcConnectionResponseTypeDef",
    "DescribeClusterOperationRequestRequestTypeDef",
    "DescribeClusterOperationResponseTypeDef",
    "DescribeClusterOperationV2RequestRequestTypeDef",
    "DescribeClusterOperationV2ResponseTypeDef",
    "DescribeClusterRequestRequestTypeDef",
    "DescribeClusterResponseTypeDef",
    "DescribeClusterV2RequestRequestTypeDef",
    "DescribeClusterV2ResponseTypeDef",
    "DescribeConfigurationRequestRequestTypeDef",
    "DescribeConfigurationResponseTypeDef",
    "DescribeConfigurationRevisionRequestRequestTypeDef",
    "DescribeConfigurationRevisionResponseTypeDef",
    "DescribeReplicatorRequestRequestTypeDef",
    "DescribeReplicatorResponseTypeDef",
    "DescribeVpcConnectionRequestRequestTypeDef",
    "DescribeVpcConnectionResponseTypeDef",
    "EBSStorageInfoTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionAtRestTypeDef",
    "EncryptionInTransitTypeDef",
    "EncryptionInfoTypeDef",
    "ErrorInfoTypeDef",
    "FirehoseTypeDef",
    "GetBootstrapBrokersRequestRequestTypeDef",
    "GetBootstrapBrokersResponseTypeDef",
    "GetClusterPolicyRequestRequestTypeDef",
    "GetClusterPolicyResponseTypeDef",
    "GetCompatibleKafkaVersionsRequestRequestTypeDef",
    "GetCompatibleKafkaVersionsResponseTypeDef",
    "IamTypeDef",
    "JmxExporterInfoTypeDef",
    "JmxExporterTypeDef",
    "KafkaClusterClientVpcConfigOutputTypeDef",
    "KafkaClusterClientVpcConfigTypeDef",
    "KafkaClusterClientVpcConfigUnionTypeDef",
    "KafkaClusterDescriptionTypeDef",
    "KafkaClusterSummaryTypeDef",
    "KafkaClusterTypeDef",
    "KafkaVersionTypeDef",
    "ListClientVpcConnectionsRequestListClientVpcConnectionsPaginateTypeDef",
    "ListClientVpcConnectionsRequestRequestTypeDef",
    "ListClientVpcConnectionsResponseTypeDef",
    "ListClusterOperationsRequestListClusterOperationsPaginateTypeDef",
    "ListClusterOperationsRequestRequestTypeDef",
    "ListClusterOperationsResponseTypeDef",
    "ListClusterOperationsV2RequestListClusterOperationsV2PaginateTypeDef",
    "ListClusterOperationsV2RequestRequestTypeDef",
    "ListClusterOperationsV2ResponseTypeDef",
    "ListClustersRequestListClustersPaginateTypeDef",
    "ListClustersRequestRequestTypeDef",
    "ListClustersResponseTypeDef",
    "ListClustersV2RequestListClustersV2PaginateTypeDef",
    "ListClustersV2RequestRequestTypeDef",
    "ListClustersV2ResponseTypeDef",
    "ListConfigurationRevisionsRequestListConfigurationRevisionsPaginateTypeDef",
    "ListConfigurationRevisionsRequestRequestTypeDef",
    "ListConfigurationRevisionsResponseTypeDef",
    "ListConfigurationsRequestListConfigurationsPaginateTypeDef",
    "ListConfigurationsRequestRequestTypeDef",
    "ListConfigurationsResponseTypeDef",
    "ListKafkaVersionsRequestListKafkaVersionsPaginateTypeDef",
    "ListKafkaVersionsRequestRequestTypeDef",
    "ListKafkaVersionsResponseTypeDef",
    "ListNodesRequestListNodesPaginateTypeDef",
    "ListNodesRequestRequestTypeDef",
    "ListNodesResponseTypeDef",
    "ListReplicatorsRequestListReplicatorsPaginateTypeDef",
    "ListReplicatorsRequestRequestTypeDef",
    "ListReplicatorsResponseTypeDef",
    "ListScramSecretsRequestListScramSecretsPaginateTypeDef",
    "ListScramSecretsRequestRequestTypeDef",
    "ListScramSecretsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListVpcConnectionsRequestListVpcConnectionsPaginateTypeDef",
    "ListVpcConnectionsRequestRequestTypeDef",
    "ListVpcConnectionsResponseTypeDef",
    "LoggingInfoTypeDef",
    "MutableClusterInfoTypeDef",
    "NodeExporterInfoTypeDef",
    "NodeExporterTypeDef",
    "NodeInfoTypeDef",
    "OpenMonitoringInfoTypeDef",
    "OpenMonitoringTypeDef",
    "PaginatorConfigTypeDef",
    "PrometheusInfoTypeDef",
    "PrometheusTypeDef",
    "ProvisionedRequestTypeDef",
    "ProvisionedThroughputTypeDef",
    "ProvisionedTypeDef",
    "PublicAccessTypeDef",
    "PutClusterPolicyRequestRequestTypeDef",
    "PutClusterPolicyResponseTypeDef",
    "RebootBrokerRequestRequestTypeDef",
    "RebootBrokerResponseTypeDef",
    "RejectClientVpcConnectionRequestRequestTypeDef",
    "ReplicationInfoDescriptionTypeDef",
    "ReplicationInfoSummaryTypeDef",
    "ReplicationInfoTypeDef",
    "ReplicationStartingPositionTypeDef",
    "ReplicationStateInfoTypeDef",
    "ReplicationTopicNameConfigurationTypeDef",
    "ReplicatorSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "S3TypeDef",
    "SaslTypeDef",
    "ScramTypeDef",
    "ServerlessClientAuthenticationTypeDef",
    "ServerlessRequestTypeDef",
    "ServerlessSaslTypeDef",
    "ServerlessTypeDef",
    "StateInfoTypeDef",
    "StorageInfoTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TlsOutputTypeDef",
    "TlsTypeDef",
    "TlsUnionTypeDef",
    "TopicReplicationOutputTypeDef",
    "TopicReplicationTypeDef",
    "TopicReplicationUnionTypeDef",
    "TopicReplicationUpdateTypeDef",
    "UnauthenticatedTypeDef",
    "UnprocessedScramSecretTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateBrokerCountRequestRequestTypeDef",
    "UpdateBrokerCountResponseTypeDef",
    "UpdateBrokerStorageRequestRequestTypeDef",
    "UpdateBrokerStorageResponseTypeDef",
    "UpdateBrokerTypeRequestRequestTypeDef",
    "UpdateBrokerTypeResponseTypeDef",
    "UpdateClusterConfigurationRequestRequestTypeDef",
    "UpdateClusterConfigurationResponseTypeDef",
    "UpdateClusterKafkaVersionRequestRequestTypeDef",
    "UpdateClusterKafkaVersionResponseTypeDef",
    "UpdateConfigurationRequestRequestTypeDef",
    "UpdateConfigurationResponseTypeDef",
    "UpdateConnectivityRequestRequestTypeDef",
    "UpdateConnectivityResponseTypeDef",
    "UpdateMonitoringRequestRequestTypeDef",
    "UpdateMonitoringResponseTypeDef",
    "UpdateReplicationInfoRequestRequestTypeDef",
    "UpdateReplicationInfoResponseTypeDef",
    "UpdateSecurityRequestRequestTypeDef",
    "UpdateSecurityResponseTypeDef",
    "UpdateStorageRequestRequestTypeDef",
    "UpdateStorageResponseTypeDef",
    "UserIdentityTypeDef",
    "VpcConfigOutputTypeDef",
    "VpcConfigTypeDef",
    "VpcConfigUnionTypeDef",
    "VpcConnectionInfoServerlessTypeDef",
    "VpcConnectionInfoTypeDef",
    "VpcConnectionTypeDef",
    "VpcConnectivityClientAuthenticationTypeDef",
    "VpcConnectivityIamTypeDef",
    "VpcConnectivitySaslTypeDef",
    "VpcConnectivityScramTypeDef",
    "VpcConnectivityTlsTypeDef",
    "VpcConnectivityTypeDef",
    "ZookeeperNodeInfoTypeDef",
)

class AmazonMskClusterTypeDef(TypedDict):
    MskClusterArn: str

class BatchAssociateScramSecretRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    SecretArnList: Sequence[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class UnprocessedScramSecretTypeDef(TypedDict):
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]
    SecretArn: NotRequired[str]

class BatchDisassociateScramSecretRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    SecretArnList: Sequence[str]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class BrokerCountUpdateInfoTypeDef(TypedDict):
    CreatedBrokerIds: NotRequired[List[float]]
    DeletedBrokerIds: NotRequired[List[float]]

class ProvisionedThroughputTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    VolumeThroughput: NotRequired[int]

class CloudWatchLogsTypeDef(TypedDict):
    Enabled: bool
    LogGroup: NotRequired[str]

class FirehoseTypeDef(TypedDict):
    Enabled: bool
    DeliveryStream: NotRequired[str]

class S3TypeDef(TypedDict):
    Enabled: bool
    Bucket: NotRequired[str]
    Prefix: NotRequired[str]

class BrokerSoftwareInfoTypeDef(TypedDict):
    ConfigurationArn: NotRequired[str]
    ConfigurationRevision: NotRequired[int]
    KafkaVersion: NotRequired[str]

class TlsOutputTypeDef(TypedDict):
    CertificateAuthorityArnList: NotRequired[List[str]]
    Enabled: NotRequired[bool]

class UnauthenticatedTypeDef(TypedDict):
    Enabled: NotRequired[bool]

class ClientVpcConnectionTypeDef(TypedDict):
    VpcConnectionArn: str
    Authentication: NotRequired[str]
    CreationTime: NotRequired[datetime]
    State: NotRequired[VpcConnectionStateType]
    Owner: NotRequired[str]

class StateInfoTypeDef(TypedDict):
    Code: NotRequired[str]
    Message: NotRequired[str]

class ErrorInfoTypeDef(TypedDict):
    ErrorCode: NotRequired[str]
    ErrorString: NotRequired[str]

class ClusterOperationStepInfoTypeDef(TypedDict):
    StepStatus: NotRequired[str]

class ClusterOperationV2SummaryTypeDef(TypedDict):
    ClusterArn: NotRequired[str]
    ClusterType: NotRequired[ClusterTypeType]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    OperationArn: NotRequired[str]
    OperationState: NotRequired[str]
    OperationType: NotRequired[str]

class CompatibleKafkaVersionTypeDef(TypedDict):
    SourceVersion: NotRequired[str]
    TargetVersions: NotRequired[List[str]]

class ConfigurationInfoTypeDef(TypedDict):
    Arn: str
    Revision: int

class ConfigurationRevisionTypeDef(TypedDict):
    CreationTime: datetime
    Revision: int
    Description: NotRequired[str]

PublicAccessTypeDef = TypedDict(
    "PublicAccessTypeDef",
    {
        "Type": NotRequired[str],
    },
)

class ConsumerGroupReplicationOutputTypeDef(TypedDict):
    ConsumerGroupsToReplicate: List[str]
    ConsumerGroupsToExclude: NotRequired[List[str]]
    DetectAndCopyNewConsumerGroups: NotRequired[bool]
    SynchroniseConsumerGroupOffsets: NotRequired[bool]

class ConsumerGroupReplicationTypeDef(TypedDict):
    ConsumerGroupsToReplicate: Sequence[str]
    ConsumerGroupsToExclude: NotRequired[Sequence[str]]
    DetectAndCopyNewConsumerGroups: NotRequired[bool]
    SynchroniseConsumerGroupOffsets: NotRequired[bool]

class ConsumerGroupReplicationUpdateTypeDef(TypedDict):
    ConsumerGroupsToExclude: Sequence[str]
    ConsumerGroupsToReplicate: Sequence[str]
    DetectAndCopyNewConsumerGroups: bool
    SynchroniseConsumerGroupOffsets: bool

class ControllerNodeInfoTypeDef(TypedDict):
    Endpoints: NotRequired[List[str]]

class CreateVpcConnectionRequestRequestTypeDef(TypedDict):
    TargetClusterArn: str
    Authentication: str
    VpcId: str
    ClientSubnets: Sequence[str]
    SecurityGroups: Sequence[str]
    Tags: NotRequired[Mapping[str, str]]

class DeleteClusterPolicyRequestRequestTypeDef(TypedDict):
    ClusterArn: str

class DeleteClusterRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: NotRequired[str]

class DeleteConfigurationRequestRequestTypeDef(TypedDict):
    Arn: str

class DeleteReplicatorRequestRequestTypeDef(TypedDict):
    ReplicatorArn: str
    CurrentVersion: NotRequired[str]

class DeleteVpcConnectionRequestRequestTypeDef(TypedDict):
    Arn: str

class DescribeClusterOperationRequestRequestTypeDef(TypedDict):
    ClusterOperationArn: str

class DescribeClusterOperationV2RequestRequestTypeDef(TypedDict):
    ClusterOperationArn: str

class DescribeClusterRequestRequestTypeDef(TypedDict):
    ClusterArn: str

class DescribeClusterV2RequestRequestTypeDef(TypedDict):
    ClusterArn: str

class DescribeConfigurationRequestRequestTypeDef(TypedDict):
    Arn: str

class DescribeConfigurationRevisionRequestRequestTypeDef(TypedDict):
    Arn: str
    Revision: int

class DescribeReplicatorRequestRequestTypeDef(TypedDict):
    ReplicatorArn: str

class ReplicationStateInfoTypeDef(TypedDict):
    Code: NotRequired[str]
    Message: NotRequired[str]

class DescribeVpcConnectionRequestRequestTypeDef(TypedDict):
    Arn: str

class EncryptionAtRestTypeDef(TypedDict):
    DataVolumeKMSKeyId: str

class EncryptionInTransitTypeDef(TypedDict):
    ClientBroker: NotRequired[ClientBrokerType]
    InCluster: NotRequired[bool]

class GetBootstrapBrokersRequestRequestTypeDef(TypedDict):
    ClusterArn: str

class GetClusterPolicyRequestRequestTypeDef(TypedDict):
    ClusterArn: str

class GetCompatibleKafkaVersionsRequestRequestTypeDef(TypedDict):
    ClusterArn: NotRequired[str]

class IamTypeDef(TypedDict):
    Enabled: NotRequired[bool]

class JmxExporterInfoTypeDef(TypedDict):
    EnabledInBroker: bool

class JmxExporterTypeDef(TypedDict):
    EnabledInBroker: bool

class KafkaClusterClientVpcConfigOutputTypeDef(TypedDict):
    SubnetIds: List[str]
    SecurityGroupIds: NotRequired[List[str]]

class KafkaClusterClientVpcConfigTypeDef(TypedDict):
    SubnetIds: Sequence[str]
    SecurityGroupIds: NotRequired[Sequence[str]]

class KafkaVersionTypeDef(TypedDict):
    Version: NotRequired[str]
    Status: NotRequired[KafkaVersionStatusType]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListClientVpcConnectionsRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListClusterOperationsRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListClusterOperationsV2RequestRequestTypeDef(TypedDict):
    ClusterArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListClustersRequestRequestTypeDef(TypedDict):
    ClusterNameFilter: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListClustersV2RequestRequestTypeDef(TypedDict):
    ClusterNameFilter: NotRequired[str]
    ClusterTypeFilter: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListConfigurationRevisionsRequestRequestTypeDef(TypedDict):
    Arn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListConfigurationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListKafkaVersionsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListNodesRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListReplicatorsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ReplicatorNameFilter: NotRequired[str]

class ListScramSecretsRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class ListVpcConnectionsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class VpcConnectionTypeDef(TypedDict):
    VpcConnectionArn: str
    TargetClusterArn: str
    CreationTime: NotRequired[datetime]
    Authentication: NotRequired[str]
    VpcId: NotRequired[str]
    State: NotRequired[VpcConnectionStateType]

class NodeExporterInfoTypeDef(TypedDict):
    EnabledInBroker: bool

class NodeExporterTypeDef(TypedDict):
    EnabledInBroker: bool

class ZookeeperNodeInfoTypeDef(TypedDict):
    AttachedENIId: NotRequired[str]
    ClientVpcIpAddress: NotRequired[str]
    Endpoints: NotRequired[List[str]]
    ZookeeperId: NotRequired[float]
    ZookeeperVersion: NotRequired[str]

class PutClusterPolicyRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    Policy: str
    CurrentVersion: NotRequired[str]

class RebootBrokerRequestRequestTypeDef(TypedDict):
    BrokerIds: Sequence[str]
    ClusterArn: str

class RejectClientVpcConnectionRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    VpcConnectionArn: str

class ReplicationInfoSummaryTypeDef(TypedDict):
    SourceKafkaClusterAlias: NotRequired[str]
    TargetKafkaClusterAlias: NotRequired[str]

ReplicationStartingPositionTypeDef = TypedDict(
    "ReplicationStartingPositionTypeDef",
    {
        "Type": NotRequired[ReplicationStartingPositionTypeType],
    },
)
ReplicationTopicNameConfigurationTypeDef = TypedDict(
    "ReplicationTopicNameConfigurationTypeDef",
    {
        "Type": NotRequired[ReplicationTopicNameConfigurationTypeType],
    },
)

class ScramTypeDef(TypedDict):
    Enabled: NotRequired[bool]

class VpcConfigOutputTypeDef(TypedDict):
    SubnetIds: List[str]
    SecurityGroupIds: NotRequired[List[str]]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class TlsTypeDef(TypedDict):
    CertificateAuthorityArnList: NotRequired[Sequence[str]]
    Enabled: NotRequired[bool]

class TopicReplicationUpdateTypeDef(TypedDict):
    CopyAccessControlListsForTopics: bool
    CopyTopicConfigurations: bool
    DetectAndCopyNewTopics: bool
    TopicsToExclude: Sequence[str]
    TopicsToReplicate: Sequence[str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateBrokerCountRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: str
    TargetNumberOfBrokerNodes: int

class UpdateBrokerTypeRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: str
    TargetInstanceType: str

UserIdentityTypeDef = TypedDict(
    "UserIdentityTypeDef",
    {
        "Type": NotRequired[UserIdentityTypeType],
        "PrincipalId": NotRequired[str],
    },
)

class VpcConfigTypeDef(TypedDict):
    SubnetIds: Sequence[str]
    SecurityGroupIds: NotRequired[Sequence[str]]

class VpcConnectivityTlsTypeDef(TypedDict):
    Enabled: NotRequired[bool]

class VpcConnectivityIamTypeDef(TypedDict):
    Enabled: NotRequired[bool]

class VpcConnectivityScramTypeDef(TypedDict):
    Enabled: NotRequired[bool]

class KafkaClusterSummaryTypeDef(TypedDict):
    AmazonMskCluster: NotRequired[AmazonMskClusterTypeDef]
    KafkaClusterAlias: NotRequired[str]

class CreateClusterResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterName: str
    State: ClusterStateType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateClusterV2ResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterName: str
    State: ClusterStateType
    ClusterType: ClusterTypeType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateReplicatorResponseTypeDef(TypedDict):
    ReplicatorArn: str
    ReplicatorName: str
    ReplicatorState: ReplicatorStateType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateVpcConnectionResponseTypeDef(TypedDict):
    VpcConnectionArn: str
    State: VpcConnectionStateType
    Authentication: str
    VpcId: str
    ClientSubnets: List[str]
    SecurityGroups: List[str]
    CreationTime: datetime
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteClusterResponseTypeDef(TypedDict):
    ClusterArn: str
    State: ClusterStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteConfigurationResponseTypeDef(TypedDict):
    Arn: str
    State: ConfigurationStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteReplicatorResponseTypeDef(TypedDict):
    ReplicatorArn: str
    ReplicatorState: ReplicatorStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteVpcConnectionResponseTypeDef(TypedDict):
    VpcConnectionArn: str
    State: VpcConnectionStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeConfigurationRevisionResponseTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    Description: str
    Revision: int
    ServerProperties: bytes
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeVpcConnectionResponseTypeDef(TypedDict):
    VpcConnectionArn: str
    TargetClusterArn: str
    State: VpcConnectionStateType
    Authentication: str
    VpcId: str
    Subnets: List[str]
    SecurityGroups: List[str]
    CreationTime: datetime
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetBootstrapBrokersResponseTypeDef(TypedDict):
    BootstrapBrokerString: str
    BootstrapBrokerStringTls: str
    BootstrapBrokerStringSaslScram: str
    BootstrapBrokerStringSaslIam: str
    BootstrapBrokerStringPublicTls: str
    BootstrapBrokerStringPublicSaslScram: str
    BootstrapBrokerStringPublicSaslIam: str
    BootstrapBrokerStringVpcConnectivityTls: str
    BootstrapBrokerStringVpcConnectivitySaslScram: str
    BootstrapBrokerStringVpcConnectivitySaslIam: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetClusterPolicyResponseTypeDef(TypedDict):
    CurrentVersion: str
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListScramSecretsResponseTypeDef(TypedDict):
    SecretArnList: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PutClusterPolicyResponseTypeDef(TypedDict):
    CurrentVersion: str
    ResponseMetadata: ResponseMetadataTypeDef

class RebootBrokerResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBrokerCountResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBrokerStorageResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBrokerTypeResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateClusterConfigurationResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateClusterKafkaVersionResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateConnectivityResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateMonitoringResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateReplicationInfoResponseTypeDef(TypedDict):
    ReplicatorArn: str
    ReplicatorState: ReplicatorStateType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSecurityResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateStorageResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class BatchAssociateScramSecretResponseTypeDef(TypedDict):
    ClusterArn: str
    UnprocessedScramSecrets: List[UnprocessedScramSecretTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDisassociateScramSecretResponseTypeDef(TypedDict):
    ClusterArn: str
    UnprocessedScramSecrets: List[UnprocessedScramSecretTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateConfigurationRequestRequestTypeDef(TypedDict):
    Name: str
    ServerProperties: BlobTypeDef
    Description: NotRequired[str]
    KafkaVersions: NotRequired[Sequence[str]]

class UpdateConfigurationRequestRequestTypeDef(TypedDict):
    Arn: str
    ServerProperties: BlobTypeDef
    Description: NotRequired[str]

class BrokerEBSVolumeInfoTypeDef(TypedDict):
    KafkaBrokerNodeId: str
    ProvisionedThroughput: NotRequired[ProvisionedThroughputTypeDef]
    VolumeSizeGB: NotRequired[int]

class EBSStorageInfoTypeDef(TypedDict):
    ProvisionedThroughput: NotRequired[ProvisionedThroughputTypeDef]
    VolumeSize: NotRequired[int]

class UpdateStorageRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: str
    ProvisionedThroughput: NotRequired[ProvisionedThroughputTypeDef]
    StorageMode: NotRequired[StorageModeType]
    VolumeSizeGB: NotRequired[int]

class BrokerLogsTypeDef(TypedDict):
    CloudWatchLogs: NotRequired[CloudWatchLogsTypeDef]
    Firehose: NotRequired[FirehoseTypeDef]
    S3: NotRequired[S3TypeDef]

class BrokerNodeInfoTypeDef(TypedDict):
    AttachedENIId: NotRequired[str]
    BrokerId: NotRequired[float]
    ClientSubnet: NotRequired[str]
    ClientVpcIpAddress: NotRequired[str]
    CurrentBrokerSoftwareInfo: NotRequired[BrokerSoftwareInfoTypeDef]
    Endpoints: NotRequired[List[str]]

class ListClientVpcConnectionsResponseTypeDef(TypedDict):
    ClientVpcConnections: List[ClientVpcConnectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ClusterOperationStepTypeDef(TypedDict):
    StepInfo: NotRequired[ClusterOperationStepInfoTypeDef]
    StepName: NotRequired[str]

class ListClusterOperationsV2ResponseTypeDef(TypedDict):
    ClusterOperationInfoList: List[ClusterOperationV2SummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetCompatibleKafkaVersionsResponseTypeDef(TypedDict):
    CompatibleKafkaVersions: List[CompatibleKafkaVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateClusterConfigurationRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    ConfigurationInfo: ConfigurationInfoTypeDef
    CurrentVersion: str

class UpdateClusterKafkaVersionRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: str
    TargetKafkaVersion: str
    ConfigurationInfo: NotRequired[ConfigurationInfoTypeDef]

class ConfigurationTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    Description: str
    KafkaVersions: List[str]
    LatestRevision: ConfigurationRevisionTypeDef
    Name: str
    State: ConfigurationStateType

class CreateConfigurationResponseTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    LatestRevision: ConfigurationRevisionTypeDef
    Name: str
    State: ConfigurationStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeConfigurationResponseTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    Description: str
    KafkaVersions: List[str]
    LatestRevision: ConfigurationRevisionTypeDef
    Name: str
    State: ConfigurationStateType
    ResponseMetadata: ResponseMetadataTypeDef

class ListConfigurationRevisionsResponseTypeDef(TypedDict):
    Revisions: List[ConfigurationRevisionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateConfigurationResponseTypeDef(TypedDict):
    Arn: str
    LatestRevision: ConfigurationRevisionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ConsumerGroupReplicationUnionTypeDef = Union[
    ConsumerGroupReplicationTypeDef, ConsumerGroupReplicationOutputTypeDef
]

class EncryptionInfoTypeDef(TypedDict):
    EncryptionAtRest: NotRequired[EncryptionAtRestTypeDef]
    EncryptionInTransit: NotRequired[EncryptionInTransitTypeDef]

class ServerlessSaslTypeDef(TypedDict):
    Iam: NotRequired[IamTypeDef]

class KafkaClusterDescriptionTypeDef(TypedDict):
    AmazonMskCluster: NotRequired[AmazonMskClusterTypeDef]
    KafkaClusterAlias: NotRequired[str]
    VpcConfig: NotRequired[KafkaClusterClientVpcConfigOutputTypeDef]

KafkaClusterClientVpcConfigUnionTypeDef = Union[
    KafkaClusterClientVpcConfigTypeDef, KafkaClusterClientVpcConfigOutputTypeDef
]

class ListKafkaVersionsResponseTypeDef(TypedDict):
    KafkaVersions: List[KafkaVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListClientVpcConnectionsRequestListClientVpcConnectionsPaginateTypeDef(TypedDict):
    ClusterArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListClusterOperationsRequestListClusterOperationsPaginateTypeDef(TypedDict):
    ClusterArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListClusterOperationsV2RequestListClusterOperationsV2PaginateTypeDef(TypedDict):
    ClusterArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListClustersRequestListClustersPaginateTypeDef(TypedDict):
    ClusterNameFilter: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListClustersV2RequestListClustersV2PaginateTypeDef(TypedDict):
    ClusterNameFilter: NotRequired[str]
    ClusterTypeFilter: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConfigurationRevisionsRequestListConfigurationRevisionsPaginateTypeDef(TypedDict):
    Arn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConfigurationsRequestListConfigurationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListKafkaVersionsRequestListKafkaVersionsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListNodesRequestListNodesPaginateTypeDef(TypedDict):
    ClusterArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListReplicatorsRequestListReplicatorsPaginateTypeDef(TypedDict):
    ReplicatorNameFilter: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListScramSecretsRequestListScramSecretsPaginateTypeDef(TypedDict):
    ClusterArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListVpcConnectionsRequestListVpcConnectionsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListVpcConnectionsResponseTypeDef(TypedDict):
    VpcConnections: List[VpcConnectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PrometheusInfoTypeDef(TypedDict):
    JmxExporter: NotRequired[JmxExporterInfoTypeDef]
    NodeExporter: NotRequired[NodeExporterInfoTypeDef]

class PrometheusTypeDef(TypedDict):
    JmxExporter: NotRequired[JmxExporterTypeDef]
    NodeExporter: NotRequired[NodeExporterTypeDef]

class TopicReplicationOutputTypeDef(TypedDict):
    TopicsToReplicate: List[str]
    CopyAccessControlListsForTopics: NotRequired[bool]
    CopyTopicConfigurations: NotRequired[bool]
    DetectAndCopyNewTopics: NotRequired[bool]
    StartingPosition: NotRequired[ReplicationStartingPositionTypeDef]
    TopicNameConfiguration: NotRequired[ReplicationTopicNameConfigurationTypeDef]
    TopicsToExclude: NotRequired[List[str]]

class TopicReplicationTypeDef(TypedDict):
    TopicsToReplicate: Sequence[str]
    CopyAccessControlListsForTopics: NotRequired[bool]
    CopyTopicConfigurations: NotRequired[bool]
    DetectAndCopyNewTopics: NotRequired[bool]
    StartingPosition: NotRequired[ReplicationStartingPositionTypeDef]
    TopicNameConfiguration: NotRequired[ReplicationTopicNameConfigurationTypeDef]
    TopicsToExclude: NotRequired[Sequence[str]]

class SaslTypeDef(TypedDict):
    Scram: NotRequired[ScramTypeDef]
    Iam: NotRequired[IamTypeDef]

TlsUnionTypeDef = Union[TlsTypeDef, TlsOutputTypeDef]

class UpdateReplicationInfoRequestRequestTypeDef(TypedDict):
    CurrentVersion: str
    ReplicatorArn: str
    SourceKafkaClusterArn: str
    TargetKafkaClusterArn: str
    ConsumerGroupReplication: NotRequired[ConsumerGroupReplicationUpdateTypeDef]
    TopicReplication: NotRequired[TopicReplicationUpdateTypeDef]

class VpcConnectionInfoServerlessTypeDef(TypedDict):
    CreationTime: NotRequired[datetime]
    Owner: NotRequired[str]
    UserIdentity: NotRequired[UserIdentityTypeDef]
    VpcConnectionArn: NotRequired[str]

class VpcConnectionInfoTypeDef(TypedDict):
    VpcConnectionArn: NotRequired[str]
    Owner: NotRequired[str]
    UserIdentity: NotRequired[UserIdentityTypeDef]
    CreationTime: NotRequired[datetime]

VpcConfigUnionTypeDef = Union[VpcConfigTypeDef, VpcConfigOutputTypeDef]

class VpcConnectivitySaslTypeDef(TypedDict):
    Scram: NotRequired[VpcConnectivityScramTypeDef]
    Iam: NotRequired[VpcConnectivityIamTypeDef]

class ReplicatorSummaryTypeDef(TypedDict):
    CreationTime: NotRequired[datetime]
    CurrentVersion: NotRequired[str]
    IsReplicatorReference: NotRequired[bool]
    KafkaClustersSummary: NotRequired[List[KafkaClusterSummaryTypeDef]]
    ReplicationInfoSummaryList: NotRequired[List[ReplicationInfoSummaryTypeDef]]
    ReplicatorArn: NotRequired[str]
    ReplicatorName: NotRequired[str]
    ReplicatorResourceArn: NotRequired[str]
    ReplicatorState: NotRequired[ReplicatorStateType]

class UpdateBrokerStorageRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: str
    TargetBrokerEBSVolumeInfo: Sequence[BrokerEBSVolumeInfoTypeDef]

class StorageInfoTypeDef(TypedDict):
    EbsStorageInfo: NotRequired[EBSStorageInfoTypeDef]

class LoggingInfoTypeDef(TypedDict):
    BrokerLogs: BrokerLogsTypeDef

class NodeInfoTypeDef(TypedDict):
    AddedToClusterTime: NotRequired[str]
    BrokerNodeInfo: NotRequired[BrokerNodeInfoTypeDef]
    ControllerNodeInfo: NotRequired[ControllerNodeInfoTypeDef]
    InstanceType: NotRequired[str]
    NodeARN: NotRequired[str]
    NodeType: NotRequired[Literal["BROKER"]]
    ZookeeperNodeInfo: NotRequired[ZookeeperNodeInfoTypeDef]

class ListConfigurationsResponseTypeDef(TypedDict):
    Configurations: List[ConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ServerlessClientAuthenticationTypeDef(TypedDict):
    Sasl: NotRequired[ServerlessSaslTypeDef]

class KafkaClusterTypeDef(TypedDict):
    AmazonMskCluster: AmazonMskClusterTypeDef
    VpcConfig: KafkaClusterClientVpcConfigUnionTypeDef

class OpenMonitoringInfoTypeDef(TypedDict):
    Prometheus: PrometheusInfoTypeDef

class OpenMonitoringTypeDef(TypedDict):
    Prometheus: PrometheusTypeDef

class ReplicationInfoDescriptionTypeDef(TypedDict):
    ConsumerGroupReplication: NotRequired[ConsumerGroupReplicationOutputTypeDef]
    SourceKafkaClusterAlias: NotRequired[str]
    TargetCompressionType: NotRequired[TargetCompressionTypeType]
    TargetKafkaClusterAlias: NotRequired[str]
    TopicReplication: NotRequired[TopicReplicationOutputTypeDef]

TopicReplicationUnionTypeDef = Union[TopicReplicationTypeDef, TopicReplicationOutputTypeDef]

class ClientAuthenticationOutputTypeDef(TypedDict):
    Sasl: NotRequired[SaslTypeDef]
    Tls: NotRequired[TlsOutputTypeDef]
    Unauthenticated: NotRequired[UnauthenticatedTypeDef]

class ClientAuthenticationTypeDef(TypedDict):
    Sasl: NotRequired[SaslTypeDef]
    Tls: NotRequired[TlsUnionTypeDef]
    Unauthenticated: NotRequired[UnauthenticatedTypeDef]

class ClusterOperationV2ServerlessTypeDef(TypedDict):
    VpcConnectionInfo: NotRequired[VpcConnectionInfoServerlessTypeDef]

class VpcConnectivityClientAuthenticationTypeDef(TypedDict):
    Sasl: NotRequired[VpcConnectivitySaslTypeDef]
    Tls: NotRequired[VpcConnectivityTlsTypeDef]

class ListReplicatorsResponseTypeDef(TypedDict):
    Replicators: List[ReplicatorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListNodesResponseTypeDef(TypedDict):
    NodeInfoList: List[NodeInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ServerlessRequestTypeDef(TypedDict):
    VpcConfigs: Sequence[VpcConfigUnionTypeDef]
    ClientAuthentication: NotRequired[ServerlessClientAuthenticationTypeDef]

class ServerlessTypeDef(TypedDict):
    VpcConfigs: List[VpcConfigOutputTypeDef]
    ClientAuthentication: NotRequired[ServerlessClientAuthenticationTypeDef]

class UpdateMonitoringRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: str
    EnhancedMonitoring: NotRequired[EnhancedMonitoringType]
    OpenMonitoring: NotRequired[OpenMonitoringInfoTypeDef]
    LoggingInfo: NotRequired[LoggingInfoTypeDef]

class DescribeReplicatorResponseTypeDef(TypedDict):
    CreationTime: datetime
    CurrentVersion: str
    IsReplicatorReference: bool
    KafkaClusters: List[KafkaClusterDescriptionTypeDef]
    ReplicationInfoList: List[ReplicationInfoDescriptionTypeDef]
    ReplicatorArn: str
    ReplicatorDescription: str
    ReplicatorName: str
    ReplicatorResourceArn: str
    ReplicatorState: ReplicatorStateType
    ServiceExecutionRoleArn: str
    StateInfo: ReplicationStateInfoTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ReplicationInfoTypeDef(TypedDict):
    ConsumerGroupReplication: ConsumerGroupReplicationUnionTypeDef
    SourceKafkaClusterArn: str
    TargetCompressionType: TargetCompressionTypeType
    TargetKafkaClusterArn: str
    TopicReplication: TopicReplicationUnionTypeDef

ClientAuthenticationUnionTypeDef = Union[
    ClientAuthenticationTypeDef, ClientAuthenticationOutputTypeDef
]

class UpdateSecurityRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: str
    ClientAuthentication: NotRequired[ClientAuthenticationTypeDef]
    EncryptionInfo: NotRequired[EncryptionInfoTypeDef]

class VpcConnectivityTypeDef(TypedDict):
    ClientAuthentication: NotRequired[VpcConnectivityClientAuthenticationTypeDef]

class CreateReplicatorRequestRequestTypeDef(TypedDict):
    KafkaClusters: Sequence[KafkaClusterTypeDef]
    ReplicationInfoList: Sequence[ReplicationInfoTypeDef]
    ReplicatorName: str
    ServiceExecutionRoleArn: str
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class ConnectivityInfoTypeDef(TypedDict):
    PublicAccess: NotRequired[PublicAccessTypeDef]
    VpcConnectivity: NotRequired[VpcConnectivityTypeDef]

class BrokerNodeGroupInfoOutputTypeDef(TypedDict):
    ClientSubnets: List[str]
    InstanceType: str
    BrokerAZDistribution: NotRequired[Literal["DEFAULT"]]
    SecurityGroups: NotRequired[List[str]]
    StorageInfo: NotRequired[StorageInfoTypeDef]
    ConnectivityInfo: NotRequired[ConnectivityInfoTypeDef]
    ZoneIds: NotRequired[List[str]]

class BrokerNodeGroupInfoTypeDef(TypedDict):
    ClientSubnets: Sequence[str]
    InstanceType: str
    BrokerAZDistribution: NotRequired[Literal["DEFAULT"]]
    SecurityGroups: NotRequired[Sequence[str]]
    StorageInfo: NotRequired[StorageInfoTypeDef]
    ConnectivityInfo: NotRequired[ConnectivityInfoTypeDef]
    ZoneIds: NotRequired[Sequence[str]]

class MutableClusterInfoTypeDef(TypedDict):
    BrokerEBSVolumeInfo: NotRequired[List[BrokerEBSVolumeInfoTypeDef]]
    ConfigurationInfo: NotRequired[ConfigurationInfoTypeDef]
    NumberOfBrokerNodes: NotRequired[int]
    EnhancedMonitoring: NotRequired[EnhancedMonitoringType]
    OpenMonitoring: NotRequired[OpenMonitoringTypeDef]
    KafkaVersion: NotRequired[str]
    LoggingInfo: NotRequired[LoggingInfoTypeDef]
    InstanceType: NotRequired[str]
    ClientAuthentication: NotRequired[ClientAuthenticationOutputTypeDef]
    EncryptionInfo: NotRequired[EncryptionInfoTypeDef]
    ConnectivityInfo: NotRequired[ConnectivityInfoTypeDef]
    StorageMode: NotRequired[StorageModeType]
    BrokerCountUpdateInfo: NotRequired[BrokerCountUpdateInfoTypeDef]

class UpdateConnectivityRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    ConnectivityInfo: ConnectivityInfoTypeDef
    CurrentVersion: str

class ClusterInfoTypeDef(TypedDict):
    ActiveOperationArn: NotRequired[str]
    BrokerNodeGroupInfo: NotRequired[BrokerNodeGroupInfoOutputTypeDef]
    ClientAuthentication: NotRequired[ClientAuthenticationOutputTypeDef]
    ClusterArn: NotRequired[str]
    ClusterName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    CurrentBrokerSoftwareInfo: NotRequired[BrokerSoftwareInfoTypeDef]
    CurrentVersion: NotRequired[str]
    EncryptionInfo: NotRequired[EncryptionInfoTypeDef]
    EnhancedMonitoring: NotRequired[EnhancedMonitoringType]
    OpenMonitoring: NotRequired[OpenMonitoringTypeDef]
    LoggingInfo: NotRequired[LoggingInfoTypeDef]
    NumberOfBrokerNodes: NotRequired[int]
    State: NotRequired[ClusterStateType]
    StateInfo: NotRequired[StateInfoTypeDef]
    Tags: NotRequired[Dict[str, str]]
    ZookeeperConnectString: NotRequired[str]
    ZookeeperConnectStringTls: NotRequired[str]
    StorageMode: NotRequired[StorageModeType]
    CustomerActionStatus: NotRequired[CustomerActionStatusType]

class ProvisionedTypeDef(TypedDict):
    BrokerNodeGroupInfo: BrokerNodeGroupInfoOutputTypeDef
    NumberOfBrokerNodes: int
    CurrentBrokerSoftwareInfo: NotRequired[BrokerSoftwareInfoTypeDef]
    ClientAuthentication: NotRequired[ClientAuthenticationOutputTypeDef]
    EncryptionInfo: NotRequired[EncryptionInfoTypeDef]
    EnhancedMonitoring: NotRequired[EnhancedMonitoringType]
    OpenMonitoring: NotRequired[OpenMonitoringInfoTypeDef]
    LoggingInfo: NotRequired[LoggingInfoTypeDef]
    ZookeeperConnectString: NotRequired[str]
    ZookeeperConnectStringTls: NotRequired[str]
    StorageMode: NotRequired[StorageModeType]
    CustomerActionStatus: NotRequired[CustomerActionStatusType]

BrokerNodeGroupInfoUnionTypeDef = Union[
    BrokerNodeGroupInfoTypeDef, BrokerNodeGroupInfoOutputTypeDef
]

class CreateClusterRequestRequestTypeDef(TypedDict):
    BrokerNodeGroupInfo: BrokerNodeGroupInfoTypeDef
    ClusterName: str
    KafkaVersion: str
    NumberOfBrokerNodes: int
    ClientAuthentication: NotRequired[ClientAuthenticationTypeDef]
    ConfigurationInfo: NotRequired[ConfigurationInfoTypeDef]
    EncryptionInfo: NotRequired[EncryptionInfoTypeDef]
    EnhancedMonitoring: NotRequired[EnhancedMonitoringType]
    OpenMonitoring: NotRequired[OpenMonitoringInfoTypeDef]
    LoggingInfo: NotRequired[LoggingInfoTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    StorageMode: NotRequired[StorageModeType]

class ClusterOperationInfoTypeDef(TypedDict):
    ClientRequestId: NotRequired[str]
    ClusterArn: NotRequired[str]
    CreationTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    ErrorInfo: NotRequired[ErrorInfoTypeDef]
    OperationArn: NotRequired[str]
    OperationState: NotRequired[str]
    OperationSteps: NotRequired[List[ClusterOperationStepTypeDef]]
    OperationType: NotRequired[str]
    SourceClusterInfo: NotRequired[MutableClusterInfoTypeDef]
    TargetClusterInfo: NotRequired[MutableClusterInfoTypeDef]
    VpcConnectionInfo: NotRequired[VpcConnectionInfoTypeDef]

class ClusterOperationV2ProvisionedTypeDef(TypedDict):
    OperationSteps: NotRequired[List[ClusterOperationStepTypeDef]]
    SourceClusterInfo: NotRequired[MutableClusterInfoTypeDef]
    TargetClusterInfo: NotRequired[MutableClusterInfoTypeDef]
    VpcConnectionInfo: NotRequired[VpcConnectionInfoTypeDef]

class DescribeClusterResponseTypeDef(TypedDict):
    ClusterInfo: ClusterInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListClustersResponseTypeDef(TypedDict):
    ClusterInfoList: List[ClusterInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ClusterTypeDef(TypedDict):
    ActiveOperationArn: NotRequired[str]
    ClusterType: NotRequired[ClusterTypeType]
    ClusterArn: NotRequired[str]
    ClusterName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    CurrentVersion: NotRequired[str]
    State: NotRequired[ClusterStateType]
    StateInfo: NotRequired[StateInfoTypeDef]
    Tags: NotRequired[Dict[str, str]]
    Provisioned: NotRequired[ProvisionedTypeDef]
    Serverless: NotRequired[ServerlessTypeDef]

class ProvisionedRequestTypeDef(TypedDict):
    BrokerNodeGroupInfo: BrokerNodeGroupInfoUnionTypeDef
    KafkaVersion: str
    NumberOfBrokerNodes: int
    ClientAuthentication: NotRequired[ClientAuthenticationUnionTypeDef]
    ConfigurationInfo: NotRequired[ConfigurationInfoTypeDef]
    EncryptionInfo: NotRequired[EncryptionInfoTypeDef]
    EnhancedMonitoring: NotRequired[EnhancedMonitoringType]
    OpenMonitoring: NotRequired[OpenMonitoringInfoTypeDef]
    LoggingInfo: NotRequired[LoggingInfoTypeDef]
    StorageMode: NotRequired[StorageModeType]

class DescribeClusterOperationResponseTypeDef(TypedDict):
    ClusterOperationInfo: ClusterOperationInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListClusterOperationsResponseTypeDef(TypedDict):
    ClusterOperationInfoList: List[ClusterOperationInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ClusterOperationV2TypeDef(TypedDict):
    ClusterArn: NotRequired[str]
    ClusterType: NotRequired[ClusterTypeType]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    ErrorInfo: NotRequired[ErrorInfoTypeDef]
    OperationArn: NotRequired[str]
    OperationState: NotRequired[str]
    OperationType: NotRequired[str]
    Provisioned: NotRequired[ClusterOperationV2ProvisionedTypeDef]
    Serverless: NotRequired[ClusterOperationV2ServerlessTypeDef]

class DescribeClusterV2ResponseTypeDef(TypedDict):
    ClusterInfo: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListClustersV2ResponseTypeDef(TypedDict):
    ClusterInfoList: List[ClusterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateClusterV2RequestRequestTypeDef(TypedDict):
    ClusterName: str
    Tags: NotRequired[Mapping[str, str]]
    Provisioned: NotRequired[ProvisionedRequestTypeDef]
    Serverless: NotRequired[ServerlessRequestTypeDef]

class DescribeClusterOperationV2ResponseTypeDef(TypedDict):
    ClusterOperationInfo: ClusterOperationV2TypeDef
    ResponseMetadata: ResponseMetadataTypeDef
