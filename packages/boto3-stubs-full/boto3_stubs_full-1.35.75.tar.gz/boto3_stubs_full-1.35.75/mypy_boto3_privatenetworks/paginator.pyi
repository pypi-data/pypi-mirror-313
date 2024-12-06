"""
Type annotations for privatenetworks service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_privatenetworks.client import Private5GClient
    from mypy_boto3_privatenetworks.paginator import (
        ListDeviceIdentifiersPaginator,
        ListNetworkResourcesPaginator,
        ListNetworkSitesPaginator,
        ListNetworksPaginator,
        ListOrdersPaginator,
    )

    session = Session()
    client: Private5GClient = session.client("privatenetworks")

    list_device_identifiers_paginator: ListDeviceIdentifiersPaginator = client.get_paginator("list_device_identifiers")
    list_network_resources_paginator: ListNetworkResourcesPaginator = client.get_paginator("list_network_resources")
    list_network_sites_paginator: ListNetworkSitesPaginator = client.get_paginator("list_network_sites")
    list_networks_paginator: ListNetworksPaginator = client.get_paginator("list_networks")
    list_orders_paginator: ListOrdersPaginator = client.get_paginator("list_orders")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDeviceIdentifiersRequestListDeviceIdentifiersPaginateTypeDef,
    ListDeviceIdentifiersResponseTypeDef,
    ListNetworkResourcesRequestListNetworkResourcesPaginateTypeDef,
    ListNetworkResourcesResponseTypeDef,
    ListNetworkSitesRequestListNetworkSitesPaginateTypeDef,
    ListNetworkSitesResponseTypeDef,
    ListNetworksRequestListNetworksPaginateTypeDef,
    ListNetworksResponseTypeDef,
    ListOrdersRequestListOrdersPaginateTypeDef,
    ListOrdersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDeviceIdentifiersPaginator",
    "ListNetworkResourcesPaginator",
    "ListNetworkSitesPaginator",
    "ListNetworksPaginator",
    "ListOrdersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDeviceIdentifiersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListDeviceIdentifiers.html#Private5G.Paginator.ListDeviceIdentifiers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listdeviceidentifierspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDeviceIdentifiersRequestListDeviceIdentifiersPaginateTypeDef]
    ) -> _PageIterator[ListDeviceIdentifiersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListDeviceIdentifiers.html#Private5G.Paginator.ListDeviceIdentifiers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listdeviceidentifierspaginator)
        """

class ListNetworkResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworkResources.html#Private5G.Paginator.ListNetworkResources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listnetworkresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListNetworkResourcesRequestListNetworkResourcesPaginateTypeDef]
    ) -> _PageIterator[ListNetworkResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworkResources.html#Private5G.Paginator.ListNetworkResources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listnetworkresourcespaginator)
        """

class ListNetworkSitesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworkSites.html#Private5G.Paginator.ListNetworkSites)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listnetworksitespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListNetworkSitesRequestListNetworkSitesPaginateTypeDef]
    ) -> _PageIterator[ListNetworkSitesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworkSites.html#Private5G.Paginator.ListNetworkSites.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listnetworksitespaginator)
        """

class ListNetworksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworks.html#Private5G.Paginator.ListNetworks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listnetworkspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListNetworksRequestListNetworksPaginateTypeDef]
    ) -> _PageIterator[ListNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworks.html#Private5G.Paginator.ListNetworks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listnetworkspaginator)
        """

class ListOrdersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListOrders.html#Private5G.Paginator.ListOrders)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listorderspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListOrdersRequestListOrdersPaginateTypeDef]
    ) -> _PageIterator[ListOrdersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListOrders.html#Private5G.Paginator.ListOrders.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listorderspaginator)
        """
