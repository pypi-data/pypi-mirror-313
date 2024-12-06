"""
Type annotations for transfer service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_transfer.client import TransferClient
    from mypy_boto3_transfer.waiter import (
        ServerOfflineWaiter,
        ServerOnlineWaiter,
    )

    session = Session()
    client: TransferClient = session.client("transfer")

    server_offline_waiter: ServerOfflineWaiter = client.get_waiter("server_offline")
    server_online_waiter: ServerOnlineWaiter = client.get_waiter("server_online")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import (
    DescribeServerRequestServerOfflineWaitTypeDef,
    DescribeServerRequestServerOnlineWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ServerOfflineWaiter", "ServerOnlineWaiter")


class ServerOfflineWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/waiter/ServerOffline.html#Transfer.Waiter.ServerOffline)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/waiters/#serverofflinewaiter)
    """

    def wait(self, **kwargs: Unpack[DescribeServerRequestServerOfflineWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/waiter/ServerOffline.html#Transfer.Waiter.ServerOffline.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/waiters/#serverofflinewaiter)
        """


class ServerOnlineWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/waiter/ServerOnline.html#Transfer.Waiter.ServerOnline)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/waiters/#serveronlinewaiter)
    """

    def wait(self, **kwargs: Unpack[DescribeServerRequestServerOnlineWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/waiter/ServerOnline.html#Transfer.Waiter.ServerOnline.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/waiters/#serveronlinewaiter)
        """
