"""
Main interface for kinesis-video-archived-media service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kinesis_video_archived_media import (
        Client,
        GetImagesPaginator,
        KinesisVideoArchivedMediaClient,
        ListFragmentsPaginator,
    )

    session = get_session()
    async with session.create_client("kinesis-video-archived-media") as client:
        client: KinesisVideoArchivedMediaClient
        ...


    get_images_paginator: GetImagesPaginator = client.get_paginator("get_images")
    list_fragments_paginator: ListFragmentsPaginator = client.get_paginator("list_fragments")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import KinesisVideoArchivedMediaClient
from .paginator import GetImagesPaginator, ListFragmentsPaginator

Client = KinesisVideoArchivedMediaClient

__all__ = (
    "Client",
    "GetImagesPaginator",
    "KinesisVideoArchivedMediaClient",
    "ListFragmentsPaginator",
)
