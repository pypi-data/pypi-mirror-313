"""
Type annotations for payment-cryptography service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_payment_cryptography.client import PaymentCryptographyControlPlaneClient
    from types_aiobotocore_payment_cryptography.paginator import (
        ListAliasesPaginator,
        ListKeysPaginator,
        ListTagsForResourcePaginator,
    )

    session = get_session()
    with session.create_client("payment-cryptography") as client:
        client: PaymentCryptographyControlPlaneClient

        list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
        list_keys_paginator: ListKeysPaginator = client.get_paginator("list_keys")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAliasesInputListAliasesPaginateTypeDef,
    ListAliasesOutputTypeDef,
    ListKeysInputListKeysPaginateTypeDef,
    ListKeysOutputTypeDef,
    ListTagsForResourceInputListTagsForResourcePaginateTypeDef,
    ListTagsForResourceOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListAliasesPaginator", "ListKeysPaginator", "ListTagsForResourcePaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAliasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/paginator/ListAliases.html#PaymentCryptographyControlPlane.Paginator.ListAliases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/paginators/#listaliasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAliasesInputListAliasesPaginateTypeDef]
    ) -> AsyncIterator[ListAliasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/paginator/ListAliases.html#PaymentCryptographyControlPlane.Paginator.ListAliases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/paginators/#listaliasespaginator)
        """

class ListKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/paginator/ListKeys.html#PaymentCryptographyControlPlane.Paginator.ListKeys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/paginators/#listkeyspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListKeysInputListKeysPaginateTypeDef]
    ) -> AsyncIterator[ListKeysOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/paginator/ListKeys.html#PaymentCryptographyControlPlane.Paginator.ListKeys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/paginators/#listkeyspaginator)
        """

class ListTagsForResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/paginator/ListTagsForResource.html#PaymentCryptographyControlPlane.Paginator.ListTagsForResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/paginators/#listtagsforresourcepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceInputListTagsForResourcePaginateTypeDef]
    ) -> AsyncIterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/paginator/ListTagsForResource.html#PaymentCryptographyControlPlane.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/paginators/#listtagsforresourcepaginator)
        """
