"""
Type annotations for groundstation service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_groundstation.client import GroundStationClient

    session = get_session()
    async with session.create_client("groundstation") as client:
        client: GroundStationClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListConfigsPaginator,
    ListContactsPaginator,
    ListDataflowEndpointGroupsPaginator,
    ListEphemeridesPaginator,
    ListGroundStationsPaginator,
    ListMissionProfilesPaginator,
    ListSatellitesPaginator,
)
from .type_defs import (
    CancelContactRequestRequestTypeDef,
    ConfigIdResponseTypeDef,
    ContactIdResponseTypeDef,
    CreateConfigRequestRequestTypeDef,
    CreateDataflowEndpointGroupRequestRequestTypeDef,
    CreateEphemerisRequestRequestTypeDef,
    CreateMissionProfileRequestRequestTypeDef,
    DataflowEndpointGroupIdResponseTypeDef,
    DeleteConfigRequestRequestTypeDef,
    DeleteDataflowEndpointGroupRequestRequestTypeDef,
    DeleteEphemerisRequestRequestTypeDef,
    DeleteMissionProfileRequestRequestTypeDef,
    DescribeContactRequestRequestTypeDef,
    DescribeContactResponseTypeDef,
    DescribeEphemerisRequestRequestTypeDef,
    DescribeEphemerisResponseTypeDef,
    EphemerisIdResponseTypeDef,
    GetAgentConfigurationRequestRequestTypeDef,
    GetAgentConfigurationResponseTypeDef,
    GetConfigRequestRequestTypeDef,
    GetConfigResponseTypeDef,
    GetDataflowEndpointGroupRequestRequestTypeDef,
    GetDataflowEndpointGroupResponseTypeDef,
    GetMinuteUsageRequestRequestTypeDef,
    GetMinuteUsageResponseTypeDef,
    GetMissionProfileRequestRequestTypeDef,
    GetMissionProfileResponseTypeDef,
    GetSatelliteRequestRequestTypeDef,
    GetSatelliteResponseTypeDef,
    ListConfigsRequestRequestTypeDef,
    ListConfigsResponseTypeDef,
    ListContactsRequestRequestTypeDef,
    ListContactsResponseTypeDef,
    ListDataflowEndpointGroupsRequestRequestTypeDef,
    ListDataflowEndpointGroupsResponseTypeDef,
    ListEphemeridesRequestRequestTypeDef,
    ListEphemeridesResponseTypeDef,
    ListGroundStationsRequestRequestTypeDef,
    ListGroundStationsResponseTypeDef,
    ListMissionProfilesRequestRequestTypeDef,
    ListMissionProfilesResponseTypeDef,
    ListSatellitesRequestRequestTypeDef,
    ListSatellitesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    MissionProfileIdResponseTypeDef,
    RegisterAgentRequestRequestTypeDef,
    RegisterAgentResponseTypeDef,
    ReserveContactRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAgentStatusRequestRequestTypeDef,
    UpdateAgentStatusResponseTypeDef,
    UpdateConfigRequestRequestTypeDef,
    UpdateEphemerisRequestRequestTypeDef,
    UpdateMissionProfileRequestRequestTypeDef,
)
from .waiter import ContactScheduledWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("GroundStationClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    DependencyException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]

class GroundStationClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GroundStationClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#close)
        """

    async def cancel_contact(
        self, **kwargs: Unpack[CancelContactRequestRequestTypeDef]
    ) -> ContactIdResponseTypeDef:
        """
        Cancels a contact with a specified contact ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/cancel_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#cancel_contact)
        """

    async def create_config(
        self, **kwargs: Unpack[CreateConfigRequestRequestTypeDef]
    ) -> ConfigIdResponseTypeDef:
        """
        Creates a <code>Config</code> with the specified <code>configData</code>
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/create_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#create_config)
        """

    async def create_dataflow_endpoint_group(
        self, **kwargs: Unpack[CreateDataflowEndpointGroupRequestRequestTypeDef]
    ) -> DataflowEndpointGroupIdResponseTypeDef:
        """
        Creates a <code>DataflowEndpoint</code> group containing the specified list of
        <code>DataflowEndpoint</code> objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/create_dataflow_endpoint_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#create_dataflow_endpoint_group)
        """

    async def create_ephemeris(
        self, **kwargs: Unpack[CreateEphemerisRequestRequestTypeDef]
    ) -> EphemerisIdResponseTypeDef:
        """
        Creates an Ephemeris with the specified <code>EphemerisData</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/create_ephemeris.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#create_ephemeris)
        """

    async def create_mission_profile(
        self, **kwargs: Unpack[CreateMissionProfileRequestRequestTypeDef]
    ) -> MissionProfileIdResponseTypeDef:
        """
        Creates a mission profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/create_mission_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#create_mission_profile)
        """

    async def delete_config(
        self, **kwargs: Unpack[DeleteConfigRequestRequestTypeDef]
    ) -> ConfigIdResponseTypeDef:
        """
        Deletes a <code>Config</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/delete_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#delete_config)
        """

    async def delete_dataflow_endpoint_group(
        self, **kwargs: Unpack[DeleteDataflowEndpointGroupRequestRequestTypeDef]
    ) -> DataflowEndpointGroupIdResponseTypeDef:
        """
        Deletes a dataflow endpoint group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/delete_dataflow_endpoint_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#delete_dataflow_endpoint_group)
        """

    async def delete_ephemeris(
        self, **kwargs: Unpack[DeleteEphemerisRequestRequestTypeDef]
    ) -> EphemerisIdResponseTypeDef:
        """
        Deletes an ephemeris.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/delete_ephemeris.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#delete_ephemeris)
        """

    async def delete_mission_profile(
        self, **kwargs: Unpack[DeleteMissionProfileRequestRequestTypeDef]
    ) -> MissionProfileIdResponseTypeDef:
        """
        Deletes a mission profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/delete_mission_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#delete_mission_profile)
        """

    async def describe_contact(
        self, **kwargs: Unpack[DescribeContactRequestRequestTypeDef]
    ) -> DescribeContactResponseTypeDef:
        """
        Describes an existing contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/describe_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#describe_contact)
        """

    async def describe_ephemeris(
        self, **kwargs: Unpack[DescribeEphemerisRequestRequestTypeDef]
    ) -> DescribeEphemerisResponseTypeDef:
        """
        Describes an existing ephemeris.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/describe_ephemeris.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#describe_ephemeris)
        """

    async def get_agent_configuration(
        self, **kwargs: Unpack[GetAgentConfigurationRequestRequestTypeDef]
    ) -> GetAgentConfigurationResponseTypeDef:
        """
        For use by AWS Ground Station Agent and shouldn't be called directly.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/get_agent_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#get_agent_configuration)
        """

    async def get_config(
        self, **kwargs: Unpack[GetConfigRequestRequestTypeDef]
    ) -> GetConfigResponseTypeDef:
        """
        Returns <code>Config</code> information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/get_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#get_config)
        """

    async def get_dataflow_endpoint_group(
        self, **kwargs: Unpack[GetDataflowEndpointGroupRequestRequestTypeDef]
    ) -> GetDataflowEndpointGroupResponseTypeDef:
        """
        Returns the dataflow endpoint group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/get_dataflow_endpoint_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#get_dataflow_endpoint_group)
        """

    async def get_minute_usage(
        self, **kwargs: Unpack[GetMinuteUsageRequestRequestTypeDef]
    ) -> GetMinuteUsageResponseTypeDef:
        """
        Returns the number of reserved minutes used by account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/get_minute_usage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#get_minute_usage)
        """

    async def get_mission_profile(
        self, **kwargs: Unpack[GetMissionProfileRequestRequestTypeDef]
    ) -> GetMissionProfileResponseTypeDef:
        """
        Returns a mission profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/get_mission_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#get_mission_profile)
        """

    async def get_satellite(
        self, **kwargs: Unpack[GetSatelliteRequestRequestTypeDef]
    ) -> GetSatelliteResponseTypeDef:
        """
        Returns a satellite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/get_satellite.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#get_satellite)
        """

    async def list_configs(
        self, **kwargs: Unpack[ListConfigsRequestRequestTypeDef]
    ) -> ListConfigsResponseTypeDef:
        """
        Returns a list of <code>Config</code> objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/list_configs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#list_configs)
        """

    async def list_contacts(
        self, **kwargs: Unpack[ListContactsRequestRequestTypeDef]
    ) -> ListContactsResponseTypeDef:
        """
        Returns a list of contacts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/list_contacts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#list_contacts)
        """

    async def list_dataflow_endpoint_groups(
        self, **kwargs: Unpack[ListDataflowEndpointGroupsRequestRequestTypeDef]
    ) -> ListDataflowEndpointGroupsResponseTypeDef:
        """
        Returns a list of <code>DataflowEndpoint</code> groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/list_dataflow_endpoint_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#list_dataflow_endpoint_groups)
        """

    async def list_ephemerides(
        self, **kwargs: Unpack[ListEphemeridesRequestRequestTypeDef]
    ) -> ListEphemeridesResponseTypeDef:
        """
        List existing ephemerides.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/list_ephemerides.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#list_ephemerides)
        """

    async def list_ground_stations(
        self, **kwargs: Unpack[ListGroundStationsRequestRequestTypeDef]
    ) -> ListGroundStationsResponseTypeDef:
        """
        Returns a list of ground stations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/list_ground_stations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#list_ground_stations)
        """

    async def list_mission_profiles(
        self, **kwargs: Unpack[ListMissionProfilesRequestRequestTypeDef]
    ) -> ListMissionProfilesResponseTypeDef:
        """
        Returns a list of mission profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/list_mission_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#list_mission_profiles)
        """

    async def list_satellites(
        self, **kwargs: Unpack[ListSatellitesRequestRequestTypeDef]
    ) -> ListSatellitesResponseTypeDef:
        """
        Returns a list of satellites.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/list_satellites.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#list_satellites)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#list_tags_for_resource)
        """

    async def register_agent(
        self, **kwargs: Unpack[RegisterAgentRequestRequestTypeDef]
    ) -> RegisterAgentResponseTypeDef:
        """
        For use by AWS Ground Station Agent and shouldn't be called directly.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/register_agent.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#register_agent)
        """

    async def reserve_contact(
        self, **kwargs: Unpack[ReserveContactRequestRequestTypeDef]
    ) -> ContactIdResponseTypeDef:
        """
        Reserves a contact using specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/reserve_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#reserve_contact)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Assigns a tag to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deassigns a resource tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#untag_resource)
        """

    async def update_agent_status(
        self, **kwargs: Unpack[UpdateAgentStatusRequestRequestTypeDef]
    ) -> UpdateAgentStatusResponseTypeDef:
        """
        For use by AWS Ground Station Agent and shouldn't be called directly.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/update_agent_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#update_agent_status)
        """

    async def update_config(
        self, **kwargs: Unpack[UpdateConfigRequestRequestTypeDef]
    ) -> ConfigIdResponseTypeDef:
        """
        Updates the <code>Config</code> used when scheduling contacts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/update_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#update_config)
        """

    async def update_ephemeris(
        self, **kwargs: Unpack[UpdateEphemerisRequestRequestTypeDef]
    ) -> EphemerisIdResponseTypeDef:
        """
        Updates an existing ephemeris.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/update_ephemeris.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#update_ephemeris)
        """

    async def update_mission_profile(
        self, **kwargs: Unpack[UpdateMissionProfileRequestRequestTypeDef]
    ) -> MissionProfileIdResponseTypeDef:
        """
        Updates a mission profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/update_mission_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#update_mission_profile)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_configs"]) -> ListConfigsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_contacts"]) -> ListContactsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dataflow_endpoint_groups"]
    ) -> ListDataflowEndpointGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ephemerides"]
    ) -> ListEphemeridesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ground_stations"]
    ) -> ListGroundStationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_mission_profiles"]
    ) -> ListMissionProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_satellites"]) -> ListSatellitesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#get_paginator)
        """

    def get_waiter(self, waiter_name: Literal["contact_scheduled"]) -> ContactScheduledWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/#get_waiter)
        """

    async def __aenter__(self) -> "GroundStationClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/client/)
        """
