"""
Type annotations for bedrock service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bedrock.client import BedrockClient
    from types_aiobotocore_bedrock.paginator import (
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

    session = get_session()
    with session.create_client("bedrock") as client:
        client: BedrockClient

        list_custom_models_paginator: ListCustomModelsPaginator = client.get_paginator("list_custom_models")
        list_evaluation_jobs_paginator: ListEvaluationJobsPaginator = client.get_paginator("list_evaluation_jobs")
        list_guardrails_paginator: ListGuardrailsPaginator = client.get_paginator("list_guardrails")
        list_imported_models_paginator: ListImportedModelsPaginator = client.get_paginator("list_imported_models")
        list_inference_profiles_paginator: ListInferenceProfilesPaginator = client.get_paginator("list_inference_profiles")
        list_model_copy_jobs_paginator: ListModelCopyJobsPaginator = client.get_paginator("list_model_copy_jobs")
        list_model_customization_jobs_paginator: ListModelCustomizationJobsPaginator = client.get_paginator("list_model_customization_jobs")
        list_model_import_jobs_paginator: ListModelImportJobsPaginator = client.get_paginator("list_model_import_jobs")
        list_model_invocation_jobs_paginator: ListModelInvocationJobsPaginator = client.get_paginator("list_model_invocation_jobs")
        list_provisioned_model_throughputs_paginator: ListProvisionedModelThroughputsPaginator = client.get_paginator("list_provisioned_model_throughputs")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListCustomModelsRequestListCustomModelsPaginateTypeDef,
    ListCustomModelsResponseTypeDef,
    ListEvaluationJobsRequestListEvaluationJobsPaginateTypeDef,
    ListEvaluationJobsResponseTypeDef,
    ListGuardrailsRequestListGuardrailsPaginateTypeDef,
    ListGuardrailsResponseTypeDef,
    ListImportedModelsRequestListImportedModelsPaginateTypeDef,
    ListImportedModelsResponseTypeDef,
    ListInferenceProfilesRequestListInferenceProfilesPaginateTypeDef,
    ListInferenceProfilesResponseTypeDef,
    ListModelCopyJobsRequestListModelCopyJobsPaginateTypeDef,
    ListModelCopyJobsResponseTypeDef,
    ListModelCustomizationJobsRequestListModelCustomizationJobsPaginateTypeDef,
    ListModelCustomizationJobsResponseTypeDef,
    ListModelImportJobsRequestListModelImportJobsPaginateTypeDef,
    ListModelImportJobsResponseTypeDef,
    ListModelInvocationJobsRequestListModelInvocationJobsPaginateTypeDef,
    ListModelInvocationJobsResponseTypeDef,
    ListProvisionedModelThroughputsRequestListProvisionedModelThroughputsPaginateTypeDef,
    ListProvisionedModelThroughputsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListCustomModelsPaginator",
    "ListEvaluationJobsPaginator",
    "ListGuardrailsPaginator",
    "ListImportedModelsPaginator",
    "ListInferenceProfilesPaginator",
    "ListModelCopyJobsPaginator",
    "ListModelCustomizationJobsPaginator",
    "ListModelImportJobsPaginator",
    "ListModelInvocationJobsPaginator",
    "ListProvisionedModelThroughputsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListCustomModelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListCustomModels.html#Bedrock.Paginator.ListCustomModels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listcustommodelspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCustomModelsRequestListCustomModelsPaginateTypeDef]
    ) -> AsyncIterator[ListCustomModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListCustomModels.html#Bedrock.Paginator.ListCustomModels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listcustommodelspaginator)
        """


class ListEvaluationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListEvaluationJobs.html#Bedrock.Paginator.ListEvaluationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listevaluationjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEvaluationJobsRequestListEvaluationJobsPaginateTypeDef]
    ) -> AsyncIterator[ListEvaluationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListEvaluationJobs.html#Bedrock.Paginator.ListEvaluationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listevaluationjobspaginator)
        """


class ListGuardrailsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListGuardrails.html#Bedrock.Paginator.ListGuardrails)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listguardrailspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGuardrailsRequestListGuardrailsPaginateTypeDef]
    ) -> AsyncIterator[ListGuardrailsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListGuardrails.html#Bedrock.Paginator.ListGuardrails.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listguardrailspaginator)
        """


class ListImportedModelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListImportedModels.html#Bedrock.Paginator.ListImportedModels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listimportedmodelspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListImportedModelsRequestListImportedModelsPaginateTypeDef]
    ) -> AsyncIterator[ListImportedModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListImportedModels.html#Bedrock.Paginator.ListImportedModels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listimportedmodelspaginator)
        """


class ListInferenceProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListInferenceProfiles.html#Bedrock.Paginator.ListInferenceProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listinferenceprofilespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListInferenceProfilesRequestListInferenceProfilesPaginateTypeDef]
    ) -> AsyncIterator[ListInferenceProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListInferenceProfiles.html#Bedrock.Paginator.ListInferenceProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listinferenceprofilespaginator)
        """


class ListModelCopyJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelCopyJobs.html#Bedrock.Paginator.ListModelCopyJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelcopyjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListModelCopyJobsRequestListModelCopyJobsPaginateTypeDef]
    ) -> AsyncIterator[ListModelCopyJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelCopyJobs.html#Bedrock.Paginator.ListModelCopyJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelcopyjobspaginator)
        """


class ListModelCustomizationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelCustomizationJobs.html#Bedrock.Paginator.ListModelCustomizationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelcustomizationjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListModelCustomizationJobsRequestListModelCustomizationJobsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListModelCustomizationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelCustomizationJobs.html#Bedrock.Paginator.ListModelCustomizationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelcustomizationjobspaginator)
        """


class ListModelImportJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelImportJobs.html#Bedrock.Paginator.ListModelImportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelimportjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListModelImportJobsRequestListModelImportJobsPaginateTypeDef]
    ) -> AsyncIterator[ListModelImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelImportJobs.html#Bedrock.Paginator.ListModelImportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelimportjobspaginator)
        """


class ListModelInvocationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelInvocationJobs.html#Bedrock.Paginator.ListModelInvocationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelinvocationjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListModelInvocationJobsRequestListModelInvocationJobsPaginateTypeDef]
    ) -> AsyncIterator[ListModelInvocationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelInvocationJobs.html#Bedrock.Paginator.ListModelInvocationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelinvocationjobspaginator)
        """


class ListProvisionedModelThroughputsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListProvisionedModelThroughputs.html#Bedrock.Paginator.ListProvisionedModelThroughputs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listprovisionedmodelthroughputspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListProvisionedModelThroughputsRequestListProvisionedModelThroughputsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListProvisionedModelThroughputsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListProvisionedModelThroughputs.html#Bedrock.Paginator.ListProvisionedModelThroughputs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listprovisionedmodelthroughputspaginator)
        """
