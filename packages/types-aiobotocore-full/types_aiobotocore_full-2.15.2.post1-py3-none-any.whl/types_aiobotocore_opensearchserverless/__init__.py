"""
Main interface for opensearchserverless service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_opensearchserverless import (
        Client,
        OpenSearchServiceServerlessClient,
    )

    session = get_session()
    async with session.create_client("opensearchserverless") as client:
        client: OpenSearchServiceServerlessClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import OpenSearchServiceServerlessClient

Client = OpenSearchServiceServerlessClient


__all__ = ("Client", "OpenSearchServiceServerlessClient")
