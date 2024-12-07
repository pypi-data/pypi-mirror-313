"""
Main interface for mwaa service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mwaa import (
        Client,
        ListEnvironmentsPaginator,
        MWAAClient,
    )

    session = get_session()
    async with session.create_client("mwaa") as client:
        client: MWAAClient
        ...


    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import MWAAClient
from .paginator import ListEnvironmentsPaginator

Client = MWAAClient


__all__ = ("Client", "ListEnvironmentsPaginator", "MWAAClient")
