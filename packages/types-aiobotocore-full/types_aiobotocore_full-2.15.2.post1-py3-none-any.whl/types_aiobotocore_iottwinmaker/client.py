"""
Type annotations for iottwinmaker service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iottwinmaker.client import IoTTwinMakerClient

    session = get_session()
    async with session.create_client("iottwinmaker") as client:
        client: IoTTwinMakerClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    BatchPutPropertyValuesRequestRequestTypeDef,
    BatchPutPropertyValuesResponseTypeDef,
    CancelMetadataTransferJobRequestRequestTypeDef,
    CancelMetadataTransferJobResponseTypeDef,
    CreateComponentTypeRequestRequestTypeDef,
    CreateComponentTypeResponseTypeDef,
    CreateEntityRequestRequestTypeDef,
    CreateEntityResponseTypeDef,
    CreateMetadataTransferJobRequestRequestTypeDef,
    CreateMetadataTransferJobResponseTypeDef,
    CreateSceneRequestRequestTypeDef,
    CreateSceneResponseTypeDef,
    CreateSyncJobRequestRequestTypeDef,
    CreateSyncJobResponseTypeDef,
    CreateWorkspaceRequestRequestTypeDef,
    CreateWorkspaceResponseTypeDef,
    DeleteComponentTypeRequestRequestTypeDef,
    DeleteComponentTypeResponseTypeDef,
    DeleteEntityRequestRequestTypeDef,
    DeleteEntityResponseTypeDef,
    DeleteSceneRequestRequestTypeDef,
    DeleteSyncJobRequestRequestTypeDef,
    DeleteSyncJobResponseTypeDef,
    DeleteWorkspaceRequestRequestTypeDef,
    DeleteWorkspaceResponseTypeDef,
    ExecuteQueryRequestRequestTypeDef,
    ExecuteQueryResponseTypeDef,
    GetComponentTypeRequestRequestTypeDef,
    GetComponentTypeResponseTypeDef,
    GetEntityRequestRequestTypeDef,
    GetEntityResponseTypeDef,
    GetMetadataTransferJobRequestRequestTypeDef,
    GetMetadataTransferJobResponseTypeDef,
    GetPricingPlanResponseTypeDef,
    GetPropertyValueHistoryRequestRequestTypeDef,
    GetPropertyValueHistoryResponseTypeDef,
    GetPropertyValueRequestRequestTypeDef,
    GetPropertyValueResponseTypeDef,
    GetSceneRequestRequestTypeDef,
    GetSceneResponseTypeDef,
    GetSyncJobRequestRequestTypeDef,
    GetSyncJobResponseTypeDef,
    GetWorkspaceRequestRequestTypeDef,
    GetWorkspaceResponseTypeDef,
    ListComponentsRequestRequestTypeDef,
    ListComponentsResponseTypeDef,
    ListComponentTypesRequestRequestTypeDef,
    ListComponentTypesResponseTypeDef,
    ListEntitiesRequestRequestTypeDef,
    ListEntitiesResponseTypeDef,
    ListMetadataTransferJobsRequestRequestTypeDef,
    ListMetadataTransferJobsResponseTypeDef,
    ListPropertiesRequestRequestTypeDef,
    ListPropertiesResponseTypeDef,
    ListScenesRequestRequestTypeDef,
    ListScenesResponseTypeDef,
    ListSyncJobsRequestRequestTypeDef,
    ListSyncJobsResponseTypeDef,
    ListSyncResourcesRequestRequestTypeDef,
    ListSyncResourcesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWorkspacesRequestRequestTypeDef,
    ListWorkspacesResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateComponentTypeRequestRequestTypeDef,
    UpdateComponentTypeResponseTypeDef,
    UpdateEntityRequestRequestTypeDef,
    UpdateEntityResponseTypeDef,
    UpdatePricingPlanRequestRequestTypeDef,
    UpdatePricingPlanResponseTypeDef,
    UpdateSceneRequestRequestTypeDef,
    UpdateSceneResponseTypeDef,
    UpdateWorkspaceRequestRequestTypeDef,
    UpdateWorkspaceResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("IoTTwinMakerClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ConnectorFailureException: Type[BotocoreClientError]
    ConnectorTimeoutException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    QueryTimeoutException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class IoTTwinMakerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTTwinMakerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#close)
        """

    async def batch_put_property_values(
        self, **kwargs: Unpack[BatchPutPropertyValuesRequestRequestTypeDef]
    ) -> BatchPutPropertyValuesResponseTypeDef:
        """
        Sets values for multiple time series properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/batch_put_property_values.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#batch_put_property_values)
        """

    async def cancel_metadata_transfer_job(
        self, **kwargs: Unpack[CancelMetadataTransferJobRequestRequestTypeDef]
    ) -> CancelMetadataTransferJobResponseTypeDef:
        """
        Cancels the metadata transfer job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/cancel_metadata_transfer_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#cancel_metadata_transfer_job)
        """

    async def create_component_type(
        self, **kwargs: Unpack[CreateComponentTypeRequestRequestTypeDef]
    ) -> CreateComponentTypeResponseTypeDef:
        """
        Creates a component type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/create_component_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#create_component_type)
        """

    async def create_entity(
        self, **kwargs: Unpack[CreateEntityRequestRequestTypeDef]
    ) -> CreateEntityResponseTypeDef:
        """
        Creates an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/create_entity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#create_entity)
        """

    async def create_metadata_transfer_job(
        self, **kwargs: Unpack[CreateMetadataTransferJobRequestRequestTypeDef]
    ) -> CreateMetadataTransferJobResponseTypeDef:
        """
        Creates a new metadata transfer job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/create_metadata_transfer_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#create_metadata_transfer_job)
        """

    async def create_scene(
        self, **kwargs: Unpack[CreateSceneRequestRequestTypeDef]
    ) -> CreateSceneResponseTypeDef:
        """
        Creates a scene.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/create_scene.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#create_scene)
        """

    async def create_sync_job(
        self, **kwargs: Unpack[CreateSyncJobRequestRequestTypeDef]
    ) -> CreateSyncJobResponseTypeDef:
        """
        This action creates a SyncJob.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/create_sync_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#create_sync_job)
        """

    async def create_workspace(
        self, **kwargs: Unpack[CreateWorkspaceRequestRequestTypeDef]
    ) -> CreateWorkspaceResponseTypeDef:
        """
        Creates a workplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/create_workspace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#create_workspace)
        """

    async def delete_component_type(
        self, **kwargs: Unpack[DeleteComponentTypeRequestRequestTypeDef]
    ) -> DeleteComponentTypeResponseTypeDef:
        """
        Deletes a component type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/delete_component_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#delete_component_type)
        """

    async def delete_entity(
        self, **kwargs: Unpack[DeleteEntityRequestRequestTypeDef]
    ) -> DeleteEntityResponseTypeDef:
        """
        Deletes an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/delete_entity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#delete_entity)
        """

    async def delete_scene(
        self, **kwargs: Unpack[DeleteSceneRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a scene.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/delete_scene.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#delete_scene)
        """

    async def delete_sync_job(
        self, **kwargs: Unpack[DeleteSyncJobRequestRequestTypeDef]
    ) -> DeleteSyncJobResponseTypeDef:
        """
        Delete the SyncJob.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/delete_sync_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#delete_sync_job)
        """

    async def delete_workspace(
        self, **kwargs: Unpack[DeleteWorkspaceRequestRequestTypeDef]
    ) -> DeleteWorkspaceResponseTypeDef:
        """
        Deletes a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/delete_workspace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#delete_workspace)
        """

    async def execute_query(
        self, **kwargs: Unpack[ExecuteQueryRequestRequestTypeDef]
    ) -> ExecuteQueryResponseTypeDef:
        """
        Run queries to access information from your knowledge graph of entities within
        individual workspaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/execute_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#execute_query)
        """

    async def get_component_type(
        self, **kwargs: Unpack[GetComponentTypeRequestRequestTypeDef]
    ) -> GetComponentTypeResponseTypeDef:
        """
        Retrieves information about a component type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/get_component_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#get_component_type)
        """

    async def get_entity(
        self, **kwargs: Unpack[GetEntityRequestRequestTypeDef]
    ) -> GetEntityResponseTypeDef:
        """
        Retrieves information about an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/get_entity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#get_entity)
        """

    async def get_metadata_transfer_job(
        self, **kwargs: Unpack[GetMetadataTransferJobRequestRequestTypeDef]
    ) -> GetMetadataTransferJobResponseTypeDef:
        """
        Gets a nmetadata transfer job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/get_metadata_transfer_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#get_metadata_transfer_job)
        """

    async def get_pricing_plan(self) -> GetPricingPlanResponseTypeDef:
        """
        Gets the pricing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/get_pricing_plan.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#get_pricing_plan)
        """

    async def get_property_value(
        self, **kwargs: Unpack[GetPropertyValueRequestRequestTypeDef]
    ) -> GetPropertyValueResponseTypeDef:
        """
        Gets the property values for a component, component type, entity, or workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/get_property_value.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#get_property_value)
        """

    async def get_property_value_history(
        self, **kwargs: Unpack[GetPropertyValueHistoryRequestRequestTypeDef]
    ) -> GetPropertyValueHistoryResponseTypeDef:
        """
        Retrieves information about the history of a time series property value for a
        component, component type, entity, or workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/get_property_value_history.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#get_property_value_history)
        """

    async def get_scene(
        self, **kwargs: Unpack[GetSceneRequestRequestTypeDef]
    ) -> GetSceneResponseTypeDef:
        """
        Retrieves information about a scene.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/get_scene.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#get_scene)
        """

    async def get_sync_job(
        self, **kwargs: Unpack[GetSyncJobRequestRequestTypeDef]
    ) -> GetSyncJobResponseTypeDef:
        """
        Gets the SyncJob.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/get_sync_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#get_sync_job)
        """

    async def get_workspace(
        self, **kwargs: Unpack[GetWorkspaceRequestRequestTypeDef]
    ) -> GetWorkspaceResponseTypeDef:
        """
        Retrieves information about a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/get_workspace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#get_workspace)
        """

    async def list_component_types(
        self, **kwargs: Unpack[ListComponentTypesRequestRequestTypeDef]
    ) -> ListComponentTypesResponseTypeDef:
        """
        Lists all component types in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/list_component_types.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#list_component_types)
        """

    async def list_components(
        self, **kwargs: Unpack[ListComponentsRequestRequestTypeDef]
    ) -> ListComponentsResponseTypeDef:
        """
        This API lists the components of an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/list_components.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#list_components)
        """

    async def list_entities(
        self, **kwargs: Unpack[ListEntitiesRequestRequestTypeDef]
    ) -> ListEntitiesResponseTypeDef:
        """
        Lists all entities in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/list_entities.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#list_entities)
        """

    async def list_metadata_transfer_jobs(
        self, **kwargs: Unpack[ListMetadataTransferJobsRequestRequestTypeDef]
    ) -> ListMetadataTransferJobsResponseTypeDef:
        """
        Lists the metadata transfer jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/list_metadata_transfer_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#list_metadata_transfer_jobs)
        """

    async def list_properties(
        self, **kwargs: Unpack[ListPropertiesRequestRequestTypeDef]
    ) -> ListPropertiesResponseTypeDef:
        """
        This API lists the properties of a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/list_properties.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#list_properties)
        """

    async def list_scenes(
        self, **kwargs: Unpack[ListScenesRequestRequestTypeDef]
    ) -> ListScenesResponseTypeDef:
        """
        Lists all scenes in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/list_scenes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#list_scenes)
        """

    async def list_sync_jobs(
        self, **kwargs: Unpack[ListSyncJobsRequestRequestTypeDef]
    ) -> ListSyncJobsResponseTypeDef:
        """
        List all SyncJobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/list_sync_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#list_sync_jobs)
        """

    async def list_sync_resources(
        self, **kwargs: Unpack[ListSyncResourcesRequestRequestTypeDef]
    ) -> ListSyncResourcesResponseTypeDef:
        """
        Lists the sync resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/list_sync_resources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#list_sync_resources)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags associated with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#list_tags_for_resource)
        """

    async def list_workspaces(
        self, **kwargs: Unpack[ListWorkspacesRequestRequestTypeDef]
    ) -> ListWorkspacesResponseTypeDef:
        """
        Retrieves information about workspaces in the current account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/list_workspaces.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#list_workspaces)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#untag_resource)
        """

    async def update_component_type(
        self, **kwargs: Unpack[UpdateComponentTypeRequestRequestTypeDef]
    ) -> UpdateComponentTypeResponseTypeDef:
        """
        Updates information in a component type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/update_component_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#update_component_type)
        """

    async def update_entity(
        self, **kwargs: Unpack[UpdateEntityRequestRequestTypeDef]
    ) -> UpdateEntityResponseTypeDef:
        """
        Updates an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/update_entity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#update_entity)
        """

    async def update_pricing_plan(
        self, **kwargs: Unpack[UpdatePricingPlanRequestRequestTypeDef]
    ) -> UpdatePricingPlanResponseTypeDef:
        """
        Update the pricing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/update_pricing_plan.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#update_pricing_plan)
        """

    async def update_scene(
        self, **kwargs: Unpack[UpdateSceneRequestRequestTypeDef]
    ) -> UpdateSceneResponseTypeDef:
        """
        Updates a scene.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/update_scene.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#update_scene)
        """

    async def update_workspace(
        self, **kwargs: Unpack[UpdateWorkspaceRequestRequestTypeDef]
    ) -> UpdateWorkspaceResponseTypeDef:
        """
        Updates a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker/client/update_workspace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#update_workspace)
        """

    async def __aenter__(self) -> "IoTTwinMakerClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/)
        """
