"""
Type annotations for cloudcontrol service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_cloudcontrol.client import CloudControlApiClient
    from mypy_boto3_cloudcontrol.paginator import (
        ListResourceRequestsPaginator,
        ListResourcesPaginator,
    )

    session = Session()
    client: CloudControlApiClient = session.client("cloudcontrol")

    list_resource_requests_paginator: ListResourceRequestsPaginator = client.get_paginator("list_resource_requests")
    list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListResourceRequestsInputListResourceRequestsPaginateTypeDef,
    ListResourceRequestsOutputTypeDef,
    ListResourcesInputListResourcesPaginateTypeDef,
    ListResourcesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListResourceRequestsPaginator", "ListResourcesPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListResourceRequestsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/paginator/ListResourceRequests.html#CloudControlApi.Paginator.ListResourceRequests)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/paginators/#listresourcerequestspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListResourceRequestsInputListResourceRequestsPaginateTypeDef]
    ) -> _PageIterator[ListResourceRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/paginator/ListResourceRequests.html#CloudControlApi.Paginator.ListResourceRequests.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/paginators/#listresourcerequestspaginator)
        """

class ListResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/paginator/ListResources.html#CloudControlApi.Paginator.ListResources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/paginators/#listresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListResourcesInputListResourcesPaginateTypeDef]
    ) -> _PageIterator[ListResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/paginator/ListResources.html#CloudControlApi.Paginator.ListResources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/paginators/#listresourcespaginator)
        """
