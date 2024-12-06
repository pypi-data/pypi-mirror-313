"""
Type annotations for es service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_es.client import ElasticsearchServiceClient
    from mypy_boto3_es.paginator import (
        DescribeReservedElasticsearchInstanceOfferingsPaginator,
        DescribeReservedElasticsearchInstancesPaginator,
        GetUpgradeHistoryPaginator,
        ListElasticsearchInstanceTypesPaginator,
        ListElasticsearchVersionsPaginator,
    )

    session = Session()
    client: ElasticsearchServiceClient = session.client("es")

    describe_reserved_elasticsearch_instance_offerings_paginator: DescribeReservedElasticsearchInstanceOfferingsPaginator = client.get_paginator("describe_reserved_elasticsearch_instance_offerings")
    describe_reserved_elasticsearch_instances_paginator: DescribeReservedElasticsearchInstancesPaginator = client.get_paginator("describe_reserved_elasticsearch_instances")
    get_upgrade_history_paginator: GetUpgradeHistoryPaginator = client.get_paginator("get_upgrade_history")
    list_elasticsearch_instance_types_paginator: ListElasticsearchInstanceTypesPaginator = client.get_paginator("list_elasticsearch_instance_types")
    list_elasticsearch_versions_paginator: ListElasticsearchVersionsPaginator = client.get_paginator("list_elasticsearch_versions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeReservedElasticsearchInstanceOfferingsRequestDescribeReservedElasticsearchInstanceOfferingsPaginateTypeDef,
    DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef,
    DescribeReservedElasticsearchInstancesRequestDescribeReservedElasticsearchInstancesPaginateTypeDef,
    DescribeReservedElasticsearchInstancesResponseTypeDef,
    GetUpgradeHistoryRequestGetUpgradeHistoryPaginateTypeDef,
    GetUpgradeHistoryResponseTypeDef,
    ListElasticsearchInstanceTypesRequestListElasticsearchInstanceTypesPaginateTypeDef,
    ListElasticsearchInstanceTypesResponseTypeDef,
    ListElasticsearchVersionsRequestListElasticsearchVersionsPaginateTypeDef,
    ListElasticsearchVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeReservedElasticsearchInstanceOfferingsPaginator",
    "DescribeReservedElasticsearchInstancesPaginator",
    "GetUpgradeHistoryPaginator",
    "ListElasticsearchInstanceTypesPaginator",
    "ListElasticsearchVersionsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeReservedElasticsearchInstanceOfferingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/DescribeReservedElasticsearchInstanceOfferings.html#ElasticsearchService.Paginator.DescribeReservedElasticsearchInstanceOfferings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/paginators/#describereservedelasticsearchinstanceofferingspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReservedElasticsearchInstanceOfferingsRequestDescribeReservedElasticsearchInstanceOfferingsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/DescribeReservedElasticsearchInstanceOfferings.html#ElasticsearchService.Paginator.DescribeReservedElasticsearchInstanceOfferings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/paginators/#describereservedelasticsearchinstanceofferingspaginator)
        """

class DescribeReservedElasticsearchInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/DescribeReservedElasticsearchInstances.html#ElasticsearchService.Paginator.DescribeReservedElasticsearchInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/paginators/#describereservedelasticsearchinstancespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReservedElasticsearchInstancesRequestDescribeReservedElasticsearchInstancesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeReservedElasticsearchInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/DescribeReservedElasticsearchInstances.html#ElasticsearchService.Paginator.DescribeReservedElasticsearchInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/paginators/#describereservedelasticsearchinstancespaginator)
        """

class GetUpgradeHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/GetUpgradeHistory.html#ElasticsearchService.Paginator.GetUpgradeHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/paginators/#getupgradehistorypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetUpgradeHistoryRequestGetUpgradeHistoryPaginateTypeDef]
    ) -> _PageIterator[GetUpgradeHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/GetUpgradeHistory.html#ElasticsearchService.Paginator.GetUpgradeHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/paginators/#getupgradehistorypaginator)
        """

class ListElasticsearchInstanceTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/ListElasticsearchInstanceTypes.html#ElasticsearchService.Paginator.ListElasticsearchInstanceTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/paginators/#listelasticsearchinstancetypespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListElasticsearchInstanceTypesRequestListElasticsearchInstanceTypesPaginateTypeDef
        ],
    ) -> _PageIterator[ListElasticsearchInstanceTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/ListElasticsearchInstanceTypes.html#ElasticsearchService.Paginator.ListElasticsearchInstanceTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/paginators/#listelasticsearchinstancetypespaginator)
        """

class ListElasticsearchVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/ListElasticsearchVersions.html#ElasticsearchService.Paginator.ListElasticsearchVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/paginators/#listelasticsearchversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListElasticsearchVersionsRequestListElasticsearchVersionsPaginateTypeDef],
    ) -> _PageIterator[ListElasticsearchVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/ListElasticsearchVersions.html#ElasticsearchService.Paginator.ListElasticsearchVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/paginators/#listelasticsearchversionspaginator)
        """
