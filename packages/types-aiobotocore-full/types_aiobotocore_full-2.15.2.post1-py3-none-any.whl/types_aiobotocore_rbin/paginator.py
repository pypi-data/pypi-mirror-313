"""
Type annotations for rbin service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_rbin.client import RecycleBinClient
    from types_aiobotocore_rbin.paginator import (
        ListRulesPaginator,
    )

    session = get_session()
    with session.create_client("rbin") as client:
        client: RecycleBinClient

        list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListRulesRequestListRulesPaginateTypeDef, ListRulesResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListRulesPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/paginator/ListRules.html#RecycleBin.Paginator.ListRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/paginators/#listrulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRulesRequestListRulesPaginateTypeDef]
    ) -> AsyncIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/paginator/ListRules.html#RecycleBin.Paginator.ListRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/paginators/#listrulespaginator)
        """
