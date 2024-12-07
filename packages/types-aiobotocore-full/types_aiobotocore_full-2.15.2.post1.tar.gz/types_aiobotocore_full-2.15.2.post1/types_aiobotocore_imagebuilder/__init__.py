"""
Main interface for imagebuilder service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_imagebuilder import (
        Client,
        ImagebuilderClient,
    )

    session = get_session()
    async with session.create_client("imagebuilder") as client:
        client: ImagebuilderClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ImagebuilderClient

Client = ImagebuilderClient


__all__ = ("Client", "ImagebuilderClient")
