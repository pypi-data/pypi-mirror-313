"""
Type annotations for emr-serverless service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_emr_serverless.client import EMRServerlessClient
    from types_aiobotocore_emr_serverless.paginator import (
        ListApplicationsPaginator,
        ListJobRunAttemptsPaginator,
        ListJobRunsPaginator,
    )

    session = get_session()
    with session.create_client("emr-serverless") as client:
        client: EMRServerlessClient

        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
        list_job_run_attempts_paginator: ListJobRunAttemptsPaginator = client.get_paginator("list_job_run_attempts")
        list_job_runs_paginator: ListJobRunsPaginator = client.get_paginator("list_job_runs")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListApplicationsRequestListApplicationsPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListJobRunAttemptsRequestListJobRunAttemptsPaginateTypeDef,
    ListJobRunAttemptsResponseTypeDef,
    ListJobRunsRequestListJobRunsPaginateTypeDef,
    ListJobRunsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListApplicationsPaginator", "ListJobRunAttemptsPaginator", "ListJobRunsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListApplicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless/paginator/ListApplications.html#EMRServerless.Paginator.ListApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/paginators/#listapplicationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListApplicationsRequestListApplicationsPaginateTypeDef]
    ) -> AsyncIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless/paginator/ListApplications.html#EMRServerless.Paginator.ListApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/paginators/#listapplicationspaginator)
        """


class ListJobRunAttemptsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless/paginator/ListJobRunAttempts.html#EMRServerless.Paginator.ListJobRunAttempts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/paginators/#listjobrunattemptspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListJobRunAttemptsRequestListJobRunAttemptsPaginateTypeDef]
    ) -> AsyncIterator[ListJobRunAttemptsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless/paginator/ListJobRunAttempts.html#EMRServerless.Paginator.ListJobRunAttempts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/paginators/#listjobrunattemptspaginator)
        """


class ListJobRunsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless/paginator/ListJobRuns.html#EMRServerless.Paginator.ListJobRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/paginators/#listjobrunspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListJobRunsRequestListJobRunsPaginateTypeDef]
    ) -> AsyncIterator[ListJobRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless/paginator/ListJobRuns.html#EMRServerless.Paginator.ListJobRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/paginators/#listjobrunspaginator)
        """
