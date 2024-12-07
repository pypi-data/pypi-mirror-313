"""
Type annotations for migrationhubstrategy service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_migrationhubstrategy.client import MigrationHubStrategyRecommendationsClient
    from types_aiobotocore_migrationhubstrategy.paginator import (
        GetServerDetailsPaginator,
        ListAnalyzableServersPaginator,
        ListApplicationComponentsPaginator,
        ListCollectorsPaginator,
        ListImportFileTaskPaginator,
        ListServersPaginator,
    )

    session = get_session()
    with session.create_client("migrationhubstrategy") as client:
        client: MigrationHubStrategyRecommendationsClient

        get_server_details_paginator: GetServerDetailsPaginator = client.get_paginator("get_server_details")
        list_analyzable_servers_paginator: ListAnalyzableServersPaginator = client.get_paginator("list_analyzable_servers")
        list_application_components_paginator: ListApplicationComponentsPaginator = client.get_paginator("list_application_components")
        list_collectors_paginator: ListCollectorsPaginator = client.get_paginator("list_collectors")
        list_import_file_task_paginator: ListImportFileTaskPaginator = client.get_paginator("list_import_file_task")
        list_servers_paginator: ListServersPaginator = client.get_paginator("list_servers")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetServerDetailsRequestGetServerDetailsPaginateTypeDef,
    GetServerDetailsResponseTypeDef,
    ListAnalyzableServersRequestListAnalyzableServersPaginateTypeDef,
    ListAnalyzableServersResponseTypeDef,
    ListApplicationComponentsRequestListApplicationComponentsPaginateTypeDef,
    ListApplicationComponentsResponseTypeDef,
    ListCollectorsRequestListCollectorsPaginateTypeDef,
    ListCollectorsResponseTypeDef,
    ListImportFileTaskRequestListImportFileTaskPaginateTypeDef,
    ListImportFileTaskResponseTypeDef,
    ListServersRequestListServersPaginateTypeDef,
    ListServersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetServerDetailsPaginator",
    "ListAnalyzableServersPaginator",
    "ListApplicationComponentsPaginator",
    "ListCollectorsPaginator",
    "ListImportFileTaskPaginator",
    "ListServersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetServerDetailsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/GetServerDetails.html#MigrationHubStrategyRecommendations.Paginator.GetServerDetails)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#getserverdetailspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetServerDetailsRequestGetServerDetailsPaginateTypeDef]
    ) -> AsyncIterator[GetServerDetailsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/GetServerDetails.html#MigrationHubStrategyRecommendations.Paginator.GetServerDetails.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#getserverdetailspaginator)
        """

class ListAnalyzableServersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListAnalyzableServers.html#MigrationHubStrategyRecommendations.Paginator.ListAnalyzableServers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listanalyzableserverspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAnalyzableServersRequestListAnalyzableServersPaginateTypeDef]
    ) -> AsyncIterator[ListAnalyzableServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListAnalyzableServers.html#MigrationHubStrategyRecommendations.Paginator.ListAnalyzableServers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listanalyzableserverspaginator)
        """

class ListApplicationComponentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListApplicationComponents.html#MigrationHubStrategyRecommendations.Paginator.ListApplicationComponents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listapplicationcomponentspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListApplicationComponentsRequestListApplicationComponentsPaginateTypeDef],
    ) -> AsyncIterator[ListApplicationComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListApplicationComponents.html#MigrationHubStrategyRecommendations.Paginator.ListApplicationComponents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listapplicationcomponentspaginator)
        """

class ListCollectorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListCollectors.html#MigrationHubStrategyRecommendations.Paginator.ListCollectors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listcollectorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCollectorsRequestListCollectorsPaginateTypeDef]
    ) -> AsyncIterator[ListCollectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListCollectors.html#MigrationHubStrategyRecommendations.Paginator.ListCollectors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listcollectorspaginator)
        """

class ListImportFileTaskPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListImportFileTask.html#MigrationHubStrategyRecommendations.Paginator.ListImportFileTask)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listimportfiletaskpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListImportFileTaskRequestListImportFileTaskPaginateTypeDef]
    ) -> AsyncIterator[ListImportFileTaskResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListImportFileTask.html#MigrationHubStrategyRecommendations.Paginator.ListImportFileTask.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listimportfiletaskpaginator)
        """

class ListServersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListServers.html#MigrationHubStrategyRecommendations.Paginator.ListServers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listserverspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListServersRequestListServersPaginateTypeDef]
    ) -> AsyncIterator[ListServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListServers.html#MigrationHubStrategyRecommendations.Paginator.ListServers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listserverspaginator)
        """
