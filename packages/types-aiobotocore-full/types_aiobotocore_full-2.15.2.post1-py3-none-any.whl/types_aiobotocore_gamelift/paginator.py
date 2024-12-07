"""
Type annotations for gamelift service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_gamelift.client import GameLiftClient
    from types_aiobotocore_gamelift.paginator import (
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
        ListContainerGroupDefinitionsPaginator,
        ListFleetsPaginator,
        ListGameServerGroupsPaginator,
        ListGameServersPaginator,
        ListLocationsPaginator,
        ListScriptsPaginator,
        SearchGameSessionsPaginator,
    )

    session = get_session()
    with session.create_client("gamelift") as client:
        client: GameLiftClient

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
        list_container_group_definitions_paginator: ListContainerGroupDefinitionsPaginator = client.get_paginator("list_container_group_definitions")
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
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

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
    ListContainerGroupDefinitionsInputListContainerGroupDefinitionsPaginateTypeDef,
    ListContainerGroupDefinitionsOutputTypeDef,
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
    "ListContainerGroupDefinitionsPaginator",
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


class DescribeFleetAttributesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetAttributes.html#GameLift.Paginator.DescribeFleetAttributes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetattributespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeFleetAttributesInputDescribeFleetAttributesPaginateTypeDef]
    ) -> AsyncIterator[DescribeFleetAttributesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetAttributes.html#GameLift.Paginator.DescribeFleetAttributes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetattributespaginator)
        """


class DescribeFleetCapacityPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetCapacity.html#GameLift.Paginator.DescribeFleetCapacity)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetcapacitypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeFleetCapacityInputDescribeFleetCapacityPaginateTypeDef]
    ) -> AsyncIterator[DescribeFleetCapacityOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetCapacity.html#GameLift.Paginator.DescribeFleetCapacity.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetcapacitypaginator)
        """


class DescribeFleetEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetEvents.html#GameLift.Paginator.DescribeFleetEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleeteventspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeFleetEventsInputDescribeFleetEventsPaginateTypeDef]
    ) -> AsyncIterator[DescribeFleetEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetEvents.html#GameLift.Paginator.DescribeFleetEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleeteventspaginator)
        """


class DescribeFleetUtilizationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetUtilization.html#GameLift.Paginator.DescribeFleetUtilization)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetutilizationpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeFleetUtilizationInputDescribeFleetUtilizationPaginateTypeDef]
    ) -> AsyncIterator[DescribeFleetUtilizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetUtilization.html#GameLift.Paginator.DescribeFleetUtilization.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetutilizationpaginator)
        """


class DescribeGameServerInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameServerInstances.html#GameLift.Paginator.DescribeGameServerInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegameserverinstancespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeGameServerInstancesInputDescribeGameServerInstancesPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeGameServerInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameServerInstances.html#GameLift.Paginator.DescribeGameServerInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegameserverinstancespaginator)
        """


class DescribeGameSessionDetailsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessionDetails.html#GameLift.Paginator.DescribeGameSessionDetails)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessiondetailspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeGameSessionDetailsInputDescribeGameSessionDetailsPaginateTypeDef],
    ) -> AsyncIterator[DescribeGameSessionDetailsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessionDetails.html#GameLift.Paginator.DescribeGameSessionDetails.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessiondetailspaginator)
        """


class DescribeGameSessionQueuesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessionQueues.html#GameLift.Paginator.DescribeGameSessionQueues)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessionqueuespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeGameSessionQueuesInputDescribeGameSessionQueuesPaginateTypeDef],
    ) -> AsyncIterator[DescribeGameSessionQueuesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessionQueues.html#GameLift.Paginator.DescribeGameSessionQueues.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessionqueuespaginator)
        """


class DescribeGameSessionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessions.html#GameLift.Paginator.DescribeGameSessions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeGameSessionsInputDescribeGameSessionsPaginateTypeDef]
    ) -> AsyncIterator[DescribeGameSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessions.html#GameLift.Paginator.DescribeGameSessions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessionspaginator)
        """


class DescribeInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeInstances.html#GameLift.Paginator.DescribeInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describeinstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeInstancesInputDescribeInstancesPaginateTypeDef]
    ) -> AsyncIterator[DescribeInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeInstances.html#GameLift.Paginator.DescribeInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describeinstancespaginator)
        """


class DescribeMatchmakingConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeMatchmakingConfigurations.html#GameLift.Paginator.DescribeMatchmakingConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describematchmakingconfigurationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMatchmakingConfigurationsInputDescribeMatchmakingConfigurationsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeMatchmakingConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeMatchmakingConfigurations.html#GameLift.Paginator.DescribeMatchmakingConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describematchmakingconfigurationspaginator)
        """


class DescribeMatchmakingRuleSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeMatchmakingRuleSets.html#GameLift.Paginator.DescribeMatchmakingRuleSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describematchmakingrulesetspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMatchmakingRuleSetsInputDescribeMatchmakingRuleSetsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeMatchmakingRuleSetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeMatchmakingRuleSets.html#GameLift.Paginator.DescribeMatchmakingRuleSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describematchmakingrulesetspaginator)
        """


class DescribePlayerSessionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribePlayerSessions.html#GameLift.Paginator.DescribePlayerSessions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describeplayersessionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribePlayerSessionsInputDescribePlayerSessionsPaginateTypeDef]
    ) -> AsyncIterator[DescribePlayerSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribePlayerSessions.html#GameLift.Paginator.DescribePlayerSessions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describeplayersessionspaginator)
        """


class DescribeScalingPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeScalingPolicies.html#GameLift.Paginator.DescribeScalingPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describescalingpoliciespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeScalingPoliciesInputDescribeScalingPoliciesPaginateTypeDef]
    ) -> AsyncIterator[DescribeScalingPoliciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeScalingPolicies.html#GameLift.Paginator.DescribeScalingPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describescalingpoliciespaginator)
        """


class ListAliasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListAliases.html#GameLift.Paginator.ListAliases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listaliasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAliasesInputListAliasesPaginateTypeDef]
    ) -> AsyncIterator[ListAliasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListAliases.html#GameLift.Paginator.ListAliases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listaliasespaginator)
        """


class ListBuildsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListBuilds.html#GameLift.Paginator.ListBuilds)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listbuildspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBuildsInputListBuildsPaginateTypeDef]
    ) -> AsyncIterator[ListBuildsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListBuilds.html#GameLift.Paginator.ListBuilds.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listbuildspaginator)
        """


class ListComputePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListCompute.html#GameLift.Paginator.ListCompute)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listcomputepaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListComputeInputListComputePaginateTypeDef]
    ) -> AsyncIterator[ListComputeOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListCompute.html#GameLift.Paginator.ListCompute.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listcomputepaginator)
        """


class ListContainerGroupDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerGroupDefinitions.html#GameLift.Paginator.ListContainerGroupDefinitions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listcontainergroupdefinitionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListContainerGroupDefinitionsInputListContainerGroupDefinitionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListContainerGroupDefinitionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerGroupDefinitions.html#GameLift.Paginator.ListContainerGroupDefinitions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listcontainergroupdefinitionspaginator)
        """


class ListFleetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListFleets.html#GameLift.Paginator.ListFleets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listfleetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFleetsInputListFleetsPaginateTypeDef]
    ) -> AsyncIterator[ListFleetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListFleets.html#GameLift.Paginator.ListFleets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listfleetspaginator)
        """


class ListGameServerGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListGameServerGroups.html#GameLift.Paginator.ListGameServerGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listgameservergroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGameServerGroupsInputListGameServerGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListGameServerGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListGameServerGroups.html#GameLift.Paginator.ListGameServerGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listgameservergroupspaginator)
        """


class ListGameServersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListGameServers.html#GameLift.Paginator.ListGameServers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listgameserverspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGameServersInputListGameServersPaginateTypeDef]
    ) -> AsyncIterator[ListGameServersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListGameServers.html#GameLift.Paginator.ListGameServers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listgameserverspaginator)
        """


class ListLocationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListLocations.html#GameLift.Paginator.ListLocations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listlocationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListLocationsInputListLocationsPaginateTypeDef]
    ) -> AsyncIterator[ListLocationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListLocations.html#GameLift.Paginator.ListLocations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listlocationspaginator)
        """


class ListScriptsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListScripts.html#GameLift.Paginator.ListScripts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listscriptspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListScriptsInputListScriptsPaginateTypeDef]
    ) -> AsyncIterator[ListScriptsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListScripts.html#GameLift.Paginator.ListScripts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listscriptspaginator)
        """


class SearchGameSessionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/SearchGameSessions.html#GameLift.Paginator.SearchGameSessions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#searchgamesessionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchGameSessionsInputSearchGameSessionsPaginateTypeDef]
    ) -> AsyncIterator[SearchGameSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/SearchGameSessions.html#GameLift.Paginator.SearchGameSessions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#searchgamesessionspaginator)
        """
