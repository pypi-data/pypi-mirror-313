"""
Type annotations for networkmanager service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_networkmanager.client import NetworkManagerClient
    from mypy_boto3_networkmanager.paginator import (
        DescribeGlobalNetworksPaginator,
        GetConnectPeerAssociationsPaginator,
        GetConnectionsPaginator,
        GetCoreNetworkChangeEventsPaginator,
        GetCoreNetworkChangeSetPaginator,
        GetCustomerGatewayAssociationsPaginator,
        GetDevicesPaginator,
        GetLinkAssociationsPaginator,
        GetLinksPaginator,
        GetNetworkResourceCountsPaginator,
        GetNetworkResourceRelationshipsPaginator,
        GetNetworkResourcesPaginator,
        GetNetworkTelemetryPaginator,
        GetSitesPaginator,
        GetTransitGatewayConnectPeerAssociationsPaginator,
        GetTransitGatewayRegistrationsPaginator,
        ListAttachmentsPaginator,
        ListConnectPeersPaginator,
        ListCoreNetworkPolicyVersionsPaginator,
        ListCoreNetworksPaginator,
        ListPeeringsPaginator,
    )

    session = Session()
    client: NetworkManagerClient = session.client("networkmanager")

    describe_global_networks_paginator: DescribeGlobalNetworksPaginator = client.get_paginator("describe_global_networks")
    get_connect_peer_associations_paginator: GetConnectPeerAssociationsPaginator = client.get_paginator("get_connect_peer_associations")
    get_connections_paginator: GetConnectionsPaginator = client.get_paginator("get_connections")
    get_core_network_change_events_paginator: GetCoreNetworkChangeEventsPaginator = client.get_paginator("get_core_network_change_events")
    get_core_network_change_set_paginator: GetCoreNetworkChangeSetPaginator = client.get_paginator("get_core_network_change_set")
    get_customer_gateway_associations_paginator: GetCustomerGatewayAssociationsPaginator = client.get_paginator("get_customer_gateway_associations")
    get_devices_paginator: GetDevicesPaginator = client.get_paginator("get_devices")
    get_link_associations_paginator: GetLinkAssociationsPaginator = client.get_paginator("get_link_associations")
    get_links_paginator: GetLinksPaginator = client.get_paginator("get_links")
    get_network_resource_counts_paginator: GetNetworkResourceCountsPaginator = client.get_paginator("get_network_resource_counts")
    get_network_resource_relationships_paginator: GetNetworkResourceRelationshipsPaginator = client.get_paginator("get_network_resource_relationships")
    get_network_resources_paginator: GetNetworkResourcesPaginator = client.get_paginator("get_network_resources")
    get_network_telemetry_paginator: GetNetworkTelemetryPaginator = client.get_paginator("get_network_telemetry")
    get_sites_paginator: GetSitesPaginator = client.get_paginator("get_sites")
    get_transit_gateway_connect_peer_associations_paginator: GetTransitGatewayConnectPeerAssociationsPaginator = client.get_paginator("get_transit_gateway_connect_peer_associations")
    get_transit_gateway_registrations_paginator: GetTransitGatewayRegistrationsPaginator = client.get_paginator("get_transit_gateway_registrations")
    list_attachments_paginator: ListAttachmentsPaginator = client.get_paginator("list_attachments")
    list_connect_peers_paginator: ListConnectPeersPaginator = client.get_paginator("list_connect_peers")
    list_core_network_policy_versions_paginator: ListCoreNetworkPolicyVersionsPaginator = client.get_paginator("list_core_network_policy_versions")
    list_core_networks_paginator: ListCoreNetworksPaginator = client.get_paginator("list_core_networks")
    list_peerings_paginator: ListPeeringsPaginator = client.get_paginator("list_peerings")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeGlobalNetworksRequestDescribeGlobalNetworksPaginateTypeDef,
    DescribeGlobalNetworksResponseTypeDef,
    GetConnectionsRequestGetConnectionsPaginateTypeDef,
    GetConnectionsResponseTypeDef,
    GetConnectPeerAssociationsRequestGetConnectPeerAssociationsPaginateTypeDef,
    GetConnectPeerAssociationsResponseTypeDef,
    GetCoreNetworkChangeEventsRequestGetCoreNetworkChangeEventsPaginateTypeDef,
    GetCoreNetworkChangeEventsResponseTypeDef,
    GetCoreNetworkChangeSetRequestGetCoreNetworkChangeSetPaginateTypeDef,
    GetCoreNetworkChangeSetResponseTypeDef,
    GetCustomerGatewayAssociationsRequestGetCustomerGatewayAssociationsPaginateTypeDef,
    GetCustomerGatewayAssociationsResponseTypeDef,
    GetDevicesRequestGetDevicesPaginateTypeDef,
    GetDevicesResponseTypeDef,
    GetLinkAssociationsRequestGetLinkAssociationsPaginateTypeDef,
    GetLinkAssociationsResponseTypeDef,
    GetLinksRequestGetLinksPaginateTypeDef,
    GetLinksResponseTypeDef,
    GetNetworkResourceCountsRequestGetNetworkResourceCountsPaginateTypeDef,
    GetNetworkResourceCountsResponseTypeDef,
    GetNetworkResourceRelationshipsRequestGetNetworkResourceRelationshipsPaginateTypeDef,
    GetNetworkResourceRelationshipsResponseTypeDef,
    GetNetworkResourcesRequestGetNetworkResourcesPaginateTypeDef,
    GetNetworkResourcesResponseTypeDef,
    GetNetworkTelemetryRequestGetNetworkTelemetryPaginateTypeDef,
    GetNetworkTelemetryResponseTypeDef,
    GetSitesRequestGetSitesPaginateTypeDef,
    GetSitesResponseTypeDef,
    GetTransitGatewayConnectPeerAssociationsRequestGetTransitGatewayConnectPeerAssociationsPaginateTypeDef,
    GetTransitGatewayConnectPeerAssociationsResponseTypeDef,
    GetTransitGatewayRegistrationsRequestGetTransitGatewayRegistrationsPaginateTypeDef,
    GetTransitGatewayRegistrationsResponseTypeDef,
    ListAttachmentsRequestListAttachmentsPaginateTypeDef,
    ListAttachmentsResponseTypeDef,
    ListConnectPeersRequestListConnectPeersPaginateTypeDef,
    ListConnectPeersResponseTypeDef,
    ListCoreNetworkPolicyVersionsRequestListCoreNetworkPolicyVersionsPaginateTypeDef,
    ListCoreNetworkPolicyVersionsResponseTypeDef,
    ListCoreNetworksRequestListCoreNetworksPaginateTypeDef,
    ListCoreNetworksResponseTypeDef,
    ListPeeringsRequestListPeeringsPaginateTypeDef,
    ListPeeringsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeGlobalNetworksPaginator",
    "GetConnectPeerAssociationsPaginator",
    "GetConnectionsPaginator",
    "GetCoreNetworkChangeEventsPaginator",
    "GetCoreNetworkChangeSetPaginator",
    "GetCustomerGatewayAssociationsPaginator",
    "GetDevicesPaginator",
    "GetLinkAssociationsPaginator",
    "GetLinksPaginator",
    "GetNetworkResourceCountsPaginator",
    "GetNetworkResourceRelationshipsPaginator",
    "GetNetworkResourcesPaginator",
    "GetNetworkTelemetryPaginator",
    "GetSitesPaginator",
    "GetTransitGatewayConnectPeerAssociationsPaginator",
    "GetTransitGatewayRegistrationsPaginator",
    "ListAttachmentsPaginator",
    "ListConnectPeersPaginator",
    "ListCoreNetworkPolicyVersionsPaginator",
    "ListCoreNetworksPaginator",
    "ListPeeringsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeGlobalNetworksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/DescribeGlobalNetworks.html#NetworkManager.Paginator.DescribeGlobalNetworks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#describeglobalnetworkspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeGlobalNetworksRequestDescribeGlobalNetworksPaginateTypeDef]
    ) -> _PageIterator[DescribeGlobalNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/DescribeGlobalNetworks.html#NetworkManager.Paginator.DescribeGlobalNetworks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#describeglobalnetworkspaginator)
        """


class GetConnectPeerAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetConnectPeerAssociations.html#NetworkManager.Paginator.GetConnectPeerAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getconnectpeerassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetConnectPeerAssociationsRequestGetConnectPeerAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[GetConnectPeerAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetConnectPeerAssociations.html#NetworkManager.Paginator.GetConnectPeerAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getconnectpeerassociationspaginator)
        """


class GetConnectionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetConnections.html#NetworkManager.Paginator.GetConnections)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getconnectionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetConnectionsRequestGetConnectionsPaginateTypeDef]
    ) -> _PageIterator[GetConnectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetConnections.html#NetworkManager.Paginator.GetConnections.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getconnectionspaginator)
        """


class GetCoreNetworkChangeEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCoreNetworkChangeEvents.html#NetworkManager.Paginator.GetCoreNetworkChangeEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getcorenetworkchangeeventspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetCoreNetworkChangeEventsRequestGetCoreNetworkChangeEventsPaginateTypeDef
        ],
    ) -> _PageIterator[GetCoreNetworkChangeEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCoreNetworkChangeEvents.html#NetworkManager.Paginator.GetCoreNetworkChangeEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getcorenetworkchangeeventspaginator)
        """


class GetCoreNetworkChangeSetPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCoreNetworkChangeSet.html#NetworkManager.Paginator.GetCoreNetworkChangeSet)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getcorenetworkchangesetpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetCoreNetworkChangeSetRequestGetCoreNetworkChangeSetPaginateTypeDef]
    ) -> _PageIterator[GetCoreNetworkChangeSetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCoreNetworkChangeSet.html#NetworkManager.Paginator.GetCoreNetworkChangeSet.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getcorenetworkchangesetpaginator)
        """


class GetCustomerGatewayAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCustomerGatewayAssociations.html#NetworkManager.Paginator.GetCustomerGatewayAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getcustomergatewayassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetCustomerGatewayAssociationsRequestGetCustomerGatewayAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[GetCustomerGatewayAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCustomerGatewayAssociations.html#NetworkManager.Paginator.GetCustomerGatewayAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getcustomergatewayassociationspaginator)
        """


class GetDevicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetDevices.html#NetworkManager.Paginator.GetDevices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getdevicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetDevicesRequestGetDevicesPaginateTypeDef]
    ) -> _PageIterator[GetDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetDevices.html#NetworkManager.Paginator.GetDevices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getdevicespaginator)
        """


class GetLinkAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetLinkAssociations.html#NetworkManager.Paginator.GetLinkAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getlinkassociationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetLinkAssociationsRequestGetLinkAssociationsPaginateTypeDef]
    ) -> _PageIterator[GetLinkAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetLinkAssociations.html#NetworkManager.Paginator.GetLinkAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getlinkassociationspaginator)
        """


class GetLinksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetLinks.html#NetworkManager.Paginator.GetLinks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getlinkspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetLinksRequestGetLinksPaginateTypeDef]
    ) -> _PageIterator[GetLinksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetLinks.html#NetworkManager.Paginator.GetLinks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getlinkspaginator)
        """


class GetNetworkResourceCountsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResourceCounts.html#NetworkManager.Paginator.GetNetworkResourceCounts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getnetworkresourcecountspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[GetNetworkResourceCountsRequestGetNetworkResourceCountsPaginateTypeDef],
    ) -> _PageIterator[GetNetworkResourceCountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResourceCounts.html#NetworkManager.Paginator.GetNetworkResourceCounts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getnetworkresourcecountspaginator)
        """


class GetNetworkResourceRelationshipsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResourceRelationships.html#NetworkManager.Paginator.GetNetworkResourceRelationships)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getnetworkresourcerelationshipspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetNetworkResourceRelationshipsRequestGetNetworkResourceRelationshipsPaginateTypeDef
        ],
    ) -> _PageIterator[GetNetworkResourceRelationshipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResourceRelationships.html#NetworkManager.Paginator.GetNetworkResourceRelationships.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getnetworkresourcerelationshipspaginator)
        """


class GetNetworkResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResources.html#NetworkManager.Paginator.GetNetworkResources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getnetworkresourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetNetworkResourcesRequestGetNetworkResourcesPaginateTypeDef]
    ) -> _PageIterator[GetNetworkResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResources.html#NetworkManager.Paginator.GetNetworkResources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getnetworkresourcespaginator)
        """


class GetNetworkTelemetryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkTelemetry.html#NetworkManager.Paginator.GetNetworkTelemetry)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getnetworktelemetrypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetNetworkTelemetryRequestGetNetworkTelemetryPaginateTypeDef]
    ) -> _PageIterator[GetNetworkTelemetryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkTelemetry.html#NetworkManager.Paginator.GetNetworkTelemetry.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getnetworktelemetrypaginator)
        """


class GetSitesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetSites.html#NetworkManager.Paginator.GetSites)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getsitespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetSitesRequestGetSitesPaginateTypeDef]
    ) -> _PageIterator[GetSitesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetSites.html#NetworkManager.Paginator.GetSites.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#getsitespaginator)
        """


class GetTransitGatewayConnectPeerAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetTransitGatewayConnectPeerAssociations.html#NetworkManager.Paginator.GetTransitGatewayConnectPeerAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#gettransitgatewayconnectpeerassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetTransitGatewayConnectPeerAssociationsRequestGetTransitGatewayConnectPeerAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[GetTransitGatewayConnectPeerAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetTransitGatewayConnectPeerAssociations.html#NetworkManager.Paginator.GetTransitGatewayConnectPeerAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#gettransitgatewayconnectpeerassociationspaginator)
        """


class GetTransitGatewayRegistrationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetTransitGatewayRegistrations.html#NetworkManager.Paginator.GetTransitGatewayRegistrations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#gettransitgatewayregistrationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetTransitGatewayRegistrationsRequestGetTransitGatewayRegistrationsPaginateTypeDef
        ],
    ) -> _PageIterator[GetTransitGatewayRegistrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetTransitGatewayRegistrations.html#NetworkManager.Paginator.GetTransitGatewayRegistrations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#gettransitgatewayregistrationspaginator)
        """


class ListAttachmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListAttachments.html#NetworkManager.Paginator.ListAttachments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#listattachmentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAttachmentsRequestListAttachmentsPaginateTypeDef]
    ) -> _PageIterator[ListAttachmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListAttachments.html#NetworkManager.Paginator.ListAttachments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#listattachmentspaginator)
        """


class ListConnectPeersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListConnectPeers.html#NetworkManager.Paginator.ListConnectPeers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#listconnectpeerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListConnectPeersRequestListConnectPeersPaginateTypeDef]
    ) -> _PageIterator[ListConnectPeersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListConnectPeers.html#NetworkManager.Paginator.ListConnectPeers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#listconnectpeerspaginator)
        """


class ListCoreNetworkPolicyVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListCoreNetworkPolicyVersions.html#NetworkManager.Paginator.ListCoreNetworkPolicyVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#listcorenetworkpolicyversionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListCoreNetworkPolicyVersionsRequestListCoreNetworkPolicyVersionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListCoreNetworkPolicyVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListCoreNetworkPolicyVersions.html#NetworkManager.Paginator.ListCoreNetworkPolicyVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#listcorenetworkpolicyversionspaginator)
        """


class ListCoreNetworksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListCoreNetworks.html#NetworkManager.Paginator.ListCoreNetworks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#listcorenetworkspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCoreNetworksRequestListCoreNetworksPaginateTypeDef]
    ) -> _PageIterator[ListCoreNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListCoreNetworks.html#NetworkManager.Paginator.ListCoreNetworks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#listcorenetworkspaginator)
        """


class ListPeeringsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListPeerings.html#NetworkManager.Paginator.ListPeerings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#listpeeringspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPeeringsRequestListPeeringsPaginateTypeDef]
    ) -> _PageIterator[ListPeeringsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListPeerings.html#NetworkManager.Paginator.ListPeerings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators/#listpeeringspaginator)
        """
