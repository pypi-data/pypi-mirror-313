"""
Type annotations for mediastore service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediastore.client import MediaStoreClient
    from types_aiobotocore_mediastore.paginator import (
        ListContainersPaginator,
    )

    session = get_session()
    with session.create_client("mediastore") as client:
        client: MediaStoreClient

        list_containers_paginator: ListContainersPaginator = client.get_paginator("list_containers")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListContainersInputListContainersPaginateTypeDef, ListContainersOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListContainersPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListContainersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/paginator/ListContainers.html#MediaStore.Paginator.ListContainers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore/paginators/#listcontainerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListContainersInputListContainersPaginateTypeDef]
    ) -> AsyncIterator[ListContainersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/paginator/ListContainers.html#MediaStore.Paginator.ListContainers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore/paginators/#listcontainerspaginator)
        """
