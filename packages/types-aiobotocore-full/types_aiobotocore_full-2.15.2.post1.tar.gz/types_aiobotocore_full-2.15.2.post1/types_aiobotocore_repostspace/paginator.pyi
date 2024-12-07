"""
Type annotations for repostspace service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_repostspace.client import RePostPrivateClient
    from types_aiobotocore_repostspace.paginator import (
        ListSpacesPaginator,
    )

    session = get_session()
    with session.create_client("repostspace") as client:
        client: RePostPrivateClient

        list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListSpacesInputListSpacesPaginateTypeDef, ListSpacesOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListSpacesPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListSpacesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/paginator/ListSpaces.html#RePostPrivate.Paginator.ListSpaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/paginators/#listspacespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSpacesInputListSpacesPaginateTypeDef]
    ) -> AsyncIterator[ListSpacesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/paginator/ListSpaces.html#RePostPrivate.Paginator.ListSpaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/paginators/#listspacespaginator)
        """
