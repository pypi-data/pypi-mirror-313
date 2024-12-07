"""
Main interface for meteringmarketplace service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_meteringmarketplace import (
        Client,
        MarketplaceMeteringClient,
    )

    session = get_session()
    async with session.create_client("meteringmarketplace") as client:
        client: MarketplaceMeteringClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import MarketplaceMeteringClient

Client = MarketplaceMeteringClient


__all__ = ("Client", "MarketplaceMeteringClient")
