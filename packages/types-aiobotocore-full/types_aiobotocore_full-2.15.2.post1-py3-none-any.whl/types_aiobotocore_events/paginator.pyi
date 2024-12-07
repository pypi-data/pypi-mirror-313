"""
Type annotations for events service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_events/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_events.client import EventBridgeClient
    from types_aiobotocore_events.paginator import (
        ListRuleNamesByTargetPaginator,
        ListRulesPaginator,
        ListTargetsByRulePaginator,
    )

    session = get_session()
    with session.create_client("events") as client:
        client: EventBridgeClient

        list_rule_names_by_target_paginator: ListRuleNamesByTargetPaginator = client.get_paginator("list_rule_names_by_target")
        list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
        list_targets_by_rule_paginator: ListTargetsByRulePaginator = client.get_paginator("list_targets_by_rule")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListRuleNamesByTargetRequestListRuleNamesByTargetPaginateTypeDef,
    ListRuleNamesByTargetResponseTypeDef,
    ListRulesRequestListRulesPaginateTypeDef,
    ListRulesResponseTypeDef,
    ListTargetsByRuleRequestListTargetsByRulePaginateTypeDef,
    ListTargetsByRuleResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListRuleNamesByTargetPaginator", "ListRulesPaginator", "ListTargetsByRulePaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListRuleNamesByTargetPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListRuleNamesByTarget.html#EventBridge.Paginator.ListRuleNamesByTarget)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_events/paginators/#listrulenamesbytargetpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRuleNamesByTargetRequestListRuleNamesByTargetPaginateTypeDef]
    ) -> AsyncIterator[ListRuleNamesByTargetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListRuleNamesByTarget.html#EventBridge.Paginator.ListRuleNamesByTarget.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_events/paginators/#listrulenamesbytargetpaginator)
        """

class ListRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListRules.html#EventBridge.Paginator.ListRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_events/paginators/#listrulespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRulesRequestListRulesPaginateTypeDef]
    ) -> AsyncIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListRules.html#EventBridge.Paginator.ListRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_events/paginators/#listrulespaginator)
        """

class ListTargetsByRulePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListTargetsByRule.html#EventBridge.Paginator.ListTargetsByRule)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_events/paginators/#listtargetsbyrulepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTargetsByRuleRequestListTargetsByRulePaginateTypeDef]
    ) -> AsyncIterator[ListTargetsByRuleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListTargetsByRule.html#EventBridge.Paginator.ListTargetsByRule.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_events/paginators/#listtargetsbyrulepaginator)
        """
