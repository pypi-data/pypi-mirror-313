"""
Main interface for marketplace-reporting service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplace_reporting import (
        Client,
        MarketplaceReportingServiceClient,
    )

    session = get_session()
    async with session.create_client("marketplace-reporting") as client:
        client: MarketplaceReportingServiceClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import MarketplaceReportingServiceClient

Client = MarketplaceReportingServiceClient

__all__ = ("Client", "MarketplaceReportingServiceClient")
