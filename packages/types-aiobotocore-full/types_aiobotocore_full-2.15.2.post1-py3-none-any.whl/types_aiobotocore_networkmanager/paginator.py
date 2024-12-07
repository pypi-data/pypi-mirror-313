"""
Type annotations for networkmanager service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_networkmanager.client import NetworkManagerClient
    from types_aiobotocore_networkmanager.paginator import (
        DescribeGlobalNetworksPaginator,
        GetConnectPeerAssociationsPaginator,
        GetConnectionsPaginator,
        GetCoreNetworkChangeEventsPaginator,
        GetCoreNetworkChangeSetPaginator,
        GetCustomerGatewayAssociationsPaginator,
        GetDevicesPaginator,
        GetLinkAssociationsPaginator,
        GetLinksPaginator,
        GetNetworkResourceCountsPaginator,
        GetNetworkResourceRelationshipsPaginator,
        GetNetworkResourcesPaginator,
        GetNetworkTelemetryPaginator,
        GetSitesPaginator,
        GetTransitGatewayConnectPeerAssociationsPaginator,
        GetTransitGatewayRegistrationsPaginator,
        ListAttachmentsPaginator,
        ListConnectPeersPaginator,
        ListCoreNetworkPolicyVersionsPaginator,
        ListCoreNetworksPaginator,
        ListPeeringsPaginator,
    )

    session = get_session()
    with session.create_client("networkmanager") as client:
        client: NetworkManagerClient

        describe_global_networks_paginator: DescribeGlobalNetworksPaginator = client.get_paginator("describe_global_networks")
        get_connect_peer_associations_paginator: GetConnectPeerAssociationsPaginator = client.get_paginator("get_connect_peer_associations")
        get_connections_paginator: GetConnectionsPaginator = client.get_paginator("get_connections")
        get_core_network_change_events_paginator: GetCoreNetworkChangeEventsPaginator = client.get_paginator("get_core_network_change_events")
        get_core_network_change_set_paginator: GetCoreNetworkChangeSetPaginator = client.get_paginator("get_core_network_change_set")
        get_customer_gateway_associations_paginator: GetCustomerGatewayAssociationsPaginator = client.get_paginator("get_customer_gateway_associations")
        get_devices_paginator: GetDevicesPaginator = client.get_paginator("get_devices")
        get_link_associations_paginator: GetLinkAssociationsPaginator = client.get_paginator("get_link_associations")
        get_links_paginator: GetLinksPaginator = client.get_paginator("get_links")
        get_network_resource_counts_paginator: GetNetworkResourceCountsPaginator = client.get_paginator("get_network_resource_counts")
        get_network_resource_relationships_paginator: GetNetworkResourceRelationshipsPaginator = client.get_paginator("get_network_resource_relationships")
        get_network_resources_paginator: GetNetworkResourcesPaginator = client.get_paginator("get_network_resources")
        get_network_telemetry_paginator: GetNetworkTelemetryPaginator = client.get_paginator("get_network_telemetry")
        get_sites_paginator: GetSitesPaginator = client.get_paginator("get_sites")
        get_transit_gateway_connect_peer_associations_paginator: GetTransitGatewayConnectPeerAssociationsPaginator = client.get_paginator("get_transit_gateway_connect_peer_associations")
        get_transit_gateway_registrations_paginator: GetTransitGatewayRegistrationsPaginator = client.get_paginator("get_transit_gateway_registrations")
        list_attachments_paginator: ListAttachmentsPaginator = client.get_paginator("list_attachments")
        list_connect_peers_paginator: ListConnectPeersPaginator = client.get_paginator("list_connect_peers")
        list_core_network_policy_versions_paginator: ListCoreNetworkPolicyVersionsPaginator = client.get_paginator("list_core_network_policy_versions")
        list_core_networks_paginator: ListCoreNetworksPaginator = client.get_paginator("list_core_networks")
        list_peerings_paginator: ListPeeringsPaginator = client.get_paginator("list_peerings")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeGlobalNetworksRequestDescribeGlobalNetworksPaginateTypeDef,
    DescribeGlobalNetworksResponseTypeDef,
    GetConnectionsRequestGetConnectionsPaginateTypeDef,
    GetConnectionsResponseTypeDef,
    GetConnectPeerAssociationsRequestGetConnectPeerAssociationsPaginateTypeDef,
    GetConnectPeerAssociationsResponseTypeDef,
    GetCoreNetworkChangeEventsRequestGetCoreNetworkChangeEventsPaginateTypeDef,
    GetCoreNetworkChangeEventsResponseTypeDef,
    GetCoreNetworkChangeSetRequestGetCoreNetworkChangeSetPaginateTypeDef,
    GetCoreNetworkChangeSetResponseTypeDef,
    GetCustomerGatewayAssociationsRequestGetCustomerGatewayAssociationsPaginateTypeDef,
    GetCustomerGatewayAssociationsResponseTypeDef,
    GetDevicesRequestGetDevicesPaginateTypeDef,
    GetDevicesResponseTypeDef,
    GetLinkAssociationsRequestGetLinkAssociationsPaginateTypeDef,
    GetLinkAssociationsResponseTypeDef,
    GetLinksRequestGetLinksPaginateTypeDef,
    GetLinksResponseTypeDef,
    GetNetworkResourceCountsRequestGetNetworkResourceCountsPaginateTypeDef,
    GetNetworkResourceCountsResponseTypeDef,
    GetNetworkResourceRelationshipsRequestGetNetworkResourceRelationshipsPaginateTypeDef,
    GetNetworkResourceRelationshipsResponseTypeDef,
    GetNetworkResourcesRequestGetNetworkResourcesPaginateTypeDef,
    GetNetworkResourcesResponseTypeDef,
    GetNetworkTelemetryRequestGetNetworkTelemetryPaginateTypeDef,
    GetNetworkTelemetryResponseTypeDef,
    GetSitesRequestGetSitesPaginateTypeDef,
    GetSitesResponseTypeDef,
    GetTransitGatewayConnectPeerAssociationsRequestGetTransitGatewayConnectPeerAssociationsPaginateTypeDef,
    GetTransitGatewayConnectPeerAssociationsResponseTypeDef,
    GetTransitGatewayRegistrationsRequestGetTransitGatewayRegistrationsPaginateTypeDef,
    GetTransitGatewayRegistrationsResponseTypeDef,
    ListAttachmentsRequestListAttachmentsPaginateTypeDef,
    ListAttachmentsResponseTypeDef,
    ListConnectPeersRequestListConnectPeersPaginateTypeDef,
    ListConnectPeersResponseTypeDef,
    ListCoreNetworkPolicyVersionsRequestListCoreNetworkPolicyVersionsPaginateTypeDef,
    ListCoreNetworkPolicyVersionsResponseTypeDef,
    ListCoreNetworksRequestListCoreNetworksPaginateTypeDef,
    ListCoreNetworksResponseTypeDef,
    ListPeeringsRequestListPeeringsPaginateTypeDef,
    ListPeeringsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeGlobalNetworksPaginator",
    "GetConnectPeerAssociationsPaginator",
    "GetConnectionsPaginator",
    "GetCoreNetworkChangeEventsPaginator",
    "GetCoreNetworkChangeSetPaginator",
    "GetCustomerGatewayAssociationsPaginator",
    "GetDevicesPaginator",
    "GetLinkAssociationsPaginator",
    "GetLinksPaginator",
    "GetNetworkResourceCountsPaginator",
    "GetNetworkResourceRelationshipsPaginator",
    "GetNetworkResourcesPaginator",
    "GetNetworkTelemetryPaginator",
    "GetSitesPaginator",
    "GetTransitGatewayConnectPeerAssociationsPaginator",
    "GetTransitGatewayRegistrationsPaginator",
    "ListAttachmentsPaginator",
    "ListConnectPeersPaginator",
    "ListCoreNetworkPolicyVersionsPaginator",
    "ListCoreNetworksPaginator",
    "ListPeeringsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeGlobalNetworksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/DescribeGlobalNetworks.html#NetworkManager.Paginator.DescribeGlobalNetworks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#describeglobalnetworkspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeGlobalNetworksRequestDescribeGlobalNetworksPaginateTypeDef]
    ) -> AsyncIterator[DescribeGlobalNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/DescribeGlobalNetworks.html#NetworkManager.Paginator.DescribeGlobalNetworks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#describeglobalnetworkspaginator)
        """


class GetConnectPeerAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetConnectPeerAssociations.html#NetworkManager.Paginator.GetConnectPeerAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getconnectpeerassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetConnectPeerAssociationsRequestGetConnectPeerAssociationsPaginateTypeDef
        ],
    ) -> AsyncIterator[GetConnectPeerAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetConnectPeerAssociations.html#NetworkManager.Paginator.GetConnectPeerAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getconnectpeerassociationspaginator)
        """


class GetConnectionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetConnections.html#NetworkManager.Paginator.GetConnections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getconnectionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetConnectionsRequestGetConnectionsPaginateTypeDef]
    ) -> AsyncIterator[GetConnectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetConnections.html#NetworkManager.Paginator.GetConnections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getconnectionspaginator)
        """


class GetCoreNetworkChangeEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCoreNetworkChangeEvents.html#NetworkManager.Paginator.GetCoreNetworkChangeEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getcorenetworkchangeeventspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetCoreNetworkChangeEventsRequestGetCoreNetworkChangeEventsPaginateTypeDef
        ],
    ) -> AsyncIterator[GetCoreNetworkChangeEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCoreNetworkChangeEvents.html#NetworkManager.Paginator.GetCoreNetworkChangeEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getcorenetworkchangeeventspaginator)
        """


class GetCoreNetworkChangeSetPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCoreNetworkChangeSet.html#NetworkManager.Paginator.GetCoreNetworkChangeSet)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getcorenetworkchangesetpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetCoreNetworkChangeSetRequestGetCoreNetworkChangeSetPaginateTypeDef]
    ) -> AsyncIterator[GetCoreNetworkChangeSetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCoreNetworkChangeSet.html#NetworkManager.Paginator.GetCoreNetworkChangeSet.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getcorenetworkchangesetpaginator)
        """


class GetCustomerGatewayAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCustomerGatewayAssociations.html#NetworkManager.Paginator.GetCustomerGatewayAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getcustomergatewayassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetCustomerGatewayAssociationsRequestGetCustomerGatewayAssociationsPaginateTypeDef
        ],
    ) -> AsyncIterator[GetCustomerGatewayAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCustomerGatewayAssociations.html#NetworkManager.Paginator.GetCustomerGatewayAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getcustomergatewayassociationspaginator)
        """


class GetDevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetDevices.html#NetworkManager.Paginator.GetDevices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getdevicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetDevicesRequestGetDevicesPaginateTypeDef]
    ) -> AsyncIterator[GetDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetDevices.html#NetworkManager.Paginator.GetDevices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getdevicespaginator)
        """


class GetLinkAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetLinkAssociations.html#NetworkManager.Paginator.GetLinkAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getlinkassociationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetLinkAssociationsRequestGetLinkAssociationsPaginateTypeDef]
    ) -> AsyncIterator[GetLinkAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetLinkAssociations.html#NetworkManager.Paginator.GetLinkAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getlinkassociationspaginator)
        """


class GetLinksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetLinks.html#NetworkManager.Paginator.GetLinks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getlinkspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetLinksRequestGetLinksPaginateTypeDef]
    ) -> AsyncIterator[GetLinksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetLinks.html#NetworkManager.Paginator.GetLinks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getlinkspaginator)
        """


class GetNetworkResourceCountsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResourceCounts.html#NetworkManager.Paginator.GetNetworkResourceCounts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getnetworkresourcecountspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[GetNetworkResourceCountsRequestGetNetworkResourceCountsPaginateTypeDef],
    ) -> AsyncIterator[GetNetworkResourceCountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResourceCounts.html#NetworkManager.Paginator.GetNetworkResourceCounts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getnetworkresourcecountspaginator)
        """


class GetNetworkResourceRelationshipsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResourceRelationships.html#NetworkManager.Paginator.GetNetworkResourceRelationships)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getnetworkresourcerelationshipspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetNetworkResourceRelationshipsRequestGetNetworkResourceRelationshipsPaginateTypeDef
        ],
    ) -> AsyncIterator[GetNetworkResourceRelationshipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResourceRelationships.html#NetworkManager.Paginator.GetNetworkResourceRelationships.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getnetworkresourcerelationshipspaginator)
        """


class GetNetworkResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResources.html#NetworkManager.Paginator.GetNetworkResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getnetworkresourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetNetworkResourcesRequestGetNetworkResourcesPaginateTypeDef]
    ) -> AsyncIterator[GetNetworkResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResources.html#NetworkManager.Paginator.GetNetworkResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getnetworkresourcespaginator)
        """


class GetNetworkTelemetryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkTelemetry.html#NetworkManager.Paginator.GetNetworkTelemetry)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getnetworktelemetrypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetNetworkTelemetryRequestGetNetworkTelemetryPaginateTypeDef]
    ) -> AsyncIterator[GetNetworkTelemetryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkTelemetry.html#NetworkManager.Paginator.GetNetworkTelemetry.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getnetworktelemetrypaginator)
        """


class GetSitesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetSites.html#NetworkManager.Paginator.GetSites)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getsitespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetSitesRequestGetSitesPaginateTypeDef]
    ) -> AsyncIterator[GetSitesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetSites.html#NetworkManager.Paginator.GetSites.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getsitespaginator)
        """


class GetTransitGatewayConnectPeerAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetTransitGatewayConnectPeerAssociations.html#NetworkManager.Paginator.GetTransitGatewayConnectPeerAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#gettransitgatewayconnectpeerassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetTransitGatewayConnectPeerAssociationsRequestGetTransitGatewayConnectPeerAssociationsPaginateTypeDef
        ],
    ) -> AsyncIterator[GetTransitGatewayConnectPeerAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetTransitGatewayConnectPeerAssociations.html#NetworkManager.Paginator.GetTransitGatewayConnectPeerAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#gettransitgatewayconnectpeerassociationspaginator)
        """


class GetTransitGatewayRegistrationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetTransitGatewayRegistrations.html#NetworkManager.Paginator.GetTransitGatewayRegistrations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#gettransitgatewayregistrationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetTransitGatewayRegistrationsRequestGetTransitGatewayRegistrationsPaginateTypeDef
        ],
    ) -> AsyncIterator[GetTransitGatewayRegistrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetTransitGatewayRegistrations.html#NetworkManager.Paginator.GetTransitGatewayRegistrations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#gettransitgatewayregistrationspaginator)
        """


class ListAttachmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListAttachments.html#NetworkManager.Paginator.ListAttachments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listattachmentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAttachmentsRequestListAttachmentsPaginateTypeDef]
    ) -> AsyncIterator[ListAttachmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListAttachments.html#NetworkManager.Paginator.ListAttachments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listattachmentspaginator)
        """


class ListConnectPeersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListConnectPeers.html#NetworkManager.Paginator.ListConnectPeers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listconnectpeerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListConnectPeersRequestListConnectPeersPaginateTypeDef]
    ) -> AsyncIterator[ListConnectPeersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListConnectPeers.html#NetworkManager.Paginator.ListConnectPeers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listconnectpeerspaginator)
        """


class ListCoreNetworkPolicyVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListCoreNetworkPolicyVersions.html#NetworkManager.Paginator.ListCoreNetworkPolicyVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listcorenetworkpolicyversionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListCoreNetworkPolicyVersionsRequestListCoreNetworkPolicyVersionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListCoreNetworkPolicyVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListCoreNetworkPolicyVersions.html#NetworkManager.Paginator.ListCoreNetworkPolicyVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listcorenetworkpolicyversionspaginator)
        """


class ListCoreNetworksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListCoreNetworks.html#NetworkManager.Paginator.ListCoreNetworks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listcorenetworkspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCoreNetworksRequestListCoreNetworksPaginateTypeDef]
    ) -> AsyncIterator[ListCoreNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListCoreNetworks.html#NetworkManager.Paginator.ListCoreNetworks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listcorenetworkspaginator)
        """


class ListPeeringsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListPeerings.html#NetworkManager.Paginator.ListPeerings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listpeeringspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPeeringsRequestListPeeringsPaginateTypeDef]
    ) -> AsyncIterator[ListPeeringsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListPeerings.html#NetworkManager.Paginator.ListPeerings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listpeeringspaginator)
        """
