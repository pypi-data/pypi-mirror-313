"""
Type annotations for neptune-graph service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_neptune_graph.client import NeptuneGraphClient
    from mypy_boto3_neptune_graph.waiter import (
        ExportTaskCancelledWaiter,
        ExportTaskSuccessfulWaiter,
        GraphAvailableWaiter,
        GraphDeletedWaiter,
        GraphSnapshotAvailableWaiter,
        GraphSnapshotDeletedWaiter,
        ImportTaskCancelledWaiter,
        ImportTaskSuccessfulWaiter,
        PrivateGraphEndpointAvailableWaiter,
        PrivateGraphEndpointDeletedWaiter,
    )

    session = Session()
    client: NeptuneGraphClient = session.client("neptune-graph")

    export_task_cancelled_waiter: ExportTaskCancelledWaiter = client.get_waiter("export_task_cancelled")
    export_task_successful_waiter: ExportTaskSuccessfulWaiter = client.get_waiter("export_task_successful")
    graph_available_waiter: GraphAvailableWaiter = client.get_waiter("graph_available")
    graph_deleted_waiter: GraphDeletedWaiter = client.get_waiter("graph_deleted")
    graph_snapshot_available_waiter: GraphSnapshotAvailableWaiter = client.get_waiter("graph_snapshot_available")
    graph_snapshot_deleted_waiter: GraphSnapshotDeletedWaiter = client.get_waiter("graph_snapshot_deleted")
    import_task_cancelled_waiter: ImportTaskCancelledWaiter = client.get_waiter("import_task_cancelled")
    import_task_successful_waiter: ImportTaskSuccessfulWaiter = client.get_waiter("import_task_successful")
    private_graph_endpoint_available_waiter: PrivateGraphEndpointAvailableWaiter = client.get_waiter("private_graph_endpoint_available")
    private_graph_endpoint_deleted_waiter: PrivateGraphEndpointDeletedWaiter = client.get_waiter("private_graph_endpoint_deleted")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import (
    GetExportTaskInputExportTaskCancelledWaitTypeDef,
    GetExportTaskInputExportTaskSuccessfulWaitTypeDef,
    GetGraphInputGraphAvailableWaitTypeDef,
    GetGraphInputGraphDeletedWaitTypeDef,
    GetGraphSnapshotInputGraphSnapshotAvailableWaitTypeDef,
    GetGraphSnapshotInputGraphSnapshotDeletedWaitTypeDef,
    GetImportTaskInputImportTaskCancelledWaitTypeDef,
    GetImportTaskInputImportTaskSuccessfulWaitTypeDef,
    GetPrivateGraphEndpointInputPrivateGraphEndpointAvailableWaitTypeDef,
    GetPrivateGraphEndpointInputPrivateGraphEndpointDeletedWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ExportTaskCancelledWaiter",
    "ExportTaskSuccessfulWaiter",
    "GraphAvailableWaiter",
    "GraphDeletedWaiter",
    "GraphSnapshotAvailableWaiter",
    "GraphSnapshotDeletedWaiter",
    "ImportTaskCancelledWaiter",
    "ImportTaskSuccessfulWaiter",
    "PrivateGraphEndpointAvailableWaiter",
    "PrivateGraphEndpointDeletedWaiter",
)


class ExportTaskCancelledWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/ExportTaskCancelled.html#NeptuneGraph.Waiter.ExportTaskCancelled)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#exporttaskcancelledwaiter)
    """

    def wait(self, **kwargs: Unpack[GetExportTaskInputExportTaskCancelledWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/ExportTaskCancelled.html#NeptuneGraph.Waiter.ExportTaskCancelled.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#exporttaskcancelledwaiter)
        """


class ExportTaskSuccessfulWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/ExportTaskSuccessful.html#NeptuneGraph.Waiter.ExportTaskSuccessful)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#exporttasksuccessfulwaiter)
    """

    def wait(self, **kwargs: Unpack[GetExportTaskInputExportTaskSuccessfulWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/ExportTaskSuccessful.html#NeptuneGraph.Waiter.ExportTaskSuccessful.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#exporttasksuccessfulwaiter)
        """


class GraphAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/GraphAvailable.html#NeptuneGraph.Waiter.GraphAvailable)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#graphavailablewaiter)
    """

    def wait(self, **kwargs: Unpack[GetGraphInputGraphAvailableWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/GraphAvailable.html#NeptuneGraph.Waiter.GraphAvailable.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#graphavailablewaiter)
        """


class GraphDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/GraphDeleted.html#NeptuneGraph.Waiter.GraphDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#graphdeletedwaiter)
    """

    def wait(self, **kwargs: Unpack[GetGraphInputGraphDeletedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/GraphDeleted.html#NeptuneGraph.Waiter.GraphDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#graphdeletedwaiter)
        """


class GraphSnapshotAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/GraphSnapshotAvailable.html#NeptuneGraph.Waiter.GraphSnapshotAvailable)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#graphsnapshotavailablewaiter)
    """

    def wait(
        self, **kwargs: Unpack[GetGraphSnapshotInputGraphSnapshotAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/GraphSnapshotAvailable.html#NeptuneGraph.Waiter.GraphSnapshotAvailable.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#graphsnapshotavailablewaiter)
        """


class GraphSnapshotDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/GraphSnapshotDeleted.html#NeptuneGraph.Waiter.GraphSnapshotDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#graphsnapshotdeletedwaiter)
    """

    def wait(self, **kwargs: Unpack[GetGraphSnapshotInputGraphSnapshotDeletedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/GraphSnapshotDeleted.html#NeptuneGraph.Waiter.GraphSnapshotDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#graphsnapshotdeletedwaiter)
        """


class ImportTaskCancelledWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/ImportTaskCancelled.html#NeptuneGraph.Waiter.ImportTaskCancelled)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#importtaskcancelledwaiter)
    """

    def wait(self, **kwargs: Unpack[GetImportTaskInputImportTaskCancelledWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/ImportTaskCancelled.html#NeptuneGraph.Waiter.ImportTaskCancelled.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#importtaskcancelledwaiter)
        """


class ImportTaskSuccessfulWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/ImportTaskSuccessful.html#NeptuneGraph.Waiter.ImportTaskSuccessful)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#importtasksuccessfulwaiter)
    """

    def wait(self, **kwargs: Unpack[GetImportTaskInputImportTaskSuccessfulWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/ImportTaskSuccessful.html#NeptuneGraph.Waiter.ImportTaskSuccessful.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#importtasksuccessfulwaiter)
        """


class PrivateGraphEndpointAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/PrivateGraphEndpointAvailable.html#NeptuneGraph.Waiter.PrivateGraphEndpointAvailable)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#privategraphendpointavailablewaiter)
    """

    def wait(
        self, **kwargs: Unpack[GetPrivateGraphEndpointInputPrivateGraphEndpointAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/PrivateGraphEndpointAvailable.html#NeptuneGraph.Waiter.PrivateGraphEndpointAvailable.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#privategraphendpointavailablewaiter)
        """


class PrivateGraphEndpointDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/PrivateGraphEndpointDeleted.html#NeptuneGraph.Waiter.PrivateGraphEndpointDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#privategraphendpointdeletedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[GetPrivateGraphEndpointInputPrivateGraphEndpointDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/waiter/PrivateGraphEndpointDeleted.html#NeptuneGraph.Waiter.PrivateGraphEndpointDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune_graph/waiters/#privategraphendpointdeletedwaiter)
        """
