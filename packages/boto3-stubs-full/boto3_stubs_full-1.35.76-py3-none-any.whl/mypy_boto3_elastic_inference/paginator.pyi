"""
Type annotations for elastic-inference service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_elastic_inference.client import ElasticInferenceClient
    from mypy_boto3_elastic_inference.paginator import (
        DescribeAcceleratorsPaginator,
    )

    session = Session()
    client: ElasticInferenceClient = session.client("elastic-inference")

    describe_accelerators_paginator: DescribeAcceleratorsPaginator = client.get_paginator("describe_accelerators")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeAcceleratorsRequestDescribeAcceleratorsPaginateTypeDef,
    DescribeAcceleratorsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("DescribeAcceleratorsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeAcceleratorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference/paginator/DescribeAccelerators.html#ElasticInference.Paginator.DescribeAccelerators)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/paginators/#describeacceleratorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeAcceleratorsRequestDescribeAcceleratorsPaginateTypeDef]
    ) -> _PageIterator[DescribeAcceleratorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference/paginator/DescribeAccelerators.html#ElasticInference.Paginator.DescribeAccelerators.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/paginators/#describeacceleratorspaginator)
        """
