"""
Type annotations for cur service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cur/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cur.client import CostandUsageReportServiceClient
    from types_aiobotocore_cur.paginator import (
        DescribeReportDefinitionsPaginator,
    )

    session = get_session()
    with session.create_client("cur") as client:
        client: CostandUsageReportServiceClient

        describe_report_definitions_paginator: DescribeReportDefinitionsPaginator = client.get_paginator("describe_report_definitions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeReportDefinitionsRequestDescribeReportDefinitionsPaginateTypeDef,
    DescribeReportDefinitionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DescribeReportDefinitionsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeReportDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur/paginator/DescribeReportDefinitions.html#CostandUsageReportService.Paginator.DescribeReportDefinitions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cur/paginators/#describereportdefinitionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeReportDefinitionsRequestDescribeReportDefinitionsPaginateTypeDef],
    ) -> AsyncIterator[DescribeReportDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur/paginator/DescribeReportDefinitions.html#CostandUsageReportService.Paginator.DescribeReportDefinitions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cur/paginators/#describereportdefinitionspaginator)
        """
