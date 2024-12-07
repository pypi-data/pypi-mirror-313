"""
Type annotations for logs service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_logs.client import CloudWatchLogsClient
    from types_aiobotocore_logs.paginator import (
        DescribeConfigurationTemplatesPaginator,
        DescribeDeliveriesPaginator,
        DescribeDeliveryDestinationsPaginator,
        DescribeDeliverySourcesPaginator,
        DescribeDestinationsPaginator,
        DescribeExportTasksPaginator,
        DescribeLogGroupsPaginator,
        DescribeLogStreamsPaginator,
        DescribeMetricFiltersPaginator,
        DescribeQueriesPaginator,
        DescribeResourcePoliciesPaginator,
        DescribeSubscriptionFiltersPaginator,
        FilterLogEventsPaginator,
        ListAnomaliesPaginator,
        ListLogAnomalyDetectorsPaginator,
    )

    session = get_session()
    with session.create_client("logs") as client:
        client: CloudWatchLogsClient

        describe_configuration_templates_paginator: DescribeConfigurationTemplatesPaginator = client.get_paginator("describe_configuration_templates")
        describe_deliveries_paginator: DescribeDeliveriesPaginator = client.get_paginator("describe_deliveries")
        describe_delivery_destinations_paginator: DescribeDeliveryDestinationsPaginator = client.get_paginator("describe_delivery_destinations")
        describe_delivery_sources_paginator: DescribeDeliverySourcesPaginator = client.get_paginator("describe_delivery_sources")
        describe_destinations_paginator: DescribeDestinationsPaginator = client.get_paginator("describe_destinations")
        describe_export_tasks_paginator: DescribeExportTasksPaginator = client.get_paginator("describe_export_tasks")
        describe_log_groups_paginator: DescribeLogGroupsPaginator = client.get_paginator("describe_log_groups")
        describe_log_streams_paginator: DescribeLogStreamsPaginator = client.get_paginator("describe_log_streams")
        describe_metric_filters_paginator: DescribeMetricFiltersPaginator = client.get_paginator("describe_metric_filters")
        describe_queries_paginator: DescribeQueriesPaginator = client.get_paginator("describe_queries")
        describe_resource_policies_paginator: DescribeResourcePoliciesPaginator = client.get_paginator("describe_resource_policies")
        describe_subscription_filters_paginator: DescribeSubscriptionFiltersPaginator = client.get_paginator("describe_subscription_filters")
        filter_log_events_paginator: FilterLogEventsPaginator = client.get_paginator("filter_log_events")
        list_anomalies_paginator: ListAnomaliesPaginator = client.get_paginator("list_anomalies")
        list_log_anomaly_detectors_paginator: ListLogAnomalyDetectorsPaginator = client.get_paginator("list_log_anomaly_detectors")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeConfigurationTemplatesRequestDescribeConfigurationTemplatesPaginateTypeDef,
    DescribeConfigurationTemplatesResponseTypeDef,
    DescribeDeliveriesRequestDescribeDeliveriesPaginateTypeDef,
    DescribeDeliveriesResponseTypeDef,
    DescribeDeliveryDestinationsRequestDescribeDeliveryDestinationsPaginateTypeDef,
    DescribeDeliveryDestinationsResponseTypeDef,
    DescribeDeliverySourcesRequestDescribeDeliverySourcesPaginateTypeDef,
    DescribeDeliverySourcesResponseTypeDef,
    DescribeDestinationsRequestDescribeDestinationsPaginateTypeDef,
    DescribeDestinationsResponseTypeDef,
    DescribeExportTasksRequestDescribeExportTasksPaginateTypeDef,
    DescribeExportTasksResponseTypeDef,
    DescribeLogGroupsRequestDescribeLogGroupsPaginateTypeDef,
    DescribeLogGroupsResponseTypeDef,
    DescribeLogStreamsRequestDescribeLogStreamsPaginateTypeDef,
    DescribeLogStreamsResponseTypeDef,
    DescribeMetricFiltersRequestDescribeMetricFiltersPaginateTypeDef,
    DescribeMetricFiltersResponseTypeDef,
    DescribeQueriesRequestDescribeQueriesPaginateTypeDef,
    DescribeQueriesResponseTypeDef,
    DescribeResourcePoliciesRequestDescribeResourcePoliciesPaginateTypeDef,
    DescribeResourcePoliciesResponseTypeDef,
    DescribeSubscriptionFiltersRequestDescribeSubscriptionFiltersPaginateTypeDef,
    DescribeSubscriptionFiltersResponseTypeDef,
    FilterLogEventsRequestFilterLogEventsPaginateTypeDef,
    FilterLogEventsResponseTypeDef,
    ListAnomaliesRequestListAnomaliesPaginateTypeDef,
    ListAnomaliesResponseTypeDef,
    ListLogAnomalyDetectorsRequestListLogAnomalyDetectorsPaginateTypeDef,
    ListLogAnomalyDetectorsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeConfigurationTemplatesPaginator",
    "DescribeDeliveriesPaginator",
    "DescribeDeliveryDestinationsPaginator",
    "DescribeDeliverySourcesPaginator",
    "DescribeDestinationsPaginator",
    "DescribeExportTasksPaginator",
    "DescribeLogGroupsPaginator",
    "DescribeLogStreamsPaginator",
    "DescribeMetricFiltersPaginator",
    "DescribeQueriesPaginator",
    "DescribeResourcePoliciesPaginator",
    "DescribeSubscriptionFiltersPaginator",
    "FilterLogEventsPaginator",
    "ListAnomaliesPaginator",
    "ListLogAnomalyDetectorsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeConfigurationTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeConfigurationTemplates.html#CloudWatchLogs.Paginator.DescribeConfigurationTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeconfigurationtemplatespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeConfigurationTemplatesRequestDescribeConfigurationTemplatesPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeConfigurationTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeConfigurationTemplates.html#CloudWatchLogs.Paginator.DescribeConfigurationTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeconfigurationtemplatespaginator)
        """

class DescribeDeliveriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliveries.html#CloudWatchLogs.Paginator.DescribeDeliveries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedeliveriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeDeliveriesRequestDescribeDeliveriesPaginateTypeDef]
    ) -> AsyncIterator[DescribeDeliveriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliveries.html#CloudWatchLogs.Paginator.DescribeDeliveries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedeliveriespaginator)
        """

class DescribeDeliveryDestinationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliveryDestinations.html#CloudWatchLogs.Paginator.DescribeDeliveryDestinations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedeliverydestinationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeDeliveryDestinationsRequestDescribeDeliveryDestinationsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeDeliveryDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliveryDestinations.html#CloudWatchLogs.Paginator.DescribeDeliveryDestinations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedeliverydestinationspaginator)
        """

class DescribeDeliverySourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliverySources.html#CloudWatchLogs.Paginator.DescribeDeliverySources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedeliverysourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeDeliverySourcesRequestDescribeDeliverySourcesPaginateTypeDef]
    ) -> AsyncIterator[DescribeDeliverySourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliverySources.html#CloudWatchLogs.Paginator.DescribeDeliverySources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedeliverysourcespaginator)
        """

class DescribeDestinationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDestinations.html#CloudWatchLogs.Paginator.DescribeDestinations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedestinationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeDestinationsRequestDescribeDestinationsPaginateTypeDef]
    ) -> AsyncIterator[DescribeDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDestinations.html#CloudWatchLogs.Paginator.DescribeDestinations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedestinationspaginator)
        """

class DescribeExportTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeExportTasks.html#CloudWatchLogs.Paginator.DescribeExportTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeexporttaskspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeExportTasksRequestDescribeExportTasksPaginateTypeDef]
    ) -> AsyncIterator[DescribeExportTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeExportTasks.html#CloudWatchLogs.Paginator.DescribeExportTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeexporttaskspaginator)
        """

class DescribeLogGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeLogGroups.html#CloudWatchLogs.Paginator.DescribeLogGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeloggroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeLogGroupsRequestDescribeLogGroupsPaginateTypeDef]
    ) -> AsyncIterator[DescribeLogGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeLogGroups.html#CloudWatchLogs.Paginator.DescribeLogGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeloggroupspaginator)
        """

class DescribeLogStreamsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeLogStreams.html#CloudWatchLogs.Paginator.DescribeLogStreams)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describelogstreamspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeLogStreamsRequestDescribeLogStreamsPaginateTypeDef]
    ) -> AsyncIterator[DescribeLogStreamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeLogStreams.html#CloudWatchLogs.Paginator.DescribeLogStreams.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describelogstreamspaginator)
        """

class DescribeMetricFiltersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeMetricFilters.html#CloudWatchLogs.Paginator.DescribeMetricFilters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describemetricfilterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeMetricFiltersRequestDescribeMetricFiltersPaginateTypeDef]
    ) -> AsyncIterator[DescribeMetricFiltersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeMetricFilters.html#CloudWatchLogs.Paginator.DescribeMetricFilters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describemetricfilterspaginator)
        """

class DescribeQueriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeQueries.html#CloudWatchLogs.Paginator.DescribeQueries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describequeriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeQueriesRequestDescribeQueriesPaginateTypeDef]
    ) -> AsyncIterator[DescribeQueriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeQueries.html#CloudWatchLogs.Paginator.DescribeQueries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describequeriespaginator)
        """

class DescribeResourcePoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeResourcePolicies.html#CloudWatchLogs.Paginator.DescribeResourcePolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeresourcepoliciespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeResourcePoliciesRequestDescribeResourcePoliciesPaginateTypeDef],
    ) -> AsyncIterator[DescribeResourcePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeResourcePolicies.html#CloudWatchLogs.Paginator.DescribeResourcePolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeresourcepoliciespaginator)
        """

class DescribeSubscriptionFiltersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeSubscriptionFilters.html#CloudWatchLogs.Paginator.DescribeSubscriptionFilters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describesubscriptionfilterspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeSubscriptionFiltersRequestDescribeSubscriptionFiltersPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeSubscriptionFiltersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeSubscriptionFilters.html#CloudWatchLogs.Paginator.DescribeSubscriptionFilters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describesubscriptionfilterspaginator)
        """

class FilterLogEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/FilterLogEvents.html#CloudWatchLogs.Paginator.FilterLogEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#filterlogeventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[FilterLogEventsRequestFilterLogEventsPaginateTypeDef]
    ) -> AsyncIterator[FilterLogEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/FilterLogEvents.html#CloudWatchLogs.Paginator.FilterLogEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#filterlogeventspaginator)
        """

class ListAnomaliesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/ListAnomalies.html#CloudWatchLogs.Paginator.ListAnomalies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#listanomaliespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAnomaliesRequestListAnomaliesPaginateTypeDef]
    ) -> AsyncIterator[ListAnomaliesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/ListAnomalies.html#CloudWatchLogs.Paginator.ListAnomalies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#listanomaliespaginator)
        """

class ListLogAnomalyDetectorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/ListLogAnomalyDetectors.html#CloudWatchLogs.Paginator.ListLogAnomalyDetectors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#listloganomalydetectorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLogAnomalyDetectorsRequestListLogAnomalyDetectorsPaginateTypeDef]
    ) -> AsyncIterator[ListLogAnomalyDetectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/ListLogAnomalyDetectors.html#CloudWatchLogs.Paginator.ListLogAnomalyDetectors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#listloganomalydetectorspaginator)
        """
