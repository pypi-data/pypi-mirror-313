"""
Type annotations for sms service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sms.client import SMSClient

    session = get_session()
    async with session.create_client("sms") as client:
        client: SMSClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    GetConnectorsPaginator,
    GetReplicationJobsPaginator,
    GetReplicationRunsPaginator,
    GetServersPaginator,
    ListAppsPaginator,
)
from .type_defs import (
    CreateAppRequestRequestTypeDef,
    CreateAppResponseTypeDef,
    CreateReplicationJobRequestRequestTypeDef,
    CreateReplicationJobResponseTypeDef,
    DeleteAppLaunchConfigurationRequestRequestTypeDef,
    DeleteAppReplicationConfigurationRequestRequestTypeDef,
    DeleteAppRequestRequestTypeDef,
    DeleteAppValidationConfigurationRequestRequestTypeDef,
    DeleteReplicationJobRequestRequestTypeDef,
    DisassociateConnectorRequestRequestTypeDef,
    GenerateChangeSetRequestRequestTypeDef,
    GenerateChangeSetResponseTypeDef,
    GenerateTemplateRequestRequestTypeDef,
    GenerateTemplateResponseTypeDef,
    GetAppLaunchConfigurationRequestRequestTypeDef,
    GetAppLaunchConfigurationResponseTypeDef,
    GetAppReplicationConfigurationRequestRequestTypeDef,
    GetAppReplicationConfigurationResponseTypeDef,
    GetAppRequestRequestTypeDef,
    GetAppResponseTypeDef,
    GetAppValidationConfigurationRequestRequestTypeDef,
    GetAppValidationConfigurationResponseTypeDef,
    GetAppValidationOutputRequestRequestTypeDef,
    GetAppValidationOutputResponseTypeDef,
    GetConnectorsRequestRequestTypeDef,
    GetConnectorsResponseTypeDef,
    GetReplicationJobsRequestRequestTypeDef,
    GetReplicationJobsResponseTypeDef,
    GetReplicationRunsRequestRequestTypeDef,
    GetReplicationRunsResponseTypeDef,
    GetServersRequestRequestTypeDef,
    GetServersResponseTypeDef,
    ImportAppCatalogRequestRequestTypeDef,
    LaunchAppRequestRequestTypeDef,
    ListAppsRequestRequestTypeDef,
    ListAppsResponseTypeDef,
    NotifyAppValidationOutputRequestRequestTypeDef,
    PutAppLaunchConfigurationRequestRequestTypeDef,
    PutAppReplicationConfigurationRequestRequestTypeDef,
    PutAppValidationConfigurationRequestRequestTypeDef,
    StartAppReplicationRequestRequestTypeDef,
    StartOnDemandAppReplicationRequestRequestTypeDef,
    StartOnDemandReplicationRunRequestRequestTypeDef,
    StartOnDemandReplicationRunResponseTypeDef,
    StopAppReplicationRequestRequestTypeDef,
    TerminateAppRequestRequestTypeDef,
    UpdateAppRequestRequestTypeDef,
    UpdateAppResponseTypeDef,
    UpdateReplicationJobRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("SMSClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    DryRunOperationException: Type[BotocoreClientError]
    InternalError: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    MissingRequiredParameterException: Type[BotocoreClientError]
    NoConnectorsAvailableException: Type[BotocoreClientError]
    OperationNotPermittedException: Type[BotocoreClientError]
    ReplicationJobAlreadyExistsException: Type[BotocoreClientError]
    ReplicationJobNotFoundException: Type[BotocoreClientError]
    ReplicationRunLimitExceededException: Type[BotocoreClientError]
    ServerCannotBeReplicatedException: Type[BotocoreClientError]
    TemporarilyUnavailableException: Type[BotocoreClientError]
    UnauthorizedOperationException: Type[BotocoreClientError]


class SMSClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms.html#SMS.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SMSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms.html#SMS.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#close)
        """

    async def create_app(
        self, **kwargs: Unpack[CreateAppRequestRequestTypeDef]
    ) -> CreateAppResponseTypeDef:
        """
        Creates an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/create_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#create_app)
        """

    async def create_replication_job(
        self, **kwargs: Unpack[CreateReplicationJobRequestRequestTypeDef]
    ) -> CreateReplicationJobResponseTypeDef:
        """
        Creates a replication job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/create_replication_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#create_replication_job)
        """

    async def delete_app(self, **kwargs: Unpack[DeleteAppRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/delete_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#delete_app)
        """

    async def delete_app_launch_configuration(
        self, **kwargs: Unpack[DeleteAppLaunchConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the launch configuration for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/delete_app_launch_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#delete_app_launch_configuration)
        """

    async def delete_app_replication_configuration(
        self, **kwargs: Unpack[DeleteAppReplicationConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the replication configuration for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/delete_app_replication_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#delete_app_replication_configuration)
        """

    async def delete_app_validation_configuration(
        self, **kwargs: Unpack[DeleteAppValidationConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the validation configuration for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/delete_app_validation_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#delete_app_validation_configuration)
        """

    async def delete_replication_job(
        self, **kwargs: Unpack[DeleteReplicationJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified replication job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/delete_replication_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#delete_replication_job)
        """

    async def delete_server_catalog(self) -> Dict[str, Any]:
        """
        Deletes all servers from your server catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/delete_server_catalog.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#delete_server_catalog)
        """

    async def disassociate_connector(
        self, **kwargs: Unpack[DisassociateConnectorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the specified connector from Server Migration Service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/disassociate_connector.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#disassociate_connector)
        """

    async def generate_change_set(
        self, **kwargs: Unpack[GenerateChangeSetRequestRequestTypeDef]
    ) -> GenerateChangeSetResponseTypeDef:
        """
        Generates a target change set for a currently launched stack and writes it to
        an Amazon S3 object in the customer's Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/generate_change_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#generate_change_set)
        """

    async def generate_template(
        self, **kwargs: Unpack[GenerateTemplateRequestRequestTypeDef]
    ) -> GenerateTemplateResponseTypeDef:
        """
        Generates an CloudFormation template based on the current launch configuration
        and writes it to an Amazon S3 object in the customer's Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/generate_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#generate_template)
        """

    async def get_app(self, **kwargs: Unpack[GetAppRequestRequestTypeDef]) -> GetAppResponseTypeDef:
        """
        Retrieve information about the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#get_app)
        """

    async def get_app_launch_configuration(
        self, **kwargs: Unpack[GetAppLaunchConfigurationRequestRequestTypeDef]
    ) -> GetAppLaunchConfigurationResponseTypeDef:
        """
        Retrieves the application launch configuration associated with the specified
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_app_launch_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#get_app_launch_configuration)
        """

    async def get_app_replication_configuration(
        self, **kwargs: Unpack[GetAppReplicationConfigurationRequestRequestTypeDef]
    ) -> GetAppReplicationConfigurationResponseTypeDef:
        """
        Retrieves the application replication configuration associated with the
        specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_app_replication_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#get_app_replication_configuration)
        """

    async def get_app_validation_configuration(
        self, **kwargs: Unpack[GetAppValidationConfigurationRequestRequestTypeDef]
    ) -> GetAppValidationConfigurationResponseTypeDef:
        """
        Retrieves information about a configuration for validating an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_app_validation_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#get_app_validation_configuration)
        """

    async def get_app_validation_output(
        self, **kwargs: Unpack[GetAppValidationOutputRequestRequestTypeDef]
    ) -> GetAppValidationOutputResponseTypeDef:
        """
        Retrieves output from validating an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_app_validation_output.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#get_app_validation_output)
        """

    async def get_connectors(
        self, **kwargs: Unpack[GetConnectorsRequestRequestTypeDef]
    ) -> GetConnectorsResponseTypeDef:
        """
        Describes the connectors registered with the Server Migration Service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_connectors.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#get_connectors)
        """

    async def get_replication_jobs(
        self, **kwargs: Unpack[GetReplicationJobsRequestRequestTypeDef]
    ) -> GetReplicationJobsResponseTypeDef:
        """
        Describes the specified replication job or all of your replication jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_replication_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#get_replication_jobs)
        """

    async def get_replication_runs(
        self, **kwargs: Unpack[GetReplicationRunsRequestRequestTypeDef]
    ) -> GetReplicationRunsResponseTypeDef:
        """
        Describes the replication runs for the specified replication job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_replication_runs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#get_replication_runs)
        """

    async def get_servers(
        self, **kwargs: Unpack[GetServersRequestRequestTypeDef]
    ) -> GetServersResponseTypeDef:
        """
        Describes the servers in your server catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_servers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#get_servers)
        """

    async def import_app_catalog(
        self, **kwargs: Unpack[ImportAppCatalogRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Allows application import from Migration Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/import_app_catalog.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#import_app_catalog)
        """

    async def import_server_catalog(self) -> Dict[str, Any]:
        """
        Gathers a complete list of on-premises servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/import_server_catalog.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#import_server_catalog)
        """

    async def launch_app(self, **kwargs: Unpack[LaunchAppRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Launches the specified application as a stack in CloudFormation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/launch_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#launch_app)
        """

    async def list_apps(
        self, **kwargs: Unpack[ListAppsRequestRequestTypeDef]
    ) -> ListAppsResponseTypeDef:
        """
        Retrieves summaries for all applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/list_apps.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#list_apps)
        """

    async def notify_app_validation_output(
        self, **kwargs: Unpack[NotifyAppValidationOutputRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Provides information to Server Migration Service about whether application
        validation is successful.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/notify_app_validation_output.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#notify_app_validation_output)
        """

    async def put_app_launch_configuration(
        self, **kwargs: Unpack[PutAppLaunchConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates or updates the launch configuration for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/put_app_launch_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#put_app_launch_configuration)
        """

    async def put_app_replication_configuration(
        self, **kwargs: Unpack[PutAppReplicationConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates or updates the replication configuration for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/put_app_replication_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#put_app_replication_configuration)
        """

    async def put_app_validation_configuration(
        self, **kwargs: Unpack[PutAppValidationConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates or updates a validation configuration for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/put_app_validation_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#put_app_validation_configuration)
        """

    async def start_app_replication(
        self, **kwargs: Unpack[StartAppReplicationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Starts replicating the specified application by creating replication jobs for
        each server in the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/start_app_replication.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#start_app_replication)
        """

    async def start_on_demand_app_replication(
        self, **kwargs: Unpack[StartOnDemandAppReplicationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Starts an on-demand replication run for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/start_on_demand_app_replication.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#start_on_demand_app_replication)
        """

    async def start_on_demand_replication_run(
        self, **kwargs: Unpack[StartOnDemandReplicationRunRequestRequestTypeDef]
    ) -> StartOnDemandReplicationRunResponseTypeDef:
        """
        Starts an on-demand replication run for the specified replication job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/start_on_demand_replication_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#start_on_demand_replication_run)
        """

    async def stop_app_replication(
        self, **kwargs: Unpack[StopAppReplicationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops replicating the specified application by deleting the replication job for
        each server in the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/stop_app_replication.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#stop_app_replication)
        """

    async def terminate_app(
        self, **kwargs: Unpack[TerminateAppRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Terminates the stack for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/terminate_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#terminate_app)
        """

    async def update_app(
        self, **kwargs: Unpack[UpdateAppRequestRequestTypeDef]
    ) -> UpdateAppResponseTypeDef:
        """
        Updates the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/update_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#update_app)
        """

    async def update_replication_job(
        self, **kwargs: Unpack[UpdateReplicationJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the specified settings for the specified replication job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/update_replication_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#update_replication_job)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_connectors"]) -> GetConnectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_replication_jobs"]
    ) -> GetReplicationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_replication_runs"]
    ) -> GetReplicationRunsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_servers"]) -> GetServersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_apps"]) -> ListAppsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/#get_paginator)
        """

    async def __aenter__(self) -> "SMSClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms.html#SMS.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms.html#SMS.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/client/)
        """
