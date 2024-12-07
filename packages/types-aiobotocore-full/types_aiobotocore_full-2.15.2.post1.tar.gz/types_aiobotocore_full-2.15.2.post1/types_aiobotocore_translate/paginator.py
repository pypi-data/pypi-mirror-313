"""
Type annotations for translate service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_translate.client import TranslateClient
    from types_aiobotocore_translate.paginator import (
        ListTerminologiesPaginator,
    )

    session = get_session()
    with session.create_client("translate") as client:
        client: TranslateClient

        list_terminologies_paginator: ListTerminologiesPaginator = client.get_paginator("list_terminologies")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListTerminologiesRequestListTerminologiesPaginateTypeDef,
    ListTerminologiesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListTerminologiesPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListTerminologiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/paginator/ListTerminologies.html#Translate.Paginator.ListTerminologies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/paginators/#listterminologiespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTerminologiesRequestListTerminologiesPaginateTypeDef]
    ) -> AsyncIterator[ListTerminologiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/paginator/ListTerminologies.html#Translate.Paginator.ListTerminologies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/paginators/#listterminologiespaginator)
        """
