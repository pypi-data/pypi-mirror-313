"""
Type annotations for mwaa service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mwaa/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_mwaa.client import MWAAClient
    from mypy_boto3_mwaa.paginator import (
        ListEnvironmentsPaginator,
    )

    session = Session()
    client: MWAAClient = session.client("mwaa")

    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListEnvironmentsInputListEnvironmentsPaginateTypeDef,
    ListEnvironmentsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListEnvironmentsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListEnvironmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/paginator/ListEnvironments.html#MWAA.Paginator.ListEnvironments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mwaa/paginators/#listenvironmentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEnvironmentsInputListEnvironmentsPaginateTypeDef]
    ) -> _PageIterator[ListEnvironmentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/paginator/ListEnvironments.html#MWAA.Paginator.ListEnvironments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mwaa/paginators/#listenvironmentspaginator)
        """
