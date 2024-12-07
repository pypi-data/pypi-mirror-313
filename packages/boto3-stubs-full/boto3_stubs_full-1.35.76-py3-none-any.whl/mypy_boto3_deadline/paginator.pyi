"""
Type annotations for deadline service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_deadline.client import DeadlineCloudClient
    from mypy_boto3_deadline.paginator import (
        GetSessionsStatisticsAggregationPaginator,
        ListAvailableMeteredProductsPaginator,
        ListBudgetsPaginator,
        ListFarmMembersPaginator,
        ListFarmsPaginator,
        ListFleetMembersPaginator,
        ListFleetsPaginator,
        ListJobMembersPaginator,
        ListJobParameterDefinitionsPaginator,
        ListJobsPaginator,
        ListLicenseEndpointsPaginator,
        ListMeteredProductsPaginator,
        ListMonitorsPaginator,
        ListQueueEnvironmentsPaginator,
        ListQueueFleetAssociationsPaginator,
        ListQueueMembersPaginator,
        ListQueuesPaginator,
        ListSessionActionsPaginator,
        ListSessionsForWorkerPaginator,
        ListSessionsPaginator,
        ListStepConsumersPaginator,
        ListStepDependenciesPaginator,
        ListStepsPaginator,
        ListStorageProfilesForQueuePaginator,
        ListStorageProfilesPaginator,
        ListTasksPaginator,
        ListWorkersPaginator,
    )

    session = Session()
    client: DeadlineCloudClient = session.client("deadline")

    get_sessions_statistics_aggregation_paginator: GetSessionsStatisticsAggregationPaginator = client.get_paginator("get_sessions_statistics_aggregation")
    list_available_metered_products_paginator: ListAvailableMeteredProductsPaginator = client.get_paginator("list_available_metered_products")
    list_budgets_paginator: ListBudgetsPaginator = client.get_paginator("list_budgets")
    list_farm_members_paginator: ListFarmMembersPaginator = client.get_paginator("list_farm_members")
    list_farms_paginator: ListFarmsPaginator = client.get_paginator("list_farms")
    list_fleet_members_paginator: ListFleetMembersPaginator = client.get_paginator("list_fleet_members")
    list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
    list_job_members_paginator: ListJobMembersPaginator = client.get_paginator("list_job_members")
    list_job_parameter_definitions_paginator: ListJobParameterDefinitionsPaginator = client.get_paginator("list_job_parameter_definitions")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_license_endpoints_paginator: ListLicenseEndpointsPaginator = client.get_paginator("list_license_endpoints")
    list_metered_products_paginator: ListMeteredProductsPaginator = client.get_paginator("list_metered_products")
    list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
    list_queue_environments_paginator: ListQueueEnvironmentsPaginator = client.get_paginator("list_queue_environments")
    list_queue_fleet_associations_paginator: ListQueueFleetAssociationsPaginator = client.get_paginator("list_queue_fleet_associations")
    list_queue_members_paginator: ListQueueMembersPaginator = client.get_paginator("list_queue_members")
    list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
    list_session_actions_paginator: ListSessionActionsPaginator = client.get_paginator("list_session_actions")
    list_sessions_for_worker_paginator: ListSessionsForWorkerPaginator = client.get_paginator("list_sessions_for_worker")
    list_sessions_paginator: ListSessionsPaginator = client.get_paginator("list_sessions")
    list_step_consumers_paginator: ListStepConsumersPaginator = client.get_paginator("list_step_consumers")
    list_step_dependencies_paginator: ListStepDependenciesPaginator = client.get_paginator("list_step_dependencies")
    list_steps_paginator: ListStepsPaginator = client.get_paginator("list_steps")
    list_storage_profiles_for_queue_paginator: ListStorageProfilesForQueuePaginator = client.get_paginator("list_storage_profiles_for_queue")
    list_storage_profiles_paginator: ListStorageProfilesPaginator = client.get_paginator("list_storage_profiles")
    list_tasks_paginator: ListTasksPaginator = client.get_paginator("list_tasks")
    list_workers_paginator: ListWorkersPaginator = client.get_paginator("list_workers")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetSessionsStatisticsAggregationRequestGetSessionsStatisticsAggregationPaginateTypeDef,
    GetSessionsStatisticsAggregationResponseTypeDef,
    ListAvailableMeteredProductsRequestListAvailableMeteredProductsPaginateTypeDef,
    ListAvailableMeteredProductsResponseTypeDef,
    ListBudgetsRequestListBudgetsPaginateTypeDef,
    ListBudgetsResponseTypeDef,
    ListFarmMembersRequestListFarmMembersPaginateTypeDef,
    ListFarmMembersResponseTypeDef,
    ListFarmsRequestListFarmsPaginateTypeDef,
    ListFarmsResponseTypeDef,
    ListFleetMembersRequestListFleetMembersPaginateTypeDef,
    ListFleetMembersResponseTypeDef,
    ListFleetsRequestListFleetsPaginateTypeDef,
    ListFleetsResponseTypeDef,
    ListJobMembersRequestListJobMembersPaginateTypeDef,
    ListJobMembersResponseTypeDef,
    ListJobParameterDefinitionsRequestListJobParameterDefinitionsPaginateTypeDef,
    ListJobParameterDefinitionsResponseTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListLicenseEndpointsRequestListLicenseEndpointsPaginateTypeDef,
    ListLicenseEndpointsResponseTypeDef,
    ListMeteredProductsRequestListMeteredProductsPaginateTypeDef,
    ListMeteredProductsResponseTypeDef,
    ListMonitorsRequestListMonitorsPaginateTypeDef,
    ListMonitorsResponseTypeDef,
    ListQueueEnvironmentsRequestListQueueEnvironmentsPaginateTypeDef,
    ListQueueEnvironmentsResponseTypeDef,
    ListQueueFleetAssociationsRequestListQueueFleetAssociationsPaginateTypeDef,
    ListQueueFleetAssociationsResponseTypeDef,
    ListQueueMembersRequestListQueueMembersPaginateTypeDef,
    ListQueueMembersResponseTypeDef,
    ListQueuesRequestListQueuesPaginateTypeDef,
    ListQueuesResponseTypeDef,
    ListSessionActionsRequestListSessionActionsPaginateTypeDef,
    ListSessionActionsResponseTypeDef,
    ListSessionsForWorkerRequestListSessionsForWorkerPaginateTypeDef,
    ListSessionsForWorkerResponseTypeDef,
    ListSessionsRequestListSessionsPaginateTypeDef,
    ListSessionsResponseTypeDef,
    ListStepConsumersRequestListStepConsumersPaginateTypeDef,
    ListStepConsumersResponseTypeDef,
    ListStepDependenciesRequestListStepDependenciesPaginateTypeDef,
    ListStepDependenciesResponseTypeDef,
    ListStepsRequestListStepsPaginateTypeDef,
    ListStepsResponseTypeDef,
    ListStorageProfilesForQueueRequestListStorageProfilesForQueuePaginateTypeDef,
    ListStorageProfilesForQueueResponseTypeDef,
    ListStorageProfilesRequestListStorageProfilesPaginateTypeDef,
    ListStorageProfilesResponseTypeDef,
    ListTasksRequestListTasksPaginateTypeDef,
    ListTasksResponseTypeDef,
    ListWorkersRequestListWorkersPaginateTypeDef,
    ListWorkersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetSessionsStatisticsAggregationPaginator",
    "ListAvailableMeteredProductsPaginator",
    "ListBudgetsPaginator",
    "ListFarmMembersPaginator",
    "ListFarmsPaginator",
    "ListFleetMembersPaginator",
    "ListFleetsPaginator",
    "ListJobMembersPaginator",
    "ListJobParameterDefinitionsPaginator",
    "ListJobsPaginator",
    "ListLicenseEndpointsPaginator",
    "ListMeteredProductsPaginator",
    "ListMonitorsPaginator",
    "ListQueueEnvironmentsPaginator",
    "ListQueueFleetAssociationsPaginator",
    "ListQueueMembersPaginator",
    "ListQueuesPaginator",
    "ListSessionActionsPaginator",
    "ListSessionsForWorkerPaginator",
    "ListSessionsPaginator",
    "ListStepConsumersPaginator",
    "ListStepDependenciesPaginator",
    "ListStepsPaginator",
    "ListStorageProfilesForQueuePaginator",
    "ListStorageProfilesPaginator",
    "ListTasksPaginator",
    "ListWorkersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetSessionsStatisticsAggregationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/GetSessionsStatisticsAggregation.html#DeadlineCloud.Paginator.GetSessionsStatisticsAggregation)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#getsessionsstatisticsaggregationpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetSessionsStatisticsAggregationRequestGetSessionsStatisticsAggregationPaginateTypeDef
        ],
    ) -> _PageIterator[GetSessionsStatisticsAggregationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/GetSessionsStatisticsAggregation.html#DeadlineCloud.Paginator.GetSessionsStatisticsAggregation.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#getsessionsstatisticsaggregationpaginator)
        """

class ListAvailableMeteredProductsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListAvailableMeteredProducts.html#DeadlineCloud.Paginator.ListAvailableMeteredProducts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listavailablemeteredproductspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAvailableMeteredProductsRequestListAvailableMeteredProductsPaginateTypeDef
        ],
    ) -> _PageIterator[ListAvailableMeteredProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListAvailableMeteredProducts.html#DeadlineCloud.Paginator.ListAvailableMeteredProducts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listavailablemeteredproductspaginator)
        """

class ListBudgetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListBudgets.html#DeadlineCloud.Paginator.ListBudgets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listbudgetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBudgetsRequestListBudgetsPaginateTypeDef]
    ) -> _PageIterator[ListBudgetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListBudgets.html#DeadlineCloud.Paginator.ListBudgets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listbudgetspaginator)
        """

class ListFarmMembersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFarmMembers.html#DeadlineCloud.Paginator.ListFarmMembers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listfarmmemberspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFarmMembersRequestListFarmMembersPaginateTypeDef]
    ) -> _PageIterator[ListFarmMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFarmMembers.html#DeadlineCloud.Paginator.ListFarmMembers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listfarmmemberspaginator)
        """

class ListFarmsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFarms.html#DeadlineCloud.Paginator.ListFarms)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listfarmspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFarmsRequestListFarmsPaginateTypeDef]
    ) -> _PageIterator[ListFarmsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFarms.html#DeadlineCloud.Paginator.ListFarms.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listfarmspaginator)
        """

class ListFleetMembersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFleetMembers.html#DeadlineCloud.Paginator.ListFleetMembers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listfleetmemberspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFleetMembersRequestListFleetMembersPaginateTypeDef]
    ) -> _PageIterator[ListFleetMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFleetMembers.html#DeadlineCloud.Paginator.ListFleetMembers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listfleetmemberspaginator)
        """

class ListFleetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFleets.html#DeadlineCloud.Paginator.ListFleets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listfleetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFleetsRequestListFleetsPaginateTypeDef]
    ) -> _PageIterator[ListFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFleets.html#DeadlineCloud.Paginator.ListFleets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listfleetspaginator)
        """

class ListJobMembersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobMembers.html#DeadlineCloud.Paginator.ListJobMembers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listjobmemberspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobMembersRequestListJobMembersPaginateTypeDef]
    ) -> _PageIterator[ListJobMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobMembers.html#DeadlineCloud.Paginator.ListJobMembers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listjobmemberspaginator)
        """

class ListJobParameterDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobParameterDefinitions.html#DeadlineCloud.Paginator.ListJobParameterDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listjobparameterdefinitionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListJobParameterDefinitionsRequestListJobParameterDefinitionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListJobParameterDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobParameterDefinitions.html#DeadlineCloud.Paginator.ListJobParameterDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listjobparameterdefinitionspaginator)
        """

class ListJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobs.html#DeadlineCloud.Paginator.ListJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> _PageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobs.html#DeadlineCloud.Paginator.ListJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listjobspaginator)
        """

class ListLicenseEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListLicenseEndpoints.html#DeadlineCloud.Paginator.ListLicenseEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listlicenseendpointspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLicenseEndpointsRequestListLicenseEndpointsPaginateTypeDef]
    ) -> _PageIterator[ListLicenseEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListLicenseEndpoints.html#DeadlineCloud.Paginator.ListLicenseEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listlicenseendpointspaginator)
        """

class ListMeteredProductsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListMeteredProducts.html#DeadlineCloud.Paginator.ListMeteredProducts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listmeteredproductspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMeteredProductsRequestListMeteredProductsPaginateTypeDef]
    ) -> _PageIterator[ListMeteredProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListMeteredProducts.html#DeadlineCloud.Paginator.ListMeteredProducts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listmeteredproductspaginator)
        """

class ListMonitorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListMonitors.html#DeadlineCloud.Paginator.ListMonitors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listmonitorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMonitorsRequestListMonitorsPaginateTypeDef]
    ) -> _PageIterator[ListMonitorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListMonitors.html#DeadlineCloud.Paginator.ListMonitors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listmonitorspaginator)
        """

class ListQueueEnvironmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueEnvironments.html#DeadlineCloud.Paginator.ListQueueEnvironments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listqueueenvironmentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListQueueEnvironmentsRequestListQueueEnvironmentsPaginateTypeDef]
    ) -> _PageIterator[ListQueueEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueEnvironments.html#DeadlineCloud.Paginator.ListQueueEnvironments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listqueueenvironmentspaginator)
        """

class ListQueueFleetAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueFleetAssociations.html#DeadlineCloud.Paginator.ListQueueFleetAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listqueuefleetassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListQueueFleetAssociationsRequestListQueueFleetAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListQueueFleetAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueFleetAssociations.html#DeadlineCloud.Paginator.ListQueueFleetAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listqueuefleetassociationspaginator)
        """

class ListQueueMembersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueMembers.html#DeadlineCloud.Paginator.ListQueueMembers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listqueuememberspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListQueueMembersRequestListQueueMembersPaginateTypeDef]
    ) -> _PageIterator[ListQueueMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueMembers.html#DeadlineCloud.Paginator.ListQueueMembers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listqueuememberspaginator)
        """

class ListQueuesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueues.html#DeadlineCloud.Paginator.ListQueues)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listqueuespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListQueuesRequestListQueuesPaginateTypeDef]
    ) -> _PageIterator[ListQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueues.html#DeadlineCloud.Paginator.ListQueues.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listqueuespaginator)
        """

class ListSessionActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessionActions.html#DeadlineCloud.Paginator.ListSessionActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listsessionactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSessionActionsRequestListSessionActionsPaginateTypeDef]
    ) -> _PageIterator[ListSessionActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessionActions.html#DeadlineCloud.Paginator.ListSessionActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listsessionactionspaginator)
        """

class ListSessionsForWorkerPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessionsForWorker.html#DeadlineCloud.Paginator.ListSessionsForWorker)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listsessionsforworkerpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSessionsForWorkerRequestListSessionsForWorkerPaginateTypeDef]
    ) -> _PageIterator[ListSessionsForWorkerResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessionsForWorker.html#DeadlineCloud.Paginator.ListSessionsForWorker.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listsessionsforworkerpaginator)
        """

class ListSessionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessions.html#DeadlineCloud.Paginator.ListSessions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listsessionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSessionsRequestListSessionsPaginateTypeDef]
    ) -> _PageIterator[ListSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessions.html#DeadlineCloud.Paginator.ListSessions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listsessionspaginator)
        """

class ListStepConsumersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStepConsumers.html#DeadlineCloud.Paginator.ListStepConsumers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststepconsumerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStepConsumersRequestListStepConsumersPaginateTypeDef]
    ) -> _PageIterator[ListStepConsumersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStepConsumers.html#DeadlineCloud.Paginator.ListStepConsumers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststepconsumerspaginator)
        """

class ListStepDependenciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStepDependencies.html#DeadlineCloud.Paginator.ListStepDependencies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststepdependenciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStepDependenciesRequestListStepDependenciesPaginateTypeDef]
    ) -> _PageIterator[ListStepDependenciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStepDependencies.html#DeadlineCloud.Paginator.ListStepDependencies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststepdependenciespaginator)
        """

class ListStepsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSteps.html#DeadlineCloud.Paginator.ListSteps)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststepspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStepsRequestListStepsPaginateTypeDef]
    ) -> _PageIterator[ListStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSteps.html#DeadlineCloud.Paginator.ListSteps.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststepspaginator)
        """

class ListStorageProfilesForQueuePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStorageProfilesForQueue.html#DeadlineCloud.Paginator.ListStorageProfilesForQueue)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststorageprofilesforqueuepaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListStorageProfilesForQueueRequestListStorageProfilesForQueuePaginateTypeDef
        ],
    ) -> _PageIterator[ListStorageProfilesForQueueResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStorageProfilesForQueue.html#DeadlineCloud.Paginator.ListStorageProfilesForQueue.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststorageprofilesforqueuepaginator)
        """

class ListStorageProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStorageProfiles.html#DeadlineCloud.Paginator.ListStorageProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststorageprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStorageProfilesRequestListStorageProfilesPaginateTypeDef]
    ) -> _PageIterator[ListStorageProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStorageProfiles.html#DeadlineCloud.Paginator.ListStorageProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststorageprofilespaginator)
        """

class ListTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListTasks.html#DeadlineCloud.Paginator.ListTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listtaskspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTasksRequestListTasksPaginateTypeDef]
    ) -> _PageIterator[ListTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListTasks.html#DeadlineCloud.Paginator.ListTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listtaskspaginator)
        """

class ListWorkersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListWorkers.html#DeadlineCloud.Paginator.ListWorkers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listworkerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListWorkersRequestListWorkersPaginateTypeDef]
    ) -> _PageIterator[ListWorkersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListWorkers.html#DeadlineCloud.Paginator.ListWorkers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listworkerspaginator)
        """
