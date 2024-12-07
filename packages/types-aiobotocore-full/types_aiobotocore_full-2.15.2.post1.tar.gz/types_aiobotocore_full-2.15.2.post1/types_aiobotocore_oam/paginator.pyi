"""
Type annotations for oam service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_oam/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_oam.client import CloudWatchObservabilityAccessManagerClient
    from types_aiobotocore_oam.paginator import (
        ListAttachedLinksPaginator,
        ListLinksPaginator,
        ListSinksPaginator,
    )

    session = get_session()
    with session.create_client("oam") as client:
        client: CloudWatchObservabilityAccessManagerClient

        list_attached_links_paginator: ListAttachedLinksPaginator = client.get_paginator("list_attached_links")
        list_links_paginator: ListLinksPaginator = client.get_paginator("list_links")
        list_sinks_paginator: ListSinksPaginator = client.get_paginator("list_sinks")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAttachedLinksInputListAttachedLinksPaginateTypeDef,
    ListAttachedLinksOutputTypeDef,
    ListLinksInputListLinksPaginateTypeDef,
    ListLinksOutputTypeDef,
    ListSinksInputListSinksPaginateTypeDef,
    ListSinksOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListAttachedLinksPaginator", "ListLinksPaginator", "ListSinksPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAttachedLinksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListAttachedLinks.html#CloudWatchObservabilityAccessManager.Paginator.ListAttachedLinks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_oam/paginators/#listattachedlinkspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAttachedLinksInputListAttachedLinksPaginateTypeDef]
    ) -> AsyncIterator[ListAttachedLinksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListAttachedLinks.html#CloudWatchObservabilityAccessManager.Paginator.ListAttachedLinks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_oam/paginators/#listattachedlinkspaginator)
        """

class ListLinksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListLinks.html#CloudWatchObservabilityAccessManager.Paginator.ListLinks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_oam/paginators/#listlinkspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLinksInputListLinksPaginateTypeDef]
    ) -> AsyncIterator[ListLinksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListLinks.html#CloudWatchObservabilityAccessManager.Paginator.ListLinks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_oam/paginators/#listlinkspaginator)
        """

class ListSinksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListSinks.html#CloudWatchObservabilityAccessManager.Paginator.ListSinks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_oam/paginators/#listsinkspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSinksInputListSinksPaginateTypeDef]
    ) -> AsyncIterator[ListSinksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListSinks.html#CloudWatchObservabilityAccessManager.Paginator.ListSinks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_oam/paginators/#listsinkspaginator)
        """
