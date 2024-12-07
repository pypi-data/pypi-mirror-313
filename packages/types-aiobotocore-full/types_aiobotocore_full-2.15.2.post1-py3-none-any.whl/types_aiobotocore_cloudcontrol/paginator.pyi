"""
Type annotations for cloudcontrol service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudcontrol.client import CloudControlApiClient
    from types_aiobotocore_cloudcontrol.paginator import (
        ListResourceRequestsPaginator,
        ListResourcesPaginator,
    )

    session = get_session()
    with session.create_client("cloudcontrol") as client:
        client: CloudControlApiClient

        list_resource_requests_paginator: ListResourceRequestsPaginator = client.get_paginator("list_resource_requests")
        list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListResourceRequestsInputListResourceRequestsPaginateTypeDef,
    ListResourceRequestsOutputTypeDef,
    ListResourcesInputListResourcesPaginateTypeDef,
    ListResourcesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListResourceRequestsPaginator", "ListResourcesPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListResourceRequestsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/paginator/ListResourceRequests.html#CloudControlApi.Paginator.ListResourceRequests)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/paginators/#listresourcerequestspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListResourceRequestsInputListResourceRequestsPaginateTypeDef]
    ) -> AsyncIterator[ListResourceRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/paginator/ListResourceRequests.html#CloudControlApi.Paginator.ListResourceRequests.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/paginators/#listresourcerequestspaginator)
        """

class ListResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/paginator/ListResources.html#CloudControlApi.Paginator.ListResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/paginators/#listresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListResourcesInputListResourcesPaginateTypeDef]
    ) -> AsyncIterator[ListResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/paginator/ListResources.html#CloudControlApi.Paginator.ListResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/paginators/#listresourcespaginator)
        """
