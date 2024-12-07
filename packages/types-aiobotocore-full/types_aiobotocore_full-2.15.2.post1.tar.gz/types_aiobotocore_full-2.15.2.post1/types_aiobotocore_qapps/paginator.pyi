"""
Type annotations for qapps service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_qapps.client import QAppsClient
    from types_aiobotocore_qapps.paginator import (
        ListLibraryItemsPaginator,
        ListQAppsPaginator,
    )

    session = get_session()
    with session.create_client("qapps") as client:
        client: QAppsClient

        list_library_items_paginator: ListLibraryItemsPaginator = client.get_paginator("list_library_items")
        list_q_apps_paginator: ListQAppsPaginator = client.get_paginator("list_q_apps")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListLibraryItemsInputListLibraryItemsPaginateTypeDef,
    ListLibraryItemsOutputTypeDef,
    ListQAppsInputListQAppsPaginateTypeDef,
    ListQAppsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListLibraryItemsPaginator", "ListQAppsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListLibraryItemsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/paginator/ListLibraryItems.html#QApps.Paginator.ListLibraryItems)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/paginators/#listlibraryitemspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLibraryItemsInputListLibraryItemsPaginateTypeDef]
    ) -> AsyncIterator[ListLibraryItemsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/paginator/ListLibraryItems.html#QApps.Paginator.ListLibraryItems.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/paginators/#listlibraryitemspaginator)
        """

class ListQAppsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/paginator/ListQApps.html#QApps.Paginator.ListQApps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/paginators/#listqappspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListQAppsInputListQAppsPaginateTypeDef]
    ) -> AsyncIterator[ListQAppsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/paginator/ListQApps.html#QApps.Paginator.ListQApps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/paginators/#listqappspaginator)
        """
