"""
Main interface for serverlessrepo service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_serverlessrepo import (
        Client,
        ListApplicationDependenciesPaginator,
        ListApplicationVersionsPaginator,
        ListApplicationsPaginator,
        ServerlessApplicationRepositoryClient,
    )

    session = get_session()
    async with session.create_client("serverlessrepo") as client:
        client: ServerlessApplicationRepositoryClient
        ...


    list_application_dependencies_paginator: ListApplicationDependenciesPaginator = client.get_paginator("list_application_dependencies")
    list_application_versions_paginator: ListApplicationVersionsPaginator = client.get_paginator("list_application_versions")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ServerlessApplicationRepositoryClient
from .paginator import (
    ListApplicationDependenciesPaginator,
    ListApplicationsPaginator,
    ListApplicationVersionsPaginator,
)

Client = ServerlessApplicationRepositoryClient


__all__ = (
    "Client",
    "ListApplicationDependenciesPaginator",
    "ListApplicationVersionsPaginator",
    "ListApplicationsPaginator",
    "ServerlessApplicationRepositoryClient",
)
