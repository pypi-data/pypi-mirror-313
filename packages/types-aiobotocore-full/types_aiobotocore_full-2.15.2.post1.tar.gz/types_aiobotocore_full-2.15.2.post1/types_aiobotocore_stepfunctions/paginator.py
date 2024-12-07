"""
Type annotations for stepfunctions service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_stepfunctions.client import SFNClient
    from types_aiobotocore_stepfunctions.paginator import (
        GetExecutionHistoryPaginator,
        ListActivitiesPaginator,
        ListExecutionsPaginator,
        ListMapRunsPaginator,
        ListStateMachinesPaginator,
    )

    session = get_session()
    with session.create_client("stepfunctions") as client:
        client: SFNClient

        get_execution_history_paginator: GetExecutionHistoryPaginator = client.get_paginator("get_execution_history")
        list_activities_paginator: ListActivitiesPaginator = client.get_paginator("list_activities")
        list_executions_paginator: ListExecutionsPaginator = client.get_paginator("list_executions")
        list_map_runs_paginator: ListMapRunsPaginator = client.get_paginator("list_map_runs")
        list_state_machines_paginator: ListStateMachinesPaginator = client.get_paginator("list_state_machines")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetExecutionHistoryInputGetExecutionHistoryPaginateTypeDef,
    GetExecutionHistoryOutputTypeDef,
    ListActivitiesInputListActivitiesPaginateTypeDef,
    ListActivitiesOutputTypeDef,
    ListExecutionsInputListExecutionsPaginateTypeDef,
    ListExecutionsOutputTypeDef,
    ListMapRunsInputListMapRunsPaginateTypeDef,
    ListMapRunsOutputTypeDef,
    ListStateMachinesInputListStateMachinesPaginateTypeDef,
    ListStateMachinesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetExecutionHistoryPaginator",
    "ListActivitiesPaginator",
    "ListExecutionsPaginator",
    "ListMapRunsPaginator",
    "ListStateMachinesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetExecutionHistoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/GetExecutionHistory.html#SFN.Paginator.GetExecutionHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#getexecutionhistorypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetExecutionHistoryInputGetExecutionHistoryPaginateTypeDef]
    ) -> AsyncIterator[GetExecutionHistoryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/GetExecutionHistory.html#SFN.Paginator.GetExecutionHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#getexecutionhistorypaginator)
        """


class ListActivitiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListActivities.html#SFN.Paginator.ListActivities)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#listactivitiespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListActivitiesInputListActivitiesPaginateTypeDef]
    ) -> AsyncIterator[ListActivitiesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListActivities.html#SFN.Paginator.ListActivities.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#listactivitiespaginator)
        """


class ListExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListExecutions.html#SFN.Paginator.ListExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#listexecutionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListExecutionsInputListExecutionsPaginateTypeDef]
    ) -> AsyncIterator[ListExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListExecutions.html#SFN.Paginator.ListExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#listexecutionspaginator)
        """


class ListMapRunsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListMapRuns.html#SFN.Paginator.ListMapRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#listmaprunspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMapRunsInputListMapRunsPaginateTypeDef]
    ) -> AsyncIterator[ListMapRunsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListMapRuns.html#SFN.Paginator.ListMapRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#listmaprunspaginator)
        """


class ListStateMachinesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListStateMachines.html#SFN.Paginator.ListStateMachines)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#liststatemachinespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStateMachinesInputListStateMachinesPaginateTypeDef]
    ) -> AsyncIterator[ListStateMachinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListStateMachines.html#SFN.Paginator.ListStateMachines.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#liststatemachinespaginator)
        """
