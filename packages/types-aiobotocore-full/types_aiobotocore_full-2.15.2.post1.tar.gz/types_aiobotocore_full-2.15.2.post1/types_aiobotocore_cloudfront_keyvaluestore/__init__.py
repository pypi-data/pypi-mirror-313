"""
Main interface for cloudfront-keyvaluestore service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudfront_keyvaluestore import (
        Client,
        CloudFrontKeyValueStoreClient,
        ListKeysPaginator,
    )

    session = get_session()
    async with session.create_client("cloudfront-keyvaluestore") as client:
        client: CloudFrontKeyValueStoreClient
        ...


    list_keys_paginator: ListKeysPaginator = client.get_paginator("list_keys")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CloudFrontKeyValueStoreClient
from .paginator import ListKeysPaginator

Client = CloudFrontKeyValueStoreClient


__all__ = ("Client", "CloudFrontKeyValueStoreClient", "ListKeysPaginator")
