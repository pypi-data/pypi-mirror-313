"""
Main interface for pipes service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pipes import (
        Client,
        EventBridgePipesClient,
        ListPipesPaginator,
    )

    session = get_session()
    async with session.create_client("pipes") as client:
        client: EventBridgePipesClient
        ...


    list_pipes_paginator: ListPipesPaginator = client.get_paginator("list_pipes")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import EventBridgePipesClient
from .paginator import ListPipesPaginator

Client = EventBridgePipesClient

__all__ = ("Client", "EventBridgePipesClient", "ListPipesPaginator")
