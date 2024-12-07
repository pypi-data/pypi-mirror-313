"""
Main interface for repostspace service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_repostspace import (
        Client,
        ListSpacesPaginator,
        RePostPrivateClient,
    )

    session = get_session()
    async with session.create_client("repostspace") as client:
        client: RePostPrivateClient
        ...


    list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import RePostPrivateClient
from .paginator import ListSpacesPaginator

Client = RePostPrivateClient

__all__ = ("Client", "ListSpacesPaginator", "RePostPrivateClient")
