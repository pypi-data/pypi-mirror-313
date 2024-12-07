"""
Type annotations for supplychain service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_supplychain.client import SupplyChainClient
    from types_aiobotocore_supplychain.paginator import (
        ListDataIntegrationFlowsPaginator,
        ListDataLakeDatasetsPaginator,
    )

    session = get_session()
    with session.create_client("supplychain") as client:
        client: SupplyChainClient

        list_data_integration_flows_paginator: ListDataIntegrationFlowsPaginator = client.get_paginator("list_data_integration_flows")
        list_data_lake_datasets_paginator: ListDataLakeDatasetsPaginator = client.get_paginator("list_data_lake_datasets")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListDataIntegrationFlowsRequestListDataIntegrationFlowsPaginateTypeDef,
    ListDataIntegrationFlowsResponseTypeDef,
    ListDataLakeDatasetsRequestListDataLakeDatasetsPaginateTypeDef,
    ListDataLakeDatasetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListDataIntegrationFlowsPaginator", "ListDataLakeDatasetsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDataIntegrationFlowsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationFlows.html#SupplyChain.Paginator.ListDataIntegrationFlows)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdataintegrationflowspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListDataIntegrationFlowsRequestListDataIntegrationFlowsPaginateTypeDef],
    ) -> AsyncIterator[ListDataIntegrationFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationFlows.html#SupplyChain.Paginator.ListDataIntegrationFlows.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdataintegrationflowspaginator)
        """

class ListDataLakeDatasetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataLakeDatasets.html#SupplyChain.Paginator.ListDataLakeDatasets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdatalakedatasetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataLakeDatasetsRequestListDataLakeDatasetsPaginateTypeDef]
    ) -> AsyncIterator[ListDataLakeDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataLakeDatasets.html#SupplyChain.Paginator.ListDataLakeDatasets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdatalakedatasetspaginator)
        """
