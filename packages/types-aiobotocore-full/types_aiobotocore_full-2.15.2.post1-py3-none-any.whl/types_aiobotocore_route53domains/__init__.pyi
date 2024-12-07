"""
Main interface for route53domains service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_route53domains import (
        Client,
        ListDomainsPaginator,
        ListOperationsPaginator,
        ListPricesPaginator,
        Route53DomainsClient,
        ViewBillingPaginator,
    )

    session = get_session()
    async with session.create_client("route53domains") as client:
        client: Route53DomainsClient
        ...


    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_operations_paginator: ListOperationsPaginator = client.get_paginator("list_operations")
    list_prices_paginator: ListPricesPaginator = client.get_paginator("list_prices")
    view_billing_paginator: ViewBillingPaginator = client.get_paginator("view_billing")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import Route53DomainsClient
from .paginator import (
    ListDomainsPaginator,
    ListOperationsPaginator,
    ListPricesPaginator,
    ViewBillingPaginator,
)

Client = Route53DomainsClient

__all__ = (
    "Client",
    "ListDomainsPaginator",
    "ListOperationsPaginator",
    "ListPricesPaginator",
    "Route53DomainsClient",
    "ViewBillingPaginator",
)
