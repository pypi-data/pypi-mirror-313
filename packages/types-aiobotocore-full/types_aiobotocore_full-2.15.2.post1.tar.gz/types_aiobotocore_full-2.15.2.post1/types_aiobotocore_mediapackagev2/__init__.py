"""
Main interface for mediapackagev2 service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mediapackagev2 import (
        Client,
        ListChannelGroupsPaginator,
        ListChannelsPaginator,
        ListOriginEndpointsPaginator,
        Mediapackagev2Client,
    )

    session = get_session()
    async with session.create_client("mediapackagev2") as client:
        client: Mediapackagev2Client
        ...


    list_channel_groups_paginator: ListChannelGroupsPaginator = client.get_paginator("list_channel_groups")
    list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
    list_origin_endpoints_paginator: ListOriginEndpointsPaginator = client.get_paginator("list_origin_endpoints")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import Mediapackagev2Client
from .paginator import (
    ListChannelGroupsPaginator,
    ListChannelsPaginator,
    ListOriginEndpointsPaginator,
)

Client = Mediapackagev2Client


__all__ = (
    "Client",
    "ListChannelGroupsPaginator",
    "ListChannelsPaginator",
    "ListOriginEndpointsPaginator",
    "Mediapackagev2Client",
)
