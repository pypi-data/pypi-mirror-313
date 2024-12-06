"""
Type annotations for autoscaling-plans service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_autoscaling_plans.client import AutoScalingPlansClient
    from mypy_boto3_autoscaling_plans.paginator import (
        DescribeScalingPlanResourcesPaginator,
        DescribeScalingPlansPaginator,
    )

    session = Session()
    client: AutoScalingPlansClient = session.client("autoscaling-plans")

    describe_scaling_plan_resources_paginator: DescribeScalingPlanResourcesPaginator = client.get_paginator("describe_scaling_plan_resources")
    describe_scaling_plans_paginator: DescribeScalingPlansPaginator = client.get_paginator("describe_scaling_plans")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeScalingPlanResourcesRequestDescribeScalingPlanResourcesPaginateTypeDef,
    DescribeScalingPlanResourcesResponseTypeDef,
    DescribeScalingPlansRequestDescribeScalingPlansPaginateTypeDef,
    DescribeScalingPlansResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("DescribeScalingPlanResourcesPaginator", "DescribeScalingPlansPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeScalingPlanResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans/paginator/DescribeScalingPlanResources.html#AutoScalingPlans.Paginator.DescribeScalingPlanResources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/paginators/#describescalingplanresourcespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeScalingPlanResourcesRequestDescribeScalingPlanResourcesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeScalingPlanResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans/paginator/DescribeScalingPlanResources.html#AutoScalingPlans.Paginator.DescribeScalingPlanResources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/paginators/#describescalingplanresourcespaginator)
        """

class DescribeScalingPlansPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans/paginator/DescribeScalingPlans.html#AutoScalingPlans.Paginator.DescribeScalingPlans)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/paginators/#describescalingplanspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeScalingPlansRequestDescribeScalingPlansPaginateTypeDef]
    ) -> _PageIterator[DescribeScalingPlansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans/paginator/DescribeScalingPlans.html#AutoScalingPlans.Paginator.DescribeScalingPlans.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/paginators/#describescalingplanspaginator)
        """
