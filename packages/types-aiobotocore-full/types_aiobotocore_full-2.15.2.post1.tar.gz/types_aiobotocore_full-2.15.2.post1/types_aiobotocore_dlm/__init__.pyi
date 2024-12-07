"""
Main interface for dlm service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_dlm import (
        Client,
        DLMClient,
    )

    session = get_session()
    async with session.create_client("dlm") as client:
        client: DLMClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import DLMClient

Client = DLMClient

__all__ = ("Client", "DLMClient")
