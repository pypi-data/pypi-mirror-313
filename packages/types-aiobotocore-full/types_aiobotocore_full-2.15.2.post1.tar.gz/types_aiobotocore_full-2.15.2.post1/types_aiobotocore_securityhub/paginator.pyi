"""
Type annotations for securityhub service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_securityhub.client import SecurityHubClient
    from types_aiobotocore_securityhub.paginator import (
        DescribeActionTargetsPaginator,
        DescribeProductsPaginator,
        DescribeStandardsControlsPaginator,
        DescribeStandardsPaginator,
        GetEnabledStandardsPaginator,
        GetFindingHistoryPaginator,
        GetFindingsPaginator,
        GetInsightsPaginator,
        ListConfigurationPoliciesPaginator,
        ListConfigurationPolicyAssociationsPaginator,
        ListEnabledProductsForImportPaginator,
        ListFindingAggregatorsPaginator,
        ListInvitationsPaginator,
        ListMembersPaginator,
        ListOrganizationAdminAccountsPaginator,
        ListSecurityControlDefinitionsPaginator,
        ListStandardsControlAssociationsPaginator,
    )

    session = get_session()
    with session.create_client("securityhub") as client:
        client: SecurityHubClient

        describe_action_targets_paginator: DescribeActionTargetsPaginator = client.get_paginator("describe_action_targets")
        describe_products_paginator: DescribeProductsPaginator = client.get_paginator("describe_products")
        describe_standards_controls_paginator: DescribeStandardsControlsPaginator = client.get_paginator("describe_standards_controls")
        describe_standards_paginator: DescribeStandardsPaginator = client.get_paginator("describe_standards")
        get_enabled_standards_paginator: GetEnabledStandardsPaginator = client.get_paginator("get_enabled_standards")
        get_finding_history_paginator: GetFindingHistoryPaginator = client.get_paginator("get_finding_history")
        get_findings_paginator: GetFindingsPaginator = client.get_paginator("get_findings")
        get_insights_paginator: GetInsightsPaginator = client.get_paginator("get_insights")
        list_configuration_policies_paginator: ListConfigurationPoliciesPaginator = client.get_paginator("list_configuration_policies")
        list_configuration_policy_associations_paginator: ListConfigurationPolicyAssociationsPaginator = client.get_paginator("list_configuration_policy_associations")
        list_enabled_products_for_import_paginator: ListEnabledProductsForImportPaginator = client.get_paginator("list_enabled_products_for_import")
        list_finding_aggregators_paginator: ListFindingAggregatorsPaginator = client.get_paginator("list_finding_aggregators")
        list_invitations_paginator: ListInvitationsPaginator = client.get_paginator("list_invitations")
        list_members_paginator: ListMembersPaginator = client.get_paginator("list_members")
        list_organization_admin_accounts_paginator: ListOrganizationAdminAccountsPaginator = client.get_paginator("list_organization_admin_accounts")
        list_security_control_definitions_paginator: ListSecurityControlDefinitionsPaginator = client.get_paginator("list_security_control_definitions")
        list_standards_control_associations_paginator: ListStandardsControlAssociationsPaginator = client.get_paginator("list_standards_control_associations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeActionTargetsRequestDescribeActionTargetsPaginateTypeDef,
    DescribeActionTargetsResponseTypeDef,
    DescribeProductsRequestDescribeProductsPaginateTypeDef,
    DescribeProductsResponseTypeDef,
    DescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef,
    DescribeStandardsControlsResponseTypeDef,
    DescribeStandardsRequestDescribeStandardsPaginateTypeDef,
    DescribeStandardsResponseTypeDef,
    GetEnabledStandardsRequestGetEnabledStandardsPaginateTypeDef,
    GetEnabledStandardsResponseTypeDef,
    GetFindingHistoryRequestGetFindingHistoryPaginateTypeDef,
    GetFindingHistoryResponseTypeDef,
    GetFindingsRequestGetFindingsPaginateTypeDef,
    GetFindingsResponseTypeDef,
    GetInsightsRequestGetInsightsPaginateTypeDef,
    GetInsightsResponseTypeDef,
    ListConfigurationPoliciesRequestListConfigurationPoliciesPaginateTypeDef,
    ListConfigurationPoliciesResponseTypeDef,
    ListConfigurationPolicyAssociationsRequestListConfigurationPolicyAssociationsPaginateTypeDef,
    ListConfigurationPolicyAssociationsResponseTypeDef,
    ListEnabledProductsForImportRequestListEnabledProductsForImportPaginateTypeDef,
    ListEnabledProductsForImportResponseTypeDef,
    ListFindingAggregatorsRequestListFindingAggregatorsPaginateTypeDef,
    ListFindingAggregatorsResponseTypeDef,
    ListInvitationsRequestListInvitationsPaginateTypeDef,
    ListInvitationsResponseTypeDef,
    ListMembersRequestListMembersPaginateTypeDef,
    ListMembersResponseTypeDef,
    ListOrganizationAdminAccountsRequestListOrganizationAdminAccountsPaginateTypeDef,
    ListOrganizationAdminAccountsResponseTypeDef,
    ListSecurityControlDefinitionsRequestListSecurityControlDefinitionsPaginateTypeDef,
    ListSecurityControlDefinitionsResponseTypeDef,
    ListStandardsControlAssociationsRequestListStandardsControlAssociationsPaginateTypeDef,
    ListStandardsControlAssociationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeActionTargetsPaginator",
    "DescribeProductsPaginator",
    "DescribeStandardsControlsPaginator",
    "DescribeStandardsPaginator",
    "GetEnabledStandardsPaginator",
    "GetFindingHistoryPaginator",
    "GetFindingsPaginator",
    "GetInsightsPaginator",
    "ListConfigurationPoliciesPaginator",
    "ListConfigurationPolicyAssociationsPaginator",
    "ListEnabledProductsForImportPaginator",
    "ListFindingAggregatorsPaginator",
    "ListInvitationsPaginator",
    "ListMembersPaginator",
    "ListOrganizationAdminAccountsPaginator",
    "ListSecurityControlDefinitionsPaginator",
    "ListStandardsControlAssociationsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeActionTargetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeActionTargets.html#SecurityHub.Paginator.DescribeActionTargets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describeactiontargetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeActionTargetsRequestDescribeActionTargetsPaginateTypeDef]
    ) -> AsyncIterator[DescribeActionTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeActionTargets.html#SecurityHub.Paginator.DescribeActionTargets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describeactiontargetspaginator)
        """

class DescribeProductsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeProducts.html#SecurityHub.Paginator.DescribeProducts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describeproductspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeProductsRequestDescribeProductsPaginateTypeDef]
    ) -> AsyncIterator[DescribeProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeProducts.html#SecurityHub.Paginator.DescribeProducts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describeproductspaginator)
        """

class DescribeStandardsControlsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeStandardsControls.html#SecurityHub.Paginator.DescribeStandardsControls)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describestandardscontrolspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef],
    ) -> AsyncIterator[DescribeStandardsControlsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeStandardsControls.html#SecurityHub.Paginator.DescribeStandardsControls.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describestandardscontrolspaginator)
        """

class DescribeStandardsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeStandards.html#SecurityHub.Paginator.DescribeStandards)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describestandardspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeStandardsRequestDescribeStandardsPaginateTypeDef]
    ) -> AsyncIterator[DescribeStandardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeStandards.html#SecurityHub.Paginator.DescribeStandards.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describestandardspaginator)
        """

class GetEnabledStandardsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetEnabledStandards.html#SecurityHub.Paginator.GetEnabledStandards)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getenabledstandardspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetEnabledStandardsRequestGetEnabledStandardsPaginateTypeDef]
    ) -> AsyncIterator[GetEnabledStandardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetEnabledStandards.html#SecurityHub.Paginator.GetEnabledStandards.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getenabledstandardspaginator)
        """

class GetFindingHistoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetFindingHistory.html#SecurityHub.Paginator.GetFindingHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getfindinghistorypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetFindingHistoryRequestGetFindingHistoryPaginateTypeDef]
    ) -> AsyncIterator[GetFindingHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetFindingHistory.html#SecurityHub.Paginator.GetFindingHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getfindinghistorypaginator)
        """

class GetFindingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetFindings.html#SecurityHub.Paginator.GetFindings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getfindingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetFindingsRequestGetFindingsPaginateTypeDef]
    ) -> AsyncIterator[GetFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetFindings.html#SecurityHub.Paginator.GetFindings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getfindingspaginator)
        """

class GetInsightsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetInsights.html#SecurityHub.Paginator.GetInsights)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getinsightspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetInsightsRequestGetInsightsPaginateTypeDef]
    ) -> AsyncIterator[GetInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetInsights.html#SecurityHub.Paginator.GetInsights.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getinsightspaginator)
        """

class ListConfigurationPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListConfigurationPolicies.html#SecurityHub.Paginator.ListConfigurationPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listconfigurationpoliciespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListConfigurationPoliciesRequestListConfigurationPoliciesPaginateTypeDef],
    ) -> AsyncIterator[ListConfigurationPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListConfigurationPolicies.html#SecurityHub.Paginator.ListConfigurationPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listconfigurationpoliciespaginator)
        """

class ListConfigurationPolicyAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListConfigurationPolicyAssociations.html#SecurityHub.Paginator.ListConfigurationPolicyAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listconfigurationpolicyassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListConfigurationPolicyAssociationsRequestListConfigurationPolicyAssociationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListConfigurationPolicyAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListConfigurationPolicyAssociations.html#SecurityHub.Paginator.ListConfigurationPolicyAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listconfigurationpolicyassociationspaginator)
        """

class ListEnabledProductsForImportPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListEnabledProductsForImport.html#SecurityHub.Paginator.ListEnabledProductsForImport)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listenabledproductsforimportpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListEnabledProductsForImportRequestListEnabledProductsForImportPaginateTypeDef
        ],
    ) -> AsyncIterator[ListEnabledProductsForImportResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListEnabledProductsForImport.html#SecurityHub.Paginator.ListEnabledProductsForImport.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listenabledproductsforimportpaginator)
        """

class ListFindingAggregatorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListFindingAggregators.html#SecurityHub.Paginator.ListFindingAggregators)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listfindingaggregatorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFindingAggregatorsRequestListFindingAggregatorsPaginateTypeDef]
    ) -> AsyncIterator[ListFindingAggregatorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListFindingAggregators.html#SecurityHub.Paginator.ListFindingAggregators.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listfindingaggregatorspaginator)
        """

class ListInvitationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListInvitations.html#SecurityHub.Paginator.ListInvitations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listinvitationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInvitationsRequestListInvitationsPaginateTypeDef]
    ) -> AsyncIterator[ListInvitationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListInvitations.html#SecurityHub.Paginator.ListInvitations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listinvitationspaginator)
        """

class ListMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListMembers.html#SecurityHub.Paginator.ListMembers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listmemberspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMembersRequestListMembersPaginateTypeDef]
    ) -> AsyncIterator[ListMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListMembers.html#SecurityHub.Paginator.ListMembers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listmemberspaginator)
        """

class ListOrganizationAdminAccountsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListOrganizationAdminAccounts.html#SecurityHub.Paginator.ListOrganizationAdminAccounts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listorganizationadminaccountspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListOrganizationAdminAccountsRequestListOrganizationAdminAccountsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListOrganizationAdminAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListOrganizationAdminAccounts.html#SecurityHub.Paginator.ListOrganizationAdminAccounts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listorganizationadminaccountspaginator)
        """

class ListSecurityControlDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListSecurityControlDefinitions.html#SecurityHub.Paginator.ListSecurityControlDefinitions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listsecuritycontroldefinitionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListSecurityControlDefinitionsRequestListSecurityControlDefinitionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListSecurityControlDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListSecurityControlDefinitions.html#SecurityHub.Paginator.ListSecurityControlDefinitions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listsecuritycontroldefinitionspaginator)
        """

class ListStandardsControlAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListStandardsControlAssociations.html#SecurityHub.Paginator.ListStandardsControlAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#liststandardscontrolassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListStandardsControlAssociationsRequestListStandardsControlAssociationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListStandardsControlAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListStandardsControlAssociations.html#SecurityHub.Paginator.ListStandardsControlAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#liststandardscontrolassociationspaginator)
        """
