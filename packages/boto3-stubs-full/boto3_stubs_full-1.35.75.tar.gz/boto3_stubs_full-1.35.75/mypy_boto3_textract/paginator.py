"""
Type annotations for textract service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_textract.client import TextractClient
    from mypy_boto3_textract.paginator import (
        ListAdapterVersionsPaginator,
        ListAdaptersPaginator,
    )

    session = Session()
    client: TextractClient = session.client("textract")

    list_adapter_versions_paginator: ListAdapterVersionsPaginator = client.get_paginator("list_adapter_versions")
    list_adapters_paginator: ListAdaptersPaginator = client.get_paginator("list_adapters")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAdaptersRequestListAdaptersPaginateTypeDef,
    ListAdaptersResponseTypeDef,
    ListAdapterVersionsRequestListAdapterVersionsPaginateTypeDef,
    ListAdapterVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListAdapterVersionsPaginator", "ListAdaptersPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAdapterVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/paginator/ListAdapterVersions.html#Textract.Paginator.ListAdapterVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/paginators/#listadapterversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAdapterVersionsRequestListAdapterVersionsPaginateTypeDef]
    ) -> _PageIterator[ListAdapterVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/paginator/ListAdapterVersions.html#Textract.Paginator.ListAdapterVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/paginators/#listadapterversionspaginator)
        """


class ListAdaptersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/paginator/ListAdapters.html#Textract.Paginator.ListAdapters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/paginators/#listadapterspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAdaptersRequestListAdaptersPaginateTypeDef]
    ) -> _PageIterator[ListAdaptersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/paginator/ListAdapters.html#Textract.Paginator.ListAdapters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/paginators/#listadapterspaginator)
        """
