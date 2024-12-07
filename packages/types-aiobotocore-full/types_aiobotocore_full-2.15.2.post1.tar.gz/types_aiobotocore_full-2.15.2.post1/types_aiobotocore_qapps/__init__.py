"""
Main interface for qapps service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_qapps import (
        Client,
        ListLibraryItemsPaginator,
        ListQAppsPaginator,
        QAppsClient,
    )

    session = get_session()
    async with session.create_client("qapps") as client:
        client: QAppsClient
        ...


    list_library_items_paginator: ListLibraryItemsPaginator = client.get_paginator("list_library_items")
    list_q_apps_paginator: ListQAppsPaginator = client.get_paginator("list_q_apps")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import QAppsClient
from .paginator import ListLibraryItemsPaginator, ListQAppsPaginator

Client = QAppsClient


__all__ = ("Client", "ListLibraryItemsPaginator", "ListQAppsPaginator", "QAppsClient")
