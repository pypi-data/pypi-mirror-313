"""
Type annotations for ecr-public service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ecr_public.client import ECRPublicClient
    from mypy_boto3_ecr_public.paginator import (
        DescribeImageTagsPaginator,
        DescribeImagesPaginator,
        DescribeRegistriesPaginator,
        DescribeRepositoriesPaginator,
    )

    session = Session()
    client: ECRPublicClient = session.client("ecr-public")

    describe_image_tags_paginator: DescribeImageTagsPaginator = client.get_paginator("describe_image_tags")
    describe_images_paginator: DescribeImagesPaginator = client.get_paginator("describe_images")
    describe_registries_paginator: DescribeRegistriesPaginator = client.get_paginator("describe_registries")
    describe_repositories_paginator: DescribeRepositoriesPaginator = client.get_paginator("describe_repositories")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeImagesRequestDescribeImagesPaginateTypeDef,
    DescribeImagesResponseTypeDef,
    DescribeImageTagsRequestDescribeImageTagsPaginateTypeDef,
    DescribeImageTagsResponseTypeDef,
    DescribeRegistriesRequestDescribeRegistriesPaginateTypeDef,
    DescribeRegistriesResponseTypeDef,
    DescribeRepositoriesRequestDescribeRepositoriesPaginateTypeDef,
    DescribeRepositoriesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeImageTagsPaginator",
    "DescribeImagesPaginator",
    "DescribeRegistriesPaginator",
    "DescribeRepositoriesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeImageTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/paginator/DescribeImageTags.html#ECRPublic.Paginator.DescribeImageTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/paginators/#describeimagetagspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeImageTagsRequestDescribeImageTagsPaginateTypeDef]
    ) -> _PageIterator[DescribeImageTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/paginator/DescribeImageTags.html#ECRPublic.Paginator.DescribeImageTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/paginators/#describeimagetagspaginator)
        """


class DescribeImagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/paginator/DescribeImages.html#ECRPublic.Paginator.DescribeImages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/paginators/#describeimagespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeImagesRequestDescribeImagesPaginateTypeDef]
    ) -> _PageIterator[DescribeImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/paginator/DescribeImages.html#ECRPublic.Paginator.DescribeImages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/paginators/#describeimagespaginator)
        """


class DescribeRegistriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/paginator/DescribeRegistries.html#ECRPublic.Paginator.DescribeRegistries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/paginators/#describeregistriespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeRegistriesRequestDescribeRegistriesPaginateTypeDef]
    ) -> _PageIterator[DescribeRegistriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/paginator/DescribeRegistries.html#ECRPublic.Paginator.DescribeRegistries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/paginators/#describeregistriespaginator)
        """


class DescribeRepositoriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/paginator/DescribeRepositories.html#ECRPublic.Paginator.DescribeRepositories)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/paginators/#describerepositoriespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeRepositoriesRequestDescribeRepositoriesPaginateTypeDef]
    ) -> _PageIterator[DescribeRepositoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/paginator/DescribeRepositories.html#ECRPublic.Paginator.DescribeRepositories.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/paginators/#describerepositoriespaginator)
        """
