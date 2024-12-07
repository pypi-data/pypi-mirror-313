"""
Type annotations for route53-recovery-cluster service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_route53_recovery_cluster.client import Route53RecoveryClusterClient
    from types_aiobotocore_route53_recovery_cluster.paginator import (
        ListRoutingControlsPaginator,
    )

    session = get_session()
    with session.create_client("route53-recovery-cluster") as client:
        client: Route53RecoveryClusterClient

        list_routing_controls_paginator: ListRoutingControlsPaginator = client.get_paginator("list_routing_controls")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListRoutingControlsRequestListRoutingControlsPaginateTypeDef,
    ListRoutingControlsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListRoutingControlsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListRoutingControlsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster/paginator/ListRoutingControls.html#Route53RecoveryCluster.Paginator.ListRoutingControls)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/paginators/#listroutingcontrolspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRoutingControlsRequestListRoutingControlsPaginateTypeDef]
    ) -> AsyncIterator[ListRoutingControlsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster/paginator/ListRoutingControls.html#Route53RecoveryCluster.Paginator.ListRoutingControls.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/paginators/#listroutingcontrolspaginator)
        """
