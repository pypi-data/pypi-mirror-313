"""
Main interface for apigatewaymanagementapi service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_apigatewaymanagementapi import (
        ApiGatewayManagementApiClient,
        Client,
    )

    session = get_session()
    async with session.create_client("apigatewaymanagementapi") as client:
        client: ApiGatewayManagementApiClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ApiGatewayManagementApiClient

Client = ApiGatewayManagementApiClient

__all__ = ("ApiGatewayManagementApiClient", "Client")
