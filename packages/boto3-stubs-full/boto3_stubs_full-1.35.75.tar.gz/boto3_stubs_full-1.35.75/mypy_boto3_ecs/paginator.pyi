"""
Type annotations for ecs service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ecs.client import ECSClient
    from mypy_boto3_ecs.paginator import (
        ListAccountSettingsPaginator,
        ListAttributesPaginator,
        ListClustersPaginator,
        ListContainerInstancesPaginator,
        ListServicesByNamespacePaginator,
        ListServicesPaginator,
        ListTaskDefinitionFamiliesPaginator,
        ListTaskDefinitionsPaginator,
        ListTasksPaginator,
    )

    session = Session()
    client: ECSClient = session.client("ecs")

    list_account_settings_paginator: ListAccountSettingsPaginator = client.get_paginator("list_account_settings")
    list_attributes_paginator: ListAttributesPaginator = client.get_paginator("list_attributes")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_container_instances_paginator: ListContainerInstancesPaginator = client.get_paginator("list_container_instances")
    list_services_by_namespace_paginator: ListServicesByNamespacePaginator = client.get_paginator("list_services_by_namespace")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    list_task_definition_families_paginator: ListTaskDefinitionFamiliesPaginator = client.get_paginator("list_task_definition_families")
    list_task_definitions_paginator: ListTaskDefinitionsPaginator = client.get_paginator("list_task_definitions")
    list_tasks_paginator: ListTasksPaginator = client.get_paginator("list_tasks")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAccountSettingsRequestListAccountSettingsPaginateTypeDef,
    ListAccountSettingsResponseTypeDef,
    ListAttributesRequestListAttributesPaginateTypeDef,
    ListAttributesResponseTypeDef,
    ListClustersRequestListClustersPaginateTypeDef,
    ListClustersResponseTypeDef,
    ListContainerInstancesRequestListContainerInstancesPaginateTypeDef,
    ListContainerInstancesResponseTypeDef,
    ListServicesByNamespaceRequestListServicesByNamespacePaginateTypeDef,
    ListServicesByNamespaceResponseTypeDef,
    ListServicesRequestListServicesPaginateTypeDef,
    ListServicesResponseTypeDef,
    ListTaskDefinitionFamiliesRequestListTaskDefinitionFamiliesPaginateTypeDef,
    ListTaskDefinitionFamiliesResponseTypeDef,
    ListTaskDefinitionsRequestListTaskDefinitionsPaginateTypeDef,
    ListTaskDefinitionsResponseTypeDef,
    ListTasksRequestListTasksPaginateTypeDef,
    ListTasksResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAccountSettingsPaginator",
    "ListAttributesPaginator",
    "ListClustersPaginator",
    "ListContainerInstancesPaginator",
    "ListServicesByNamespacePaginator",
    "ListServicesPaginator",
    "ListTaskDefinitionFamiliesPaginator",
    "ListTaskDefinitionsPaginator",
    "ListTasksPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAccountSettingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListAccountSettings.html#ECS.Paginator.ListAccountSettings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listaccountsettingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAccountSettingsRequestListAccountSettingsPaginateTypeDef]
    ) -> _PageIterator[ListAccountSettingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListAccountSettings.html#ECS.Paginator.ListAccountSettings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listaccountsettingspaginator)
        """

class ListAttributesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListAttributes.html#ECS.Paginator.ListAttributes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listattributespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAttributesRequestListAttributesPaginateTypeDef]
    ) -> _PageIterator[ListAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListAttributes.html#ECS.Paginator.ListAttributes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listattributespaginator)
        """

class ListClustersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListClusters.html#ECS.Paginator.ListClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListClustersRequestListClustersPaginateTypeDef]
    ) -> _PageIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListClusters.html#ECS.Paginator.ListClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listclusterspaginator)
        """

class ListContainerInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListContainerInstances.html#ECS.Paginator.ListContainerInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listcontainerinstancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListContainerInstancesRequestListContainerInstancesPaginateTypeDef]
    ) -> _PageIterator[ListContainerInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListContainerInstances.html#ECS.Paginator.ListContainerInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listcontainerinstancespaginator)
        """

class ListServicesByNamespacePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListServicesByNamespace.html#ECS.Paginator.ListServicesByNamespace)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listservicesbynamespacepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListServicesByNamespaceRequestListServicesByNamespacePaginateTypeDef]
    ) -> _PageIterator[ListServicesByNamespaceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListServicesByNamespace.html#ECS.Paginator.ListServicesByNamespace.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listservicesbynamespacepaginator)
        """

class ListServicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListServices.html#ECS.Paginator.ListServices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listservicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListServicesRequestListServicesPaginateTypeDef]
    ) -> _PageIterator[ListServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListServices.html#ECS.Paginator.ListServices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listservicespaginator)
        """

class ListTaskDefinitionFamiliesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListTaskDefinitionFamilies.html#ECS.Paginator.ListTaskDefinitionFamilies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listtaskdefinitionfamiliespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListTaskDefinitionFamiliesRequestListTaskDefinitionFamiliesPaginateTypeDef
        ],
    ) -> _PageIterator[ListTaskDefinitionFamiliesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListTaskDefinitionFamilies.html#ECS.Paginator.ListTaskDefinitionFamilies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listtaskdefinitionfamiliespaginator)
        """

class ListTaskDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListTaskDefinitions.html#ECS.Paginator.ListTaskDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listtaskdefinitionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTaskDefinitionsRequestListTaskDefinitionsPaginateTypeDef]
    ) -> _PageIterator[ListTaskDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListTaskDefinitions.html#ECS.Paginator.ListTaskDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listtaskdefinitionspaginator)
        """

class ListTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListTasks.html#ECS.Paginator.ListTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listtaskspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTasksRequestListTasksPaginateTypeDef]
    ) -> _PageIterator[ListTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListTasks.html#ECS.Paginator.ListTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listtaskspaginator)
        """
