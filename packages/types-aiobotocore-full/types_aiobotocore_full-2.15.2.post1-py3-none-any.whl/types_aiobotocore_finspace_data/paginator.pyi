"""
Type annotations for finspace-data service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_finspace_data.client import FinSpaceDataClient
    from types_aiobotocore_finspace_data.paginator import (
        ListChangesetsPaginator,
        ListDataViewsPaginator,
        ListDatasetsPaginator,
        ListPermissionGroupsPaginator,
        ListUsersPaginator,
    )

    session = get_session()
    with session.create_client("finspace-data") as client:
        client: FinSpaceDataClient

        list_changesets_paginator: ListChangesetsPaginator = client.get_paginator("list_changesets")
        list_data_views_paginator: ListDataViewsPaginator = client.get_paginator("list_data_views")
        list_datasets_paginator: ListDatasetsPaginator = client.get_paginator("list_datasets")
        list_permission_groups_paginator: ListPermissionGroupsPaginator = client.get_paginator("list_permission_groups")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListChangesetsRequestListChangesetsPaginateTypeDef,
    ListChangesetsResponseTypeDef,
    ListDatasetsRequestListDatasetsPaginateTypeDef,
    ListDatasetsResponseTypeDef,
    ListDataViewsRequestListDataViewsPaginateTypeDef,
    ListDataViewsResponseTypeDef,
    ListPermissionGroupsRequestListPermissionGroupsPaginateTypeDef,
    ListPermissionGroupsResponseTypeDef,
    ListUsersRequestListUsersPaginateTypeDef,
    ListUsersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListChangesetsPaginator",
    "ListDataViewsPaginator",
    "ListDatasetsPaginator",
    "ListPermissionGroupsPaginator",
    "ListUsersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListChangesetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListChangesets.html#FinSpaceData.Paginator.ListChangesets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listchangesetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListChangesetsRequestListChangesetsPaginateTypeDef]
    ) -> AsyncIterator[ListChangesetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListChangesets.html#FinSpaceData.Paginator.ListChangesets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listchangesetspaginator)
        """

class ListDataViewsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListDataViews.html#FinSpaceData.Paginator.ListDataViews)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listdataviewspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataViewsRequestListDataViewsPaginateTypeDef]
    ) -> AsyncIterator[ListDataViewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListDataViews.html#FinSpaceData.Paginator.ListDataViews.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listdataviewspaginator)
        """

class ListDatasetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListDatasets.html#FinSpaceData.Paginator.ListDatasets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listdatasetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDatasetsRequestListDatasetsPaginateTypeDef]
    ) -> AsyncIterator[ListDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListDatasets.html#FinSpaceData.Paginator.ListDatasets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listdatasetspaginator)
        """

class ListPermissionGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListPermissionGroups.html#FinSpaceData.Paginator.ListPermissionGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listpermissiongroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPermissionGroupsRequestListPermissionGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListPermissionGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListPermissionGroups.html#FinSpaceData.Paginator.ListPermissionGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listpermissiongroupspaginator)
        """

class ListUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListUsers.html#FinSpaceData.Paginator.ListUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listuserspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUsersRequestListUsersPaginateTypeDef]
    ) -> AsyncIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListUsers.html#FinSpaceData.Paginator.ListUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listuserspaginator)
        """
