"""
Type annotations for route53-recovery-readiness service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_route53_recovery_readiness.client import Route53RecoveryReadinessClient
    from types_aiobotocore_route53_recovery_readiness.paginator import (
        GetCellReadinessSummaryPaginator,
        GetReadinessCheckResourceStatusPaginator,
        GetReadinessCheckStatusPaginator,
        GetRecoveryGroupReadinessSummaryPaginator,
        ListCellsPaginator,
        ListCrossAccountAuthorizationsPaginator,
        ListReadinessChecksPaginator,
        ListRecoveryGroupsPaginator,
        ListResourceSetsPaginator,
        ListRulesPaginator,
    )

    session = get_session()
    with session.create_client("route53-recovery-readiness") as client:
        client: Route53RecoveryReadinessClient

        get_cell_readiness_summary_paginator: GetCellReadinessSummaryPaginator = client.get_paginator("get_cell_readiness_summary")
        get_readiness_check_resource_status_paginator: GetReadinessCheckResourceStatusPaginator = client.get_paginator("get_readiness_check_resource_status")
        get_readiness_check_status_paginator: GetReadinessCheckStatusPaginator = client.get_paginator("get_readiness_check_status")
        get_recovery_group_readiness_summary_paginator: GetRecoveryGroupReadinessSummaryPaginator = client.get_paginator("get_recovery_group_readiness_summary")
        list_cells_paginator: ListCellsPaginator = client.get_paginator("list_cells")
        list_cross_account_authorizations_paginator: ListCrossAccountAuthorizationsPaginator = client.get_paginator("list_cross_account_authorizations")
        list_readiness_checks_paginator: ListReadinessChecksPaginator = client.get_paginator("list_readiness_checks")
        list_recovery_groups_paginator: ListRecoveryGroupsPaginator = client.get_paginator("list_recovery_groups")
        list_resource_sets_paginator: ListResourceSetsPaginator = client.get_paginator("list_resource_sets")
        list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetCellReadinessSummaryRequestGetCellReadinessSummaryPaginateTypeDef,
    GetCellReadinessSummaryResponseTypeDef,
    GetReadinessCheckResourceStatusRequestGetReadinessCheckResourceStatusPaginateTypeDef,
    GetReadinessCheckResourceStatusResponseTypeDef,
    GetReadinessCheckStatusRequestGetReadinessCheckStatusPaginateTypeDef,
    GetReadinessCheckStatusResponseTypeDef,
    GetRecoveryGroupReadinessSummaryRequestGetRecoveryGroupReadinessSummaryPaginateTypeDef,
    GetRecoveryGroupReadinessSummaryResponseTypeDef,
    ListCellsRequestListCellsPaginateTypeDef,
    ListCellsResponseTypeDef,
    ListCrossAccountAuthorizationsRequestListCrossAccountAuthorizationsPaginateTypeDef,
    ListCrossAccountAuthorizationsResponseTypeDef,
    ListReadinessChecksRequestListReadinessChecksPaginateTypeDef,
    ListReadinessChecksResponseTypeDef,
    ListRecoveryGroupsRequestListRecoveryGroupsPaginateTypeDef,
    ListRecoveryGroupsResponseTypeDef,
    ListResourceSetsRequestListResourceSetsPaginateTypeDef,
    ListResourceSetsResponseTypeDef,
    ListRulesRequestListRulesPaginateTypeDef,
    ListRulesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetCellReadinessSummaryPaginator",
    "GetReadinessCheckResourceStatusPaginator",
    "GetReadinessCheckStatusPaginator",
    "GetRecoveryGroupReadinessSummaryPaginator",
    "ListCellsPaginator",
    "ListCrossAccountAuthorizationsPaginator",
    "ListReadinessChecksPaginator",
    "ListRecoveryGroupsPaginator",
    "ListResourceSetsPaginator",
    "ListRulesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetCellReadinessSummaryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/GetCellReadinessSummary.html#Route53RecoveryReadiness.Paginator.GetCellReadinessSummary)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#getcellreadinesssummarypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetCellReadinessSummaryRequestGetCellReadinessSummaryPaginateTypeDef]
    ) -> AsyncIterator[GetCellReadinessSummaryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/GetCellReadinessSummary.html#Route53RecoveryReadiness.Paginator.GetCellReadinessSummary.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#getcellreadinesssummarypaginator)
        """


class GetReadinessCheckResourceStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/GetReadinessCheckResourceStatus.html#Route53RecoveryReadiness.Paginator.GetReadinessCheckResourceStatus)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#getreadinesscheckresourcestatuspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetReadinessCheckResourceStatusRequestGetReadinessCheckResourceStatusPaginateTypeDef
        ],
    ) -> AsyncIterator[GetReadinessCheckResourceStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/GetReadinessCheckResourceStatus.html#Route53RecoveryReadiness.Paginator.GetReadinessCheckResourceStatus.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#getreadinesscheckresourcestatuspaginator)
        """


class GetReadinessCheckStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/GetReadinessCheckStatus.html#Route53RecoveryReadiness.Paginator.GetReadinessCheckStatus)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#getreadinesscheckstatuspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetReadinessCheckStatusRequestGetReadinessCheckStatusPaginateTypeDef]
    ) -> AsyncIterator[GetReadinessCheckStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/GetReadinessCheckStatus.html#Route53RecoveryReadiness.Paginator.GetReadinessCheckStatus.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#getreadinesscheckstatuspaginator)
        """


class GetRecoveryGroupReadinessSummaryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/GetRecoveryGroupReadinessSummary.html#Route53RecoveryReadiness.Paginator.GetRecoveryGroupReadinessSummary)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#getrecoverygroupreadinesssummarypaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetRecoveryGroupReadinessSummaryRequestGetRecoveryGroupReadinessSummaryPaginateTypeDef
        ],
    ) -> AsyncIterator[GetRecoveryGroupReadinessSummaryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/GetRecoveryGroupReadinessSummary.html#Route53RecoveryReadiness.Paginator.GetRecoveryGroupReadinessSummary.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#getrecoverygroupreadinesssummarypaginator)
        """


class ListCellsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListCells.html#Route53RecoveryReadiness.Paginator.ListCells)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#listcellspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCellsRequestListCellsPaginateTypeDef]
    ) -> AsyncIterator[ListCellsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListCells.html#Route53RecoveryReadiness.Paginator.ListCells.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#listcellspaginator)
        """


class ListCrossAccountAuthorizationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListCrossAccountAuthorizations.html#Route53RecoveryReadiness.Paginator.ListCrossAccountAuthorizations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#listcrossaccountauthorizationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListCrossAccountAuthorizationsRequestListCrossAccountAuthorizationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListCrossAccountAuthorizationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListCrossAccountAuthorizations.html#Route53RecoveryReadiness.Paginator.ListCrossAccountAuthorizations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#listcrossaccountauthorizationspaginator)
        """


class ListReadinessChecksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListReadinessChecks.html#Route53RecoveryReadiness.Paginator.ListReadinessChecks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#listreadinesscheckspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReadinessChecksRequestListReadinessChecksPaginateTypeDef]
    ) -> AsyncIterator[ListReadinessChecksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListReadinessChecks.html#Route53RecoveryReadiness.Paginator.ListReadinessChecks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#listreadinesscheckspaginator)
        """


class ListRecoveryGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListRecoveryGroups.html#Route53RecoveryReadiness.Paginator.ListRecoveryGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#listrecoverygroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRecoveryGroupsRequestListRecoveryGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListRecoveryGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListRecoveryGroups.html#Route53RecoveryReadiness.Paginator.ListRecoveryGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#listrecoverygroupspaginator)
        """


class ListResourceSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListResourceSets.html#Route53RecoveryReadiness.Paginator.ListResourceSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#listresourcesetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResourceSetsRequestListResourceSetsPaginateTypeDef]
    ) -> AsyncIterator[ListResourceSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListResourceSets.html#Route53RecoveryReadiness.Paginator.ListResourceSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#listresourcesetspaginator)
        """


class ListRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListRules.html#Route53RecoveryReadiness.Paginator.ListRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#listrulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRulesRequestListRulesPaginateTypeDef]
    ) -> AsyncIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListRules.html#Route53RecoveryReadiness.Paginator.ListRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators/#listrulespaginator)
        """
