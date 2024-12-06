"""
Type annotations for kinesisanalyticsv2 service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_kinesisanalyticsv2.client import KinesisAnalyticsV2Client
    from mypy_boto3_kinesisanalyticsv2.paginator import (
        ListApplicationOperationsPaginator,
        ListApplicationSnapshotsPaginator,
        ListApplicationVersionsPaginator,
        ListApplicationsPaginator,
    )

    session = Session()
    client: KinesisAnalyticsV2Client = session.client("kinesisanalyticsv2")

    list_application_operations_paginator: ListApplicationOperationsPaginator = client.get_paginator("list_application_operations")
    list_application_snapshots_paginator: ListApplicationSnapshotsPaginator = client.get_paginator("list_application_snapshots")
    list_application_versions_paginator: ListApplicationVersionsPaginator = client.get_paginator("list_application_versions")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListApplicationOperationsRequestListApplicationOperationsPaginateTypeDef,
    ListApplicationOperationsResponseTypeDef,
    ListApplicationSnapshotsRequestListApplicationSnapshotsPaginateTypeDef,
    ListApplicationSnapshotsResponseTypeDef,
    ListApplicationsRequestListApplicationsPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef,
    ListApplicationVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListApplicationOperationsPaginator",
    "ListApplicationSnapshotsPaginator",
    "ListApplicationVersionsPaginator",
    "ListApplicationsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListApplicationOperationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/paginator/ListApplicationOperations.html#KinesisAnalyticsV2.Paginator.ListApplicationOperations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/paginators/#listapplicationoperationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListApplicationOperationsRequestListApplicationOperationsPaginateTypeDef],
    ) -> _PageIterator[ListApplicationOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/paginator/ListApplicationOperations.html#KinesisAnalyticsV2.Paginator.ListApplicationOperations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/paginators/#listapplicationoperationspaginator)
        """

class ListApplicationSnapshotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/paginator/ListApplicationSnapshots.html#KinesisAnalyticsV2.Paginator.ListApplicationSnapshots)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/paginators/#listapplicationsnapshotspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListApplicationSnapshotsRequestListApplicationSnapshotsPaginateTypeDef],
    ) -> _PageIterator[ListApplicationSnapshotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/paginator/ListApplicationSnapshots.html#KinesisAnalyticsV2.Paginator.ListApplicationSnapshots.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/paginators/#listapplicationsnapshotspaginator)
        """

class ListApplicationVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/paginator/ListApplicationVersions.html#KinesisAnalyticsV2.Paginator.ListApplicationVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/paginators/#listapplicationversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef]
    ) -> _PageIterator[ListApplicationVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/paginator/ListApplicationVersions.html#KinesisAnalyticsV2.Paginator.ListApplicationVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/paginators/#listapplicationversionspaginator)
        """

class ListApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/paginator/ListApplications.html#KinesisAnalyticsV2.Paginator.ListApplications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/paginators/#listapplicationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListApplicationsRequestListApplicationsPaginateTypeDef]
    ) -> _PageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/paginator/ListApplications.html#KinesisAnalyticsV2.Paginator.ListApplications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/paginators/#listapplicationspaginator)
        """
