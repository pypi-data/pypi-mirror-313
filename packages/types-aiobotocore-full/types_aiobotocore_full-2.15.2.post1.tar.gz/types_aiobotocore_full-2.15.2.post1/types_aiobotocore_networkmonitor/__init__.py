"""
Main interface for networkmonitor service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_networkmonitor import (
        Client,
        CloudWatchNetworkMonitorClient,
        ListMonitorsPaginator,
    )

    session = get_session()
    async with session.create_client("networkmonitor") as client:
        client: CloudWatchNetworkMonitorClient
        ...


    list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CloudWatchNetworkMonitorClient
from .paginator import ListMonitorsPaginator

Client = CloudWatchNetworkMonitorClient


__all__ = ("Client", "CloudWatchNetworkMonitorClient", "ListMonitorsPaginator")
