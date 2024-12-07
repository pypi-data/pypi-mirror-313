"""
Main interface for iotevents service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iotevents import (
        Client,
        IoTEventsClient,
    )

    session = get_session()
    async with session.create_client("iotevents") as client:
        client: IoTEventsClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import IoTEventsClient

Client = IoTEventsClient

__all__ = ("Client", "IoTEventsClient")
