"""
Type annotations for importexport service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_importexport.client import ImportExportClient
    from types_aiobotocore_importexport.paginator import (
        ListJobsPaginator,
    )

    session = get_session()
    with session.create_client("importexport") as client:
        client: ImportExportClient

        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListJobsInputListJobsPaginateTypeDef, ListJobsOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListJobsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/paginator/ListJobs.html#ImportExport.Paginator.ListJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/paginators/#listjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsInputListJobsPaginateTypeDef]
    ) -> AsyncIterator[ListJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/paginator/ListJobs.html#ImportExport.Paginator.ListJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/paginators/#listjobspaginator)
        """
