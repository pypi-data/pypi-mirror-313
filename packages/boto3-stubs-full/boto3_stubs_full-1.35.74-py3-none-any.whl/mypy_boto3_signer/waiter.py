"""
Type annotations for signer service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_signer.client import SignerClient
    from mypy_boto3_signer.waiter import (
        SuccessfulSigningJobWaiter,
    )

    session = Session()
    client: SignerClient = session.client("signer")

    successful_signing_job_waiter: SuccessfulSigningJobWaiter = client.get_waiter("successful_signing_job")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import DescribeSigningJobRequestSuccessfulSigningJobWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("SuccessfulSigningJobWaiter",)


class SuccessfulSigningJobWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/waiter/SuccessfulSigningJob.html#Signer.Waiter.SuccessfulSigningJob)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/waiters/#successfulsigningjobwaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeSigningJobRequestSuccessfulSigningJobWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/waiter/SuccessfulSigningJob.html#Signer.Waiter.SuccessfulSigningJob.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/waiters/#successfulsigningjobwaiter)
        """
