"""
Main interface for translate service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_translate import (
        Client,
        ListTerminologiesPaginator,
        TranslateClient,
    )

    session = get_session()
    async with session.create_client("translate") as client:
        client: TranslateClient
        ...


    list_terminologies_paginator: ListTerminologiesPaginator = client.get_paginator("list_terminologies")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import TranslateClient
from .paginator import ListTerminologiesPaginator

Client = TranslateClient

__all__ = ("Client", "ListTerminologiesPaginator", "TranslateClient")
