"""
Type annotations for devicefarm service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_devicefarm.client import DeviceFarmClient
    from types_aiobotocore_devicefarm.paginator import (
        GetOfferingStatusPaginator,
        ListArtifactsPaginator,
        ListDeviceInstancesPaginator,
        ListDevicePoolsPaginator,
        ListDevicesPaginator,
        ListInstanceProfilesPaginator,
        ListJobsPaginator,
        ListNetworkProfilesPaginator,
        ListOfferingPromotionsPaginator,
        ListOfferingTransactionsPaginator,
        ListOfferingsPaginator,
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

    session = get_session()
    with session.create_client("devicefarm") as client:
        client: DeviceFarmClient

        get_offering_status_paginator: GetOfferingStatusPaginator = client.get_paginator("get_offering_status")
        list_artifacts_paginator: ListArtifactsPaginator = client.get_paginator("list_artifacts")
        list_device_instances_paginator: ListDeviceInstancesPaginator = client.get_paginator("list_device_instances")
        list_device_pools_paginator: ListDevicePoolsPaginator = client.get_paginator("list_device_pools")
        list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
        list_instance_profiles_paginator: ListInstanceProfilesPaginator = client.get_paginator("list_instance_profiles")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_network_profiles_paginator: ListNetworkProfilesPaginator = client.get_paginator("list_network_profiles")
        list_offering_promotions_paginator: ListOfferingPromotionsPaginator = client.get_paginator("list_offering_promotions")
        list_offering_transactions_paginator: ListOfferingTransactionsPaginator = client.get_paginator("list_offering_transactions")
        list_offerings_paginator: ListOfferingsPaginator = client.get_paginator("list_offerings")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
        list_remote_access_sessions_paginator: ListRemoteAccessSessionsPaginator = client.get_paginator("list_remote_access_sessions")
        list_runs_paginator: ListRunsPaginator = client.get_paginator("list_runs")
        list_samples_paginator: ListSamplesPaginator = client.get_paginator("list_samples")
        list_suites_paginator: ListSuitesPaginator = client.get_paginator("list_suites")
        list_tests_paginator: ListTestsPaginator = client.get_paginator("list_tests")
        list_unique_problems_paginator: ListUniqueProblemsPaginator = client.get_paginator("list_unique_problems")
        list_uploads_paginator: ListUploadsPaginator = client.get_paginator("list_uploads")
        list_vpce_configurations_paginator: ListVPCEConfigurationsPaginator = client.get_paginator("list_vpce_configurations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetOfferingStatusRequestGetOfferingStatusPaginateTypeDef,
    GetOfferingStatusResultTypeDef,
    ListArtifactsRequestListArtifactsPaginateTypeDef,
    ListArtifactsResultTypeDef,
    ListDeviceInstancesRequestListDeviceInstancesPaginateTypeDef,
    ListDeviceInstancesResultTypeDef,
    ListDevicePoolsRequestListDevicePoolsPaginateTypeDef,
    ListDevicePoolsResultTypeDef,
    ListDevicesRequestListDevicesPaginateTypeDef,
    ListDevicesResultTypeDef,
    ListInstanceProfilesRequestListInstanceProfilesPaginateTypeDef,
    ListInstanceProfilesResultTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResultTypeDef,
    ListNetworkProfilesRequestListNetworkProfilesPaginateTypeDef,
    ListNetworkProfilesResultTypeDef,
    ListOfferingPromotionsRequestListOfferingPromotionsPaginateTypeDef,
    ListOfferingPromotionsResultTypeDef,
    ListOfferingsRequestListOfferingsPaginateTypeDef,
    ListOfferingsResultTypeDef,
    ListOfferingTransactionsRequestListOfferingTransactionsPaginateTypeDef,
    ListOfferingTransactionsResultTypeDef,
    ListProjectsRequestListProjectsPaginateTypeDef,
    ListProjectsResultTypeDef,
    ListRemoteAccessSessionsRequestListRemoteAccessSessionsPaginateTypeDef,
    ListRemoteAccessSessionsResultTypeDef,
    ListRunsRequestListRunsPaginateTypeDef,
    ListRunsResultTypeDef,
    ListSamplesRequestListSamplesPaginateTypeDef,
    ListSamplesResultTypeDef,
    ListSuitesRequestListSuitesPaginateTypeDef,
    ListSuitesResultTypeDef,
    ListTestsRequestListTestsPaginateTypeDef,
    ListTestsResultTypeDef,
    ListUniqueProblemsRequestListUniqueProblemsPaginateTypeDef,
    ListUniqueProblemsResultTypeDef,
    ListUploadsRequestListUploadsPaginateTypeDef,
    ListUploadsResultTypeDef,
    ListVPCEConfigurationsRequestListVPCEConfigurationsPaginateTypeDef,
    ListVPCEConfigurationsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetOfferingStatusPaginator",
    "ListArtifactsPaginator",
    "ListDeviceInstancesPaginator",
    "ListDevicePoolsPaginator",
    "ListDevicesPaginator",
    "ListInstanceProfilesPaginator",
    "ListJobsPaginator",
    "ListNetworkProfilesPaginator",
    "ListOfferingPromotionsPaginator",
    "ListOfferingTransactionsPaginator",
    "ListOfferingsPaginator",
    "ListProjectsPaginator",
    "ListRemoteAccessSessionsPaginator",
    "ListRunsPaginator",
    "ListSamplesPaginator",
    "ListSuitesPaginator",
    "ListTestsPaginator",
    "ListUniqueProblemsPaginator",
    "ListUploadsPaginator",
    "ListVPCEConfigurationsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetOfferingStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/GetOfferingStatus.html#DeviceFarm.Paginator.GetOfferingStatus)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#getofferingstatuspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetOfferingStatusRequestGetOfferingStatusPaginateTypeDef]
    ) -> AsyncIterator[GetOfferingStatusResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/GetOfferingStatus.html#DeviceFarm.Paginator.GetOfferingStatus.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#getofferingstatuspaginator)
        """

class ListArtifactsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListArtifacts.html#DeviceFarm.Paginator.ListArtifacts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listartifactspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListArtifactsRequestListArtifactsPaginateTypeDef]
    ) -> AsyncIterator[ListArtifactsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListArtifacts.html#DeviceFarm.Paginator.ListArtifacts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listartifactspaginator)
        """

class ListDeviceInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListDeviceInstances.html#DeviceFarm.Paginator.ListDeviceInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdeviceinstancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDeviceInstancesRequestListDeviceInstancesPaginateTypeDef]
    ) -> AsyncIterator[ListDeviceInstancesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListDeviceInstances.html#DeviceFarm.Paginator.ListDeviceInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdeviceinstancespaginator)
        """

class ListDevicePoolsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListDevicePools.html#DeviceFarm.Paginator.ListDevicePools)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdevicepoolspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDevicePoolsRequestListDevicePoolsPaginateTypeDef]
    ) -> AsyncIterator[ListDevicePoolsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListDevicePools.html#DeviceFarm.Paginator.ListDevicePools.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdevicepoolspaginator)
        """

class ListDevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListDevices.html#DeviceFarm.Paginator.ListDevices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdevicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDevicesRequestListDevicesPaginateTypeDef]
    ) -> AsyncIterator[ListDevicesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListDevices.html#DeviceFarm.Paginator.ListDevices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdevicespaginator)
        """

class ListInstanceProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListInstanceProfiles.html#DeviceFarm.Paginator.ListInstanceProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listinstanceprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInstanceProfilesRequestListInstanceProfilesPaginateTypeDef]
    ) -> AsyncIterator[ListInstanceProfilesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListInstanceProfiles.html#DeviceFarm.Paginator.ListInstanceProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listinstanceprofilespaginator)
        """

class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListJobs.html#DeviceFarm.Paginator.ListJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> AsyncIterator[ListJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListJobs.html#DeviceFarm.Paginator.ListJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listjobspaginator)
        """

class ListNetworkProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListNetworkProfiles.html#DeviceFarm.Paginator.ListNetworkProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listnetworkprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListNetworkProfilesRequestListNetworkProfilesPaginateTypeDef]
    ) -> AsyncIterator[ListNetworkProfilesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListNetworkProfiles.html#DeviceFarm.Paginator.ListNetworkProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listnetworkprofilespaginator)
        """

class ListOfferingPromotionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListOfferingPromotions.html#DeviceFarm.Paginator.ListOfferingPromotions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingpromotionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListOfferingPromotionsRequestListOfferingPromotionsPaginateTypeDef]
    ) -> AsyncIterator[ListOfferingPromotionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListOfferingPromotions.html#DeviceFarm.Paginator.ListOfferingPromotions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingpromotionspaginator)
        """

class ListOfferingTransactionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListOfferingTransactions.html#DeviceFarm.Paginator.ListOfferingTransactions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingtransactionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListOfferingTransactionsRequestListOfferingTransactionsPaginateTypeDef],
    ) -> AsyncIterator[ListOfferingTransactionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListOfferingTransactions.html#DeviceFarm.Paginator.ListOfferingTransactions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingtransactionspaginator)
        """

class ListOfferingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListOfferings.html#DeviceFarm.Paginator.ListOfferings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListOfferingsRequestListOfferingsPaginateTypeDef]
    ) -> AsyncIterator[ListOfferingsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListOfferings.html#DeviceFarm.Paginator.ListOfferings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingspaginator)
        """

class ListProjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListProjects.html#DeviceFarm.Paginator.ListProjects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listprojectspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProjectsRequestListProjectsPaginateTypeDef]
    ) -> AsyncIterator[ListProjectsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListProjects.html#DeviceFarm.Paginator.ListProjects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listprojectspaginator)
        """

class ListRemoteAccessSessionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListRemoteAccessSessions.html#DeviceFarm.Paginator.ListRemoteAccessSessions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listremoteaccesssessionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListRemoteAccessSessionsRequestListRemoteAccessSessionsPaginateTypeDef],
    ) -> AsyncIterator[ListRemoteAccessSessionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListRemoteAccessSessions.html#DeviceFarm.Paginator.ListRemoteAccessSessions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listremoteaccesssessionspaginator)
        """

class ListRunsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListRuns.html#DeviceFarm.Paginator.ListRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listrunspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRunsRequestListRunsPaginateTypeDef]
    ) -> AsyncIterator[ListRunsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListRuns.html#DeviceFarm.Paginator.ListRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listrunspaginator)
        """

class ListSamplesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListSamples.html#DeviceFarm.Paginator.ListSamples)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listsamplespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSamplesRequestListSamplesPaginateTypeDef]
    ) -> AsyncIterator[ListSamplesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListSamples.html#DeviceFarm.Paginator.ListSamples.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listsamplespaginator)
        """

class ListSuitesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListSuites.html#DeviceFarm.Paginator.ListSuites)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listsuitespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSuitesRequestListSuitesPaginateTypeDef]
    ) -> AsyncIterator[ListSuitesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListSuites.html#DeviceFarm.Paginator.ListSuites.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listsuitespaginator)
        """

class ListTestsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListTests.html#DeviceFarm.Paginator.ListTests)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listtestspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTestsRequestListTestsPaginateTypeDef]
    ) -> AsyncIterator[ListTestsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListTests.html#DeviceFarm.Paginator.ListTests.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listtestspaginator)
        """

class ListUniqueProblemsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListUniqueProblems.html#DeviceFarm.Paginator.ListUniqueProblems)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listuniqueproblemspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUniqueProblemsRequestListUniqueProblemsPaginateTypeDef]
    ) -> AsyncIterator[ListUniqueProblemsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListUniqueProblems.html#DeviceFarm.Paginator.ListUniqueProblems.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listuniqueproblemspaginator)
        """

class ListUploadsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListUploads.html#DeviceFarm.Paginator.ListUploads)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listuploadspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUploadsRequestListUploadsPaginateTypeDef]
    ) -> AsyncIterator[ListUploadsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListUploads.html#DeviceFarm.Paginator.ListUploads.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listuploadspaginator)
        """

class ListVPCEConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListVPCEConfigurations.html#DeviceFarm.Paginator.ListVPCEConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listvpceconfigurationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListVPCEConfigurationsRequestListVPCEConfigurationsPaginateTypeDef]
    ) -> AsyncIterator[ListVPCEConfigurationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListVPCEConfigurations.html#DeviceFarm.Paginator.ListVPCEConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listvpceconfigurationspaginator)
        """
