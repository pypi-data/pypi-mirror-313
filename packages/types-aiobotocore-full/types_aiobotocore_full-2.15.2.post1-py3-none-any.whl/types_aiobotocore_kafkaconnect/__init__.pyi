"""
Main interface for kafkaconnect service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kafkaconnect import (
        Client,
        KafkaConnectClient,
        ListConnectorsPaginator,
        ListCustomPluginsPaginator,
        ListWorkerConfigurationsPaginator,
    )

    session = get_session()
    async with session.create_client("kafkaconnect") as client:
        client: KafkaConnectClient
        ...


    list_connectors_paginator: ListConnectorsPaginator = client.get_paginator("list_connectors")
    list_custom_plugins_paginator: ListCustomPluginsPaginator = client.get_paginator("list_custom_plugins")
    list_worker_configurations_paginator: ListWorkerConfigurationsPaginator = client.get_paginator("list_worker_configurations")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import KafkaConnectClient
from .paginator import (
    ListConnectorsPaginator,
    ListCustomPluginsPaginator,
    ListWorkerConfigurationsPaginator,
)

Client = KafkaConnectClient

__all__ = (
    "Client",
    "KafkaConnectClient",
    "ListConnectorsPaginator",
    "ListCustomPluginsPaginator",
    "ListWorkerConfigurationsPaginator",
)
