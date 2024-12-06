"""
Type annotations for codestar-notifications service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar_notifications/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_codestar_notifications.client import CodeStarNotificationsClient
    from mypy_boto3_codestar_notifications.paginator import (
        ListEventTypesPaginator,
        ListNotificationRulesPaginator,
        ListTargetsPaginator,
    )

    session = Session()
    client: CodeStarNotificationsClient = session.client("codestar-notifications")

    list_event_types_paginator: ListEventTypesPaginator = client.get_paginator("list_event_types")
    list_notification_rules_paginator: ListNotificationRulesPaginator = client.get_paginator("list_notification_rules")
    list_targets_paginator: ListTargetsPaginator = client.get_paginator("list_targets")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListEventTypesRequestListEventTypesPaginateTypeDef,
    ListEventTypesResultTypeDef,
    ListNotificationRulesRequestListNotificationRulesPaginateTypeDef,
    ListNotificationRulesResultTypeDef,
    ListTargetsRequestListTargetsPaginateTypeDef,
    ListTargetsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListEventTypesPaginator", "ListNotificationRulesPaginator", "ListTargetsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListEventTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListEventTypes.html#CodeStarNotifications.Paginator.ListEventTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar_notifications/paginators/#listeventtypespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEventTypesRequestListEventTypesPaginateTypeDef]
    ) -> _PageIterator[ListEventTypesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListEventTypes.html#CodeStarNotifications.Paginator.ListEventTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar_notifications/paginators/#listeventtypespaginator)
        """

class ListNotificationRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListNotificationRules.html#CodeStarNotifications.Paginator.ListNotificationRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar_notifications/paginators/#listnotificationrulespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListNotificationRulesRequestListNotificationRulesPaginateTypeDef]
    ) -> _PageIterator[ListNotificationRulesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListNotificationRules.html#CodeStarNotifications.Paginator.ListNotificationRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar_notifications/paginators/#listnotificationrulespaginator)
        """

class ListTargetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListTargets.html#CodeStarNotifications.Paginator.ListTargets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar_notifications/paginators/#listtargetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTargetsRequestListTargetsPaginateTypeDef]
    ) -> _PageIterator[ListTargetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListTargets.html#CodeStarNotifications.Paginator.ListTargets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar_notifications/paginators/#listtargetspaginator)
        """
