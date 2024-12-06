"""
Type annotations for ses service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ses/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ses.client import SESClient
    from mypy_boto3_ses.waiter import (
        IdentityExistsWaiter,
    )

    session = Session()
    client: SESClient = session.client("ses")

    identity_exists_waiter: IdentityExistsWaiter = client.get_waiter("identity_exists")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import GetIdentityVerificationAttributesRequestIdentityExistsWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("IdentityExistsWaiter",)

class IdentityExistsWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/waiter/IdentityExists.html#SES.Waiter.IdentityExists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ses/waiters/#identityexistswaiter)
    """
    def wait(
        self, **kwargs: Unpack[GetIdentityVerificationAttributesRequestIdentityExistsWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/waiter/IdentityExists.html#SES.Waiter.IdentityExists.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ses/waiters/#identityexistswaiter)
        """
