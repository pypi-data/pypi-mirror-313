"""
Type annotations for emr-containers service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_emr_containers.client import EMRContainersClient
    from mypy_boto3_emr_containers.paginator import (
        ListJobRunsPaginator,
        ListJobTemplatesPaginator,
        ListManagedEndpointsPaginator,
        ListSecurityConfigurationsPaginator,
        ListVirtualClustersPaginator,
    )

    session = Session()
    client: EMRContainersClient = session.client("emr-containers")

    list_job_runs_paginator: ListJobRunsPaginator = client.get_paginator("list_job_runs")
    list_job_templates_paginator: ListJobTemplatesPaginator = client.get_paginator("list_job_templates")
    list_managed_endpoints_paginator: ListManagedEndpointsPaginator = client.get_paginator("list_managed_endpoints")
    list_security_configurations_paginator: ListSecurityConfigurationsPaginator = client.get_paginator("list_security_configurations")
    list_virtual_clusters_paginator: ListVirtualClustersPaginator = client.get_paginator("list_virtual_clusters")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListJobRunsRequestListJobRunsPaginateTypeDef,
    ListJobRunsResponsePaginatorTypeDef,
    ListJobTemplatesRequestListJobTemplatesPaginateTypeDef,
    ListJobTemplatesResponsePaginatorTypeDef,
    ListManagedEndpointsRequestListManagedEndpointsPaginateTypeDef,
    ListManagedEndpointsResponsePaginatorTypeDef,
    ListSecurityConfigurationsRequestListSecurityConfigurationsPaginateTypeDef,
    ListSecurityConfigurationsResponseTypeDef,
    ListVirtualClustersRequestListVirtualClustersPaginateTypeDef,
    ListVirtualClustersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListJobRunsPaginator",
    "ListJobTemplatesPaginator",
    "ListManagedEndpointsPaginator",
    "ListSecurityConfigurationsPaginator",
    "ListVirtualClustersPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListJobRunsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListJobRuns.html#EMRContainers.Paginator.ListJobRuns)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listjobrunspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListJobRunsRequestListJobRunsPaginateTypeDef]
    ) -> _PageIterator[ListJobRunsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListJobRuns.html#EMRContainers.Paginator.ListJobRuns.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listjobrunspaginator)
        """


class ListJobTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListJobTemplates.html#EMRContainers.Paginator.ListJobTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listjobtemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListJobTemplatesRequestListJobTemplatesPaginateTypeDef]
    ) -> _PageIterator[ListJobTemplatesResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListJobTemplates.html#EMRContainers.Paginator.ListJobTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listjobtemplatespaginator)
        """


class ListManagedEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListManagedEndpoints.html#EMRContainers.Paginator.ListManagedEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listmanagedendpointspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListManagedEndpointsRequestListManagedEndpointsPaginateTypeDef]
    ) -> _PageIterator[ListManagedEndpointsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListManagedEndpoints.html#EMRContainers.Paginator.ListManagedEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listmanagedendpointspaginator)
        """


class ListSecurityConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListSecurityConfigurations.html#EMRContainers.Paginator.ListSecurityConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listsecurityconfigurationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListSecurityConfigurationsRequestListSecurityConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListSecurityConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListSecurityConfigurations.html#EMRContainers.Paginator.ListSecurityConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listsecurityconfigurationspaginator)
        """


class ListVirtualClustersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListVirtualClusters.html#EMRContainers.Paginator.ListVirtualClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listvirtualclusterspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListVirtualClustersRequestListVirtualClustersPaginateTypeDef]
    ) -> _PageIterator[ListVirtualClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListVirtualClusters.html#EMRContainers.Paginator.ListVirtualClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listvirtualclusterspaginator)
        """
