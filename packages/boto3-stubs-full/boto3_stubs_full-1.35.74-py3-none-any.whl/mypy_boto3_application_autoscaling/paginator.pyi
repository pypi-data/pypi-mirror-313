"""
Type annotations for application-autoscaling service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_application_autoscaling.client import ApplicationAutoScalingClient
    from mypy_boto3_application_autoscaling.paginator import (
        DescribeScalableTargetsPaginator,
        DescribeScalingActivitiesPaginator,
        DescribeScalingPoliciesPaginator,
        DescribeScheduledActionsPaginator,
    )

    session = Session()
    client: ApplicationAutoScalingClient = session.client("application-autoscaling")

    describe_scalable_targets_paginator: DescribeScalableTargetsPaginator = client.get_paginator("describe_scalable_targets")
    describe_scaling_activities_paginator: DescribeScalingActivitiesPaginator = client.get_paginator("describe_scaling_activities")
    describe_scaling_policies_paginator: DescribeScalingPoliciesPaginator = client.get_paginator("describe_scaling_policies")
    describe_scheduled_actions_paginator: DescribeScheduledActionsPaginator = client.get_paginator("describe_scheduled_actions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeScalableTargetsRequestDescribeScalableTargetsPaginateTypeDef,
    DescribeScalableTargetsResponseTypeDef,
    DescribeScalingActivitiesRequestDescribeScalingActivitiesPaginateTypeDef,
    DescribeScalingActivitiesResponseTypeDef,
    DescribeScalingPoliciesRequestDescribeScalingPoliciesPaginateTypeDef,
    DescribeScalingPoliciesResponseTypeDef,
    DescribeScheduledActionsRequestDescribeScheduledActionsPaginateTypeDef,
    DescribeScheduledActionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeScalableTargetsPaginator",
    "DescribeScalingActivitiesPaginator",
    "DescribeScalingPoliciesPaginator",
    "DescribeScheduledActionsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeScalableTargetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/paginator/DescribeScalableTargets.html#ApplicationAutoScaling.Paginator.DescribeScalableTargets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/paginators/#describescalabletargetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeScalableTargetsRequestDescribeScalableTargetsPaginateTypeDef]
    ) -> _PageIterator[DescribeScalableTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/paginator/DescribeScalableTargets.html#ApplicationAutoScaling.Paginator.DescribeScalableTargets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/paginators/#describescalabletargetspaginator)
        """

class DescribeScalingActivitiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/paginator/DescribeScalingActivities.html#ApplicationAutoScaling.Paginator.DescribeScalingActivities)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/paginators/#describescalingactivitiespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeScalingActivitiesRequestDescribeScalingActivitiesPaginateTypeDef],
    ) -> _PageIterator[DescribeScalingActivitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/paginator/DescribeScalingActivities.html#ApplicationAutoScaling.Paginator.DescribeScalingActivities.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/paginators/#describescalingactivitiespaginator)
        """

class DescribeScalingPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/paginator/DescribeScalingPolicies.html#ApplicationAutoScaling.Paginator.DescribeScalingPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/paginators/#describescalingpoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeScalingPoliciesRequestDescribeScalingPoliciesPaginateTypeDef]
    ) -> _PageIterator[DescribeScalingPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/paginator/DescribeScalingPolicies.html#ApplicationAutoScaling.Paginator.DescribeScalingPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/paginators/#describescalingpoliciespaginator)
        """

class DescribeScheduledActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/paginator/DescribeScheduledActions.html#ApplicationAutoScaling.Paginator.DescribeScheduledActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/paginators/#describescheduledactionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeScheduledActionsRequestDescribeScheduledActionsPaginateTypeDef],
    ) -> _PageIterator[DescribeScheduledActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/paginator/DescribeScheduledActions.html#ApplicationAutoScaling.Paginator.DescribeScheduledActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/paginators/#describescheduledactionspaginator)
        """
