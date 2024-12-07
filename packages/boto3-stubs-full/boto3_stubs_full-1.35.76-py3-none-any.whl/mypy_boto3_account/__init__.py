"""
Main interface for account service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_account import (
        AccountClient,
        Client,
        ListRegionsPaginator,
    )

    session = Session()
    client: AccountClient = session.client("account")

    list_regions_paginator: ListRegionsPaginator = client.get_paginator("list_regions")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import AccountClient
from .paginator import ListRegionsPaginator

Client = AccountClient


__all__ = ("AccountClient", "Client", "ListRegionsPaginator")
