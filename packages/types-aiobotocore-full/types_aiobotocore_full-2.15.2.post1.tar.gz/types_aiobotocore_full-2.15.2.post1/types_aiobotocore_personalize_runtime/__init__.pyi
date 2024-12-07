"""
Main interface for personalize-runtime service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_personalize_runtime import (
        Client,
        PersonalizeRuntimeClient,
    )

    session = get_session()
    async with session.create_client("personalize-runtime") as client:
        client: PersonalizeRuntimeClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import PersonalizeRuntimeClient

Client = PersonalizeRuntimeClient

__all__ = ("Client", "PersonalizeRuntimeClient")
