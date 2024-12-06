"""
Type annotations for iot-data service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_iot_data.client import IoTDataPlaneClient
    from mypy_boto3_iot_data.paginator import (
        ListRetainedMessagesPaginator,
    )

    session = Session()
    client: IoTDataPlaneClient = session.client("iot-data")

    list_retained_messages_paginator: ListRetainedMessagesPaginator = client.get_paginator("list_retained_messages")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListRetainedMessagesRequestListRetainedMessagesPaginateTypeDef,
    ListRetainedMessagesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListRetainedMessagesPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListRetainedMessagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/paginator/ListRetainedMessages.html#IoTDataPlane.Paginator.ListRetainedMessages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/paginators/#listretainedmessagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRetainedMessagesRequestListRetainedMessagesPaginateTypeDef]
    ) -> _PageIterator[ListRetainedMessagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/paginator/ListRetainedMessages.html#IoTDataPlane.Paginator.ListRetainedMessages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/paginators/#listretainedmessagespaginator)
        """
