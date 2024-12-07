"""
Main interface for cognito-identity service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cognito_identity import (
        Client,
        CognitoIdentityClient,
        ListIdentityPoolsPaginator,
    )

    session = get_session()
    async with session.create_client("cognito-identity") as client:
        client: CognitoIdentityClient
        ...


    list_identity_pools_paginator: ListIdentityPoolsPaginator = client.get_paginator("list_identity_pools")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CognitoIdentityClient
from .paginator import ListIdentityPoolsPaginator

Client = CognitoIdentityClient


__all__ = ("Client", "CognitoIdentityClient", "ListIdentityPoolsPaginator")
