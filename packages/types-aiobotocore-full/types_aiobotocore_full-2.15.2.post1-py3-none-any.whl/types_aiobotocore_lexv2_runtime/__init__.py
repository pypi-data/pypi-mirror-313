"""
Main interface for lexv2-runtime service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lexv2_runtime import (
        Client,
        LexRuntimeV2Client,
    )

    session = get_session()
    async with session.create_client("lexv2-runtime") as client:
        client: LexRuntimeV2Client
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import LexRuntimeV2Client

Client = LexRuntimeV2Client


__all__ = ("Client", "LexRuntimeV2Client")
