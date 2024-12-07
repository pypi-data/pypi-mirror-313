"""
Main interface for forecastquery service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_forecastquery import (
        Client,
        ForecastQueryServiceClient,
    )

    session = get_session()
    async with session.create_client("forecastquery") as client:
        client: ForecastQueryServiceClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ForecastQueryServiceClient

Client = ForecastQueryServiceClient


__all__ = ("Client", "ForecastQueryServiceClient")
