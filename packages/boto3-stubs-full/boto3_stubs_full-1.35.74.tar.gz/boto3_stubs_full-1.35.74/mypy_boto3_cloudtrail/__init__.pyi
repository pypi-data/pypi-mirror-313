"""
Main interface for cloudtrail service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloudtrail import (
        Client,
        CloudTrailClient,
        ListImportFailuresPaginator,
        ListImportsPaginator,
        ListPublicKeysPaginator,
        ListTagsPaginator,
        ListTrailsPaginator,
        LookupEventsPaginator,
    )

    session = Session()
    client: CloudTrailClient = session.client("cloudtrail")

    list_import_failures_paginator: ListImportFailuresPaginator = client.get_paginator("list_import_failures")
    list_imports_paginator: ListImportsPaginator = client.get_paginator("list_imports")
    list_public_keys_paginator: ListPublicKeysPaginator = client.get_paginator("list_public_keys")
    list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
    list_trails_paginator: ListTrailsPaginator = client.get_paginator("list_trails")
    lookup_events_paginator: LookupEventsPaginator = client.get_paginator("lookup_events")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CloudTrailClient
from .paginator import (
    ListImportFailuresPaginator,
    ListImportsPaginator,
    ListPublicKeysPaginator,
    ListTagsPaginator,
    ListTrailsPaginator,
    LookupEventsPaginator,
)

Client = CloudTrailClient

__all__ = (
    "Client",
    "CloudTrailClient",
    "ListImportFailuresPaginator",
    "ListImportsPaginator",
    "ListPublicKeysPaginator",
    "ListTagsPaginator",
    "ListTrailsPaginator",
    "LookupEventsPaginator",
)
