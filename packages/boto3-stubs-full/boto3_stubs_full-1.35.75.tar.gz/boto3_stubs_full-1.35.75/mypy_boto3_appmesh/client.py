"""
Type annotations for appmesh service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_appmesh.client import AppMeshClient

    session = Session()
    client: AppMeshClient = session.client("appmesh")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListGatewayRoutesPaginator,
    ListMeshesPaginator,
    ListRoutesPaginator,
    ListTagsForResourcePaginator,
    ListVirtualGatewaysPaginator,
    ListVirtualNodesPaginator,
    ListVirtualRoutersPaginator,
    ListVirtualServicesPaginator,
)
from .type_defs import (
    CreateGatewayRouteInputRequestTypeDef,
    CreateGatewayRouteOutputTypeDef,
    CreateMeshInputRequestTypeDef,
    CreateMeshOutputTypeDef,
    CreateRouteInputRequestTypeDef,
    CreateRouteOutputTypeDef,
    CreateVirtualGatewayInputRequestTypeDef,
    CreateVirtualGatewayOutputTypeDef,
    CreateVirtualNodeInputRequestTypeDef,
    CreateVirtualNodeOutputTypeDef,
    CreateVirtualRouterInputRequestTypeDef,
    CreateVirtualRouterOutputTypeDef,
    CreateVirtualServiceInputRequestTypeDef,
    CreateVirtualServiceOutputTypeDef,
    DeleteGatewayRouteInputRequestTypeDef,
    DeleteGatewayRouteOutputTypeDef,
    DeleteMeshInputRequestTypeDef,
    DeleteMeshOutputTypeDef,
    DeleteRouteInputRequestTypeDef,
    DeleteRouteOutputTypeDef,
    DeleteVirtualGatewayInputRequestTypeDef,
    DeleteVirtualGatewayOutputTypeDef,
    DeleteVirtualNodeInputRequestTypeDef,
    DeleteVirtualNodeOutputTypeDef,
    DeleteVirtualRouterInputRequestTypeDef,
    DeleteVirtualRouterOutputTypeDef,
    DeleteVirtualServiceInputRequestTypeDef,
    DeleteVirtualServiceOutputTypeDef,
    DescribeGatewayRouteInputRequestTypeDef,
    DescribeGatewayRouteOutputTypeDef,
    DescribeMeshInputRequestTypeDef,
    DescribeMeshOutputTypeDef,
    DescribeRouteInputRequestTypeDef,
    DescribeRouteOutputTypeDef,
    DescribeVirtualGatewayInputRequestTypeDef,
    DescribeVirtualGatewayOutputTypeDef,
    DescribeVirtualNodeInputRequestTypeDef,
    DescribeVirtualNodeOutputTypeDef,
    DescribeVirtualRouterInputRequestTypeDef,
    DescribeVirtualRouterOutputTypeDef,
    DescribeVirtualServiceInputRequestTypeDef,
    DescribeVirtualServiceOutputTypeDef,
    ListGatewayRoutesInputRequestTypeDef,
    ListGatewayRoutesOutputTypeDef,
    ListMeshesInputRequestTypeDef,
    ListMeshesOutputTypeDef,
    ListRoutesInputRequestTypeDef,
    ListRoutesOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListVirtualGatewaysInputRequestTypeDef,
    ListVirtualGatewaysOutputTypeDef,
    ListVirtualNodesInputRequestTypeDef,
    ListVirtualNodesOutputTypeDef,
    ListVirtualRoutersInputRequestTypeDef,
    ListVirtualRoutersOutputTypeDef,
    ListVirtualServicesInputRequestTypeDef,
    ListVirtualServicesOutputTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateGatewayRouteInputRequestTypeDef,
    UpdateGatewayRouteOutputTypeDef,
    UpdateMeshInputRequestTypeDef,
    UpdateMeshOutputTypeDef,
    UpdateRouteInputRequestTypeDef,
    UpdateRouteOutputTypeDef,
    UpdateVirtualGatewayInputRequestTypeDef,
    UpdateVirtualGatewayOutputTypeDef,
    UpdateVirtualNodeInputRequestTypeDef,
    UpdateVirtualNodeOutputTypeDef,
    UpdateVirtualRouterInputRequestTypeDef,
    UpdateVirtualRouterOutputTypeDef,
    UpdateVirtualServiceInputRequestTypeDef,
    UpdateVirtualServiceOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("AppMeshClient",)


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
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]


class AppMeshClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppMeshClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#close)
        """

    def create_gateway_route(
        self, **kwargs: Unpack[CreateGatewayRouteInputRequestTypeDef]
    ) -> CreateGatewayRouteOutputTypeDef:
        """
        Creates a gateway route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/create_gateway_route.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#create_gateway_route)
        """

    def create_mesh(
        self, **kwargs: Unpack[CreateMeshInputRequestTypeDef]
    ) -> CreateMeshOutputTypeDef:
        """
        Creates a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/create_mesh.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#create_mesh)
        """

    def create_route(
        self, **kwargs: Unpack[CreateRouteInputRequestTypeDef]
    ) -> CreateRouteOutputTypeDef:
        """
        Creates a route that is associated with a virtual router.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/create_route.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#create_route)
        """

    def create_virtual_gateway(
        self, **kwargs: Unpack[CreateVirtualGatewayInputRequestTypeDef]
    ) -> CreateVirtualGatewayOutputTypeDef:
        """
        Creates a virtual gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/create_virtual_gateway.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#create_virtual_gateway)
        """

    def create_virtual_node(
        self, **kwargs: Unpack[CreateVirtualNodeInputRequestTypeDef]
    ) -> CreateVirtualNodeOutputTypeDef:
        """
        Creates a virtual node within a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/create_virtual_node.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#create_virtual_node)
        """

    def create_virtual_router(
        self, **kwargs: Unpack[CreateVirtualRouterInputRequestTypeDef]
    ) -> CreateVirtualRouterOutputTypeDef:
        """
        Creates a virtual router within a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/create_virtual_router.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#create_virtual_router)
        """

    def create_virtual_service(
        self, **kwargs: Unpack[CreateVirtualServiceInputRequestTypeDef]
    ) -> CreateVirtualServiceOutputTypeDef:
        """
        Creates a virtual service within a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/create_virtual_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#create_virtual_service)
        """

    def delete_gateway_route(
        self, **kwargs: Unpack[DeleteGatewayRouteInputRequestTypeDef]
    ) -> DeleteGatewayRouteOutputTypeDef:
        """
        Deletes an existing gateway route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/delete_gateway_route.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#delete_gateway_route)
        """

    def delete_mesh(
        self, **kwargs: Unpack[DeleteMeshInputRequestTypeDef]
    ) -> DeleteMeshOutputTypeDef:
        """
        Deletes an existing service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/delete_mesh.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#delete_mesh)
        """

    def delete_route(
        self, **kwargs: Unpack[DeleteRouteInputRequestTypeDef]
    ) -> DeleteRouteOutputTypeDef:
        """
        Deletes an existing route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/delete_route.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#delete_route)
        """

    def delete_virtual_gateway(
        self, **kwargs: Unpack[DeleteVirtualGatewayInputRequestTypeDef]
    ) -> DeleteVirtualGatewayOutputTypeDef:
        """
        Deletes an existing virtual gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/delete_virtual_gateway.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#delete_virtual_gateway)
        """

    def delete_virtual_node(
        self, **kwargs: Unpack[DeleteVirtualNodeInputRequestTypeDef]
    ) -> DeleteVirtualNodeOutputTypeDef:
        """
        Deletes an existing virtual node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/delete_virtual_node.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#delete_virtual_node)
        """

    def delete_virtual_router(
        self, **kwargs: Unpack[DeleteVirtualRouterInputRequestTypeDef]
    ) -> DeleteVirtualRouterOutputTypeDef:
        """
        Deletes an existing virtual router.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/delete_virtual_router.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#delete_virtual_router)
        """

    def delete_virtual_service(
        self, **kwargs: Unpack[DeleteVirtualServiceInputRequestTypeDef]
    ) -> DeleteVirtualServiceOutputTypeDef:
        """
        Deletes an existing virtual service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/delete_virtual_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#delete_virtual_service)
        """

    def describe_gateway_route(
        self, **kwargs: Unpack[DescribeGatewayRouteInputRequestTypeDef]
    ) -> DescribeGatewayRouteOutputTypeDef:
        """
        Describes an existing gateway route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/describe_gateway_route.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#describe_gateway_route)
        """

    def describe_mesh(
        self, **kwargs: Unpack[DescribeMeshInputRequestTypeDef]
    ) -> DescribeMeshOutputTypeDef:
        """
        Describes an existing service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/describe_mesh.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#describe_mesh)
        """

    def describe_route(
        self, **kwargs: Unpack[DescribeRouteInputRequestTypeDef]
    ) -> DescribeRouteOutputTypeDef:
        """
        Describes an existing route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/describe_route.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#describe_route)
        """

    def describe_virtual_gateway(
        self, **kwargs: Unpack[DescribeVirtualGatewayInputRequestTypeDef]
    ) -> DescribeVirtualGatewayOutputTypeDef:
        """
        Describes an existing virtual gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/describe_virtual_gateway.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#describe_virtual_gateway)
        """

    def describe_virtual_node(
        self, **kwargs: Unpack[DescribeVirtualNodeInputRequestTypeDef]
    ) -> DescribeVirtualNodeOutputTypeDef:
        """
        Describes an existing virtual node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/describe_virtual_node.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#describe_virtual_node)
        """

    def describe_virtual_router(
        self, **kwargs: Unpack[DescribeVirtualRouterInputRequestTypeDef]
    ) -> DescribeVirtualRouterOutputTypeDef:
        """
        Describes an existing virtual router.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/describe_virtual_router.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#describe_virtual_router)
        """

    def describe_virtual_service(
        self, **kwargs: Unpack[DescribeVirtualServiceInputRequestTypeDef]
    ) -> DescribeVirtualServiceOutputTypeDef:
        """
        Describes an existing virtual service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/describe_virtual_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#describe_virtual_service)
        """

    def list_gateway_routes(
        self, **kwargs: Unpack[ListGatewayRoutesInputRequestTypeDef]
    ) -> ListGatewayRoutesOutputTypeDef:
        """
        Returns a list of existing gateway routes that are associated to a virtual
        gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/list_gateway_routes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#list_gateway_routes)
        """

    def list_meshes(
        self, **kwargs: Unpack[ListMeshesInputRequestTypeDef]
    ) -> ListMeshesOutputTypeDef:
        """
        Returns a list of existing service meshes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/list_meshes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#list_meshes)
        """

    def list_routes(
        self, **kwargs: Unpack[ListRoutesInputRequestTypeDef]
    ) -> ListRoutesOutputTypeDef:
        """
        Returns a list of existing routes in a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/list_routes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#list_routes)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        List the tags for an App Mesh resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#list_tags_for_resource)
        """

    def list_virtual_gateways(
        self, **kwargs: Unpack[ListVirtualGatewaysInputRequestTypeDef]
    ) -> ListVirtualGatewaysOutputTypeDef:
        """
        Returns a list of existing virtual gateways in a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/list_virtual_gateways.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#list_virtual_gateways)
        """

    def list_virtual_nodes(
        self, **kwargs: Unpack[ListVirtualNodesInputRequestTypeDef]
    ) -> ListVirtualNodesOutputTypeDef:
        """
        Returns a list of existing virtual nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/list_virtual_nodes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#list_virtual_nodes)
        """

    def list_virtual_routers(
        self, **kwargs: Unpack[ListVirtualRoutersInputRequestTypeDef]
    ) -> ListVirtualRoutersOutputTypeDef:
        """
        Returns a list of existing virtual routers in a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/list_virtual_routers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#list_virtual_routers)
        """

    def list_virtual_services(
        self, **kwargs: Unpack[ListVirtualServicesInputRequestTypeDef]
    ) -> ListVirtualServicesOutputTypeDef:
        """
        Returns a list of existing virtual services in a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/list_virtual_services.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#list_virtual_services)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified
        <code>resourceArn</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#untag_resource)
        """

    def update_gateway_route(
        self, **kwargs: Unpack[UpdateGatewayRouteInputRequestTypeDef]
    ) -> UpdateGatewayRouteOutputTypeDef:
        """
        Updates an existing gateway route that is associated to a specified virtual
        gateway in a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/update_gateway_route.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#update_gateway_route)
        """

    def update_mesh(
        self, **kwargs: Unpack[UpdateMeshInputRequestTypeDef]
    ) -> UpdateMeshOutputTypeDef:
        """
        Updates an existing service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/update_mesh.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#update_mesh)
        """

    def update_route(
        self, **kwargs: Unpack[UpdateRouteInputRequestTypeDef]
    ) -> UpdateRouteOutputTypeDef:
        """
        Updates an existing route for a specified service mesh and virtual router.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/update_route.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#update_route)
        """

    def update_virtual_gateway(
        self, **kwargs: Unpack[UpdateVirtualGatewayInputRequestTypeDef]
    ) -> UpdateVirtualGatewayOutputTypeDef:
        """
        Updates an existing virtual gateway in a specified service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/update_virtual_gateway.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#update_virtual_gateway)
        """

    def update_virtual_node(
        self, **kwargs: Unpack[UpdateVirtualNodeInputRequestTypeDef]
    ) -> UpdateVirtualNodeOutputTypeDef:
        """
        Updates an existing virtual node in a specified service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/update_virtual_node.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#update_virtual_node)
        """

    def update_virtual_router(
        self, **kwargs: Unpack[UpdateVirtualRouterInputRequestTypeDef]
    ) -> UpdateVirtualRouterOutputTypeDef:
        """
        Updates an existing virtual router in a specified service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/update_virtual_router.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#update_virtual_router)
        """

    def update_virtual_service(
        self, **kwargs: Unpack[UpdateVirtualServiceInputRequestTypeDef]
    ) -> UpdateVirtualServiceOutputTypeDef:
        """
        Updates an existing virtual service in a specified service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/update_virtual_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#update_virtual_service)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_gateway_routes"]
    ) -> ListGatewayRoutesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_meshes"]) -> ListMeshesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_routes"]) -> ListRoutesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_virtual_gateways"]
    ) -> ListVirtualGatewaysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_virtual_nodes"]
    ) -> ListVirtualNodesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_virtual_routers"]
    ) -> ListVirtualRoutersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_virtual_services"]
    ) -> ListVirtualServicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#get_paginator)
        """
