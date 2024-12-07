"""
Type annotations for privatenetworks service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_privatenetworks.client import Private5GClient
    from types_aiobotocore_privatenetworks.paginator import (
        ListDeviceIdentifiersPaginator,
        ListNetworkResourcesPaginator,
        ListNetworkSitesPaginator,
        ListNetworksPaginator,
        ListOrdersPaginator,
    )

    session = get_session()
    with session.create_client("privatenetworks") as client:
        client: Private5GClient

        list_device_identifiers_paginator: ListDeviceIdentifiersPaginator = client.get_paginator("list_device_identifiers")
        list_network_resources_paginator: ListNetworkResourcesPaginator = client.get_paginator("list_network_resources")
        list_network_sites_paginator: ListNetworkSitesPaginator = client.get_paginator("list_network_sites")
        list_networks_paginator: ListNetworksPaginator = client.get_paginator("list_networks")
        list_orders_paginator: ListOrdersPaginator = client.get_paginator("list_orders")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListDeviceIdentifiersRequestListDeviceIdentifiersPaginateTypeDef,
    ListDeviceIdentifiersResponseTypeDef,
    ListNetworkResourcesRequestListNetworkResourcesPaginateTypeDef,
    ListNetworkResourcesResponseTypeDef,
    ListNetworkSitesRequestListNetworkSitesPaginateTypeDef,
    ListNetworkSitesResponseTypeDef,
    ListNetworksRequestListNetworksPaginateTypeDef,
    ListNetworksResponseTypeDef,
    ListOrdersRequestListOrdersPaginateTypeDef,
    ListOrdersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListDeviceIdentifiersPaginator",
    "ListNetworkResourcesPaginator",
    "ListNetworkSitesPaginator",
    "ListNetworksPaginator",
    "ListOrdersPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDeviceIdentifiersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListDeviceIdentifiers.html#Private5G.Paginator.ListDeviceIdentifiers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listdeviceidentifierspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDeviceIdentifiersRequestListDeviceIdentifiersPaginateTypeDef]
    ) -> AsyncIterator[ListDeviceIdentifiersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListDeviceIdentifiers.html#Private5G.Paginator.ListDeviceIdentifiers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listdeviceidentifierspaginator)
        """


class ListNetworkResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworkResources.html#Private5G.Paginator.ListNetworkResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listnetworkresourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListNetworkResourcesRequestListNetworkResourcesPaginateTypeDef]
    ) -> AsyncIterator[ListNetworkResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworkResources.html#Private5G.Paginator.ListNetworkResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listnetworkresourcespaginator)
        """


class ListNetworkSitesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworkSites.html#Private5G.Paginator.ListNetworkSites)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listnetworksitespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListNetworkSitesRequestListNetworkSitesPaginateTypeDef]
    ) -> AsyncIterator[ListNetworkSitesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworkSites.html#Private5G.Paginator.ListNetworkSites.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listnetworksitespaginator)
        """


class ListNetworksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworks.html#Private5G.Paginator.ListNetworks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listnetworkspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListNetworksRequestListNetworksPaginateTypeDef]
    ) -> AsyncIterator[ListNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworks.html#Private5G.Paginator.ListNetworks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listnetworkspaginator)
        """


class ListOrdersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListOrders.html#Private5G.Paginator.ListOrders)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listorderspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOrdersRequestListOrdersPaginateTypeDef]
    ) -> AsyncIterator[ListOrdersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListOrders.html#Private5G.Paginator.ListOrders.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listorderspaginator)
        """
