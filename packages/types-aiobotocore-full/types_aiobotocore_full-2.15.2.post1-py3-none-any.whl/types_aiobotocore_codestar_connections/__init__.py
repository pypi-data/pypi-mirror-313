"""
Main interface for codestar-connections service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codestar_connections import (
        Client,
        CodeStarconnectionsClient,
    )

    session = get_session()
    async with session.create_client("codestar-connections") as client:
        client: CodeStarconnectionsClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CodeStarconnectionsClient

Client = CodeStarconnectionsClient


__all__ = ("Client", "CodeStarconnectionsClient")
