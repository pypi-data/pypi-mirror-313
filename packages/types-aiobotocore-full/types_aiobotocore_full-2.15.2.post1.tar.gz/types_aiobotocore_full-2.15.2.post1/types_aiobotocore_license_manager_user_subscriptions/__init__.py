"""
Main interface for license-manager-user-subscriptions service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_license_manager_user_subscriptions import (
        Client,
        LicenseManagerUserSubscriptionsClient,
        ListIdentityProvidersPaginator,
        ListInstancesPaginator,
        ListProductSubscriptionsPaginator,
        ListUserAssociationsPaginator,
    )

    session = get_session()
    async with session.create_client("license-manager-user-subscriptions") as client:
        client: LicenseManagerUserSubscriptionsClient
        ...


    list_identity_providers_paginator: ListIdentityProvidersPaginator = client.get_paginator("list_identity_providers")
    list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    list_product_subscriptions_paginator: ListProductSubscriptionsPaginator = client.get_paginator("list_product_subscriptions")
    list_user_associations_paginator: ListUserAssociationsPaginator = client.get_paginator("list_user_associations")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import LicenseManagerUserSubscriptionsClient
from .paginator import (
    ListIdentityProvidersPaginator,
    ListInstancesPaginator,
    ListProductSubscriptionsPaginator,
    ListUserAssociationsPaginator,
)

Client = LicenseManagerUserSubscriptionsClient


__all__ = (
    "Client",
    "LicenseManagerUserSubscriptionsClient",
    "ListIdentityProvidersPaginator",
    "ListInstancesPaginator",
    "ListProductSubscriptionsPaginator",
    "ListUserAssociationsPaginator",
)
