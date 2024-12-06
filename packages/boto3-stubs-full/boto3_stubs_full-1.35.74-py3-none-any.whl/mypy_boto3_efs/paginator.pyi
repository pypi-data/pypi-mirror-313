"""
Type annotations for efs service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_efs.client import EFSClient
    from mypy_boto3_efs.paginator import (
        DescribeAccessPointsPaginator,
        DescribeFileSystemsPaginator,
        DescribeMountTargetsPaginator,
        DescribeReplicationConfigurationsPaginator,
        DescribeTagsPaginator,
    )

    session = Session()
    client: EFSClient = session.client("efs")

    describe_access_points_paginator: DescribeAccessPointsPaginator = client.get_paginator("describe_access_points")
    describe_file_systems_paginator: DescribeFileSystemsPaginator = client.get_paginator("describe_file_systems")
    describe_mount_targets_paginator: DescribeMountTargetsPaginator = client.get_paginator("describe_mount_targets")
    describe_replication_configurations_paginator: DescribeReplicationConfigurationsPaginator = client.get_paginator("describe_replication_configurations")
    describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeAccessPointsRequestDescribeAccessPointsPaginateTypeDef,
    DescribeAccessPointsResponseTypeDef,
    DescribeFileSystemsRequestDescribeFileSystemsPaginateTypeDef,
    DescribeFileSystemsResponseTypeDef,
    DescribeMountTargetsRequestDescribeMountTargetsPaginateTypeDef,
    DescribeMountTargetsResponseTypeDef,
    DescribeReplicationConfigurationsRequestDescribeReplicationConfigurationsPaginateTypeDef,
    DescribeReplicationConfigurationsResponseTypeDef,
    DescribeTagsRequestDescribeTagsPaginateTypeDef,
    DescribeTagsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeAccessPointsPaginator",
    "DescribeFileSystemsPaginator",
    "DescribeMountTargetsPaginator",
    "DescribeReplicationConfigurationsPaginator",
    "DescribeTagsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeAccessPointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeAccessPoints.html#EFS.Paginator.DescribeAccessPoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/paginators/#describeaccesspointspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeAccessPointsRequestDescribeAccessPointsPaginateTypeDef]
    ) -> _PageIterator[DescribeAccessPointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeAccessPoints.html#EFS.Paginator.DescribeAccessPoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/paginators/#describeaccesspointspaginator)
        """

class DescribeFileSystemsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeFileSystems.html#EFS.Paginator.DescribeFileSystems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/paginators/#describefilesystemspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeFileSystemsRequestDescribeFileSystemsPaginateTypeDef]
    ) -> _PageIterator[DescribeFileSystemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeFileSystems.html#EFS.Paginator.DescribeFileSystems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/paginators/#describefilesystemspaginator)
        """

class DescribeMountTargetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeMountTargets.html#EFS.Paginator.DescribeMountTargets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/paginators/#describemounttargetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeMountTargetsRequestDescribeMountTargetsPaginateTypeDef]
    ) -> _PageIterator[DescribeMountTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeMountTargets.html#EFS.Paginator.DescribeMountTargets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/paginators/#describemounttargetspaginator)
        """

class DescribeReplicationConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeReplicationConfigurations.html#EFS.Paginator.DescribeReplicationConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/paginators/#describereplicationconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReplicationConfigurationsRequestDescribeReplicationConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeReplicationConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeReplicationConfigurations.html#EFS.Paginator.DescribeReplicationConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/paginators/#describereplicationconfigurationspaginator)
        """

class DescribeTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeTags.html#EFS.Paginator.DescribeTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/paginators/#describetagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeTagsRequestDescribeTagsPaginateTypeDef]
    ) -> _PageIterator[DescribeTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeTags.html#EFS.Paginator.DescribeTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/paginators/#describetagspaginator)
        """
