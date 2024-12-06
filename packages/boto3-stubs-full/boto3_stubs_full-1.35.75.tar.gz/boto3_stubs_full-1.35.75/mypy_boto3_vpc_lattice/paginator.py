"""
Type annotations for vpc-lattice service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_vpc_lattice.client import VPCLatticeClient
    from mypy_boto3_vpc_lattice.paginator import (
        ListAccessLogSubscriptionsPaginator,
        ListListenersPaginator,
        ListResourceConfigurationsPaginator,
        ListResourceEndpointAssociationsPaginator,
        ListResourceGatewaysPaginator,
        ListRulesPaginator,
        ListServiceNetworkResourceAssociationsPaginator,
        ListServiceNetworkServiceAssociationsPaginator,
        ListServiceNetworkVpcAssociationsPaginator,
        ListServiceNetworkVpcEndpointAssociationsPaginator,
        ListServiceNetworksPaginator,
        ListServicesPaginator,
        ListTargetGroupsPaginator,
        ListTargetsPaginator,
    )

    session = Session()
    client: VPCLatticeClient = session.client("vpc-lattice")

    list_access_log_subscriptions_paginator: ListAccessLogSubscriptionsPaginator = client.get_paginator("list_access_log_subscriptions")
    list_listeners_paginator: ListListenersPaginator = client.get_paginator("list_listeners")
    list_resource_configurations_paginator: ListResourceConfigurationsPaginator = client.get_paginator("list_resource_configurations")
    list_resource_endpoint_associations_paginator: ListResourceEndpointAssociationsPaginator = client.get_paginator("list_resource_endpoint_associations")
    list_resource_gateways_paginator: ListResourceGatewaysPaginator = client.get_paginator("list_resource_gateways")
    list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    list_service_network_resource_associations_paginator: ListServiceNetworkResourceAssociationsPaginator = client.get_paginator("list_service_network_resource_associations")
    list_service_network_service_associations_paginator: ListServiceNetworkServiceAssociationsPaginator = client.get_paginator("list_service_network_service_associations")
    list_service_network_vpc_associations_paginator: ListServiceNetworkVpcAssociationsPaginator = client.get_paginator("list_service_network_vpc_associations")
    list_service_network_vpc_endpoint_associations_paginator: ListServiceNetworkVpcEndpointAssociationsPaginator = client.get_paginator("list_service_network_vpc_endpoint_associations")
    list_service_networks_paginator: ListServiceNetworksPaginator = client.get_paginator("list_service_networks")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    list_target_groups_paginator: ListTargetGroupsPaginator = client.get_paginator("list_target_groups")
    list_targets_paginator: ListTargetsPaginator = client.get_paginator("list_targets")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAccessLogSubscriptionsRequestListAccessLogSubscriptionsPaginateTypeDef,
    ListAccessLogSubscriptionsResponseTypeDef,
    ListListenersRequestListListenersPaginateTypeDef,
    ListListenersResponseTypeDef,
    ListResourceConfigurationsRequestListResourceConfigurationsPaginateTypeDef,
    ListResourceConfigurationsResponseTypeDef,
    ListResourceEndpointAssociationsRequestListResourceEndpointAssociationsPaginateTypeDef,
    ListResourceEndpointAssociationsResponseTypeDef,
    ListResourceGatewaysRequestListResourceGatewaysPaginateTypeDef,
    ListResourceGatewaysResponseTypeDef,
    ListRulesRequestListRulesPaginateTypeDef,
    ListRulesResponseTypeDef,
    ListServiceNetworkResourceAssociationsRequestListServiceNetworkResourceAssociationsPaginateTypeDef,
    ListServiceNetworkResourceAssociationsResponseTypeDef,
    ListServiceNetworkServiceAssociationsRequestListServiceNetworkServiceAssociationsPaginateTypeDef,
    ListServiceNetworkServiceAssociationsResponseTypeDef,
    ListServiceNetworksRequestListServiceNetworksPaginateTypeDef,
    ListServiceNetworksResponseTypeDef,
    ListServiceNetworkVpcAssociationsRequestListServiceNetworkVpcAssociationsPaginateTypeDef,
    ListServiceNetworkVpcAssociationsResponseTypeDef,
    ListServiceNetworkVpcEndpointAssociationsRequestListServiceNetworkVpcEndpointAssociationsPaginateTypeDef,
    ListServiceNetworkVpcEndpointAssociationsResponseTypeDef,
    ListServicesRequestListServicesPaginateTypeDef,
    ListServicesResponseTypeDef,
    ListTargetGroupsRequestListTargetGroupsPaginateTypeDef,
    ListTargetGroupsResponseTypeDef,
    ListTargetsRequestListTargetsPaginateTypeDef,
    ListTargetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAccessLogSubscriptionsPaginator",
    "ListListenersPaginator",
    "ListResourceConfigurationsPaginator",
    "ListResourceEndpointAssociationsPaginator",
    "ListResourceGatewaysPaginator",
    "ListRulesPaginator",
    "ListServiceNetworkResourceAssociationsPaginator",
    "ListServiceNetworkServiceAssociationsPaginator",
    "ListServiceNetworkVpcAssociationsPaginator",
    "ListServiceNetworkVpcEndpointAssociationsPaginator",
    "ListServiceNetworksPaginator",
    "ListServicesPaginator",
    "ListTargetGroupsPaginator",
    "ListTargetsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAccessLogSubscriptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListAccessLogSubscriptions.html#VPCLattice.Paginator.ListAccessLogSubscriptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listaccesslogsubscriptionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListAccessLogSubscriptionsRequestListAccessLogSubscriptionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListAccessLogSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListAccessLogSubscriptions.html#VPCLattice.Paginator.ListAccessLogSubscriptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listaccesslogsubscriptionspaginator)
        """


class ListListenersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListListeners.html#VPCLattice.Paginator.ListListeners)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listlistenerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListListenersRequestListListenersPaginateTypeDef]
    ) -> _PageIterator[ListListenersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListListeners.html#VPCLattice.Paginator.ListListeners.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listlistenerspaginator)
        """


class ListResourceConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListResourceConfigurations.html#VPCLattice.Paginator.ListResourceConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listresourceconfigurationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListResourceConfigurationsRequestListResourceConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListResourceConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListResourceConfigurations.html#VPCLattice.Paginator.ListResourceConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listresourceconfigurationspaginator)
        """


class ListResourceEndpointAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListResourceEndpointAssociations.html#VPCLattice.Paginator.ListResourceEndpointAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listresourceendpointassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListResourceEndpointAssociationsRequestListResourceEndpointAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListResourceEndpointAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListResourceEndpointAssociations.html#VPCLattice.Paginator.ListResourceEndpointAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listresourceendpointassociationspaginator)
        """


class ListResourceGatewaysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListResourceGateways.html#VPCLattice.Paginator.ListResourceGateways)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listresourcegatewayspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResourceGatewaysRequestListResourceGatewaysPaginateTypeDef]
    ) -> _PageIterator[ListResourceGatewaysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListResourceGateways.html#VPCLattice.Paginator.ListResourceGateways.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listresourcegatewayspaginator)
        """


class ListRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListRules.html#VPCLattice.Paginator.ListRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listrulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRulesRequestListRulesPaginateTypeDef]
    ) -> _PageIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListRules.html#VPCLattice.Paginator.ListRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listrulespaginator)
        """


class ListServiceNetworkResourceAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkResourceAssociations.html#VPCLattice.Paginator.ListServiceNetworkResourceAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicenetworkresourceassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListServiceNetworkResourceAssociationsRequestListServiceNetworkResourceAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListServiceNetworkResourceAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkResourceAssociations.html#VPCLattice.Paginator.ListServiceNetworkResourceAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicenetworkresourceassociationspaginator)
        """


class ListServiceNetworkServiceAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkServiceAssociations.html#VPCLattice.Paginator.ListServiceNetworkServiceAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicenetworkserviceassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListServiceNetworkServiceAssociationsRequestListServiceNetworkServiceAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListServiceNetworkServiceAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkServiceAssociations.html#VPCLattice.Paginator.ListServiceNetworkServiceAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicenetworkserviceassociationspaginator)
        """


class ListServiceNetworkVpcAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkVpcAssociations.html#VPCLattice.Paginator.ListServiceNetworkVpcAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicenetworkvpcassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListServiceNetworkVpcAssociationsRequestListServiceNetworkVpcAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListServiceNetworkVpcAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkVpcAssociations.html#VPCLattice.Paginator.ListServiceNetworkVpcAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicenetworkvpcassociationspaginator)
        """


class ListServiceNetworkVpcEndpointAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkVpcEndpointAssociations.html#VPCLattice.Paginator.ListServiceNetworkVpcEndpointAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicenetworkvpcendpointassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListServiceNetworkVpcEndpointAssociationsRequestListServiceNetworkVpcEndpointAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListServiceNetworkVpcEndpointAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkVpcEndpointAssociations.html#VPCLattice.Paginator.ListServiceNetworkVpcEndpointAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicenetworkvpcendpointassociationspaginator)
        """


class ListServiceNetworksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworks.html#VPCLattice.Paginator.ListServiceNetworks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicenetworkspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListServiceNetworksRequestListServiceNetworksPaginateTypeDef]
    ) -> _PageIterator[ListServiceNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworks.html#VPCLattice.Paginator.ListServiceNetworks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicenetworkspaginator)
        """


class ListServicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServices.html#VPCLattice.Paginator.ListServices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListServicesRequestListServicesPaginateTypeDef]
    ) -> _PageIterator[ListServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServices.html#VPCLattice.Paginator.ListServices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicespaginator)
        """


class ListTargetGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListTargetGroups.html#VPCLattice.Paginator.ListTargetGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listtargetgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTargetGroupsRequestListTargetGroupsPaginateTypeDef]
    ) -> _PageIterator[ListTargetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListTargetGroups.html#VPCLattice.Paginator.ListTargetGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listtargetgroupspaginator)
        """


class ListTargetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListTargets.html#VPCLattice.Paginator.ListTargets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listtargetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTargetsRequestListTargetsPaginateTypeDef]
    ) -> _PageIterator[ListTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListTargets.html#VPCLattice.Paginator.ListTargets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listtargetspaginator)
        """
