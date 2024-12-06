"""
Type annotations for elasticache service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_elasticache.client import ElastiCacheClient

    session = Session()
    client: ElastiCacheClient = session.client("elasticache")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeCacheClustersPaginator,
    DescribeCacheEngineVersionsPaginator,
    DescribeCacheParameterGroupsPaginator,
    DescribeCacheParametersPaginator,
    DescribeCacheSecurityGroupsPaginator,
    DescribeCacheSubnetGroupsPaginator,
    DescribeEngineDefaultParametersPaginator,
    DescribeEventsPaginator,
    DescribeGlobalReplicationGroupsPaginator,
    DescribeReplicationGroupsPaginator,
    DescribeReservedCacheNodesOfferingsPaginator,
    DescribeReservedCacheNodesPaginator,
    DescribeServerlessCacheSnapshotsPaginator,
    DescribeServerlessCachesPaginator,
    DescribeServiceUpdatesPaginator,
    DescribeSnapshotsPaginator,
    DescribeUpdateActionsPaginator,
    DescribeUserGroupsPaginator,
    DescribeUsersPaginator,
)
from .type_defs import (
    AddTagsToResourceMessageRequestTypeDef,
    AllowedNodeTypeModificationsMessageTypeDef,
    AuthorizeCacheSecurityGroupIngressMessageRequestTypeDef,
    AuthorizeCacheSecurityGroupIngressResultTypeDef,
    BatchApplyUpdateActionMessageRequestTypeDef,
    BatchStopUpdateActionMessageRequestTypeDef,
    CacheClusterMessageTypeDef,
    CacheEngineVersionMessageTypeDef,
    CacheParameterGroupDetailsTypeDef,
    CacheParameterGroupNameMessageTypeDef,
    CacheParameterGroupsMessageTypeDef,
    CacheSecurityGroupMessageTypeDef,
    CacheSubnetGroupMessageTypeDef,
    CompleteMigrationMessageRequestTypeDef,
    CompleteMigrationResponseTypeDef,
    CopyServerlessCacheSnapshotRequestRequestTypeDef,
    CopyServerlessCacheSnapshotResponseTypeDef,
    CopySnapshotMessageRequestTypeDef,
    CopySnapshotResultTypeDef,
    CreateCacheClusterMessageRequestTypeDef,
    CreateCacheClusterResultTypeDef,
    CreateCacheParameterGroupMessageRequestTypeDef,
    CreateCacheParameterGroupResultTypeDef,
    CreateCacheSecurityGroupMessageRequestTypeDef,
    CreateCacheSecurityGroupResultTypeDef,
    CreateCacheSubnetGroupMessageRequestTypeDef,
    CreateCacheSubnetGroupResultTypeDef,
    CreateGlobalReplicationGroupMessageRequestTypeDef,
    CreateGlobalReplicationGroupResultTypeDef,
    CreateReplicationGroupMessageRequestTypeDef,
    CreateReplicationGroupResultTypeDef,
    CreateServerlessCacheRequestRequestTypeDef,
    CreateServerlessCacheResponseTypeDef,
    CreateServerlessCacheSnapshotRequestRequestTypeDef,
    CreateServerlessCacheSnapshotResponseTypeDef,
    CreateSnapshotMessageRequestTypeDef,
    CreateSnapshotResultTypeDef,
    CreateUserGroupMessageRequestTypeDef,
    CreateUserMessageRequestTypeDef,
    DecreaseNodeGroupsInGlobalReplicationGroupMessageRequestTypeDef,
    DecreaseNodeGroupsInGlobalReplicationGroupResultTypeDef,
    DecreaseReplicaCountMessageRequestTypeDef,
    DecreaseReplicaCountResultTypeDef,
    DeleteCacheClusterMessageRequestTypeDef,
    DeleteCacheClusterResultTypeDef,
    DeleteCacheParameterGroupMessageRequestTypeDef,
    DeleteCacheSecurityGroupMessageRequestTypeDef,
    DeleteCacheSubnetGroupMessageRequestTypeDef,
    DeleteGlobalReplicationGroupMessageRequestTypeDef,
    DeleteGlobalReplicationGroupResultTypeDef,
    DeleteReplicationGroupMessageRequestTypeDef,
    DeleteReplicationGroupResultTypeDef,
    DeleteServerlessCacheRequestRequestTypeDef,
    DeleteServerlessCacheResponseTypeDef,
    DeleteServerlessCacheSnapshotRequestRequestTypeDef,
    DeleteServerlessCacheSnapshotResponseTypeDef,
    DeleteSnapshotMessageRequestTypeDef,
    DeleteSnapshotResultTypeDef,
    DeleteUserGroupMessageRequestTypeDef,
    DeleteUserMessageRequestTypeDef,
    DescribeCacheClustersMessageRequestTypeDef,
    DescribeCacheEngineVersionsMessageRequestTypeDef,
    DescribeCacheParameterGroupsMessageRequestTypeDef,
    DescribeCacheParametersMessageRequestTypeDef,
    DescribeCacheSecurityGroupsMessageRequestTypeDef,
    DescribeCacheSubnetGroupsMessageRequestTypeDef,
    DescribeEngineDefaultParametersMessageRequestTypeDef,
    DescribeEngineDefaultParametersResultTypeDef,
    DescribeEventsMessageRequestTypeDef,
    DescribeGlobalReplicationGroupsMessageRequestTypeDef,
    DescribeGlobalReplicationGroupsResultTypeDef,
    DescribeReplicationGroupsMessageRequestTypeDef,
    DescribeReservedCacheNodesMessageRequestTypeDef,
    DescribeReservedCacheNodesOfferingsMessageRequestTypeDef,
    DescribeServerlessCacheSnapshotsRequestRequestTypeDef,
    DescribeServerlessCacheSnapshotsResponseTypeDef,
    DescribeServerlessCachesRequestRequestTypeDef,
    DescribeServerlessCachesResponseTypeDef,
    DescribeServiceUpdatesMessageRequestTypeDef,
    DescribeSnapshotsListMessageTypeDef,
    DescribeSnapshotsMessageRequestTypeDef,
    DescribeUpdateActionsMessageRequestTypeDef,
    DescribeUserGroupsMessageRequestTypeDef,
    DescribeUserGroupsResultTypeDef,
    DescribeUsersMessageRequestTypeDef,
    DescribeUsersResultTypeDef,
    DisassociateGlobalReplicationGroupMessageRequestTypeDef,
    DisassociateGlobalReplicationGroupResultTypeDef,
    EmptyResponseMetadataTypeDef,
    EventsMessageTypeDef,
    ExportServerlessCacheSnapshotRequestRequestTypeDef,
    ExportServerlessCacheSnapshotResponseTypeDef,
    FailoverGlobalReplicationGroupMessageRequestTypeDef,
    FailoverGlobalReplicationGroupResultTypeDef,
    IncreaseNodeGroupsInGlobalReplicationGroupMessageRequestTypeDef,
    IncreaseNodeGroupsInGlobalReplicationGroupResultTypeDef,
    IncreaseReplicaCountMessageRequestTypeDef,
    IncreaseReplicaCountResultTypeDef,
    ListAllowedNodeTypeModificationsMessageRequestTypeDef,
    ListTagsForResourceMessageRequestTypeDef,
    ModifyCacheClusterMessageRequestTypeDef,
    ModifyCacheClusterResultTypeDef,
    ModifyCacheParameterGroupMessageRequestTypeDef,
    ModifyCacheSubnetGroupMessageRequestTypeDef,
    ModifyCacheSubnetGroupResultTypeDef,
    ModifyGlobalReplicationGroupMessageRequestTypeDef,
    ModifyGlobalReplicationGroupResultTypeDef,
    ModifyReplicationGroupMessageRequestTypeDef,
    ModifyReplicationGroupResultTypeDef,
    ModifyReplicationGroupShardConfigurationMessageRequestTypeDef,
    ModifyReplicationGroupShardConfigurationResultTypeDef,
    ModifyServerlessCacheRequestRequestTypeDef,
    ModifyServerlessCacheResponseTypeDef,
    ModifyUserGroupMessageRequestTypeDef,
    ModifyUserMessageRequestTypeDef,
    PurchaseReservedCacheNodesOfferingMessageRequestTypeDef,
    PurchaseReservedCacheNodesOfferingResultTypeDef,
    RebalanceSlotsInGlobalReplicationGroupMessageRequestTypeDef,
    RebalanceSlotsInGlobalReplicationGroupResultTypeDef,
    RebootCacheClusterMessageRequestTypeDef,
    RebootCacheClusterResultTypeDef,
    RemoveTagsFromResourceMessageRequestTypeDef,
    ReplicationGroupMessageTypeDef,
    ReservedCacheNodeMessageTypeDef,
    ReservedCacheNodesOfferingMessageTypeDef,
    ResetCacheParameterGroupMessageRequestTypeDef,
    RevokeCacheSecurityGroupIngressMessageRequestTypeDef,
    RevokeCacheSecurityGroupIngressResultTypeDef,
    ServiceUpdatesMessageTypeDef,
    StartMigrationMessageRequestTypeDef,
    StartMigrationResponseTypeDef,
    TagListMessageTypeDef,
    TestFailoverMessageRequestTypeDef,
    TestFailoverResultTypeDef,
    TestMigrationMessageRequestTypeDef,
    TestMigrationResponseTypeDef,
    UpdateActionResultsMessageTypeDef,
    UpdateActionsMessageTypeDef,
    UserGroupResponseTypeDef,
    UserResponseTypeDef,
)
from .waiter import (
    CacheClusterAvailableWaiter,
    CacheClusterDeletedWaiter,
    ReplicationGroupAvailableWaiter,
    ReplicationGroupDeletedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ElastiCacheClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    APICallRateForCustomerExceededFault: Type[BotocoreClientError]
    AuthorizationAlreadyExistsFault: Type[BotocoreClientError]
    AuthorizationNotFoundFault: Type[BotocoreClientError]
    CacheClusterAlreadyExistsFault: Type[BotocoreClientError]
    CacheClusterNotFoundFault: Type[BotocoreClientError]
    CacheParameterGroupAlreadyExistsFault: Type[BotocoreClientError]
    CacheParameterGroupNotFoundFault: Type[BotocoreClientError]
    CacheParameterGroupQuotaExceededFault: Type[BotocoreClientError]
    CacheSecurityGroupAlreadyExistsFault: Type[BotocoreClientError]
    CacheSecurityGroupNotFoundFault: Type[BotocoreClientError]
    CacheSecurityGroupQuotaExceededFault: Type[BotocoreClientError]
    CacheSubnetGroupAlreadyExistsFault: Type[BotocoreClientError]
    CacheSubnetGroupInUse: Type[BotocoreClientError]
    CacheSubnetGroupNotFoundFault: Type[BotocoreClientError]
    CacheSubnetGroupQuotaExceededFault: Type[BotocoreClientError]
    CacheSubnetQuotaExceededFault: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClusterQuotaForCustomerExceededFault: Type[BotocoreClientError]
    DefaultUserAssociatedToUserGroupFault: Type[BotocoreClientError]
    DefaultUserRequired: Type[BotocoreClientError]
    DuplicateUserNameFault: Type[BotocoreClientError]
    GlobalReplicationGroupAlreadyExistsFault: Type[BotocoreClientError]
    GlobalReplicationGroupNotFoundFault: Type[BotocoreClientError]
    InsufficientCacheClusterCapacityFault: Type[BotocoreClientError]
    InvalidARNFault: Type[BotocoreClientError]
    InvalidCacheClusterStateFault: Type[BotocoreClientError]
    InvalidCacheParameterGroupStateFault: Type[BotocoreClientError]
    InvalidCacheSecurityGroupStateFault: Type[BotocoreClientError]
    InvalidCredentialsException: Type[BotocoreClientError]
    InvalidGlobalReplicationGroupStateFault: Type[BotocoreClientError]
    InvalidKMSKeyFault: Type[BotocoreClientError]
    InvalidParameterCombinationException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    InvalidReplicationGroupStateFault: Type[BotocoreClientError]
    InvalidServerlessCacheSnapshotStateFault: Type[BotocoreClientError]
    InvalidServerlessCacheStateFault: Type[BotocoreClientError]
    InvalidSnapshotStateFault: Type[BotocoreClientError]
    InvalidSubnet: Type[BotocoreClientError]
    InvalidUserGroupStateFault: Type[BotocoreClientError]
    InvalidUserStateFault: Type[BotocoreClientError]
    InvalidVPCNetworkStateFault: Type[BotocoreClientError]
    NoOperationFault: Type[BotocoreClientError]
    NodeGroupNotFoundFault: Type[BotocoreClientError]
    NodeGroupsPerReplicationGroupQuotaExceededFault: Type[BotocoreClientError]
    NodeQuotaForClusterExceededFault: Type[BotocoreClientError]
    NodeQuotaForCustomerExceededFault: Type[BotocoreClientError]
    ReplicationGroupAlreadyExistsFault: Type[BotocoreClientError]
    ReplicationGroupAlreadyUnderMigrationFault: Type[BotocoreClientError]
    ReplicationGroupNotFoundFault: Type[BotocoreClientError]
    ReplicationGroupNotUnderMigrationFault: Type[BotocoreClientError]
    ReservedCacheNodeAlreadyExistsFault: Type[BotocoreClientError]
    ReservedCacheNodeNotFoundFault: Type[BotocoreClientError]
    ReservedCacheNodeQuotaExceededFault: Type[BotocoreClientError]
    ReservedCacheNodesOfferingNotFoundFault: Type[BotocoreClientError]
    ServerlessCacheAlreadyExistsFault: Type[BotocoreClientError]
    ServerlessCacheNotFoundFault: Type[BotocoreClientError]
    ServerlessCacheQuotaForCustomerExceededFault: Type[BotocoreClientError]
    ServerlessCacheSnapshotAlreadyExistsFault: Type[BotocoreClientError]
    ServerlessCacheSnapshotNotFoundFault: Type[BotocoreClientError]
    ServerlessCacheSnapshotQuotaExceededFault: Type[BotocoreClientError]
    ServiceLinkedRoleNotFoundFault: Type[BotocoreClientError]
    ServiceUpdateNotFoundFault: Type[BotocoreClientError]
    SnapshotAlreadyExistsFault: Type[BotocoreClientError]
    SnapshotFeatureNotSupportedFault: Type[BotocoreClientError]
    SnapshotNotFoundFault: Type[BotocoreClientError]
    SnapshotQuotaExceededFault: Type[BotocoreClientError]
    SubnetInUse: Type[BotocoreClientError]
    SubnetNotAllowedFault: Type[BotocoreClientError]
    TagNotFoundFault: Type[BotocoreClientError]
    TagQuotaPerResourceExceeded: Type[BotocoreClientError]
    TestFailoverNotAvailableFault: Type[BotocoreClientError]
    UserAlreadyExistsFault: Type[BotocoreClientError]
    UserGroupAlreadyExistsFault: Type[BotocoreClientError]
    UserGroupNotFoundFault: Type[BotocoreClientError]
    UserGroupQuotaExceededFault: Type[BotocoreClientError]
    UserNotFoundFault: Type[BotocoreClientError]
    UserQuotaExceededFault: Type[BotocoreClientError]


class ElastiCacheClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElastiCacheClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#close)
        """

    def add_tags_to_resource(
        self, **kwargs: Unpack[AddTagsToResourceMessageRequestTypeDef]
    ) -> TagListMessageTypeDef:
        """
        A tag is a key-value pair where the key and value are case-sensitive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/add_tags_to_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#add_tags_to_resource)
        """

    def authorize_cache_security_group_ingress(
        self, **kwargs: Unpack[AuthorizeCacheSecurityGroupIngressMessageRequestTypeDef]
    ) -> AuthorizeCacheSecurityGroupIngressResultTypeDef:
        """
        Allows network ingress to a cache security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/authorize_cache_security_group_ingress.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#authorize_cache_security_group_ingress)
        """

    def batch_apply_update_action(
        self, **kwargs: Unpack[BatchApplyUpdateActionMessageRequestTypeDef]
    ) -> UpdateActionResultsMessageTypeDef:
        """
        Apply the service update.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/batch_apply_update_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#batch_apply_update_action)
        """

    def batch_stop_update_action(
        self, **kwargs: Unpack[BatchStopUpdateActionMessageRequestTypeDef]
    ) -> UpdateActionResultsMessageTypeDef:
        """
        Stop the service update.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/batch_stop_update_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#batch_stop_update_action)
        """

    def complete_migration(
        self, **kwargs: Unpack[CompleteMigrationMessageRequestTypeDef]
    ) -> CompleteMigrationResponseTypeDef:
        """
        Complete the migration of data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/complete_migration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#complete_migration)
        """

    def copy_serverless_cache_snapshot(
        self, **kwargs: Unpack[CopyServerlessCacheSnapshotRequestRequestTypeDef]
    ) -> CopyServerlessCacheSnapshotResponseTypeDef:
        """
        Creates a copy of an existing serverless cache's snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/copy_serverless_cache_snapshot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#copy_serverless_cache_snapshot)
        """

    def copy_snapshot(
        self, **kwargs: Unpack[CopySnapshotMessageRequestTypeDef]
    ) -> CopySnapshotResultTypeDef:
        """
        Makes a copy of an existing snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/copy_snapshot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#copy_snapshot)
        """

    def create_cache_cluster(
        self, **kwargs: Unpack[CreateCacheClusterMessageRequestTypeDef]
    ) -> CreateCacheClusterResultTypeDef:
        """
        Creates a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/create_cache_cluster.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#create_cache_cluster)
        """

    def create_cache_parameter_group(
        self, **kwargs: Unpack[CreateCacheParameterGroupMessageRequestTypeDef]
    ) -> CreateCacheParameterGroupResultTypeDef:
        """
        Creates a new Amazon ElastiCache cache parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/create_cache_parameter_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#create_cache_parameter_group)
        """

    def create_cache_security_group(
        self, **kwargs: Unpack[CreateCacheSecurityGroupMessageRequestTypeDef]
    ) -> CreateCacheSecurityGroupResultTypeDef:
        """
        Creates a new cache security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/create_cache_security_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#create_cache_security_group)
        """

    def create_cache_subnet_group(
        self, **kwargs: Unpack[CreateCacheSubnetGroupMessageRequestTypeDef]
    ) -> CreateCacheSubnetGroupResultTypeDef:
        """
        Creates a new cache subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/create_cache_subnet_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#create_cache_subnet_group)
        """

    def create_global_replication_group(
        self, **kwargs: Unpack[CreateGlobalReplicationGroupMessageRequestTypeDef]
    ) -> CreateGlobalReplicationGroupResultTypeDef:
        """
        Global Datastore offers fully managed, fast, reliable and secure cross-region
        replication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/create_global_replication_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#create_global_replication_group)
        """

    def create_replication_group(
        self, **kwargs: Unpack[CreateReplicationGroupMessageRequestTypeDef]
    ) -> CreateReplicationGroupResultTypeDef:
        """
        Creates a Valkey or Redis OSS (cluster mode disabled) or a Valkey or Redis OSS
        (cluster mode enabled) replication group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/create_replication_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#create_replication_group)
        """

    def create_serverless_cache(
        self, **kwargs: Unpack[CreateServerlessCacheRequestRequestTypeDef]
    ) -> CreateServerlessCacheResponseTypeDef:
        """
        Creates a serverless cache.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/create_serverless_cache.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#create_serverless_cache)
        """

    def create_serverless_cache_snapshot(
        self, **kwargs: Unpack[CreateServerlessCacheSnapshotRequestRequestTypeDef]
    ) -> CreateServerlessCacheSnapshotResponseTypeDef:
        """
        This API creates a copy of an entire ServerlessCache at a specific moment in
        time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/create_serverless_cache_snapshot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#create_serverless_cache_snapshot)
        """

    def create_snapshot(
        self, **kwargs: Unpack[CreateSnapshotMessageRequestTypeDef]
    ) -> CreateSnapshotResultTypeDef:
        """
        Creates a copy of an entire cluster or replication group at a specific moment
        in time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/create_snapshot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#create_snapshot)
        """

    def create_user(self, **kwargs: Unpack[CreateUserMessageRequestTypeDef]) -> UserResponseTypeDef:
        """
        For Valkey engine version 7.2 onwards and Redis OSS 6.0 and onwards: Creates a
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/create_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#create_user)
        """

    def create_user_group(
        self, **kwargs: Unpack[CreateUserGroupMessageRequestTypeDef]
    ) -> UserGroupResponseTypeDef:
        """
        For Valkey engine version 7.2 onwards and Redis OSS 6.0 onwards: Creates a user
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/create_user_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#create_user_group)
        """

    def decrease_node_groups_in_global_replication_group(
        self, **kwargs: Unpack[DecreaseNodeGroupsInGlobalReplicationGroupMessageRequestTypeDef]
    ) -> DecreaseNodeGroupsInGlobalReplicationGroupResultTypeDef:
        """
        Decreases the number of node groups in a Global datastore.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/decrease_node_groups_in_global_replication_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#decrease_node_groups_in_global_replication_group)
        """

    def decrease_replica_count(
        self, **kwargs: Unpack[DecreaseReplicaCountMessageRequestTypeDef]
    ) -> DecreaseReplicaCountResultTypeDef:
        """
        Dynamically decreases the number of replicas in a Valkey or Redis OSS (cluster
        mode disabled) replication group or the number of replica nodes in one or more
        node groups (shards) of a Valkey or Redis OSS (cluster mode enabled)
        replication group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/decrease_replica_count.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#decrease_replica_count)
        """

    def delete_cache_cluster(
        self, **kwargs: Unpack[DeleteCacheClusterMessageRequestTypeDef]
    ) -> DeleteCacheClusterResultTypeDef:
        """
        Deletes a previously provisioned cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/delete_cache_cluster.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#delete_cache_cluster)
        """

    def delete_cache_parameter_group(
        self, **kwargs: Unpack[DeleteCacheParameterGroupMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified cache parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/delete_cache_parameter_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#delete_cache_parameter_group)
        """

    def delete_cache_security_group(
        self, **kwargs: Unpack[DeleteCacheSecurityGroupMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a cache security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/delete_cache_security_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#delete_cache_security_group)
        """

    def delete_cache_subnet_group(
        self, **kwargs: Unpack[DeleteCacheSubnetGroupMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a cache subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/delete_cache_subnet_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#delete_cache_subnet_group)
        """

    def delete_global_replication_group(
        self, **kwargs: Unpack[DeleteGlobalReplicationGroupMessageRequestTypeDef]
    ) -> DeleteGlobalReplicationGroupResultTypeDef:
        """
        Deleting a Global datastore is a two-step process:.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/delete_global_replication_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#delete_global_replication_group)
        """

    def delete_replication_group(
        self, **kwargs: Unpack[DeleteReplicationGroupMessageRequestTypeDef]
    ) -> DeleteReplicationGroupResultTypeDef:
        """
        Deletes an existing replication group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/delete_replication_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#delete_replication_group)
        """

    def delete_serverless_cache(
        self, **kwargs: Unpack[DeleteServerlessCacheRequestRequestTypeDef]
    ) -> DeleteServerlessCacheResponseTypeDef:
        """
        Deletes a specified existing serverless cache.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/delete_serverless_cache.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#delete_serverless_cache)
        """

    def delete_serverless_cache_snapshot(
        self, **kwargs: Unpack[DeleteServerlessCacheSnapshotRequestRequestTypeDef]
    ) -> DeleteServerlessCacheSnapshotResponseTypeDef:
        """
        Deletes an existing serverless cache snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/delete_serverless_cache_snapshot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#delete_serverless_cache_snapshot)
        """

    def delete_snapshot(
        self, **kwargs: Unpack[DeleteSnapshotMessageRequestTypeDef]
    ) -> DeleteSnapshotResultTypeDef:
        """
        Deletes an existing snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/delete_snapshot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#delete_snapshot)
        """

    def delete_user(self, **kwargs: Unpack[DeleteUserMessageRequestTypeDef]) -> UserResponseTypeDef:
        """
        For Valkey engine version 7.2 onwards and Redis OSS 6.0 onwards: Deletes a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/delete_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#delete_user)
        """

    def delete_user_group(
        self, **kwargs: Unpack[DeleteUserGroupMessageRequestTypeDef]
    ) -> UserGroupResponseTypeDef:
        """
        For Valkey engine version 7.2 onwards and Redis OSS 6.0 onwards: Deletes a user
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/delete_user_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#delete_user_group)
        """

    def describe_cache_clusters(
        self, **kwargs: Unpack[DescribeCacheClustersMessageRequestTypeDef]
    ) -> CacheClusterMessageTypeDef:
        """
        Returns information about all provisioned clusters if no cluster identifier is
        specified, or about a specific cache cluster if a cluster identifier is
        supplied.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_cache_clusters.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_cache_clusters)
        """

    def describe_cache_engine_versions(
        self, **kwargs: Unpack[DescribeCacheEngineVersionsMessageRequestTypeDef]
    ) -> CacheEngineVersionMessageTypeDef:
        """
        Returns a list of the available cache engines and their versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_cache_engine_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_cache_engine_versions)
        """

    def describe_cache_parameter_groups(
        self, **kwargs: Unpack[DescribeCacheParameterGroupsMessageRequestTypeDef]
    ) -> CacheParameterGroupsMessageTypeDef:
        """
        Returns a list of cache parameter group descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_cache_parameter_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_cache_parameter_groups)
        """

    def describe_cache_parameters(
        self, **kwargs: Unpack[DescribeCacheParametersMessageRequestTypeDef]
    ) -> CacheParameterGroupDetailsTypeDef:
        """
        Returns the detailed parameter list for a particular cache parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_cache_parameters.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_cache_parameters)
        """

    def describe_cache_security_groups(
        self, **kwargs: Unpack[DescribeCacheSecurityGroupsMessageRequestTypeDef]
    ) -> CacheSecurityGroupMessageTypeDef:
        """
        Returns a list of cache security group descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_cache_security_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_cache_security_groups)
        """

    def describe_cache_subnet_groups(
        self, **kwargs: Unpack[DescribeCacheSubnetGroupsMessageRequestTypeDef]
    ) -> CacheSubnetGroupMessageTypeDef:
        """
        Returns a list of cache subnet group descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_cache_subnet_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_cache_subnet_groups)
        """

    def describe_engine_default_parameters(
        self, **kwargs: Unpack[DescribeEngineDefaultParametersMessageRequestTypeDef]
    ) -> DescribeEngineDefaultParametersResultTypeDef:
        """
        Returns the default engine and system parameter information for the specified
        cache engine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_engine_default_parameters.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_engine_default_parameters)
        """

    def describe_events(
        self, **kwargs: Unpack[DescribeEventsMessageRequestTypeDef]
    ) -> EventsMessageTypeDef:
        """
        Returns events related to clusters, cache security groups, and cache parameter
        groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_events.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_events)
        """

    def describe_global_replication_groups(
        self, **kwargs: Unpack[DescribeGlobalReplicationGroupsMessageRequestTypeDef]
    ) -> DescribeGlobalReplicationGroupsResultTypeDef:
        """
        Returns information about a particular global replication group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_global_replication_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_global_replication_groups)
        """

    def describe_replication_groups(
        self, **kwargs: Unpack[DescribeReplicationGroupsMessageRequestTypeDef]
    ) -> ReplicationGroupMessageTypeDef:
        """
        Returns information about a particular replication group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_replication_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_replication_groups)
        """

    def describe_reserved_cache_nodes(
        self, **kwargs: Unpack[DescribeReservedCacheNodesMessageRequestTypeDef]
    ) -> ReservedCacheNodeMessageTypeDef:
        """
        Returns information about reserved cache nodes for this account, or about a
        specified reserved cache node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_reserved_cache_nodes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_reserved_cache_nodes)
        """

    def describe_reserved_cache_nodes_offerings(
        self, **kwargs: Unpack[DescribeReservedCacheNodesOfferingsMessageRequestTypeDef]
    ) -> ReservedCacheNodesOfferingMessageTypeDef:
        """
        Lists available reserved cache node offerings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_reserved_cache_nodes_offerings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_reserved_cache_nodes_offerings)
        """

    def describe_serverless_cache_snapshots(
        self, **kwargs: Unpack[DescribeServerlessCacheSnapshotsRequestRequestTypeDef]
    ) -> DescribeServerlessCacheSnapshotsResponseTypeDef:
        """
        Returns information about serverless cache snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_serverless_cache_snapshots.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_serverless_cache_snapshots)
        """

    def describe_serverless_caches(
        self, **kwargs: Unpack[DescribeServerlessCachesRequestRequestTypeDef]
    ) -> DescribeServerlessCachesResponseTypeDef:
        """
        Returns information about a specific serverless cache.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_serverless_caches.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_serverless_caches)
        """

    def describe_service_updates(
        self, **kwargs: Unpack[DescribeServiceUpdatesMessageRequestTypeDef]
    ) -> ServiceUpdatesMessageTypeDef:
        """
        Returns details of the service updates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_service_updates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_service_updates)
        """

    def describe_snapshots(
        self, **kwargs: Unpack[DescribeSnapshotsMessageRequestTypeDef]
    ) -> DescribeSnapshotsListMessageTypeDef:
        """
        Returns information about cluster or replication group snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_snapshots.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_snapshots)
        """

    def describe_update_actions(
        self, **kwargs: Unpack[DescribeUpdateActionsMessageRequestTypeDef]
    ) -> UpdateActionsMessageTypeDef:
        """
        Returns details of the update actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_update_actions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_update_actions)
        """

    def describe_user_groups(
        self, **kwargs: Unpack[DescribeUserGroupsMessageRequestTypeDef]
    ) -> DescribeUserGroupsResultTypeDef:
        """
        Returns a list of user groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_user_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_user_groups)
        """

    def describe_users(
        self, **kwargs: Unpack[DescribeUsersMessageRequestTypeDef]
    ) -> DescribeUsersResultTypeDef:
        """
        Returns a list of users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_users.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#describe_users)
        """

    def disassociate_global_replication_group(
        self, **kwargs: Unpack[DisassociateGlobalReplicationGroupMessageRequestTypeDef]
    ) -> DisassociateGlobalReplicationGroupResultTypeDef:
        """
        Remove a secondary cluster from the Global datastore using the Global datastore
        name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/disassociate_global_replication_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#disassociate_global_replication_group)
        """

    def export_serverless_cache_snapshot(
        self, **kwargs: Unpack[ExportServerlessCacheSnapshotRequestRequestTypeDef]
    ) -> ExportServerlessCacheSnapshotResponseTypeDef:
        """
        Provides the functionality to export the serverless cache snapshot data to
        Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/export_serverless_cache_snapshot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#export_serverless_cache_snapshot)
        """

    def failover_global_replication_group(
        self, **kwargs: Unpack[FailoverGlobalReplicationGroupMessageRequestTypeDef]
    ) -> FailoverGlobalReplicationGroupResultTypeDef:
        """
        Used to failover the primary region to a secondary region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/failover_global_replication_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#failover_global_replication_group)
        """

    def increase_node_groups_in_global_replication_group(
        self, **kwargs: Unpack[IncreaseNodeGroupsInGlobalReplicationGroupMessageRequestTypeDef]
    ) -> IncreaseNodeGroupsInGlobalReplicationGroupResultTypeDef:
        """
        Increase the number of node groups in the Global datastore.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/increase_node_groups_in_global_replication_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#increase_node_groups_in_global_replication_group)
        """

    def increase_replica_count(
        self, **kwargs: Unpack[IncreaseReplicaCountMessageRequestTypeDef]
    ) -> IncreaseReplicaCountResultTypeDef:
        """
        Dynamically increases the number of replicas in a Valkey or Redis OSS (cluster
        mode disabled) replication group or the number of replica nodes in one or more
        node groups (shards) of a Valkey or Redis OSS (cluster mode enabled)
        replication group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/increase_replica_count.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#increase_replica_count)
        """

    def list_allowed_node_type_modifications(
        self, **kwargs: Unpack[ListAllowedNodeTypeModificationsMessageRequestTypeDef]
    ) -> AllowedNodeTypeModificationsMessageTypeDef:
        """
        Lists all available node types that you can scale with your cluster's
        replication group's current node type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/list_allowed_node_type_modifications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#list_allowed_node_type_modifications)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceMessageRequestTypeDef]
    ) -> TagListMessageTypeDef:
        """
        Lists all tags currently on a named resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#list_tags_for_resource)
        """

    def modify_cache_cluster(
        self, **kwargs: Unpack[ModifyCacheClusterMessageRequestTypeDef]
    ) -> ModifyCacheClusterResultTypeDef:
        """
        Modifies the settings for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/modify_cache_cluster.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#modify_cache_cluster)
        """

    def modify_cache_parameter_group(
        self, **kwargs: Unpack[ModifyCacheParameterGroupMessageRequestTypeDef]
    ) -> CacheParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a cache parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/modify_cache_parameter_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#modify_cache_parameter_group)
        """

    def modify_cache_subnet_group(
        self, **kwargs: Unpack[ModifyCacheSubnetGroupMessageRequestTypeDef]
    ) -> ModifyCacheSubnetGroupResultTypeDef:
        """
        Modifies an existing cache subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/modify_cache_subnet_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#modify_cache_subnet_group)
        """

    def modify_global_replication_group(
        self, **kwargs: Unpack[ModifyGlobalReplicationGroupMessageRequestTypeDef]
    ) -> ModifyGlobalReplicationGroupResultTypeDef:
        """
        Modifies the settings for a Global datastore.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/modify_global_replication_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#modify_global_replication_group)
        """

    def modify_replication_group(
        self, **kwargs: Unpack[ModifyReplicationGroupMessageRequestTypeDef]
    ) -> ModifyReplicationGroupResultTypeDef:
        """
        Modifies the settings for a replication group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/modify_replication_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#modify_replication_group)
        """

    def modify_replication_group_shard_configuration(
        self, **kwargs: Unpack[ModifyReplicationGroupShardConfigurationMessageRequestTypeDef]
    ) -> ModifyReplicationGroupShardConfigurationResultTypeDef:
        """
        Modifies a replication group's shards (node groups) by allowing you to add
        shards, remove shards, or rebalance the keyspaces among existing shards.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/modify_replication_group_shard_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#modify_replication_group_shard_configuration)
        """

    def modify_serverless_cache(
        self, **kwargs: Unpack[ModifyServerlessCacheRequestRequestTypeDef]
    ) -> ModifyServerlessCacheResponseTypeDef:
        """
        This API modifies the attributes of a serverless cache.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/modify_serverless_cache.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#modify_serverless_cache)
        """

    def modify_user(self, **kwargs: Unpack[ModifyUserMessageRequestTypeDef]) -> UserResponseTypeDef:
        """
        Changes user password(s) and/or access string.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/modify_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#modify_user)
        """

    def modify_user_group(
        self, **kwargs: Unpack[ModifyUserGroupMessageRequestTypeDef]
    ) -> UserGroupResponseTypeDef:
        """
        Changes the list of users that belong to the user group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/modify_user_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#modify_user_group)
        """

    def purchase_reserved_cache_nodes_offering(
        self, **kwargs: Unpack[PurchaseReservedCacheNodesOfferingMessageRequestTypeDef]
    ) -> PurchaseReservedCacheNodesOfferingResultTypeDef:
        """
        Allows you to purchase a reserved cache node offering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/purchase_reserved_cache_nodes_offering.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#purchase_reserved_cache_nodes_offering)
        """

    def rebalance_slots_in_global_replication_group(
        self, **kwargs: Unpack[RebalanceSlotsInGlobalReplicationGroupMessageRequestTypeDef]
    ) -> RebalanceSlotsInGlobalReplicationGroupResultTypeDef:
        """
        Redistribute slots to ensure uniform distribution across existing shards in the
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/rebalance_slots_in_global_replication_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#rebalance_slots_in_global_replication_group)
        """

    def reboot_cache_cluster(
        self, **kwargs: Unpack[RebootCacheClusterMessageRequestTypeDef]
    ) -> RebootCacheClusterResultTypeDef:
        """
        Reboots some, or all, of the cache nodes within a provisioned cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/reboot_cache_cluster.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#reboot_cache_cluster)
        """

    def remove_tags_from_resource(
        self, **kwargs: Unpack[RemoveTagsFromResourceMessageRequestTypeDef]
    ) -> TagListMessageTypeDef:
        """
        Removes the tags identified by the <code>TagKeys</code> list from the named
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/remove_tags_from_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#remove_tags_from_resource)
        """

    def reset_cache_parameter_group(
        self, **kwargs: Unpack[ResetCacheParameterGroupMessageRequestTypeDef]
    ) -> CacheParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a cache parameter group to the engine or system
        default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/reset_cache_parameter_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#reset_cache_parameter_group)
        """

    def revoke_cache_security_group_ingress(
        self, **kwargs: Unpack[RevokeCacheSecurityGroupIngressMessageRequestTypeDef]
    ) -> RevokeCacheSecurityGroupIngressResultTypeDef:
        """
        Revokes ingress from a cache security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/revoke_cache_security_group_ingress.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#revoke_cache_security_group_ingress)
        """

    def start_migration(
        self, **kwargs: Unpack[StartMigrationMessageRequestTypeDef]
    ) -> StartMigrationResponseTypeDef:
        """
        Start the migration of data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/start_migration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#start_migration)
        """

    def test_failover(
        self, **kwargs: Unpack[TestFailoverMessageRequestTypeDef]
    ) -> TestFailoverResultTypeDef:
        """
        Represents the input of a <code>TestFailover</code> operation which tests
        automatic failover on a specified node group (called shard in the console) in a
        replication group (called cluster in the console).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/test_failover.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#test_failover)
        """

    def test_migration(
        self, **kwargs: Unpack[TestMigrationMessageRequestTypeDef]
    ) -> TestMigrationResponseTypeDef:
        """
        Async API to test connection between source and target replication group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/test_migration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#test_migration)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cache_clusters"]
    ) -> DescribeCacheClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cache_engine_versions"]
    ) -> DescribeCacheEngineVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cache_parameter_groups"]
    ) -> DescribeCacheParameterGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cache_parameters"]
    ) -> DescribeCacheParametersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cache_security_groups"]
    ) -> DescribeCacheSecurityGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cache_subnet_groups"]
    ) -> DescribeCacheSubnetGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_engine_default_parameters"]
    ) -> DescribeEngineDefaultParametersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_events"]) -> DescribeEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_global_replication_groups"]
    ) -> DescribeGlobalReplicationGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_replication_groups"]
    ) -> DescribeReplicationGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_cache_nodes_offerings"]
    ) -> DescribeReservedCacheNodesOfferingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_cache_nodes"]
    ) -> DescribeReservedCacheNodesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_serverless_cache_snapshots"]
    ) -> DescribeServerlessCacheSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_serverless_caches"]
    ) -> DescribeServerlessCachesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_service_updates"]
    ) -> DescribeServiceUpdatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_snapshots"]
    ) -> DescribeSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_update_actions"]
    ) -> DescribeUpdateActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_user_groups"]
    ) -> DescribeUserGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_users"]) -> DescribeUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["cache_cluster_available"]
    ) -> CacheClusterAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["cache_cluster_deleted"]
    ) -> CacheClusterDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["replication_group_available"]
    ) -> ReplicationGroupAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["replication_group_deleted"]
    ) -> ReplicationGroupDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/client/#get_waiter)
        """
