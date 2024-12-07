"""
Type annotations for budgets service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_budgets.client import BudgetsClient
    from types_aiobotocore_budgets.paginator import (
        DescribeBudgetActionHistoriesPaginator,
        DescribeBudgetActionsForAccountPaginator,
        DescribeBudgetActionsForBudgetPaginator,
        DescribeBudgetNotificationsForAccountPaginator,
        DescribeBudgetPerformanceHistoryPaginator,
        DescribeBudgetsPaginator,
        DescribeNotificationsForBudgetPaginator,
        DescribeSubscribersForNotificationPaginator,
    )

    session = get_session()
    with session.create_client("budgets") as client:
        client: BudgetsClient

        describe_budget_action_histories_paginator: DescribeBudgetActionHistoriesPaginator = client.get_paginator("describe_budget_action_histories")
        describe_budget_actions_for_account_paginator: DescribeBudgetActionsForAccountPaginator = client.get_paginator("describe_budget_actions_for_account")
        describe_budget_actions_for_budget_paginator: DescribeBudgetActionsForBudgetPaginator = client.get_paginator("describe_budget_actions_for_budget")
        describe_budget_notifications_for_account_paginator: DescribeBudgetNotificationsForAccountPaginator = client.get_paginator("describe_budget_notifications_for_account")
        describe_budget_performance_history_paginator: DescribeBudgetPerformanceHistoryPaginator = client.get_paginator("describe_budget_performance_history")
        describe_budgets_paginator: DescribeBudgetsPaginator = client.get_paginator("describe_budgets")
        describe_notifications_for_budget_paginator: DescribeNotificationsForBudgetPaginator = client.get_paginator("describe_notifications_for_budget")
        describe_subscribers_for_notification_paginator: DescribeSubscribersForNotificationPaginator = client.get_paginator("describe_subscribers_for_notification")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeBudgetActionHistoriesRequestDescribeBudgetActionHistoriesPaginateTypeDef,
    DescribeBudgetActionHistoriesResponseTypeDef,
    DescribeBudgetActionsForAccountRequestDescribeBudgetActionsForAccountPaginateTypeDef,
    DescribeBudgetActionsForAccountResponseTypeDef,
    DescribeBudgetActionsForBudgetRequestDescribeBudgetActionsForBudgetPaginateTypeDef,
    DescribeBudgetActionsForBudgetResponseTypeDef,
    DescribeBudgetNotificationsForAccountRequestDescribeBudgetNotificationsForAccountPaginateTypeDef,
    DescribeBudgetNotificationsForAccountResponseTypeDef,
    DescribeBudgetPerformanceHistoryRequestDescribeBudgetPerformanceHistoryPaginateTypeDef,
    DescribeBudgetPerformanceHistoryResponseTypeDef,
    DescribeBudgetsRequestDescribeBudgetsPaginateTypeDef,
    DescribeBudgetsResponseTypeDef,
    DescribeNotificationsForBudgetRequestDescribeNotificationsForBudgetPaginateTypeDef,
    DescribeNotificationsForBudgetResponseTypeDef,
    DescribeSubscribersForNotificationRequestDescribeSubscribersForNotificationPaginateTypeDef,
    DescribeSubscribersForNotificationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeBudgetActionHistoriesPaginator",
    "DescribeBudgetActionsForAccountPaginator",
    "DescribeBudgetActionsForBudgetPaginator",
    "DescribeBudgetNotificationsForAccountPaginator",
    "DescribeBudgetPerformanceHistoryPaginator",
    "DescribeBudgetsPaginator",
    "DescribeNotificationsForBudgetPaginator",
    "DescribeSubscribersForNotificationPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeBudgetActionHistoriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetActionHistories.html#Budgets.Paginator.DescribeBudgetActionHistories)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetactionhistoriespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeBudgetActionHistoriesRequestDescribeBudgetActionHistoriesPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeBudgetActionHistoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetActionHistories.html#Budgets.Paginator.DescribeBudgetActionHistories.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetactionhistoriespaginator)
        """

class DescribeBudgetActionsForAccountPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetActionsForAccount.html#Budgets.Paginator.DescribeBudgetActionsForAccount)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetactionsforaccountpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeBudgetActionsForAccountRequestDescribeBudgetActionsForAccountPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeBudgetActionsForAccountResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetActionsForAccount.html#Budgets.Paginator.DescribeBudgetActionsForAccount.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetactionsforaccountpaginator)
        """

class DescribeBudgetActionsForBudgetPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetActionsForBudget.html#Budgets.Paginator.DescribeBudgetActionsForBudget)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetactionsforbudgetpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeBudgetActionsForBudgetRequestDescribeBudgetActionsForBudgetPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeBudgetActionsForBudgetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetActionsForBudget.html#Budgets.Paginator.DescribeBudgetActionsForBudget.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetactionsforbudgetpaginator)
        """

class DescribeBudgetNotificationsForAccountPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetNotificationsForAccount.html#Budgets.Paginator.DescribeBudgetNotificationsForAccount)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetnotificationsforaccountpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeBudgetNotificationsForAccountRequestDescribeBudgetNotificationsForAccountPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeBudgetNotificationsForAccountResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetNotificationsForAccount.html#Budgets.Paginator.DescribeBudgetNotificationsForAccount.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetnotificationsforaccountpaginator)
        """

class DescribeBudgetPerformanceHistoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetPerformanceHistory.html#Budgets.Paginator.DescribeBudgetPerformanceHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetperformancehistorypaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeBudgetPerformanceHistoryRequestDescribeBudgetPerformanceHistoryPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeBudgetPerformanceHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetPerformanceHistory.html#Budgets.Paginator.DescribeBudgetPerformanceHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetperformancehistorypaginator)
        """

class DescribeBudgetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgets.html#Budgets.Paginator.DescribeBudgets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeBudgetsRequestDescribeBudgetsPaginateTypeDef]
    ) -> AsyncIterator[DescribeBudgetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgets.html#Budgets.Paginator.DescribeBudgets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetspaginator)
        """

class DescribeNotificationsForBudgetPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeNotificationsForBudget.html#Budgets.Paginator.DescribeNotificationsForBudget)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describenotificationsforbudgetpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeNotificationsForBudgetRequestDescribeNotificationsForBudgetPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeNotificationsForBudgetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeNotificationsForBudget.html#Budgets.Paginator.DescribeNotificationsForBudget.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describenotificationsforbudgetpaginator)
        """

class DescribeSubscribersForNotificationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeSubscribersForNotification.html#Budgets.Paginator.DescribeSubscribersForNotification)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describesubscribersfornotificationpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeSubscribersForNotificationRequestDescribeSubscribersForNotificationPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeSubscribersForNotificationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeSubscribersForNotification.html#Budgets.Paginator.DescribeSubscribersForNotification.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describesubscribersfornotificationpaginator)
        """
