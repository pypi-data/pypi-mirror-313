"""
Type annotations for cloudhsmv2 service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsmv2/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_cloudhsmv2.client import CloudHSMV2Client
    from mypy_boto3_cloudhsmv2.paginator import (
        DescribeBackupsPaginator,
        DescribeClustersPaginator,
        ListTagsPaginator,
    )

    session = Session()
    client: CloudHSMV2Client = session.client("cloudhsmv2")

    describe_backups_paginator: DescribeBackupsPaginator = client.get_paginator("describe_backups")
    describe_clusters_paginator: DescribeClustersPaginator = client.get_paginator("describe_clusters")
    list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeBackupsRequestDescribeBackupsPaginateTypeDef,
    DescribeBackupsResponseTypeDef,
    DescribeClustersRequestDescribeClustersPaginateTypeDef,
    DescribeClustersResponseTypeDef,
    ListTagsRequestListTagsPaginateTypeDef,
    ListTagsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("DescribeBackupsPaginator", "DescribeClustersPaginator", "ListTagsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeBackupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/DescribeBackups.html#CloudHSMV2.Paginator.DescribeBackups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsmv2/paginators/#describebackupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeBackupsRequestDescribeBackupsPaginateTypeDef]
    ) -> _PageIterator[DescribeBackupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/DescribeBackups.html#CloudHSMV2.Paginator.DescribeBackups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsmv2/paginators/#describebackupspaginator)
        """

class DescribeClustersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/DescribeClusters.html#CloudHSMV2.Paginator.DescribeClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsmv2/paginators/#describeclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeClustersRequestDescribeClustersPaginateTypeDef]
    ) -> _PageIterator[DescribeClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/DescribeClusters.html#CloudHSMV2.Paginator.DescribeClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsmv2/paginators/#describeclusterspaginator)
        """

class ListTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/ListTags.html#CloudHSMV2.Paginator.ListTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsmv2/paginators/#listtagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsRequestListTagsPaginateTypeDef]
    ) -> _PageIterator[ListTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/ListTags.html#CloudHSMV2.Paginator.ListTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsmv2/paginators/#listtagspaginator)
        """
