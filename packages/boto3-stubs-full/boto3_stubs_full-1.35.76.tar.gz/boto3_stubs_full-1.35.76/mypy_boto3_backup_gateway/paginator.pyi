"""
Type annotations for backup-gateway service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_backup_gateway.client import BackupGatewayClient
    from mypy_boto3_backup_gateway.paginator import (
        ListGatewaysPaginator,
        ListHypervisorsPaginator,
        ListVirtualMachinesPaginator,
    )

    session = Session()
    client: BackupGatewayClient = session.client("backup-gateway")

    list_gateways_paginator: ListGatewaysPaginator = client.get_paginator("list_gateways")
    list_hypervisors_paginator: ListHypervisorsPaginator = client.get_paginator("list_hypervisors")
    list_virtual_machines_paginator: ListVirtualMachinesPaginator = client.get_paginator("list_virtual_machines")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListGatewaysInputListGatewaysPaginateTypeDef,
    ListGatewaysOutputTypeDef,
    ListHypervisorsInputListHypervisorsPaginateTypeDef,
    ListHypervisorsOutputTypeDef,
    ListVirtualMachinesInputListVirtualMachinesPaginateTypeDef,
    ListVirtualMachinesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListGatewaysPaginator", "ListHypervisorsPaginator", "ListVirtualMachinesPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListGatewaysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListGateways.html#BackupGateway.Paginator.ListGateways)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/paginators/#listgatewayspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGatewaysInputListGatewaysPaginateTypeDef]
    ) -> _PageIterator[ListGatewaysOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListGateways.html#BackupGateway.Paginator.ListGateways.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/paginators/#listgatewayspaginator)
        """

class ListHypervisorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListHypervisors.html#BackupGateway.Paginator.ListHypervisors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/paginators/#listhypervisorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListHypervisorsInputListHypervisorsPaginateTypeDef]
    ) -> _PageIterator[ListHypervisorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListHypervisors.html#BackupGateway.Paginator.ListHypervisors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/paginators/#listhypervisorspaginator)
        """

class ListVirtualMachinesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListVirtualMachines.html#BackupGateway.Paginator.ListVirtualMachines)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/paginators/#listvirtualmachinespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListVirtualMachinesInputListVirtualMachinesPaginateTypeDef]
    ) -> _PageIterator[ListVirtualMachinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListVirtualMachines.html#BackupGateway.Paginator.ListVirtualMachines.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/paginators/#listvirtualmachinespaginator)
        """
