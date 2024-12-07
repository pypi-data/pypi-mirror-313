"""
Main interface for iotwireless service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iotwireless import (
        Client,
        IoTWirelessClient,
    )

    session = get_session()
    async with session.create_client("iotwireless") as client:
        client: IoTWirelessClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import IoTWirelessClient

Client = IoTWirelessClient

__all__ = ("Client", "IoTWirelessClient")
