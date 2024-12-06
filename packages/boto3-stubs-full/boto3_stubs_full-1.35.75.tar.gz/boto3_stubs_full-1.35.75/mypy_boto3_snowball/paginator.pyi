"""
Type annotations for snowball service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snowball/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_snowball.client import SnowballClient
    from mypy_boto3_snowball.paginator import (
        DescribeAddressesPaginator,
        ListClusterJobsPaginator,
        ListClustersPaginator,
        ListCompatibleImagesPaginator,
        ListJobsPaginator,
        ListLongTermPricingPaginator,
    )

    session = Session()
    client: SnowballClient = session.client("snowball")

    describe_addresses_paginator: DescribeAddressesPaginator = client.get_paginator("describe_addresses")
    list_cluster_jobs_paginator: ListClusterJobsPaginator = client.get_paginator("list_cluster_jobs")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_compatible_images_paginator: ListCompatibleImagesPaginator = client.get_paginator("list_compatible_images")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_long_term_pricing_paginator: ListLongTermPricingPaginator = client.get_paginator("list_long_term_pricing")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeAddressesRequestDescribeAddressesPaginateTypeDef,
    DescribeAddressesResultTypeDef,
    ListClusterJobsRequestListClusterJobsPaginateTypeDef,
    ListClusterJobsResultTypeDef,
    ListClustersRequestListClustersPaginateTypeDef,
    ListClustersResultTypeDef,
    ListCompatibleImagesRequestListCompatibleImagesPaginateTypeDef,
    ListCompatibleImagesResultTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResultTypeDef,
    ListLongTermPricingRequestListLongTermPricingPaginateTypeDef,
    ListLongTermPricingResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeAddressesPaginator",
    "ListClusterJobsPaginator",
    "ListClustersPaginator",
    "ListCompatibleImagesPaginator",
    "ListJobsPaginator",
    "ListLongTermPricingPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeAddressesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/DescribeAddresses.html#Snowball.Paginator.DescribeAddresses)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snowball/paginators/#describeaddressespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeAddressesRequestDescribeAddressesPaginateTypeDef]
    ) -> _PageIterator[DescribeAddressesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/DescribeAddresses.html#Snowball.Paginator.DescribeAddresses.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snowball/paginators/#describeaddressespaginator)
        """

class ListClusterJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListClusterJobs.html#Snowball.Paginator.ListClusterJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snowball/paginators/#listclusterjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListClusterJobsRequestListClusterJobsPaginateTypeDef]
    ) -> _PageIterator[ListClusterJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListClusterJobs.html#Snowball.Paginator.ListClusterJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snowball/paginators/#listclusterjobspaginator)
        """

class ListClustersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListClusters.html#Snowball.Paginator.ListClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snowball/paginators/#listclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListClustersRequestListClustersPaginateTypeDef]
    ) -> _PageIterator[ListClustersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListClusters.html#Snowball.Paginator.ListClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snowball/paginators/#listclusterspaginator)
        """

class ListCompatibleImagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListCompatibleImages.html#Snowball.Paginator.ListCompatibleImages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snowball/paginators/#listcompatibleimagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCompatibleImagesRequestListCompatibleImagesPaginateTypeDef]
    ) -> _PageIterator[ListCompatibleImagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListCompatibleImages.html#Snowball.Paginator.ListCompatibleImages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snowball/paginators/#listcompatibleimagespaginator)
        """

class ListJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListJobs.html#Snowball.Paginator.ListJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snowball/paginators/#listjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> _PageIterator[ListJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListJobs.html#Snowball.Paginator.ListJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snowball/paginators/#listjobspaginator)
        """

class ListLongTermPricingPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListLongTermPricing.html#Snowball.Paginator.ListLongTermPricing)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snowball/paginators/#listlongtermpricingpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLongTermPricingRequestListLongTermPricingPaginateTypeDef]
    ) -> _PageIterator[ListLongTermPricingResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListLongTermPricing.html#Snowball.Paginator.ListLongTermPricing.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snowball/paginators/#listlongtermpricingpaginator)
        """
