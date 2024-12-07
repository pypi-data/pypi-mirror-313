"""
Type annotations for dms service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_dms.client import DatabaseMigrationServiceClient
    from mypy_boto3_dms.paginator import (
        DescribeCertificatesPaginator,
        DescribeConnectionsPaginator,
        DescribeDataMigrationsPaginator,
        DescribeEndpointTypesPaginator,
        DescribeEndpointsPaginator,
        DescribeEventSubscriptionsPaginator,
        DescribeEventsPaginator,
        DescribeOrderableReplicationInstancesPaginator,
        DescribeReplicationInstancesPaginator,
        DescribeReplicationSubnetGroupsPaginator,
        DescribeReplicationTaskAssessmentResultsPaginator,
        DescribeReplicationTasksPaginator,
        DescribeSchemasPaginator,
        DescribeTableStatisticsPaginator,
    )

    session = Session()
    client: DatabaseMigrationServiceClient = session.client("dms")

    describe_certificates_paginator: DescribeCertificatesPaginator = client.get_paginator("describe_certificates")
    describe_connections_paginator: DescribeConnectionsPaginator = client.get_paginator("describe_connections")
    describe_data_migrations_paginator: DescribeDataMigrationsPaginator = client.get_paginator("describe_data_migrations")
    describe_endpoint_types_paginator: DescribeEndpointTypesPaginator = client.get_paginator("describe_endpoint_types")
    describe_endpoints_paginator: DescribeEndpointsPaginator = client.get_paginator("describe_endpoints")
    describe_event_subscriptions_paginator: DescribeEventSubscriptionsPaginator = client.get_paginator("describe_event_subscriptions")
    describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
    describe_orderable_replication_instances_paginator: DescribeOrderableReplicationInstancesPaginator = client.get_paginator("describe_orderable_replication_instances")
    describe_replication_instances_paginator: DescribeReplicationInstancesPaginator = client.get_paginator("describe_replication_instances")
    describe_replication_subnet_groups_paginator: DescribeReplicationSubnetGroupsPaginator = client.get_paginator("describe_replication_subnet_groups")
    describe_replication_task_assessment_results_paginator: DescribeReplicationTaskAssessmentResultsPaginator = client.get_paginator("describe_replication_task_assessment_results")
    describe_replication_tasks_paginator: DescribeReplicationTasksPaginator = client.get_paginator("describe_replication_tasks")
    describe_schemas_paginator: DescribeSchemasPaginator = client.get_paginator("describe_schemas")
    describe_table_statistics_paginator: DescribeTableStatisticsPaginator = client.get_paginator("describe_table_statistics")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef,
    DescribeCertificatesResponseTypeDef,
    DescribeConnectionsMessageDescribeConnectionsPaginateTypeDef,
    DescribeConnectionsResponseTypeDef,
    DescribeDataMigrationsMessageDescribeDataMigrationsPaginateTypeDef,
    DescribeDataMigrationsResponseTypeDef,
    DescribeEndpointsMessageDescribeEndpointsPaginateTypeDef,
    DescribeEndpointsResponseTypeDef,
    DescribeEndpointTypesMessageDescribeEndpointTypesPaginateTypeDef,
    DescribeEndpointTypesResponseTypeDef,
    DescribeEventsMessageDescribeEventsPaginateTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef,
    DescribeEventSubscriptionsResponseTypeDef,
    DescribeOrderableReplicationInstancesMessageDescribeOrderableReplicationInstancesPaginateTypeDef,
    DescribeOrderableReplicationInstancesResponseTypeDef,
    DescribeReplicationInstancesMessageDescribeReplicationInstancesPaginateTypeDef,
    DescribeReplicationInstancesResponseTypeDef,
    DescribeReplicationSubnetGroupsMessageDescribeReplicationSubnetGroupsPaginateTypeDef,
    DescribeReplicationSubnetGroupsResponseTypeDef,
    DescribeReplicationTaskAssessmentResultsMessageDescribeReplicationTaskAssessmentResultsPaginateTypeDef,
    DescribeReplicationTaskAssessmentResultsResponseTypeDef,
    DescribeReplicationTasksMessageDescribeReplicationTasksPaginateTypeDef,
    DescribeReplicationTasksResponseTypeDef,
    DescribeSchemasMessageDescribeSchemasPaginateTypeDef,
    DescribeSchemasResponseTypeDef,
    DescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef,
    DescribeTableStatisticsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeCertificatesPaginator",
    "DescribeConnectionsPaginator",
    "DescribeDataMigrationsPaginator",
    "DescribeEndpointTypesPaginator",
    "DescribeEndpointsPaginator",
    "DescribeEventSubscriptionsPaginator",
    "DescribeEventsPaginator",
    "DescribeOrderableReplicationInstancesPaginator",
    "DescribeReplicationInstancesPaginator",
    "DescribeReplicationSubnetGroupsPaginator",
    "DescribeReplicationTaskAssessmentResultsPaginator",
    "DescribeReplicationTasksPaginator",
    "DescribeSchemasPaginator",
    "DescribeTableStatisticsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeCertificatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeCertificates.html#DatabaseMigrationService.Paginator.DescribeCertificates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describecertificatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef]
    ) -> _PageIterator[DescribeCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeCertificates.html#DatabaseMigrationService.Paginator.DescribeCertificates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describecertificatespaginator)
        """

class DescribeConnectionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeConnections.html#DatabaseMigrationService.Paginator.DescribeConnections)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describeconnectionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeConnectionsMessageDescribeConnectionsPaginateTypeDef]
    ) -> _PageIterator[DescribeConnectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeConnections.html#DatabaseMigrationService.Paginator.DescribeConnections.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describeconnectionspaginator)
        """

class DescribeDataMigrationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeDataMigrations.html#DatabaseMigrationService.Paginator.DescribeDataMigrations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describedatamigrationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeDataMigrationsMessageDescribeDataMigrationsPaginateTypeDef]
    ) -> _PageIterator[DescribeDataMigrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeDataMigrations.html#DatabaseMigrationService.Paginator.DescribeDataMigrations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describedatamigrationspaginator)
        """

class DescribeEndpointTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeEndpointTypes.html#DatabaseMigrationService.Paginator.DescribeEndpointTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describeendpointtypespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeEndpointTypesMessageDescribeEndpointTypesPaginateTypeDef]
    ) -> _PageIterator[DescribeEndpointTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeEndpointTypes.html#DatabaseMigrationService.Paginator.DescribeEndpointTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describeendpointtypespaginator)
        """

class DescribeEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeEndpoints.html#DatabaseMigrationService.Paginator.DescribeEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describeendpointspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeEndpointsMessageDescribeEndpointsPaginateTypeDef]
    ) -> _PageIterator[DescribeEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeEndpoints.html#DatabaseMigrationService.Paginator.DescribeEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describeendpointspaginator)
        """

class DescribeEventSubscriptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeEventSubscriptions.html#DatabaseMigrationService.Paginator.DescribeEventSubscriptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describeeventsubscriptionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeEventSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeEventSubscriptions.html#DatabaseMigrationService.Paginator.DescribeEventSubscriptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describeeventsubscriptionspaginator)
        """

class DescribeEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeEvents.html#DatabaseMigrationService.Paginator.DescribeEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describeeventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeEventsMessageDescribeEventsPaginateTypeDef]
    ) -> _PageIterator[DescribeEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeEvents.html#DatabaseMigrationService.Paginator.DescribeEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describeeventspaginator)
        """

class DescribeOrderableReplicationInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeOrderableReplicationInstances.html#DatabaseMigrationService.Paginator.DescribeOrderableReplicationInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describeorderablereplicationinstancespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeOrderableReplicationInstancesMessageDescribeOrderableReplicationInstancesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeOrderableReplicationInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeOrderableReplicationInstances.html#DatabaseMigrationService.Paginator.DescribeOrderableReplicationInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describeorderablereplicationinstancespaginator)
        """

class DescribeReplicationInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeReplicationInstances.html#DatabaseMigrationService.Paginator.DescribeReplicationInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describereplicationinstancespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReplicationInstancesMessageDescribeReplicationInstancesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeReplicationInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeReplicationInstances.html#DatabaseMigrationService.Paginator.DescribeReplicationInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describereplicationinstancespaginator)
        """

class DescribeReplicationSubnetGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeReplicationSubnetGroups.html#DatabaseMigrationService.Paginator.DescribeReplicationSubnetGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describereplicationsubnetgroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReplicationSubnetGroupsMessageDescribeReplicationSubnetGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeReplicationSubnetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeReplicationSubnetGroups.html#DatabaseMigrationService.Paginator.DescribeReplicationSubnetGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describereplicationsubnetgroupspaginator)
        """

class DescribeReplicationTaskAssessmentResultsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeReplicationTaskAssessmentResults.html#DatabaseMigrationService.Paginator.DescribeReplicationTaskAssessmentResults)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describereplicationtaskassessmentresultspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReplicationTaskAssessmentResultsMessageDescribeReplicationTaskAssessmentResultsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeReplicationTaskAssessmentResultsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeReplicationTaskAssessmentResults.html#DatabaseMigrationService.Paginator.DescribeReplicationTaskAssessmentResults.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describereplicationtaskassessmentresultspaginator)
        """

class DescribeReplicationTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeReplicationTasks.html#DatabaseMigrationService.Paginator.DescribeReplicationTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describereplicationtaskspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeReplicationTasksMessageDescribeReplicationTasksPaginateTypeDef],
    ) -> _PageIterator[DescribeReplicationTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeReplicationTasks.html#DatabaseMigrationService.Paginator.DescribeReplicationTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describereplicationtaskspaginator)
        """

class DescribeSchemasPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeSchemas.html#DatabaseMigrationService.Paginator.DescribeSchemas)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describeschemaspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeSchemasMessageDescribeSchemasPaginateTypeDef]
    ) -> _PageIterator[DescribeSchemasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeSchemas.html#DatabaseMigrationService.Paginator.DescribeSchemas.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describeschemaspaginator)
        """

class DescribeTableStatisticsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeTableStatistics.html#DatabaseMigrationService.Paginator.DescribeTableStatistics)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describetablestatisticspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef]
    ) -> _PageIterator[DescribeTableStatisticsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeTableStatistics.html#DatabaseMigrationService.Paginator.DescribeTableStatistics.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/paginators/#describetablestatisticspaginator)
        """
