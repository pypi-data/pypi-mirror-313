"""
Type annotations for applicationcostprofiler service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_applicationcostprofiler/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_applicationcostprofiler.client import ApplicationCostProfilerClient
    from mypy_boto3_applicationcostprofiler.paginator import (
        ListReportDefinitionsPaginator,
    )

    session = Session()
    client: ApplicationCostProfilerClient = session.client("applicationcostprofiler")

    list_report_definitions_paginator: ListReportDefinitionsPaginator = client.get_paginator("list_report_definitions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListReportDefinitionsRequestListReportDefinitionsPaginateTypeDef,
    ListReportDefinitionsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListReportDefinitionsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListReportDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler/paginator/ListReportDefinitions.html#ApplicationCostProfiler.Paginator.ListReportDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_applicationcostprofiler/paginators/#listreportdefinitionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReportDefinitionsRequestListReportDefinitionsPaginateTypeDef]
    ) -> _PageIterator[ListReportDefinitionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler/paginator/ListReportDefinitions.html#ApplicationCostProfiler.Paginator.ListReportDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_applicationcostprofiler/paginators/#listreportdefinitionspaginator)
        """
