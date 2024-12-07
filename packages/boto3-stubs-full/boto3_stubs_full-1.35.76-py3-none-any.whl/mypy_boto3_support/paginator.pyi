"""
Type annotations for support service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_support.client import SupportClient
    from mypy_boto3_support.paginator import (
        DescribeCasesPaginator,
        DescribeCommunicationsPaginator,
    )

    session = Session()
    client: SupportClient = session.client("support")

    describe_cases_paginator: DescribeCasesPaginator = client.get_paginator("describe_cases")
    describe_communications_paginator: DescribeCommunicationsPaginator = client.get_paginator("describe_communications")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeCasesRequestDescribeCasesPaginateTypeDef,
    DescribeCasesResponseTypeDef,
    DescribeCommunicationsRequestDescribeCommunicationsPaginateTypeDef,
    DescribeCommunicationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("DescribeCasesPaginator", "DescribeCommunicationsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeCasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/paginator/DescribeCases.html#Support.Paginator.DescribeCases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/paginators/#describecasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeCasesRequestDescribeCasesPaginateTypeDef]
    ) -> _PageIterator[DescribeCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/paginator/DescribeCases.html#Support.Paginator.DescribeCases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/paginators/#describecasespaginator)
        """

class DescribeCommunicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/paginator/DescribeCommunications.html#Support.Paginator.DescribeCommunications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/paginators/#describecommunicationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeCommunicationsRequestDescribeCommunicationsPaginateTypeDef]
    ) -> _PageIterator[DescribeCommunicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/paginator/DescribeCommunications.html#Support.Paginator.DescribeCommunications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/paginators/#describecommunicationspaginator)
        """
