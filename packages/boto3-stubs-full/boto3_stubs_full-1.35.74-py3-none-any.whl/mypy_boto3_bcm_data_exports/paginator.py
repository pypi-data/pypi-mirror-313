"""
Type annotations for bcm-data-exports service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_data_exports/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_bcm_data_exports.client import BillingandCostManagementDataExportsClient
    from mypy_boto3_bcm_data_exports.paginator import (
        ListExecutionsPaginator,
        ListExportsPaginator,
        ListTablesPaginator,
    )

    session = Session()
    client: BillingandCostManagementDataExportsClient = session.client("bcm-data-exports")

    list_executions_paginator: ListExecutionsPaginator = client.get_paginator("list_executions")
    list_exports_paginator: ListExportsPaginator = client.get_paginator("list_exports")
    list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListExecutionsRequestListExecutionsPaginateTypeDef,
    ListExecutionsResponseTypeDef,
    ListExportsRequestListExportsPaginateTypeDef,
    ListExportsResponseTypeDef,
    ListTablesRequestListTablesPaginateTypeDef,
    ListTablesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListExecutionsPaginator", "ListExportsPaginator", "ListTablesPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-data-exports/paginator/ListExecutions.html#BillingandCostManagementDataExports.Paginator.ListExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_data_exports/paginators/#listexecutionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListExecutionsRequestListExecutionsPaginateTypeDef]
    ) -> _PageIterator[ListExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-data-exports/paginator/ListExecutions.html#BillingandCostManagementDataExports.Paginator.ListExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_data_exports/paginators/#listexecutionspaginator)
        """


class ListExportsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-data-exports/paginator/ListExports.html#BillingandCostManagementDataExports.Paginator.ListExports)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_data_exports/paginators/#listexportspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListExportsRequestListExportsPaginateTypeDef]
    ) -> _PageIterator[ListExportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-data-exports/paginator/ListExports.html#BillingandCostManagementDataExports.Paginator.ListExports.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_data_exports/paginators/#listexportspaginator)
        """


class ListTablesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-data-exports/paginator/ListTables.html#BillingandCostManagementDataExports.Paginator.ListTables)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_data_exports/paginators/#listtablespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTablesRequestListTablesPaginateTypeDef]
    ) -> _PageIterator[ListTablesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-data-exports/paginator/ListTables.html#BillingandCostManagementDataExports.Paginator.ListTables.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_data_exports/paginators/#listtablespaginator)
        """
