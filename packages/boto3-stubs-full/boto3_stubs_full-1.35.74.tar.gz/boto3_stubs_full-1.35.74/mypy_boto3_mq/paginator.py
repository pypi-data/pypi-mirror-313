"""
Type annotations for mq service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_mq.client import MQClient
    from mypy_boto3_mq.paginator import (
        ListBrokersPaginator,
    )

    session = Session()
    client: MQClient = session.client("mq")

    list_brokers_paginator: ListBrokersPaginator = client.get_paginator("list_brokers")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListBrokersRequestListBrokersPaginateTypeDef, ListBrokersResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListBrokersPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListBrokersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/paginator/ListBrokers.html#MQ.Paginator.ListBrokers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/paginators/#listbrokerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBrokersRequestListBrokersPaginateTypeDef]
    ) -> _PageIterator[ListBrokersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/paginator/ListBrokers.html#MQ.Paginator.ListBrokers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/paginators/#listbrokerspaginator)
        """
