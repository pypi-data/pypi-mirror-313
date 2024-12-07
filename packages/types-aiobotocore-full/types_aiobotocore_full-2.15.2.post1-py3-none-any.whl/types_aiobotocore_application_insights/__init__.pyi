"""
Main interface for application-insights service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_application_insights import (
        ApplicationInsightsClient,
        Client,
    )

    session = get_session()
    async with session.create_client("application-insights") as client:
        client: ApplicationInsightsClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ApplicationInsightsClient

Client = ApplicationInsightsClient

__all__ = ("ApplicationInsightsClient", "Client")
