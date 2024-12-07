"""
Main interface for apprunner service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_apprunner import (
        AppRunnerClient,
        Client,
    )

    session = get_session()
    async with session.create_client("apprunner") as client:
        client: AppRunnerClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import AppRunnerClient

Client = AppRunnerClient

__all__ = ("AppRunnerClient", "Client")
