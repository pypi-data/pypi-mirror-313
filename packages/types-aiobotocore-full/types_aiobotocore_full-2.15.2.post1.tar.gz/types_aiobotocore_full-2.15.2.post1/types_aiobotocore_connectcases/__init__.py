"""
Main interface for connectcases service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_connectcases import (
        Client,
        ConnectCasesClient,
        SearchCasesPaginator,
        SearchRelatedItemsPaginator,
    )

    session = get_session()
    async with session.create_client("connectcases") as client:
        client: ConnectCasesClient
        ...


    search_cases_paginator: SearchCasesPaginator = client.get_paginator("search_cases")
    search_related_items_paginator: SearchRelatedItemsPaginator = client.get_paginator("search_related_items")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ConnectCasesClient
from .paginator import SearchCasesPaginator, SearchRelatedItemsPaginator

Client = ConnectCasesClient


__all__ = ("Client", "ConnectCasesClient", "SearchCasesPaginator", "SearchRelatedItemsPaginator")
