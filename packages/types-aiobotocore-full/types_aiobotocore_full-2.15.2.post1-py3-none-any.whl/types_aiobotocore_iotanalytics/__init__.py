"""
Main interface for iotanalytics service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iotanalytics import (
        Client,
        IoTAnalyticsClient,
        ListChannelsPaginator,
        ListDatasetContentsPaginator,
        ListDatasetsPaginator,
        ListDatastoresPaginator,
        ListPipelinesPaginator,
    )

    session = get_session()
    async with session.create_client("iotanalytics") as client:
        client: IoTAnalyticsClient
        ...


    list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
    list_dataset_contents_paginator: ListDatasetContentsPaginator = client.get_paginator("list_dataset_contents")
    list_datasets_paginator: ListDatasetsPaginator = client.get_paginator("list_datasets")
    list_datastores_paginator: ListDatastoresPaginator = client.get_paginator("list_datastores")
    list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import IoTAnalyticsClient
from .paginator import (
    ListChannelsPaginator,
    ListDatasetContentsPaginator,
    ListDatasetsPaginator,
    ListDatastoresPaginator,
    ListPipelinesPaginator,
)

Client = IoTAnalyticsClient


__all__ = (
    "Client",
    "IoTAnalyticsClient",
    "ListChannelsPaginator",
    "ListDatasetContentsPaginator",
    "ListDatasetsPaginator",
    "ListDatastoresPaginator",
    "ListPipelinesPaginator",
)
