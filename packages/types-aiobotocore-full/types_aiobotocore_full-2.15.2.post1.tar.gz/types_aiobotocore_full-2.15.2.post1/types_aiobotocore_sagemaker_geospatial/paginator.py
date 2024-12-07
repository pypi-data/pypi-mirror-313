"""
Type annotations for sagemaker-geospatial service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sagemaker_geospatial.client import SageMakergeospatialcapabilitiesClient
    from types_aiobotocore_sagemaker_geospatial.paginator import (
        ListEarthObservationJobsPaginator,
        ListRasterDataCollectionsPaginator,
        ListVectorEnrichmentJobsPaginator,
    )

    session = get_session()
    with session.create_client("sagemaker-geospatial") as client:
        client: SageMakergeospatialcapabilitiesClient

        list_earth_observation_jobs_paginator: ListEarthObservationJobsPaginator = client.get_paginator("list_earth_observation_jobs")
        list_raster_data_collections_paginator: ListRasterDataCollectionsPaginator = client.get_paginator("list_raster_data_collections")
        list_vector_enrichment_jobs_paginator: ListVectorEnrichmentJobsPaginator = client.get_paginator("list_vector_enrichment_jobs")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListEarthObservationJobInputListEarthObservationJobsPaginateTypeDef,
    ListEarthObservationJobOutputTypeDef,
    ListRasterDataCollectionsInputListRasterDataCollectionsPaginateTypeDef,
    ListRasterDataCollectionsOutputTypeDef,
    ListVectorEnrichmentJobInputListVectorEnrichmentJobsPaginateTypeDef,
    ListVectorEnrichmentJobOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListEarthObservationJobsPaginator",
    "ListRasterDataCollectionsPaginator",
    "ListVectorEnrichmentJobsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListEarthObservationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/paginator/ListEarthObservationJobs.html#SageMakergeospatialcapabilities.Paginator.ListEarthObservationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/paginators/#listearthobservationjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEarthObservationJobInputListEarthObservationJobsPaginateTypeDef]
    ) -> AsyncIterator[ListEarthObservationJobOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/paginator/ListEarthObservationJobs.html#SageMakergeospatialcapabilities.Paginator.ListEarthObservationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/paginators/#listearthobservationjobspaginator)
        """


class ListRasterDataCollectionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/paginator/ListRasterDataCollections.html#SageMakergeospatialcapabilities.Paginator.ListRasterDataCollections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/paginators/#listrasterdatacollectionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListRasterDataCollectionsInputListRasterDataCollectionsPaginateTypeDef],
    ) -> AsyncIterator[ListRasterDataCollectionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/paginator/ListRasterDataCollections.html#SageMakergeospatialcapabilities.Paginator.ListRasterDataCollections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/paginators/#listrasterdatacollectionspaginator)
        """


class ListVectorEnrichmentJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/paginator/ListVectorEnrichmentJobs.html#SageMakergeospatialcapabilities.Paginator.ListVectorEnrichmentJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/paginators/#listvectorenrichmentjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListVectorEnrichmentJobInputListVectorEnrichmentJobsPaginateTypeDef]
    ) -> AsyncIterator[ListVectorEnrichmentJobOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/paginator/ListVectorEnrichmentJobs.html#SageMakergeospatialcapabilities.Paginator.ListVectorEnrichmentJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/paginators/#listvectorenrichmentjobspaginator)
        """
