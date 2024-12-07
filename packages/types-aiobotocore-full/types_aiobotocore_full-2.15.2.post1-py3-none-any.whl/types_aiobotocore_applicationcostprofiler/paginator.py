"""
Type annotations for applicationcostprofiler service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_applicationcostprofiler/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_applicationcostprofiler.client import ApplicationCostProfilerClient
    from types_aiobotocore_applicationcostprofiler.paginator import (
        ListReportDefinitionsPaginator,
    )

    session = get_session()
    with session.create_client("applicationcostprofiler") as client:
        client: ApplicationCostProfilerClient

        list_report_definitions_paginator: ListReportDefinitionsPaginator = client.get_paginator("list_report_definitions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListReportDefinitionsRequestListReportDefinitionsPaginateTypeDef,
    ListReportDefinitionsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListReportDefinitionsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListReportDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler/paginator/ListReportDefinitions.html#ApplicationCostProfiler.Paginator.ListReportDefinitions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_applicationcostprofiler/paginators/#listreportdefinitionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReportDefinitionsRequestListReportDefinitionsPaginateTypeDef]
    ) -> AsyncIterator[ListReportDefinitionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler/paginator/ListReportDefinitions.html#ApplicationCostProfiler.Paginator.ListReportDefinitions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_applicationcostprofiler/paginators/#listreportdefinitionspaginator)
        """
