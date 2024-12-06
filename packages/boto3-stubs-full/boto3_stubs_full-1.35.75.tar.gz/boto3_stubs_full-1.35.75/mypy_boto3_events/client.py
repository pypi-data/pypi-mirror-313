"""
Type annotations for events service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_events.client import EventBridgeClient

    session = Session()
    client: EventBridgeClient = session.client("events")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListRuleNamesByTargetPaginator,
    ListRulesPaginator,
    ListTargetsByRulePaginator,
)
from .type_defs import (
    ActivateEventSourceRequestRequestTypeDef,
    CancelReplayRequestRequestTypeDef,
    CancelReplayResponseTypeDef,
    CreateApiDestinationRequestRequestTypeDef,
    CreateApiDestinationResponseTypeDef,
    CreateArchiveRequestRequestTypeDef,
    CreateArchiveResponseTypeDef,
    CreateConnectionRequestRequestTypeDef,
    CreateConnectionResponseTypeDef,
    CreateEndpointRequestRequestTypeDef,
    CreateEndpointResponseTypeDef,
    CreateEventBusRequestRequestTypeDef,
    CreateEventBusResponseTypeDef,
    CreatePartnerEventSourceRequestRequestTypeDef,
    CreatePartnerEventSourceResponseTypeDef,
    DeactivateEventSourceRequestRequestTypeDef,
    DeauthorizeConnectionRequestRequestTypeDef,
    DeauthorizeConnectionResponseTypeDef,
    DeleteApiDestinationRequestRequestTypeDef,
    DeleteArchiveRequestRequestTypeDef,
    DeleteConnectionRequestRequestTypeDef,
    DeleteConnectionResponseTypeDef,
    DeleteEndpointRequestRequestTypeDef,
    DeleteEventBusRequestRequestTypeDef,
    DeletePartnerEventSourceRequestRequestTypeDef,
    DeleteRuleRequestRequestTypeDef,
    DescribeApiDestinationRequestRequestTypeDef,
    DescribeApiDestinationResponseTypeDef,
    DescribeArchiveRequestRequestTypeDef,
    DescribeArchiveResponseTypeDef,
    DescribeConnectionRequestRequestTypeDef,
    DescribeConnectionResponseTypeDef,
    DescribeEndpointRequestRequestTypeDef,
    DescribeEndpointResponseTypeDef,
    DescribeEventBusRequestRequestTypeDef,
    DescribeEventBusResponseTypeDef,
    DescribeEventSourceRequestRequestTypeDef,
    DescribeEventSourceResponseTypeDef,
    DescribePartnerEventSourceRequestRequestTypeDef,
    DescribePartnerEventSourceResponseTypeDef,
    DescribeReplayRequestRequestTypeDef,
    DescribeReplayResponseTypeDef,
    DescribeRuleRequestRequestTypeDef,
    DescribeRuleResponseTypeDef,
    DisableRuleRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableRuleRequestRequestTypeDef,
    ListApiDestinationsRequestRequestTypeDef,
    ListApiDestinationsResponseTypeDef,
    ListArchivesRequestRequestTypeDef,
    ListArchivesResponseTypeDef,
    ListConnectionsRequestRequestTypeDef,
    ListConnectionsResponseTypeDef,
    ListEndpointsRequestRequestTypeDef,
    ListEndpointsResponseTypeDef,
    ListEventBusesRequestRequestTypeDef,
    ListEventBusesResponseTypeDef,
    ListEventSourcesRequestRequestTypeDef,
    ListEventSourcesResponseTypeDef,
    ListPartnerEventSourceAccountsRequestRequestTypeDef,
    ListPartnerEventSourceAccountsResponseTypeDef,
    ListPartnerEventSourcesRequestRequestTypeDef,
    ListPartnerEventSourcesResponseTypeDef,
    ListReplaysRequestRequestTypeDef,
    ListReplaysResponseTypeDef,
    ListRuleNamesByTargetRequestRequestTypeDef,
    ListRuleNamesByTargetResponseTypeDef,
    ListRulesRequestRequestTypeDef,
    ListRulesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTargetsByRuleRequestRequestTypeDef,
    ListTargetsByRuleResponseTypeDef,
    PutEventsRequestRequestTypeDef,
    PutEventsResponseTypeDef,
    PutPartnerEventsRequestRequestTypeDef,
    PutPartnerEventsResponseTypeDef,
    PutPermissionRequestRequestTypeDef,
    PutRuleRequestRequestTypeDef,
    PutRuleResponseTypeDef,
    PutTargetsRequestRequestTypeDef,
    PutTargetsResponseTypeDef,
    RemovePermissionRequestRequestTypeDef,
    RemoveTargetsRequestRequestTypeDef,
    RemoveTargetsResponseTypeDef,
    StartReplayRequestRequestTypeDef,
    StartReplayResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    TestEventPatternRequestRequestTypeDef,
    TestEventPatternResponseTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateApiDestinationRequestRequestTypeDef,
    UpdateApiDestinationResponseTypeDef,
    UpdateArchiveRequestRequestTypeDef,
    UpdateArchiveResponseTypeDef,
    UpdateConnectionRequestRequestTypeDef,
    UpdateConnectionResponseTypeDef,
    UpdateEndpointRequestRequestTypeDef,
    UpdateEndpointResponseTypeDef,
    UpdateEventBusRequestRequestTypeDef,
    UpdateEventBusResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("EventBridgeClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    IllegalStatusException: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidEventPatternException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ManagedRuleException: Type[BotocoreClientError]
    OperationDisabledException: Type[BotocoreClientError]
    PolicyLengthExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class EventBridgeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EventBridgeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#close)
        """

    def activate_event_source(
        self, **kwargs: Unpack[ActivateEventSourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Activates a partner event source that has been deactivated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/activate_event_source.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#activate_event_source)
        """

    def cancel_replay(
        self, **kwargs: Unpack[CancelReplayRequestRequestTypeDef]
    ) -> CancelReplayResponseTypeDef:
        """
        Cancels the specified replay.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/cancel_replay.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#cancel_replay)
        """

    def create_api_destination(
        self, **kwargs: Unpack[CreateApiDestinationRequestRequestTypeDef]
    ) -> CreateApiDestinationResponseTypeDef:
        """
        Creates an API destination, which is an HTTP invocation endpoint configured as
        a target for events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/create_api_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#create_api_destination)
        """

    def create_archive(
        self, **kwargs: Unpack[CreateArchiveRequestRequestTypeDef]
    ) -> CreateArchiveResponseTypeDef:
        """
        Creates an archive of events with the specified settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/create_archive.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#create_archive)
        """

    def create_connection(
        self, **kwargs: Unpack[CreateConnectionRequestRequestTypeDef]
    ) -> CreateConnectionResponseTypeDef:
        """
        Creates a connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/create_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#create_connection)
        """

    def create_endpoint(
        self, **kwargs: Unpack[CreateEndpointRequestRequestTypeDef]
    ) -> CreateEndpointResponseTypeDef:
        """
        Creates a global endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/create_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#create_endpoint)
        """

    def create_event_bus(
        self, **kwargs: Unpack[CreateEventBusRequestRequestTypeDef]
    ) -> CreateEventBusResponseTypeDef:
        """
        Creates a new event bus within your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/create_event_bus.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#create_event_bus)
        """

    def create_partner_event_source(
        self, **kwargs: Unpack[CreatePartnerEventSourceRequestRequestTypeDef]
    ) -> CreatePartnerEventSourceResponseTypeDef:
        """
        Called by an SaaS partner to create a partner event source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/create_partner_event_source.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#create_partner_event_source)
        """

    def deactivate_event_source(
        self, **kwargs: Unpack[DeactivateEventSourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        You can use this operation to temporarily stop receiving events from the
        specified partner event source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/deactivate_event_source.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#deactivate_event_source)
        """

    def deauthorize_connection(
        self, **kwargs: Unpack[DeauthorizeConnectionRequestRequestTypeDef]
    ) -> DeauthorizeConnectionResponseTypeDef:
        """
        Removes all authorization parameters from the connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/deauthorize_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#deauthorize_connection)
        """

    def delete_api_destination(
        self, **kwargs: Unpack[DeleteApiDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified API destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/delete_api_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#delete_api_destination)
        """

    def delete_archive(
        self, **kwargs: Unpack[DeleteArchiveRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/delete_archive.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#delete_archive)
        """

    def delete_connection(
        self, **kwargs: Unpack[DeleteConnectionRequestRequestTypeDef]
    ) -> DeleteConnectionResponseTypeDef:
        """
        Deletes a connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/delete_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#delete_connection)
        """

    def delete_endpoint(
        self, **kwargs: Unpack[DeleteEndpointRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete an existing global endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/delete_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#delete_endpoint)
        """

    def delete_event_bus(
        self, **kwargs: Unpack[DeleteEventBusRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified custom event bus or partner event bus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/delete_event_bus.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#delete_event_bus)
        """

    def delete_partner_event_source(
        self, **kwargs: Unpack[DeletePartnerEventSourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation is used by SaaS partners to delete a partner event source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/delete_partner_event_source.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#delete_partner_event_source)
        """

    def delete_rule(
        self, **kwargs: Unpack[DeleteRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/delete_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#delete_rule)
        """

    def describe_api_destination(
        self, **kwargs: Unpack[DescribeApiDestinationRequestRequestTypeDef]
    ) -> DescribeApiDestinationResponseTypeDef:
        """
        Retrieves details about an API destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/describe_api_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_api_destination)
        """

    def describe_archive(
        self, **kwargs: Unpack[DescribeArchiveRequestRequestTypeDef]
    ) -> DescribeArchiveResponseTypeDef:
        """
        Retrieves details about an archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/describe_archive.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_archive)
        """

    def describe_connection(
        self, **kwargs: Unpack[DescribeConnectionRequestRequestTypeDef]
    ) -> DescribeConnectionResponseTypeDef:
        """
        Retrieves details about a connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/describe_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_connection)
        """

    def describe_endpoint(
        self, **kwargs: Unpack[DescribeEndpointRequestRequestTypeDef]
    ) -> DescribeEndpointResponseTypeDef:
        """
        Get the information about an existing global endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/describe_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_endpoint)
        """

    def describe_event_bus(
        self, **kwargs: Unpack[DescribeEventBusRequestRequestTypeDef]
    ) -> DescribeEventBusResponseTypeDef:
        """
        Displays details about an event bus in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/describe_event_bus.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_event_bus)
        """

    def describe_event_source(
        self, **kwargs: Unpack[DescribeEventSourceRequestRequestTypeDef]
    ) -> DescribeEventSourceResponseTypeDef:
        """
        This operation lists details about a partner event source that is shared with
        your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/describe_event_source.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_event_source)
        """

    def describe_partner_event_source(
        self, **kwargs: Unpack[DescribePartnerEventSourceRequestRequestTypeDef]
    ) -> DescribePartnerEventSourceResponseTypeDef:
        """
        An SaaS partner can use this operation to list details about a partner event
        source that they have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/describe_partner_event_source.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_partner_event_source)
        """

    def describe_replay(
        self, **kwargs: Unpack[DescribeReplayRequestRequestTypeDef]
    ) -> DescribeReplayResponseTypeDef:
        """
        Retrieves details about a replay.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/describe_replay.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_replay)
        """

    def describe_rule(
        self, **kwargs: Unpack[DescribeRuleRequestRequestTypeDef]
    ) -> DescribeRuleResponseTypeDef:
        """
        Describes the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/describe_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_rule)
        """

    def disable_rule(
        self, **kwargs: Unpack[DisableRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disables the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/disable_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#disable_rule)
        """

    def enable_rule(
        self, **kwargs: Unpack[EnableRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/enable_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#enable_rule)
        """

    def list_api_destinations(
        self, **kwargs: Unpack[ListApiDestinationsRequestRequestTypeDef]
    ) -> ListApiDestinationsResponseTypeDef:
        """
        Retrieves a list of API destination in the account in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/list_api_destinations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_api_destinations)
        """

    def list_archives(
        self, **kwargs: Unpack[ListArchivesRequestRequestTypeDef]
    ) -> ListArchivesResponseTypeDef:
        """
        Lists your archives.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/list_archives.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_archives)
        """

    def list_connections(
        self, **kwargs: Unpack[ListConnectionsRequestRequestTypeDef]
    ) -> ListConnectionsResponseTypeDef:
        """
        Retrieves a list of connections from the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/list_connections.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_connections)
        """

    def list_endpoints(
        self, **kwargs: Unpack[ListEndpointsRequestRequestTypeDef]
    ) -> ListEndpointsResponseTypeDef:
        """
        List the global endpoints associated with this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/list_endpoints.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_endpoints)
        """

    def list_event_buses(
        self, **kwargs: Unpack[ListEventBusesRequestRequestTypeDef]
    ) -> ListEventBusesResponseTypeDef:
        """
        Lists all the event buses in your account, including the default event bus,
        custom event buses, and partner event buses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/list_event_buses.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_event_buses)
        """

    def list_event_sources(
        self, **kwargs: Unpack[ListEventSourcesRequestRequestTypeDef]
    ) -> ListEventSourcesResponseTypeDef:
        """
        You can use this to see all the partner event sources that have been shared
        with your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/list_event_sources.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_event_sources)
        """

    def list_partner_event_source_accounts(
        self, **kwargs: Unpack[ListPartnerEventSourceAccountsRequestRequestTypeDef]
    ) -> ListPartnerEventSourceAccountsResponseTypeDef:
        """
        An SaaS partner can use this operation to display the Amazon Web Services
        account ID that a particular partner event source name is associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/list_partner_event_source_accounts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_partner_event_source_accounts)
        """

    def list_partner_event_sources(
        self, **kwargs: Unpack[ListPartnerEventSourcesRequestRequestTypeDef]
    ) -> ListPartnerEventSourcesResponseTypeDef:
        """
        An SaaS partner can use this operation to list all the partner event source
        names that they have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/list_partner_event_sources.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_partner_event_sources)
        """

    def list_replays(
        self, **kwargs: Unpack[ListReplaysRequestRequestTypeDef]
    ) -> ListReplaysResponseTypeDef:
        """
        Lists your replays.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/list_replays.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_replays)
        """

    def list_rule_names_by_target(
        self, **kwargs: Unpack[ListRuleNamesByTargetRequestRequestTypeDef]
    ) -> ListRuleNamesByTargetResponseTypeDef:
        """
        Lists the rules for the specified target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/list_rule_names_by_target.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_rule_names_by_target)
        """

    def list_rules(
        self, **kwargs: Unpack[ListRulesRequestRequestTypeDef]
    ) -> ListRulesResponseTypeDef:
        """
        Lists your Amazon EventBridge rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/list_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_rules)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Displays the tags associated with an EventBridge resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_tags_for_resource)
        """

    def list_targets_by_rule(
        self, **kwargs: Unpack[ListTargetsByRuleRequestRequestTypeDef]
    ) -> ListTargetsByRuleResponseTypeDef:
        """
        Lists the targets assigned to the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/list_targets_by_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_targets_by_rule)
        """

    def put_events(
        self, **kwargs: Unpack[PutEventsRequestRequestTypeDef]
    ) -> PutEventsResponseTypeDef:
        """
        Sends custom events to Amazon EventBridge so that they can be matched to rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/put_events.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#put_events)
        """

    def put_partner_events(
        self, **kwargs: Unpack[PutPartnerEventsRequestRequestTypeDef]
    ) -> PutPartnerEventsResponseTypeDef:
        """
        This is used by SaaS partners to write events to a customer's partner event bus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/put_partner_events.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#put_partner_events)
        """

    def put_permission(
        self, **kwargs: Unpack[PutPermissionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Running <code>PutPermission</code> permits the specified Amazon Web Services
        account or Amazon Web Services organization to put events to the specified
        <i>event bus</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/put_permission.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#put_permission)
        """

    def put_rule(self, **kwargs: Unpack[PutRuleRequestRequestTypeDef]) -> PutRuleResponseTypeDef:
        """
        Creates or updates the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/put_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#put_rule)
        """

    def put_targets(
        self, **kwargs: Unpack[PutTargetsRequestRequestTypeDef]
    ) -> PutTargetsResponseTypeDef:
        """
        Adds the specified targets to the specified rule, or updates the targets if
        they are already associated with the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/put_targets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#put_targets)
        """

    def remove_permission(
        self, **kwargs: Unpack[RemovePermissionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Revokes the permission of another Amazon Web Services account to be able to put
        events to the specified event bus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/remove_permission.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#remove_permission)
        """

    def remove_targets(
        self, **kwargs: Unpack[RemoveTargetsRequestRequestTypeDef]
    ) -> RemoveTargetsResponseTypeDef:
        """
        Removes the specified targets from the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/remove_targets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#remove_targets)
        """

    def start_replay(
        self, **kwargs: Unpack[StartReplayRequestRequestTypeDef]
    ) -> StartReplayResponseTypeDef:
        """
        Starts the specified replay.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/start_replay.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#start_replay)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified EventBridge
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#tag_resource)
        """

    def test_event_pattern(
        self, **kwargs: Unpack[TestEventPatternRequestRequestTypeDef]
    ) -> TestEventPatternResponseTypeDef:
        """
        Tests whether the specified event pattern matches the provided event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/test_event_pattern.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#test_event_pattern)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified EventBridge resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#untag_resource)
        """

    def update_api_destination(
        self, **kwargs: Unpack[UpdateApiDestinationRequestRequestTypeDef]
    ) -> UpdateApiDestinationResponseTypeDef:
        """
        Updates an API destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/update_api_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#update_api_destination)
        """

    def update_archive(
        self, **kwargs: Unpack[UpdateArchiveRequestRequestTypeDef]
    ) -> UpdateArchiveResponseTypeDef:
        """
        Updates the specified archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/update_archive.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#update_archive)
        """

    def update_connection(
        self, **kwargs: Unpack[UpdateConnectionRequestRequestTypeDef]
    ) -> UpdateConnectionResponseTypeDef:
        """
        Updates settings for a connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/update_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#update_connection)
        """

    def update_endpoint(
        self, **kwargs: Unpack[UpdateEndpointRequestRequestTypeDef]
    ) -> UpdateEndpointResponseTypeDef:
        """
        Update an existing endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/update_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#update_endpoint)
        """

    def update_event_bus(
        self, **kwargs: Unpack[UpdateEventBusRequestRequestTypeDef]
    ) -> UpdateEventBusResponseTypeDef:
        """
        Updates the specified event bus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/update_event_bus.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#update_event_bus)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_rule_names_by_target"]
    ) -> ListRuleNamesByTargetPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_rules"]) -> ListRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_targets_by_rule"]
    ) -> ListTargetsByRulePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#get_paginator)
        """
