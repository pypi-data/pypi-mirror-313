"""
Type annotations for rekognition service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_rekognition.client import RekognitionClient
    from types_aiobotocore_rekognition.paginator import (
        DescribeProjectVersionsPaginator,
        DescribeProjectsPaginator,
        ListCollectionsPaginator,
        ListDatasetEntriesPaginator,
        ListDatasetLabelsPaginator,
        ListFacesPaginator,
        ListProjectPoliciesPaginator,
        ListStreamProcessorsPaginator,
        ListUsersPaginator,
    )

    session = get_session()
    with session.create_client("rekognition") as client:
        client: RekognitionClient

        describe_project_versions_paginator: DescribeProjectVersionsPaginator = client.get_paginator("describe_project_versions")
        describe_projects_paginator: DescribeProjectsPaginator = client.get_paginator("describe_projects")
        list_collections_paginator: ListCollectionsPaginator = client.get_paginator("list_collections")
        list_dataset_entries_paginator: ListDatasetEntriesPaginator = client.get_paginator("list_dataset_entries")
        list_dataset_labels_paginator: ListDatasetLabelsPaginator = client.get_paginator("list_dataset_labels")
        list_faces_paginator: ListFacesPaginator = client.get_paginator("list_faces")
        list_project_policies_paginator: ListProjectPoliciesPaginator = client.get_paginator("list_project_policies")
        list_stream_processors_paginator: ListStreamProcessorsPaginator = client.get_paginator("list_stream_processors")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeProjectsRequestDescribeProjectsPaginateTypeDef,
    DescribeProjectsResponseTypeDef,
    DescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef,
    DescribeProjectVersionsResponseTypeDef,
    ListCollectionsRequestListCollectionsPaginateTypeDef,
    ListCollectionsResponseTypeDef,
    ListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef,
    ListDatasetEntriesResponseTypeDef,
    ListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef,
    ListDatasetLabelsResponseTypeDef,
    ListFacesRequestListFacesPaginateTypeDef,
    ListFacesResponseTypeDef,
    ListProjectPoliciesRequestListProjectPoliciesPaginateTypeDef,
    ListProjectPoliciesResponseTypeDef,
    ListStreamProcessorsRequestListStreamProcessorsPaginateTypeDef,
    ListStreamProcessorsResponseTypeDef,
    ListUsersRequestListUsersPaginateTypeDef,
    ListUsersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeProjectVersionsPaginator",
    "DescribeProjectsPaginator",
    "ListCollectionsPaginator",
    "ListDatasetEntriesPaginator",
    "ListDatasetLabelsPaginator",
    "ListFacesPaginator",
    "ListProjectPoliciesPaginator",
    "ListStreamProcessorsPaginator",
    "ListUsersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeProjectVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/DescribeProjectVersions.html#Rekognition.Paginator.DescribeProjectVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#describeprojectversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef]
    ) -> AsyncIterator[DescribeProjectVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/DescribeProjectVersions.html#Rekognition.Paginator.DescribeProjectVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#describeprojectversionspaginator)
        """

class DescribeProjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/DescribeProjects.html#Rekognition.Paginator.DescribeProjects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#describeprojectspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeProjectsRequestDescribeProjectsPaginateTypeDef]
    ) -> AsyncIterator[DescribeProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/DescribeProjects.html#Rekognition.Paginator.DescribeProjects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#describeprojectspaginator)
        """

class ListCollectionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListCollections.html#Rekognition.Paginator.ListCollections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listcollectionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCollectionsRequestListCollectionsPaginateTypeDef]
    ) -> AsyncIterator[ListCollectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListCollections.html#Rekognition.Paginator.ListCollections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listcollectionspaginator)
        """

class ListDatasetEntriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListDatasetEntries.html#Rekognition.Paginator.ListDatasetEntries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listdatasetentriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef]
    ) -> AsyncIterator[ListDatasetEntriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListDatasetEntries.html#Rekognition.Paginator.ListDatasetEntries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listdatasetentriespaginator)
        """

class ListDatasetLabelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListDatasetLabels.html#Rekognition.Paginator.ListDatasetLabels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listdatasetlabelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef]
    ) -> AsyncIterator[ListDatasetLabelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListDatasetLabels.html#Rekognition.Paginator.ListDatasetLabels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listdatasetlabelspaginator)
        """

class ListFacesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListFaces.html#Rekognition.Paginator.ListFaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listfacespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFacesRequestListFacesPaginateTypeDef]
    ) -> AsyncIterator[ListFacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListFaces.html#Rekognition.Paginator.ListFaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listfacespaginator)
        """

class ListProjectPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListProjectPolicies.html#Rekognition.Paginator.ListProjectPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listprojectpoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProjectPoliciesRequestListProjectPoliciesPaginateTypeDef]
    ) -> AsyncIterator[ListProjectPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListProjectPolicies.html#Rekognition.Paginator.ListProjectPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listprojectpoliciespaginator)
        """

class ListStreamProcessorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListStreamProcessors.html#Rekognition.Paginator.ListStreamProcessors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#liststreamprocessorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStreamProcessorsRequestListStreamProcessorsPaginateTypeDef]
    ) -> AsyncIterator[ListStreamProcessorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListStreamProcessors.html#Rekognition.Paginator.ListStreamProcessors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#liststreamprocessorspaginator)
        """

class ListUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListUsers.html#Rekognition.Paginator.ListUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listuserspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUsersRequestListUsersPaginateTypeDef]
    ) -> AsyncIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListUsers.html#Rekognition.Paginator.ListUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listuserspaginator)
        """
