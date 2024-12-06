"""
Type annotations for appintegrations service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_appintegrations.client import AppIntegrationsServiceClient
    from mypy_boto3_appintegrations.paginator import (
        ListApplicationAssociationsPaginator,
        ListApplicationsPaginator,
        ListDataIntegrationAssociationsPaginator,
        ListDataIntegrationsPaginator,
        ListEventIntegrationAssociationsPaginator,
        ListEventIntegrationsPaginator,
    )

    session = Session()
    client: AppIntegrationsServiceClient = session.client("appintegrations")

    list_application_associations_paginator: ListApplicationAssociationsPaginator = client.get_paginator("list_application_associations")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_data_integration_associations_paginator: ListDataIntegrationAssociationsPaginator = client.get_paginator("list_data_integration_associations")
    list_data_integrations_paginator: ListDataIntegrationsPaginator = client.get_paginator("list_data_integrations")
    list_event_integration_associations_paginator: ListEventIntegrationAssociationsPaginator = client.get_paginator("list_event_integration_associations")
    list_event_integrations_paginator: ListEventIntegrationsPaginator = client.get_paginator("list_event_integrations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListApplicationAssociationsRequestListApplicationAssociationsPaginateTypeDef,
    ListApplicationAssociationsResponseTypeDef,
    ListApplicationsRequestListApplicationsPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListDataIntegrationAssociationsRequestListDataIntegrationAssociationsPaginateTypeDef,
    ListDataIntegrationAssociationsResponseTypeDef,
    ListDataIntegrationsRequestListDataIntegrationsPaginateTypeDef,
    ListDataIntegrationsResponseTypeDef,
    ListEventIntegrationAssociationsRequestListEventIntegrationAssociationsPaginateTypeDef,
    ListEventIntegrationAssociationsResponseTypeDef,
    ListEventIntegrationsRequestListEventIntegrationsPaginateTypeDef,
    ListEventIntegrationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListApplicationAssociationsPaginator",
    "ListApplicationsPaginator",
    "ListDataIntegrationAssociationsPaginator",
    "ListDataIntegrationsPaginator",
    "ListEventIntegrationAssociationsPaginator",
    "ListEventIntegrationsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListApplicationAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListApplicationAssociations.html#AppIntegrationsService.Paginator.ListApplicationAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/paginators/#listapplicationassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListApplicationAssociationsRequestListApplicationAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListApplicationAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListApplicationAssociations.html#AppIntegrationsService.Paginator.ListApplicationAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/paginators/#listapplicationassociationspaginator)
        """


class ListApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListApplications.html#AppIntegrationsService.Paginator.ListApplications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/paginators/#listapplicationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListApplicationsRequestListApplicationsPaginateTypeDef]
    ) -> _PageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListApplications.html#AppIntegrationsService.Paginator.ListApplications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/paginators/#listapplicationspaginator)
        """


class ListDataIntegrationAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListDataIntegrationAssociations.html#AppIntegrationsService.Paginator.ListDataIntegrationAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/paginators/#listdataintegrationassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListDataIntegrationAssociationsRequestListDataIntegrationAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListDataIntegrationAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListDataIntegrationAssociations.html#AppIntegrationsService.Paginator.ListDataIntegrationAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/paginators/#listdataintegrationassociationspaginator)
        """


class ListDataIntegrationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListDataIntegrations.html#AppIntegrationsService.Paginator.ListDataIntegrations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/paginators/#listdataintegrationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDataIntegrationsRequestListDataIntegrationsPaginateTypeDef]
    ) -> _PageIterator[ListDataIntegrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListDataIntegrations.html#AppIntegrationsService.Paginator.ListDataIntegrations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/paginators/#listdataintegrationspaginator)
        """


class ListEventIntegrationAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListEventIntegrationAssociations.html#AppIntegrationsService.Paginator.ListEventIntegrationAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/paginators/#listeventintegrationassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListEventIntegrationAssociationsRequestListEventIntegrationAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListEventIntegrationAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListEventIntegrationAssociations.html#AppIntegrationsService.Paginator.ListEventIntegrationAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/paginators/#listeventintegrationassociationspaginator)
        """


class ListEventIntegrationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListEventIntegrations.html#AppIntegrationsService.Paginator.ListEventIntegrations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/paginators/#listeventintegrationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEventIntegrationsRequestListEventIntegrationsPaginateTypeDef]
    ) -> _PageIterator[ListEventIntegrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListEventIntegrations.html#AppIntegrationsService.Paginator.ListEventIntegrations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/paginators/#listeventintegrationspaginator)
        """
