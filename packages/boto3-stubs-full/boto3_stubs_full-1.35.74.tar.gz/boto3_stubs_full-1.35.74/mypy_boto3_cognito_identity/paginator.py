"""
Type annotations for cognito-identity service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_identity/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_cognito_identity.client import CognitoIdentityClient
    from mypy_boto3_cognito_identity.paginator import (
        ListIdentityPoolsPaginator,
    )

    session = Session()
    client: CognitoIdentityClient = session.client("cognito-identity")

    list_identity_pools_paginator: ListIdentityPoolsPaginator = client.get_paginator("list_identity_pools")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListIdentityPoolsInputListIdentityPoolsPaginateTypeDef,
    ListIdentityPoolsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListIdentityPoolsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListIdentityPoolsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/paginator/ListIdentityPools.html#CognitoIdentity.Paginator.ListIdentityPools)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_identity/paginators/#listidentitypoolspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListIdentityPoolsInputListIdentityPoolsPaginateTypeDef]
    ) -> _PageIterator[ListIdentityPoolsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/paginator/ListIdentityPools.html#CognitoIdentity.Paginator.ListIdentityPools.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_identity/paginators/#listidentitypoolspaginator)
        """
