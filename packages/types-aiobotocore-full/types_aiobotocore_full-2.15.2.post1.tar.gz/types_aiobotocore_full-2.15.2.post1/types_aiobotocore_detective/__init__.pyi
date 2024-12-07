"""
Main interface for detective service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_detective import (
        Client,
        DetectiveClient,
    )

    session = get_session()
    async with session.create_client("detective") as client:
        client: DetectiveClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import DetectiveClient

Client = DetectiveClient

__all__ = ("Client", "DetectiveClient")
