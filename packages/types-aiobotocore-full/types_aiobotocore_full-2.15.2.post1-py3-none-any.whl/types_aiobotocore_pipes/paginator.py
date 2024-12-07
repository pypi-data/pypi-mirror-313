"""
Type annotations for pipes service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pipes/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_pipes.client import EventBridgePipesClient
    from types_aiobotocore_pipes.paginator import (
        ListPipesPaginator,
    )

    session = get_session()
    with session.create_client("pipes") as client:
        client: EventBridgePipesClient

        list_pipes_paginator: ListPipesPaginator = client.get_paginator("list_pipes")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListPipesRequestListPipesPaginateTypeDef, ListPipesResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListPipesPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListPipesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/paginator/ListPipes.html#EventBridgePipes.Paginator.ListPipes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pipes/paginators/#listpipespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPipesRequestListPipesPaginateTypeDef]
    ) -> AsyncIterator[ListPipesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/paginator/ListPipes.html#EventBridgePipes.Paginator.ListPipes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pipes/paginators/#listpipespaginator)
        """
