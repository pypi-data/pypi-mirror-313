"""
Type annotations for cloudfront service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_cloudfront.client import CloudFrontClient
    from mypy_boto3_cloudfront.waiter import (
        DistributionDeployedWaiter,
        InvalidationCompletedWaiter,
        StreamingDistributionDeployedWaiter,
    )

    session = Session()
    client: CloudFrontClient = session.client("cloudfront")

    distribution_deployed_waiter: DistributionDeployedWaiter = client.get_waiter("distribution_deployed")
    invalidation_completed_waiter: InvalidationCompletedWaiter = client.get_waiter("invalidation_completed")
    streaming_distribution_deployed_waiter: StreamingDistributionDeployedWaiter = client.get_waiter("streaming_distribution_deployed")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import (
    GetDistributionRequestDistributionDeployedWaitTypeDef,
    GetInvalidationRequestInvalidationCompletedWaitTypeDef,
    GetStreamingDistributionRequestStreamingDistributionDeployedWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DistributionDeployedWaiter",
    "InvalidationCompletedWaiter",
    "StreamingDistributionDeployedWaiter",
)

class DistributionDeployedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/waiter/DistributionDeployed.html#CloudFront.Waiter.DistributionDeployed)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/waiters/#distributiondeployedwaiter)
    """
    def wait(self, **kwargs: Unpack[GetDistributionRequestDistributionDeployedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/waiter/DistributionDeployed.html#CloudFront.Waiter.DistributionDeployed.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/waiters/#distributiondeployedwaiter)
        """

class InvalidationCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/waiter/InvalidationCompleted.html#CloudFront.Waiter.InvalidationCompleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/waiters/#invalidationcompletedwaiter)
    """
    def wait(
        self, **kwargs: Unpack[GetInvalidationRequestInvalidationCompletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/waiter/InvalidationCompleted.html#CloudFront.Waiter.InvalidationCompleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/waiters/#invalidationcompletedwaiter)
        """

class StreamingDistributionDeployedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/waiter/StreamingDistributionDeployed.html#CloudFront.Waiter.StreamingDistributionDeployed)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/waiters/#streamingdistributiondeployedwaiter)
    """
    def wait(
        self,
        **kwargs: Unpack[GetStreamingDistributionRequestStreamingDistributionDeployedWaitTypeDef],
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/waiter/StreamingDistributionDeployed.html#CloudFront.Waiter.StreamingDistributionDeployed.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/waiters/#streamingdistributiondeployedwaiter)
        """
