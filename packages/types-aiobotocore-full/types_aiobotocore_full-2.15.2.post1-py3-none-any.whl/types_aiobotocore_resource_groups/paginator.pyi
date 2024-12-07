"""
Type annotations for resource-groups service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_resource_groups.client import ResourceGroupsClient
    from types_aiobotocore_resource_groups.paginator import (
        ListGroupResourcesPaginator,
        ListGroupingStatusesPaginator,
        ListGroupsPaginator,
        ListTagSyncTasksPaginator,
        SearchResourcesPaginator,
    )

    session = get_session()
    with session.create_client("resource-groups") as client:
        client: ResourceGroupsClient

        list_group_resources_paginator: ListGroupResourcesPaginator = client.get_paginator("list_group_resources")
        list_grouping_statuses_paginator: ListGroupingStatusesPaginator = client.get_paginator("list_grouping_statuses")
        list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
        list_tag_sync_tasks_paginator: ListTagSyncTasksPaginator = client.get_paginator("list_tag_sync_tasks")
        search_resources_paginator: SearchResourcesPaginator = client.get_paginator("search_resources")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListGroupingStatusesInputListGroupingStatusesPaginateTypeDef,
    ListGroupingStatusesOutputTypeDef,
    ListGroupResourcesInputListGroupResourcesPaginateTypeDef,
    ListGroupResourcesOutputTypeDef,
    ListGroupsInputListGroupsPaginateTypeDef,
    ListGroupsOutputTypeDef,
    ListTagSyncTasksInputListTagSyncTasksPaginateTypeDef,
    ListTagSyncTasksOutputTypeDef,
    SearchResourcesInputSearchResourcesPaginateTypeDef,
    SearchResourcesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListGroupResourcesPaginator",
    "ListGroupingStatusesPaginator",
    "ListGroupsPaginator",
    "ListTagSyncTasksPaginator",
    "SearchResourcesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListGroupResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/paginator/ListGroupResources.html#ResourceGroups.Paginator.ListGroupResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/#listgroupresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGroupResourcesInputListGroupResourcesPaginateTypeDef]
    ) -> AsyncIterator[ListGroupResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/paginator/ListGroupResources.html#ResourceGroups.Paginator.ListGroupResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/#listgroupresourcespaginator)
        """

class ListGroupingStatusesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/paginator/ListGroupingStatuses.html#ResourceGroups.Paginator.ListGroupingStatuses)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/#listgroupingstatusespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGroupingStatusesInputListGroupingStatusesPaginateTypeDef]
    ) -> AsyncIterator[ListGroupingStatusesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/paginator/ListGroupingStatuses.html#ResourceGroups.Paginator.ListGroupingStatuses.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/#listgroupingstatusespaginator)
        """

class ListGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/paginator/ListGroups.html#ResourceGroups.Paginator.ListGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/#listgroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGroupsInputListGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/paginator/ListGroups.html#ResourceGroups.Paginator.ListGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/#listgroupspaginator)
        """

class ListTagSyncTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/paginator/ListTagSyncTasks.html#ResourceGroups.Paginator.ListTagSyncTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/#listtagsynctaskspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagSyncTasksInputListTagSyncTasksPaginateTypeDef]
    ) -> AsyncIterator[ListTagSyncTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/paginator/ListTagSyncTasks.html#ResourceGroups.Paginator.ListTagSyncTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/#listtagsynctaskspaginator)
        """

class SearchResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/paginator/SearchResources.html#ResourceGroups.Paginator.SearchResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/#searchresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchResourcesInputSearchResourcesPaginateTypeDef]
    ) -> AsyncIterator[SearchResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/paginator/SearchResources.html#ResourceGroups.Paginator.SearchResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/#searchresourcespaginator)
        """
