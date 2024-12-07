"""
Type annotations for elb service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elb.client import ElasticLoadBalancingClient
    from types_aiobotocore_elb.waiter import (
        AnyInstanceInServiceWaiter,
        InstanceDeregisteredWaiter,
        InstanceInServiceWaiter,
    )

    session = get_session()
    async with session.create_client("elb") as client:
        client: ElasticLoadBalancingClient

        any_instance_in_service_waiter: AnyInstanceInServiceWaiter = client.get_waiter("any_instance_in_service")
        instance_deregistered_waiter: InstanceDeregisteredWaiter = client.get_waiter("instance_deregistered")
        instance_in_service_waiter: InstanceInServiceWaiter = client.get_waiter("instance_in_service")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeEndPointStateInputAnyInstanceInServiceWaitTypeDef,
    DescribeEndPointStateInputInstanceDeregisteredWaitTypeDef,
    DescribeEndPointStateInputInstanceInServiceWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("AnyInstanceInServiceWaiter", "InstanceDeregisteredWaiter", "InstanceInServiceWaiter")


class AnyInstanceInServiceWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/waiter/AnyInstanceInService.html#ElasticLoadBalancing.Waiter.AnyInstanceInService)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters/#anyinstanceinservicewaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeEndPointStateInputAnyInstanceInServiceWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/waiter/AnyInstanceInService.html#ElasticLoadBalancing.Waiter.AnyInstanceInService.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters/#anyinstanceinservicewaiter)
        """


class InstanceDeregisteredWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/waiter/InstanceDeregistered.html#ElasticLoadBalancing.Waiter.InstanceDeregistered)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters/#instancederegisteredwaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeEndPointStateInputInstanceDeregisteredWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/waiter/InstanceDeregistered.html#ElasticLoadBalancing.Waiter.InstanceDeregistered.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters/#instancederegisteredwaiter)
        """


class InstanceInServiceWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/waiter/InstanceInService.html#ElasticLoadBalancing.Waiter.InstanceInService)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters/#instanceinservicewaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeEndPointStateInputInstanceInServiceWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/waiter/InstanceInService.html#ElasticLoadBalancing.Waiter.InstanceInService.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters/#instanceinservicewaiter)
        """
