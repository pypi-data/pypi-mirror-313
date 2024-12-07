"""
Type annotations for account service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_account.client import AccountClient
    from types_aiobotocore_account.paginator import (
        ListRegionsPaginator,
    )

    session = get_session()
    with session.create_client("account") as client:
        client: AccountClient

        list_regions_paginator: ListRegionsPaginator = client.get_paginator("list_regions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListRegionsRequestListRegionsPaginateTypeDef, ListRegionsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListRegionsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListRegionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/paginator/ListRegions.html#Account.Paginator.ListRegions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/paginators/#listregionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRegionsRequestListRegionsPaginateTypeDef]
    ) -> AsyncIterator[ListRegionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/paginator/ListRegions.html#Account.Paginator.ListRegions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/paginators/#listregionspaginator)
        """
