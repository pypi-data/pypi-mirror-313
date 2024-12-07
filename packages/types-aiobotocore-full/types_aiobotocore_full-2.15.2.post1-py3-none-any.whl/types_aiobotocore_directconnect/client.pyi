"""
Type annotations for directconnect service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_directconnect.client import DirectConnectClient

    session = get_session()
    async with session.create_client("directconnect") as client:
        client: DirectConnectClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    DescribeDirectConnectGatewayAssociationsPaginator,
    DescribeDirectConnectGatewayAttachmentsPaginator,
    DescribeDirectConnectGatewaysPaginator,
)
from .type_defs import (
    AcceptDirectConnectGatewayAssociationProposalRequestRequestTypeDef,
    AcceptDirectConnectGatewayAssociationProposalResultTypeDef,
    AllocateConnectionOnInterconnectRequestRequestTypeDef,
    AllocateHostedConnectionRequestRequestTypeDef,
    AllocatePrivateVirtualInterfaceRequestRequestTypeDef,
    AllocatePublicVirtualInterfaceRequestRequestTypeDef,
    AllocateTransitVirtualInterfaceRequestRequestTypeDef,
    AllocateTransitVirtualInterfaceResultTypeDef,
    AssociateConnectionWithLagRequestRequestTypeDef,
    AssociateHostedConnectionRequestRequestTypeDef,
    AssociateMacSecKeyRequestRequestTypeDef,
    AssociateMacSecKeyResponseTypeDef,
    AssociateVirtualInterfaceRequestRequestTypeDef,
    ConfirmConnectionRequestRequestTypeDef,
    ConfirmConnectionResponseTypeDef,
    ConfirmCustomerAgreementRequestRequestTypeDef,
    ConfirmCustomerAgreementResponseTypeDef,
    ConfirmPrivateVirtualInterfaceRequestRequestTypeDef,
    ConfirmPrivateVirtualInterfaceResponseTypeDef,
    ConfirmPublicVirtualInterfaceRequestRequestTypeDef,
    ConfirmPublicVirtualInterfaceResponseTypeDef,
    ConfirmTransitVirtualInterfaceRequestRequestTypeDef,
    ConfirmTransitVirtualInterfaceResponseTypeDef,
    ConnectionResponseTypeDef,
    ConnectionsTypeDef,
    CreateBGPPeerRequestRequestTypeDef,
    CreateBGPPeerResponseTypeDef,
    CreateConnectionRequestRequestTypeDef,
    CreateDirectConnectGatewayAssociationProposalRequestRequestTypeDef,
    CreateDirectConnectGatewayAssociationProposalResultTypeDef,
    CreateDirectConnectGatewayAssociationRequestRequestTypeDef,
    CreateDirectConnectGatewayAssociationResultTypeDef,
    CreateDirectConnectGatewayRequestRequestTypeDef,
    CreateDirectConnectGatewayResultTypeDef,
    CreateInterconnectRequestRequestTypeDef,
    CreateLagRequestRequestTypeDef,
    CreatePrivateVirtualInterfaceRequestRequestTypeDef,
    CreatePublicVirtualInterfaceRequestRequestTypeDef,
    CreateTransitVirtualInterfaceRequestRequestTypeDef,
    CreateTransitVirtualInterfaceResultTypeDef,
    DeleteBGPPeerRequestRequestTypeDef,
    DeleteBGPPeerResponseTypeDef,
    DeleteConnectionRequestRequestTypeDef,
    DeleteDirectConnectGatewayAssociationProposalRequestRequestTypeDef,
    DeleteDirectConnectGatewayAssociationProposalResultTypeDef,
    DeleteDirectConnectGatewayAssociationRequestRequestTypeDef,
    DeleteDirectConnectGatewayAssociationResultTypeDef,
    DeleteDirectConnectGatewayRequestRequestTypeDef,
    DeleteDirectConnectGatewayResultTypeDef,
    DeleteInterconnectRequestRequestTypeDef,
    DeleteInterconnectResponseTypeDef,
    DeleteLagRequestRequestTypeDef,
    DeleteVirtualInterfaceRequestRequestTypeDef,
    DeleteVirtualInterfaceResponseTypeDef,
    DescribeConnectionLoaRequestRequestTypeDef,
    DescribeConnectionLoaResponseTypeDef,
    DescribeConnectionsOnInterconnectRequestRequestTypeDef,
    DescribeConnectionsRequestRequestTypeDef,
    DescribeCustomerMetadataResponseTypeDef,
    DescribeDirectConnectGatewayAssociationProposalsRequestRequestTypeDef,
    DescribeDirectConnectGatewayAssociationProposalsResultTypeDef,
    DescribeDirectConnectGatewayAssociationsRequestRequestTypeDef,
    DescribeDirectConnectGatewayAssociationsResultTypeDef,
    DescribeDirectConnectGatewayAttachmentsRequestRequestTypeDef,
    DescribeDirectConnectGatewayAttachmentsResultTypeDef,
    DescribeDirectConnectGatewaysRequestRequestTypeDef,
    DescribeDirectConnectGatewaysResultTypeDef,
    DescribeHostedConnectionsRequestRequestTypeDef,
    DescribeInterconnectLoaRequestRequestTypeDef,
    DescribeInterconnectLoaResponseTypeDef,
    DescribeInterconnectsRequestRequestTypeDef,
    DescribeLagsRequestRequestTypeDef,
    DescribeLoaRequestRequestTypeDef,
    DescribeRouterConfigurationRequestRequestTypeDef,
    DescribeRouterConfigurationResponseTypeDef,
    DescribeTagsRequestRequestTypeDef,
    DescribeTagsResponseTypeDef,
    DescribeVirtualInterfacesRequestRequestTypeDef,
    DisassociateConnectionFromLagRequestRequestTypeDef,
    DisassociateMacSecKeyRequestRequestTypeDef,
    DisassociateMacSecKeyResponseTypeDef,
    InterconnectResponseTypeDef,
    InterconnectsTypeDef,
    LagResponseTypeDef,
    LagsTypeDef,
    ListVirtualInterfaceTestHistoryRequestRequestTypeDef,
    ListVirtualInterfaceTestHistoryResponseTypeDef,
    LoaResponseTypeDef,
    LocationsTypeDef,
    StartBgpFailoverTestRequestRequestTypeDef,
    StartBgpFailoverTestResponseTypeDef,
    StopBgpFailoverTestRequestRequestTypeDef,
    StopBgpFailoverTestResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateConnectionRequestRequestTypeDef,
    UpdateDirectConnectGatewayAssociationRequestRequestTypeDef,
    UpdateDirectConnectGatewayAssociationResultTypeDef,
    UpdateDirectConnectGatewayRequestRequestTypeDef,
    UpdateDirectConnectGatewayResponseTypeDef,
    UpdateLagRequestRequestTypeDef,
    UpdateVirtualInterfaceAttributesRequestRequestTypeDef,
    VirtualGatewaysTypeDef,
    VirtualInterfaceResponseTypeDef,
    VirtualInterfacesTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("DirectConnectClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    DirectConnectClientException: Type[BotocoreClientError]
    DirectConnectServerException: Type[BotocoreClientError]
    DuplicateTagKeysException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]

class DirectConnectClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DirectConnectClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#close)
        """

    async def accept_direct_connect_gateway_association_proposal(
        self, **kwargs: Unpack[AcceptDirectConnectGatewayAssociationProposalRequestRequestTypeDef]
    ) -> AcceptDirectConnectGatewayAssociationProposalResultTypeDef:
        """
        Accepts a proposal request to attach a virtual private gateway or transit
        gateway to a Direct Connect gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/accept_direct_connect_gateway_association_proposal.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#accept_direct_connect_gateway_association_proposal)
        """

    async def allocate_connection_on_interconnect(
        self, **kwargs: Unpack[AllocateConnectionOnInterconnectRequestRequestTypeDef]
    ) -> ConnectionResponseTypeDef:
        """
        Deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/allocate_connection_on_interconnect.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#allocate_connection_on_interconnect)
        """

    async def allocate_hosted_connection(
        self, **kwargs: Unpack[AllocateHostedConnectionRequestRequestTypeDef]
    ) -> ConnectionResponseTypeDef:
        """
        Creates a hosted connection on the specified interconnect or a link aggregation
        group (LAG) of interconnects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/allocate_hosted_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#allocate_hosted_connection)
        """

    async def allocate_private_virtual_interface(
        self, **kwargs: Unpack[AllocatePrivateVirtualInterfaceRequestRequestTypeDef]
    ) -> VirtualInterfaceResponseTypeDef:
        """
        Provisions a private virtual interface to be owned by the specified Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/allocate_private_virtual_interface.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#allocate_private_virtual_interface)
        """

    async def allocate_public_virtual_interface(
        self, **kwargs: Unpack[AllocatePublicVirtualInterfaceRequestRequestTypeDef]
    ) -> VirtualInterfaceResponseTypeDef:
        """
        Provisions a public virtual interface to be owned by the specified Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/allocate_public_virtual_interface.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#allocate_public_virtual_interface)
        """

    async def allocate_transit_virtual_interface(
        self, **kwargs: Unpack[AllocateTransitVirtualInterfaceRequestRequestTypeDef]
    ) -> AllocateTransitVirtualInterfaceResultTypeDef:
        """
        Provisions a transit virtual interface to be owned by the specified Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/allocate_transit_virtual_interface.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#allocate_transit_virtual_interface)
        """

    async def associate_connection_with_lag(
        self, **kwargs: Unpack[AssociateConnectionWithLagRequestRequestTypeDef]
    ) -> ConnectionResponseTypeDef:
        """
        Associates an existing connection with a link aggregation group (LAG).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/associate_connection_with_lag.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#associate_connection_with_lag)
        """

    async def associate_hosted_connection(
        self, **kwargs: Unpack[AssociateHostedConnectionRequestRequestTypeDef]
    ) -> ConnectionResponseTypeDef:
        """
        Associates a hosted connection and its virtual interfaces with a link
        aggregation group (LAG) or interconnect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/associate_hosted_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#associate_hosted_connection)
        """

    async def associate_mac_sec_key(
        self, **kwargs: Unpack[AssociateMacSecKeyRequestRequestTypeDef]
    ) -> AssociateMacSecKeyResponseTypeDef:
        """
        Associates a MAC Security (MACsec) Connection Key Name (CKN)/ Connectivity
        Association Key (CAK) pair with an Direct Connect dedicated connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/associate_mac_sec_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#associate_mac_sec_key)
        """

    async def associate_virtual_interface(
        self, **kwargs: Unpack[AssociateVirtualInterfaceRequestRequestTypeDef]
    ) -> VirtualInterfaceResponseTypeDef:
        """
        Associates a virtual interface with a specified link aggregation group (LAG) or
        connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/associate_virtual_interface.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#associate_virtual_interface)
        """

    async def confirm_connection(
        self, **kwargs: Unpack[ConfirmConnectionRequestRequestTypeDef]
    ) -> ConfirmConnectionResponseTypeDef:
        """
        Confirms the creation of the specified hosted connection on an interconnect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/confirm_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#confirm_connection)
        """

    async def confirm_customer_agreement(
        self, **kwargs: Unpack[ConfirmCustomerAgreementRequestRequestTypeDef]
    ) -> ConfirmCustomerAgreementResponseTypeDef:
        """
        The confirmation of the terms of agreement when creating the connection/link
        aggregation group (LAG).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/confirm_customer_agreement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#confirm_customer_agreement)
        """

    async def confirm_private_virtual_interface(
        self, **kwargs: Unpack[ConfirmPrivateVirtualInterfaceRequestRequestTypeDef]
    ) -> ConfirmPrivateVirtualInterfaceResponseTypeDef:
        """
        Accepts ownership of a private virtual interface created by another Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/confirm_private_virtual_interface.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#confirm_private_virtual_interface)
        """

    async def confirm_public_virtual_interface(
        self, **kwargs: Unpack[ConfirmPublicVirtualInterfaceRequestRequestTypeDef]
    ) -> ConfirmPublicVirtualInterfaceResponseTypeDef:
        """
        Accepts ownership of a public virtual interface created by another Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/confirm_public_virtual_interface.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#confirm_public_virtual_interface)
        """

    async def confirm_transit_virtual_interface(
        self, **kwargs: Unpack[ConfirmTransitVirtualInterfaceRequestRequestTypeDef]
    ) -> ConfirmTransitVirtualInterfaceResponseTypeDef:
        """
        Accepts ownership of a transit virtual interface created by another Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/confirm_transit_virtual_interface.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#confirm_transit_virtual_interface)
        """

    async def create_bgp_peer(
        self, **kwargs: Unpack[CreateBGPPeerRequestRequestTypeDef]
    ) -> CreateBGPPeerResponseTypeDef:
        """
        Creates a BGP peer on the specified virtual interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/create_bgp_peer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_bgp_peer)
        """

    async def create_connection(
        self, **kwargs: Unpack[CreateConnectionRequestRequestTypeDef]
    ) -> ConnectionResponseTypeDef:
        """
        Creates a connection between a customer network and a specific Direct Connect
        location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/create_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_connection)
        """

    async def create_direct_connect_gateway(
        self, **kwargs: Unpack[CreateDirectConnectGatewayRequestRequestTypeDef]
    ) -> CreateDirectConnectGatewayResultTypeDef:
        """
        Creates a Direct Connect gateway, which is an intermediate object that enables
        you to connect a set of virtual interfaces and virtual private gateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/create_direct_connect_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_direct_connect_gateway)
        """

    async def create_direct_connect_gateway_association(
        self, **kwargs: Unpack[CreateDirectConnectGatewayAssociationRequestRequestTypeDef]
    ) -> CreateDirectConnectGatewayAssociationResultTypeDef:
        """
        Creates an association between a Direct Connect gateway and a virtual private
        gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/create_direct_connect_gateway_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_direct_connect_gateway_association)
        """

    async def create_direct_connect_gateway_association_proposal(
        self, **kwargs: Unpack[CreateDirectConnectGatewayAssociationProposalRequestRequestTypeDef]
    ) -> CreateDirectConnectGatewayAssociationProposalResultTypeDef:
        """
        Creates a proposal to associate the specified virtual private gateway or
        transit gateway with the specified Direct Connect gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/create_direct_connect_gateway_association_proposal.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_direct_connect_gateway_association_proposal)
        """

    async def create_interconnect(
        self, **kwargs: Unpack[CreateInterconnectRequestRequestTypeDef]
    ) -> InterconnectResponseTypeDef:
        """
        Creates an interconnect between an Direct Connect Partner's network and a
        specific Direct Connect location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/create_interconnect.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_interconnect)
        """

    async def create_lag(
        self, **kwargs: Unpack[CreateLagRequestRequestTypeDef]
    ) -> LagResponseTypeDef:
        """
        Creates a link aggregation group (LAG) with the specified number of bundled
        physical dedicated connections between the customer network and a specific
        Direct Connect location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/create_lag.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_lag)
        """

    async def create_private_virtual_interface(
        self, **kwargs: Unpack[CreatePrivateVirtualInterfaceRequestRequestTypeDef]
    ) -> VirtualInterfaceResponseTypeDef:
        """
        Creates a private virtual interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/create_private_virtual_interface.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_private_virtual_interface)
        """

    async def create_public_virtual_interface(
        self, **kwargs: Unpack[CreatePublicVirtualInterfaceRequestRequestTypeDef]
    ) -> VirtualInterfaceResponseTypeDef:
        """
        Creates a public virtual interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/create_public_virtual_interface.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_public_virtual_interface)
        """

    async def create_transit_virtual_interface(
        self, **kwargs: Unpack[CreateTransitVirtualInterfaceRequestRequestTypeDef]
    ) -> CreateTransitVirtualInterfaceResultTypeDef:
        """
        Creates a transit virtual interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/create_transit_virtual_interface.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_transit_virtual_interface)
        """

    async def delete_bgp_peer(
        self, **kwargs: Unpack[DeleteBGPPeerRequestRequestTypeDef]
    ) -> DeleteBGPPeerResponseTypeDef:
        """
        Deletes the specified BGP peer on the specified virtual interface with the
        specified customer address and ASN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/delete_bgp_peer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#delete_bgp_peer)
        """

    async def delete_connection(
        self, **kwargs: Unpack[DeleteConnectionRequestRequestTypeDef]
    ) -> ConnectionResponseTypeDef:
        """
        Deletes the specified connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/delete_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#delete_connection)
        """

    async def delete_direct_connect_gateway(
        self, **kwargs: Unpack[DeleteDirectConnectGatewayRequestRequestTypeDef]
    ) -> DeleteDirectConnectGatewayResultTypeDef:
        """
        Deletes the specified Direct Connect gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/delete_direct_connect_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#delete_direct_connect_gateway)
        """

    async def delete_direct_connect_gateway_association(
        self, **kwargs: Unpack[DeleteDirectConnectGatewayAssociationRequestRequestTypeDef]
    ) -> DeleteDirectConnectGatewayAssociationResultTypeDef:
        """
        Deletes the association between the specified Direct Connect gateway and
        virtual private gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/delete_direct_connect_gateway_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#delete_direct_connect_gateway_association)
        """

    async def delete_direct_connect_gateway_association_proposal(
        self, **kwargs: Unpack[DeleteDirectConnectGatewayAssociationProposalRequestRequestTypeDef]
    ) -> DeleteDirectConnectGatewayAssociationProposalResultTypeDef:
        """
        Deletes the association proposal request between the specified Direct Connect
        gateway and virtual private gateway or transit gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/delete_direct_connect_gateway_association_proposal.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#delete_direct_connect_gateway_association_proposal)
        """

    async def delete_interconnect(
        self, **kwargs: Unpack[DeleteInterconnectRequestRequestTypeDef]
    ) -> DeleteInterconnectResponseTypeDef:
        """
        Deletes the specified interconnect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/delete_interconnect.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#delete_interconnect)
        """

    async def delete_lag(
        self, **kwargs: Unpack[DeleteLagRequestRequestTypeDef]
    ) -> LagResponseTypeDef:
        """
        Deletes the specified link aggregation group (LAG).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/delete_lag.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#delete_lag)
        """

    async def delete_virtual_interface(
        self, **kwargs: Unpack[DeleteVirtualInterfaceRequestRequestTypeDef]
    ) -> DeleteVirtualInterfaceResponseTypeDef:
        """
        Deletes a virtual interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/delete_virtual_interface.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#delete_virtual_interface)
        """

    async def describe_connection_loa(
        self, **kwargs: Unpack[DescribeConnectionLoaRequestRequestTypeDef]
    ) -> DescribeConnectionLoaResponseTypeDef:
        """
        Deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_connection_loa.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_connection_loa)
        """

    async def describe_connections(
        self, **kwargs: Unpack[DescribeConnectionsRequestRequestTypeDef]
    ) -> ConnectionsTypeDef:
        """
        Displays the specified connection or all connections in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_connections)
        """

    async def describe_connections_on_interconnect(
        self, **kwargs: Unpack[DescribeConnectionsOnInterconnectRequestRequestTypeDef]
    ) -> ConnectionsTypeDef:
        """
        Deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_connections_on_interconnect.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_connections_on_interconnect)
        """

    async def describe_customer_metadata(self) -> DescribeCustomerMetadataResponseTypeDef:
        """
        Get and view a list of customer agreements, along with their signed status and
        whether the customer is an NNIPartner, NNIPartnerV2, or a nonPartner.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_customer_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_customer_metadata)
        """

    async def describe_direct_connect_gateway_association_proposals(
        self,
        **kwargs: Unpack[DescribeDirectConnectGatewayAssociationProposalsRequestRequestTypeDef],
    ) -> DescribeDirectConnectGatewayAssociationProposalsResultTypeDef:
        """
        Describes one or more association proposals for connection between a virtual
        private gateway or transit gateway and a Direct Connect gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_direct_connect_gateway_association_proposals.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_direct_connect_gateway_association_proposals)
        """

    async def describe_direct_connect_gateway_associations(
        self, **kwargs: Unpack[DescribeDirectConnectGatewayAssociationsRequestRequestTypeDef]
    ) -> DescribeDirectConnectGatewayAssociationsResultTypeDef:
        """
        Lists the associations between your Direct Connect gateways and virtual private
        gateways and transit gateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_direct_connect_gateway_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_direct_connect_gateway_associations)
        """

    async def describe_direct_connect_gateway_attachments(
        self, **kwargs: Unpack[DescribeDirectConnectGatewayAttachmentsRequestRequestTypeDef]
    ) -> DescribeDirectConnectGatewayAttachmentsResultTypeDef:
        """
        Lists the attachments between your Direct Connect gateways and virtual
        interfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_direct_connect_gateway_attachments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_direct_connect_gateway_attachments)
        """

    async def describe_direct_connect_gateways(
        self, **kwargs: Unpack[DescribeDirectConnectGatewaysRequestRequestTypeDef]
    ) -> DescribeDirectConnectGatewaysResultTypeDef:
        """
        Lists all your Direct Connect gateways or only the specified Direct Connect
        gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_direct_connect_gateways.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_direct_connect_gateways)
        """

    async def describe_hosted_connections(
        self, **kwargs: Unpack[DescribeHostedConnectionsRequestRequestTypeDef]
    ) -> ConnectionsTypeDef:
        """
        Lists the hosted connections that have been provisioned on the specified
        interconnect or link aggregation group (LAG).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_hosted_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_hosted_connections)
        """

    async def describe_interconnect_loa(
        self, **kwargs: Unpack[DescribeInterconnectLoaRequestRequestTypeDef]
    ) -> DescribeInterconnectLoaResponseTypeDef:
        """
        Deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_interconnect_loa.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_interconnect_loa)
        """

    async def describe_interconnects(
        self, **kwargs: Unpack[DescribeInterconnectsRequestRequestTypeDef]
    ) -> InterconnectsTypeDef:
        """
        Lists the interconnects owned by the Amazon Web Services account or only the
        specified interconnect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_interconnects.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_interconnects)
        """

    async def describe_lags(
        self, **kwargs: Unpack[DescribeLagsRequestRequestTypeDef]
    ) -> LagsTypeDef:
        """
        Describes all your link aggregation groups (LAG) or the specified LAG.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_lags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_lags)
        """

    async def describe_loa(
        self, **kwargs: Unpack[DescribeLoaRequestRequestTypeDef]
    ) -> LoaResponseTypeDef:
        """
        Gets the LOA-CFA for a connection, interconnect, or link aggregation group
        (LAG).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_loa.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_loa)
        """

    async def describe_locations(self) -> LocationsTypeDef:
        """
        Lists the Direct Connect locations in the current Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_locations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_locations)
        """

    async def describe_router_configuration(
        self, **kwargs: Unpack[DescribeRouterConfigurationRequestRequestTypeDef]
    ) -> DescribeRouterConfigurationResponseTypeDef:
        """
        Details about the router.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_router_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_router_configuration)
        """

    async def describe_tags(
        self, **kwargs: Unpack[DescribeTagsRequestRequestTypeDef]
    ) -> DescribeTagsResponseTypeDef:
        """
        Describes the tags associated with the specified Direct Connect resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_tags)
        """

    async def describe_virtual_gateways(self) -> VirtualGatewaysTypeDef:
        """
        Deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_virtual_gateways.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_virtual_gateways)
        """

    async def describe_virtual_interfaces(
        self, **kwargs: Unpack[DescribeVirtualInterfacesRequestRequestTypeDef]
    ) -> VirtualInterfacesTypeDef:
        """
        Displays all virtual interfaces for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/describe_virtual_interfaces.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_virtual_interfaces)
        """

    async def disassociate_connection_from_lag(
        self, **kwargs: Unpack[DisassociateConnectionFromLagRequestRequestTypeDef]
    ) -> ConnectionResponseTypeDef:
        """
        Disassociates a connection from a link aggregation group (LAG).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/disassociate_connection_from_lag.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#disassociate_connection_from_lag)
        """

    async def disassociate_mac_sec_key(
        self, **kwargs: Unpack[DisassociateMacSecKeyRequestRequestTypeDef]
    ) -> DisassociateMacSecKeyResponseTypeDef:
        """
        Removes the association between a MAC Security (MACsec) security key and an
        Direct Connect dedicated connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/disassociate_mac_sec_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#disassociate_mac_sec_key)
        """

    async def list_virtual_interface_test_history(
        self, **kwargs: Unpack[ListVirtualInterfaceTestHistoryRequestRequestTypeDef]
    ) -> ListVirtualInterfaceTestHistoryResponseTypeDef:
        """
        Lists the virtual interface failover test history.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/list_virtual_interface_test_history.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#list_virtual_interface_test_history)
        """

    async def start_bgp_failover_test(
        self, **kwargs: Unpack[StartBgpFailoverTestRequestRequestTypeDef]
    ) -> StartBgpFailoverTestResponseTypeDef:
        """
        Starts the virtual interface failover test that verifies your configuration
        meets your resiliency requirements by placing the BGP peering session in the
        DOWN state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/start_bgp_failover_test.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#start_bgp_failover_test)
        """

    async def stop_bgp_failover_test(
        self, **kwargs: Unpack[StopBgpFailoverTestRequestRequestTypeDef]
    ) -> StopBgpFailoverTestResponseTypeDef:
        """
        Stops the virtual interface failover test.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/stop_bgp_failover_test.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#stop_bgp_failover_test)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified Direct Connect resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified Direct Connect resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#untag_resource)
        """

    async def update_connection(
        self, **kwargs: Unpack[UpdateConnectionRequestRequestTypeDef]
    ) -> ConnectionResponseTypeDef:
        """
        Updates the Direct Connect dedicated connection configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/update_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#update_connection)
        """

    async def update_direct_connect_gateway(
        self, **kwargs: Unpack[UpdateDirectConnectGatewayRequestRequestTypeDef]
    ) -> UpdateDirectConnectGatewayResponseTypeDef:
        """
        Updates the name of a current Direct Connect gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/update_direct_connect_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#update_direct_connect_gateway)
        """

    async def update_direct_connect_gateway_association(
        self, **kwargs: Unpack[UpdateDirectConnectGatewayAssociationRequestRequestTypeDef]
    ) -> UpdateDirectConnectGatewayAssociationResultTypeDef:
        """
        Updates the specified attributes of the Direct Connect gateway association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/update_direct_connect_gateway_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#update_direct_connect_gateway_association)
        """

    async def update_lag(
        self, **kwargs: Unpack[UpdateLagRequestRequestTypeDef]
    ) -> LagResponseTypeDef:
        """
        Updates the attributes of the specified link aggregation group (LAG).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/update_lag.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#update_lag)
        """

    async def update_virtual_interface_attributes(
        self, **kwargs: Unpack[UpdateVirtualInterfaceAttributesRequestRequestTypeDef]
    ) -> VirtualInterfaceResponseTypeDef:
        """
        Updates the specified attributes of the specified virtual private interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/update_virtual_interface_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#update_virtual_interface_attributes)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_direct_connect_gateway_associations"]
    ) -> DescribeDirectConnectGatewayAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_direct_connect_gateway_attachments"]
    ) -> DescribeDirectConnectGatewayAttachmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_direct_connect_gateways"]
    ) -> DescribeDirectConnectGatewaysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#get_paginator)
        """

    async def __aenter__(self) -> "DirectConnectClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/)
        """
