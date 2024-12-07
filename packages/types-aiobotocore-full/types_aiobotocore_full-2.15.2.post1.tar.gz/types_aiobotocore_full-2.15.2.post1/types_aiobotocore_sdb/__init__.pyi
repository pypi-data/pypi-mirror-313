"""
Main interface for sdb service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sdb import (
        Client,
        ListDomainsPaginator,
        SelectPaginator,
        SimpleDBClient,
    )

    session = get_session()
    async with session.create_client("sdb") as client:
        client: SimpleDBClient
        ...


    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    select_paginator: SelectPaginator = client.get_paginator("select")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SimpleDBClient
from .paginator import ListDomainsPaginator, SelectPaginator

Client = SimpleDBClient

__all__ = ("Client", "ListDomainsPaginator", "SelectPaginator", "SimpleDBClient")
