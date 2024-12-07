"""
Type annotations for marketplace-entitlement service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_marketplace_entitlement.client import MarketplaceEntitlementServiceClient
    from types_aiobotocore_marketplace_entitlement.paginator import (
        GetEntitlementsPaginator,
    )

    session = get_session()
    with session.create_client("marketplace-entitlement") as client:
        client: MarketplaceEntitlementServiceClient

        get_entitlements_paginator: GetEntitlementsPaginator = client.get_paginator("get_entitlements")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetEntitlementsRequestGetEntitlementsPaginateTypeDef,
    GetEntitlementsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("GetEntitlementsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetEntitlementsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement/paginator/GetEntitlements.html#MarketplaceEntitlementService.Paginator.GetEntitlements)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/paginators/#getentitlementspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetEntitlementsRequestGetEntitlementsPaginateTypeDef]
    ) -> AsyncIterator[GetEntitlementsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement/paginator/GetEntitlements.html#MarketplaceEntitlementService.Paginator.GetEntitlements.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/paginators/#getentitlementspaginator)
        """
