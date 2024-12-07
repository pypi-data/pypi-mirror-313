"""
Main interface for kinesis-video-signaling service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kinesis_video_signaling import (
        Client,
        KinesisVideoSignalingChannelsClient,
    )

    session = get_session()
    async with session.create_client("kinesis-video-signaling") as client:
        client: KinesisVideoSignalingChannelsClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import KinesisVideoSignalingChannelsClient

Client = KinesisVideoSignalingChannelsClient


__all__ = ("Client", "KinesisVideoSignalingChannelsClient")
