"""
Type annotations for snowball service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_snowball.client import SnowballClient
    from types_aiobotocore_snowball.paginator import (
        DescribeAddressesPaginator,
        ListClusterJobsPaginator,
        ListClustersPaginator,
        ListCompatibleImagesPaginator,
        ListJobsPaginator,
        ListLongTermPricingPaginator,
    )

    session = get_session()
    with session.create_client("snowball") as client:
        client: SnowballClient

        describe_addresses_paginator: DescribeAddressesPaginator = client.get_paginator("describe_addresses")
        list_cluster_jobs_paginator: ListClusterJobsPaginator = client.get_paginator("list_cluster_jobs")
        list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
        list_compatible_images_paginator: ListCompatibleImagesPaginator = client.get_paginator("list_compatible_images")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_long_term_pricing_paginator: ListLongTermPricingPaginator = client.get_paginator("list_long_term_pricing")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeAddressesRequestDescribeAddressesPaginateTypeDef,
    DescribeAddressesResultTypeDef,
    ListClusterJobsRequestListClusterJobsPaginateTypeDef,
    ListClusterJobsResultTypeDef,
    ListClustersRequestListClustersPaginateTypeDef,
    ListClustersResultTypeDef,
    ListCompatibleImagesRequestListCompatibleImagesPaginateTypeDef,
    ListCompatibleImagesResultTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResultTypeDef,
    ListLongTermPricingRequestListLongTermPricingPaginateTypeDef,
    ListLongTermPricingResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeAddressesPaginator",
    "ListClusterJobsPaginator",
    "ListClustersPaginator",
    "ListCompatibleImagesPaginator",
    "ListJobsPaginator",
    "ListLongTermPricingPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeAddressesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/DescribeAddresses.html#Snowball.Paginator.DescribeAddresses)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#describeaddressespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeAddressesRequestDescribeAddressesPaginateTypeDef]
    ) -> AsyncIterator[DescribeAddressesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/DescribeAddresses.html#Snowball.Paginator.DescribeAddresses.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#describeaddressespaginator)
        """

class ListClusterJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListClusterJobs.html#Snowball.Paginator.ListClusterJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listclusterjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListClusterJobsRequestListClusterJobsPaginateTypeDef]
    ) -> AsyncIterator[ListClusterJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListClusterJobs.html#Snowball.Paginator.ListClusterJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listclusterjobspaginator)
        """

class ListClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListClusters.html#Snowball.Paginator.ListClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListClustersRequestListClustersPaginateTypeDef]
    ) -> AsyncIterator[ListClustersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListClusters.html#Snowball.Paginator.ListClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listclusterspaginator)
        """

class ListCompatibleImagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListCompatibleImages.html#Snowball.Paginator.ListCompatibleImages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listcompatibleimagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCompatibleImagesRequestListCompatibleImagesPaginateTypeDef]
    ) -> AsyncIterator[ListCompatibleImagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListCompatibleImages.html#Snowball.Paginator.ListCompatibleImages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listcompatibleimagespaginator)
        """

class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListJobs.html#Snowball.Paginator.ListJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> AsyncIterator[ListJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListJobs.html#Snowball.Paginator.ListJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listjobspaginator)
        """

class ListLongTermPricingPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListLongTermPricing.html#Snowball.Paginator.ListLongTermPricing)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listlongtermpricingpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLongTermPricingRequestListLongTermPricingPaginateTypeDef]
    ) -> AsyncIterator[ListLongTermPricingResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListLongTermPricing.html#Snowball.Paginator.ListLongTermPricing.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listlongtermpricingpaginator)
        """
