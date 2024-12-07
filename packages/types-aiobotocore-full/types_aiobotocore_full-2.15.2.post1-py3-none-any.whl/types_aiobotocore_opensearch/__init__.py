"""
Main interface for opensearch service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_opensearch import (
        Client,
        OpenSearchServiceClient,
    )

    session = get_session()
    async with session.create_client("opensearch") as client:
        client: OpenSearchServiceClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import OpenSearchServiceClient

Client = OpenSearchServiceClient


__all__ = ("Client", "OpenSearchServiceClient")
