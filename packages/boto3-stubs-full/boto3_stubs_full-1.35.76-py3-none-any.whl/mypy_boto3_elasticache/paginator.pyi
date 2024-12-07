"""
Type annotations for elasticache service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_elasticache.client import ElastiCacheClient
    from mypy_boto3_elasticache.paginator import (
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

    session = Session()
    client: ElastiCacheClient = session.client("elasticache")

    describe_cache_clusters_paginator: DescribeCacheClustersPaginator = client.get_paginator("describe_cache_clusters")
    describe_cache_engine_versions_paginator: DescribeCacheEngineVersionsPaginator = client.get_paginator("describe_cache_engine_versions")
    describe_cache_parameter_groups_paginator: DescribeCacheParameterGroupsPaginator = client.get_paginator("describe_cache_parameter_groups")
    describe_cache_parameters_paginator: DescribeCacheParametersPaginator = client.get_paginator("describe_cache_parameters")
    describe_cache_security_groups_paginator: DescribeCacheSecurityGroupsPaginator = client.get_paginator("describe_cache_security_groups")
    describe_cache_subnet_groups_paginator: DescribeCacheSubnetGroupsPaginator = client.get_paginator("describe_cache_subnet_groups")
    describe_engine_default_parameters_paginator: DescribeEngineDefaultParametersPaginator = client.get_paginator("describe_engine_default_parameters")
    describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
    describe_global_replication_groups_paginator: DescribeGlobalReplicationGroupsPaginator = client.get_paginator("describe_global_replication_groups")
    describe_replication_groups_paginator: DescribeReplicationGroupsPaginator = client.get_paginator("describe_replication_groups")
    describe_reserved_cache_nodes_offerings_paginator: DescribeReservedCacheNodesOfferingsPaginator = client.get_paginator("describe_reserved_cache_nodes_offerings")
    describe_reserved_cache_nodes_paginator: DescribeReservedCacheNodesPaginator = client.get_paginator("describe_reserved_cache_nodes")
    describe_serverless_cache_snapshots_paginator: DescribeServerlessCacheSnapshotsPaginator = client.get_paginator("describe_serverless_cache_snapshots")
    describe_serverless_caches_paginator: DescribeServerlessCachesPaginator = client.get_paginator("describe_serverless_caches")
    describe_service_updates_paginator: DescribeServiceUpdatesPaginator = client.get_paginator("describe_service_updates")
    describe_snapshots_paginator: DescribeSnapshotsPaginator = client.get_paginator("describe_snapshots")
    describe_update_actions_paginator: DescribeUpdateActionsPaginator = client.get_paginator("describe_update_actions")
    describe_user_groups_paginator: DescribeUserGroupsPaginator = client.get_paginator("describe_user_groups")
    describe_users_paginator: DescribeUsersPaginator = client.get_paginator("describe_users")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    CacheClusterMessageTypeDef,
    CacheEngineVersionMessageTypeDef,
    CacheParameterGroupDetailsTypeDef,
    CacheParameterGroupsMessageTypeDef,
    CacheSecurityGroupMessageTypeDef,
    CacheSubnetGroupMessageTypeDef,
    DescribeCacheClustersMessageDescribeCacheClustersPaginateTypeDef,
    DescribeCacheEngineVersionsMessageDescribeCacheEngineVersionsPaginateTypeDef,
    DescribeCacheParameterGroupsMessageDescribeCacheParameterGroupsPaginateTypeDef,
    DescribeCacheParametersMessageDescribeCacheParametersPaginateTypeDef,
    DescribeCacheSecurityGroupsMessageDescribeCacheSecurityGroupsPaginateTypeDef,
    DescribeCacheSubnetGroupsMessageDescribeCacheSubnetGroupsPaginateTypeDef,
    DescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef,
    DescribeEngineDefaultParametersResultTypeDef,
    DescribeEventsMessageDescribeEventsPaginateTypeDef,
    DescribeGlobalReplicationGroupsMessageDescribeGlobalReplicationGroupsPaginateTypeDef,
    DescribeGlobalReplicationGroupsResultTypeDef,
    DescribeReplicationGroupsMessageDescribeReplicationGroupsPaginateTypeDef,
    DescribeReservedCacheNodesMessageDescribeReservedCacheNodesPaginateTypeDef,
    DescribeReservedCacheNodesOfferingsMessageDescribeReservedCacheNodesOfferingsPaginateTypeDef,
    DescribeServerlessCacheSnapshotsRequestDescribeServerlessCacheSnapshotsPaginateTypeDef,
    DescribeServerlessCacheSnapshotsResponseTypeDef,
    DescribeServerlessCachesRequestDescribeServerlessCachesPaginateTypeDef,
    DescribeServerlessCachesResponseTypeDef,
    DescribeServiceUpdatesMessageDescribeServiceUpdatesPaginateTypeDef,
    DescribeSnapshotsListMessageTypeDef,
    DescribeSnapshotsMessageDescribeSnapshotsPaginateTypeDef,
    DescribeUpdateActionsMessageDescribeUpdateActionsPaginateTypeDef,
    DescribeUserGroupsMessageDescribeUserGroupsPaginateTypeDef,
    DescribeUserGroupsResultTypeDef,
    DescribeUsersMessageDescribeUsersPaginateTypeDef,
    DescribeUsersResultTypeDef,
    EventsMessageTypeDef,
    ReplicationGroupMessageTypeDef,
    ReservedCacheNodeMessageTypeDef,
    ReservedCacheNodesOfferingMessageTypeDef,
    ServiceUpdatesMessageTypeDef,
    UpdateActionsMessageTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeCacheClustersPaginator",
    "DescribeCacheEngineVersionsPaginator",
    "DescribeCacheParameterGroupsPaginator",
    "DescribeCacheParametersPaginator",
    "DescribeCacheSecurityGroupsPaginator",
    "DescribeCacheSubnetGroupsPaginator",
    "DescribeEngineDefaultParametersPaginator",
    "DescribeEventsPaginator",
    "DescribeGlobalReplicationGroupsPaginator",
    "DescribeReplicationGroupsPaginator",
    "DescribeReservedCacheNodesOfferingsPaginator",
    "DescribeReservedCacheNodesPaginator",
    "DescribeServerlessCacheSnapshotsPaginator",
    "DescribeServerlessCachesPaginator",
    "DescribeServiceUpdatesPaginator",
    "DescribeSnapshotsPaginator",
    "DescribeUpdateActionsPaginator",
    "DescribeUserGroupsPaginator",
    "DescribeUsersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeCacheClustersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheClusters.html#ElastiCache.Paginator.DescribeCacheClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describecacheclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeCacheClustersMessageDescribeCacheClustersPaginateTypeDef]
    ) -> _PageIterator[CacheClusterMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheClusters.html#ElastiCache.Paginator.DescribeCacheClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describecacheclusterspaginator)
        """

class DescribeCacheEngineVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheEngineVersions.html#ElastiCache.Paginator.DescribeCacheEngineVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describecacheengineversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeCacheEngineVersionsMessageDescribeCacheEngineVersionsPaginateTypeDef
        ],
    ) -> _PageIterator[CacheEngineVersionMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheEngineVersions.html#ElastiCache.Paginator.DescribeCacheEngineVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describecacheengineversionspaginator)
        """

class DescribeCacheParameterGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheParameterGroups.html#ElastiCache.Paginator.DescribeCacheParameterGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describecacheparametergroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeCacheParameterGroupsMessageDescribeCacheParameterGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[CacheParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheParameterGroups.html#ElastiCache.Paginator.DescribeCacheParameterGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describecacheparametergroupspaginator)
        """

class DescribeCacheParametersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheParameters.html#ElastiCache.Paginator.DescribeCacheParameters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describecacheparameterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeCacheParametersMessageDescribeCacheParametersPaginateTypeDef]
    ) -> _PageIterator[CacheParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheParameters.html#ElastiCache.Paginator.DescribeCacheParameters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describecacheparameterspaginator)
        """

class DescribeCacheSecurityGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheSecurityGroups.html#ElastiCache.Paginator.DescribeCacheSecurityGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describecachesecuritygroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeCacheSecurityGroupsMessageDescribeCacheSecurityGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[CacheSecurityGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheSecurityGroups.html#ElastiCache.Paginator.DescribeCacheSecurityGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describecachesecuritygroupspaginator)
        """

class DescribeCacheSubnetGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheSubnetGroups.html#ElastiCache.Paginator.DescribeCacheSubnetGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describecachesubnetgroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeCacheSubnetGroupsMessageDescribeCacheSubnetGroupsPaginateTypeDef],
    ) -> _PageIterator[CacheSubnetGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheSubnetGroups.html#ElastiCache.Paginator.DescribeCacheSubnetGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describecachesubnetgroupspaginator)
        """

class DescribeEngineDefaultParametersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeEngineDefaultParameters.html#ElastiCache.Paginator.DescribeEngineDefaultParameters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeenginedefaultparameterspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeEngineDefaultParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeEngineDefaultParameters.html#ElastiCache.Paginator.DescribeEngineDefaultParameters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeenginedefaultparameterspaginator)
        """

class DescribeEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeEvents.html#ElastiCache.Paginator.DescribeEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeeventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeEventsMessageDescribeEventsPaginateTypeDef]
    ) -> _PageIterator[EventsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeEvents.html#ElastiCache.Paginator.DescribeEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeeventspaginator)
        """

class DescribeGlobalReplicationGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeGlobalReplicationGroups.html#ElastiCache.Paginator.DescribeGlobalReplicationGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeglobalreplicationgroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeGlobalReplicationGroupsMessageDescribeGlobalReplicationGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeGlobalReplicationGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeGlobalReplicationGroups.html#ElastiCache.Paginator.DescribeGlobalReplicationGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeglobalreplicationgroupspaginator)
        """

class DescribeReplicationGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReplicationGroups.html#ElastiCache.Paginator.DescribeReplicationGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describereplicationgroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeReplicationGroupsMessageDescribeReplicationGroupsPaginateTypeDef],
    ) -> _PageIterator[ReplicationGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReplicationGroups.html#ElastiCache.Paginator.DescribeReplicationGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describereplicationgroupspaginator)
        """

class DescribeReservedCacheNodesOfferingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReservedCacheNodesOfferings.html#ElastiCache.Paginator.DescribeReservedCacheNodesOfferings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describereservedcachenodesofferingspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReservedCacheNodesOfferingsMessageDescribeReservedCacheNodesOfferingsPaginateTypeDef
        ],
    ) -> _PageIterator[ReservedCacheNodesOfferingMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReservedCacheNodesOfferings.html#ElastiCache.Paginator.DescribeReservedCacheNodesOfferings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describereservedcachenodesofferingspaginator)
        """

class DescribeReservedCacheNodesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReservedCacheNodes.html#ElastiCache.Paginator.DescribeReservedCacheNodes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describereservedcachenodespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReservedCacheNodesMessageDescribeReservedCacheNodesPaginateTypeDef
        ],
    ) -> _PageIterator[ReservedCacheNodeMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReservedCacheNodes.html#ElastiCache.Paginator.DescribeReservedCacheNodes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describereservedcachenodespaginator)
        """

class DescribeServerlessCacheSnapshotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServerlessCacheSnapshots.html#ElastiCache.Paginator.DescribeServerlessCacheSnapshots)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeserverlesscachesnapshotspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeServerlessCacheSnapshotsRequestDescribeServerlessCacheSnapshotsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeServerlessCacheSnapshotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServerlessCacheSnapshots.html#ElastiCache.Paginator.DescribeServerlessCacheSnapshots.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeserverlesscachesnapshotspaginator)
        """

class DescribeServerlessCachesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServerlessCaches.html#ElastiCache.Paginator.DescribeServerlessCaches)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeserverlesscachespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeServerlessCachesRequestDescribeServerlessCachesPaginateTypeDef],
    ) -> _PageIterator[DescribeServerlessCachesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServerlessCaches.html#ElastiCache.Paginator.DescribeServerlessCaches.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeserverlesscachespaginator)
        """

class DescribeServiceUpdatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServiceUpdates.html#ElastiCache.Paginator.DescribeServiceUpdates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeserviceupdatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeServiceUpdatesMessageDescribeServiceUpdatesPaginateTypeDef]
    ) -> _PageIterator[ServiceUpdatesMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServiceUpdates.html#ElastiCache.Paginator.DescribeServiceUpdates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeserviceupdatespaginator)
        """

class DescribeSnapshotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeSnapshots.html#ElastiCache.Paginator.DescribeSnapshots)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describesnapshotspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeSnapshotsMessageDescribeSnapshotsPaginateTypeDef]
    ) -> _PageIterator[DescribeSnapshotsListMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeSnapshots.html#ElastiCache.Paginator.DescribeSnapshots.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describesnapshotspaginator)
        """

class DescribeUpdateActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUpdateActions.html#ElastiCache.Paginator.DescribeUpdateActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeupdateactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeUpdateActionsMessageDescribeUpdateActionsPaginateTypeDef]
    ) -> _PageIterator[UpdateActionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUpdateActions.html#ElastiCache.Paginator.DescribeUpdateActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeupdateactionspaginator)
        """

class DescribeUserGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUserGroups.html#ElastiCache.Paginator.DescribeUserGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeusergroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeUserGroupsMessageDescribeUserGroupsPaginateTypeDef]
    ) -> _PageIterator[DescribeUserGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUserGroups.html#ElastiCache.Paginator.DescribeUserGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeusergroupspaginator)
        """

class DescribeUsersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUsers.html#ElastiCache.Paginator.DescribeUsers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeuserspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeUsersMessageDescribeUsersPaginateTypeDef]
    ) -> _PageIterator[DescribeUsersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUsers.html#ElastiCache.Paginator.DescribeUsers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/paginators/#describeuserspaginator)
        """
