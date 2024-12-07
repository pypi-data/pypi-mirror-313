"""
Main interface for verifiedpermissions service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_verifiedpermissions import (
        Client,
        ListIdentitySourcesPaginator,
        ListPoliciesPaginator,
        ListPolicyStoresPaginator,
        ListPolicyTemplatesPaginator,
        VerifiedPermissionsClient,
    )

    session = get_session()
    async with session.create_client("verifiedpermissions") as client:
        client: VerifiedPermissionsClient
        ...


    list_identity_sources_paginator: ListIdentitySourcesPaginator = client.get_paginator("list_identity_sources")
    list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
    list_policy_stores_paginator: ListPolicyStoresPaginator = client.get_paginator("list_policy_stores")
    list_policy_templates_paginator: ListPolicyTemplatesPaginator = client.get_paginator("list_policy_templates")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import VerifiedPermissionsClient
from .paginator import (
    ListIdentitySourcesPaginator,
    ListPoliciesPaginator,
    ListPolicyStoresPaginator,
    ListPolicyTemplatesPaginator,
)

Client = VerifiedPermissionsClient

__all__ = (
    "Client",
    "ListIdentitySourcesPaginator",
    "ListPoliciesPaginator",
    "ListPolicyStoresPaginator",
    "ListPolicyTemplatesPaginator",
    "VerifiedPermissionsClient",
)
