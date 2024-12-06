"""
Type annotations for route53-recovery-cluster service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_cluster/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_route53_recovery_cluster.client import Route53RecoveryClusterClient
    from mypy_boto3_route53_recovery_cluster.paginator import (
        ListRoutingControlsPaginator,
    )

    session = Session()
    client: Route53RecoveryClusterClient = session.client("route53-recovery-cluster")

    list_routing_controls_paginator: ListRoutingControlsPaginator = client.get_paginator("list_routing_controls")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListRoutingControlsRequestListRoutingControlsPaginateTypeDef,
    ListRoutingControlsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListRoutingControlsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListRoutingControlsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster/paginator/ListRoutingControls.html#Route53RecoveryCluster.Paginator.ListRoutingControls)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_cluster/paginators/#listroutingcontrolspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRoutingControlsRequestListRoutingControlsPaginateTypeDef]
    ) -> _PageIterator[ListRoutingControlsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster/paginator/ListRoutingControls.html#Route53RecoveryCluster.Paginator.ListRoutingControls.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_cluster/paginators/#listroutingcontrolspaginator)
        """
