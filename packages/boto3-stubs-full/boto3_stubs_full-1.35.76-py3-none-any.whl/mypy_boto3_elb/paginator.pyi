"""
Type annotations for elb service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_elb.client import ElasticLoadBalancingClient
    from mypy_boto3_elb.paginator import (
        DescribeAccountLimitsPaginator,
        DescribeLoadBalancersPaginator,
    )

    session = Session()
    client: ElasticLoadBalancingClient = session.client("elb")

    describe_account_limits_paginator: DescribeAccountLimitsPaginator = client.get_paginator("describe_account_limits")
    describe_load_balancers_paginator: DescribeLoadBalancersPaginator = client.get_paginator("describe_load_balancers")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeAccessPointsInputDescribeLoadBalancersPaginateTypeDef,
    DescribeAccessPointsOutputTypeDef,
    DescribeAccountLimitsInputDescribeAccountLimitsPaginateTypeDef,
    DescribeAccountLimitsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("DescribeAccountLimitsPaginator", "DescribeLoadBalancersPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeAccountLimitsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/paginator/DescribeAccountLimits.html#ElasticLoadBalancing.Paginator.DescribeAccountLimits)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/paginators/#describeaccountlimitspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeAccountLimitsInputDescribeAccountLimitsPaginateTypeDef]
    ) -> _PageIterator[DescribeAccountLimitsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/paginator/DescribeAccountLimits.html#ElasticLoadBalancing.Paginator.DescribeAccountLimits.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/paginators/#describeaccountlimitspaginator)
        """

class DescribeLoadBalancersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/paginator/DescribeLoadBalancers.html#ElasticLoadBalancing.Paginator.DescribeLoadBalancers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/paginators/#describeloadbalancerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeAccessPointsInputDescribeLoadBalancersPaginateTypeDef]
    ) -> _PageIterator[DescribeAccessPointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/paginator/DescribeLoadBalancers.html#ElasticLoadBalancing.Paginator.DescribeLoadBalancers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/paginators/#describeloadbalancerspaginator)
        """
