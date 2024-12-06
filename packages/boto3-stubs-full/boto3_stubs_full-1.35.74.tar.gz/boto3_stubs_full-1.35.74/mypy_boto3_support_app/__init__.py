"""
Main interface for support-app service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_support_app import (
        Client,
        SupportAppClient,
    )

    session = Session()
    client: SupportAppClient = session.client("support-app")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SupportAppClient

Client = SupportAppClient


__all__ = ("Client", "SupportAppClient")
