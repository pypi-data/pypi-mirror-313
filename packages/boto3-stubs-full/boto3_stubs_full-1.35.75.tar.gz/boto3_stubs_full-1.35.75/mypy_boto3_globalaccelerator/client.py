"""
Type annotations for globalaccelerator service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_globalaccelerator.client import GlobalAcceleratorClient

    session = Session()
    client: GlobalAcceleratorClient = session.client("globalaccelerator")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListAcceleratorsPaginator,
    ListByoipCidrsPaginator,
    ListCrossAccountAttachmentsPaginator,
    ListCrossAccountResourcesPaginator,
    ListCustomRoutingAcceleratorsPaginator,
    ListCustomRoutingEndpointGroupsPaginator,
    ListCustomRoutingListenersPaginator,
    ListCustomRoutingPortMappingsByDestinationPaginator,
    ListCustomRoutingPortMappingsPaginator,
    ListEndpointGroupsPaginator,
    ListListenersPaginator,
)
from .type_defs import (
    AddCustomRoutingEndpointsRequestRequestTypeDef,
    AddCustomRoutingEndpointsResponseTypeDef,
    AddEndpointsRequestRequestTypeDef,
    AddEndpointsResponseTypeDef,
    AdvertiseByoipCidrRequestRequestTypeDef,
    AdvertiseByoipCidrResponseTypeDef,
    AllowCustomRoutingTrafficRequestRequestTypeDef,
    CreateAcceleratorRequestRequestTypeDef,
    CreateAcceleratorResponseTypeDef,
    CreateCrossAccountAttachmentRequestRequestTypeDef,
    CreateCrossAccountAttachmentResponseTypeDef,
    CreateCustomRoutingAcceleratorRequestRequestTypeDef,
    CreateCustomRoutingAcceleratorResponseTypeDef,
    CreateCustomRoutingEndpointGroupRequestRequestTypeDef,
    CreateCustomRoutingEndpointGroupResponseTypeDef,
    CreateCustomRoutingListenerRequestRequestTypeDef,
    CreateCustomRoutingListenerResponseTypeDef,
    CreateEndpointGroupRequestRequestTypeDef,
    CreateEndpointGroupResponseTypeDef,
    CreateListenerRequestRequestTypeDef,
    CreateListenerResponseTypeDef,
    DeleteAcceleratorRequestRequestTypeDef,
    DeleteCrossAccountAttachmentRequestRequestTypeDef,
    DeleteCustomRoutingAcceleratorRequestRequestTypeDef,
    DeleteCustomRoutingEndpointGroupRequestRequestTypeDef,
    DeleteCustomRoutingListenerRequestRequestTypeDef,
    DeleteEndpointGroupRequestRequestTypeDef,
    DeleteListenerRequestRequestTypeDef,
    DenyCustomRoutingTrafficRequestRequestTypeDef,
    DeprovisionByoipCidrRequestRequestTypeDef,
    DeprovisionByoipCidrResponseTypeDef,
    DescribeAcceleratorAttributesRequestRequestTypeDef,
    DescribeAcceleratorAttributesResponseTypeDef,
    DescribeAcceleratorRequestRequestTypeDef,
    DescribeAcceleratorResponseTypeDef,
    DescribeCrossAccountAttachmentRequestRequestTypeDef,
    DescribeCrossAccountAttachmentResponseTypeDef,
    DescribeCustomRoutingAcceleratorAttributesRequestRequestTypeDef,
    DescribeCustomRoutingAcceleratorAttributesResponseTypeDef,
    DescribeCustomRoutingAcceleratorRequestRequestTypeDef,
    DescribeCustomRoutingAcceleratorResponseTypeDef,
    DescribeCustomRoutingEndpointGroupRequestRequestTypeDef,
    DescribeCustomRoutingEndpointGroupResponseTypeDef,
    DescribeCustomRoutingListenerRequestRequestTypeDef,
    DescribeCustomRoutingListenerResponseTypeDef,
    DescribeEndpointGroupRequestRequestTypeDef,
    DescribeEndpointGroupResponseTypeDef,
    DescribeListenerRequestRequestTypeDef,
    DescribeListenerResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ListAcceleratorsRequestRequestTypeDef,
    ListAcceleratorsResponseTypeDef,
    ListByoipCidrsRequestRequestTypeDef,
    ListByoipCidrsResponseTypeDef,
    ListCrossAccountAttachmentsRequestRequestTypeDef,
    ListCrossAccountAttachmentsResponseTypeDef,
    ListCrossAccountResourceAccountsResponseTypeDef,
    ListCrossAccountResourcesRequestRequestTypeDef,
    ListCrossAccountResourcesResponseTypeDef,
    ListCustomRoutingAcceleratorsRequestRequestTypeDef,
    ListCustomRoutingAcceleratorsResponseTypeDef,
    ListCustomRoutingEndpointGroupsRequestRequestTypeDef,
    ListCustomRoutingEndpointGroupsResponseTypeDef,
    ListCustomRoutingListenersRequestRequestTypeDef,
    ListCustomRoutingListenersResponseTypeDef,
    ListCustomRoutingPortMappingsByDestinationRequestRequestTypeDef,
    ListCustomRoutingPortMappingsByDestinationResponseTypeDef,
    ListCustomRoutingPortMappingsRequestRequestTypeDef,
    ListCustomRoutingPortMappingsResponseTypeDef,
    ListEndpointGroupsRequestRequestTypeDef,
    ListEndpointGroupsResponseTypeDef,
    ListListenersRequestRequestTypeDef,
    ListListenersResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ProvisionByoipCidrRequestRequestTypeDef,
    ProvisionByoipCidrResponseTypeDef,
    RemoveCustomRoutingEndpointsRequestRequestTypeDef,
    RemoveEndpointsRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAcceleratorAttributesRequestRequestTypeDef,
    UpdateAcceleratorAttributesResponseTypeDef,
    UpdateAcceleratorRequestRequestTypeDef,
    UpdateAcceleratorResponseTypeDef,
    UpdateCrossAccountAttachmentRequestRequestTypeDef,
    UpdateCrossAccountAttachmentResponseTypeDef,
    UpdateCustomRoutingAcceleratorAttributesRequestRequestTypeDef,
    UpdateCustomRoutingAcceleratorAttributesResponseTypeDef,
    UpdateCustomRoutingAcceleratorRequestRequestTypeDef,
    UpdateCustomRoutingAcceleratorResponseTypeDef,
    UpdateCustomRoutingListenerRequestRequestTypeDef,
    UpdateCustomRoutingListenerResponseTypeDef,
    UpdateEndpointGroupRequestRequestTypeDef,
    UpdateEndpointGroupResponseTypeDef,
    UpdateListenerRequestRequestTypeDef,
    UpdateListenerResponseTypeDef,
    WithdrawByoipCidrRequestRequestTypeDef,
    WithdrawByoipCidrResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("GlobalAcceleratorClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AcceleratorNotDisabledException: Type[BotocoreClientError]
    AcceleratorNotFoundException: Type[BotocoreClientError]
    AccessDeniedException: Type[BotocoreClientError]
    AssociatedEndpointGroupFoundException: Type[BotocoreClientError]
    AssociatedListenerFoundException: Type[BotocoreClientError]
    AttachmentNotFoundException: Type[BotocoreClientError]
    ByoipCidrNotFoundException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    EndpointAlreadyExistsException: Type[BotocoreClientError]
    EndpointGroupAlreadyExistsException: Type[BotocoreClientError]
    EndpointGroupNotFoundException: Type[BotocoreClientError]
    EndpointNotFoundException: Type[BotocoreClientError]
    IncorrectCidrStateException: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidPortRangeException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ListenerNotFoundException: Type[BotocoreClientError]
    TransactionInProgressException: Type[BotocoreClientError]


class GlobalAcceleratorClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GlobalAcceleratorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#close)
        """

    def add_custom_routing_endpoints(
        self, **kwargs: Unpack[AddCustomRoutingEndpointsRequestRequestTypeDef]
    ) -> AddCustomRoutingEndpointsResponseTypeDef:
        """
        Associate a virtual private cloud (VPC) subnet endpoint with your custom
        routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/add_custom_routing_endpoints.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#add_custom_routing_endpoints)
        """

    def add_endpoints(
        self, **kwargs: Unpack[AddEndpointsRequestRequestTypeDef]
    ) -> AddEndpointsResponseTypeDef:
        """
        Add endpoints to an endpoint group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/add_endpoints.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#add_endpoints)
        """

    def advertise_byoip_cidr(
        self, **kwargs: Unpack[AdvertiseByoipCidrRequestRequestTypeDef]
    ) -> AdvertiseByoipCidrResponseTypeDef:
        """
        Advertises an IPv4 address range that is provisioned for use with your Amazon
        Web Services resources through bring your own IP addresses (BYOIP).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/advertise_byoip_cidr.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#advertise_byoip_cidr)
        """

    def allow_custom_routing_traffic(
        self, **kwargs: Unpack[AllowCustomRoutingTrafficRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specify the Amazon EC2 instance (destination) IP addresses and ports for a VPC
        subnet endpoint that can receive traffic for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/allow_custom_routing_traffic.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#allow_custom_routing_traffic)
        """

    def create_accelerator(
        self, **kwargs: Unpack[CreateAcceleratorRequestRequestTypeDef]
    ) -> CreateAcceleratorResponseTypeDef:
        """
        Create an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/create_accelerator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#create_accelerator)
        """

    def create_cross_account_attachment(
        self, **kwargs: Unpack[CreateCrossAccountAttachmentRequestRequestTypeDef]
    ) -> CreateCrossAccountAttachmentResponseTypeDef:
        """
        Create a cross-account attachment in Global Accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/create_cross_account_attachment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#create_cross_account_attachment)
        """

    def create_custom_routing_accelerator(
        self, **kwargs: Unpack[CreateCustomRoutingAcceleratorRequestRequestTypeDef]
    ) -> CreateCustomRoutingAcceleratorResponseTypeDef:
        """
        Create a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/create_custom_routing_accelerator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#create_custom_routing_accelerator)
        """

    def create_custom_routing_endpoint_group(
        self, **kwargs: Unpack[CreateCustomRoutingEndpointGroupRequestRequestTypeDef]
    ) -> CreateCustomRoutingEndpointGroupResponseTypeDef:
        """
        Create an endpoint group for the specified listener for a custom routing
        accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/create_custom_routing_endpoint_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#create_custom_routing_endpoint_group)
        """

    def create_custom_routing_listener(
        self, **kwargs: Unpack[CreateCustomRoutingListenerRequestRequestTypeDef]
    ) -> CreateCustomRoutingListenerResponseTypeDef:
        """
        Create a listener to process inbound connections from clients to a custom
        routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/create_custom_routing_listener.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#create_custom_routing_listener)
        """

    def create_endpoint_group(
        self, **kwargs: Unpack[CreateEndpointGroupRequestRequestTypeDef]
    ) -> CreateEndpointGroupResponseTypeDef:
        """
        Create an endpoint group for the specified listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/create_endpoint_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#create_endpoint_group)
        """

    def create_listener(
        self, **kwargs: Unpack[CreateListenerRequestRequestTypeDef]
    ) -> CreateListenerResponseTypeDef:
        """
        Create a listener to process inbound connections from clients to an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/create_listener.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#create_listener)
        """

    def delete_accelerator(
        self, **kwargs: Unpack[DeleteAcceleratorRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/delete_accelerator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#delete_accelerator)
        """

    def delete_cross_account_attachment(
        self, **kwargs: Unpack[DeleteCrossAccountAttachmentRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a cross-account attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/delete_cross_account_attachment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#delete_cross_account_attachment)
        """

    def delete_custom_routing_accelerator(
        self, **kwargs: Unpack[DeleteCustomRoutingAcceleratorRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/delete_custom_routing_accelerator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#delete_custom_routing_accelerator)
        """

    def delete_custom_routing_endpoint_group(
        self, **kwargs: Unpack[DeleteCustomRoutingEndpointGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete an endpoint group from a listener for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/delete_custom_routing_endpoint_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#delete_custom_routing_endpoint_group)
        """

    def delete_custom_routing_listener(
        self, **kwargs: Unpack[DeleteCustomRoutingListenerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a listener for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/delete_custom_routing_listener.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#delete_custom_routing_listener)
        """

    def delete_endpoint_group(
        self, **kwargs: Unpack[DeleteEndpointGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete an endpoint group from a listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/delete_endpoint_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#delete_endpoint_group)
        """

    def delete_listener(
        self, **kwargs: Unpack[DeleteListenerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a listener from an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/delete_listener.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#delete_listener)
        """

    def deny_custom_routing_traffic(
        self, **kwargs: Unpack[DenyCustomRoutingTrafficRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specify the Amazon EC2 instance (destination) IP addresses and ports for a VPC
        subnet endpoint that cannot receive traffic for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/deny_custom_routing_traffic.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#deny_custom_routing_traffic)
        """

    def deprovision_byoip_cidr(
        self, **kwargs: Unpack[DeprovisionByoipCidrRequestRequestTypeDef]
    ) -> DeprovisionByoipCidrResponseTypeDef:
        """
        Releases the specified address range that you provisioned to use with your
        Amazon Web Services resources through bring your own IP addresses (BYOIP) and
        deletes the corresponding address pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/deprovision_byoip_cidr.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#deprovision_byoip_cidr)
        """

    def describe_accelerator(
        self, **kwargs: Unpack[DescribeAcceleratorRequestRequestTypeDef]
    ) -> DescribeAcceleratorResponseTypeDef:
        """
        Describe an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_accelerator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#describe_accelerator)
        """

    def describe_accelerator_attributes(
        self, **kwargs: Unpack[DescribeAcceleratorAttributesRequestRequestTypeDef]
    ) -> DescribeAcceleratorAttributesResponseTypeDef:
        """
        Describe the attributes of an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_accelerator_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#describe_accelerator_attributes)
        """

    def describe_cross_account_attachment(
        self, **kwargs: Unpack[DescribeCrossAccountAttachmentRequestRequestTypeDef]
    ) -> DescribeCrossAccountAttachmentResponseTypeDef:
        """
        Gets configuration information about a cross-account attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_cross_account_attachment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#describe_cross_account_attachment)
        """

    def describe_custom_routing_accelerator(
        self, **kwargs: Unpack[DescribeCustomRoutingAcceleratorRequestRequestTypeDef]
    ) -> DescribeCustomRoutingAcceleratorResponseTypeDef:
        """
        Describe a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_custom_routing_accelerator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#describe_custom_routing_accelerator)
        """

    def describe_custom_routing_accelerator_attributes(
        self, **kwargs: Unpack[DescribeCustomRoutingAcceleratorAttributesRequestRequestTypeDef]
    ) -> DescribeCustomRoutingAcceleratorAttributesResponseTypeDef:
        """
        Describe the attributes of a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_custom_routing_accelerator_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#describe_custom_routing_accelerator_attributes)
        """

    def describe_custom_routing_endpoint_group(
        self, **kwargs: Unpack[DescribeCustomRoutingEndpointGroupRequestRequestTypeDef]
    ) -> DescribeCustomRoutingEndpointGroupResponseTypeDef:
        """
        Describe an endpoint group for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_custom_routing_endpoint_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#describe_custom_routing_endpoint_group)
        """

    def describe_custom_routing_listener(
        self, **kwargs: Unpack[DescribeCustomRoutingListenerRequestRequestTypeDef]
    ) -> DescribeCustomRoutingListenerResponseTypeDef:
        """
        The description of a listener for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_custom_routing_listener.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#describe_custom_routing_listener)
        """

    def describe_endpoint_group(
        self, **kwargs: Unpack[DescribeEndpointGroupRequestRequestTypeDef]
    ) -> DescribeEndpointGroupResponseTypeDef:
        """
        Describe an endpoint group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_endpoint_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#describe_endpoint_group)
        """

    def describe_listener(
        self, **kwargs: Unpack[DescribeListenerRequestRequestTypeDef]
    ) -> DescribeListenerResponseTypeDef:
        """
        Describe a listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_listener.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#describe_listener)
        """

    def list_accelerators(
        self, **kwargs: Unpack[ListAcceleratorsRequestRequestTypeDef]
    ) -> ListAcceleratorsResponseTypeDef:
        """
        List the accelerators for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_accelerators.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#list_accelerators)
        """

    def list_byoip_cidrs(
        self, **kwargs: Unpack[ListByoipCidrsRequestRequestTypeDef]
    ) -> ListByoipCidrsResponseTypeDef:
        """
        Lists the IP address ranges that were specified in calls to <a
        href="https://docs.aws.amazon.com/global-accelerator/latest/api/ProvisionByoipCidr.html">ProvisionByoipCidr</a>,
        including the current state and a history of state changes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_byoip_cidrs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#list_byoip_cidrs)
        """

    def list_cross_account_attachments(
        self, **kwargs: Unpack[ListCrossAccountAttachmentsRequestRequestTypeDef]
    ) -> ListCrossAccountAttachmentsResponseTypeDef:
        """
        List the cross-account attachments that have been created in Global Accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_cross_account_attachments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#list_cross_account_attachments)
        """

    def list_cross_account_resource_accounts(
        self,
    ) -> ListCrossAccountResourceAccountsResponseTypeDef:
        """
        List the accounts that have cross-account resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_cross_account_resource_accounts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#list_cross_account_resource_accounts)
        """

    def list_cross_account_resources(
        self, **kwargs: Unpack[ListCrossAccountResourcesRequestRequestTypeDef]
    ) -> ListCrossAccountResourcesResponseTypeDef:
        """
        List the cross-account resources available to work with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_cross_account_resources.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#list_cross_account_resources)
        """

    def list_custom_routing_accelerators(
        self, **kwargs: Unpack[ListCustomRoutingAcceleratorsRequestRequestTypeDef]
    ) -> ListCustomRoutingAcceleratorsResponseTypeDef:
        """
        List the custom routing accelerators for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_custom_routing_accelerators.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#list_custom_routing_accelerators)
        """

    def list_custom_routing_endpoint_groups(
        self, **kwargs: Unpack[ListCustomRoutingEndpointGroupsRequestRequestTypeDef]
    ) -> ListCustomRoutingEndpointGroupsResponseTypeDef:
        """
        List the endpoint groups that are associated with a listener for a custom
        routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_custom_routing_endpoint_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#list_custom_routing_endpoint_groups)
        """

    def list_custom_routing_listeners(
        self, **kwargs: Unpack[ListCustomRoutingListenersRequestRequestTypeDef]
    ) -> ListCustomRoutingListenersResponseTypeDef:
        """
        List the listeners for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_custom_routing_listeners.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#list_custom_routing_listeners)
        """

    def list_custom_routing_port_mappings(
        self, **kwargs: Unpack[ListCustomRoutingPortMappingsRequestRequestTypeDef]
    ) -> ListCustomRoutingPortMappingsResponseTypeDef:
        """
        Provides a complete mapping from the public accelerator IP address and port to
        destination EC2 instance IP addresses and ports in the virtual public cloud
        (VPC) subnet endpoint for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_custom_routing_port_mappings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#list_custom_routing_port_mappings)
        """

    def list_custom_routing_port_mappings_by_destination(
        self, **kwargs: Unpack[ListCustomRoutingPortMappingsByDestinationRequestRequestTypeDef]
    ) -> ListCustomRoutingPortMappingsByDestinationResponseTypeDef:
        """
        List the port mappings for a specific EC2 instance (destination) in a VPC
        subnet endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_custom_routing_port_mappings_by_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#list_custom_routing_port_mappings_by_destination)
        """

    def list_endpoint_groups(
        self, **kwargs: Unpack[ListEndpointGroupsRequestRequestTypeDef]
    ) -> ListEndpointGroupsResponseTypeDef:
        """
        List the endpoint groups that are associated with a listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_endpoint_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#list_endpoint_groups)
        """

    def list_listeners(
        self, **kwargs: Unpack[ListListenersRequestRequestTypeDef]
    ) -> ListListenersResponseTypeDef:
        """
        List the listeners for an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_listeners.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#list_listeners)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List all tags for an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#list_tags_for_resource)
        """

    def provision_byoip_cidr(
        self, **kwargs: Unpack[ProvisionByoipCidrRequestRequestTypeDef]
    ) -> ProvisionByoipCidrResponseTypeDef:
        """
        Provisions an IP address range to use with your Amazon Web Services resources
        through bring your own IP addresses (BYOIP) and creates a corresponding address
        pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/provision_byoip_cidr.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#provision_byoip_cidr)
        """

    def remove_custom_routing_endpoints(
        self, **kwargs: Unpack[RemoveCustomRoutingEndpointsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove endpoints from a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/remove_custom_routing_endpoints.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#remove_custom_routing_endpoints)
        """

    def remove_endpoints(
        self, **kwargs: Unpack[RemoveEndpointsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove endpoints from an endpoint group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/remove_endpoints.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#remove_endpoints)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Add tags to an accelerator resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Remove tags from a Global Accelerator resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#untag_resource)
        """

    def update_accelerator(
        self, **kwargs: Unpack[UpdateAcceleratorRequestRequestTypeDef]
    ) -> UpdateAcceleratorResponseTypeDef:
        """
        Update an accelerator to make changes, such as the following:.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/update_accelerator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#update_accelerator)
        """

    def update_accelerator_attributes(
        self, **kwargs: Unpack[UpdateAcceleratorAttributesRequestRequestTypeDef]
    ) -> UpdateAcceleratorAttributesResponseTypeDef:
        """
        Update the attributes for an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/update_accelerator_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#update_accelerator_attributes)
        """

    def update_cross_account_attachment(
        self, **kwargs: Unpack[UpdateCrossAccountAttachmentRequestRequestTypeDef]
    ) -> UpdateCrossAccountAttachmentResponseTypeDef:
        """
        Update a cross-account attachment to add or remove principals or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/update_cross_account_attachment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#update_cross_account_attachment)
        """

    def update_custom_routing_accelerator(
        self, **kwargs: Unpack[UpdateCustomRoutingAcceleratorRequestRequestTypeDef]
    ) -> UpdateCustomRoutingAcceleratorResponseTypeDef:
        """
        Update a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/update_custom_routing_accelerator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#update_custom_routing_accelerator)
        """

    def update_custom_routing_accelerator_attributes(
        self, **kwargs: Unpack[UpdateCustomRoutingAcceleratorAttributesRequestRequestTypeDef]
    ) -> UpdateCustomRoutingAcceleratorAttributesResponseTypeDef:
        """
        Update the attributes for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/update_custom_routing_accelerator_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#update_custom_routing_accelerator_attributes)
        """

    def update_custom_routing_listener(
        self, **kwargs: Unpack[UpdateCustomRoutingListenerRequestRequestTypeDef]
    ) -> UpdateCustomRoutingListenerResponseTypeDef:
        """
        Update a listener for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/update_custom_routing_listener.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#update_custom_routing_listener)
        """

    def update_endpoint_group(
        self, **kwargs: Unpack[UpdateEndpointGroupRequestRequestTypeDef]
    ) -> UpdateEndpointGroupResponseTypeDef:
        """
        Update an endpoint group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/update_endpoint_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#update_endpoint_group)
        """

    def update_listener(
        self, **kwargs: Unpack[UpdateListenerRequestRequestTypeDef]
    ) -> UpdateListenerResponseTypeDef:
        """
        Update a listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/update_listener.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#update_listener)
        """

    def withdraw_byoip_cidr(
        self, **kwargs: Unpack[WithdrawByoipCidrRequestRequestTypeDef]
    ) -> WithdrawByoipCidrResponseTypeDef:
        """
        Stops advertising an address range that is provisioned as an address pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/withdraw_byoip_cidr.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#withdraw_byoip_cidr)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_accelerators"]
    ) -> ListAcceleratorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_byoip_cidrs"]) -> ListByoipCidrsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cross_account_attachments"]
    ) -> ListCrossAccountAttachmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cross_account_resources"]
    ) -> ListCrossAccountResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_routing_accelerators"]
    ) -> ListCustomRoutingAcceleratorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_routing_endpoint_groups"]
    ) -> ListCustomRoutingEndpointGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_routing_listeners"]
    ) -> ListCustomRoutingListenersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_routing_port_mappings_by_destination"]
    ) -> ListCustomRoutingPortMappingsByDestinationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_routing_port_mappings"]
    ) -> ListCustomRoutingPortMappingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_endpoint_groups"]
    ) -> ListEndpointGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_listeners"]) -> ListListenersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/client/#get_paginator)
        """
