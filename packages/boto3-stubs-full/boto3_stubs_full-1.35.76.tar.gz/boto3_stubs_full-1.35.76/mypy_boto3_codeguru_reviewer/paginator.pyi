"""
Type annotations for codeguru-reviewer service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_codeguru_reviewer.client import CodeGuruReviewerClient
    from mypy_boto3_codeguru_reviewer.paginator import (
        ListRepositoryAssociationsPaginator,
    )

    session = Session()
    client: CodeGuruReviewerClient = session.client("codeguru-reviewer")

    list_repository_associations_paginator: ListRepositoryAssociationsPaginator = client.get_paginator("list_repository_associations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListRepositoryAssociationsRequestListRepositoryAssociationsPaginateTypeDef,
    ListRepositoryAssociationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListRepositoryAssociationsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListRepositoryAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/paginator/ListRepositoryAssociations.html#CodeGuruReviewer.Paginator.ListRepositoryAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/paginators/#listrepositoryassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListRepositoryAssociationsRequestListRepositoryAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListRepositoryAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/paginator/ListRepositoryAssociations.html#CodeGuruReviewer.Paginator.ListRepositoryAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/paginators/#listrepositoryassociationspaginator)
        """
