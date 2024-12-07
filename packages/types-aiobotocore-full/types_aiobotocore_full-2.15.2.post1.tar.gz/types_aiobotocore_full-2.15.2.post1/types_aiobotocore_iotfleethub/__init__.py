"""
Main interface for iotfleethub service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iotfleethub import (
        Client,
        IoTFleetHubClient,
        ListApplicationsPaginator,
    )

    session = get_session()
    async with session.create_client("iotfleethub") as client:
        client: IoTFleetHubClient
        ...


    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import IoTFleetHubClient
from .paginator import ListApplicationsPaginator

Client = IoTFleetHubClient


__all__ = ("Client", "IoTFleetHubClient", "ListApplicationsPaginator")
