"""
Main interface for cloudfront-keyvaluestore service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloudfront_keyvaluestore import (
        Client,
        CloudFrontKeyValueStoreClient,
        ListKeysPaginator,
    )

    session = Session()
    client: CloudFrontKeyValueStoreClient = session.client("cloudfront-keyvaluestore")

    list_keys_paginator: ListKeysPaginator = client.get_paginator("list_keys")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CloudFrontKeyValueStoreClient
from .paginator import ListKeysPaginator

Client = CloudFrontKeyValueStoreClient

__all__ = ("Client", "CloudFrontKeyValueStoreClient", "ListKeysPaginator")
