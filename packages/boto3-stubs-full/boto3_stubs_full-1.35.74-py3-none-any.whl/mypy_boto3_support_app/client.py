"""
Type annotations for support-app service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support_app/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_support_app.client import SupportAppClient

    session = Session()
    client: SupportAppClient = session.client("support-app")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateSlackChannelConfigurationRequestRequestTypeDef,
    DeleteSlackChannelConfigurationRequestRequestTypeDef,
    DeleteSlackWorkspaceConfigurationRequestRequestTypeDef,
    GetAccountAliasResultTypeDef,
    ListSlackChannelConfigurationsRequestRequestTypeDef,
    ListSlackChannelConfigurationsResultTypeDef,
    ListSlackWorkspaceConfigurationsRequestRequestTypeDef,
    ListSlackWorkspaceConfigurationsResultTypeDef,
    PutAccountAliasRequestRequestTypeDef,
    RegisterSlackWorkspaceForOrganizationRequestRequestTypeDef,
    RegisterSlackWorkspaceForOrganizationResultTypeDef,
    UpdateSlackChannelConfigurationRequestRequestTypeDef,
    UpdateSlackChannelConfigurationResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("SupportAppClient",)


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
    ValidationException: Type[BotocoreClientError]


class SupportAppClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app.html#SupportApp.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support_app/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SupportAppClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app.html#SupportApp.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support_app/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support_app/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support_app/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support_app/client/#close)
        """

    def create_slack_channel_configuration(
        self, **kwargs: Unpack[CreateSlackChannelConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a Slack channel configuration for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/create_slack_channel_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support_app/client/#create_slack_channel_configuration)
        """

    def delete_account_alias(self) -> Dict[str, Any]:
        """
        Deletes an alias for an Amazon Web Services account ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/delete_account_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support_app/client/#delete_account_alias)
        """

    def delete_slack_channel_configuration(
        self, **kwargs: Unpack[DeleteSlackChannelConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Slack channel configuration from your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/delete_slack_channel_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support_app/client/#delete_slack_channel_configuration)
        """

    def delete_slack_workspace_configuration(
        self, **kwargs: Unpack[DeleteSlackWorkspaceConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Slack workspace configuration from your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/delete_slack_workspace_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support_app/client/#delete_slack_workspace_configuration)
        """

    def get_account_alias(self) -> GetAccountAliasResultTypeDef:
        """
        Retrieves the alias from an Amazon Web Services account ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/get_account_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support_app/client/#get_account_alias)
        """

    def list_slack_channel_configurations(
        self, **kwargs: Unpack[ListSlackChannelConfigurationsRequestRequestTypeDef]
    ) -> ListSlackChannelConfigurationsResultTypeDef:
        """
        Lists the Slack channel configurations for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/list_slack_channel_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support_app/client/#list_slack_channel_configurations)
        """

    def list_slack_workspace_configurations(
        self, **kwargs: Unpack[ListSlackWorkspaceConfigurationsRequestRequestTypeDef]
    ) -> ListSlackWorkspaceConfigurationsResultTypeDef:
        """
        Lists the Slack workspace configurations for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/list_slack_workspace_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support_app/client/#list_slack_workspace_configurations)
        """

    def put_account_alias(
        self, **kwargs: Unpack[PutAccountAliasRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates or updates an individual alias for each Amazon Web Services account ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/put_account_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support_app/client/#put_account_alias)
        """

    def register_slack_workspace_for_organization(
        self, **kwargs: Unpack[RegisterSlackWorkspaceForOrganizationRequestRequestTypeDef]
    ) -> RegisterSlackWorkspaceForOrganizationResultTypeDef:
        """
        Registers a Slack workspace for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/register_slack_workspace_for_organization.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support_app/client/#register_slack_workspace_for_organization)
        """

    def update_slack_channel_configuration(
        self, **kwargs: Unpack[UpdateSlackChannelConfigurationRequestRequestTypeDef]
    ) -> UpdateSlackChannelConfigurationResultTypeDef:
        """
        Updates the configuration for a Slack channel, such as case update
        notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/update_slack_channel_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support_app/client/#update_slack_channel_configuration)
        """
