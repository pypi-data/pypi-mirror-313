"""
Main interface for kendra service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kendra import (
        Client,
        KendraClient,
    )

    session = Session()
    client: KendraClient = session.client("kendra")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import KendraClient

Client = KendraClient

__all__ = ("Client", "KendraClient")
