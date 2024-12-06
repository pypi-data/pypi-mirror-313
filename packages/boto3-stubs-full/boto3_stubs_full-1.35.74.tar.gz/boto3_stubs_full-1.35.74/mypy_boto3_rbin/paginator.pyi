"""
Type annotations for rbin service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rbin/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_rbin.client import RecycleBinClient
    from mypy_boto3_rbin.paginator import (
        ListRulesPaginator,
    )

    session = Session()
    client: RecycleBinClient = session.client("rbin")

    list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListRulesRequestListRulesPaginateTypeDef, ListRulesResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListRulesPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/paginator/ListRules.html#RecycleBin.Paginator.ListRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rbin/paginators/#listrulespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRulesRequestListRulesPaginateTypeDef]
    ) -> _PageIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/paginator/ListRules.html#RecycleBin.Paginator.ListRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rbin/paginators/#listrulespaginator)
        """
