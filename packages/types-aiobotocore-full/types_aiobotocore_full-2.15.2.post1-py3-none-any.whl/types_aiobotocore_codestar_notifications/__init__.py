"""
Main interface for codestar-notifications service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codestar_notifications import (
        Client,
        CodeStarNotificationsClient,
        ListEventTypesPaginator,
        ListNotificationRulesPaginator,
        ListTargetsPaginator,
    )

    session = get_session()
    async with session.create_client("codestar-notifications") as client:
        client: CodeStarNotificationsClient
        ...


    list_event_types_paginator: ListEventTypesPaginator = client.get_paginator("list_event_types")
    list_notification_rules_paginator: ListNotificationRulesPaginator = client.get_paginator("list_notification_rules")
    list_targets_paginator: ListTargetsPaginator = client.get_paginator("list_targets")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CodeStarNotificationsClient
from .paginator import ListEventTypesPaginator, ListNotificationRulesPaginator, ListTargetsPaginator

Client = CodeStarNotificationsClient


__all__ = (
    "Client",
    "CodeStarNotificationsClient",
    "ListEventTypesPaginator",
    "ListNotificationRulesPaginator",
    "ListTargetsPaginator",
)
