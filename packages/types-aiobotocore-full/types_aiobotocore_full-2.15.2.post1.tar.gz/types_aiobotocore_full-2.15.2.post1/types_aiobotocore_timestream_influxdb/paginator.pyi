"""
Type annotations for timestream-influxdb service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_timestream_influxdb.client import TimestreamInfluxDBClient
    from types_aiobotocore_timestream_influxdb.paginator import (
        ListDbInstancesPaginator,
        ListDbParameterGroupsPaginator,
    )

    session = get_session()
    with session.create_client("timestream-influxdb") as client:
        client: TimestreamInfluxDBClient

        list_db_instances_paginator: ListDbInstancesPaginator = client.get_paginator("list_db_instances")
        list_db_parameter_groups_paginator: ListDbParameterGroupsPaginator = client.get_paginator("list_db_parameter_groups")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListDbInstancesInputListDbInstancesPaginateTypeDef,
    ListDbInstancesOutputTypeDef,
    ListDbParameterGroupsInputListDbParameterGroupsPaginateTypeDef,
    ListDbParameterGroupsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListDbInstancesPaginator", "ListDbParameterGroupsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDbInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/paginator/ListDbInstances.html#TimestreamInfluxDB.Paginator.ListDbInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/paginators/#listdbinstancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDbInstancesInputListDbInstancesPaginateTypeDef]
    ) -> AsyncIterator[ListDbInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/paginator/ListDbInstances.html#TimestreamInfluxDB.Paginator.ListDbInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/paginators/#listdbinstancespaginator)
        """

class ListDbParameterGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/paginator/ListDbParameterGroups.html#TimestreamInfluxDB.Paginator.ListDbParameterGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/paginators/#listdbparametergroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDbParameterGroupsInputListDbParameterGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListDbParameterGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/paginator/ListDbParameterGroups.html#TimestreamInfluxDB.Paginator.ListDbParameterGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/paginators/#listdbparametergroupspaginator)
        """
