"""
Main interface for kendra-ranking service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kendra_ranking import (
        Client,
        KendraRankingClient,
    )

    session = get_session()
    async with session.create_client("kendra-ranking") as client:
        client: KendraRankingClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import KendraRankingClient

Client = KendraRankingClient


__all__ = ("Client", "KendraRankingClient")
