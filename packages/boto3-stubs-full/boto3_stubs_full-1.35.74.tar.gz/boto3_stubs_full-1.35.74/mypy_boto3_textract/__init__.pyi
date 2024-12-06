"""
Main interface for textract service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_textract import (
        Client,
        ListAdapterVersionsPaginator,
        ListAdaptersPaginator,
        TextractClient,
    )

    session = Session()
    client: TextractClient = session.client("textract")

    list_adapter_versions_paginator: ListAdapterVersionsPaginator = client.get_paginator("list_adapter_versions")
    list_adapters_paginator: ListAdaptersPaginator = client.get_paginator("list_adapters")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import TextractClient
from .paginator import ListAdaptersPaginator, ListAdapterVersionsPaginator

Client = TextractClient

__all__ = ("Client", "ListAdapterVersionsPaginator", "ListAdaptersPaginator", "TextractClient")
