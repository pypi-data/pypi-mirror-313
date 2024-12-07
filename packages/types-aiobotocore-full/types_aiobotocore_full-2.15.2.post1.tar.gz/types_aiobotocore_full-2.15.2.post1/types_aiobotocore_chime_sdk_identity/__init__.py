"""
Main interface for chime-sdk-identity service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chime_sdk_identity import (
        ChimeSDKIdentityClient,
        Client,
    )

    session = get_session()
    async with session.create_client("chime-sdk-identity") as client:
        client: ChimeSDKIdentityClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ChimeSDKIdentityClient

Client = ChimeSDKIdentityClient


__all__ = ("ChimeSDKIdentityClient", "Client")
