"""
Type annotations for application-signals service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_application_signals.client import CloudWatchApplicationSignalsClient

    session = get_session()
    async with session.create_client("application-signals") as client:
        client: CloudWatchApplicationSignalsClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListServiceDependenciesPaginator,
    ListServiceDependentsPaginator,
    ListServiceLevelObjectivesPaginator,
    ListServiceOperationsPaginator,
    ListServicesPaginator,
)
from .type_defs import (
    BatchGetServiceLevelObjectiveBudgetReportInputRequestTypeDef,
    BatchGetServiceLevelObjectiveBudgetReportOutputTypeDef,
    CreateServiceLevelObjectiveInputRequestTypeDef,
    CreateServiceLevelObjectiveOutputTypeDef,
    DeleteServiceLevelObjectiveInputRequestTypeDef,
    GetServiceInputRequestTypeDef,
    GetServiceLevelObjectiveInputRequestTypeDef,
    GetServiceLevelObjectiveOutputTypeDef,
    GetServiceOutputTypeDef,
    ListServiceDependenciesInputRequestTypeDef,
    ListServiceDependenciesOutputTypeDef,
    ListServiceDependentsInputRequestTypeDef,
    ListServiceDependentsOutputTypeDef,
    ListServiceLevelObjectivesInputRequestTypeDef,
    ListServiceLevelObjectivesOutputTypeDef,
    ListServiceOperationsInputRequestTypeDef,
    ListServiceOperationsOutputTypeDef,
    ListServicesInputRequestTypeDef,
    ListServicesOutputTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateServiceLevelObjectiveInputRequestTypeDef,
    UpdateServiceLevelObjectiveOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("CloudWatchApplicationSignalsClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CloudWatchApplicationSignalsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals.html#CloudWatchApplicationSignals.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudWatchApplicationSignalsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals.html#CloudWatchApplicationSignals.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#close)
        """

    async def batch_get_service_level_objective_budget_report(
        self, **kwargs: Unpack[BatchGetServiceLevelObjectiveBudgetReportInputRequestTypeDef]
    ) -> BatchGetServiceLevelObjectiveBudgetReportOutputTypeDef:
        """
        Use this operation to retrieve one or more <i>service level objective (SLO)
        budget reports</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/batch_get_service_level_objective_budget_report.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#batch_get_service_level_objective_budget_report)
        """

    async def create_service_level_objective(
        self, **kwargs: Unpack[CreateServiceLevelObjectiveInputRequestTypeDef]
    ) -> CreateServiceLevelObjectiveOutputTypeDef:
        """
        Creates a service level objective (SLO), which can help you ensure that your
        critical business operations are meeting customer expectations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/create_service_level_objective.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#create_service_level_objective)
        """

    async def delete_service_level_objective(
        self, **kwargs: Unpack[DeleteServiceLevelObjectiveInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified service level objective.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/delete_service_level_objective.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#delete_service_level_objective)
        """

    async def get_service(
        self, **kwargs: Unpack[GetServiceInputRequestTypeDef]
    ) -> GetServiceOutputTypeDef:
        """
        Returns information about a service discovered by Application Signals.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#get_service)
        """

    async def get_service_level_objective(
        self, **kwargs: Unpack[GetServiceLevelObjectiveInputRequestTypeDef]
    ) -> GetServiceLevelObjectiveOutputTypeDef:
        """
        Returns information about one SLO created in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_service_level_objective.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#get_service_level_objective)
        """

    async def list_service_dependencies(
        self, **kwargs: Unpack[ListServiceDependenciesInputRequestTypeDef]
    ) -> ListServiceDependenciesOutputTypeDef:
        """
        Returns a list of service dependencies of the service that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_service_dependencies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#list_service_dependencies)
        """

    async def list_service_dependents(
        self, **kwargs: Unpack[ListServiceDependentsInputRequestTypeDef]
    ) -> ListServiceDependentsOutputTypeDef:
        """
        Returns the list of dependents that invoked the specified service during the
        provided time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_service_dependents.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#list_service_dependents)
        """

    async def list_service_level_objectives(
        self, **kwargs: Unpack[ListServiceLevelObjectivesInputRequestTypeDef]
    ) -> ListServiceLevelObjectivesOutputTypeDef:
        """
        Returns a list of SLOs created in this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_service_level_objectives.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#list_service_level_objectives)
        """

    async def list_service_operations(
        self, **kwargs: Unpack[ListServiceOperationsInputRequestTypeDef]
    ) -> ListServiceOperationsOutputTypeDef:
        """
        Returns a list of the <i>operations</i> of this service that have been
        discovered by Application Signals.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_service_operations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#list_service_operations)
        """

    async def list_services(
        self, **kwargs: Unpack[ListServicesInputRequestTypeDef]
    ) -> ListServicesOutputTypeDef:
        """
        Returns a list of services that have been discovered by Application Signals.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_services.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#list_services)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Displays the tags associated with a CloudWatch resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#list_tags_for_resource)
        """

    async def start_discovery(self) -> Dict[str, Any]:
        """
        Enables this Amazon Web Services account to be able to use CloudWatch
        Application Signals by creating the
        <i>AWSServiceRoleForCloudWatchApplicationSignals</i> service-linked role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/start_discovery.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#start_discovery)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified CloudWatch
        resource, such as a service level objective.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#untag_resource)
        """

    async def update_service_level_objective(
        self, **kwargs: Unpack[UpdateServiceLevelObjectiveInputRequestTypeDef]
    ) -> UpdateServiceLevelObjectiveOutputTypeDef:
        """
        Updates an existing service level objective (SLO).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/update_service_level_objective.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#update_service_level_objective)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_dependencies"]
    ) -> ListServiceDependenciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_dependents"]
    ) -> ListServiceDependentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_level_objectives"]
    ) -> ListServiceLevelObjectivesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_operations"]
    ) -> ListServiceOperationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_services"]) -> ListServicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/#get_paginator)
        """

    async def __aenter__(self) -> "CloudWatchApplicationSignalsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals.html#CloudWatchApplicationSignals.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals.html#CloudWatchApplicationSignals.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/client/)
        """
