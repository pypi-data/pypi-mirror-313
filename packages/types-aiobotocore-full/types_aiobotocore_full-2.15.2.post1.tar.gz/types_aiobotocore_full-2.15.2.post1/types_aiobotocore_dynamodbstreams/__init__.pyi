"""
Main interface for dynamodbstreams service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_dynamodbstreams import (
        Client,
        DynamoDBStreamsClient,
    )

    session = get_session()
    async with session.create_client("dynamodbstreams") as client:
        client: DynamoDBStreamsClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import DynamoDBStreamsClient

Client = DynamoDBStreamsClient

__all__ = ("Client", "DynamoDBStreamsClient")
