"""
Main interface for timestream-query service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_timestream_query import (
        Client,
        ListScheduledQueriesPaginator,
        ListTagsForResourcePaginator,
        QueryPaginator,
        TimestreamQueryClient,
    )

    session = get_session()
    async with session.create_client("timestream-query") as client:
        client: TimestreamQueryClient
        ...


    list_scheduled_queries_paginator: ListScheduledQueriesPaginator = client.get_paginator("list_scheduled_queries")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    query_paginator: QueryPaginator = client.get_paginator("query")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import TimestreamQueryClient
from .paginator import ListScheduledQueriesPaginator, ListTagsForResourcePaginator, QueryPaginator

Client = TimestreamQueryClient


__all__ = (
    "Client",
    "ListScheduledQueriesPaginator",
    "ListTagsForResourcePaginator",
    "QueryPaginator",
    "TimestreamQueryClient",
)
