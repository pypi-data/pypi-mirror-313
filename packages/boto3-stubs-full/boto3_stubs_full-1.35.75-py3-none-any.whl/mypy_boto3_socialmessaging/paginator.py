"""
Type annotations for socialmessaging service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_socialmessaging.client import EndUserMessagingSocialClient
    from mypy_boto3_socialmessaging.paginator import (
        ListLinkedWhatsAppBusinessAccountsPaginator,
    )

    session = Session()
    client: EndUserMessagingSocialClient = session.client("socialmessaging")

    list_linked_whatsapp_business_accounts_paginator: ListLinkedWhatsAppBusinessAccountsPaginator = client.get_paginator("list_linked_whatsapp_business_accounts")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListLinkedWhatsAppBusinessAccountsInputListLinkedWhatsAppBusinessAccountsPaginateTypeDef,
    ListLinkedWhatsAppBusinessAccountsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListLinkedWhatsAppBusinessAccountsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListLinkedWhatsAppBusinessAccountsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListLinkedWhatsAppBusinessAccounts.html#EndUserMessagingSocial.Paginator.ListLinkedWhatsAppBusinessAccounts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/paginators/#listlinkedwhatsappbusinessaccountspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListLinkedWhatsAppBusinessAccountsInputListLinkedWhatsAppBusinessAccountsPaginateTypeDef
        ],
    ) -> _PageIterator[ListLinkedWhatsAppBusinessAccountsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListLinkedWhatsAppBusinessAccounts.html#EndUserMessagingSocial.Paginator.ListLinkedWhatsAppBusinessAccounts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/paginators/#listlinkedwhatsappbusinessaccountspaginator)
        """
