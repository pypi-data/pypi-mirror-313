"""
Main interface for savingsplans service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_savingsplans import (
        Client,
        SavingsPlansClient,
    )

    session = get_session()
    async with session.create_client("savingsplans") as client:
        client: SavingsPlansClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SavingsPlansClient

Client = SavingsPlansClient

__all__ = ("Client", "SavingsPlansClient")
