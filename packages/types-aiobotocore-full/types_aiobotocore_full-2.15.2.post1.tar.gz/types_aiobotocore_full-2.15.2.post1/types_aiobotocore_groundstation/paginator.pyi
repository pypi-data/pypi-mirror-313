"""
Type annotations for groundstation service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_groundstation.client import GroundStationClient
    from types_aiobotocore_groundstation.paginator import (
        ListConfigsPaginator,
        ListContactsPaginator,
        ListDataflowEndpointGroupsPaginator,
        ListEphemeridesPaginator,
        ListGroundStationsPaginator,
        ListMissionProfilesPaginator,
        ListSatellitesPaginator,
    )

    session = get_session()
    with session.create_client("groundstation") as client:
        client: GroundStationClient

        list_configs_paginator: ListConfigsPaginator = client.get_paginator("list_configs")
        list_contacts_paginator: ListContactsPaginator = client.get_paginator("list_contacts")
        list_dataflow_endpoint_groups_paginator: ListDataflowEndpointGroupsPaginator = client.get_paginator("list_dataflow_endpoint_groups")
        list_ephemerides_paginator: ListEphemeridesPaginator = client.get_paginator("list_ephemerides")
        list_ground_stations_paginator: ListGroundStationsPaginator = client.get_paginator("list_ground_stations")
        list_mission_profiles_paginator: ListMissionProfilesPaginator = client.get_paginator("list_mission_profiles")
        list_satellites_paginator: ListSatellitesPaginator = client.get_paginator("list_satellites")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListConfigsRequestListConfigsPaginateTypeDef,
    ListConfigsResponseTypeDef,
    ListContactsRequestListContactsPaginateTypeDef,
    ListContactsResponseTypeDef,
    ListDataflowEndpointGroupsRequestListDataflowEndpointGroupsPaginateTypeDef,
    ListDataflowEndpointGroupsResponseTypeDef,
    ListEphemeridesRequestListEphemeridesPaginateTypeDef,
    ListEphemeridesResponseTypeDef,
    ListGroundStationsRequestListGroundStationsPaginateTypeDef,
    ListGroundStationsResponseTypeDef,
    ListMissionProfilesRequestListMissionProfilesPaginateTypeDef,
    ListMissionProfilesResponseTypeDef,
    ListSatellitesRequestListSatellitesPaginateTypeDef,
    ListSatellitesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListConfigsPaginator",
    "ListContactsPaginator",
    "ListDataflowEndpointGroupsPaginator",
    "ListEphemeridesPaginator",
    "ListGroundStationsPaginator",
    "ListMissionProfilesPaginator",
    "ListSatellitesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListConfigs.html#GroundStation.Paginator.ListConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listconfigspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListConfigsRequestListConfigsPaginateTypeDef]
    ) -> AsyncIterator[ListConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListConfigs.html#GroundStation.Paginator.ListConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listconfigspaginator)
        """

class ListContactsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListContacts.html#GroundStation.Paginator.ListContacts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listcontactspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListContactsRequestListContactsPaginateTypeDef]
    ) -> AsyncIterator[ListContactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListContacts.html#GroundStation.Paginator.ListContacts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listcontactspaginator)
        """

class ListDataflowEndpointGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListDataflowEndpointGroups.html#GroundStation.Paginator.ListDataflowEndpointGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listdataflowendpointgroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListDataflowEndpointGroupsRequestListDataflowEndpointGroupsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListDataflowEndpointGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListDataflowEndpointGroups.html#GroundStation.Paginator.ListDataflowEndpointGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listdataflowendpointgroupspaginator)
        """

class ListEphemeridesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListEphemerides.html#GroundStation.Paginator.ListEphemerides)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listephemeridespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEphemeridesRequestListEphemeridesPaginateTypeDef]
    ) -> AsyncIterator[ListEphemeridesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListEphemerides.html#GroundStation.Paginator.ListEphemerides.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listephemeridespaginator)
        """

class ListGroundStationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListGroundStations.html#GroundStation.Paginator.ListGroundStations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listgroundstationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGroundStationsRequestListGroundStationsPaginateTypeDef]
    ) -> AsyncIterator[ListGroundStationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListGroundStations.html#GroundStation.Paginator.ListGroundStations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listgroundstationspaginator)
        """

class ListMissionProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListMissionProfiles.html#GroundStation.Paginator.ListMissionProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listmissionprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMissionProfilesRequestListMissionProfilesPaginateTypeDef]
    ) -> AsyncIterator[ListMissionProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListMissionProfiles.html#GroundStation.Paginator.ListMissionProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listmissionprofilespaginator)
        """

class ListSatellitesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListSatellites.html#GroundStation.Paginator.ListSatellites)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listsatellitespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSatellitesRequestListSatellitesPaginateTypeDef]
    ) -> AsyncIterator[ListSatellitesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListSatellites.html#GroundStation.Paginator.ListSatellites.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listsatellitespaginator)
        """
