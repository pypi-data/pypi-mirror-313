"""
Type annotations for s3tables service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3tables/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_s3tables.client import S3TablesClient
    from mypy_boto3_s3tables.paginator import (
        ListNamespacesPaginator,
        ListTableBucketsPaginator,
        ListTablesPaginator,
    )

    session = Session()
    client: S3TablesClient = session.client("s3tables")

    list_namespaces_paginator: ListNamespacesPaginator = client.get_paginator("list_namespaces")
    list_table_buckets_paginator: ListTableBucketsPaginator = client.get_paginator("list_table_buckets")
    list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListNamespacesRequestListNamespacesPaginateTypeDef,
    ListNamespacesResponseTypeDef,
    ListTableBucketsRequestListTableBucketsPaginateTypeDef,
    ListTableBucketsResponseTypeDef,
    ListTablesRequestListTablesPaginateTypeDef,
    ListTablesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListNamespacesPaginator", "ListTableBucketsPaginator", "ListTablesPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListNamespacesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListNamespaces.html#S3Tables.Paginator.ListNamespaces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3tables/paginators/#listnamespacespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListNamespacesRequestListNamespacesPaginateTypeDef]
    ) -> _PageIterator[ListNamespacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListNamespaces.html#S3Tables.Paginator.ListNamespaces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3tables/paginators/#listnamespacespaginator)
        """


class ListTableBucketsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListTableBuckets.html#S3Tables.Paginator.ListTableBuckets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3tables/paginators/#listtablebucketspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTableBucketsRequestListTableBucketsPaginateTypeDef]
    ) -> _PageIterator[ListTableBucketsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListTableBuckets.html#S3Tables.Paginator.ListTableBuckets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3tables/paginators/#listtablebucketspaginator)
        """


class ListTablesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListTables.html#S3Tables.Paginator.ListTables)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3tables/paginators/#listtablespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTablesRequestListTablesPaginateTypeDef]
    ) -> _PageIterator[ListTablesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListTables.html#S3Tables.Paginator.ListTables.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3tables/paginators/#listtablespaginator)
        """
