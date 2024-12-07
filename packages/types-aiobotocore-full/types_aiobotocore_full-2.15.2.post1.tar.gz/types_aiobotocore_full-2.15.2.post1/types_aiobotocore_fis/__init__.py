"""
Main interface for fis service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_fis import (
        Client,
        FISClient,
    )

    session = get_session()
    async with session.create_client("fis") as client:
        client: FISClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import FISClient

Client = FISClient


__all__ = ("Client", "FISClient")
