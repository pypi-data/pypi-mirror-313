"""
Type annotations for sdb service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sdb.client import SimpleDBClient
    from types_aiobotocore_sdb.paginator import (
        ListDomainsPaginator,
        SelectPaginator,
    )

    session = get_session()
    with session.create_client("sdb") as client:
        client: SimpleDBClient

        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        select_paginator: SelectPaginator = client.get_paginator("select")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListDomainsRequestListDomainsPaginateTypeDef,
    ListDomainsResultTypeDef,
    SelectRequestSelectPaginateTypeDef,
    SelectResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListDomainsPaginator", "SelectPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDomainsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/paginator/ListDomains.html#SimpleDB.Paginator.ListDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/paginators/#listdomainspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDomainsRequestListDomainsPaginateTypeDef]
    ) -> AsyncIterator[ListDomainsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/paginator/ListDomains.html#SimpleDB.Paginator.ListDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/paginators/#listdomainspaginator)
        """

class SelectPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/paginator/Select.html#SimpleDB.Paginator.Select)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/paginators/#selectpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SelectRequestSelectPaginateTypeDef]
    ) -> AsyncIterator[SelectResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/paginator/Select.html#SimpleDB.Paginator.Select.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/paginators/#selectpaginator)
        """
