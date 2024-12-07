"""
Type annotations for rum service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_rum.client import CloudWatchRUMClient
    from types_aiobotocore_rum.paginator import (
        BatchGetRumMetricDefinitionsPaginator,
        GetAppMonitorDataPaginator,
        ListAppMonitorsPaginator,
        ListRumMetricsDestinationsPaginator,
    )

    session = get_session()
    with session.create_client("rum") as client:
        client: CloudWatchRUMClient

        batch_get_rum_metric_definitions_paginator: BatchGetRumMetricDefinitionsPaginator = client.get_paginator("batch_get_rum_metric_definitions")
        get_app_monitor_data_paginator: GetAppMonitorDataPaginator = client.get_paginator("get_app_monitor_data")
        list_app_monitors_paginator: ListAppMonitorsPaginator = client.get_paginator("list_app_monitors")
        list_rum_metrics_destinations_paginator: ListRumMetricsDestinationsPaginator = client.get_paginator("list_rum_metrics_destinations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    BatchGetRumMetricDefinitionsRequestBatchGetRumMetricDefinitionsPaginateTypeDef,
    BatchGetRumMetricDefinitionsResponseTypeDef,
    GetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef,
    GetAppMonitorDataResponseTypeDef,
    ListAppMonitorsRequestListAppMonitorsPaginateTypeDef,
    ListAppMonitorsResponseTypeDef,
    ListRumMetricsDestinationsRequestListRumMetricsDestinationsPaginateTypeDef,
    ListRumMetricsDestinationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "BatchGetRumMetricDefinitionsPaginator",
    "GetAppMonitorDataPaginator",
    "ListAppMonitorsPaginator",
    "ListRumMetricsDestinationsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class BatchGetRumMetricDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/BatchGetRumMetricDefinitions.html#CloudWatchRUM.Paginator.BatchGetRumMetricDefinitions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/#batchgetrummetricdefinitionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            BatchGetRumMetricDefinitionsRequestBatchGetRumMetricDefinitionsPaginateTypeDef
        ],
    ) -> AsyncIterator[BatchGetRumMetricDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/BatchGetRumMetricDefinitions.html#CloudWatchRUM.Paginator.BatchGetRumMetricDefinitions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/#batchgetrummetricdefinitionspaginator)
        """


class GetAppMonitorDataPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/GetAppMonitorData.html#CloudWatchRUM.Paginator.GetAppMonitorData)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/#getappmonitordatapaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef]
    ) -> AsyncIterator[GetAppMonitorDataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/GetAppMonitorData.html#CloudWatchRUM.Paginator.GetAppMonitorData.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/#getappmonitordatapaginator)
        """


class ListAppMonitorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/ListAppMonitors.html#CloudWatchRUM.Paginator.ListAppMonitors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/#listappmonitorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAppMonitorsRequestListAppMonitorsPaginateTypeDef]
    ) -> AsyncIterator[ListAppMonitorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/ListAppMonitors.html#CloudWatchRUM.Paginator.ListAppMonitors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/#listappmonitorspaginator)
        """


class ListRumMetricsDestinationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/ListRumMetricsDestinations.html#CloudWatchRUM.Paginator.ListRumMetricsDestinations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/#listrummetricsdestinationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListRumMetricsDestinationsRequestListRumMetricsDestinationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListRumMetricsDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/ListRumMetricsDestinations.html#CloudWatchRUM.Paginator.ListRumMetricsDestinations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/#listrummetricsdestinationspaginator)
        """
