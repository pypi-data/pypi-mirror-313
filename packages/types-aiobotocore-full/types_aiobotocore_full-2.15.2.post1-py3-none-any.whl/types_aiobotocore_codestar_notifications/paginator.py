"""
Type annotations for codestar-notifications service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codestar_notifications.client import CodeStarNotificationsClient
    from types_aiobotocore_codestar_notifications.paginator import (
        ListEventTypesPaginator,
        ListNotificationRulesPaginator,
        ListTargetsPaginator,
    )

    session = get_session()
    with session.create_client("codestar-notifications") as client:
        client: CodeStarNotificationsClient

        list_event_types_paginator: ListEventTypesPaginator = client.get_paginator("list_event_types")
        list_notification_rules_paginator: ListNotificationRulesPaginator = client.get_paginator("list_notification_rules")
        list_targets_paginator: ListTargetsPaginator = client.get_paginator("list_targets")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListEventTypesRequestListEventTypesPaginateTypeDef,
    ListEventTypesResultTypeDef,
    ListNotificationRulesRequestListNotificationRulesPaginateTypeDef,
    ListNotificationRulesResultTypeDef,
    ListTargetsRequestListTargetsPaginateTypeDef,
    ListTargetsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListEventTypesPaginator", "ListNotificationRulesPaginator", "ListTargetsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListEventTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListEventTypes.html#CodeStarNotifications.Paginator.ListEventTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/paginators/#listeventtypespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEventTypesRequestListEventTypesPaginateTypeDef]
    ) -> AsyncIterator[ListEventTypesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListEventTypes.html#CodeStarNotifications.Paginator.ListEventTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/paginators/#listeventtypespaginator)
        """


class ListNotificationRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListNotificationRules.html#CodeStarNotifications.Paginator.ListNotificationRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/paginators/#listnotificationrulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListNotificationRulesRequestListNotificationRulesPaginateTypeDef]
    ) -> AsyncIterator[ListNotificationRulesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListNotificationRules.html#CodeStarNotifications.Paginator.ListNotificationRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/paginators/#listnotificationrulespaginator)
        """


class ListTargetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListTargets.html#CodeStarNotifications.Paginator.ListTargets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/paginators/#listtargetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTargetsRequestListTargetsPaginateTypeDef]
    ) -> AsyncIterator[ListTargetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListTargets.html#CodeStarNotifications.Paginator.ListTargets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/paginators/#listtargetspaginator)
        """
