"""
Type annotations for kms service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_kms.client import KMSClient
    from types_aiobotocore_kms.paginator import (
        DescribeCustomKeyStoresPaginator,
        ListAliasesPaginator,
        ListGrantsPaginator,
        ListKeyPoliciesPaginator,
        ListKeyRotationsPaginator,
        ListKeysPaginator,
        ListResourceTagsPaginator,
        ListRetirableGrantsPaginator,
    )

    session = get_session()
    with session.create_client("kms") as client:
        client: KMSClient

        describe_custom_key_stores_paginator: DescribeCustomKeyStoresPaginator = client.get_paginator("describe_custom_key_stores")
        list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
        list_grants_paginator: ListGrantsPaginator = client.get_paginator("list_grants")
        list_key_policies_paginator: ListKeyPoliciesPaginator = client.get_paginator("list_key_policies")
        list_key_rotations_paginator: ListKeyRotationsPaginator = client.get_paginator("list_key_rotations")
        list_keys_paginator: ListKeysPaginator = client.get_paginator("list_keys")
        list_resource_tags_paginator: ListResourceTagsPaginator = client.get_paginator("list_resource_tags")
        list_retirable_grants_paginator: ListRetirableGrantsPaginator = client.get_paginator("list_retirable_grants")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeCustomKeyStoresRequestDescribeCustomKeyStoresPaginateTypeDef,
    DescribeCustomKeyStoresResponseTypeDef,
    ListAliasesRequestListAliasesPaginateTypeDef,
    ListAliasesResponseTypeDef,
    ListGrantsRequestListGrantsPaginateTypeDef,
    ListGrantsResponseTypeDef,
    ListKeyPoliciesRequestListKeyPoliciesPaginateTypeDef,
    ListKeyPoliciesResponseTypeDef,
    ListKeyRotationsRequestListKeyRotationsPaginateTypeDef,
    ListKeyRotationsResponseTypeDef,
    ListKeysRequestListKeysPaginateTypeDef,
    ListKeysResponseTypeDef,
    ListResourceTagsRequestListResourceTagsPaginateTypeDef,
    ListResourceTagsResponseTypeDef,
    ListRetirableGrantsRequestListRetirableGrantsPaginateTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeCustomKeyStoresPaginator",
    "ListAliasesPaginator",
    "ListGrantsPaginator",
    "ListKeyPoliciesPaginator",
    "ListKeyRotationsPaginator",
    "ListKeysPaginator",
    "ListResourceTagsPaginator",
    "ListRetirableGrantsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeCustomKeyStoresPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/DescribeCustomKeyStores.html#KMS.Paginator.DescribeCustomKeyStores)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#describecustomkeystorespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeCustomKeyStoresRequestDescribeCustomKeyStoresPaginateTypeDef]
    ) -> AsyncIterator[DescribeCustomKeyStoresResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/DescribeCustomKeyStores.html#KMS.Paginator.DescribeCustomKeyStores.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#describecustomkeystorespaginator)
        """


class ListAliasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListAliases.html#KMS.Paginator.ListAliases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listaliasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAliasesRequestListAliasesPaginateTypeDef]
    ) -> AsyncIterator[ListAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListAliases.html#KMS.Paginator.ListAliases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listaliasespaginator)
        """


class ListGrantsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListGrants.html#KMS.Paginator.ListGrants)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listgrantspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGrantsRequestListGrantsPaginateTypeDef]
    ) -> AsyncIterator[ListGrantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListGrants.html#KMS.Paginator.ListGrants.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listgrantspaginator)
        """


class ListKeyPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeyPolicies.html#KMS.Paginator.ListKeyPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listkeypoliciespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListKeyPoliciesRequestListKeyPoliciesPaginateTypeDef]
    ) -> AsyncIterator[ListKeyPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeyPolicies.html#KMS.Paginator.ListKeyPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listkeypoliciespaginator)
        """


class ListKeyRotationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeyRotations.html#KMS.Paginator.ListKeyRotations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listkeyrotationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListKeyRotationsRequestListKeyRotationsPaginateTypeDef]
    ) -> AsyncIterator[ListKeyRotationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeyRotations.html#KMS.Paginator.ListKeyRotations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listkeyrotationspaginator)
        """


class ListKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeys.html#KMS.Paginator.ListKeys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listkeyspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListKeysRequestListKeysPaginateTypeDef]
    ) -> AsyncIterator[ListKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeys.html#KMS.Paginator.ListKeys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listkeyspaginator)
        """


class ListResourceTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListResourceTags.html#KMS.Paginator.ListResourceTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listresourcetagspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResourceTagsRequestListResourceTagsPaginateTypeDef]
    ) -> AsyncIterator[ListResourceTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListResourceTags.html#KMS.Paginator.ListResourceTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listresourcetagspaginator)
        """


class ListRetirableGrantsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListRetirableGrants.html#KMS.Paginator.ListRetirableGrants)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listretirablegrantspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRetirableGrantsRequestListRetirableGrantsPaginateTypeDef]
    ) -> AsyncIterator[ListGrantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListRetirableGrants.html#KMS.Paginator.ListRetirableGrants.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listretirablegrantspaginator)
        """
