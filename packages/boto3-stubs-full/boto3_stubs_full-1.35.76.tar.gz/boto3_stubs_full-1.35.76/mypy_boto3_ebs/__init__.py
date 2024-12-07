"""
Main interface for ebs service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_ebs import (
        Client,
        EBSClient,
    )

    session = Session()
    client: EBSClient = session.client("ebs")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import EBSClient

Client = EBSClient


__all__ = ("Client", "EBSClient")
