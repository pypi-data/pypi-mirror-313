"""
Type annotations for datazone service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_datazone.client import DataZoneClient
    from types_aiobotocore_datazone.paginator import (
        ListAssetFiltersPaginator,
        ListAssetRevisionsPaginator,
        ListDataProductRevisionsPaginator,
        ListDataSourceRunActivitiesPaginator,
        ListDataSourceRunsPaginator,
        ListDataSourcesPaginator,
        ListDomainUnitsForParentPaginator,
        ListDomainsPaginator,
        ListEntityOwnersPaginator,
        ListEnvironmentActionsPaginator,
        ListEnvironmentBlueprintConfigurationsPaginator,
        ListEnvironmentBlueprintsPaginator,
        ListEnvironmentProfilesPaginator,
        ListEnvironmentsPaginator,
        ListLineageNodeHistoryPaginator,
        ListMetadataGenerationRunsPaginator,
        ListNotificationsPaginator,
        ListPolicyGrantsPaginator,
        ListProjectMembershipsPaginator,
        ListProjectsPaginator,
        ListSubscriptionGrantsPaginator,
        ListSubscriptionRequestsPaginator,
        ListSubscriptionTargetsPaginator,
        ListSubscriptionsPaginator,
        ListTimeSeriesDataPointsPaginator,
        SearchGroupProfilesPaginator,
        SearchListingsPaginator,
        SearchPaginator,
        SearchTypesPaginator,
        SearchUserProfilesPaginator,
    )

    session = get_session()
    with session.create_client("datazone") as client:
        client: DataZoneClient

        list_asset_filters_paginator: ListAssetFiltersPaginator = client.get_paginator("list_asset_filters")
        list_asset_revisions_paginator: ListAssetRevisionsPaginator = client.get_paginator("list_asset_revisions")
        list_data_product_revisions_paginator: ListDataProductRevisionsPaginator = client.get_paginator("list_data_product_revisions")
        list_data_source_run_activities_paginator: ListDataSourceRunActivitiesPaginator = client.get_paginator("list_data_source_run_activities")
        list_data_source_runs_paginator: ListDataSourceRunsPaginator = client.get_paginator("list_data_source_runs")
        list_data_sources_paginator: ListDataSourcesPaginator = client.get_paginator("list_data_sources")
        list_domain_units_for_parent_paginator: ListDomainUnitsForParentPaginator = client.get_paginator("list_domain_units_for_parent")
        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_entity_owners_paginator: ListEntityOwnersPaginator = client.get_paginator("list_entity_owners")
        list_environment_actions_paginator: ListEnvironmentActionsPaginator = client.get_paginator("list_environment_actions")
        list_environment_blueprint_configurations_paginator: ListEnvironmentBlueprintConfigurationsPaginator = client.get_paginator("list_environment_blueprint_configurations")
        list_environment_blueprints_paginator: ListEnvironmentBlueprintsPaginator = client.get_paginator("list_environment_blueprints")
        list_environment_profiles_paginator: ListEnvironmentProfilesPaginator = client.get_paginator("list_environment_profiles")
        list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
        list_lineage_node_history_paginator: ListLineageNodeHistoryPaginator = client.get_paginator("list_lineage_node_history")
        list_metadata_generation_runs_paginator: ListMetadataGenerationRunsPaginator = client.get_paginator("list_metadata_generation_runs")
        list_notifications_paginator: ListNotificationsPaginator = client.get_paginator("list_notifications")
        list_policy_grants_paginator: ListPolicyGrantsPaginator = client.get_paginator("list_policy_grants")
        list_project_memberships_paginator: ListProjectMembershipsPaginator = client.get_paginator("list_project_memberships")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
        list_subscription_grants_paginator: ListSubscriptionGrantsPaginator = client.get_paginator("list_subscription_grants")
        list_subscription_requests_paginator: ListSubscriptionRequestsPaginator = client.get_paginator("list_subscription_requests")
        list_subscription_targets_paginator: ListSubscriptionTargetsPaginator = client.get_paginator("list_subscription_targets")
        list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
        list_time_series_data_points_paginator: ListTimeSeriesDataPointsPaginator = client.get_paginator("list_time_series_data_points")
        search_group_profiles_paginator: SearchGroupProfilesPaginator = client.get_paginator("search_group_profiles")
        search_listings_paginator: SearchListingsPaginator = client.get_paginator("search_listings")
        search_paginator: SearchPaginator = client.get_paginator("search")
        search_types_paginator: SearchTypesPaginator = client.get_paginator("search_types")
        search_user_profiles_paginator: SearchUserProfilesPaginator = client.get_paginator("search_user_profiles")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAssetFiltersInputListAssetFiltersPaginateTypeDef,
    ListAssetFiltersOutputTypeDef,
    ListAssetRevisionsInputListAssetRevisionsPaginateTypeDef,
    ListAssetRevisionsOutputTypeDef,
    ListDataProductRevisionsInputListDataProductRevisionsPaginateTypeDef,
    ListDataProductRevisionsOutputTypeDef,
    ListDataSourceRunActivitiesInputListDataSourceRunActivitiesPaginateTypeDef,
    ListDataSourceRunActivitiesOutputTypeDef,
    ListDataSourceRunsInputListDataSourceRunsPaginateTypeDef,
    ListDataSourceRunsOutputTypeDef,
    ListDataSourcesInputListDataSourcesPaginateTypeDef,
    ListDataSourcesOutputTypeDef,
    ListDomainsInputListDomainsPaginateTypeDef,
    ListDomainsOutputTypeDef,
    ListDomainUnitsForParentInputListDomainUnitsForParentPaginateTypeDef,
    ListDomainUnitsForParentOutputTypeDef,
    ListEntityOwnersInputListEntityOwnersPaginateTypeDef,
    ListEntityOwnersOutputTypeDef,
    ListEnvironmentActionsInputListEnvironmentActionsPaginateTypeDef,
    ListEnvironmentActionsOutputTypeDef,
    ListEnvironmentBlueprintConfigurationsInputListEnvironmentBlueprintConfigurationsPaginateTypeDef,
    ListEnvironmentBlueprintConfigurationsOutputTypeDef,
    ListEnvironmentBlueprintsInputListEnvironmentBlueprintsPaginateTypeDef,
    ListEnvironmentBlueprintsOutputTypeDef,
    ListEnvironmentProfilesInputListEnvironmentProfilesPaginateTypeDef,
    ListEnvironmentProfilesOutputTypeDef,
    ListEnvironmentsInputListEnvironmentsPaginateTypeDef,
    ListEnvironmentsOutputTypeDef,
    ListLineageNodeHistoryInputListLineageNodeHistoryPaginateTypeDef,
    ListLineageNodeHistoryOutputTypeDef,
    ListMetadataGenerationRunsInputListMetadataGenerationRunsPaginateTypeDef,
    ListMetadataGenerationRunsOutputTypeDef,
    ListNotificationsInputListNotificationsPaginateTypeDef,
    ListNotificationsOutputTypeDef,
    ListPolicyGrantsInputListPolicyGrantsPaginateTypeDef,
    ListPolicyGrantsOutputTypeDef,
    ListProjectMembershipsInputListProjectMembershipsPaginateTypeDef,
    ListProjectMembershipsOutputTypeDef,
    ListProjectsInputListProjectsPaginateTypeDef,
    ListProjectsOutputTypeDef,
    ListSubscriptionGrantsInputListSubscriptionGrantsPaginateTypeDef,
    ListSubscriptionGrantsOutputTypeDef,
    ListSubscriptionRequestsInputListSubscriptionRequestsPaginateTypeDef,
    ListSubscriptionRequestsOutputTypeDef,
    ListSubscriptionsInputListSubscriptionsPaginateTypeDef,
    ListSubscriptionsOutputTypeDef,
    ListSubscriptionTargetsInputListSubscriptionTargetsPaginateTypeDef,
    ListSubscriptionTargetsOutputTypeDef,
    ListTimeSeriesDataPointsInputListTimeSeriesDataPointsPaginateTypeDef,
    ListTimeSeriesDataPointsOutputTypeDef,
    SearchGroupProfilesInputSearchGroupProfilesPaginateTypeDef,
    SearchGroupProfilesOutputTypeDef,
    SearchInputSearchPaginateTypeDef,
    SearchListingsInputSearchListingsPaginateTypeDef,
    SearchListingsOutputTypeDef,
    SearchOutputTypeDef,
    SearchTypesInputSearchTypesPaginateTypeDef,
    SearchTypesOutputTypeDef,
    SearchUserProfilesInputSearchUserProfilesPaginateTypeDef,
    SearchUserProfilesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAssetFiltersPaginator",
    "ListAssetRevisionsPaginator",
    "ListDataProductRevisionsPaginator",
    "ListDataSourceRunActivitiesPaginator",
    "ListDataSourceRunsPaginator",
    "ListDataSourcesPaginator",
    "ListDomainUnitsForParentPaginator",
    "ListDomainsPaginator",
    "ListEntityOwnersPaginator",
    "ListEnvironmentActionsPaginator",
    "ListEnvironmentBlueprintConfigurationsPaginator",
    "ListEnvironmentBlueprintsPaginator",
    "ListEnvironmentProfilesPaginator",
    "ListEnvironmentsPaginator",
    "ListLineageNodeHistoryPaginator",
    "ListMetadataGenerationRunsPaginator",
    "ListNotificationsPaginator",
    "ListPolicyGrantsPaginator",
    "ListProjectMembershipsPaginator",
    "ListProjectsPaginator",
    "ListSubscriptionGrantsPaginator",
    "ListSubscriptionRequestsPaginator",
    "ListSubscriptionTargetsPaginator",
    "ListSubscriptionsPaginator",
    "ListTimeSeriesDataPointsPaginator",
    "SearchGroupProfilesPaginator",
    "SearchListingsPaginator",
    "SearchPaginator",
    "SearchTypesPaginator",
    "SearchUserProfilesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAssetFiltersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListAssetFilters.html#DataZone.Paginator.ListAssetFilters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listassetfilterspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAssetFiltersInputListAssetFiltersPaginateTypeDef]
    ) -> AsyncIterator[ListAssetFiltersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListAssetFilters.html#DataZone.Paginator.ListAssetFilters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listassetfilterspaginator)
        """


class ListAssetRevisionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListAssetRevisions.html#DataZone.Paginator.ListAssetRevisions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listassetrevisionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAssetRevisionsInputListAssetRevisionsPaginateTypeDef]
    ) -> AsyncIterator[ListAssetRevisionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListAssetRevisions.html#DataZone.Paginator.ListAssetRevisions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listassetrevisionspaginator)
        """


class ListDataProductRevisionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataProductRevisions.html#DataZone.Paginator.ListDataProductRevisions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdataproductrevisionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDataProductRevisionsInputListDataProductRevisionsPaginateTypeDef]
    ) -> AsyncIterator[ListDataProductRevisionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataProductRevisions.html#DataZone.Paginator.ListDataProductRevisions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdataproductrevisionspaginator)
        """


class ListDataSourceRunActivitiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSourceRunActivities.html#DataZone.Paginator.ListDataSourceRunActivities)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdatasourcerunactivitiespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListDataSourceRunActivitiesInputListDataSourceRunActivitiesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListDataSourceRunActivitiesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSourceRunActivities.html#DataZone.Paginator.ListDataSourceRunActivities.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdatasourcerunactivitiespaginator)
        """


class ListDataSourceRunsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSourceRuns.html#DataZone.Paginator.ListDataSourceRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdatasourcerunspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDataSourceRunsInputListDataSourceRunsPaginateTypeDef]
    ) -> AsyncIterator[ListDataSourceRunsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSourceRuns.html#DataZone.Paginator.ListDataSourceRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdatasourcerunspaginator)
        """


class ListDataSourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSources.html#DataZone.Paginator.ListDataSources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdatasourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDataSourcesInputListDataSourcesPaginateTypeDef]
    ) -> AsyncIterator[ListDataSourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSources.html#DataZone.Paginator.ListDataSources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdatasourcespaginator)
        """


class ListDomainUnitsForParentPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDomainUnitsForParent.html#DataZone.Paginator.ListDomainUnitsForParent)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdomainunitsforparentpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDomainUnitsForParentInputListDomainUnitsForParentPaginateTypeDef]
    ) -> AsyncIterator[ListDomainUnitsForParentOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDomainUnitsForParent.html#DataZone.Paginator.ListDomainUnitsForParent.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdomainunitsforparentpaginator)
        """


class ListDomainsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDomains.html#DataZone.Paginator.ListDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdomainspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDomainsInputListDomainsPaginateTypeDef]
    ) -> AsyncIterator[ListDomainsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDomains.html#DataZone.Paginator.ListDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdomainspaginator)
        """


class ListEntityOwnersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEntityOwners.html#DataZone.Paginator.ListEntityOwners)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listentityownerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEntityOwnersInputListEntityOwnersPaginateTypeDef]
    ) -> AsyncIterator[ListEntityOwnersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEntityOwners.html#DataZone.Paginator.ListEntityOwners.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listentityownerspaginator)
        """


class ListEnvironmentActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentActions.html#DataZone.Paginator.ListEnvironmentActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentactionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEnvironmentActionsInputListEnvironmentActionsPaginateTypeDef]
    ) -> AsyncIterator[ListEnvironmentActionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentActions.html#DataZone.Paginator.ListEnvironmentActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentactionspaginator)
        """


class ListEnvironmentBlueprintConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentBlueprintConfigurations.html#DataZone.Paginator.ListEnvironmentBlueprintConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentblueprintconfigurationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListEnvironmentBlueprintConfigurationsInputListEnvironmentBlueprintConfigurationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListEnvironmentBlueprintConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentBlueprintConfigurations.html#DataZone.Paginator.ListEnvironmentBlueprintConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentblueprintconfigurationspaginator)
        """


class ListEnvironmentBlueprintsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentBlueprints.html#DataZone.Paginator.ListEnvironmentBlueprints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentblueprintspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListEnvironmentBlueprintsInputListEnvironmentBlueprintsPaginateTypeDef],
    ) -> AsyncIterator[ListEnvironmentBlueprintsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentBlueprints.html#DataZone.Paginator.ListEnvironmentBlueprints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentblueprintspaginator)
        """


class ListEnvironmentProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentProfiles.html#DataZone.Paginator.ListEnvironmentProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentprofilespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEnvironmentProfilesInputListEnvironmentProfilesPaginateTypeDef]
    ) -> AsyncIterator[ListEnvironmentProfilesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentProfiles.html#DataZone.Paginator.ListEnvironmentProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentprofilespaginator)
        """


class ListEnvironmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironments.html#DataZone.Paginator.ListEnvironments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEnvironmentsInputListEnvironmentsPaginateTypeDef]
    ) -> AsyncIterator[ListEnvironmentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironments.html#DataZone.Paginator.ListEnvironments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentspaginator)
        """


class ListLineageNodeHistoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListLineageNodeHistory.html#DataZone.Paginator.ListLineageNodeHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listlineagenodehistorypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListLineageNodeHistoryInputListLineageNodeHistoryPaginateTypeDef]
    ) -> AsyncIterator[ListLineageNodeHistoryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListLineageNodeHistory.html#DataZone.Paginator.ListLineageNodeHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listlineagenodehistorypaginator)
        """


class ListMetadataGenerationRunsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListMetadataGenerationRuns.html#DataZone.Paginator.ListMetadataGenerationRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listmetadatagenerationrunspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListMetadataGenerationRunsInputListMetadataGenerationRunsPaginateTypeDef],
    ) -> AsyncIterator[ListMetadataGenerationRunsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListMetadataGenerationRuns.html#DataZone.Paginator.ListMetadataGenerationRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listmetadatagenerationrunspaginator)
        """


class ListNotificationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListNotifications.html#DataZone.Paginator.ListNotifications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listnotificationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListNotificationsInputListNotificationsPaginateTypeDef]
    ) -> AsyncIterator[ListNotificationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListNotifications.html#DataZone.Paginator.ListNotifications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listnotificationspaginator)
        """


class ListPolicyGrantsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListPolicyGrants.html#DataZone.Paginator.ListPolicyGrants)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listpolicygrantspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPolicyGrantsInputListPolicyGrantsPaginateTypeDef]
    ) -> AsyncIterator[ListPolicyGrantsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListPolicyGrants.html#DataZone.Paginator.ListPolicyGrants.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listpolicygrantspaginator)
        """


class ListProjectMembershipsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListProjectMemberships.html#DataZone.Paginator.ListProjectMemberships)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listprojectmembershipspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListProjectMembershipsInputListProjectMembershipsPaginateTypeDef]
    ) -> AsyncIterator[ListProjectMembershipsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListProjectMemberships.html#DataZone.Paginator.ListProjectMemberships.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listprojectmembershipspaginator)
        """


class ListProjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListProjects.html#DataZone.Paginator.ListProjects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listprojectspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListProjectsInputListProjectsPaginateTypeDef]
    ) -> AsyncIterator[ListProjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListProjects.html#DataZone.Paginator.ListProjects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listprojectspaginator)
        """


class ListSubscriptionGrantsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionGrants.html#DataZone.Paginator.ListSubscriptionGrants)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listsubscriptiongrantspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSubscriptionGrantsInputListSubscriptionGrantsPaginateTypeDef]
    ) -> AsyncIterator[ListSubscriptionGrantsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionGrants.html#DataZone.Paginator.ListSubscriptionGrants.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listsubscriptiongrantspaginator)
        """


class ListSubscriptionRequestsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionRequests.html#DataZone.Paginator.ListSubscriptionRequests)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listsubscriptionrequestspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSubscriptionRequestsInputListSubscriptionRequestsPaginateTypeDef]
    ) -> AsyncIterator[ListSubscriptionRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionRequests.html#DataZone.Paginator.ListSubscriptionRequests.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listsubscriptionrequestspaginator)
        """


class ListSubscriptionTargetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionTargets.html#DataZone.Paginator.ListSubscriptionTargets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listsubscriptiontargetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSubscriptionTargetsInputListSubscriptionTargetsPaginateTypeDef]
    ) -> AsyncIterator[ListSubscriptionTargetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionTargets.html#DataZone.Paginator.ListSubscriptionTargets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listsubscriptiontargetspaginator)
        """


class ListSubscriptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptions.html#DataZone.Paginator.ListSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listsubscriptionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSubscriptionsInputListSubscriptionsPaginateTypeDef]
    ) -> AsyncIterator[ListSubscriptionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptions.html#DataZone.Paginator.ListSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listsubscriptionspaginator)
        """


class ListTimeSeriesDataPointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListTimeSeriesDataPoints.html#DataZone.Paginator.ListTimeSeriesDataPoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listtimeseriesdatapointspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTimeSeriesDataPointsInputListTimeSeriesDataPointsPaginateTypeDef]
    ) -> AsyncIterator[ListTimeSeriesDataPointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListTimeSeriesDataPoints.html#DataZone.Paginator.ListTimeSeriesDataPoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listtimeseriesdatapointspaginator)
        """


class SearchGroupProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchGroupProfiles.html#DataZone.Paginator.SearchGroupProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchgroupprofilespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchGroupProfilesInputSearchGroupProfilesPaginateTypeDef]
    ) -> AsyncIterator[SearchGroupProfilesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchGroupProfiles.html#DataZone.Paginator.SearchGroupProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchgroupprofilespaginator)
        """


class SearchListingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchListings.html#DataZone.Paginator.SearchListings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchlistingspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchListingsInputSearchListingsPaginateTypeDef]
    ) -> AsyncIterator[SearchListingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchListings.html#DataZone.Paginator.SearchListings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchlistingspaginator)
        """


class SearchPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/Search.html#DataZone.Paginator.Search)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchInputSearchPaginateTypeDef]
    ) -> AsyncIterator[SearchOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/Search.html#DataZone.Paginator.Search.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchpaginator)
        """


class SearchTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchTypes.html#DataZone.Paginator.SearchTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchtypespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchTypesInputSearchTypesPaginateTypeDef]
    ) -> AsyncIterator[SearchTypesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchTypes.html#DataZone.Paginator.SearchTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchtypespaginator)
        """


class SearchUserProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchUserProfiles.html#DataZone.Paginator.SearchUserProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchuserprofilespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchUserProfilesInputSearchUserProfilesPaginateTypeDef]
    ) -> AsyncIterator[SearchUserProfilesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchUserProfiles.html#DataZone.Paginator.SearchUserProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchuserprofilespaginator)
        """
