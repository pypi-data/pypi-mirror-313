"""
Main interface for resource-explorer-2 service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_resource_explorer_2 import (
        Client,
        ListIndexesForMembersPaginator,
        ListIndexesPaginator,
        ListResourcesPaginator,
        ListSupportedResourceTypesPaginator,
        ListViewsPaginator,
        ResourceExplorerClient,
        SearchPaginator,
    )

    session = get_session()
    async with session.create_client("resource-explorer-2") as client:
        client: ResourceExplorerClient
        ...


    list_indexes_for_members_paginator: ListIndexesForMembersPaginator = client.get_paginator("list_indexes_for_members")
    list_indexes_paginator: ListIndexesPaginator = client.get_paginator("list_indexes")
    list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
    list_supported_resource_types_paginator: ListSupportedResourceTypesPaginator = client.get_paginator("list_supported_resource_types")
    list_views_paginator: ListViewsPaginator = client.get_paginator("list_views")
    search_paginator: SearchPaginator = client.get_paginator("search")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ResourceExplorerClient
from .paginator import (
    ListIndexesForMembersPaginator,
    ListIndexesPaginator,
    ListResourcesPaginator,
    ListSupportedResourceTypesPaginator,
    ListViewsPaginator,
    SearchPaginator,
)

Client = ResourceExplorerClient

__all__ = (
    "Client",
    "ListIndexesForMembersPaginator",
    "ListIndexesPaginator",
    "ListResourcesPaginator",
    "ListSupportedResourceTypesPaginator",
    "ListViewsPaginator",
    "ResourceExplorerClient",
    "SearchPaginator",
)
