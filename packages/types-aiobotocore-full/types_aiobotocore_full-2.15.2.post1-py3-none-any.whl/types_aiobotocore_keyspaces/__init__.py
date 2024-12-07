"""
Main interface for keyspaces service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_keyspaces import (
        Client,
        KeyspacesClient,
        ListKeyspacesPaginator,
        ListTablesPaginator,
        ListTagsForResourcePaginator,
    )

    session = get_session()
    async with session.create_client("keyspaces") as client:
        client: KeyspacesClient
        ...


    list_keyspaces_paginator: ListKeyspacesPaginator = client.get_paginator("list_keyspaces")
    list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import KeyspacesClient
from .paginator import ListKeyspacesPaginator, ListTablesPaginator, ListTagsForResourcePaginator

Client = KeyspacesClient


__all__ = (
    "Client",
    "KeyspacesClient",
    "ListKeyspacesPaginator",
    "ListTablesPaginator",
    "ListTagsForResourcePaginator",
)
