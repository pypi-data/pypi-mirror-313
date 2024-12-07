"""
Main interface for codeconnections service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codeconnections import (
        Client,
        CodeConnectionsClient,
    )

    session = get_session()
    async with session.create_client("codeconnections") as client:
        client: CodeConnectionsClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CodeConnectionsClient

Client = CodeConnectionsClient


__all__ = ("Client", "CodeConnectionsClient")
