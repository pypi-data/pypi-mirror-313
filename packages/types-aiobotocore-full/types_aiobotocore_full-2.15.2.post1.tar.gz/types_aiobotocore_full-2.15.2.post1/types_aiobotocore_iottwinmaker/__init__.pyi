"""
Main interface for iottwinmaker service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iottwinmaker import (
        Client,
        IoTTwinMakerClient,
    )

    session = get_session()
    async with session.create_client("iottwinmaker") as client:
        client: IoTTwinMakerClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import IoTTwinMakerClient

Client = IoTTwinMakerClient

__all__ = ("Client", "IoTTwinMakerClient")
