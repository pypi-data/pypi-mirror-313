"""
Main interface for auditmanager service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_auditmanager import (
        AuditManagerClient,
        Client,
    )

    session = get_session()
    async with session.create_client("auditmanager") as client:
        client: AuditManagerClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import AuditManagerClient

Client = AuditManagerClient

__all__ = ("AuditManagerClient", "Client")
