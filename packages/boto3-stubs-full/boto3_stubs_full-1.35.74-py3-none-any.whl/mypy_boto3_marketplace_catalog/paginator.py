"""
Type annotations for marketplace-catalog service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_catalog/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_marketplace_catalog.client import MarketplaceCatalogClient
    from mypy_boto3_marketplace_catalog.paginator import (
        ListChangeSetsPaginator,
        ListEntitiesPaginator,
    )

    session = Session()
    client: MarketplaceCatalogClient = session.client("marketplace-catalog")

    list_change_sets_paginator: ListChangeSetsPaginator = client.get_paginator("list_change_sets")
    list_entities_paginator: ListEntitiesPaginator = client.get_paginator("list_entities")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListChangeSetsRequestListChangeSetsPaginateTypeDef,
    ListChangeSetsResponseTypeDef,
    ListEntitiesRequestListEntitiesPaginateTypeDef,
    ListEntitiesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListChangeSetsPaginator", "ListEntitiesPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListChangeSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-catalog/paginator/ListChangeSets.html#MarketplaceCatalog.Paginator.ListChangeSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_catalog/paginators/#listchangesetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListChangeSetsRequestListChangeSetsPaginateTypeDef]
    ) -> _PageIterator[ListChangeSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-catalog/paginator/ListChangeSets.html#MarketplaceCatalog.Paginator.ListChangeSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_catalog/paginators/#listchangesetspaginator)
        """


class ListEntitiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-catalog/paginator/ListEntities.html#MarketplaceCatalog.Paginator.ListEntities)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_catalog/paginators/#listentitiespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEntitiesRequestListEntitiesPaginateTypeDef]
    ) -> _PageIterator[ListEntitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-catalog/paginator/ListEntities.html#MarketplaceCatalog.Paginator.ListEntities.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_catalog/paginators/#listentitiespaginator)
        """
