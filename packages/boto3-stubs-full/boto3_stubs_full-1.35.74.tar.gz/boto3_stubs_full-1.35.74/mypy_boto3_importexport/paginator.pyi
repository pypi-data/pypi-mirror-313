"""
Type annotations for importexport service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_importexport/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_importexport.client import ImportExportClient
    from mypy_boto3_importexport.paginator import (
        ListJobsPaginator,
    )

    session = Session()
    client: ImportExportClient = session.client("importexport")

    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListJobsInputListJobsPaginateTypeDef, ListJobsOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListJobsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/paginator/ListJobs.html#ImportExport.Paginator.ListJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_importexport/paginators/#listjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsInputListJobsPaginateTypeDef]
    ) -> _PageIterator[ListJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/paginator/ListJobs.html#ImportExport.Paginator.ListJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_importexport/paginators/#listjobspaginator)
        """
