"""
Main interface for lex-runtime service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lex_runtime import (
        Client,
        LexRuntimeServiceClient,
    )

    session = get_session()
    async with session.create_client("lex-runtime") as client:
        client: LexRuntimeServiceClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import LexRuntimeServiceClient

Client = LexRuntimeServiceClient

__all__ = ("Client", "LexRuntimeServiceClient")
