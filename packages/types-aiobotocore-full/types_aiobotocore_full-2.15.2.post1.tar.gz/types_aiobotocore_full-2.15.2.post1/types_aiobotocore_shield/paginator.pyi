"""
Type annotations for shield service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_shield/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_shield.client import ShieldClient
    from types_aiobotocore_shield.paginator import (
        ListAttacksPaginator,
        ListProtectionsPaginator,
    )

    session = get_session()
    with session.create_client("shield") as client:
        client: ShieldClient

        list_attacks_paginator: ListAttacksPaginator = client.get_paginator("list_attacks")
        list_protections_paginator: ListProtectionsPaginator = client.get_paginator("list_protections")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAttacksRequestListAttacksPaginateTypeDef,
    ListAttacksResponseTypeDef,
    ListProtectionsRequestListProtectionsPaginateTypeDef,
    ListProtectionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListAttacksPaginator", "ListProtectionsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAttacksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield/paginator/ListAttacks.html#Shield.Paginator.ListAttacks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_shield/paginators/#listattackspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAttacksRequestListAttacksPaginateTypeDef]
    ) -> AsyncIterator[ListAttacksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield/paginator/ListAttacks.html#Shield.Paginator.ListAttacks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_shield/paginators/#listattackspaginator)
        """

class ListProtectionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield/paginator/ListProtections.html#Shield.Paginator.ListProtections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_shield/paginators/#listprotectionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProtectionsRequestListProtectionsPaginateTypeDef]
    ) -> AsyncIterator[ListProtectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield/paginator/ListProtections.html#Shield.Paginator.ListProtections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_shield/paginators/#listprotectionspaginator)
        """
