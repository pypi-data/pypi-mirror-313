"""
Type annotations for ivs-realtime service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ivs_realtime.client import IvsrealtimeClient
    from mypy_boto3_ivs_realtime.paginator import (
        ListIngestConfigurationsPaginator,
        ListPublicKeysPaginator,
    )

    session = Session()
    client: IvsrealtimeClient = session.client("ivs-realtime")

    list_ingest_configurations_paginator: ListIngestConfigurationsPaginator = client.get_paginator("list_ingest_configurations")
    list_public_keys_paginator: ListPublicKeysPaginator = client.get_paginator("list_public_keys")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListIngestConfigurationsRequestListIngestConfigurationsPaginateTypeDef,
    ListIngestConfigurationsResponseTypeDef,
    ListPublicKeysRequestListPublicKeysPaginateTypeDef,
    ListPublicKeysResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListIngestConfigurationsPaginator", "ListPublicKeysPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListIngestConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime/paginator/ListIngestConfigurations.html#Ivsrealtime.Paginator.ListIngestConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/paginators/#listingestconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListIngestConfigurationsRequestListIngestConfigurationsPaginateTypeDef],
    ) -> _PageIterator[ListIngestConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime/paginator/ListIngestConfigurations.html#Ivsrealtime.Paginator.ListIngestConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/paginators/#listingestconfigurationspaginator)
        """

class ListPublicKeysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime/paginator/ListPublicKeys.html#Ivsrealtime.Paginator.ListPublicKeys)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/paginators/#listpublickeyspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPublicKeysRequestListPublicKeysPaginateTypeDef]
    ) -> _PageIterator[ListPublicKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime/paginator/ListPublicKeys.html#Ivsrealtime.Paginator.ListPublicKeys.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/paginators/#listpublickeyspaginator)
        """
