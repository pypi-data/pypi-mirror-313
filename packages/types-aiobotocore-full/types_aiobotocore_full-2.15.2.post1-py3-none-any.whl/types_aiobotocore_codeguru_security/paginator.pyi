"""
Type annotations for codeguru-security service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_security/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codeguru_security.client import CodeGuruSecurityClient
    from types_aiobotocore_codeguru_security.paginator import (
        GetFindingsPaginator,
        ListFindingsMetricsPaginator,
        ListScansPaginator,
    )

    session = get_session()
    with session.create_client("codeguru-security") as client:
        client: CodeGuruSecurityClient

        get_findings_paginator: GetFindingsPaginator = client.get_paginator("get_findings")
        list_findings_metrics_paginator: ListFindingsMetricsPaginator = client.get_paginator("list_findings_metrics")
        list_scans_paginator: ListScansPaginator = client.get_paginator("list_scans")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetFindingsRequestGetFindingsPaginateTypeDef,
    GetFindingsResponseTypeDef,
    ListFindingsMetricsRequestListFindingsMetricsPaginateTypeDef,
    ListFindingsMetricsResponseTypeDef,
    ListScansRequestListScansPaginateTypeDef,
    ListScansResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("GetFindingsPaginator", "ListFindingsMetricsPaginator", "ListScansPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetFindingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/GetFindings.html#CodeGuruSecurity.Paginator.GetFindings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_security/paginators/#getfindingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetFindingsRequestGetFindingsPaginateTypeDef]
    ) -> AsyncIterator[GetFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/GetFindings.html#CodeGuruSecurity.Paginator.GetFindings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_security/paginators/#getfindingspaginator)
        """

class ListFindingsMetricsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/ListFindingsMetrics.html#CodeGuruSecurity.Paginator.ListFindingsMetrics)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_security/paginators/#listfindingsmetricspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFindingsMetricsRequestListFindingsMetricsPaginateTypeDef]
    ) -> AsyncIterator[ListFindingsMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/ListFindingsMetrics.html#CodeGuruSecurity.Paginator.ListFindingsMetrics.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_security/paginators/#listfindingsmetricspaginator)
        """

class ListScansPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/ListScans.html#CodeGuruSecurity.Paginator.ListScans)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_security/paginators/#listscanspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListScansRequestListScansPaginateTypeDef]
    ) -> AsyncIterator[ListScansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/ListScans.html#CodeGuruSecurity.Paginator.ListScans.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_security/paginators/#listscanspaginator)
        """
