"""
Main interface for marketplace-entitlement service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplace_entitlement import (
        Client,
        GetEntitlementsPaginator,
        MarketplaceEntitlementServiceClient,
    )

    session = get_session()
    async with session.create_client("marketplace-entitlement") as client:
        client: MarketplaceEntitlementServiceClient
        ...


    get_entitlements_paginator: GetEntitlementsPaginator = client.get_paginator("get_entitlements")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import MarketplaceEntitlementServiceClient
from .paginator import GetEntitlementsPaginator

Client = MarketplaceEntitlementServiceClient


__all__ = ("Client", "GetEntitlementsPaginator", "MarketplaceEntitlementServiceClient")
