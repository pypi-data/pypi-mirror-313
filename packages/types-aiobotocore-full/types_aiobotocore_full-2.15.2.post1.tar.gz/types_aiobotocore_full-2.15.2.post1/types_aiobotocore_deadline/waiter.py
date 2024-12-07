"""
Type annotations for deadline service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_deadline.client import DeadlineCloudClient
    from types_aiobotocore_deadline.waiter import (
        FleetActiveWaiter,
        JobCreateCompleteWaiter,
        LicenseEndpointDeletedWaiter,
        LicenseEndpointValidWaiter,
        QueueFleetAssociationStoppedWaiter,
        QueueSchedulingBlockedWaiter,
        QueueSchedulingWaiter,
    )

    session = get_session()
    async with session.create_client("deadline") as client:
        client: DeadlineCloudClient

        fleet_active_waiter: FleetActiveWaiter = client.get_waiter("fleet_active")
        job_create_complete_waiter: JobCreateCompleteWaiter = client.get_waiter("job_create_complete")
        license_endpoint_deleted_waiter: LicenseEndpointDeletedWaiter = client.get_waiter("license_endpoint_deleted")
        license_endpoint_valid_waiter: LicenseEndpointValidWaiter = client.get_waiter("license_endpoint_valid")
        queue_fleet_association_stopped_waiter: QueueFleetAssociationStoppedWaiter = client.get_waiter("queue_fleet_association_stopped")
        queue_scheduling_blocked_waiter: QueueSchedulingBlockedWaiter = client.get_waiter("queue_scheduling_blocked")
        queue_scheduling_waiter: QueueSchedulingWaiter = client.get_waiter("queue_scheduling")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    GetFleetRequestFleetActiveWaitTypeDef,
    GetJobRequestJobCreateCompleteWaitTypeDef,
    GetLicenseEndpointRequestLicenseEndpointDeletedWaitTypeDef,
    GetLicenseEndpointRequestLicenseEndpointValidWaitTypeDef,
    GetQueueFleetAssociationRequestQueueFleetAssociationStoppedWaitTypeDef,
    GetQueueRequestQueueSchedulingBlockedWaitTypeDef,
    GetQueueRequestQueueSchedulingWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "FleetActiveWaiter",
    "JobCreateCompleteWaiter",
    "LicenseEndpointDeletedWaiter",
    "LicenseEndpointValidWaiter",
    "QueueFleetAssociationStoppedWaiter",
    "QueueSchedulingBlockedWaiter",
    "QueueSchedulingWaiter",
)


class FleetActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/FleetActive.html#DeadlineCloud.Waiter.FleetActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#fleetactivewaiter)
    """

    async def wait(self, **kwargs: Unpack[GetFleetRequestFleetActiveWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/FleetActive.html#DeadlineCloud.Waiter.FleetActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#fleetactivewaiter)
        """


class JobCreateCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/JobCreateComplete.html#DeadlineCloud.Waiter.JobCreateComplete)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#jobcreatecompletewaiter)
    """

    async def wait(self, **kwargs: Unpack[GetJobRequestJobCreateCompleteWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/JobCreateComplete.html#DeadlineCloud.Waiter.JobCreateComplete.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#jobcreatecompletewaiter)
        """


class LicenseEndpointDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/LicenseEndpointDeleted.html#DeadlineCloud.Waiter.LicenseEndpointDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#licenseendpointdeletedwaiter)
    """

    async def wait(
        self, **kwargs: Unpack[GetLicenseEndpointRequestLicenseEndpointDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/LicenseEndpointDeleted.html#DeadlineCloud.Waiter.LicenseEndpointDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#licenseendpointdeletedwaiter)
        """


class LicenseEndpointValidWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/LicenseEndpointValid.html#DeadlineCloud.Waiter.LicenseEndpointValid)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#licenseendpointvalidwaiter)
    """

    async def wait(
        self, **kwargs: Unpack[GetLicenseEndpointRequestLicenseEndpointValidWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/LicenseEndpointValid.html#DeadlineCloud.Waiter.LicenseEndpointValid.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#licenseendpointvalidwaiter)
        """


class QueueFleetAssociationStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/QueueFleetAssociationStopped.html#DeadlineCloud.Waiter.QueueFleetAssociationStopped)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#queuefleetassociationstoppedwaiter)
    """

    async def wait(
        self,
        **kwargs: Unpack[GetQueueFleetAssociationRequestQueueFleetAssociationStoppedWaitTypeDef],
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/QueueFleetAssociationStopped.html#DeadlineCloud.Waiter.QueueFleetAssociationStopped.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#queuefleetassociationstoppedwaiter)
        """


class QueueSchedulingBlockedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/QueueSchedulingBlocked.html#DeadlineCloud.Waiter.QueueSchedulingBlocked)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#queueschedulingblockedwaiter)
    """

    async def wait(
        self, **kwargs: Unpack[GetQueueRequestQueueSchedulingBlockedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/QueueSchedulingBlocked.html#DeadlineCloud.Waiter.QueueSchedulingBlocked.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#queueschedulingblockedwaiter)
        """


class QueueSchedulingWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/QueueScheduling.html#DeadlineCloud.Waiter.QueueScheduling)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#queueschedulingwaiter)
    """

    async def wait(self, **kwargs: Unpack[GetQueueRequestQueueSchedulingWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/QueueScheduling.html#DeadlineCloud.Waiter.QueueScheduling.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#queueschedulingwaiter)
        """
