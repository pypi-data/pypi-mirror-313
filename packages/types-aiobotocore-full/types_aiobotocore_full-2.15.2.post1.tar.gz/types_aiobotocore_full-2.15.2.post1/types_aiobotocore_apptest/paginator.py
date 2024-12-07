"""
Type annotations for apptest service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_apptest.client import MainframeModernizationApplicationTestingClient
    from types_aiobotocore_apptest.paginator import (
        ListTestCasesPaginator,
        ListTestConfigurationsPaginator,
        ListTestRunStepsPaginator,
        ListTestRunTestCasesPaginator,
        ListTestRunsPaginator,
        ListTestSuitesPaginator,
    )

    session = get_session()
    with session.create_client("apptest") as client:
        client: MainframeModernizationApplicationTestingClient

        list_test_cases_paginator: ListTestCasesPaginator = client.get_paginator("list_test_cases")
        list_test_configurations_paginator: ListTestConfigurationsPaginator = client.get_paginator("list_test_configurations")
        list_test_run_steps_paginator: ListTestRunStepsPaginator = client.get_paginator("list_test_run_steps")
        list_test_run_test_cases_paginator: ListTestRunTestCasesPaginator = client.get_paginator("list_test_run_test_cases")
        list_test_runs_paginator: ListTestRunsPaginator = client.get_paginator("list_test_runs")
        list_test_suites_paginator: ListTestSuitesPaginator = client.get_paginator("list_test_suites")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListTestCasesRequestListTestCasesPaginateTypeDef,
    ListTestCasesResponseTypeDef,
    ListTestConfigurationsRequestListTestConfigurationsPaginateTypeDef,
    ListTestConfigurationsResponseTypeDef,
    ListTestRunsRequestListTestRunsPaginateTypeDef,
    ListTestRunsResponseTypeDef,
    ListTestRunStepsRequestListTestRunStepsPaginateTypeDef,
    ListTestRunStepsResponseTypeDef,
    ListTestRunTestCasesRequestListTestRunTestCasesPaginateTypeDef,
    ListTestRunTestCasesResponseTypeDef,
    ListTestSuitesRequestListTestSuitesPaginateTypeDef,
    ListTestSuitesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListTestCasesPaginator",
    "ListTestConfigurationsPaginator",
    "ListTestRunStepsPaginator",
    "ListTestRunTestCasesPaginator",
    "ListTestRunsPaginator",
    "ListTestSuitesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListTestCasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestCases.html#MainframeModernizationApplicationTesting.Paginator.ListTestCases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestcasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTestCasesRequestListTestCasesPaginateTypeDef]
    ) -> AsyncIterator[ListTestCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestCases.html#MainframeModernizationApplicationTesting.Paginator.ListTestCases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestcasespaginator)
        """


class ListTestConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestConfigurations.html#MainframeModernizationApplicationTesting.Paginator.ListTestConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestconfigurationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTestConfigurationsRequestListTestConfigurationsPaginateTypeDef]
    ) -> AsyncIterator[ListTestConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestConfigurations.html#MainframeModernizationApplicationTesting.Paginator.ListTestConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestconfigurationspaginator)
        """


class ListTestRunStepsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestRunSteps.html#MainframeModernizationApplicationTesting.Paginator.ListTestRunSteps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestrunstepspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTestRunStepsRequestListTestRunStepsPaginateTypeDef]
    ) -> AsyncIterator[ListTestRunStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestRunSteps.html#MainframeModernizationApplicationTesting.Paginator.ListTestRunSteps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestrunstepspaginator)
        """


class ListTestRunTestCasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestRunTestCases.html#MainframeModernizationApplicationTesting.Paginator.ListTestRunTestCases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestruntestcasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTestRunTestCasesRequestListTestRunTestCasesPaginateTypeDef]
    ) -> AsyncIterator[ListTestRunTestCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestRunTestCases.html#MainframeModernizationApplicationTesting.Paginator.ListTestRunTestCases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestruntestcasespaginator)
        """


class ListTestRunsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestRuns.html#MainframeModernizationApplicationTesting.Paginator.ListTestRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestrunspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTestRunsRequestListTestRunsPaginateTypeDef]
    ) -> AsyncIterator[ListTestRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestRuns.html#MainframeModernizationApplicationTesting.Paginator.ListTestRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestrunspaginator)
        """


class ListTestSuitesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestSuites.html#MainframeModernizationApplicationTesting.Paginator.ListTestSuites)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestsuitespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTestSuitesRequestListTestSuitesPaginateTypeDef]
    ) -> AsyncIterator[ListTestSuitesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestSuites.html#MainframeModernizationApplicationTesting.Paginator.ListTestSuites.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestsuitespaginator)
        """
