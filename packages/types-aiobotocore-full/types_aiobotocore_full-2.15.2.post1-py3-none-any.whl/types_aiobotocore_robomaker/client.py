"""
Type annotations for robomaker service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_robomaker.client import RoboMakerClient

    session = get_session()
    async with session.create_client("robomaker") as client:
        client: RoboMakerClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListDeploymentJobsPaginator,
    ListFleetsPaginator,
    ListRobotApplicationsPaginator,
    ListRobotsPaginator,
    ListSimulationApplicationsPaginator,
    ListSimulationJobBatchesPaginator,
    ListSimulationJobsPaginator,
    ListWorldExportJobsPaginator,
    ListWorldGenerationJobsPaginator,
    ListWorldsPaginator,
    ListWorldTemplatesPaginator,
)
from .type_defs import (
    BatchDeleteWorldsRequestRequestTypeDef,
    BatchDeleteWorldsResponseTypeDef,
    BatchDescribeSimulationJobRequestRequestTypeDef,
    BatchDescribeSimulationJobResponseTypeDef,
    CancelDeploymentJobRequestRequestTypeDef,
    CancelSimulationJobBatchRequestRequestTypeDef,
    CancelSimulationJobRequestRequestTypeDef,
    CancelWorldExportJobRequestRequestTypeDef,
    CancelWorldGenerationJobRequestRequestTypeDef,
    CreateDeploymentJobRequestRequestTypeDef,
    CreateDeploymentJobResponseTypeDef,
    CreateFleetRequestRequestTypeDef,
    CreateFleetResponseTypeDef,
    CreateRobotApplicationRequestRequestTypeDef,
    CreateRobotApplicationResponseTypeDef,
    CreateRobotApplicationVersionRequestRequestTypeDef,
    CreateRobotApplicationVersionResponseTypeDef,
    CreateRobotRequestRequestTypeDef,
    CreateRobotResponseTypeDef,
    CreateSimulationApplicationRequestRequestTypeDef,
    CreateSimulationApplicationResponseTypeDef,
    CreateSimulationApplicationVersionRequestRequestTypeDef,
    CreateSimulationApplicationVersionResponseTypeDef,
    CreateSimulationJobRequestRequestTypeDef,
    CreateSimulationJobResponseTypeDef,
    CreateWorldExportJobRequestRequestTypeDef,
    CreateWorldExportJobResponseTypeDef,
    CreateWorldGenerationJobRequestRequestTypeDef,
    CreateWorldGenerationJobResponseTypeDef,
    CreateWorldTemplateRequestRequestTypeDef,
    CreateWorldTemplateResponseTypeDef,
    DeleteFleetRequestRequestTypeDef,
    DeleteRobotApplicationRequestRequestTypeDef,
    DeleteRobotRequestRequestTypeDef,
    DeleteSimulationApplicationRequestRequestTypeDef,
    DeleteWorldTemplateRequestRequestTypeDef,
    DeregisterRobotRequestRequestTypeDef,
    DeregisterRobotResponseTypeDef,
    DescribeDeploymentJobRequestRequestTypeDef,
    DescribeDeploymentJobResponseTypeDef,
    DescribeFleetRequestRequestTypeDef,
    DescribeFleetResponseTypeDef,
    DescribeRobotApplicationRequestRequestTypeDef,
    DescribeRobotApplicationResponseTypeDef,
    DescribeRobotRequestRequestTypeDef,
    DescribeRobotResponseTypeDef,
    DescribeSimulationApplicationRequestRequestTypeDef,
    DescribeSimulationApplicationResponseTypeDef,
    DescribeSimulationJobBatchRequestRequestTypeDef,
    DescribeSimulationJobBatchResponseTypeDef,
    DescribeSimulationJobRequestRequestTypeDef,
    DescribeSimulationJobResponseTypeDef,
    DescribeWorldExportJobRequestRequestTypeDef,
    DescribeWorldExportJobResponseTypeDef,
    DescribeWorldGenerationJobRequestRequestTypeDef,
    DescribeWorldGenerationJobResponseTypeDef,
    DescribeWorldRequestRequestTypeDef,
    DescribeWorldResponseTypeDef,
    DescribeWorldTemplateRequestRequestTypeDef,
    DescribeWorldTemplateResponseTypeDef,
    GetWorldTemplateBodyRequestRequestTypeDef,
    GetWorldTemplateBodyResponseTypeDef,
    ListDeploymentJobsRequestRequestTypeDef,
    ListDeploymentJobsResponseTypeDef,
    ListFleetsRequestRequestTypeDef,
    ListFleetsResponseTypeDef,
    ListRobotApplicationsRequestRequestTypeDef,
    ListRobotApplicationsResponseTypeDef,
    ListRobotsRequestRequestTypeDef,
    ListRobotsResponseTypeDef,
    ListSimulationApplicationsRequestRequestTypeDef,
    ListSimulationApplicationsResponseTypeDef,
    ListSimulationJobBatchesRequestRequestTypeDef,
    ListSimulationJobBatchesResponseTypeDef,
    ListSimulationJobsRequestRequestTypeDef,
    ListSimulationJobsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWorldExportJobsRequestRequestTypeDef,
    ListWorldExportJobsResponseTypeDef,
    ListWorldGenerationJobsRequestRequestTypeDef,
    ListWorldGenerationJobsResponseTypeDef,
    ListWorldsRequestRequestTypeDef,
    ListWorldsResponseTypeDef,
    ListWorldTemplatesRequestRequestTypeDef,
    ListWorldTemplatesResponseTypeDef,
    RegisterRobotRequestRequestTypeDef,
    RegisterRobotResponseTypeDef,
    RestartSimulationJobRequestRequestTypeDef,
    StartSimulationJobBatchRequestRequestTypeDef,
    StartSimulationJobBatchResponseTypeDef,
    SyncDeploymentJobRequestRequestTypeDef,
    SyncDeploymentJobResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateRobotApplicationRequestRequestTypeDef,
    UpdateRobotApplicationResponseTypeDef,
    UpdateSimulationApplicationRequestRequestTypeDef,
    UpdateSimulationApplicationResponseTypeDef,
    UpdateWorldTemplateRequestRequestTypeDef,
    UpdateWorldTemplateResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("RoboMakerClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentDeploymentException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class RoboMakerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        RoboMakerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#close)
        """

    async def batch_delete_worlds(
        self, **kwargs: Unpack[BatchDeleteWorldsRequestRequestTypeDef]
    ) -> BatchDeleteWorldsResponseTypeDef:
        """
        Deletes one or more worlds in a batch operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/batch_delete_worlds.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#batch_delete_worlds)
        """

    async def batch_describe_simulation_job(
        self, **kwargs: Unpack[BatchDescribeSimulationJobRequestRequestTypeDef]
    ) -> BatchDescribeSimulationJobResponseTypeDef:
        """
        Describes one or more simulation jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/batch_describe_simulation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#batch_describe_simulation_job)
        """

    async def cancel_deployment_job(
        self, **kwargs: Unpack[CancelDeploymentJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels the specified deployment job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/cancel_deployment_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#cancel_deployment_job)
        """

    async def cancel_simulation_job(
        self, **kwargs: Unpack[CancelSimulationJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels the specified simulation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/cancel_simulation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#cancel_simulation_job)
        """

    async def cancel_simulation_job_batch(
        self, **kwargs: Unpack[CancelSimulationJobBatchRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels a simulation job batch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/cancel_simulation_job_batch.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#cancel_simulation_job_batch)
        """

    async def cancel_world_export_job(
        self, **kwargs: Unpack[CancelWorldExportJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels the specified export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/cancel_world_export_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#cancel_world_export_job)
        """

    async def cancel_world_generation_job(
        self, **kwargs: Unpack[CancelWorldGenerationJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels the specified world generator job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/cancel_world_generation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#cancel_world_generation_job)
        """

    async def create_deployment_job(
        self, **kwargs: Unpack[CreateDeploymentJobRequestRequestTypeDef]
    ) -> CreateDeploymentJobResponseTypeDef:
        """
        Deploys a specific version of a robot application to robots in a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_deployment_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_deployment_job)
        """

    async def create_fleet(
        self, **kwargs: Unpack[CreateFleetRequestRequestTypeDef]
    ) -> CreateFleetResponseTypeDef:
        """
        Creates a fleet, a logical group of robots running the same robot application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_fleet)
        """

    async def create_robot(
        self, **kwargs: Unpack[CreateRobotRequestRequestTypeDef]
    ) -> CreateRobotResponseTypeDef:
        """
        Creates a robot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_robot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_robot)
        """

    async def create_robot_application(
        self, **kwargs: Unpack[CreateRobotApplicationRequestRequestTypeDef]
    ) -> CreateRobotApplicationResponseTypeDef:
        """
        Creates a robot application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_robot_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_robot_application)
        """

    async def create_robot_application_version(
        self, **kwargs: Unpack[CreateRobotApplicationVersionRequestRequestTypeDef]
    ) -> CreateRobotApplicationVersionResponseTypeDef:
        """
        Creates a version of a robot application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_robot_application_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_robot_application_version)
        """

    async def create_simulation_application(
        self, **kwargs: Unpack[CreateSimulationApplicationRequestRequestTypeDef]
    ) -> CreateSimulationApplicationResponseTypeDef:
        """
        Creates a simulation application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_simulation_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_simulation_application)
        """

    async def create_simulation_application_version(
        self, **kwargs: Unpack[CreateSimulationApplicationVersionRequestRequestTypeDef]
    ) -> CreateSimulationApplicationVersionResponseTypeDef:
        """
        Creates a simulation application with a specific revision id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_simulation_application_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_simulation_application_version)
        """

    async def create_simulation_job(
        self, **kwargs: Unpack[CreateSimulationJobRequestRequestTypeDef]
    ) -> CreateSimulationJobResponseTypeDef:
        """
        Creates a simulation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_simulation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_simulation_job)
        """

    async def create_world_export_job(
        self, **kwargs: Unpack[CreateWorldExportJobRequestRequestTypeDef]
    ) -> CreateWorldExportJobResponseTypeDef:
        """
        Creates a world export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_world_export_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_world_export_job)
        """

    async def create_world_generation_job(
        self, **kwargs: Unpack[CreateWorldGenerationJobRequestRequestTypeDef]
    ) -> CreateWorldGenerationJobResponseTypeDef:
        """
        Creates worlds using the specified template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_world_generation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_world_generation_job)
        """

    async def create_world_template(
        self, **kwargs: Unpack[CreateWorldTemplateRequestRequestTypeDef]
    ) -> CreateWorldTemplateResponseTypeDef:
        """
        Creates a world template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_world_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_world_template)
        """

    async def delete_fleet(
        self, **kwargs: Unpack[DeleteFleetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/delete_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#delete_fleet)
        """

    async def delete_robot(
        self, **kwargs: Unpack[DeleteRobotRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a robot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/delete_robot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#delete_robot)
        """

    async def delete_robot_application(
        self, **kwargs: Unpack[DeleteRobotApplicationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a robot application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/delete_robot_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#delete_robot_application)
        """

    async def delete_simulation_application(
        self, **kwargs: Unpack[DeleteSimulationApplicationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a simulation application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/delete_simulation_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#delete_simulation_application)
        """

    async def delete_world_template(
        self, **kwargs: Unpack[DeleteWorldTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a world template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/delete_world_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#delete_world_template)
        """

    async def deregister_robot(
        self, **kwargs: Unpack[DeregisterRobotRequestRequestTypeDef]
    ) -> DeregisterRobotResponseTypeDef:
        """
        Deregisters a robot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/deregister_robot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#deregister_robot)
        """

    async def describe_deployment_job(
        self, **kwargs: Unpack[DescribeDeploymentJobRequestRequestTypeDef]
    ) -> DescribeDeploymentJobResponseTypeDef:
        """
        Describes a deployment job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_deployment_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_deployment_job)
        """

    async def describe_fleet(
        self, **kwargs: Unpack[DescribeFleetRequestRequestTypeDef]
    ) -> DescribeFleetResponseTypeDef:
        """
        Describes a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_fleet)
        """

    async def describe_robot(
        self, **kwargs: Unpack[DescribeRobotRequestRequestTypeDef]
    ) -> DescribeRobotResponseTypeDef:
        """
        Describes a robot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_robot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_robot)
        """

    async def describe_robot_application(
        self, **kwargs: Unpack[DescribeRobotApplicationRequestRequestTypeDef]
    ) -> DescribeRobotApplicationResponseTypeDef:
        """
        Describes a robot application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_robot_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_robot_application)
        """

    async def describe_simulation_application(
        self, **kwargs: Unpack[DescribeSimulationApplicationRequestRequestTypeDef]
    ) -> DescribeSimulationApplicationResponseTypeDef:
        """
        Describes a simulation application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_simulation_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_simulation_application)
        """

    async def describe_simulation_job(
        self, **kwargs: Unpack[DescribeSimulationJobRequestRequestTypeDef]
    ) -> DescribeSimulationJobResponseTypeDef:
        """
        Describes a simulation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_simulation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_simulation_job)
        """

    async def describe_simulation_job_batch(
        self, **kwargs: Unpack[DescribeSimulationJobBatchRequestRequestTypeDef]
    ) -> DescribeSimulationJobBatchResponseTypeDef:
        """
        Describes a simulation job batch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_simulation_job_batch.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_simulation_job_batch)
        """

    async def describe_world(
        self, **kwargs: Unpack[DescribeWorldRequestRequestTypeDef]
    ) -> DescribeWorldResponseTypeDef:
        """
        Describes a world.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_world.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_world)
        """

    async def describe_world_export_job(
        self, **kwargs: Unpack[DescribeWorldExportJobRequestRequestTypeDef]
    ) -> DescribeWorldExportJobResponseTypeDef:
        """
        Describes a world export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_world_export_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_world_export_job)
        """

    async def describe_world_generation_job(
        self, **kwargs: Unpack[DescribeWorldGenerationJobRequestRequestTypeDef]
    ) -> DescribeWorldGenerationJobResponseTypeDef:
        """
        Describes a world generation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_world_generation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_world_generation_job)
        """

    async def describe_world_template(
        self, **kwargs: Unpack[DescribeWorldTemplateRequestRequestTypeDef]
    ) -> DescribeWorldTemplateResponseTypeDef:
        """
        Describes a world template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_world_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_world_template)
        """

    async def get_world_template_body(
        self, **kwargs: Unpack[GetWorldTemplateBodyRequestRequestTypeDef]
    ) -> GetWorldTemplateBodyResponseTypeDef:
        """
        Gets the world template body.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_world_template_body.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_world_template_body)
        """

    async def list_deployment_jobs(
        self, **kwargs: Unpack[ListDeploymentJobsRequestRequestTypeDef]
    ) -> ListDeploymentJobsResponseTypeDef:
        """
        Returns a list of deployment jobs for a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_deployment_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_deployment_jobs)
        """

    async def list_fleets(
        self, **kwargs: Unpack[ListFleetsRequestRequestTypeDef]
    ) -> ListFleetsResponseTypeDef:
        """
        Returns a list of fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_fleets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_fleets)
        """

    async def list_robot_applications(
        self, **kwargs: Unpack[ListRobotApplicationsRequestRequestTypeDef]
    ) -> ListRobotApplicationsResponseTypeDef:
        """
        Returns a list of robot application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_robot_applications.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_robot_applications)
        """

    async def list_robots(
        self, **kwargs: Unpack[ListRobotsRequestRequestTypeDef]
    ) -> ListRobotsResponseTypeDef:
        """
        Returns a list of robots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_robots.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_robots)
        """

    async def list_simulation_applications(
        self, **kwargs: Unpack[ListSimulationApplicationsRequestRequestTypeDef]
    ) -> ListSimulationApplicationsResponseTypeDef:
        """
        Returns a list of simulation applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_simulation_applications.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_simulation_applications)
        """

    async def list_simulation_job_batches(
        self, **kwargs: Unpack[ListSimulationJobBatchesRequestRequestTypeDef]
    ) -> ListSimulationJobBatchesResponseTypeDef:
        """
        Returns a list simulation job batches.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_simulation_job_batches.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_simulation_job_batches)
        """

    async def list_simulation_jobs(
        self, **kwargs: Unpack[ListSimulationJobsRequestRequestTypeDef]
    ) -> ListSimulationJobsResponseTypeDef:
        """
        Returns a list of simulation jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_simulation_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_simulation_jobs)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags on a AWS RoboMaker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_tags_for_resource)
        """

    async def list_world_export_jobs(
        self, **kwargs: Unpack[ListWorldExportJobsRequestRequestTypeDef]
    ) -> ListWorldExportJobsResponseTypeDef:
        """
        Lists world export jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_world_export_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_world_export_jobs)
        """

    async def list_world_generation_jobs(
        self, **kwargs: Unpack[ListWorldGenerationJobsRequestRequestTypeDef]
    ) -> ListWorldGenerationJobsResponseTypeDef:
        """
        Lists world generator jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_world_generation_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_world_generation_jobs)
        """

    async def list_world_templates(
        self, **kwargs: Unpack[ListWorldTemplatesRequestRequestTypeDef]
    ) -> ListWorldTemplatesResponseTypeDef:
        """
        Lists world templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_world_templates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_world_templates)
        """

    async def list_worlds(
        self, **kwargs: Unpack[ListWorldsRequestRequestTypeDef]
    ) -> ListWorldsResponseTypeDef:
        """
        Lists worlds.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_worlds.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_worlds)
        """

    async def register_robot(
        self, **kwargs: Unpack[RegisterRobotRequestRequestTypeDef]
    ) -> RegisterRobotResponseTypeDef:
        """
        Registers a robot with a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/register_robot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#register_robot)
        """

    async def restart_simulation_job(
        self, **kwargs: Unpack[RestartSimulationJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Restarts a running simulation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/restart_simulation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#restart_simulation_job)
        """

    async def start_simulation_job_batch(
        self, **kwargs: Unpack[StartSimulationJobBatchRequestRequestTypeDef]
    ) -> StartSimulationJobBatchResponseTypeDef:
        """
        Starts a new simulation job batch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/start_simulation_job_batch.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#start_simulation_job_batch)
        """

    async def sync_deployment_job(
        self, **kwargs: Unpack[SyncDeploymentJobRequestRequestTypeDef]
    ) -> SyncDeploymentJobResponseTypeDef:
        """
        Syncrhonizes robots in a fleet to the latest deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/sync_deployment_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#sync_deployment_job)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds or edits tags for a AWS RoboMaker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified AWS RoboMaker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#untag_resource)
        """

    async def update_robot_application(
        self, **kwargs: Unpack[UpdateRobotApplicationRequestRequestTypeDef]
    ) -> UpdateRobotApplicationResponseTypeDef:
        """
        Updates a robot application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/update_robot_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#update_robot_application)
        """

    async def update_simulation_application(
        self, **kwargs: Unpack[UpdateSimulationApplicationRequestRequestTypeDef]
    ) -> UpdateSimulationApplicationResponseTypeDef:
        """
        Updates a simulation application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/update_simulation_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#update_simulation_application)
        """

    async def update_world_template(
        self, **kwargs: Unpack[UpdateWorldTemplateRequestRequestTypeDef]
    ) -> UpdateWorldTemplateResponseTypeDef:
        """
        Updates a world template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/update_world_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#update_world_template)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_deployment_jobs"]
    ) -> ListDeploymentJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_fleets"]) -> ListFleetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_robot_applications"]
    ) -> ListRobotApplicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_robots"]) -> ListRobotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_simulation_applications"]
    ) -> ListSimulationApplicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_simulation_job_batches"]
    ) -> ListSimulationJobBatchesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_simulation_jobs"]
    ) -> ListSimulationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_world_export_jobs"]
    ) -> ListWorldExportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_world_generation_jobs"]
    ) -> ListWorldGenerationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_world_templates"]
    ) -> ListWorldTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_worlds"]) -> ListWorldsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    async def __aenter__(self) -> "RoboMakerClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/)
        """
