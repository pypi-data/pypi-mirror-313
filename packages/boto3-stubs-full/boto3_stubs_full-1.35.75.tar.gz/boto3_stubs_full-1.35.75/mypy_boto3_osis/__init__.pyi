"""
Main interface for osis service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_osis import (
        Client,
        OpenSearchIngestionClient,
    )

    session = Session()
    client: OpenSearchIngestionClient = session.client("osis")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import OpenSearchIngestionClient

Client = OpenSearchIngestionClient

__all__ = ("Client", "OpenSearchIngestionClient")
