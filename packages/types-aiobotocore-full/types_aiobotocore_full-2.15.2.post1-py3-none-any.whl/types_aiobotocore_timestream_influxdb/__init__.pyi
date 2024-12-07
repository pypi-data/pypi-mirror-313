"""
Main interface for timestream-influxdb service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_timestream_influxdb import (
        Client,
        ListDbInstancesPaginator,
        ListDbParameterGroupsPaginator,
        TimestreamInfluxDBClient,
    )

    session = get_session()
    async with session.create_client("timestream-influxdb") as client:
        client: TimestreamInfluxDBClient
        ...


    list_db_instances_paginator: ListDbInstancesPaginator = client.get_paginator("list_db_instances")
    list_db_parameter_groups_paginator: ListDbParameterGroupsPaginator = client.get_paginator("list_db_parameter_groups")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import TimestreamInfluxDBClient
from .paginator import ListDbInstancesPaginator, ListDbParameterGroupsPaginator

Client = TimestreamInfluxDBClient

__all__ = (
    "Client",
    "ListDbInstancesPaginator",
    "ListDbParameterGroupsPaginator",
    "TimestreamInfluxDBClient",
)
