"""
Type annotations for docdb service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_docdb.client import DocDBClient
    from mypy_boto3_docdb.paginator import (
        DescribeCertificatesPaginator,
        DescribeDBClusterParameterGroupsPaginator,
        DescribeDBClusterParametersPaginator,
        DescribeDBClusterSnapshotsPaginator,
        DescribeDBClustersPaginator,
        DescribeDBEngineVersionsPaginator,
        DescribeDBInstancesPaginator,
        DescribeDBSubnetGroupsPaginator,
        DescribeEventSubscriptionsPaginator,
        DescribeEventsPaginator,
        DescribeGlobalClustersPaginator,
        DescribeOrderableDBInstanceOptionsPaginator,
        DescribePendingMaintenanceActionsPaginator,
    )

    session = Session()
    client: DocDBClient = session.client("docdb")

    describe_certificates_paginator: DescribeCertificatesPaginator = client.get_paginator("describe_certificates")
    describe_db_cluster_parameter_groups_paginator: DescribeDBClusterParameterGroupsPaginator = client.get_paginator("describe_db_cluster_parameter_groups")
    describe_db_cluster_parameters_paginator: DescribeDBClusterParametersPaginator = client.get_paginator("describe_db_cluster_parameters")
    describe_db_cluster_snapshots_paginator: DescribeDBClusterSnapshotsPaginator = client.get_paginator("describe_db_cluster_snapshots")
    describe_db_clusters_paginator: DescribeDBClustersPaginator = client.get_paginator("describe_db_clusters")
    describe_db_engine_versions_paginator: DescribeDBEngineVersionsPaginator = client.get_paginator("describe_db_engine_versions")
    describe_db_instances_paginator: DescribeDBInstancesPaginator = client.get_paginator("describe_db_instances")
    describe_db_subnet_groups_paginator: DescribeDBSubnetGroupsPaginator = client.get_paginator("describe_db_subnet_groups")
    describe_event_subscriptions_paginator: DescribeEventSubscriptionsPaginator = client.get_paginator("describe_event_subscriptions")
    describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
    describe_global_clusters_paginator: DescribeGlobalClustersPaginator = client.get_paginator("describe_global_clusters")
    describe_orderable_db_instance_options_paginator: DescribeOrderableDBInstanceOptionsPaginator = client.get_paginator("describe_orderable_db_instance_options")
    describe_pending_maintenance_actions_paginator: DescribePendingMaintenanceActionsPaginator = client.get_paginator("describe_pending_maintenance_actions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    CertificateMessageTypeDef,
    DBClusterMessageTypeDef,
    DBClusterParameterGroupDetailsTypeDef,
    DBClusterParameterGroupsMessageTypeDef,
    DBClusterSnapshotMessageTypeDef,
    DBEngineVersionMessageTypeDef,
    DBInstanceMessageTypeDef,
    DBSubnetGroupMessageTypeDef,
    DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef,
    DescribeDBClusterParameterGroupsMessageDescribeDBClusterParameterGroupsPaginateTypeDef,
    DescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef,
    DescribeDBClustersMessageDescribeDBClustersPaginateTypeDef,
    DescribeDBClusterSnapshotsMessageDescribeDBClusterSnapshotsPaginateTypeDef,
    DescribeDBEngineVersionsMessageDescribeDBEngineVersionsPaginateTypeDef,
    DescribeDBInstancesMessageDescribeDBInstancesPaginateTypeDef,
    DescribeDBSubnetGroupsMessageDescribeDBSubnetGroupsPaginateTypeDef,
    DescribeEventsMessageDescribeEventsPaginateTypeDef,
    DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef,
    DescribeGlobalClustersMessageDescribeGlobalClustersPaginateTypeDef,
    DescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef,
    DescribePendingMaintenanceActionsMessageDescribePendingMaintenanceActionsPaginateTypeDef,
    EventsMessageTypeDef,
    EventSubscriptionsMessageTypeDef,
    GlobalClustersMessageTypeDef,
    OrderableDBInstanceOptionsMessageTypeDef,
    PendingMaintenanceActionsMessageTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeCertificatesPaginator",
    "DescribeDBClusterParameterGroupsPaginator",
    "DescribeDBClusterParametersPaginator",
    "DescribeDBClusterSnapshotsPaginator",
    "DescribeDBClustersPaginator",
    "DescribeDBEngineVersionsPaginator",
    "DescribeDBInstancesPaginator",
    "DescribeDBSubnetGroupsPaginator",
    "DescribeEventSubscriptionsPaginator",
    "DescribeEventsPaginator",
    "DescribeGlobalClustersPaginator",
    "DescribeOrderableDBInstanceOptionsPaginator",
    "DescribePendingMaintenanceActionsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeCertificatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeCertificates.html#DocDB.Paginator.DescribeCertificates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describecertificatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef]
    ) -> _PageIterator[CertificateMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeCertificates.html#DocDB.Paginator.DescribeCertificates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describecertificatespaginator)
        """

class DescribeDBClusterParameterGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterParameterGroups.html#DocDB.Paginator.DescribeDBClusterParameterGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbclusterparametergroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeDBClusterParameterGroupsMessageDescribeDBClusterParameterGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[DBClusterParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterParameterGroups.html#DocDB.Paginator.DescribeDBClusterParameterGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbclusterparametergroupspaginator)
        """

class DescribeDBClusterParametersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterParameters.html#DocDB.Paginator.DescribeDBClusterParameters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbclusterparameterspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef
        ],
    ) -> _PageIterator[DBClusterParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterParameters.html#DocDB.Paginator.DescribeDBClusterParameters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbclusterparameterspaginator)
        """

class DescribeDBClusterSnapshotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterSnapshots.html#DocDB.Paginator.DescribeDBClusterSnapshots)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbclustersnapshotspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeDBClusterSnapshotsMessageDescribeDBClusterSnapshotsPaginateTypeDef
        ],
    ) -> _PageIterator[DBClusterSnapshotMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterSnapshots.html#DocDB.Paginator.DescribeDBClusterSnapshots.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbclustersnapshotspaginator)
        """

class DescribeDBClustersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusters.html#DocDB.Paginator.DescribeDBClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeDBClustersMessageDescribeDBClustersPaginateTypeDef]
    ) -> _PageIterator[DBClusterMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusters.html#DocDB.Paginator.DescribeDBClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbclusterspaginator)
        """

class DescribeDBEngineVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBEngineVersions.html#DocDB.Paginator.DescribeDBEngineVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbengineversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeDBEngineVersionsMessageDescribeDBEngineVersionsPaginateTypeDef],
    ) -> _PageIterator[DBEngineVersionMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBEngineVersions.html#DocDB.Paginator.DescribeDBEngineVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbengineversionspaginator)
        """

class DescribeDBInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBInstances.html#DocDB.Paginator.DescribeDBInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbinstancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeDBInstancesMessageDescribeDBInstancesPaginateTypeDef]
    ) -> _PageIterator[DBInstanceMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBInstances.html#DocDB.Paginator.DescribeDBInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbinstancespaginator)
        """

class DescribeDBSubnetGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBSubnetGroups.html#DocDB.Paginator.DescribeDBSubnetGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbsubnetgroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeDBSubnetGroupsMessageDescribeDBSubnetGroupsPaginateTypeDef]
    ) -> _PageIterator[DBSubnetGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBSubnetGroups.html#DocDB.Paginator.DescribeDBSubnetGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbsubnetgroupspaginator)
        """

class DescribeEventSubscriptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeEventSubscriptions.html#DocDB.Paginator.DescribeEventSubscriptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describeeventsubscriptionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef
        ],
    ) -> _PageIterator[EventSubscriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeEventSubscriptions.html#DocDB.Paginator.DescribeEventSubscriptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describeeventsubscriptionspaginator)
        """

class DescribeEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeEvents.html#DocDB.Paginator.DescribeEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describeeventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeEventsMessageDescribeEventsPaginateTypeDef]
    ) -> _PageIterator[EventsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeEvents.html#DocDB.Paginator.DescribeEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describeeventspaginator)
        """

class DescribeGlobalClustersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeGlobalClusters.html#DocDB.Paginator.DescribeGlobalClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describeglobalclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeGlobalClustersMessageDescribeGlobalClustersPaginateTypeDef]
    ) -> _PageIterator[GlobalClustersMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeGlobalClusters.html#DocDB.Paginator.DescribeGlobalClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describeglobalclusterspaginator)
        """

class DescribeOrderableDBInstanceOptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeOrderableDBInstanceOptions.html#DocDB.Paginator.DescribeOrderableDBInstanceOptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describeorderabledbinstanceoptionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef
        ],
    ) -> _PageIterator[OrderableDBInstanceOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeOrderableDBInstanceOptions.html#DocDB.Paginator.DescribeOrderableDBInstanceOptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describeorderabledbinstanceoptionspaginator)
        """

class DescribePendingMaintenanceActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribePendingMaintenanceActions.html#DocDB.Paginator.DescribePendingMaintenanceActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describependingmaintenanceactionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribePendingMaintenanceActionsMessageDescribePendingMaintenanceActionsPaginateTypeDef
        ],
    ) -> _PageIterator[PendingMaintenanceActionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribePendingMaintenanceActions.html#DocDB.Paginator.DescribePendingMaintenanceActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describependingmaintenanceactionspaginator)
        """
