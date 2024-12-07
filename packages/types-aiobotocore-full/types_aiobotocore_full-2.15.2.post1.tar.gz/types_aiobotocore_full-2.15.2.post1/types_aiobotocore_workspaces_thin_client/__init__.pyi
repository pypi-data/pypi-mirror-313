"""
Main interface for workspaces-thin-client service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_workspaces_thin_client import (
        Client,
        ListDevicesPaginator,
        ListEnvironmentsPaginator,
        ListSoftwareSetsPaginator,
        WorkSpacesThinClientClient,
    )

    session = get_session()
    async with session.create_client("workspaces-thin-client") as client:
        client: WorkSpacesThinClientClient
        ...


    list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    list_software_sets_paginator: ListSoftwareSetsPaginator = client.get_paginator("list_software_sets")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import WorkSpacesThinClientClient
from .paginator import ListDevicesPaginator, ListEnvironmentsPaginator, ListSoftwareSetsPaginator

Client = WorkSpacesThinClientClient

__all__ = (
    "Client",
    "ListDevicesPaginator",
    "ListEnvironmentsPaginator",
    "ListSoftwareSetsPaginator",
    "WorkSpacesThinClientClient",
)
