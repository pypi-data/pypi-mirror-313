"""
Main interface for iot-jobs-data service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iot_jobs_data import (
        Client,
        IoTJobsDataPlaneClient,
    )

    session = get_session()
    async with session.create_client("iot-jobs-data") as client:
        client: IoTJobsDataPlaneClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import IoTJobsDataPlaneClient

Client = IoTJobsDataPlaneClient


__all__ = ("Client", "IoTJobsDataPlaneClient")
