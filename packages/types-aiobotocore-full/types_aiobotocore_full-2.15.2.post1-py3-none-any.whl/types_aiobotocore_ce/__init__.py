"""
Main interface for ce service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ce import (
        Client,
        CostExplorerClient,
    )

    session = get_session()
    async with session.create_client("ce") as client:
        client: CostExplorerClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CostExplorerClient

Client = CostExplorerClient


__all__ = ("Client", "CostExplorerClient")
