"""
Main interface for cloudtrail-data service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudtrail_data import (
        Client,
        CloudTrailDataServiceClient,
    )

    session = get_session()
    async with session.create_client("cloudtrail-data") as client:
        client: CloudTrailDataServiceClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CloudTrailDataServiceClient

Client = CloudTrailDataServiceClient


__all__ = ("Client", "CloudTrailDataServiceClient")
