"""
Type annotations for amp service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_amp.client import PrometheusServiceClient
    from types_aiobotocore_amp.paginator import (
        ListRuleGroupsNamespacesPaginator,
        ListScrapersPaginator,
        ListWorkspacesPaginator,
    )

    session = get_session()
    with session.create_client("amp") as client:
        client: PrometheusServiceClient

        list_rule_groups_namespaces_paginator: ListRuleGroupsNamespacesPaginator = client.get_paginator("list_rule_groups_namespaces")
        list_scrapers_paginator: ListScrapersPaginator = client.get_paginator("list_scrapers")
        list_workspaces_paginator: ListWorkspacesPaginator = client.get_paginator("list_workspaces")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef,
    ListRuleGroupsNamespacesResponseTypeDef,
    ListScrapersRequestListScrapersPaginateTypeDef,
    ListScrapersResponseTypeDef,
    ListWorkspacesRequestListWorkspacesPaginateTypeDef,
    ListWorkspacesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListRuleGroupsNamespacesPaginator", "ListScrapersPaginator", "ListWorkspacesPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListRuleGroupsNamespacesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/paginator/ListRuleGroupsNamespaces.html#PrometheusService.Paginator.ListRuleGroupsNamespaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/paginators/#listrulegroupsnamespacespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef],
    ) -> AsyncIterator[ListRuleGroupsNamespacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/paginator/ListRuleGroupsNamespaces.html#PrometheusService.Paginator.ListRuleGroupsNamespaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/paginators/#listrulegroupsnamespacespaginator)
        """


class ListScrapersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/paginator/ListScrapers.html#PrometheusService.Paginator.ListScrapers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/paginators/#listscraperspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListScrapersRequestListScrapersPaginateTypeDef]
    ) -> AsyncIterator[ListScrapersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/paginator/ListScrapers.html#PrometheusService.Paginator.ListScrapers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/paginators/#listscraperspaginator)
        """


class ListWorkspacesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/paginator/ListWorkspaces.html#PrometheusService.Paginator.ListWorkspaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/paginators/#listworkspacespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorkspacesRequestListWorkspacesPaginateTypeDef]
    ) -> AsyncIterator[ListWorkspacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/paginator/ListWorkspaces.html#PrometheusService.Paginator.ListWorkspaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/paginators/#listworkspacespaginator)
        """
