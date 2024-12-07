"""
Type annotations for opsworkscm service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworkscm/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_opsworkscm.client import OpsWorksCMClient
    from types_aiobotocore_opsworkscm.waiter import (
        NodeAssociatedWaiter,
    )

    session = get_session()
    async with session.create_client("opsworkscm") as client:
        client: OpsWorksCMClient

        node_associated_waiter: NodeAssociatedWaiter = client.get_waiter("node_associated")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import DescribeNodeAssociationStatusRequestNodeAssociatedWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("NodeAssociatedWaiter",)


class NodeAssociatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworkscm/waiter/NodeAssociated.html#OpsWorksCM.Waiter.NodeAssociated)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworkscm/waiters/#nodeassociatedwaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeNodeAssociationStatusRequestNodeAssociatedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworkscm/waiter/NodeAssociated.html#OpsWorksCM.Waiter.NodeAssociated.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworkscm/waiters/#nodeassociatedwaiter)
        """
