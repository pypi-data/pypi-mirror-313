"""
Type annotations for redshift-data service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_data/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_redshift_data.client import RedshiftDataAPIServiceClient
    from mypy_boto3_redshift_data.paginator import (
        DescribeTablePaginator,
        GetStatementResultPaginator,
        GetStatementResultV2Paginator,
        ListDatabasesPaginator,
        ListSchemasPaginator,
        ListStatementsPaginator,
        ListTablesPaginator,
    )

    session = Session()
    client: RedshiftDataAPIServiceClient = session.client("redshift-data")

    describe_table_paginator: DescribeTablePaginator = client.get_paginator("describe_table")
    get_statement_result_paginator: GetStatementResultPaginator = client.get_paginator("get_statement_result")
    get_statement_result_v2_paginator: GetStatementResultV2Paginator = client.get_paginator("get_statement_result_v2")
    list_databases_paginator: ListDatabasesPaginator = client.get_paginator("list_databases")
    list_schemas_paginator: ListSchemasPaginator = client.get_paginator("list_schemas")
    list_statements_paginator: ListStatementsPaginator = client.get_paginator("list_statements")
    list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeTableRequestDescribeTablePaginateTypeDef,
    DescribeTableResponseTypeDef,
    GetStatementResultRequestGetStatementResultPaginateTypeDef,
    GetStatementResultResponseTypeDef,
    GetStatementResultV2RequestGetStatementResultV2PaginateTypeDef,
    GetStatementResultV2ResponseTypeDef,
    ListDatabasesRequestListDatabasesPaginateTypeDef,
    ListDatabasesResponseTypeDef,
    ListSchemasRequestListSchemasPaginateTypeDef,
    ListSchemasResponseTypeDef,
    ListStatementsRequestListStatementsPaginateTypeDef,
    ListStatementsResponseTypeDef,
    ListTablesRequestListTablesPaginateTypeDef,
    ListTablesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeTablePaginator",
    "GetStatementResultPaginator",
    "GetStatementResultV2Paginator",
    "ListDatabasesPaginator",
    "ListSchemasPaginator",
    "ListStatementsPaginator",
    "ListTablesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeTablePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/paginator/DescribeTable.html#RedshiftDataAPIService.Paginator.DescribeTable)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_data/paginators/#describetablepaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeTableRequestDescribeTablePaginateTypeDef]
    ) -> _PageIterator[DescribeTableResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/paginator/DescribeTable.html#RedshiftDataAPIService.Paginator.DescribeTable.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_data/paginators/#describetablepaginator)
        """


class GetStatementResultPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/paginator/GetStatementResult.html#RedshiftDataAPIService.Paginator.GetStatementResult)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_data/paginators/#getstatementresultpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetStatementResultRequestGetStatementResultPaginateTypeDef]
    ) -> _PageIterator[GetStatementResultResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/paginator/GetStatementResult.html#RedshiftDataAPIService.Paginator.GetStatementResult.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_data/paginators/#getstatementresultpaginator)
        """


class GetStatementResultV2Paginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/paginator/GetStatementResultV2.html#RedshiftDataAPIService.Paginator.GetStatementResultV2)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_data/paginators/#getstatementresultv2paginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetStatementResultV2RequestGetStatementResultV2PaginateTypeDef]
    ) -> _PageIterator[GetStatementResultV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/paginator/GetStatementResultV2.html#RedshiftDataAPIService.Paginator.GetStatementResultV2.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_data/paginators/#getstatementresultv2paginator)
        """


class ListDatabasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/paginator/ListDatabases.html#RedshiftDataAPIService.Paginator.ListDatabases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_data/paginators/#listdatabasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDatabasesRequestListDatabasesPaginateTypeDef]
    ) -> _PageIterator[ListDatabasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/paginator/ListDatabases.html#RedshiftDataAPIService.Paginator.ListDatabases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_data/paginators/#listdatabasespaginator)
        """


class ListSchemasPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/paginator/ListSchemas.html#RedshiftDataAPIService.Paginator.ListSchemas)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_data/paginators/#listschemaspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSchemasRequestListSchemasPaginateTypeDef]
    ) -> _PageIterator[ListSchemasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/paginator/ListSchemas.html#RedshiftDataAPIService.Paginator.ListSchemas.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_data/paginators/#listschemaspaginator)
        """


class ListStatementsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/paginator/ListStatements.html#RedshiftDataAPIService.Paginator.ListStatements)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_data/paginators/#liststatementspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStatementsRequestListStatementsPaginateTypeDef]
    ) -> _PageIterator[ListStatementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/paginator/ListStatements.html#RedshiftDataAPIService.Paginator.ListStatements.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_data/paginators/#liststatementspaginator)
        """


class ListTablesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/paginator/ListTables.html#RedshiftDataAPIService.Paginator.ListTables)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_data/paginators/#listtablespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTablesRequestListTablesPaginateTypeDef]
    ) -> _PageIterator[ListTablesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/paginator/ListTables.html#RedshiftDataAPIService.Paginator.ListTables.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_data/paginators/#listtablespaginator)
        """
