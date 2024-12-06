"""
Type annotations for servicediscovery service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_servicediscovery.client import ServiceDiscoveryClient

    session = Session()
    client: ServiceDiscoveryClient = session.client("servicediscovery")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListInstancesPaginator,
    ListNamespacesPaginator,
    ListOperationsPaginator,
    ListServicesPaginator,
)
from .type_defs import (
    CreateHttpNamespaceRequestRequestTypeDef,
    CreateHttpNamespaceResponseTypeDef,
    CreatePrivateDnsNamespaceRequestRequestTypeDef,
    CreatePrivateDnsNamespaceResponseTypeDef,
    CreatePublicDnsNamespaceRequestRequestTypeDef,
    CreatePublicDnsNamespaceResponseTypeDef,
    CreateServiceRequestRequestTypeDef,
    CreateServiceResponseTypeDef,
    DeleteNamespaceRequestRequestTypeDef,
    DeleteNamespaceResponseTypeDef,
    DeleteServiceRequestRequestTypeDef,
    DeregisterInstanceRequestRequestTypeDef,
    DeregisterInstanceResponseTypeDef,
    DiscoverInstancesRequestRequestTypeDef,
    DiscoverInstancesResponseTypeDef,
    DiscoverInstancesRevisionRequestRequestTypeDef,
    DiscoverInstancesRevisionResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetInstanceRequestRequestTypeDef,
    GetInstanceResponseTypeDef,
    GetInstancesHealthStatusRequestRequestTypeDef,
    GetInstancesHealthStatusResponseTypeDef,
    GetNamespaceRequestRequestTypeDef,
    GetNamespaceResponseTypeDef,
    GetOperationRequestRequestTypeDef,
    GetOperationResponseTypeDef,
    GetServiceRequestRequestTypeDef,
    GetServiceResponseTypeDef,
    ListInstancesRequestRequestTypeDef,
    ListInstancesResponseTypeDef,
    ListNamespacesRequestRequestTypeDef,
    ListNamespacesResponseTypeDef,
    ListOperationsRequestRequestTypeDef,
    ListOperationsResponseTypeDef,
    ListServicesRequestRequestTypeDef,
    ListServicesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RegisterInstanceRequestRequestTypeDef,
    RegisterInstanceResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateHttpNamespaceRequestRequestTypeDef,
    UpdateHttpNamespaceResponseTypeDef,
    UpdateInstanceCustomHealthStatusRequestRequestTypeDef,
    UpdatePrivateDnsNamespaceRequestRequestTypeDef,
    UpdatePrivateDnsNamespaceResponseTypeDef,
    UpdatePublicDnsNamespaceRequestRequestTypeDef,
    UpdatePublicDnsNamespaceResponseTypeDef,
    UpdateServiceRequestRequestTypeDef,
    UpdateServiceResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ServiceDiscoveryClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    CustomHealthNotFound: Type[BotocoreClientError]
    DuplicateRequest: Type[BotocoreClientError]
    InstanceNotFound: Type[BotocoreClientError]
    InvalidInput: Type[BotocoreClientError]
    NamespaceAlreadyExists: Type[BotocoreClientError]
    NamespaceNotFound: Type[BotocoreClientError]
    OperationNotFound: Type[BotocoreClientError]
    RequestLimitExceeded: Type[BotocoreClientError]
    ResourceInUse: Type[BotocoreClientError]
    ResourceLimitExceeded: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceAlreadyExists: Type[BotocoreClientError]
    ServiceNotFound: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]

class ServiceDiscoveryClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ServiceDiscoveryClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#close)
        """

    def create_http_namespace(
        self, **kwargs: Unpack[CreateHttpNamespaceRequestRequestTypeDef]
    ) -> CreateHttpNamespaceResponseTypeDef:
        """
        Creates an HTTP namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/create_http_namespace.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#create_http_namespace)
        """

    def create_private_dns_namespace(
        self, **kwargs: Unpack[CreatePrivateDnsNamespaceRequestRequestTypeDef]
    ) -> CreatePrivateDnsNamespaceResponseTypeDef:
        """
        Creates a private namespace based on DNS, which is visible only inside a
        specified Amazon VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/create_private_dns_namespace.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#create_private_dns_namespace)
        """

    def create_public_dns_namespace(
        self, **kwargs: Unpack[CreatePublicDnsNamespaceRequestRequestTypeDef]
    ) -> CreatePublicDnsNamespaceResponseTypeDef:
        """
        Creates a public namespace based on DNS, which is visible on the internet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/create_public_dns_namespace.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#create_public_dns_namespace)
        """

    def create_service(
        self, **kwargs: Unpack[CreateServiceRequestRequestTypeDef]
    ) -> CreateServiceResponseTypeDef:
        """
        Creates a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/create_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#create_service)
        """

    def delete_namespace(
        self, **kwargs: Unpack[DeleteNamespaceRequestRequestTypeDef]
    ) -> DeleteNamespaceResponseTypeDef:
        """
        Deletes a namespace from the current account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/delete_namespace.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#delete_namespace)
        """

    def delete_service(
        self, **kwargs: Unpack[DeleteServiceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/delete_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#delete_service)
        """

    def deregister_instance(
        self, **kwargs: Unpack[DeregisterInstanceRequestRequestTypeDef]
    ) -> DeregisterInstanceResponseTypeDef:
        """
        Deletes the Amazon Route 53 DNS records and health check, if any, that Cloud
        Map created for the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/deregister_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#deregister_instance)
        """

    def discover_instances(
        self, **kwargs: Unpack[DiscoverInstancesRequestRequestTypeDef]
    ) -> DiscoverInstancesResponseTypeDef:
        """
        Discovers registered instances for a specified namespace and service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/discover_instances.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#discover_instances)
        """

    def discover_instances_revision(
        self, **kwargs: Unpack[DiscoverInstancesRevisionRequestRequestTypeDef]
    ) -> DiscoverInstancesRevisionResponseTypeDef:
        """
        Discovers the increasing revision associated with an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/discover_instances_revision.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#discover_instances_revision)
        """

    def get_instance(
        self, **kwargs: Unpack[GetInstanceRequestRequestTypeDef]
    ) -> GetInstanceResponseTypeDef:
        """
        Gets information about a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_instance)
        """

    def get_instances_health_status(
        self, **kwargs: Unpack[GetInstancesHealthStatusRequestRequestTypeDef]
    ) -> GetInstancesHealthStatusResponseTypeDef:
        """
        Gets the current health status (<code>Healthy</code>, <code>Unhealthy</code>,
        or <code>Unknown</code>) of one or more instances that are associated with a
        specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_instances_health_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_instances_health_status)
        """

    def get_namespace(
        self, **kwargs: Unpack[GetNamespaceRequestRequestTypeDef]
    ) -> GetNamespaceResponseTypeDef:
        """
        Gets information about a namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_namespace.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_namespace)
        """

    def get_operation(
        self, **kwargs: Unpack[GetOperationRequestRequestTypeDef]
    ) -> GetOperationResponseTypeDef:
        """
        Gets information about any operation that returns an operation ID in the
        response, such as a <code>CreateHttpNamespace</code> request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_operation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_operation)
        """

    def get_service(
        self, **kwargs: Unpack[GetServiceRequestRequestTypeDef]
    ) -> GetServiceResponseTypeDef:
        """
        Gets the settings for a specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_service)
        """

    def list_instances(
        self, **kwargs: Unpack[ListInstancesRequestRequestTypeDef]
    ) -> ListInstancesResponseTypeDef:
        """
        Lists summary information about the instances that you registered by using a
        specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/list_instances.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#list_instances)
        """

    def list_namespaces(
        self, **kwargs: Unpack[ListNamespacesRequestRequestTypeDef]
    ) -> ListNamespacesResponseTypeDef:
        """
        Lists summary information about the namespaces that were created by the current
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/list_namespaces.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#list_namespaces)
        """

    def list_operations(
        self, **kwargs: Unpack[ListOperationsRequestRequestTypeDef]
    ) -> ListOperationsResponseTypeDef:
        """
        Lists operations that match the criteria that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/list_operations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#list_operations)
        """

    def list_services(
        self, **kwargs: Unpack[ListServicesRequestRequestTypeDef]
    ) -> ListServicesResponseTypeDef:
        """
        Lists summary information for all the services that are associated with one or
        more namespaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/list_services.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#list_services)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#list_tags_for_resource)
        """

    def register_instance(
        self, **kwargs: Unpack[RegisterInstanceRequestRequestTypeDef]
    ) -> RegisterInstanceResponseTypeDef:
        """
        Creates or updates one or more records and, optionally, creates a health check
        based on the settings in a specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/register_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#register_instance)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#untag_resource)
        """

    def update_http_namespace(
        self, **kwargs: Unpack[UpdateHttpNamespaceRequestRequestTypeDef]
    ) -> UpdateHttpNamespaceResponseTypeDef:
        """
        Updates an HTTP namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/update_http_namespace.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#update_http_namespace)
        """

    def update_instance_custom_health_status(
        self, **kwargs: Unpack[UpdateInstanceCustomHealthStatusRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Submits a request to change the health status of a custom health check to
        healthy or unhealthy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/update_instance_custom_health_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#update_instance_custom_health_status)
        """

    def update_private_dns_namespace(
        self, **kwargs: Unpack[UpdatePrivateDnsNamespaceRequestRequestTypeDef]
    ) -> UpdatePrivateDnsNamespaceResponseTypeDef:
        """
        Updates a private DNS namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/update_private_dns_namespace.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#update_private_dns_namespace)
        """

    def update_public_dns_namespace(
        self, **kwargs: Unpack[UpdatePublicDnsNamespaceRequestRequestTypeDef]
    ) -> UpdatePublicDnsNamespaceResponseTypeDef:
        """
        Updates a public DNS namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/update_public_dns_namespace.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#update_public_dns_namespace)
        """

    def update_service(
        self, **kwargs: Unpack[UpdateServiceRequestRequestTypeDef]
    ) -> UpdateServiceResponseTypeDef:
        """
        Submits a request to perform the following operations:.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/update_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#update_service)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_instances"]) -> ListInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_namespaces"]) -> ListNamespacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_operations"]) -> ListOperationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_services"]) -> ListServicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_paginator)
        """
