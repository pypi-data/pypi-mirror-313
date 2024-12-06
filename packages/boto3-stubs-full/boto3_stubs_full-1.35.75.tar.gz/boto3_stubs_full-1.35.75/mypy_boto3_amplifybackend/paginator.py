"""
Type annotations for amplifybackend service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifybackend/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_amplifybackend.client import AmplifyBackendClient
    from mypy_boto3_amplifybackend.paginator import (
        ListBackendJobsPaginator,
    )

    session = Session()
    client: AmplifyBackendClient = session.client("amplifybackend")

    list_backend_jobs_paginator: ListBackendJobsPaginator = client.get_paginator("list_backend_jobs")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListBackendJobsRequestListBackendJobsPaginateTypeDef,
    ListBackendJobsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListBackendJobsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListBackendJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/paginator/ListBackendJobs.html#AmplifyBackend.Paginator.ListBackendJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifybackend/paginators/#listbackendjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBackendJobsRequestListBackendJobsPaginateTypeDef]
    ) -> _PageIterator[ListBackendJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/paginator/ListBackendJobs.html#AmplifyBackend.Paginator.ListBackendJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifybackend/paginators/#listbackendjobspaginator)
        """
