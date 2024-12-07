"""
Type annotations for s3outposts service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_s3outposts.client import S3OutpostsClient
    from types_aiobotocore_s3outposts.paginator import (
        ListEndpointsPaginator,
        ListOutpostsWithS3Paginator,
        ListSharedEndpointsPaginator,
    )

    session = get_session()
    with session.create_client("s3outposts") as client:
        client: S3OutpostsClient

        list_endpoints_paginator: ListEndpointsPaginator = client.get_paginator("list_endpoints")
        list_outposts_with_s3_paginator: ListOutpostsWithS3Paginator = client.get_paginator("list_outposts_with_s3")
        list_shared_endpoints_paginator: ListSharedEndpointsPaginator = client.get_paginator("list_shared_endpoints")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListEndpointsRequestListEndpointsPaginateTypeDef,
    ListEndpointsResultTypeDef,
    ListOutpostsWithS3RequestListOutpostsWithS3PaginateTypeDef,
    ListOutpostsWithS3ResultTypeDef,
    ListSharedEndpointsRequestListSharedEndpointsPaginateTypeDef,
    ListSharedEndpointsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListEndpointsPaginator", "ListOutpostsWithS3Paginator", "ListSharedEndpointsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListEndpoints.html#S3Outposts.Paginator.ListEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/#listendpointspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEndpointsRequestListEndpointsPaginateTypeDef]
    ) -> AsyncIterator[ListEndpointsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListEndpoints.html#S3Outposts.Paginator.ListEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/#listendpointspaginator)
        """

class ListOutpostsWithS3Paginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListOutpostsWithS3.html#S3Outposts.Paginator.ListOutpostsWithS3)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/#listoutpostswiths3paginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListOutpostsWithS3RequestListOutpostsWithS3PaginateTypeDef]
    ) -> AsyncIterator[ListOutpostsWithS3ResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListOutpostsWithS3.html#S3Outposts.Paginator.ListOutpostsWithS3.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/#listoutpostswiths3paginator)
        """

class ListSharedEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListSharedEndpoints.html#S3Outposts.Paginator.ListSharedEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/#listsharedendpointspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSharedEndpointsRequestListSharedEndpointsPaginateTypeDef]
    ) -> AsyncIterator[ListSharedEndpointsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListSharedEndpoints.html#S3Outposts.Paginator.ListSharedEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/#listsharedendpointspaginator)
        """
