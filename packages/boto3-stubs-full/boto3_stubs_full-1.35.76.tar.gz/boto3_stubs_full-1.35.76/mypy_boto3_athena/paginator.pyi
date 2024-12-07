"""
Type annotations for athena service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_athena.client import AthenaClient
    from mypy_boto3_athena.paginator import (
        GetQueryResultsPaginator,
        ListDataCatalogsPaginator,
        ListDatabasesPaginator,
        ListNamedQueriesPaginator,
        ListQueryExecutionsPaginator,
        ListTableMetadataPaginator,
        ListTagsForResourcePaginator,
    )

    session = Session()
    client: AthenaClient = session.client("athena")

    get_query_results_paginator: GetQueryResultsPaginator = client.get_paginator("get_query_results")
    list_data_catalogs_paginator: ListDataCatalogsPaginator = client.get_paginator("list_data_catalogs")
    list_databases_paginator: ListDatabasesPaginator = client.get_paginator("list_databases")
    list_named_queries_paginator: ListNamedQueriesPaginator = client.get_paginator("list_named_queries")
    list_query_executions_paginator: ListQueryExecutionsPaginator = client.get_paginator("list_query_executions")
    list_table_metadata_paginator: ListTableMetadataPaginator = client.get_paginator("list_table_metadata")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetQueryResultsInputGetQueryResultsPaginateTypeDef,
    GetQueryResultsOutputTypeDef,
    ListDatabasesInputListDatabasesPaginateTypeDef,
    ListDatabasesOutputTypeDef,
    ListDataCatalogsInputListDataCatalogsPaginateTypeDef,
    ListDataCatalogsOutputTypeDef,
    ListNamedQueriesInputListNamedQueriesPaginateTypeDef,
    ListNamedQueriesOutputTypeDef,
    ListQueryExecutionsInputListQueryExecutionsPaginateTypeDef,
    ListQueryExecutionsOutputTypeDef,
    ListTableMetadataInputListTableMetadataPaginateTypeDef,
    ListTableMetadataOutputTypeDef,
    ListTagsForResourceInputListTagsForResourcePaginateTypeDef,
    ListTagsForResourceOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetQueryResultsPaginator",
    "ListDataCatalogsPaginator",
    "ListDatabasesPaginator",
    "ListNamedQueriesPaginator",
    "ListQueryExecutionsPaginator",
    "ListTableMetadataPaginator",
    "ListTagsForResourcePaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetQueryResultsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/GetQueryResults.html#Athena.Paginator.GetQueryResults)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#getqueryresultspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetQueryResultsInputGetQueryResultsPaginateTypeDef]
    ) -> _PageIterator[GetQueryResultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/GetQueryResults.html#Athena.Paginator.GetQueryResults.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#getqueryresultspaginator)
        """

class ListDataCatalogsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListDataCatalogs.html#Athena.Paginator.ListDataCatalogs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listdatacatalogspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataCatalogsInputListDataCatalogsPaginateTypeDef]
    ) -> _PageIterator[ListDataCatalogsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListDataCatalogs.html#Athena.Paginator.ListDataCatalogs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listdatacatalogspaginator)
        """

class ListDatabasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListDatabases.html#Athena.Paginator.ListDatabases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listdatabasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDatabasesInputListDatabasesPaginateTypeDef]
    ) -> _PageIterator[ListDatabasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListDatabases.html#Athena.Paginator.ListDatabases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listdatabasespaginator)
        """

class ListNamedQueriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListNamedQueries.html#Athena.Paginator.ListNamedQueries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listnamedqueriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListNamedQueriesInputListNamedQueriesPaginateTypeDef]
    ) -> _PageIterator[ListNamedQueriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListNamedQueries.html#Athena.Paginator.ListNamedQueries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listnamedqueriespaginator)
        """

class ListQueryExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListQueryExecutions.html#Athena.Paginator.ListQueryExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listqueryexecutionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListQueryExecutionsInputListQueryExecutionsPaginateTypeDef]
    ) -> _PageIterator[ListQueryExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListQueryExecutions.html#Athena.Paginator.ListQueryExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listqueryexecutionspaginator)
        """

class ListTableMetadataPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListTableMetadata.html#Athena.Paginator.ListTableMetadata)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listtablemetadatapaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTableMetadataInputListTableMetadataPaginateTypeDef]
    ) -> _PageIterator[ListTableMetadataOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListTableMetadata.html#Athena.Paginator.ListTableMetadata.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listtablemetadatapaginator)
        """

class ListTagsForResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListTagsForResource.html#Athena.Paginator.ListTagsForResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listtagsforresourcepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceInputListTagsForResourcePaginateTypeDef]
    ) -> _PageIterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListTagsForResource.html#Athena.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listtagsforresourcepaginator)
        """
