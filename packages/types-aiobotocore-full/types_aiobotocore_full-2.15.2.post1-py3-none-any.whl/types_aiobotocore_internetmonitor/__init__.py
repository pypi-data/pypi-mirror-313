"""
Main interface for internetmonitor service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_internetmonitor import (
        Client,
        CloudWatchInternetMonitorClient,
        ListHealthEventsPaginator,
        ListInternetEventsPaginator,
        ListMonitorsPaginator,
    )

    session = get_session()
    async with session.create_client("internetmonitor") as client:
        client: CloudWatchInternetMonitorClient
        ...


    list_health_events_paginator: ListHealthEventsPaginator = client.get_paginator("list_health_events")
    list_internet_events_paginator: ListInternetEventsPaginator = client.get_paginator("list_internet_events")
    list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CloudWatchInternetMonitorClient
from .paginator import ListHealthEventsPaginator, ListInternetEventsPaginator, ListMonitorsPaginator

Client = CloudWatchInternetMonitorClient


__all__ = (
    "Client",
    "CloudWatchInternetMonitorClient",
    "ListHealthEventsPaginator",
    "ListInternetEventsPaginator",
    "ListMonitorsPaginator",
)
