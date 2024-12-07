"""
Type annotations for appstream service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_appstream.client import AppStreamClient
    from types_aiobotocore_appstream.waiter import (
        FleetStartedWaiter,
        FleetStoppedWaiter,
    )

    session = get_session()
    async with session.create_client("appstream") as client:
        client: AppStreamClient

        fleet_started_waiter: FleetStartedWaiter = client.get_waiter("fleet_started")
        fleet_stopped_waiter: FleetStoppedWaiter = client.get_waiter("fleet_stopped")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeFleetsRequestFleetStartedWaitTypeDef,
    DescribeFleetsRequestFleetStoppedWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("FleetStartedWaiter", "FleetStoppedWaiter")


class FleetStartedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/waiter/FleetStarted.html#AppStream.Waiter.FleetStarted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/waiters/#fleetstartedwaiter)
    """

    async def wait(self, **kwargs: Unpack[DescribeFleetsRequestFleetStartedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/waiter/FleetStarted.html#AppStream.Waiter.FleetStarted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/waiters/#fleetstartedwaiter)
        """


class FleetStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/waiter/FleetStopped.html#AppStream.Waiter.FleetStopped)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/waiters/#fleetstoppedwaiter)
    """

    async def wait(self, **kwargs: Unpack[DescribeFleetsRequestFleetStoppedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/waiter/FleetStopped.html#AppStream.Waiter.FleetStopped.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/waiters/#fleetstoppedwaiter)
        """
