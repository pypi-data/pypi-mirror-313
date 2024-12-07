"""
Type annotations for devops-guru service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_devops_guru.client import DevOpsGuruClient
    from types_aiobotocore_devops_guru.paginator import (
        DescribeOrganizationResourceCollectionHealthPaginator,
        DescribeResourceCollectionHealthPaginator,
        GetCostEstimationPaginator,
        GetResourceCollectionPaginator,
        ListAnomaliesForInsightPaginator,
        ListAnomalousLogGroupsPaginator,
        ListEventsPaginator,
        ListInsightsPaginator,
        ListMonitoredResourcesPaginator,
        ListNotificationChannelsPaginator,
        ListOrganizationInsightsPaginator,
        ListRecommendationsPaginator,
        SearchInsightsPaginator,
        SearchOrganizationInsightsPaginator,
    )

    session = get_session()
    with session.create_client("devops-guru") as client:
        client: DevOpsGuruClient

        describe_organization_resource_collection_health_paginator: DescribeOrganizationResourceCollectionHealthPaginator = client.get_paginator("describe_organization_resource_collection_health")
        describe_resource_collection_health_paginator: DescribeResourceCollectionHealthPaginator = client.get_paginator("describe_resource_collection_health")
        get_cost_estimation_paginator: GetCostEstimationPaginator = client.get_paginator("get_cost_estimation")
        get_resource_collection_paginator: GetResourceCollectionPaginator = client.get_paginator("get_resource_collection")
        list_anomalies_for_insight_paginator: ListAnomaliesForInsightPaginator = client.get_paginator("list_anomalies_for_insight")
        list_anomalous_log_groups_paginator: ListAnomalousLogGroupsPaginator = client.get_paginator("list_anomalous_log_groups")
        list_events_paginator: ListEventsPaginator = client.get_paginator("list_events")
        list_insights_paginator: ListInsightsPaginator = client.get_paginator("list_insights")
        list_monitored_resources_paginator: ListMonitoredResourcesPaginator = client.get_paginator("list_monitored_resources")
        list_notification_channels_paginator: ListNotificationChannelsPaginator = client.get_paginator("list_notification_channels")
        list_organization_insights_paginator: ListOrganizationInsightsPaginator = client.get_paginator("list_organization_insights")
        list_recommendations_paginator: ListRecommendationsPaginator = client.get_paginator("list_recommendations")
        search_insights_paginator: SearchInsightsPaginator = client.get_paginator("search_insights")
        search_organization_insights_paginator: SearchOrganizationInsightsPaginator = client.get_paginator("search_organization_insights")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeOrganizationResourceCollectionHealthRequestDescribeOrganizationResourceCollectionHealthPaginateTypeDef,
    DescribeOrganizationResourceCollectionHealthResponseTypeDef,
    DescribeResourceCollectionHealthRequestDescribeResourceCollectionHealthPaginateTypeDef,
    DescribeResourceCollectionHealthResponseTypeDef,
    GetCostEstimationRequestGetCostEstimationPaginateTypeDef,
    GetCostEstimationResponseTypeDef,
    GetResourceCollectionRequestGetResourceCollectionPaginateTypeDef,
    GetResourceCollectionResponseTypeDef,
    ListAnomaliesForInsightRequestListAnomaliesForInsightPaginateTypeDef,
    ListAnomaliesForInsightResponseTypeDef,
    ListAnomalousLogGroupsRequestListAnomalousLogGroupsPaginateTypeDef,
    ListAnomalousLogGroupsResponseTypeDef,
    ListEventsRequestListEventsPaginateTypeDef,
    ListEventsResponseTypeDef,
    ListInsightsRequestListInsightsPaginateTypeDef,
    ListInsightsResponseTypeDef,
    ListMonitoredResourcesRequestListMonitoredResourcesPaginateTypeDef,
    ListMonitoredResourcesResponseTypeDef,
    ListNotificationChannelsRequestListNotificationChannelsPaginateTypeDef,
    ListNotificationChannelsResponseTypeDef,
    ListOrganizationInsightsRequestListOrganizationInsightsPaginateTypeDef,
    ListOrganizationInsightsResponseTypeDef,
    ListRecommendationsRequestListRecommendationsPaginateTypeDef,
    ListRecommendationsResponseTypeDef,
    SearchInsightsRequestSearchInsightsPaginateTypeDef,
    SearchInsightsResponseTypeDef,
    SearchOrganizationInsightsRequestSearchOrganizationInsightsPaginateTypeDef,
    SearchOrganizationInsightsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeOrganizationResourceCollectionHealthPaginator",
    "DescribeResourceCollectionHealthPaginator",
    "GetCostEstimationPaginator",
    "GetResourceCollectionPaginator",
    "ListAnomaliesForInsightPaginator",
    "ListAnomalousLogGroupsPaginator",
    "ListEventsPaginator",
    "ListInsightsPaginator",
    "ListMonitoredResourcesPaginator",
    "ListNotificationChannelsPaginator",
    "ListOrganizationInsightsPaginator",
    "ListRecommendationsPaginator",
    "SearchInsightsPaginator",
    "SearchOrganizationInsightsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeOrganizationResourceCollectionHealthPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/DescribeOrganizationResourceCollectionHealth.html#DevOpsGuru.Paginator.DescribeOrganizationResourceCollectionHealth)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#describeorganizationresourcecollectionhealthpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeOrganizationResourceCollectionHealthRequestDescribeOrganizationResourceCollectionHealthPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeOrganizationResourceCollectionHealthResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/DescribeOrganizationResourceCollectionHealth.html#DevOpsGuru.Paginator.DescribeOrganizationResourceCollectionHealth.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#describeorganizationresourcecollectionhealthpaginator)
        """

class DescribeResourceCollectionHealthPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/DescribeResourceCollectionHealth.html#DevOpsGuru.Paginator.DescribeResourceCollectionHealth)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#describeresourcecollectionhealthpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeResourceCollectionHealthRequestDescribeResourceCollectionHealthPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeResourceCollectionHealthResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/DescribeResourceCollectionHealth.html#DevOpsGuru.Paginator.DescribeResourceCollectionHealth.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#describeresourcecollectionhealthpaginator)
        """

class GetCostEstimationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/GetCostEstimation.html#DevOpsGuru.Paginator.GetCostEstimation)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#getcostestimationpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetCostEstimationRequestGetCostEstimationPaginateTypeDef]
    ) -> AsyncIterator[GetCostEstimationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/GetCostEstimation.html#DevOpsGuru.Paginator.GetCostEstimation.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#getcostestimationpaginator)
        """

class GetResourceCollectionPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/GetResourceCollection.html#DevOpsGuru.Paginator.GetResourceCollection)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#getresourcecollectionpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetResourceCollectionRequestGetResourceCollectionPaginateTypeDef]
    ) -> AsyncIterator[GetResourceCollectionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/GetResourceCollection.html#DevOpsGuru.Paginator.GetResourceCollection.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#getresourcecollectionpaginator)
        """

class ListAnomaliesForInsightPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListAnomaliesForInsight.html#DevOpsGuru.Paginator.ListAnomaliesForInsight)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listanomaliesforinsightpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAnomaliesForInsightRequestListAnomaliesForInsightPaginateTypeDef]
    ) -> AsyncIterator[ListAnomaliesForInsightResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListAnomaliesForInsight.html#DevOpsGuru.Paginator.ListAnomaliesForInsight.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listanomaliesforinsightpaginator)
        """

class ListAnomalousLogGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListAnomalousLogGroups.html#DevOpsGuru.Paginator.ListAnomalousLogGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listanomalousloggroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAnomalousLogGroupsRequestListAnomalousLogGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListAnomalousLogGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListAnomalousLogGroups.html#DevOpsGuru.Paginator.ListAnomalousLogGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listanomalousloggroupspaginator)
        """

class ListEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListEvents.html#DevOpsGuru.Paginator.ListEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listeventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEventsRequestListEventsPaginateTypeDef]
    ) -> AsyncIterator[ListEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListEvents.html#DevOpsGuru.Paginator.ListEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listeventspaginator)
        """

class ListInsightsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListInsights.html#DevOpsGuru.Paginator.ListInsights)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listinsightspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInsightsRequestListInsightsPaginateTypeDef]
    ) -> AsyncIterator[ListInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListInsights.html#DevOpsGuru.Paginator.ListInsights.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listinsightspaginator)
        """

class ListMonitoredResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListMonitoredResources.html#DevOpsGuru.Paginator.ListMonitoredResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listmonitoredresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMonitoredResourcesRequestListMonitoredResourcesPaginateTypeDef]
    ) -> AsyncIterator[ListMonitoredResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListMonitoredResources.html#DevOpsGuru.Paginator.ListMonitoredResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listmonitoredresourcespaginator)
        """

class ListNotificationChannelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListNotificationChannels.html#DevOpsGuru.Paginator.ListNotificationChannels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listnotificationchannelspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListNotificationChannelsRequestListNotificationChannelsPaginateTypeDef],
    ) -> AsyncIterator[ListNotificationChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListNotificationChannels.html#DevOpsGuru.Paginator.ListNotificationChannels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listnotificationchannelspaginator)
        """

class ListOrganizationInsightsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListOrganizationInsights.html#DevOpsGuru.Paginator.ListOrganizationInsights)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listorganizationinsightspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListOrganizationInsightsRequestListOrganizationInsightsPaginateTypeDef],
    ) -> AsyncIterator[ListOrganizationInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListOrganizationInsights.html#DevOpsGuru.Paginator.ListOrganizationInsights.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listorganizationinsightspaginator)
        """

class ListRecommendationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListRecommendations.html#DevOpsGuru.Paginator.ListRecommendations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listrecommendationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRecommendationsRequestListRecommendationsPaginateTypeDef]
    ) -> AsyncIterator[ListRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListRecommendations.html#DevOpsGuru.Paginator.ListRecommendations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listrecommendationspaginator)
        """

class SearchInsightsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/SearchInsights.html#DevOpsGuru.Paginator.SearchInsights)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#searchinsightspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchInsightsRequestSearchInsightsPaginateTypeDef]
    ) -> AsyncIterator[SearchInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/SearchInsights.html#DevOpsGuru.Paginator.SearchInsights.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#searchinsightspaginator)
        """

class SearchOrganizationInsightsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/SearchOrganizationInsights.html#DevOpsGuru.Paginator.SearchOrganizationInsights)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#searchorganizationinsightspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            SearchOrganizationInsightsRequestSearchOrganizationInsightsPaginateTypeDef
        ],
    ) -> AsyncIterator[SearchOrganizationInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/SearchOrganizationInsights.html#DevOpsGuru.Paginator.SearchOrganizationInsights.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#searchorganizationinsightspaginator)
        """
