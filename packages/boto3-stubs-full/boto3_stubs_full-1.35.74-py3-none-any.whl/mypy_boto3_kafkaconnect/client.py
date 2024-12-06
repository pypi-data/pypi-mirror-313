"""
Type annotations for kafkaconnect service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kafkaconnect.client import KafkaConnectClient

    session = Session()
    client: KafkaConnectClient = session.client("kafkaconnect")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListConnectorsPaginator,
    ListCustomPluginsPaginator,
    ListWorkerConfigurationsPaginator,
)
from .type_defs import (
    CreateConnectorRequestRequestTypeDef,
    CreateConnectorResponseTypeDef,
    CreateCustomPluginRequestRequestTypeDef,
    CreateCustomPluginResponseTypeDef,
    CreateWorkerConfigurationRequestRequestTypeDef,
    CreateWorkerConfigurationResponseTypeDef,
    DeleteConnectorRequestRequestTypeDef,
    DeleteConnectorResponseTypeDef,
    DeleteCustomPluginRequestRequestTypeDef,
    DeleteCustomPluginResponseTypeDef,
    DeleteWorkerConfigurationRequestRequestTypeDef,
    DeleteWorkerConfigurationResponseTypeDef,
    DescribeConnectorRequestRequestTypeDef,
    DescribeConnectorResponseTypeDef,
    DescribeCustomPluginRequestRequestTypeDef,
    DescribeCustomPluginResponseTypeDef,
    DescribeWorkerConfigurationRequestRequestTypeDef,
    DescribeWorkerConfigurationResponseTypeDef,
    ListConnectorsRequestRequestTypeDef,
    ListConnectorsResponseTypeDef,
    ListCustomPluginsRequestRequestTypeDef,
    ListCustomPluginsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWorkerConfigurationsRequestRequestTypeDef,
    ListWorkerConfigurationsResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateConnectorRequestRequestTypeDef,
    UpdateConnectorResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("KafkaConnectClient",)


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
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]


class KafkaConnectClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KafkaConnectClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#close)
        """

    def create_connector(
        self, **kwargs: Unpack[CreateConnectorRequestRequestTypeDef]
    ) -> CreateConnectorResponseTypeDef:
        """
        Creates a connector using the specified properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/create_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#create_connector)
        """

    def create_custom_plugin(
        self, **kwargs: Unpack[CreateCustomPluginRequestRequestTypeDef]
    ) -> CreateCustomPluginResponseTypeDef:
        """
        Creates a custom plugin using the specified properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/create_custom_plugin.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#create_custom_plugin)
        """

    def create_worker_configuration(
        self, **kwargs: Unpack[CreateWorkerConfigurationRequestRequestTypeDef]
    ) -> CreateWorkerConfigurationResponseTypeDef:
        """
        Creates a worker configuration using the specified properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/create_worker_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#create_worker_configuration)
        """

    def delete_connector(
        self, **kwargs: Unpack[DeleteConnectorRequestRequestTypeDef]
    ) -> DeleteConnectorResponseTypeDef:
        """
        Deletes the specified connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/delete_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#delete_connector)
        """

    def delete_custom_plugin(
        self, **kwargs: Unpack[DeleteCustomPluginRequestRequestTypeDef]
    ) -> DeleteCustomPluginResponseTypeDef:
        """
        Deletes a custom plugin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/delete_custom_plugin.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#delete_custom_plugin)
        """

    def delete_worker_configuration(
        self, **kwargs: Unpack[DeleteWorkerConfigurationRequestRequestTypeDef]
    ) -> DeleteWorkerConfigurationResponseTypeDef:
        """
        Deletes the specified worker configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/delete_worker_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#delete_worker_configuration)
        """

    def describe_connector(
        self, **kwargs: Unpack[DescribeConnectorRequestRequestTypeDef]
    ) -> DescribeConnectorResponseTypeDef:
        """
        Returns summary information about the connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/describe_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#describe_connector)
        """

    def describe_custom_plugin(
        self, **kwargs: Unpack[DescribeCustomPluginRequestRequestTypeDef]
    ) -> DescribeCustomPluginResponseTypeDef:
        """
        A summary description of the custom plugin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/describe_custom_plugin.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#describe_custom_plugin)
        """

    def describe_worker_configuration(
        self, **kwargs: Unpack[DescribeWorkerConfigurationRequestRequestTypeDef]
    ) -> DescribeWorkerConfigurationResponseTypeDef:
        """
        Returns information about a worker configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/describe_worker_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#describe_worker_configuration)
        """

    def list_connectors(
        self, **kwargs: Unpack[ListConnectorsRequestRequestTypeDef]
    ) -> ListConnectorsResponseTypeDef:
        """
        Returns a list of all the connectors in this account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/list_connectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#list_connectors)
        """

    def list_custom_plugins(
        self, **kwargs: Unpack[ListCustomPluginsRequestRequestTypeDef]
    ) -> ListCustomPluginsResponseTypeDef:
        """
        Returns a list of all of the custom plugins in this account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/list_custom_plugins.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#list_custom_plugins)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all the tags attached to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#list_tags_for_resource)
        """

    def list_worker_configurations(
        self, **kwargs: Unpack[ListWorkerConfigurationsRequestRequestTypeDef]
    ) -> ListWorkerConfigurationsResponseTypeDef:
        """
        Returns a list of all of the worker configurations in this account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/list_worker_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#list_worker_configurations)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Attaches tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#untag_resource)
        """

    def update_connector(
        self, **kwargs: Unpack[UpdateConnectorRequestRequestTypeDef]
    ) -> UpdateConnectorResponseTypeDef:
        """
        Updates the specified connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/update_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#update_connector)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_connectors"]) -> ListConnectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_plugins"]
    ) -> ListCustomPluginsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_worker_configurations"]
    ) -> ListWorkerConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/client/#get_paginator)
        """
