"""
Main interface for mq service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mq import (
        Client,
        ListBrokersPaginator,
        MQClient,
    )

    session = get_session()
    async with session.create_client("mq") as client:
        client: MQClient
        ...


    list_brokers_paginator: ListBrokersPaginator = client.get_paginator("list_brokers")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import MQClient
from .paginator import ListBrokersPaginator

Client = MQClient

__all__ = ("Client", "ListBrokersPaginator", "MQClient")
