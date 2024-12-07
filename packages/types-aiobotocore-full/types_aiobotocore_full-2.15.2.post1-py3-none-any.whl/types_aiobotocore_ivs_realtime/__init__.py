"""
Main interface for ivs-realtime service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ivs_realtime import (
        Client,
        IvsrealtimeClient,
        ListIngestConfigurationsPaginator,
        ListPublicKeysPaginator,
    )

    session = get_session()
    async with session.create_client("ivs-realtime") as client:
        client: IvsrealtimeClient
        ...


    list_ingest_configurations_paginator: ListIngestConfigurationsPaginator = client.get_paginator("list_ingest_configurations")
    list_public_keys_paginator: ListPublicKeysPaginator = client.get_paginator("list_public_keys")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import IvsrealtimeClient
from .paginator import ListIngestConfigurationsPaginator, ListPublicKeysPaginator

Client = IvsrealtimeClient


__all__ = (
    "Client",
    "IvsrealtimeClient",
    "ListIngestConfigurationsPaginator",
    "ListPublicKeysPaginator",
)
