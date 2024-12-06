"""
Type annotations for glacier service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_glacier.client import GlacierClient
    from mypy_boto3_glacier.paginator import (
        ListJobsPaginator,
        ListMultipartUploadsPaginator,
        ListPartsPaginator,
        ListVaultsPaginator,
    )

    session = Session()
    client: GlacierClient = session.client("glacier")

    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_multipart_uploads_paginator: ListMultipartUploadsPaginator = client.get_paginator("list_multipart_uploads")
    list_parts_paginator: ListPartsPaginator = client.get_paginator("list_parts")
    list_vaults_paginator: ListVaultsPaginator = client.get_paginator("list_vaults")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListJobsInputListJobsPaginateTypeDef,
    ListJobsOutputTypeDef,
    ListMultipartUploadsInputListMultipartUploadsPaginateTypeDef,
    ListMultipartUploadsOutputTypeDef,
    ListPartsInputListPartsPaginateTypeDef,
    ListPartsOutputTypeDef,
    ListVaultsInputListVaultsPaginateTypeDef,
    ListVaultsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListJobsPaginator",
    "ListMultipartUploadsPaginator",
    "ListPartsPaginator",
    "ListVaultsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListJobs.html#Glacier.Paginator.ListJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/#listjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsInputListJobsPaginateTypeDef]
    ) -> _PageIterator[ListJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListJobs.html#Glacier.Paginator.ListJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/#listjobspaginator)
        """

class ListMultipartUploadsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListMultipartUploads.html#Glacier.Paginator.ListMultipartUploads)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/#listmultipartuploadspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMultipartUploadsInputListMultipartUploadsPaginateTypeDef]
    ) -> _PageIterator[ListMultipartUploadsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListMultipartUploads.html#Glacier.Paginator.ListMultipartUploads.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/#listmultipartuploadspaginator)
        """

class ListPartsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListParts.html#Glacier.Paginator.ListParts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/#listpartspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPartsInputListPartsPaginateTypeDef]
    ) -> _PageIterator[ListPartsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListParts.html#Glacier.Paginator.ListParts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/#listpartspaginator)
        """

class ListVaultsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListVaults.html#Glacier.Paginator.ListVaults)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/#listvaultspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListVaultsInputListVaultsPaginateTypeDef]
    ) -> _PageIterator[ListVaultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListVaults.html#Glacier.Paginator.ListVaults.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/#listvaultspaginator)
        """
