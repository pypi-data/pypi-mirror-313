"""
Type annotations for lookoutvision service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lookoutvision.client import LookoutforVisionClient
    from types_aiobotocore_lookoutvision.paginator import (
        ListDatasetEntriesPaginator,
        ListModelPackagingJobsPaginator,
        ListModelsPaginator,
        ListProjectsPaginator,
    )

    session = get_session()
    with session.create_client("lookoutvision") as client:
        client: LookoutforVisionClient

        list_dataset_entries_paginator: ListDatasetEntriesPaginator = client.get_paginator("list_dataset_entries")
        list_model_packaging_jobs_paginator: ListModelPackagingJobsPaginator = client.get_paginator("list_model_packaging_jobs")
        list_models_paginator: ListModelsPaginator = client.get_paginator("list_models")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef,
    ListDatasetEntriesResponseTypeDef,
    ListModelPackagingJobsRequestListModelPackagingJobsPaginateTypeDef,
    ListModelPackagingJobsResponseTypeDef,
    ListModelsRequestListModelsPaginateTypeDef,
    ListModelsResponseTypeDef,
    ListProjectsRequestListProjectsPaginateTypeDef,
    ListProjectsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListDatasetEntriesPaginator",
    "ListModelPackagingJobsPaginator",
    "ListModelsPaginator",
    "ListProjectsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDatasetEntriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListDatasetEntries.html#LookoutforVision.Paginator.ListDatasetEntries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/#listdatasetentriespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef]
    ) -> AsyncIterator[ListDatasetEntriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListDatasetEntries.html#LookoutforVision.Paginator.ListDatasetEntries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/#listdatasetentriespaginator)
        """


class ListModelPackagingJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListModelPackagingJobs.html#LookoutforVision.Paginator.ListModelPackagingJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/#listmodelpackagingjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListModelPackagingJobsRequestListModelPackagingJobsPaginateTypeDef]
    ) -> AsyncIterator[ListModelPackagingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListModelPackagingJobs.html#LookoutforVision.Paginator.ListModelPackagingJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/#listmodelpackagingjobspaginator)
        """


class ListModelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListModels.html#LookoutforVision.Paginator.ListModels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/#listmodelspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListModelsRequestListModelsPaginateTypeDef]
    ) -> AsyncIterator[ListModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListModels.html#LookoutforVision.Paginator.ListModels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/#listmodelspaginator)
        """


class ListProjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListProjects.html#LookoutforVision.Paginator.ListProjects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/#listprojectspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListProjectsRequestListProjectsPaginateTypeDef]
    ) -> AsyncIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListProjects.html#LookoutforVision.Paginator.ListProjects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/#listprojectspaginator)
        """
