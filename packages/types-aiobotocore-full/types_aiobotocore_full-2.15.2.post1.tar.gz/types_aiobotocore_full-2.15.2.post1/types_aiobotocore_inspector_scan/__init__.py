"""
Main interface for inspector-scan service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_inspector_scan import (
        Client,
        InspectorscanClient,
    )

    session = get_session()
    async with session.create_client("inspector-scan") as client:
        client: InspectorscanClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import InspectorscanClient

Client = InspectorscanClient


__all__ = ("Client", "InspectorscanClient")
