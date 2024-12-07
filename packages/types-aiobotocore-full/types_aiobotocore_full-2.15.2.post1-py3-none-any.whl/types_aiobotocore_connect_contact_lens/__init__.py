"""
Main interface for connect-contact-lens service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_connect_contact_lens import (
        Client,
        ConnectContactLensClient,
    )

    session = get_session()
    async with session.create_client("connect-contact-lens") as client:
        client: ConnectContactLensClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ConnectContactLensClient

Client = ConnectContactLensClient


__all__ = ("Client", "ConnectContactLensClient")
