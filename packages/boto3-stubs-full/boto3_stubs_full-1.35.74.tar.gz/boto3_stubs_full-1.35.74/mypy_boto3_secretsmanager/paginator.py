"""
Type annotations for secretsmanager service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_secretsmanager/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_secretsmanager.client import SecretsManagerClient
    from mypy_boto3_secretsmanager.paginator import (
        ListSecretsPaginator,
    )

    session = Session()
    client: SecretsManagerClient = session.client("secretsmanager")

    list_secrets_paginator: ListSecretsPaginator = client.get_paginator("list_secrets")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListSecretsRequestListSecretsPaginateTypeDef, ListSecretsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListSecretsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListSecretsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/paginator/ListSecrets.html#SecretsManager.Paginator.ListSecrets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_secretsmanager/paginators/#listsecretspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSecretsRequestListSecretsPaginateTypeDef]
    ) -> _PageIterator[ListSecretsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/paginator/ListSecrets.html#SecretsManager.Paginator.ListSecrets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_secretsmanager/paginators/#listsecretspaginator)
        """
