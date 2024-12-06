"""
Main interface for controlcatalog service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_controlcatalog import (
        Client,
        ControlCatalogClient,
        ListCommonControlsPaginator,
        ListControlsPaginator,
        ListDomainsPaginator,
        ListObjectivesPaginator,
    )

    session = Session()
    client: ControlCatalogClient = session.client("controlcatalog")

    list_common_controls_paginator: ListCommonControlsPaginator = client.get_paginator("list_common_controls")
    list_controls_paginator: ListControlsPaginator = client.get_paginator("list_controls")
    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_objectives_paginator: ListObjectivesPaginator = client.get_paginator("list_objectives")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ControlCatalogClient
from .paginator import (
    ListCommonControlsPaginator,
    ListControlsPaginator,
    ListDomainsPaginator,
    ListObjectivesPaginator,
)

Client = ControlCatalogClient


__all__ = (
    "Client",
    "ControlCatalogClient",
    "ListCommonControlsPaginator",
    "ListControlsPaginator",
    "ListDomainsPaginator",
    "ListObjectivesPaginator",
)
