"""
Type annotations for gamelift service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_gamelift.client import GameLiftClient

    session = get_session()
    async with session.create_client("gamelift") as client:
        client: GameLiftClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
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
from .type_defs import (
    AcceptMatchInputRequestTypeDef,
    ClaimGameServerInputRequestTypeDef,
    ClaimGameServerOutputTypeDef,
    CreateAliasInputRequestTypeDef,
    CreateAliasOutputTypeDef,
    CreateBuildInputRequestTypeDef,
    CreateBuildOutputTypeDef,
    CreateContainerGroupDefinitionInputRequestTypeDef,
    CreateContainerGroupDefinitionOutputTypeDef,
    CreateFleetInputRequestTypeDef,
    CreateFleetLocationsInputRequestTypeDef,
    CreateFleetLocationsOutputTypeDef,
    CreateFleetOutputTypeDef,
    CreateGameServerGroupInputRequestTypeDef,
    CreateGameServerGroupOutputTypeDef,
    CreateGameSessionInputRequestTypeDef,
    CreateGameSessionOutputTypeDef,
    CreateGameSessionQueueInputRequestTypeDef,
    CreateGameSessionQueueOutputTypeDef,
    CreateLocationInputRequestTypeDef,
    CreateLocationOutputTypeDef,
    CreateMatchmakingConfigurationInputRequestTypeDef,
    CreateMatchmakingConfigurationOutputTypeDef,
    CreateMatchmakingRuleSetInputRequestTypeDef,
    CreateMatchmakingRuleSetOutputTypeDef,
    CreatePlayerSessionInputRequestTypeDef,
    CreatePlayerSessionOutputTypeDef,
    CreatePlayerSessionsInputRequestTypeDef,
    CreatePlayerSessionsOutputTypeDef,
    CreateScriptInputRequestTypeDef,
    CreateScriptOutputTypeDef,
    CreateVpcPeeringAuthorizationInputRequestTypeDef,
    CreateVpcPeeringAuthorizationOutputTypeDef,
    CreateVpcPeeringConnectionInputRequestTypeDef,
    DeleteAliasInputRequestTypeDef,
    DeleteBuildInputRequestTypeDef,
    DeleteContainerGroupDefinitionInputRequestTypeDef,
    DeleteFleetInputRequestTypeDef,
    DeleteFleetLocationsInputRequestTypeDef,
    DeleteFleetLocationsOutputTypeDef,
    DeleteGameServerGroupInputRequestTypeDef,
    DeleteGameServerGroupOutputTypeDef,
    DeleteGameSessionQueueInputRequestTypeDef,
    DeleteLocationInputRequestTypeDef,
    DeleteMatchmakingConfigurationInputRequestTypeDef,
    DeleteMatchmakingRuleSetInputRequestTypeDef,
    DeleteScalingPolicyInputRequestTypeDef,
    DeleteScriptInputRequestTypeDef,
    DeleteVpcPeeringAuthorizationInputRequestTypeDef,
    DeleteVpcPeeringConnectionInputRequestTypeDef,
    DeregisterComputeInputRequestTypeDef,
    DeregisterGameServerInputRequestTypeDef,
    DescribeAliasInputRequestTypeDef,
    DescribeAliasOutputTypeDef,
    DescribeBuildInputRequestTypeDef,
    DescribeBuildOutputTypeDef,
    DescribeComputeInputRequestTypeDef,
    DescribeComputeOutputTypeDef,
    DescribeContainerGroupDefinitionInputRequestTypeDef,
    DescribeContainerGroupDefinitionOutputTypeDef,
    DescribeEC2InstanceLimitsInputRequestTypeDef,
    DescribeEC2InstanceLimitsOutputTypeDef,
    DescribeFleetAttributesInputRequestTypeDef,
    DescribeFleetAttributesOutputTypeDef,
    DescribeFleetCapacityInputRequestTypeDef,
    DescribeFleetCapacityOutputTypeDef,
    DescribeFleetEventsInputRequestTypeDef,
    DescribeFleetEventsOutputTypeDef,
    DescribeFleetLocationAttributesInputRequestTypeDef,
    DescribeFleetLocationAttributesOutputTypeDef,
    DescribeFleetLocationCapacityInputRequestTypeDef,
    DescribeFleetLocationCapacityOutputTypeDef,
    DescribeFleetLocationUtilizationInputRequestTypeDef,
    DescribeFleetLocationUtilizationOutputTypeDef,
    DescribeFleetPortSettingsInputRequestTypeDef,
    DescribeFleetPortSettingsOutputTypeDef,
    DescribeFleetUtilizationInputRequestTypeDef,
    DescribeFleetUtilizationOutputTypeDef,
    DescribeGameServerGroupInputRequestTypeDef,
    DescribeGameServerGroupOutputTypeDef,
    DescribeGameServerInputRequestTypeDef,
    DescribeGameServerInstancesInputRequestTypeDef,
    DescribeGameServerInstancesOutputTypeDef,
    DescribeGameServerOutputTypeDef,
    DescribeGameSessionDetailsInputRequestTypeDef,
    DescribeGameSessionDetailsOutputTypeDef,
    DescribeGameSessionPlacementInputRequestTypeDef,
    DescribeGameSessionPlacementOutputTypeDef,
    DescribeGameSessionQueuesInputRequestTypeDef,
    DescribeGameSessionQueuesOutputTypeDef,
    DescribeGameSessionsInputRequestTypeDef,
    DescribeGameSessionsOutputTypeDef,
    DescribeInstancesInputRequestTypeDef,
    DescribeInstancesOutputTypeDef,
    DescribeMatchmakingConfigurationsInputRequestTypeDef,
    DescribeMatchmakingConfigurationsOutputTypeDef,
    DescribeMatchmakingInputRequestTypeDef,
    DescribeMatchmakingOutputTypeDef,
    DescribeMatchmakingRuleSetsInputRequestTypeDef,
    DescribeMatchmakingRuleSetsOutputTypeDef,
    DescribePlayerSessionsInputRequestTypeDef,
    DescribePlayerSessionsOutputTypeDef,
    DescribeRuntimeConfigurationInputRequestTypeDef,
    DescribeRuntimeConfigurationOutputTypeDef,
    DescribeScalingPoliciesInputRequestTypeDef,
    DescribeScalingPoliciesOutputTypeDef,
    DescribeScriptInputRequestTypeDef,
    DescribeScriptOutputTypeDef,
    DescribeVpcPeeringAuthorizationsOutputTypeDef,
    DescribeVpcPeeringConnectionsInputRequestTypeDef,
    DescribeVpcPeeringConnectionsOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    GetComputeAccessInputRequestTypeDef,
    GetComputeAccessOutputTypeDef,
    GetComputeAuthTokenInputRequestTypeDef,
    GetComputeAuthTokenOutputTypeDef,
    GetGameSessionLogUrlInputRequestTypeDef,
    GetGameSessionLogUrlOutputTypeDef,
    GetInstanceAccessInputRequestTypeDef,
    GetInstanceAccessOutputTypeDef,
    ListAliasesInputRequestTypeDef,
    ListAliasesOutputTypeDef,
    ListBuildsInputRequestTypeDef,
    ListBuildsOutputTypeDef,
    ListComputeInputRequestTypeDef,
    ListComputeOutputTypeDef,
    ListContainerGroupDefinitionsInputRequestTypeDef,
    ListContainerGroupDefinitionsOutputTypeDef,
    ListFleetsInputRequestTypeDef,
    ListFleetsOutputTypeDef,
    ListGameServerGroupsInputRequestTypeDef,
    ListGameServerGroupsOutputTypeDef,
    ListGameServersInputRequestTypeDef,
    ListGameServersOutputTypeDef,
    ListLocationsInputRequestTypeDef,
    ListLocationsOutputTypeDef,
    ListScriptsInputRequestTypeDef,
    ListScriptsOutputTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutScalingPolicyInputRequestTypeDef,
    PutScalingPolicyOutputTypeDef,
    RegisterComputeInputRequestTypeDef,
    RegisterComputeOutputTypeDef,
    RegisterGameServerInputRequestTypeDef,
    RegisterGameServerOutputTypeDef,
    RequestUploadCredentialsInputRequestTypeDef,
    RequestUploadCredentialsOutputTypeDef,
    ResolveAliasInputRequestTypeDef,
    ResolveAliasOutputTypeDef,
    ResumeGameServerGroupInputRequestTypeDef,
    ResumeGameServerGroupOutputTypeDef,
    SearchGameSessionsInputRequestTypeDef,
    SearchGameSessionsOutputTypeDef,
    StartFleetActionsInputRequestTypeDef,
    StartFleetActionsOutputTypeDef,
    StartGameSessionPlacementInputRequestTypeDef,
    StartGameSessionPlacementOutputTypeDef,
    StartMatchBackfillInputRequestTypeDef,
    StartMatchBackfillOutputTypeDef,
    StartMatchmakingInputRequestTypeDef,
    StartMatchmakingOutputTypeDef,
    StopFleetActionsInputRequestTypeDef,
    StopFleetActionsOutputTypeDef,
    StopGameSessionPlacementInputRequestTypeDef,
    StopGameSessionPlacementOutputTypeDef,
    StopMatchmakingInputRequestTypeDef,
    SuspendGameServerGroupInputRequestTypeDef,
    SuspendGameServerGroupOutputTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAliasInputRequestTypeDef,
    UpdateAliasOutputTypeDef,
    UpdateBuildInputRequestTypeDef,
    UpdateBuildOutputTypeDef,
    UpdateFleetAttributesInputRequestTypeDef,
    UpdateFleetAttributesOutputTypeDef,
    UpdateFleetCapacityInputRequestTypeDef,
    UpdateFleetCapacityOutputTypeDef,
    UpdateFleetPortSettingsInputRequestTypeDef,
    UpdateFleetPortSettingsOutputTypeDef,
    UpdateGameServerGroupInputRequestTypeDef,
    UpdateGameServerGroupOutputTypeDef,
    UpdateGameServerInputRequestTypeDef,
    UpdateGameServerOutputTypeDef,
    UpdateGameSessionInputRequestTypeDef,
    UpdateGameSessionOutputTypeDef,
    UpdateGameSessionQueueInputRequestTypeDef,
    UpdateGameSessionQueueOutputTypeDef,
    UpdateMatchmakingConfigurationInputRequestTypeDef,
    UpdateMatchmakingConfigurationOutputTypeDef,
    UpdateRuntimeConfigurationInputRequestTypeDef,
    UpdateRuntimeConfigurationOutputTypeDef,
    UpdateScriptInputRequestTypeDef,
    UpdateScriptOutputTypeDef,
    ValidateMatchmakingRuleSetInputRequestTypeDef,
    ValidateMatchmakingRuleSetOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("GameLiftClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    FleetCapacityExceededException: Type[BotocoreClientError]
    GameSessionFullException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidFleetStatusException: Type[BotocoreClientError]
    InvalidGameSessionStatusException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    NotReadyException: Type[BotocoreClientError]
    OutOfCapacityException: Type[BotocoreClientError]
    TaggingFailedException: Type[BotocoreClientError]
    TerminalRoutingStrategyException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    UnsupportedRegionException: Type[BotocoreClientError]


class GameLiftClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GameLiftClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#close)
        """

    async def accept_match(
        self, **kwargs: Unpack[AcceptMatchInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Registers a player's acceptance or rejection of a proposed FlexMatch match.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/accept_match.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#accept_match)
        """

    async def claim_game_server(
        self, **kwargs: Unpack[ClaimGameServerInputRequestTypeDef]
    ) -> ClaimGameServerOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/claim_game_server.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#claim_game_server)
        """

    async def create_alias(
        self, **kwargs: Unpack[CreateAliasInputRequestTypeDef]
    ) -> CreateAliasOutputTypeDef:
        """
        Creates an alias for a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#create_alias)
        """

    async def create_build(
        self, **kwargs: Unpack[CreateBuildInputRequestTypeDef]
    ) -> CreateBuildOutputTypeDef:
        """
        Creates a new Amazon GameLift build resource for your game server binary files.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_build.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#create_build)
        """

    async def create_container_group_definition(
        self, **kwargs: Unpack[CreateContainerGroupDefinitionInputRequestTypeDef]
    ) -> CreateContainerGroupDefinitionOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift containers feature, which is
        currently in public preview.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_container_group_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#create_container_group_definition)
        """

    async def create_fleet(
        self, **kwargs: Unpack[CreateFleetInputRequestTypeDef]
    ) -> CreateFleetOutputTypeDef:
        """
        <b>This operation has been expanded to use with the Amazon GameLift containers
        feature, which is currently in public preview.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#create_fleet)
        """

    async def create_fleet_locations(
        self, **kwargs: Unpack[CreateFleetLocationsInputRequestTypeDef]
    ) -> CreateFleetLocationsOutputTypeDef:
        """
        <b>This operation has been expanded to use with the Amazon GameLift containers
        feature, which is currently in public preview.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_fleet_locations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#create_fleet_locations)
        """

    async def create_game_server_group(
        self, **kwargs: Unpack[CreateGameServerGroupInputRequestTypeDef]
    ) -> CreateGameServerGroupOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_game_server_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#create_game_server_group)
        """

    async def create_game_session(
        self, **kwargs: Unpack[CreateGameSessionInputRequestTypeDef]
    ) -> CreateGameSessionOutputTypeDef:
        """
        Creates a multiplayer game session for players in a specific fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_game_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#create_game_session)
        """

    async def create_game_session_queue(
        self, **kwargs: Unpack[CreateGameSessionQueueInputRequestTypeDef]
    ) -> CreateGameSessionQueueOutputTypeDef:
        """
        Creates a placement queue that processes requests for new game sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_game_session_queue.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#create_game_session_queue)
        """

    async def create_location(
        self, **kwargs: Unpack[CreateLocationInputRequestTypeDef]
    ) -> CreateLocationOutputTypeDef:
        """
        Creates a custom location for use in an Anywhere fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_location.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#create_location)
        """

    async def create_matchmaking_configuration(
        self, **kwargs: Unpack[CreateMatchmakingConfigurationInputRequestTypeDef]
    ) -> CreateMatchmakingConfigurationOutputTypeDef:
        """
        Defines a new matchmaking configuration for use with FlexMatch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_matchmaking_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#create_matchmaking_configuration)
        """

    async def create_matchmaking_rule_set(
        self, **kwargs: Unpack[CreateMatchmakingRuleSetInputRequestTypeDef]
    ) -> CreateMatchmakingRuleSetOutputTypeDef:
        """
        Creates a new rule set for FlexMatch matchmaking.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_matchmaking_rule_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#create_matchmaking_rule_set)
        """

    async def create_player_session(
        self, **kwargs: Unpack[CreatePlayerSessionInputRequestTypeDef]
    ) -> CreatePlayerSessionOutputTypeDef:
        """
        Reserves an open player slot in a game session for a player.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_player_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#create_player_session)
        """

    async def create_player_sessions(
        self, **kwargs: Unpack[CreatePlayerSessionsInputRequestTypeDef]
    ) -> CreatePlayerSessionsOutputTypeDef:
        """
        Reserves open slots in a game session for a group of players.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_player_sessions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#create_player_sessions)
        """

    async def create_script(
        self, **kwargs: Unpack[CreateScriptInputRequestTypeDef]
    ) -> CreateScriptOutputTypeDef:
        """
        Creates a new script record for your Realtime Servers script.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_script.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#create_script)
        """

    async def create_vpc_peering_authorization(
        self, **kwargs: Unpack[CreateVpcPeeringAuthorizationInputRequestTypeDef]
    ) -> CreateVpcPeeringAuthorizationOutputTypeDef:
        """
        Requests authorization to create or delete a peer connection between the VPC
        for your Amazon GameLift fleet and a virtual private cloud (VPC) in your Amazon
        Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_vpc_peering_authorization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#create_vpc_peering_authorization)
        """

    async def create_vpc_peering_connection(
        self, **kwargs: Unpack[CreateVpcPeeringConnectionInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Establishes a VPC peering connection between a virtual private cloud (VPC) in
        an Amazon Web Services account with the VPC for your Amazon GameLift fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_vpc_peering_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#create_vpc_peering_connection)
        """

    async def delete_alias(
        self, **kwargs: Unpack[DeleteAliasInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#delete_alias)
        """

    async def delete_build(
        self, **kwargs: Unpack[DeleteBuildInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_build.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#delete_build)
        """

    async def delete_container_group_definition(
        self, **kwargs: Unpack[DeleteContainerGroupDefinitionInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        <b>This operation is used with the Amazon GameLift containers feature, which is
        currently in public preview.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_container_group_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#delete_container_group_definition)
        """

    async def delete_fleet(
        self, **kwargs: Unpack[DeleteFleetInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes all resources and information related to a fleet and shuts down any
        currently running fleet instances, including those in remote locations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#delete_fleet)
        """

    async def delete_fleet_locations(
        self, **kwargs: Unpack[DeleteFleetLocationsInputRequestTypeDef]
    ) -> DeleteFleetLocationsOutputTypeDef:
        """
        Removes locations from a multi-location fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_fleet_locations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#delete_fleet_locations)
        """

    async def delete_game_server_group(
        self, **kwargs: Unpack[DeleteGameServerGroupInputRequestTypeDef]
    ) -> DeleteGameServerGroupOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_game_server_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#delete_game_server_group)
        """

    async def delete_game_session_queue(
        self, **kwargs: Unpack[DeleteGameSessionQueueInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a game session queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_game_session_queue.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#delete_game_session_queue)
        """

    async def delete_location(
        self, **kwargs: Unpack[DeleteLocationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a custom location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_location.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#delete_location)
        """

    async def delete_matchmaking_configuration(
        self, **kwargs: Unpack[DeleteMatchmakingConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Permanently removes a FlexMatch matchmaking configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_matchmaking_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#delete_matchmaking_configuration)
        """

    async def delete_matchmaking_rule_set(
        self, **kwargs: Unpack[DeleteMatchmakingRuleSetInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an existing matchmaking rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_matchmaking_rule_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#delete_matchmaking_rule_set)
        """

    async def delete_scaling_policy(
        self, **kwargs: Unpack[DeleteScalingPolicyInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a fleet scaling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_scaling_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#delete_scaling_policy)
        """

    async def delete_script(
        self, **kwargs: Unpack[DeleteScriptInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Realtime script.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_script.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#delete_script)
        """

    async def delete_vpc_peering_authorization(
        self, **kwargs: Unpack[DeleteVpcPeeringAuthorizationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels a pending VPC peering authorization for the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_vpc_peering_authorization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#delete_vpc_peering_authorization)
        """

    async def delete_vpc_peering_connection(
        self, **kwargs: Unpack[DeleteVpcPeeringConnectionInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a VPC peering connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_vpc_peering_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#delete_vpc_peering_connection)
        """

    async def deregister_compute(
        self, **kwargs: Unpack[DeregisterComputeInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        <b>This operation has been expanded to use with the Amazon GameLift containers
        feature, which is currently in public preview.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/deregister_compute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#deregister_compute)
        """

    async def deregister_game_server(
        self, **kwargs: Unpack[DeregisterGameServerInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/deregister_game_server.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#deregister_game_server)
        """

    async def describe_alias(
        self, **kwargs: Unpack[DescribeAliasInputRequestTypeDef]
    ) -> DescribeAliasOutputTypeDef:
        """
        Retrieves properties for an alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_alias)
        """

    async def describe_build(
        self, **kwargs: Unpack[DescribeBuildInputRequestTypeDef]
    ) -> DescribeBuildOutputTypeDef:
        """
        Retrieves properties for a custom game build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_build.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_build)
        """

    async def describe_compute(
        self, **kwargs: Unpack[DescribeComputeInputRequestTypeDef]
    ) -> DescribeComputeOutputTypeDef:
        """
        <b>This operation has been expanded to use with the Amazon GameLift containers
        feature, which is currently in public preview.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_compute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_compute)
        """

    async def describe_container_group_definition(
        self, **kwargs: Unpack[DescribeContainerGroupDefinitionInputRequestTypeDef]
    ) -> DescribeContainerGroupDefinitionOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift containers feature, which is
        currently in public preview.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_container_group_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_container_group_definition)
        """

    async def describe_ec2_instance_limits(
        self, **kwargs: Unpack[DescribeEC2InstanceLimitsInputRequestTypeDef]
    ) -> DescribeEC2InstanceLimitsOutputTypeDef:
        """
        Retrieves the instance limits and current utilization for an Amazon Web
        Services Region or location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_ec2_instance_limits.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_ec2_instance_limits)
        """

    async def describe_fleet_attributes(
        self, **kwargs: Unpack[DescribeFleetAttributesInputRequestTypeDef]
    ) -> DescribeFleetAttributesOutputTypeDef:
        """
        <b>This operation has been expanded to use with the Amazon GameLift containers
        feature, which is currently in public preview.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_fleet_attributes)
        """

    async def describe_fleet_capacity(
        self, **kwargs: Unpack[DescribeFleetCapacityInputRequestTypeDef]
    ) -> DescribeFleetCapacityOutputTypeDef:
        """
        <b>This operation has been expanded to use with the Amazon GameLift containers
        feature, which is currently in public preview.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_capacity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_fleet_capacity)
        """

    async def describe_fleet_events(
        self, **kwargs: Unpack[DescribeFleetEventsInputRequestTypeDef]
    ) -> DescribeFleetEventsOutputTypeDef:
        """
        Retrieves entries from a fleet's event log.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_events.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_fleet_events)
        """

    async def describe_fleet_location_attributes(
        self, **kwargs: Unpack[DescribeFleetLocationAttributesInputRequestTypeDef]
    ) -> DescribeFleetLocationAttributesOutputTypeDef:
        """
        Retrieves information on a fleet's remote locations, including life-cycle
        status and any suspended fleet activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_location_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_fleet_location_attributes)
        """

    async def describe_fleet_location_capacity(
        self, **kwargs: Unpack[DescribeFleetLocationCapacityInputRequestTypeDef]
    ) -> DescribeFleetLocationCapacityOutputTypeDef:
        """
        Retrieves the resource capacity settings for a fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_location_capacity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_fleet_location_capacity)
        """

    async def describe_fleet_location_utilization(
        self, **kwargs: Unpack[DescribeFleetLocationUtilizationInputRequestTypeDef]
    ) -> DescribeFleetLocationUtilizationOutputTypeDef:
        """
        Retrieves current usage data for a fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_location_utilization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_fleet_location_utilization)
        """

    async def describe_fleet_port_settings(
        self, **kwargs: Unpack[DescribeFleetPortSettingsInputRequestTypeDef]
    ) -> DescribeFleetPortSettingsOutputTypeDef:
        """
        Retrieves a fleet's inbound connection permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_port_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_fleet_port_settings)
        """

    async def describe_fleet_utilization(
        self, **kwargs: Unpack[DescribeFleetUtilizationInputRequestTypeDef]
    ) -> DescribeFleetUtilizationOutputTypeDef:
        """
        Retrieves utilization statistics for one or more fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_utilization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_fleet_utilization)
        """

    async def describe_game_server(
        self, **kwargs: Unpack[DescribeGameServerInputRequestTypeDef]
    ) -> DescribeGameServerOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_server.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_game_server)
        """

    async def describe_game_server_group(
        self, **kwargs: Unpack[DescribeGameServerGroupInputRequestTypeDef]
    ) -> DescribeGameServerGroupOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_server_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_game_server_group)
        """

    async def describe_game_server_instances(
        self, **kwargs: Unpack[DescribeGameServerInstancesInputRequestTypeDef]
    ) -> DescribeGameServerInstancesOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_server_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_game_server_instances)
        """

    async def describe_game_session_details(
        self, **kwargs: Unpack[DescribeGameSessionDetailsInputRequestTypeDef]
    ) -> DescribeGameSessionDetailsOutputTypeDef:
        """
        Retrieves additional game session properties, including the game session
        protection policy in force, a set of one or more game sessions in a specific
        fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_session_details.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_game_session_details)
        """

    async def describe_game_session_placement(
        self, **kwargs: Unpack[DescribeGameSessionPlacementInputRequestTypeDef]
    ) -> DescribeGameSessionPlacementOutputTypeDef:
        """
        Retrieves information, including current status, about a game session placement
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_session_placement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_game_session_placement)
        """

    async def describe_game_session_queues(
        self, **kwargs: Unpack[DescribeGameSessionQueuesInputRequestTypeDef]
    ) -> DescribeGameSessionQueuesOutputTypeDef:
        """
        Retrieves the properties for one or more game session queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_session_queues.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_game_session_queues)
        """

    async def describe_game_sessions(
        self, **kwargs: Unpack[DescribeGameSessionsInputRequestTypeDef]
    ) -> DescribeGameSessionsOutputTypeDef:
        """
        Retrieves a set of one or more game sessions in a specific fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_sessions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_game_sessions)
        """

    async def describe_instances(
        self, **kwargs: Unpack[DescribeInstancesInputRequestTypeDef]
    ) -> DescribeInstancesOutputTypeDef:
        """
        Retrieves information about the EC2 instances in an Amazon GameLift managed
        fleet, including instance ID, connection data, and status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_instances)
        """

    async def describe_matchmaking(
        self, **kwargs: Unpack[DescribeMatchmakingInputRequestTypeDef]
    ) -> DescribeMatchmakingOutputTypeDef:
        """
        Retrieves one or more matchmaking tickets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_matchmaking.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_matchmaking)
        """

    async def describe_matchmaking_configurations(
        self, **kwargs: Unpack[DescribeMatchmakingConfigurationsInputRequestTypeDef]
    ) -> DescribeMatchmakingConfigurationsOutputTypeDef:
        """
        Retrieves the details of FlexMatch matchmaking configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_matchmaking_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_matchmaking_configurations)
        """

    async def describe_matchmaking_rule_sets(
        self, **kwargs: Unpack[DescribeMatchmakingRuleSetsInputRequestTypeDef]
    ) -> DescribeMatchmakingRuleSetsOutputTypeDef:
        """
        Retrieves the details for FlexMatch matchmaking rule sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_matchmaking_rule_sets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_matchmaking_rule_sets)
        """

    async def describe_player_sessions(
        self, **kwargs: Unpack[DescribePlayerSessionsInputRequestTypeDef]
    ) -> DescribePlayerSessionsOutputTypeDef:
        """
        Retrieves properties for one or more player sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_player_sessions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_player_sessions)
        """

    async def describe_runtime_configuration(
        self, **kwargs: Unpack[DescribeRuntimeConfigurationInputRequestTypeDef]
    ) -> DescribeRuntimeConfigurationOutputTypeDef:
        """
        Retrieves a fleet's runtime configuration settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_runtime_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_runtime_configuration)
        """

    async def describe_scaling_policies(
        self, **kwargs: Unpack[DescribeScalingPoliciesInputRequestTypeDef]
    ) -> DescribeScalingPoliciesOutputTypeDef:
        """
        Retrieves all scaling policies applied to a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_scaling_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_scaling_policies)
        """

    async def describe_script(
        self, **kwargs: Unpack[DescribeScriptInputRequestTypeDef]
    ) -> DescribeScriptOutputTypeDef:
        """
        Retrieves properties for a Realtime script.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_script.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_script)
        """

    async def describe_vpc_peering_authorizations(
        self,
    ) -> DescribeVpcPeeringAuthorizationsOutputTypeDef:
        """
        Retrieves valid VPC peering authorizations that are pending for the Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_vpc_peering_authorizations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_vpc_peering_authorizations)
        """

    async def describe_vpc_peering_connections(
        self, **kwargs: Unpack[DescribeVpcPeeringConnectionsInputRequestTypeDef]
    ) -> DescribeVpcPeeringConnectionsOutputTypeDef:
        """
        Retrieves information on VPC peering connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_vpc_peering_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#describe_vpc_peering_connections)
        """

    async def get_compute_access(
        self, **kwargs: Unpack[GetComputeAccessInputRequestTypeDef]
    ) -> GetComputeAccessOutputTypeDef:
        """
        <b>This operation has been expanded to use with the Amazon GameLift containers
        feature, which is currently in public preview.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_compute_access.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_compute_access)
        """

    async def get_compute_auth_token(
        self, **kwargs: Unpack[GetComputeAuthTokenInputRequestTypeDef]
    ) -> GetComputeAuthTokenOutputTypeDef:
        """
        Requests an authentication token from Amazon GameLift for a compute resource in
        an Amazon GameLift Anywhere fleet or container fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_compute_auth_token.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_compute_auth_token)
        """

    async def get_game_session_log_url(
        self, **kwargs: Unpack[GetGameSessionLogUrlInputRequestTypeDef]
    ) -> GetGameSessionLogUrlOutputTypeDef:
        """
        Retrieves the location of stored game session logs for a specified game session
        on Amazon GameLift managed fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_game_session_log_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_game_session_log_url)
        """

    async def get_instance_access(
        self, **kwargs: Unpack[GetInstanceAccessInputRequestTypeDef]
    ) -> GetInstanceAccessOutputTypeDef:
        """
        Requests authorization to remotely connect to an instance in an Amazon GameLift
        managed fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_instance_access.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_instance_access)
        """

    async def list_aliases(
        self, **kwargs: Unpack[ListAliasesInputRequestTypeDef]
    ) -> ListAliasesOutputTypeDef:
        """
        Retrieves all aliases for this Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_aliases.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#list_aliases)
        """

    async def list_builds(
        self, **kwargs: Unpack[ListBuildsInputRequestTypeDef]
    ) -> ListBuildsOutputTypeDef:
        """
        Retrieves build resources for all builds associated with the Amazon Web
        Services account in use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_builds.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#list_builds)
        """

    async def list_compute(
        self, **kwargs: Unpack[ListComputeInputRequestTypeDef]
    ) -> ListComputeOutputTypeDef:
        """
        <b>This operation has been expanded to use with the Amazon GameLift containers
        feature, which is currently in public preview.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_compute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#list_compute)
        """

    async def list_container_group_definitions(
        self, **kwargs: Unpack[ListContainerGroupDefinitionsInputRequestTypeDef]
    ) -> ListContainerGroupDefinitionsOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift containers feature, which is
        currently in public preview.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_container_group_definitions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#list_container_group_definitions)
        """

    async def list_fleets(
        self, **kwargs: Unpack[ListFleetsInputRequestTypeDef]
    ) -> ListFleetsOutputTypeDef:
        """
        <b>This operation has been expanded to use with the Amazon GameLift containers
        feature, which is currently in public preview.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_fleets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#list_fleets)
        """

    async def list_game_server_groups(
        self, **kwargs: Unpack[ListGameServerGroupsInputRequestTypeDef]
    ) -> ListGameServerGroupsOutputTypeDef:
        """
        Lists a game server groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_game_server_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#list_game_server_groups)
        """

    async def list_game_servers(
        self, **kwargs: Unpack[ListGameServersInputRequestTypeDef]
    ) -> ListGameServersOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_game_servers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#list_game_servers)
        """

    async def list_locations(
        self, **kwargs: Unpack[ListLocationsInputRequestTypeDef]
    ) -> ListLocationsOutputTypeDef:
        """
        Lists all custom and Amazon Web Services locations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_locations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#list_locations)
        """

    async def list_scripts(
        self, **kwargs: Unpack[ListScriptsInputRequestTypeDef]
    ) -> ListScriptsOutputTypeDef:
        """
        Retrieves script records for all Realtime scripts that are associated with the
        Amazon Web Services account in use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_scripts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#list_scripts)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves all tags assigned to a Amazon GameLift resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#list_tags_for_resource)
        """

    async def put_scaling_policy(
        self, **kwargs: Unpack[PutScalingPolicyInputRequestTypeDef]
    ) -> PutScalingPolicyOutputTypeDef:
        """
        Creates or updates a scaling policy for a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/put_scaling_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#put_scaling_policy)
        """

    async def register_compute(
        self, **kwargs: Unpack[RegisterComputeInputRequestTypeDef]
    ) -> RegisterComputeOutputTypeDef:
        """
        <b>This operation has been expanded to use with the Amazon GameLift containers
        feature, which is currently in public preview.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/register_compute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#register_compute)
        """

    async def register_game_server(
        self, **kwargs: Unpack[RegisterGameServerInputRequestTypeDef]
    ) -> RegisterGameServerOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/register_game_server.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#register_game_server)
        """

    async def request_upload_credentials(
        self, **kwargs: Unpack[RequestUploadCredentialsInputRequestTypeDef]
    ) -> RequestUploadCredentialsOutputTypeDef:
        """
        Retrieves a fresh set of credentials for use when uploading a new set of game
        build files to Amazon GameLift's Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/request_upload_credentials.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#request_upload_credentials)
        """

    async def resolve_alias(
        self, **kwargs: Unpack[ResolveAliasInputRequestTypeDef]
    ) -> ResolveAliasOutputTypeDef:
        """
        Attempts to retrieve a fleet ID that is associated with an alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/resolve_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#resolve_alias)
        """

    async def resume_game_server_group(
        self, **kwargs: Unpack[ResumeGameServerGroupInputRequestTypeDef]
    ) -> ResumeGameServerGroupOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/resume_game_server_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#resume_game_server_group)
        """

    async def search_game_sessions(
        self, **kwargs: Unpack[SearchGameSessionsInputRequestTypeDef]
    ) -> SearchGameSessionsOutputTypeDef:
        """
        Retrieves all active game sessions that match a set of search criteria and
        sorts them into a specified order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/search_game_sessions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#search_game_sessions)
        """

    async def start_fleet_actions(
        self, **kwargs: Unpack[StartFleetActionsInputRequestTypeDef]
    ) -> StartFleetActionsOutputTypeDef:
        """
        Resumes certain types of activity on fleet instances that were suspended with
        <a
        href="https://docs.aws.amazon.com/gamelift/latest/apireference/API_StopFleetActions.html">StopFleetActions</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/start_fleet_actions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#start_fleet_actions)
        """

    async def start_game_session_placement(
        self, **kwargs: Unpack[StartGameSessionPlacementInputRequestTypeDef]
    ) -> StartGameSessionPlacementOutputTypeDef:
        """
        Places a request for a new game session in a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/start_game_session_placement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#start_game_session_placement)
        """

    async def start_match_backfill(
        self, **kwargs: Unpack[StartMatchBackfillInputRequestTypeDef]
    ) -> StartMatchBackfillOutputTypeDef:
        """
        Finds new players to fill open slots in currently running game sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/start_match_backfill.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#start_match_backfill)
        """

    async def start_matchmaking(
        self, **kwargs: Unpack[StartMatchmakingInputRequestTypeDef]
    ) -> StartMatchmakingOutputTypeDef:
        """
        Uses FlexMatch to create a game match for a group of players based on custom
        matchmaking rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/start_matchmaking.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#start_matchmaking)
        """

    async def stop_fleet_actions(
        self, **kwargs: Unpack[StopFleetActionsInputRequestTypeDef]
    ) -> StopFleetActionsOutputTypeDef:
        """
        Suspends certain types of activity in a fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/stop_fleet_actions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#stop_fleet_actions)
        """

    async def stop_game_session_placement(
        self, **kwargs: Unpack[StopGameSessionPlacementInputRequestTypeDef]
    ) -> StopGameSessionPlacementOutputTypeDef:
        """
        Cancels a game session placement that is in <code>PENDING</code> status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/stop_game_session_placement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#stop_game_session_placement)
        """

    async def stop_matchmaking(
        self, **kwargs: Unpack[StopMatchmakingInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels a matchmaking ticket or match backfill ticket that is currently being
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/stop_matchmaking.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#stop_matchmaking)
        """

    async def suspend_game_server_group(
        self, **kwargs: Unpack[SuspendGameServerGroupInputRequestTypeDef]
    ) -> SuspendGameServerGroupOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/suspend_game_server_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#suspend_game_server_group)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Assigns a tag to an Amazon GameLift resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a tag assigned to a Amazon GameLift resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#untag_resource)
        """

    async def update_alias(
        self, **kwargs: Unpack[UpdateAliasInputRequestTypeDef]
    ) -> UpdateAliasOutputTypeDef:
        """
        Updates properties for an alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#update_alias)
        """

    async def update_build(
        self, **kwargs: Unpack[UpdateBuildInputRequestTypeDef]
    ) -> UpdateBuildOutputTypeDef:
        """
        Updates metadata in a build resource, including the build name and version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_build.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#update_build)
        """

    async def update_fleet_attributes(
        self, **kwargs: Unpack[UpdateFleetAttributesInputRequestTypeDef]
    ) -> UpdateFleetAttributesOutputTypeDef:
        """
        Updates a fleet's mutable attributes, such as game session protection and
        resource creation limits.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_fleet_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#update_fleet_attributes)
        """

    async def update_fleet_capacity(
        self, **kwargs: Unpack[UpdateFleetCapacityInputRequestTypeDef]
    ) -> UpdateFleetCapacityOutputTypeDef:
        """
        <b>This operation has been expanded to use with the Amazon GameLift containers
        feature, which is currently in public preview.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_fleet_capacity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#update_fleet_capacity)
        """

    async def update_fleet_port_settings(
        self, **kwargs: Unpack[UpdateFleetPortSettingsInputRequestTypeDef]
    ) -> UpdateFleetPortSettingsOutputTypeDef:
        """
        Updates permissions that allow inbound traffic to connect to game sessions in
        the fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_fleet_port_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#update_fleet_port_settings)
        """

    async def update_game_server(
        self, **kwargs: Unpack[UpdateGameServerInputRequestTypeDef]
    ) -> UpdateGameServerOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_game_server.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#update_game_server)
        """

    async def update_game_server_group(
        self, **kwargs: Unpack[UpdateGameServerGroupInputRequestTypeDef]
    ) -> UpdateGameServerGroupOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_game_server_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#update_game_server_group)
        """

    async def update_game_session(
        self, **kwargs: Unpack[UpdateGameSessionInputRequestTypeDef]
    ) -> UpdateGameSessionOutputTypeDef:
        """
        Updates the mutable properties of a game session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_game_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#update_game_session)
        """

    async def update_game_session_queue(
        self, **kwargs: Unpack[UpdateGameSessionQueueInputRequestTypeDef]
    ) -> UpdateGameSessionQueueOutputTypeDef:
        """
        Updates the configuration of a game session queue, which determines how the
        queue processes new game session requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_game_session_queue.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#update_game_session_queue)
        """

    async def update_matchmaking_configuration(
        self, **kwargs: Unpack[UpdateMatchmakingConfigurationInputRequestTypeDef]
    ) -> UpdateMatchmakingConfigurationOutputTypeDef:
        """
        Updates settings for a FlexMatch matchmaking configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_matchmaking_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#update_matchmaking_configuration)
        """

    async def update_runtime_configuration(
        self, **kwargs: Unpack[UpdateRuntimeConfigurationInputRequestTypeDef]
    ) -> UpdateRuntimeConfigurationOutputTypeDef:
        """
        Updates the runtime configuration for the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_runtime_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#update_runtime_configuration)
        """

    async def update_script(
        self, **kwargs: Unpack[UpdateScriptInputRequestTypeDef]
    ) -> UpdateScriptOutputTypeDef:
        """
        Updates Realtime script metadata and content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_script.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#update_script)
        """

    async def validate_matchmaking_rule_set(
        self, **kwargs: Unpack[ValidateMatchmakingRuleSetInputRequestTypeDef]
    ) -> ValidateMatchmakingRuleSetOutputTypeDef:
        """
        Validates the syntax of a matchmaking rule or rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/validate_matchmaking_rule_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#validate_matchmaking_rule_set)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_fleet_attributes"]
    ) -> DescribeFleetAttributesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_fleet_capacity"]
    ) -> DescribeFleetCapacityPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_fleet_events"]
    ) -> DescribeFleetEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_fleet_utilization"]
    ) -> DescribeFleetUtilizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_game_server_instances"]
    ) -> DescribeGameServerInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_game_session_details"]
    ) -> DescribeGameSessionDetailsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_game_session_queues"]
    ) -> DescribeGameSessionQueuesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_game_sessions"]
    ) -> DescribeGameSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instances"]
    ) -> DescribeInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_matchmaking_configurations"]
    ) -> DescribeMatchmakingConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_matchmaking_rule_sets"]
    ) -> DescribeMatchmakingRuleSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_player_sessions"]
    ) -> DescribePlayerSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scaling_policies"]
    ) -> DescribeScalingPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_aliases"]) -> ListAliasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_builds"]) -> ListBuildsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_compute"]) -> ListComputePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_container_group_definitions"]
    ) -> ListContainerGroupDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_fleets"]) -> ListFleetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_game_server_groups"]
    ) -> ListGameServerGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_game_servers"]
    ) -> ListGameServersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_locations"]) -> ListLocationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_scripts"]) -> ListScriptsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_game_sessions"]
    ) -> SearchGameSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/#get_paginator)
        """

    async def __aenter__(self) -> "GameLiftClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/client/)
        """
