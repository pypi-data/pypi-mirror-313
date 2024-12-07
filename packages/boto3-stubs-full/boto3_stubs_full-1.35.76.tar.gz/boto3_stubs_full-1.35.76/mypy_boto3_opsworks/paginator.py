"""
Type annotations for opsworks service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_opsworks.client import OpsWorksClient
    from mypy_boto3_opsworks.paginator import (
        DescribeEcsClustersPaginator,
    )

    session = Session()
    client: OpsWorksClient = session.client("opsworks")

    describe_ecs_clusters_paginator: DescribeEcsClustersPaginator = client.get_paginator("describe_ecs_clusters")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeEcsClustersRequestDescribeEcsClustersPaginateTypeDef,
    DescribeEcsClustersResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DescribeEcsClustersPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeEcsClustersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/paginator/DescribeEcsClusters.html#OpsWorks.Paginator.DescribeEcsClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/paginators/#describeecsclusterspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeEcsClustersRequestDescribeEcsClustersPaginateTypeDef]
    ) -> _PageIterator[DescribeEcsClustersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/paginator/DescribeEcsClusters.html#OpsWorks.Paginator.DescribeEcsClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/paginators/#describeecsclusterspaginator)
        """
