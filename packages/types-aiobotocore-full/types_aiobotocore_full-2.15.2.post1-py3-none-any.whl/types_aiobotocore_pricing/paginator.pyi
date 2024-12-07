"""
Type annotations for pricing service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_pricing.client import PricingClient
    from types_aiobotocore_pricing.paginator import (
        DescribeServicesPaginator,
        GetAttributeValuesPaginator,
        GetProductsPaginator,
        ListPriceListsPaginator,
    )

    session = get_session()
    with session.create_client("pricing") as client:
        client: PricingClient

        describe_services_paginator: DescribeServicesPaginator = client.get_paginator("describe_services")
        get_attribute_values_paginator: GetAttributeValuesPaginator = client.get_paginator("get_attribute_values")
        get_products_paginator: GetProductsPaginator = client.get_paginator("get_products")
        list_price_lists_paginator: ListPriceListsPaginator = client.get_paginator("list_price_lists")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeServicesRequestDescribeServicesPaginateTypeDef,
    DescribeServicesResponseTypeDef,
    GetAttributeValuesRequestGetAttributeValuesPaginateTypeDef,
    GetAttributeValuesResponseTypeDef,
    GetProductsRequestGetProductsPaginateTypeDef,
    GetProductsResponseTypeDef,
    ListPriceListsRequestListPriceListsPaginateTypeDef,
    ListPriceListsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeServicesPaginator",
    "GetAttributeValuesPaginator",
    "GetProductsPaginator",
    "ListPriceListsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeServicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/DescribeServices.html#Pricing.Paginator.DescribeServices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#describeservicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeServicesRequestDescribeServicesPaginateTypeDef]
    ) -> AsyncIterator[DescribeServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/DescribeServices.html#Pricing.Paginator.DescribeServices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#describeservicespaginator)
        """

class GetAttributeValuesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/GetAttributeValues.html#Pricing.Paginator.GetAttributeValues)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#getattributevaluespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetAttributeValuesRequestGetAttributeValuesPaginateTypeDef]
    ) -> AsyncIterator[GetAttributeValuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/GetAttributeValues.html#Pricing.Paginator.GetAttributeValues.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#getattributevaluespaginator)
        """

class GetProductsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/GetProducts.html#Pricing.Paginator.GetProducts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#getproductspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetProductsRequestGetProductsPaginateTypeDef]
    ) -> AsyncIterator[GetProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/GetProducts.html#Pricing.Paginator.GetProducts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#getproductspaginator)
        """

class ListPriceListsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/ListPriceLists.html#Pricing.Paginator.ListPriceLists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#listpricelistspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPriceListsRequestListPriceListsPaginateTypeDef]
    ) -> AsyncIterator[ListPriceListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/ListPriceLists.html#Pricing.Paginator.ListPriceLists.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#listpricelistspaginator)
        """
