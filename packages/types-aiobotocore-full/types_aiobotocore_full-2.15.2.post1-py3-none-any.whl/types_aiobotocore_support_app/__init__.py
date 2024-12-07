"""
Main interface for support-app service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_support_app import (
        Client,
        SupportAppClient,
    )

    session = get_session()
    async with session.create_client("support-app") as client:
        client: SupportAppClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SupportAppClient

Client = SupportAppClient


__all__ = ("Client", "SupportAppClient")
