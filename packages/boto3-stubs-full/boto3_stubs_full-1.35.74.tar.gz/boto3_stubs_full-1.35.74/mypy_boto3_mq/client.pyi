"""
Type annotations for mq service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_mq.client import MQClient

    session = Session()
    client: MQClient = session.client("mq")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListBrokersPaginator
from .type_defs import (
    CreateBrokerRequestRequestTypeDef,
    CreateBrokerResponseTypeDef,
    CreateConfigurationRequestRequestTypeDef,
    CreateConfigurationResponseTypeDef,
    CreateTagsRequestRequestTypeDef,
    CreateUserRequestRequestTypeDef,
    DeleteBrokerRequestRequestTypeDef,
    DeleteBrokerResponseTypeDef,
    DeleteTagsRequestRequestTypeDef,
    DeleteUserRequestRequestTypeDef,
    DescribeBrokerEngineTypesRequestRequestTypeDef,
    DescribeBrokerEngineTypesResponseTypeDef,
    DescribeBrokerInstanceOptionsRequestRequestTypeDef,
    DescribeBrokerInstanceOptionsResponseTypeDef,
    DescribeBrokerRequestRequestTypeDef,
    DescribeBrokerResponseTypeDef,
    DescribeConfigurationRequestRequestTypeDef,
    DescribeConfigurationResponseTypeDef,
    DescribeConfigurationRevisionRequestRequestTypeDef,
    DescribeConfigurationRevisionResponseTypeDef,
    DescribeUserRequestRequestTypeDef,
    DescribeUserResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ListBrokersRequestRequestTypeDef,
    ListBrokersResponseTypeDef,
    ListConfigurationRevisionsRequestRequestTypeDef,
    ListConfigurationRevisionsResponseTypeDef,
    ListConfigurationsRequestRequestTypeDef,
    ListConfigurationsResponseTypeDef,
    ListTagsRequestRequestTypeDef,
    ListTagsResponseTypeDef,
    ListUsersRequestRequestTypeDef,
    ListUsersResponseTypeDef,
    PromoteRequestRequestTypeDef,
    PromoteResponseTypeDef,
    RebootBrokerRequestRequestTypeDef,
    UpdateBrokerRequestRequestTypeDef,
    UpdateBrokerResponseTypeDef,
    UpdateConfigurationRequestRequestTypeDef,
    UpdateConfigurationResponseTypeDef,
    UpdateUserRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("MQClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]

class MQClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MQClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#close)
        """

    def create_broker(
        self, **kwargs: Unpack[CreateBrokerRequestRequestTypeDef]
    ) -> CreateBrokerResponseTypeDef:
        """
        Creates a broker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/create_broker.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#create_broker)
        """

    def create_configuration(
        self, **kwargs: Unpack[CreateConfigurationRequestRequestTypeDef]
    ) -> CreateConfigurationResponseTypeDef:
        """
        Creates a new configuration for the specified configuration name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/create_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#create_configuration)
        """

    def create_tags(
        self, **kwargs: Unpack[CreateTagsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Add a tag to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/create_tags.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#create_tags)
        """

    def create_user(self, **kwargs: Unpack[CreateUserRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Creates an ActiveMQ user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/create_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#create_user)
        """

    def delete_broker(
        self, **kwargs: Unpack[DeleteBrokerRequestRequestTypeDef]
    ) -> DeleteBrokerResponseTypeDef:
        """
        Deletes a broker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/delete_broker.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#delete_broker)
        """

    def delete_tags(
        self, **kwargs: Unpack[DeleteTagsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/delete_tags.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#delete_tags)
        """

    def delete_user(self, **kwargs: Unpack[DeleteUserRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes an ActiveMQ user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/delete_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#delete_user)
        """

    def describe_broker(
        self, **kwargs: Unpack[DescribeBrokerRequestRequestTypeDef]
    ) -> DescribeBrokerResponseTypeDef:
        """
        Returns information about the specified broker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/describe_broker.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#describe_broker)
        """

    def describe_broker_engine_types(
        self, **kwargs: Unpack[DescribeBrokerEngineTypesRequestRequestTypeDef]
    ) -> DescribeBrokerEngineTypesResponseTypeDef:
        """
        Describe available engine types and versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/describe_broker_engine_types.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#describe_broker_engine_types)
        """

    def describe_broker_instance_options(
        self, **kwargs: Unpack[DescribeBrokerInstanceOptionsRequestRequestTypeDef]
    ) -> DescribeBrokerInstanceOptionsResponseTypeDef:
        """
        Describe available broker instance options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/describe_broker_instance_options.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#describe_broker_instance_options)
        """

    def describe_configuration(
        self, **kwargs: Unpack[DescribeConfigurationRequestRequestTypeDef]
    ) -> DescribeConfigurationResponseTypeDef:
        """
        Returns information about the specified configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/describe_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#describe_configuration)
        """

    def describe_configuration_revision(
        self, **kwargs: Unpack[DescribeConfigurationRevisionRequestRequestTypeDef]
    ) -> DescribeConfigurationRevisionResponseTypeDef:
        """
        Returns the specified configuration revision for the specified configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/describe_configuration_revision.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#describe_configuration_revision)
        """

    def describe_user(
        self, **kwargs: Unpack[DescribeUserRequestRequestTypeDef]
    ) -> DescribeUserResponseTypeDef:
        """
        Returns information about an ActiveMQ user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/describe_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#describe_user)
        """

    def list_brokers(
        self, **kwargs: Unpack[ListBrokersRequestRequestTypeDef]
    ) -> ListBrokersResponseTypeDef:
        """
        Returns a list of all brokers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/list_brokers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#list_brokers)
        """

    def list_configuration_revisions(
        self, **kwargs: Unpack[ListConfigurationRevisionsRequestRequestTypeDef]
    ) -> ListConfigurationRevisionsResponseTypeDef:
        """
        Returns a list of all revisions for the specified configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/list_configuration_revisions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#list_configuration_revisions)
        """

    def list_configurations(
        self, **kwargs: Unpack[ListConfigurationsRequestRequestTypeDef]
    ) -> ListConfigurationsResponseTypeDef:
        """
        Returns a list of all configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/list_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#list_configurations)
        """

    def list_tags(self, **kwargs: Unpack[ListTagsRequestRequestTypeDef]) -> ListTagsResponseTypeDef:
        """
        Lists tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/list_tags.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#list_tags)
        """

    def list_users(
        self, **kwargs: Unpack[ListUsersRequestRequestTypeDef]
    ) -> ListUsersResponseTypeDef:
        """
        Returns a list of all ActiveMQ users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/list_users.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#list_users)
        """

    def promote(self, **kwargs: Unpack[PromoteRequestRequestTypeDef]) -> PromoteResponseTypeDef:
        """
        Promotes a data replication replica broker to the primary broker role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/promote.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#promote)
        """

    def reboot_broker(self, **kwargs: Unpack[RebootBrokerRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Reboots a broker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/reboot_broker.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#reboot_broker)
        """

    def update_broker(
        self, **kwargs: Unpack[UpdateBrokerRequestRequestTypeDef]
    ) -> UpdateBrokerResponseTypeDef:
        """
        Adds a pending configuration change to a broker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/update_broker.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#update_broker)
        """

    def update_configuration(
        self, **kwargs: Unpack[UpdateConfigurationRequestRequestTypeDef]
    ) -> UpdateConfigurationResponseTypeDef:
        """
        Updates the specified configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/update_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#update_configuration)
        """

    def update_user(self, **kwargs: Unpack[UpdateUserRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates the information for an ActiveMQ user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/update_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#update_user)
        """

    def get_paginator(self, operation_name: Literal["list_brokers"]) -> ListBrokersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#get_paginator)
        """
