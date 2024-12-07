"""
Main interface for kinesis-video-media service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kinesis_video_media import (
        Client,
        KinesisVideoMediaClient,
    )

    session = get_session()
    async with session.create_client("kinesis-video-media") as client:
        client: KinesisVideoMediaClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import KinesisVideoMediaClient

Client = KinesisVideoMediaClient


__all__ = ("Client", "KinesisVideoMediaClient")
