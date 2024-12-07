"""
Type annotations for mediastore-data service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediastore_data.client import MediaStoreDataClient
    from types_aiobotocore_mediastore_data.paginator import (
        ListItemsPaginator,
    )

    session = get_session()
    with session.create_client("mediastore-data") as client:
        client: MediaStoreDataClient

        list_items_paginator: ListItemsPaginator = client.get_paginator("list_items")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListItemsRequestListItemsPaginateTypeDef, ListItemsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListItemsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListItemsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data/paginator/ListItems.html#MediaStoreData.Paginator.ListItems)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/paginators/#listitemspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListItemsRequestListItemsPaginateTypeDef]
    ) -> AsyncIterator[ListItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data/paginator/ListItems.html#MediaStoreData.Paginator.ListItems.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/paginators/#listitemspaginator)
        """
