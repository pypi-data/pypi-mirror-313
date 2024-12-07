"""
Type annotations for inspector2 service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_inspector2.client import Inspector2Client
    from types_aiobotocore_inspector2.paginator import (
        GetCisScanResultDetailsPaginator,
        ListAccountPermissionsPaginator,
        ListCisScanConfigurationsPaginator,
        ListCisScanResultsAggregatedByChecksPaginator,
        ListCisScanResultsAggregatedByTargetResourcePaginator,
        ListCisScansPaginator,
        ListCoveragePaginator,
        ListCoverageStatisticsPaginator,
        ListDelegatedAdminAccountsPaginator,
        ListFiltersPaginator,
        ListFindingAggregationsPaginator,
        ListFindingsPaginator,
        ListMembersPaginator,
        ListUsageTotalsPaginator,
        SearchVulnerabilitiesPaginator,
    )

    session = get_session()
    with session.create_client("inspector2") as client:
        client: Inspector2Client

        get_cis_scan_result_details_paginator: GetCisScanResultDetailsPaginator = client.get_paginator("get_cis_scan_result_details")
        list_account_permissions_paginator: ListAccountPermissionsPaginator = client.get_paginator("list_account_permissions")
        list_cis_scan_configurations_paginator: ListCisScanConfigurationsPaginator = client.get_paginator("list_cis_scan_configurations")
        list_cis_scan_results_aggregated_by_checks_paginator: ListCisScanResultsAggregatedByChecksPaginator = client.get_paginator("list_cis_scan_results_aggregated_by_checks")
        list_cis_scan_results_aggregated_by_target_resource_paginator: ListCisScanResultsAggregatedByTargetResourcePaginator = client.get_paginator("list_cis_scan_results_aggregated_by_target_resource")
        list_cis_scans_paginator: ListCisScansPaginator = client.get_paginator("list_cis_scans")
        list_coverage_paginator: ListCoveragePaginator = client.get_paginator("list_coverage")
        list_coverage_statistics_paginator: ListCoverageStatisticsPaginator = client.get_paginator("list_coverage_statistics")
        list_delegated_admin_accounts_paginator: ListDelegatedAdminAccountsPaginator = client.get_paginator("list_delegated_admin_accounts")
        list_filters_paginator: ListFiltersPaginator = client.get_paginator("list_filters")
        list_finding_aggregations_paginator: ListFindingAggregationsPaginator = client.get_paginator("list_finding_aggregations")
        list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
        list_members_paginator: ListMembersPaginator = client.get_paginator("list_members")
        list_usage_totals_paginator: ListUsageTotalsPaginator = client.get_paginator("list_usage_totals")
        search_vulnerabilities_paginator: SearchVulnerabilitiesPaginator = client.get_paginator("search_vulnerabilities")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetCisScanResultDetailsRequestGetCisScanResultDetailsPaginateTypeDef,
    GetCisScanResultDetailsResponseTypeDef,
    ListAccountPermissionsRequestListAccountPermissionsPaginateTypeDef,
    ListAccountPermissionsResponseTypeDef,
    ListCisScanConfigurationsRequestListCisScanConfigurationsPaginateTypeDef,
    ListCisScanConfigurationsResponseTypeDef,
    ListCisScanResultsAggregatedByChecksRequestListCisScanResultsAggregatedByChecksPaginateTypeDef,
    ListCisScanResultsAggregatedByChecksResponseTypeDef,
    ListCisScanResultsAggregatedByTargetResourceRequestListCisScanResultsAggregatedByTargetResourcePaginateTypeDef,
    ListCisScanResultsAggregatedByTargetResourceResponseTypeDef,
    ListCisScansRequestListCisScansPaginateTypeDef,
    ListCisScansResponseTypeDef,
    ListCoverageRequestListCoveragePaginateTypeDef,
    ListCoverageResponseTypeDef,
    ListCoverageStatisticsRequestListCoverageStatisticsPaginateTypeDef,
    ListCoverageStatisticsResponseTypeDef,
    ListDelegatedAdminAccountsRequestListDelegatedAdminAccountsPaginateTypeDef,
    ListDelegatedAdminAccountsResponseTypeDef,
    ListFiltersRequestListFiltersPaginateTypeDef,
    ListFiltersResponseTypeDef,
    ListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef,
    ListFindingAggregationsResponseTypeDef,
    ListFindingsRequestListFindingsPaginateTypeDef,
    ListFindingsResponseTypeDef,
    ListMembersRequestListMembersPaginateTypeDef,
    ListMembersResponseTypeDef,
    ListUsageTotalsRequestListUsageTotalsPaginateTypeDef,
    ListUsageTotalsResponseTypeDef,
    SearchVulnerabilitiesRequestSearchVulnerabilitiesPaginateTypeDef,
    SearchVulnerabilitiesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetCisScanResultDetailsPaginator",
    "ListAccountPermissionsPaginator",
    "ListCisScanConfigurationsPaginator",
    "ListCisScanResultsAggregatedByChecksPaginator",
    "ListCisScanResultsAggregatedByTargetResourcePaginator",
    "ListCisScansPaginator",
    "ListCoveragePaginator",
    "ListCoverageStatisticsPaginator",
    "ListDelegatedAdminAccountsPaginator",
    "ListFiltersPaginator",
    "ListFindingAggregationsPaginator",
    "ListFindingsPaginator",
    "ListMembersPaginator",
    "ListUsageTotalsPaginator",
    "SearchVulnerabilitiesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetCisScanResultDetailsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/GetCisScanResultDetails.html#Inspector2.Paginator.GetCisScanResultDetails)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#getcisscanresultdetailspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetCisScanResultDetailsRequestGetCisScanResultDetailsPaginateTypeDef]
    ) -> AsyncIterator[GetCisScanResultDetailsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/GetCisScanResultDetails.html#Inspector2.Paginator.GetCisScanResultDetails.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#getcisscanresultdetailspaginator)
        """

class ListAccountPermissionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListAccountPermissions.html#Inspector2.Paginator.ListAccountPermissions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listaccountpermissionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAccountPermissionsRequestListAccountPermissionsPaginateTypeDef]
    ) -> AsyncIterator[ListAccountPermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListAccountPermissions.html#Inspector2.Paginator.ListAccountPermissions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listaccountpermissionspaginator)
        """

class ListCisScanConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCisScanConfigurations.html#Inspector2.Paginator.ListCisScanConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcisscanconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListCisScanConfigurationsRequestListCisScanConfigurationsPaginateTypeDef],
    ) -> AsyncIterator[ListCisScanConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCisScanConfigurations.html#Inspector2.Paginator.ListCisScanConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcisscanconfigurationspaginator)
        """

class ListCisScanResultsAggregatedByChecksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCisScanResultsAggregatedByChecks.html#Inspector2.Paginator.ListCisScanResultsAggregatedByChecks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcisscanresultsaggregatedbycheckspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCisScanResultsAggregatedByChecksRequestListCisScanResultsAggregatedByChecksPaginateTypeDef
        ],
    ) -> AsyncIterator[ListCisScanResultsAggregatedByChecksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCisScanResultsAggregatedByChecks.html#Inspector2.Paginator.ListCisScanResultsAggregatedByChecks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcisscanresultsaggregatedbycheckspaginator)
        """

class ListCisScanResultsAggregatedByTargetResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCisScanResultsAggregatedByTargetResource.html#Inspector2.Paginator.ListCisScanResultsAggregatedByTargetResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcisscanresultsaggregatedbytargetresourcepaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCisScanResultsAggregatedByTargetResourceRequestListCisScanResultsAggregatedByTargetResourcePaginateTypeDef
        ],
    ) -> AsyncIterator[ListCisScanResultsAggregatedByTargetResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCisScanResultsAggregatedByTargetResource.html#Inspector2.Paginator.ListCisScanResultsAggregatedByTargetResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcisscanresultsaggregatedbytargetresourcepaginator)
        """

class ListCisScansPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCisScans.html#Inspector2.Paginator.ListCisScans)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcisscanspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCisScansRequestListCisScansPaginateTypeDef]
    ) -> AsyncIterator[ListCisScansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCisScans.html#Inspector2.Paginator.ListCisScans.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcisscanspaginator)
        """

class ListCoveragePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCoverage.html#Inspector2.Paginator.ListCoverage)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcoveragepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCoverageRequestListCoveragePaginateTypeDef]
    ) -> AsyncIterator[ListCoverageResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCoverage.html#Inspector2.Paginator.ListCoverage.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcoveragepaginator)
        """

class ListCoverageStatisticsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCoverageStatistics.html#Inspector2.Paginator.ListCoverageStatistics)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcoveragestatisticspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCoverageStatisticsRequestListCoverageStatisticsPaginateTypeDef]
    ) -> AsyncIterator[ListCoverageStatisticsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCoverageStatistics.html#Inspector2.Paginator.ListCoverageStatistics.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcoveragestatisticspaginator)
        """

class ListDelegatedAdminAccountsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListDelegatedAdminAccounts.html#Inspector2.Paginator.ListDelegatedAdminAccounts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listdelegatedadminaccountspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListDelegatedAdminAccountsRequestListDelegatedAdminAccountsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListDelegatedAdminAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListDelegatedAdminAccounts.html#Inspector2.Paginator.ListDelegatedAdminAccounts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listdelegatedadminaccountspaginator)
        """

class ListFiltersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListFilters.html#Inspector2.Paginator.ListFilters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listfilterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFiltersRequestListFiltersPaginateTypeDef]
    ) -> AsyncIterator[ListFiltersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListFilters.html#Inspector2.Paginator.ListFilters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listfilterspaginator)
        """

class ListFindingAggregationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListFindingAggregations.html#Inspector2.Paginator.ListFindingAggregations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listfindingaggregationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef]
    ) -> AsyncIterator[ListFindingAggregationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListFindingAggregations.html#Inspector2.Paginator.ListFindingAggregations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listfindingaggregationspaginator)
        """

class ListFindingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListFindings.html#Inspector2.Paginator.ListFindings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listfindingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFindingsRequestListFindingsPaginateTypeDef]
    ) -> AsyncIterator[ListFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListFindings.html#Inspector2.Paginator.ListFindings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listfindingspaginator)
        """

class ListMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListMembers.html#Inspector2.Paginator.ListMembers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listmemberspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMembersRequestListMembersPaginateTypeDef]
    ) -> AsyncIterator[ListMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListMembers.html#Inspector2.Paginator.ListMembers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listmemberspaginator)
        """

class ListUsageTotalsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListUsageTotals.html#Inspector2.Paginator.ListUsageTotals)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listusagetotalspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUsageTotalsRequestListUsageTotalsPaginateTypeDef]
    ) -> AsyncIterator[ListUsageTotalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListUsageTotals.html#Inspector2.Paginator.ListUsageTotals.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listusagetotalspaginator)
        """

class SearchVulnerabilitiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/SearchVulnerabilities.html#Inspector2.Paginator.SearchVulnerabilities)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#searchvulnerabilitiespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchVulnerabilitiesRequestSearchVulnerabilitiesPaginateTypeDef]
    ) -> AsyncIterator[SearchVulnerabilitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/SearchVulnerabilities.html#Inspector2.Paginator.SearchVulnerabilities.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#searchvulnerabilitiespaginator)
        """
