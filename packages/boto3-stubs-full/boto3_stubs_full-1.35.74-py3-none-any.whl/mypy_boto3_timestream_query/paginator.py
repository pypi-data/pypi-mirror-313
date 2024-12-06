"""
Type annotations for timestream-query service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_timestream_query.client import TimestreamQueryClient
    from mypy_boto3_timestream_query.paginator import (
        ListScheduledQueriesPaginator,
        ListTagsForResourcePaginator,
        QueryPaginator,
    )

    session = Session()
    client: TimestreamQueryClient = session.client("timestream-query")

    list_scheduled_queries_paginator: ListScheduledQueriesPaginator = client.get_paginator("list_scheduled_queries")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    query_paginator: QueryPaginator = client.get_paginator("query")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListScheduledQueriesRequestListScheduledQueriesPaginateTypeDef,
    ListScheduledQueriesResponseTypeDef,
    ListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    QueryRequestQueryPaginateTypeDef,
    QueryResponsePaginatorTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListScheduledQueriesPaginator", "ListTagsForResourcePaginator", "QueryPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListScheduledQueriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query/paginator/ListScheduledQueries.html#TimestreamQuery.Paginator.ListScheduledQueries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/paginators/#listscheduledqueriespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListScheduledQueriesRequestListScheduledQueriesPaginateTypeDef]
    ) -> _PageIterator[ListScheduledQueriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query/paginator/ListScheduledQueries.html#TimestreamQuery.Paginator.ListScheduledQueries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/paginators/#listscheduledqueriespaginator)
        """


class ListTagsForResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query/paginator/ListTagsForResource.html#TimestreamQuery.Paginator.ListTagsForResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceRequestListTagsForResourcePaginateTypeDef]
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query/paginator/ListTagsForResource.html#TimestreamQuery.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/paginators/#listtagsforresourcepaginator)
        """


class QueryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query/paginator/Query.html#TimestreamQuery.Paginator.Query)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/paginators/#querypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[QueryRequestQueryPaginateTypeDef]
    ) -> _PageIterator[QueryResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query/paginator/Query.html#TimestreamQuery.Paginator.Query.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/paginators/#querypaginator)
        """
