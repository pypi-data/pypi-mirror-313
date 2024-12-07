"""
Main interface for kendra service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kendra import (
        Client,
        KendraClient,
    )

    session = get_session()
    async with session.create_client("kendra") as client:
        client: KendraClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import KendraClient

Client = KendraClient


__all__ = ("Client", "KendraClient")
