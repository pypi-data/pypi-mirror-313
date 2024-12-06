"""
Main interface for kendra-ranking service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kendra_ranking import (
        Client,
        KendraRankingClient,
    )

    session = Session()
    client: KendraRankingClient = session.client("kendra-ranking")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import KendraRankingClient

Client = KendraRankingClient


__all__ = ("Client", "KendraRankingClient")
