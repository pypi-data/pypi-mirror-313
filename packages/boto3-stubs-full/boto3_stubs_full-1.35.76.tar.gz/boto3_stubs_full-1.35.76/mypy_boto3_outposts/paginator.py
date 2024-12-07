"""
Type annotations for outposts service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_outposts.client import OutpostsClient
    from mypy_boto3_outposts.paginator import (
        GetOutpostInstanceTypesPaginator,
        GetOutpostSupportedInstanceTypesPaginator,
        ListAssetInstancesPaginator,
        ListAssetsPaginator,
        ListBlockingInstancesForCapacityTaskPaginator,
        ListCapacityTasksPaginator,
        ListCatalogItemsPaginator,
        ListOrdersPaginator,
        ListOutpostsPaginator,
        ListSitesPaginator,
    )

    session = Session()
    client: OutpostsClient = session.client("outposts")

    get_outpost_instance_types_paginator: GetOutpostInstanceTypesPaginator = client.get_paginator("get_outpost_instance_types")
    get_outpost_supported_instance_types_paginator: GetOutpostSupportedInstanceTypesPaginator = client.get_paginator("get_outpost_supported_instance_types")
    list_asset_instances_paginator: ListAssetInstancesPaginator = client.get_paginator("list_asset_instances")
    list_assets_paginator: ListAssetsPaginator = client.get_paginator("list_assets")
    list_blocking_instances_for_capacity_task_paginator: ListBlockingInstancesForCapacityTaskPaginator = client.get_paginator("list_blocking_instances_for_capacity_task")
    list_capacity_tasks_paginator: ListCapacityTasksPaginator = client.get_paginator("list_capacity_tasks")
    list_catalog_items_paginator: ListCatalogItemsPaginator = client.get_paginator("list_catalog_items")
    list_orders_paginator: ListOrdersPaginator = client.get_paginator("list_orders")
    list_outposts_paginator: ListOutpostsPaginator = client.get_paginator("list_outposts")
    list_sites_paginator: ListSitesPaginator = client.get_paginator("list_sites")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetOutpostInstanceTypesInputGetOutpostInstanceTypesPaginateTypeDef,
    GetOutpostInstanceTypesOutputTypeDef,
    GetOutpostSupportedInstanceTypesInputGetOutpostSupportedInstanceTypesPaginateTypeDef,
    GetOutpostSupportedInstanceTypesOutputTypeDef,
    ListAssetInstancesInputListAssetInstancesPaginateTypeDef,
    ListAssetInstancesOutputTypeDef,
    ListAssetsInputListAssetsPaginateTypeDef,
    ListAssetsOutputTypeDef,
    ListBlockingInstancesForCapacityTaskInputListBlockingInstancesForCapacityTaskPaginateTypeDef,
    ListBlockingInstancesForCapacityTaskOutputTypeDef,
    ListCapacityTasksInputListCapacityTasksPaginateTypeDef,
    ListCapacityTasksOutputTypeDef,
    ListCatalogItemsInputListCatalogItemsPaginateTypeDef,
    ListCatalogItemsOutputTypeDef,
    ListOrdersInputListOrdersPaginateTypeDef,
    ListOrdersOutputTypeDef,
    ListOutpostsInputListOutpostsPaginateTypeDef,
    ListOutpostsOutputTypeDef,
    ListSitesInputListSitesPaginateTypeDef,
    ListSitesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetOutpostInstanceTypesPaginator",
    "GetOutpostSupportedInstanceTypesPaginator",
    "ListAssetInstancesPaginator",
    "ListAssetsPaginator",
    "ListBlockingInstancesForCapacityTaskPaginator",
    "ListCapacityTasksPaginator",
    "ListCatalogItemsPaginator",
    "ListOrdersPaginator",
    "ListOutpostsPaginator",
    "ListSitesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetOutpostInstanceTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/GetOutpostInstanceTypes.html#Outposts.Paginator.GetOutpostInstanceTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#getoutpostinstancetypespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetOutpostInstanceTypesInputGetOutpostInstanceTypesPaginateTypeDef]
    ) -> _PageIterator[GetOutpostInstanceTypesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/GetOutpostInstanceTypes.html#Outposts.Paginator.GetOutpostInstanceTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#getoutpostinstancetypespaginator)
        """


class GetOutpostSupportedInstanceTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/GetOutpostSupportedInstanceTypes.html#Outposts.Paginator.GetOutpostSupportedInstanceTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#getoutpostsupportedinstancetypespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetOutpostSupportedInstanceTypesInputGetOutpostSupportedInstanceTypesPaginateTypeDef
        ],
    ) -> _PageIterator[GetOutpostSupportedInstanceTypesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/GetOutpostSupportedInstanceTypes.html#Outposts.Paginator.GetOutpostSupportedInstanceTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#getoutpostsupportedinstancetypespaginator)
        """


class ListAssetInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListAssetInstances.html#Outposts.Paginator.ListAssetInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#listassetinstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAssetInstancesInputListAssetInstancesPaginateTypeDef]
    ) -> _PageIterator[ListAssetInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListAssetInstances.html#Outposts.Paginator.ListAssetInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#listassetinstancespaginator)
        """


class ListAssetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListAssets.html#Outposts.Paginator.ListAssets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#listassetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAssetsInputListAssetsPaginateTypeDef]
    ) -> _PageIterator[ListAssetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListAssets.html#Outposts.Paginator.ListAssets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#listassetspaginator)
        """


class ListBlockingInstancesForCapacityTaskPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListBlockingInstancesForCapacityTask.html#Outposts.Paginator.ListBlockingInstancesForCapacityTask)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#listblockinginstancesforcapacitytaskpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListBlockingInstancesForCapacityTaskInputListBlockingInstancesForCapacityTaskPaginateTypeDef
        ],
    ) -> _PageIterator[ListBlockingInstancesForCapacityTaskOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListBlockingInstancesForCapacityTask.html#Outposts.Paginator.ListBlockingInstancesForCapacityTask.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#listblockinginstancesforcapacitytaskpaginator)
        """


class ListCapacityTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListCapacityTasks.html#Outposts.Paginator.ListCapacityTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#listcapacitytaskspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCapacityTasksInputListCapacityTasksPaginateTypeDef]
    ) -> _PageIterator[ListCapacityTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListCapacityTasks.html#Outposts.Paginator.ListCapacityTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#listcapacitytaskspaginator)
        """


class ListCatalogItemsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListCatalogItems.html#Outposts.Paginator.ListCatalogItems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#listcatalogitemspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCatalogItemsInputListCatalogItemsPaginateTypeDef]
    ) -> _PageIterator[ListCatalogItemsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListCatalogItems.html#Outposts.Paginator.ListCatalogItems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#listcatalogitemspaginator)
        """


class ListOrdersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListOrders.html#Outposts.Paginator.ListOrders)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#listorderspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOrdersInputListOrdersPaginateTypeDef]
    ) -> _PageIterator[ListOrdersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListOrders.html#Outposts.Paginator.ListOrders.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#listorderspaginator)
        """


class ListOutpostsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListOutposts.html#Outposts.Paginator.ListOutposts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#listoutpostspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOutpostsInputListOutpostsPaginateTypeDef]
    ) -> _PageIterator[ListOutpostsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListOutposts.html#Outposts.Paginator.ListOutposts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#listoutpostspaginator)
        """


class ListSitesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListSites.html#Outposts.Paginator.ListSites)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#listsitespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSitesInputListSitesPaginateTypeDef]
    ) -> _PageIterator[ListSitesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListSites.html#Outposts.Paginator.ListSites.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/paginators/#listsitespaginator)
        """
