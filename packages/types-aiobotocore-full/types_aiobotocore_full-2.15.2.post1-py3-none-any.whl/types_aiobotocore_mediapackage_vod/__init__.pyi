"""
Main interface for mediapackage-vod service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mediapackage_vod import (
        Client,
        ListAssetsPaginator,
        ListPackagingConfigurationsPaginator,
        ListPackagingGroupsPaginator,
        MediaPackageVodClient,
    )

    session = get_session()
    async with session.create_client("mediapackage-vod") as client:
        client: MediaPackageVodClient
        ...


    list_assets_paginator: ListAssetsPaginator = client.get_paginator("list_assets")
    list_packaging_configurations_paginator: ListPackagingConfigurationsPaginator = client.get_paginator("list_packaging_configurations")
    list_packaging_groups_paginator: ListPackagingGroupsPaginator = client.get_paginator("list_packaging_groups")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import MediaPackageVodClient
from .paginator import (
    ListAssetsPaginator,
    ListPackagingConfigurationsPaginator,
    ListPackagingGroupsPaginator,
)

Client = MediaPackageVodClient

__all__ = (
    "Client",
    "ListAssetsPaginator",
    "ListPackagingConfigurationsPaginator",
    "ListPackagingGroupsPaginator",
    "MediaPackageVodClient",
)
