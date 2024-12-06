"""
Main interface for inspector-scan service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_inspector_scan import (
        Client,
        InspectorscanClient,
    )

    session = Session()
    client: InspectorscanClient = session.client("inspector-scan")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import InspectorscanClient

Client = InspectorscanClient


__all__ = ("Client", "InspectorscanClient")
