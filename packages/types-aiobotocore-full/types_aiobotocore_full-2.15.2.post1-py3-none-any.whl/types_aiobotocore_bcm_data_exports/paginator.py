"""
Type annotations for bcm-data-exports service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_data_exports/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bcm_data_exports.client import BillingandCostManagementDataExportsClient
    from types_aiobotocore_bcm_data_exports.paginator import (
        ListExecutionsPaginator,
        ListExportsPaginator,
        ListTablesPaginator,
    )

    session = get_session()
    with session.create_client("bcm-data-exports") as client:
        client: BillingandCostManagementDataExportsClient

        list_executions_paginator: ListExecutionsPaginator = client.get_paginator("list_executions")
        list_exports_paginator: ListExportsPaginator = client.get_paginator("list_exports")
        list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListExecutionsRequestListExecutionsPaginateTypeDef,
    ListExecutionsResponseTypeDef,
    ListExportsRequestListExportsPaginateTypeDef,
    ListExportsResponseTypeDef,
    ListTablesRequestListTablesPaginateTypeDef,
    ListTablesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListExecutionsPaginator", "ListExportsPaginator", "ListTablesPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-data-exports/paginator/ListExecutions.html#BillingandCostManagementDataExports.Paginator.ListExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_data_exports/paginators/#listexecutionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListExecutionsRequestListExecutionsPaginateTypeDef]
    ) -> AsyncIterator[ListExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-data-exports/paginator/ListExecutions.html#BillingandCostManagementDataExports.Paginator.ListExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_data_exports/paginators/#listexecutionspaginator)
        """


class ListExportsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-data-exports/paginator/ListExports.html#BillingandCostManagementDataExports.Paginator.ListExports)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_data_exports/paginators/#listexportspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListExportsRequestListExportsPaginateTypeDef]
    ) -> AsyncIterator[ListExportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-data-exports/paginator/ListExports.html#BillingandCostManagementDataExports.Paginator.ListExports.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_data_exports/paginators/#listexportspaginator)
        """


class ListTablesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-data-exports/paginator/ListTables.html#BillingandCostManagementDataExports.Paginator.ListTables)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_data_exports/paginators/#listtablespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTablesRequestListTablesPaginateTypeDef]
    ) -> AsyncIterator[ListTablesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-data-exports/paginator/ListTables.html#BillingandCostManagementDataExports.Paginator.ListTables.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_data_exports/paginators/#listtablespaginator)
        """
