"""
Main interface for dsql service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_dsql import (
        AuroraDSQLClient,
        Client,
        ClusterActiveWaiter,
        ClusterNotExistsWaiter,
        ListClustersPaginator,
    )

    session = Session()
    client: AuroraDSQLClient = session.client("dsql")

    cluster_active_waiter: ClusterActiveWaiter = client.get_waiter("cluster_active")
    cluster_not_exists_waiter: ClusterNotExistsWaiter = client.get_waiter("cluster_not_exists")

    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import AuroraDSQLClient
from .paginator import ListClustersPaginator
from .waiter import ClusterActiveWaiter, ClusterNotExistsWaiter

Client = AuroraDSQLClient

__all__ = (
    "AuroraDSQLClient",
    "Client",
    "ClusterActiveWaiter",
    "ClusterNotExistsWaiter",
    "ListClustersPaginator",
)
