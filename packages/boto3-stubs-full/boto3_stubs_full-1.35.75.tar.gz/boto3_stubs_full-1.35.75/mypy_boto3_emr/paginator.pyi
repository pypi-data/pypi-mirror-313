"""
Type annotations for emr service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_emr.client import EMRClient
    from mypy_boto3_emr.paginator import (
        ListBootstrapActionsPaginator,
        ListClustersPaginator,
        ListInstanceFleetsPaginator,
        ListInstanceGroupsPaginator,
        ListInstancesPaginator,
        ListNotebookExecutionsPaginator,
        ListSecurityConfigurationsPaginator,
        ListStepsPaginator,
        ListStudioSessionMappingsPaginator,
        ListStudiosPaginator,
    )

    session = Session()
    client: EMRClient = session.client("emr")

    list_bootstrap_actions_paginator: ListBootstrapActionsPaginator = client.get_paginator("list_bootstrap_actions")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_instance_fleets_paginator: ListInstanceFleetsPaginator = client.get_paginator("list_instance_fleets")
    list_instance_groups_paginator: ListInstanceGroupsPaginator = client.get_paginator("list_instance_groups")
    list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    list_notebook_executions_paginator: ListNotebookExecutionsPaginator = client.get_paginator("list_notebook_executions")
    list_security_configurations_paginator: ListSecurityConfigurationsPaginator = client.get_paginator("list_security_configurations")
    list_steps_paginator: ListStepsPaginator = client.get_paginator("list_steps")
    list_studio_session_mappings_paginator: ListStudioSessionMappingsPaginator = client.get_paginator("list_studio_session_mappings")
    list_studios_paginator: ListStudiosPaginator = client.get_paginator("list_studios")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListBootstrapActionsInputListBootstrapActionsPaginateTypeDef,
    ListBootstrapActionsOutputTypeDef,
    ListClustersInputListClustersPaginateTypeDef,
    ListClustersOutputTypeDef,
    ListInstanceFleetsInputListInstanceFleetsPaginateTypeDef,
    ListInstanceFleetsOutputPaginatorTypeDef,
    ListInstanceGroupsInputListInstanceGroupsPaginateTypeDef,
    ListInstanceGroupsOutputPaginatorTypeDef,
    ListInstancesInputListInstancesPaginateTypeDef,
    ListInstancesOutputTypeDef,
    ListNotebookExecutionsInputListNotebookExecutionsPaginateTypeDef,
    ListNotebookExecutionsOutputTypeDef,
    ListSecurityConfigurationsInputListSecurityConfigurationsPaginateTypeDef,
    ListSecurityConfigurationsOutputTypeDef,
    ListStepsInputListStepsPaginateTypeDef,
    ListStepsOutputTypeDef,
    ListStudioSessionMappingsInputListStudioSessionMappingsPaginateTypeDef,
    ListStudioSessionMappingsOutputTypeDef,
    ListStudiosInputListStudiosPaginateTypeDef,
    ListStudiosOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListBootstrapActionsPaginator",
    "ListClustersPaginator",
    "ListInstanceFleetsPaginator",
    "ListInstanceGroupsPaginator",
    "ListInstancesPaginator",
    "ListNotebookExecutionsPaginator",
    "ListSecurityConfigurationsPaginator",
    "ListStepsPaginator",
    "ListStudioSessionMappingsPaginator",
    "ListStudiosPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListBootstrapActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListBootstrapActions.html#EMR.Paginator.ListBootstrapActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listbootstrapactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBootstrapActionsInputListBootstrapActionsPaginateTypeDef]
    ) -> _PageIterator[ListBootstrapActionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListBootstrapActions.html#EMR.Paginator.ListBootstrapActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listbootstrapactionspaginator)
        """

class ListClustersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListClusters.html#EMR.Paginator.ListClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListClustersInputListClustersPaginateTypeDef]
    ) -> _PageIterator[ListClustersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListClusters.html#EMR.Paginator.ListClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listclusterspaginator)
        """

class ListInstanceFleetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListInstanceFleets.html#EMR.Paginator.ListInstanceFleets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listinstancefleetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInstanceFleetsInputListInstanceFleetsPaginateTypeDef]
    ) -> _PageIterator[ListInstanceFleetsOutputPaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListInstanceFleets.html#EMR.Paginator.ListInstanceFleets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listinstancefleetspaginator)
        """

class ListInstanceGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListInstanceGroups.html#EMR.Paginator.ListInstanceGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listinstancegroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInstanceGroupsInputListInstanceGroupsPaginateTypeDef]
    ) -> _PageIterator[ListInstanceGroupsOutputPaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListInstanceGroups.html#EMR.Paginator.ListInstanceGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listinstancegroupspaginator)
        """

class ListInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListInstances.html#EMR.Paginator.ListInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listinstancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInstancesInputListInstancesPaginateTypeDef]
    ) -> _PageIterator[ListInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListInstances.html#EMR.Paginator.ListInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listinstancespaginator)
        """

class ListNotebookExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListNotebookExecutions.html#EMR.Paginator.ListNotebookExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listnotebookexecutionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListNotebookExecutionsInputListNotebookExecutionsPaginateTypeDef]
    ) -> _PageIterator[ListNotebookExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListNotebookExecutions.html#EMR.Paginator.ListNotebookExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listnotebookexecutionspaginator)
        """

class ListSecurityConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListSecurityConfigurations.html#EMR.Paginator.ListSecurityConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listsecurityconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListSecurityConfigurationsInputListSecurityConfigurationsPaginateTypeDef],
    ) -> _PageIterator[ListSecurityConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListSecurityConfigurations.html#EMR.Paginator.ListSecurityConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listsecurityconfigurationspaginator)
        """

class ListStepsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListSteps.html#EMR.Paginator.ListSteps)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#liststepspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStepsInputListStepsPaginateTypeDef]
    ) -> _PageIterator[ListStepsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListSteps.html#EMR.Paginator.ListSteps.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#liststepspaginator)
        """

class ListStudioSessionMappingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListStudioSessionMappings.html#EMR.Paginator.ListStudioSessionMappings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#liststudiosessionmappingspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListStudioSessionMappingsInputListStudioSessionMappingsPaginateTypeDef],
    ) -> _PageIterator[ListStudioSessionMappingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListStudioSessionMappings.html#EMR.Paginator.ListStudioSessionMappings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#liststudiosessionmappingspaginator)
        """

class ListStudiosPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListStudios.html#EMR.Paginator.ListStudios)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#liststudiospaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStudiosInputListStudiosPaginateTypeDef]
    ) -> _PageIterator[ListStudiosOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListStudios.html#EMR.Paginator.ListStudios.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#liststudiospaginator)
        """
