"""
Type annotations for fsx service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_fsx.client import FSxClient
    from mypy_boto3_fsx.paginator import (
        DescribeBackupsPaginator,
        DescribeFileSystemsPaginator,
        DescribeStorageVirtualMachinesPaginator,
        DescribeVolumesPaginator,
        ListTagsForResourcePaginator,
    )

    session = Session()
    client: FSxClient = session.client("fsx")

    describe_backups_paginator: DescribeBackupsPaginator = client.get_paginator("describe_backups")
    describe_file_systems_paginator: DescribeFileSystemsPaginator = client.get_paginator("describe_file_systems")
    describe_storage_virtual_machines_paginator: DescribeStorageVirtualMachinesPaginator = client.get_paginator("describe_storage_virtual_machines")
    describe_volumes_paginator: DescribeVolumesPaginator = client.get_paginator("describe_volumes")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeBackupsRequestDescribeBackupsPaginateTypeDef,
    DescribeBackupsResponsePaginatorTypeDef,
    DescribeFileSystemsRequestDescribeFileSystemsPaginateTypeDef,
    DescribeFileSystemsResponsePaginatorTypeDef,
    DescribeStorageVirtualMachinesRequestDescribeStorageVirtualMachinesPaginateTypeDef,
    DescribeStorageVirtualMachinesResponseTypeDef,
    DescribeVolumesRequestDescribeVolumesPaginateTypeDef,
    DescribeVolumesResponsePaginatorTypeDef,
    ListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeBackupsPaginator",
    "DescribeFileSystemsPaginator",
    "DescribeStorageVirtualMachinesPaginator",
    "DescribeVolumesPaginator",
    "ListTagsForResourcePaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeBackupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeBackups.html#FSx.Paginator.DescribeBackups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describebackupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeBackupsRequestDescribeBackupsPaginateTypeDef]
    ) -> _PageIterator[DescribeBackupsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeBackups.html#FSx.Paginator.DescribeBackups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describebackupspaginator)
        """

class DescribeFileSystemsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeFileSystems.html#FSx.Paginator.DescribeFileSystems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describefilesystemspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeFileSystemsRequestDescribeFileSystemsPaginateTypeDef]
    ) -> _PageIterator[DescribeFileSystemsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeFileSystems.html#FSx.Paginator.DescribeFileSystems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describefilesystemspaginator)
        """

class DescribeStorageVirtualMachinesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeStorageVirtualMachines.html#FSx.Paginator.DescribeStorageVirtualMachines)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describestoragevirtualmachinespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeStorageVirtualMachinesRequestDescribeStorageVirtualMachinesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeStorageVirtualMachinesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeStorageVirtualMachines.html#FSx.Paginator.DescribeStorageVirtualMachines.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describestoragevirtualmachinespaginator)
        """

class DescribeVolumesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeVolumes.html#FSx.Paginator.DescribeVolumes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describevolumespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeVolumesRequestDescribeVolumesPaginateTypeDef]
    ) -> _PageIterator[DescribeVolumesResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeVolumes.html#FSx.Paginator.DescribeVolumes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describevolumespaginator)
        """

class ListTagsForResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/ListTagsForResource.html#FSx.Paginator.ListTagsForResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#listtagsforresourcepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceRequestListTagsForResourcePaginateTypeDef]
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/ListTagsForResource.html#FSx.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#listtagsforresourcepaginator)
        """
