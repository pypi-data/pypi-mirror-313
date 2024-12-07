"""
Main interface for lookoutmetrics service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lookoutmetrics import (
        Client,
        LookoutMetricsClient,
    )

    session = get_session()
    async with session.create_client("lookoutmetrics") as client:
        client: LookoutMetricsClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import LookoutMetricsClient

Client = LookoutMetricsClient


__all__ = ("Client", "LookoutMetricsClient")
