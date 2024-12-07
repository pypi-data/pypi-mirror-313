"""
Main interface for mediastore service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mediastore import (
        Client,
        ListContainersPaginator,
        MediaStoreClient,
    )

    session = get_session()
    async with session.create_client("mediastore") as client:
        client: MediaStoreClient
        ...


    list_containers_paginator: ListContainersPaginator = client.get_paginator("list_containers")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import MediaStoreClient
from .paginator import ListContainersPaginator

Client = MediaStoreClient

__all__ = ("Client", "ListContainersPaginator", "MediaStoreClient")
