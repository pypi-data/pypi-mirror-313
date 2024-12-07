"""
Type annotations for devicefarm service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_devicefarm.client import DeviceFarmClient

    session = get_session()
    async with session.create_client("devicefarm") as client:
        client: DeviceFarmClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    GetOfferingStatusPaginator,
    ListArtifactsPaginator,
    ListDeviceInstancesPaginator,
    ListDevicePoolsPaginator,
    ListDevicesPaginator,
    ListInstanceProfilesPaginator,
    ListJobsPaginator,
    ListNetworkProfilesPaginator,
    ListOfferingPromotionsPaginator,
    ListOfferingsPaginator,
    ListOfferingTransactionsPaginator,
    ListProjectsPaginator,
    ListRemoteAccessSessionsPaginator,
    ListRunsPaginator,
    ListSamplesPaginator,
    ListSuitesPaginator,
    ListTestsPaginator,
    ListUniqueProblemsPaginator,
    ListUploadsPaginator,
    ListVPCEConfigurationsPaginator,
)
from .type_defs import (
    CreateDevicePoolRequestRequestTypeDef,
    CreateDevicePoolResultTypeDef,
    CreateInstanceProfileRequestRequestTypeDef,
    CreateInstanceProfileResultTypeDef,
    CreateNetworkProfileRequestRequestTypeDef,
    CreateNetworkProfileResultTypeDef,
    CreateProjectRequestRequestTypeDef,
    CreateProjectResultTypeDef,
    CreateRemoteAccessSessionRequestRequestTypeDef,
    CreateRemoteAccessSessionResultTypeDef,
    CreateTestGridProjectRequestRequestTypeDef,
    CreateTestGridProjectResultTypeDef,
    CreateTestGridUrlRequestRequestTypeDef,
    CreateTestGridUrlResultTypeDef,
    CreateUploadRequestRequestTypeDef,
    CreateUploadResultTypeDef,
    CreateVPCEConfigurationRequestRequestTypeDef,
    CreateVPCEConfigurationResultTypeDef,
    DeleteDevicePoolRequestRequestTypeDef,
    DeleteInstanceProfileRequestRequestTypeDef,
    DeleteNetworkProfileRequestRequestTypeDef,
    DeleteProjectRequestRequestTypeDef,
    DeleteRemoteAccessSessionRequestRequestTypeDef,
    DeleteRunRequestRequestTypeDef,
    DeleteTestGridProjectRequestRequestTypeDef,
    DeleteUploadRequestRequestTypeDef,
    DeleteVPCEConfigurationRequestRequestTypeDef,
    GetAccountSettingsResultTypeDef,
    GetDeviceInstanceRequestRequestTypeDef,
    GetDeviceInstanceResultTypeDef,
    GetDevicePoolCompatibilityRequestRequestTypeDef,
    GetDevicePoolCompatibilityResultTypeDef,
    GetDevicePoolRequestRequestTypeDef,
    GetDevicePoolResultTypeDef,
    GetDeviceRequestRequestTypeDef,
    GetDeviceResultTypeDef,
    GetInstanceProfileRequestRequestTypeDef,
    GetInstanceProfileResultTypeDef,
    GetJobRequestRequestTypeDef,
    GetJobResultTypeDef,
    GetNetworkProfileRequestRequestTypeDef,
    GetNetworkProfileResultTypeDef,
    GetOfferingStatusRequestRequestTypeDef,
    GetOfferingStatusResultTypeDef,
    GetProjectRequestRequestTypeDef,
    GetProjectResultTypeDef,
    GetRemoteAccessSessionRequestRequestTypeDef,
    GetRemoteAccessSessionResultTypeDef,
    GetRunRequestRequestTypeDef,
    GetRunResultTypeDef,
    GetSuiteRequestRequestTypeDef,
    GetSuiteResultTypeDef,
    GetTestGridProjectRequestRequestTypeDef,
    GetTestGridProjectResultTypeDef,
    GetTestGridSessionRequestRequestTypeDef,
    GetTestGridSessionResultTypeDef,
    GetTestRequestRequestTypeDef,
    GetTestResultTypeDef,
    GetUploadRequestRequestTypeDef,
    GetUploadResultTypeDef,
    GetVPCEConfigurationRequestRequestTypeDef,
    GetVPCEConfigurationResultTypeDef,
    InstallToRemoteAccessSessionRequestRequestTypeDef,
    InstallToRemoteAccessSessionResultTypeDef,
    ListArtifactsRequestRequestTypeDef,
    ListArtifactsResultTypeDef,
    ListDeviceInstancesRequestRequestTypeDef,
    ListDeviceInstancesResultTypeDef,
    ListDevicePoolsRequestRequestTypeDef,
    ListDevicePoolsResultTypeDef,
    ListDevicesRequestRequestTypeDef,
    ListDevicesResultTypeDef,
    ListInstanceProfilesRequestRequestTypeDef,
    ListInstanceProfilesResultTypeDef,
    ListJobsRequestRequestTypeDef,
    ListJobsResultTypeDef,
    ListNetworkProfilesRequestRequestTypeDef,
    ListNetworkProfilesResultTypeDef,
    ListOfferingPromotionsRequestRequestTypeDef,
    ListOfferingPromotionsResultTypeDef,
    ListOfferingsRequestRequestTypeDef,
    ListOfferingsResultTypeDef,
    ListOfferingTransactionsRequestRequestTypeDef,
    ListOfferingTransactionsResultTypeDef,
    ListProjectsRequestRequestTypeDef,
    ListProjectsResultTypeDef,
    ListRemoteAccessSessionsRequestRequestTypeDef,
    ListRemoteAccessSessionsResultTypeDef,
    ListRunsRequestRequestTypeDef,
    ListRunsResultTypeDef,
    ListSamplesRequestRequestTypeDef,
    ListSamplesResultTypeDef,
    ListSuitesRequestRequestTypeDef,
    ListSuitesResultTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTestGridProjectsRequestRequestTypeDef,
    ListTestGridProjectsResultTypeDef,
    ListTestGridSessionActionsRequestRequestTypeDef,
    ListTestGridSessionActionsResultTypeDef,
    ListTestGridSessionArtifactsRequestRequestTypeDef,
    ListTestGridSessionArtifactsResultTypeDef,
    ListTestGridSessionsRequestRequestTypeDef,
    ListTestGridSessionsResultTypeDef,
    ListTestsRequestRequestTypeDef,
    ListTestsResultTypeDef,
    ListUniqueProblemsRequestRequestTypeDef,
    ListUniqueProblemsResultTypeDef,
    ListUploadsRequestRequestTypeDef,
    ListUploadsResultTypeDef,
    ListVPCEConfigurationsRequestRequestTypeDef,
    ListVPCEConfigurationsResultTypeDef,
    PurchaseOfferingRequestRequestTypeDef,
    PurchaseOfferingResultTypeDef,
    RenewOfferingRequestRequestTypeDef,
    RenewOfferingResultTypeDef,
    ScheduleRunRequestRequestTypeDef,
    ScheduleRunResultTypeDef,
    StopJobRequestRequestTypeDef,
    StopJobResultTypeDef,
    StopRemoteAccessSessionRequestRequestTypeDef,
    StopRemoteAccessSessionResultTypeDef,
    StopRunRequestRequestTypeDef,
    StopRunResultTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDeviceInstanceRequestRequestTypeDef,
    UpdateDeviceInstanceResultTypeDef,
    UpdateDevicePoolRequestRequestTypeDef,
    UpdateDevicePoolResultTypeDef,
    UpdateInstanceProfileRequestRequestTypeDef,
    UpdateInstanceProfileResultTypeDef,
    UpdateNetworkProfileRequestRequestTypeDef,
    UpdateNetworkProfileResultTypeDef,
    UpdateProjectRequestRequestTypeDef,
    UpdateProjectResultTypeDef,
    UpdateTestGridProjectRequestRequestTypeDef,
    UpdateTestGridProjectResultTypeDef,
    UpdateUploadRequestRequestTypeDef,
    UpdateUploadResultTypeDef,
    UpdateVPCEConfigurationRequestRequestTypeDef,
    UpdateVPCEConfigurationResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("DeviceFarmClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ArgumentException: Type[BotocoreClientError]
    CannotDeleteException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    IdempotencyException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidOperationException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotEligibleException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceAccountException: Type[BotocoreClientError]
    TagOperationException: Type[BotocoreClientError]
    TagPolicyException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]


class DeviceFarmClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DeviceFarmClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#close)
        """

    async def create_device_pool(
        self, **kwargs: Unpack[CreateDevicePoolRequestRequestTypeDef]
    ) -> CreateDevicePoolResultTypeDef:
        """
        Creates a device pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/create_device_pool.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_device_pool)
        """

    async def create_instance_profile(
        self, **kwargs: Unpack[CreateInstanceProfileRequestRequestTypeDef]
    ) -> CreateInstanceProfileResultTypeDef:
        """
        Creates a profile that can be applied to one or more private fleet device
        instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/create_instance_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_instance_profile)
        """

    async def create_network_profile(
        self, **kwargs: Unpack[CreateNetworkProfileRequestRequestTypeDef]
    ) -> CreateNetworkProfileResultTypeDef:
        """
        Creates a network profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/create_network_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_network_profile)
        """

    async def create_project(
        self, **kwargs: Unpack[CreateProjectRequestRequestTypeDef]
    ) -> CreateProjectResultTypeDef:
        """
        Creates a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/create_project.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_project)
        """

    async def create_remote_access_session(
        self, **kwargs: Unpack[CreateRemoteAccessSessionRequestRequestTypeDef]
    ) -> CreateRemoteAccessSessionResultTypeDef:
        """
        Specifies and starts a remote access session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/create_remote_access_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_remote_access_session)
        """

    async def create_test_grid_project(
        self, **kwargs: Unpack[CreateTestGridProjectRequestRequestTypeDef]
    ) -> CreateTestGridProjectResultTypeDef:
        """
        Creates a Selenium testing project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/create_test_grid_project.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_test_grid_project)
        """

    async def create_test_grid_url(
        self, **kwargs: Unpack[CreateTestGridUrlRequestRequestTypeDef]
    ) -> CreateTestGridUrlResultTypeDef:
        """
        Creates a signed, short-term URL that can be passed to a Selenium
        <code>RemoteWebDriver</code> constructor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/create_test_grid_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_test_grid_url)
        """

    async def create_upload(
        self, **kwargs: Unpack[CreateUploadRequestRequestTypeDef]
    ) -> CreateUploadResultTypeDef:
        """
        Uploads an app or test scripts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/create_upload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_upload)
        """

    async def create_vpce_configuration(
        self, **kwargs: Unpack[CreateVPCEConfigurationRequestRequestTypeDef]
    ) -> CreateVPCEConfigurationResultTypeDef:
        """
        Creates a configuration record in Device Farm for your Amazon Virtual Private
        Cloud (VPC) endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/create_vpce_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_vpce_configuration)
        """

    async def delete_device_pool(
        self, **kwargs: Unpack[DeleteDevicePoolRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a device pool given the pool ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/delete_device_pool.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_device_pool)
        """

    async def delete_instance_profile(
        self, **kwargs: Unpack[DeleteInstanceProfileRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a profile that can be applied to one or more private device instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/delete_instance_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_instance_profile)
        """

    async def delete_network_profile(
        self, **kwargs: Unpack[DeleteNetworkProfileRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a network profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/delete_network_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_network_profile)
        """

    async def delete_project(
        self, **kwargs: Unpack[DeleteProjectRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an AWS Device Farm project, given the project ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/delete_project.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_project)
        """

    async def delete_remote_access_session(
        self, **kwargs: Unpack[DeleteRemoteAccessSessionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a completed remote access session and its results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/delete_remote_access_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_remote_access_session)
        """

    async def delete_run(self, **kwargs: Unpack[DeleteRunRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the run, given the run ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/delete_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_run)
        """

    async def delete_test_grid_project(
        self, **kwargs: Unpack[DeleteTestGridProjectRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Selenium testing project and all content generated under it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/delete_test_grid_project.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_test_grid_project)
        """

    async def delete_upload(
        self, **kwargs: Unpack[DeleteUploadRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an upload given the upload ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/delete_upload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_upload)
        """

    async def delete_vpce_configuration(
        self, **kwargs: Unpack[DeleteVPCEConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a configuration for your Amazon Virtual Private Cloud (VPC) endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/delete_vpce_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_vpce_configuration)
        """

    async def get_account_settings(self) -> GetAccountSettingsResultTypeDef:
        """
        Returns the number of unmetered iOS or unmetered Android devices that have been
        purchased by the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_account_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_account_settings)
        """

    async def get_device(
        self, **kwargs: Unpack[GetDeviceRequestRequestTypeDef]
    ) -> GetDeviceResultTypeDef:
        """
        Gets information about a unique device type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_device.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_device)
        """

    async def get_device_instance(
        self, **kwargs: Unpack[GetDeviceInstanceRequestRequestTypeDef]
    ) -> GetDeviceInstanceResultTypeDef:
        """
        Returns information about a device instance that belongs to a private device
        fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_device_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_device_instance)
        """

    async def get_device_pool(
        self, **kwargs: Unpack[GetDevicePoolRequestRequestTypeDef]
    ) -> GetDevicePoolResultTypeDef:
        """
        Gets information about a device pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_device_pool.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_device_pool)
        """

    async def get_device_pool_compatibility(
        self, **kwargs: Unpack[GetDevicePoolCompatibilityRequestRequestTypeDef]
    ) -> GetDevicePoolCompatibilityResultTypeDef:
        """
        Gets information about compatibility with a device pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_device_pool_compatibility.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_device_pool_compatibility)
        """

    async def get_instance_profile(
        self, **kwargs: Unpack[GetInstanceProfileRequestRequestTypeDef]
    ) -> GetInstanceProfileResultTypeDef:
        """
        Returns information about the specified instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_instance_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_instance_profile)
        """

    async def get_job(self, **kwargs: Unpack[GetJobRequestRequestTypeDef]) -> GetJobResultTypeDef:
        """
        Gets information about a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_job)
        """

    async def get_network_profile(
        self, **kwargs: Unpack[GetNetworkProfileRequestRequestTypeDef]
    ) -> GetNetworkProfileResultTypeDef:
        """
        Returns information about a network profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_network_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_network_profile)
        """

    async def get_offering_status(
        self, **kwargs: Unpack[GetOfferingStatusRequestRequestTypeDef]
    ) -> GetOfferingStatusResultTypeDef:
        """
        Gets the current status and future status of all offerings purchased by an AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_offering_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_offering_status)
        """

    async def get_project(
        self, **kwargs: Unpack[GetProjectRequestRequestTypeDef]
    ) -> GetProjectResultTypeDef:
        """
        Gets information about a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_project.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_project)
        """

    async def get_remote_access_session(
        self, **kwargs: Unpack[GetRemoteAccessSessionRequestRequestTypeDef]
    ) -> GetRemoteAccessSessionResultTypeDef:
        """
        Returns a link to a currently running remote access session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_remote_access_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_remote_access_session)
        """

    async def get_run(self, **kwargs: Unpack[GetRunRequestRequestTypeDef]) -> GetRunResultTypeDef:
        """
        Gets information about a run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_run)
        """

    async def get_suite(
        self, **kwargs: Unpack[GetSuiteRequestRequestTypeDef]
    ) -> GetSuiteResultTypeDef:
        """
        Gets information about a suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_suite.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_suite)
        """

    async def get_test(
        self, **kwargs: Unpack[GetTestRequestRequestTypeDef]
    ) -> GetTestResultTypeDef:
        """
        Gets information about a test.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_test.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_test)
        """

    async def get_test_grid_project(
        self, **kwargs: Unpack[GetTestGridProjectRequestRequestTypeDef]
    ) -> GetTestGridProjectResultTypeDef:
        """
        Retrieves information about a Selenium testing project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_test_grid_project.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_test_grid_project)
        """

    async def get_test_grid_session(
        self, **kwargs: Unpack[GetTestGridSessionRequestRequestTypeDef]
    ) -> GetTestGridSessionResultTypeDef:
        """
        A session is an instance of a browser created through a
        <code>RemoteWebDriver</code> with the URL from
        <a>CreateTestGridUrlResult$url</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_test_grid_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_test_grid_session)
        """

    async def get_upload(
        self, **kwargs: Unpack[GetUploadRequestRequestTypeDef]
    ) -> GetUploadResultTypeDef:
        """
        Gets information about an upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_upload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_upload)
        """

    async def get_vpce_configuration(
        self, **kwargs: Unpack[GetVPCEConfigurationRequestRequestTypeDef]
    ) -> GetVPCEConfigurationResultTypeDef:
        """
        Returns information about the configuration settings for your Amazon Virtual
        Private Cloud (VPC) endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_vpce_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_vpce_configuration)
        """

    async def install_to_remote_access_session(
        self, **kwargs: Unpack[InstallToRemoteAccessSessionRequestRequestTypeDef]
    ) -> InstallToRemoteAccessSessionResultTypeDef:
        """
        Installs an application to the device in a remote access session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/install_to_remote_access_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#install_to_remote_access_session)
        """

    async def list_artifacts(
        self, **kwargs: Unpack[ListArtifactsRequestRequestTypeDef]
    ) -> ListArtifactsResultTypeDef:
        """
        Gets information about artifacts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_artifacts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_artifacts)
        """

    async def list_device_instances(
        self, **kwargs: Unpack[ListDeviceInstancesRequestRequestTypeDef]
    ) -> ListDeviceInstancesResultTypeDef:
        """
        Returns information about the private device instances associated with one or
        more AWS accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_device_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_device_instances)
        """

    async def list_device_pools(
        self, **kwargs: Unpack[ListDevicePoolsRequestRequestTypeDef]
    ) -> ListDevicePoolsResultTypeDef:
        """
        Gets information about device pools.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_device_pools.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_device_pools)
        """

    async def list_devices(
        self, **kwargs: Unpack[ListDevicesRequestRequestTypeDef]
    ) -> ListDevicesResultTypeDef:
        """
        Gets information about unique device types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_devices.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_devices)
        """

    async def list_instance_profiles(
        self, **kwargs: Unpack[ListInstanceProfilesRequestRequestTypeDef]
    ) -> ListInstanceProfilesResultTypeDef:
        """
        Returns information about all the instance profiles in an AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_instance_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_instance_profiles)
        """

    async def list_jobs(
        self, **kwargs: Unpack[ListJobsRequestRequestTypeDef]
    ) -> ListJobsResultTypeDef:
        """
        Gets information about jobs for a given test run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_jobs)
        """

    async def list_network_profiles(
        self, **kwargs: Unpack[ListNetworkProfilesRequestRequestTypeDef]
    ) -> ListNetworkProfilesResultTypeDef:
        """
        Returns the list of available network profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_network_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_network_profiles)
        """

    async def list_offering_promotions(
        self, **kwargs: Unpack[ListOfferingPromotionsRequestRequestTypeDef]
    ) -> ListOfferingPromotionsResultTypeDef:
        """
        Returns a list of offering promotions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_offering_promotions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_offering_promotions)
        """

    async def list_offering_transactions(
        self, **kwargs: Unpack[ListOfferingTransactionsRequestRequestTypeDef]
    ) -> ListOfferingTransactionsResultTypeDef:
        """
        Returns a list of all historical purchases, renewals, and system renewal
        transactions for an AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_offering_transactions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_offering_transactions)
        """

    async def list_offerings(
        self, **kwargs: Unpack[ListOfferingsRequestRequestTypeDef]
    ) -> ListOfferingsResultTypeDef:
        """
        Returns a list of products or offerings that the user can manage through the
        API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_offerings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_offerings)
        """

    async def list_projects(
        self, **kwargs: Unpack[ListProjectsRequestRequestTypeDef]
    ) -> ListProjectsResultTypeDef:
        """
        Gets information about projects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_projects.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_projects)
        """

    async def list_remote_access_sessions(
        self, **kwargs: Unpack[ListRemoteAccessSessionsRequestRequestTypeDef]
    ) -> ListRemoteAccessSessionsResultTypeDef:
        """
        Returns a list of all currently running remote access sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_remote_access_sessions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_remote_access_sessions)
        """

    async def list_runs(
        self, **kwargs: Unpack[ListRunsRequestRequestTypeDef]
    ) -> ListRunsResultTypeDef:
        """
        Gets information about runs, given an AWS Device Farm project ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_runs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_runs)
        """

    async def list_samples(
        self, **kwargs: Unpack[ListSamplesRequestRequestTypeDef]
    ) -> ListSamplesResultTypeDef:
        """
        Gets information about samples, given an AWS Device Farm job ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_samples.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_samples)
        """

    async def list_suites(
        self, **kwargs: Unpack[ListSuitesRequestRequestTypeDef]
    ) -> ListSuitesResultTypeDef:
        """
        Gets information about test suites for a given job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_suites.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_suites)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List the tags for an AWS Device Farm resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_tags_for_resource)
        """

    async def list_test_grid_projects(
        self, **kwargs: Unpack[ListTestGridProjectsRequestRequestTypeDef]
    ) -> ListTestGridProjectsResultTypeDef:
        """
        Gets a list of all Selenium testing projects in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_test_grid_projects.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_test_grid_projects)
        """

    async def list_test_grid_session_actions(
        self, **kwargs: Unpack[ListTestGridSessionActionsRequestRequestTypeDef]
    ) -> ListTestGridSessionActionsResultTypeDef:
        """
        Returns a list of the actions taken in a <a>TestGridSession</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_test_grid_session_actions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_test_grid_session_actions)
        """

    async def list_test_grid_session_artifacts(
        self, **kwargs: Unpack[ListTestGridSessionArtifactsRequestRequestTypeDef]
    ) -> ListTestGridSessionArtifactsResultTypeDef:
        """
        Retrieves a list of artifacts created during the session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_test_grid_session_artifacts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_test_grid_session_artifacts)
        """

    async def list_test_grid_sessions(
        self, **kwargs: Unpack[ListTestGridSessionsRequestRequestTypeDef]
    ) -> ListTestGridSessionsResultTypeDef:
        """
        Retrieves a list of sessions for a <a>TestGridProject</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_test_grid_sessions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_test_grid_sessions)
        """

    async def list_tests(
        self, **kwargs: Unpack[ListTestsRequestRequestTypeDef]
    ) -> ListTestsResultTypeDef:
        """
        Gets information about tests in a given test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_tests.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_tests)
        """

    async def list_unique_problems(
        self, **kwargs: Unpack[ListUniqueProblemsRequestRequestTypeDef]
    ) -> ListUniqueProblemsResultTypeDef:
        """
        Gets information about unique problems, such as exceptions or crashes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_unique_problems.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_unique_problems)
        """

    async def list_uploads(
        self, **kwargs: Unpack[ListUploadsRequestRequestTypeDef]
    ) -> ListUploadsResultTypeDef:
        """
        Gets information about uploads, given an AWS Device Farm project ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_uploads.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_uploads)
        """

    async def list_vpce_configurations(
        self, **kwargs: Unpack[ListVPCEConfigurationsRequestRequestTypeDef]
    ) -> ListVPCEConfigurationsResultTypeDef:
        """
        Returns information about all Amazon Virtual Private Cloud (VPC) endpoint
        configurations in the AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/list_vpce_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_vpce_configurations)
        """

    async def purchase_offering(
        self, **kwargs: Unpack[PurchaseOfferingRequestRequestTypeDef]
    ) -> PurchaseOfferingResultTypeDef:
        """
        Immediately purchases offerings for an AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/purchase_offering.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#purchase_offering)
        """

    async def renew_offering(
        self, **kwargs: Unpack[RenewOfferingRequestRequestTypeDef]
    ) -> RenewOfferingResultTypeDef:
        """
        Explicitly sets the quantity of devices to renew for an offering, starting from
        the <code>effectiveDate</code> of the next period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/renew_offering.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#renew_offering)
        """

    async def schedule_run(
        self, **kwargs: Unpack[ScheduleRunRequestRequestTypeDef]
    ) -> ScheduleRunResultTypeDef:
        """
        Schedules a run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/schedule_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#schedule_run)
        """

    async def stop_job(
        self, **kwargs: Unpack[StopJobRequestRequestTypeDef]
    ) -> StopJobResultTypeDef:
        """
        Initiates a stop request for the current job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/stop_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#stop_job)
        """

    async def stop_remote_access_session(
        self, **kwargs: Unpack[StopRemoteAccessSessionRequestRequestTypeDef]
    ) -> StopRemoteAccessSessionResultTypeDef:
        """
        Ends a specified remote access session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/stop_remote_access_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#stop_remote_access_session)
        """

    async def stop_run(
        self, **kwargs: Unpack[StopRunRequestRequestTypeDef]
    ) -> StopRunResultTypeDef:
        """
        Initiates a stop request for the current test run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/stop_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#stop_run)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified
        <code>resourceArn</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#untag_resource)
        """

    async def update_device_instance(
        self, **kwargs: Unpack[UpdateDeviceInstanceRequestRequestTypeDef]
    ) -> UpdateDeviceInstanceResultTypeDef:
        """
        Updates information about a private device instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/update_device_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#update_device_instance)
        """

    async def update_device_pool(
        self, **kwargs: Unpack[UpdateDevicePoolRequestRequestTypeDef]
    ) -> UpdateDevicePoolResultTypeDef:
        """
        Modifies the name, description, and rules in a device pool given the attributes
        and the pool ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/update_device_pool.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#update_device_pool)
        """

    async def update_instance_profile(
        self, **kwargs: Unpack[UpdateInstanceProfileRequestRequestTypeDef]
    ) -> UpdateInstanceProfileResultTypeDef:
        """
        Updates information about an existing private device instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/update_instance_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#update_instance_profile)
        """

    async def update_network_profile(
        self, **kwargs: Unpack[UpdateNetworkProfileRequestRequestTypeDef]
    ) -> UpdateNetworkProfileResultTypeDef:
        """
        Updates the network profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/update_network_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#update_network_profile)
        """

    async def update_project(
        self, **kwargs: Unpack[UpdateProjectRequestRequestTypeDef]
    ) -> UpdateProjectResultTypeDef:
        """
        Modifies the specified project name, given the project ARN and a new name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/update_project.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#update_project)
        """

    async def update_test_grid_project(
        self, **kwargs: Unpack[UpdateTestGridProjectRequestRequestTypeDef]
    ) -> UpdateTestGridProjectResultTypeDef:
        """
        Change details of a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/update_test_grid_project.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#update_test_grid_project)
        """

    async def update_upload(
        self, **kwargs: Unpack[UpdateUploadRequestRequestTypeDef]
    ) -> UpdateUploadResultTypeDef:
        """
        Updates an uploaded test spec.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/update_upload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#update_upload)
        """

    async def update_vpce_configuration(
        self, **kwargs: Unpack[UpdateVPCEConfigurationRequestRequestTypeDef]
    ) -> UpdateVPCEConfigurationResultTypeDef:
        """
        Updates information about an Amazon Virtual Private Cloud (VPC) endpoint
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/update_vpce_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#update_vpce_configuration)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_offering_status"]
    ) -> GetOfferingStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_artifacts"]) -> ListArtifactsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_instances"]
    ) -> ListDeviceInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_pools"]
    ) -> ListDevicePoolsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_devices"]) -> ListDevicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_instance_profiles"]
    ) -> ListInstanceProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_network_profiles"]
    ) -> ListNetworkProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_offering_promotions"]
    ) -> ListOfferingPromotionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_offering_transactions"]
    ) -> ListOfferingTransactionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_offerings"]) -> ListOfferingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_remote_access_sessions"]
    ) -> ListRemoteAccessSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_runs"]) -> ListRunsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_samples"]) -> ListSamplesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_suites"]) -> ListSuitesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tests"]) -> ListTestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_unique_problems"]
    ) -> ListUniqueProblemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_uploads"]) -> ListUploadsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_vpce_configurations"]
    ) -> ListVPCEConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """

    async def __aenter__(self) -> "DeviceFarmClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/)
        """
