"""
Type annotations for fms service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_fms.client import FMSClient
    from types_aiobotocore_fms.paginator import (
        ListAdminAccountsForOrganizationPaginator,
        ListAdminsManagingAccountPaginator,
        ListAppsListsPaginator,
        ListComplianceStatusPaginator,
        ListMemberAccountsPaginator,
        ListPoliciesPaginator,
        ListProtocolsListsPaginator,
        ListThirdPartyFirewallFirewallPoliciesPaginator,
    )

    session = get_session()
    with session.create_client("fms") as client:
        client: FMSClient

        list_admin_accounts_for_organization_paginator: ListAdminAccountsForOrganizationPaginator = client.get_paginator("list_admin_accounts_for_organization")
        list_admins_managing_account_paginator: ListAdminsManagingAccountPaginator = client.get_paginator("list_admins_managing_account")
        list_apps_lists_paginator: ListAppsListsPaginator = client.get_paginator("list_apps_lists")
        list_compliance_status_paginator: ListComplianceStatusPaginator = client.get_paginator("list_compliance_status")
        list_member_accounts_paginator: ListMemberAccountsPaginator = client.get_paginator("list_member_accounts")
        list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
        list_protocols_lists_paginator: ListProtocolsListsPaginator = client.get_paginator("list_protocols_lists")
        list_third_party_firewall_firewall_policies_paginator: ListThirdPartyFirewallFirewallPoliciesPaginator = client.get_paginator("list_third_party_firewall_firewall_policies")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAdminAccountsForOrganizationRequestListAdminAccountsForOrganizationPaginateTypeDef,
    ListAdminAccountsForOrganizationResponseTypeDef,
    ListAdminsManagingAccountRequestListAdminsManagingAccountPaginateTypeDef,
    ListAdminsManagingAccountResponseTypeDef,
    ListAppsListsRequestListAppsListsPaginateTypeDef,
    ListAppsListsResponseTypeDef,
    ListComplianceStatusRequestListComplianceStatusPaginateTypeDef,
    ListComplianceStatusResponseTypeDef,
    ListMemberAccountsRequestListMemberAccountsPaginateTypeDef,
    ListMemberAccountsResponseTypeDef,
    ListPoliciesRequestListPoliciesPaginateTypeDef,
    ListPoliciesResponseTypeDef,
    ListProtocolsListsRequestListProtocolsListsPaginateTypeDef,
    ListProtocolsListsResponseTypeDef,
    ListThirdPartyFirewallFirewallPoliciesRequestListThirdPartyFirewallFirewallPoliciesPaginateTypeDef,
    ListThirdPartyFirewallFirewallPoliciesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAdminAccountsForOrganizationPaginator",
    "ListAdminsManagingAccountPaginator",
    "ListAppsListsPaginator",
    "ListComplianceStatusPaginator",
    "ListMemberAccountsPaginator",
    "ListPoliciesPaginator",
    "ListProtocolsListsPaginator",
    "ListThirdPartyFirewallFirewallPoliciesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAdminAccountsForOrganizationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAdminAccountsForOrganization.html#FMS.Paginator.ListAdminAccountsForOrganization)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listadminaccountsfororganizationpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListAdminAccountsForOrganizationRequestListAdminAccountsForOrganizationPaginateTypeDef
        ],
    ) -> AsyncIterator[ListAdminAccountsForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAdminAccountsForOrganization.html#FMS.Paginator.ListAdminAccountsForOrganization.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listadminaccountsfororganizationpaginator)
        """


class ListAdminsManagingAccountPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAdminsManagingAccount.html#FMS.Paginator.ListAdminsManagingAccount)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listadminsmanagingaccountpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListAdminsManagingAccountRequestListAdminsManagingAccountPaginateTypeDef],
    ) -> AsyncIterator[ListAdminsManagingAccountResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAdminsManagingAccount.html#FMS.Paginator.ListAdminsManagingAccount.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listadminsmanagingaccountpaginator)
        """


class ListAppsListsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAppsLists.html#FMS.Paginator.ListAppsLists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listappslistspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAppsListsRequestListAppsListsPaginateTypeDef]
    ) -> AsyncIterator[ListAppsListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAppsLists.html#FMS.Paginator.ListAppsLists.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listappslistspaginator)
        """


class ListComplianceStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListComplianceStatus.html#FMS.Paginator.ListComplianceStatus)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listcompliancestatuspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListComplianceStatusRequestListComplianceStatusPaginateTypeDef]
    ) -> AsyncIterator[ListComplianceStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListComplianceStatus.html#FMS.Paginator.ListComplianceStatus.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listcompliancestatuspaginator)
        """


class ListMemberAccountsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListMemberAccounts.html#FMS.Paginator.ListMemberAccounts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listmemberaccountspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMemberAccountsRequestListMemberAccountsPaginateTypeDef]
    ) -> AsyncIterator[ListMemberAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListMemberAccounts.html#FMS.Paginator.ListMemberAccounts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listmemberaccountspaginator)
        """


class ListPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListPolicies.html#FMS.Paginator.ListPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listpoliciespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPoliciesRequestListPoliciesPaginateTypeDef]
    ) -> AsyncIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListPolicies.html#FMS.Paginator.ListPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listpoliciespaginator)
        """


class ListProtocolsListsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListProtocolsLists.html#FMS.Paginator.ListProtocolsLists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listprotocolslistspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListProtocolsListsRequestListProtocolsListsPaginateTypeDef]
    ) -> AsyncIterator[ListProtocolsListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListProtocolsLists.html#FMS.Paginator.ListProtocolsLists.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listprotocolslistspaginator)
        """


class ListThirdPartyFirewallFirewallPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListThirdPartyFirewallFirewallPolicies.html#FMS.Paginator.ListThirdPartyFirewallFirewallPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listthirdpartyfirewallfirewallpoliciespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListThirdPartyFirewallFirewallPoliciesRequestListThirdPartyFirewallFirewallPoliciesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListThirdPartyFirewallFirewallPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListThirdPartyFirewallFirewallPolicies.html#FMS.Paginator.ListThirdPartyFirewallFirewallPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listthirdpartyfirewallfirewallpoliciespaginator)
        """
