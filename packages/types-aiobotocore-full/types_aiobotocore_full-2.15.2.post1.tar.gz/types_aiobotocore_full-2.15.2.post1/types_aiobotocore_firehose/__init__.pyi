"""
Main interface for firehose service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_firehose import (
        Client,
        FirehoseClient,
    )

    session = get_session()
    async with session.create_client("firehose") as client:
        client: FirehoseClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import FirehoseClient

Client = FirehoseClient

__all__ = ("Client", "FirehoseClient")
