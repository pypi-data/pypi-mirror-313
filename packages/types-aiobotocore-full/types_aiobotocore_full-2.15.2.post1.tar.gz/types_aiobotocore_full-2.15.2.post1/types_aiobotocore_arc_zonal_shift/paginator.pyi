"""
Type annotations for arc-zonal-shift service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_arc_zonal_shift.client import ARCZonalShiftClient
    from types_aiobotocore_arc_zonal_shift.paginator import (
        ListAutoshiftsPaginator,
        ListManagedResourcesPaginator,
        ListZonalShiftsPaginator,
    )

    session = get_session()
    with session.create_client("arc-zonal-shift") as client:
        client: ARCZonalShiftClient

        list_autoshifts_paginator: ListAutoshiftsPaginator = client.get_paginator("list_autoshifts")
        list_managed_resources_paginator: ListManagedResourcesPaginator = client.get_paginator("list_managed_resources")
        list_zonal_shifts_paginator: ListZonalShiftsPaginator = client.get_paginator("list_zonal_shifts")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAutoshiftsRequestListAutoshiftsPaginateTypeDef,
    ListAutoshiftsResponseTypeDef,
    ListManagedResourcesRequestListManagedResourcesPaginateTypeDef,
    ListManagedResourcesResponseTypeDef,
    ListZonalShiftsRequestListZonalShiftsPaginateTypeDef,
    ListZonalShiftsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListAutoshiftsPaginator", "ListManagedResourcesPaginator", "ListZonalShiftsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAutoshiftsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListAutoshifts.html#ARCZonalShift.Paginator.ListAutoshifts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/paginators/#listautoshiftspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAutoshiftsRequestListAutoshiftsPaginateTypeDef]
    ) -> AsyncIterator[ListAutoshiftsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListAutoshifts.html#ARCZonalShift.Paginator.ListAutoshifts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/paginators/#listautoshiftspaginator)
        """

class ListManagedResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListManagedResources.html#ARCZonalShift.Paginator.ListManagedResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/paginators/#listmanagedresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListManagedResourcesRequestListManagedResourcesPaginateTypeDef]
    ) -> AsyncIterator[ListManagedResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListManagedResources.html#ARCZonalShift.Paginator.ListManagedResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/paginators/#listmanagedresourcespaginator)
        """

class ListZonalShiftsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListZonalShifts.html#ARCZonalShift.Paginator.ListZonalShifts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/paginators/#listzonalshiftspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListZonalShiftsRequestListZonalShiftsPaginateTypeDef]
    ) -> AsyncIterator[ListZonalShiftsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListZonalShifts.html#ARCZonalShift.Paginator.ListZonalShifts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/paginators/#listzonalshiftspaginator)
        """
