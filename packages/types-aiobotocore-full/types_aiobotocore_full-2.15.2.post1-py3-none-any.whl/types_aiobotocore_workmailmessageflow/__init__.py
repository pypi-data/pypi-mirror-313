"""
Main interface for workmailmessageflow service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_workmailmessageflow import (
        Client,
        WorkMailMessageFlowClient,
    )

    session = get_session()
    async with session.create_client("workmailmessageflow") as client:
        client: WorkMailMessageFlowClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import WorkMailMessageFlowClient

Client = WorkMailMessageFlowClient


__all__ = ("Client", "WorkMailMessageFlowClient")
