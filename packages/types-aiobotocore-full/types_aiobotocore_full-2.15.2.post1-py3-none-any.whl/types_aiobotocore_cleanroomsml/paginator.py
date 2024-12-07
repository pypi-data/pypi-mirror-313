"""
Type annotations for cleanroomsml service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cleanroomsml.client import CleanRoomsMLClient
    from types_aiobotocore_cleanroomsml.paginator import (
        ListAudienceExportJobsPaginator,
        ListAudienceGenerationJobsPaginator,
        ListAudienceModelsPaginator,
        ListConfiguredAudienceModelsPaginator,
        ListTrainingDatasetsPaginator,
    )

    session = get_session()
    with session.create_client("cleanroomsml") as client:
        client: CleanRoomsMLClient

        list_audience_export_jobs_paginator: ListAudienceExportJobsPaginator = client.get_paginator("list_audience_export_jobs")
        list_audience_generation_jobs_paginator: ListAudienceGenerationJobsPaginator = client.get_paginator("list_audience_generation_jobs")
        list_audience_models_paginator: ListAudienceModelsPaginator = client.get_paginator("list_audience_models")
        list_configured_audience_models_paginator: ListConfiguredAudienceModelsPaginator = client.get_paginator("list_configured_audience_models")
        list_training_datasets_paginator: ListTrainingDatasetsPaginator = client.get_paginator("list_training_datasets")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAudienceExportJobsRequestListAudienceExportJobsPaginateTypeDef,
    ListAudienceExportJobsResponseTypeDef,
    ListAudienceGenerationJobsRequestListAudienceGenerationJobsPaginateTypeDef,
    ListAudienceGenerationJobsResponseTypeDef,
    ListAudienceModelsRequestListAudienceModelsPaginateTypeDef,
    ListAudienceModelsResponseTypeDef,
    ListConfiguredAudienceModelsRequestListConfiguredAudienceModelsPaginateTypeDef,
    ListConfiguredAudienceModelsResponseTypeDef,
    ListTrainingDatasetsRequestListTrainingDatasetsPaginateTypeDef,
    ListTrainingDatasetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAudienceExportJobsPaginator",
    "ListAudienceGenerationJobsPaginator",
    "ListAudienceModelsPaginator",
    "ListConfiguredAudienceModelsPaginator",
    "ListTrainingDatasetsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAudienceExportJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceExportJobs.html#CleanRoomsML.Paginator.ListAudienceExportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listaudienceexportjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAudienceExportJobsRequestListAudienceExportJobsPaginateTypeDef]
    ) -> AsyncIterator[ListAudienceExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceExportJobs.html#CleanRoomsML.Paginator.ListAudienceExportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listaudienceexportjobspaginator)
        """


class ListAudienceGenerationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceGenerationJobs.html#CleanRoomsML.Paginator.ListAudienceGenerationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listaudiencegenerationjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListAudienceGenerationJobsRequestListAudienceGenerationJobsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListAudienceGenerationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceGenerationJobs.html#CleanRoomsML.Paginator.ListAudienceGenerationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listaudiencegenerationjobspaginator)
        """


class ListAudienceModelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceModels.html#CleanRoomsML.Paginator.ListAudienceModels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listaudiencemodelspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAudienceModelsRequestListAudienceModelsPaginateTypeDef]
    ) -> AsyncIterator[ListAudienceModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceModels.html#CleanRoomsML.Paginator.ListAudienceModels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listaudiencemodelspaginator)
        """


class ListConfiguredAudienceModelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListConfiguredAudienceModels.html#CleanRoomsML.Paginator.ListConfiguredAudienceModels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listconfiguredaudiencemodelspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListConfiguredAudienceModelsRequestListConfiguredAudienceModelsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListConfiguredAudienceModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListConfiguredAudienceModels.html#CleanRoomsML.Paginator.ListConfiguredAudienceModels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listconfiguredaudiencemodelspaginator)
        """


class ListTrainingDatasetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListTrainingDatasets.html#CleanRoomsML.Paginator.ListTrainingDatasets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listtrainingdatasetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTrainingDatasetsRequestListTrainingDatasetsPaginateTypeDef]
    ) -> AsyncIterator[ListTrainingDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListTrainingDatasets.html#CleanRoomsML.Paginator.ListTrainingDatasets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listtrainingdatasetspaginator)
        """
