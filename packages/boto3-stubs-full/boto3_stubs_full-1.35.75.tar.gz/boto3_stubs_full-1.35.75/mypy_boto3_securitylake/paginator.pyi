"""
Type annotations for securitylake service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_securitylake.client import SecurityLakeClient
    from mypy_boto3_securitylake.paginator import (
        GetDataLakeSourcesPaginator,
        ListDataLakeExceptionsPaginator,
        ListLogSourcesPaginator,
        ListSubscribersPaginator,
    )

    session = Session()
    client: SecurityLakeClient = session.client("securitylake")

    get_data_lake_sources_paginator: GetDataLakeSourcesPaginator = client.get_paginator("get_data_lake_sources")
    list_data_lake_exceptions_paginator: ListDataLakeExceptionsPaginator = client.get_paginator("list_data_lake_exceptions")
    list_log_sources_paginator: ListLogSourcesPaginator = client.get_paginator("list_log_sources")
    list_subscribers_paginator: ListSubscribersPaginator = client.get_paginator("list_subscribers")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetDataLakeSourcesRequestGetDataLakeSourcesPaginateTypeDef,
    GetDataLakeSourcesResponseTypeDef,
    ListDataLakeExceptionsRequestListDataLakeExceptionsPaginateTypeDef,
    ListDataLakeExceptionsResponseTypeDef,
    ListLogSourcesRequestListLogSourcesPaginateTypeDef,
    ListLogSourcesResponseTypeDef,
    ListSubscribersRequestListSubscribersPaginateTypeDef,
    ListSubscribersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetDataLakeSourcesPaginator",
    "ListDataLakeExceptionsPaginator",
    "ListLogSourcesPaginator",
    "ListSubscribersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetDataLakeSourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/GetDataLakeSources.html#SecurityLake.Paginator.GetDataLakeSources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/#getdatalakesourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDataLakeSourcesRequestGetDataLakeSourcesPaginateTypeDef]
    ) -> _PageIterator[GetDataLakeSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/GetDataLakeSources.html#SecurityLake.Paginator.GetDataLakeSources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/#getdatalakesourcespaginator)
        """

class ListDataLakeExceptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListDataLakeExceptions.html#SecurityLake.Paginator.ListDataLakeExceptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/#listdatalakeexceptionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataLakeExceptionsRequestListDataLakeExceptionsPaginateTypeDef]
    ) -> _PageIterator[ListDataLakeExceptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListDataLakeExceptions.html#SecurityLake.Paginator.ListDataLakeExceptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/#listdatalakeexceptionspaginator)
        """

class ListLogSourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListLogSources.html#SecurityLake.Paginator.ListLogSources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/#listlogsourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLogSourcesRequestListLogSourcesPaginateTypeDef]
    ) -> _PageIterator[ListLogSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListLogSources.html#SecurityLake.Paginator.ListLogSources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/#listlogsourcespaginator)
        """

class ListSubscribersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListSubscribers.html#SecurityLake.Paginator.ListSubscribers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/#listsubscriberspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSubscribersRequestListSubscribersPaginateTypeDef]
    ) -> _PageIterator[ListSubscribersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListSubscribers.html#SecurityLake.Paginator.ListSubscribers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/#listsubscriberspaginator)
        """
