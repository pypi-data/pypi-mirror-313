"""
Main interface for freetier service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_freetier import (
        Client,
        FreeTierClient,
        GetFreeTierUsagePaginator,
    )

    session = Session()
    client: FreeTierClient = session.client("freetier")

    get_free_tier_usage_paginator: GetFreeTierUsagePaginator = client.get_paginator("get_free_tier_usage")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import FreeTierClient
from .paginator import GetFreeTierUsagePaginator

Client = FreeTierClient


__all__ = ("Client", "FreeTierClient", "GetFreeTierUsagePaginator")
