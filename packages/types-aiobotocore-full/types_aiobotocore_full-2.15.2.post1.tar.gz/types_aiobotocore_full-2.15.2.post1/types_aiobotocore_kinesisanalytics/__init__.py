"""
Main interface for kinesisanalytics service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kinesisanalytics import (
        Client,
        KinesisAnalyticsClient,
    )

    session = get_session()
    async with session.create_client("kinesisanalytics") as client:
        client: KinesisAnalyticsClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import KinesisAnalyticsClient

Client = KinesisAnalyticsClient


__all__ = ("Client", "KinesisAnalyticsClient")
