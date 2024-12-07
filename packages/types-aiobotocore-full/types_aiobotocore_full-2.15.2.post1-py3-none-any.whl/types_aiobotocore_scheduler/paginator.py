"""
Type annotations for scheduler service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_scheduler.client import EventBridgeSchedulerClient
    from types_aiobotocore_scheduler.paginator import (
        ListScheduleGroupsPaginator,
        ListSchedulesPaginator,
    )

    session = get_session()
    with session.create_client("scheduler") as client:
        client: EventBridgeSchedulerClient

        list_schedule_groups_paginator: ListScheduleGroupsPaginator = client.get_paginator("list_schedule_groups")
        list_schedules_paginator: ListSchedulesPaginator = client.get_paginator("list_schedules")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListScheduleGroupsInputListScheduleGroupsPaginateTypeDef,
    ListScheduleGroupsOutputTypeDef,
    ListSchedulesInputListSchedulesPaginateTypeDef,
    ListSchedulesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListScheduleGroupsPaginator", "ListSchedulesPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListScheduleGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/paginator/ListScheduleGroups.html#EventBridgeScheduler.Paginator.ListScheduleGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/paginators/#listschedulegroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListScheduleGroupsInputListScheduleGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListScheduleGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/paginator/ListScheduleGroups.html#EventBridgeScheduler.Paginator.ListScheduleGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/paginators/#listschedulegroupspaginator)
        """


class ListSchedulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/paginator/ListSchedules.html#EventBridgeScheduler.Paginator.ListSchedules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/paginators/#listschedulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSchedulesInputListSchedulesPaginateTypeDef]
    ) -> AsyncIterator[ListSchedulesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/paginator/ListSchedules.html#EventBridgeScheduler.Paginator.ListSchedules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/paginators/#listschedulespaginator)
        """
