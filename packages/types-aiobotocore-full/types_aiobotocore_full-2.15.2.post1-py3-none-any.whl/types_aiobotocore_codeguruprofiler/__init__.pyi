"""
Main interface for codeguruprofiler service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codeguruprofiler import (
        Client,
        CodeGuruProfilerClient,
        ListProfileTimesPaginator,
    )

    session = get_session()
    async with session.create_client("codeguruprofiler") as client:
        client: CodeGuruProfilerClient
        ...


    list_profile_times_paginator: ListProfileTimesPaginator = client.get_paginator("list_profile_times")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CodeGuruProfilerClient
from .paginator import ListProfileTimesPaginator

Client = CodeGuruProfilerClient

__all__ = ("Client", "CodeGuruProfilerClient", "ListProfileTimesPaginator")
