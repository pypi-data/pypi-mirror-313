"""
Type annotations for codecommit service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codecommit.client import CodeCommitClient
    from types_aiobotocore_codecommit.paginator import (
        DescribePullRequestEventsPaginator,
        GetCommentsForComparedCommitPaginator,
        GetCommentsForPullRequestPaginator,
        GetDifferencesPaginator,
        ListBranchesPaginator,
        ListPullRequestsPaginator,
        ListRepositoriesPaginator,
    )

    session = get_session()
    with session.create_client("codecommit") as client:
        client: CodeCommitClient

        describe_pull_request_events_paginator: DescribePullRequestEventsPaginator = client.get_paginator("describe_pull_request_events")
        get_comments_for_compared_commit_paginator: GetCommentsForComparedCommitPaginator = client.get_paginator("get_comments_for_compared_commit")
        get_comments_for_pull_request_paginator: GetCommentsForPullRequestPaginator = client.get_paginator("get_comments_for_pull_request")
        get_differences_paginator: GetDifferencesPaginator = client.get_paginator("get_differences")
        list_branches_paginator: ListBranchesPaginator = client.get_paginator("list_branches")
        list_pull_requests_paginator: ListPullRequestsPaginator = client.get_paginator("list_pull_requests")
        list_repositories_paginator: ListRepositoriesPaginator = client.get_paginator("list_repositories")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribePullRequestEventsInputDescribePullRequestEventsPaginateTypeDef,
    DescribePullRequestEventsOutputTypeDef,
    GetCommentsForComparedCommitInputGetCommentsForComparedCommitPaginateTypeDef,
    GetCommentsForComparedCommitOutputTypeDef,
    GetCommentsForPullRequestInputGetCommentsForPullRequestPaginateTypeDef,
    GetCommentsForPullRequestOutputTypeDef,
    GetDifferencesInputGetDifferencesPaginateTypeDef,
    GetDifferencesOutputTypeDef,
    ListBranchesInputListBranchesPaginateTypeDef,
    ListBranchesOutputTypeDef,
    ListPullRequestsInputListPullRequestsPaginateTypeDef,
    ListPullRequestsOutputTypeDef,
    ListRepositoriesInputListRepositoriesPaginateTypeDef,
    ListRepositoriesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribePullRequestEventsPaginator",
    "GetCommentsForComparedCommitPaginator",
    "GetCommentsForPullRequestPaginator",
    "GetDifferencesPaginator",
    "ListBranchesPaginator",
    "ListPullRequestsPaginator",
    "ListRepositoriesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribePullRequestEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/DescribePullRequestEvents.html#CodeCommit.Paginator.DescribePullRequestEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#describepullrequesteventspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribePullRequestEventsInputDescribePullRequestEventsPaginateTypeDef],
    ) -> AsyncIterator[DescribePullRequestEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/DescribePullRequestEvents.html#CodeCommit.Paginator.DescribePullRequestEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#describepullrequesteventspaginator)
        """


class GetCommentsForComparedCommitPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetCommentsForComparedCommit.html#CodeCommit.Paginator.GetCommentsForComparedCommit)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#getcommentsforcomparedcommitpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetCommentsForComparedCommitInputGetCommentsForComparedCommitPaginateTypeDef
        ],
    ) -> AsyncIterator[GetCommentsForComparedCommitOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetCommentsForComparedCommit.html#CodeCommit.Paginator.GetCommentsForComparedCommit.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#getcommentsforcomparedcommitpaginator)
        """


class GetCommentsForPullRequestPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetCommentsForPullRequest.html#CodeCommit.Paginator.GetCommentsForPullRequest)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#getcommentsforpullrequestpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[GetCommentsForPullRequestInputGetCommentsForPullRequestPaginateTypeDef],
    ) -> AsyncIterator[GetCommentsForPullRequestOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetCommentsForPullRequest.html#CodeCommit.Paginator.GetCommentsForPullRequest.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#getcommentsforpullrequestpaginator)
        """


class GetDifferencesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetDifferences.html#CodeCommit.Paginator.GetDifferences)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#getdifferencespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetDifferencesInputGetDifferencesPaginateTypeDef]
    ) -> AsyncIterator[GetDifferencesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetDifferences.html#CodeCommit.Paginator.GetDifferences.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#getdifferencespaginator)
        """


class ListBranchesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListBranches.html#CodeCommit.Paginator.ListBranches)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#listbranchespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBranchesInputListBranchesPaginateTypeDef]
    ) -> AsyncIterator[ListBranchesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListBranches.html#CodeCommit.Paginator.ListBranches.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#listbranchespaginator)
        """


class ListPullRequestsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListPullRequests.html#CodeCommit.Paginator.ListPullRequests)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#listpullrequestspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPullRequestsInputListPullRequestsPaginateTypeDef]
    ) -> AsyncIterator[ListPullRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListPullRequests.html#CodeCommit.Paginator.ListPullRequests.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#listpullrequestspaginator)
        """


class ListRepositoriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListRepositories.html#CodeCommit.Paginator.ListRepositories)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#listrepositoriespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRepositoriesInputListRepositoriesPaginateTypeDef]
    ) -> AsyncIterator[ListRepositoriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListRepositories.html#CodeCommit.Paginator.ListRepositories.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#listrepositoriespaginator)
        """
