"""
Type annotations for opsworkscm service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworkscm/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_opsworkscm.client import OpsWorksCMClient
    from mypy_boto3_opsworkscm.waiter import (
        NodeAssociatedWaiter,
    )

    session = Session()
    client: OpsWorksCMClient = session.client("opsworkscm")

    node_associated_waiter: NodeAssociatedWaiter = client.get_waiter("node_associated")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import DescribeNodeAssociationStatusRequestNodeAssociatedWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("NodeAssociatedWaiter",)


class NodeAssociatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworkscm/waiter/NodeAssociated.html#OpsWorksCM.Waiter.NodeAssociated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworkscm/waiters/#nodeassociatedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeNodeAssociationStatusRequestNodeAssociatedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworkscm/waiter/NodeAssociated.html#OpsWorksCM.Waiter.NodeAssociated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworkscm/waiters/#nodeassociatedwaiter)
        """
