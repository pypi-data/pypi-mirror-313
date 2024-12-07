"""
Type annotations for mq service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mq.client import MQClient
    from types_aiobotocore_mq.paginator import (
        ListBrokersPaginator,
    )

    session = get_session()
    with session.create_client("mq") as client:
        client: MQClient

        list_brokers_paginator: ListBrokersPaginator = client.get_paginator("list_brokers")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListBrokersRequestListBrokersPaginateTypeDef, ListBrokersResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListBrokersPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListBrokersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/paginator/ListBrokers.html#MQ.Paginator.ListBrokers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/paginators/#listbrokerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBrokersRequestListBrokersPaginateTypeDef]
    ) -> AsyncIterator[ListBrokersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/paginator/ListBrokers.html#MQ.Paginator.ListBrokers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/paginators/#listbrokerspaginator)
        """
