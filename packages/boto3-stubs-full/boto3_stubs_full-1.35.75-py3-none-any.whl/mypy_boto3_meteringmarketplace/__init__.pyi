"""
Main interface for meteringmarketplace service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_meteringmarketplace import (
        Client,
        MarketplaceMeteringClient,
    )

    session = Session()
    client: MarketplaceMeteringClient = session.client("meteringmarketplace")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import MarketplaceMeteringClient

Client = MarketplaceMeteringClient

__all__ = ("Client", "MarketplaceMeteringClient")
