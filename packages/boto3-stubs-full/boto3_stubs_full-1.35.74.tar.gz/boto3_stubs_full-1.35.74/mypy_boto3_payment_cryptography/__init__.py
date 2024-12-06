"""
Main interface for payment-cryptography service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_payment_cryptography import (
        Client,
        ListAliasesPaginator,
        ListKeysPaginator,
        ListTagsForResourcePaginator,
        PaymentCryptographyControlPlaneClient,
    )

    session = Session()
    client: PaymentCryptographyControlPlaneClient = session.client("payment-cryptography")

    list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
    list_keys_paginator: ListKeysPaginator = client.get_paginator("list_keys")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import PaymentCryptographyControlPlaneClient
from .paginator import ListAliasesPaginator, ListKeysPaginator, ListTagsForResourcePaginator

Client = PaymentCryptographyControlPlaneClient


__all__ = (
    "Client",
    "ListAliasesPaginator",
    "ListKeysPaginator",
    "ListTagsForResourcePaginator",
    "PaymentCryptographyControlPlaneClient",
)
