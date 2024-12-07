"""
Type annotations for groundstation service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_groundstation.client import GroundStationClient
    from types_aiobotocore_groundstation.waiter import (
        ContactScheduledWaiter,
    )

    session = get_session()
    async with session.create_client("groundstation") as client:
        client: GroundStationClient

        contact_scheduled_waiter: ContactScheduledWaiter = client.get_waiter("contact_scheduled")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import DescribeContactRequestContactScheduledWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ContactScheduledWaiter",)


class ContactScheduledWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/waiter/ContactScheduled.html#GroundStation.Waiter.ContactScheduled)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/waiters/#contactscheduledwaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeContactRequestContactScheduledWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/waiter/ContactScheduled.html#GroundStation.Waiter.ContactScheduled.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/waiters/#contactscheduledwaiter)
        """
