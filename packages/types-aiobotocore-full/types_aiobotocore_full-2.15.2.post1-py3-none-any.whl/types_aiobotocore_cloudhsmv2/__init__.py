"""
Main interface for cloudhsmv2 service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudhsmv2 import (
        Client,
        CloudHSMV2Client,
        DescribeBackupsPaginator,
        DescribeClustersPaginator,
        ListTagsPaginator,
    )

    session = get_session()
    async with session.create_client("cloudhsmv2") as client:
        client: CloudHSMV2Client
        ...


    describe_backups_paginator: DescribeBackupsPaginator = client.get_paginator("describe_backups")
    describe_clusters_paginator: DescribeClustersPaginator = client.get_paginator("describe_clusters")
    list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CloudHSMV2Client
from .paginator import DescribeBackupsPaginator, DescribeClustersPaginator, ListTagsPaginator

Client = CloudHSMV2Client


__all__ = (
    "Client",
    "CloudHSMV2Client",
    "DescribeBackupsPaginator",
    "DescribeClustersPaginator",
    "ListTagsPaginator",
)
