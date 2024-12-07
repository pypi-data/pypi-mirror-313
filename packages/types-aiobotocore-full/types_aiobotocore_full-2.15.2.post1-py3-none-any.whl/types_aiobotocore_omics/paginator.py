"""
Type annotations for omics service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_omics.client import OmicsClient
    from types_aiobotocore_omics.paginator import (
        ListAnnotationImportJobsPaginator,
        ListAnnotationStoreVersionsPaginator,
        ListAnnotationStoresPaginator,
        ListMultipartReadSetUploadsPaginator,
        ListReadSetActivationJobsPaginator,
        ListReadSetExportJobsPaginator,
        ListReadSetImportJobsPaginator,
        ListReadSetUploadPartsPaginator,
        ListReadSetsPaginator,
        ListReferenceImportJobsPaginator,
        ListReferenceStoresPaginator,
        ListReferencesPaginator,
        ListRunGroupsPaginator,
        ListRunTasksPaginator,
        ListRunsPaginator,
        ListSequenceStoresPaginator,
        ListSharesPaginator,
        ListVariantImportJobsPaginator,
        ListVariantStoresPaginator,
        ListWorkflowsPaginator,
    )

    session = get_session()
    with session.create_client("omics") as client:
        client: OmicsClient

        list_annotation_import_jobs_paginator: ListAnnotationImportJobsPaginator = client.get_paginator("list_annotation_import_jobs")
        list_annotation_store_versions_paginator: ListAnnotationStoreVersionsPaginator = client.get_paginator("list_annotation_store_versions")
        list_annotation_stores_paginator: ListAnnotationStoresPaginator = client.get_paginator("list_annotation_stores")
        list_multipart_read_set_uploads_paginator: ListMultipartReadSetUploadsPaginator = client.get_paginator("list_multipart_read_set_uploads")
        list_read_set_activation_jobs_paginator: ListReadSetActivationJobsPaginator = client.get_paginator("list_read_set_activation_jobs")
        list_read_set_export_jobs_paginator: ListReadSetExportJobsPaginator = client.get_paginator("list_read_set_export_jobs")
        list_read_set_import_jobs_paginator: ListReadSetImportJobsPaginator = client.get_paginator("list_read_set_import_jobs")
        list_read_set_upload_parts_paginator: ListReadSetUploadPartsPaginator = client.get_paginator("list_read_set_upload_parts")
        list_read_sets_paginator: ListReadSetsPaginator = client.get_paginator("list_read_sets")
        list_reference_import_jobs_paginator: ListReferenceImportJobsPaginator = client.get_paginator("list_reference_import_jobs")
        list_reference_stores_paginator: ListReferenceStoresPaginator = client.get_paginator("list_reference_stores")
        list_references_paginator: ListReferencesPaginator = client.get_paginator("list_references")
        list_run_groups_paginator: ListRunGroupsPaginator = client.get_paginator("list_run_groups")
        list_run_tasks_paginator: ListRunTasksPaginator = client.get_paginator("list_run_tasks")
        list_runs_paginator: ListRunsPaginator = client.get_paginator("list_runs")
        list_sequence_stores_paginator: ListSequenceStoresPaginator = client.get_paginator("list_sequence_stores")
        list_shares_paginator: ListSharesPaginator = client.get_paginator("list_shares")
        list_variant_import_jobs_paginator: ListVariantImportJobsPaginator = client.get_paginator("list_variant_import_jobs")
        list_variant_stores_paginator: ListVariantStoresPaginator = client.get_paginator("list_variant_stores")
        list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAnnotationImportJobsRequestListAnnotationImportJobsPaginateTypeDef,
    ListAnnotationImportJobsResponseTypeDef,
    ListAnnotationStoresRequestListAnnotationStoresPaginateTypeDef,
    ListAnnotationStoresResponseTypeDef,
    ListAnnotationStoreVersionsRequestListAnnotationStoreVersionsPaginateTypeDef,
    ListAnnotationStoreVersionsResponseTypeDef,
    ListMultipartReadSetUploadsRequestListMultipartReadSetUploadsPaginateTypeDef,
    ListMultipartReadSetUploadsResponseTypeDef,
    ListReadSetActivationJobsRequestListReadSetActivationJobsPaginateTypeDef,
    ListReadSetActivationJobsResponseTypeDef,
    ListReadSetExportJobsRequestListReadSetExportJobsPaginateTypeDef,
    ListReadSetExportJobsResponseTypeDef,
    ListReadSetImportJobsRequestListReadSetImportJobsPaginateTypeDef,
    ListReadSetImportJobsResponseTypeDef,
    ListReadSetsRequestListReadSetsPaginateTypeDef,
    ListReadSetsResponseTypeDef,
    ListReadSetUploadPartsRequestListReadSetUploadPartsPaginateTypeDef,
    ListReadSetUploadPartsResponseTypeDef,
    ListReferenceImportJobsRequestListReferenceImportJobsPaginateTypeDef,
    ListReferenceImportJobsResponseTypeDef,
    ListReferencesRequestListReferencesPaginateTypeDef,
    ListReferencesResponseTypeDef,
    ListReferenceStoresRequestListReferenceStoresPaginateTypeDef,
    ListReferenceStoresResponseTypeDef,
    ListRunGroupsRequestListRunGroupsPaginateTypeDef,
    ListRunGroupsResponseTypeDef,
    ListRunsRequestListRunsPaginateTypeDef,
    ListRunsResponseTypeDef,
    ListRunTasksRequestListRunTasksPaginateTypeDef,
    ListRunTasksResponseTypeDef,
    ListSequenceStoresRequestListSequenceStoresPaginateTypeDef,
    ListSequenceStoresResponseTypeDef,
    ListSharesRequestListSharesPaginateTypeDef,
    ListSharesResponseTypeDef,
    ListVariantImportJobsRequestListVariantImportJobsPaginateTypeDef,
    ListVariantImportJobsResponseTypeDef,
    ListVariantStoresRequestListVariantStoresPaginateTypeDef,
    ListVariantStoresResponseTypeDef,
    ListWorkflowsRequestListWorkflowsPaginateTypeDef,
    ListWorkflowsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAnnotationImportJobsPaginator",
    "ListAnnotationStoreVersionsPaginator",
    "ListAnnotationStoresPaginator",
    "ListMultipartReadSetUploadsPaginator",
    "ListReadSetActivationJobsPaginator",
    "ListReadSetExportJobsPaginator",
    "ListReadSetImportJobsPaginator",
    "ListReadSetUploadPartsPaginator",
    "ListReadSetsPaginator",
    "ListReferenceImportJobsPaginator",
    "ListReferenceStoresPaginator",
    "ListReferencesPaginator",
    "ListRunGroupsPaginator",
    "ListRunTasksPaginator",
    "ListRunsPaginator",
    "ListSequenceStoresPaginator",
    "ListSharesPaginator",
    "ListVariantImportJobsPaginator",
    "ListVariantStoresPaginator",
    "ListWorkflowsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAnnotationImportJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListAnnotationImportJobs.html#Omics.Paginator.ListAnnotationImportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listannotationimportjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListAnnotationImportJobsRequestListAnnotationImportJobsPaginateTypeDef],
    ) -> AsyncIterator[ListAnnotationImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListAnnotationImportJobs.html#Omics.Paginator.ListAnnotationImportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listannotationimportjobspaginator)
        """


class ListAnnotationStoreVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListAnnotationStoreVersions.html#Omics.Paginator.ListAnnotationStoreVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listannotationstoreversionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListAnnotationStoreVersionsRequestListAnnotationStoreVersionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListAnnotationStoreVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListAnnotationStoreVersions.html#Omics.Paginator.ListAnnotationStoreVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listannotationstoreversionspaginator)
        """


class ListAnnotationStoresPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListAnnotationStores.html#Omics.Paginator.ListAnnotationStores)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listannotationstorespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAnnotationStoresRequestListAnnotationStoresPaginateTypeDef]
    ) -> AsyncIterator[ListAnnotationStoresResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListAnnotationStores.html#Omics.Paginator.ListAnnotationStores.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listannotationstorespaginator)
        """


class ListMultipartReadSetUploadsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListMultipartReadSetUploads.html#Omics.Paginator.ListMultipartReadSetUploads)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listmultipartreadsetuploadspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListMultipartReadSetUploadsRequestListMultipartReadSetUploadsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListMultipartReadSetUploadsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListMultipartReadSetUploads.html#Omics.Paginator.ListMultipartReadSetUploads.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listmultipartreadsetuploadspaginator)
        """


class ListReadSetActivationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSetActivationJobs.html#Omics.Paginator.ListReadSetActivationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listreadsetactivationjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListReadSetActivationJobsRequestListReadSetActivationJobsPaginateTypeDef],
    ) -> AsyncIterator[ListReadSetActivationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSetActivationJobs.html#Omics.Paginator.ListReadSetActivationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listreadsetactivationjobspaginator)
        """


class ListReadSetExportJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSetExportJobs.html#Omics.Paginator.ListReadSetExportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listreadsetexportjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReadSetExportJobsRequestListReadSetExportJobsPaginateTypeDef]
    ) -> AsyncIterator[ListReadSetExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSetExportJobs.html#Omics.Paginator.ListReadSetExportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listreadsetexportjobspaginator)
        """


class ListReadSetImportJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSetImportJobs.html#Omics.Paginator.ListReadSetImportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listreadsetimportjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReadSetImportJobsRequestListReadSetImportJobsPaginateTypeDef]
    ) -> AsyncIterator[ListReadSetImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSetImportJobs.html#Omics.Paginator.ListReadSetImportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listreadsetimportjobspaginator)
        """


class ListReadSetUploadPartsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSetUploadParts.html#Omics.Paginator.ListReadSetUploadParts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listreadsetuploadpartspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReadSetUploadPartsRequestListReadSetUploadPartsPaginateTypeDef]
    ) -> AsyncIterator[ListReadSetUploadPartsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSetUploadParts.html#Omics.Paginator.ListReadSetUploadParts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listreadsetuploadpartspaginator)
        """


class ListReadSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSets.html#Omics.Paginator.ListReadSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listreadsetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReadSetsRequestListReadSetsPaginateTypeDef]
    ) -> AsyncIterator[ListReadSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSets.html#Omics.Paginator.ListReadSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listreadsetspaginator)
        """


class ListReferenceImportJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReferenceImportJobs.html#Omics.Paginator.ListReferenceImportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listreferenceimportjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReferenceImportJobsRequestListReferenceImportJobsPaginateTypeDef]
    ) -> AsyncIterator[ListReferenceImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReferenceImportJobs.html#Omics.Paginator.ListReferenceImportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listreferenceimportjobspaginator)
        """


class ListReferenceStoresPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReferenceStores.html#Omics.Paginator.ListReferenceStores)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listreferencestorespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReferenceStoresRequestListReferenceStoresPaginateTypeDef]
    ) -> AsyncIterator[ListReferenceStoresResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReferenceStores.html#Omics.Paginator.ListReferenceStores.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listreferencestorespaginator)
        """


class ListReferencesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReferences.html#Omics.Paginator.ListReferences)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listreferencespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReferencesRequestListReferencesPaginateTypeDef]
    ) -> AsyncIterator[ListReferencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReferences.html#Omics.Paginator.ListReferences.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listreferencespaginator)
        """


class ListRunGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListRunGroups.html#Omics.Paginator.ListRunGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listrungroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRunGroupsRequestListRunGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListRunGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListRunGroups.html#Omics.Paginator.ListRunGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listrungroupspaginator)
        """


class ListRunTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListRunTasks.html#Omics.Paginator.ListRunTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listruntaskspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRunTasksRequestListRunTasksPaginateTypeDef]
    ) -> AsyncIterator[ListRunTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListRunTasks.html#Omics.Paginator.ListRunTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listruntaskspaginator)
        """


class ListRunsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListRuns.html#Omics.Paginator.ListRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listrunspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRunsRequestListRunsPaginateTypeDef]
    ) -> AsyncIterator[ListRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListRuns.html#Omics.Paginator.ListRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listrunspaginator)
        """


class ListSequenceStoresPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListSequenceStores.html#Omics.Paginator.ListSequenceStores)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listsequencestorespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSequenceStoresRequestListSequenceStoresPaginateTypeDef]
    ) -> AsyncIterator[ListSequenceStoresResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListSequenceStores.html#Omics.Paginator.ListSequenceStores.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listsequencestorespaginator)
        """


class ListSharesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListShares.html#Omics.Paginator.ListShares)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listsharespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSharesRequestListSharesPaginateTypeDef]
    ) -> AsyncIterator[ListSharesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListShares.html#Omics.Paginator.ListShares.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listsharespaginator)
        """


class ListVariantImportJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListVariantImportJobs.html#Omics.Paginator.ListVariantImportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listvariantimportjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListVariantImportJobsRequestListVariantImportJobsPaginateTypeDef]
    ) -> AsyncIterator[ListVariantImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListVariantImportJobs.html#Omics.Paginator.ListVariantImportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listvariantimportjobspaginator)
        """


class ListVariantStoresPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListVariantStores.html#Omics.Paginator.ListVariantStores)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listvariantstorespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListVariantStoresRequestListVariantStoresPaginateTypeDef]
    ) -> AsyncIterator[ListVariantStoresResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListVariantStores.html#Omics.Paginator.ListVariantStores.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listvariantstorespaginator)
        """


class ListWorkflowsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListWorkflows.html#Omics.Paginator.ListWorkflows)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listworkflowspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorkflowsRequestListWorkflowsPaginateTypeDef]
    ) -> AsyncIterator[ListWorkflowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListWorkflows.html#Omics.Paginator.ListWorkflows.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/paginators/#listworkflowspaginator)
        """
