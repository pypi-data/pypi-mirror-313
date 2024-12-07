"""
Type annotations for quicksight service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_quicksight.client import QuickSightClient
    from types_aiobotocore_quicksight.paginator import (
        DescribeFolderPermissionsPaginator,
        DescribeFolderResolvedPermissionsPaginator,
        ListAnalysesPaginator,
        ListAssetBundleExportJobsPaginator,
        ListAssetBundleImportJobsPaginator,
        ListDashboardVersionsPaginator,
        ListDashboardsPaginator,
        ListDataSetsPaginator,
        ListDataSourcesPaginator,
        ListFolderMembersPaginator,
        ListFoldersForResourcePaginator,
        ListFoldersPaginator,
        ListGroupMembershipsPaginator,
        ListGroupsPaginator,
        ListIAMPolicyAssignmentsForUserPaginator,
        ListIAMPolicyAssignmentsPaginator,
        ListIngestionsPaginator,
        ListNamespacesPaginator,
        ListRoleMembershipsPaginator,
        ListTemplateAliasesPaginator,
        ListTemplateVersionsPaginator,
        ListTemplatesPaginator,
        ListThemeVersionsPaginator,
        ListThemesPaginator,
        ListUserGroupsPaginator,
        ListUsersPaginator,
        SearchAnalysesPaginator,
        SearchDashboardsPaginator,
        SearchDataSetsPaginator,
        SearchDataSourcesPaginator,
        SearchFoldersPaginator,
        SearchGroupsPaginator,
    )

    session = get_session()
    with session.create_client("quicksight") as client:
        client: QuickSightClient

        describe_folder_permissions_paginator: DescribeFolderPermissionsPaginator = client.get_paginator("describe_folder_permissions")
        describe_folder_resolved_permissions_paginator: DescribeFolderResolvedPermissionsPaginator = client.get_paginator("describe_folder_resolved_permissions")
        list_analyses_paginator: ListAnalysesPaginator = client.get_paginator("list_analyses")
        list_asset_bundle_export_jobs_paginator: ListAssetBundleExportJobsPaginator = client.get_paginator("list_asset_bundle_export_jobs")
        list_asset_bundle_import_jobs_paginator: ListAssetBundleImportJobsPaginator = client.get_paginator("list_asset_bundle_import_jobs")
        list_dashboard_versions_paginator: ListDashboardVersionsPaginator = client.get_paginator("list_dashboard_versions")
        list_dashboards_paginator: ListDashboardsPaginator = client.get_paginator("list_dashboards")
        list_data_sets_paginator: ListDataSetsPaginator = client.get_paginator("list_data_sets")
        list_data_sources_paginator: ListDataSourcesPaginator = client.get_paginator("list_data_sources")
        list_folder_members_paginator: ListFolderMembersPaginator = client.get_paginator("list_folder_members")
        list_folders_for_resource_paginator: ListFoldersForResourcePaginator = client.get_paginator("list_folders_for_resource")
        list_folders_paginator: ListFoldersPaginator = client.get_paginator("list_folders")
        list_group_memberships_paginator: ListGroupMembershipsPaginator = client.get_paginator("list_group_memberships")
        list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
        list_iam_policy_assignments_for_user_paginator: ListIAMPolicyAssignmentsForUserPaginator = client.get_paginator("list_iam_policy_assignments_for_user")
        list_iam_policy_assignments_paginator: ListIAMPolicyAssignmentsPaginator = client.get_paginator("list_iam_policy_assignments")
        list_ingestions_paginator: ListIngestionsPaginator = client.get_paginator("list_ingestions")
        list_namespaces_paginator: ListNamespacesPaginator = client.get_paginator("list_namespaces")
        list_role_memberships_paginator: ListRoleMembershipsPaginator = client.get_paginator("list_role_memberships")
        list_template_aliases_paginator: ListTemplateAliasesPaginator = client.get_paginator("list_template_aliases")
        list_template_versions_paginator: ListTemplateVersionsPaginator = client.get_paginator("list_template_versions")
        list_templates_paginator: ListTemplatesPaginator = client.get_paginator("list_templates")
        list_theme_versions_paginator: ListThemeVersionsPaginator = client.get_paginator("list_theme_versions")
        list_themes_paginator: ListThemesPaginator = client.get_paginator("list_themes")
        list_user_groups_paginator: ListUserGroupsPaginator = client.get_paginator("list_user_groups")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
        search_analyses_paginator: SearchAnalysesPaginator = client.get_paginator("search_analyses")
        search_dashboards_paginator: SearchDashboardsPaginator = client.get_paginator("search_dashboards")
        search_data_sets_paginator: SearchDataSetsPaginator = client.get_paginator("search_data_sets")
        search_data_sources_paginator: SearchDataSourcesPaginator = client.get_paginator("search_data_sources")
        search_folders_paginator: SearchFoldersPaginator = client.get_paginator("search_folders")
        search_groups_paginator: SearchGroupsPaginator = client.get_paginator("search_groups")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeFolderPermissionsRequestDescribeFolderPermissionsPaginateTypeDef,
    DescribeFolderPermissionsResponseTypeDef,
    DescribeFolderResolvedPermissionsRequestDescribeFolderResolvedPermissionsPaginateTypeDef,
    DescribeFolderResolvedPermissionsResponseTypeDef,
    ListAnalysesRequestListAnalysesPaginateTypeDef,
    ListAnalysesResponseTypeDef,
    ListAssetBundleExportJobsRequestListAssetBundleExportJobsPaginateTypeDef,
    ListAssetBundleExportJobsResponseTypeDef,
    ListAssetBundleImportJobsRequestListAssetBundleImportJobsPaginateTypeDef,
    ListAssetBundleImportJobsResponseTypeDef,
    ListDashboardsRequestListDashboardsPaginateTypeDef,
    ListDashboardsResponseTypeDef,
    ListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef,
    ListDashboardVersionsResponseTypeDef,
    ListDataSetsRequestListDataSetsPaginateTypeDef,
    ListDataSetsResponseTypeDef,
    ListDataSourcesRequestListDataSourcesPaginateTypeDef,
    ListDataSourcesResponseTypeDef,
    ListFolderMembersRequestListFolderMembersPaginateTypeDef,
    ListFolderMembersResponseTypeDef,
    ListFoldersForResourceRequestListFoldersForResourcePaginateTypeDef,
    ListFoldersForResourceResponseTypeDef,
    ListFoldersRequestListFoldersPaginateTypeDef,
    ListFoldersResponseTypeDef,
    ListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef,
    ListGroupMembershipsResponseTypeDef,
    ListGroupsRequestListGroupsPaginateTypeDef,
    ListGroupsResponseTypeDef,
    ListIAMPolicyAssignmentsForUserRequestListIAMPolicyAssignmentsForUserPaginateTypeDef,
    ListIAMPolicyAssignmentsForUserResponseTypeDef,
    ListIAMPolicyAssignmentsRequestListIAMPolicyAssignmentsPaginateTypeDef,
    ListIAMPolicyAssignmentsResponseTypeDef,
    ListIngestionsRequestListIngestionsPaginateTypeDef,
    ListIngestionsResponseTypeDef,
    ListNamespacesRequestListNamespacesPaginateTypeDef,
    ListNamespacesResponseTypeDef,
    ListRoleMembershipsRequestListRoleMembershipsPaginateTypeDef,
    ListRoleMembershipsResponseTypeDef,
    ListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef,
    ListTemplateAliasesResponseTypeDef,
    ListTemplatesRequestListTemplatesPaginateTypeDef,
    ListTemplatesResponseTypeDef,
    ListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef,
    ListTemplateVersionsResponseTypeDef,
    ListThemesRequestListThemesPaginateTypeDef,
    ListThemesResponseTypeDef,
    ListThemeVersionsRequestListThemeVersionsPaginateTypeDef,
    ListThemeVersionsResponseTypeDef,
    ListUserGroupsRequestListUserGroupsPaginateTypeDef,
    ListUserGroupsResponseTypeDef,
    ListUsersRequestListUsersPaginateTypeDef,
    ListUsersResponseTypeDef,
    SearchAnalysesRequestSearchAnalysesPaginateTypeDef,
    SearchAnalysesResponseTypeDef,
    SearchDashboardsRequestSearchDashboardsPaginateTypeDef,
    SearchDashboardsResponseTypeDef,
    SearchDataSetsRequestSearchDataSetsPaginateTypeDef,
    SearchDataSetsResponseTypeDef,
    SearchDataSourcesRequestSearchDataSourcesPaginateTypeDef,
    SearchDataSourcesResponseTypeDef,
    SearchFoldersRequestSearchFoldersPaginateTypeDef,
    SearchFoldersResponseTypeDef,
    SearchGroupsRequestSearchGroupsPaginateTypeDef,
    SearchGroupsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeFolderPermissionsPaginator",
    "DescribeFolderResolvedPermissionsPaginator",
    "ListAnalysesPaginator",
    "ListAssetBundleExportJobsPaginator",
    "ListAssetBundleImportJobsPaginator",
    "ListDashboardVersionsPaginator",
    "ListDashboardsPaginator",
    "ListDataSetsPaginator",
    "ListDataSourcesPaginator",
    "ListFolderMembersPaginator",
    "ListFoldersForResourcePaginator",
    "ListFoldersPaginator",
    "ListGroupMembershipsPaginator",
    "ListGroupsPaginator",
    "ListIAMPolicyAssignmentsForUserPaginator",
    "ListIAMPolicyAssignmentsPaginator",
    "ListIngestionsPaginator",
    "ListNamespacesPaginator",
    "ListRoleMembershipsPaginator",
    "ListTemplateAliasesPaginator",
    "ListTemplateVersionsPaginator",
    "ListTemplatesPaginator",
    "ListThemeVersionsPaginator",
    "ListThemesPaginator",
    "ListUserGroupsPaginator",
    "ListUsersPaginator",
    "SearchAnalysesPaginator",
    "SearchDashboardsPaginator",
    "SearchDataSetsPaginator",
    "SearchDataSourcesPaginator",
    "SearchFoldersPaginator",
    "SearchGroupsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeFolderPermissionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/DescribeFolderPermissions.html#QuickSight.Paginator.DescribeFolderPermissions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#describefolderpermissionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeFolderPermissionsRequestDescribeFolderPermissionsPaginateTypeDef],
    ) -> AsyncIterator[DescribeFolderPermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/DescribeFolderPermissions.html#QuickSight.Paginator.DescribeFolderPermissions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#describefolderpermissionspaginator)
        """


class DescribeFolderResolvedPermissionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/DescribeFolderResolvedPermissions.html#QuickSight.Paginator.DescribeFolderResolvedPermissions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#describefolderresolvedpermissionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeFolderResolvedPermissionsRequestDescribeFolderResolvedPermissionsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeFolderResolvedPermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/DescribeFolderResolvedPermissions.html#QuickSight.Paginator.DescribeFolderResolvedPermissions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#describefolderresolvedpermissionspaginator)
        """


class ListAnalysesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListAnalyses.html#QuickSight.Paginator.ListAnalyses)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listanalysespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAnalysesRequestListAnalysesPaginateTypeDef]
    ) -> AsyncIterator[ListAnalysesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListAnalyses.html#QuickSight.Paginator.ListAnalyses.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listanalysespaginator)
        """


class ListAssetBundleExportJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListAssetBundleExportJobs.html#QuickSight.Paginator.ListAssetBundleExportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listassetbundleexportjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListAssetBundleExportJobsRequestListAssetBundleExportJobsPaginateTypeDef],
    ) -> AsyncIterator[ListAssetBundleExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListAssetBundleExportJobs.html#QuickSight.Paginator.ListAssetBundleExportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listassetbundleexportjobspaginator)
        """


class ListAssetBundleImportJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListAssetBundleImportJobs.html#QuickSight.Paginator.ListAssetBundleImportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listassetbundleimportjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListAssetBundleImportJobsRequestListAssetBundleImportJobsPaginateTypeDef],
    ) -> AsyncIterator[ListAssetBundleImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListAssetBundleImportJobs.html#QuickSight.Paginator.ListAssetBundleImportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listassetbundleimportjobspaginator)
        """


class ListDashboardVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListDashboardVersions.html#QuickSight.Paginator.ListDashboardVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listdashboardversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef]
    ) -> AsyncIterator[ListDashboardVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListDashboardVersions.html#QuickSight.Paginator.ListDashboardVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listdashboardversionspaginator)
        """


class ListDashboardsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListDashboards.html#QuickSight.Paginator.ListDashboards)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listdashboardspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDashboardsRequestListDashboardsPaginateTypeDef]
    ) -> AsyncIterator[ListDashboardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListDashboards.html#QuickSight.Paginator.ListDashboards.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listdashboardspaginator)
        """


class ListDataSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListDataSets.html#QuickSight.Paginator.ListDataSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listdatasetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDataSetsRequestListDataSetsPaginateTypeDef]
    ) -> AsyncIterator[ListDataSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListDataSets.html#QuickSight.Paginator.ListDataSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listdatasetspaginator)
        """


class ListDataSourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListDataSources.html#QuickSight.Paginator.ListDataSources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listdatasourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDataSourcesRequestListDataSourcesPaginateTypeDef]
    ) -> AsyncIterator[ListDataSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListDataSources.html#QuickSight.Paginator.ListDataSources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listdatasourcespaginator)
        """


class ListFolderMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListFolderMembers.html#QuickSight.Paginator.ListFolderMembers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listfoldermemberspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFolderMembersRequestListFolderMembersPaginateTypeDef]
    ) -> AsyncIterator[ListFolderMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListFolderMembers.html#QuickSight.Paginator.ListFolderMembers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listfoldermemberspaginator)
        """


class ListFoldersForResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListFoldersForResource.html#QuickSight.Paginator.ListFoldersForResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listfoldersforresourcepaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFoldersForResourceRequestListFoldersForResourcePaginateTypeDef]
    ) -> AsyncIterator[ListFoldersForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListFoldersForResource.html#QuickSight.Paginator.ListFoldersForResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listfoldersforresourcepaginator)
        """


class ListFoldersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListFolders.html#QuickSight.Paginator.ListFolders)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listfolderspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFoldersRequestListFoldersPaginateTypeDef]
    ) -> AsyncIterator[ListFoldersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListFolders.html#QuickSight.Paginator.ListFolders.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listfolderspaginator)
        """


class ListGroupMembershipsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListGroupMemberships.html#QuickSight.Paginator.ListGroupMemberships)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listgroupmembershipspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef]
    ) -> AsyncIterator[ListGroupMembershipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListGroupMemberships.html#QuickSight.Paginator.ListGroupMemberships.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listgroupmembershipspaginator)
        """


class ListGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListGroups.html#QuickSight.Paginator.ListGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGroupsRequestListGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListGroups.html#QuickSight.Paginator.ListGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listgroupspaginator)
        """


class ListIAMPolicyAssignmentsForUserPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListIAMPolicyAssignmentsForUser.html#QuickSight.Paginator.ListIAMPolicyAssignmentsForUser)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listiampolicyassignmentsforuserpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListIAMPolicyAssignmentsForUserRequestListIAMPolicyAssignmentsForUserPaginateTypeDef
        ],
    ) -> AsyncIterator[ListIAMPolicyAssignmentsForUserResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListIAMPolicyAssignmentsForUser.html#QuickSight.Paginator.ListIAMPolicyAssignmentsForUser.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listiampolicyassignmentsforuserpaginator)
        """


class ListIAMPolicyAssignmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListIAMPolicyAssignments.html#QuickSight.Paginator.ListIAMPolicyAssignments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listiampolicyassignmentspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListIAMPolicyAssignmentsRequestListIAMPolicyAssignmentsPaginateTypeDef],
    ) -> AsyncIterator[ListIAMPolicyAssignmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListIAMPolicyAssignments.html#QuickSight.Paginator.ListIAMPolicyAssignments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listiampolicyassignmentspaginator)
        """


class ListIngestionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListIngestions.html#QuickSight.Paginator.ListIngestions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listingestionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListIngestionsRequestListIngestionsPaginateTypeDef]
    ) -> AsyncIterator[ListIngestionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListIngestions.html#QuickSight.Paginator.ListIngestions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listingestionspaginator)
        """


class ListNamespacesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListNamespaces.html#QuickSight.Paginator.ListNamespaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listnamespacespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListNamespacesRequestListNamespacesPaginateTypeDef]
    ) -> AsyncIterator[ListNamespacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListNamespaces.html#QuickSight.Paginator.ListNamespaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listnamespacespaginator)
        """


class ListRoleMembershipsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListRoleMemberships.html#QuickSight.Paginator.ListRoleMemberships)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listrolemembershipspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRoleMembershipsRequestListRoleMembershipsPaginateTypeDef]
    ) -> AsyncIterator[ListRoleMembershipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListRoleMemberships.html#QuickSight.Paginator.ListRoleMemberships.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listrolemembershipspaginator)
        """


class ListTemplateAliasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListTemplateAliases.html#QuickSight.Paginator.ListTemplateAliases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listtemplatealiasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef]
    ) -> AsyncIterator[ListTemplateAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListTemplateAliases.html#QuickSight.Paginator.ListTemplateAliases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listtemplatealiasespaginator)
        """


class ListTemplateVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListTemplateVersions.html#QuickSight.Paginator.ListTemplateVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listtemplateversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef]
    ) -> AsyncIterator[ListTemplateVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListTemplateVersions.html#QuickSight.Paginator.ListTemplateVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listtemplateversionspaginator)
        """


class ListTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListTemplates.html#QuickSight.Paginator.ListTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listtemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTemplatesRequestListTemplatesPaginateTypeDef]
    ) -> AsyncIterator[ListTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListTemplates.html#QuickSight.Paginator.ListTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listtemplatespaginator)
        """


class ListThemeVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListThemeVersions.html#QuickSight.Paginator.ListThemeVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listthemeversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListThemeVersionsRequestListThemeVersionsPaginateTypeDef]
    ) -> AsyncIterator[ListThemeVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListThemeVersions.html#QuickSight.Paginator.ListThemeVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listthemeversionspaginator)
        """


class ListThemesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListThemes.html#QuickSight.Paginator.ListThemes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listthemespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListThemesRequestListThemesPaginateTypeDef]
    ) -> AsyncIterator[ListThemesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListThemes.html#QuickSight.Paginator.ListThemes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listthemespaginator)
        """


class ListUserGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListUserGroups.html#QuickSight.Paginator.ListUserGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listusergroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListUserGroupsRequestListUserGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListUserGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListUserGroups.html#QuickSight.Paginator.ListUserGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listusergroupspaginator)
        """


class ListUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListUsers.html#QuickSight.Paginator.ListUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listuserspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListUsersRequestListUsersPaginateTypeDef]
    ) -> AsyncIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListUsers.html#QuickSight.Paginator.ListUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listuserspaginator)
        """


class SearchAnalysesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchAnalyses.html#QuickSight.Paginator.SearchAnalyses)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchanalysespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchAnalysesRequestSearchAnalysesPaginateTypeDef]
    ) -> AsyncIterator[SearchAnalysesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchAnalyses.html#QuickSight.Paginator.SearchAnalyses.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchanalysespaginator)
        """


class SearchDashboardsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchDashboards.html#QuickSight.Paginator.SearchDashboards)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchdashboardspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchDashboardsRequestSearchDashboardsPaginateTypeDef]
    ) -> AsyncIterator[SearchDashboardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchDashboards.html#QuickSight.Paginator.SearchDashboards.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchdashboardspaginator)
        """


class SearchDataSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchDataSets.html#QuickSight.Paginator.SearchDataSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchdatasetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchDataSetsRequestSearchDataSetsPaginateTypeDef]
    ) -> AsyncIterator[SearchDataSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchDataSets.html#QuickSight.Paginator.SearchDataSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchdatasetspaginator)
        """


class SearchDataSourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchDataSources.html#QuickSight.Paginator.SearchDataSources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchdatasourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchDataSourcesRequestSearchDataSourcesPaginateTypeDef]
    ) -> AsyncIterator[SearchDataSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchDataSources.html#QuickSight.Paginator.SearchDataSources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchdatasourcespaginator)
        """


class SearchFoldersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchFolders.html#QuickSight.Paginator.SearchFolders)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchfolderspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchFoldersRequestSearchFoldersPaginateTypeDef]
    ) -> AsyncIterator[SearchFoldersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchFolders.html#QuickSight.Paginator.SearchFolders.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchfolderspaginator)
        """


class SearchGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchGroups.html#QuickSight.Paginator.SearchGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchGroupsRequestSearchGroupsPaginateTypeDef]
    ) -> AsyncIterator[SearchGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchGroups.html#QuickSight.Paginator.SearchGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchgroupspaginator)
        """
