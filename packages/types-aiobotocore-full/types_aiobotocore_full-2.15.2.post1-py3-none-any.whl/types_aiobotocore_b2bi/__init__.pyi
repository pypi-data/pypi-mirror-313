"""
Main interface for b2bi service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_b2bi import (
        B2BIClient,
        Client,
        ListCapabilitiesPaginator,
        ListPartnershipsPaginator,
        ListProfilesPaginator,
        ListTransformersPaginator,
    )

    session = get_session()
    async with session.create_client("b2bi") as client:
        client: B2BIClient
        ...


    list_capabilities_paginator: ListCapabilitiesPaginator = client.get_paginator("list_capabilities")
    list_partnerships_paginator: ListPartnershipsPaginator = client.get_paginator("list_partnerships")
    list_profiles_paginator: ListProfilesPaginator = client.get_paginator("list_profiles")
    list_transformers_paginator: ListTransformersPaginator = client.get_paginator("list_transformers")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import B2BIClient
from .paginator import (
    ListCapabilitiesPaginator,
    ListPartnershipsPaginator,
    ListProfilesPaginator,
    ListTransformersPaginator,
)

Client = B2BIClient

__all__ = (
    "B2BIClient",
    "Client",
    "ListCapabilitiesPaginator",
    "ListPartnershipsPaginator",
    "ListProfilesPaginator",
    "ListTransformersPaginator",
)
