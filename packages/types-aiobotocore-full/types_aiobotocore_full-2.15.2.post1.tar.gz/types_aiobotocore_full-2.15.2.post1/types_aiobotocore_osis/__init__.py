"""
Main interface for osis service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_osis import (
        Client,
        OpenSearchIngestionClient,
    )

    session = get_session()
    async with session.create_client("osis") as client:
        client: OpenSearchIngestionClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import OpenSearchIngestionClient

Client = OpenSearchIngestionClient


__all__ = ("Client", "OpenSearchIngestionClient")
