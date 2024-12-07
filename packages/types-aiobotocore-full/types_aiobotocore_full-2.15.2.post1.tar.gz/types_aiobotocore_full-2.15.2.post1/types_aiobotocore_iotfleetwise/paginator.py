"""
Type annotations for iotfleetwise service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iotfleetwise.client import IoTFleetWiseClient
    from types_aiobotocore_iotfleetwise.paginator import (
        GetVehicleStatusPaginator,
        ListCampaignsPaginator,
        ListDecoderManifestNetworkInterfacesPaginator,
        ListDecoderManifestSignalsPaginator,
        ListDecoderManifestsPaginator,
        ListFleetsForVehiclePaginator,
        ListFleetsPaginator,
        ListModelManifestNodesPaginator,
        ListModelManifestsPaginator,
        ListSignalCatalogNodesPaginator,
        ListSignalCatalogsPaginator,
        ListVehiclesInFleetPaginator,
        ListVehiclesPaginator,
    )

    session = get_session()
    with session.create_client("iotfleetwise") as client:
        client: IoTFleetWiseClient

        get_vehicle_status_paginator: GetVehicleStatusPaginator = client.get_paginator("get_vehicle_status")
        list_campaigns_paginator: ListCampaignsPaginator = client.get_paginator("list_campaigns")
        list_decoder_manifest_network_interfaces_paginator: ListDecoderManifestNetworkInterfacesPaginator = client.get_paginator("list_decoder_manifest_network_interfaces")
        list_decoder_manifest_signals_paginator: ListDecoderManifestSignalsPaginator = client.get_paginator("list_decoder_manifest_signals")
        list_decoder_manifests_paginator: ListDecoderManifestsPaginator = client.get_paginator("list_decoder_manifests")
        list_fleets_for_vehicle_paginator: ListFleetsForVehiclePaginator = client.get_paginator("list_fleets_for_vehicle")
        list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
        list_model_manifest_nodes_paginator: ListModelManifestNodesPaginator = client.get_paginator("list_model_manifest_nodes")
        list_model_manifests_paginator: ListModelManifestsPaginator = client.get_paginator("list_model_manifests")
        list_signal_catalog_nodes_paginator: ListSignalCatalogNodesPaginator = client.get_paginator("list_signal_catalog_nodes")
        list_signal_catalogs_paginator: ListSignalCatalogsPaginator = client.get_paginator("list_signal_catalogs")
        list_vehicles_in_fleet_paginator: ListVehiclesInFleetPaginator = client.get_paginator("list_vehicles_in_fleet")
        list_vehicles_paginator: ListVehiclesPaginator = client.get_paginator("list_vehicles")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetVehicleStatusRequestGetVehicleStatusPaginateTypeDef,
    GetVehicleStatusResponseTypeDef,
    ListCampaignsRequestListCampaignsPaginateTypeDef,
    ListCampaignsResponseTypeDef,
    ListDecoderManifestNetworkInterfacesRequestListDecoderManifestNetworkInterfacesPaginateTypeDef,
    ListDecoderManifestNetworkInterfacesResponseTypeDef,
    ListDecoderManifestSignalsRequestListDecoderManifestSignalsPaginateTypeDef,
    ListDecoderManifestSignalsResponsePaginatorTypeDef,
    ListDecoderManifestsRequestListDecoderManifestsPaginateTypeDef,
    ListDecoderManifestsResponseTypeDef,
    ListFleetsForVehicleRequestListFleetsForVehiclePaginateTypeDef,
    ListFleetsForVehicleResponseTypeDef,
    ListFleetsRequestListFleetsPaginateTypeDef,
    ListFleetsResponseTypeDef,
    ListModelManifestNodesRequestListModelManifestNodesPaginateTypeDef,
    ListModelManifestNodesResponseTypeDef,
    ListModelManifestsRequestListModelManifestsPaginateTypeDef,
    ListModelManifestsResponseTypeDef,
    ListSignalCatalogNodesRequestListSignalCatalogNodesPaginateTypeDef,
    ListSignalCatalogNodesResponseTypeDef,
    ListSignalCatalogsRequestListSignalCatalogsPaginateTypeDef,
    ListSignalCatalogsResponseTypeDef,
    ListVehiclesInFleetRequestListVehiclesInFleetPaginateTypeDef,
    ListVehiclesInFleetResponseTypeDef,
    ListVehiclesRequestListVehiclesPaginateTypeDef,
    ListVehiclesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetVehicleStatusPaginator",
    "ListCampaignsPaginator",
    "ListDecoderManifestNetworkInterfacesPaginator",
    "ListDecoderManifestSignalsPaginator",
    "ListDecoderManifestsPaginator",
    "ListFleetsForVehiclePaginator",
    "ListFleetsPaginator",
    "ListModelManifestNodesPaginator",
    "ListModelManifestsPaginator",
    "ListSignalCatalogNodesPaginator",
    "ListSignalCatalogsPaginator",
    "ListVehiclesInFleetPaginator",
    "ListVehiclesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetVehicleStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/GetVehicleStatus.html#IoTFleetWise.Paginator.GetVehicleStatus)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#getvehiclestatuspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetVehicleStatusRequestGetVehicleStatusPaginateTypeDef]
    ) -> AsyncIterator[GetVehicleStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/GetVehicleStatus.html#IoTFleetWise.Paginator.GetVehicleStatus.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#getvehiclestatuspaginator)
        """


class ListCampaignsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListCampaigns.html#IoTFleetWise.Paginator.ListCampaigns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listcampaignspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCampaignsRequestListCampaignsPaginateTypeDef]
    ) -> AsyncIterator[ListCampaignsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListCampaigns.html#IoTFleetWise.Paginator.ListCampaigns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listcampaignspaginator)
        """


class ListDecoderManifestNetworkInterfacesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifestNetworkInterfaces.html#IoTFleetWise.Paginator.ListDecoderManifestNetworkInterfaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestnetworkinterfacespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListDecoderManifestNetworkInterfacesRequestListDecoderManifestNetworkInterfacesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListDecoderManifestNetworkInterfacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifestNetworkInterfaces.html#IoTFleetWise.Paginator.ListDecoderManifestNetworkInterfaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestnetworkinterfacespaginator)
        """


class ListDecoderManifestSignalsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifestSignals.html#IoTFleetWise.Paginator.ListDecoderManifestSignals)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestsignalspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListDecoderManifestSignalsRequestListDecoderManifestSignalsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListDecoderManifestSignalsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifestSignals.html#IoTFleetWise.Paginator.ListDecoderManifestSignals.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestsignalspaginator)
        """


class ListDecoderManifestsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifests.html#IoTFleetWise.Paginator.ListDecoderManifests)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDecoderManifestsRequestListDecoderManifestsPaginateTypeDef]
    ) -> AsyncIterator[ListDecoderManifestsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifests.html#IoTFleetWise.Paginator.ListDecoderManifests.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestspaginator)
        """


class ListFleetsForVehiclePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListFleetsForVehicle.html#IoTFleetWise.Paginator.ListFleetsForVehicle)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listfleetsforvehiclepaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFleetsForVehicleRequestListFleetsForVehiclePaginateTypeDef]
    ) -> AsyncIterator[ListFleetsForVehicleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListFleetsForVehicle.html#IoTFleetWise.Paginator.ListFleetsForVehicle.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listfleetsforvehiclepaginator)
        """


class ListFleetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListFleets.html#IoTFleetWise.Paginator.ListFleets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listfleetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFleetsRequestListFleetsPaginateTypeDef]
    ) -> AsyncIterator[ListFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListFleets.html#IoTFleetWise.Paginator.ListFleets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listfleetspaginator)
        """


class ListModelManifestNodesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListModelManifestNodes.html#IoTFleetWise.Paginator.ListModelManifestNodes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listmodelmanifestnodespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListModelManifestNodesRequestListModelManifestNodesPaginateTypeDef]
    ) -> AsyncIterator[ListModelManifestNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListModelManifestNodes.html#IoTFleetWise.Paginator.ListModelManifestNodes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listmodelmanifestnodespaginator)
        """


class ListModelManifestsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListModelManifests.html#IoTFleetWise.Paginator.ListModelManifests)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listmodelmanifestspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListModelManifestsRequestListModelManifestsPaginateTypeDef]
    ) -> AsyncIterator[ListModelManifestsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListModelManifests.html#IoTFleetWise.Paginator.ListModelManifests.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listmodelmanifestspaginator)
        """


class ListSignalCatalogNodesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListSignalCatalogNodes.html#IoTFleetWise.Paginator.ListSignalCatalogNodes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listsignalcatalognodespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSignalCatalogNodesRequestListSignalCatalogNodesPaginateTypeDef]
    ) -> AsyncIterator[ListSignalCatalogNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListSignalCatalogNodes.html#IoTFleetWise.Paginator.ListSignalCatalogNodes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listsignalcatalognodespaginator)
        """


class ListSignalCatalogsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListSignalCatalogs.html#IoTFleetWise.Paginator.ListSignalCatalogs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listsignalcatalogspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSignalCatalogsRequestListSignalCatalogsPaginateTypeDef]
    ) -> AsyncIterator[ListSignalCatalogsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListSignalCatalogs.html#IoTFleetWise.Paginator.ListSignalCatalogs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listsignalcatalogspaginator)
        """


class ListVehiclesInFleetPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListVehiclesInFleet.html#IoTFleetWise.Paginator.ListVehiclesInFleet)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listvehiclesinfleetpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListVehiclesInFleetRequestListVehiclesInFleetPaginateTypeDef]
    ) -> AsyncIterator[ListVehiclesInFleetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListVehiclesInFleet.html#IoTFleetWise.Paginator.ListVehiclesInFleet.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listvehiclesinfleetpaginator)
        """


class ListVehiclesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListVehicles.html#IoTFleetWise.Paginator.ListVehicles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listvehiclespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListVehiclesRequestListVehiclesPaginateTypeDef]
    ) -> AsyncIterator[ListVehiclesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListVehicles.html#IoTFleetWise.Paginator.ListVehicles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listvehiclespaginator)
        """
