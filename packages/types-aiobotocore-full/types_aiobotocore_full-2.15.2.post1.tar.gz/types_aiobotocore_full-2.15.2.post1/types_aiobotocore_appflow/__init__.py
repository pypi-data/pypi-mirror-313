"""
Main interface for appflow service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_appflow import (
        AppflowClient,
        Client,
    )

    session = get_session()
    async with session.create_client("appflow") as client:
        client: AppflowClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import AppflowClient

Client = AppflowClient


__all__ = ("AppflowClient", "Client")
