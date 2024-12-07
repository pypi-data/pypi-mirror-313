"""
Main interface for frauddetector service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_frauddetector import (
        Client,
        FraudDetectorClient,
    )

    session = get_session()
    async with session.create_client("frauddetector") as client:
        client: FraudDetectorClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import FraudDetectorClient

Client = FraudDetectorClient


__all__ = ("Client", "FraudDetectorClient")
