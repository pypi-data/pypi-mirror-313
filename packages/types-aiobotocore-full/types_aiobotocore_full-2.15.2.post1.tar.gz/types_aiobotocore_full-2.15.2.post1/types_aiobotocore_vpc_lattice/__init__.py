"""
Main interface for vpc-lattice service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_vpc_lattice import (
        Client,
        ListAccessLogSubscriptionsPaginator,
        ListListenersPaginator,
        ListRulesPaginator,
        ListServiceNetworkServiceAssociationsPaginator,
        ListServiceNetworkVpcAssociationsPaginator,
        ListServiceNetworksPaginator,
        ListServicesPaginator,
        ListTargetGroupsPaginator,
        ListTargetsPaginator,
        VPCLatticeClient,
    )

    session = get_session()
    async with session.create_client("vpc-lattice") as client:
        client: VPCLatticeClient
        ...


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

from .client import VPCLatticeClient
from .paginator import (
    ListAccessLogSubscriptionsPaginator,
    ListListenersPaginator,
    ListRulesPaginator,
    ListServiceNetworkServiceAssociationsPaginator,
    ListServiceNetworksPaginator,
    ListServiceNetworkVpcAssociationsPaginator,
    ListServicesPaginator,
    ListTargetGroupsPaginator,
    ListTargetsPaginator,
)

Client = VPCLatticeClient


__all__ = (
    "Client",
    "ListAccessLogSubscriptionsPaginator",
    "ListListenersPaginator",
    "ListRulesPaginator",
    "ListServiceNetworkServiceAssociationsPaginator",
    "ListServiceNetworkVpcAssociationsPaginator",
    "ListServiceNetworksPaginator",
    "ListServicesPaginator",
    "ListTargetGroupsPaginator",
    "ListTargetsPaginator",
    "VPCLatticeClient",
)
