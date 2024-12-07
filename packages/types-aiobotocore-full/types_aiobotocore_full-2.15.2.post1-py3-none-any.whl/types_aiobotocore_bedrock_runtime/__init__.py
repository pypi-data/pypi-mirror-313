"""
Main interface for bedrock-runtime service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_bedrock_runtime import (
        BedrockRuntimeClient,
        Client,
    )

    session = get_session()
    async with session.create_client("bedrock-runtime") as client:
        client: BedrockRuntimeClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import BedrockRuntimeClient

Client = BedrockRuntimeClient


__all__ = ("BedrockRuntimeClient", "Client")
