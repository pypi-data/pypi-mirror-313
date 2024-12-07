"""
Type annotations for imagebuilder service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_imagebuilder.client import ImagebuilderClient

    session = get_session()
    async with session.create_client("imagebuilder") as client:
        client: ImagebuilderClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    CancelImageCreationRequestRequestTypeDef,
    CancelImageCreationResponseTypeDef,
    CancelLifecycleExecutionRequestRequestTypeDef,
    CancelLifecycleExecutionResponseTypeDef,
    CreateComponentRequestRequestTypeDef,
    CreateComponentResponseTypeDef,
    CreateContainerRecipeRequestRequestTypeDef,
    CreateContainerRecipeResponseTypeDef,
    CreateDistributionConfigurationRequestRequestTypeDef,
    CreateDistributionConfigurationResponseTypeDef,
    CreateImagePipelineRequestRequestTypeDef,
    CreateImagePipelineResponseTypeDef,
    CreateImageRecipeRequestRequestTypeDef,
    CreateImageRecipeResponseTypeDef,
    CreateImageRequestRequestTypeDef,
    CreateImageResponseTypeDef,
    CreateInfrastructureConfigurationRequestRequestTypeDef,
    CreateInfrastructureConfigurationResponseTypeDef,
    CreateLifecyclePolicyRequestRequestTypeDef,
    CreateLifecyclePolicyResponseTypeDef,
    CreateWorkflowRequestRequestTypeDef,
    CreateWorkflowResponseTypeDef,
    DeleteComponentRequestRequestTypeDef,
    DeleteComponentResponseTypeDef,
    DeleteContainerRecipeRequestRequestTypeDef,
    DeleteContainerRecipeResponseTypeDef,
    DeleteDistributionConfigurationRequestRequestTypeDef,
    DeleteDistributionConfigurationResponseTypeDef,
    DeleteImagePipelineRequestRequestTypeDef,
    DeleteImagePipelineResponseTypeDef,
    DeleteImageRecipeRequestRequestTypeDef,
    DeleteImageRecipeResponseTypeDef,
    DeleteImageRequestRequestTypeDef,
    DeleteImageResponseTypeDef,
    DeleteInfrastructureConfigurationRequestRequestTypeDef,
    DeleteInfrastructureConfigurationResponseTypeDef,
    DeleteLifecyclePolicyRequestRequestTypeDef,
    DeleteLifecyclePolicyResponseTypeDef,
    DeleteWorkflowRequestRequestTypeDef,
    DeleteWorkflowResponseTypeDef,
    GetComponentPolicyRequestRequestTypeDef,
    GetComponentPolicyResponseTypeDef,
    GetComponentRequestRequestTypeDef,
    GetComponentResponseTypeDef,
    GetContainerRecipePolicyRequestRequestTypeDef,
    GetContainerRecipePolicyResponseTypeDef,
    GetContainerRecipeRequestRequestTypeDef,
    GetContainerRecipeResponseTypeDef,
    GetDistributionConfigurationRequestRequestTypeDef,
    GetDistributionConfigurationResponseTypeDef,
    GetImagePipelineRequestRequestTypeDef,
    GetImagePipelineResponseTypeDef,
    GetImagePolicyRequestRequestTypeDef,
    GetImagePolicyResponseTypeDef,
    GetImageRecipePolicyRequestRequestTypeDef,
    GetImageRecipePolicyResponseTypeDef,
    GetImageRecipeRequestRequestTypeDef,
    GetImageRecipeResponseTypeDef,
    GetImageRequestRequestTypeDef,
    GetImageResponseTypeDef,
    GetInfrastructureConfigurationRequestRequestTypeDef,
    GetInfrastructureConfigurationResponseTypeDef,
    GetLifecycleExecutionRequestRequestTypeDef,
    GetLifecycleExecutionResponseTypeDef,
    GetLifecyclePolicyRequestRequestTypeDef,
    GetLifecyclePolicyResponseTypeDef,
    GetWorkflowExecutionRequestRequestTypeDef,
    GetWorkflowExecutionResponseTypeDef,
    GetWorkflowRequestRequestTypeDef,
    GetWorkflowResponseTypeDef,
    GetWorkflowStepExecutionRequestRequestTypeDef,
    GetWorkflowStepExecutionResponseTypeDef,
    ImportComponentRequestRequestTypeDef,
    ImportComponentResponseTypeDef,
    ImportVmImageRequestRequestTypeDef,
    ImportVmImageResponseTypeDef,
    ListComponentBuildVersionsRequestRequestTypeDef,
    ListComponentBuildVersionsResponseTypeDef,
    ListComponentsRequestRequestTypeDef,
    ListComponentsResponseTypeDef,
    ListContainerRecipesRequestRequestTypeDef,
    ListContainerRecipesResponseTypeDef,
    ListDistributionConfigurationsRequestRequestTypeDef,
    ListDistributionConfigurationsResponseTypeDef,
    ListImageBuildVersionsRequestRequestTypeDef,
    ListImageBuildVersionsResponseTypeDef,
    ListImagePackagesRequestRequestTypeDef,
    ListImagePackagesResponseTypeDef,
    ListImagePipelineImagesRequestRequestTypeDef,
    ListImagePipelineImagesResponseTypeDef,
    ListImagePipelinesRequestRequestTypeDef,
    ListImagePipelinesResponseTypeDef,
    ListImageRecipesRequestRequestTypeDef,
    ListImageRecipesResponseTypeDef,
    ListImageScanFindingAggregationsRequestRequestTypeDef,
    ListImageScanFindingAggregationsResponseTypeDef,
    ListImageScanFindingsRequestRequestTypeDef,
    ListImageScanFindingsResponseTypeDef,
    ListImagesRequestRequestTypeDef,
    ListImagesResponseTypeDef,
    ListInfrastructureConfigurationsRequestRequestTypeDef,
    ListInfrastructureConfigurationsResponseTypeDef,
    ListLifecycleExecutionResourcesRequestRequestTypeDef,
    ListLifecycleExecutionResourcesResponseTypeDef,
    ListLifecycleExecutionsRequestRequestTypeDef,
    ListLifecycleExecutionsResponseTypeDef,
    ListLifecyclePoliciesRequestRequestTypeDef,
    ListLifecyclePoliciesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWaitingWorkflowStepsRequestRequestTypeDef,
    ListWaitingWorkflowStepsResponseTypeDef,
    ListWorkflowBuildVersionsRequestRequestTypeDef,
    ListWorkflowBuildVersionsResponseTypeDef,
    ListWorkflowExecutionsRequestRequestTypeDef,
    ListWorkflowExecutionsResponseTypeDef,
    ListWorkflowsRequestRequestTypeDef,
    ListWorkflowsResponseTypeDef,
    ListWorkflowStepExecutionsRequestRequestTypeDef,
    ListWorkflowStepExecutionsResponseTypeDef,
    PutComponentPolicyRequestRequestTypeDef,
    PutComponentPolicyResponseTypeDef,
    PutContainerRecipePolicyRequestRequestTypeDef,
    PutContainerRecipePolicyResponseTypeDef,
    PutImagePolicyRequestRequestTypeDef,
    PutImagePolicyResponseTypeDef,
    PutImageRecipePolicyRequestRequestTypeDef,
    PutImageRecipePolicyResponseTypeDef,
    SendWorkflowStepActionRequestRequestTypeDef,
    SendWorkflowStepActionResponseTypeDef,
    StartImagePipelineExecutionRequestRequestTypeDef,
    StartImagePipelineExecutionResponseTypeDef,
    StartResourceStateUpdateRequestRequestTypeDef,
    StartResourceStateUpdateResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDistributionConfigurationRequestRequestTypeDef,
    UpdateDistributionConfigurationResponseTypeDef,
    UpdateImagePipelineRequestRequestTypeDef,
    UpdateImagePipelineResponseTypeDef,
    UpdateInfrastructureConfigurationRequestRequestTypeDef,
    UpdateInfrastructureConfigurationResponseTypeDef,
    UpdateLifecyclePolicyRequestRequestTypeDef,
    UpdateLifecyclePolicyResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ImagebuilderClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    CallRateLimitExceededException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClientException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    InvalidPaginationTokenException: Type[BotocoreClientError]
    InvalidParameterCombinationException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidVersionNumberException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceDependencyException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]

class ImagebuilderClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ImagebuilderClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#close)
        """

    async def cancel_image_creation(
        self, **kwargs: Unpack[CancelImageCreationRequestRequestTypeDef]
    ) -> CancelImageCreationResponseTypeDef:
        """
        CancelImageCreation cancels the creation of Image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/cancel_image_creation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#cancel_image_creation)
        """

    async def cancel_lifecycle_execution(
        self, **kwargs: Unpack[CancelLifecycleExecutionRequestRequestTypeDef]
    ) -> CancelLifecycleExecutionResponseTypeDef:
        """
        Cancel a specific image lifecycle policy runtime instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/cancel_lifecycle_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#cancel_lifecycle_execution)
        """

    async def create_component(
        self, **kwargs: Unpack[CreateComponentRequestRequestTypeDef]
    ) -> CreateComponentResponseTypeDef:
        """
        Creates a new component that can be used to build, validate, test, and assess
        your image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_component)
        """

    async def create_container_recipe(
        self, **kwargs: Unpack[CreateContainerRecipeRequestRequestTypeDef]
    ) -> CreateContainerRecipeResponseTypeDef:
        """
        Creates a new container recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_container_recipe.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_container_recipe)
        """

    async def create_distribution_configuration(
        self, **kwargs: Unpack[CreateDistributionConfigurationRequestRequestTypeDef]
    ) -> CreateDistributionConfigurationResponseTypeDef:
        """
        Creates a new distribution configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_distribution_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_distribution_configuration)
        """

    async def create_image(
        self, **kwargs: Unpack[CreateImageRequestRequestTypeDef]
    ) -> CreateImageResponseTypeDef:
        """
        Creates a new image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_image)
        """

    async def create_image_pipeline(
        self, **kwargs: Unpack[CreateImagePipelineRequestRequestTypeDef]
    ) -> CreateImagePipelineResponseTypeDef:
        """
        Creates a new image pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_image_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_image_pipeline)
        """

    async def create_image_recipe(
        self, **kwargs: Unpack[CreateImageRecipeRequestRequestTypeDef]
    ) -> CreateImageRecipeResponseTypeDef:
        """
        Creates a new image recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_image_recipe.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_image_recipe)
        """

    async def create_infrastructure_configuration(
        self, **kwargs: Unpack[CreateInfrastructureConfigurationRequestRequestTypeDef]
    ) -> CreateInfrastructureConfigurationResponseTypeDef:
        """
        Creates a new infrastructure configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_infrastructure_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_infrastructure_configuration)
        """

    async def create_lifecycle_policy(
        self, **kwargs: Unpack[CreateLifecyclePolicyRequestRequestTypeDef]
    ) -> CreateLifecyclePolicyResponseTypeDef:
        """
        Create a lifecycle policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_lifecycle_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_lifecycle_policy)
        """

    async def create_workflow(
        self, **kwargs: Unpack[CreateWorkflowRequestRequestTypeDef]
    ) -> CreateWorkflowResponseTypeDef:
        """
        Create a new workflow or a new version of an existing workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_workflow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_workflow)
        """

    async def delete_component(
        self, **kwargs: Unpack[DeleteComponentRequestRequestTypeDef]
    ) -> DeleteComponentResponseTypeDef:
        """
        Deletes a component build version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_component)
        """

    async def delete_container_recipe(
        self, **kwargs: Unpack[DeleteContainerRecipeRequestRequestTypeDef]
    ) -> DeleteContainerRecipeResponseTypeDef:
        """
        Deletes a container recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_container_recipe.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_container_recipe)
        """

    async def delete_distribution_configuration(
        self, **kwargs: Unpack[DeleteDistributionConfigurationRequestRequestTypeDef]
    ) -> DeleteDistributionConfigurationResponseTypeDef:
        """
        Deletes a distribution configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_distribution_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_distribution_configuration)
        """

    async def delete_image(
        self, **kwargs: Unpack[DeleteImageRequestRequestTypeDef]
    ) -> DeleteImageResponseTypeDef:
        """
        Deletes an Image Builder image resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_image)
        """

    async def delete_image_pipeline(
        self, **kwargs: Unpack[DeleteImagePipelineRequestRequestTypeDef]
    ) -> DeleteImagePipelineResponseTypeDef:
        """
        Deletes an image pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_image_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_image_pipeline)
        """

    async def delete_image_recipe(
        self, **kwargs: Unpack[DeleteImageRecipeRequestRequestTypeDef]
    ) -> DeleteImageRecipeResponseTypeDef:
        """
        Deletes an image recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_image_recipe.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_image_recipe)
        """

    async def delete_infrastructure_configuration(
        self, **kwargs: Unpack[DeleteInfrastructureConfigurationRequestRequestTypeDef]
    ) -> DeleteInfrastructureConfigurationResponseTypeDef:
        """
        Deletes an infrastructure configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_infrastructure_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_infrastructure_configuration)
        """

    async def delete_lifecycle_policy(
        self, **kwargs: Unpack[DeleteLifecyclePolicyRequestRequestTypeDef]
    ) -> DeleteLifecyclePolicyResponseTypeDef:
        """
        Delete the specified lifecycle policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_lifecycle_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_lifecycle_policy)
        """

    async def delete_workflow(
        self, **kwargs: Unpack[DeleteWorkflowRequestRequestTypeDef]
    ) -> DeleteWorkflowResponseTypeDef:
        """
        Deletes a specific workflow resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_workflow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_workflow)
        """

    async def get_component(
        self, **kwargs: Unpack[GetComponentRequestRequestTypeDef]
    ) -> GetComponentResponseTypeDef:
        """
        Gets a component object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_component)
        """

    async def get_component_policy(
        self, **kwargs: Unpack[GetComponentPolicyRequestRequestTypeDef]
    ) -> GetComponentPolicyResponseTypeDef:
        """
        Gets a component policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_component_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_component_policy)
        """

    async def get_container_recipe(
        self, **kwargs: Unpack[GetContainerRecipeRequestRequestTypeDef]
    ) -> GetContainerRecipeResponseTypeDef:
        """
        Retrieves a container recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_container_recipe.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_container_recipe)
        """

    async def get_container_recipe_policy(
        self, **kwargs: Unpack[GetContainerRecipePolicyRequestRequestTypeDef]
    ) -> GetContainerRecipePolicyResponseTypeDef:
        """
        Retrieves the policy for a container recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_container_recipe_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_container_recipe_policy)
        """

    async def get_distribution_configuration(
        self, **kwargs: Unpack[GetDistributionConfigurationRequestRequestTypeDef]
    ) -> GetDistributionConfigurationResponseTypeDef:
        """
        Gets a distribution configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_distribution_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_distribution_configuration)
        """

    async def get_image(
        self, **kwargs: Unpack[GetImageRequestRequestTypeDef]
    ) -> GetImageResponseTypeDef:
        """
        Gets an image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_image)
        """

    async def get_image_pipeline(
        self, **kwargs: Unpack[GetImagePipelineRequestRequestTypeDef]
    ) -> GetImagePipelineResponseTypeDef:
        """
        Gets an image pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_image_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_image_pipeline)
        """

    async def get_image_policy(
        self, **kwargs: Unpack[GetImagePolicyRequestRequestTypeDef]
    ) -> GetImagePolicyResponseTypeDef:
        """
        Gets an image policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_image_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_image_policy)
        """

    async def get_image_recipe(
        self, **kwargs: Unpack[GetImageRecipeRequestRequestTypeDef]
    ) -> GetImageRecipeResponseTypeDef:
        """
        Gets an image recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_image_recipe.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_image_recipe)
        """

    async def get_image_recipe_policy(
        self, **kwargs: Unpack[GetImageRecipePolicyRequestRequestTypeDef]
    ) -> GetImageRecipePolicyResponseTypeDef:
        """
        Gets an image recipe policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_image_recipe_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_image_recipe_policy)
        """

    async def get_infrastructure_configuration(
        self, **kwargs: Unpack[GetInfrastructureConfigurationRequestRequestTypeDef]
    ) -> GetInfrastructureConfigurationResponseTypeDef:
        """
        Gets an infrastructure configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_infrastructure_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_infrastructure_configuration)
        """

    async def get_lifecycle_execution(
        self, **kwargs: Unpack[GetLifecycleExecutionRequestRequestTypeDef]
    ) -> GetLifecycleExecutionResponseTypeDef:
        """
        Get the runtime information that was logged for a specific runtime instance of
        the lifecycle policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_lifecycle_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_lifecycle_execution)
        """

    async def get_lifecycle_policy(
        self, **kwargs: Unpack[GetLifecyclePolicyRequestRequestTypeDef]
    ) -> GetLifecyclePolicyResponseTypeDef:
        """
        Get details for the specified image lifecycle policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_lifecycle_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_lifecycle_policy)
        """

    async def get_workflow(
        self, **kwargs: Unpack[GetWorkflowRequestRequestTypeDef]
    ) -> GetWorkflowResponseTypeDef:
        """
        Get a workflow resource object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_workflow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_workflow)
        """

    async def get_workflow_execution(
        self, **kwargs: Unpack[GetWorkflowExecutionRequestRequestTypeDef]
    ) -> GetWorkflowExecutionResponseTypeDef:
        """
        Get the runtime information that was logged for a specific runtime instance of
        the workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_workflow_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_workflow_execution)
        """

    async def get_workflow_step_execution(
        self, **kwargs: Unpack[GetWorkflowStepExecutionRequestRequestTypeDef]
    ) -> GetWorkflowStepExecutionResponseTypeDef:
        """
        Get the runtime information that was logged for a specific runtime instance of
        the workflow step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_workflow_step_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_workflow_step_execution)
        """

    async def import_component(
        self, **kwargs: Unpack[ImportComponentRequestRequestTypeDef]
    ) -> ImportComponentResponseTypeDef:
        """
        Imports a component and transforms its data into a component document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/import_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#import_component)
        """

    async def import_vm_image(
        self, **kwargs: Unpack[ImportVmImageRequestRequestTypeDef]
    ) -> ImportVmImageResponseTypeDef:
        """
        When you export your virtual machine (VM) from its virtualization environment,
        that process creates a set of one or more disk container files that act as
        snapshots of your VM's environment, settings, and data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/import_vm_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#import_vm_image)
        """

    async def list_component_build_versions(
        self, **kwargs: Unpack[ListComponentBuildVersionsRequestRequestTypeDef]
    ) -> ListComponentBuildVersionsResponseTypeDef:
        """
        Returns the list of component build versions for the specified semantic version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_component_build_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_component_build_versions)
        """

    async def list_components(
        self, **kwargs: Unpack[ListComponentsRequestRequestTypeDef]
    ) -> ListComponentsResponseTypeDef:
        """
        Returns the list of components that can be filtered by name, or by using the
        listed <code>filters</code> to streamline results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_components.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_components)
        """

    async def list_container_recipes(
        self, **kwargs: Unpack[ListContainerRecipesRequestRequestTypeDef]
    ) -> ListContainerRecipesResponseTypeDef:
        """
        Returns a list of container recipes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_container_recipes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_container_recipes)
        """

    async def list_distribution_configurations(
        self, **kwargs: Unpack[ListDistributionConfigurationsRequestRequestTypeDef]
    ) -> ListDistributionConfigurationsResponseTypeDef:
        """
        Returns a list of distribution configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_distribution_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_distribution_configurations)
        """

    async def list_image_build_versions(
        self, **kwargs: Unpack[ListImageBuildVersionsRequestRequestTypeDef]
    ) -> ListImageBuildVersionsResponseTypeDef:
        """
        Returns a list of image build versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_image_build_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_build_versions)
        """

    async def list_image_packages(
        self, **kwargs: Unpack[ListImagePackagesRequestRequestTypeDef]
    ) -> ListImagePackagesResponseTypeDef:
        """
        List the Packages that are associated with an Image Build Version, as
        determined by Amazon Web Services Systems Manager Inventory at build time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_image_packages.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_packages)
        """

    async def list_image_pipeline_images(
        self, **kwargs: Unpack[ListImagePipelineImagesRequestRequestTypeDef]
    ) -> ListImagePipelineImagesResponseTypeDef:
        """
        Returns a list of images created by the specified pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_image_pipeline_images.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_pipeline_images)
        """

    async def list_image_pipelines(
        self, **kwargs: Unpack[ListImagePipelinesRequestRequestTypeDef]
    ) -> ListImagePipelinesResponseTypeDef:
        """
        Returns a list of image pipelines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_image_pipelines.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_pipelines)
        """

    async def list_image_recipes(
        self, **kwargs: Unpack[ListImageRecipesRequestRequestTypeDef]
    ) -> ListImageRecipesResponseTypeDef:
        """
        Returns a list of image recipes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_image_recipes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_recipes)
        """

    async def list_image_scan_finding_aggregations(
        self, **kwargs: Unpack[ListImageScanFindingAggregationsRequestRequestTypeDef]
    ) -> ListImageScanFindingAggregationsResponseTypeDef:
        """
        Returns a list of image scan aggregations for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_image_scan_finding_aggregations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_scan_finding_aggregations)
        """

    async def list_image_scan_findings(
        self, **kwargs: Unpack[ListImageScanFindingsRequestRequestTypeDef]
    ) -> ListImageScanFindingsResponseTypeDef:
        """
        Returns a list of image scan findings for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_image_scan_findings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_scan_findings)
        """

    async def list_images(
        self, **kwargs: Unpack[ListImagesRequestRequestTypeDef]
    ) -> ListImagesResponseTypeDef:
        """
        Returns the list of images that you have access to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_images.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_images)
        """

    async def list_infrastructure_configurations(
        self, **kwargs: Unpack[ListInfrastructureConfigurationsRequestRequestTypeDef]
    ) -> ListInfrastructureConfigurationsResponseTypeDef:
        """
        Returns a list of infrastructure configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_infrastructure_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_infrastructure_configurations)
        """

    async def list_lifecycle_execution_resources(
        self, **kwargs: Unpack[ListLifecycleExecutionResourcesRequestRequestTypeDef]
    ) -> ListLifecycleExecutionResourcesResponseTypeDef:
        """
        List resources that the runtime instance of the image lifecycle identified for
        lifecycle actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_lifecycle_execution_resources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_lifecycle_execution_resources)
        """

    async def list_lifecycle_executions(
        self, **kwargs: Unpack[ListLifecycleExecutionsRequestRequestTypeDef]
    ) -> ListLifecycleExecutionsResponseTypeDef:
        """
        Get the lifecycle runtime history for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_lifecycle_executions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_lifecycle_executions)
        """

    async def list_lifecycle_policies(
        self, **kwargs: Unpack[ListLifecyclePoliciesRequestRequestTypeDef]
    ) -> ListLifecyclePoliciesResponseTypeDef:
        """
        Get a list of lifecycle policies in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_lifecycle_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_lifecycle_policies)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns the list of tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_tags_for_resource)
        """

    async def list_waiting_workflow_steps(
        self, **kwargs: Unpack[ListWaitingWorkflowStepsRequestRequestTypeDef]
    ) -> ListWaitingWorkflowStepsResponseTypeDef:
        """
        Get a list of workflow steps that are waiting for action for workflows in your
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_waiting_workflow_steps.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_waiting_workflow_steps)
        """

    async def list_workflow_build_versions(
        self, **kwargs: Unpack[ListWorkflowBuildVersionsRequestRequestTypeDef]
    ) -> ListWorkflowBuildVersionsResponseTypeDef:
        """
        Returns a list of build versions for a specific workflow resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_workflow_build_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_workflow_build_versions)
        """

    async def list_workflow_executions(
        self, **kwargs: Unpack[ListWorkflowExecutionsRequestRequestTypeDef]
    ) -> ListWorkflowExecutionsResponseTypeDef:
        """
        Returns a list of workflow runtime instance metadata objects for a specific
        image build version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_workflow_executions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_workflow_executions)
        """

    async def list_workflow_step_executions(
        self, **kwargs: Unpack[ListWorkflowStepExecutionsRequestRequestTypeDef]
    ) -> ListWorkflowStepExecutionsResponseTypeDef:
        """
        Returns runtime data for each step in a runtime instance of the workflow that
        you specify in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_workflow_step_executions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_workflow_step_executions)
        """

    async def list_workflows(
        self, **kwargs: Unpack[ListWorkflowsRequestRequestTypeDef]
    ) -> ListWorkflowsResponseTypeDef:
        """
        Lists workflow build versions based on filtering parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_workflows.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_workflows)
        """

    async def put_component_policy(
        self, **kwargs: Unpack[PutComponentPolicyRequestRequestTypeDef]
    ) -> PutComponentPolicyResponseTypeDef:
        """
        Applies a policy to a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/put_component_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#put_component_policy)
        """

    async def put_container_recipe_policy(
        self, **kwargs: Unpack[PutContainerRecipePolicyRequestRequestTypeDef]
    ) -> PutContainerRecipePolicyResponseTypeDef:
        """
        Applies a policy to a container image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/put_container_recipe_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#put_container_recipe_policy)
        """

    async def put_image_policy(
        self, **kwargs: Unpack[PutImagePolicyRequestRequestTypeDef]
    ) -> PutImagePolicyResponseTypeDef:
        """
        Applies a policy to an image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/put_image_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#put_image_policy)
        """

    async def put_image_recipe_policy(
        self, **kwargs: Unpack[PutImageRecipePolicyRequestRequestTypeDef]
    ) -> PutImageRecipePolicyResponseTypeDef:
        """
        Applies a policy to an image recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/put_image_recipe_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#put_image_recipe_policy)
        """

    async def send_workflow_step_action(
        self, **kwargs: Unpack[SendWorkflowStepActionRequestRequestTypeDef]
    ) -> SendWorkflowStepActionResponseTypeDef:
        """
        Pauses or resumes image creation when the associated workflow runs a
        <code>WaitForAction</code> step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/send_workflow_step_action.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#send_workflow_step_action)
        """

    async def start_image_pipeline_execution(
        self, **kwargs: Unpack[StartImagePipelineExecutionRequestRequestTypeDef]
    ) -> StartImagePipelineExecutionResponseTypeDef:
        """
        Manually triggers a pipeline to create an image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/start_image_pipeline_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#start_image_pipeline_execution)
        """

    async def start_resource_state_update(
        self, **kwargs: Unpack[StartResourceStateUpdateRequestRequestTypeDef]
    ) -> StartResourceStateUpdateResponseTypeDef:
        """
        Begin asynchronous resource state update for lifecycle changes to the specified
        image resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/start_resource_state_update.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#start_resource_state_update)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds a tag to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#untag_resource)
        """

    async def update_distribution_configuration(
        self, **kwargs: Unpack[UpdateDistributionConfigurationRequestRequestTypeDef]
    ) -> UpdateDistributionConfigurationResponseTypeDef:
        """
        Updates a new distribution configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/update_distribution_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#update_distribution_configuration)
        """

    async def update_image_pipeline(
        self, **kwargs: Unpack[UpdateImagePipelineRequestRequestTypeDef]
    ) -> UpdateImagePipelineResponseTypeDef:
        """
        Updates an image pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/update_image_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#update_image_pipeline)
        """

    async def update_infrastructure_configuration(
        self, **kwargs: Unpack[UpdateInfrastructureConfigurationRequestRequestTypeDef]
    ) -> UpdateInfrastructureConfigurationResponseTypeDef:
        """
        Updates a new infrastructure configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/update_infrastructure_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#update_infrastructure_configuration)
        """

    async def update_lifecycle_policy(
        self, **kwargs: Unpack[UpdateLifecyclePolicyRequestRequestTypeDef]
    ) -> UpdateLifecyclePolicyResponseTypeDef:
        """
        Update the specified lifecycle policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/update_lifecycle_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#update_lifecycle_policy)
        """

    async def __aenter__(self) -> "ImagebuilderClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/)
        """
