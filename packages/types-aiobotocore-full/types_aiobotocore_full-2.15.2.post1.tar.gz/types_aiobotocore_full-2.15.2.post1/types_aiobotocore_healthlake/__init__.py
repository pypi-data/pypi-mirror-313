"""
Main interface for healthlake service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_healthlake import (
        Client,
        HealthLakeClient,
    )

    session = get_session()
    async with session.create_client("healthlake") as client:
        client: HealthLakeClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import HealthLakeClient

Client = HealthLakeClient


__all__ = ("Client", "HealthLakeClient")
