"""
Main interface for scheduler service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_scheduler import (
        Client,
        EventBridgeSchedulerClient,
        ListScheduleGroupsPaginator,
        ListSchedulesPaginator,
    )

    session = get_session()
    async with session.create_client("scheduler") as client:
        client: EventBridgeSchedulerClient
        ...


    list_schedule_groups_paginator: ListScheduleGroupsPaginator = client.get_paginator("list_schedule_groups")
    list_schedules_paginator: ListSchedulesPaginator = client.get_paginator("list_schedules")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import EventBridgeSchedulerClient
from .paginator import ListScheduleGroupsPaginator, ListSchedulesPaginator

Client = EventBridgeSchedulerClient


__all__ = (
    "Client",
    "EventBridgeSchedulerClient",
    "ListScheduleGroupsPaginator",
    "ListSchedulesPaginator",
)
