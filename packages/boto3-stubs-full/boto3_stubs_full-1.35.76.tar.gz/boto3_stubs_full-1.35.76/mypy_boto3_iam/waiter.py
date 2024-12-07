"""
Type annotations for iam service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_iam.client import IAMClient
    from mypy_boto3_iam.waiter import (
        InstanceProfileExistsWaiter,
        PolicyExistsWaiter,
        RoleExistsWaiter,
        UserExistsWaiter,
    )

    session = Session()
    client: IAMClient = session.client("iam")

    instance_profile_exists_waiter: InstanceProfileExistsWaiter = client.get_waiter("instance_profile_exists")
    policy_exists_waiter: PolicyExistsWaiter = client.get_waiter("policy_exists")
    role_exists_waiter: RoleExistsWaiter = client.get_waiter("role_exists")
    user_exists_waiter: UserExistsWaiter = client.get_waiter("user_exists")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import (
    GetInstanceProfileRequestInstanceProfileExistsWaitTypeDef,
    GetPolicyRequestPolicyExistsWaitTypeDef,
    GetRoleRequestRoleExistsWaitTypeDef,
    GetUserRequestUserExistsWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "InstanceProfileExistsWaiter",
    "PolicyExistsWaiter",
    "RoleExistsWaiter",
    "UserExistsWaiter",
)


class InstanceProfileExistsWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/waiter/InstanceProfileExists.html#IAM.Waiter.InstanceProfileExists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/waiters/#instanceprofileexistswaiter)
    """

    def wait(
        self, **kwargs: Unpack[GetInstanceProfileRequestInstanceProfileExistsWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/waiter/InstanceProfileExists.html#IAM.Waiter.InstanceProfileExists.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/waiters/#instanceprofileexistswaiter)
        """


class PolicyExistsWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/waiter/PolicyExists.html#IAM.Waiter.PolicyExists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/waiters/#policyexistswaiter)
    """

    def wait(self, **kwargs: Unpack[GetPolicyRequestPolicyExistsWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/waiter/PolicyExists.html#IAM.Waiter.PolicyExists.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/waiters/#policyexistswaiter)
        """


class RoleExistsWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/waiter/RoleExists.html#IAM.Waiter.RoleExists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/waiters/#roleexistswaiter)
    """

    def wait(self, **kwargs: Unpack[GetRoleRequestRoleExistsWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/waiter/RoleExists.html#IAM.Waiter.RoleExists.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/waiters/#roleexistswaiter)
        """


class UserExistsWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/waiter/UserExists.html#IAM.Waiter.UserExists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/waiters/#userexistswaiter)
    """

    def wait(self, **kwargs: Unpack[GetUserRequestUserExistsWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/waiter/UserExists.html#IAM.Waiter.UserExists.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/waiters/#userexistswaiter)
        """
