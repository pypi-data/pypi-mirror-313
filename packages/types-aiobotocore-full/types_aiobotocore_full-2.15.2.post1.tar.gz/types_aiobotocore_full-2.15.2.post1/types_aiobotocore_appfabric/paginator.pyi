"""
Type annotations for appfabric service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_appfabric.client import AppFabricClient
    from types_aiobotocore_appfabric.paginator import (
        ListAppAuthorizationsPaginator,
        ListAppBundlesPaginator,
        ListIngestionDestinationsPaginator,
        ListIngestionsPaginator,
    )

    session = get_session()
    with session.create_client("appfabric") as client:
        client: AppFabricClient

        list_app_authorizations_paginator: ListAppAuthorizationsPaginator = client.get_paginator("list_app_authorizations")
        list_app_bundles_paginator: ListAppBundlesPaginator = client.get_paginator("list_app_bundles")
        list_ingestion_destinations_paginator: ListIngestionDestinationsPaginator = client.get_paginator("list_ingestion_destinations")
        list_ingestions_paginator: ListIngestionsPaginator = client.get_paginator("list_ingestions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAppAuthorizationsRequestListAppAuthorizationsPaginateTypeDef,
    ListAppAuthorizationsResponseTypeDef,
    ListAppBundlesRequestListAppBundlesPaginateTypeDef,
    ListAppBundlesResponseTypeDef,
    ListIngestionDestinationsRequestListIngestionDestinationsPaginateTypeDef,
    ListIngestionDestinationsResponseTypeDef,
    ListIngestionsRequestListIngestionsPaginateTypeDef,
    ListIngestionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAppAuthorizationsPaginator",
    "ListAppBundlesPaginator",
    "ListIngestionDestinationsPaginator",
    "ListIngestionsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAppAuthorizationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/paginator/ListAppAuthorizations.html#AppFabric.Paginator.ListAppAuthorizations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/#listappauthorizationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAppAuthorizationsRequestListAppAuthorizationsPaginateTypeDef]
    ) -> AsyncIterator[ListAppAuthorizationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/paginator/ListAppAuthorizations.html#AppFabric.Paginator.ListAppAuthorizations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/#listappauthorizationspaginator)
        """

class ListAppBundlesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/paginator/ListAppBundles.html#AppFabric.Paginator.ListAppBundles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/#listappbundlespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAppBundlesRequestListAppBundlesPaginateTypeDef]
    ) -> AsyncIterator[ListAppBundlesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/paginator/ListAppBundles.html#AppFabric.Paginator.ListAppBundles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/#listappbundlespaginator)
        """

class ListIngestionDestinationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/paginator/ListIngestionDestinations.html#AppFabric.Paginator.ListIngestionDestinations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/#listingestiondestinationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListIngestionDestinationsRequestListIngestionDestinationsPaginateTypeDef],
    ) -> AsyncIterator[ListIngestionDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/paginator/ListIngestionDestinations.html#AppFabric.Paginator.ListIngestionDestinations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/#listingestiondestinationspaginator)
        """

class ListIngestionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/paginator/ListIngestions.html#AppFabric.Paginator.ListIngestions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/#listingestionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIngestionsRequestListIngestionsPaginateTypeDef]
    ) -> AsyncIterator[ListIngestionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/paginator/ListIngestions.html#AppFabric.Paginator.ListIngestions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/#listingestionspaginator)
        """
