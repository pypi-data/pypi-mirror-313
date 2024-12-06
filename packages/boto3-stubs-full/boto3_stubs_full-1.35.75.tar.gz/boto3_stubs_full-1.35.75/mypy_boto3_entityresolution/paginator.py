"""
Type annotations for entityresolution service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_entityresolution.client import EntityResolutionClient
    from mypy_boto3_entityresolution.paginator import (
        ListIdMappingJobsPaginator,
        ListIdMappingWorkflowsPaginator,
        ListIdNamespacesPaginator,
        ListMatchingJobsPaginator,
        ListMatchingWorkflowsPaginator,
        ListProviderServicesPaginator,
        ListSchemaMappingsPaginator,
    )

    session = Session()
    client: EntityResolutionClient = session.client("entityresolution")

    list_id_mapping_jobs_paginator: ListIdMappingJobsPaginator = client.get_paginator("list_id_mapping_jobs")
    list_id_mapping_workflows_paginator: ListIdMappingWorkflowsPaginator = client.get_paginator("list_id_mapping_workflows")
    list_id_namespaces_paginator: ListIdNamespacesPaginator = client.get_paginator("list_id_namespaces")
    list_matching_jobs_paginator: ListMatchingJobsPaginator = client.get_paginator("list_matching_jobs")
    list_matching_workflows_paginator: ListMatchingWorkflowsPaginator = client.get_paginator("list_matching_workflows")
    list_provider_services_paginator: ListProviderServicesPaginator = client.get_paginator("list_provider_services")
    list_schema_mappings_paginator: ListSchemaMappingsPaginator = client.get_paginator("list_schema_mappings")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListIdMappingJobsInputListIdMappingJobsPaginateTypeDef,
    ListIdMappingJobsOutputTypeDef,
    ListIdMappingWorkflowsInputListIdMappingWorkflowsPaginateTypeDef,
    ListIdMappingWorkflowsOutputTypeDef,
    ListIdNamespacesInputListIdNamespacesPaginateTypeDef,
    ListIdNamespacesOutputTypeDef,
    ListMatchingJobsInputListMatchingJobsPaginateTypeDef,
    ListMatchingJobsOutputTypeDef,
    ListMatchingWorkflowsInputListMatchingWorkflowsPaginateTypeDef,
    ListMatchingWorkflowsOutputTypeDef,
    ListProviderServicesInputListProviderServicesPaginateTypeDef,
    ListProviderServicesOutputTypeDef,
    ListSchemaMappingsInputListSchemaMappingsPaginateTypeDef,
    ListSchemaMappingsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListIdMappingJobsPaginator",
    "ListIdMappingWorkflowsPaginator",
    "ListIdNamespacesPaginator",
    "ListMatchingJobsPaginator",
    "ListMatchingWorkflowsPaginator",
    "ListProviderServicesPaginator",
    "ListSchemaMappingsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListIdMappingJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdMappingJobs.html#EntityResolution.Paginator.ListIdMappingJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/paginators/#listidmappingjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListIdMappingJobsInputListIdMappingJobsPaginateTypeDef]
    ) -> _PageIterator[ListIdMappingJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdMappingJobs.html#EntityResolution.Paginator.ListIdMappingJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/paginators/#listidmappingjobspaginator)
        """


class ListIdMappingWorkflowsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdMappingWorkflows.html#EntityResolution.Paginator.ListIdMappingWorkflows)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/paginators/#listidmappingworkflowspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListIdMappingWorkflowsInputListIdMappingWorkflowsPaginateTypeDef]
    ) -> _PageIterator[ListIdMappingWorkflowsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdMappingWorkflows.html#EntityResolution.Paginator.ListIdMappingWorkflows.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/paginators/#listidmappingworkflowspaginator)
        """


class ListIdNamespacesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdNamespaces.html#EntityResolution.Paginator.ListIdNamespaces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/paginators/#listidnamespacespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListIdNamespacesInputListIdNamespacesPaginateTypeDef]
    ) -> _PageIterator[ListIdNamespacesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdNamespaces.html#EntityResolution.Paginator.ListIdNamespaces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/paginators/#listidnamespacespaginator)
        """


class ListMatchingJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListMatchingJobs.html#EntityResolution.Paginator.ListMatchingJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/paginators/#listmatchingjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMatchingJobsInputListMatchingJobsPaginateTypeDef]
    ) -> _PageIterator[ListMatchingJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListMatchingJobs.html#EntityResolution.Paginator.ListMatchingJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/paginators/#listmatchingjobspaginator)
        """


class ListMatchingWorkflowsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListMatchingWorkflows.html#EntityResolution.Paginator.ListMatchingWorkflows)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/paginators/#listmatchingworkflowspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMatchingWorkflowsInputListMatchingWorkflowsPaginateTypeDef]
    ) -> _PageIterator[ListMatchingWorkflowsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListMatchingWorkflows.html#EntityResolution.Paginator.ListMatchingWorkflows.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/paginators/#listmatchingworkflowspaginator)
        """


class ListProviderServicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListProviderServices.html#EntityResolution.Paginator.ListProviderServices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/paginators/#listproviderservicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListProviderServicesInputListProviderServicesPaginateTypeDef]
    ) -> _PageIterator[ListProviderServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListProviderServices.html#EntityResolution.Paginator.ListProviderServices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/paginators/#listproviderservicespaginator)
        """


class ListSchemaMappingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListSchemaMappings.html#EntityResolution.Paginator.ListSchemaMappings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/paginators/#listschemamappingspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSchemaMappingsInputListSchemaMappingsPaginateTypeDef]
    ) -> _PageIterator[ListSchemaMappingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListSchemaMappings.html#EntityResolution.Paginator.ListSchemaMappings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/paginators/#listschemamappingspaginator)
        """
