"""
Main interface for datapipeline service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_datapipeline import (
        Client,
        DataPipelineClient,
        DescribeObjectsPaginator,
        ListPipelinesPaginator,
        QueryObjectsPaginator,
    )

    session = get_session()
    async with session.create_client("datapipeline") as client:
        client: DataPipelineClient
        ...


    describe_objects_paginator: DescribeObjectsPaginator = client.get_paginator("describe_objects")
    list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
    query_objects_paginator: QueryObjectsPaginator = client.get_paginator("query_objects")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import DataPipelineClient
from .paginator import DescribeObjectsPaginator, ListPipelinesPaginator, QueryObjectsPaginator

Client = DataPipelineClient


__all__ = (
    "Client",
    "DataPipelineClient",
    "DescribeObjectsPaginator",
    "ListPipelinesPaginator",
    "QueryObjectsPaginator",
)
