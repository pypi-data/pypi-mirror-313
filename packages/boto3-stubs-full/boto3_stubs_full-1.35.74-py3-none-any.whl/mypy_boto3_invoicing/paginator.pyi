"""
Type annotations for invoicing service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_invoicing/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_invoicing.client import InvoicingClient
    from mypy_boto3_invoicing.paginator import (
        ListInvoiceUnitsPaginator,
    )

    session = Session()
    client: InvoicingClient = session.client("invoicing")

    list_invoice_units_paginator: ListInvoiceUnitsPaginator = client.get_paginator("list_invoice_units")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListInvoiceUnitsRequestListInvoiceUnitsPaginateTypeDef,
    ListInvoiceUnitsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListInvoiceUnitsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListInvoiceUnitsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListInvoiceUnits.html#Invoicing.Paginator.ListInvoiceUnits)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_invoicing/paginators/#listinvoiceunitspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInvoiceUnitsRequestListInvoiceUnitsPaginateTypeDef]
    ) -> _PageIterator[ListInvoiceUnitsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListInvoiceUnits.html#Invoicing.Paginator.ListInvoiceUnits.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_invoicing/paginators/#listinvoiceunitspaginator)
        """
