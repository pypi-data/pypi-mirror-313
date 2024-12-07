"""
Main interface for customer-profiles service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_customer_profiles import (
        Client,
        CustomerProfilesClient,
        ListEventStreamsPaginator,
    )

    session = get_session()
    async with session.create_client("customer-profiles") as client:
        client: CustomerProfilesClient
        ...


    list_event_streams_paginator: ListEventStreamsPaginator = client.get_paginator("list_event_streams")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CustomerProfilesClient
from .paginator import ListEventStreamsPaginator

Client = CustomerProfilesClient

__all__ = ("Client", "CustomerProfilesClient", "ListEventStreamsPaginator")
