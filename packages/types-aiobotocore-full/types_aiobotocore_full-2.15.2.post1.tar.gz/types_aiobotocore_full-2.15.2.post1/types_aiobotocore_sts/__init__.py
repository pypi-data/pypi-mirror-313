"""
Main interface for sts service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sts import (
        Client,
        STSClient,
    )

    session = get_session()
    async with session.create_client("sts") as client:
        client: STSClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import STSClient

Client = STSClient


__all__ = ("Client", "STSClient")
