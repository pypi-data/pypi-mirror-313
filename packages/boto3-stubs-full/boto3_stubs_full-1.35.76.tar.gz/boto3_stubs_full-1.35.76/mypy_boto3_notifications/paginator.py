"""
Type annotations for notifications service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_notifications.client import UserNotificationsClient
    from mypy_boto3_notifications.paginator import (
        ListChannelsPaginator,
        ListEventRulesPaginator,
        ListNotificationConfigurationsPaginator,
        ListNotificationEventsPaginator,
        ListNotificationHubsPaginator,
    )

    session = Session()
    client: UserNotificationsClient = session.client("notifications")

    list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
    list_event_rules_paginator: ListEventRulesPaginator = client.get_paginator("list_event_rules")
    list_notification_configurations_paginator: ListNotificationConfigurationsPaginator = client.get_paginator("list_notification_configurations")
    list_notification_events_paginator: ListNotificationEventsPaginator = client.get_paginator("list_notification_events")
    list_notification_hubs_paginator: ListNotificationHubsPaginator = client.get_paginator("list_notification_hubs")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListChannelsRequestListChannelsPaginateTypeDef,
    ListChannelsResponseTypeDef,
    ListEventRulesRequestListEventRulesPaginateTypeDef,
    ListEventRulesResponseTypeDef,
    ListNotificationConfigurationsRequestListNotificationConfigurationsPaginateTypeDef,
    ListNotificationConfigurationsResponseTypeDef,
    ListNotificationEventsRequestListNotificationEventsPaginateTypeDef,
    ListNotificationEventsResponseTypeDef,
    ListNotificationHubsRequestListNotificationHubsPaginateTypeDef,
    ListNotificationHubsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListChannelsPaginator",
    "ListEventRulesPaginator",
    "ListNotificationConfigurationsPaginator",
    "ListNotificationEventsPaginator",
    "ListNotificationHubsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListChannelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListChannels.html#UserNotifications.Paginator.ListChannels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/paginators/#listchannelspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListChannelsRequestListChannelsPaginateTypeDef]
    ) -> _PageIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListChannels.html#UserNotifications.Paginator.ListChannels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/paginators/#listchannelspaginator)
        """


class ListEventRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListEventRules.html#UserNotifications.Paginator.ListEventRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/paginators/#listeventrulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEventRulesRequestListEventRulesPaginateTypeDef]
    ) -> _PageIterator[ListEventRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListEventRules.html#UserNotifications.Paginator.ListEventRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/paginators/#listeventrulespaginator)
        """


class ListNotificationConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationConfigurations.html#UserNotifications.Paginator.ListNotificationConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/paginators/#listnotificationconfigurationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListNotificationConfigurationsRequestListNotificationConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListNotificationConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationConfigurations.html#UserNotifications.Paginator.ListNotificationConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/paginators/#listnotificationconfigurationspaginator)
        """


class ListNotificationEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationEvents.html#UserNotifications.Paginator.ListNotificationEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/paginators/#listnotificationeventspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListNotificationEventsRequestListNotificationEventsPaginateTypeDef]
    ) -> _PageIterator[ListNotificationEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationEvents.html#UserNotifications.Paginator.ListNotificationEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/paginators/#listnotificationeventspaginator)
        """


class ListNotificationHubsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationHubs.html#UserNotifications.Paginator.ListNotificationHubs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/paginators/#listnotificationhubspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListNotificationHubsRequestListNotificationHubsPaginateTypeDef]
    ) -> _PageIterator[ListNotificationHubsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationHubs.html#UserNotifications.Paginator.ListNotificationHubs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/paginators/#listnotificationhubspaginator)
        """
