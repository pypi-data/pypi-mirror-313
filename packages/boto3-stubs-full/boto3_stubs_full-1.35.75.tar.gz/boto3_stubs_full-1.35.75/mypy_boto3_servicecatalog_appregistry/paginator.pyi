"""
Type annotations for servicecatalog-appregistry service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_servicecatalog_appregistry.client import AppRegistryClient
    from mypy_boto3_servicecatalog_appregistry.paginator import (
        ListApplicationsPaginator,
        ListAssociatedAttributeGroupsPaginator,
        ListAssociatedResourcesPaginator,
        ListAttributeGroupsForApplicationPaginator,
        ListAttributeGroupsPaginator,
    )

    session = Session()
    client: AppRegistryClient = session.client("servicecatalog-appregistry")

    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_associated_attribute_groups_paginator: ListAssociatedAttributeGroupsPaginator = client.get_paginator("list_associated_attribute_groups")
    list_associated_resources_paginator: ListAssociatedResourcesPaginator = client.get_paginator("list_associated_resources")
    list_attribute_groups_for_application_paginator: ListAttributeGroupsForApplicationPaginator = client.get_paginator("list_attribute_groups_for_application")
    list_attribute_groups_paginator: ListAttributeGroupsPaginator = client.get_paginator("list_attribute_groups")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListApplicationsRequestListApplicationsPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef,
    ListAssociatedAttributeGroupsResponseTypeDef,
    ListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef,
    ListAssociatedResourcesResponseTypeDef,
    ListAttributeGroupsForApplicationRequestListAttributeGroupsForApplicationPaginateTypeDef,
    ListAttributeGroupsForApplicationResponseTypeDef,
    ListAttributeGroupsRequestListAttributeGroupsPaginateTypeDef,
    ListAttributeGroupsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListApplicationsPaginator",
    "ListAssociatedAttributeGroupsPaginator",
    "ListAssociatedResourcesPaginator",
    "ListAttributeGroupsForApplicationPaginator",
    "ListAttributeGroupsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListApplications.html#AppRegistry.Paginator.ListApplications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators/#listapplicationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListApplicationsRequestListApplicationsPaginateTypeDef]
    ) -> _PageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListApplications.html#AppRegistry.Paginator.ListApplications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators/#listapplicationspaginator)
        """

class ListAssociatedAttributeGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListAssociatedAttributeGroups.html#AppRegistry.Paginator.ListAssociatedAttributeGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators/#listassociatedattributegroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[ListAssociatedAttributeGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListAssociatedAttributeGroups.html#AppRegistry.Paginator.ListAssociatedAttributeGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators/#listassociatedattributegroupspaginator)
        """

class ListAssociatedResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListAssociatedResources.html#AppRegistry.Paginator.ListAssociatedResources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators/#listassociatedresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef]
    ) -> _PageIterator[ListAssociatedResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListAssociatedResources.html#AppRegistry.Paginator.ListAssociatedResources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators/#listassociatedresourcespaginator)
        """

class ListAttributeGroupsForApplicationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListAttributeGroupsForApplication.html#AppRegistry.Paginator.ListAttributeGroupsForApplication)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators/#listattributegroupsforapplicationpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAttributeGroupsForApplicationRequestListAttributeGroupsForApplicationPaginateTypeDef
        ],
    ) -> _PageIterator[ListAttributeGroupsForApplicationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListAttributeGroupsForApplication.html#AppRegistry.Paginator.ListAttributeGroupsForApplication.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators/#listattributegroupsforapplicationpaginator)
        """

class ListAttributeGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListAttributeGroups.html#AppRegistry.Paginator.ListAttributeGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators/#listattributegroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAttributeGroupsRequestListAttributeGroupsPaginateTypeDef]
    ) -> _PageIterator[ListAttributeGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListAttributeGroups.html#AppRegistry.Paginator.ListAttributeGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators/#listattributegroupspaginator)
        """
