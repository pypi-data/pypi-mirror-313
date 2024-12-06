"""
Type annotations for schemas service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_schemas.client import SchemasClient
    from mypy_boto3_schemas.paginator import (
        ListDiscoverersPaginator,
        ListRegistriesPaginator,
        ListSchemaVersionsPaginator,
        ListSchemasPaginator,
        SearchSchemasPaginator,
    )

    session = Session()
    client: SchemasClient = session.client("schemas")

    list_discoverers_paginator: ListDiscoverersPaginator = client.get_paginator("list_discoverers")
    list_registries_paginator: ListRegistriesPaginator = client.get_paginator("list_registries")
    list_schema_versions_paginator: ListSchemaVersionsPaginator = client.get_paginator("list_schema_versions")
    list_schemas_paginator: ListSchemasPaginator = client.get_paginator("list_schemas")
    search_schemas_paginator: SearchSchemasPaginator = client.get_paginator("search_schemas")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDiscoverersRequestListDiscoverersPaginateTypeDef,
    ListDiscoverersResponseTypeDef,
    ListRegistriesRequestListRegistriesPaginateTypeDef,
    ListRegistriesResponseTypeDef,
    ListSchemasRequestListSchemasPaginateTypeDef,
    ListSchemasResponseTypeDef,
    ListSchemaVersionsRequestListSchemaVersionsPaginateTypeDef,
    ListSchemaVersionsResponseTypeDef,
    SearchSchemasRequestSearchSchemasPaginateTypeDef,
    SearchSchemasResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDiscoverersPaginator",
    "ListRegistriesPaginator",
    "ListSchemaVersionsPaginator",
    "ListSchemasPaginator",
    "SearchSchemasPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDiscoverersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/ListDiscoverers.html#Schemas.Paginator.ListDiscoverers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators/#listdiscovererspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDiscoverersRequestListDiscoverersPaginateTypeDef]
    ) -> _PageIterator[ListDiscoverersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/ListDiscoverers.html#Schemas.Paginator.ListDiscoverers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators/#listdiscovererspaginator)
        """

class ListRegistriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/ListRegistries.html#Schemas.Paginator.ListRegistries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators/#listregistriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRegistriesRequestListRegistriesPaginateTypeDef]
    ) -> _PageIterator[ListRegistriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/ListRegistries.html#Schemas.Paginator.ListRegistries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators/#listregistriespaginator)
        """

class ListSchemaVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/ListSchemaVersions.html#Schemas.Paginator.ListSchemaVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators/#listschemaversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSchemaVersionsRequestListSchemaVersionsPaginateTypeDef]
    ) -> _PageIterator[ListSchemaVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/ListSchemaVersions.html#Schemas.Paginator.ListSchemaVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators/#listschemaversionspaginator)
        """

class ListSchemasPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/ListSchemas.html#Schemas.Paginator.ListSchemas)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators/#listschemaspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSchemasRequestListSchemasPaginateTypeDef]
    ) -> _PageIterator[ListSchemasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/ListSchemas.html#Schemas.Paginator.ListSchemas.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators/#listschemaspaginator)
        """

class SearchSchemasPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/SearchSchemas.html#Schemas.Paginator.SearchSchemas)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators/#searchschemaspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchSchemasRequestSearchSchemasPaginateTypeDef]
    ) -> _PageIterator[SearchSchemasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/SearchSchemas.html#Schemas.Paginator.SearchSchemas.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators/#searchschemaspaginator)
        """
