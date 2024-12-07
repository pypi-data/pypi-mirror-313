"""
Main interface for connectcampaigns service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_connectcampaigns import (
        Client,
        ConnectCampaignServiceClient,
        ListCampaignsPaginator,
    )

    session = Session()
    client: ConnectCampaignServiceClient = session.client("connectcampaigns")

    list_campaigns_paginator: ListCampaignsPaginator = client.get_paginator("list_campaigns")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ConnectCampaignServiceClient
from .paginator import ListCampaignsPaginator

Client = ConnectCampaignServiceClient

__all__ = ("Client", "ConnectCampaignServiceClient", "ListCampaignsPaginator")
