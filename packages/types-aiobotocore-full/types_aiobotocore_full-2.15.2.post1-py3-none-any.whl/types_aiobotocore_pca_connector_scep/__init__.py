"""
Main interface for pca-connector-scep service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pca_connector_scep import (
        Client,
        ListChallengeMetadataPaginator,
        ListConnectorsPaginator,
        PrivateCAConnectorforSCEPClient,
    )

    session = get_session()
    async with session.create_client("pca-connector-scep") as client:
        client: PrivateCAConnectorforSCEPClient
        ...


    list_challenge_metadata_paginator: ListChallengeMetadataPaginator = client.get_paginator("list_challenge_metadata")
    list_connectors_paginator: ListConnectorsPaginator = client.get_paginator("list_connectors")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import PrivateCAConnectorforSCEPClient
from .paginator import ListChallengeMetadataPaginator, ListConnectorsPaginator

Client = PrivateCAConnectorforSCEPClient


__all__ = (
    "Client",
    "ListChallengeMetadataPaginator",
    "ListConnectorsPaginator",
    "PrivateCAConnectorforSCEPClient",
)
