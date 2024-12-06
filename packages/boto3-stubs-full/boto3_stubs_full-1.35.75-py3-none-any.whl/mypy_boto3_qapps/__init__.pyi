"""
Main interface for qapps service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_qapps import (
        Client,
        ListLibraryItemsPaginator,
        ListQAppsPaginator,
        QAppsClient,
    )

    session = Session()
    client: QAppsClient = session.client("qapps")

    list_library_items_paginator: ListLibraryItemsPaginator = client.get_paginator("list_library_items")
    list_q_apps_paginator: ListQAppsPaginator = client.get_paginator("list_q_apps")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import QAppsClient
from .paginator import ListLibraryItemsPaginator, ListQAppsPaginator

Client = QAppsClient

__all__ = ("Client", "ListLibraryItemsPaginator", "ListQAppsPaginator", "QAppsClient")
