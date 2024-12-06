"""
Type annotations for docdb service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_docdb.client import DocDBClient
    from mypy_boto3_docdb.waiter import (
        DBInstanceAvailableWaiter,
        DBInstanceDeletedWaiter,
    )

    session = Session()
    client: DocDBClient = session.client("docdb")

    db_instance_available_waiter: DBInstanceAvailableWaiter = client.get_waiter("db_instance_available")
    db_instance_deleted_waiter: DBInstanceDeletedWaiter = client.get_waiter("db_instance_deleted")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import (
    DescribeDBInstancesMessageDBInstanceAvailableWaitTypeDef,
    DescribeDBInstancesMessageDBInstanceDeletedWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DBInstanceAvailableWaiter", "DBInstanceDeletedWaiter")


class DBInstanceAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/waiter/DBInstanceAvailable.html#DocDB.Waiter.DBInstanceAvailable)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/waiters/#dbinstanceavailablewaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeDBInstancesMessageDBInstanceAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/waiter/DBInstanceAvailable.html#DocDB.Waiter.DBInstanceAvailable.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/waiters/#dbinstanceavailablewaiter)
        """


class DBInstanceDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/waiter/DBInstanceDeleted.html#DocDB.Waiter.DBInstanceDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/waiters/#dbinstancedeletedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeDBInstancesMessageDBInstanceDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/waiter/DBInstanceDeleted.html#DocDB.Waiter.DBInstanceDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/waiters/#dbinstancedeletedwaiter)
        """
