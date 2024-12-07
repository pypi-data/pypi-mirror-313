"""
Main interface for simspaceweaver service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_simspaceweaver import (
        Client,
        SimSpaceWeaverClient,
    )

    session = get_session()
    async with session.create_client("simspaceweaver") as client:
        client: SimSpaceWeaverClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SimSpaceWeaverClient

Client = SimSpaceWeaverClient


__all__ = ("Client", "SimSpaceWeaverClient")
