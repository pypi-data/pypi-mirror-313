"""
Main interface for marketplace-deployment service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplace_deployment import (
        Client,
        MarketplaceDeploymentServiceClient,
    )

    session = get_session()
    async with session.create_client("marketplace-deployment") as client:
        client: MarketplaceDeploymentServiceClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import MarketplaceDeploymentServiceClient

Client = MarketplaceDeploymentServiceClient


__all__ = ("Client", "MarketplaceDeploymentServiceClient")
