"""
Type annotations for braket service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_braket.client import BraketClient
    from types_aiobotocore_braket.paginator import (
        SearchDevicesPaginator,
        SearchJobsPaginator,
        SearchQuantumTasksPaginator,
    )

    session = get_session()
    with session.create_client("braket") as client:
        client: BraketClient

        search_devices_paginator: SearchDevicesPaginator = client.get_paginator("search_devices")
        search_jobs_paginator: SearchJobsPaginator = client.get_paginator("search_jobs")
        search_quantum_tasks_paginator: SearchQuantumTasksPaginator = client.get_paginator("search_quantum_tasks")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    SearchDevicesRequestSearchDevicesPaginateTypeDef,
    SearchDevicesResponseTypeDef,
    SearchJobsRequestSearchJobsPaginateTypeDef,
    SearchJobsResponseTypeDef,
    SearchQuantumTasksRequestSearchQuantumTasksPaginateTypeDef,
    SearchQuantumTasksResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("SearchDevicesPaginator", "SearchJobsPaginator", "SearchQuantumTasksPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class SearchDevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/paginator/SearchDevices.html#Braket.Paginator.SearchDevices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators/#searchdevicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchDevicesRequestSearchDevicesPaginateTypeDef]
    ) -> AsyncIterator[SearchDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/paginator/SearchDevices.html#Braket.Paginator.SearchDevices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators/#searchdevicespaginator)
        """


class SearchJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/paginator/SearchJobs.html#Braket.Paginator.SearchJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators/#searchjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchJobsRequestSearchJobsPaginateTypeDef]
    ) -> AsyncIterator[SearchJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/paginator/SearchJobs.html#Braket.Paginator.SearchJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators/#searchjobspaginator)
        """


class SearchQuantumTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/paginator/SearchQuantumTasks.html#Braket.Paginator.SearchQuantumTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators/#searchquantumtaskspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchQuantumTasksRequestSearchQuantumTasksPaginateTypeDef]
    ) -> AsyncIterator[SearchQuantumTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/paginator/SearchQuantumTasks.html#Braket.Paginator.SearchQuantumTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators/#searchquantumtaskspaginator)
        """
