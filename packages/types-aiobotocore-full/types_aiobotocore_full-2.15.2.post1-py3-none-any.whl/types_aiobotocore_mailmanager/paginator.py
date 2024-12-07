"""
Type annotations for mailmanager service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mailmanager.client import MailManagerClient
    from types_aiobotocore_mailmanager.paginator import (
        ListAddonInstancesPaginator,
        ListAddonSubscriptionsPaginator,
        ListArchiveExportsPaginator,
        ListArchiveSearchesPaginator,
        ListArchivesPaginator,
        ListIngressPointsPaginator,
        ListRelaysPaginator,
        ListRuleSetsPaginator,
        ListTrafficPoliciesPaginator,
    )

    session = get_session()
    with session.create_client("mailmanager") as client:
        client: MailManagerClient

        list_addon_instances_paginator: ListAddonInstancesPaginator = client.get_paginator("list_addon_instances")
        list_addon_subscriptions_paginator: ListAddonSubscriptionsPaginator = client.get_paginator("list_addon_subscriptions")
        list_archive_exports_paginator: ListArchiveExportsPaginator = client.get_paginator("list_archive_exports")
        list_archive_searches_paginator: ListArchiveSearchesPaginator = client.get_paginator("list_archive_searches")
        list_archives_paginator: ListArchivesPaginator = client.get_paginator("list_archives")
        list_ingress_points_paginator: ListIngressPointsPaginator = client.get_paginator("list_ingress_points")
        list_relays_paginator: ListRelaysPaginator = client.get_paginator("list_relays")
        list_rule_sets_paginator: ListRuleSetsPaginator = client.get_paginator("list_rule_sets")
        list_traffic_policies_paginator: ListTrafficPoliciesPaginator = client.get_paginator("list_traffic_policies")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAddonInstancesRequestListAddonInstancesPaginateTypeDef,
    ListAddonInstancesResponseTypeDef,
    ListAddonSubscriptionsRequestListAddonSubscriptionsPaginateTypeDef,
    ListAddonSubscriptionsResponseTypeDef,
    ListArchiveExportsRequestListArchiveExportsPaginateTypeDef,
    ListArchiveExportsResponseTypeDef,
    ListArchiveSearchesRequestListArchiveSearchesPaginateTypeDef,
    ListArchiveSearchesResponseTypeDef,
    ListArchivesRequestListArchivesPaginateTypeDef,
    ListArchivesResponseTypeDef,
    ListIngressPointsRequestListIngressPointsPaginateTypeDef,
    ListIngressPointsResponseTypeDef,
    ListRelaysRequestListRelaysPaginateTypeDef,
    ListRelaysResponseTypeDef,
    ListRuleSetsRequestListRuleSetsPaginateTypeDef,
    ListRuleSetsResponseTypeDef,
    ListTrafficPoliciesRequestListTrafficPoliciesPaginateTypeDef,
    ListTrafficPoliciesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAddonInstancesPaginator",
    "ListAddonSubscriptionsPaginator",
    "ListArchiveExportsPaginator",
    "ListArchiveSearchesPaginator",
    "ListArchivesPaginator",
    "ListIngressPointsPaginator",
    "ListRelaysPaginator",
    "ListRuleSetsPaginator",
    "ListTrafficPoliciesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAddonInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListAddonInstances.html#MailManager.Paginator.ListAddonInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listaddoninstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAddonInstancesRequestListAddonInstancesPaginateTypeDef]
    ) -> AsyncIterator[ListAddonInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListAddonInstances.html#MailManager.Paginator.ListAddonInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listaddoninstancespaginator)
        """


class ListAddonSubscriptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListAddonSubscriptions.html#MailManager.Paginator.ListAddonSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listaddonsubscriptionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAddonSubscriptionsRequestListAddonSubscriptionsPaginateTypeDef]
    ) -> AsyncIterator[ListAddonSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListAddonSubscriptions.html#MailManager.Paginator.ListAddonSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listaddonsubscriptionspaginator)
        """


class ListArchiveExportsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchiveExports.html#MailManager.Paginator.ListArchiveExports)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listarchiveexportspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListArchiveExportsRequestListArchiveExportsPaginateTypeDef]
    ) -> AsyncIterator[ListArchiveExportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchiveExports.html#MailManager.Paginator.ListArchiveExports.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listarchiveexportspaginator)
        """


class ListArchiveSearchesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchiveSearches.html#MailManager.Paginator.ListArchiveSearches)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listarchivesearchespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListArchiveSearchesRequestListArchiveSearchesPaginateTypeDef]
    ) -> AsyncIterator[ListArchiveSearchesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchiveSearches.html#MailManager.Paginator.ListArchiveSearches.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listarchivesearchespaginator)
        """


class ListArchivesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchives.html#MailManager.Paginator.ListArchives)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listarchivespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListArchivesRequestListArchivesPaginateTypeDef]
    ) -> AsyncIterator[ListArchivesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchives.html#MailManager.Paginator.ListArchives.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listarchivespaginator)
        """


class ListIngressPointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListIngressPoints.html#MailManager.Paginator.ListIngressPoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listingresspointspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListIngressPointsRequestListIngressPointsPaginateTypeDef]
    ) -> AsyncIterator[ListIngressPointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListIngressPoints.html#MailManager.Paginator.ListIngressPoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listingresspointspaginator)
        """


class ListRelaysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListRelays.html#MailManager.Paginator.ListRelays)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listrelayspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRelaysRequestListRelaysPaginateTypeDef]
    ) -> AsyncIterator[ListRelaysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListRelays.html#MailManager.Paginator.ListRelays.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listrelayspaginator)
        """


class ListRuleSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListRuleSets.html#MailManager.Paginator.ListRuleSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listrulesetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRuleSetsRequestListRuleSetsPaginateTypeDef]
    ) -> AsyncIterator[ListRuleSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListRuleSets.html#MailManager.Paginator.ListRuleSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listrulesetspaginator)
        """


class ListTrafficPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListTrafficPolicies.html#MailManager.Paginator.ListTrafficPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listtrafficpoliciespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTrafficPoliciesRequestListTrafficPoliciesPaginateTypeDef]
    ) -> AsyncIterator[ListTrafficPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListTrafficPolicies.html#MailManager.Paginator.ListTrafficPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listtrafficpoliciespaginator)
        """
