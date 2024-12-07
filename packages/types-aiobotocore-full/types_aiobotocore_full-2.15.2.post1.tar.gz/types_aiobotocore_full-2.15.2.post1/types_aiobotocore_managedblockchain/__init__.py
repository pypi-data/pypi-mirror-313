"""
Main interface for managedblockchain service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_managedblockchain import (
        Client,
        ListAccessorsPaginator,
        ManagedBlockchainClient,
    )

    session = get_session()
    async with session.create_client("managedblockchain") as client:
        client: ManagedBlockchainClient
        ...


    list_accessors_paginator: ListAccessorsPaginator = client.get_paginator("list_accessors")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ManagedBlockchainClient
from .paginator import ListAccessorsPaginator

Client = ManagedBlockchainClient


__all__ = ("Client", "ListAccessorsPaginator", "ManagedBlockchainClient")
