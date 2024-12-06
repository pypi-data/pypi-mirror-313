"""
Type annotations for gamelift service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_gamelift.client import GameLiftClient
    from mypy_boto3_gamelift.paginator import (
        DescribeFleetAttributesPaginator,
        DescribeFleetCapacityPaginator,
        DescribeFleetEventsPaginator,
        DescribeFleetUtilizationPaginator,
        DescribeGameServerInstancesPaginator,
        DescribeGameSessionDetailsPaginator,
        DescribeGameSessionQueuesPaginator,
        DescribeGameSessionsPaginator,
        DescribeInstancesPaginator,
        DescribeMatchmakingConfigurationsPaginator,
        DescribeMatchmakingRuleSetsPaginator,
        DescribePlayerSessionsPaginator,
        DescribeScalingPoliciesPaginator,
        ListAliasesPaginator,
        ListBuildsPaginator,
        ListComputePaginator,
        ListContainerFleetsPaginator,
        ListContainerGroupDefinitionVersionsPaginator,
        ListContainerGroupDefinitionsPaginator,
        ListFleetDeploymentsPaginator,
        ListFleetsPaginator,
        ListGameServerGroupsPaginator,
        ListGameServersPaginator,
        ListLocationsPaginator,
        ListScriptsPaginator,
        SearchGameSessionsPaginator,
    )

    session = Session()
    client: GameLiftClient = session.client("gamelift")

    describe_fleet_attributes_paginator: DescribeFleetAttributesPaginator = client.get_paginator("describe_fleet_attributes")
    describe_fleet_capacity_paginator: DescribeFleetCapacityPaginator = client.get_paginator("describe_fleet_capacity")
    describe_fleet_events_paginator: DescribeFleetEventsPaginator = client.get_paginator("describe_fleet_events")
    describe_fleet_utilization_paginator: DescribeFleetUtilizationPaginator = client.get_paginator("describe_fleet_utilization")
    describe_game_server_instances_paginator: DescribeGameServerInstancesPaginator = client.get_paginator("describe_game_server_instances")
    describe_game_session_details_paginator: DescribeGameSessionDetailsPaginator = client.get_paginator("describe_game_session_details")
    describe_game_session_queues_paginator: DescribeGameSessionQueuesPaginator = client.get_paginator("describe_game_session_queues")
    describe_game_sessions_paginator: DescribeGameSessionsPaginator = client.get_paginator("describe_game_sessions")
    describe_instances_paginator: DescribeInstancesPaginator = client.get_paginator("describe_instances")
    describe_matchmaking_configurations_paginator: DescribeMatchmakingConfigurationsPaginator = client.get_paginator("describe_matchmaking_configurations")
    describe_matchmaking_rule_sets_paginator: DescribeMatchmakingRuleSetsPaginator = client.get_paginator("describe_matchmaking_rule_sets")
    describe_player_sessions_paginator: DescribePlayerSessionsPaginator = client.get_paginator("describe_player_sessions")
    describe_scaling_policies_paginator: DescribeScalingPoliciesPaginator = client.get_paginator("describe_scaling_policies")
    list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
    list_builds_paginator: ListBuildsPaginator = client.get_paginator("list_builds")
    list_compute_paginator: ListComputePaginator = client.get_paginator("list_compute")
    list_container_fleets_paginator: ListContainerFleetsPaginator = client.get_paginator("list_container_fleets")
    list_container_group_definition_versions_paginator: ListContainerGroupDefinitionVersionsPaginator = client.get_paginator("list_container_group_definition_versions")
    list_container_group_definitions_paginator: ListContainerGroupDefinitionsPaginator = client.get_paginator("list_container_group_definitions")
    list_fleet_deployments_paginator: ListFleetDeploymentsPaginator = client.get_paginator("list_fleet_deployments")
    list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
    list_game_server_groups_paginator: ListGameServerGroupsPaginator = client.get_paginator("list_game_server_groups")
    list_game_servers_paginator: ListGameServersPaginator = client.get_paginator("list_game_servers")
    list_locations_paginator: ListLocationsPaginator = client.get_paginator("list_locations")
    list_scripts_paginator: ListScriptsPaginator = client.get_paginator("list_scripts")
    search_game_sessions_paginator: SearchGameSessionsPaginator = client.get_paginator("search_game_sessions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeFleetAttributesInputDescribeFleetAttributesPaginateTypeDef,
    DescribeFleetAttributesOutputTypeDef,
    DescribeFleetCapacityInputDescribeFleetCapacityPaginateTypeDef,
    DescribeFleetCapacityOutputTypeDef,
    DescribeFleetEventsInputDescribeFleetEventsPaginateTypeDef,
    DescribeFleetEventsOutputTypeDef,
    DescribeFleetUtilizationInputDescribeFleetUtilizationPaginateTypeDef,
    DescribeFleetUtilizationOutputTypeDef,
    DescribeGameServerInstancesInputDescribeGameServerInstancesPaginateTypeDef,
    DescribeGameServerInstancesOutputTypeDef,
    DescribeGameSessionDetailsInputDescribeGameSessionDetailsPaginateTypeDef,
    DescribeGameSessionDetailsOutputTypeDef,
    DescribeGameSessionQueuesInputDescribeGameSessionQueuesPaginateTypeDef,
    DescribeGameSessionQueuesOutputTypeDef,
    DescribeGameSessionsInputDescribeGameSessionsPaginateTypeDef,
    DescribeGameSessionsOutputTypeDef,
    DescribeInstancesInputDescribeInstancesPaginateTypeDef,
    DescribeInstancesOutputTypeDef,
    DescribeMatchmakingConfigurationsInputDescribeMatchmakingConfigurationsPaginateTypeDef,
    DescribeMatchmakingConfigurationsOutputTypeDef,
    DescribeMatchmakingRuleSetsInputDescribeMatchmakingRuleSetsPaginateTypeDef,
    DescribeMatchmakingRuleSetsOutputTypeDef,
    DescribePlayerSessionsInputDescribePlayerSessionsPaginateTypeDef,
    DescribePlayerSessionsOutputTypeDef,
    DescribeScalingPoliciesInputDescribeScalingPoliciesPaginateTypeDef,
    DescribeScalingPoliciesOutputTypeDef,
    ListAliasesInputListAliasesPaginateTypeDef,
    ListAliasesOutputTypeDef,
    ListBuildsInputListBuildsPaginateTypeDef,
    ListBuildsOutputTypeDef,
    ListComputeInputListComputePaginateTypeDef,
    ListComputeOutputTypeDef,
    ListContainerFleetsInputListContainerFleetsPaginateTypeDef,
    ListContainerFleetsOutputTypeDef,
    ListContainerGroupDefinitionsInputListContainerGroupDefinitionsPaginateTypeDef,
    ListContainerGroupDefinitionsOutputTypeDef,
    ListContainerGroupDefinitionVersionsInputListContainerGroupDefinitionVersionsPaginateTypeDef,
    ListContainerGroupDefinitionVersionsOutputTypeDef,
    ListFleetDeploymentsInputListFleetDeploymentsPaginateTypeDef,
    ListFleetDeploymentsOutputTypeDef,
    ListFleetsInputListFleetsPaginateTypeDef,
    ListFleetsOutputTypeDef,
    ListGameServerGroupsInputListGameServerGroupsPaginateTypeDef,
    ListGameServerGroupsOutputTypeDef,
    ListGameServersInputListGameServersPaginateTypeDef,
    ListGameServersOutputTypeDef,
    ListLocationsInputListLocationsPaginateTypeDef,
    ListLocationsOutputTypeDef,
    ListScriptsInputListScriptsPaginateTypeDef,
    ListScriptsOutputTypeDef,
    SearchGameSessionsInputSearchGameSessionsPaginateTypeDef,
    SearchGameSessionsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeFleetAttributesPaginator",
    "DescribeFleetCapacityPaginator",
    "DescribeFleetEventsPaginator",
    "DescribeFleetUtilizationPaginator",
    "DescribeGameServerInstancesPaginator",
    "DescribeGameSessionDetailsPaginator",
    "DescribeGameSessionQueuesPaginator",
    "DescribeGameSessionsPaginator",
    "DescribeInstancesPaginator",
    "DescribeMatchmakingConfigurationsPaginator",
    "DescribeMatchmakingRuleSetsPaginator",
    "DescribePlayerSessionsPaginator",
    "DescribeScalingPoliciesPaginator",
    "ListAliasesPaginator",
    "ListBuildsPaginator",
    "ListComputePaginator",
    "ListContainerFleetsPaginator",
    "ListContainerGroupDefinitionVersionsPaginator",
    "ListContainerGroupDefinitionsPaginator",
    "ListFleetDeploymentsPaginator",
    "ListFleetsPaginator",
    "ListGameServerGroupsPaginator",
    "ListGameServersPaginator",
    "ListLocationsPaginator",
    "ListScriptsPaginator",
    "SearchGameSessionsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeFleetAttributesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetAttributes.html#GameLift.Paginator.DescribeFleetAttributes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetattributespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeFleetAttributesInputDescribeFleetAttributesPaginateTypeDef]
    ) -> _PageIterator[DescribeFleetAttributesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetAttributes.html#GameLift.Paginator.DescribeFleetAttributes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetattributespaginator)
        """

class DescribeFleetCapacityPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetCapacity.html#GameLift.Paginator.DescribeFleetCapacity)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetcapacitypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeFleetCapacityInputDescribeFleetCapacityPaginateTypeDef]
    ) -> _PageIterator[DescribeFleetCapacityOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetCapacity.html#GameLift.Paginator.DescribeFleetCapacity.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetcapacitypaginator)
        """

class DescribeFleetEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetEvents.html#GameLift.Paginator.DescribeFleetEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleeteventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeFleetEventsInputDescribeFleetEventsPaginateTypeDef]
    ) -> _PageIterator[DescribeFleetEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetEvents.html#GameLift.Paginator.DescribeFleetEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleeteventspaginator)
        """

class DescribeFleetUtilizationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetUtilization.html#GameLift.Paginator.DescribeFleetUtilization)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetutilizationpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeFleetUtilizationInputDescribeFleetUtilizationPaginateTypeDef]
    ) -> _PageIterator[DescribeFleetUtilizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetUtilization.html#GameLift.Paginator.DescribeFleetUtilization.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetutilizationpaginator)
        """

class DescribeGameServerInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameServerInstances.html#GameLift.Paginator.DescribeGameServerInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegameserverinstancespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeGameServerInstancesInputDescribeGameServerInstancesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeGameServerInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameServerInstances.html#GameLift.Paginator.DescribeGameServerInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegameserverinstancespaginator)
        """

class DescribeGameSessionDetailsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessionDetails.html#GameLift.Paginator.DescribeGameSessionDetails)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessiondetailspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeGameSessionDetailsInputDescribeGameSessionDetailsPaginateTypeDef],
    ) -> _PageIterator[DescribeGameSessionDetailsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessionDetails.html#GameLift.Paginator.DescribeGameSessionDetails.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessiondetailspaginator)
        """

class DescribeGameSessionQueuesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessionQueues.html#GameLift.Paginator.DescribeGameSessionQueues)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessionqueuespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeGameSessionQueuesInputDescribeGameSessionQueuesPaginateTypeDef],
    ) -> _PageIterator[DescribeGameSessionQueuesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessionQueues.html#GameLift.Paginator.DescribeGameSessionQueues.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessionqueuespaginator)
        """

class DescribeGameSessionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessions.html#GameLift.Paginator.DescribeGameSessions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeGameSessionsInputDescribeGameSessionsPaginateTypeDef]
    ) -> _PageIterator[DescribeGameSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessions.html#GameLift.Paginator.DescribeGameSessions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessionspaginator)
        """

class DescribeInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeInstances.html#GameLift.Paginator.DescribeInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describeinstancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeInstancesInputDescribeInstancesPaginateTypeDef]
    ) -> _PageIterator[DescribeInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeInstances.html#GameLift.Paginator.DescribeInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describeinstancespaginator)
        """

class DescribeMatchmakingConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeMatchmakingConfigurations.html#GameLift.Paginator.DescribeMatchmakingConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describematchmakingconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMatchmakingConfigurationsInputDescribeMatchmakingConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeMatchmakingConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeMatchmakingConfigurations.html#GameLift.Paginator.DescribeMatchmakingConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describematchmakingconfigurationspaginator)
        """

class DescribeMatchmakingRuleSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeMatchmakingRuleSets.html#GameLift.Paginator.DescribeMatchmakingRuleSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describematchmakingrulesetspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMatchmakingRuleSetsInputDescribeMatchmakingRuleSetsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeMatchmakingRuleSetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeMatchmakingRuleSets.html#GameLift.Paginator.DescribeMatchmakingRuleSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describematchmakingrulesetspaginator)
        """

class DescribePlayerSessionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribePlayerSessions.html#GameLift.Paginator.DescribePlayerSessions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describeplayersessionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribePlayerSessionsInputDescribePlayerSessionsPaginateTypeDef]
    ) -> _PageIterator[DescribePlayerSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribePlayerSessions.html#GameLift.Paginator.DescribePlayerSessions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describeplayersessionspaginator)
        """

class DescribeScalingPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeScalingPolicies.html#GameLift.Paginator.DescribeScalingPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describescalingpoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeScalingPoliciesInputDescribeScalingPoliciesPaginateTypeDef]
    ) -> _PageIterator[DescribeScalingPoliciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeScalingPolicies.html#GameLift.Paginator.DescribeScalingPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describescalingpoliciespaginator)
        """

class ListAliasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListAliases.html#GameLift.Paginator.ListAliases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listaliasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAliasesInputListAliasesPaginateTypeDef]
    ) -> _PageIterator[ListAliasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListAliases.html#GameLift.Paginator.ListAliases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listaliasespaginator)
        """

class ListBuildsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListBuilds.html#GameLift.Paginator.ListBuilds)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listbuildspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBuildsInputListBuildsPaginateTypeDef]
    ) -> _PageIterator[ListBuildsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListBuilds.html#GameLift.Paginator.ListBuilds.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listbuildspaginator)
        """

class ListComputePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListCompute.html#GameLift.Paginator.ListCompute)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listcomputepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListComputeInputListComputePaginateTypeDef]
    ) -> _PageIterator[ListComputeOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListCompute.html#GameLift.Paginator.ListCompute.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listcomputepaginator)
        """

class ListContainerFleetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerFleets.html#GameLift.Paginator.ListContainerFleets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listcontainerfleetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListContainerFleetsInputListContainerFleetsPaginateTypeDef]
    ) -> _PageIterator[ListContainerFleetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerFleets.html#GameLift.Paginator.ListContainerFleets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listcontainerfleetspaginator)
        """

class ListContainerGroupDefinitionVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerGroupDefinitionVersions.html#GameLift.Paginator.ListContainerGroupDefinitionVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listcontainergroupdefinitionversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListContainerGroupDefinitionVersionsInputListContainerGroupDefinitionVersionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListContainerGroupDefinitionVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerGroupDefinitionVersions.html#GameLift.Paginator.ListContainerGroupDefinitionVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listcontainergroupdefinitionversionspaginator)
        """

class ListContainerGroupDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerGroupDefinitions.html#GameLift.Paginator.ListContainerGroupDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listcontainergroupdefinitionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListContainerGroupDefinitionsInputListContainerGroupDefinitionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListContainerGroupDefinitionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerGroupDefinitions.html#GameLift.Paginator.ListContainerGroupDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listcontainergroupdefinitionspaginator)
        """

class ListFleetDeploymentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListFleetDeployments.html#GameLift.Paginator.ListFleetDeployments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listfleetdeploymentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFleetDeploymentsInputListFleetDeploymentsPaginateTypeDef]
    ) -> _PageIterator[ListFleetDeploymentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListFleetDeployments.html#GameLift.Paginator.ListFleetDeployments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listfleetdeploymentspaginator)
        """

class ListFleetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListFleets.html#GameLift.Paginator.ListFleets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listfleetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFleetsInputListFleetsPaginateTypeDef]
    ) -> _PageIterator[ListFleetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListFleets.html#GameLift.Paginator.ListFleets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listfleetspaginator)
        """

class ListGameServerGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListGameServerGroups.html#GameLift.Paginator.ListGameServerGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listgameservergroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGameServerGroupsInputListGameServerGroupsPaginateTypeDef]
    ) -> _PageIterator[ListGameServerGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListGameServerGroups.html#GameLift.Paginator.ListGameServerGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listgameservergroupspaginator)
        """

class ListGameServersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListGameServers.html#GameLift.Paginator.ListGameServers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listgameserverspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGameServersInputListGameServersPaginateTypeDef]
    ) -> _PageIterator[ListGameServersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListGameServers.html#GameLift.Paginator.ListGameServers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listgameserverspaginator)
        """

class ListLocationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListLocations.html#GameLift.Paginator.ListLocations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listlocationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLocationsInputListLocationsPaginateTypeDef]
    ) -> _PageIterator[ListLocationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListLocations.html#GameLift.Paginator.ListLocations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listlocationspaginator)
        """

class ListScriptsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListScripts.html#GameLift.Paginator.ListScripts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listscriptspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListScriptsInputListScriptsPaginateTypeDef]
    ) -> _PageIterator[ListScriptsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListScripts.html#GameLift.Paginator.ListScripts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listscriptspaginator)
        """

class SearchGameSessionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/SearchGameSessions.html#GameLift.Paginator.SearchGameSessions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#searchgamesessionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchGameSessionsInputSearchGameSessionsPaginateTypeDef]
    ) -> _PageIterator[SearchGameSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/SearchGameSessions.html#GameLift.Paginator.SearchGameSessions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#searchgamesessionspaginator)
        """
