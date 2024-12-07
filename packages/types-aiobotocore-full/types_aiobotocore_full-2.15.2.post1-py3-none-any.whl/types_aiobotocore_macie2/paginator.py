"""
Type annotations for macie2 service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_macie2.client import Macie2Client
    from types_aiobotocore_macie2.paginator import (
        DescribeBucketsPaginator,
        GetUsageStatisticsPaginator,
        ListAllowListsPaginator,
        ListAutomatedDiscoveryAccountsPaginator,
        ListClassificationJobsPaginator,
        ListClassificationScopesPaginator,
        ListCustomDataIdentifiersPaginator,
        ListFindingsFiltersPaginator,
        ListFindingsPaginator,
        ListInvitationsPaginator,
        ListManagedDataIdentifiersPaginator,
        ListMembersPaginator,
        ListOrganizationAdminAccountsPaginator,
        ListResourceProfileArtifactsPaginator,
        ListResourceProfileDetectionsPaginator,
        ListSensitivityInspectionTemplatesPaginator,
        SearchResourcesPaginator,
    )

    session = get_session()
    with session.create_client("macie2") as client:
        client: Macie2Client

        describe_buckets_paginator: DescribeBucketsPaginator = client.get_paginator("describe_buckets")
        get_usage_statistics_paginator: GetUsageStatisticsPaginator = client.get_paginator("get_usage_statistics")
        list_allow_lists_paginator: ListAllowListsPaginator = client.get_paginator("list_allow_lists")
        list_automated_discovery_accounts_paginator: ListAutomatedDiscoveryAccountsPaginator = client.get_paginator("list_automated_discovery_accounts")
        list_classification_jobs_paginator: ListClassificationJobsPaginator = client.get_paginator("list_classification_jobs")
        list_classification_scopes_paginator: ListClassificationScopesPaginator = client.get_paginator("list_classification_scopes")
        list_custom_data_identifiers_paginator: ListCustomDataIdentifiersPaginator = client.get_paginator("list_custom_data_identifiers")
        list_findings_filters_paginator: ListFindingsFiltersPaginator = client.get_paginator("list_findings_filters")
        list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
        list_invitations_paginator: ListInvitationsPaginator = client.get_paginator("list_invitations")
        list_managed_data_identifiers_paginator: ListManagedDataIdentifiersPaginator = client.get_paginator("list_managed_data_identifiers")
        list_members_paginator: ListMembersPaginator = client.get_paginator("list_members")
        list_organization_admin_accounts_paginator: ListOrganizationAdminAccountsPaginator = client.get_paginator("list_organization_admin_accounts")
        list_resource_profile_artifacts_paginator: ListResourceProfileArtifactsPaginator = client.get_paginator("list_resource_profile_artifacts")
        list_resource_profile_detections_paginator: ListResourceProfileDetectionsPaginator = client.get_paginator("list_resource_profile_detections")
        list_sensitivity_inspection_templates_paginator: ListSensitivityInspectionTemplatesPaginator = client.get_paginator("list_sensitivity_inspection_templates")
        search_resources_paginator: SearchResourcesPaginator = client.get_paginator("search_resources")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeBucketsRequestDescribeBucketsPaginateTypeDef,
    DescribeBucketsResponseTypeDef,
    GetUsageStatisticsRequestGetUsageStatisticsPaginateTypeDef,
    GetUsageStatisticsResponseTypeDef,
    ListAllowListsRequestListAllowListsPaginateTypeDef,
    ListAllowListsResponseTypeDef,
    ListAutomatedDiscoveryAccountsRequestListAutomatedDiscoveryAccountsPaginateTypeDef,
    ListAutomatedDiscoveryAccountsResponseTypeDef,
    ListClassificationJobsRequestListClassificationJobsPaginateTypeDef,
    ListClassificationJobsResponseTypeDef,
    ListClassificationScopesRequestListClassificationScopesPaginateTypeDef,
    ListClassificationScopesResponseTypeDef,
    ListCustomDataIdentifiersRequestListCustomDataIdentifiersPaginateTypeDef,
    ListCustomDataIdentifiersResponseTypeDef,
    ListFindingsFiltersRequestListFindingsFiltersPaginateTypeDef,
    ListFindingsFiltersResponseTypeDef,
    ListFindingsRequestListFindingsPaginateTypeDef,
    ListFindingsResponseTypeDef,
    ListInvitationsRequestListInvitationsPaginateTypeDef,
    ListInvitationsResponseTypeDef,
    ListManagedDataIdentifiersRequestListManagedDataIdentifiersPaginateTypeDef,
    ListManagedDataIdentifiersResponseTypeDef,
    ListMembersRequestListMembersPaginateTypeDef,
    ListMembersResponseTypeDef,
    ListOrganizationAdminAccountsRequestListOrganizationAdminAccountsPaginateTypeDef,
    ListOrganizationAdminAccountsResponseTypeDef,
    ListResourceProfileArtifactsRequestListResourceProfileArtifactsPaginateTypeDef,
    ListResourceProfileArtifactsResponseTypeDef,
    ListResourceProfileDetectionsRequestListResourceProfileDetectionsPaginateTypeDef,
    ListResourceProfileDetectionsResponseTypeDef,
    ListSensitivityInspectionTemplatesRequestListSensitivityInspectionTemplatesPaginateTypeDef,
    ListSensitivityInspectionTemplatesResponseTypeDef,
    SearchResourcesRequestSearchResourcesPaginateTypeDef,
    SearchResourcesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeBucketsPaginator",
    "GetUsageStatisticsPaginator",
    "ListAllowListsPaginator",
    "ListAutomatedDiscoveryAccountsPaginator",
    "ListClassificationJobsPaginator",
    "ListClassificationScopesPaginator",
    "ListCustomDataIdentifiersPaginator",
    "ListFindingsFiltersPaginator",
    "ListFindingsPaginator",
    "ListInvitationsPaginator",
    "ListManagedDataIdentifiersPaginator",
    "ListMembersPaginator",
    "ListOrganizationAdminAccountsPaginator",
    "ListResourceProfileArtifactsPaginator",
    "ListResourceProfileDetectionsPaginator",
    "ListSensitivityInspectionTemplatesPaginator",
    "SearchResourcesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeBucketsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/DescribeBuckets.html#Macie2.Paginator.DescribeBuckets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#describebucketspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeBucketsRequestDescribeBucketsPaginateTypeDef]
    ) -> AsyncIterator[DescribeBucketsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/DescribeBuckets.html#Macie2.Paginator.DescribeBuckets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#describebucketspaginator)
        """


class GetUsageStatisticsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/GetUsageStatistics.html#Macie2.Paginator.GetUsageStatistics)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#getusagestatisticspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetUsageStatisticsRequestGetUsageStatisticsPaginateTypeDef]
    ) -> AsyncIterator[GetUsageStatisticsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/GetUsageStatistics.html#Macie2.Paginator.GetUsageStatistics.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#getusagestatisticspaginator)
        """


class ListAllowListsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListAllowLists.html#Macie2.Paginator.ListAllowLists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listallowlistspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAllowListsRequestListAllowListsPaginateTypeDef]
    ) -> AsyncIterator[ListAllowListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListAllowLists.html#Macie2.Paginator.ListAllowLists.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listallowlistspaginator)
        """


class ListAutomatedDiscoveryAccountsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListAutomatedDiscoveryAccounts.html#Macie2.Paginator.ListAutomatedDiscoveryAccounts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listautomateddiscoveryaccountspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListAutomatedDiscoveryAccountsRequestListAutomatedDiscoveryAccountsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListAutomatedDiscoveryAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListAutomatedDiscoveryAccounts.html#Macie2.Paginator.ListAutomatedDiscoveryAccounts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listautomateddiscoveryaccountspaginator)
        """


class ListClassificationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListClassificationJobs.html#Macie2.Paginator.ListClassificationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listclassificationjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListClassificationJobsRequestListClassificationJobsPaginateTypeDef]
    ) -> AsyncIterator[ListClassificationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListClassificationJobs.html#Macie2.Paginator.ListClassificationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listclassificationjobspaginator)
        """


class ListClassificationScopesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListClassificationScopes.html#Macie2.Paginator.ListClassificationScopes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listclassificationscopespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListClassificationScopesRequestListClassificationScopesPaginateTypeDef],
    ) -> AsyncIterator[ListClassificationScopesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListClassificationScopes.html#Macie2.Paginator.ListClassificationScopes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listclassificationscopespaginator)
        """


class ListCustomDataIdentifiersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListCustomDataIdentifiers.html#Macie2.Paginator.ListCustomDataIdentifiers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listcustomdataidentifierspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListCustomDataIdentifiersRequestListCustomDataIdentifiersPaginateTypeDef],
    ) -> AsyncIterator[ListCustomDataIdentifiersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListCustomDataIdentifiers.html#Macie2.Paginator.ListCustomDataIdentifiers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listcustomdataidentifierspaginator)
        """


class ListFindingsFiltersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListFindingsFilters.html#Macie2.Paginator.ListFindingsFilters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listfindingsfilterspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFindingsFiltersRequestListFindingsFiltersPaginateTypeDef]
    ) -> AsyncIterator[ListFindingsFiltersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListFindingsFilters.html#Macie2.Paginator.ListFindingsFilters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listfindingsfilterspaginator)
        """


class ListFindingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListFindings.html#Macie2.Paginator.ListFindings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listfindingspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFindingsRequestListFindingsPaginateTypeDef]
    ) -> AsyncIterator[ListFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListFindings.html#Macie2.Paginator.ListFindings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listfindingspaginator)
        """


class ListInvitationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListInvitations.html#Macie2.Paginator.ListInvitations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listinvitationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListInvitationsRequestListInvitationsPaginateTypeDef]
    ) -> AsyncIterator[ListInvitationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListInvitations.html#Macie2.Paginator.ListInvitations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listinvitationspaginator)
        """


class ListManagedDataIdentifiersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListManagedDataIdentifiers.html#Macie2.Paginator.ListManagedDataIdentifiers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listmanageddataidentifierspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListManagedDataIdentifiersRequestListManagedDataIdentifiersPaginateTypeDef
        ],
    ) -> AsyncIterator[ListManagedDataIdentifiersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListManagedDataIdentifiers.html#Macie2.Paginator.ListManagedDataIdentifiers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listmanageddataidentifierspaginator)
        """


class ListMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListMembers.html#Macie2.Paginator.ListMembers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listmemberspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMembersRequestListMembersPaginateTypeDef]
    ) -> AsyncIterator[ListMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListMembers.html#Macie2.Paginator.ListMembers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listmemberspaginator)
        """


class ListOrganizationAdminAccountsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListOrganizationAdminAccounts.html#Macie2.Paginator.ListOrganizationAdminAccounts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listorganizationadminaccountspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListOrganizationAdminAccountsRequestListOrganizationAdminAccountsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListOrganizationAdminAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListOrganizationAdminAccounts.html#Macie2.Paginator.ListOrganizationAdminAccounts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listorganizationadminaccountspaginator)
        """


class ListResourceProfileArtifactsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListResourceProfileArtifacts.html#Macie2.Paginator.ListResourceProfileArtifacts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listresourceprofileartifactspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListResourceProfileArtifactsRequestListResourceProfileArtifactsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListResourceProfileArtifactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListResourceProfileArtifacts.html#Macie2.Paginator.ListResourceProfileArtifacts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listresourceprofileartifactspaginator)
        """


class ListResourceProfileDetectionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListResourceProfileDetections.html#Macie2.Paginator.ListResourceProfileDetections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listresourceprofiledetectionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListResourceProfileDetectionsRequestListResourceProfileDetectionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListResourceProfileDetectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListResourceProfileDetections.html#Macie2.Paginator.ListResourceProfileDetections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listresourceprofiledetectionspaginator)
        """


class ListSensitivityInspectionTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListSensitivityInspectionTemplates.html#Macie2.Paginator.ListSensitivityInspectionTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listsensitivityinspectiontemplatespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListSensitivityInspectionTemplatesRequestListSensitivityInspectionTemplatesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListSensitivityInspectionTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListSensitivityInspectionTemplates.html#Macie2.Paginator.ListSensitivityInspectionTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listsensitivityinspectiontemplatespaginator)
        """


class SearchResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/SearchResources.html#Macie2.Paginator.SearchResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#searchresourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchResourcesRequestSearchResourcesPaginateTypeDef]
    ) -> AsyncIterator[SearchResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/SearchResources.html#Macie2.Paginator.SearchResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#searchresourcespaginator)
        """
