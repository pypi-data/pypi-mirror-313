"""
Main interface for marketplace-agreement service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplace_agreement import (
        AgreementServiceClient,
        Client,
    )

    session = get_session()
    async with session.create_client("marketplace-agreement") as client:
        client: AgreementServiceClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import AgreementServiceClient

Client = AgreementServiceClient


__all__ = ("AgreementServiceClient", "Client")
