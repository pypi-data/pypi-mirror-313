"""
Type annotations for translate service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_translate/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_translate.client import TranslateClient
    from mypy_boto3_translate.paginator import (
        ListTerminologiesPaginator,
    )

    session = Session()
    client: TranslateClient = session.client("translate")

    list_terminologies_paginator: ListTerminologiesPaginator = client.get_paginator("list_terminologies")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListTerminologiesRequestListTerminologiesPaginateTypeDef,
    ListTerminologiesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListTerminologiesPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListTerminologiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/paginator/ListTerminologies.html#Translate.Paginator.ListTerminologies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_translate/paginators/#listterminologiespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTerminologiesRequestListTerminologiesPaginateTypeDef]
    ) -> _PageIterator[ListTerminologiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/paginator/ListTerminologies.html#Translate.Paginator.ListTerminologies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_translate/paginators/#listterminologiespaginator)
        """
