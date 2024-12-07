"""
Main interface for comprehendmedical service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_comprehendmedical import (
        Client,
        ComprehendMedicalClient,
    )

    session = get_session()
    async with session.create_client("comprehendmedical") as client:
        client: ComprehendMedicalClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ComprehendMedicalClient

Client = ComprehendMedicalClient


__all__ = ("Client", "ComprehendMedicalClient")
