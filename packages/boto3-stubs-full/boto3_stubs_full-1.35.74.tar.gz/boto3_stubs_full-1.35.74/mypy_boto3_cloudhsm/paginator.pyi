"""
Type annotations for cloudhsm service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_cloudhsm.client import CloudHSMClient
    from mypy_boto3_cloudhsm.paginator import (
        ListHapgsPaginator,
        ListHsmsPaginator,
        ListLunaClientsPaginator,
    )

    session = Session()
    client: CloudHSMClient = session.client("cloudhsm")

    list_hapgs_paginator: ListHapgsPaginator = client.get_paginator("list_hapgs")
    list_hsms_paginator: ListHsmsPaginator = client.get_paginator("list_hsms")
    list_luna_clients_paginator: ListLunaClientsPaginator = client.get_paginator("list_luna_clients")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListHapgsRequestListHapgsPaginateTypeDef,
    ListHapgsResponseTypeDef,
    ListHsmsRequestListHsmsPaginateTypeDef,
    ListHsmsResponseTypeDef,
    ListLunaClientsRequestListLunaClientsPaginateTypeDef,
    ListLunaClientsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListHapgsPaginator", "ListHsmsPaginator", "ListLunaClientsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListHapgsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/paginator/ListHapgs.html#CloudHSM.Paginator.ListHapgs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/paginators/#listhapgspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListHapgsRequestListHapgsPaginateTypeDef]
    ) -> _PageIterator[ListHapgsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/paginator/ListHapgs.html#CloudHSM.Paginator.ListHapgs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/paginators/#listhapgspaginator)
        """

class ListHsmsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/paginator/ListHsms.html#CloudHSM.Paginator.ListHsms)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/paginators/#listhsmspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListHsmsRequestListHsmsPaginateTypeDef]
    ) -> _PageIterator[ListHsmsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/paginator/ListHsms.html#CloudHSM.Paginator.ListHsms.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/paginators/#listhsmspaginator)
        """

class ListLunaClientsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/paginator/ListLunaClients.html#CloudHSM.Paginator.ListLunaClients)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/paginators/#listlunaclientspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLunaClientsRequestListLunaClientsPaginateTypeDef]
    ) -> _PageIterator[ListLunaClientsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/paginator/ListLunaClients.html#CloudHSM.Paginator.ListLunaClients.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/paginators/#listlunaclientspaginator)
        """
