"""
Main interface for marketplacecommerceanalytics service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplacecommerceanalytics import (
        Client,
        MarketplaceCommerceAnalyticsClient,
    )

    session = get_session()
    async with session.create_client("marketplacecommerceanalytics") as client:
        client: MarketplaceCommerceAnalyticsClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import MarketplaceCommerceAnalyticsClient

Client = MarketplaceCommerceAnalyticsClient


__all__ = ("Client", "MarketplaceCommerceAnalyticsClient")
