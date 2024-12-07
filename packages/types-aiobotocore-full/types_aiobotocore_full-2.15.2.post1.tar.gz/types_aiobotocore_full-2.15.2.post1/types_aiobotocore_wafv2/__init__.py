"""
Main interface for wafv2 service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_wafv2 import (
        Client,
        WAFV2Client,
    )

    session = get_session()
    async with session.create_client("wafv2") as client:
        client: WAFV2Client
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import WAFV2Client

Client = WAFV2Client


__all__ = ("Client", "WAFV2Client")
