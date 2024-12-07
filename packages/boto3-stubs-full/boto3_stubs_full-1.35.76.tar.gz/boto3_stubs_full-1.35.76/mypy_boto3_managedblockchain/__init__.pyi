"""
Main interface for managedblockchain service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_managedblockchain import (
        Client,
        ListAccessorsPaginator,
        ManagedBlockchainClient,
    )

    session = Session()
    client: ManagedBlockchainClient = session.client("managedblockchain")

    list_accessors_paginator: ListAccessorsPaginator = client.get_paginator("list_accessors")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ManagedBlockchainClient
from .paginator import ListAccessorsPaginator

Client = ManagedBlockchainClient

__all__ = ("Client", "ListAccessorsPaginator", "ManagedBlockchainClient")
