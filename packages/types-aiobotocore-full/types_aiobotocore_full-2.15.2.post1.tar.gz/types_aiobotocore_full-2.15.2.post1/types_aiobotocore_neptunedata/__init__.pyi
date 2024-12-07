"""
Main interface for neptunedata service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_neptunedata import (
        Client,
        NeptuneDataClient,
    )

    session = get_session()
    async with session.create_client("neptunedata") as client:
        client: NeptuneDataClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import NeptuneDataClient

Client = NeptuneDataClient

__all__ = ("Client", "NeptuneDataClient")
