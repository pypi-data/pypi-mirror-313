"""
Type annotations for iot1click-projects service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_projects/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iot1click_projects.client import IoT1ClickProjectsClient
    from types_aiobotocore_iot1click_projects.paginator import (
        ListPlacementsPaginator,
        ListProjectsPaginator,
    )

    session = get_session()
    with session.create_client("iot1click-projects") as client:
        client: IoT1ClickProjectsClient

        list_placements_paginator: ListPlacementsPaginator = client.get_paginator("list_placements")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListPlacementsRequestListPlacementsPaginateTypeDef,
    ListPlacementsResponseTypeDef,
    ListProjectsRequestListProjectsPaginateTypeDef,
    ListProjectsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListPlacementsPaginator", "ListProjectsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListPlacementsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/paginator/ListPlacements.html#IoT1ClickProjects.Paginator.ListPlacements)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_projects/paginators/#listplacementspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPlacementsRequestListPlacementsPaginateTypeDef]
    ) -> AsyncIterator[ListPlacementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/paginator/ListPlacements.html#IoT1ClickProjects.Paginator.ListPlacements.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_projects/paginators/#listplacementspaginator)
        """

class ListProjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/paginator/ListProjects.html#IoT1ClickProjects.Paginator.ListProjects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_projects/paginators/#listprojectspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProjectsRequestListProjectsPaginateTypeDef]
    ) -> AsyncIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/paginator/ListProjects.html#IoT1ClickProjects.Paginator.ListProjects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_projects/paginators/#listprojectspaginator)
        """
