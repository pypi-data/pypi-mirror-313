"""
Type annotations for neptune-graph service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_neptune_graph.client import NeptuneGraphClient
    from types_aiobotocore_neptune_graph.paginator import (
        ListGraphSnapshotsPaginator,
        ListGraphsPaginator,
        ListImportTasksPaginator,
        ListPrivateGraphEndpointsPaginator,
    )

    session = get_session()
    with session.create_client("neptune-graph") as client:
        client: NeptuneGraphClient

        list_graph_snapshots_paginator: ListGraphSnapshotsPaginator = client.get_paginator("list_graph_snapshots")
        list_graphs_paginator: ListGraphsPaginator = client.get_paginator("list_graphs")
        list_import_tasks_paginator: ListImportTasksPaginator = client.get_paginator("list_import_tasks")
        list_private_graph_endpoints_paginator: ListPrivateGraphEndpointsPaginator = client.get_paginator("list_private_graph_endpoints")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListGraphsInputListGraphsPaginateTypeDef,
    ListGraphSnapshotsInputListGraphSnapshotsPaginateTypeDef,
    ListGraphSnapshotsOutputTypeDef,
    ListGraphsOutputTypeDef,
    ListImportTasksInputListImportTasksPaginateTypeDef,
    ListImportTasksOutputTypeDef,
    ListPrivateGraphEndpointsInputListPrivateGraphEndpointsPaginateTypeDef,
    ListPrivateGraphEndpointsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListGraphSnapshotsPaginator",
    "ListGraphsPaginator",
    "ListImportTasksPaginator",
    "ListPrivateGraphEndpointsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListGraphSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListGraphSnapshots.html#NeptuneGraph.Paginator.ListGraphSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listgraphsnapshotspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGraphSnapshotsInputListGraphSnapshotsPaginateTypeDef]
    ) -> AsyncIterator[ListGraphSnapshotsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListGraphSnapshots.html#NeptuneGraph.Paginator.ListGraphSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listgraphsnapshotspaginator)
        """

class ListGraphsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListGraphs.html#NeptuneGraph.Paginator.ListGraphs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listgraphspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGraphsInputListGraphsPaginateTypeDef]
    ) -> AsyncIterator[ListGraphsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListGraphs.html#NeptuneGraph.Paginator.ListGraphs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listgraphspaginator)
        """

class ListImportTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListImportTasks.html#NeptuneGraph.Paginator.ListImportTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listimporttaskspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListImportTasksInputListImportTasksPaginateTypeDef]
    ) -> AsyncIterator[ListImportTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListImportTasks.html#NeptuneGraph.Paginator.ListImportTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listimporttaskspaginator)
        """

class ListPrivateGraphEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListPrivateGraphEndpoints.html#NeptuneGraph.Paginator.ListPrivateGraphEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listprivategraphendpointspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListPrivateGraphEndpointsInputListPrivateGraphEndpointsPaginateTypeDef],
    ) -> AsyncIterator[ListPrivateGraphEndpointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListPrivateGraphEndpoints.html#NeptuneGraph.Paginator.ListPrivateGraphEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listprivategraphendpointspaginator)
        """
