"""
Type annotations for neptune-graph service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_neptune_graph.client import NeptuneGraphClient
    from mypy_boto3_neptune_graph.paginator import (
        ListExportTasksPaginator,
        ListGraphSnapshotsPaginator,
        ListGraphsPaginator,
        ListImportTasksPaginator,
        ListPrivateGraphEndpointsPaginator,
    )

    session = Session()
    client: NeptuneGraphClient = session.client("neptune-graph")

    list_export_tasks_paginator: ListExportTasksPaginator = client.get_paginator("list_export_tasks")
    list_graph_snapshots_paginator: ListGraphSnapshotsPaginator = client.get_paginator("list_graph_snapshots")
    list_graphs_paginator: ListGraphsPaginator = client.get_paginator("list_graphs")
    list_import_tasks_paginator: ListImportTasksPaginator = client.get_paginator("list_import_tasks")
    list_private_graph_endpoints_paginator: ListPrivateGraphEndpointsPaginator = client.get_paginator("list_private_graph_endpoints")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListExportTasksInputListExportTasksPaginateTypeDef,
    ListExportTasksOutputTypeDef,
    ListGraphsInputListGraphsPaginateTypeDef,
    ListGraphSnapshotsInputListGraphSnapshotsPaginateTypeDef,
    ListGraphSnapshotsOutputTypeDef,
    ListGraphsOutputTypeDef,
    ListImportTasksInputListImportTasksPaginateTypeDef,
    ListImportTasksOutputTypeDef,
    ListPrivateGraphEndpointsInputListPrivateGraphEndpointsPaginateTypeDef,
    ListPrivateGraphEndpointsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListExportTasksPaginator",
    "ListGraphSnapshotsPaginator",
    "ListGraphsPaginator",
    "ListImportTasksPaginator",
    "ListPrivateGraphEndpointsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListExportTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListExportTasks.html#NeptuneGraph.Paginator.ListExportTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/paginators/#listexporttaskspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListExportTasksInputListExportTasksPaginateTypeDef]
    ) -> _PageIterator[ListExportTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListExportTasks.html#NeptuneGraph.Paginator.ListExportTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/paginators/#listexporttaskspaginator)
        """

class ListGraphSnapshotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListGraphSnapshots.html#NeptuneGraph.Paginator.ListGraphSnapshots)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/paginators/#listgraphsnapshotspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGraphSnapshotsInputListGraphSnapshotsPaginateTypeDef]
    ) -> _PageIterator[ListGraphSnapshotsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListGraphSnapshots.html#NeptuneGraph.Paginator.ListGraphSnapshots.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/paginators/#listgraphsnapshotspaginator)
        """

class ListGraphsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListGraphs.html#NeptuneGraph.Paginator.ListGraphs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/paginators/#listgraphspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGraphsInputListGraphsPaginateTypeDef]
    ) -> _PageIterator[ListGraphsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListGraphs.html#NeptuneGraph.Paginator.ListGraphs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/paginators/#listgraphspaginator)
        """

class ListImportTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListImportTasks.html#NeptuneGraph.Paginator.ListImportTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/paginators/#listimporttaskspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListImportTasksInputListImportTasksPaginateTypeDef]
    ) -> _PageIterator[ListImportTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListImportTasks.html#NeptuneGraph.Paginator.ListImportTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/paginators/#listimporttaskspaginator)
        """

class ListPrivateGraphEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListPrivateGraphEndpoints.html#NeptuneGraph.Paginator.ListPrivateGraphEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/paginators/#listprivategraphendpointspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListPrivateGraphEndpointsInputListPrivateGraphEndpointsPaginateTypeDef],
    ) -> _PageIterator[ListPrivateGraphEndpointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListPrivateGraphEndpoints.html#NeptuneGraph.Paginator.ListPrivateGraphEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/paginators/#listprivategraphendpointspaginator)
        """
