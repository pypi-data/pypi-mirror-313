"""
Type annotations for controlcatalog service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_controlcatalog.client import ControlCatalogClient
    from types_aiobotocore_controlcatalog.paginator import (
        ListCommonControlsPaginator,
        ListControlsPaginator,
        ListDomainsPaginator,
        ListObjectivesPaginator,
    )

    session = get_session()
    with session.create_client("controlcatalog") as client:
        client: ControlCatalogClient

        list_common_controls_paginator: ListCommonControlsPaginator = client.get_paginator("list_common_controls")
        list_controls_paginator: ListControlsPaginator = client.get_paginator("list_controls")
        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_objectives_paginator: ListObjectivesPaginator = client.get_paginator("list_objectives")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListCommonControlsRequestListCommonControlsPaginateTypeDef,
    ListCommonControlsResponseTypeDef,
    ListControlsRequestListControlsPaginateTypeDef,
    ListControlsResponseTypeDef,
    ListDomainsRequestListDomainsPaginateTypeDef,
    ListDomainsResponseTypeDef,
    ListObjectivesRequestListObjectivesPaginateTypeDef,
    ListObjectivesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListCommonControlsPaginator",
    "ListControlsPaginator",
    "ListDomainsPaginator",
    "ListObjectivesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListCommonControlsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListCommonControls.html#ControlCatalog.Paginator.ListCommonControls)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listcommoncontrolspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCommonControlsRequestListCommonControlsPaginateTypeDef]
    ) -> AsyncIterator[ListCommonControlsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListCommonControls.html#ControlCatalog.Paginator.ListCommonControls.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listcommoncontrolspaginator)
        """


class ListControlsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListControls.html#ControlCatalog.Paginator.ListControls)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listcontrolspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListControlsRequestListControlsPaginateTypeDef]
    ) -> AsyncIterator[ListControlsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListControls.html#ControlCatalog.Paginator.ListControls.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listcontrolspaginator)
        """


class ListDomainsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListDomains.html#ControlCatalog.Paginator.ListDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listdomainspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDomainsRequestListDomainsPaginateTypeDef]
    ) -> AsyncIterator[ListDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListDomains.html#ControlCatalog.Paginator.ListDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listdomainspaginator)
        """


class ListObjectivesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListObjectives.html#ControlCatalog.Paginator.ListObjectives)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listobjectivespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListObjectivesRequestListObjectivesPaginateTypeDef]
    ) -> AsyncIterator[ListObjectivesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListObjectives.html#ControlCatalog.Paginator.ListObjectives.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listobjectivespaginator)
        """
