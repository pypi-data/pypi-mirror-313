"""
Main interface for pipes service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_pipes import (
        Client,
        EventBridgePipesClient,
        ListPipesPaginator,
    )

    session = Session()
    client: EventBridgePipesClient = session.client("pipes")

    list_pipes_paginator: ListPipesPaginator = client.get_paginator("list_pipes")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import EventBridgePipesClient
from .paginator import ListPipesPaginator

Client = EventBridgePipesClient


__all__ = ("Client", "EventBridgePipesClient", "ListPipesPaginator")
