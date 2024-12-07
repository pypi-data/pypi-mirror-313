"""
Main interface for cloudsearchdomain service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudsearchdomain import (
        Client,
        CloudSearchDomainClient,
    )

    session = get_session()
    async with session.create_client("cloudsearchdomain") as client:
        client: CloudSearchDomainClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CloudSearchDomainClient

Client = CloudSearchDomainClient

__all__ = ("Client", "CloudSearchDomainClient")
