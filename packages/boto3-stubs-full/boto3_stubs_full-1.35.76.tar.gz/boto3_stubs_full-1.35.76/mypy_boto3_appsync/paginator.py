"""
Type annotations for appsync service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_appsync.client import AppSyncClient
    from mypy_boto3_appsync.paginator import (
        ListApiKeysPaginator,
        ListApisPaginator,
        ListChannelNamespacesPaginator,
        ListDataSourcesPaginator,
        ListDomainNamesPaginator,
        ListFunctionsPaginator,
        ListGraphqlApisPaginator,
        ListResolversByFunctionPaginator,
        ListResolversPaginator,
        ListSourceApiAssociationsPaginator,
        ListTypesByAssociationPaginator,
        ListTypesPaginator,
    )

    session = Session()
    client: AppSyncClient = session.client("appsync")

    list_api_keys_paginator: ListApiKeysPaginator = client.get_paginator("list_api_keys")
    list_apis_paginator: ListApisPaginator = client.get_paginator("list_apis")
    list_channel_namespaces_paginator: ListChannelNamespacesPaginator = client.get_paginator("list_channel_namespaces")
    list_data_sources_paginator: ListDataSourcesPaginator = client.get_paginator("list_data_sources")
    list_domain_names_paginator: ListDomainNamesPaginator = client.get_paginator("list_domain_names")
    list_functions_paginator: ListFunctionsPaginator = client.get_paginator("list_functions")
    list_graphql_apis_paginator: ListGraphqlApisPaginator = client.get_paginator("list_graphql_apis")
    list_resolvers_by_function_paginator: ListResolversByFunctionPaginator = client.get_paginator("list_resolvers_by_function")
    list_resolvers_paginator: ListResolversPaginator = client.get_paginator("list_resolvers")
    list_source_api_associations_paginator: ListSourceApiAssociationsPaginator = client.get_paginator("list_source_api_associations")
    list_types_by_association_paginator: ListTypesByAssociationPaginator = client.get_paginator("list_types_by_association")
    list_types_paginator: ListTypesPaginator = client.get_paginator("list_types")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListApiKeysRequestListApiKeysPaginateTypeDef,
    ListApiKeysResponseTypeDef,
    ListApisRequestListApisPaginateTypeDef,
    ListApisResponseTypeDef,
    ListChannelNamespacesRequestListChannelNamespacesPaginateTypeDef,
    ListChannelNamespacesResponseTypeDef,
    ListDataSourcesRequestListDataSourcesPaginateTypeDef,
    ListDataSourcesResponseTypeDef,
    ListDomainNamesRequestListDomainNamesPaginateTypeDef,
    ListDomainNamesResponseTypeDef,
    ListFunctionsRequestListFunctionsPaginateTypeDef,
    ListFunctionsResponseTypeDef,
    ListGraphqlApisRequestListGraphqlApisPaginateTypeDef,
    ListGraphqlApisResponseTypeDef,
    ListResolversByFunctionRequestListResolversByFunctionPaginateTypeDef,
    ListResolversByFunctionResponseTypeDef,
    ListResolversRequestListResolversPaginateTypeDef,
    ListResolversResponseTypeDef,
    ListSourceApiAssociationsRequestListSourceApiAssociationsPaginateTypeDef,
    ListSourceApiAssociationsResponseTypeDef,
    ListTypesByAssociationRequestListTypesByAssociationPaginateTypeDef,
    ListTypesByAssociationResponseTypeDef,
    ListTypesRequestListTypesPaginateTypeDef,
    ListTypesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListApiKeysPaginator",
    "ListApisPaginator",
    "ListChannelNamespacesPaginator",
    "ListDataSourcesPaginator",
    "ListDomainNamesPaginator",
    "ListFunctionsPaginator",
    "ListGraphqlApisPaginator",
    "ListResolversByFunctionPaginator",
    "ListResolversPaginator",
    "ListSourceApiAssociationsPaginator",
    "ListTypesByAssociationPaginator",
    "ListTypesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListApiKeysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListApiKeys.html#AppSync.Paginator.ListApiKeys)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listapikeyspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListApiKeysRequestListApiKeysPaginateTypeDef]
    ) -> _PageIterator[ListApiKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListApiKeys.html#AppSync.Paginator.ListApiKeys.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listapikeyspaginator)
        """


class ListApisPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListApis.html#AppSync.Paginator.ListApis)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listapispaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListApisRequestListApisPaginateTypeDef]
    ) -> _PageIterator[ListApisResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListApis.html#AppSync.Paginator.ListApis.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listapispaginator)
        """


class ListChannelNamespacesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListChannelNamespaces.html#AppSync.Paginator.ListChannelNamespaces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listchannelnamespacespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListChannelNamespacesRequestListChannelNamespacesPaginateTypeDef]
    ) -> _PageIterator[ListChannelNamespacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListChannelNamespaces.html#AppSync.Paginator.ListChannelNamespaces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listchannelnamespacespaginator)
        """


class ListDataSourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListDataSources.html#AppSync.Paginator.ListDataSources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listdatasourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDataSourcesRequestListDataSourcesPaginateTypeDef]
    ) -> _PageIterator[ListDataSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListDataSources.html#AppSync.Paginator.ListDataSources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listdatasourcespaginator)
        """


class ListDomainNamesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListDomainNames.html#AppSync.Paginator.ListDomainNames)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listdomainnamespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDomainNamesRequestListDomainNamesPaginateTypeDef]
    ) -> _PageIterator[ListDomainNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListDomainNames.html#AppSync.Paginator.ListDomainNames.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listdomainnamespaginator)
        """


class ListFunctionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListFunctions.html#AppSync.Paginator.ListFunctions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listfunctionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFunctionsRequestListFunctionsPaginateTypeDef]
    ) -> _PageIterator[ListFunctionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListFunctions.html#AppSync.Paginator.ListFunctions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listfunctionspaginator)
        """


class ListGraphqlApisPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListGraphqlApis.html#AppSync.Paginator.ListGraphqlApis)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listgraphqlapispaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGraphqlApisRequestListGraphqlApisPaginateTypeDef]
    ) -> _PageIterator[ListGraphqlApisResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListGraphqlApis.html#AppSync.Paginator.ListGraphqlApis.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listgraphqlapispaginator)
        """


class ListResolversByFunctionPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListResolversByFunction.html#AppSync.Paginator.ListResolversByFunction)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listresolversbyfunctionpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResolversByFunctionRequestListResolversByFunctionPaginateTypeDef]
    ) -> _PageIterator[ListResolversByFunctionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListResolversByFunction.html#AppSync.Paginator.ListResolversByFunction.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listresolversbyfunctionpaginator)
        """


class ListResolversPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListResolvers.html#AppSync.Paginator.ListResolvers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listresolverspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResolversRequestListResolversPaginateTypeDef]
    ) -> _PageIterator[ListResolversResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListResolvers.html#AppSync.Paginator.ListResolvers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listresolverspaginator)
        """


class ListSourceApiAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListSourceApiAssociations.html#AppSync.Paginator.ListSourceApiAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listsourceapiassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListSourceApiAssociationsRequestListSourceApiAssociationsPaginateTypeDef],
    ) -> _PageIterator[ListSourceApiAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListSourceApiAssociations.html#AppSync.Paginator.ListSourceApiAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listsourceapiassociationspaginator)
        """


class ListTypesByAssociationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListTypesByAssociation.html#AppSync.Paginator.ListTypesByAssociation)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listtypesbyassociationpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTypesByAssociationRequestListTypesByAssociationPaginateTypeDef]
    ) -> _PageIterator[ListTypesByAssociationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListTypesByAssociation.html#AppSync.Paginator.ListTypesByAssociation.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listtypesbyassociationpaginator)
        """


class ListTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListTypes.html#AppSync.Paginator.ListTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listtypespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTypesRequestListTypesPaginateTypeDef]
    ) -> _PageIterator[ListTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListTypes.html#AppSync.Paginator.ListTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/paginators/#listtypespaginator)
        """
