"""
Main interface for kinesisanalyticsv2 service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kinesisanalyticsv2 import (
        Client,
        KinesisAnalyticsV2Client,
        ListApplicationOperationsPaginator,
        ListApplicationSnapshotsPaginator,
        ListApplicationVersionsPaginator,
        ListApplicationsPaginator,
    )

    session = Session()
    client: KinesisAnalyticsV2Client = session.client("kinesisanalyticsv2")

    list_application_operations_paginator: ListApplicationOperationsPaginator = client.get_paginator("list_application_operations")
    list_application_snapshots_paginator: ListApplicationSnapshotsPaginator = client.get_paginator("list_application_snapshots")
    list_application_versions_paginator: ListApplicationVersionsPaginator = client.get_paginator("list_application_versions")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import KinesisAnalyticsV2Client
from .paginator import (
    ListApplicationOperationsPaginator,
    ListApplicationSnapshotsPaginator,
    ListApplicationsPaginator,
    ListApplicationVersionsPaginator,
)

Client = KinesisAnalyticsV2Client

__all__ = (
    "Client",
    "KinesisAnalyticsV2Client",
    "ListApplicationOperationsPaginator",
    "ListApplicationSnapshotsPaginator",
    "ListApplicationVersionsPaginator",
    "ListApplicationsPaginator",
)
