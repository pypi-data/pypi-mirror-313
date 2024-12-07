"""
Main interface for eks-auth service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_eks_auth import (
        Client,
        EKSAuthClient,
    )

    session = get_session()
    async with session.create_client("eks-auth") as client:
        client: EKSAuthClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import EKSAuthClient

Client = EKSAuthClient

__all__ = ("Client", "EKSAuthClient")
