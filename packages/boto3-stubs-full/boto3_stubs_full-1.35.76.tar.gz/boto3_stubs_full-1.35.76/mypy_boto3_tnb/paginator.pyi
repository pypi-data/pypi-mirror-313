"""
Type annotations for tnb service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_tnb/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_tnb.client import TelcoNetworkBuilderClient
    from mypy_boto3_tnb.paginator import (
        ListSolFunctionInstancesPaginator,
        ListSolFunctionPackagesPaginator,
        ListSolNetworkInstancesPaginator,
        ListSolNetworkOperationsPaginator,
        ListSolNetworkPackagesPaginator,
    )

    session = Session()
    client: TelcoNetworkBuilderClient = session.client("tnb")

    list_sol_function_instances_paginator: ListSolFunctionInstancesPaginator = client.get_paginator("list_sol_function_instances")
    list_sol_function_packages_paginator: ListSolFunctionPackagesPaginator = client.get_paginator("list_sol_function_packages")
    list_sol_network_instances_paginator: ListSolNetworkInstancesPaginator = client.get_paginator("list_sol_network_instances")
    list_sol_network_operations_paginator: ListSolNetworkOperationsPaginator = client.get_paginator("list_sol_network_operations")
    list_sol_network_packages_paginator: ListSolNetworkPackagesPaginator = client.get_paginator("list_sol_network_packages")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListSolFunctionInstancesInputListSolFunctionInstancesPaginateTypeDef,
    ListSolFunctionInstancesOutputTypeDef,
    ListSolFunctionPackagesInputListSolFunctionPackagesPaginateTypeDef,
    ListSolFunctionPackagesOutputTypeDef,
    ListSolNetworkInstancesInputListSolNetworkInstancesPaginateTypeDef,
    ListSolNetworkInstancesOutputTypeDef,
    ListSolNetworkOperationsInputListSolNetworkOperationsPaginateTypeDef,
    ListSolNetworkOperationsOutputTypeDef,
    ListSolNetworkPackagesInputListSolNetworkPackagesPaginateTypeDef,
    ListSolNetworkPackagesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListSolFunctionInstancesPaginator",
    "ListSolFunctionPackagesPaginator",
    "ListSolNetworkInstancesPaginator",
    "ListSolNetworkOperationsPaginator",
    "ListSolNetworkPackagesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListSolFunctionInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolFunctionInstances.html#TelcoNetworkBuilder.Paginator.ListSolFunctionInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_tnb/paginators/#listsolfunctioninstancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSolFunctionInstancesInputListSolFunctionInstancesPaginateTypeDef]
    ) -> _PageIterator[ListSolFunctionInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolFunctionInstances.html#TelcoNetworkBuilder.Paginator.ListSolFunctionInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_tnb/paginators/#listsolfunctioninstancespaginator)
        """

class ListSolFunctionPackagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolFunctionPackages.html#TelcoNetworkBuilder.Paginator.ListSolFunctionPackages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_tnb/paginators/#listsolfunctionpackagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSolFunctionPackagesInputListSolFunctionPackagesPaginateTypeDef]
    ) -> _PageIterator[ListSolFunctionPackagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolFunctionPackages.html#TelcoNetworkBuilder.Paginator.ListSolFunctionPackages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_tnb/paginators/#listsolfunctionpackagespaginator)
        """

class ListSolNetworkInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkInstances.html#TelcoNetworkBuilder.Paginator.ListSolNetworkInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_tnb/paginators/#listsolnetworkinstancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSolNetworkInstancesInputListSolNetworkInstancesPaginateTypeDef]
    ) -> _PageIterator[ListSolNetworkInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkInstances.html#TelcoNetworkBuilder.Paginator.ListSolNetworkInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_tnb/paginators/#listsolnetworkinstancespaginator)
        """

class ListSolNetworkOperationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkOperations.html#TelcoNetworkBuilder.Paginator.ListSolNetworkOperations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_tnb/paginators/#listsolnetworkoperationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSolNetworkOperationsInputListSolNetworkOperationsPaginateTypeDef]
    ) -> _PageIterator[ListSolNetworkOperationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkOperations.html#TelcoNetworkBuilder.Paginator.ListSolNetworkOperations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_tnb/paginators/#listsolnetworkoperationspaginator)
        """

class ListSolNetworkPackagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkPackages.html#TelcoNetworkBuilder.Paginator.ListSolNetworkPackages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_tnb/paginators/#listsolnetworkpackagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSolNetworkPackagesInputListSolNetworkPackagesPaginateTypeDef]
    ) -> _PageIterator[ListSolNetworkPackagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkPackages.html#TelcoNetworkBuilder.Paginator.ListSolNetworkPackages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_tnb/paginators/#listsolnetworkpackagespaginator)
        """
