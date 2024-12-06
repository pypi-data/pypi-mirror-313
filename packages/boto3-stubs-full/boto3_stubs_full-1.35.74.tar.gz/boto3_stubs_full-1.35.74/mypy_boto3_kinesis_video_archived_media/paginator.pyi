"""
Type annotations for kinesis-video-archived-media service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_kinesis_video_archived_media.client import KinesisVideoArchivedMediaClient
    from mypy_boto3_kinesis_video_archived_media.paginator import (
        GetImagesPaginator,
        ListFragmentsPaginator,
    )

    session = Session()
    client: KinesisVideoArchivedMediaClient = session.client("kinesis-video-archived-media")

    get_images_paginator: GetImagesPaginator = client.get_paginator("get_images")
    list_fragments_paginator: ListFragmentsPaginator = client.get_paginator("list_fragments")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetImagesInputGetImagesPaginateTypeDef,
    GetImagesOutputTypeDef,
    ListFragmentsInputListFragmentsPaginateTypeDef,
    ListFragmentsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("GetImagesPaginator", "ListFragmentsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetImagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/paginator/GetImages.html#KinesisVideoArchivedMedia.Paginator.GetImages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/paginators/#getimagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetImagesInputGetImagesPaginateTypeDef]
    ) -> _PageIterator[GetImagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/paginator/GetImages.html#KinesisVideoArchivedMedia.Paginator.GetImages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/paginators/#getimagespaginator)
        """

class ListFragmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/paginator/ListFragments.html#KinesisVideoArchivedMedia.Paginator.ListFragments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/paginators/#listfragmentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFragmentsInputListFragmentsPaginateTypeDef]
    ) -> _PageIterator[ListFragmentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/paginator/ListFragments.html#KinesisVideoArchivedMedia.Paginator.ListFragments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/paginators/#listfragmentspaginator)
        """
