"""
Type annotations for bedrock-runtime service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_runtime/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_bedrock_runtime.client import BedrockRuntimeClient
    from mypy_boto3_bedrock_runtime.paginator import (
        ListAsyncInvokesPaginator,
    )

    session = Session()
    client: BedrockRuntimeClient = session.client("bedrock-runtime")

    list_async_invokes_paginator: ListAsyncInvokesPaginator = client.get_paginator("list_async_invokes")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAsyncInvokesRequestListAsyncInvokesPaginateTypeDef,
    ListAsyncInvokesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListAsyncInvokesPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAsyncInvokesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/paginator/ListAsyncInvokes.html#BedrockRuntime.Paginator.ListAsyncInvokes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_runtime/paginators/#listasyncinvokespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAsyncInvokesRequestListAsyncInvokesPaginateTypeDef]
    ) -> _PageIterator[ListAsyncInvokesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/paginator/ListAsyncInvokes.html#BedrockRuntime.Paginator.ListAsyncInvokes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_runtime/paginators/#listasyncinvokespaginator)
        """
