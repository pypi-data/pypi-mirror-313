"""
Type annotations for s3outposts service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_s3outposts.client import S3OutpostsClient
    from mypy_boto3_s3outposts.paginator import (
        ListEndpointsPaginator,
        ListOutpostsWithS3Paginator,
        ListSharedEndpointsPaginator,
    )

    session = Session()
    client: S3OutpostsClient = session.client("s3outposts")

    list_endpoints_paginator: ListEndpointsPaginator = client.get_paginator("list_endpoints")
    list_outposts_with_s3_paginator: ListOutpostsWithS3Paginator = client.get_paginator("list_outposts_with_s3")
    list_shared_endpoints_paginator: ListSharedEndpointsPaginator = client.get_paginator("list_shared_endpoints")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListEndpointsRequestListEndpointsPaginateTypeDef,
    ListEndpointsResultTypeDef,
    ListOutpostsWithS3RequestListOutpostsWithS3PaginateTypeDef,
    ListOutpostsWithS3ResultTypeDef,
    ListSharedEndpointsRequestListSharedEndpointsPaginateTypeDef,
    ListSharedEndpointsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListEndpointsPaginator", "ListOutpostsWithS3Paginator", "ListSharedEndpointsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListEndpoints.html#S3Outposts.Paginator.ListEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/paginators/#listendpointspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEndpointsRequestListEndpointsPaginateTypeDef]
    ) -> _PageIterator[ListEndpointsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListEndpoints.html#S3Outposts.Paginator.ListEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/paginators/#listendpointspaginator)
        """

class ListOutpostsWithS3Paginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListOutpostsWithS3.html#S3Outposts.Paginator.ListOutpostsWithS3)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/paginators/#listoutpostswiths3paginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListOutpostsWithS3RequestListOutpostsWithS3PaginateTypeDef]
    ) -> _PageIterator[ListOutpostsWithS3ResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListOutpostsWithS3.html#S3Outposts.Paginator.ListOutpostsWithS3.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/paginators/#listoutpostswiths3paginator)
        """

class ListSharedEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListSharedEndpoints.html#S3Outposts.Paginator.ListSharedEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/paginators/#listsharedendpointspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSharedEndpointsRequestListSharedEndpointsPaginateTypeDef]
    ) -> _PageIterator[ListSharedEndpointsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListSharedEndpoints.html#S3Outposts.Paginator.ListSharedEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/paginators/#listsharedendpointspaginator)
        """
