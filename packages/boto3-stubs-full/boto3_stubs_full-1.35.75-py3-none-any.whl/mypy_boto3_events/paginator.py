"""
Type annotations for events service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_events.client import EventBridgeClient
    from mypy_boto3_events.paginator import (
        ListRuleNamesByTargetPaginator,
        ListRulesPaginator,
        ListTargetsByRulePaginator,
    )

    session = Session()
    client: EventBridgeClient = session.client("events")

    list_rule_names_by_target_paginator: ListRuleNamesByTargetPaginator = client.get_paginator("list_rule_names_by_target")
    list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    list_targets_by_rule_paginator: ListTargetsByRulePaginator = client.get_paginator("list_targets_by_rule")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListRuleNamesByTargetRequestListRuleNamesByTargetPaginateTypeDef,
    ListRuleNamesByTargetResponseTypeDef,
    ListRulesRequestListRulesPaginateTypeDef,
    ListRulesResponseTypeDef,
    ListTargetsByRuleRequestListTargetsByRulePaginateTypeDef,
    ListTargetsByRuleResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListRuleNamesByTargetPaginator", "ListRulesPaginator", "ListTargetsByRulePaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListRuleNamesByTargetPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListRuleNamesByTarget.html#EventBridge.Paginator.ListRuleNamesByTarget)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/paginators/#listrulenamesbytargetpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRuleNamesByTargetRequestListRuleNamesByTargetPaginateTypeDef]
    ) -> _PageIterator[ListRuleNamesByTargetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListRuleNamesByTarget.html#EventBridge.Paginator.ListRuleNamesByTarget.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/paginators/#listrulenamesbytargetpaginator)
        """


class ListRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListRules.html#EventBridge.Paginator.ListRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/paginators/#listrulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRulesRequestListRulesPaginateTypeDef]
    ) -> _PageIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListRules.html#EventBridge.Paginator.ListRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/paginators/#listrulespaginator)
        """


class ListTargetsByRulePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListTargetsByRule.html#EventBridge.Paginator.ListTargetsByRule)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/paginators/#listtargetsbyrulepaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTargetsByRuleRequestListTargetsByRulePaginateTypeDef]
    ) -> _PageIterator[ListTargetsByRuleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListTargetsByRule.html#EventBridge.Paginator.ListTargetsByRule.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/paginators/#listtargetsbyrulepaginator)
        """
