"""
Type annotations for es service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_es.client import ElasticsearchServiceClient
    from types_aiobotocore_es.paginator import (
        DescribeReservedElasticsearchInstanceOfferingsPaginator,
        DescribeReservedElasticsearchInstancesPaginator,
        GetUpgradeHistoryPaginator,
        ListElasticsearchInstanceTypesPaginator,
        ListElasticsearchVersionsPaginator,
    )

    session = get_session()
    with session.create_client("es") as client:
        client: ElasticsearchServiceClient

        describe_reserved_elasticsearch_instance_offerings_paginator: DescribeReservedElasticsearchInstanceOfferingsPaginator = client.get_paginator("describe_reserved_elasticsearch_instance_offerings")
        describe_reserved_elasticsearch_instances_paginator: DescribeReservedElasticsearchInstancesPaginator = client.get_paginator("describe_reserved_elasticsearch_instances")
        get_upgrade_history_paginator: GetUpgradeHistoryPaginator = client.get_paginator("get_upgrade_history")
        list_elasticsearch_instance_types_paginator: ListElasticsearchInstanceTypesPaginator = client.get_paginator("list_elasticsearch_instance_types")
        list_elasticsearch_versions_paginator: ListElasticsearchVersionsPaginator = client.get_paginator("list_elasticsearch_versions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeReservedElasticsearchInstanceOfferingsRequestDescribeReservedElasticsearchInstanceOfferingsPaginateTypeDef,
    DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef,
    DescribeReservedElasticsearchInstancesRequestDescribeReservedElasticsearchInstancesPaginateTypeDef,
    DescribeReservedElasticsearchInstancesResponseTypeDef,
    GetUpgradeHistoryRequestGetUpgradeHistoryPaginateTypeDef,
    GetUpgradeHistoryResponseTypeDef,
    ListElasticsearchInstanceTypesRequestListElasticsearchInstanceTypesPaginateTypeDef,
    ListElasticsearchInstanceTypesResponseTypeDef,
    ListElasticsearchVersionsRequestListElasticsearchVersionsPaginateTypeDef,
    ListElasticsearchVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeReservedElasticsearchInstanceOfferingsPaginator",
    "DescribeReservedElasticsearchInstancesPaginator",
    "GetUpgradeHistoryPaginator",
    "ListElasticsearchInstanceTypesPaginator",
    "ListElasticsearchVersionsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeReservedElasticsearchInstanceOfferingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/DescribeReservedElasticsearchInstanceOfferings.html#ElasticsearchService.Paginator.DescribeReservedElasticsearchInstanceOfferings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators/#describereservedelasticsearchinstanceofferingspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReservedElasticsearchInstanceOfferingsRequestDescribeReservedElasticsearchInstanceOfferingsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/DescribeReservedElasticsearchInstanceOfferings.html#ElasticsearchService.Paginator.DescribeReservedElasticsearchInstanceOfferings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators/#describereservedelasticsearchinstanceofferingspaginator)
        """

class DescribeReservedElasticsearchInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/DescribeReservedElasticsearchInstances.html#ElasticsearchService.Paginator.DescribeReservedElasticsearchInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators/#describereservedelasticsearchinstancespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReservedElasticsearchInstancesRequestDescribeReservedElasticsearchInstancesPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeReservedElasticsearchInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/DescribeReservedElasticsearchInstances.html#ElasticsearchService.Paginator.DescribeReservedElasticsearchInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators/#describereservedelasticsearchinstancespaginator)
        """

class GetUpgradeHistoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/GetUpgradeHistory.html#ElasticsearchService.Paginator.GetUpgradeHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators/#getupgradehistorypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetUpgradeHistoryRequestGetUpgradeHistoryPaginateTypeDef]
    ) -> AsyncIterator[GetUpgradeHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/GetUpgradeHistory.html#ElasticsearchService.Paginator.GetUpgradeHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators/#getupgradehistorypaginator)
        """

class ListElasticsearchInstanceTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/ListElasticsearchInstanceTypes.html#ElasticsearchService.Paginator.ListElasticsearchInstanceTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators/#listelasticsearchinstancetypespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListElasticsearchInstanceTypesRequestListElasticsearchInstanceTypesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListElasticsearchInstanceTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/ListElasticsearchInstanceTypes.html#ElasticsearchService.Paginator.ListElasticsearchInstanceTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators/#listelasticsearchinstancetypespaginator)
        """

class ListElasticsearchVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/ListElasticsearchVersions.html#ElasticsearchService.Paginator.ListElasticsearchVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators/#listelasticsearchversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListElasticsearchVersionsRequestListElasticsearchVersionsPaginateTypeDef],
    ) -> AsyncIterator[ListElasticsearchVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/paginator/ListElasticsearchVersions.html#ElasticsearchService.Paginator.ListElasticsearchVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators/#listelasticsearchversionspaginator)
        """
