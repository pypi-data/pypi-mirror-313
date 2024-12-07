"""
Main interface for synthetics service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_synthetics import (
        Client,
        SyntheticsClient,
    )

    session = get_session()
    async with session.create_client("synthetics") as client:
        client: SyntheticsClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SyntheticsClient

Client = SyntheticsClient

__all__ = ("Client", "SyntheticsClient")
