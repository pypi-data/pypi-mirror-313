"""
Main interface for rbin service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_rbin import (
        Client,
        ListRulesPaginator,
        RecycleBinClient,
    )

    session = get_session()
    async with session.create_client("rbin") as client:
        client: RecycleBinClient
        ...


    list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import RecycleBinClient
from .paginator import ListRulesPaginator

Client = RecycleBinClient

__all__ = ("Client", "ListRulesPaginator", "RecycleBinClient")
