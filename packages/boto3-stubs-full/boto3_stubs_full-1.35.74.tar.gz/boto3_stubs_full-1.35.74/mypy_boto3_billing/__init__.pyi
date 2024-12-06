"""
Main interface for billing service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_billing import (
        BillingClient,
        Client,
        ListBillingViewsPaginator,
    )

    session = Session()
    client: BillingClient = session.client("billing")

    list_billing_views_paginator: ListBillingViewsPaginator = client.get_paginator("list_billing_views")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import BillingClient
from .paginator import ListBillingViewsPaginator

Client = BillingClient

__all__ = ("BillingClient", "Client", "ListBillingViewsPaginator")
