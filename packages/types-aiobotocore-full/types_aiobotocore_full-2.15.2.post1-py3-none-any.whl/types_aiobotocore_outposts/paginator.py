"""
Type annotations for outposts service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_outposts.client import OutpostsClient
    from types_aiobotocore_outposts.paginator import (
        GetOutpostInstanceTypesPaginator,
        GetOutpostSupportedInstanceTypesPaginator,
        ListAssetsPaginator,
        ListCapacityTasksPaginator,
        ListCatalogItemsPaginator,
        ListOrdersPaginator,
        ListOutpostsPaginator,
        ListSitesPaginator,
    )

    session = get_session()
    with session.create_client("outposts") as client:
        client: OutpostsClient

        get_outpost_instance_types_paginator: GetOutpostInstanceTypesPaginator = client.get_paginator("get_outpost_instance_types")
        get_outpost_supported_instance_types_paginator: GetOutpostSupportedInstanceTypesPaginator = client.get_paginator("get_outpost_supported_instance_types")
        list_assets_paginator: ListAssetsPaginator = client.get_paginator("list_assets")
        list_capacity_tasks_paginator: ListCapacityTasksPaginator = client.get_paginator("list_capacity_tasks")
        list_catalog_items_paginator: ListCatalogItemsPaginator = client.get_paginator("list_catalog_items")
        list_orders_paginator: ListOrdersPaginator = client.get_paginator("list_orders")
        list_outposts_paginator: ListOutpostsPaginator = client.get_paginator("list_outposts")
        list_sites_paginator: ListSitesPaginator = client.get_paginator("list_sites")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetOutpostInstanceTypesInputGetOutpostInstanceTypesPaginateTypeDef,
    GetOutpostInstanceTypesOutputTypeDef,
    GetOutpostSupportedInstanceTypesInputGetOutpostSupportedInstanceTypesPaginateTypeDef,
    GetOutpostSupportedInstanceTypesOutputTypeDef,
    ListAssetsInputListAssetsPaginateTypeDef,
    ListAssetsOutputTypeDef,
    ListCapacityTasksInputListCapacityTasksPaginateTypeDef,
    ListCapacityTasksOutputTypeDef,
    ListCatalogItemsInputListCatalogItemsPaginateTypeDef,
    ListCatalogItemsOutputTypeDef,
    ListOrdersInputListOrdersPaginateTypeDef,
    ListOrdersOutputTypeDef,
    ListOutpostsInputListOutpostsPaginateTypeDef,
    ListOutpostsOutputTypeDef,
    ListSitesInputListSitesPaginateTypeDef,
    ListSitesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetOutpostInstanceTypesPaginator",
    "GetOutpostSupportedInstanceTypesPaginator",
    "ListAssetsPaginator",
    "ListCapacityTasksPaginator",
    "ListCatalogItemsPaginator",
    "ListOrdersPaginator",
    "ListOutpostsPaginator",
    "ListSitesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetOutpostInstanceTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/GetOutpostInstanceTypes.html#Outposts.Paginator.GetOutpostInstanceTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#getoutpostinstancetypespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetOutpostInstanceTypesInputGetOutpostInstanceTypesPaginateTypeDef]
    ) -> AsyncIterator[GetOutpostInstanceTypesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/GetOutpostInstanceTypes.html#Outposts.Paginator.GetOutpostInstanceTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#getoutpostinstancetypespaginator)
        """


class GetOutpostSupportedInstanceTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/GetOutpostSupportedInstanceTypes.html#Outposts.Paginator.GetOutpostSupportedInstanceTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#getoutpostsupportedinstancetypespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetOutpostSupportedInstanceTypesInputGetOutpostSupportedInstanceTypesPaginateTypeDef
        ],
    ) -> AsyncIterator[GetOutpostSupportedInstanceTypesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/GetOutpostSupportedInstanceTypes.html#Outposts.Paginator.GetOutpostSupportedInstanceTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#getoutpostsupportedinstancetypespaginator)
        """


class ListAssetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListAssets.html#Outposts.Paginator.ListAssets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listassetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAssetsInputListAssetsPaginateTypeDef]
    ) -> AsyncIterator[ListAssetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListAssets.html#Outposts.Paginator.ListAssets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listassetspaginator)
        """


class ListCapacityTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListCapacityTasks.html#Outposts.Paginator.ListCapacityTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listcapacitytaskspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCapacityTasksInputListCapacityTasksPaginateTypeDef]
    ) -> AsyncIterator[ListCapacityTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListCapacityTasks.html#Outposts.Paginator.ListCapacityTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listcapacitytaskspaginator)
        """


class ListCatalogItemsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListCatalogItems.html#Outposts.Paginator.ListCatalogItems)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listcatalogitemspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCatalogItemsInputListCatalogItemsPaginateTypeDef]
    ) -> AsyncIterator[ListCatalogItemsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListCatalogItems.html#Outposts.Paginator.ListCatalogItems.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listcatalogitemspaginator)
        """


class ListOrdersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListOrders.html#Outposts.Paginator.ListOrders)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listorderspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOrdersInputListOrdersPaginateTypeDef]
    ) -> AsyncIterator[ListOrdersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListOrders.html#Outposts.Paginator.ListOrders.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listorderspaginator)
        """


class ListOutpostsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListOutposts.html#Outposts.Paginator.ListOutposts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listoutpostspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOutpostsInputListOutpostsPaginateTypeDef]
    ) -> AsyncIterator[ListOutpostsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListOutposts.html#Outposts.Paginator.ListOutposts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listoutpostspaginator)
        """


class ListSitesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListSites.html#Outposts.Paginator.ListSites)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listsitespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSitesInputListSitesPaginateTypeDef]
    ) -> AsyncIterator[ListSitesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListSites.html#Outposts.Paginator.ListSites.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listsitespaginator)
        """
