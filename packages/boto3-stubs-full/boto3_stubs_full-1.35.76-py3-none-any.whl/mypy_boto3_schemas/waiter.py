"""
Type annotations for schemas service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_schemas/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_schemas.client import SchemasClient
    from mypy_boto3_schemas.waiter import (
        CodeBindingExistsWaiter,
    )

    session = Session()
    client: SchemasClient = session.client("schemas")

    code_binding_exists_waiter: CodeBindingExistsWaiter = client.get_waiter("code_binding_exists")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import DescribeCodeBindingRequestCodeBindingExistsWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("CodeBindingExistsWaiter",)


class CodeBindingExistsWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/waiter/CodeBindingExists.html#Schemas.Waiter.CodeBindingExists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_schemas/waiters/#codebindingexistswaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeCodeBindingRequestCodeBindingExistsWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/waiter/CodeBindingExists.html#Schemas.Waiter.CodeBindingExists.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_schemas/waiters/#codebindingexistswaiter)
        """
