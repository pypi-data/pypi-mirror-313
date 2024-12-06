"""
Main interface for finspace service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_finspace import (
        Client,
        FinspaceClient,
        ListKxEnvironmentsPaginator,
    )

    session = Session()
    client: FinspaceClient = session.client("finspace")

    list_kx_environments_paginator: ListKxEnvironmentsPaginator = client.get_paginator("list_kx_environments")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import FinspaceClient
from .paginator import ListKxEnvironmentsPaginator

Client = FinspaceClient

__all__ = ("Client", "FinspaceClient", "ListKxEnvironmentsPaginator")
