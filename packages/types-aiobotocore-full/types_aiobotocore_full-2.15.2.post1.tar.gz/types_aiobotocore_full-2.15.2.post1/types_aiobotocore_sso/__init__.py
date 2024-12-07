"""
Main interface for sso service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sso import (
        Client,
        ListAccountRolesPaginator,
        ListAccountsPaginator,
        SSOClient,
    )

    session = get_session()
    async with session.create_client("sso") as client:
        client: SSOClient
        ...


    list_account_roles_paginator: ListAccountRolesPaginator = client.get_paginator("list_account_roles")
    list_accounts_paginator: ListAccountsPaginator = client.get_paginator("list_accounts")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SSOClient
from .paginator import ListAccountRolesPaginator, ListAccountsPaginator

Client = SSOClient


__all__ = ("Client", "ListAccountRolesPaginator", "ListAccountsPaginator", "SSOClient")
