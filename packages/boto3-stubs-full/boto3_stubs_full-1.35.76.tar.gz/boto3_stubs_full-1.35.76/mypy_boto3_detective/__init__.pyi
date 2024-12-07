"""
Main interface for detective service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_detective import (
        Client,
        DetectiveClient,
    )

    session = Session()
    client: DetectiveClient = session.client("detective")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import DetectiveClient

Client = DetectiveClient

__all__ = ("Client", "DetectiveClient")
