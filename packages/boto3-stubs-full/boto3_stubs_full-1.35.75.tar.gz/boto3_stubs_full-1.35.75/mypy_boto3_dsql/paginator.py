"""
Type annotations for dsql service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dsql/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_dsql.client import AuroraDSQLClient
    from mypy_boto3_dsql.paginator import (
        ListClustersPaginator,
    )

    session = Session()
    client: AuroraDSQLClient = session.client("dsql")

    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListClustersInputListClustersPaginateTypeDef, ListClustersOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListClustersPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListClustersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dsql/paginator/ListClusters.html#AuroraDSQL.Paginator.ListClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dsql/paginators/#listclusterspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListClustersInputListClustersPaginateTypeDef]
    ) -> _PageIterator[ListClustersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dsql/paginator/ListClusters.html#AuroraDSQL.Paginator.ListClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dsql/paginators/#listclusterspaginator)
        """
