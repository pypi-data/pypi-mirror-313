"""
Type annotations for pca-connector-ad service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_pca_connector_ad.client import PcaConnectorAdClient
    from mypy_boto3_pca_connector_ad.paginator import (
        ListConnectorsPaginator,
        ListDirectoryRegistrationsPaginator,
        ListServicePrincipalNamesPaginator,
        ListTemplateGroupAccessControlEntriesPaginator,
        ListTemplatesPaginator,
    )

    session = Session()
    client: PcaConnectorAdClient = session.client("pca-connector-ad")

    list_connectors_paginator: ListConnectorsPaginator = client.get_paginator("list_connectors")
    list_directory_registrations_paginator: ListDirectoryRegistrationsPaginator = client.get_paginator("list_directory_registrations")
    list_service_principal_names_paginator: ListServicePrincipalNamesPaginator = client.get_paginator("list_service_principal_names")
    list_template_group_access_control_entries_paginator: ListTemplateGroupAccessControlEntriesPaginator = client.get_paginator("list_template_group_access_control_entries")
    list_templates_paginator: ListTemplatesPaginator = client.get_paginator("list_templates")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListConnectorsRequestListConnectorsPaginateTypeDef,
    ListConnectorsResponseTypeDef,
    ListDirectoryRegistrationsRequestListDirectoryRegistrationsPaginateTypeDef,
    ListDirectoryRegistrationsResponseTypeDef,
    ListServicePrincipalNamesRequestListServicePrincipalNamesPaginateTypeDef,
    ListServicePrincipalNamesResponseTypeDef,
    ListTemplateGroupAccessControlEntriesRequestListTemplateGroupAccessControlEntriesPaginateTypeDef,
    ListTemplateGroupAccessControlEntriesResponseTypeDef,
    ListTemplatesRequestListTemplatesPaginateTypeDef,
    ListTemplatesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListConnectorsPaginator",
    "ListDirectoryRegistrationsPaginator",
    "ListServicePrincipalNamesPaginator",
    "ListTemplateGroupAccessControlEntriesPaginator",
    "ListTemplatesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListConnectorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListConnectors.html#PcaConnectorAd.Paginator.ListConnectors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/paginators/#listconnectorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListConnectorsRequestListConnectorsPaginateTypeDef]
    ) -> _PageIterator[ListConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListConnectors.html#PcaConnectorAd.Paginator.ListConnectors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/paginators/#listconnectorspaginator)
        """


class ListDirectoryRegistrationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListDirectoryRegistrations.html#PcaConnectorAd.Paginator.ListDirectoryRegistrations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/paginators/#listdirectoryregistrationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListDirectoryRegistrationsRequestListDirectoryRegistrationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListDirectoryRegistrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListDirectoryRegistrations.html#PcaConnectorAd.Paginator.ListDirectoryRegistrations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/paginators/#listdirectoryregistrationspaginator)
        """


class ListServicePrincipalNamesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListServicePrincipalNames.html#PcaConnectorAd.Paginator.ListServicePrincipalNames)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/paginators/#listserviceprincipalnamespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListServicePrincipalNamesRequestListServicePrincipalNamesPaginateTypeDef],
    ) -> _PageIterator[ListServicePrincipalNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListServicePrincipalNames.html#PcaConnectorAd.Paginator.ListServicePrincipalNames.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/paginators/#listserviceprincipalnamespaginator)
        """


class ListTemplateGroupAccessControlEntriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListTemplateGroupAccessControlEntries.html#PcaConnectorAd.Paginator.ListTemplateGroupAccessControlEntries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/paginators/#listtemplategroupaccesscontrolentriespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListTemplateGroupAccessControlEntriesRequestListTemplateGroupAccessControlEntriesPaginateTypeDef
        ],
    ) -> _PageIterator[ListTemplateGroupAccessControlEntriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListTemplateGroupAccessControlEntries.html#PcaConnectorAd.Paginator.ListTemplateGroupAccessControlEntries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/paginators/#listtemplategroupaccesscontrolentriespaginator)
        """


class ListTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListTemplates.html#PcaConnectorAd.Paginator.ListTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/paginators/#listtemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTemplatesRequestListTemplatesPaginateTypeDef]
    ) -> _PageIterator[ListTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListTemplates.html#PcaConnectorAd.Paginator.ListTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/paginators/#listtemplatespaginator)
        """
