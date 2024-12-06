"""
Type annotations for signer service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_signer.client import SignerClient
    from mypy_boto3_signer.paginator import (
        ListSigningJobsPaginator,
        ListSigningPlatformsPaginator,
        ListSigningProfilesPaginator,
    )

    session = Session()
    client: SignerClient = session.client("signer")

    list_signing_jobs_paginator: ListSigningJobsPaginator = client.get_paginator("list_signing_jobs")
    list_signing_platforms_paginator: ListSigningPlatformsPaginator = client.get_paginator("list_signing_platforms")
    list_signing_profiles_paginator: ListSigningProfilesPaginator = client.get_paginator("list_signing_profiles")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListSigningJobsRequestListSigningJobsPaginateTypeDef,
    ListSigningJobsResponseTypeDef,
    ListSigningPlatformsRequestListSigningPlatformsPaginateTypeDef,
    ListSigningPlatformsResponseTypeDef,
    ListSigningProfilesRequestListSigningProfilesPaginateTypeDef,
    ListSigningProfilesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListSigningJobsPaginator",
    "ListSigningPlatformsPaginator",
    "ListSigningProfilesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListSigningJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningJobs.html#Signer.Paginator.ListSigningJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/paginators/#listsigningjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSigningJobsRequestListSigningJobsPaginateTypeDef]
    ) -> _PageIterator[ListSigningJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningJobs.html#Signer.Paginator.ListSigningJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/paginators/#listsigningjobspaginator)
        """

class ListSigningPlatformsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningPlatforms.html#Signer.Paginator.ListSigningPlatforms)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/paginators/#listsigningplatformspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSigningPlatformsRequestListSigningPlatformsPaginateTypeDef]
    ) -> _PageIterator[ListSigningPlatformsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningPlatforms.html#Signer.Paginator.ListSigningPlatforms.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/paginators/#listsigningplatformspaginator)
        """

class ListSigningProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningProfiles.html#Signer.Paginator.ListSigningProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/paginators/#listsigningprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSigningProfilesRequestListSigningProfilesPaginateTypeDef]
    ) -> _PageIterator[ListSigningProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningProfiles.html#Signer.Paginator.ListSigningProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/paginators/#listsigningprofilespaginator)
        """
