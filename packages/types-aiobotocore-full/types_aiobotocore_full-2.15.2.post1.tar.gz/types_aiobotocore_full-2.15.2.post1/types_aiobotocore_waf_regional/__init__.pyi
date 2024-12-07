"""
Main interface for waf-regional service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_waf_regional import (
        Client,
        WAFRegionalClient,
    )

    session = get_session()
    async with session.create_client("waf-regional") as client:
        client: WAFRegionalClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import WAFRegionalClient

Client = WAFRegionalClient

__all__ = ("Client", "WAFRegionalClient")
