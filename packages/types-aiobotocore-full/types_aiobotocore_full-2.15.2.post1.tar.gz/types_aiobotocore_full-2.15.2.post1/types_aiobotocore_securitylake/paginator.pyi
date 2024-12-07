"""
Type annotations for securitylake service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_securitylake.client import SecurityLakeClient
    from types_aiobotocore_securitylake.paginator import (
        GetDataLakeSourcesPaginator,
        ListDataLakeExceptionsPaginator,
        ListLogSourcesPaginator,
        ListSubscribersPaginator,
    )

    session = get_session()
    with session.create_client("securitylake") as client:
        client: SecurityLakeClient

        get_data_lake_sources_paginator: GetDataLakeSourcesPaginator = client.get_paginator("get_data_lake_sources")
        list_data_lake_exceptions_paginator: ListDataLakeExceptionsPaginator = client.get_paginator("list_data_lake_exceptions")
        list_log_sources_paginator: ListLogSourcesPaginator = client.get_paginator("list_log_sources")
        list_subscribers_paginator: ListSubscribersPaginator = client.get_paginator("list_subscribers")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetDataLakeSourcesRequestGetDataLakeSourcesPaginateTypeDef,
    GetDataLakeSourcesResponseTypeDef,
    ListDataLakeExceptionsRequestListDataLakeExceptionsPaginateTypeDef,
    ListDataLakeExceptionsResponseTypeDef,
    ListLogSourcesRequestListLogSourcesPaginateTypeDef,
    ListLogSourcesResponseTypeDef,
    ListSubscribersRequestListSubscribersPaginateTypeDef,
    ListSubscribersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetDataLakeSourcesPaginator",
    "ListDataLakeExceptionsPaginator",
    "ListLogSourcesPaginator",
    "ListSubscribersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetDataLakeSourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/GetDataLakeSources.html#SecurityLake.Paginator.GetDataLakeSources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#getdatalakesourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDataLakeSourcesRequestGetDataLakeSourcesPaginateTypeDef]
    ) -> AsyncIterator[GetDataLakeSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/GetDataLakeSources.html#SecurityLake.Paginator.GetDataLakeSources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#getdatalakesourcespaginator)
        """

class ListDataLakeExceptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListDataLakeExceptions.html#SecurityLake.Paginator.ListDataLakeExceptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listdatalakeexceptionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataLakeExceptionsRequestListDataLakeExceptionsPaginateTypeDef]
    ) -> AsyncIterator[ListDataLakeExceptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListDataLakeExceptions.html#SecurityLake.Paginator.ListDataLakeExceptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listdatalakeexceptionspaginator)
        """

class ListLogSourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListLogSources.html#SecurityLake.Paginator.ListLogSources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listlogsourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLogSourcesRequestListLogSourcesPaginateTypeDef]
    ) -> AsyncIterator[ListLogSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListLogSources.html#SecurityLake.Paginator.ListLogSources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listlogsourcespaginator)
        """

class ListSubscribersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListSubscribers.html#SecurityLake.Paginator.ListSubscribers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listsubscriberspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSubscribersRequestListSubscribersPaginateTypeDef]
    ) -> AsyncIterator[ListSubscribersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListSubscribers.html#SecurityLake.Paginator.ListSubscribers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listsubscriberspaginator)
        """
