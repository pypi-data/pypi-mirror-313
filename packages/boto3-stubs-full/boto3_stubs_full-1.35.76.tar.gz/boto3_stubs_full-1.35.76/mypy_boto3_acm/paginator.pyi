"""
Type annotations for acm service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_acm.client import ACMClient
    from mypy_boto3_acm.paginator import (
        ListCertificatesPaginator,
    )

    session = Session()
    client: ACMClient = session.client("acm")

    list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListCertificatesRequestListCertificatesPaginateTypeDef,
    ListCertificatesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListCertificatesPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListCertificatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListCertificates.html#ACM.Paginator.ListCertificates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listcertificatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCertificatesRequestListCertificatesPaginateTypeDef]
    ) -> _PageIterator[ListCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListCertificates.html#ACM.Paginator.ListCertificates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listcertificatespaginator)
        """
