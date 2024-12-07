"""
Type annotations for chatbot service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_chatbot.client import ChatbotClient
    from mypy_boto3_chatbot.paginator import (
        DescribeChimeWebhookConfigurationsPaginator,
        DescribeSlackChannelConfigurationsPaginator,
        DescribeSlackUserIdentitiesPaginator,
        DescribeSlackWorkspacesPaginator,
        ListAssociationsPaginator,
        ListCustomActionsPaginator,
        ListMicrosoftTeamsChannelConfigurationsPaginator,
        ListMicrosoftTeamsConfiguredTeamsPaginator,
        ListMicrosoftTeamsUserIdentitiesPaginator,
    )

    session = Session()
    client: ChatbotClient = session.client("chatbot")

    describe_chime_webhook_configurations_paginator: DescribeChimeWebhookConfigurationsPaginator = client.get_paginator("describe_chime_webhook_configurations")
    describe_slack_channel_configurations_paginator: DescribeSlackChannelConfigurationsPaginator = client.get_paginator("describe_slack_channel_configurations")
    describe_slack_user_identities_paginator: DescribeSlackUserIdentitiesPaginator = client.get_paginator("describe_slack_user_identities")
    describe_slack_workspaces_paginator: DescribeSlackWorkspacesPaginator = client.get_paginator("describe_slack_workspaces")
    list_associations_paginator: ListAssociationsPaginator = client.get_paginator("list_associations")
    list_custom_actions_paginator: ListCustomActionsPaginator = client.get_paginator("list_custom_actions")
    list_microsoft_teams_channel_configurations_paginator: ListMicrosoftTeamsChannelConfigurationsPaginator = client.get_paginator("list_microsoft_teams_channel_configurations")
    list_microsoft_teams_configured_teams_paginator: ListMicrosoftTeamsConfiguredTeamsPaginator = client.get_paginator("list_microsoft_teams_configured_teams")
    list_microsoft_teams_user_identities_paginator: ListMicrosoftTeamsUserIdentitiesPaginator = client.get_paginator("list_microsoft_teams_user_identities")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeChimeWebhookConfigurationsRequestDescribeChimeWebhookConfigurationsPaginateTypeDef,
    DescribeChimeWebhookConfigurationsResultTypeDef,
    DescribeSlackChannelConfigurationsRequestDescribeSlackChannelConfigurationsPaginateTypeDef,
    DescribeSlackChannelConfigurationsResultTypeDef,
    DescribeSlackUserIdentitiesRequestDescribeSlackUserIdentitiesPaginateTypeDef,
    DescribeSlackUserIdentitiesResultTypeDef,
    DescribeSlackWorkspacesRequestDescribeSlackWorkspacesPaginateTypeDef,
    DescribeSlackWorkspacesResultTypeDef,
    ListAssociationsRequestListAssociationsPaginateTypeDef,
    ListAssociationsResultTypeDef,
    ListCustomActionsRequestListCustomActionsPaginateTypeDef,
    ListCustomActionsResultTypeDef,
    ListMicrosoftTeamsConfiguredTeamsRequestListMicrosoftTeamsConfiguredTeamsPaginateTypeDef,
    ListMicrosoftTeamsConfiguredTeamsResultTypeDef,
    ListMicrosoftTeamsUserIdentitiesRequestListMicrosoftTeamsUserIdentitiesPaginateTypeDef,
    ListMicrosoftTeamsUserIdentitiesResultTypeDef,
    ListTeamsChannelConfigurationsRequestListMicrosoftTeamsChannelConfigurationsPaginateTypeDef,
    ListTeamsChannelConfigurationsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeChimeWebhookConfigurationsPaginator",
    "DescribeSlackChannelConfigurationsPaginator",
    "DescribeSlackUserIdentitiesPaginator",
    "DescribeSlackWorkspacesPaginator",
    "ListAssociationsPaginator",
    "ListCustomActionsPaginator",
    "ListMicrosoftTeamsChannelConfigurationsPaginator",
    "ListMicrosoftTeamsConfiguredTeamsPaginator",
    "ListMicrosoftTeamsUserIdentitiesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeChimeWebhookConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeChimeWebhookConfigurations.html#Chatbot.Paginator.DescribeChimeWebhookConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#describechimewebhookconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeChimeWebhookConfigurationsRequestDescribeChimeWebhookConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeChimeWebhookConfigurationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeChimeWebhookConfigurations.html#Chatbot.Paginator.DescribeChimeWebhookConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#describechimewebhookconfigurationspaginator)
        """

class DescribeSlackChannelConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackChannelConfigurations.html#Chatbot.Paginator.DescribeSlackChannelConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#describeslackchannelconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeSlackChannelConfigurationsRequestDescribeSlackChannelConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeSlackChannelConfigurationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackChannelConfigurations.html#Chatbot.Paginator.DescribeSlackChannelConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#describeslackchannelconfigurationspaginator)
        """

class DescribeSlackUserIdentitiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackUserIdentities.html#Chatbot.Paginator.DescribeSlackUserIdentities)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#describeslackuseridentitiespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeSlackUserIdentitiesRequestDescribeSlackUserIdentitiesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeSlackUserIdentitiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackUserIdentities.html#Chatbot.Paginator.DescribeSlackUserIdentities.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#describeslackuseridentitiespaginator)
        """

class DescribeSlackWorkspacesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackWorkspaces.html#Chatbot.Paginator.DescribeSlackWorkspaces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#describeslackworkspacespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeSlackWorkspacesRequestDescribeSlackWorkspacesPaginateTypeDef]
    ) -> _PageIterator[DescribeSlackWorkspacesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackWorkspaces.html#Chatbot.Paginator.DescribeSlackWorkspaces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#describeslackworkspacespaginator)
        """

class ListAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListAssociations.html#Chatbot.Paginator.ListAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#listassociationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAssociationsRequestListAssociationsPaginateTypeDef]
    ) -> _PageIterator[ListAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListAssociations.html#Chatbot.Paginator.ListAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#listassociationspaginator)
        """

class ListCustomActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListCustomActions.html#Chatbot.Paginator.ListCustomActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#listcustomactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCustomActionsRequestListCustomActionsPaginateTypeDef]
    ) -> _PageIterator[ListCustomActionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListCustomActions.html#Chatbot.Paginator.ListCustomActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#listcustomactionspaginator)
        """

class ListMicrosoftTeamsChannelConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsChannelConfigurations.html#Chatbot.Paginator.ListMicrosoftTeamsChannelConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#listmicrosoftteamschannelconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListTeamsChannelConfigurationsRequestListMicrosoftTeamsChannelConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListTeamsChannelConfigurationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsChannelConfigurations.html#Chatbot.Paginator.ListMicrosoftTeamsChannelConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#listmicrosoftteamschannelconfigurationspaginator)
        """

class ListMicrosoftTeamsConfiguredTeamsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsConfiguredTeams.html#Chatbot.Paginator.ListMicrosoftTeamsConfiguredTeams)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#listmicrosoftteamsconfiguredteamspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListMicrosoftTeamsConfiguredTeamsRequestListMicrosoftTeamsConfiguredTeamsPaginateTypeDef
        ],
    ) -> _PageIterator[ListMicrosoftTeamsConfiguredTeamsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsConfiguredTeams.html#Chatbot.Paginator.ListMicrosoftTeamsConfiguredTeams.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#listmicrosoftteamsconfiguredteamspaginator)
        """

class ListMicrosoftTeamsUserIdentitiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsUserIdentities.html#Chatbot.Paginator.ListMicrosoftTeamsUserIdentities)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#listmicrosoftteamsuseridentitiespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListMicrosoftTeamsUserIdentitiesRequestListMicrosoftTeamsUserIdentitiesPaginateTypeDef
        ],
    ) -> _PageIterator[ListMicrosoftTeamsUserIdentitiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsUserIdentities.html#Chatbot.Paginator.ListMicrosoftTeamsUserIdentities.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/paginators/#listmicrosoftteamsuseridentitiespaginator)
        """
