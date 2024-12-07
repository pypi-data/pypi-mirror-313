"""
Type annotations for redshift service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_redshift.client import RedshiftClient
    from types_aiobotocore_redshift.waiter import (
        ClusterAvailableWaiter,
        ClusterDeletedWaiter,
        ClusterRestoredWaiter,
        SnapshotAvailableWaiter,
    )

    session = get_session()
    async with session.create_client("redshift") as client:
        client: RedshiftClient

        cluster_available_waiter: ClusterAvailableWaiter = client.get_waiter("cluster_available")
        cluster_deleted_waiter: ClusterDeletedWaiter = client.get_waiter("cluster_deleted")
        cluster_restored_waiter: ClusterRestoredWaiter = client.get_waiter("cluster_restored")
        snapshot_available_waiter: SnapshotAvailableWaiter = client.get_waiter("snapshot_available")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeClustersMessageClusterAvailableWaitTypeDef,
    DescribeClustersMessageClusterDeletedWaitTypeDef,
    DescribeClustersMessageClusterRestoredWaitTypeDef,
    DescribeClusterSnapshotsMessageSnapshotAvailableWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ClusterAvailableWaiter",
    "ClusterDeletedWaiter",
    "ClusterRestoredWaiter",
    "SnapshotAvailableWaiter",
)


class ClusterAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/waiter/ClusterAvailable.html#Redshift.Waiter.ClusterAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/#clusteravailablewaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeClustersMessageClusterAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/waiter/ClusterAvailable.html#Redshift.Waiter.ClusterAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/#clusteravailablewaiter)
        """


class ClusterDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/waiter/ClusterDeleted.html#Redshift.Waiter.ClusterDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/#clusterdeletedwaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeClustersMessageClusterDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/waiter/ClusterDeleted.html#Redshift.Waiter.ClusterDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/#clusterdeletedwaiter)
        """


class ClusterRestoredWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/waiter/ClusterRestored.html#Redshift.Waiter.ClusterRestored)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/#clusterrestoredwaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeClustersMessageClusterRestoredWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/waiter/ClusterRestored.html#Redshift.Waiter.ClusterRestored.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/#clusterrestoredwaiter)
        """


class SnapshotAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/waiter/SnapshotAvailable.html#Redshift.Waiter.SnapshotAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/#snapshotavailablewaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeClusterSnapshotsMessageSnapshotAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/waiter/SnapshotAvailable.html#Redshift.Waiter.SnapshotAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/#snapshotavailablewaiter)
        """
