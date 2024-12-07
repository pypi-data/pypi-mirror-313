"""
Type annotations for notifications service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_notifications.client import UserNotificationsClient

    session = Session()
    client: UserNotificationsClient = session.client("notifications")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListChannelsPaginator,
    ListEventRulesPaginator,
    ListNotificationConfigurationsPaginator,
    ListNotificationEventsPaginator,
    ListNotificationHubsPaginator,
)
from .type_defs import (
    AssociateChannelRequestRequestTypeDef,
    CreateEventRuleRequestRequestTypeDef,
    CreateEventRuleResponseTypeDef,
    CreateNotificationConfigurationRequestRequestTypeDef,
    CreateNotificationConfigurationResponseTypeDef,
    DeleteEventRuleRequestRequestTypeDef,
    DeleteNotificationConfigurationRequestRequestTypeDef,
    DeregisterNotificationHubRequestRequestTypeDef,
    DeregisterNotificationHubResponseTypeDef,
    DisassociateChannelRequestRequestTypeDef,
    GetEventRuleRequestRequestTypeDef,
    GetEventRuleResponseTypeDef,
    GetNotificationConfigurationRequestRequestTypeDef,
    GetNotificationConfigurationResponseTypeDef,
    GetNotificationEventRequestRequestTypeDef,
    GetNotificationEventResponseTypeDef,
    ListChannelsRequestRequestTypeDef,
    ListChannelsResponseTypeDef,
    ListEventRulesRequestRequestTypeDef,
    ListEventRulesResponseTypeDef,
    ListNotificationConfigurationsRequestRequestTypeDef,
    ListNotificationConfigurationsResponseTypeDef,
    ListNotificationEventsRequestRequestTypeDef,
    ListNotificationEventsResponseTypeDef,
    ListNotificationHubsRequestRequestTypeDef,
    ListNotificationHubsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RegisterNotificationHubRequestRequestTypeDef,
    RegisterNotificationHubResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateEventRuleRequestRequestTypeDef,
    UpdateEventRuleResponseTypeDef,
    UpdateNotificationConfigurationRequestRequestTypeDef,
    UpdateNotificationConfigurationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("UserNotificationsClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class UserNotificationsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications.html#UserNotifications.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        UserNotificationsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications.html#UserNotifications.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#close)
        """

    def associate_channel(
        self, **kwargs: Unpack[AssociateChannelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a delivery <a
        href="https://docs.aws.amazon.com/notifications/latest/userguide/managing-delivery-channels.html">Channel</a>
        with a particular NotificationConfiguration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/associate_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#associate_channel)
        """

    def create_event_rule(
        self, **kwargs: Unpack[CreateEventRuleRequestRequestTypeDef]
    ) -> CreateEventRuleResponseTypeDef:
        """
        Creates an <a
        href="https://docs.aws.amazon.com/notifications/latest/userguide/glossary.html">EventRule</a>
        that is associated with a specified Notification Configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/create_event_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#create_event_rule)
        """

    def create_notification_configuration(
        self, **kwargs: Unpack[CreateNotificationConfigurationRequestRequestTypeDef]
    ) -> CreateNotificationConfigurationResponseTypeDef:
        """
        Creates a new NotificationConfiguration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/create_notification_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#create_notification_configuration)
        """

    def delete_event_rule(
        self, **kwargs: Unpack[DeleteEventRuleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an EventRule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/delete_event_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#delete_event_rule)
        """

    def delete_notification_configuration(
        self, **kwargs: Unpack[DeleteNotificationConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a NotificationConfiguration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/delete_notification_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#delete_notification_configuration)
        """

    def deregister_notification_hub(
        self, **kwargs: Unpack[DeregisterNotificationHubRequestRequestTypeDef]
    ) -> DeregisterNotificationHubResponseTypeDef:
        """
        Deregisters a NotificationHub in the specified Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/deregister_notification_hub.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#deregister_notification_hub)
        """

    def disassociate_channel(
        self, **kwargs: Unpack[DisassociateChannelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a Channel from a specified NotificationConfiguration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/disassociate_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#disassociate_channel)
        """

    def get_event_rule(
        self, **kwargs: Unpack[GetEventRuleRequestRequestTypeDef]
    ) -> GetEventRuleResponseTypeDef:
        """
        Returns a specified EventRule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_event_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#get_event_rule)
        """

    def get_notification_configuration(
        self, **kwargs: Unpack[GetNotificationConfigurationRequestRequestTypeDef]
    ) -> GetNotificationConfigurationResponseTypeDef:
        """
        Returns a specified NotificationConfiguration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_notification_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#get_notification_configuration)
        """

    def get_notification_event(
        self, **kwargs: Unpack[GetNotificationEventRequestRequestTypeDef]
    ) -> GetNotificationEventResponseTypeDef:
        """
        Returns a specified NotificationEvent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_notification_event.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#get_notification_event)
        """

    def list_channels(
        self, **kwargs: Unpack[ListChannelsRequestRequestTypeDef]
    ) -> ListChannelsResponseTypeDef:
        """
        Returns a list of Channels for a NotificationConfiguration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_channels.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#list_channels)
        """

    def list_event_rules(
        self, **kwargs: Unpack[ListEventRulesRequestRequestTypeDef]
    ) -> ListEventRulesResponseTypeDef:
        """
        Returns a list of EventRules according to specified filters, in reverse
        chronological order (newest first).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_event_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#list_event_rules)
        """

    def list_notification_configurations(
        self, **kwargs: Unpack[ListNotificationConfigurationsRequestRequestTypeDef]
    ) -> ListNotificationConfigurationsResponseTypeDef:
        """
        Returns a list of abbreviated NotificationConfigurations according to specified
        filters, in reverse chronological order (newest first).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_notification_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#list_notification_configurations)
        """

    def list_notification_events(
        self, **kwargs: Unpack[ListNotificationEventsRequestRequestTypeDef]
    ) -> ListNotificationEventsResponseTypeDef:
        """
        Returns a list of NotificationEvents according to specified filters, in reverse
        chronological order (newest first).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_notification_events.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#list_notification_events)
        """

    def list_notification_hubs(
        self, **kwargs: Unpack[ListNotificationHubsRequestRequestTypeDef]
    ) -> ListNotificationHubsResponseTypeDef:
        """
        Returns a list of NotificationHubs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_notification_hubs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#list_notification_hubs)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a specified Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#list_tags_for_resource)
        """

    def register_notification_hub(
        self, **kwargs: Unpack[RegisterNotificationHubRequestRequestTypeDef]
    ) -> RegisterNotificationHubResponseTypeDef:
        """
        Registers a NotificationHub in the specified Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/register_notification_hub.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#register_notification_hub)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags the resource with a tag key and value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Untags a resource with a specified Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#untag_resource)
        """

    def update_event_rule(
        self, **kwargs: Unpack[UpdateEventRuleRequestRequestTypeDef]
    ) -> UpdateEventRuleResponseTypeDef:
        """
        Updates an existing EventRule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/update_event_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#update_event_rule)
        """

    def update_notification_configuration(
        self, **kwargs: Unpack[UpdateNotificationConfigurationRequestRequestTypeDef]
    ) -> UpdateNotificationConfigurationResponseTypeDef:
        """
        Updates a NotificationConfiguration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/update_notification_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#update_notification_configuration)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_channels"]) -> ListChannelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_event_rules"]) -> ListEventRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_notification_configurations"]
    ) -> ListNotificationConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_notification_events"]
    ) -> ListNotificationEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_notification_hubs"]
    ) -> ListNotificationHubsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notifications/client/#get_paginator)
        """
