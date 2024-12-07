"""
Type annotations for emr service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_emr.client import EMRClient
    from types_aiobotocore_emr.waiter import (
        ClusterRunningWaiter,
        ClusterTerminatedWaiter,
        StepCompleteWaiter,
    )

    session = get_session()
    async with session.create_client("emr") as client:
        client: EMRClient

        cluster_running_waiter: ClusterRunningWaiter = client.get_waiter("cluster_running")
        cluster_terminated_waiter: ClusterTerminatedWaiter = client.get_waiter("cluster_terminated")
        step_complete_waiter: StepCompleteWaiter = client.get_waiter("step_complete")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeClusterInputClusterRunningWaitTypeDef,
    DescribeClusterInputClusterTerminatedWaitTypeDef,
    DescribeStepInputStepCompleteWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ClusterRunningWaiter", "ClusterTerminatedWaiter", "StepCompleteWaiter")


class ClusterRunningWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/waiter/ClusterRunning.html#EMR.Waiter.ClusterRunning)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/waiters/#clusterrunningwaiter)
    """

    async def wait(self, **kwargs: Unpack[DescribeClusterInputClusterRunningWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/waiter/ClusterRunning.html#EMR.Waiter.ClusterRunning.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/waiters/#clusterrunningwaiter)
        """


class ClusterTerminatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/waiter/ClusterTerminated.html#EMR.Waiter.ClusterTerminated)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/waiters/#clusterterminatedwaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeClusterInputClusterTerminatedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/waiter/ClusterTerminated.html#EMR.Waiter.ClusterTerminated.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/waiters/#clusterterminatedwaiter)
        """


class StepCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/waiter/StepComplete.html#EMR.Waiter.StepComplete)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/waiters/#stepcompletewaiter)
    """

    async def wait(self, **kwargs: Unpack[DescribeStepInputStepCompleteWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/waiter/StepComplete.html#EMR.Waiter.StepComplete.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/waiters/#stepcompletewaiter)
        """
