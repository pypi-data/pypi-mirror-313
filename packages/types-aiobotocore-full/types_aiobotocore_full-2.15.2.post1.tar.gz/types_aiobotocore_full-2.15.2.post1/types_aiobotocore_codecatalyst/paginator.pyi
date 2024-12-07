"""
Type annotations for codecatalyst service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codecatalyst.client import CodeCatalystClient
    from types_aiobotocore_codecatalyst.paginator import (
        ListAccessTokensPaginator,
        ListDevEnvironmentSessionsPaginator,
        ListDevEnvironmentsPaginator,
        ListEventLogsPaginator,
        ListProjectsPaginator,
        ListSourceRepositoriesPaginator,
        ListSourceRepositoryBranchesPaginator,
        ListSpacesPaginator,
        ListWorkflowRunsPaginator,
        ListWorkflowsPaginator,
    )

    session = get_session()
    with session.create_client("codecatalyst") as client:
        client: CodeCatalystClient

        list_access_tokens_paginator: ListAccessTokensPaginator = client.get_paginator("list_access_tokens")
        list_dev_environment_sessions_paginator: ListDevEnvironmentSessionsPaginator = client.get_paginator("list_dev_environment_sessions")
        list_dev_environments_paginator: ListDevEnvironmentsPaginator = client.get_paginator("list_dev_environments")
        list_event_logs_paginator: ListEventLogsPaginator = client.get_paginator("list_event_logs")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
        list_source_repositories_paginator: ListSourceRepositoriesPaginator = client.get_paginator("list_source_repositories")
        list_source_repository_branches_paginator: ListSourceRepositoryBranchesPaginator = client.get_paginator("list_source_repository_branches")
        list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
        list_workflow_runs_paginator: ListWorkflowRunsPaginator = client.get_paginator("list_workflow_runs")
        list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAccessTokensRequestListAccessTokensPaginateTypeDef,
    ListAccessTokensResponseTypeDef,
    ListDevEnvironmentSessionsRequestListDevEnvironmentSessionsPaginateTypeDef,
    ListDevEnvironmentSessionsResponseTypeDef,
    ListDevEnvironmentsRequestListDevEnvironmentsPaginateTypeDef,
    ListDevEnvironmentsResponseTypeDef,
    ListEventLogsRequestListEventLogsPaginateTypeDef,
    ListEventLogsResponseTypeDef,
    ListProjectsRequestListProjectsPaginateTypeDef,
    ListProjectsResponseTypeDef,
    ListSourceRepositoriesRequestListSourceRepositoriesPaginateTypeDef,
    ListSourceRepositoriesResponseTypeDef,
    ListSourceRepositoryBranchesRequestListSourceRepositoryBranchesPaginateTypeDef,
    ListSourceRepositoryBranchesResponseTypeDef,
    ListSpacesRequestListSpacesPaginateTypeDef,
    ListSpacesResponseTypeDef,
    ListWorkflowRunsRequestListWorkflowRunsPaginateTypeDef,
    ListWorkflowRunsResponseTypeDef,
    ListWorkflowsRequestListWorkflowsPaginateTypeDef,
    ListWorkflowsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAccessTokensPaginator",
    "ListDevEnvironmentSessionsPaginator",
    "ListDevEnvironmentsPaginator",
    "ListEventLogsPaginator",
    "ListProjectsPaginator",
    "ListSourceRepositoriesPaginator",
    "ListSourceRepositoryBranchesPaginator",
    "ListSpacesPaginator",
    "ListWorkflowRunsPaginator",
    "ListWorkflowsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAccessTokensPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListAccessTokens.html#CodeCatalyst.Paginator.ListAccessTokens)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listaccesstokenspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAccessTokensRequestListAccessTokensPaginateTypeDef]
    ) -> AsyncIterator[ListAccessTokensResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListAccessTokens.html#CodeCatalyst.Paginator.ListAccessTokens.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listaccesstokenspaginator)
        """

class ListDevEnvironmentSessionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListDevEnvironmentSessions.html#CodeCatalyst.Paginator.ListDevEnvironmentSessions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listdevenvironmentsessionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListDevEnvironmentSessionsRequestListDevEnvironmentSessionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListDevEnvironmentSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListDevEnvironmentSessions.html#CodeCatalyst.Paginator.ListDevEnvironmentSessions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listdevenvironmentsessionspaginator)
        """

class ListDevEnvironmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListDevEnvironments.html#CodeCatalyst.Paginator.ListDevEnvironments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listdevenvironmentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDevEnvironmentsRequestListDevEnvironmentsPaginateTypeDef]
    ) -> AsyncIterator[ListDevEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListDevEnvironments.html#CodeCatalyst.Paginator.ListDevEnvironments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listdevenvironmentspaginator)
        """

class ListEventLogsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListEventLogs.html#CodeCatalyst.Paginator.ListEventLogs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listeventlogspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEventLogsRequestListEventLogsPaginateTypeDef]
    ) -> AsyncIterator[ListEventLogsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListEventLogs.html#CodeCatalyst.Paginator.ListEventLogs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listeventlogspaginator)
        """

class ListProjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListProjects.html#CodeCatalyst.Paginator.ListProjects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listprojectspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProjectsRequestListProjectsPaginateTypeDef]
    ) -> AsyncIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListProjects.html#CodeCatalyst.Paginator.ListProjects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listprojectspaginator)
        """

class ListSourceRepositoriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSourceRepositories.html#CodeCatalyst.Paginator.ListSourceRepositories)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listsourcerepositoriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSourceRepositoriesRequestListSourceRepositoriesPaginateTypeDef]
    ) -> AsyncIterator[ListSourceRepositoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSourceRepositories.html#CodeCatalyst.Paginator.ListSourceRepositories.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listsourcerepositoriespaginator)
        """

class ListSourceRepositoryBranchesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSourceRepositoryBranches.html#CodeCatalyst.Paginator.ListSourceRepositoryBranches)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listsourcerepositorybranchespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListSourceRepositoryBranchesRequestListSourceRepositoryBranchesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListSourceRepositoryBranchesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSourceRepositoryBranches.html#CodeCatalyst.Paginator.ListSourceRepositoryBranches.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listsourcerepositorybranchespaginator)
        """

class ListSpacesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSpaces.html#CodeCatalyst.Paginator.ListSpaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listspacespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSpacesRequestListSpacesPaginateTypeDef]
    ) -> AsyncIterator[ListSpacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSpaces.html#CodeCatalyst.Paginator.ListSpaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listspacespaginator)
        """

class ListWorkflowRunsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListWorkflowRuns.html#CodeCatalyst.Paginator.ListWorkflowRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listworkflowrunspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListWorkflowRunsRequestListWorkflowRunsPaginateTypeDef]
    ) -> AsyncIterator[ListWorkflowRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListWorkflowRuns.html#CodeCatalyst.Paginator.ListWorkflowRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listworkflowrunspaginator)
        """

class ListWorkflowsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListWorkflows.html#CodeCatalyst.Paginator.ListWorkflows)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listworkflowspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListWorkflowsRequestListWorkflowsPaginateTypeDef]
    ) -> AsyncIterator[ListWorkflowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListWorkflows.html#CodeCatalyst.Paginator.ListWorkflows.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listworkflowspaginator)
        """
