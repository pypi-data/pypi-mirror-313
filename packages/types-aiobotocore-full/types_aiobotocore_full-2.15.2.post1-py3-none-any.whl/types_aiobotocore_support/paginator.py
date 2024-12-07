"""
Type annotations for support service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_support.client import SupportClient
    from types_aiobotocore_support.paginator import (
        DescribeCasesPaginator,
        DescribeCommunicationsPaginator,
    )

    session = get_session()
    with session.create_client("support") as client:
        client: SupportClient

        describe_cases_paginator: DescribeCasesPaginator = client.get_paginator("describe_cases")
        describe_communications_paginator: DescribeCommunicationsPaginator = client.get_paginator("describe_communications")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeCasesRequestDescribeCasesPaginateTypeDef,
    DescribeCasesResponseTypeDef,
    DescribeCommunicationsRequestDescribeCommunicationsPaginateTypeDef,
    DescribeCommunicationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DescribeCasesPaginator", "DescribeCommunicationsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeCasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/paginator/DescribeCases.html#Support.Paginator.DescribeCases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/paginators/#describecasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeCasesRequestDescribeCasesPaginateTypeDef]
    ) -> AsyncIterator[DescribeCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/paginator/DescribeCases.html#Support.Paginator.DescribeCases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/paginators/#describecasespaginator)
        """


class DescribeCommunicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/paginator/DescribeCommunications.html#Support.Paginator.DescribeCommunications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/paginators/#describecommunicationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeCommunicationsRequestDescribeCommunicationsPaginateTypeDef]
    ) -> AsyncIterator[DescribeCommunicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/paginator/DescribeCommunications.html#Support.Paginator.DescribeCommunications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/paginators/#describecommunicationspaginator)
        """
