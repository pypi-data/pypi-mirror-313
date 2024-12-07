"""
Main interface for pcs service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pcs import (
        Client,
        ListClustersPaginator,
        ListComputeNodeGroupsPaginator,
        ListQueuesPaginator,
        ParallelComputingServiceClient,
    )

    session = get_session()
    async with session.create_client("pcs") as client:
        client: ParallelComputingServiceClient
        ...


    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_compute_node_groups_paginator: ListComputeNodeGroupsPaginator = client.get_paginator("list_compute_node_groups")
    list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ParallelComputingServiceClient
from .paginator import ListClustersPaginator, ListComputeNodeGroupsPaginator, ListQueuesPaginator

Client = ParallelComputingServiceClient


__all__ = (
    "Client",
    "ListClustersPaginator",
    "ListComputeNodeGroupsPaginator",
    "ListQueuesPaginator",
    "ParallelComputingServiceClient",
)
