"""
Type annotations for b2bi service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_b2bi.client import B2BIClient
    from types_aiobotocore_b2bi.paginator import (
        ListCapabilitiesPaginator,
        ListPartnershipsPaginator,
        ListProfilesPaginator,
        ListTransformersPaginator,
    )

    session = get_session()
    with session.create_client("b2bi") as client:
        client: B2BIClient

        list_capabilities_paginator: ListCapabilitiesPaginator = client.get_paginator("list_capabilities")
        list_partnerships_paginator: ListPartnershipsPaginator = client.get_paginator("list_partnerships")
        list_profiles_paginator: ListProfilesPaginator = client.get_paginator("list_profiles")
        list_transformers_paginator: ListTransformersPaginator = client.get_paginator("list_transformers")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListCapabilitiesRequestListCapabilitiesPaginateTypeDef,
    ListCapabilitiesResponseTypeDef,
    ListPartnershipsRequestListPartnershipsPaginateTypeDef,
    ListPartnershipsResponseTypeDef,
    ListProfilesRequestListProfilesPaginateTypeDef,
    ListProfilesResponseTypeDef,
    ListTransformersRequestListTransformersPaginateTypeDef,
    ListTransformersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListCapabilitiesPaginator",
    "ListPartnershipsPaginator",
    "ListProfilesPaginator",
    "ListTransformersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListCapabilitiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListCapabilities.html#B2BI.Paginator.ListCapabilities)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/#listcapabilitiespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCapabilitiesRequestListCapabilitiesPaginateTypeDef]
    ) -> AsyncIterator[ListCapabilitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListCapabilities.html#B2BI.Paginator.ListCapabilities.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/#listcapabilitiespaginator)
        """

class ListPartnershipsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListPartnerships.html#B2BI.Paginator.ListPartnerships)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/#listpartnershipspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPartnershipsRequestListPartnershipsPaginateTypeDef]
    ) -> AsyncIterator[ListPartnershipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListPartnerships.html#B2BI.Paginator.ListPartnerships.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/#listpartnershipspaginator)
        """

class ListProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListProfiles.html#B2BI.Paginator.ListProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/#listprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProfilesRequestListProfilesPaginateTypeDef]
    ) -> AsyncIterator[ListProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListProfiles.html#B2BI.Paginator.ListProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/#listprofilespaginator)
        """

class ListTransformersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListTransformers.html#B2BI.Paginator.ListTransformers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/#listtransformerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTransformersRequestListTransformersPaginateTypeDef]
    ) -> AsyncIterator[ListTransformersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListTransformers.html#B2BI.Paginator.ListTransformers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/#listtransformerspaginator)
        """
