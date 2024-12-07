"""
Main interface for chime-sdk-meetings service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chime_sdk_meetings import (
        ChimeSDKMeetingsClient,
        Client,
    )

    session = get_session()
    async with session.create_client("chime-sdk-meetings") as client:
        client: ChimeSDKMeetingsClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ChimeSDKMeetingsClient

Client = ChimeSDKMeetingsClient

__all__ = ("ChimeSDKMeetingsClient", "Client")
