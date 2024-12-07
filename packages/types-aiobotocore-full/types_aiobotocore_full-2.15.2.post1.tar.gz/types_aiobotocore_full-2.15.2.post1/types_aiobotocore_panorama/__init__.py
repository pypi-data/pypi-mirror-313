"""
Main interface for panorama service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_panorama import (
        Client,
        PanoramaClient,
    )

    session = get_session()
    async with session.create_client("panorama") as client:
        client: PanoramaClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import PanoramaClient

Client = PanoramaClient


__all__ = ("Client", "PanoramaClient")
