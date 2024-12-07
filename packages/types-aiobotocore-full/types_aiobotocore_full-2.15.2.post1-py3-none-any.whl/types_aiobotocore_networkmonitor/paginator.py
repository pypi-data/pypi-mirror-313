"""
Type annotations for networkmonitor service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_networkmonitor.client import CloudWatchNetworkMonitorClient
    from types_aiobotocore_networkmonitor.paginator import (
        ListMonitorsPaginator,
    )

    session = get_session()
    with session.create_client("networkmonitor") as client:
        client: CloudWatchNetworkMonitorClient

        list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListMonitorsInputListMonitorsPaginateTypeDef, ListMonitorsOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListMonitorsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListMonitorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor/paginator/ListMonitors.html#CloudWatchNetworkMonitor.Paginator.ListMonitors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/paginators/#listmonitorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMonitorsInputListMonitorsPaginateTypeDef]
    ) -> AsyncIterator[ListMonitorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor/paginator/ListMonitors.html#CloudWatchNetworkMonitor.Paginator.ListMonitors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/paginators/#listmonitorspaginator)
        """
