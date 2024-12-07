"""
Type annotations for swf service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_swf.client import SWFClient
    from types_aiobotocore_swf.paginator import (
        GetWorkflowExecutionHistoryPaginator,
        ListActivityTypesPaginator,
        ListClosedWorkflowExecutionsPaginator,
        ListDomainsPaginator,
        ListOpenWorkflowExecutionsPaginator,
        ListWorkflowTypesPaginator,
        PollForDecisionTaskPaginator,
    )

    session = get_session()
    with session.create_client("swf") as client:
        client: SWFClient

        get_workflow_execution_history_paginator: GetWorkflowExecutionHistoryPaginator = client.get_paginator("get_workflow_execution_history")
        list_activity_types_paginator: ListActivityTypesPaginator = client.get_paginator("list_activity_types")
        list_closed_workflow_executions_paginator: ListClosedWorkflowExecutionsPaginator = client.get_paginator("list_closed_workflow_executions")
        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_open_workflow_executions_paginator: ListOpenWorkflowExecutionsPaginator = client.get_paginator("list_open_workflow_executions")
        list_workflow_types_paginator: ListWorkflowTypesPaginator = client.get_paginator("list_workflow_types")
        poll_for_decision_task_paginator: PollForDecisionTaskPaginator = client.get_paginator("poll_for_decision_task")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ActivityTypeInfosTypeDef,
    DecisionTaskTypeDef,
    DomainInfosTypeDef,
    GetWorkflowExecutionHistoryInputGetWorkflowExecutionHistoryPaginateTypeDef,
    HistoryTypeDef,
    ListActivityTypesInputListActivityTypesPaginateTypeDef,
    ListClosedWorkflowExecutionsInputListClosedWorkflowExecutionsPaginateTypeDef,
    ListDomainsInputListDomainsPaginateTypeDef,
    ListOpenWorkflowExecutionsInputListOpenWorkflowExecutionsPaginateTypeDef,
    ListWorkflowTypesInputListWorkflowTypesPaginateTypeDef,
    PollForDecisionTaskInputPollForDecisionTaskPaginateTypeDef,
    WorkflowExecutionInfosTypeDef,
    WorkflowTypeInfosTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetWorkflowExecutionHistoryPaginator",
    "ListActivityTypesPaginator",
    "ListClosedWorkflowExecutionsPaginator",
    "ListDomainsPaginator",
    "ListOpenWorkflowExecutionsPaginator",
    "ListWorkflowTypesPaginator",
    "PollForDecisionTaskPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetWorkflowExecutionHistoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/GetWorkflowExecutionHistory.html#SWF.Paginator.GetWorkflowExecutionHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#getworkflowexecutionhistorypaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetWorkflowExecutionHistoryInputGetWorkflowExecutionHistoryPaginateTypeDef
        ],
    ) -> AsyncIterator[HistoryTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/GetWorkflowExecutionHistory.html#SWF.Paginator.GetWorkflowExecutionHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#getworkflowexecutionhistorypaginator)
        """


class ListActivityTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListActivityTypes.html#SWF.Paginator.ListActivityTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listactivitytypespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListActivityTypesInputListActivityTypesPaginateTypeDef]
    ) -> AsyncIterator[ActivityTypeInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListActivityTypes.html#SWF.Paginator.ListActivityTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listactivitytypespaginator)
        """


class ListClosedWorkflowExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListClosedWorkflowExecutions.html#SWF.Paginator.ListClosedWorkflowExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listclosedworkflowexecutionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListClosedWorkflowExecutionsInputListClosedWorkflowExecutionsPaginateTypeDef
        ],
    ) -> AsyncIterator[WorkflowExecutionInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListClosedWorkflowExecutions.html#SWF.Paginator.ListClosedWorkflowExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listclosedworkflowexecutionspaginator)
        """


class ListDomainsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListDomains.html#SWF.Paginator.ListDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listdomainspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDomainsInputListDomainsPaginateTypeDef]
    ) -> AsyncIterator[DomainInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListDomains.html#SWF.Paginator.ListDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listdomainspaginator)
        """


class ListOpenWorkflowExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListOpenWorkflowExecutions.html#SWF.Paginator.ListOpenWorkflowExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listopenworkflowexecutionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListOpenWorkflowExecutionsInputListOpenWorkflowExecutionsPaginateTypeDef],
    ) -> AsyncIterator[WorkflowExecutionInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListOpenWorkflowExecutions.html#SWF.Paginator.ListOpenWorkflowExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listopenworkflowexecutionspaginator)
        """


class ListWorkflowTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListWorkflowTypes.html#SWF.Paginator.ListWorkflowTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listworkflowtypespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorkflowTypesInputListWorkflowTypesPaginateTypeDef]
    ) -> AsyncIterator[WorkflowTypeInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListWorkflowTypes.html#SWF.Paginator.ListWorkflowTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listworkflowtypespaginator)
        """


class PollForDecisionTaskPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/PollForDecisionTask.html#SWF.Paginator.PollForDecisionTask)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#pollfordecisiontaskpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[PollForDecisionTaskInputPollForDecisionTaskPaginateTypeDef]
    ) -> AsyncIterator[DecisionTaskTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/PollForDecisionTask.html#SWF.Paginator.PollForDecisionTask.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#pollfordecisiontaskpaginator)
        """
