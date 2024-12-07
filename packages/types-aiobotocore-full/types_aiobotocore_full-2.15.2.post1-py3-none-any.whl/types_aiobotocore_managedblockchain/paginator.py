"""
Type annotations for managedblockchain service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_managedblockchain.client import ManagedBlockchainClient
    from types_aiobotocore_managedblockchain.paginator import (
        ListAccessorsPaginator,
    )

    session = get_session()
    with session.create_client("managedblockchain") as client:
        client: ManagedBlockchainClient

        list_accessors_paginator: ListAccessorsPaginator = client.get_paginator("list_accessors")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListAccessorsInputListAccessorsPaginateTypeDef, ListAccessorsOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListAccessorsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAccessorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/paginator/ListAccessors.html#ManagedBlockchain.Paginator.ListAccessors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/paginators/#listaccessorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAccessorsInputListAccessorsPaginateTypeDef]
    ) -> AsyncIterator[ListAccessorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/paginator/ListAccessors.html#ManagedBlockchain.Paginator.ListAccessors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/paginators/#listaccessorspaginator)
        """
