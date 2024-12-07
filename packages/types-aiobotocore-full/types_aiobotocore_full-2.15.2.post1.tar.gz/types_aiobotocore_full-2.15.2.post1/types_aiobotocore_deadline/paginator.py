"""
Type annotations for deadline service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_deadline.client import DeadlineCloudClient
    from types_aiobotocore_deadline.paginator import (
        GetSessionsStatisticsAggregationPaginator,
        ListAvailableMeteredProductsPaginator,
        ListBudgetsPaginator,
        ListFarmMembersPaginator,
        ListFarmsPaginator,
        ListFleetMembersPaginator,
        ListFleetsPaginator,
        ListJobMembersPaginator,
        ListJobParameterDefinitionsPaginator,
        ListJobsPaginator,
        ListLicenseEndpointsPaginator,
        ListMeteredProductsPaginator,
        ListMonitorsPaginator,
        ListQueueEnvironmentsPaginator,
        ListQueueFleetAssociationsPaginator,
        ListQueueMembersPaginator,
        ListQueuesPaginator,
        ListSessionActionsPaginator,
        ListSessionsForWorkerPaginator,
        ListSessionsPaginator,
        ListStepConsumersPaginator,
        ListStepDependenciesPaginator,
        ListStepsPaginator,
        ListStorageProfilesForQueuePaginator,
        ListStorageProfilesPaginator,
        ListTasksPaginator,
        ListWorkersPaginator,
    )

    session = get_session()
    with session.create_client("deadline") as client:
        client: DeadlineCloudClient

        get_sessions_statistics_aggregation_paginator: GetSessionsStatisticsAggregationPaginator = client.get_paginator("get_sessions_statistics_aggregation")
        list_available_metered_products_paginator: ListAvailableMeteredProductsPaginator = client.get_paginator("list_available_metered_products")
        list_budgets_paginator: ListBudgetsPaginator = client.get_paginator("list_budgets")
        list_farm_members_paginator: ListFarmMembersPaginator = client.get_paginator("list_farm_members")
        list_farms_paginator: ListFarmsPaginator = client.get_paginator("list_farms")
        list_fleet_members_paginator: ListFleetMembersPaginator = client.get_paginator("list_fleet_members")
        list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
        list_job_members_paginator: ListJobMembersPaginator = client.get_paginator("list_job_members")
        list_job_parameter_definitions_paginator: ListJobParameterDefinitionsPaginator = client.get_paginator("list_job_parameter_definitions")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_license_endpoints_paginator: ListLicenseEndpointsPaginator = client.get_paginator("list_license_endpoints")
        list_metered_products_paginator: ListMeteredProductsPaginator = client.get_paginator("list_metered_products")
        list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
        list_queue_environments_paginator: ListQueueEnvironmentsPaginator = client.get_paginator("list_queue_environments")
        list_queue_fleet_associations_paginator: ListQueueFleetAssociationsPaginator = client.get_paginator("list_queue_fleet_associations")
        list_queue_members_paginator: ListQueueMembersPaginator = client.get_paginator("list_queue_members")
        list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
        list_session_actions_paginator: ListSessionActionsPaginator = client.get_paginator("list_session_actions")
        list_sessions_for_worker_paginator: ListSessionsForWorkerPaginator = client.get_paginator("list_sessions_for_worker")
        list_sessions_paginator: ListSessionsPaginator = client.get_paginator("list_sessions")
        list_step_consumers_paginator: ListStepConsumersPaginator = client.get_paginator("list_step_consumers")
        list_step_dependencies_paginator: ListStepDependenciesPaginator = client.get_paginator("list_step_dependencies")
        list_steps_paginator: ListStepsPaginator = client.get_paginator("list_steps")
        list_storage_profiles_for_queue_paginator: ListStorageProfilesForQueuePaginator = client.get_paginator("list_storage_profiles_for_queue")
        list_storage_profiles_paginator: ListStorageProfilesPaginator = client.get_paginator("list_storage_profiles")
        list_tasks_paginator: ListTasksPaginator = client.get_paginator("list_tasks")
        list_workers_paginator: ListWorkersPaginator = client.get_paginator("list_workers")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetSessionsStatisticsAggregationRequestGetSessionsStatisticsAggregationPaginateTypeDef,
    GetSessionsStatisticsAggregationResponseTypeDef,
    ListAvailableMeteredProductsRequestListAvailableMeteredProductsPaginateTypeDef,
    ListAvailableMeteredProductsResponseTypeDef,
    ListBudgetsRequestListBudgetsPaginateTypeDef,
    ListBudgetsResponseTypeDef,
    ListFarmMembersRequestListFarmMembersPaginateTypeDef,
    ListFarmMembersResponseTypeDef,
    ListFarmsRequestListFarmsPaginateTypeDef,
    ListFarmsResponseTypeDef,
    ListFleetMembersRequestListFleetMembersPaginateTypeDef,
    ListFleetMembersResponseTypeDef,
    ListFleetsRequestListFleetsPaginateTypeDef,
    ListFleetsResponseTypeDef,
    ListJobMembersRequestListJobMembersPaginateTypeDef,
    ListJobMembersResponseTypeDef,
    ListJobParameterDefinitionsRequestListJobParameterDefinitionsPaginateTypeDef,
    ListJobParameterDefinitionsResponseTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListLicenseEndpointsRequestListLicenseEndpointsPaginateTypeDef,
    ListLicenseEndpointsResponseTypeDef,
    ListMeteredProductsRequestListMeteredProductsPaginateTypeDef,
    ListMeteredProductsResponseTypeDef,
    ListMonitorsRequestListMonitorsPaginateTypeDef,
    ListMonitorsResponseTypeDef,
    ListQueueEnvironmentsRequestListQueueEnvironmentsPaginateTypeDef,
    ListQueueEnvironmentsResponseTypeDef,
    ListQueueFleetAssociationsRequestListQueueFleetAssociationsPaginateTypeDef,
    ListQueueFleetAssociationsResponseTypeDef,
    ListQueueMembersRequestListQueueMembersPaginateTypeDef,
    ListQueueMembersResponseTypeDef,
    ListQueuesRequestListQueuesPaginateTypeDef,
    ListQueuesResponseTypeDef,
    ListSessionActionsRequestListSessionActionsPaginateTypeDef,
    ListSessionActionsResponseTypeDef,
    ListSessionsForWorkerRequestListSessionsForWorkerPaginateTypeDef,
    ListSessionsForWorkerResponseTypeDef,
    ListSessionsRequestListSessionsPaginateTypeDef,
    ListSessionsResponseTypeDef,
    ListStepConsumersRequestListStepConsumersPaginateTypeDef,
    ListStepConsumersResponseTypeDef,
    ListStepDependenciesRequestListStepDependenciesPaginateTypeDef,
    ListStepDependenciesResponseTypeDef,
    ListStepsRequestListStepsPaginateTypeDef,
    ListStepsResponseTypeDef,
    ListStorageProfilesForQueueRequestListStorageProfilesForQueuePaginateTypeDef,
    ListStorageProfilesForQueueResponseTypeDef,
    ListStorageProfilesRequestListStorageProfilesPaginateTypeDef,
    ListStorageProfilesResponseTypeDef,
    ListTasksRequestListTasksPaginateTypeDef,
    ListTasksResponseTypeDef,
    ListWorkersRequestListWorkersPaginateTypeDef,
    ListWorkersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetSessionsStatisticsAggregationPaginator",
    "ListAvailableMeteredProductsPaginator",
    "ListBudgetsPaginator",
    "ListFarmMembersPaginator",
    "ListFarmsPaginator",
    "ListFleetMembersPaginator",
    "ListFleetsPaginator",
    "ListJobMembersPaginator",
    "ListJobParameterDefinitionsPaginator",
    "ListJobsPaginator",
    "ListLicenseEndpointsPaginator",
    "ListMeteredProductsPaginator",
    "ListMonitorsPaginator",
    "ListQueueEnvironmentsPaginator",
    "ListQueueFleetAssociationsPaginator",
    "ListQueueMembersPaginator",
    "ListQueuesPaginator",
    "ListSessionActionsPaginator",
    "ListSessionsForWorkerPaginator",
    "ListSessionsPaginator",
    "ListStepConsumersPaginator",
    "ListStepDependenciesPaginator",
    "ListStepsPaginator",
    "ListStorageProfilesForQueuePaginator",
    "ListStorageProfilesPaginator",
    "ListTasksPaginator",
    "ListWorkersPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetSessionsStatisticsAggregationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/GetSessionsStatisticsAggregation.html#DeadlineCloud.Paginator.GetSessionsStatisticsAggregation)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#getsessionsstatisticsaggregationpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetSessionsStatisticsAggregationRequestGetSessionsStatisticsAggregationPaginateTypeDef
        ],
    ) -> AsyncIterator[GetSessionsStatisticsAggregationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/GetSessionsStatisticsAggregation.html#DeadlineCloud.Paginator.GetSessionsStatisticsAggregation.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#getsessionsstatisticsaggregationpaginator)
        """


class ListAvailableMeteredProductsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListAvailableMeteredProducts.html#DeadlineCloud.Paginator.ListAvailableMeteredProducts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listavailablemeteredproductspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListAvailableMeteredProductsRequestListAvailableMeteredProductsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListAvailableMeteredProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListAvailableMeteredProducts.html#DeadlineCloud.Paginator.ListAvailableMeteredProducts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listavailablemeteredproductspaginator)
        """


class ListBudgetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListBudgets.html#DeadlineCloud.Paginator.ListBudgets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listbudgetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBudgetsRequestListBudgetsPaginateTypeDef]
    ) -> AsyncIterator[ListBudgetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListBudgets.html#DeadlineCloud.Paginator.ListBudgets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listbudgetspaginator)
        """


class ListFarmMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFarmMembers.html#DeadlineCloud.Paginator.ListFarmMembers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfarmmemberspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFarmMembersRequestListFarmMembersPaginateTypeDef]
    ) -> AsyncIterator[ListFarmMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFarmMembers.html#DeadlineCloud.Paginator.ListFarmMembers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfarmmemberspaginator)
        """


class ListFarmsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFarms.html#DeadlineCloud.Paginator.ListFarms)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfarmspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFarmsRequestListFarmsPaginateTypeDef]
    ) -> AsyncIterator[ListFarmsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFarms.html#DeadlineCloud.Paginator.ListFarms.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfarmspaginator)
        """


class ListFleetMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFleetMembers.html#DeadlineCloud.Paginator.ListFleetMembers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfleetmemberspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFleetMembersRequestListFleetMembersPaginateTypeDef]
    ) -> AsyncIterator[ListFleetMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFleetMembers.html#DeadlineCloud.Paginator.ListFleetMembers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfleetmemberspaginator)
        """


class ListFleetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFleets.html#DeadlineCloud.Paginator.ListFleets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfleetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFleetsRequestListFleetsPaginateTypeDef]
    ) -> AsyncIterator[ListFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFleets.html#DeadlineCloud.Paginator.ListFleets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfleetspaginator)
        """


class ListJobMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobMembers.html#DeadlineCloud.Paginator.ListJobMembers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listjobmemberspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListJobMembersRequestListJobMembersPaginateTypeDef]
    ) -> AsyncIterator[ListJobMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobMembers.html#DeadlineCloud.Paginator.ListJobMembers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listjobmemberspaginator)
        """


class ListJobParameterDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobParameterDefinitions.html#DeadlineCloud.Paginator.ListJobParameterDefinitions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listjobparameterdefinitionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListJobParameterDefinitionsRequestListJobParameterDefinitionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListJobParameterDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobParameterDefinitions.html#DeadlineCloud.Paginator.ListJobParameterDefinitions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listjobparameterdefinitionspaginator)
        """


class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobs.html#DeadlineCloud.Paginator.ListJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> AsyncIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobs.html#DeadlineCloud.Paginator.ListJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listjobspaginator)
        """


class ListLicenseEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListLicenseEndpoints.html#DeadlineCloud.Paginator.ListLicenseEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listlicenseendpointspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListLicenseEndpointsRequestListLicenseEndpointsPaginateTypeDef]
    ) -> AsyncIterator[ListLicenseEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListLicenseEndpoints.html#DeadlineCloud.Paginator.ListLicenseEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listlicenseendpointspaginator)
        """


class ListMeteredProductsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListMeteredProducts.html#DeadlineCloud.Paginator.ListMeteredProducts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listmeteredproductspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMeteredProductsRequestListMeteredProductsPaginateTypeDef]
    ) -> AsyncIterator[ListMeteredProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListMeteredProducts.html#DeadlineCloud.Paginator.ListMeteredProducts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listmeteredproductspaginator)
        """


class ListMonitorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListMonitors.html#DeadlineCloud.Paginator.ListMonitors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listmonitorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMonitorsRequestListMonitorsPaginateTypeDef]
    ) -> AsyncIterator[ListMonitorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListMonitors.html#DeadlineCloud.Paginator.ListMonitors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listmonitorspaginator)
        """


class ListQueueEnvironmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueEnvironments.html#DeadlineCloud.Paginator.ListQueueEnvironments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueueenvironmentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListQueueEnvironmentsRequestListQueueEnvironmentsPaginateTypeDef]
    ) -> AsyncIterator[ListQueueEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueEnvironments.html#DeadlineCloud.Paginator.ListQueueEnvironments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueueenvironmentspaginator)
        """


class ListQueueFleetAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueFleetAssociations.html#DeadlineCloud.Paginator.ListQueueFleetAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuefleetassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListQueueFleetAssociationsRequestListQueueFleetAssociationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListQueueFleetAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueFleetAssociations.html#DeadlineCloud.Paginator.ListQueueFleetAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuefleetassociationspaginator)
        """


class ListQueueMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueMembers.html#DeadlineCloud.Paginator.ListQueueMembers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuememberspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListQueueMembersRequestListQueueMembersPaginateTypeDef]
    ) -> AsyncIterator[ListQueueMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueMembers.html#DeadlineCloud.Paginator.ListQueueMembers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuememberspaginator)
        """


class ListQueuesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueues.html#DeadlineCloud.Paginator.ListQueues)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListQueuesRequestListQueuesPaginateTypeDef]
    ) -> AsyncIterator[ListQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueues.html#DeadlineCloud.Paginator.ListQueues.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuespaginator)
        """


class ListSessionActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessionActions.html#DeadlineCloud.Paginator.ListSessionActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionactionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSessionActionsRequestListSessionActionsPaginateTypeDef]
    ) -> AsyncIterator[ListSessionActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessionActions.html#DeadlineCloud.Paginator.ListSessionActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionactionspaginator)
        """


class ListSessionsForWorkerPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessionsForWorker.html#DeadlineCloud.Paginator.ListSessionsForWorker)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionsforworkerpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSessionsForWorkerRequestListSessionsForWorkerPaginateTypeDef]
    ) -> AsyncIterator[ListSessionsForWorkerResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessionsForWorker.html#DeadlineCloud.Paginator.ListSessionsForWorker.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionsforworkerpaginator)
        """


class ListSessionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessions.html#DeadlineCloud.Paginator.ListSessions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSessionsRequestListSessionsPaginateTypeDef]
    ) -> AsyncIterator[ListSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessions.html#DeadlineCloud.Paginator.ListSessions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionspaginator)
        """


class ListStepConsumersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStepConsumers.html#DeadlineCloud.Paginator.ListStepConsumers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepconsumerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStepConsumersRequestListStepConsumersPaginateTypeDef]
    ) -> AsyncIterator[ListStepConsumersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStepConsumers.html#DeadlineCloud.Paginator.ListStepConsumers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepconsumerspaginator)
        """


class ListStepDependenciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStepDependencies.html#DeadlineCloud.Paginator.ListStepDependencies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepdependenciespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStepDependenciesRequestListStepDependenciesPaginateTypeDef]
    ) -> AsyncIterator[ListStepDependenciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStepDependencies.html#DeadlineCloud.Paginator.ListStepDependencies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepdependenciespaginator)
        """


class ListStepsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSteps.html#DeadlineCloud.Paginator.ListSteps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStepsRequestListStepsPaginateTypeDef]
    ) -> AsyncIterator[ListStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSteps.html#DeadlineCloud.Paginator.ListSteps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepspaginator)
        """


class ListStorageProfilesForQueuePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStorageProfilesForQueue.html#DeadlineCloud.Paginator.ListStorageProfilesForQueue)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststorageprofilesforqueuepaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListStorageProfilesForQueueRequestListStorageProfilesForQueuePaginateTypeDef
        ],
    ) -> AsyncIterator[ListStorageProfilesForQueueResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStorageProfilesForQueue.html#DeadlineCloud.Paginator.ListStorageProfilesForQueue.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststorageprofilesforqueuepaginator)
        """


class ListStorageProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStorageProfiles.html#DeadlineCloud.Paginator.ListStorageProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststorageprofilespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStorageProfilesRequestListStorageProfilesPaginateTypeDef]
    ) -> AsyncIterator[ListStorageProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStorageProfiles.html#DeadlineCloud.Paginator.ListStorageProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststorageprofilespaginator)
        """


class ListTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListTasks.html#DeadlineCloud.Paginator.ListTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listtaskspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTasksRequestListTasksPaginateTypeDef]
    ) -> AsyncIterator[ListTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListTasks.html#DeadlineCloud.Paginator.ListTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listtaskspaginator)
        """


class ListWorkersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListWorkers.html#DeadlineCloud.Paginator.ListWorkers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listworkerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorkersRequestListWorkersPaginateTypeDef]
    ) -> AsyncIterator[ListWorkersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListWorkers.html#DeadlineCloud.Paginator.ListWorkers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listworkerspaginator)
        """
