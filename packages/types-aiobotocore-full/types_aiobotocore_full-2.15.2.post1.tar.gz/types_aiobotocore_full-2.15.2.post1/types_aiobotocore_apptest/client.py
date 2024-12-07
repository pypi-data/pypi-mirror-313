"""
Type annotations for apptest service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_apptest.client import MainframeModernizationApplicationTestingClient

    session = get_session()
    async with session.create_client("apptest") as client:
        client: MainframeModernizationApplicationTestingClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListTestCasesPaginator,
    ListTestConfigurationsPaginator,
    ListTestRunsPaginator,
    ListTestRunStepsPaginator,
    ListTestRunTestCasesPaginator,
    ListTestSuitesPaginator,
)
from .type_defs import (
    CreateTestCaseRequestRequestTypeDef,
    CreateTestCaseResponseTypeDef,
    CreateTestConfigurationRequestRequestTypeDef,
    CreateTestConfigurationResponseTypeDef,
    CreateTestSuiteRequestRequestTypeDef,
    CreateTestSuiteResponseTypeDef,
    DeleteTestCaseRequestRequestTypeDef,
    DeleteTestConfigurationRequestRequestTypeDef,
    DeleteTestRunRequestRequestTypeDef,
    DeleteTestSuiteRequestRequestTypeDef,
    GetTestCaseRequestRequestTypeDef,
    GetTestCaseResponseTypeDef,
    GetTestConfigurationRequestRequestTypeDef,
    GetTestConfigurationResponseTypeDef,
    GetTestRunStepRequestRequestTypeDef,
    GetTestRunStepResponseTypeDef,
    GetTestSuiteRequestRequestTypeDef,
    GetTestSuiteResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTestCasesRequestRequestTypeDef,
    ListTestCasesResponseTypeDef,
    ListTestConfigurationsRequestRequestTypeDef,
    ListTestConfigurationsResponseTypeDef,
    ListTestRunsRequestRequestTypeDef,
    ListTestRunsResponseTypeDef,
    ListTestRunStepsRequestRequestTypeDef,
    ListTestRunStepsResponseTypeDef,
    ListTestRunTestCasesRequestRequestTypeDef,
    ListTestRunTestCasesResponseTypeDef,
    ListTestSuitesRequestRequestTypeDef,
    ListTestSuitesResponseTypeDef,
    StartTestRunRequestRequestTypeDef,
    StartTestRunResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateTestCaseRequestRequestTypeDef,
    UpdateTestCaseResponseTypeDef,
    UpdateTestConfigurationRequestRequestTypeDef,
    UpdateTestConfigurationResponseTypeDef,
    UpdateTestSuiteRequestRequestTypeDef,
    UpdateTestSuiteResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("MainframeModernizationApplicationTestingClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class MainframeModernizationApplicationTestingClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MainframeModernizationApplicationTestingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#close)
        """

    async def create_test_case(
        self, **kwargs: Unpack[CreateTestCaseRequestRequestTypeDef]
    ) -> CreateTestCaseResponseTypeDef:
        """
        Creates a test case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/create_test_case.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#create_test_case)
        """

    async def create_test_configuration(
        self, **kwargs: Unpack[CreateTestConfigurationRequestRequestTypeDef]
    ) -> CreateTestConfigurationResponseTypeDef:
        """
        Creates a test configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/create_test_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#create_test_configuration)
        """

    async def create_test_suite(
        self, **kwargs: Unpack[CreateTestSuiteRequestRequestTypeDef]
    ) -> CreateTestSuiteResponseTypeDef:
        """
        Creates a test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/create_test_suite.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#create_test_suite)
        """

    async def delete_test_case(
        self, **kwargs: Unpack[DeleteTestCaseRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a test case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/delete_test_case.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#delete_test_case)
        """

    async def delete_test_configuration(
        self, **kwargs: Unpack[DeleteTestConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a test configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/delete_test_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#delete_test_configuration)
        """

    async def delete_test_run(
        self, **kwargs: Unpack[DeleteTestRunRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a test run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/delete_test_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#delete_test_run)
        """

    async def delete_test_suite(
        self, **kwargs: Unpack[DeleteTestSuiteRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/delete_test_suite.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#delete_test_suite)
        """

    async def get_test_case(
        self, **kwargs: Unpack[GetTestCaseRequestRequestTypeDef]
    ) -> GetTestCaseResponseTypeDef:
        """
        Gets a test case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/get_test_case.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#get_test_case)
        """

    async def get_test_configuration(
        self, **kwargs: Unpack[GetTestConfigurationRequestRequestTypeDef]
    ) -> GetTestConfigurationResponseTypeDef:
        """
        Gets a test configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/get_test_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#get_test_configuration)
        """

    async def get_test_run_step(
        self, **kwargs: Unpack[GetTestRunStepRequestRequestTypeDef]
    ) -> GetTestRunStepResponseTypeDef:
        """
        Gets a test run step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/get_test_run_step.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#get_test_run_step)
        """

    async def get_test_suite(
        self, **kwargs: Unpack[GetTestSuiteRequestRequestTypeDef]
    ) -> GetTestSuiteResponseTypeDef:
        """
        Gets a test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/get_test_suite.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#get_test_suite)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#list_tags_for_resource)
        """

    async def list_test_cases(
        self, **kwargs: Unpack[ListTestCasesRequestRequestTypeDef]
    ) -> ListTestCasesResponseTypeDef:
        """
        Lists test cases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/list_test_cases.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#list_test_cases)
        """

    async def list_test_configurations(
        self, **kwargs: Unpack[ListTestConfigurationsRequestRequestTypeDef]
    ) -> ListTestConfigurationsResponseTypeDef:
        """
        Lists test configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/list_test_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#list_test_configurations)
        """

    async def list_test_run_steps(
        self, **kwargs: Unpack[ListTestRunStepsRequestRequestTypeDef]
    ) -> ListTestRunStepsResponseTypeDef:
        """
        Lists test run steps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/list_test_run_steps.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#list_test_run_steps)
        """

    async def list_test_run_test_cases(
        self, **kwargs: Unpack[ListTestRunTestCasesRequestRequestTypeDef]
    ) -> ListTestRunTestCasesResponseTypeDef:
        """
        Lists test run test cases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/list_test_run_test_cases.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#list_test_run_test_cases)
        """

    async def list_test_runs(
        self, **kwargs: Unpack[ListTestRunsRequestRequestTypeDef]
    ) -> ListTestRunsResponseTypeDef:
        """
        Lists test runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/list_test_runs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#list_test_runs)
        """

    async def list_test_suites(
        self, **kwargs: Unpack[ListTestSuitesRequestRequestTypeDef]
    ) -> ListTestSuitesResponseTypeDef:
        """
        Lists test suites.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/list_test_suites.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#list_test_suites)
        """

    async def start_test_run(
        self, **kwargs: Unpack[StartTestRunRequestRequestTypeDef]
    ) -> StartTestRunResponseTypeDef:
        """
        Starts a test run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/start_test_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#start_test_run)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Specifies tags of a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Untags a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#untag_resource)
        """

    async def update_test_case(
        self, **kwargs: Unpack[UpdateTestCaseRequestRequestTypeDef]
    ) -> UpdateTestCaseResponseTypeDef:
        """
        Updates a test case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/update_test_case.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#update_test_case)
        """

    async def update_test_configuration(
        self, **kwargs: Unpack[UpdateTestConfigurationRequestRequestTypeDef]
    ) -> UpdateTestConfigurationResponseTypeDef:
        """
        Updates a test configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/update_test_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#update_test_configuration)
        """

    async def update_test_suite(
        self, **kwargs: Unpack[UpdateTestSuiteRequestRequestTypeDef]
    ) -> UpdateTestSuiteResponseTypeDef:
        """
        Updates a test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/update_test_suite.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#update_test_suite)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_test_cases"]) -> ListTestCasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_test_configurations"]
    ) -> ListTestConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_test_run_steps"]
    ) -> ListTestRunStepsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_test_run_test_cases"]
    ) -> ListTestRunTestCasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_test_runs"]) -> ListTestRunsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_test_suites"]) -> ListTestSuitesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/#get_paginator)
        """

    async def __aenter__(self) -> "MainframeModernizationApplicationTestingClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/client/)
        """
