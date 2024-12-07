"""
Main interface for pinpoint service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pinpoint import (
        Client,
        PinpointClient,
    )

    session = get_session()
    async with session.create_client("pinpoint") as client:
        client: PinpointClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import PinpointClient

Client = PinpointClient


__all__ = ("Client", "PinpointClient")
