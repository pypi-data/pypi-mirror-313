"""
Type annotations for ivs-realtime service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ivs_realtime.client import IvsrealtimeClient
    from types_aiobotocore_ivs_realtime.paginator import (
        ListIngestConfigurationsPaginator,
        ListPublicKeysPaginator,
    )

    session = get_session()
    with session.create_client("ivs-realtime") as client:
        client: IvsrealtimeClient

        list_ingest_configurations_paginator: ListIngestConfigurationsPaginator = client.get_paginator("list_ingest_configurations")
        list_public_keys_paginator: ListPublicKeysPaginator = client.get_paginator("list_public_keys")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListIngestConfigurationsRequestListIngestConfigurationsPaginateTypeDef,
    ListIngestConfigurationsResponseTypeDef,
    ListPublicKeysRequestListPublicKeysPaginateTypeDef,
    ListPublicKeysResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListIngestConfigurationsPaginator", "ListPublicKeysPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListIngestConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime/paginator/ListIngestConfigurations.html#Ivsrealtime.Paginator.ListIngestConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/paginators/#listingestconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListIngestConfigurationsRequestListIngestConfigurationsPaginateTypeDef],
    ) -> AsyncIterator[ListIngestConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime/paginator/ListIngestConfigurations.html#Ivsrealtime.Paginator.ListIngestConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/paginators/#listingestconfigurationspaginator)
        """

class ListPublicKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime/paginator/ListPublicKeys.html#Ivsrealtime.Paginator.ListPublicKeys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/paginators/#listpublickeyspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPublicKeysRequestListPublicKeysPaginateTypeDef]
    ) -> AsyncIterator[ListPublicKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime/paginator/ListPublicKeys.html#Ivsrealtime.Paginator.ListPublicKeys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/paginators/#listpublickeyspaginator)
        """
