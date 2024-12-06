"""
Main interface for partnercentral-selling service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_partnercentral_selling import (
        Client,
        ListEngagementInvitationsPaginator,
        ListOpportunitiesPaginator,
        ListSolutionsPaginator,
        PartnerCentralSellingAPIClient,
    )

    session = Session()
    client: PartnerCentralSellingAPIClient = session.client("partnercentral-selling")

    list_engagement_invitations_paginator: ListEngagementInvitationsPaginator = client.get_paginator("list_engagement_invitations")
    list_opportunities_paginator: ListOpportunitiesPaginator = client.get_paginator("list_opportunities")
    list_solutions_paginator: ListSolutionsPaginator = client.get_paginator("list_solutions")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import PartnerCentralSellingAPIClient
from .paginator import (
    ListEngagementInvitationsPaginator,
    ListOpportunitiesPaginator,
    ListSolutionsPaginator,
)

Client = PartnerCentralSellingAPIClient

__all__ = (
    "Client",
    "ListEngagementInvitationsPaginator",
    "ListOpportunitiesPaginator",
    "ListSolutionsPaginator",
    "PartnerCentralSellingAPIClient",
)
