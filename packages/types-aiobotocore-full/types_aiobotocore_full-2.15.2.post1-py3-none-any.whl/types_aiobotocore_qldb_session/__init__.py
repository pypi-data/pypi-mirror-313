"""
Main interface for qldb-session service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_qldb_session import (
        Client,
        QLDBSessionClient,
    )

    session = get_session()
    async with session.create_client("qldb-session") as client:
        client: QLDBSessionClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import QLDBSessionClient

Client = QLDBSessionClient


__all__ = ("Client", "QLDBSessionClient")
