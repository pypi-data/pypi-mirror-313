"""
Type annotations for mediapackagev2 service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackagev2/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediapackagev2.client import Mediapackagev2Client
    from types_aiobotocore_mediapackagev2.paginator import (
        ListChannelGroupsPaginator,
        ListChannelsPaginator,
        ListOriginEndpointsPaginator,
    )

    session = get_session()
    with session.create_client("mediapackagev2") as client:
        client: Mediapackagev2Client

        list_channel_groups_paginator: ListChannelGroupsPaginator = client.get_paginator("list_channel_groups")
        list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
        list_origin_endpoints_paginator: ListOriginEndpointsPaginator = client.get_paginator("list_origin_endpoints")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListChannelGroupsRequestListChannelGroupsPaginateTypeDef,
    ListChannelGroupsResponseTypeDef,
    ListChannelsRequestListChannelsPaginateTypeDef,
    ListChannelsResponseTypeDef,
    ListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef,
    ListOriginEndpointsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListChannelGroupsPaginator", "ListChannelsPaginator", "ListOriginEndpointsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListChannelGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2/paginator/ListChannelGroups.html#Mediapackagev2.Paginator.ListChannelGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackagev2/paginators/#listchannelgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListChannelGroupsRequestListChannelGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListChannelGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2/paginator/ListChannelGroups.html#Mediapackagev2.Paginator.ListChannelGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackagev2/paginators/#listchannelgroupspaginator)
        """


class ListChannelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2/paginator/ListChannels.html#Mediapackagev2.Paginator.ListChannels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackagev2/paginators/#listchannelspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListChannelsRequestListChannelsPaginateTypeDef]
    ) -> AsyncIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2/paginator/ListChannels.html#Mediapackagev2.Paginator.ListChannels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackagev2/paginators/#listchannelspaginator)
        """


class ListOriginEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2/paginator/ListOriginEndpoints.html#Mediapackagev2.Paginator.ListOriginEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackagev2/paginators/#listoriginendpointspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef]
    ) -> AsyncIterator[ListOriginEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2/paginator/ListOriginEndpoints.html#Mediapackagev2.Paginator.ListOriginEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackagev2/paginators/#listoriginendpointspaginator)
        """
