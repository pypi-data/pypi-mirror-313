"""
Main interface for transcribe service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_transcribe import (
        Client,
        TranscribeServiceClient,
    )

    session = get_session()
    async with session.create_client("transcribe") as client:
        client: TranscribeServiceClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import TranscribeServiceClient

Client = TranscribeServiceClient


__all__ = ("Client", "TranscribeServiceClient")
