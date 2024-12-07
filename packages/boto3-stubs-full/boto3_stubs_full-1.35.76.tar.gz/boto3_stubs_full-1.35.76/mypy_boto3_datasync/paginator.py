"""
Type annotations for datasync service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_datasync.client import DataSyncClient
    from mypy_boto3_datasync.paginator import (
        DescribeStorageSystemResourceMetricsPaginator,
        ListAgentsPaginator,
        ListDiscoveryJobsPaginator,
        ListLocationsPaginator,
        ListStorageSystemsPaginator,
        ListTagsForResourcePaginator,
        ListTaskExecutionsPaginator,
        ListTasksPaginator,
    )

    session = Session()
    client: DataSyncClient = session.client("datasync")

    describe_storage_system_resource_metrics_paginator: DescribeStorageSystemResourceMetricsPaginator = client.get_paginator("describe_storage_system_resource_metrics")
    list_agents_paginator: ListAgentsPaginator = client.get_paginator("list_agents")
    list_discovery_jobs_paginator: ListDiscoveryJobsPaginator = client.get_paginator("list_discovery_jobs")
    list_locations_paginator: ListLocationsPaginator = client.get_paginator("list_locations")
    list_storage_systems_paginator: ListStorageSystemsPaginator = client.get_paginator("list_storage_systems")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    list_task_executions_paginator: ListTaskExecutionsPaginator = client.get_paginator("list_task_executions")
    list_tasks_paginator: ListTasksPaginator = client.get_paginator("list_tasks")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeStorageSystemResourceMetricsRequestDescribeStorageSystemResourceMetricsPaginateTypeDef,
    DescribeStorageSystemResourceMetricsResponseTypeDef,
    ListAgentsRequestListAgentsPaginateTypeDef,
    ListAgentsResponseTypeDef,
    ListDiscoveryJobsRequestListDiscoveryJobsPaginateTypeDef,
    ListDiscoveryJobsResponseTypeDef,
    ListLocationsRequestListLocationsPaginateTypeDef,
    ListLocationsResponseTypeDef,
    ListStorageSystemsRequestListStorageSystemsPaginateTypeDef,
    ListStorageSystemsResponseTypeDef,
    ListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTaskExecutionsRequestListTaskExecutionsPaginateTypeDef,
    ListTaskExecutionsResponseTypeDef,
    ListTasksRequestListTasksPaginateTypeDef,
    ListTasksResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeStorageSystemResourceMetricsPaginator",
    "ListAgentsPaginator",
    "ListDiscoveryJobsPaginator",
    "ListLocationsPaginator",
    "ListStorageSystemsPaginator",
    "ListTagsForResourcePaginator",
    "ListTaskExecutionsPaginator",
    "ListTasksPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeStorageSystemResourceMetricsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/DescribeStorageSystemResourceMetrics.html#DataSync.Paginator.DescribeStorageSystemResourceMetrics)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/paginators/#describestoragesystemresourcemetricspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeStorageSystemResourceMetricsRequestDescribeStorageSystemResourceMetricsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeStorageSystemResourceMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/DescribeStorageSystemResourceMetrics.html#DataSync.Paginator.DescribeStorageSystemResourceMetrics.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/paginators/#describestoragesystemresourcemetricspaginator)
        """


class ListAgentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListAgents.html#DataSync.Paginator.ListAgents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/paginators/#listagentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAgentsRequestListAgentsPaginateTypeDef]
    ) -> _PageIterator[ListAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListAgents.html#DataSync.Paginator.ListAgents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/paginators/#listagentspaginator)
        """


class ListDiscoveryJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListDiscoveryJobs.html#DataSync.Paginator.ListDiscoveryJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/paginators/#listdiscoveryjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDiscoveryJobsRequestListDiscoveryJobsPaginateTypeDef]
    ) -> _PageIterator[ListDiscoveryJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListDiscoveryJobs.html#DataSync.Paginator.ListDiscoveryJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/paginators/#listdiscoveryjobspaginator)
        """


class ListLocationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListLocations.html#DataSync.Paginator.ListLocations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/paginators/#listlocationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListLocationsRequestListLocationsPaginateTypeDef]
    ) -> _PageIterator[ListLocationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListLocations.html#DataSync.Paginator.ListLocations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/paginators/#listlocationspaginator)
        """


class ListStorageSystemsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListStorageSystems.html#DataSync.Paginator.ListStorageSystems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/paginators/#liststoragesystemspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStorageSystemsRequestListStorageSystemsPaginateTypeDef]
    ) -> _PageIterator[ListStorageSystemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListStorageSystems.html#DataSync.Paginator.ListStorageSystems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/paginators/#liststoragesystemspaginator)
        """


class ListTagsForResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListTagsForResource.html#DataSync.Paginator.ListTagsForResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceRequestListTagsForResourcePaginateTypeDef]
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListTagsForResource.html#DataSync.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/paginators/#listtagsforresourcepaginator)
        """


class ListTaskExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListTaskExecutions.html#DataSync.Paginator.ListTaskExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/paginators/#listtaskexecutionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTaskExecutionsRequestListTaskExecutionsPaginateTypeDef]
    ) -> _PageIterator[ListTaskExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListTaskExecutions.html#DataSync.Paginator.ListTaskExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/paginators/#listtaskexecutionspaginator)
        """


class ListTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListTasks.html#DataSync.Paginator.ListTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/paginators/#listtaskspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTasksRequestListTasksPaginateTypeDef]
    ) -> _PageIterator[ListTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListTasks.html#DataSync.Paginator.ListTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/paginators/#listtaskspaginator)
        """
