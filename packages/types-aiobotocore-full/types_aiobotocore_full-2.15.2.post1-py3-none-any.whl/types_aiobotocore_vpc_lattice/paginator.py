"""
Type annotations for vpc-lattice service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_vpc_lattice.client import VPCLatticeClient
    from types_aiobotocore_vpc_lattice.paginator import (
        ListAccessLogSubscriptionsPaginator,
        ListListenersPaginator,
        ListRulesPaginator,
        ListServiceNetworkServiceAssociationsPaginator,
        ListServiceNetworkVpcAssociationsPaginator,
        ListServiceNetworksPaginator,
        ListServicesPaginator,
        ListTargetGroupsPaginator,
        ListTargetsPaginator,
    )

    session = get_session()
    with session.create_client("vpc-lattice") as client:
        client: VPCLatticeClient

        list_access_log_subscriptions_paginator: ListAccessLogSubscriptionsPaginator = client.get_paginator("list_access_log_subscriptions")
        list_listeners_paginator: ListListenersPaginator = client.get_paginator("list_listeners")
        list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
        list_service_network_service_associations_paginator: ListServiceNetworkServiceAssociationsPaginator = client.get_paginator("list_service_network_service_associations")
        list_service_network_vpc_associations_paginator: ListServiceNetworkVpcAssociationsPaginator = client.get_paginator("list_service_network_vpc_associations")
        list_service_networks_paginator: ListServiceNetworksPaginator = client.get_paginator("list_service_networks")
        list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
        list_target_groups_paginator: ListTargetGroupsPaginator = client.get_paginator("list_target_groups")
        list_targets_paginator: ListTargetsPaginator = client.get_paginator("list_targets")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAccessLogSubscriptionsRequestListAccessLogSubscriptionsPaginateTypeDef,
    ListAccessLogSubscriptionsResponseTypeDef,
    ListListenersRequestListListenersPaginateTypeDef,
    ListListenersResponseTypeDef,
    ListRulesRequestListRulesPaginateTypeDef,
    ListRulesResponseTypeDef,
    ListServiceNetworkServiceAssociationsRequestListServiceNetworkServiceAssociationsPaginateTypeDef,
    ListServiceNetworkServiceAssociationsResponseTypeDef,
    ListServiceNetworksRequestListServiceNetworksPaginateTypeDef,
    ListServiceNetworksResponseTypeDef,
    ListServiceNetworkVpcAssociationsRequestListServiceNetworkVpcAssociationsPaginateTypeDef,
    ListServiceNetworkVpcAssociationsResponseTypeDef,
    ListServicesRequestListServicesPaginateTypeDef,
    ListServicesResponseTypeDef,
    ListTargetGroupsRequestListTargetGroupsPaginateTypeDef,
    ListTargetGroupsResponseTypeDef,
    ListTargetsRequestListTargetsPaginateTypeDef,
    ListTargetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAccessLogSubscriptionsPaginator",
    "ListListenersPaginator",
    "ListRulesPaginator",
    "ListServiceNetworkServiceAssociationsPaginator",
    "ListServiceNetworkVpcAssociationsPaginator",
    "ListServiceNetworksPaginator",
    "ListServicesPaginator",
    "ListTargetGroupsPaginator",
    "ListTargetsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAccessLogSubscriptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListAccessLogSubscriptions.html#VPCLattice.Paginator.ListAccessLogSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listaccesslogsubscriptionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListAccessLogSubscriptionsRequestListAccessLogSubscriptionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListAccessLogSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListAccessLogSubscriptions.html#VPCLattice.Paginator.ListAccessLogSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listaccesslogsubscriptionspaginator)
        """


class ListListenersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListListeners.html#VPCLattice.Paginator.ListListeners)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listlistenerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListListenersRequestListListenersPaginateTypeDef]
    ) -> AsyncIterator[ListListenersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListListeners.html#VPCLattice.Paginator.ListListeners.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listlistenerspaginator)
        """


class ListRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListRules.html#VPCLattice.Paginator.ListRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listrulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRulesRequestListRulesPaginateTypeDef]
    ) -> AsyncIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListRules.html#VPCLattice.Paginator.ListRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listrulespaginator)
        """


class ListServiceNetworkServiceAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkServiceAssociations.html#VPCLattice.Paginator.ListServiceNetworkServiceAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicenetworkserviceassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListServiceNetworkServiceAssociationsRequestListServiceNetworkServiceAssociationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListServiceNetworkServiceAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkServiceAssociations.html#VPCLattice.Paginator.ListServiceNetworkServiceAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicenetworkserviceassociationspaginator)
        """


class ListServiceNetworkVpcAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkVpcAssociations.html#VPCLattice.Paginator.ListServiceNetworkVpcAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicenetworkvpcassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListServiceNetworkVpcAssociationsRequestListServiceNetworkVpcAssociationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListServiceNetworkVpcAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkVpcAssociations.html#VPCLattice.Paginator.ListServiceNetworkVpcAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicenetworkvpcassociationspaginator)
        """


class ListServiceNetworksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworks.html#VPCLattice.Paginator.ListServiceNetworks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicenetworkspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListServiceNetworksRequestListServiceNetworksPaginateTypeDef]
    ) -> AsyncIterator[ListServiceNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworks.html#VPCLattice.Paginator.ListServiceNetworks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicenetworkspaginator)
        """


class ListServicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServices.html#VPCLattice.Paginator.ListServices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListServicesRequestListServicesPaginateTypeDef]
    ) -> AsyncIterator[ListServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServices.html#VPCLattice.Paginator.ListServices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicespaginator)
        """


class ListTargetGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListTargetGroups.html#VPCLattice.Paginator.ListTargetGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listtargetgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTargetGroupsRequestListTargetGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListTargetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListTargetGroups.html#VPCLattice.Paginator.ListTargetGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listtargetgroupspaginator)
        """


class ListTargetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListTargets.html#VPCLattice.Paginator.ListTargets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listtargetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTargetsRequestListTargetsPaginateTypeDef]
    ) -> AsyncIterator[ListTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListTargets.html#VPCLattice.Paginator.ListTargets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listtargetspaginator)
        """
