"""
Main interface for sesv2 service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sesv2 import (
        Client,
        SESV2Client,
    )

    session = get_session()
    async with session.create_client("sesv2") as client:
        client: SESV2Client
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SESV2Client

Client = SESV2Client

__all__ = ("Client", "SESV2Client")
