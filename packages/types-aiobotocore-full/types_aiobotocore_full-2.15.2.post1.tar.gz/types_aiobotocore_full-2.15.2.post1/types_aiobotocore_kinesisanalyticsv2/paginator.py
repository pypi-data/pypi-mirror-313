"""
Type annotations for kinesisanalyticsv2 service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisanalyticsv2/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_kinesisanalyticsv2.client import KinesisAnalyticsV2Client
    from types_aiobotocore_kinesisanalyticsv2.paginator import (
        ListApplicationOperationsPaginator,
        ListApplicationSnapshotsPaginator,
        ListApplicationVersionsPaginator,
        ListApplicationsPaginator,
    )

    session = get_session()
    with session.create_client("kinesisanalyticsv2") as client:
        client: KinesisAnalyticsV2Client

        list_application_operations_paginator: ListApplicationOperationsPaginator = client.get_paginator("list_application_operations")
        list_application_snapshots_paginator: ListApplicationSnapshotsPaginator = client.get_paginator("list_application_snapshots")
        list_application_versions_paginator: ListApplicationVersionsPaginator = client.get_paginator("list_application_versions")
        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListApplicationOperationsRequestListApplicationOperationsPaginateTypeDef,
    ListApplicationOperationsResponseTypeDef,
    ListApplicationSnapshotsRequestListApplicationSnapshotsPaginateTypeDef,
    ListApplicationSnapshotsResponseTypeDef,
    ListApplicationsRequestListApplicationsPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef,
    ListApplicationVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListApplicationOperationsPaginator",
    "ListApplicationSnapshotsPaginator",
    "ListApplicationVersionsPaginator",
    "ListApplicationsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListApplicationOperationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/paginator/ListApplicationOperations.html#KinesisAnalyticsV2.Paginator.ListApplicationOperations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisanalyticsv2/paginators/#listapplicationoperationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListApplicationOperationsRequestListApplicationOperationsPaginateTypeDef],
    ) -> AsyncIterator[ListApplicationOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/paginator/ListApplicationOperations.html#KinesisAnalyticsV2.Paginator.ListApplicationOperations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisanalyticsv2/paginators/#listapplicationoperationspaginator)
        """


class ListApplicationSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/paginator/ListApplicationSnapshots.html#KinesisAnalyticsV2.Paginator.ListApplicationSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisanalyticsv2/paginators/#listapplicationsnapshotspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListApplicationSnapshotsRequestListApplicationSnapshotsPaginateTypeDef],
    ) -> AsyncIterator[ListApplicationSnapshotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/paginator/ListApplicationSnapshots.html#KinesisAnalyticsV2.Paginator.ListApplicationSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisanalyticsv2/paginators/#listapplicationsnapshotspaginator)
        """


class ListApplicationVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/paginator/ListApplicationVersions.html#KinesisAnalyticsV2.Paginator.ListApplicationVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisanalyticsv2/paginators/#listapplicationversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef]
    ) -> AsyncIterator[ListApplicationVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/paginator/ListApplicationVersions.html#KinesisAnalyticsV2.Paginator.ListApplicationVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisanalyticsv2/paginators/#listapplicationversionspaginator)
        """


class ListApplicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/paginator/ListApplications.html#KinesisAnalyticsV2.Paginator.ListApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisanalyticsv2/paginators/#listapplicationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListApplicationsRequestListApplicationsPaginateTypeDef]
    ) -> AsyncIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/paginator/ListApplications.html#KinesisAnalyticsV2.Paginator.ListApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisanalyticsv2/paginators/#listapplicationspaginator)
        """
