"""
Type annotations for sms service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sms.client import SMSClient
    from types_aiobotocore_sms.paginator import (
        GetConnectorsPaginator,
        GetReplicationJobsPaginator,
        GetReplicationRunsPaginator,
        GetServersPaginator,
        ListAppsPaginator,
    )

    session = get_session()
    with session.create_client("sms") as client:
        client: SMSClient

        get_connectors_paginator: GetConnectorsPaginator = client.get_paginator("get_connectors")
        get_replication_jobs_paginator: GetReplicationJobsPaginator = client.get_paginator("get_replication_jobs")
        get_replication_runs_paginator: GetReplicationRunsPaginator = client.get_paginator("get_replication_runs")
        get_servers_paginator: GetServersPaginator = client.get_paginator("get_servers")
        list_apps_paginator: ListAppsPaginator = client.get_paginator("list_apps")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetConnectorsRequestGetConnectorsPaginateTypeDef,
    GetConnectorsResponseTypeDef,
    GetReplicationJobsRequestGetReplicationJobsPaginateTypeDef,
    GetReplicationJobsResponseTypeDef,
    GetReplicationRunsRequestGetReplicationRunsPaginateTypeDef,
    GetReplicationRunsResponseTypeDef,
    GetServersRequestGetServersPaginateTypeDef,
    GetServersResponseTypeDef,
    ListAppsRequestListAppsPaginateTypeDef,
    ListAppsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetConnectorsPaginator",
    "GetReplicationJobsPaginator",
    "GetReplicationRunsPaginator",
    "GetServersPaginator",
    "ListAppsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetConnectorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetConnectors.html#SMS.Paginator.GetConnectors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#getconnectorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetConnectorsRequestGetConnectorsPaginateTypeDef]
    ) -> AsyncIterator[GetConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetConnectors.html#SMS.Paginator.GetConnectors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#getconnectorspaginator)
        """


class GetReplicationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetReplicationJobs.html#SMS.Paginator.GetReplicationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#getreplicationjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetReplicationJobsRequestGetReplicationJobsPaginateTypeDef]
    ) -> AsyncIterator[GetReplicationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetReplicationJobs.html#SMS.Paginator.GetReplicationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#getreplicationjobspaginator)
        """


class GetReplicationRunsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetReplicationRuns.html#SMS.Paginator.GetReplicationRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#getreplicationrunspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetReplicationRunsRequestGetReplicationRunsPaginateTypeDef]
    ) -> AsyncIterator[GetReplicationRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetReplicationRuns.html#SMS.Paginator.GetReplicationRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#getreplicationrunspaginator)
        """


class GetServersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetServers.html#SMS.Paginator.GetServers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#getserverspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetServersRequestGetServersPaginateTypeDef]
    ) -> AsyncIterator[GetServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetServers.html#SMS.Paginator.GetServers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#getserverspaginator)
        """


class ListAppsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/ListApps.html#SMS.Paginator.ListApps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#listappspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAppsRequestListAppsPaginateTypeDef]
    ) -> AsyncIterator[ListAppsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/ListApps.html#SMS.Paginator.ListApps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#listappspaginator)
        """
