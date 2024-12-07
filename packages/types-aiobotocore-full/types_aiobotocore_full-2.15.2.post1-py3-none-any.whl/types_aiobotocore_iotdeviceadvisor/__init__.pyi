"""
Main interface for iotdeviceadvisor service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iotdeviceadvisor import (
        Client,
        IoTDeviceAdvisorClient,
    )

    session = get_session()
    async with session.create_client("iotdeviceadvisor") as client:
        client: IoTDeviceAdvisorClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import IoTDeviceAdvisorClient

Client = IoTDeviceAdvisorClient

__all__ = ("Client", "IoTDeviceAdvisorClient")
