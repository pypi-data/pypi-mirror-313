"""
Main interface for chime-sdk-messaging service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chime_sdk_messaging import (
        ChimeSDKMessagingClient,
        Client,
    )

    session = get_session()
    async with session.create_client("chime-sdk-messaging") as client:
        client: ChimeSDKMessagingClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ChimeSDKMessagingClient

Client = ChimeSDKMessagingClient

__all__ = ("ChimeSDKMessagingClient", "Client")
