"""
Type annotations for cognito-identity service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cognito_identity.client import CognitoIdentityClient
    from types_aiobotocore_cognito_identity.paginator import (
        ListIdentityPoolsPaginator,
    )

    session = get_session()
    with session.create_client("cognito-identity") as client:
        client: CognitoIdentityClient

        list_identity_pools_paginator: ListIdentityPoolsPaginator = client.get_paginator("list_identity_pools")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListIdentityPoolsInputListIdentityPoolsPaginateTypeDef,
    ListIdentityPoolsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListIdentityPoolsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListIdentityPoolsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/paginator/ListIdentityPools.html#CognitoIdentity.Paginator.ListIdentityPools)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/paginators/#listidentitypoolspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIdentityPoolsInputListIdentityPoolsPaginateTypeDef]
    ) -> AsyncIterator[ListIdentityPoolsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/paginator/ListIdentityPools.html#CognitoIdentity.Paginator.ListIdentityPools.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/paginators/#listidentitypoolspaginator)
        """
