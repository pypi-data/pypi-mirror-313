"""
Main interface for ebs service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ebs import (
        Client,
        EBSClient,
    )

    session = get_session()
    async with session.create_client("ebs") as client:
        client: EBSClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import EBSClient

Client = EBSClient


__all__ = ("Client", "EBSClient")
