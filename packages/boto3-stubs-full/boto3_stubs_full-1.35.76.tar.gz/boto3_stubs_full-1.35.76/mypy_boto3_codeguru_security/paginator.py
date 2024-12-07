"""
Type annotations for codeguru-security service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_codeguru_security.client import CodeGuruSecurityClient
    from mypy_boto3_codeguru_security.paginator import (
        GetFindingsPaginator,
        ListFindingsMetricsPaginator,
        ListScansPaginator,
    )

    session = Session()
    client: CodeGuruSecurityClient = session.client("codeguru-security")

    get_findings_paginator: GetFindingsPaginator = client.get_paginator("get_findings")
    list_findings_metrics_paginator: ListFindingsMetricsPaginator = client.get_paginator("list_findings_metrics")
    list_scans_paginator: ListScansPaginator = client.get_paginator("list_scans")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetFindingsRequestGetFindingsPaginateTypeDef,
    GetFindingsResponseTypeDef,
    ListFindingsMetricsRequestListFindingsMetricsPaginateTypeDef,
    ListFindingsMetricsResponseTypeDef,
    ListScansRequestListScansPaginateTypeDef,
    ListScansResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("GetFindingsPaginator", "ListFindingsMetricsPaginator", "ListScansPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetFindingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/GetFindings.html#CodeGuruSecurity.Paginator.GetFindings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/paginators/#getfindingspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetFindingsRequestGetFindingsPaginateTypeDef]
    ) -> _PageIterator[GetFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/GetFindings.html#CodeGuruSecurity.Paginator.GetFindings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/paginators/#getfindingspaginator)
        """


class ListFindingsMetricsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/ListFindingsMetrics.html#CodeGuruSecurity.Paginator.ListFindingsMetrics)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/paginators/#listfindingsmetricspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFindingsMetricsRequestListFindingsMetricsPaginateTypeDef]
    ) -> _PageIterator[ListFindingsMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/ListFindingsMetrics.html#CodeGuruSecurity.Paginator.ListFindingsMetrics.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/paginators/#listfindingsmetricspaginator)
        """


class ListScansPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/ListScans.html#CodeGuruSecurity.Paginator.ListScans)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/paginators/#listscanspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListScansRequestListScansPaginateTypeDef]
    ) -> _PageIterator[ListScansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/ListScans.html#CodeGuruSecurity.Paginator.ListScans.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/paginators/#listscanspaginator)
        """
