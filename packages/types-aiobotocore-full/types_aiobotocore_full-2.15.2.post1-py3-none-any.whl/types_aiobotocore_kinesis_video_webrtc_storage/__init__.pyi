"""
Main interface for kinesis-video-webrtc-storage service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kinesis_video_webrtc_storage import (
        Client,
        KinesisVideoWebRTCStorageClient,
    )

    session = get_session()
    async with session.create_client("kinesis-video-webrtc-storage") as client:
        client: KinesisVideoWebRTCStorageClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import KinesisVideoWebRTCStorageClient

Client = KinesisVideoWebRTCStorageClient

__all__ = ("Client", "KinesisVideoWebRTCStorageClient")
