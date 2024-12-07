"""
Main interface for frauddetector service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_frauddetector import (
        Client,
        FraudDetectorClient,
    )

    session = Session()
    client: FraudDetectorClient = session.client("frauddetector")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import FraudDetectorClient

Client = FraudDetectorClient


__all__ = ("Client", "FraudDetectorClient")
