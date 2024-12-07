"""
Type annotations for eks service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_eks.client import EKSClient
    from types_aiobotocore_eks.paginator import (
        DescribeAddonVersionsPaginator,
        ListAccessEntriesPaginator,
        ListAccessPoliciesPaginator,
        ListAddonsPaginator,
        ListAssociatedAccessPoliciesPaginator,
        ListClustersPaginator,
        ListEksAnywhereSubscriptionsPaginator,
        ListFargateProfilesPaginator,
        ListIdentityProviderConfigsPaginator,
        ListInsightsPaginator,
        ListNodegroupsPaginator,
        ListPodIdentityAssociationsPaginator,
        ListUpdatesPaginator,
    )

    session = get_session()
    with session.create_client("eks") as client:
        client: EKSClient

        describe_addon_versions_paginator: DescribeAddonVersionsPaginator = client.get_paginator("describe_addon_versions")
        list_access_entries_paginator: ListAccessEntriesPaginator = client.get_paginator("list_access_entries")
        list_access_policies_paginator: ListAccessPoliciesPaginator = client.get_paginator("list_access_policies")
        list_addons_paginator: ListAddonsPaginator = client.get_paginator("list_addons")
        list_associated_access_policies_paginator: ListAssociatedAccessPoliciesPaginator = client.get_paginator("list_associated_access_policies")
        list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
        list_eks_anywhere_subscriptions_paginator: ListEksAnywhereSubscriptionsPaginator = client.get_paginator("list_eks_anywhere_subscriptions")
        list_fargate_profiles_paginator: ListFargateProfilesPaginator = client.get_paginator("list_fargate_profiles")
        list_identity_provider_configs_paginator: ListIdentityProviderConfigsPaginator = client.get_paginator("list_identity_provider_configs")
        list_insights_paginator: ListInsightsPaginator = client.get_paginator("list_insights")
        list_nodegroups_paginator: ListNodegroupsPaginator = client.get_paginator("list_nodegroups")
        list_pod_identity_associations_paginator: ListPodIdentityAssociationsPaginator = client.get_paginator("list_pod_identity_associations")
        list_updates_paginator: ListUpdatesPaginator = client.get_paginator("list_updates")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeAddonVersionsRequestDescribeAddonVersionsPaginateTypeDef,
    DescribeAddonVersionsResponseTypeDef,
    ListAccessEntriesRequestListAccessEntriesPaginateTypeDef,
    ListAccessEntriesResponseTypeDef,
    ListAccessPoliciesRequestListAccessPoliciesPaginateTypeDef,
    ListAccessPoliciesResponseTypeDef,
    ListAddonsRequestListAddonsPaginateTypeDef,
    ListAddonsResponseTypeDef,
    ListAssociatedAccessPoliciesRequestListAssociatedAccessPoliciesPaginateTypeDef,
    ListAssociatedAccessPoliciesResponseTypeDef,
    ListClustersRequestListClustersPaginateTypeDef,
    ListClustersResponseTypeDef,
    ListEksAnywhereSubscriptionsRequestListEksAnywhereSubscriptionsPaginateTypeDef,
    ListEksAnywhereSubscriptionsResponseTypeDef,
    ListFargateProfilesRequestListFargateProfilesPaginateTypeDef,
    ListFargateProfilesResponseTypeDef,
    ListIdentityProviderConfigsRequestListIdentityProviderConfigsPaginateTypeDef,
    ListIdentityProviderConfigsResponseTypeDef,
    ListInsightsRequestListInsightsPaginateTypeDef,
    ListInsightsResponseTypeDef,
    ListNodegroupsRequestListNodegroupsPaginateTypeDef,
    ListNodegroupsResponseTypeDef,
    ListPodIdentityAssociationsRequestListPodIdentityAssociationsPaginateTypeDef,
    ListPodIdentityAssociationsResponseTypeDef,
    ListUpdatesRequestListUpdatesPaginateTypeDef,
    ListUpdatesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeAddonVersionsPaginator",
    "ListAccessEntriesPaginator",
    "ListAccessPoliciesPaginator",
    "ListAddonsPaginator",
    "ListAssociatedAccessPoliciesPaginator",
    "ListClustersPaginator",
    "ListEksAnywhereSubscriptionsPaginator",
    "ListFargateProfilesPaginator",
    "ListIdentityProviderConfigsPaginator",
    "ListInsightsPaginator",
    "ListNodegroupsPaginator",
    "ListPodIdentityAssociationsPaginator",
    "ListUpdatesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeAddonVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/DescribeAddonVersions.html#EKS.Paginator.DescribeAddonVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#describeaddonversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeAddonVersionsRequestDescribeAddonVersionsPaginateTypeDef]
    ) -> AsyncIterator[DescribeAddonVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/DescribeAddonVersions.html#EKS.Paginator.DescribeAddonVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#describeaddonversionspaginator)
        """

class ListAccessEntriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAccessEntries.html#EKS.Paginator.ListAccessEntries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listaccessentriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAccessEntriesRequestListAccessEntriesPaginateTypeDef]
    ) -> AsyncIterator[ListAccessEntriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAccessEntries.html#EKS.Paginator.ListAccessEntries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listaccessentriespaginator)
        """

class ListAccessPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAccessPolicies.html#EKS.Paginator.ListAccessPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listaccesspoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAccessPoliciesRequestListAccessPoliciesPaginateTypeDef]
    ) -> AsyncIterator[ListAccessPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAccessPolicies.html#EKS.Paginator.ListAccessPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listaccesspoliciespaginator)
        """

class ListAddonsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAddons.html#EKS.Paginator.ListAddons)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listaddonspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAddonsRequestListAddonsPaginateTypeDef]
    ) -> AsyncIterator[ListAddonsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAddons.html#EKS.Paginator.ListAddons.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listaddonspaginator)
        """

class ListAssociatedAccessPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAssociatedAccessPolicies.html#EKS.Paginator.ListAssociatedAccessPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listassociatedaccesspoliciespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAssociatedAccessPoliciesRequestListAssociatedAccessPoliciesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListAssociatedAccessPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAssociatedAccessPolicies.html#EKS.Paginator.ListAssociatedAccessPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listassociatedaccesspoliciespaginator)
        """

class ListClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListClusters.html#EKS.Paginator.ListClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListClustersRequestListClustersPaginateTypeDef]
    ) -> AsyncIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListClusters.html#EKS.Paginator.ListClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listclusterspaginator)
        """

class ListEksAnywhereSubscriptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListEksAnywhereSubscriptions.html#EKS.Paginator.ListEksAnywhereSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listeksanywheresubscriptionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListEksAnywhereSubscriptionsRequestListEksAnywhereSubscriptionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListEksAnywhereSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListEksAnywhereSubscriptions.html#EKS.Paginator.ListEksAnywhereSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listeksanywheresubscriptionspaginator)
        """

class ListFargateProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListFargateProfiles.html#EKS.Paginator.ListFargateProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listfargateprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFargateProfilesRequestListFargateProfilesPaginateTypeDef]
    ) -> AsyncIterator[ListFargateProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListFargateProfiles.html#EKS.Paginator.ListFargateProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listfargateprofilespaginator)
        """

class ListIdentityProviderConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListIdentityProviderConfigs.html#EKS.Paginator.ListIdentityProviderConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listidentityproviderconfigspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListIdentityProviderConfigsRequestListIdentityProviderConfigsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListIdentityProviderConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListIdentityProviderConfigs.html#EKS.Paginator.ListIdentityProviderConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listidentityproviderconfigspaginator)
        """

class ListInsightsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListInsights.html#EKS.Paginator.ListInsights)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listinsightspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInsightsRequestListInsightsPaginateTypeDef]
    ) -> AsyncIterator[ListInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListInsights.html#EKS.Paginator.ListInsights.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listinsightspaginator)
        """

class ListNodegroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListNodegroups.html#EKS.Paginator.ListNodegroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listnodegroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListNodegroupsRequestListNodegroupsPaginateTypeDef]
    ) -> AsyncIterator[ListNodegroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListNodegroups.html#EKS.Paginator.ListNodegroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listnodegroupspaginator)
        """

class ListPodIdentityAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListPodIdentityAssociations.html#EKS.Paginator.ListPodIdentityAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listpodidentityassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListPodIdentityAssociationsRequestListPodIdentityAssociationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListPodIdentityAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListPodIdentityAssociations.html#EKS.Paginator.ListPodIdentityAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listpodidentityassociationspaginator)
        """

class ListUpdatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListUpdates.html#EKS.Paginator.ListUpdates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listupdatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUpdatesRequestListUpdatesPaginateTypeDef]
    ) -> AsyncIterator[ListUpdatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListUpdates.html#EKS.Paginator.ListUpdates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listupdatespaginator)
        """
