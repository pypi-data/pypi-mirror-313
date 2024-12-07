"""
Main interface for oam service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_oam import (
        Client,
        CloudWatchObservabilityAccessManagerClient,
        ListAttachedLinksPaginator,
        ListLinksPaginator,
        ListSinksPaginator,
    )

    session = get_session()
    async with session.create_client("oam") as client:
        client: CloudWatchObservabilityAccessManagerClient
        ...


    list_attached_links_paginator: ListAttachedLinksPaginator = client.get_paginator("list_attached_links")
    list_links_paginator: ListLinksPaginator = client.get_paginator("list_links")
    list_sinks_paginator: ListSinksPaginator = client.get_paginator("list_sinks")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CloudWatchObservabilityAccessManagerClient
from .paginator import ListAttachedLinksPaginator, ListLinksPaginator, ListSinksPaginator

Client = CloudWatchObservabilityAccessManagerClient


__all__ = (
    "Client",
    "CloudWatchObservabilityAccessManagerClient",
    "ListAttachedLinksPaginator",
    "ListLinksPaginator",
    "ListSinksPaginator",
)
