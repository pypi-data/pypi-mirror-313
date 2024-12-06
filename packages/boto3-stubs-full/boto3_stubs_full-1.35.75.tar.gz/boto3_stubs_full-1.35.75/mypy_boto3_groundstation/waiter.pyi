"""
Type annotations for groundstation service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_groundstation.client import GroundStationClient
    from mypy_boto3_groundstation.waiter import (
        ContactScheduledWaiter,
    )

    session = Session()
    client: GroundStationClient = session.client("groundstation")

    contact_scheduled_waiter: ContactScheduledWaiter = client.get_waiter("contact_scheduled")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import DescribeContactRequestContactScheduledWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ContactScheduledWaiter",)

class ContactScheduledWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/waiter/ContactScheduled.html#GroundStation.Waiter.ContactScheduled)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/waiters/#contactscheduledwaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeContactRequestContactScheduledWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/waiter/ContactScheduled.html#GroundStation.Waiter.ContactScheduled.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/waiters/#contactscheduledwaiter)
        """
