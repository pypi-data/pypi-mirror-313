"""
Type annotations for datazone service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_datazone.client import DataZoneClient
    from mypy_boto3_datazone.paginator import (
        ListAssetFiltersPaginator,
        ListAssetRevisionsPaginator,
        ListConnectionsPaginator,
        ListDataProductRevisionsPaginator,
        ListDataSourceRunActivitiesPaginator,
        ListDataSourceRunsPaginator,
        ListDataSourcesPaginator,
        ListDomainUnitsForParentPaginator,
        ListDomainsPaginator,
        ListEntityOwnersPaginator,
        ListEnvironmentActionsPaginator,
        ListEnvironmentBlueprintConfigurationsPaginator,
        ListEnvironmentBlueprintsPaginator,
        ListEnvironmentProfilesPaginator,
        ListEnvironmentsPaginator,
        ListJobRunsPaginator,
        ListLineageEventsPaginator,
        ListLineageNodeHistoryPaginator,
        ListMetadataGenerationRunsPaginator,
        ListNotificationsPaginator,
        ListPolicyGrantsPaginator,
        ListProjectMembershipsPaginator,
        ListProjectProfilesPaginator,
        ListProjectsPaginator,
        ListRulesPaginator,
        ListSubscriptionGrantsPaginator,
        ListSubscriptionRequestsPaginator,
        ListSubscriptionTargetsPaginator,
        ListSubscriptionsPaginator,
        ListTimeSeriesDataPointsPaginator,
        SearchGroupProfilesPaginator,
        SearchListingsPaginator,
        SearchPaginator,
        SearchTypesPaginator,
        SearchUserProfilesPaginator,
    )

    session = Session()
    client: DataZoneClient = session.client("datazone")

    list_asset_filters_paginator: ListAssetFiltersPaginator = client.get_paginator("list_asset_filters")
    list_asset_revisions_paginator: ListAssetRevisionsPaginator = client.get_paginator("list_asset_revisions")
    list_connections_paginator: ListConnectionsPaginator = client.get_paginator("list_connections")
    list_data_product_revisions_paginator: ListDataProductRevisionsPaginator = client.get_paginator("list_data_product_revisions")
    list_data_source_run_activities_paginator: ListDataSourceRunActivitiesPaginator = client.get_paginator("list_data_source_run_activities")
    list_data_source_runs_paginator: ListDataSourceRunsPaginator = client.get_paginator("list_data_source_runs")
    list_data_sources_paginator: ListDataSourcesPaginator = client.get_paginator("list_data_sources")
    list_domain_units_for_parent_paginator: ListDomainUnitsForParentPaginator = client.get_paginator("list_domain_units_for_parent")
    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_entity_owners_paginator: ListEntityOwnersPaginator = client.get_paginator("list_entity_owners")
    list_environment_actions_paginator: ListEnvironmentActionsPaginator = client.get_paginator("list_environment_actions")
    list_environment_blueprint_configurations_paginator: ListEnvironmentBlueprintConfigurationsPaginator = client.get_paginator("list_environment_blueprint_configurations")
    list_environment_blueprints_paginator: ListEnvironmentBlueprintsPaginator = client.get_paginator("list_environment_blueprints")
    list_environment_profiles_paginator: ListEnvironmentProfilesPaginator = client.get_paginator("list_environment_profiles")
    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    list_job_runs_paginator: ListJobRunsPaginator = client.get_paginator("list_job_runs")
    list_lineage_events_paginator: ListLineageEventsPaginator = client.get_paginator("list_lineage_events")
    list_lineage_node_history_paginator: ListLineageNodeHistoryPaginator = client.get_paginator("list_lineage_node_history")
    list_metadata_generation_runs_paginator: ListMetadataGenerationRunsPaginator = client.get_paginator("list_metadata_generation_runs")
    list_notifications_paginator: ListNotificationsPaginator = client.get_paginator("list_notifications")
    list_policy_grants_paginator: ListPolicyGrantsPaginator = client.get_paginator("list_policy_grants")
    list_project_memberships_paginator: ListProjectMembershipsPaginator = client.get_paginator("list_project_memberships")
    list_project_profiles_paginator: ListProjectProfilesPaginator = client.get_paginator("list_project_profiles")
    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    list_subscription_grants_paginator: ListSubscriptionGrantsPaginator = client.get_paginator("list_subscription_grants")
    list_subscription_requests_paginator: ListSubscriptionRequestsPaginator = client.get_paginator("list_subscription_requests")
    list_subscription_targets_paginator: ListSubscriptionTargetsPaginator = client.get_paginator("list_subscription_targets")
    list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
    list_time_series_data_points_paginator: ListTimeSeriesDataPointsPaginator = client.get_paginator("list_time_series_data_points")
    search_group_profiles_paginator: SearchGroupProfilesPaginator = client.get_paginator("search_group_profiles")
    search_listings_paginator: SearchListingsPaginator = client.get_paginator("search_listings")
    search_paginator: SearchPaginator = client.get_paginator("search")
    search_types_paginator: SearchTypesPaginator = client.get_paginator("search_types")
    search_user_profiles_paginator: SearchUserProfilesPaginator = client.get_paginator("search_user_profiles")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAssetFiltersInputListAssetFiltersPaginateTypeDef,
    ListAssetFiltersOutputTypeDef,
    ListAssetRevisionsInputListAssetRevisionsPaginateTypeDef,
    ListAssetRevisionsOutputTypeDef,
    ListConnectionsInputListConnectionsPaginateTypeDef,
    ListConnectionsOutputTypeDef,
    ListDataProductRevisionsInputListDataProductRevisionsPaginateTypeDef,
    ListDataProductRevisionsOutputTypeDef,
    ListDataSourceRunActivitiesInputListDataSourceRunActivitiesPaginateTypeDef,
    ListDataSourceRunActivitiesOutputTypeDef,
    ListDataSourceRunsInputListDataSourceRunsPaginateTypeDef,
    ListDataSourceRunsOutputTypeDef,
    ListDataSourcesInputListDataSourcesPaginateTypeDef,
    ListDataSourcesOutputTypeDef,
    ListDomainsInputListDomainsPaginateTypeDef,
    ListDomainsOutputTypeDef,
    ListDomainUnitsForParentInputListDomainUnitsForParentPaginateTypeDef,
    ListDomainUnitsForParentOutputTypeDef,
    ListEntityOwnersInputListEntityOwnersPaginateTypeDef,
    ListEntityOwnersOutputTypeDef,
    ListEnvironmentActionsInputListEnvironmentActionsPaginateTypeDef,
    ListEnvironmentActionsOutputTypeDef,
    ListEnvironmentBlueprintConfigurationsInputListEnvironmentBlueprintConfigurationsPaginateTypeDef,
    ListEnvironmentBlueprintConfigurationsOutputTypeDef,
    ListEnvironmentBlueprintsInputListEnvironmentBlueprintsPaginateTypeDef,
    ListEnvironmentBlueprintsOutputTypeDef,
    ListEnvironmentProfilesInputListEnvironmentProfilesPaginateTypeDef,
    ListEnvironmentProfilesOutputTypeDef,
    ListEnvironmentsInputListEnvironmentsPaginateTypeDef,
    ListEnvironmentsOutputTypeDef,
    ListJobRunsInputListJobRunsPaginateTypeDef,
    ListJobRunsOutputTypeDef,
    ListLineageEventsInputListLineageEventsPaginateTypeDef,
    ListLineageEventsOutputTypeDef,
    ListLineageNodeHistoryInputListLineageNodeHistoryPaginateTypeDef,
    ListLineageNodeHistoryOutputTypeDef,
    ListMetadataGenerationRunsInputListMetadataGenerationRunsPaginateTypeDef,
    ListMetadataGenerationRunsOutputTypeDef,
    ListNotificationsInputListNotificationsPaginateTypeDef,
    ListNotificationsOutputTypeDef,
    ListPolicyGrantsInputListPolicyGrantsPaginateTypeDef,
    ListPolicyGrantsOutputTypeDef,
    ListProjectMembershipsInputListProjectMembershipsPaginateTypeDef,
    ListProjectMembershipsOutputTypeDef,
    ListProjectProfilesInputListProjectProfilesPaginateTypeDef,
    ListProjectProfilesOutputTypeDef,
    ListProjectsInputListProjectsPaginateTypeDef,
    ListProjectsOutputTypeDef,
    ListRulesInputListRulesPaginateTypeDef,
    ListRulesOutputTypeDef,
    ListSubscriptionGrantsInputListSubscriptionGrantsPaginateTypeDef,
    ListSubscriptionGrantsOutputTypeDef,
    ListSubscriptionRequestsInputListSubscriptionRequestsPaginateTypeDef,
    ListSubscriptionRequestsOutputTypeDef,
    ListSubscriptionsInputListSubscriptionsPaginateTypeDef,
    ListSubscriptionsOutputTypeDef,
    ListSubscriptionTargetsInputListSubscriptionTargetsPaginateTypeDef,
    ListSubscriptionTargetsOutputTypeDef,
    ListTimeSeriesDataPointsInputListTimeSeriesDataPointsPaginateTypeDef,
    ListTimeSeriesDataPointsOutputTypeDef,
    SearchGroupProfilesInputSearchGroupProfilesPaginateTypeDef,
    SearchGroupProfilesOutputTypeDef,
    SearchInputSearchPaginateTypeDef,
    SearchListingsInputSearchListingsPaginateTypeDef,
    SearchListingsOutputTypeDef,
    SearchOutputTypeDef,
    SearchTypesInputSearchTypesPaginateTypeDef,
    SearchTypesOutputTypeDef,
    SearchUserProfilesInputSearchUserProfilesPaginateTypeDef,
    SearchUserProfilesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAssetFiltersPaginator",
    "ListAssetRevisionsPaginator",
    "ListConnectionsPaginator",
    "ListDataProductRevisionsPaginator",
    "ListDataSourceRunActivitiesPaginator",
    "ListDataSourceRunsPaginator",
    "ListDataSourcesPaginator",
    "ListDomainUnitsForParentPaginator",
    "ListDomainsPaginator",
    "ListEntityOwnersPaginator",
    "ListEnvironmentActionsPaginator",
    "ListEnvironmentBlueprintConfigurationsPaginator",
    "ListEnvironmentBlueprintsPaginator",
    "ListEnvironmentProfilesPaginator",
    "ListEnvironmentsPaginator",
    "ListJobRunsPaginator",
    "ListLineageEventsPaginator",
    "ListLineageNodeHistoryPaginator",
    "ListMetadataGenerationRunsPaginator",
    "ListNotificationsPaginator",
    "ListPolicyGrantsPaginator",
    "ListProjectMembershipsPaginator",
    "ListProjectProfilesPaginator",
    "ListProjectsPaginator",
    "ListRulesPaginator",
    "ListSubscriptionGrantsPaginator",
    "ListSubscriptionRequestsPaginator",
    "ListSubscriptionTargetsPaginator",
    "ListSubscriptionsPaginator",
    "ListTimeSeriesDataPointsPaginator",
    "SearchGroupProfilesPaginator",
    "SearchListingsPaginator",
    "SearchPaginator",
    "SearchTypesPaginator",
    "SearchUserProfilesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAssetFiltersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListAssetFilters.html#DataZone.Paginator.ListAssetFilters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listassetfilterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAssetFiltersInputListAssetFiltersPaginateTypeDef]
    ) -> _PageIterator[ListAssetFiltersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListAssetFilters.html#DataZone.Paginator.ListAssetFilters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listassetfilterspaginator)
        """

class ListAssetRevisionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListAssetRevisions.html#DataZone.Paginator.ListAssetRevisions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listassetrevisionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAssetRevisionsInputListAssetRevisionsPaginateTypeDef]
    ) -> _PageIterator[ListAssetRevisionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListAssetRevisions.html#DataZone.Paginator.ListAssetRevisions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listassetrevisionspaginator)
        """

class ListConnectionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListConnections.html#DataZone.Paginator.ListConnections)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listconnectionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListConnectionsInputListConnectionsPaginateTypeDef]
    ) -> _PageIterator[ListConnectionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListConnections.html#DataZone.Paginator.ListConnections.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listconnectionspaginator)
        """

class ListDataProductRevisionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataProductRevisions.html#DataZone.Paginator.ListDataProductRevisions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listdataproductrevisionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataProductRevisionsInputListDataProductRevisionsPaginateTypeDef]
    ) -> _PageIterator[ListDataProductRevisionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataProductRevisions.html#DataZone.Paginator.ListDataProductRevisions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listdataproductrevisionspaginator)
        """

class ListDataSourceRunActivitiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSourceRunActivities.html#DataZone.Paginator.ListDataSourceRunActivities)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listdatasourcerunactivitiespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListDataSourceRunActivitiesInputListDataSourceRunActivitiesPaginateTypeDef
        ],
    ) -> _PageIterator[ListDataSourceRunActivitiesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSourceRunActivities.html#DataZone.Paginator.ListDataSourceRunActivities.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listdatasourcerunactivitiespaginator)
        """

class ListDataSourceRunsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSourceRuns.html#DataZone.Paginator.ListDataSourceRuns)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listdatasourcerunspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataSourceRunsInputListDataSourceRunsPaginateTypeDef]
    ) -> _PageIterator[ListDataSourceRunsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSourceRuns.html#DataZone.Paginator.ListDataSourceRuns.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listdatasourcerunspaginator)
        """

class ListDataSourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSources.html#DataZone.Paginator.ListDataSources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listdatasourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataSourcesInputListDataSourcesPaginateTypeDef]
    ) -> _PageIterator[ListDataSourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSources.html#DataZone.Paginator.ListDataSources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listdatasourcespaginator)
        """

class ListDomainUnitsForParentPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDomainUnitsForParent.html#DataZone.Paginator.ListDomainUnitsForParent)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listdomainunitsforparentpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDomainUnitsForParentInputListDomainUnitsForParentPaginateTypeDef]
    ) -> _PageIterator[ListDomainUnitsForParentOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDomainUnitsForParent.html#DataZone.Paginator.ListDomainUnitsForParent.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listdomainunitsforparentpaginator)
        """

class ListDomainsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDomains.html#DataZone.Paginator.ListDomains)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listdomainspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDomainsInputListDomainsPaginateTypeDef]
    ) -> _PageIterator[ListDomainsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDomains.html#DataZone.Paginator.ListDomains.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listdomainspaginator)
        """

class ListEntityOwnersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEntityOwners.html#DataZone.Paginator.ListEntityOwners)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listentityownerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEntityOwnersInputListEntityOwnersPaginateTypeDef]
    ) -> _PageIterator[ListEntityOwnersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEntityOwners.html#DataZone.Paginator.ListEntityOwners.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listentityownerspaginator)
        """

class ListEnvironmentActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentActions.html#DataZone.Paginator.ListEnvironmentActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listenvironmentactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEnvironmentActionsInputListEnvironmentActionsPaginateTypeDef]
    ) -> _PageIterator[ListEnvironmentActionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentActions.html#DataZone.Paginator.ListEnvironmentActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listenvironmentactionspaginator)
        """

class ListEnvironmentBlueprintConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentBlueprintConfigurations.html#DataZone.Paginator.ListEnvironmentBlueprintConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listenvironmentblueprintconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListEnvironmentBlueprintConfigurationsInputListEnvironmentBlueprintConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListEnvironmentBlueprintConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentBlueprintConfigurations.html#DataZone.Paginator.ListEnvironmentBlueprintConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listenvironmentblueprintconfigurationspaginator)
        """

class ListEnvironmentBlueprintsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentBlueprints.html#DataZone.Paginator.ListEnvironmentBlueprints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listenvironmentblueprintspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListEnvironmentBlueprintsInputListEnvironmentBlueprintsPaginateTypeDef],
    ) -> _PageIterator[ListEnvironmentBlueprintsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentBlueprints.html#DataZone.Paginator.ListEnvironmentBlueprints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listenvironmentblueprintspaginator)
        """

class ListEnvironmentProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentProfiles.html#DataZone.Paginator.ListEnvironmentProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listenvironmentprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEnvironmentProfilesInputListEnvironmentProfilesPaginateTypeDef]
    ) -> _PageIterator[ListEnvironmentProfilesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentProfiles.html#DataZone.Paginator.ListEnvironmentProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listenvironmentprofilespaginator)
        """

class ListEnvironmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironments.html#DataZone.Paginator.ListEnvironments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listenvironmentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEnvironmentsInputListEnvironmentsPaginateTypeDef]
    ) -> _PageIterator[ListEnvironmentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironments.html#DataZone.Paginator.ListEnvironments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listenvironmentspaginator)
        """

class ListJobRunsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListJobRuns.html#DataZone.Paginator.ListJobRuns)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listjobrunspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobRunsInputListJobRunsPaginateTypeDef]
    ) -> _PageIterator[ListJobRunsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListJobRuns.html#DataZone.Paginator.ListJobRuns.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listjobrunspaginator)
        """

class ListLineageEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListLineageEvents.html#DataZone.Paginator.ListLineageEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listlineageeventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLineageEventsInputListLineageEventsPaginateTypeDef]
    ) -> _PageIterator[ListLineageEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListLineageEvents.html#DataZone.Paginator.ListLineageEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listlineageeventspaginator)
        """

class ListLineageNodeHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListLineageNodeHistory.html#DataZone.Paginator.ListLineageNodeHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listlineagenodehistorypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLineageNodeHistoryInputListLineageNodeHistoryPaginateTypeDef]
    ) -> _PageIterator[ListLineageNodeHistoryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListLineageNodeHistory.html#DataZone.Paginator.ListLineageNodeHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listlineagenodehistorypaginator)
        """

class ListMetadataGenerationRunsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListMetadataGenerationRuns.html#DataZone.Paginator.ListMetadataGenerationRuns)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listmetadatagenerationrunspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListMetadataGenerationRunsInputListMetadataGenerationRunsPaginateTypeDef],
    ) -> _PageIterator[ListMetadataGenerationRunsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListMetadataGenerationRuns.html#DataZone.Paginator.ListMetadataGenerationRuns.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listmetadatagenerationrunspaginator)
        """

class ListNotificationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListNotifications.html#DataZone.Paginator.ListNotifications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listnotificationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListNotificationsInputListNotificationsPaginateTypeDef]
    ) -> _PageIterator[ListNotificationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListNotifications.html#DataZone.Paginator.ListNotifications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listnotificationspaginator)
        """

class ListPolicyGrantsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListPolicyGrants.html#DataZone.Paginator.ListPolicyGrants)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listpolicygrantspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPolicyGrantsInputListPolicyGrantsPaginateTypeDef]
    ) -> _PageIterator[ListPolicyGrantsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListPolicyGrants.html#DataZone.Paginator.ListPolicyGrants.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listpolicygrantspaginator)
        """

class ListProjectMembershipsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListProjectMemberships.html#DataZone.Paginator.ListProjectMemberships)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listprojectmembershipspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProjectMembershipsInputListProjectMembershipsPaginateTypeDef]
    ) -> _PageIterator[ListProjectMembershipsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListProjectMemberships.html#DataZone.Paginator.ListProjectMemberships.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listprojectmembershipspaginator)
        """

class ListProjectProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListProjectProfiles.html#DataZone.Paginator.ListProjectProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listprojectprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProjectProfilesInputListProjectProfilesPaginateTypeDef]
    ) -> _PageIterator[ListProjectProfilesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListProjectProfiles.html#DataZone.Paginator.ListProjectProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listprojectprofilespaginator)
        """

class ListProjectsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListProjects.html#DataZone.Paginator.ListProjects)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listprojectspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProjectsInputListProjectsPaginateTypeDef]
    ) -> _PageIterator[ListProjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListProjects.html#DataZone.Paginator.ListProjects.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listprojectspaginator)
        """

class ListRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListRules.html#DataZone.Paginator.ListRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listrulespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRulesInputListRulesPaginateTypeDef]
    ) -> _PageIterator[ListRulesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListRules.html#DataZone.Paginator.ListRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listrulespaginator)
        """

class ListSubscriptionGrantsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionGrants.html#DataZone.Paginator.ListSubscriptionGrants)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listsubscriptiongrantspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSubscriptionGrantsInputListSubscriptionGrantsPaginateTypeDef]
    ) -> _PageIterator[ListSubscriptionGrantsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionGrants.html#DataZone.Paginator.ListSubscriptionGrants.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listsubscriptiongrantspaginator)
        """

class ListSubscriptionRequestsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionRequests.html#DataZone.Paginator.ListSubscriptionRequests)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listsubscriptionrequestspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSubscriptionRequestsInputListSubscriptionRequestsPaginateTypeDef]
    ) -> _PageIterator[ListSubscriptionRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionRequests.html#DataZone.Paginator.ListSubscriptionRequests.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listsubscriptionrequestspaginator)
        """

class ListSubscriptionTargetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionTargets.html#DataZone.Paginator.ListSubscriptionTargets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listsubscriptiontargetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSubscriptionTargetsInputListSubscriptionTargetsPaginateTypeDef]
    ) -> _PageIterator[ListSubscriptionTargetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionTargets.html#DataZone.Paginator.ListSubscriptionTargets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listsubscriptiontargetspaginator)
        """

class ListSubscriptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptions.html#DataZone.Paginator.ListSubscriptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listsubscriptionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSubscriptionsInputListSubscriptionsPaginateTypeDef]
    ) -> _PageIterator[ListSubscriptionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptions.html#DataZone.Paginator.ListSubscriptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listsubscriptionspaginator)
        """

class ListTimeSeriesDataPointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListTimeSeriesDataPoints.html#DataZone.Paginator.ListTimeSeriesDataPoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listtimeseriesdatapointspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTimeSeriesDataPointsInputListTimeSeriesDataPointsPaginateTypeDef]
    ) -> _PageIterator[ListTimeSeriesDataPointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListTimeSeriesDataPoints.html#DataZone.Paginator.ListTimeSeriesDataPoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#listtimeseriesdatapointspaginator)
        """

class SearchGroupProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchGroupProfiles.html#DataZone.Paginator.SearchGroupProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#searchgroupprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchGroupProfilesInputSearchGroupProfilesPaginateTypeDef]
    ) -> _PageIterator[SearchGroupProfilesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchGroupProfiles.html#DataZone.Paginator.SearchGroupProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#searchgroupprofilespaginator)
        """

class SearchListingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchListings.html#DataZone.Paginator.SearchListings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#searchlistingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchListingsInputSearchListingsPaginateTypeDef]
    ) -> _PageIterator[SearchListingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchListings.html#DataZone.Paginator.SearchListings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#searchlistingspaginator)
        """

class SearchPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/Search.html#DataZone.Paginator.Search)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#searchpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchInputSearchPaginateTypeDef]
    ) -> _PageIterator[SearchOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/Search.html#DataZone.Paginator.Search.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#searchpaginator)
        """

class SearchTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchTypes.html#DataZone.Paginator.SearchTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#searchtypespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchTypesInputSearchTypesPaginateTypeDef]
    ) -> _PageIterator[SearchTypesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchTypes.html#DataZone.Paginator.SearchTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#searchtypespaginator)
        """

class SearchUserProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchUserProfiles.html#DataZone.Paginator.SearchUserProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#searchuserprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchUserProfilesInputSearchUserProfilesPaginateTypeDef]
    ) -> _PageIterator[SearchUserProfilesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchUserProfiles.html#DataZone.Paginator.SearchUserProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/paginators/#searchuserprofilespaginator)
        """
