"""
Type annotations for pca-connector-scep service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_scep/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_pca_connector_scep.client import PrivateCAConnectorforSCEPClient
    from types_aiobotocore_pca_connector_scep.paginator import (
        ListChallengeMetadataPaginator,
        ListConnectorsPaginator,
    )

    session = get_session()
    with session.create_client("pca-connector-scep") as client:
        client: PrivateCAConnectorforSCEPClient

        list_challenge_metadata_paginator: ListChallengeMetadataPaginator = client.get_paginator("list_challenge_metadata")
        list_connectors_paginator: ListConnectorsPaginator = client.get_paginator("list_connectors")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListChallengeMetadataRequestListChallengeMetadataPaginateTypeDef,
    ListChallengeMetadataResponseTypeDef,
    ListConnectorsRequestListConnectorsPaginateTypeDef,
    ListConnectorsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListChallengeMetadataPaginator", "ListConnectorsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListChallengeMetadataPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-scep/paginator/ListChallengeMetadata.html#PrivateCAConnectorforSCEP.Paginator.ListChallengeMetadata)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_scep/paginators/#listchallengemetadatapaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListChallengeMetadataRequestListChallengeMetadataPaginateTypeDef]
    ) -> AsyncIterator[ListChallengeMetadataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-scep/paginator/ListChallengeMetadata.html#PrivateCAConnectorforSCEP.Paginator.ListChallengeMetadata.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_scep/paginators/#listchallengemetadatapaginator)
        """

class ListConnectorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-scep/paginator/ListConnectors.html#PrivateCAConnectorforSCEP.Paginator.ListConnectors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_scep/paginators/#listconnectorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListConnectorsRequestListConnectorsPaginateTypeDef]
    ) -> AsyncIterator[ListConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-scep/paginator/ListConnectors.html#PrivateCAConnectorforSCEP.Paginator.ListConnectors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_scep/paginators/#listconnectorspaginator)
        """
