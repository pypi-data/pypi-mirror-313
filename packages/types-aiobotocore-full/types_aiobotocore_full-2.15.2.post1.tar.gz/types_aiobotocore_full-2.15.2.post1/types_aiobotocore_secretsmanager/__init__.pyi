"""
Main interface for secretsmanager service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_secretsmanager import (
        Client,
        ListSecretsPaginator,
        SecretsManagerClient,
    )

    session = get_session()
    async with session.create_client("secretsmanager") as client:
        client: SecretsManagerClient
        ...


    list_secrets_paginator: ListSecretsPaginator = client.get_paginator("list_secrets")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SecretsManagerClient
from .paginator import ListSecretsPaginator

Client = SecretsManagerClient

__all__ = ("Client", "ListSecretsPaginator", "SecretsManagerClient")
