"""
Main interface for opensearchserverless service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_opensearchserverless import (
        Client,
        OpenSearchServiceServerlessClient,
    )

    session = Session()
    client: OpenSearchServiceServerlessClient = session.client("opensearchserverless")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import OpenSearchServiceServerlessClient

Client = OpenSearchServiceServerlessClient

__all__ = ("Client", "OpenSearchServiceServerlessClient")
