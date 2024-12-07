"""
Type annotations for location service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_location.client import LocationServiceClient
    from types_aiobotocore_location.paginator import (
        ForecastGeofenceEventsPaginator,
        GetDevicePositionHistoryPaginator,
        ListDevicePositionsPaginator,
        ListGeofenceCollectionsPaginator,
        ListGeofencesPaginator,
        ListKeysPaginator,
        ListMapsPaginator,
        ListPlaceIndexesPaginator,
        ListRouteCalculatorsPaginator,
        ListTrackerConsumersPaginator,
        ListTrackersPaginator,
    )

    session = get_session()
    with session.create_client("location") as client:
        client: LocationServiceClient

        forecast_geofence_events_paginator: ForecastGeofenceEventsPaginator = client.get_paginator("forecast_geofence_events")
        get_device_position_history_paginator: GetDevicePositionHistoryPaginator = client.get_paginator("get_device_position_history")
        list_device_positions_paginator: ListDevicePositionsPaginator = client.get_paginator("list_device_positions")
        list_geofence_collections_paginator: ListGeofenceCollectionsPaginator = client.get_paginator("list_geofence_collections")
        list_geofences_paginator: ListGeofencesPaginator = client.get_paginator("list_geofences")
        list_keys_paginator: ListKeysPaginator = client.get_paginator("list_keys")
        list_maps_paginator: ListMapsPaginator = client.get_paginator("list_maps")
        list_place_indexes_paginator: ListPlaceIndexesPaginator = client.get_paginator("list_place_indexes")
        list_route_calculators_paginator: ListRouteCalculatorsPaginator = client.get_paginator("list_route_calculators")
        list_tracker_consumers_paginator: ListTrackerConsumersPaginator = client.get_paginator("list_tracker_consumers")
        list_trackers_paginator: ListTrackersPaginator = client.get_paginator("list_trackers")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ForecastGeofenceEventsRequestForecastGeofenceEventsPaginateTypeDef,
    ForecastGeofenceEventsResponseTypeDef,
    GetDevicePositionHistoryRequestGetDevicePositionHistoryPaginateTypeDef,
    GetDevicePositionHistoryResponseTypeDef,
    ListDevicePositionsRequestListDevicePositionsPaginateTypeDef,
    ListDevicePositionsResponseTypeDef,
    ListGeofenceCollectionsRequestListGeofenceCollectionsPaginateTypeDef,
    ListGeofenceCollectionsResponseTypeDef,
    ListGeofencesRequestListGeofencesPaginateTypeDef,
    ListGeofencesResponseTypeDef,
    ListKeysRequestListKeysPaginateTypeDef,
    ListKeysResponseTypeDef,
    ListMapsRequestListMapsPaginateTypeDef,
    ListMapsResponseTypeDef,
    ListPlaceIndexesRequestListPlaceIndexesPaginateTypeDef,
    ListPlaceIndexesResponseTypeDef,
    ListRouteCalculatorsRequestListRouteCalculatorsPaginateTypeDef,
    ListRouteCalculatorsResponseTypeDef,
    ListTrackerConsumersRequestListTrackerConsumersPaginateTypeDef,
    ListTrackerConsumersResponseTypeDef,
    ListTrackersRequestListTrackersPaginateTypeDef,
    ListTrackersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ForecastGeofenceEventsPaginator",
    "GetDevicePositionHistoryPaginator",
    "ListDevicePositionsPaginator",
    "ListGeofenceCollectionsPaginator",
    "ListGeofencesPaginator",
    "ListKeysPaginator",
    "ListMapsPaginator",
    "ListPlaceIndexesPaginator",
    "ListRouteCalculatorsPaginator",
    "ListTrackerConsumersPaginator",
    "ListTrackersPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ForecastGeofenceEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ForecastGeofenceEvents.html#LocationService.Paginator.ForecastGeofenceEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#forecastgeofenceeventspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ForecastGeofenceEventsRequestForecastGeofenceEventsPaginateTypeDef]
    ) -> AsyncIterator[ForecastGeofenceEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ForecastGeofenceEvents.html#LocationService.Paginator.ForecastGeofenceEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#forecastgeofenceeventspaginator)
        """


class GetDevicePositionHistoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/GetDevicePositionHistory.html#LocationService.Paginator.GetDevicePositionHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#getdevicepositionhistorypaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[GetDevicePositionHistoryRequestGetDevicePositionHistoryPaginateTypeDef],
    ) -> AsyncIterator[GetDevicePositionHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/GetDevicePositionHistory.html#LocationService.Paginator.GetDevicePositionHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#getdevicepositionhistorypaginator)
        """


class ListDevicePositionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListDevicePositions.html#LocationService.Paginator.ListDevicePositions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listdevicepositionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDevicePositionsRequestListDevicePositionsPaginateTypeDef]
    ) -> AsyncIterator[ListDevicePositionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListDevicePositions.html#LocationService.Paginator.ListDevicePositions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listdevicepositionspaginator)
        """


class ListGeofenceCollectionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListGeofenceCollections.html#LocationService.Paginator.ListGeofenceCollections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listgeofencecollectionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGeofenceCollectionsRequestListGeofenceCollectionsPaginateTypeDef]
    ) -> AsyncIterator[ListGeofenceCollectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListGeofenceCollections.html#LocationService.Paginator.ListGeofenceCollections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listgeofencecollectionspaginator)
        """


class ListGeofencesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListGeofences.html#LocationService.Paginator.ListGeofences)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listgeofencespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGeofencesRequestListGeofencesPaginateTypeDef]
    ) -> AsyncIterator[ListGeofencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListGeofences.html#LocationService.Paginator.ListGeofences.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listgeofencespaginator)
        """


class ListKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListKeys.html#LocationService.Paginator.ListKeys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listkeyspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListKeysRequestListKeysPaginateTypeDef]
    ) -> AsyncIterator[ListKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListKeys.html#LocationService.Paginator.ListKeys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listkeyspaginator)
        """


class ListMapsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListMaps.html#LocationService.Paginator.ListMaps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listmapspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMapsRequestListMapsPaginateTypeDef]
    ) -> AsyncIterator[ListMapsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListMaps.html#LocationService.Paginator.ListMaps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listmapspaginator)
        """


class ListPlaceIndexesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListPlaceIndexes.html#LocationService.Paginator.ListPlaceIndexes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listplaceindexespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPlaceIndexesRequestListPlaceIndexesPaginateTypeDef]
    ) -> AsyncIterator[ListPlaceIndexesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListPlaceIndexes.html#LocationService.Paginator.ListPlaceIndexes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listplaceindexespaginator)
        """


class ListRouteCalculatorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListRouteCalculators.html#LocationService.Paginator.ListRouteCalculators)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listroutecalculatorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRouteCalculatorsRequestListRouteCalculatorsPaginateTypeDef]
    ) -> AsyncIterator[ListRouteCalculatorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListRouteCalculators.html#LocationService.Paginator.ListRouteCalculators.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listroutecalculatorspaginator)
        """


class ListTrackerConsumersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListTrackerConsumers.html#LocationService.Paginator.ListTrackerConsumers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listtrackerconsumerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTrackerConsumersRequestListTrackerConsumersPaginateTypeDef]
    ) -> AsyncIterator[ListTrackerConsumersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListTrackerConsumers.html#LocationService.Paginator.ListTrackerConsumers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listtrackerconsumerspaginator)
        """


class ListTrackersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListTrackers.html#LocationService.Paginator.ListTrackers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listtrackerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTrackersRequestListTrackersPaginateTypeDef]
    ) -> AsyncIterator[ListTrackersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListTrackers.html#LocationService.Paginator.ListTrackers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listtrackerspaginator)
        """
