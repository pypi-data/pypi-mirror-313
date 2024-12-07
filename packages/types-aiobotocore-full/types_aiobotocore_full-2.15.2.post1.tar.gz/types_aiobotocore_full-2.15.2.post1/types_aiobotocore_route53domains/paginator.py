"""
Type annotations for route53domains service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_route53domains.client import Route53DomainsClient
    from types_aiobotocore_route53domains.paginator import (
        ListDomainsPaginator,
        ListOperationsPaginator,
        ListPricesPaginator,
        ViewBillingPaginator,
    )

    session = get_session()
    with session.create_client("route53domains") as client:
        client: Route53DomainsClient

        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_operations_paginator: ListOperationsPaginator = client.get_paginator("list_operations")
        list_prices_paginator: ListPricesPaginator = client.get_paginator("list_prices")
        view_billing_paginator: ViewBillingPaginator = client.get_paginator("view_billing")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListDomainsRequestListDomainsPaginateTypeDef,
    ListDomainsResponseTypeDef,
    ListOperationsRequestListOperationsPaginateTypeDef,
    ListOperationsResponseTypeDef,
    ListPricesRequestListPricesPaginateTypeDef,
    ListPricesResponseTypeDef,
    ViewBillingRequestViewBillingPaginateTypeDef,
    ViewBillingResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListDomainsPaginator",
    "ListOperationsPaginator",
    "ListPricesPaginator",
    "ViewBillingPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDomainsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/paginator/ListDomains.html#Route53Domains.Paginator.ListDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/#listdomainspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDomainsRequestListDomainsPaginateTypeDef]
    ) -> AsyncIterator[ListDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/paginator/ListDomains.html#Route53Domains.Paginator.ListDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/#listdomainspaginator)
        """


class ListOperationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/paginator/ListOperations.html#Route53Domains.Paginator.ListOperations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/#listoperationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOperationsRequestListOperationsPaginateTypeDef]
    ) -> AsyncIterator[ListOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/paginator/ListOperations.html#Route53Domains.Paginator.ListOperations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/#listoperationspaginator)
        """


class ListPricesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/paginator/ListPrices.html#Route53Domains.Paginator.ListPrices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/#listpricespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPricesRequestListPricesPaginateTypeDef]
    ) -> AsyncIterator[ListPricesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/paginator/ListPrices.html#Route53Domains.Paginator.ListPrices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/#listpricespaginator)
        """


class ViewBillingPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/paginator/ViewBilling.html#Route53Domains.Paginator.ViewBilling)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/#viewbillingpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ViewBillingRequestViewBillingPaginateTypeDef]
    ) -> AsyncIterator[ViewBillingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/paginator/ViewBilling.html#Route53Domains.Paginator.ViewBilling.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/#viewbillingpaginator)
        """
