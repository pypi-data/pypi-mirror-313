"""
Main interface for migrationhub-config service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_migrationhub_config import (
        Client,
        MigrationHubConfigClient,
    )

    session = get_session()
    async with session.create_client("migrationhub-config") as client:
        client: MigrationHubConfigClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import MigrationHubConfigClient

Client = MigrationHubConfigClient


__all__ = ("Client", "MigrationHubConfigClient")
