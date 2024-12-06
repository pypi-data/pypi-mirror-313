"""
Type annotations for codedeploy service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_codedeploy.client import CodeDeployClient
    from mypy_boto3_codedeploy.waiter import (
        DeploymentSuccessfulWaiter,
    )

    session = Session()
    client: CodeDeployClient = session.client("codedeploy")

    deployment_successful_waiter: DeploymentSuccessfulWaiter = client.get_waiter("deployment_successful")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import GetDeploymentInputDeploymentSuccessfulWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DeploymentSuccessfulWaiter",)


class DeploymentSuccessfulWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/waiter/DeploymentSuccessful.html#CodeDeploy.Waiter.DeploymentSuccessful)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/waiters/#deploymentsuccessfulwaiter)
    """

    def wait(self, **kwargs: Unpack[GetDeploymentInputDeploymentSuccessfulWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/waiter/DeploymentSuccessful.html#CodeDeploy.Waiter.DeploymentSuccessful.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/waiters/#deploymentsuccessfulwaiter)
        """
