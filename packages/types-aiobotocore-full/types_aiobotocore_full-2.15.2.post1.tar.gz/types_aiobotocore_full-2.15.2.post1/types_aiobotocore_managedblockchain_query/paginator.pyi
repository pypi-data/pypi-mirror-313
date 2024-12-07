"""
Type annotations for managedblockchain-query service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_managedblockchain_query.client import ManagedBlockchainQueryClient
    from types_aiobotocore_managedblockchain_query.paginator import (
        ListAssetContractsPaginator,
        ListFilteredTransactionEventsPaginator,
        ListTokenBalancesPaginator,
        ListTransactionEventsPaginator,
        ListTransactionsPaginator,
    )

    session = get_session()
    with session.create_client("managedblockchain-query") as client:
        client: ManagedBlockchainQueryClient

        list_asset_contracts_paginator: ListAssetContractsPaginator = client.get_paginator("list_asset_contracts")
        list_filtered_transaction_events_paginator: ListFilteredTransactionEventsPaginator = client.get_paginator("list_filtered_transaction_events")
        list_token_balances_paginator: ListTokenBalancesPaginator = client.get_paginator("list_token_balances")
        list_transaction_events_paginator: ListTransactionEventsPaginator = client.get_paginator("list_transaction_events")
        list_transactions_paginator: ListTransactionsPaginator = client.get_paginator("list_transactions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAssetContractsInputListAssetContractsPaginateTypeDef,
    ListAssetContractsOutputTypeDef,
    ListFilteredTransactionEventsInputListFilteredTransactionEventsPaginateTypeDef,
    ListFilteredTransactionEventsOutputTypeDef,
    ListTokenBalancesInputListTokenBalancesPaginateTypeDef,
    ListTokenBalancesOutputTypeDef,
    ListTransactionEventsInputListTransactionEventsPaginateTypeDef,
    ListTransactionEventsOutputTypeDef,
    ListTransactionsInputListTransactionsPaginateTypeDef,
    ListTransactionsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAssetContractsPaginator",
    "ListFilteredTransactionEventsPaginator",
    "ListTokenBalancesPaginator",
    "ListTransactionEventsPaginator",
    "ListTransactionsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAssetContractsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListAssetContracts.html#ManagedBlockchainQuery.Paginator.ListAssetContracts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listassetcontractspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAssetContractsInputListAssetContractsPaginateTypeDef]
    ) -> AsyncIterator[ListAssetContractsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListAssetContracts.html#ManagedBlockchainQuery.Paginator.ListAssetContracts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listassetcontractspaginator)
        """

class ListFilteredTransactionEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListFilteredTransactionEvents.html#ManagedBlockchainQuery.Paginator.ListFilteredTransactionEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listfilteredtransactioneventspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListFilteredTransactionEventsInputListFilteredTransactionEventsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListFilteredTransactionEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListFilteredTransactionEvents.html#ManagedBlockchainQuery.Paginator.ListFilteredTransactionEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listfilteredtransactioneventspaginator)
        """

class ListTokenBalancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTokenBalances.html#ManagedBlockchainQuery.Paginator.ListTokenBalances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listtokenbalancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTokenBalancesInputListTokenBalancesPaginateTypeDef]
    ) -> AsyncIterator[ListTokenBalancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTokenBalances.html#ManagedBlockchainQuery.Paginator.ListTokenBalances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listtokenbalancespaginator)
        """

class ListTransactionEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTransactionEvents.html#ManagedBlockchainQuery.Paginator.ListTransactionEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listtransactioneventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTransactionEventsInputListTransactionEventsPaginateTypeDef]
    ) -> AsyncIterator[ListTransactionEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTransactionEvents.html#ManagedBlockchainQuery.Paginator.ListTransactionEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listtransactioneventspaginator)
        """

class ListTransactionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTransactions.html#ManagedBlockchainQuery.Paginator.ListTransactions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listtransactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTransactionsInputListTransactionsPaginateTypeDef]
    ) -> AsyncIterator[ListTransactionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTransactions.html#ManagedBlockchainQuery.Paginator.ListTransactions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listtransactionspaginator)
        """
