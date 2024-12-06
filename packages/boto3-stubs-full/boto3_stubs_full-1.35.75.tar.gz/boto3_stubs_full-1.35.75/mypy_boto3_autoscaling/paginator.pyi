"""
Type annotations for autoscaling service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_autoscaling.client import AutoScalingClient
    from mypy_boto3_autoscaling.paginator import (
        DescribeAutoScalingGroupsPaginator,
        DescribeAutoScalingInstancesPaginator,
        DescribeLaunchConfigurationsPaginator,
        DescribeLoadBalancerTargetGroupsPaginator,
        DescribeLoadBalancersPaginator,
        DescribeNotificationConfigurationsPaginator,
        DescribePoliciesPaginator,
        DescribeScalingActivitiesPaginator,
        DescribeScheduledActionsPaginator,
        DescribeTagsPaginator,
        DescribeWarmPoolPaginator,
    )

    session = Session()
    client: AutoScalingClient = session.client("autoscaling")

    describe_auto_scaling_groups_paginator: DescribeAutoScalingGroupsPaginator = client.get_paginator("describe_auto_scaling_groups")
    describe_auto_scaling_instances_paginator: DescribeAutoScalingInstancesPaginator = client.get_paginator("describe_auto_scaling_instances")
    describe_launch_configurations_paginator: DescribeLaunchConfigurationsPaginator = client.get_paginator("describe_launch_configurations")
    describe_load_balancer_target_groups_paginator: DescribeLoadBalancerTargetGroupsPaginator = client.get_paginator("describe_load_balancer_target_groups")
    describe_load_balancers_paginator: DescribeLoadBalancersPaginator = client.get_paginator("describe_load_balancers")
    describe_notification_configurations_paginator: DescribeNotificationConfigurationsPaginator = client.get_paginator("describe_notification_configurations")
    describe_policies_paginator: DescribePoliciesPaginator = client.get_paginator("describe_policies")
    describe_scaling_activities_paginator: DescribeScalingActivitiesPaginator = client.get_paginator("describe_scaling_activities")
    describe_scheduled_actions_paginator: DescribeScheduledActionsPaginator = client.get_paginator("describe_scheduled_actions")
    describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
    describe_warm_pool_paginator: DescribeWarmPoolPaginator = client.get_paginator("describe_warm_pool")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ActivitiesTypeTypeDef,
    AutoScalingGroupNamesTypeDescribeAutoScalingGroupsPaginateTypeDef,
    AutoScalingGroupsTypeTypeDef,
    AutoScalingInstancesTypeTypeDef,
    DescribeAutoScalingInstancesTypeDescribeAutoScalingInstancesPaginateTypeDef,
    DescribeLoadBalancersRequestDescribeLoadBalancersPaginateTypeDef,
    DescribeLoadBalancersResponseTypeDef,
    DescribeLoadBalancerTargetGroupsRequestDescribeLoadBalancerTargetGroupsPaginateTypeDef,
    DescribeLoadBalancerTargetGroupsResponseTypeDef,
    DescribeNotificationConfigurationsAnswerTypeDef,
    DescribeNotificationConfigurationsTypeDescribeNotificationConfigurationsPaginateTypeDef,
    DescribePoliciesTypeDescribePoliciesPaginateTypeDef,
    DescribeScalingActivitiesTypeDescribeScalingActivitiesPaginateTypeDef,
    DescribeScheduledActionsTypeDescribeScheduledActionsPaginateTypeDef,
    DescribeTagsTypeDescribeTagsPaginateTypeDef,
    DescribeWarmPoolAnswerTypeDef,
    DescribeWarmPoolTypeDescribeWarmPoolPaginateTypeDef,
    LaunchConfigurationNamesTypeDescribeLaunchConfigurationsPaginateTypeDef,
    LaunchConfigurationsTypeTypeDef,
    PoliciesTypeTypeDef,
    ScheduledActionsTypeTypeDef,
    TagsTypeTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeAutoScalingGroupsPaginator",
    "DescribeAutoScalingInstancesPaginator",
    "DescribeLaunchConfigurationsPaginator",
    "DescribeLoadBalancerTargetGroupsPaginator",
    "DescribeLoadBalancersPaginator",
    "DescribeNotificationConfigurationsPaginator",
    "DescribePoliciesPaginator",
    "DescribeScalingActivitiesPaginator",
    "DescribeScheduledActionsPaginator",
    "DescribeTagsPaginator",
    "DescribeWarmPoolPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeAutoScalingGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeAutoScalingGroups.html#AutoScaling.Paginator.DescribeAutoScalingGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describeautoscalinggroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[AutoScalingGroupNamesTypeDescribeAutoScalingGroupsPaginateTypeDef]
    ) -> _PageIterator[AutoScalingGroupsTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeAutoScalingGroups.html#AutoScaling.Paginator.DescribeAutoScalingGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describeautoscalinggroupspaginator)
        """

class DescribeAutoScalingInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeAutoScalingInstances.html#AutoScaling.Paginator.DescribeAutoScalingInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describeautoscalinginstancespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAutoScalingInstancesTypeDescribeAutoScalingInstancesPaginateTypeDef
        ],
    ) -> _PageIterator[AutoScalingInstancesTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeAutoScalingInstances.html#AutoScaling.Paginator.DescribeAutoScalingInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describeautoscalinginstancespaginator)
        """

class DescribeLaunchConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLaunchConfigurations.html#AutoScaling.Paginator.DescribeLaunchConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describelaunchconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[LaunchConfigurationNamesTypeDescribeLaunchConfigurationsPaginateTypeDef],
    ) -> _PageIterator[LaunchConfigurationsTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLaunchConfigurations.html#AutoScaling.Paginator.DescribeLaunchConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describelaunchconfigurationspaginator)
        """

class DescribeLoadBalancerTargetGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLoadBalancerTargetGroups.html#AutoScaling.Paginator.DescribeLoadBalancerTargetGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describeloadbalancertargetgroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeLoadBalancerTargetGroupsRequestDescribeLoadBalancerTargetGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeLoadBalancerTargetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLoadBalancerTargetGroups.html#AutoScaling.Paginator.DescribeLoadBalancerTargetGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describeloadbalancertargetgroupspaginator)
        """

class DescribeLoadBalancersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLoadBalancers.html#AutoScaling.Paginator.DescribeLoadBalancers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describeloadbalancerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeLoadBalancersRequestDescribeLoadBalancersPaginateTypeDef]
    ) -> _PageIterator[DescribeLoadBalancersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLoadBalancers.html#AutoScaling.Paginator.DescribeLoadBalancers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describeloadbalancerspaginator)
        """

class DescribeNotificationConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeNotificationConfigurations.html#AutoScaling.Paginator.DescribeNotificationConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describenotificationconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeNotificationConfigurationsTypeDescribeNotificationConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeNotificationConfigurationsAnswerTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeNotificationConfigurations.html#AutoScaling.Paginator.DescribeNotificationConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describenotificationconfigurationspaginator)
        """

class DescribePoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribePolicies.html#AutoScaling.Paginator.DescribePolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describepoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribePoliciesTypeDescribePoliciesPaginateTypeDef]
    ) -> _PageIterator[PoliciesTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribePolicies.html#AutoScaling.Paginator.DescribePolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describepoliciespaginator)
        """

class DescribeScalingActivitiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeScalingActivities.html#AutoScaling.Paginator.DescribeScalingActivities)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describescalingactivitiespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeScalingActivitiesTypeDescribeScalingActivitiesPaginateTypeDef],
    ) -> _PageIterator[ActivitiesTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeScalingActivities.html#AutoScaling.Paginator.DescribeScalingActivities.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describescalingactivitiespaginator)
        """

class DescribeScheduledActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeScheduledActions.html#AutoScaling.Paginator.DescribeScheduledActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describescheduledactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeScheduledActionsTypeDescribeScheduledActionsPaginateTypeDef]
    ) -> _PageIterator[ScheduledActionsTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeScheduledActions.html#AutoScaling.Paginator.DescribeScheduledActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describescheduledactionspaginator)
        """

class DescribeTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeTags.html#AutoScaling.Paginator.DescribeTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describetagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeTagsTypeDescribeTagsPaginateTypeDef]
    ) -> _PageIterator[TagsTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeTags.html#AutoScaling.Paginator.DescribeTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describetagspaginator)
        """

class DescribeWarmPoolPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeWarmPool.html#AutoScaling.Paginator.DescribeWarmPool)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describewarmpoolpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeWarmPoolTypeDescribeWarmPoolPaginateTypeDef]
    ) -> _PageIterator[DescribeWarmPoolAnswerTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeWarmPool.html#AutoScaling.Paginator.DescribeWarmPool.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/paginators/#describewarmpoolpaginator)
        """
