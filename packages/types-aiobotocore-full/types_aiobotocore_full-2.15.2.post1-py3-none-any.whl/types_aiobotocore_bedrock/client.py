"""
Type annotations for bedrock service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_bedrock.client import BedrockClient

    session = get_session()
    async with session.create_client("bedrock") as client:
        client: BedrockClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListCustomModelsPaginator,
    ListEvaluationJobsPaginator,
    ListGuardrailsPaginator,
    ListImportedModelsPaginator,
    ListInferenceProfilesPaginator,
    ListModelCopyJobsPaginator,
    ListModelCustomizationJobsPaginator,
    ListModelImportJobsPaginator,
    ListModelInvocationJobsPaginator,
    ListProvisionedModelThroughputsPaginator,
)
from .type_defs import (
    BatchDeleteEvaluationJobRequestRequestTypeDef,
    BatchDeleteEvaluationJobResponseTypeDef,
    CreateEvaluationJobRequestRequestTypeDef,
    CreateEvaluationJobResponseTypeDef,
    CreateGuardrailRequestRequestTypeDef,
    CreateGuardrailResponseTypeDef,
    CreateGuardrailVersionRequestRequestTypeDef,
    CreateGuardrailVersionResponseTypeDef,
    CreateModelCopyJobRequestRequestTypeDef,
    CreateModelCopyJobResponseTypeDef,
    CreateModelCustomizationJobRequestRequestTypeDef,
    CreateModelCustomizationJobResponseTypeDef,
    CreateModelImportJobRequestRequestTypeDef,
    CreateModelImportJobResponseTypeDef,
    CreateModelInvocationJobRequestRequestTypeDef,
    CreateModelInvocationJobResponseTypeDef,
    CreateProvisionedModelThroughputRequestRequestTypeDef,
    CreateProvisionedModelThroughputResponseTypeDef,
    DeleteCustomModelRequestRequestTypeDef,
    DeleteGuardrailRequestRequestTypeDef,
    DeleteImportedModelRequestRequestTypeDef,
    DeleteProvisionedModelThroughputRequestRequestTypeDef,
    GetCustomModelRequestRequestTypeDef,
    GetCustomModelResponseTypeDef,
    GetEvaluationJobRequestRequestTypeDef,
    GetEvaluationJobResponseTypeDef,
    GetFoundationModelRequestRequestTypeDef,
    GetFoundationModelResponseTypeDef,
    GetGuardrailRequestRequestTypeDef,
    GetGuardrailResponseTypeDef,
    GetImportedModelRequestRequestTypeDef,
    GetImportedModelResponseTypeDef,
    GetInferenceProfileRequestRequestTypeDef,
    GetInferenceProfileResponseTypeDef,
    GetModelCopyJobRequestRequestTypeDef,
    GetModelCopyJobResponseTypeDef,
    GetModelCustomizationJobRequestRequestTypeDef,
    GetModelCustomizationJobResponseTypeDef,
    GetModelImportJobRequestRequestTypeDef,
    GetModelImportJobResponseTypeDef,
    GetModelInvocationJobRequestRequestTypeDef,
    GetModelInvocationJobResponseTypeDef,
    GetModelInvocationLoggingConfigurationResponseTypeDef,
    GetProvisionedModelThroughputRequestRequestTypeDef,
    GetProvisionedModelThroughputResponseTypeDef,
    ListCustomModelsRequestRequestTypeDef,
    ListCustomModelsResponseTypeDef,
    ListEvaluationJobsRequestRequestTypeDef,
    ListEvaluationJobsResponseTypeDef,
    ListFoundationModelsRequestRequestTypeDef,
    ListFoundationModelsResponseTypeDef,
    ListGuardrailsRequestRequestTypeDef,
    ListGuardrailsResponseTypeDef,
    ListImportedModelsRequestRequestTypeDef,
    ListImportedModelsResponseTypeDef,
    ListInferenceProfilesRequestRequestTypeDef,
    ListInferenceProfilesResponseTypeDef,
    ListModelCopyJobsRequestRequestTypeDef,
    ListModelCopyJobsResponseTypeDef,
    ListModelCustomizationJobsRequestRequestTypeDef,
    ListModelCustomizationJobsResponseTypeDef,
    ListModelImportJobsRequestRequestTypeDef,
    ListModelImportJobsResponseTypeDef,
    ListModelInvocationJobsRequestRequestTypeDef,
    ListModelInvocationJobsResponseTypeDef,
    ListProvisionedModelThroughputsRequestRequestTypeDef,
    ListProvisionedModelThroughputsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutModelInvocationLoggingConfigurationRequestRequestTypeDef,
    StopEvaluationJobRequestRequestTypeDef,
    StopModelCustomizationJobRequestRequestTypeDef,
    StopModelInvocationJobRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateGuardrailRequestRequestTypeDef,
    UpdateGuardrailResponseTypeDef,
    UpdateProvisionedModelThroughputRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("BedrockClient",)


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
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class BedrockClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BedrockClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#close)
        """

    async def batch_delete_evaluation_job(
        self, **kwargs: Unpack[BatchDeleteEvaluationJobRequestRequestTypeDef]
    ) -> BatchDeleteEvaluationJobResponseTypeDef:
        """
        Creates a batch deletion job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/batch_delete_evaluation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#batch_delete_evaluation_job)
        """

    async def create_evaluation_job(
        self, **kwargs: Unpack[CreateEvaluationJobRequestRequestTypeDef]
    ) -> CreateEvaluationJobResponseTypeDef:
        """
        API operation for creating and managing Amazon Bedrock automatic model
        evaluation jobs and model evaluation jobs that use human workers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_evaluation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#create_evaluation_job)
        """

    async def create_guardrail(
        self, **kwargs: Unpack[CreateGuardrailRequestRequestTypeDef]
    ) -> CreateGuardrailResponseTypeDef:
        """
        Creates a guardrail to block topics and to implement safeguards for your
        generative AI applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_guardrail.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#create_guardrail)
        """

    async def create_guardrail_version(
        self, **kwargs: Unpack[CreateGuardrailVersionRequestRequestTypeDef]
    ) -> CreateGuardrailVersionResponseTypeDef:
        """
        Creates a version of the guardrail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_guardrail_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#create_guardrail_version)
        """

    async def create_model_copy_job(
        self, **kwargs: Unpack[CreateModelCopyJobRequestRequestTypeDef]
    ) -> CreateModelCopyJobResponseTypeDef:
        """
        Copies a model to another region so that it can be used there.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_model_copy_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#create_model_copy_job)
        """

    async def create_model_customization_job(
        self, **kwargs: Unpack[CreateModelCustomizationJobRequestRequestTypeDef]
    ) -> CreateModelCustomizationJobResponseTypeDef:
        """
        Creates a fine-tuning job to customize a base model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_model_customization_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#create_model_customization_job)
        """

    async def create_model_import_job(
        self, **kwargs: Unpack[CreateModelImportJobRequestRequestTypeDef]
    ) -> CreateModelImportJobResponseTypeDef:
        """
        Creates a model import job to import model that you have customized in other
        environments, such as Amazon SageMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_model_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#create_model_import_job)
        """

    async def create_model_invocation_job(
        self, **kwargs: Unpack[CreateModelInvocationJobRequestRequestTypeDef]
    ) -> CreateModelInvocationJobResponseTypeDef:
        """
        Creates a batch inference job to invoke a model on multiple prompts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_model_invocation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#create_model_invocation_job)
        """

    async def create_provisioned_model_throughput(
        self, **kwargs: Unpack[CreateProvisionedModelThroughputRequestRequestTypeDef]
    ) -> CreateProvisionedModelThroughputResponseTypeDef:
        """
        Creates dedicated throughput for a base or custom model with the model units
        and for the duration that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_provisioned_model_throughput.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#create_provisioned_model_throughput)
        """

    async def delete_custom_model(
        self, **kwargs: Unpack[DeleteCustomModelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a custom model that you created earlier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/delete_custom_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#delete_custom_model)
        """

    async def delete_guardrail(
        self, **kwargs: Unpack[DeleteGuardrailRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a guardrail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/delete_guardrail.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#delete_guardrail)
        """

    async def delete_imported_model(
        self, **kwargs: Unpack[DeleteImportedModelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a custom model that you imported earlier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/delete_imported_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#delete_imported_model)
        """

    async def delete_model_invocation_logging_configuration(self) -> Dict[str, Any]:
        """
        Delete the invocation logging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/delete_model_invocation_logging_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#delete_model_invocation_logging_configuration)
        """

    async def delete_provisioned_model_throughput(
        self, **kwargs: Unpack[DeleteProvisionedModelThroughputRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Provisioned Throughput.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/delete_provisioned_model_throughput.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#delete_provisioned_model_throughput)
        """

    async def get_custom_model(
        self, **kwargs: Unpack[GetCustomModelRequestRequestTypeDef]
    ) -> GetCustomModelResponseTypeDef:
        """
        Get the properties associated with a Amazon Bedrock custom model that you have
        created.For more information, see <a
        href="https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html">Custom
        models</a> in the <a
        href="https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service...

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_custom_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_custom_model)
        """

    async def get_evaluation_job(
        self, **kwargs: Unpack[GetEvaluationJobRequestRequestTypeDef]
    ) -> GetEvaluationJobResponseTypeDef:
        """
        Retrieves the properties associated with a model evaluation job, including the
        status of the job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_evaluation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_evaluation_job)
        """

    async def get_foundation_model(
        self, **kwargs: Unpack[GetFoundationModelRequestRequestTypeDef]
    ) -> GetFoundationModelResponseTypeDef:
        """
        Get details about a Amazon Bedrock foundation model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_foundation_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_foundation_model)
        """

    async def get_guardrail(
        self, **kwargs: Unpack[GetGuardrailRequestRequestTypeDef]
    ) -> GetGuardrailResponseTypeDef:
        """
        Gets details about a guardrail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_guardrail.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_guardrail)
        """

    async def get_imported_model(
        self, **kwargs: Unpack[GetImportedModelRequestRequestTypeDef]
    ) -> GetImportedModelResponseTypeDef:
        """
        Gets properties associated with a customized model you imported.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_imported_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_imported_model)
        """

    async def get_inference_profile(
        self, **kwargs: Unpack[GetInferenceProfileRequestRequestTypeDef]
    ) -> GetInferenceProfileResponseTypeDef:
        """
        Gets information about an inference profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_inference_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_inference_profile)
        """

    async def get_model_copy_job(
        self, **kwargs: Unpack[GetModelCopyJobRequestRequestTypeDef]
    ) -> GetModelCopyJobResponseTypeDef:
        """
        Retrieves information about a model copy job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_model_copy_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_model_copy_job)
        """

    async def get_model_customization_job(
        self, **kwargs: Unpack[GetModelCustomizationJobRequestRequestTypeDef]
    ) -> GetModelCustomizationJobResponseTypeDef:
        """
        Retrieves the properties associated with a model-customization job, including
        the status of the job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_model_customization_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_model_customization_job)
        """

    async def get_model_import_job(
        self, **kwargs: Unpack[GetModelImportJobRequestRequestTypeDef]
    ) -> GetModelImportJobResponseTypeDef:
        """
        Retrieves the properties associated with import model job, including the status
        of the job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_model_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_model_import_job)
        """

    async def get_model_invocation_job(
        self, **kwargs: Unpack[GetModelInvocationJobRequestRequestTypeDef]
    ) -> GetModelInvocationJobResponseTypeDef:
        """
        Gets details about a batch inference job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_model_invocation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_model_invocation_job)
        """

    async def get_model_invocation_logging_configuration(
        self,
    ) -> GetModelInvocationLoggingConfigurationResponseTypeDef:
        """
        Get the current configuration values for model invocation logging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_model_invocation_logging_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_model_invocation_logging_configuration)
        """

    async def get_provisioned_model_throughput(
        self, **kwargs: Unpack[GetProvisionedModelThroughputRequestRequestTypeDef]
    ) -> GetProvisionedModelThroughputResponseTypeDef:
        """
        Returns details for a Provisioned Throughput.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_provisioned_model_throughput.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_provisioned_model_throughput)
        """

    async def list_custom_models(
        self, **kwargs: Unpack[ListCustomModelsRequestRequestTypeDef]
    ) -> ListCustomModelsResponseTypeDef:
        """
        Returns a list of the custom models that you have created with the
        <code>CreateModelCustomizationJob</code> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_custom_models.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#list_custom_models)
        """

    async def list_evaluation_jobs(
        self, **kwargs: Unpack[ListEvaluationJobsRequestRequestTypeDef]
    ) -> ListEvaluationJobsResponseTypeDef:
        """
        Lists model evaluation jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_evaluation_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#list_evaluation_jobs)
        """

    async def list_foundation_models(
        self, **kwargs: Unpack[ListFoundationModelsRequestRequestTypeDef]
    ) -> ListFoundationModelsResponseTypeDef:
        """
        Lists Amazon Bedrock foundation models that you can use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_foundation_models.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#list_foundation_models)
        """

    async def list_guardrails(
        self, **kwargs: Unpack[ListGuardrailsRequestRequestTypeDef]
    ) -> ListGuardrailsResponseTypeDef:
        """
        Lists details about all the guardrails in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_guardrails.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#list_guardrails)
        """

    async def list_imported_models(
        self, **kwargs: Unpack[ListImportedModelsRequestRequestTypeDef]
    ) -> ListImportedModelsResponseTypeDef:
        """
        Returns a list of models you've imported.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_imported_models.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#list_imported_models)
        """

    async def list_inference_profiles(
        self, **kwargs: Unpack[ListInferenceProfilesRequestRequestTypeDef]
    ) -> ListInferenceProfilesResponseTypeDef:
        """
        Returns a list of inference profiles that you can use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_inference_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#list_inference_profiles)
        """

    async def list_model_copy_jobs(
        self, **kwargs: Unpack[ListModelCopyJobsRequestRequestTypeDef]
    ) -> ListModelCopyJobsResponseTypeDef:
        """
        Returns a list of model copy jobs that you have submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_model_copy_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#list_model_copy_jobs)
        """

    async def list_model_customization_jobs(
        self, **kwargs: Unpack[ListModelCustomizationJobsRequestRequestTypeDef]
    ) -> ListModelCustomizationJobsResponseTypeDef:
        """
        Returns a list of model customization jobs that you have submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_model_customization_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#list_model_customization_jobs)
        """

    async def list_model_import_jobs(
        self, **kwargs: Unpack[ListModelImportJobsRequestRequestTypeDef]
    ) -> ListModelImportJobsResponseTypeDef:
        """
        Returns a list of import jobs you've submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_model_import_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#list_model_import_jobs)
        """

    async def list_model_invocation_jobs(
        self, **kwargs: Unpack[ListModelInvocationJobsRequestRequestTypeDef]
    ) -> ListModelInvocationJobsResponseTypeDef:
        """
        Lists all batch inference jobs in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_model_invocation_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#list_model_invocation_jobs)
        """

    async def list_provisioned_model_throughputs(
        self, **kwargs: Unpack[ListProvisionedModelThroughputsRequestRequestTypeDef]
    ) -> ListProvisionedModelThroughputsResponseTypeDef:
        """
        Lists the Provisioned Throughputs in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_provisioned_model_throughputs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#list_provisioned_model_throughputs)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List the tags associated with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#list_tags_for_resource)
        """

    async def put_model_invocation_logging_configuration(
        self, **kwargs: Unpack[PutModelInvocationLoggingConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Set the configuration values for model invocation logging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/put_model_invocation_logging_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#put_model_invocation_logging_configuration)
        """

    async def stop_evaluation_job(
        self, **kwargs: Unpack[StopEvaluationJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops an in progress model evaluation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/stop_evaluation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#stop_evaluation_job)
        """

    async def stop_model_customization_job(
        self, **kwargs: Unpack[StopModelCustomizationJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops an active model customization job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/stop_model_customization_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#stop_model_customization_job)
        """

    async def stop_model_invocation_job(
        self, **kwargs: Unpack[StopModelInvocationJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops a batch inference job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/stop_model_invocation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#stop_model_invocation_job)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associate tags with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Remove one or more tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#untag_resource)
        """

    async def update_guardrail(
        self, **kwargs: Unpack[UpdateGuardrailRequestRequestTypeDef]
    ) -> UpdateGuardrailResponseTypeDef:
        """
        Updates a guardrail with the values you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/update_guardrail.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#update_guardrail)
        """

    async def update_provisioned_model_throughput(
        self, **kwargs: Unpack[UpdateProvisionedModelThroughputRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the name or associated model for a Provisioned Throughput.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/update_provisioned_model_throughput.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#update_provisioned_model_throughput)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_models"]
    ) -> ListCustomModelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_evaluation_jobs"]
    ) -> ListEvaluationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_guardrails"]) -> ListGuardrailsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_imported_models"]
    ) -> ListImportedModelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_inference_profiles"]
    ) -> ListInferenceProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_copy_jobs"]
    ) -> ListModelCopyJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_customization_jobs"]
    ) -> ListModelCustomizationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_import_jobs"]
    ) -> ListModelImportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_invocation_jobs"]
    ) -> ListModelInvocationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_provisioned_model_throughputs"]
    ) -> ListProvisionedModelThroughputsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/#get_paginator)
        """

    async def __aenter__(self) -> "BedrockClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/client/)
        """
