"""
Type annotations for elasticbeanstalk service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_elasticbeanstalk.client import ElasticBeanstalkClient
    from mypy_boto3_elasticbeanstalk.waiter import (
        EnvironmentExistsWaiter,
        EnvironmentTerminatedWaiter,
        EnvironmentUpdatedWaiter,
    )

    session = Session()
    client: ElasticBeanstalkClient = session.client("elasticbeanstalk")

    environment_exists_waiter: EnvironmentExistsWaiter = client.get_waiter("environment_exists")
    environment_terminated_waiter: EnvironmentTerminatedWaiter = client.get_waiter("environment_terminated")
    environment_updated_waiter: EnvironmentUpdatedWaiter = client.get_waiter("environment_updated")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import (
    DescribeEnvironmentsMessageEnvironmentExistsWaitTypeDef,
    DescribeEnvironmentsMessageEnvironmentTerminatedWaitTypeDef,
    DescribeEnvironmentsMessageEnvironmentUpdatedWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("EnvironmentExistsWaiter", "EnvironmentTerminatedWaiter", "EnvironmentUpdatedWaiter")


class EnvironmentExistsWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/waiter/EnvironmentExists.html#ElasticBeanstalk.Waiter.EnvironmentExists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/waiters/#environmentexistswaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeEnvironmentsMessageEnvironmentExistsWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/waiter/EnvironmentExists.html#ElasticBeanstalk.Waiter.EnvironmentExists.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/waiters/#environmentexistswaiter)
        """


class EnvironmentTerminatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/waiter/EnvironmentTerminated.html#ElasticBeanstalk.Waiter.EnvironmentTerminated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/waiters/#environmentterminatedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeEnvironmentsMessageEnvironmentTerminatedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/waiter/EnvironmentTerminated.html#ElasticBeanstalk.Waiter.EnvironmentTerminated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/waiters/#environmentterminatedwaiter)
        """


class EnvironmentUpdatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/waiter/EnvironmentUpdated.html#ElasticBeanstalk.Waiter.EnvironmentUpdated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/waiters/#environmentupdatedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeEnvironmentsMessageEnvironmentUpdatedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/waiter/EnvironmentUpdated.html#ElasticBeanstalk.Waiter.EnvironmentUpdated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/waiters/#environmentupdatedwaiter)
        """
