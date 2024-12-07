"""
Main interface for workspaces-web service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_workspaces_web import (
        Client,
        ListSessionsPaginator,
        WorkSpacesWebClient,
    )

    session = get_session()
    async with session.create_client("workspaces-web") as client:
        client: WorkSpacesWebClient
        ...


    list_sessions_paginator: ListSessionsPaginator = client.get_paginator("list_sessions")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import WorkSpacesWebClient
from .paginator import ListSessionsPaginator

Client = WorkSpacesWebClient


__all__ = ("Client", "ListSessionsPaginator", "WorkSpacesWebClient")
