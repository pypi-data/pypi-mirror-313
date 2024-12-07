"""
Type annotations for freetier service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_freetier/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_freetier.client import FreeTierClient
    from types_aiobotocore_freetier.paginator import (
        GetFreeTierUsagePaginator,
    )

    session = get_session()
    with session.create_client("freetier") as client:
        client: FreeTierClient

        get_free_tier_usage_paginator: GetFreeTierUsagePaginator = client.get_paginator("get_free_tier_usage")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetFreeTierUsageRequestGetFreeTierUsagePaginateTypeDef,
    GetFreeTierUsageResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("GetFreeTierUsagePaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetFreeTierUsagePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/freetier/paginator/GetFreeTierUsage.html#FreeTier.Paginator.GetFreeTierUsage)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_freetier/paginators/#getfreetierusagepaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetFreeTierUsageRequestGetFreeTierUsagePaginateTypeDef]
    ) -> AsyncIterator[GetFreeTierUsageResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/freetier/paginator/GetFreeTierUsage.html#FreeTier.Paginator.GetFreeTierUsage.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_freetier/paginators/#getfreetierusagepaginator)
        """
