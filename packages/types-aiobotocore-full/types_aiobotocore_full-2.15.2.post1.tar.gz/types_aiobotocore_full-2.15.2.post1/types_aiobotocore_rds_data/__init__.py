"""
Main interface for rds-data service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_rds_data import (
        Client,
        RDSDataServiceClient,
    )

    session = get_session()
    async with session.create_client("rds-data") as client:
        client: RDSDataServiceClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import RDSDataServiceClient

Client = RDSDataServiceClient


__all__ = ("Client", "RDSDataServiceClient")
