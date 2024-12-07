"""
Main interface for glacier service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_glacier import (
        Client,
        GlacierClient,
        ListJobsPaginator,
        ListMultipartUploadsPaginator,
        ListPartsPaginator,
        ListVaultsPaginator,
        VaultExistsWaiter,
        VaultNotExistsWaiter,
    )

    session = get_session()
    async with session.create_client("glacier") as client:
        client: GlacierClient
        ...


    vault_exists_waiter: VaultExistsWaiter = client.get_waiter("vault_exists")
    vault_not_exists_waiter: VaultNotExistsWaiter = client.get_waiter("vault_not_exists")

    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_multipart_uploads_paginator: ListMultipartUploadsPaginator = client.get_paginator("list_multipart_uploads")
    list_parts_paginator: ListPartsPaginator = client.get_paginator("list_parts")
    list_vaults_paginator: ListVaultsPaginator = client.get_paginator("list_vaults")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import GlacierClient
from .paginator import (
    ListJobsPaginator,
    ListMultipartUploadsPaginator,
    ListPartsPaginator,
    ListVaultsPaginator,
)
from .waiter import VaultExistsWaiter, VaultNotExistsWaiter

Client = GlacierClient

__all__ = (
    "Client",
    "GlacierClient",
    "ListJobsPaginator",
    "ListMultipartUploadsPaginator",
    "ListPartsPaginator",
    "ListVaultsPaginator",
    "VaultExistsWaiter",
    "VaultNotExistsWaiter",
)
