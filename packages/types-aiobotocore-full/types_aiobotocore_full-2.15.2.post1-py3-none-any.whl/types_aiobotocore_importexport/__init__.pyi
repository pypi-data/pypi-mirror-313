"""
Main interface for importexport service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_importexport import (
        Client,
        ImportExportClient,
        ListJobsPaginator,
    )

    session = get_session()
    async with session.create_client("importexport") as client:
        client: ImportExportClient
        ...


    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ImportExportClient
from .paginator import ListJobsPaginator

Client = ImportExportClient

__all__ = ("Client", "ImportExportClient", "ListJobsPaginator")
