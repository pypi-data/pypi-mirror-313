"""
Type annotations for dms service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_dms.client import DatabaseMigrationServiceClient
    from types_aiobotocore_dms.waiter import (
        EndpointDeletedWaiter,
        ReplicationInstanceAvailableWaiter,
        ReplicationInstanceDeletedWaiter,
        ReplicationTaskDeletedWaiter,
        ReplicationTaskReadyWaiter,
        ReplicationTaskRunningWaiter,
        ReplicationTaskStoppedWaiter,
        TestConnectionSucceedsWaiter,
    )

    session = get_session()
    async with session.create_client("dms") as client:
        client: DatabaseMigrationServiceClient

        endpoint_deleted_waiter: EndpointDeletedWaiter = client.get_waiter("endpoint_deleted")
        replication_instance_available_waiter: ReplicationInstanceAvailableWaiter = client.get_waiter("replication_instance_available")
        replication_instance_deleted_waiter: ReplicationInstanceDeletedWaiter = client.get_waiter("replication_instance_deleted")
        replication_task_deleted_waiter: ReplicationTaskDeletedWaiter = client.get_waiter("replication_task_deleted")
        replication_task_ready_waiter: ReplicationTaskReadyWaiter = client.get_waiter("replication_task_ready")
        replication_task_running_waiter: ReplicationTaskRunningWaiter = client.get_waiter("replication_task_running")
        replication_task_stopped_waiter: ReplicationTaskStoppedWaiter = client.get_waiter("replication_task_stopped")
        test_connection_succeeds_waiter: TestConnectionSucceedsWaiter = client.get_waiter("test_connection_succeeds")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeConnectionsMessageTestConnectionSucceedsWaitTypeDef,
    DescribeEndpointsMessageEndpointDeletedWaitTypeDef,
    DescribeReplicationInstancesMessageReplicationInstanceAvailableWaitTypeDef,
    DescribeReplicationInstancesMessageReplicationInstanceDeletedWaitTypeDef,
    DescribeReplicationTasksMessageReplicationTaskDeletedWaitTypeDef,
    DescribeReplicationTasksMessageReplicationTaskReadyWaitTypeDef,
    DescribeReplicationTasksMessageReplicationTaskRunningWaitTypeDef,
    DescribeReplicationTasksMessageReplicationTaskStoppedWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "EndpointDeletedWaiter",
    "ReplicationInstanceAvailableWaiter",
    "ReplicationInstanceDeletedWaiter",
    "ReplicationTaskDeletedWaiter",
    "ReplicationTaskReadyWaiter",
    "ReplicationTaskRunningWaiter",
    "ReplicationTaskStoppedWaiter",
    "TestConnectionSucceedsWaiter",
)


class EndpointDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/EndpointDeleted.html#DatabaseMigrationService.Waiter.EndpointDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#endpointdeletedwaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeEndpointsMessageEndpointDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/EndpointDeleted.html#DatabaseMigrationService.Waiter.EndpointDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#endpointdeletedwaiter)
        """


class ReplicationInstanceAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationInstanceAvailable.html#DatabaseMigrationService.Waiter.ReplicationInstanceAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationinstanceavailablewaiter)
    """

    async def wait(
        self,
        **kwargs: Unpack[
            DescribeReplicationInstancesMessageReplicationInstanceAvailableWaitTypeDef
        ],
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationInstanceAvailable.html#DatabaseMigrationService.Waiter.ReplicationInstanceAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationinstanceavailablewaiter)
        """


class ReplicationInstanceDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationInstanceDeleted.html#DatabaseMigrationService.Waiter.ReplicationInstanceDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationinstancedeletedwaiter)
    """

    async def wait(
        self,
        **kwargs: Unpack[DescribeReplicationInstancesMessageReplicationInstanceDeletedWaitTypeDef],
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationInstanceDeleted.html#DatabaseMigrationService.Waiter.ReplicationInstanceDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationinstancedeletedwaiter)
        """


class ReplicationTaskDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskDeleted.html#DatabaseMigrationService.Waiter.ReplicationTaskDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskdeletedwaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeReplicationTasksMessageReplicationTaskDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskDeleted.html#DatabaseMigrationService.Waiter.ReplicationTaskDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskdeletedwaiter)
        """


class ReplicationTaskReadyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskReady.html#DatabaseMigrationService.Waiter.ReplicationTaskReady)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskreadywaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeReplicationTasksMessageReplicationTaskReadyWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskReady.html#DatabaseMigrationService.Waiter.ReplicationTaskReady.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskreadywaiter)
        """


class ReplicationTaskRunningWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskRunning.html#DatabaseMigrationService.Waiter.ReplicationTaskRunning)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskrunningwaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeReplicationTasksMessageReplicationTaskRunningWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskRunning.html#DatabaseMigrationService.Waiter.ReplicationTaskRunning.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskrunningwaiter)
        """


class ReplicationTaskStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskStopped.html#DatabaseMigrationService.Waiter.ReplicationTaskStopped)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskstoppedwaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeReplicationTasksMessageReplicationTaskStoppedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskStopped.html#DatabaseMigrationService.Waiter.ReplicationTaskStopped.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskstoppedwaiter)
        """


class TestConnectionSucceedsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/TestConnectionSucceeds.html#DatabaseMigrationService.Waiter.TestConnectionSucceeds)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#testconnectionsucceedswaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeConnectionsMessageTestConnectionSucceedsWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/TestConnectionSucceeds.html#DatabaseMigrationService.Waiter.TestConnectionSucceeds.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#testconnectionsucceedswaiter)
        """
