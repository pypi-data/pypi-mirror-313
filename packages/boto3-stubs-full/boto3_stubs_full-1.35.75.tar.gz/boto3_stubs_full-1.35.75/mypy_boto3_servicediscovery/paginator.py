"""
Type annotations for servicediscovery service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_servicediscovery.client import ServiceDiscoveryClient
    from mypy_boto3_servicediscovery.paginator import (
        ListInstancesPaginator,
        ListNamespacesPaginator,
        ListOperationsPaginator,
        ListServicesPaginator,
    )

    session = Session()
    client: ServiceDiscoveryClient = session.client("servicediscovery")

    list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    list_namespaces_paginator: ListNamespacesPaginator = client.get_paginator("list_namespaces")
    list_operations_paginator: ListOperationsPaginator = client.get_paginator("list_operations")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListInstancesRequestListInstancesPaginateTypeDef,
    ListInstancesResponseTypeDef,
    ListNamespacesRequestListNamespacesPaginateTypeDef,
    ListNamespacesResponseTypeDef,
    ListOperationsRequestListOperationsPaginateTypeDef,
    ListOperationsResponseTypeDef,
    ListServicesRequestListServicesPaginateTypeDef,
    ListServicesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListInstancesPaginator",
    "ListNamespacesPaginator",
    "ListOperationsPaginator",
    "ListServicesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/paginator/ListInstances.html#ServiceDiscovery.Paginator.ListInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/paginators/#listinstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListInstancesRequestListInstancesPaginateTypeDef]
    ) -> _PageIterator[ListInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/paginator/ListInstances.html#ServiceDiscovery.Paginator.ListInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/paginators/#listinstancespaginator)
        """


class ListNamespacesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/paginator/ListNamespaces.html#ServiceDiscovery.Paginator.ListNamespaces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/paginators/#listnamespacespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListNamespacesRequestListNamespacesPaginateTypeDef]
    ) -> _PageIterator[ListNamespacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/paginator/ListNamespaces.html#ServiceDiscovery.Paginator.ListNamespaces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/paginators/#listnamespacespaginator)
        """


class ListOperationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/paginator/ListOperations.html#ServiceDiscovery.Paginator.ListOperations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/paginators/#listoperationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOperationsRequestListOperationsPaginateTypeDef]
    ) -> _PageIterator[ListOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/paginator/ListOperations.html#ServiceDiscovery.Paginator.ListOperations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/paginators/#listoperationspaginator)
        """


class ListServicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/paginator/ListServices.html#ServiceDiscovery.Paginator.ListServices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/paginators/#listservicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListServicesRequestListServicesPaginateTypeDef]
    ) -> _PageIterator[ListServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/paginator/ListServices.html#ServiceDiscovery.Paginator.ListServices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/paginators/#listservicespaginator)
        """
