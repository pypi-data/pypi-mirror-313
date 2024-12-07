"""
Type annotations for omics service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_omics.client import OmicsClient

    session = get_session()
    async with session.create_client("omics") as client:
        client: OmicsClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListAnnotationImportJobsPaginator,
    ListAnnotationStoresPaginator,
    ListAnnotationStoreVersionsPaginator,
    ListMultipartReadSetUploadsPaginator,
    ListReadSetActivationJobsPaginator,
    ListReadSetExportJobsPaginator,
    ListReadSetImportJobsPaginator,
    ListReadSetsPaginator,
    ListReadSetUploadPartsPaginator,
    ListReferenceImportJobsPaginator,
    ListReferencesPaginator,
    ListReferenceStoresPaginator,
    ListRunGroupsPaginator,
    ListRunsPaginator,
    ListRunTasksPaginator,
    ListSequenceStoresPaginator,
    ListSharesPaginator,
    ListVariantImportJobsPaginator,
    ListVariantStoresPaginator,
    ListWorkflowsPaginator,
)
from .type_defs import (
    AbortMultipartReadSetUploadRequestRequestTypeDef,
    AcceptShareRequestRequestTypeDef,
    AcceptShareResponseTypeDef,
    BatchDeleteReadSetRequestRequestTypeDef,
    BatchDeleteReadSetResponseTypeDef,
    CancelAnnotationImportRequestRequestTypeDef,
    CancelRunRequestRequestTypeDef,
    CancelVariantImportRequestRequestTypeDef,
    CompleteMultipartReadSetUploadRequestRequestTypeDef,
    CompleteMultipartReadSetUploadResponseTypeDef,
    CreateAnnotationStoreRequestRequestTypeDef,
    CreateAnnotationStoreResponseTypeDef,
    CreateAnnotationStoreVersionRequestRequestTypeDef,
    CreateAnnotationStoreVersionResponseTypeDef,
    CreateMultipartReadSetUploadRequestRequestTypeDef,
    CreateMultipartReadSetUploadResponseTypeDef,
    CreateReferenceStoreRequestRequestTypeDef,
    CreateReferenceStoreResponseTypeDef,
    CreateRunGroupRequestRequestTypeDef,
    CreateRunGroupResponseTypeDef,
    CreateSequenceStoreRequestRequestTypeDef,
    CreateSequenceStoreResponseTypeDef,
    CreateShareRequestRequestTypeDef,
    CreateShareResponseTypeDef,
    CreateVariantStoreRequestRequestTypeDef,
    CreateVariantStoreResponseTypeDef,
    CreateWorkflowRequestRequestTypeDef,
    CreateWorkflowResponseTypeDef,
    DeleteAnnotationStoreRequestRequestTypeDef,
    DeleteAnnotationStoreResponseTypeDef,
    DeleteAnnotationStoreVersionsRequestRequestTypeDef,
    DeleteAnnotationStoreVersionsResponseTypeDef,
    DeleteReferenceRequestRequestTypeDef,
    DeleteReferenceStoreRequestRequestTypeDef,
    DeleteRunGroupRequestRequestTypeDef,
    DeleteRunRequestRequestTypeDef,
    DeleteSequenceStoreRequestRequestTypeDef,
    DeleteShareRequestRequestTypeDef,
    DeleteShareResponseTypeDef,
    DeleteVariantStoreRequestRequestTypeDef,
    DeleteVariantStoreResponseTypeDef,
    DeleteWorkflowRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAnnotationImportRequestRequestTypeDef,
    GetAnnotationImportResponseTypeDef,
    GetAnnotationStoreRequestRequestTypeDef,
    GetAnnotationStoreResponseTypeDef,
    GetAnnotationStoreVersionRequestRequestTypeDef,
    GetAnnotationStoreVersionResponseTypeDef,
    GetReadSetActivationJobRequestRequestTypeDef,
    GetReadSetActivationJobResponseTypeDef,
    GetReadSetExportJobRequestRequestTypeDef,
    GetReadSetExportJobResponseTypeDef,
    GetReadSetImportJobRequestRequestTypeDef,
    GetReadSetImportJobResponseTypeDef,
    GetReadSetMetadataRequestRequestTypeDef,
    GetReadSetMetadataResponseTypeDef,
    GetReadSetRequestRequestTypeDef,
    GetReadSetResponseTypeDef,
    GetReferenceImportJobRequestRequestTypeDef,
    GetReferenceImportJobResponseTypeDef,
    GetReferenceMetadataRequestRequestTypeDef,
    GetReferenceMetadataResponseTypeDef,
    GetReferenceRequestRequestTypeDef,
    GetReferenceResponseTypeDef,
    GetReferenceStoreRequestRequestTypeDef,
    GetReferenceStoreResponseTypeDef,
    GetRunGroupRequestRequestTypeDef,
    GetRunGroupResponseTypeDef,
    GetRunRequestRequestTypeDef,
    GetRunResponseTypeDef,
    GetRunTaskRequestRequestTypeDef,
    GetRunTaskResponseTypeDef,
    GetSequenceStoreRequestRequestTypeDef,
    GetSequenceStoreResponseTypeDef,
    GetShareRequestRequestTypeDef,
    GetShareResponseTypeDef,
    GetVariantImportRequestRequestTypeDef,
    GetVariantImportResponseTypeDef,
    GetVariantStoreRequestRequestTypeDef,
    GetVariantStoreResponseTypeDef,
    GetWorkflowRequestRequestTypeDef,
    GetWorkflowResponseTypeDef,
    ListAnnotationImportJobsRequestRequestTypeDef,
    ListAnnotationImportJobsResponseTypeDef,
    ListAnnotationStoresRequestRequestTypeDef,
    ListAnnotationStoresResponseTypeDef,
    ListAnnotationStoreVersionsRequestRequestTypeDef,
    ListAnnotationStoreVersionsResponseTypeDef,
    ListMultipartReadSetUploadsRequestRequestTypeDef,
    ListMultipartReadSetUploadsResponseTypeDef,
    ListReadSetActivationJobsRequestRequestTypeDef,
    ListReadSetActivationJobsResponseTypeDef,
    ListReadSetExportJobsRequestRequestTypeDef,
    ListReadSetExportJobsResponseTypeDef,
    ListReadSetImportJobsRequestRequestTypeDef,
    ListReadSetImportJobsResponseTypeDef,
    ListReadSetsRequestRequestTypeDef,
    ListReadSetsResponseTypeDef,
    ListReadSetUploadPartsRequestRequestTypeDef,
    ListReadSetUploadPartsResponseTypeDef,
    ListReferenceImportJobsRequestRequestTypeDef,
    ListReferenceImportJobsResponseTypeDef,
    ListReferencesRequestRequestTypeDef,
    ListReferencesResponseTypeDef,
    ListReferenceStoresRequestRequestTypeDef,
    ListReferenceStoresResponseTypeDef,
    ListRunGroupsRequestRequestTypeDef,
    ListRunGroupsResponseTypeDef,
    ListRunsRequestRequestTypeDef,
    ListRunsResponseTypeDef,
    ListRunTasksRequestRequestTypeDef,
    ListRunTasksResponseTypeDef,
    ListSequenceStoresRequestRequestTypeDef,
    ListSequenceStoresResponseTypeDef,
    ListSharesRequestRequestTypeDef,
    ListSharesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVariantImportJobsRequestRequestTypeDef,
    ListVariantImportJobsResponseTypeDef,
    ListVariantStoresRequestRequestTypeDef,
    ListVariantStoresResponseTypeDef,
    ListWorkflowsRequestRequestTypeDef,
    ListWorkflowsResponseTypeDef,
    StartAnnotationImportRequestRequestTypeDef,
    StartAnnotationImportResponseTypeDef,
    StartReadSetActivationJobRequestRequestTypeDef,
    StartReadSetActivationJobResponseTypeDef,
    StartReadSetExportJobRequestRequestTypeDef,
    StartReadSetExportJobResponseTypeDef,
    StartReadSetImportJobRequestRequestTypeDef,
    StartReadSetImportJobResponseTypeDef,
    StartReferenceImportJobRequestRequestTypeDef,
    StartReferenceImportJobResponseTypeDef,
    StartRunRequestRequestTypeDef,
    StartRunResponseTypeDef,
    StartVariantImportRequestRequestTypeDef,
    StartVariantImportResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAnnotationStoreRequestRequestTypeDef,
    UpdateAnnotationStoreResponseTypeDef,
    UpdateAnnotationStoreVersionRequestRequestTypeDef,
    UpdateAnnotationStoreVersionResponseTypeDef,
    UpdateRunGroupRequestRequestTypeDef,
    UpdateVariantStoreRequestRequestTypeDef,
    UpdateVariantStoreResponseTypeDef,
    UpdateWorkflowRequestRequestTypeDef,
    UploadReadSetPartRequestRequestTypeDef,
    UploadReadSetPartResponseTypeDef,
)
from .waiter import (
    AnnotationImportJobCreatedWaiter,
    AnnotationStoreCreatedWaiter,
    AnnotationStoreDeletedWaiter,
    AnnotationStoreVersionCreatedWaiter,
    AnnotationStoreVersionDeletedWaiter,
    ReadSetActivationJobCompletedWaiter,
    ReadSetExportJobCompletedWaiter,
    ReadSetImportJobCompletedWaiter,
    ReferenceImportJobCompletedWaiter,
    RunCompletedWaiter,
    RunRunningWaiter,
    TaskCompletedWaiter,
    TaskRunningWaiter,
    VariantImportJobCreatedWaiter,
    VariantStoreCreatedWaiter,
    VariantStoreDeletedWaiter,
    WorkflowActiveWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("OmicsClient",)


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
    NotSupportedOperationException: Type[BotocoreClientError]
    RangeNotSatisfiableException: Type[BotocoreClientError]
    RequestTimeoutException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class OmicsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        OmicsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#close)
        """

    async def abort_multipart_read_set_upload(
        self, **kwargs: Unpack[AbortMultipartReadSetUploadRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops a multipart upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/abort_multipart_read_set_upload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#abort_multipart_read_set_upload)
        """

    async def accept_share(
        self, **kwargs: Unpack[AcceptShareRequestRequestTypeDef]
    ) -> AcceptShareResponseTypeDef:
        """
        Accept a resource share request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/accept_share.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#accept_share)
        """

    async def batch_delete_read_set(
        self, **kwargs: Unpack[BatchDeleteReadSetRequestRequestTypeDef]
    ) -> BatchDeleteReadSetResponseTypeDef:
        """
        Deletes one or more read sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/batch_delete_read_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#batch_delete_read_set)
        """

    async def cancel_annotation_import_job(
        self, **kwargs: Unpack[CancelAnnotationImportRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels an annotation import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/cancel_annotation_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#cancel_annotation_import_job)
        """

    async def cancel_run(
        self, **kwargs: Unpack[CancelRunRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels a run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/cancel_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#cancel_run)
        """

    async def cancel_variant_import_job(
        self, **kwargs: Unpack[CancelVariantImportRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels a variant import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/cancel_variant_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#cancel_variant_import_job)
        """

    async def complete_multipart_read_set_upload(
        self, **kwargs: Unpack[CompleteMultipartReadSetUploadRequestRequestTypeDef]
    ) -> CompleteMultipartReadSetUploadResponseTypeDef:
        """
        Concludes a multipart upload once you have uploaded all the components.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/complete_multipart_read_set_upload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#complete_multipart_read_set_upload)
        """

    async def create_annotation_store(
        self, **kwargs: Unpack[CreateAnnotationStoreRequestRequestTypeDef]
    ) -> CreateAnnotationStoreResponseTypeDef:
        """
        Creates an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_annotation_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_annotation_store)
        """

    async def create_annotation_store_version(
        self, **kwargs: Unpack[CreateAnnotationStoreVersionRequestRequestTypeDef]
    ) -> CreateAnnotationStoreVersionResponseTypeDef:
        """
        Creates a new version of an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_annotation_store_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_annotation_store_version)
        """

    async def create_multipart_read_set_upload(
        self, **kwargs: Unpack[CreateMultipartReadSetUploadRequestRequestTypeDef]
    ) -> CreateMultipartReadSetUploadResponseTypeDef:
        """
        Begins a multipart read set upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_multipart_read_set_upload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_multipart_read_set_upload)
        """

    async def create_reference_store(
        self, **kwargs: Unpack[CreateReferenceStoreRequestRequestTypeDef]
    ) -> CreateReferenceStoreResponseTypeDef:
        """
        Creates a reference store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_reference_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_reference_store)
        """

    async def create_run_group(
        self, **kwargs: Unpack[CreateRunGroupRequestRequestTypeDef]
    ) -> CreateRunGroupResponseTypeDef:
        """
        You can optionally create a run group to limit the compute resources for the
        runs that you add to the group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_run_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_run_group)
        """

    async def create_sequence_store(
        self, **kwargs: Unpack[CreateSequenceStoreRequestRequestTypeDef]
    ) -> CreateSequenceStoreResponseTypeDef:
        """
        Creates a sequence store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_sequence_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_sequence_store)
        """

    async def create_share(
        self, **kwargs: Unpack[CreateShareRequestRequestTypeDef]
    ) -> CreateShareResponseTypeDef:
        """
        Creates a cross-account shared resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_share.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_share)
        """

    async def create_variant_store(
        self, **kwargs: Unpack[CreateVariantStoreRequestRequestTypeDef]
    ) -> CreateVariantStoreResponseTypeDef:
        """
        Creates a variant store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_variant_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_variant_store)
        """

    async def create_workflow(
        self, **kwargs: Unpack[CreateWorkflowRequestRequestTypeDef]
    ) -> CreateWorkflowResponseTypeDef:
        """
        Creates a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_workflow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_workflow)
        """

    async def delete_annotation_store(
        self, **kwargs: Unpack[DeleteAnnotationStoreRequestRequestTypeDef]
    ) -> DeleteAnnotationStoreResponseTypeDef:
        """
        Deletes an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_annotation_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_annotation_store)
        """

    async def delete_annotation_store_versions(
        self, **kwargs: Unpack[DeleteAnnotationStoreVersionsRequestRequestTypeDef]
    ) -> DeleteAnnotationStoreVersionsResponseTypeDef:
        """
        Deletes one or multiple versions of an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_annotation_store_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_annotation_store_versions)
        """

    async def delete_reference(
        self, **kwargs: Unpack[DeleteReferenceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a genome reference.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_reference.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_reference)
        """

    async def delete_reference_store(
        self, **kwargs: Unpack[DeleteReferenceStoreRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a genome reference store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_reference_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_reference_store)
        """

    async def delete_run(
        self, **kwargs: Unpack[DeleteRunRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_run)
        """

    async def delete_run_group(
        self, **kwargs: Unpack[DeleteRunGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a workflow run group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_run_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_run_group)
        """

    async def delete_sequence_store(
        self, **kwargs: Unpack[DeleteSequenceStoreRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a sequence store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_sequence_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_sequence_store)
        """

    async def delete_share(
        self, **kwargs: Unpack[DeleteShareRequestRequestTypeDef]
    ) -> DeleteShareResponseTypeDef:
        """
        Deletes a resource share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_share.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_share)
        """

    async def delete_variant_store(
        self, **kwargs: Unpack[DeleteVariantStoreRequestRequestTypeDef]
    ) -> DeleteVariantStoreResponseTypeDef:
        """
        Deletes a variant store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_variant_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_variant_store)
        """

    async def delete_workflow(
        self, **kwargs: Unpack[DeleteWorkflowRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_workflow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_workflow)
        """

    async def get_annotation_import_job(
        self, **kwargs: Unpack[GetAnnotationImportRequestRequestTypeDef]
    ) -> GetAnnotationImportResponseTypeDef:
        """
        Gets information about an annotation import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_annotation_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_annotation_import_job)
        """

    async def get_annotation_store(
        self, **kwargs: Unpack[GetAnnotationStoreRequestRequestTypeDef]
    ) -> GetAnnotationStoreResponseTypeDef:
        """
        Gets information about an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_annotation_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_annotation_store)
        """

    async def get_annotation_store_version(
        self, **kwargs: Unpack[GetAnnotationStoreVersionRequestRequestTypeDef]
    ) -> GetAnnotationStoreVersionResponseTypeDef:
        """
        Retrieves the metadata for an annotation store version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_annotation_store_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_annotation_store_version)
        """

    async def get_read_set(
        self, **kwargs: Unpack[GetReadSetRequestRequestTypeDef]
    ) -> GetReadSetResponseTypeDef:
        """
        Gets a file from a read set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_read_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_read_set)
        """

    async def get_read_set_activation_job(
        self, **kwargs: Unpack[GetReadSetActivationJobRequestRequestTypeDef]
    ) -> GetReadSetActivationJobResponseTypeDef:
        """
        Gets information about a read set activation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_read_set_activation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_read_set_activation_job)
        """

    async def get_read_set_export_job(
        self, **kwargs: Unpack[GetReadSetExportJobRequestRequestTypeDef]
    ) -> GetReadSetExportJobResponseTypeDef:
        """
        Gets information about a read set export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_read_set_export_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_read_set_export_job)
        """

    async def get_read_set_import_job(
        self, **kwargs: Unpack[GetReadSetImportJobRequestRequestTypeDef]
    ) -> GetReadSetImportJobResponseTypeDef:
        """
        Gets information about a read set import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_read_set_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_read_set_import_job)
        """

    async def get_read_set_metadata(
        self, **kwargs: Unpack[GetReadSetMetadataRequestRequestTypeDef]
    ) -> GetReadSetMetadataResponseTypeDef:
        """
        Gets details about a read set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_read_set_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_read_set_metadata)
        """

    async def get_reference(
        self, **kwargs: Unpack[GetReferenceRequestRequestTypeDef]
    ) -> GetReferenceResponseTypeDef:
        """
        Gets a reference file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_reference.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_reference)
        """

    async def get_reference_import_job(
        self, **kwargs: Unpack[GetReferenceImportJobRequestRequestTypeDef]
    ) -> GetReferenceImportJobResponseTypeDef:
        """
        Gets information about a reference import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_reference_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_reference_import_job)
        """

    async def get_reference_metadata(
        self, **kwargs: Unpack[GetReferenceMetadataRequestRequestTypeDef]
    ) -> GetReferenceMetadataResponseTypeDef:
        """
        Gets information about a genome reference's metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_reference_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_reference_metadata)
        """

    async def get_reference_store(
        self, **kwargs: Unpack[GetReferenceStoreRequestRequestTypeDef]
    ) -> GetReferenceStoreResponseTypeDef:
        """
        Gets information about a reference store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_reference_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_reference_store)
        """

    async def get_run(self, **kwargs: Unpack[GetRunRequestRequestTypeDef]) -> GetRunResponseTypeDef:
        """
        Gets information about a workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_run)
        """

    async def get_run_group(
        self, **kwargs: Unpack[GetRunGroupRequestRequestTypeDef]
    ) -> GetRunGroupResponseTypeDef:
        """
        Gets information about a workflow run group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_run_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_run_group)
        """

    async def get_run_task(
        self, **kwargs: Unpack[GetRunTaskRequestRequestTypeDef]
    ) -> GetRunTaskResponseTypeDef:
        """
        Gets information about a workflow run task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_run_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_run_task)
        """

    async def get_sequence_store(
        self, **kwargs: Unpack[GetSequenceStoreRequestRequestTypeDef]
    ) -> GetSequenceStoreResponseTypeDef:
        """
        Gets information about a sequence store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_sequence_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_sequence_store)
        """

    async def get_share(
        self, **kwargs: Unpack[GetShareRequestRequestTypeDef]
    ) -> GetShareResponseTypeDef:
        """
        Retrieves the metadata for the specified resource share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_share.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_share)
        """

    async def get_variant_import_job(
        self, **kwargs: Unpack[GetVariantImportRequestRequestTypeDef]
    ) -> GetVariantImportResponseTypeDef:
        """
        Gets information about a variant import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_variant_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_variant_import_job)
        """

    async def get_variant_store(
        self, **kwargs: Unpack[GetVariantStoreRequestRequestTypeDef]
    ) -> GetVariantStoreResponseTypeDef:
        """
        Gets information about a variant store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_variant_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_variant_store)
        """

    async def get_workflow(
        self, **kwargs: Unpack[GetWorkflowRequestRequestTypeDef]
    ) -> GetWorkflowResponseTypeDef:
        """
        Gets information about a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_workflow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_workflow)
        """

    async def list_annotation_import_jobs(
        self, **kwargs: Unpack[ListAnnotationImportJobsRequestRequestTypeDef]
    ) -> ListAnnotationImportJobsResponseTypeDef:
        """
        Retrieves a list of annotation import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_annotation_import_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_annotation_import_jobs)
        """

    async def list_annotation_store_versions(
        self, **kwargs: Unpack[ListAnnotationStoreVersionsRequestRequestTypeDef]
    ) -> ListAnnotationStoreVersionsResponseTypeDef:
        """
        Lists the versions of an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_annotation_store_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_annotation_store_versions)
        """

    async def list_annotation_stores(
        self, **kwargs: Unpack[ListAnnotationStoresRequestRequestTypeDef]
    ) -> ListAnnotationStoresResponseTypeDef:
        """
        Retrieves a list of annotation stores.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_annotation_stores.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_annotation_stores)
        """

    async def list_multipart_read_set_uploads(
        self, **kwargs: Unpack[ListMultipartReadSetUploadsRequestRequestTypeDef]
    ) -> ListMultipartReadSetUploadsResponseTypeDef:
        """
        Lists multipart read set uploads and for in progress uploads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_multipart_read_set_uploads.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_multipart_read_set_uploads)
        """

    async def list_read_set_activation_jobs(
        self, **kwargs: Unpack[ListReadSetActivationJobsRequestRequestTypeDef]
    ) -> ListReadSetActivationJobsResponseTypeDef:
        """
        Retrieves a list of read set activation jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_read_set_activation_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_read_set_activation_jobs)
        """

    async def list_read_set_export_jobs(
        self, **kwargs: Unpack[ListReadSetExportJobsRequestRequestTypeDef]
    ) -> ListReadSetExportJobsResponseTypeDef:
        """
        Retrieves a list of read set export jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_read_set_export_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_read_set_export_jobs)
        """

    async def list_read_set_import_jobs(
        self, **kwargs: Unpack[ListReadSetImportJobsRequestRequestTypeDef]
    ) -> ListReadSetImportJobsResponseTypeDef:
        """
        Retrieves a list of read set import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_read_set_import_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_read_set_import_jobs)
        """

    async def list_read_set_upload_parts(
        self, **kwargs: Unpack[ListReadSetUploadPartsRequestRequestTypeDef]
    ) -> ListReadSetUploadPartsResponseTypeDef:
        """
        This operation will list all parts in a requested multipart upload for a
        sequence store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_read_set_upload_parts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_read_set_upload_parts)
        """

    async def list_read_sets(
        self, **kwargs: Unpack[ListReadSetsRequestRequestTypeDef]
    ) -> ListReadSetsResponseTypeDef:
        """
        Retrieves a list of read sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_read_sets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_read_sets)
        """

    async def list_reference_import_jobs(
        self, **kwargs: Unpack[ListReferenceImportJobsRequestRequestTypeDef]
    ) -> ListReferenceImportJobsResponseTypeDef:
        """
        Retrieves a list of reference import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_reference_import_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_reference_import_jobs)
        """

    async def list_reference_stores(
        self, **kwargs: Unpack[ListReferenceStoresRequestRequestTypeDef]
    ) -> ListReferenceStoresResponseTypeDef:
        """
        Retrieves a list of reference stores.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_reference_stores.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_reference_stores)
        """

    async def list_references(
        self, **kwargs: Unpack[ListReferencesRequestRequestTypeDef]
    ) -> ListReferencesResponseTypeDef:
        """
        Retrieves a list of references.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_references.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_references)
        """

    async def list_run_groups(
        self, **kwargs: Unpack[ListRunGroupsRequestRequestTypeDef]
    ) -> ListRunGroupsResponseTypeDef:
        """
        Retrieves a list of run groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_run_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_run_groups)
        """

    async def list_run_tasks(
        self, **kwargs: Unpack[ListRunTasksRequestRequestTypeDef]
    ) -> ListRunTasksResponseTypeDef:
        """
        Retrieves a list of tasks for a run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_run_tasks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_run_tasks)
        """

    async def list_runs(
        self, **kwargs: Unpack[ListRunsRequestRequestTypeDef]
    ) -> ListRunsResponseTypeDef:
        """
        Retrieves a list of runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_runs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_runs)
        """

    async def list_sequence_stores(
        self, **kwargs: Unpack[ListSequenceStoresRequestRequestTypeDef]
    ) -> ListSequenceStoresResponseTypeDef:
        """
        Retrieves a list of sequence stores.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_sequence_stores.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_sequence_stores)
        """

    async def list_shares(
        self, **kwargs: Unpack[ListSharesRequestRequestTypeDef]
    ) -> ListSharesResponseTypeDef:
        """
        Retrieves the resource shares associated with an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_shares.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_shares)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves a list of tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_tags_for_resource)
        """

    async def list_variant_import_jobs(
        self, **kwargs: Unpack[ListVariantImportJobsRequestRequestTypeDef]
    ) -> ListVariantImportJobsResponseTypeDef:
        """
        Retrieves a list of variant import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_variant_import_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_variant_import_jobs)
        """

    async def list_variant_stores(
        self, **kwargs: Unpack[ListVariantStoresRequestRequestTypeDef]
    ) -> ListVariantStoresResponseTypeDef:
        """
        Retrieves a list of variant stores.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_variant_stores.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_variant_stores)
        """

    async def list_workflows(
        self, **kwargs: Unpack[ListWorkflowsRequestRequestTypeDef]
    ) -> ListWorkflowsResponseTypeDef:
        """
        Retrieves a list of workflows.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_workflows.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_workflows)
        """

    async def start_annotation_import_job(
        self, **kwargs: Unpack[StartAnnotationImportRequestRequestTypeDef]
    ) -> StartAnnotationImportResponseTypeDef:
        """
        Starts an annotation import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/start_annotation_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#start_annotation_import_job)
        """

    async def start_read_set_activation_job(
        self, **kwargs: Unpack[StartReadSetActivationJobRequestRequestTypeDef]
    ) -> StartReadSetActivationJobResponseTypeDef:
        """
        Activates an archived read set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/start_read_set_activation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#start_read_set_activation_job)
        """

    async def start_read_set_export_job(
        self, **kwargs: Unpack[StartReadSetExportJobRequestRequestTypeDef]
    ) -> StartReadSetExportJobResponseTypeDef:
        """
        Exports a read set to Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/start_read_set_export_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#start_read_set_export_job)
        """

    async def start_read_set_import_job(
        self, **kwargs: Unpack[StartReadSetImportJobRequestRequestTypeDef]
    ) -> StartReadSetImportJobResponseTypeDef:
        """
        Starts a read set import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/start_read_set_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#start_read_set_import_job)
        """

    async def start_reference_import_job(
        self, **kwargs: Unpack[StartReferenceImportJobRequestRequestTypeDef]
    ) -> StartReferenceImportJobResponseTypeDef:
        """
        Starts a reference import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/start_reference_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#start_reference_import_job)
        """

    async def start_run(
        self, **kwargs: Unpack[StartRunRequestRequestTypeDef]
    ) -> StartRunResponseTypeDef:
        """
        Starts a workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/start_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#start_run)
        """

    async def start_variant_import_job(
        self, **kwargs: Unpack[StartVariantImportRequestRequestTypeDef]
    ) -> StartVariantImportResponseTypeDef:
        """
        Starts a variant import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/start_variant_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#start_variant_import_job)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Tags a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#untag_resource)
        """

    async def update_annotation_store(
        self, **kwargs: Unpack[UpdateAnnotationStoreRequestRequestTypeDef]
    ) -> UpdateAnnotationStoreResponseTypeDef:
        """
        Updates an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/update_annotation_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#update_annotation_store)
        """

    async def update_annotation_store_version(
        self, **kwargs: Unpack[UpdateAnnotationStoreVersionRequestRequestTypeDef]
    ) -> UpdateAnnotationStoreVersionResponseTypeDef:
        """
        Updates the description of an annotation store version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/update_annotation_store_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#update_annotation_store_version)
        """

    async def update_run_group(
        self, **kwargs: Unpack[UpdateRunGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a run group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/update_run_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#update_run_group)
        """

    async def update_variant_store(
        self, **kwargs: Unpack[UpdateVariantStoreRequestRequestTypeDef]
    ) -> UpdateVariantStoreResponseTypeDef:
        """
        Updates a variant store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/update_variant_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#update_variant_store)
        """

    async def update_workflow(
        self, **kwargs: Unpack[UpdateWorkflowRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/update_workflow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#update_workflow)
        """

    async def upload_read_set_part(
        self, **kwargs: Unpack[UploadReadSetPartRequestRequestTypeDef]
    ) -> UploadReadSetPartResponseTypeDef:
        """
        This operation uploads a specific part of a read set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/upload_read_set_part.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#upload_read_set_part)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_annotation_import_jobs"]
    ) -> ListAnnotationImportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_annotation_store_versions"]
    ) -> ListAnnotationStoreVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_annotation_stores"]
    ) -> ListAnnotationStoresPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_multipart_read_set_uploads"]
    ) -> ListMultipartReadSetUploadsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_read_set_activation_jobs"]
    ) -> ListReadSetActivationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_read_set_export_jobs"]
    ) -> ListReadSetExportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_read_set_import_jobs"]
    ) -> ListReadSetImportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_read_set_upload_parts"]
    ) -> ListReadSetUploadPartsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_read_sets"]) -> ListReadSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_reference_import_jobs"]
    ) -> ListReferenceImportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_reference_stores"]
    ) -> ListReferenceStoresPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_references"]) -> ListReferencesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_run_groups"]) -> ListRunGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_run_tasks"]) -> ListRunTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_runs"]) -> ListRunsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_sequence_stores"]
    ) -> ListSequenceStoresPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_shares"]) -> ListSharesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_variant_import_jobs"]
    ) -> ListVariantImportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_variant_stores"]
    ) -> ListVariantStoresPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workflows"]) -> ListWorkflowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["annotation_import_job_created"]
    ) -> AnnotationImportJobCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["annotation_store_created"]
    ) -> AnnotationStoreCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["annotation_store_deleted"]
    ) -> AnnotationStoreDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["annotation_store_version_created"]
    ) -> AnnotationStoreVersionCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["annotation_store_version_deleted"]
    ) -> AnnotationStoreVersionDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["read_set_activation_job_completed"]
    ) -> ReadSetActivationJobCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["read_set_export_job_completed"]
    ) -> ReadSetExportJobCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["read_set_import_job_completed"]
    ) -> ReadSetImportJobCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["reference_import_job_completed"]
    ) -> ReferenceImportJobCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["run_completed"]) -> RunCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["run_running"]) -> RunRunningWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["task_completed"]) -> TaskCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["task_running"]) -> TaskRunningWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["variant_import_job_created"]
    ) -> VariantImportJobCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["variant_store_created"]
    ) -> VariantStoreCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["variant_store_deleted"]
    ) -> VariantStoreDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["workflow_active"]) -> WorkflowActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    async def __aenter__(self) -> "OmicsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/)
        """
